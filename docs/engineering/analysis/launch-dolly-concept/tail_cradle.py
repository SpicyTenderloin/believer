"""
Believer launch dolly - tail support cradle (BLV-DOL-007).
Printed V-cradle on an adjustable 32 mm post, on a tee in the middle of the rear cross member.
Writes out/BLV-DOL-007-tail-cradle.pdf/.png and out/printed-tail-cradle-v2.step/.stl and -liner.stl.
Fuselage section at the station is estimated from the manufacturer drawing (TBD - measure).
"""
import math, os, sys
import numpy as np
import cadquery as cq
from cadquery import Vector as V
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch, Arc

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("DD_DIR", HERE))
import dolly_drawings as dd
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
MM, INK = dd.MM, dd.INK
NAVY, OR, TPU, TUBE = "#0A2A5B", "#E8772E", "#3B3B3B", "#ECEBE6"

# ---------------- parameters (mm)
AXLE_Z = 98.0                 # axle / rail centreline above ground (wheel 196 mm)
BELLY_ABOVE_AXLE = 160.0      # belly bottom above the axle at the rear axle station (side-view fit)
SEC_W, SEC_D, SEC_N = 130.0, 65.0, 2.5   # estimated fuselage section at the station: width, depth, superellipse n (TBD)
PHI = 20.0                    # flank angle from horizontal (140 deg included)
FLAT = 10.0                   # half-width of the flat at the bottom of the V
HALF_W = 80.0                 # cradle half-width (160 wide)
LEN = 70.0                    # fore-aft length
TILT = 6.0                    # top surface slope, higher at the rear
T_TPU = 4.0                   # TPU liner
BASE = 18.0                   # printed body thickness under the V at the centreline
TUBE_OD, BORE = 32.0, 32.6
SLEEVE_OD, SLEEVE_L = 42.0, 55.0
BOLT = 5.5                    # M5 cross-bolt, holes in the post at 10 mm pitch for +/-20 mm
RAIL_Y, WHEEL_Y, WHEEL_W, R_W = 170.0, 225.0, 45.0, 98.0

def section(a, b=SEC_D / 2, n=SEC_N, k=400):
    t = np.linspace(0, 2 * np.pi, k)
    c, s = np.cos(t), np.sin(t)
    return np.c_[a * np.sign(c) * np.abs(c) ** (2 / n), b * np.sign(s) * np.abs(s) ** (2 / n)]

def v_surface_y(y):          # height of the TPU surface above the apex, at lateral offset y
    return np.where(np.abs(y) <= FLAT, 0.0, (np.abs(y) - FLAT) * math.tan(math.radians(PHI)))

def seat_clean(width):
    P = section(width / 2); lower = P[P[:, 1] < 0]
    shift = -(lower[:, 1] - v_surface_y(lower[:, 0])).min()          # raise section by this to touch the V
    i = np.argmin(lower[:, 1] - v_surface_y(lower[:, 0]))
    bottom_above_apex = lower[:, 1].min() + shift
    return bottom_above_apex, abs(lower[i, 0])

APEX_GAP, CONTACT_Y = seat_clean(SEC_W)
APEX_Z = AXLE_Z + BELLY_ABOVE_AXLE - APEX_GAP          # TPU surface at the centreline, above ground
BODY_APEX_Z = APEX_Z - T_TPU

# ---------------- CAD (local: x fwd, y port, z up; origin = printed V apex at the post axis)
def build():
    tphi = math.tan(math.radians(PHI))
    top = (HALF_W - FLAT) * tphi
    prof = [(-HALF_W, -BASE), (HALF_W, -BASE), (HALF_W, top), (FLAT, 0), (-FLAT, 0), (-HALF_W, top)]
    body = cq.Workplane("YZ").polyline(prof).close().extrude(LEN / 2, both=True).val()          # extrude along x
    body = body.rotate(V(0, 0, 0), V(0, 1, 0), -TILT)                                            # rear (-x) higher
    sleeve = cq.Solid.makeCylinder(SLEEVE_OD / 2, SLEEVE_L + BASE, V(0, 0, -BASE - SLEEVE_L), V(0, 0, 1))
    body = body.fuse(sleeve)
    body = body.cut(cq.Solid.makeCylinder(BORE / 2, SLEEVE_L + 2, V(0, 0, -BASE - SLEEVE_L - 1), V(0, 0, 1)))
    body = body.cut(cq.Solid.makeCylinder(BOLT / 2, SLEEVE_OD + 4, V(-SLEEVE_OD / 2 - 2, 0, -BASE - SLEEVE_L / 2), V(1, 0, 0)))
    # TPU liner: 4 mm on the V faces
    lin = [(-HALF_W, top), (-FLAT, 0), (FLAT, 0), (HALF_W, top), (HALF_W, top + T_TPU / math.cos(math.radians(PHI))),
           (FLAT, T_TPU), (-FLAT, T_TPU), (-HALF_W, top + T_TPU / math.cos(math.radians(PHI)))]
    liner = cq.Workplane("YZ").polyline(lin).close().extrude(LEN / 2, both=True).val().rotate(V(0, 0, 0), V(0, 1, 0), -TILT)
    return body.clean(), liner.clean()

def main():
    body, liner = build()
    cq.exporters.export(cq.Workplane().add(body), os.path.join(OUT, "printed-tail-cradle-v2.step"))
    cq.exporters.export(cq.Workplane().add(body), os.path.join(OUT, "printed-tail-cradle-v2.stl"))
    cq.exporters.export(cq.Workplane().add(liner), os.path.join(OUT, "printed-tail-cradle-v2-liner.stl"))
    sheet()

# ---------------- drawing
def sheet():
    fig, ax = dd.new_sheet()
    dd.REV, dd.DATE = "A", "2026-11-05"
    dd.title_block(ax, "TAIL SUPPORT CRADLE", "BLV-DOL-007", 1, 1, "AS SHOWN")
    x0, y0, w, h = 230, 10, 180, 38
    ax.add_patch(Rectangle((x0 + 60.2, y0 + 0.3), 59.6, 6.4, fc="white", ec="none", zorder=12))
    ax.text(x0 + 62, y0 + 3.5, "GENERATED: tail_cradle.py", fontsize=5.5, va="center", zorder=13)
    ax.add_patch(Rectangle((x0 + 0.3, y0 + h + 0.3), w - 0.6, 5.4, fc="#fff3cd", ec="none", zorder=12))
    ax.text(x0 + 2, y0 + h + 3, "Fuselage section at the station is estimated from the drawing (TBD) - measure before printing.",
            fontsize=5.6, va="center", zorder=13)
    tphi = math.tan(math.radians(PHI)); top = (HALF_W - FLAT) * tphi

    # ===== view 1: section at the rear axle, looking forward, 1:4
    s = 1 / 3; O = np.array([120.0, 112.0])                     # sheet position of (y=0, z=0 ground)
    P = lambda y, z: O + s * np.array([-y, z])                 # looking forward: port (+y) on the left
    def rect(y0_, z0_, y1_, z1_, **k):
        a, b = P(y0_, z0_), P(y1_, z1_)
        ax.add_patch(Rectangle((min(a[0], b[0]), min(a[1], b[1])), abs(b[0] - a[0]), abs(b[1] - a[1]), **k))
    ax.plot(*np.array([P(-300, 0), P(300, 0)]).T, color="#5E7A3A", lw=0.6 * MM)
    for g in (-1, 1):
        rect(g * (WHEEL_Y - WHEEL_W / 2), 0, g * (WHEEL_Y + WHEEL_W / 2), 2 * R_W, fc="#2E2E2E", ec=INK, lw=0.3 * MM)
        rect(g * RAIL_Y, AXLE_Z - 4, g * (WHEEL_Y - WHEEL_W / 2), AXLE_Z + 4, fc="#999", ec=INK, lw=0.2 * MM)    # axle stub
        ax.add_patch(Circle(P(g * RAIL_Y, AXLE_Z), s * 21, fc=OR, ec=INK, lw=0.3 * MM, zorder=4))
        ax.add_patch(Circle(P(g * RAIL_Y, AXLE_Z), s * TUBE_OD / 2, fc=TUBE, ec=INK, lw=0.25 * MM, zorder=5))
    rect(-RAIL_Y, AXLE_Z - TUBE_OD / 2, RAIL_Y, AXLE_Z + TUBE_OD / 2, fc=TUBE, ec=INK, lw=0.3 * MM)
    rect(-38, AXLE_Z - 21, 38, AXLE_Z + 21, fc=OR, ec=INK, lw=0.3 * MM)                       # centre tee
    rect(-21, AXLE_Z + 21, 21, AXLE_Z + 50, fc=OR, ec=INK, lw=0.3 * MM)                       # tee socket
    zb = BODY_APEX_Z - BASE; zs = zb - SLEEVE_L
    rect(-TUBE_OD / 2, AXLE_Z + 21, TUBE_OD / 2, zb + 10, fc=TUBE, ec=INK, lw=0.3 * MM, zorder=3)  # post
    rect(-SLEEVE_OD / 2, zs, SLEEVE_OD / 2, zb, fc=OR, ec=INK, lw=0.3 * MM, zorder=4)            # sleeve
    body = [(-HALF_W, zb), (HALF_W, zb), (HALF_W, BODY_APEX_Z + top), (FLAT, BODY_APEX_Z), (-FLAT, BODY_APEX_Z), (-HALF_W, BODY_APEX_Z + top)]
    ax.add_patch(Polygon([P(y, z) for y, z in body], closed=True, fc=OR, ec=INK, lw=0.35 * MM, zorder=4))
    lt = T_TPU / math.cos(math.radians(PHI))
    lin = [(-HALF_W, BODY_APEX_Z + top), (-FLAT, BODY_APEX_Z), (FLAT, BODY_APEX_Z), (HALF_W, BODY_APEX_Z + top),
           (HALF_W, BODY_APEX_Z + top + lt), (FLAT, APEX_Z), (-FLAT, APEX_Z), (-HALF_W, BODY_APEX_Z + top + lt)]
    ax.add_patch(Polygon([P(y, z) for y, z in lin], closed=True, fc=TPU, ec=INK, lw=0.25 * MM, zorder=5))
    ax.add_patch(Circle(P(0, zs + SLEEVE_L / 2), s * BOLT / 2 + 0.4, fc="white", ec=INK, lw=0.2 * MM, zorder=6))
    # fuselage sections: nominal + range
    for wdt, ls, lw_, col in ((SEC_W, "-", 0.45, NAVY), (SEC_W - 30, (0, (4, 2)), 0.25, "#6b86ad"), (SEC_W + 30, (0, (4, 2)), 0.25, "#6b86ad")):
        gap, _ = seat_clean(wdt)
        sec = section(wdt / 2) + [0, APEX_Z + gap + SEC_D / 2]
        ax.plot(*np.array([P(y, z) for y, z in sec]).T, color=col, lw=lw_ * MM, ls=ls, zorder=7)
    ax.plot(*np.array([P(0, -10), P(0, APEX_Z + SEC_D + 25)]).T, color=INK, lw=0.15 * MM, ls=(0, (8, 2, 1, 2)))
    for g in (-1, 1):
        ax.plot(*P(g * CONTACT_Y, APEX_Z + v_surface_y(np.array([CONTACT_Y]))[0]), "o", ms=2.2, color="#C0392B", zorder=8)
    dd.view_label(ax, O[0], 278, "SECTION AT THE REAR AXLE, LOOKING FORWARD  1:3",
                  "fuselage section estimated (solid = 130 mm wide, dashed = 100 / 160 mm); red = contact lines")
    # dims
    xr = P(-300, 0)[0]
    dd.dim_v(ax, P(-260, AXLE_Z), P(-260, AXLE_Z + BELLY_ABOVE_AXLE), xr + 2, f"{BELLY_ABOVE_AXLE:.0f} belly", left=False)
    dd.dim_v(ax, P(-260, AXLE_Z), P(-260, APEX_Z), xr - 8, f"{APEX_Z - AXLE_Z:.0f} V", left=False)
    for zz in (AXLE_Z, APEX_Z, AXLE_Z + BELLY_ABOVE_AXLE):
        ax.plot(*np.array([P(-60 if zz != AXLE_Z else -RAIL_Y, zz), P(-262, zz)]).T, color=INK, lw=0.15 * MM)
    dd.dim_v(ax, P(300, 0), P(300, AXLE_Z), P(300, 0)[0] - 3, f"{AXLE_Z:.0f}", left=True)
    dd.dim_h(ax, P(RAIL_Y, AXLE_Z), P(-RAIL_Y, AXLE_Z), P(0, 0)[1] - 6, f"{2 * RAIL_Y:.0f} rails (TBD)", above=False)
    dd.dim_h(ax, P(WHEEL_Y, 0), P(-WHEEL_Y, 0), P(0, 0)[1] - 12, f"{2 * WHEEL_Y:.0f} rear track", above=False)
    dd.leader(ax, P(-HALF_W + 20, BODY_APEX_Z + (HALF_W - 20 - FLAT) * tphi + 2), P(-HALF_W - 10, APEX_Z + 95), "TPU liner 4", fs=5.8, ha="right")
    dd.leader(ax, P(0, zs + SLEEVE_L / 2), P(-110, zs + 5), "M5 cross-bolt", fs=5.8, ha="left")
    dd.leader(ax, P(0, AXLE_Z + 80), P(110, AXLE_Z + 120), "32 mm post", fs=5.8, ha="right")
    dd.leader(ax, P(-25, AXLE_Z - 15), P(-110, AXLE_Z - 50), "printed tee on rear cross", fs=5.8, ha="left")

    # ===== view 2: cradle section 1:2
    s2 = 0.5; O2 = np.array([318.0, 236.0])
    Q = lambda y, z: O2 + s2 * np.array([-y, z])          # z relative to the printed V apex
    body2 = [(-HALF_W, -BASE), (HALF_W, -BASE), (HALF_W, top), (FLAT, 0), (-FLAT, 0), (-HALF_W, top)]
    ax.add_patch(Polygon([Q(y, z) for y, z in body2], closed=True, fc=OR, ec=INK, lw=0.35 * MM, alpha=0.9))
    lin2 = [(y, z - BODY_APEX_Z) for y, z in lin]
    ax.add_patch(Polygon([Q(y, z) for y, z in lin2], closed=True, fc=TPU, ec=INK, lw=0.25 * MM))
    ax.add_patch(Rectangle(Q(SLEEVE_OD / 2, -BASE - SLEEVE_L), s2 * SLEEVE_OD, s2 * SLEEVE_L, fc=OR, ec=INK, lw=0.35 * MM, alpha=0.9))
    ax.add_patch(Rectangle(Q(BORE / 2, -BASE - SLEEVE_L), s2 * BORE, s2 * (SLEEVE_L), fc="white", ec=INK, lw=0.2 * MM, ls=(0, (3, 1.5))))
    dd.view_label(ax, O2[0], 272, "CRADLE SECTION  1:2", "printed PETG body, TPU liner")
    dd.dim_h(ax, Q(HALF_W, top), Q(-HALF_W, top), Q(0, top)[1] + 9, f"{2 * HALF_W:.0f}")
    dd.dim_h(ax, Q(FLAT, 0), Q(-FLAT, 0), Q(0, 0)[1] - 4, f"{2 * FLAT:.0f} flat", above=False)
    dd.dim_v(ax, Q(-HALF_W, -BASE), Q(-HALF_W, top), Q(-HALF_W, 0)[0] + 4, f"{BASE + top:.0f}", left=False)
    dd.dim_v(ax, Q(SLEEVE_OD / 2, -BASE - SLEEVE_L), Q(SLEEVE_OD / 2, -BASE), Q(SLEEVE_OD / 2, 0)[0] - 4, f"{SLEEVE_L:.0f}", left=True)
    dd.dim_h(ax, Q(SLEEVE_OD / 2, -BASE - SLEEVE_L), Q(-SLEEVE_OD / 2, -BASE - SLEEVE_L), Q(0, -BASE - SLEEVE_L)[1] - 5,
             f"OD {SLEEVE_OD:.0f}, bore {BORE:.1f}", above=False)
    c = Q(-HALF_W + 14, (HALF_W - 14 - FLAT) * tphi)
    ax.add_patch(Arc(Q(-FLAT, 0), 2 * s2 * 45, 2 * s2 * 45, theta1=0, theta2=PHI, lw=0.25 * MM))
    ax.plot(*np.array([Q(-FLAT, 0), Q(-FLAT - 50, 0)]).T, color=INK, lw=0.15 * MM)
    ax.text(*(Q(-FLAT - 50, 6)), f"{PHI:.0f}° (140° included)", fontsize=6, va="bottom")

    # ===== view 3: cradle side 1:2
    O3 = np.array([318.0, 150.0])
    R = lambda x, z: O3 + s2 * np.array([x, z])           # nose to the right
    t6 = math.tan(math.radians(TILT))
    side = [(-LEN / 2, -BASE + LEN / 2 * t6), (LEN / 2, -BASE - LEN / 2 * t6), (LEN / 2, top - LEN / 2 * t6), (-LEN / 2, top + LEN / 2 * t6)]
    ax.add_patch(Polygon([R(x, z) for x, z in side], closed=True, fc=OR, ec=INK, lw=0.35 * MM, alpha=0.9))
    apex = [(-LEN / 2, LEN / 2 * t6), (LEN / 2, -LEN / 2 * t6)]
    ax.plot(*np.array([R(*p) for p in apex]).T, color=INK, lw=0.25 * MM, ls=(0, (3, 1.5)))
    ax.add_patch(Rectangle(R(-SLEEVE_OD / 2, -BASE - SLEEVE_L), s2 * SLEEVE_OD, s2 * (SLEEVE_L + 2), fc=OR, ec=INK, lw=0.35 * MM, alpha=0.9))
    ax.add_patch(Circle(R(0, -BASE - SLEEVE_L / 2), s2 * BOLT / 2, fc="white", ec=INK, lw=0.25 * MM))
    dd.view_label(ax, O3[0], 184, "CRADLE SIDE  1:2", "nose to the right")
    dd.dim_h(ax, R(-LEN / 2, top + LEN / 2 * t6), R(LEN / 2, top - LEN / 2 * t6), R(0, top)[1] + 10, f"{LEN:.0f}")
    ax.text(*(R(LEN / 2 + 6, top - 2)), f"top {TILT:.0f}° to the sleeve axis,\nhigher at the rear (matches the belly)", fontsize=5.8, va="center")
    ax.text(*(R(SLEEVE_OD / 2 + 4, -BASE - SLEEVE_L / 2)), "M5 hole; post drilled\nat 10 mm pitch, +/-20", fontsize=5.8, va="center")

    # ===== notes and data
    gap_lo, _ = seat_clean(SEC_W - 30); gap_hi, _ = seat_clean(SEC_W + 30)
    dd.notes(ax, 18, 62, [
        f"Cradle sits on a 32 mm post in a printed tee at the middle of the rear cross member, at the rear axle\n"
        f"station (about 600 mm aft of the wing LE). The belly bottom sits {BELLY_ABOVE_AXLE:.0f} mm above the axle.",
        f"V-cradle, {PHI:.0f} deg flanks: self-centres the tail and opens upward, so the tail lifts straight out when it rises.\n"
        f"Belly bottom sits {gap_lo:.0f}-{gap_hi:.0f} mm above the V apex for sections 100-160 mm wide ({APEX_GAP:.0f} mm at 130).",
        "Set height on the aircraft: wing seated on both trays, belly just bearing on the cradle without lifting the LEs.\n"
        "Measure the belly width and profile at the station and check pushrods/antennas clear the cradle (TBD).",
        "Print PETG, 4 walls, 30% infill; liner TPU 95A (print or cut from 4 mm TPU sheet, bond with CA/contact cement).",
    ], fs=5.9, lh=3.3)
    kd = [("V apex (TPU) above axle", f"{APEX_Z - AXLE_Z:.0f} mm  ({APEX_Z:.0f} above ground)"),
          ("Belly bottom above axle", f"{BELLY_ABOVE_AXLE:.0f} mm (nominal section)"),
          ("Cradle", f"{2 * HALF_W:.0f} wide x {LEN:.0f} long, {PHI:.0f} deg flanks, {2 * FLAT:.0f} flat"),
          ("Post", f"32 mm tube, top {zb + 10 - AXLE_Z:.0f} above axle; adjust +/-20 mm"),
          ("Section assumed (TBD)", f"{SEC_W:.0f} wide x {SEC_D:.0f} deep, rounded")]
    dd.table(ax, 232, 104, ["KEY DATA", "VALUE"], [list(r) for r in kd], [52, 126], fs=5.8, rh=4.2)
    fig.savefig(os.path.join(OUT, "BLV-DOL-007-tail-cradle.pdf"))
    fig.savefig(os.path.join(OUT, "BLV-DOL-007.png"), dpi=170)
    assets = os.path.join(HERE, "..", "..", "..", "assets", "diagrams")
    if os.path.isdir(assets):
        fig.savefig(os.path.join(assets, "launch-dolly-BLV-DOL-007.png"), dpi=170)
    print("apex above axle", round(APEX_Z - AXLE_Z, 1), "gap", round(APEX_Z and APEX_GAP, 1), "contact y", round(CONTACT_Y, 1))

if __name__ == "__main__":
    main()
