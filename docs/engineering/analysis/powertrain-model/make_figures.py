import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from powertrain_model import MOTORS, prop, solve_aircraft, drag, G, set_prop_scale

S = os.path.dirname(os.path.abspath(__file__))
PNAME, VOC, F, B, R_PACK = "PER3_12x6E", 24.0, 1.0, 0.06, 0.021
set_prop_scale(0.99, 1.22)      # default: MN3110 12x6E calibration (calibrate_12x6e.py)
PROP_SCALE = {"U5 KV400": (0.98, 1.01)}   # motor-specific calibration where directly measured (calibrate_u5.py, 2026-09-30)
AVIONICS_W = 12.0
pr = prop(PNAME)

# reference palette, light mode, slots 1-3 in order (blue, orange, aqua); chrome from the palette's ink and surface roles
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SERIES = {"MN3110 KV700": "#2a78d6", "U5 KV400": "#eb6834", "KDE3510XF-475": "#1baf7a"}
MASS = {"MN3110 KV700": 3.80, "U5 KV400": 3.95, "KDE3510XF-475": 3.88}      # maiden mass with that motor pair fitted


def run(mot, v, duty, name=None):
    ct, cp = PROP_SCALE.get(name, (None, None))
    return solve_aircraft(pr, PNAME, mot, v, duty, VOC, R_PACK, F, B, ct=ct, cp=cp)


def duty_at_rating(mot, v, name=None):
    st = run(mot, v, 1.0, name)
    if st["iw"] <= mot.rating_a:
        return 1.0
    return brentq(lambda d: run(mot, v, d, name)["iw"] - mot.rating_a, 0.15, 1.0, xtol=1e-4)


plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Segoe UI", "DejaVu Sans"], "font.size": 9.5,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7, "axes.axisbelow": True,
})
fig, ax = plt.subplots(1, 3, figsize=(16, 5.0))

# ---------------------------------------------------------------- A: sustainable thrust in flight against drag
a = ax[0]
speeds = np.arange(0, 28.1, 1.0)
for name, col in SERIES.items():
    mot = MOTORS[name]
    thr = []
    for v in speeds:
        d = duty_at_rating(mot, v, name)
        thr.append(2 * run(mot, v, d, name)["thrust"] / G)
    a.plot(speeds, thr, color=col, lw=2.0, label=name)
    a.text(speeds[-1] + 0.3, thr[-1], name.split()[0], color=INK2, va="center", fontsize=8.5)
vd = np.arange(9.5, 28.1, 0.5)
a.plot(vd, [drag(3.8, v) / G for v in vd], color=INK2, lw=1.6, label="Level-flight drag, 3.8 kg")
a.plot(vd, [drag(4.3, v) / G for v in vd], color=INK2, lw=1.6, ls=(0, (4, 3)), label="Level-flight drag, 4.3 kg")
a.axvline(9.4, color=MUTED, lw=0.9, ls=":")
a.text(9.6, 4.62, "stall about 9.4 m/s\n(3.8 kg, estimate)", color=MUTED, fontsize=8, va="top")
a.set_xlim(0, 31); a.set_ylim(0, 4.8)
a.set_xlabel("Airspeed (m/s)"); a.set_ylabel("Total thrust, two motors (kgf)")
a.set_title("Thrust each drive can sustain (winding current at or under its rating)\nagainst the drag it has to overcome", loc="left", fontsize=10, color=INK)
a.legend(loc="upper right", frameon=False, fontsize=8.5)

# ---------------------------------------------------------------- B: level-flight electrical power against airspeed
b = ax[1]
vs = np.arange(10, 24.1, 0.5)
for name, col in SERIES.items():
    mot = MOTORS[name]
    m = MASS[name]
    p = []
    for v in vs:
        dr = drag(m, v)
        if 2 * run(mot, v, 1.0, name)["thrust"] < dr:
            p.append(np.nan); continue
        d = brentq(lambda x: 2 * run(mot, v, x, name)["thrust"] - dr, 0.15, 1.0, xtol=1e-4)
        p.append(2 * run(mot, v, d, name)["p_bus"] + AVIONICS_W)
    b.plot(vs, p, color=col, lw=2.0, label=name)
    b.text(vs[-1] + 0.25, p[-1], name.split()[0], color=INK2, va="center", fontsize=8.5)
    for v0 in (15, 20):
        i = int(np.argmin(np.abs(vs - v0)))
        b.plot(vs[i], p[i], "o", ms=5, color=col, mec=SURFACE, mew=1.5)
b.axvline(13.5, color=MUTED, lw=0.9, ls=":")
b.text(13.65, 100, "best range 13.5 m/s", color=MUTED, fontsize=8, va="bottom")
b.set_xlim(10, 26.8); b.set_ylim(90, 480)
b.set_xlabel("Airspeed (m/s)"); b.set_ylabel("Electrical power from the pack (W)")
b.set_title("Level-flight power, whole aircraft\n(includes 12 W avionics; dots mark 15 and 20 m/s)", loc="left", fontsize=10, color=INK)
b.legend(loc="upper left", frameon=False, fontsize=8.5)

# ---------------------------------------------------------------- C: static thrust per motor against winding current
c = ax[2]
for name, col in SERIES.items():
    mot = MOTORS[name]
    duties = np.linspace(0.2, 1.0, 60)
    xs, ys = [], []
    for d in duties:
        st = run(mot, 0.0, d, name)
        if st is None:
            continue
        xs.append(st["iw"]); ys.append(st["thrust"] / G)
    xs, ys = np.array(xs), np.array(ys)
    keep = xs <= 33.0                       # the model is calibrated on the stand data up to about 33 A winding
    xs, ys = xs[keep], ys[keep]
    over = xs > mot.rating_a
    solid = ~over | (np.arange(len(xs)) == (np.argmax(over) if over.any() else -1))
    c.plot(xs[solid], ys[solid], color=col, lw=2.0, label=name)
    if over.any():
        k = np.argmax(over)
        c.plot(xs[k - 1:], ys[k - 1:], color=col, lw=1.6, ls=(0, (2, 2)))
        c.plot(mot.rating_a, np.interp(mot.rating_a, xs, ys), "o", ms=6, color=col, mec=SURFACE, mew=1.5)
    else:
        c.plot(xs[-1], ys[-1], "o", ms=6, color=col, mec=SURFACE, mew=1.5)
c.axhline(1.6, color=INK2, lw=1.2, ls=(0, (4, 3)), label="0.8 thrust-to-weight at about 4.0 kg\n(1.6 kgf per motor)")
c.set_xlim(0, 36); c.set_ylim(0, 2.6)
c.set_xlabel("Winding current = ESC output current (A)"); c.set_ylabel("Static thrust per motor (kgf)")
c.set_title("Static thrust against winding current\n(dot = rated current or full throttle; dashed = beyond rating)", loc="left", fontsize=10, color=INK)
c.legend(loc="lower right", frameon=False, fontsize=8.5)

fig.text(0.5, 0.008, "Model: APC 12x6E tables, thrust/power factors calibrated on the RCbenchmark stand data per motor where measured (U5: x0.98/x1.01, 2026-09-30; others: x0.99/x1.22, 2026-09-15), 6S pack at 24.0 V with 21 mOhm, datasheet KV and resistance plus extra ohms, "
         "Weishaeupl et al. drag polar. Unverified beyond the calibrated range (about 29 A winding); no flight or in-aircraft measurement yet.",
         ha="center", fontsize=8, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1))
out = os.path.join(S, "powertrain-model-figure.png")
fig.savefig(out, dpi=150)
print("saved", out)
