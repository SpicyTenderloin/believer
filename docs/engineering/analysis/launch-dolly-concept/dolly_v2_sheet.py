"""BLV-DOL-006: concept views of the complete dolly (Julian's Fusion design + braced front outrigger wheels)."""
import math, os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle, Circle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("DD_DIR", HERE))
import dolly_drawings as dd
import dolly_v2_model as m

MM, INK, KEEP = dd.MM, dd.INK, dd.KEEP
dd.VIEWS.update({
    "v2_side":  ((0, -1, 0), (1, 0, 0)),            # from starboard, nose right
    "v2_plan":  ((0, 0, 1), (1, 0, 0)),             # from above, nose right, port up
    "v2_front": ((1, 0, 0), (0, 1, 0)),             # from ahead
    "v2_iso":   ((1, -1, 0.9), (1, 1, 0)),          # front-starboard-above
    "v2_iso_r": ((-1, -1, 1.0), (1, -1, 0)),        # rear-starboard-above
})
OR, TUBE, TYRE, PAD = "#E8772E", "#ECEBE6", "#2E2E2E", "#3B3B3B"
def colour(n):
    if n.startswith("tube_"): return TUBE
    if n.startswith("wheel"): return TYRE
    if n.startswith("axle"): return "#888888"
    return OR

parts = m.build()
discs = m.prop_discs()
P, ZR = m.P, m.ZR

def disc_pts(c, r, n=72):
    t = np.linspace(0, 2 * np.pi, n)
    return np.c_[np.full(n, c[0]), c[1] + r * np.cos(t), c[2] + r * np.sin(t)]

def prop_clearance():
    best = (1e9, None)
    rr, tt = np.meshgrid(np.linspace(0, 152.4, 40), np.linspace(0, 2 * np.pi, 120))
    for c, R in discs:
        D = np.c_[np.full(rr.size, c[0]), c[1] + (rr * np.cos(tt)).ravel(), c[2] + (rr * np.sin(tt)).ravel()]
        for k, s in parts.items():
            v, _ = s.tessellate(0.5, 0.2)
            Q = np.array([[q.x, q.y, q.z] for q in v])
            if len(Q) == 0: continue
            # cheap prefilter
            d = np.sqrt(((Q[:, None, :] - D[None, ::7, :]) ** 2).sum(-1)).min()
            if d < best[0] + 40:
                d = min(np.sqrt(((Q[i:i + 400, None, :] - D[None, :, :]) ** 2).sum(-1)).min() for i in range(0, len(Q), 400))
                if d < best[0]: best = (d, k)
    return best

def view(ax, name, centre, scale, anchor3, lw=0.35, shade=True, discs_on=True):
    a = dd.proj(name, anchor3)[0]
    tf = lambda q: np.asarray(centre) + scale * (np.atleast_2d(q) - a)
    if shade:
        dd.shaded(ax, parts, name, tf, colour, tol=0.8)
    vis, hid = dd.hlr(parts.values(), name, "v2")
    ax.add_collection(LineCollection([tf(q) for q in vis], colors="#1a1a1a", linewidths=lw * MM / 2, zorder=4))
    if discs_on:
        for c, R in discs:
            uv = dd.proj(name, disc_pts(c, R))
            if np.ptp(uv[:, 0]) < 1 or np.ptp(uv[:, 1]) < 1:       # edge-on
                ax.plot(*tf(uv).T, color=KEEP, lw=0.6 * MM, ls=(0, (5, 2)), zorder=6)
            else:
                ax.add_patch(Polygon(tf(uv), closed=True, fc=(0.84, 0.15, 0.16, 0.12), ec=KEEP,
                                     lw=0.3 * MM, ls=(0, (5, 2)), zorder=6))
    return lambda p3: tf(dd.proj(name, p3))[0]

def title_block(ax):
    dd.REV, dd.DATE = "A", "2026-11-05"
    dd.title_block(ax, "CONCEPT VIEWS - COMPLETE DOLLY", "BLV-DOL-006", 1, 1, "AS SHOWN")
    # overwrite generator + assumption strip text
    x0, y0, w, h = 230, 10, 180, 38
    ax.add_patch(Rectangle((x0 + 60.2, y0 + 0.3), 59.6, 6.4, fc="white", ec="none", zorder=12))
    ax.text(x0 + 62, y0 + 3.5, "GENERATED: dolly_v2_sheet.py", fontsize=5.5, va="center", zorder=13)
    ax.add_patch(Rectangle((x0 + 0.3, y0 + h + 0.3), w - 0.6, 5.4, fc="#fff3cd", ec="none", zorder=12))
    ax.text(x0 + 2, y0 + h + 3, "Side frame from the Fusion model; values marked TBD and the prop discs are not yet measured.",
            fontsize=5.6, va="center", zorder=13)

fig, ax = dd.new_sheet()
title_block(ax)

# ---- isometric (front, starboard, above) - large
P_iso = view(ax, "v2_iso", (120, 222), 0.118, (-200, 0, 180))
dd.view_label(ax, 120, 280, "ISOMETRIC - FRONT, STARBOARD, ABOVE", "red dashed = 12 in propeller discs at the drawing's motor station (TBD)")
items = [("tray-S", "1", (-4, 30)), ("fit_tail-pad", "2", (-20, 14)), ("wheel-FS", "3", (-26, -6)),
         ("tube_outrigger-S", "4", (20, -14)), ("tube_brace-S", "5", (-22, -14)), ("tube_strut-S", "6", (28, 4)),
         ("tube_front-cross", "7", (34, -2)), ("tube_rear-cross", "8", (-26, -2)), ("wheel-S", "9", (-22, -10)),
         ("tube_diag-S", "10", (-22, 20)), ("tube_rail-S", "11", (-30, -10)), ("tube_upright-S", "12", (24, 26))]
for k, l, off in items:
    c = parts[k].Center(); xy = P_iso((c.x, c.y, c.z))
    dd.balloon(ax, xy, xy + np.array(off), l)

# ---- rear isometric - small
view(ax, "v2_iso_r", (330, 222), 0.08, (-200, 0, 180), discs_on=False)
dd.view_label(ax, 330, 280, "ISOMETRIC - REAR, STARBOARD, ABOVE")

# ---- orthographic views, 1:10
s = 1 / 15
Pside = view(ax, "v2_side", (152, 104), s, (-235, 0, 0))
dd.view_label(ax, 152, 150, "SIDE (FROM STARBOARD)  1:15")
Pplan = view(ax, "v2_plan", (58, 108), s, (-235, 0, 0))
dd.view_label(ax, 58, 150, "PLAN  1:15")
Pfront = view(ax, "v2_front", (262, 104), s, (0, 0, 0))
dd.view_label(ax, 262, 150, "FRONT  1:15")

# dimensions - side
xa, xn = P["x_axle"], 0.0
g0 = Pside((xa - m.R_W, -200, 0)); g1 = Pside((xn + m.R_W + 60, -200, 0))
ax.plot([g0[0] - 4, g1[0] + 4], [g0[1]] * 2, color="#5E7A3A", lw=0.4 * MM)
dd.dim_h(ax, Pside((xa, 0, 0)), Pside((0, 0, 0)), g0[1] - 4, f"{-xa:.0f} wheelbase", above=False)
dd.dim_v(ax, Pside((P["x_ramp"] + 12, 0, 0)), Pside((P["x_ramp"] + 12, 0, ZR + P["z_lip"])), Pside((P["x_ramp"], 0, 0))[0] + 26,
         f"{ZR + P['z_lip']:.0f} lip", left=False)
zp = ZR + 16 + P["pad_rise"]
dd.dim_v(ax, Pside((xa, 0, 0)), Pside((xa, 0, zp)), Pside((xa - m.R_W, 0, 0))[0] - 4, f"{zp:.0f} tail pad", left=True)
dd.leader(ax, Pside((-120, 0, ZR + m.tray_top(-120))), Pside((-120, 0, ZR + m.tray_top(-120)))+ np.array([-6, 12]), "tray 5.2 deg", fs=5.6, ha="right") if False else None

# dimensions - plan
yr, yw = P["y_rail"], P["y_wheel"]
dd.dim_v(ax, Pplan((xa - m.R_W, -yr, 0)), Pplan((xa - m.R_W, yr, 0)), Pplan((xa - m.R_W, 0, 0))[0] - 4, f"{2 * yr:.0f} rails (TBD)", left=True)
yf = P["y_front"] + P["wheel_w"] / 2 + 14
dd.dim_v(ax, Pplan((m.R_W, -yf, 0)), Pplan((m.R_W, yf, 0)), Pplan((m.R_W, 0, 0))[0] + 5, f"{2 * yf:.0f} front track", left=False)
dd.dim_v(ax, Pplan((xa + m.R_W, -yw, 0)), Pplan((xa + m.R_W, yw, 0)), Pplan((xa + m.R_W, 0, 0))[0] + 4, f"{2 * yw:.0f}", left=False)

zl = ZR + P['z_lip']
dd.dim_v(ax, Pfront((0, -P['y_rail'] - 30, 0)), Pfront((0, -P['y_rail'] - 30, zl)), Pfront((0, -260, 0))[0] - 2, f"{zl:.0f}", left=True)
# clearance check
dmin, near = prop_clearance()
print("prop clearance", round(dmin, 1), near)

kd = [("Layout", "4 wheels: rear wheels on the rails, front wheels on outriggers"),
      ("Wheels", f"{P['wheel_d']:.0f} mm; track {2 * yf:.0f} front / {2 * yw:.0f} rear; wheelbase {-xa:.0f}"),
      ("Wing supports", f"5.2 deg wedge trays at y = +/-{yr:.0f} (TBD), 30 mm lip"),
      ("Tail support", f"Pad top {zp:.0f} above ground, {P['pad_deg']:.0f} deg, adjustable +/-20"),
      ("Front outriggers", "Arm + horizontal brace + vertical strut each side; wheel outboard of prop disc"),
      ("Prop disc to dolly", f"{dmin:.0f} mm, at {near.replace('tray-', 'ramp ').replace('fit_', '')} (req. >= 75; prop position TBD)"),
      ("Overall L x W x H", f"{m.R_W - (xa - m.R_W):.0f} x {2 * (yf + P['wheel_w'] / 2):.0f} x {ZR + P['z_lip']:.0f} mm")]
dd.table(ax, 232, 91, ["KEY DATA", "VALUE"], [list(r) for r in kd], [40, 138], fs=5.8, rh=4.2)

legend = ["Wedge tray with ramp stop (PETG, TPU cover)", "Tail support pad (TPU) on adjustable centre post",
          "Front wheel (x2), outboard of the prop discs", "Outrigger arm from the front tee (x2)",
          "Horizontal brace, outrigger end to rail tee (x2)", "Vertical strut, outrigger end to upright tee (x2)",
          "Front cross member", "Rear cross member (carries tail post)",
          "Rear wheel (x2)", "Diagonal strut, rail tee to tray", "Rail (x2)", "Front upright (x2)"]
yy = 46
ax.text(18, yy + 5, "ITEMS", fontsize=7, weight="bold")
for i, t in enumerate(legend):
    col, row = divmod(i, 6)
    x, y = 18 + col * 104, yy - row * 4.4
    ax.add_patch(Circle((x + 2.5, y + 0.3), 2.1, fc="white", ec=INK, lw=0.25 * MM))
    ax.text(x + 2.5, y + 0.3, str(i + 1), fontsize=5, ha="center", va="center", weight="bold")
    ax.text(x + 6.5, y, t, fontsize=6, va="center")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
fig.savefig(os.path.join(HERE, "out", "BLV-DOL-006-concept-views.pdf"))
fig.savefig(os.path.join(HERE, "out", "BLV-DOL-006.png"), dpi=170)
assets = os.path.join(HERE, "..", "..", "..", "assets", "diagrams")
if os.path.isdir(assets):
    fig.savefig(os.path.join(assets, "launch-dolly-BLV-DOL-006.png"), dpi=170)
