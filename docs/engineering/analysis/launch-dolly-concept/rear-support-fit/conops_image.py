"""Believer launch dolly: concept-of-operations image (six phases, side view, to scale).
Uses the side-view fit in fit_side_view.py; writes docs/assets/diagrams/launch-dolly-conops.png."""
import os, math, numpy as np, cv2
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch
import fit_side_view as F
_fonts = {f.name for f in matplotlib.font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = next(f for f in ("Inter", "Segoe UI", "DejaVu Sans") if f in _fonts)

NAVY, OR, ORD, TUBE, GREY = "#0A2A5B", "#D9772E", "#B85E1E", "#E6E1D3", "#8C8778"
S, X0, Y0 = F.S, 755.3, F.RAIL_C                     # screenshot px -> dolly mm (origin: front cross centre)
def mm(P): P = np.atleast_2d(P); return np.c_[(P[:, 0] - X0) * S, (Y0 - P[:, 1]) * S]
X_AX = (F.AXLE_X - X0) * S                           # tail-support contact station (side-view fit)
WHEELBASE, D_WHEEL = 580.0, 218.0                    # Fusion side view 2026-11-09: rear axle aft of the front axle; wheel dia over tread
X_RW, R_W = -WHEELBASE, D_WHEEL / 2                  # rear axle (tail post on it, cradle ~10 mm ahead)
GROUND = -R_W                                        # axles on the rail centreline
def tray_top(x): return (Y0 - F.tray_y(x / S + X0)) * S
X_RAMP = (F.RAMP_X - X0) * S; Y_LIP = (Y0 - F.LIP_Y) * S
RAIL_TOP = (Y0 - F.RAIL_TOP) * S
PAD_TOP = RAIL_TOP + 142.3

tv = cv2.imread(F.TV, 0)
art = np.zeros(tv.shape, np.float32)
art[270:490, 1070:1770] = (tv[270:490, 1070:1770] < 140)            # side view only
SRC = np.float32([[1200, 300], [1700, 300], [1200, 480]])
base = mm(F.pose(F.TRAY_DEG)(SRC))                   # aircraft at rest, mm
LE = mm(F.pose(F.TRAY_DEG)([F.LE]))[0]
B = mm(F.pose(F.TRAY_DEG)(F.belly)); o = np.argsort(B[:, 0])
TAIL = np.array([X_AX, np.interp(X_AX, B[o, 0], B[o, 1])])      # tail-support contact
h_lip = Y_LIP - LE[1]
x_T = LE[0] - TAIL[0]
d_alpha = math.degrees(math.atan2(h_lip, x_T))

def rigid(P, rot=0.0, about=(0, 0), dx=0.0, dy=0.0):
    a = math.radians(rot); c, s_ = math.cos(a), math.sin(a)
    Q = P - about
    return np.c_[c * Q[:, 0] - s_ * Q[:, 1], s_ * Q[:, 0] + c * Q[:, 1]] + about + [dx, dy]

EXT = (-930, 720, -150, 800); RES = 1.6
def aircraft(ax, rot=0.0, dx=0.0, dy=0.0, about=None, alpha=1.0, colour=None):
    about = TAIL if about is None else about
    P = rigid(base, rot, about, dx, dy)
    W, H = int((EXT[1] - EXT[0]) * RES), int((EXT[3] - EXT[2]) * RES)
    dst = np.c_[(P[:, 0] - EXT[0]) * RES, (EXT[3] - P[:, 1]) * RES].astype(np.float32)
    M = cv2.getAffineTransform(SRC, dst)
    a = cv2.warpAffine(art, M, (W, H), flags=cv2.INTER_LINEAR)
    rgba = np.zeros((H, W, 4)); rgba[..., :3] = matplotlib.colors.to_rgb(colour or NAVY); rgba[..., 3] = np.clip(a * 1.3, 0, 1) * alpha
    ax.imshow(rgba, extent=(EXT[0], EXT[1], EXT[2], EXT[3]), zorder=6, interpolation="antialiased")
    return lambda Q: rigid(np.atleast_2d(Q), rot, about, dx, dy)[0]

def tube(ax, p, q, w=33, fc=TUBE, z=3):
    p, q = np.array(p, float), np.array(q, float); d = q - p; n = np.array([-d[1], d[0]]) / np.hypot(*d) * w / 2
    ax.add_patch(Polygon([p + n, q + n, q - n, p - n], closed=True, fc=fc, ec="k", lw=0.6, zorder=z))

def dolly(ax, dx=0.0):
    sh = lambda pts: [(x + dx, y) for x, y in pts]
    ax.add_patch(Rectangle((EXT[0], EXT[2]), EXT[1] - EXT[0], GROUND - EXT[2], fc="#DCE8C8", ec="none", zorder=1))
    ax.plot([EXT[0], EXT[1]], [GROUND] * 2, color="#5E7A3A", lw=1.2, zorder=2)
    tube(ax, (X_RW + dx, 0), (dx + 8, 0))
    tube(ax, (dx, 0), (dx, 192)); tube(ax, (-436 + dx, 0), (-272 + dx, 205))
    for x0, x1 in ((X_RW + 10, X_RW + 70), (-470, -400), (-35, 8)):
        ax.add_patch(Rectangle((x0 + dx, -18), x1 - x0, 36, fc=OR, ec="k", lw=0.6, zorder=4))
    xs = np.linspace(-275, X_RAMP, 30)
    tray = [(-275, 190), (X_RAMP + 12, 190), (X_RAMP + 12, Y_LIP), (X_RAMP, Y_LIP), (X_RAMP, tray_top(X_RAMP))] + \
           [(x, tray_top(x)) for x in xs[::-1]]
    ax.add_patch(Polygon(sh(tray), closed=True, fc=OR, ec="k", lw=0.7, zorder=5))
    # tail support: V-cradle on a centreline post on the rear cross member, belly in the V, top 6 deg (higher at the rear)
    t6 = math.tan(math.radians(6)); L2 = 35
    apex, tips, bot = PAD_TOP - 7, PAD_TOP + 18.5, PAD_TOP - 25
    tube(ax, (X_RW + dx, 18), (X_RW + dx, bot - 40), w=32, z=3)
    ax.add_patch(Rectangle((X_RW - 21 + dx, bot - 55), 42, 56, fc=OR, ec="k", lw=0.7, zorder=4))
    ax.add_patch(Polygon(sh([(X_AX - L2, bot + L2 * t6), (X_AX + L2, bot - L2 * t6), (X_AX + L2, tips - L2 * t6), (X_AX - L2, tips + L2 * t6)]),
                         closed=True, fc=OR, ec="k", lw=0.7, zorder=4, alpha=0.95))
    ax.plot([X_AX - L2 + dx, X_AX + L2 + dx], [apex + L2 * t6, apex - L2 * t6], color="k", lw=0.6, ls=(0, (3, 2)), zorder=4)
    wheel(ax, X_RW + dx, 5); wheel(ax, dx, 7)

def wheel(ax, x, z):
    """Five-spoke printed wheel with a tyre, as in the Fusion model."""
    ax.add_patch(Circle((x, 0), R_W, fc="#3A3A3A", ec="k", lw=0.8, zorder=z))
    ax.add_patch(Circle((x, 0), R_W * 0.84, fc=OR, ec="k", lw=0.6, zorder=z))
    for k in range(5):
        th = np.radians(90 + 72 * k + np.linspace(-24, 24, 12))
        r1, r2 = R_W * 0.30, R_W * 0.72
        P = np.r_[np.c_[r2 * np.cos(th), r2 * np.sin(th)], np.c_[r1 * np.cos(th[::-1]), r1 * np.sin(th[::-1])]] + [x, 0]
        ax.add_patch(Polygon(P, closed=True, fc="white", ec="k", lw=0.5, zorder=z))
    ax.add_patch(Circle((x, 0), R_W * 0.17, fc=OR, ec="k", lw=0.6, zorder=z))
    ax.add_patch(Circle((x, 0), R_W * 0.08, fc="#3A3A3A", ec="none", zorder=z))

def arrow(ax, p, q, col, lw=2.2, z=9, ms=14):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=col, zorder=z))

def label(ax, x, y, t, **k):
    k.setdefault("fontsize", 8.5); k.setdefault("zorder", 10)
    ax.text(x, y, t, bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.2), **k)

def speedlines(ax, x, ys, L=120):
    for y in ys: ax.plot([x - L, x], [y, y], color="#9AA7B8", lw=1.2, zorder=2)

def panel(ax, n, title, body):
    ax.set_xlim(EXT[0], EXT[1]); ax.set_ylim(EXT[2], EXT[3]); ax.set_aspect("equal"); ax.axis("off")
    ax.text(EXT[0] + 15, EXT[3] - 20, f"{n}  {title}", fontsize=12, weight="bold", va="top", color=NAVY, zorder=11)
    ax.text(EXT[0] + 15, EXT[3] - 78, body, fontsize=8.8, va="top", color="#222", zorder=11, linespacing=1.35)

fig = plt.figure(figsize=(18, 7.9), dpi=140)
fig.text(0.012, 0.982, "Believer launch dolly - concept of operations", fontsize=16, weight="bold", va="top", color=NAVY)
fig.text(0.012, 0.942, "Side view to scale: manufacturer outline at 1:1 on the dolly geometry. Nearest side frame and wheels shown; "
         "the V-cradle tail support is on the centreline.", fontsize=9.5, va="top", color="#444")
axs = [fig.add_axes([0.005 + c * 0.332, 0.475 - r * 0.44, 0.325, 0.44]) for r in range(2) for c in range(3)]
LEc = np.array([LE[0], LE[1] - 2.0])                       # leading-edge contact on the tray (pivot for pitch-down)
A_LOW = 2.0                                                # illustrative lower AoA (trim), TBD
D_ROT = A_LOW - F.TRAY_DEG                                 # nose-down rotation (negative)

def aoa(ax, f, alpha, col=NAVY, ghost=False, L=330, R=290, lab=True):
    """Wing-underside reference line from the LE, horizontal reference and the angle between them."""
    le = f(LE)
    a = math.radians(alpha)
    ax.plot([le[0], le[0] - L * math.cos(a)], [le[1], le[1] - L * math.sin(a)], color=col, lw=1.4 if not ghost else 1.0,
            ls="-" if not ghost else (0, (4, 3)), alpha=1 if not ghost else 0.6, zorder=8)
    if not ghost:
        ax.plot([le[0], le[0] - L], [le[1], le[1]], color="#777", lw=0.8, ls=(0, (3, 3)), zorder=8)
        th = np.radians(np.linspace(180, 180 + alpha, 30))
        ax.plot(le[0] + R * np.cos(th), le[1] + R * np.sin(th), color=col, lw=1.6, zorder=8)
    if lab:
        label(ax, le[0] - L - 10, le[1] - L * math.sin(a) - 8, f"α ≈ {alpha:.0f}°" if not ghost else f"{alpha:.0f}° at rest",
              fontsize=9 if not ghost else 7.5, color=col, ha="right", va="center")


def gauge(ax, alpha, ghost=None, cx=330, cy=490):
    """Attitude gauge: wing section at its true angle against a horizontal reference."""
    C = 300.0
    xs = np.linspace(0, 1, 40)
    t = 0.12 * 5 * (0.2969 * np.sqrt(xs) - 0.126 * xs - 0.3516 * xs ** 2 + 0.2843 * xs ** 3 - 0.1015 * xs ** 4)
    up = np.c_[-xs * C, t * C * 0.9]; lo = np.c_[-xs * C, -t * C * 0.25]          # LE at origin, chord aft (-x)
    sec = np.vstack([up, lo[::-1]])
    le = np.array([cx + C / 2, cy])
    ax.plot([cx - C / 2 - 30, cx + C / 2 + 30], [cy, cy], color="#999", lw=0.8, ls=(0, (3, 3)), zorder=8)
    for a, fc, ec, z in ([(ghost, "none", "#9a9a9a", 8)] if ghost is not None else []) + [(alpha, "#DCE6F2", NAVY, 9)]:
        r = math.radians(a)
        R = np.array([[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]])
        P = sec @ R.T + le
        ax.add_patch(Polygon(P, closed=True, fc=fc, ec=ec, lw=1.0, ls="-" if fc != "none" else (0, (3, 2)), zorder=z))
    ax.add_patch(Polygon([le + [0, 0]], closed=False))
    th = np.radians(np.linspace(180, 180 + alpha, 20))
    ax.plot(le[0] + 0 * th, le[1] + 0 * th, alpha=0)
    ax.text(le[0] + 40, cy + 5, f"α ≈ {alpha:.0f}°", fontsize=10.5, weight="bold", color=NAVY, va="center", zorder=10)
    if ghost is not None:
        ax.text(le[0] + 40, cy - 55, f"from {ghost:.0f}°", fontsize=8, color="#777", va="center", zorder=10)
    ax.text(cx - C / 2 - 30, cy + 62, "wing attitude", fontsize=7.5, color="#666", zorder=10)

def ghost(ax):
    aircraft(ax, alpha=0.18, colour="#555555")

# 1 set-up
ax = axs[0]; panel(ax, 1, "Set-up", "Dolly pointed into wind. Wing seated on both 5° trays, leading\nedge ~3 mm behind the ramps; rear fuselage in the V-cradle tail support.\nHand launch remains the fallback.")
dolly(ax); f = aircraft(ax); gauge(ax, F.TRAY_DEG)
label(ax, X_RAMP + 30, Y_LIP + 10, "ramp lip\n30 mm", fontsize=8)
label(ax, -925, 150, "tail support", fontsize=8)
arrow(ax, (-800, 175), (X_AX - 25, PAD_TOP - 20), "#555", lw=1, ms=8)

# 2 ground roll
ax = axs[1]; panel(ax, 2, "Ground roll", "Throttle up. The leading edges bear on the ramps and the\naircraft drives the dolly at its 5° resting attitude.")
dolly(ax); f = aircraft(ax); gauge(ax, F.TRAY_DEG)
arrow(ax, (LE[0] + 120, LE[1] + 75), (LE[0] + 330, LE[1] + 75), "#C0392B"); label(ax, LE[0] + 200, LE[1] + 100, "$T$", fontsize=11, color="#C0392B")
arrow(ax, (X_RAMP - 60, Y_LIP - 18), (X_RAMP + 5, Y_LIP - 18), ORD, lw=1.8, ms=11)
speedlines(ax, X_AX - 110, [40, 110, 300, 360], 110)

# 3 tail rises, nose-down to a lower AoA
ax = axs[2]; panel(ax, 3, "Tail rises, AoA reduces", "As airspeed builds the tail lifts off its support and the aircraft\npitches nose-down about the leading edges, settling at a lower\nAoA as the wing takes up its weight.")
dolly(ax); ghost(ax)
f = aircraft(ax, rot=D_ROT, about=LEc); gauge(ax, A_LOW, ghost=F.TRAY_DEG)
ax.add_patch(Circle(tuple(LEc), 10, fc="#C0392B", ec="none", zorder=9)); label(ax, LEc[0] + 45, LEc[1] - 95, "pivot at\nthe ramps", fontsize=8, ha="left")
tl = f(TAIL)
arrow(ax, (tl[0] - 40, tl[1] + 20), (tl[0] - 40, tl[1] + 120), "#1E7B45", lw=2.0); label(ax, tl[0] - 20, tl[1] + 110, "tail lifts", fontsize=8.5, color="#1E7B45")
arrow(ax, (LE[0] + 120, LE[1] + 70), (LE[0] + 330, LE[1] + 70), "#C0392B")
speedlines(ax, X_AX - 110, [40, 110, 300, 360], 110)

# 4 lift-off over the lips at the lower AoA
ax = axs[3]; panel(ax, 4, "Lift-off", "The wing lifts off the trays at the lower AoA and rises over\nthe 30 mm lips. The tail support no longer carries any load.")
dolly(ax)
f = aircraft(ax, rot=D_ROT, about=LEc, dx=25, dy=h_lip + 14); gauge(ax, A_LOW)
le = f(LE)
arrow(ax, (le[0] - 150, le[1] + 120), (le[0] - 150, le[1] + 260), "#1E7B45", lw=2.0); label(ax, le[0] - 130, le[1] + 240, "$L > W$", fontsize=10, color="#1E7B45")
arrow(ax, (le[0] + 120, le[1] + 70), (le[0] + 330, le[1] + 70), "#C0392B")

# 5 separation
ax = axs[4]; panel(ax, 5, "Separation", "Over the lips, thrust carries the aircraft forward and clear.\nThe dolly is no longer driven; it slows on the grass and\nstops behind the aircraft.")
dolly(ax, dx=-140)
f = aircraft(ax, rot=D_ROT + 1.5, about=LEc, dx=330, dy=110)
le = f(LE)
arrow(ax, (le[0] + 120, le[1] + 80), (le[0] + 300, le[1] + 95), "#C0392B")
arrow(ax, (X_RAMP - 140 + 30, -125), (X_RAMP - 140 - 150, -125), "#555", lw=1.6, ms=11); label(ax, X_RAMP - 330, -135, "dolly decelerates", fontsize=8, ha="right")

# 6 recovery
ax = axs[5]; panel(ax, 6, "Recovery", "The dolly is retrieved once the aircraft has left the\nrunway area, and is reused for the next flight.")
dolly(ax)
label(ax, -560, 430, "aircraft climbing out", fontsize=8, color=NAVY)
arrow(ax, (-180, 450), (120, 540), NAVY, lw=1.6, ms=11)

fig.text(0.012, 0.015, f"Lower AoA shown at {A_LOW:.0f}° for illustration: the value the aircraft settles at depends on its trim and elevator input (TBD). "
         "Angles are of the wing underside, assuming it is parallel to the fuselage datum (wing incidence TBD).", fontsize=8.5, color="#444")
fig.savefig(os.environ.get("OUTPNG", os.path.join(F.HERE, "..", "..", "..", "..", "assets", "diagrams", "launch-dolly-conops.png")), dpi=140)
print("d_alpha", round(d_alpha, 2), "h_lip", round(h_lip, 1), "x_T", round(x_T), "tail", TAIL.round(1), "LE", LE.round(1))
