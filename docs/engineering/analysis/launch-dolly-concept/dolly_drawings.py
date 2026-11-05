"""
Believer launch dolly - drawing set generator.

Run:  python dolly_drawings.py
Writes to ./out/ : BLV-DOL-001..005 as PDF (multi-page) + per-sheet SVG/PNG,
STEP models, results JSON.  Every view is a hidden-line projection of the
CadQuery solids in dolly_model.py; every dimension is read from the model.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, FancyBboxPatch
from matplotlib.backends.backend_pdf import PdfPages

import cadquery as cq
from cadquery import Vector as V
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dolly_model as dm
from dolly_model import p, P
import dolly_analysis as da

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
DATE = "2026-11-04"
REV = "B"
MM = 72 / 25.4          # points per mm
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7,
                     "svg.fonttype": "none", "pdf.fonttype": 42})

INK = "#111111"
PHANTOM = "#5b7a99"
RELEASE = "#1f6fd1"
KEEP = "#d62728"
ORANGE = "#e8772e"

# ---------------------------------------------------------------- projection
VIEWS = {
    "side": ((0, -1, 0), (1, 0, 0)),          # from port, nose left
    "plan": ((0, 0, 1), (1, 0, 0)),           # from above, nose left, stbd up
    "end":  ((-1, 0, 0), (0, -1, 0)),         # from ahead
    "iso_fl": ((-1, -1, 1), (1, -1, 0)),      # front-port-above
    "iso_rr": ((1, 1, 1), (-1, 1, 0)),        # rear-starboard-above
}


def _unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def axes_of(view):
    N, Vx = VIEWS[view]
    N, Vx = _unit(N), _unit(Vx)
    Vy = np.cross(N, Vx)
    return N, Vx, Vy


def proj(view, pts):
    _, Vx, Vy = axes_of(view)
    pts = np.atleast_2d(pts)
    return np.c_[pts @ Vx, pts @ Vy]


def _edges_to_polys(shape):
    polys = []
    if shape is None:
        return polys
    for e in cq.Shape.cast(shape).Edges():
        L = e.Length()
        if L < 1e-6:
            continue
        n = 2 if e.geomType() == "LINE" else max(6, min(200, int(L / 1.5)))
        pts = [e.positionAt(t) for t in np.linspace(0, 1, n)]
        polys.append(np.array([[q.x, q.y] for q in pts]))
    return polys


_hlr_cache = {}


def hlr_poly(shapes, view):
    """Mesh-based HLR (reliable silhouettes on smooth spline surfaces)."""
    from OCP.HLRBRep import HLRBRep_PolyAlgo, HLRBRep_PolyHLRToShape
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    N, Vx, _ = axes_of(view)
    pa = HLRBRep_PolyAlgo()
    for sh in shapes:
        BRepMesh_IncrementalMesh(sh.wrapped, 0.4, False, 0.25, True)
        pa.Load(sh.wrapped)
    pa.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*N), gp_Dir(*Vx))))
    pa.Update()
    h = HLRBRep_PolyHLRToShape()
    h.Update(pa)
    vis = []
    for getter in (h.VCompound, h.OutLineVCompound):
        s_ = getter()
        if not s_.IsNull():
            vis += _edges_to_polys(s_)
    return vis, []


def hlr(shapes, view, key=None, poly=False):
    """Hidden-line removal. Returns (visible, hidden) lists of (u, v) polylines."""
    if key and (key, view) in _hlr_cache:
        return _hlr_cache[(key, view)]
    if poly:
        res = hlr_poly(list(shapes), view)
        if key:
            _hlr_cache[(key, view)] = res
        return res
    comp = cq.Compound.makeCompound(list(shapes))
    N, Vx, _ = axes_of(view)
    algo = HLRBRep_Algo()
    algo.Add(comp.wrapped)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*N), gp_Dir(*Vx))))
    algo.Update()
    algo.Hide()
    h = HLRBRep_HLRToShape(algo)
    vis, hid = [], []
    for getter, dst in ((h.VCompound, vis), (h.OutLineVCompound, vis),
                        (h.HCompound, hid), (h.OutLineHCompound, hid)):
        s = getter()
        if not s.IsNull():
            dst += _edges_to_polys(s)
    if key:
        _hlr_cache[(key, view)] = (vis, hid)
    return vis, hid


class View:
    """Places model (u, v) coordinates on the sheet: sheet = origin + scale*(uv - anchor)."""

    def __init__(self, ax, view, scale, origin, anchor_uv=(0, 0)):
        self.ax, self.view, self.s = ax, view, scale
        self.o = np.asarray(origin, float)
        self.a = np.asarray(anchor_uv, float)

    def tf(self, uv):
        return self.o + self.s * (np.atleast_2d(uv) - self.a)

    def pt(self, p3):
        return self.tf(proj(self.view, p3))[0]

    def lines(self, polys, **kw):
        if polys:
            self.ax.add_collection(LineCollection([self.tf(q) for q in polys], **kw))

    def draw(self, shapes, key=None, hidden=False, lw=0.45, color=INK, ls="solid",
             hidden_lw=0.2, zorder=3, poly=False):
        vis, hid = hlr(shapes, self.view, key, poly)
        self.lines(vis, colors=color, linewidths=lw * MM, linestyles=ls, zorder=zorder,
                   capstyle="round")
        if hidden:
            self.lines(hid, colors="#888888", linewidths=hidden_lw * MM,
                       linestyles=(0, (3, 1.5)), zorder=zorder - 1)


# ---------------------------------------------------------------- shading
def shaded(ax, parts, view, tf, colors, light=(-0.35, -0.45, 0.82), alpha=1.0, zorder=2,
           tol=0.6):
    N, Vx, Vy = axes_of(view)
    Lg = _unit(light)
    polys, cols, depth = [], [], []
    for name, shp in parts.items():
        base = np.array(matplotlib.colors.to_rgb(colors(name)))
        verts, tris = shp.tessellate(tol, 0.3)
        Vt = np.array([[q.x, q.y, q.z] for q in verts])
        T = np.array(tris)
        if len(T) == 0:
            continue
        P3 = Vt[T]                                      # (n,3,3)
        nrm = np.cross(P3[:, 1] - P3[:, 0], P3[:, 2] - P3[:, 0])
        nn = np.linalg.norm(nrm, axis=1)
        ok = nn > 1e-9
        P3, nrm = P3[ok], nrm[ok] / nn[ok, None]
        facing = np.sign(nrm @ N)
        nrm = nrm * np.where(facing == 0, 1, facing)[:, None]
        diff = np.clip(nrm @ Lg, 0, 1)
        shade = 0.45 + 0.55 * diff
        c = np.clip(base[None, :] * shade[:, None] + 0.08 * (1 - shade[:, None]), 0, 1)
        uv = np.stack([P3 @ Vx, P3 @ Vy], axis=-1)
        polys += [tf(q) for q in uv]
        cols += [tuple(ci) + (alpha,) for ci in c]
        depth += list((P3.mean(axis=1) @ N))
    order = np.argsort(depth)
    pc = PolyCollection([polys[i] for i in order], facecolors=[cols[i] for i in order],
                        edgecolors=[cols[i] for i in order], linewidths=0.15, zorder=zorder)
    ax.add_collection(pc)


def part_color(name):
    if name.startswith("tube_"):
        return "#ecebe6"
    if name.startswith("fit_"):
        return ORANGE
    if name.startswith("ramp_head") or name == "tail_cradle":
        return ORANGE
    if name.startswith("pad_"):
        return "#3b3b3b"
    if name.startswith("wheel"):
        return "#2a2a2a"
    return "#bbbbbb"


# ---------------------------------------------------------------- sheet furniture
def new_sheet():
    fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 420)
    ax.set_ylim(0, 297)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((10, 10), 400, 277, fill=False, lw=0.7 * MM, ec=INK))
    for i in range(1, 8):          # zone ticks
        x = 10 + i * 400 / 8
        ax.plot([x, x], [10, 13], color=INK, lw=0.25 * MM)
        ax.plot([x, x], [284, 287], color=INK, lw=0.25 * MM)
    return fig, ax


def third_angle_symbol(ax, x, y, s=1.0):
    ax.add_patch(Polygon([[x, y + 1.3 * s], [x + 8 * s, y + 0.5 * s], [x + 8 * s, y + 3.5 * s], [x, y + 2.7 * s]],
                         closed=True, fill=False, lw=0.3 * MM, zorder=13))
    ax.add_patch(Circle((x + 13 * s, y + 2 * s), 1.5 * s, fill=False, lw=0.3 * MM, zorder=13))
    ax.add_patch(Circle((x + 13 * s, y + 2 * s), 0.7 * s, fill=False, lw=0.3 * MM, zorder=13))
    ax.plot([x - 1, x + 9.5 * s], [y + 2 * s] * 2, lw=0.15 * MM, color=INK, ls=(0, (4, 1, 1, 1)), zorder=13)
    ax.plot([x + 13 * s - 2.5, x + 13 * s + 2.5], [y + 2 * s] * 2, lw=0.15 * MM, color=INK, zorder=13)
    ax.plot([x + 13 * s] * 2, [y + 2 * s - 2.5, y + 2 * s + 2.5], lw=0.15 * MM, color=INK, zorder=13)


def title_block(ax, title, dwg, sheet, nsheets, scale):
    x0, y0, w, h = 230, 10, 180, 38
    ax.add_patch(Rectangle((x0, y0), w, h, fill=True, fc="white", lw=0.5 * MM, ec=INK, zorder=10))
    rows = [y0 + 30, y0 + 22, y0 + 14, y0 + 7]
    for y in rows:
        ax.plot([x0, x0 + w], [y, y], color=INK, lw=0.25 * MM, zorder=11)
    for x in (x0 + 60, x0 + 120):
        ax.plot([x, x], [y0, y0 + 14], color=INK, lw=0.25 * MM, zorder=11)
    ax.plot([x0 + 135, x0 + 135], [y0 + 14, y0 + 30], color=INK, lw=0.25 * MM, zorder=11)
    t = dict(zorder=12, va="center")
    logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qutas-logo.png")
    if os.path.exists(logo):
        img = plt.imread(logo)
        lh = 6.8
        lw = lh * img.shape[1] / img.shape[0]
        ax.imshow(img, extent=(x0 + 2, x0 + 2 + lw, y0 + 30.6, y0 + 30.6 + lh), zorder=12,
                  interpolation="antialiased")
        ax.text(x0 + 4.5 + lw, y0 + 34, "QUT AEROSPACE SOCIETY  -  BELIEVER UAV", fontsize=8,
                weight="bold", **t)
        ax.set_xlim(0, 420)
        ax.set_ylim(0, 297)
    else:
        ax.text(x0 + 2, y0 + 34, "QUT AEROSPACE SOCIETY  -  BELIEVER UAV", fontsize=8, weight="bold", **t)
    ax.text(x0 + w - 2, y0 + 34, "CONCEPT", fontsize=8, weight="bold", color=KEEP, ha="right", **t)
    ax.text(x0 + 2, y0 + 26, "LAUNCH DOLLY", fontsize=6, color="#555", **t)
    ax.text(x0 + 2, y0 + 18.5, title, fontsize=9.5, weight="bold", **t)
    ax.text(x0 + 137, y0 + 26, "DWG No.", fontsize=5, color="#555", **t)
    ax.text(x0 + 137, y0 + 18.5, dwg, fontsize=9.5, weight="bold", **t)
    cells = [(x0 + 2, f"SCALE  {scale}  (A3)"), (x0 + 62, f"SHEET  {sheet} OF {nsheets}"),
             (x0 + 122, f"REV {REV}   {DATE}")]
    for x, s in cells:
        ax.text(x, y0 + 10.5, s, fontsize=6.5, **t)
    ax.text(x0 + 2, y0 + 3.5, "UNITS mm  |  ANGLES deg", fontsize=6, **t)
    ax.text(x0 + 62, y0 + 3.5, "GENERATED: dolly_drawings.py", fontsize=5.5, **t)
    ax.text(x0 + 122, y0 + 3.5, "PROJECTION", fontsize=5.5, **t)
    third_angle_symbol(ax, x0 + 148, y0 + 1.6, 0.85)
    # assumption flag strip
    ax.add_patch(Rectangle((x0, y0 + h), w, 6, fc="#fff3cd", ec=INK, lw=0.25 * MM, zorder=10))
    ax.text(x0 + 2, y0 + h + 3, "Airframe dims marked ASSUMED are not yet measured - verify before cutting tube.",
            fontsize=5.6, zorder=12, va="center")


def view_label(ax, x, y, text, sub=None):
    ax.text(x, y, text, fontsize=8, weight="bold", ha="center", va="top")
    if sub:
        ax.text(x, y - 4, sub, fontsize=6, ha="center", va="top", color="#444")


# ---------------------------------------------------------------- dimensions
def _arrow(ax, a, b, color=INK):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="<|-|>", lw=0.25 * MM, color=color,
                                                    mutation_scale=5, shrinkA=0, shrinkB=0))


def dim_h(ax, p1, p2, y, text, color=INK, fs=6.2, above=True):
    """Horizontal dimension between sheet points p1, p2 with dim line at sheet y."""
    for q in (p1, p2):
        s = np.sign(y - q[1]) or 1
        ax.plot([q[0], q[0]], [q[1] + s * 1.0, y + s * 1.5], color=color, lw=0.18 * MM)
    _arrow(ax, (p1[0], y), (p2[0], y), color)
    ax.text((p1[0] + p2[0]) / 2, y + (0.8 if above else -0.8), text, fontsize=fs, ha="center",
            va="bottom" if above else "top", color=color,
            bbox=dict(fc="white", ec="none", pad=0.15) if not above else None)


def dim_v(ax, p1, p2, x, text, color=INK, fs=6.2, left=True):
    for q in (p1, p2):
        s = np.sign(x - q[0]) or 1
        ax.plot([q[0] + s * 1.0, x + s * 1.5], [q[1], q[1]], color=color, lw=0.18 * MM)
    _arrow(ax, (x, p1[1]), (x, p2[1]), color)
    ax.text(x + (-0.8 if left else 0.8), (p1[1] + p2[1]) / 2, text, fontsize=fs, rotation=90,
            ha="right" if left else "left", va="center", color=color)


def leader(ax, xy, xytext, text, color=INK, fs=6.2, ha="left"):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=fs, color=color, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-|>", lw=0.2 * MM, color=color, mutation_scale=5,
                                shrinkA=1, shrinkB=0))


def balloon(ax, xy, xytext, label, color=INK):
    ax.annotate("", xy=xy, xytext=xytext,
                arrowprops=dict(arrowstyle="-", lw=0.2 * MM, color=color, shrinkA=3.2, shrinkB=0))
    ax.plot(*xy, marker="o", ms=1.2, color=color)
    ax.add_patch(Circle(xytext, 3.2, fc="white", ec=color, lw=0.3 * MM, zorder=6))
    ax.text(*xytext, label, ha="center", va="center", fontsize=6, weight="bold", zorder=7)


def table(ax, x, y, cols, rows, widths, fs=5.8, rh=4.2, header_fc="#e9eef3"):
    """Draw a simple ruled table; (x, y) = top-left. Returns bottom y."""
    W = sum(widths)
    ax.add_patch(Rectangle((x, y - rh), W, rh, fc=header_fc, ec=INK, lw=0.25 * MM))
    cx = x
    for c, w in zip(cols, widths):
        ax.text(cx + 1, y - rh / 2, c, fontsize=fs, weight="bold", va="center")
        cx += w
    yy = y - rh
    for r in rows:
        fill = None
        if isinstance(r, dict):
            fill, r = r.get("fill"), r["cells"]
        ax.add_patch(Rectangle((x, yy - rh), W, rh, fc=fill or "white", ec=INK, lw=0.15 * MM))
        cx = x
        for c, w in zip(r, widths):
            ax.text(cx + 1, yy - rh / 2, str(c), fontsize=fs, va="center")
            cx += w
        yy -= rh
    cx = x
    for w in widths[:-1]:
        cx += w
        ax.plot([cx, cx], [y, yy], color=INK, lw=0.15 * MM)
    return yy


def notes(ax, x, y, lines, fs=6.0, lh=3.4, title="NOTES"):
    ax.text(x, y, title, fontsize=7, weight="bold", va="top")
    yy = y - 4.5
    for i, ln in enumerate(lines, 1):
        first = True
        for chunk in ln.split("\n"):
            ax.text(x, yy, (f"{i}." if first else "") , fontsize=fs, va="top")
            ax.text(x + 4, yy, chunk, fontsize=fs, va="top")
            yy -= lh
            first = False
    return yy


def fmt(v, d=0):
    return f"{v:.{d}f}"


# ---------------------------------------------------------------- build everything
def build():
    t0 = time.time()
    ac = dm.build_aircraft()
    D = dm.solve_and_build(ac)
    rest = da.posed_aircraft(ac, D, "rest")
    rel = da.posed_aircraft(ac, D, "release")
    parts = D.all_parts()
    m_d, tube_total, n_fit = dm.dolly_mass(D)
    cg = da.dolly_cg(D)
    hist = da.launch_sim(m_d)
    R = {
        "prop": da.prop_clearance(ac, D),
        "rest": da.rest_checks(ac, D),
        "m_d": m_d, "tube_total": tube_total, "dolly_cg": cg,
        "hist": hist,
        "pitch_margin": da.pitch_over_margin(D, m_d, cg[0], cg[2], hist),
        "ride_table": da.ride_up_table(m_d),
        "alpha_stall": da.alpha_stall(),
    }
    print("checks done", round(time.time() - t0, 1), "s")
    R["sweep"] = (da.separation_sweep(ac, D, slope=0.25, step=50) if os.environ.get("ALL_SHEETS")
                  else [])
    os_prop = da.min_dist({k: v for k, v in rest.items() if k.startswith("prop_")},
                          {k: v for k, v in parts.items() if k.startswith("tube_OS")})
    R["strut_prop"] = os_prop
    # closest prop point pair (rest) for the callout
    pk = R["prop"]["rest"]
    R["prop_pts"] = da.closest_points(rest[pk[1]], parts[pk[2]])
    return ac, D, rest, rel, parts, R


# ---------------------------------------------------------------- sheet 1: concept isometric
def sheet1(ac, D, rest, rel, parts, R):
    fig, ax = new_sheet()
    title_block(ax, "CONCEPT ISOMETRIC", "BLV-DOL-001", 1, 1, "NTS")
    g = D.geo

    # big iso: dolly only, rear-starboard-above (ramp faces and pads visible)
    view = "iso_rr"
    uv = np.vstack([proj(view, q.BoundingBox().center.toTuple()) for q in parts.values()])
    anchor = uv.mean(axis=0)
    s1 = 0.16
    tf1 = lambda q: np.array([128, 192]) + s1 * (np.atleast_2d(q) - anchor)
    shaded(ax, parts, view, tf1, part_color)
    vis, _ = hlr(parts.values(), view, "dolly")
    ax.add_collection(LineCollection([tf1(q) for q in vis], colors="#222", linewidths=0.18 * MM, zorder=3))
    view_label(ax, 130, 278, "DOLLY - ISOMETRIC (REAR, STARBOARD, ABOVE)", "aircraft removed for clarity")

    def P1(p3):
        return tf1(proj(view, p3))[0]

    lab = [("ramp_head_R", "1", (14, 26)), ("pad_R", "2", (36, 24)), ("tube_SAD-R", None, None),
           ("tail_cradle", "3", (-30, -20)), ("tube_RX", "4", (-38, -6)), ("tube_RA3-R", "5", (30, -20)),
           ("tube_BR-L", "6", (-38, 2)), ("tube_OUT-L", "7", (-8, 32)), ("wheel_OL", "8", (-24, 22)),
           ("fit_BR", "9", (12, -18)), ("tube_UPR-R", "10", (44, 12)), ("tube_FX-R", "11", (24, -26)),
           ("tube_OS-L", "12", (22, 30))]
    for k, l, off in lab:
        if l is None:
            continue
        c = parts[k].Center()
        xy = P1((c.x, c.y, c.z))
        balloon(ax, xy, xy + np.array(off), l)

    legend = [("1", "Ramp head (PETG, TPU face) - front stop; wing must lift to clear lip"),
              ("2", "TPU wing saddle pad on saddle tube, inboard of motor"),
              ("3", "Tail cradle (PETG, TPU pad) on rear cross member"),
              ("4", "Rear cross member (tail support)"),
              ("5", "Rail (each side, under the pads)"),
              ("6", "Outrigger brace"),
              ("7", "Front outrigger - wheels outside prop disc"),
              ("8", f"Wheel {fmt(p('wheel_d'))} mm, grass tyre (x4)"),
              ("9", "Printed fittings (orange), screwed to tube"),
              ("10", "Rear upright (front upright under ramp head)"),
              ("11", "Front cross member (passes under fuselage)"),
              ("12", f"Outrigger strut (vertical truss) to front upright at {p('strut_z'):.0f} mm")]
    yy = 117
    ax.text(18, yy + 6, "ITEMS", fontsize=7, weight="bold")
    for n, t in legend:
        ax.add_patch(Circle((20.5, yy + 0.3), 2.2, fc="white", ec=INK, lw=0.25 * MM))
        ax.text(20.5, yy + 0.3, n, fontsize=5, ha="center", va="center", weight="bold")
        ax.text(25, yy, t, fontsize=6, va="center")
        yy -= 4.5

    # small iso: dolly + aircraft phantom, front-port-above
    view2 = "iso_fl"
    allp = list(parts.values()) + list(rest.values())
    uv2 = np.vstack([proj(view2, q.BoundingBox().center.toTuple()) for q in allp])
    anchor2 = proj(view2, (250, 0, 250))[0]
    s2 = 0.1
    tf2 = lambda q: np.array([322, 212]) + s2 * (np.atleast_2d(q) - anchor2)
    shaded(ax, parts, view2, tf2, part_color, tol=1.0)
    vis2, _ = hlr([v for k, v in rest.items() if not k.startswith("prop_")], view2, "ac_rest", poly=True)
    ax.add_collection(LineCollection([tf2(q) for q in vis2], colors=PHANTOM, linewidths=0.3 * MM,
                                     linestyles=(0, (6, 1.5, 1.5, 1.5)), zorder=5))
    # prop discs as translucent keep-out
    for side in ("L", "R"):
        verts, tris = rest[f"prop_{side}"].tessellate(1.0, 0.3)
        Vt = np.array([[q.x, q.y, q.z] for q in verts])
        uvp = proj(view2, Vt)
        from scipy.spatial import ConvexHull
        hull = ConvexHull(uvp)
        ax.add_patch(Polygon(tf2(uvp[hull.vertices]), closed=True, fc=(0.84, 0.15, 0.16, 0.22),
                             ec=KEEP, lw=0.3 * MM, zorder=6))
    view_label(ax, 330, 278, "ASSEMBLY WITH BELIEVER AT REST", "aircraft envelope = phantom; red = propeller discs (12 in)")
    pr = R["prop"]
    ax.text(330, 150, f"Min. prop-disc to dolly: {pr['rest'][0]:.0f} mm at rest, "
            f"{pr['release'][0]:.0f} mm at release (req. >= {p('prop_margin'):.0f})",
            fontsize=6.3, ha="center", color=KEEP)

    # key data
    W = p("mass_kg") * 9.81
    h = R["hist"]
    kd = [
        ("Wing support", f"2 x TPU saddle at y = +/-{p('pad_y'):.0f}, inboard of motors"),
        ("Resting wing angle", f"{p('alpha_rest'):.1f} deg (underside to ground)"),
        ("Release angle", f"{p('alpha_rel'):.1f} deg (stall approx {R['alpha_stall']:.1f} deg)"),
        ("Ramp lip above wing LE", f"{g['h_lip']:.1f} mm, face {p('ramp_theta'):.0f} deg"),
        ("Est. lift-off speed", f"{h['v'][-1]:.1f} m/s at {p('mass_kg'):.1f} kg"),
        ("Est. ground roll", f"{h['x'][-1]:.0f} m / {h['t'][-1]:.1f} s (Crr {p('Crr'):.2f})"),
        ("Motor shaft height", f"{R['rest']['shaft_z']:.0f} mm (REQ-DOL-11 >= 150)"),
        ("Overall L x W", f"{D.geo['xR'] - p('x_front') + p('wheel_d'):.0f} x "
                          f"{2 * (D.geo['y_out'] + D.geo['axle_out'] + p('wheel_w') / 2):.0f} mm"),
        ("Est. dolly mass", f"{R['m_d']:.1f} kg ({R['tube_total'] / 1000:.1f} m of {p('tube_od'):.0f} mm PVC)"),
    ]
    yb = table(ax, 250, 143, ["KEY DATA", "VALUE"], [list(r) for r in kd], [52, 106], fs=6.0, rh=4.4)

    notes(ax, 18, 60, [
        "Concept: the aircraft sits on two wing saddles and a tail cradle. Thrust pushes the wing\n"
        "leading edge against the ramp heads, so the aircraft pushes the dolly down the runway.",
        "The aircraft cannot leave until wing lift carries most of its weight: it then pivots nose-up on\n"
        "the tail cradle and rides over the ramp lip. Lift-off speed is set by the resting wing angle.",
        "The tail sits on the cradle, so elevator cannot rotate the aircraft on the dolly; rotation comes\n"
        "from wing lift.",
        "All dolly structure stays clear of the 12 in prop discs; front wheels sit outboard of the discs.",
    ], fs=5.9, lh=3.3)
    return fig


# ---------------------------------------------------------------- sheet 2: GA with aircraft (1:10)
def sheet2(ac, D, rest, rel, parts, R):
    fig, ax = new_sheet()
    title_block(ax, "GENERAL ARRANGEMENT WITH AIRCRAFT", "BLV-DOL-002", 2, 5, "1:15")
    s = 1 / 15
    acp = {k: v for k, v in rest.items() if not k.startswith("prop_")}
    props = {k: v for k, v in rest.items() if k.startswith("prop_")}
    g = D.geo

    # side (principal) - anchor model x=0, z=0 at sheet (255, 70)
    sv = View(ax, "side", s, (300, 66), (0, 0))
    sv.draw(acp.values(), "ac_rest", lw=0.3, color=PHANTOM, ls=(0, (6, 1.5, 1.5, 1.5)), poly=True)
    sv.draw(parts.values(), "dolly", lw=0.4)
    sv.draw(props.values(), "props_rest", lw=0.35, color=KEEP, poly=True)
    ax.plot([sv.pt((-420, 0, 0))[0], sv.pt((820, 0, 0))[0]], [66, 66], color=INK, lw=0.35 * MM)
    ax.text(sv.pt((820, 0, 0))[0] + 2, 66, "GROUND", fontsize=5.5, ha="left", va="center")
    view_label(ax, 300, 62.5, "SIDE ELEVATION (FROM PORT)")

    # plan - above side, aligned in x
    pv = View(ax, "plan", s, (300, 178), (0, 0))
    pv.draw(acp.values(), "ac_rest", lw=0.3, color=PHANTOM, ls=(0, (6, 1.5, 1.5, 1.5)), poly=True)
    pv.draw(parts.values(), "dolly", lw=0.4)
    pv.draw(props.values(), "props_rest", lw=0.35, color=KEEP, poly=True)
    # prop keep-out bands in plan
    xp = -p("prop_ahead_LE")
    Rr = p("prop_d") / 2
    for sg in (-1, 1):
        ym = sg * p("motor_y")
        a = pv.pt((xp - 25, ym - Rr - p("prop_margin"), 0))
        b = pv.pt((xp + 25, ym + Rr + p("prop_margin"), 0))
        ax.add_patch(Rectangle(a, b[0] - a[0], b[1] - a[1], fc=(0.84, 0.15, 0.16, 0.12), ec="none", zorder=1))
    view_label(ax, 300, 254, "PLAN", "red band = prop disc + required margin (spanwise)")

    # end view - left of side, aligned in z
    ev = View(ax, "end", s, (120, 66), (0, 0))
    ev.draw(acp.values(), "ac_rest", lw=0.3, color=PHANTOM, ls=(0, (6, 1.5, 1.5, 1.5)), poly=True)
    ev.draw(parts.values(), "dolly", lw=0.4)
    ev.draw(props.values(), "props_rest", lw=0.35, color=KEEP, poly=True)
    ax.plot([ev.pt((0, 1050, 0))[0], ev.pt((0, -1050, 0))[0]], [66, 66], color=INK, lw=0.35 * MM)
    view_label(ax, 120, 62.5, "FRONT VIEW (FROM AHEAD)")

    # --- dimensions
    # plan: span and motor station
    tipL, tipR = pv.pt((0, -p("span") / 2, 0)), pv.pt((0, p("span") / 2, 0))
    dim_v(ax, tipL, tipR, pv.pt((-400, 0, 0))[0] - 8, f"SPAN {p('span'):.0f}")
    mR = pv.pt((xp, p("motor_y"), 0))
    c0 = pv.pt((xp, 0, 0))
    dim_v(ax, c0, mR, pv.pt((-400, 0, 0))[0] + 3, f"{p('motor_y'):.0f} ASSUMED", left=False, color="#a15c00")
    yo = g["y_out"] + g["axle_out"] + p("wheel_w") / 2
    wL, wR = pv.pt((p("x_front"), -yo, 0)), pv.pt((p("x_front"), yo, 0))
    dim_v(ax, wL, wR, pv.pt((800, 0, 0))[0] + 6, f"DOLLY {2 * yo:.0f}", left=False)
    dim_h(ax, ev.pt((0, p("span") / 2, 0)), ev.pt((0, -p("span") / 2, 0)), ev.pt((0, 0, 0))[1] + 48,
          f"SPAN {p('span'):.0f}")
    # side: shaft height, LE height, disc bottom
    sh = R["rest"]["shaft_z"]
    psh = sv.pt((xp, 0, sh))
    dim_v(ax, sv.pt((xp, 0, 0)), psh, psh[0] - 14, f"SHAFT {sh:.0f}")
    pLE = sv.pt((0, 0, g["z0"]))
    dim_v(ax, sv.pt((0, 0, 0)), pLE, sv.pt((-600, 0, 0))[0], f"WING LE {g['z0']:.0f}")
    # closest prop approach
    pa, pb, dd = R["prop_pts"]
    for vw in (sv, pv, ev):
        a_, b_ = vw.pt(pa), vw.pt(pb)
        ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=KEEP, lw=0.45 * MM, zorder=8)
        ax.plot(*a_, "o", ms=1.5, color=KEEP, zorder=8)
    a_ = ev.pt(pa)
    leader(ax, a_, (a_[0] + 10, a_[1] + 62), f"MIN PROP CLEARANCE {dd:.0f}\n(disc to ramp head, 3D)",
           color=KEEP)

    # clearance table
    pr, rc = R["prop"], R["rest"]
    sw = [r for r in R["sweep"] if r[0] >= 50]
    swmin = min(sw, key=lambda r: r[1])
    ok = lambda b: "OK" if b else "CHECK"
    rows = [
        ["Prop disc to dolly, at rest", f"{pr['rest'][0]:.0f}", f">= {p('prop_margin'):.0f}", ok(pr['rest'][0] >= p('prop_margin'))],
        ["Prop disc to dolly, at release", f"{pr['release'][0]:.0f}", f">= {p('prop_margin'):.0f}", ok(pr['release'][0] >= p('prop_margin'))],
        ["Motor shaft above ground", f"{rc['shaft_z']:.0f}", ">= 150 (REQ-DOL-11)", ok(rc['shaft_z'] >= 150)],
        ["Prop tip above ground", f"{rc['disc_bottom_z']:.0f}", "> 0", ok(rc['disc_bottom_z'] > 0)],
        ["Belly over base frame", f"{rc['belly_vert'][0]:.0f}", f">= {p('belly_margin'):.0f}", ok(rc['belly_vert'][0] >= p('belly_margin'))],
        ["Fuselage side to pad/ramp", f"{rc['belly'][0]:.0f}", ">= 20", ok(rc['belly'][0] >= 20)],
        ["Separation path, min (1:4 climb)", f"{swmin[1]:.0f}", "> 0", ok(swmin[1] > 0)],
        ["Wing-tip strike roll angle", f"{rc['roll_to_tip_strike_deg']:.1f} deg", "info", ""],
        ["Dolly pitch-over margin", f"{R['pitch_margin']:.2f}", "> 1.0", ok(R['pitch_margin'] > 1)],
    ]
    rows = [{"cells": r, "fill": "#e6f4ea" if r[3] == "OK" else ("#fde2e1" if r[3] == "CHECK" else None)} for r in rows]
    table(ax, 18, 280, ["CLEARANCE CHECK (mm)", "RESULT", "REQUIRED", ""], rows, [52, 18, 30, 12], fs=5.6, rh=4.2)
    notes(ax, 18, 232, [
        "All clearances are minimum 3D distances between\nCAD solids (OpenCascade), not view distances.",
        "Release = aircraft pivoted on the tail cradle to the\nrelease angle. Separation path: from release the\naircraft moves ahead of the dolly rising 1 mm per 4 mm.",
        "Motor station, prop plane, chord and fuselage\ndimensions are ASSUMED (see BLV-DOL-005).",
    ], fs=5.6, lh=3.1)
    return fig


# ---------------------------------------------------------------- sheet 3: dolly 3-view (1:5)
def sheet3(ac, D, rest, rel, parts, R):
    fig, ax = new_sheet()
    title_block(ax, "DOLLY THREE-VIEW", "BLV-DOL-003", 3, 5, "1:10")
    s = 0.1
    g, N = D.geo, D.nodes
    zb, r = g["zb"], p("tube_od") / 2
    sv = View(ax, "side", s, (285, 80), (0, 0))
    pv = View(ax, "plan", s, (285, 190), (0, 0))
    ev = View(ax, "end", s, (130, 80), (0, 0))
    for vw in (sv, ev, pv):
        vw.draw(parts.values(), "dolly", lw=0.4)
    # ground lines + LE datum
    ax.plot([sv.pt((-120, 0, 0))[0], sv.pt((620, 0, 0))[0]], [80, 80], color=INK, lw=0.35 * MM)
    ax.plot([ev.pt((0, 700, 0))[0], ev.pt((0, -700, 0))[0]], [80, 80], color=INK, lw=0.35 * MM)
    for vw, z1, z2 in ((sv, -10, 360),):
        a_, b_ = vw.pt((0, 0, z1)), vw.pt((0, 0, z2))
        ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=PHANTOM, lw=0.25 * MM, ls=(0, (8, 2, 2, 2)))
        ax.text(b_[0] - 1, b_[1] - 1, "WING LE (REST)", fontsize=5, ha="right", va="top", color=PHANTOM)
    a_, b_ = pv.pt((0, -620, 0)), pv.pt((0, 620, 0))
    ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=PHANTOM, lw=0.25 * MM, ls=(0, (8, 2, 2, 2)))
    # wing underside line in side view (phantom)
    ta = math.tan(math.radians(p("alpha_rest")))
    u1, u2 = sv.pt((-20, 0, g["z0"] + 20 * ta)), sv.pt((300, 0, g["z0"] - 300 * ta))
    ax.plot([u1[0], u2[0]], [u1[1], u2[1]], color=PHANTOM, lw=0.3 * MM, ls=(0, (6, 1.5, 1.5, 1.5)))

    # ---- plan dims
    yo_w = g["y_out"] + g["axle_out"] + p("wheel_w") / 2
    top = pv.pt((0, 700, 0))[1]
    dim_v(ax, pv.pt((p("x_front"), -yo_w, 0)), pv.pt((p("x_front"), yo_w, 0)),
          pv.pt((-200, 0, 0))[0], f"{2 * yo_w:.0f} OVER WHEELS")
    dim_v(ax, pv.pt((p("x_front"), -g["y_out"], 0)), pv.pt((p("x_front"), g["y_out"], 0)),
          pv.pt((-110, 0, 0))[0], f"{2 * g['y_out']:.0f} OUTRIGGER C/C")
    dim_v(ax, pv.pt(N["RL"]), pv.pt(N["RR"]), pv.pt((620, 0, 0))[0],
          f"{2 * p('pad_y'):.0f} RAIL C/C", left=False)
    yd = pv.pt((0, 640, 0))[1] + 5
    xs = [("F", p("x_front")), ("M", p("x_pad_rear")), ("B", p("x_brace")), ("R", g["xR"])]
    for (n1, x1), (n2, x2) in zip(xs[:-1], xs[1:]):
        dim_h(ax, pv.pt((x1, p("pad_y"), 0)), pv.pt((x2, p("pad_y"), 0)), yd, f"{x2 - x1:.0f}")
    dim_h(ax, pv.pt((p("x_front"), p("y_out") if False else g["y_out"], 0)), pv.pt((0, g["y_out"], 0)),
          yd + 7, f"{abs(p('x_front')):.0f} TO WING LE")
    dim_h(ax, pv.pt((p("x_front"), p("pad_y"), 0)), pv.pt((g["xR"], p("pad_y"), 0)), yd + 14,
          f"{g['xR'] - p('x_front'):.0f} FRONT TO REAR CROSS C/C")
    view_label(ax, 285 + 25, yd + 26, "PLAN")

    # ---- side dims
    xr_dim = sv.pt((640, 0, 0))[0]
    for z, lab in ((zb, f"{zb:.0f} TUBE C/L"), (g["z0"], f"{g['z0']:.0f} WING LE"),
                   (g["z_lip"], f"{g['z_lip']:.1f} LIP"), (g["pivot"][2], f"{g['pivot'][2]:.0f} TAIL")):
        pass
    dim_v(ax, sv.pt((p("x_front") - 40, 0, 0)), sv.pt((p("x_front") - 40, 0, g["z_lip"])),
          sv.pt((-140, 0, 0))[0], f"{g['z_lip']:.0f} LIP")
    dim_v(ax, sv.pt((0, 0, 0)), sv.pt((0, 0, g["z0"])), sv.pt((-90, 0, 0))[0], f"{g['z0']:.0f} WING LE")
    dim_v(ax, sv.pt((g["xR"], 0, 0)), sv.pt((g["xR"], 0, g["pivot"][2])), sv.pt((g["xR"] + 110, 0, 0))[0],
          f"{g['pivot'][2]:.0f} TAIL CONTACT", left=False)
    dim_v(ax, sv.pt((g["xR"] + 40, 0, 0)), sv.pt((g["xR"] + 40, 0, zb)), sv.pt((g["xR"] + 40, 0, 0))[0] + 3,
          f"{zb:.0f}", left=False)
    leader(ax, sv.pt((p("x_pad_rear") - 40, 0, g["z0"] - (p("x_pad_rear") - 40) * ta)),
           (sv.pt((200, 0, 0))[0] + 10, sv.pt((0, 0, 470))[1]),
           f"PAD TOP FOLLOWS WING UNDERSIDE AT {p('alpha_rest'):.1f} deg")
    view_label(ax, 285 + 25, 72, "SIDE (FROM PORT)")

    # ---- end view dims
    dim_h(ax, ev.pt(N["UFR"]), ev.pt(N["UFL"]), ev.pt((0, 0, 480))[1] + 4,
          f"{2 * p('pad_y'):.0f} PAD C/L")
    dim_h(ax, ev.pt((0, -(p("pad_y") - p("pad_w") / 2), g["z0"])), ev.pt((0, p("pad_y") - p("pad_w") / 2, g["z0"])),
          ev.pt((0, 0, 480))[1] + 11, f"{2 * (p('pad_y') - p('pad_w') / 2):.0f} BETWEEN PADS")
    dim_h(ax, ev.pt((0, p("motor_y") + p("prop_d") / 2, 0)), ev.pt((0, p("motor_y") - p("prop_d") / 2, 0)),
          ev.pt((0, 0, 0))[1] - 7, f"PROP DISC {p('prop_d'):.0f} (ASSUMED STN)", above=False)
    c_ = ev.pt((0, p("motor_y"), R["rest"]["shaft_z"]))
    ax.add_patch(Circle(c_, p("prop_d") / 2 * 0.2, fill=False, ec=KEEP, lw=0.3 * MM, ls=(0, (4, 1.5))))
    c2 = ev.pt((0, -p("motor_y"), R["rest"]["shaft_z"]))
    ax.add_patch(Circle(c2, p("prop_d") / 2 * 0.2, fill=False, ec=KEEP, lw=0.3 * MM, ls=(0, (4, 1.5))))
    ax.text(c_[0], c_[1], "PROP\nDISC", fontsize=5, color=KEEP, ha="center", va="center")
    wc = g["wheel_centres"]["OL"]
    dim_v(ax, ev.pt((0, wc[1], 0)), ev.pt((0, wc[1], p("wheel_d"))), ev.pt((0, wc[1], 0))[0] + 6,
          f"WHEEL {p('wheel_d'):.0f}", left=False)
    view_label(ax, 130, 65, "FRONT (FROM AHEAD)")

    notes(ax, 18, 280, [
        f"Tube: {p('tube_od'):.0f} mm OD PVC. Set tube_od = 25 in dolly_model.py and re-run for 25 mm.",
        "Fittings and ramp heads 3D printed (PETG); pads and ramp faces TPU.",
        "Heights are to the ground with the tyres unloaded.",
        "Hidden detail omitted for clarity; see STEP model for full geometry.",
    ], fs=5.8, lh=3.3)
    return fig


# ---------------------------------------------------------------- sheet 4: launch geometry
def airfoil_section_2d(alpha, zlift, pivot=None, d_alpha=0.0, y=None):
    y = p("pad_y") if y is None else y
    c = p("c_root") + (p("c_tip") - p("c_root")) * abs(y) / (p("span") / 2)
    pts = dm.airfoil(c, p("wing_t"), 80)
    out = [dm.pose_point((x, y, z), alpha, zlift, pivot, d_alpha) for x, z in pts]
    return np.array([[q[0], q[2]] for q in out])


def sheet4(ac, D, rest, rel, parts, R):
    fig, ax = new_sheet()
    title_block(ax, "LAUNCH GEOMETRY AND RAMP", "BLV-DOL-004", 4, 5, "1:5 / 1:1")
    g = D.geo
    s = 0.2
    sv = View(ax, "side", s, (95, 170), (0, 0))
    acp = {k: v for k, v in rest.items() if not k.startswith("prop_")}
    acr = {k: v for k, v in rel.items() if not k.startswith("prop_")}
    sv.draw(acp.values(), "ac_rest", lw=0.3, color=PHANTOM, ls=(0, (6, 1.5, 1.5, 1.5)), poly=True)
    sv.draw(acr.values(), "ac_rel", lw=0.3, color=RELEASE, ls=(0, (3, 1.2)), poly=True)
    sv.draw(parts.values(), "dolly", lw=0.45)
    ax.plot([sv.pt((-380, 0, 0))[0], sv.pt((800, 0, 0))[0]], [170, 170], color=INK, lw=0.35 * MM)
    piv = sv.pt(g["pivot"])
    ax.plot(*piv, "o", ms=3, mfc="white", mec=RELEASE, mew=0.8, zorder=9)
    leader(ax, piv, (piv[0] + 8, piv[1] - 14), "PIVOT: TAIL CRADLE CONTACT", color=RELEASE)
    view_label(ax, 140, 284, "SIDE - REST (PHANTOM) AND RELEASE (BLUE), 1:5")
    ax.text(18, 164, f"REST: wing underside {p('alpha_rest'):.1f} deg", fontsize=6.3, color=PHANTOM)
    ax.text(18, 159.5, f"RELEASE: pivoted +{p('alpha_rel') - p('alpha_rest'):.1f} deg on tail cradle -> "
            f"{p('alpha_rel'):.1f} deg; LE now level with ramp lip", fontsize=6.3, color=RELEASE)
    # detail callout circle
    cA = sv.pt((-8, 0, g["z0"] + 5))
    ax.add_patch(Circle(cA, 9, fill=False, ec=INK, lw=0.3 * MM, ls=(0, (5, 1.5))))
    ax.text(cA[0] - 10, cA[1] + 8, "A", fontsize=8, weight="bold")

    # ---- detail A at 1:1 (2D from model)
    o = np.array([318, 222])            # sheet point for model (x=0, z=z0)
    sc = 1.0
    T = lambda xz: o + sc * (np.atleast_2d(xz) - np.array([0, g["z0"]]))
    clip = lambda a: a[(a[:, 0] > -60) & (a[:, 0] < 75)]
    rest_sec = airfoil_section_2d(p("alpha_rest"), p("z_LE"))
    rel_sec = airfoil_section_2d(p("alpha_rest"), p("z_LE"), g["pivot"], p("alpha_rel") - p("alpha_rest"))
    for sec, col, ls in ((rest_sec, PHANTOM, (0, (6, 1.5, 1.5, 1.5))), (rel_sec, RELEASE, (0, (3, 1.2)))):
        q = sec[(sec[:, 0] < 55)]
        ax.plot(*T(q).T, color=col, lw=0.4 * MM, ls=ls)
    prof = np.array(g["ramp_prof"] + [g["ramp_prof"][0]])
    sp = T(prof)
    ax.add_patch(Polygon(sp, closed=True, fc="#f6c9a6", ec=INK, lw=0.5 * MM, zorder=4))
    # TPU face layer (3 mm) along the face
    A_, L_ = prof[0], prof[1]
    dvec = (L_ - A_) / np.linalg.norm(L_ - A_)
    nvec = np.array([dvec[1], -dvec[0]])
    if nvec[0] > 0:
        nvec = -nvec
    face = np.array([A_, L_, L_ + nvec * 3, A_ + nvec * 3])
    ax.add_patch(Polygon(T(face), closed=True, fc="#555", ec=INK, lw=0.3 * MM, zorder=5))
    # pad + saddle tube section
    nodeF = D.nodes["UFR"]
    r = p("tube_od") / 2
    ta = math.tan(math.radians(p("alpha_rest")))
    xs = np.linspace(prof[:, 0].max() + 3, 55, 2)
    padtop = np.c_[xs, g["z0"] - xs * ta]
    padbot = np.c_[xs, g["z0"] - xs * ta - p("pad_t")]
    ax.add_patch(Polygon(T(np.vstack([padtop, padbot[::-1]])), closed=True, fc="#3b3b3b", ec=INK,
                         lw=0.3 * MM, zorder=3))
    xs2 = np.array([nodeF[0] + 20, 55])
    zc = g["z0"] - xs2 * ta - p("pad_t") - r
    for off in (r, -r):
        ax.plot(*T(np.c_[xs2, zc + off]).T, color=INK, lw=0.45 * MM, zorder=2)
    ax.add_patch(Circle(T([nodeF[0], nodeF[2]])[0], r + p("fit_wall"), fill=False, ec=INK, lw=0.3 * MM,
                        ls=(0, (3, 1.5))))
    # dims on detail
    lipx = prof[1][0]
    dim_v(ax, T([lipx - 12, g["z0"]])[0], T([lipx - 12, g["z_lip"]])[0], T([-52, 0])[0][0],
          f"{g['h_lip']:.1f} LIP")
    ax.plot(*T(np.array([[-55, g["z0"]], [5, g["z0"]]])).T, color=INK, lw=0.15 * MM, ls=(0, (4, 1)))
    # theta arc
    base = T(A_)[0]
    ax.add_patch(Arc(base, 24, 24, theta1=180 - p("ramp_theta"), theta2=180, lw=0.25 * MM))
    ax.plot([base[0] - 14, base[0]], [base[1], base[1]], color=INK, lw=0.15 * MM)
    ax.text(base[0] - 15, base[1] + 5.5, f"{p('ramp_theta'):.0f} deg", fontsize=6, ha="right")
    leader(ax, T([-p("ramp_gap"), g["z0"] + 2])[0], (o[0] + 30, o[1] + 52),
           f"GAP {p('ramp_gap'):.0f} TO LE AT REST")
    leader(ax, T(face.mean(axis=0))[0], (o[0] - 52, o[1] + 40), "TPU FACE 3 mm")
    leader(ax, T([40, g["z0"] - 40 * ta - p("pad_t") / 2])[0], (o[0] + 20, o[1] - 35),
           f"TPU PAD {p('pad_t'):.0f} THK x {p('pad_w'):.0f} WIDE")
    ax.text(o[0] - 72, o[1] - 62, "Chain line = wing section at pad, rest\nBlue dashed = same section at release\n(profile ASSUMED: flat-bottom 12%)", fontsize=5.5, color=PHANTOM, va="top")
    view_label(ax, 340, 284, "DETAIL A - RAMP HEAD AT PAD STATION", "1:1, section at y = pad station")

    # ---- charts
    W = p("mass_kg") * 9.81
    # (1) V_LO vs alpha_rest
    ax1 = fig.add_axes([0.065, 0.075, 0.2, 0.22])
    al = np.linspace(2, 9, 50)
    for m, ls in ((3.8, ":"), (4.0, "-"), (4.2, "--")):
        ax1.plot(al, [da.v_for_lift(a, m * 9.81) for a in al], color=INK, ls=ls, lw=0.9, label=f"{m:.1f} kg")
    ax1.axvline(p("alpha_rest"), color=ORANGE, lw=1)
    ax1.axhspan(11, 13, color="#d9ead3", zorder=0)
    ax1.text(2.2, 12.6, "SRD target 11-13 m/s", fontsize=5.5, color="#38761d")
    ax1.set_xlabel("Resting wing angle (deg)", fontsize=6)
    ax1.set_ylabel("Lift-off speed (m/s)", fontsize=6)
    ax1.set_title("Lift-off speed vs resting angle", fontsize=7, weight="bold")
    ax1.legend(fontsize=5.5, frameon=False)
    ax1.tick_params(labelsize=5.5)
    ax1.grid(alpha=0.3, lw=0.4)
    # (2) ride-up ratio
    ax2 = fig.add_axes([0.33, 0.075, 0.2, 0.22])
    for th, lsx in ((60, ":"), (70, "-."), (80, "-"), (85, "--")):
        h = da.launch_sim(R["m_d"], th)
        ax2.plot(h["v"], h["ride"], lw=1.4 if th == p("ramp_theta") else 0.7, ls=lsx,
                 color=ORANGE if th == p("ramp_theta") else INK, label=f"ramp {th} deg")
    h = R["hist"]
    ax2.plot(h["v"], h["L"] / W, color=RELEASE, lw=0.9, ls="--", label="lift / weight")
    ax2.axhline(1.0, color=KEEP, lw=0.6)
    ax2.text(0.3, 1.02, "climbs ramp above this line", fontsize=5.5, color=KEEP, va="bottom")
    ax2.set_xlabel("Ground speed (m/s)", fontsize=6)
    ax2.set_ylabel("(L + F_ramp cot theta) / W", fontsize=6)
    ax2.set_title("When the aircraft can climb the ramp", fontsize=7, weight="bold")
    ax2.legend(fontsize=5.3, frameon=False, loc="center left")
    ax2.tick_params(labelsize=5.5)
    ax2.set_ylim(0, 1.25)
    ax2.grid(alpha=0.3, lw=0.4)
    # (3) separation sweep
    ax3 = fig.add_axes([0.065, 0.42, 0.0, 0.0])
    ax3.axis("off")
    ax4 = fig.add_axes([0.615, 0.27, 0.17, 0.18])
    sw = np.array([[r_[0], r_[1]] for r_ in R["sweep"]])
    ax4.plot(sw[:, 0], sw[:, 1], color=INK, lw=0.9, marker="o", ms=1.6)
    ax4.axhline(0, color=KEEP, lw=0.6)
    ax4.set_xlabel("Aircraft travel ahead of dolly (mm)", fontsize=6)
    ax4.set_ylabel("Min. aircraft-dolly gap (mm)", fontsize=6)
    ax4.set_title("Separation path (1:4 climb)", fontsize=7, weight="bold")
    ax4.tick_params(labelsize=5.5)
    ax4.grid(alpha=0.3, lw=0.4)

    rt = {r_["theta"]: r_ for r_ in R["ride_table"]}
    ch = rt.get(int(p("ramp_theta")))
    notes(ax, 18, 151, [
        f"Lift-off: on the dolly the tail rests on the cradle, so the aircraft pivots there and the wing\n"
        f"angle stays at the resting angle until lift approx. equals weight. Lift-off speed is therefore set by the\n"
        f"resting angle: {p('alpha_rest'):.1f} deg gives {R['hist']['v'][-1]:.1f} m/s at {p('mass_kg'):.1f} kg "
        f"(Weishaupl CL0/CLa; alpha datum TBD).",
        f"Ramp: thrust pushes the LE into the ramp face. Neglecting friction, the aircraft can climb the face\n"
        f"once L + F_ramp cot(theta) >= W. At {p('ramp_theta'):.0f} deg this first happens at "
        f"{ch['v_ride']:.1f} m/s with lift = {ch['L_over_W'] * 100:.0f}% of weight;\n"
        f"friction raises this. As the LE rides up, the aircraft pivots nose-up on the tail cradle, so lift exceeds weight at the lip.",
        f"Lip height {g['h_lip']:.1f} mm = rise of the LE when pivoting from {p('alpha_rest'):.1f} to "
        f"{p('alpha_rel'):.1f} deg about the tail contact\n(release angle {p('alpha_stall' if False else 'alpha_rel'):.1f} deg vs approx. "
        f"{R['alpha_stall']:.1f} deg stall).",
        f"Thrust model: {p('T_static_N'):.0f} N static falling {p('T_drop_per_ms'):.1f} N per m/s (ASSUMED); "
        f"rolling resistance Crr {p('Crr'):.2f} (ASSUMED).",
    ], fs=5.6, lh=3.05, title="LAUNCH LOGIC")
    return fig


# ---------------------------------------------------------------- sheet 5: cut list / BOM
def sheet5(ac, D, rest, rel, parts, R):
    fig, ax = new_sheet()
    title_block(ax, "FRAME LAYOUT, CUT LIST AND BOM", "BLV-DOL-005", 5, 5, "1:10 (layout)")
    rows, tot = dm.bom(D)
    pv = View(ax, "plan", 0.1, (318, 200), (260, 0))
    # centreline schematic
    for m in D.members:
        a, b = pv.pt(D.nodes[m.a]), pv.pt(D.nodes[m.b])
        vertical = abs(a[0] - b[0]) < 0.01 and abs(a[1] - b[1]) < 0.01
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#999" if m.role.endswith("upright") else INK,
                lw=0.5 * MM)
        if m.mid.endswith("-L") or m.mid in ("FX-L", "RX"):
            mid = (a + b) / 2
            off = np.array([0, -3.2]) if m.role != "wing saddle" else np.array([0, 3.2])
            if m.role.endswith("upright"):
                continue
            ax.text(*(mid + off * 0.8), m.mid.replace("-L", ""), fontsize=5, ha="center", va="center",
                    bbox=dict(fc="white", ec="none", pad=0.2), color="#0b5394")
    for k, c in D.nodes.items():
        q = pv.pt(c)
        if k.startswith("U"):
            continue
        ax.plot(*q, "s", ms=3.2, mfc=ORANGE, mec=INK, mew=0.3)
        if k.endswith("L") or k == "FC":
            ax.text(q[0] + 1.5, q[1] - 2.2, k, fontsize=4.6, color="#a15c00")
    for k in ("OL", "OR", "RL", "RR"):
        wc = D.geo["wheel_centres"][k]
        a = pv.pt(wc - [p("wheel_d") / 2, 0, 0]); b = pv.pt(wc + [p("wheel_d") / 2, 0, 0])
        ax.add_patch(Rectangle((a[0], a[1] - p("wheel_w") * pv.s / 2), b[0] - a[0], p("wheel_w") * pv.s,
                               fc="#333", ec=INK, lw=0.2 * MM))
    ax.text(pv.pt((250, 0, 0))[0], pv.pt((0, 640, 0))[1] + 6,
            "FRAME CENTRELINES - PLAN (uprights UPF/UPR rise at F and M nodes)", fontsize=7,
            weight="bold", ha="center")
    ax.text(pv.pt((250, 0, 0))[0], pv.pt((0, 640, 0))[1] + 2,
            "orange squares = printed fittings; blue = member IDs (L shown, R mirrored)",
            fontsize=5.6, ha="center", color="#444")

    cut_rows = [[r_["id"], r_["role"], r_["qty"], f"{r_['c2c']:.0f}", f"{r_['cut']:.0f}"] for r_ in rows]
    yb = table(ax, 18, 280, ["ID", "MEMBER", "QTY", "C/C", "CUT"], cut_rows, [14, 46, 10, 14, 14], fs=5.8)
    ax.text(18, yb - 3.5, f"Cut = C/C - 2 x {D.geo['stop']:.0f} mm (tube stops {D.geo['stop']:.0f} mm "
            f"from node centre). Total {tot / 1000:.2f} m;", fontsize=5.5)
    ax.text(18, yb - 7, f"buy {math.ceil(tot / 1000 * 1.15 * 2) / 2:.1f} m of {p('tube_od'):.0f} mm PVC "
            f"(15% allowance).", fontsize=5.5)

    fits = dm.fitting_types(D)
    frows = [[f["id"], f["desc"], f["qty"], ", ".join(f"{a}" for a in f["angles"]) or "-"] for f in fits]
    yb2 = table(ax, 18, yb - 12, ["ID", "PRINTED PART", "QTY", "SOCKET ANGLES (deg)"], frows,
                [14, 76, 10, 30], fs=5.6)

    buy = [["Wheel, 150 mm foam/pneumatic, 12 mm bore", "4"],
           ["Axle bolt M8 x 70 + nyloc + 2 washers", "4"],
           ["PVC conduit 32 mm (or 25 mm, re-run model)", f"{math.ceil(tot / 1000 * 1.15 * 2) / 2:.1f} m"],
           ["PETG filament (fittings, ramp heads, cradle)", "approx. 0.6 kg"],
           ["TPU 95A filament (pads, ramp faces, cradle pad)", "approx. 0.15 kg"],
           ["M4 x 16 self-tapping screws, 2 per socket (no solvent cement on PETG)", "approx. 70"]]
    yb3 = table(ax, 18, yb2 - 6, ["PURCHASED ITEM", "QTY"], buy, [104, 26], fs=5.6)
    m_d = R["m_d"]
    ax.text(18, yb3 - 4, f"Estimated dolly mass {m_d:.1f} kg (tube {p('tube_kg_per_m'):.2f} kg/m, "
            f"fitting {p('fitting_kg') * 1000:.0f} g, wheel {p('wheel_kg') * 1000:.0f} g - ASSUMED).",
            fontsize=5.6)

    # parameter table (assumed values to measure)
    ass = [[k, f"{v[0]:g}", v[2]] for k, v in P.items() if v[1] == "ASSUMED"]
    table(ax, 230, 120, ["PARAMETER (ASSUMED)", "VALUE", "MEASURE / CONFIRM"], ass, [42, 16, 122], fs=5.3, rh=3.7)
    return fig


# ---------------------------------------------------------------- exports
def export_step(D, rest, parts):
    cq.exporters.export(cq.Workplane().add(D.compound()), os.path.join(OUT, "believer-dolly-assembly.step"))
    cq.exporters.export(cq.Workplane().add(cq.Compound.makeCompound(list(rest.values()))),
                        os.path.join(OUT, "believer-envelope-at-rest.step"))
    for k in ("ramp_head_R", "tail_cradle", "pad_R"):
        cq.exporters.export(cq.Workplane().add(parts[k]), os.path.join(OUT, f"printed-{k}.step"))
        cq.exporters.export(cq.Workplane().add(parts[k]), os.path.join(OUT, f"printed-{k}.stl"))


def export_results(D, R):
    rows, tot = dm.bom(D)
    res = {
        "parameters": {k: {"value": v[0], "source": v[1], "desc": v[2]} for k, v in P.items()},
        "solved": {"ramp_lip_mm": D.geo["h_lip"], "z_lip": D.geo["z_lip"],
                   "tail_pivot": list(map(float, D.geo["pivot"])),
                   "tail_cradle_height_above_tube": D.geo["tail_cradle_h"]},
        "clearances_mm": {"prop_rest": R["prop"]["rest"][0], "prop_release": R["prop"]["release"][0],
                          "prop_nearest_part": R["prop"]["rest"][2],
                          "shaft_height": float(R["rest"]["shaft_z"]),
                          "prop_tip_height": float(R["rest"]["disc_bottom_z"]),
                          "belly_over_frame": R["rest"]["belly_vert"][0],
                          "fuselage_side_to_pad": R["rest"]["belly"][0],
                          "separation_min_after_50mm": min(r[1] for r in R["sweep"] if r[0] >= 50)},
        "launch": {"v_liftoff_ms": float(R["hist"]["v"][-1]), "ground_roll_m": float(R["hist"]["x"][-1]),
                   "time_s": float(R["hist"]["t"][-1]), "pitch_over_margin": R["pitch_margin"],
                   "alpha_stall_deg": R["alpha_stall"], "ride_up": R["ride_table"]},
        "dolly_mass_kg": R["m_d"], "tube_total_mm": tot,
        "cut_list": rows,
        "separation_sweep": [{"s": r[0], "gap": r[1], "aircraft_part": r[2], "dolly_part": r[3]} for r in R["sweep"]],
    }
    with open(os.path.join(OUT, "dolly-results.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    return res


def main():
    ac, D, rest, rel, parts, R = build()
    sheets = [sheet1, sheet2, sheet3, sheet4, sheet5] if os.environ.get("ALL_SHEETS") else [sheet1]
    with PdfPages(os.path.join(OUT, "BLV-DOL-001-launch-dolly-concept.pdf")) as pdf:
        for i, fn in enumerate(sheets, 1):
            t = time.time()
            fig = fn(ac, D, rest, rel, parts, R)
            pdf.savefig(fig)
            fig.savefig(os.path.join(OUT, f"BLV-DOL-00{i}.png"), dpi=200)
            plt.close(fig)
            print(f"sheet {i} {time.time() - t:.1f}s")
    export_step(D, rest, parts)
    if os.environ.get("ALL_SHEETS"):
        export_results(D, R)
    print("strut to prop disc (3D):", round(R["strut_prop"][0], 1), "mm")
    print("done")


if __name__ == "__main__":
    main()
