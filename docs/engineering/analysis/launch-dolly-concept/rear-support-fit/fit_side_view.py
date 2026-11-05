"""Rest the manufacturer side view on Julian's dolly side view (Fusion screenshot, 2026-11-05 rev)
and estimate the rear (tail) support height and angle.
Screenshot scale from Julian's Fusion measure: 40 mm circles at the rear axle and front cross,
570.35 mm apart (570.0 mm in the side plane, 19.8 mm lateral offset) = 595.35 px."""
import os, math, numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
TV = os.environ.get("TV", os.path.join(HERE, "..", "..", "..", "..", "assets", "livery", "out", "three-view-clean.png"))
SS = os.environ.get("SS", os.path.join(HERE, "dolly-side-view-input.png"))

# ---- manufacturer side view (drawing px); 1070 mm overall length = 1750 - 1082 px
K = 1070 / (1750 - 1082)
LE = (1211.0, 407.5)                 # wing root LE / lowest underside point

# ---- dolly screenshot (px), measured
S = 570.0 / 595.35                   # mm per px
TRAY0, TRAY_SLOPE = (480.0, 209.0), 28 / 310      # tray top line: y = 209 - slope (x - 480), y down
TRAY_DEG = math.degrees(math.atan(TRAY_SLOPE))
RAMP_X, LIP_Y = 793.0, 150.0
RAIL_C, RAIL_TOP, GROUND, AXLE_X = 440.2, 422.0, 542.0, 160.0
GAP, TPU = 3.0, 2.0                  # mm: LE to ramp face, cover on the tray

def tray_y(x): return TRAY0[1] - TRAY_SLOPE * (x - TRAY0[0])

tv = cv2.imread(TV, 0)
belly = []
for x in range(1180, 1701):
    c = np.nonzero(tv[300:485, x] < 130)[0]
    if c.size: belly.append((x, 300 + c.max()))
belly = np.array(belly, float)

def pose(pitch):
    a = math.radians(pitch)
    x0 = RAMP_X - GAP / S
    def f(P):
        P = np.atleast_2d(np.asarray(P, float))
        X = -(P[:, 0] - LE[0]) * K; Y = -(P[:, 1] - LE[1]) * K
        Xr = X * math.cos(a) - Y * math.sin(a); Yr = X * math.sin(a) + Y * math.cos(a)
        return np.c_[x0 + Xr / S, tray_y(x0) - (TPU + Yr) / S]
    return f

def belly_y(pitch, x):
    B = pose(pitch)(belly); o = np.argsort(B[:, 0])
    return np.interp(x, B[o, 0], B[o, 1])

def report(pitch, d_mm):
    """belly at d_mm aft of the wing LE: (above rail top, above rail centre, above ground, slope deg rising aft)"""
    x = RAMP_X - (GAP + d_mm) / S
    y = belly_y(pitch, x)
    y1, y2 = belly_y(pitch, x - 15 / S), belly_y(pitch, x + 15 / S)
    return x, (RAIL_TOP - y) * S, (RAIL_C - y) * S, (GROUND - y) * S, math.degrees(math.atan((y2 - y1) / (30 / S)))

if __name__ == "__main__":
    print(f"scale {S:.4f} mm/px, tray {TRAY_DEG:.2f} deg, lip {(tray_y(RAMP_X) - LIP_Y) * S:.1f} mm, "
          f"rail OD {(458 - 422) * S:.1f} mm, wheel dia {(542 - 337) * S:.0f} mm, axle {(RAMP_X - AXLE_X) * S - GAP:.0f} mm aft of LE")
    for pitch, lab in [(TRAY_DEG - 2, "wing +2 to datum"), (TRAY_DEG, "wing parallel to datum"), (TRAY_DEG + 2, "wing -2 to datum")]:
        print(lab)
        for d in (450, 500, 550, 600, 620):
            x, hrt, hrc, hg, sl = report(pitch, d)
            print(f"   {d} mm aft LE (px {x:.0f}): {hrt:6.1f} above rail top, {hrc:6.1f} above rail/axle centre, {hg:6.1f} above ground, belly {sl:4.1f} deg")
    B = pose(TRAY_DEG)(belly)
    print("tail end", round((RAMP_X - B[:, 0].min()) * S - GAP), "mm aft of LE; skid lowest",
          round((RAIL_TOP - B[:, 1].max()) * S), "mm above rail top")
