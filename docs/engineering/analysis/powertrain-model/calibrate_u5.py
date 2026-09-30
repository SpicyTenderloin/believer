"""Calibrate the propeller thrust/power scale factors for the U5 KV400 + 12x6E combination
from the 2026-09-30 RCbenchmark stand data (BELIEVER_STAND_DIR/../u5_12_6, or set U5_STAND_DIR).

Also cross-checks the stand's Motor Electrical Speed column against the rotor speed implied
by the measured thrust and the propeller's static thrust coefficient (as done for the MN3110
in calibrate_rpm.py) - above about 1560 us the column reads usable rotor speed."""
import glob
import os
import numpy as np
import pandas as pd
from scipy.optimize import brentq, minimize_scalar
import powertrain_model as pm
from powertrain_model import MOTORS, prop, G, RHO, diameter

U5_DIR = os.environ.get("U5_STAND_DIR", r"E:\u5_12_6")
PN = "PER3_12x6E"
pr = prop(PN)
D = diameter(PN)
MOT = MOTORS["U5 KV400"]
COLS = ["t", "esc", "s1", "s2", "s3", "thr", "v", "i", "erpm", "orpm", "p", "eff", "lc", "bc",
        "p1", "p2", "p3", "p4", "d0", "d1", "d2", "d3", "msg", "u"]


def load_points(lo=1560, hi=2000, minrows=10):
    frames = []
    for f in sorted(glob.glob(os.path.join(U5_DIR, "*.csv"))):
        d = pd.read_csv(f, encoding="utf-8-sig", on_bad_lines="skip")
        d.columns = COLS[:len(d.columns)]
        frames.append(d)
    d = pd.concat(frames).dropna(subset=["thr"])
    d = d[(d.esc >= lo) & (d.esc <= hi) & (d.i > 2)]
    d["bin"] = (d.esc // 40) * 40
    g = d.groupby("bin").agg(thr=("thr", "mean"), i=("i", "mean"), v=("v", "mean"), rpm=("erpm", "mean"), n=("thr", "size")).reset_index()
    return g[g.n >= minrows]


def rpm_from_thrust(thrust_kgf, ct_scale=0.99):
    def f(rpm):
        n = rpm / 60
        ct, _ = pr.coeffs(rpm, 0.0)
        return ct_scale * ct * RHO * n * n * D ** 4 / G - thrust_kgf
    return brentq(f, 1500, 14900)


def bus_current(r, cp_scale, f, b):
    n = r.rpm / 60
    _, cp_tab = pr.coeffs(r.rpm, 0.0)
    q = cp_scale * cp_tab * RHO * n * n * D ** 5 / (2 * np.pi)
    kv = MOT.kv * f
    iw = q * kv / 9.549 + MOT.i0
    vm = r.rpm / kv + iw * (MOT.r * pm.RFAC + b)
    duty = vm / r.v
    return duty * iw / pm.ETA_ESC, iw, duty


if __name__ == "__main__":
    g = load_points()
    print(g.round(2).to_string(index=False))

    g["rpm_thr"] = [rpm_from_thrust(t) for t in g.thr]
    g["ratio"] = g.rpm / g.rpm_thr
    print("\nrotor-speed cross-check (stand column / thrust-implied):")
    print(g[["bin", "rpm", "rpm_thr", "ratio"]].round(3).to_string(index=False))
    print(f"mean ratio {g.ratio.mean():.3f}, sd {g.ratio.std():.3f}")

    ct_i = []
    for _, r in g.iterrows():
        n = r.rpm / 60
        ct_tab, _ = pr.coeffs(r.rpm, 0.0)
        ct_i.append(r.thr * G / (ct_tab * RHO * n * n * D ** 4))
    CT = float(np.mean(ct_i))
    print(f"\nthrust scale per point: {np.round(ct_i, 3)}, mean {CT:.3f}")

    f, b = 1.0, 0.06
    res = minimize_scalar(lambda cps: sum((bus_current(r, cps, f, b)[0] / r.i - 1) ** 2 for _, r in g.iterrows()),
                           bounds=(0.3, 2.5), method="bounded")
    CP = res.x
    err = [bus_current(r, CP, f, b)[0] / r.i - 1 for _, r in g.iterrows()]
    print(f"power scale (f={f}, b={b}): {CP:.3f}; bus current rms error {np.sqrt(np.mean(np.square(err))) * 100:.1f}%")
    print(f"winding current at full throttle (last bin): {bus_current(g.iloc[-1], CP, f, b)[1]:.1f} A")
