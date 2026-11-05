"""
Believer livery options: wingtip roundels and warbird-style side codes.

Writes to ./out/:
  options-wingtip-roundels.png  : 5 wingtip options, each with a to-scale top-view mockup
  options-side-codes.png        : "QA <icon> BLV" in 6 fonts x 2 colours, on the side view to scale

Reuses the vector QUTAS icon and helpers from make_stickers.py.
"""
from __future__ import annotations
import os
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from PIL import Image

from make_stickers import icon, icon_width, NAVY, ORANGE_L, ORANGE_D, OUT, HERE

WHITE = "#FFFFFF"
FONTS = [  # (label, file) - all SIL Open Font License, in ./fonts
    ("Anton", "Anton-Regular.ttf"),
    ("Bebas Neue", "BebasNeue-Regular.ttf"),
    ("Black Ops One", "BlackOpsOne-Regular.ttf"),
    ("Saira Stencil One", "SairaStencilOne-Regular.ttf"),
    ("Stardos Stencil Bold", "StardosStencil-Bold.ttf"),
    ("Allerta Stencil", "AllertaStencil-Regular.ttf"),
]
CODE_CAP = 45.0          # side code letter height (mm)
ROUNDEL_D = 130.0        # wingtip roundel diameter (mm)
IMG = os.path.join(HERE, "out", "three-view-clean.png")          # written by mockup.py (dimension lines removed)
if not os.path.exists(IMG):
    IMG = os.path.join(HERE, "..", "diagrams", "makeflyeasy-believer-three-view.png")
TOP_MM_PX = 1960 / (975 - 205)
SIDE_MM_PX = 1070 / (1750 - 1082)


# ---------------------------------------------------------------- geometry
def text(s, font_file, cap, x=0.0, y=0.0):
    prop = FontProperties(fname=os.path.join(HERE, "fonts", font_file))
    tp = TextPath((0, 0), s, size=100, prop=prop)
    g = None
    for ring in tp.to_polygons(closed_only=True):
        if len(ring) < 3:
            continue
        p = Polygon(ring).buffer(0)
        g = p if g is None else g.symmetric_difference(p)
    capH = TextPath((0, 0), "H", size=100, prop=prop).get_extents().height
    k = cap / capH
    g = affinity.scale(g, k, k, origin=(0, 0))
    return affinity.translate(g, x - g.bounds[0], y)


def side_code(font_file, colour, cap=CODE_CAP, left="QA", right="BLV", centre=None):
    """Code letters either side of a centre mark. `centre` is a list of (colour, geom)
    centred on the origin (e.g. a roundel); default is the bare QUTAS icon."""
    gap = 0.22 * cap
    a = text(left, font_file, cap)
    x = a.bounds[2] + gap
    if centre is None:
        ih = cap * 1.05
        mark = icon(ih, x, -0.025 * cap)
        w = icon_width(ih)
    else:
        u = unary_union([g for _, g in centre])
        w = u.bounds[2] - u.bounds[0]
        mark = [(c, affinity.translate(g, x - u.bounds[0], cap / 2 - (u.bounds[1] + u.bounds[3]) / 2))
                for c, g in centre]
    x += w + gap
    b = text(right, font_file, cap, x)
    return [(colour, a), *mark, (colour, b)]


def disc(r, cx=0, cy=0):
    return Point(cx, cy).buffer(r, resolution=96)


def ring(r_out, r_in):
    return disc(r_out).difference(disc(r_in))


def centred_icon(height):
    sh = icon(height)
    u = unary_union([g for _, g in sh])
    minx, miny, maxx, maxy = u.bounds
    dx, dy = -(minx + maxx) / 2, -(miny + maxy) / 2
    return [(c, affinity.translate(g, dx, dy)) for c, g in sh]


def inscribed_icon(r):
    """Largest icon that fits inside a circle of radius r, centred on x and shifted
    vertically so its extreme points (top tips and outer bottom corners) touch the circle."""
    base = icon(1.0)
    u = unary_union([g for _, g in base])
    cx = (u.bounds[0] + u.bounds[2]) / 2
    pts = np.vstack([np.array(g.exterior.coords) for _, g in base]) - [cx, 0]
    best_s, best_dy = 0.0, 0.0
    for dy in np.linspace(-1.0, 0.0, 1001):          # icon height is 1.0 at this scale
        s = r / np.max(np.hypot(pts[:, 0], pts[:, 1] + dy))
        if s > best_s:
            best_s, best_dy = s, dy
    return [(c, affinity.scale(affinity.translate(g, -cx, best_dy), best_s, best_s, origin=(0, 0)))
            for c, g in base]


def wingtip_options(D=ROUNDEL_D):
    R = D / 2
    opts = []
    opts.append(("A  Logo as is", centred_icon(0.85 * D)))
    opts.append(("B  Roundel: navy ring,\nlogo tips touching the ring",
                 [(WHITE, disc(R)), (NAVY, ring(R, 0.80 * R)), *inscribed_icon(0.80 * R)]))
    opts.append(("C  Roundel: navy + orange rings,\nlogo tips touching the orange ring",
                 [(WHITE, disc(R)), (NAVY, ring(R, 0.84 * R)), (ORANGE_D, ring(0.84 * R, 0.74 * R)),
                  *inscribed_icon(0.74 * R)]))
    opts.append(("D  Bullseye: navy / white / orange\n(RAF Type A style)",
                 [(NAVY, ring(R, 0.6 * R)), (WHITE, ring(0.6 * R, 0.4 * R)), (ORANGE_D, disc(0.4 * R))]))
    opts.append(("E  Bullseye: navy / light orange /\ndark orange (logo colours)",
                 [(NAVY, ring(R, 0.62 * R)), (ORANGE_L, ring(0.62 * R, 0.34 * R)), (ORANGE_D, disc(0.34 * R))]))
    return opts


# ---------------------------------------------------------------- drawing
def patch(ax, geom, colour, tf, z=5, ec="none", lw=0):
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    for p in polys:
        if p.is_empty:
            continue
        verts, codes = [], []
        for r in [p.exterior, *p.interiors]:
            cs = tf(np.array(r.coords))
            verts += list(map(tuple, cs)); codes += [Path.MOVETO] + [Path.LINETO] * (len(cs) - 2) + [Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts, codes), fc=colour, ec=ec, lw=lw, zorder=z))


def place(ax, shapes, mm_px, cx, cy, rot=0.0, z=5):
    u = unary_union([g for _, g in shapes])
    ox, oy = (u.bounds[0] + u.bounds[2]) / 2, (u.bounds[1] + u.bounds[3]) / 2
    a = np.radians(rot)
    def tf(xy):
        x, y = xy[:, 0] - ox, xy[:, 1] - oy
        xr, yr = x * np.cos(a) - y * np.sin(a), x * np.sin(a) + y * np.cos(a)
        return np.c_[cx + xr / mm_px, cy - yr / mm_px]
    for c, g in shapes:
        patch(ax, g, c, tf, z=z, ec="#00000055" if c == WHITE else "none", lw=0.3)


def board_roundels():
    img = np.array(Image.open(IMG).convert("RGB"))
    top = img[150:620, 190:990]
    opts = wingtip_options()
    fig = plt.figure(figsize=(16, 7.6))
    fig.suptitle("Wingtip options  -  roundel diameter %.0f mm (logo-only option %.0f mm tall), shown to scale on the top view"
                 % (ROUNDEL_D, 0.85 * ROUNDEL_D), fontsize=12, weight="bold", x=0.01, ha="left")
    n = len(opts)
    for i, (label, shapes) in enumerate(opts):
        ax = fig.add_axes([0.01 + i * 0.198, 0.50, 0.17, 0.38])
        ax.set_aspect("equal"); ax.axis("off")
        place(ax, shapes, 1.0, 0, 0)
        ax.set_xlim(-75, 75); ax.set_ylim(75, -75)
        ax.set_title(label, fontsize=9.5, loc="left")
        ax2 = fig.add_axes([0.005 + i * 0.198, 0.04, 0.19, 0.40])
        ax2.imshow(top); ax2.axis("off")
        for cx in (258 - 190, 922 - 190):
            place(ax2, shapes, TOP_MM_PX, cx, 405 - 150, rot=180)
    fig.savefig(os.path.join(OUT, "options-wingtip-roundels.png"), dpi=150)
    plt.close(fig)


def board_side_codes():
    img = np.array(Image.open(IMG).convert("RGB"))
    side = img[270:480, 1075:1760]
    fig = plt.figure(figsize=(16, 3.0 * len(FONTS) + 0.8))
    fig.suptitle('Side code "QA ▲ BLV"  -  %.0f mm letters, QUTAS icon as the centre mark, shown to scale on the side view'
                 % CODE_CAP, fontsize=12, weight="bold", x=0.01, ha="left")
    rows = len(FONTS)
    h = 0.93 / rows
    for r, (name, f) in enumerate(FONTS):
        for c, (cname, col) in enumerate((("navy", NAVY), ("orange", ORANGE_D))):
            shapes = side_code(f, col)
            u = unary_union([g for _, g in shapes])
            L = u.bounds[2] - u.bounds[0]
            y0 = 0.93 - (r + 1) * h + 0.005
            # large artwork
            ax = fig.add_axes([0.01 + c * 0.5, y0 + h * 0.52, 0.22, h * 0.42])
            ax.set_aspect("equal"); ax.axis("off")
            place(ax, shapes, 1.0, 0, 0)
            ax.set_xlim(-L / 2 - 5, L / 2 + 5); ax.set_ylim(35, -35)
            ax.set_title(f"{name}  -  {cname}  ({L:.0f} mm long)", fontsize=9, loc="left")
            # on the aircraft
            ax2 = fig.add_axes([0.24 + c * 0.5, y0, 0.25, h * 0.98])
            ax2.imshow(side); ax2.axis("off")
            place(ax2, shapes, SIDE_MM_PX, 1440 - 1075, 420 - 270)
    fig.savefig(os.path.join(OUT, "options-side-codes.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    # Geometry library for mockup.py and print_stickers.py; the option images are made by mockup.py.
    print("Run mockup.py for the option images and print_stickers.py for the print files.")
