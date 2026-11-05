import os, math, numpy as np, cv2
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fit_side_view import *

PADL = 140
ss = cv2.cvtColor(cv2.imread(SS), cv2.COLOR_BGR2RGB)
ss = cv2.copyMakeBorder(ss, 0, 0, PADL, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
tv = cv2.imread(TV, 0)
src = np.float32([[1200, 300], [1700, 300], [1200, 480]])
M = cv2.getAffineTransform(src, np.float32(pose(TRAY_DEG)(src) + [PADL, 0]))
w = cv2.warpAffine(255 - tv, M, (ss.shape[1], ss.shape[0])) / 255.0
img = ss.astype(float) / 255
img = img * (1 - 0.9 * w[..., None]) + np.array([0.05, 0.25, 0.75]) * 0.9 * w[..., None]

fig = plt.figure(figsize=(12, 8.4), dpi=130)
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.imshow(img, extent=(-PADL - 0.5, ss.shape[1] - PADL - 0.5, ss.shape[0] - 0.5, -0.5)); ax.set_xlim(-PADL + 5, 912); ax.set_ylim(650, 10)
for d, ls in ((-2, "--"), (2, ":")):
    B = pose(TRAY_DEG + d)(belly); o = np.argsort(B[:, 0])
    ax.plot(B[o, 0], B[o, 1], ls, color="#888", lw=1.1)

D = 600.0                                    # support station, mm aft of wing LE (at the rear axle)
xp, hrt, hrc, hg, _ = report(TRAY_DEG, D)
yb = belly_y(TRAY_DEG, xp)
ya, yf = belly_y(TRAY_DEG, xp - 50 / S), belly_y(TRAY_DEG, xp + 50 / S)
ang = math.degrees(math.atan((yf - ya) / (100 / S)))
hw = 22 / S
ax.add_patch(plt.Polygon([[xp - hw, yb - (yf - ya) / 100 * S * hw * -1 * -1 - (yf-ya)/(100/S)*hw*0],
                          [xp - hw, yb + (yf - ya) / (100 / S) * -hw], [xp + hw, yb + (yf - ya) / (100 / S) * hw],
                          [xp + hw, RAIL_C], [xp - hw, RAIL_C]][1:], closed=True,
                         fc="#e8792e", ec="k", alpha=0.85, lw=1, zorder=5))
def vdim(x, y0, y1, t, side=1):
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", lw=1, color="k"))
    ax.text(x + 6 * side, (y0 + y1) / 2, t, fontsize=9.5, va="center", ha="left" if side > 0 else "right",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
vdim(xp + 40, yb, RAIL_C, f"{hrc:.0f} mm\nbelly to rail /\naxle centreline")
vdim(xp + 110, yb, GROUND, f"{hg:.0f} mm\nto ground")
ax.plot([xp + 60, xp + 170], [GROUND, GROUND], color="k", lw=0.8)
ax.text(xp + 40, yb + 24, f"pad top ~{abs(ang):.0f}° from level, higher at the rear", fontsize=9.5,
        bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
x0 = RAMP_X - GAP / S
ax.annotate("", (x0, 105), (xp, 105), arrowprops=dict(arrowstyle="<->", lw=1, color="k"))
ax.text((x0 + xp) / 2, 98, f"{D:.0f} mm, wing LE to support (rear axle station)", ha="center", fontsize=9.5,
        bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
ax.text(-PADL + 15, 585, f"Scale from your Fusion measure (570.35 mm between the 40 mm circles): {S:.3f} mm/px. Tray {TRAY_DEG:.1f}°, lip {(tray_y(RAMP_X) - LIP_Y) * S:.0f} mm.\n"
        "Manufacturer side view at 1:1, wing root on the tray, LE 3 mm off the ramp, 2 mm TPU, wing underside parallel to the fuselage datum.\n"
        "Grey dashed / dotted = belly if the wing sits +2° / -2° to the datum. Orange = rear support pad on a cross member (fuselage is on the centreline).",
        fontsize=8.6, color="#333", va="top")
fig.savefig(os.path.join(os.environ.get("OUT", HERE), "rear-support-fit.png"), dpi=130)
print(f"{D} mm: {hrt:.1f} above rail top, {hrc:.1f} above centreline, {hg:.1f} above ground, pad angle {ang:.1f}")
