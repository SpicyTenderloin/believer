import numpy as np
from scipy.optimize import brentq, minimize_scalar
import powertrain_model as pm
from powertrain_model import MOTORS, prop, G, RHO, diameter
import glob
import os
import pandas as pd


def points(folder, lo=1520, hi=1790, minrows=25):
    fr = []
    for fpath in sorted(glob.glob(os.path.join(STAND, folder, "*.csv"))):
        if "combined" in fpath:
            continue
        d = pd.read_csv(fpath, encoding="utf-8-sig", on_bad_lines="skip")
        fr.append(pd.DataFrame({"esc": d.iloc[:, 1], "thr": d.iloc[:, 5], "v": d.iloc[:, 6], "i": d.iloc[:, 7], "rpm": d.iloc[:, 8]}))
    d = pd.concat(fr)
    d = d[(d.esc >= lo) & (d.esc <= hi) & (d.i > 3) & (d.rpm > 5000) & (d.rpm < 10500)].dropna(subset=["thr", "rpm"])
    d["bin"] = (d.esc // 20) * 20
    g = d.groupby("bin").agg(thr=("thr", "mean"), i=("i", "mean"), v=("v", "mean"), rpm=("rpm", "median"), n=("i", "size")).reset_index()
    return g[g.n >= minrows]


MOT = MOTORS["MN3110 KV700"]
PN = "PER3_12x6E"
pr = prop(PN)
D = diameter(PN)
pts = points("MN3110_12_6", lo=1560, hi=1700)
print(pts.round(2).to_string(index=False))

# thrust scale: measured thrust against the table's static thrust at the measured rotor speed
ct_i = []
for _, r in pts.iterrows():
    n = r.rpm / 60
    ct_tab, _ = pr.coeffs(r.rpm, 0.0)
    ct_i.append(r.thr * G / (ct_tab * RHO * n * n * D ** 4))
ct_i = np.array(ct_i)
print("thrust scale per point:", ct_i.round(3), " mean %.3f" % ct_i.mean())
CT = float(ct_i.mean())


def bus_current(r, cp_scale, f, b):
    n = r.rpm / 60
    _, cp_tab = pr.coeffs(r.rpm, 0.0)
    q = cp_scale * cp_tab * RHO * n * n * D ** 5 / (2 * np.pi)
    kv = MOT.kv * f
    iw = q * kv / 9.549 + MOT.i0
    vm = r.rpm / kv + iw * (MOT.r * pm.RFAC + b)
    duty = vm / r.v
    return duty * iw / pm.ETA_ESC, iw, duty


for f in (0.90, 1.00, 1.05):
    for b in (0.03, 0.06, 0.09):
        def loss(cps):
            return sum((bus_current(r, cps, f, b)[0] / r.i - 1) ** 2 for _, r in pts.iterrows())
        res = minimize_scalar(loss, bounds=(0.6, 2.5), method="bounded")
        cps = res.x
        err = [bus_current(r, cps, f, b)[0] / r.i - 1 for _, r in pts.iterrows()]
        iw = [bus_current(r, cps, f, b)[1] for _, r in pts.iterrows()]
        print(f"f={f:.2f} b={b:.2f}: power scale {cps:.2f}; bus current error rms {np.sqrt(np.mean(np.square(err)))*100:.1f}%; winding at last point {iw[-1]:.1f} A")
