"""Steady-state powertrain and performance model for the Believer: battery -> ESC -> motor -> propeller -> airframe.

Propeller: APC PER3 performance tables (Ct, Cp against J and rpm).
Motor: KV, winding resistance, idle current (datasheet or listing values, with an effective-KV factor f and an extra series
resistance b calibrated on the RCbenchmark stand data).
ESC: buck converter, duty = throttle fraction, efficiency ETA.
Battery: open-circuit voltage with a series resistance.
Airframe: parabolic drag polar from Weishaeupl et al. 2024 (wind tunnel).
"""
import glob
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from apcprop import Prop, D as D12   # noqa: F401  (D is 12 inch for both 12x6 and, per file, overridden below)

S_DIR = os.path.dirname(os.path.abspath(__file__))
RHO = 1.19            # Brisbane, about 25 C
G = 9.81
ETA_ESC = 0.98
RFAC = 1.15           # copper resistance rise over the datasheet value at operating temperature

# propeller calibration factors applied to the APC tables (thrust and power coefficients), set with set_prop_scale()
CT_SCALE, CP_SCALE = 1.0, 1.0


def set_prop_scale(ct=1.0, cp=1.0):
    global CT_SCALE, CP_SCALE
    CT_SCALE, CP_SCALE = ct, cp


# airframe (Weishaeupl et al. 2024, Tables 1 and 2)
S_WING, CD0, K_IND = 0.488, 0.0503, 0.0764


@dataclass
class Motor:
    name: str
    kv: float
    r: float
    i0: float
    rating_a: float
    mass_g: float


MOTORS = {
    "MN3110 KV700": Motor("MN3110 KV700", 700, 0.092, 0.3, 21, 80),
    "U5 KV400": Motor("U5 KV400", 400, 0.116, 0.3, 30, 156),
    "KDE3510XF-475": Motor("KDE3510XF-475", 475, 0.105, 0.5, 30, 120),
    "MN3510 KV700": Motor("MN3510 KV700", 700, 0.050, 0.5, 25, 97),
    "SunnySky X2814 KV900": Motor("SunnySky X2814 KV900", 900, 0.0336, 1.0, 50, 108),
}

PROPS = {}


def prop(name):
    if name not in PROPS:
        PROPS[name] = Prop(os.path.join(S_DIR, name + ".dat"))
    return PROPS[name]


def diameter(name):
    return 12 * 0.0254 if "12x" in name else 11 * 0.0254


def motor_state(pr, pname, mot, v_air, duty, vbat, f, b, ct=None, cp=None):
    """Steady state of one motor+ESC+prop at airspeed v_air (m/s), throttle duty and battery voltage vbat."""
    d = diameter(pname)
    reff = mot.r * RFAC + b
    kv = mot.kv * f
    kt = 9.549 / kv
    vm = duty * vbat
    if vm <= 0.05:
        return None
    ct_s = CT_SCALE if ct is None else ct
    cp_s = CP_SCALE if cp is None else cp

    def resid(rpm):
        e = rpm / kv
        iw = (vm - e) / reff
        qm = (iw - mot.i0) * kt
        n = rpm / 60.0
        j = v_air / (n * d)
        ct, cp = pr.coeffs(rpm, j)
        qp = cp_s * cp * RHO * n ** 2 * d ** 5 / (2 * np.pi)
        return qm - qp

    hi = vm * kv - 1.0
    if hi <= 400 or resid(400.0) < 0:
        return None
    if resid(hi) > 0:
        rpm = hi
    else:
        rpm = brentq(resid, 400.0, hi, xtol=0.5)
    n = rpm / 60.0
    j = v_air / (n * d)
    ct, cp = pr.coeffs(rpm, j)
    thrust = ct_s * ct * RHO * n ** 2 * d ** 4
    p_shaft = cp_s * cp * RHO * n ** 3 * d ** 5
    iw = (vm - rpm / kv) / reff
    i_bus = duty * iw / ETA_ESC
    return dict(rpm=rpm, thrust=thrust, p_shaft=p_shaft, iw=iw, i_bus=i_bus, p_bus=vbat * i_bus, vm=vm, j=j,
                eta_prop=(thrust * v_air / p_shaft if p_shaft > 1 else 0.0))


def solve_aircraft(pr, pname, mot, v_air, duty, voc, r_pack, f, b, n_motors=2, ct=None, cp=None):
    """Battery sag closes the loop: vbat = voc - r_pack * total bus current."""
    vbat = voc
    st = None
    for _ in range(25):
        st = motor_state(pr, pname, mot, v_air, duty, vbat, f, b, ct=ct, cp=cp)
        if st is None:
            return None
        new = voc - r_pack * n_motors * st["i_bus"]
        if abs(new - vbat) < 1e-3:
            break
        vbat = 0.5 * vbat + 0.5 * new
    st["vbat"] = vbat
    return st


def drag(mass, v):
    w = mass * G
    q = 0.5 * RHO * v * v
    cl = w / (q * S_WING)
    return q * S_WING * (CD0 + K_IND * cl * cl)


# ------------------------------------------------------------------ calibration on the RCbenchmark stand data
STAND = os.environ.get("BELIEVER_STAND_DIR", r"C:\Users\Metabox\OneDrive\University\MATLAB\QUTAS\Believer\Motor Testing")


def stand_points(folder, lo=1400, hi=1780, minrows=15):
    fr = []
    for fpath in sorted(glob.glob(os.path.join(STAND, folder, "*.csv"))):
        if "combined" in fpath:
            continue
        d = pd.read_csv(fpath, encoding="utf-8-sig", on_bad_lines="skip")
        fr.append(pd.DataFrame({"esc": d.iloc[:, 1], "thr": d.iloc[:, 5], "v": d.iloc[:, 6], "i": d.iloc[:, 7]}))
    d = pd.concat(fr).dropna()
    d = d[(d.esc >= lo) & (d.esc <= hi) & (d.i > 3)]
    d["bin"] = (d.esc // 20) * 20
    g = d.groupby("bin").agg(thr=("thr", "mean"), i=("i", "mean"), v=("v", "mean"), n=("i", "size")).reset_index()
    return g[g.n >= minrows]


def stand_error(points, pname, f, b, mot=MOTORS["MN3110 KV700"]):
    pr = prop(pname)
    errs = []
    for _, r in points.iterrows():
        target = r.i

        def fi(duty):
            st = motor_state(pr, pname, mot, 0.0, duty, r.v, f, b)
            return -1e3 if st is None else st["i_bus"] - target

        try:
            duty = brentq(fi, 0.15, 1.0, xtol=1e-4)
        except ValueError:
            errs.append(0.5)
            continue
        st = motor_state(pr, pname, mot, 0.0, duty, r.v, f, b)
        errs.append(st["thrust"] / G / r.thr - 1.0)
    return np.array(errs)
