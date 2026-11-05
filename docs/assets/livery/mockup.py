"""
Believer livery mockups on a cleaned manufacturer three-view (top and side views only).

Adds the as-flown details from the build: orange tape on the aileron and
ruddervator hinges, nacelles and motor-access strips; the QUTAS logo on the
rear hatch; orange antenna mounts. Then places a wingtip option and a side
code, fitted to the wing and fuselage outlines measured from the drawing.

Writes to ./out/:
  three-view-clean.png            : drawing with dimension lines removed (top + side views)
  mockup-<wingtip>-<font>-<colour>.png
  mockup-board-wingtips.png       : wingtip options A-E on the top view
  mockup-board-side-codes.png     : 6 fonts x navy/orange on the side view

Tape, antenna and hatch-logo positions are approximate, from a photo of the aircraft.
"""
from __future__ import annotations
import os
import math
import textwrap
import numpy as np
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle, FancyBboxPatch
from shapely.ops import unary_union

from make_stickers import icon, NAVY, ORANGE_D, OUT, HERE
from livery_options import wingtip_options, side_code, place, FONTS, TOP_MM_PX, SIDE_MM_PX

TAPE = "#FF6A13"
SRC = os.path.join(HERE, "..", "diagrams", "makeflyeasy-believer-three-view.png")
MIRROR = 1177.0          # top view: x' = MIRROR - x for the starboard side


# ---------------------------------------------------------------- base image
def clean_base():
    img = cv2.imread(SRC)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, sat, v = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
    red = ((h < 12) | (h > 168)) & (sat > 40) & (v > 90)          # includes the pale anti-aliased edges
    mask = cv2.dilate(red.astype(np.uint8) * 255, np.ones((5, 5), np.uint8), 1)
    out = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    # inside the removed area: re-join the black outline where a dashed line crossed it,
    # and whiten everything else (no grey smudges or faint dots left behind)
    near = cv2.dilate(mask, np.ones((9, 9), np.uint8), 1) > 0
    gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    ink = (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) < 110) & (mask == 0)
    out[near & ~ink] = 255
    # where a dashed line ran along the outline (wingtips, nose), redraw the outline across the gap:
    # take the outermost line pixel per row, fit a cubic through the rows either side, draw over the gap
    for (x0, x1, y0, y1, side) in ((195, 240, 360, 460, "min"), (940, 990, 350, 450, "max"),
                                   (1075, 1115, 360, 470, "min")):
        rows, xs = [], []
        for y in range(y0, y1):
            c = np.where(ink[y, x0:x1])[0]
            if c.size:
                rows.append(y); xs.append(x0 + (c.min() if side == "min" else c.max()))
        rows, xs = np.array(rows), np.array(xs)
        gaps = [y for y in range(rows.min(), rows.max()) if y not in set(rows)]
        if not gaps:
            continue
        g0, g1 = min(gaps), max(gaps)
        sel = (rows > g0 - 25) & (rows < g1 + 25)
        p = np.polyfit(rows[sel], xs[sel], 3)
        yy = np.arange(g0 - 2, g1 + 3)
        pts = np.c_[np.polyval(p, yy) + (1 if side == "min" else -1), yy].astype(np.int32)
        cv2.polylines(out, [pts], False, (30, 30, 30), 2, cv2.LINE_AA)
    out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    return out


# ---------------------------------------------------------------- fitted geometry (pixels in the drawing)
# Wing outlines measured column-by-column from the drawing; the starboard wing is drawn
# about 20 px higher than the port wing, so each side has its own fit: y = y0 + k (x - x0)
WING = {
    "port": dict(te=(250, 380.5, -0.080), le=(250, 449.5, 0.0433), hinge=((267, 386.5), (403, 381.4)),
                 tip=205, access=((492, 451.5), (546, 451.5)),
                 nac=[(453, 455), (491, 455), (488, 468), (458, 468)]),
    "stbd": dict(te=(927, 361.5, 0.0267), le=(927, 431.0, -0.0967), hinge=((774, 370.6), (910, 369.3)),
                 tip=972, access=((631, 447.5), (687, 447.5)),
                 nac=[(687, 451), (726, 451), (723, 464), (693, 464)]),
}


def _line(p, x):
    x0, y0, k = p
    return y0 + k * (x - x0)


def fus_top(x):   # side view
    return 380 + 0.0547 * (x - 1415)


def fus_bot(x):
    return 467.5 - 0.204 * (x - 1410)


def wingtip_pose(D_mm, margin_mm=45):
    """Centre of the wingtip marking on each wing: `margin_mm` in from the tip, mid-chord,
    rotated to the local chord midline."""
    r_px = D_mm / 2 / TOP_MM_PX
    out = []
    for side, sgn in (("port", 1), ("stbd", -1)):
        w = WING[side]
        x = w["tip"] + sgn * (margin_mm / TOP_MM_PX + r_px)
        y = (_line(w["te"], x) + _line(w["le"], x)) / 2
        slope = (w["te"][2] + w["le"][2]) / 2
        out.append((x, y, math.degrees(math.atan(-slope))))
    return out


def side_pose(length_mm):
    """Level code centred on the fuselage side between the wing-root fairing (x~1390)
    and the start of the V-tail root (x~1546), clear of the side mount and the tail."""
    x0, x1 = 1390, 1546
    avail = (x1 - x0) * SIDE_MM_PX
    k = min(1.0, 0.92 * avail / length_mm)
    cx = (x0 + x1) / 2
    cy = (fus_top(cx) + fus_bot(cx)) / 2
    return k, (cx, cy, 0.0)


# ---------------------------------------------------------------- build details
def poly(ax, pts, fc, z=4, alpha=0.95, ec="none"):
    ax.add_patch(MPoly(pts, closed=True, fc=fc, ec=ec, lw=0.6, alpha=alpha, zorder=z))


def strip(p0, p1, w):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = (p1 - p0) / np.linalg.norm(p1 - p0)
    n = np.array([-d[1], d[0]]) * w / 2
    return [p0 + n, p1 + n, p1 - n, p0 - n]


def details_top(ax):
    for side in ("port", "stbd"):
        w = WING[side]
        poly(ax, strip(*w["hinge"], 25 / TOP_MM_PX), TAPE)          # aileron hinge
        poly(ax, strip(*w["access"], 22 / TOP_MM_PX), TAPE)         # motor-access strip, inboard LE
        poly(ax, w["nac"], TAPE)                                    # nacelle wrap, LE to motor (measured outline)
    # rear-hatch logo (arrow forward = down the page)
    place(ax, icon(60), TOP_MM_PX, 587, 346, rot=180, z=6)
    # antenna on the spine, and the two side mounts by the hatch
    ax.add_patch(Circle((587, 312), 6, fc=TAPE, ec="#333", lw=0.5, zorder=6))
    ax.add_patch(Circle((587, 312), 2.5, fc="#111", zorder=7))
    for x in (552, 622):
        ax.add_patch(FancyBboxPatch((x - 4, 338), 8, 9, boxstyle="round,pad=0.5", fc=TAPE, ec="#333", lw=0.5, zorder=6))


def details_side(ax):
    # ruddervator hinge line on the V-tail
    poly(ax, strip((1650, 401), (1724, 298.5), 20 / SIDE_MM_PX), TAPE)
    # nacelle wrap behind the motor
    poly(ax, [(1185, 368), (1198, 366), (1198, 410), (1185, 411)], TAPE)
    # antenna on the spine
    xa = 1489
    ya = fus_top(xa)
    poly(ax, [(xa - 7, ya + 1), (xa + 7, ya + 1), (xa + 4, ya - 5), (xa - 4, ya - 5)], TAPE, z=6, ec="#333")
    ax.add_patch(FancyBboxPatch((xa - 2, ya - 5 - 44), 4, 44, boxstyle="round,pad=0.6", fc="#111", ec="none", zorder=6))


# ---------------------------------------------------------------- rendering
TOP_BOX = (180, 150, 1000, 590)       # x0, y0, x1, y1 of the top view in the drawing
SIDE_BOX = (1060, 240, 1770, 490)


def draw_view(ax, base, box, details, extra):
    x0, y0, x1, y1 = box
    ax.imshow(base, extent=(0, base.shape[1], base.shape[0], 0))
    details(ax)
    extra(ax)
    ax.set_xlim(x0, x1); ax.set_ylim(y1, y0); ax.set_aspect("equal"); ax.axis("off")


def add_wingtips(ax, shapes, D_mm):
    for (x, y, rot) in wingtip_pose(D_mm):
        place(ax, shapes, TOP_MM_PX, x, y, rot=180 + rot, z=6)


CODE_FONT = ("Bebas Neue", "BebasNeue-Regular.ttf")


def centre_mark(key, cap):
    """Centre mark for the side code: option A = bare icon, B-E = that roundel at 1.2 x letter height."""
    if key == "A":
        return None
    opts = dict((lbl[0], sh) for lbl, sh in wingtip_options(D=1.2 * cap))
    return opts[key]


def add_code(ax, font_file, colour, cap=45.0, mark="A"):
    shapes = side_code(font_file, colour, cap, centre=centre_mark(mark, cap))
    u = unary_union([g for _, g in shapes])
    k, (cx, cy, rot) = side_pose(u.bounds[2] - u.bounds[0])
    if k < 1.0:
        cap = cap * k
        shapes = side_code(font_file, colour, cap, centre=centre_mark(mark, cap))
    place(ax, shapes, SIDE_MM_PX, cx, cy, rot=rot, z=6)
    return cap


def full_mockup(base, wt_key="B", colour=("navy", NAVY), font=CODE_FONT):
    opts = dict((lbl[0], (lbl, sh)) for lbl, sh in wingtip_options())
    lbl, shapes = opts[wt_key]
    fig = plt.figure(figsize=(14, 5.2))
    ax1 = fig.add_axes([0.0, 0.02, 0.52, 0.9]); ax2 = fig.add_axes([0.53, 0.12, 0.47, 0.75])
    draw_view(ax1, base, TOP_BOX, details_top, lambda a: add_wingtips(a, shapes, 130))
    cap = {}
    draw_view(ax2, base, SIDE_BOX, details_side,
              lambda a: cap.setdefault("c", add_code(a, font[1], colour[1], mark=wt_key)))
    fig.suptitle(f"Wingtip {lbl.replace(chr(10), ' ')}   |   side code \"QA {wt_key} BLV\" {font[0]}, {colour[0]}, "
                 f"{cap['c']:.0f} mm letters", fontsize=11, weight="bold", x=0.01, ha="left")
    name = f"mockup-{wt_key}-{font[0].split()[0].lower()}-{colour[0]}.png"
    fig.savefig(os.path.join(OUT, name), dpi=170)
    plt.close(fig)
    return name


# ---------------------------------------------------------------- the three option images
DESC = {
    "A": "QUTAS logo on its own, no roundel",
    "B": "Logo inside a navy ring, tips touching the ring",
    "C": "Logo inside navy and orange rings, tips touching the orange ring",
    "D": "Bullseye: navy, white, orange (RAF wartime style)",
    "E": "Bullseye: navy, light orange, dark orange (logo colours)",
}
CENTRE = {"A": "QUTAS logo", "B": "roundel B", "C": "roundel C", "D": "roundel D", "E": "roundel E"}
LETTERS = (("1", "Navy", NAVY), ("2", "Orange", ORANGE_D))


def image_roundels():
    opts = dict((lbl[0], sh) for lbl, sh in wingtip_options())
    fig = plt.figure(figsize=(16, 5.2))
    fig.suptitle("Roundel options", fontsize=16, weight="bold", x=0.012, ha="left", y=0.97)
    for i, key in enumerate("ABCDE"):
        ax = fig.add_axes([0.012 + i * 0.198, 0.22, 0.17, 0.58])
        ax.set_aspect("equal"); ax.axis("off")
        place(ax, opts[key], 1.0, 0, 0)
        ax.set_xlim(-72, 72); ax.set_ylim(72, -72)
        ax.text(0.5, 1.08, key, transform=ax.transAxes, fontsize=22, weight="bold", ha="center", va="bottom")
        ax.text(0.5, -0.06, textwrap.fill(DESC[key], 30), transform=ax.transAxes, fontsize=10.5, ha="center",
                va="top", linespacing=1.3)
    fig.savefig(os.path.join(OUT, "1-roundel-options.png"), dpi=150)
    plt.close(fig)


def image_wingtips(base):
    opts = dict((lbl[0], sh) for lbl, sh in wingtip_options())
    fig = plt.figure(figsize=(16, 8.4))
    fig.suptitle("Wingtip options mockup", fontsize=16, weight="bold", x=0.012, ha="left", y=0.975)
    cells = [(0, 0), (0, 1), (0, 2), (1, 0.5), (1, 1.5)]
    for key, (r, c) in zip("ABCDE", cells):
        ax = fig.add_axes([0.005 + c * 0.333, 0.47 - r * 0.45, 0.325, 0.40])
        draw_view(ax, base, TOP_BOX, details_top, lambda a, s=opts[key]: add_wingtips(a, s, 130))
        ax.text(0.02, 1.0, key, transform=ax.transAxes, fontsize=20, weight="bold", va="bottom")
        ax.text(0.09, 1.012, DESC[key], transform=ax.transAxes, fontsize=10, va="bottom")
    fig.savefig(os.path.join(OUT, "2-wingtip-options-mockup.png"), dpi=150)
    plt.close(fig)


def image_codes(base, font=CODE_FONT):
    fig = plt.figure(figsize=(16, 13.4))
    fig.suptitle("Identification number and roundel options", fontsize=16, weight="bold", x=0.012, ha="left", y=0.985)
    h = 0.92 / 5
    for r, key in enumerate("ABCDE"):
        for c, (n, cname, col) in enumerate(LETTERS):
            ax = fig.add_axes([0.005 + c * 0.5, 0.93 - (r + 1) * h + 0.008, 0.49, h * 0.84])
            cap = {}
            draw_view(ax, base, SIDE_BOX, details_side,
                      lambda a, k=key, cl=col: cap.setdefault("c", add_code(a, font[1], cl, mark=k)))
            ax.text(0.02, 1.0, f"{key}{n}", transform=ax.transAxes, fontsize=18, weight="bold", va="bottom")
            ax.text(0.115, 1.012, f"{cname} letters, {CENTRE[key]} in the centre",
                    transform=ax.transAxes, fontsize=10, va="bottom")
    fig.savefig(os.path.join(OUT, "3-identification-and-roundel-options.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    base = clean_base()
    cv2.imwrite(os.path.join(OUT, "three-view-clean.png"), cv2.cvtColor(base, cv2.COLOR_RGB2BGR))
    image_roundels()
    image_wingtips(base)
    image_codes(base)
