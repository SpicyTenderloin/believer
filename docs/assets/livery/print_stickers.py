"""
Print-ready Believer stickers for every livery option, at 1:1 scale (mm).

Writes to ./out/print/:
  wingtip-<A..E>.svg / .pdf     wingtip roundel options, 130 mm (A: logo 110 mm tall)   qty 2 each
  id-<A1..E2>.svg / .pdf        side identification "QA <mark> BLV", 45 mm letters    qty 2 each
  proof-sheet-A3.pdf            every design at 1:1 with its code, quantity and a 100 mm scale bar (multi-page)

Each SVG/PDF has the artwork plus a magenta (#EC008C) 0.25 mm "CutContour" line
2.5 mm outside the artwork, for print-and-cut on white vinyl. Text is outlined.
Option codes match 1-roundel-options.png and 3-identification-and-roundel-options.png.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.backends.backend_pdf import PdfPages
from shapely.geometry import MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

from make_stickers import write_svg, write_pdf_preview, contour, NAVY, ORANGE_D, HERE
from livery_options import wingtip_options, side_code, ROUNDEL_D
from mockup import centre_mark, CODE_FONT, DESC

OUT = os.path.join(HERE, "out", "print")
os.makedirs(OUT, exist_ok=True)
CAP = 45.0
LETTERS = (("1", "navy", NAVY), ("2", "orange", ORANGE_D))


def designs():
    out = []
    for lbl, shapes in wingtip_options(ROUNDEL_D):
        k = lbl[0]
        out.append((f"wingtip-{k}", f"{k}  wingtip", DESC[k], shapes, 2))
    for k in "ABCDE":
        for n, cname, col in LETTERS:
            sh = side_code(os.path.join(HERE, "fonts", CODE_FONT[1]), col, CAP, centre=centre_mark(k, CAP))
            out.append((f"id-{k}{n}", f"{k}{n}  side ID",
                        f"QA BLV, {cname} letters, {'QUTAS logo' if k == 'A' else 'roundel ' + k} centre", sh, 2))
    return out


def _draw(ax, shapes, cut, dx, dy):
    for c, g in shapes:
        for p in (g.geoms if isinstance(g, MultiPolygon) else [g]):
            verts, codes = [], []
            for ring in [p.exterior, *p.interiors]:
                cs = [(x + dx, y + dy) for x, y in ring.coords]
                verts += cs; codes += [Path.MOVETO] + [Path.LINETO] * (len(cs) - 2) + [Path.CLOSEPOLY]
            ax.add_patch(PathPatch(Path(verts, codes), fc=c, ec="none"))
    for p in (cut.geoms if isinstance(cut, MultiPolygon) else [cut]):
        xs, ys = p.exterior.xy
        ax.plot(np.array(xs) + dx, np.array(ys) + dy, color="#EC008C", lw=0.25 * 72 / 25.4)


def proof_sheet(items):
    """A3 landscape pages at 1:1; designs flow across rows and onto further pages as needed."""
    W, H, m = 420.0, 297.0, 8.0
    gap, rgap = 6.0, 11.0

    def new_page(n):
        fig = plt.figure(figsize=(W / 25.4, H / 25.4))
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")
        ax.text(m, H - m, f"Believer livery - sticker proof sheet {n} (print at 100%, A3)", fontsize=12,
                weight="bold", va="top")
        ax.text(m, H - m - 7, "Magenta = cut line (CutContour, 2.5 mm offset). Print on white vinyl.",
                fontsize=8, va="top")
        ax.plot([W - m - 100, W - m], [H - m - 4] * 2, color="k", lw=1.2)
        for x in (W - m - 100, W - m):
            ax.plot([x, x], [H - m - 6, H - m - 2], color="k", lw=1.2)
        ax.text(W - m - 50, H - m - 7, "100 mm - check after printing", fontsize=7, ha="center", va="top")
        return fig, ax

    pages = 1
    with PdfPages(os.path.join(OUT, "proof-sheet-A3.pdf")) as pdf:
        fig, ax = new_page(pages)
        x, y, rowh = m, H - m - 18, 0.0
        for name, code, desc, shapes, qty in items:
            cut = contour(shapes)
            minx, miny, maxx, maxy = cut.bounds
            w, h = maxx - minx, maxy - miny
            if x + w > W - m:
                x, y, rowh = m, y - rowh - rgap, 0.0
            if y - h - 6 < m:
                pdf.savefig(fig); plt.close(fig); pages += 1
                fig, ax = new_page(pages)
                x, y, rowh = m, H - m - 18, 0.0
            _draw(ax, shapes, cut, x - minx, y - h - miny)
            ax.text(x, y - h - 2, f"{code}  (x{qty})", fontsize=7.5, weight="bold", va="top")
            x += w + gap
            rowh = max(rowh, h)
        pdf.savefig(fig); plt.close(fig)
    return pages


if __name__ == "__main__":
    items = designs()
    for name, code, desc, shapes, qty in items:
        cut = contour(shapes)
        Wmm, Hmm = write_svg(os.path.join(OUT, f"{name}.svg"), shapes, cut)
        write_pdf_preview(os.path.join(OUT, f"{name}.pdf"), os.path.join(OUT, f"{name}.png"), shapes, cut, code)
        os.remove(os.path.join(OUT, f"{name}.png"))
        print(f"{name:12s} {Wmm:6.1f} x {Hmm:5.1f} mm  (incl. 2 mm margin)  {desc}")
    print("proof sheet pages:", proof_sheet(items))
