import glob
import itertools
import os
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from powertrain_model import MOTORS, prop, motor_state, G, STAND

MOT = MOTORS["MN3110 KV700"]


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


def errors(pts, pname, f, b):
    pr = prop(pname)
    et, er = [], []
    for _, r in pts.iterrows():
        def fi(duty):
            st = motor_state(pr, pname, MOT, 0.0, duty, r.v, f, b)
            return -1e3 if st is None else st["i_bus"] - r.i
        try:
            duty = brentq(fi, 0.15, 1.0, xtol=1e-4)
        except ValueError:
            et.append(0.5); er.append(0.5); continue
        st = motor_state(pr, pname, MOT, 0.0, duty, r.v, f, b)
        et.append(st["thrust"] / G / r.thr - 1.0)
        er.append(st["rpm"] / r.rpm - 1.0)
    return np.array(et), np.array(er)


p126, p117 = points("MN3110_12_6"), points("MN3110_11_7")
print("12x6 points:", len(p126), " 11x7 points:", len(p117))
print(p126.round(1).to_string(index=False))
print("\nnominal f=1.0, b=0.06: mean thrust error / mean rpm error (model vs stand, rpm = stand's 'Motor Electrical Speed' column)")
for name, pts in (("PER3_12x6E", p126), ("PER3_12x6", p126), ("PER3_12x6SF", p126), ("PER3_11x7E", p117), ("PER3_11x7", p117), ("PER3_11x7SF", p117)):
    et, er = errors(pts, name, 1.0, 0.06)
    print(f"  {name:12s} thrust {et.mean()*100:6.1f}% (rms {np.sqrt((et**2).mean())*100:4.1f}%)   rpm {er.mean()*100:6.1f}% (rms {np.sqrt((er**2).mean())*100:4.1f}%)")

print("\nbest (f, b) per variant on thrust and rpm together")
for name, pts in (("PER3_12x6E", p126), ("PER3_12x6", p126), ("PER3_12x6SF", p126), ("PER3_11x7E", p117), ("PER3_11x7", p117), ("PER3_11x7SF", p117)):
    best = None
    for f, b in itertools.product((0.80, 0.85, 0.90, 0.95, 1.00, 1.05), (0.0, 0.03, 0.06, 0.09, 0.12, 0.15)):
        et, er = errors(pts, name, f, b)
        rms = float(np.sqrt(np.mean(np.concatenate([et, er]) ** 2)))
        if best is None or rms < best[0]:
            best = (rms, f, b, et.mean(), er.mean())
    print(f"  {name:12s} rms {best[0]*100:5.1f}%  f={best[1]:.2f} b={best[2]:.2f}  thrust mean {best[3]*100:5.1f}%  rpm mean {best[4]*100:5.1f}%")
