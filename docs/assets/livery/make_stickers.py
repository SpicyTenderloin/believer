"""
Believer vinyl sticker helpers: the vector QUTAS icon, the print-and-cut contour,
and SVG / PDF writers (1:1, millimetres). Used by livery_options.py, mockup.py and
print_stickers.py.

Original first-round designs (QUTAS-lettered wingtip, Barlow side marking) were
dropped after review; see AI-context/CHANGELOG.md.

Sticker SVGs have two layers: "Artwork" (filled shapes) and "CutContour"
(magenta 0.25 mm stroke, offset `CONTOUR` mm outside the artwork) for
print-and-cut on white vinyl. Text is converted to outlines.
"""
from __future__ import annotations
import os
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# ---- parameters (mm) ----
NAVY, ORANGE_L, ORANGE_D = "#0A2A5B", "#E98A4A", "#D66521"
CONTOUR = 2.5          # cut line offset outside the artwork

# ---- QUTAS icon: six triangles measured from the supplied logo (900 px frame) ----
_L = {  # left half; right half mirrored about x = 449.5
    ORANGE_L: [(438, 92), (185, 545), (438, 228)],
    ORANGE_D: [(438, 228), (185, 545), (438, 408)],
    NAVY:     [(185, 545), (438, 408), (185, 738)],
}
_X0, _Y0, _Y1 = 185.0, 92.0, 738.0


def icon(height, x=0.0, y=0.0):
    """List of (colour, Polygon); bottom-left of the icon at (x, y), y up, in mm."""
    s = height / (_Y1 - _Y0)
    out = []
    for col, tri in _L.items():
        for mirror in (False, True):
            pts = [((899 - px) if mirror else px, py) for px, py in tri]
            out.append((col, Polygon([(x + (px - _X0) * s, y + (_Y1 - py) * s) for px, py in pts])))
    return out


def icon_width(height):
    return (714 - 185) * height / (_Y1 - _Y0)


def contour(shapes):
    u = unary_union([g for _, g in shapes])
    # close the icon's centre gap and letter counters into one smooth outline
    return u.buffer(CONTOUR + 9, join_style=1).buffer(-9, join_style=1)


# ---------------------------------------------------------------- SVG output
def _path_d(geom, H):
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    d = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            c = list(ring.coords)
            d.append("M" + " L".join(f"{x:.3f},{H - y:.3f}" for x, y in c) + " Z")
    return " ".join(d)


def write_svg(path, shapes, cut):
    minx, miny, maxx, maxy = cut.bounds
    pad = 2.0
    shift = (-minx + pad, -miny + pad)
    W, H = maxx - minx + 2 * pad, maxy - miny + 2 * pad
    mv = lambda g: affinity.translate(g, *shift)
    art = "\n".join(f'    <path fill="{c}" fill-rule="evenodd" d="{_path_d(mv(g), H)}"/>' for c, g in shapes)
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="{W:.2f}mm" height="{H:.2f}mm" viewBox="0 0 {W:.3f} {H:.3f}">
  <g id="Artwork" inkscape:groupmode="layer" inkscape:label="Artwork">
{art}
  </g>
  <g id="CutContour" inkscape:groupmode="layer" inkscape:label="CutContour">
    <path fill="none" stroke="#EC008C" stroke-width="0.25" d="{_path_d(mv(cut), H)}"/>
  </g>
</svg>
'''
    with open(path, "w") as f:
        f.write(svg)
    return W, H


def write_pdf_preview(path_pdf, path_png, shapes, cut, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as P
    minx, miny, maxx, maxy = cut.bounds
    W, H = maxx - minx + 4, maxy - miny + 4
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(minx - 2, maxx + 2); ax.set_ylim(miny - 2, maxy + 2); ax.set_aspect("equal"); ax.axis("off")
    for c, g in shapes:
        for p in (g.geoms if isinstance(g, MultiPolygon) else [g]):
            from matplotlib.path import Path
            verts, codes = [], []
            for ring in [p.exterior, *p.interiors]:
                cs = list(ring.coords)
                verts += cs; codes += [Path.MOVETO] + [Path.LINETO] * (len(cs) - 2) + [Path.CLOSEPOLY]
            from matplotlib.patches import PathPatch
            ax.add_patch(PathPatch(Path(verts, codes), fc=c, ec="none"))
    for p in (cut.geoms if isinstance(cut, MultiPolygon) else [cut]):
        xs, ys = p.exterior.xy
        ax.plot(xs, ys, color="#EC008C", lw=0.25 * 72 / 25.4)
    fig.savefig(path_pdf)
    fig.savefig(path_png, dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    ic = icon(100)
    write_svg(os.path.join(OUT, "qutas-icon.svg"), ic, contour(ic))
