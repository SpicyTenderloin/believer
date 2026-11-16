"""
Stand-alone PNGs of the chosen Believer stickers, for sending to someone who will make them.

Each image is the finished die-cut sticker at actual size: the artwork on a white backing
filled out to the print-and-cut outline (2.5 mm outside the artwork), transparent outside
it, cropped to the outline and saved at 600 dpi so it prints at the right size. Reads the
1:1 print files written by print_stickers.py (out/print/wingtip-<X>.svg and id-<XN>.svg).

Writes out/print/believer-roundel-<X>-<d>mm.png and believer-side-id-<XN>-<w>x<h>mm.png.
Needs only numpy and matplotlib.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch

from home_print_sheet import PRINT, WINGTIP, SIDE_ID, read_svg, compound

DPI = 600


def render(svg_name, out_stem):
    w, h, art, cut = read_svg(os.path.join(PRINT, svg_name))
    pts = np.vstack(cut)
    x0, y0 = pts.min(axis=0)
    x1, y1 = pts.max(axis=0)
    cw, ch = x1 - x0, y1 - y0

    fig = plt.figure(figsize=(cw / 25.4, ch / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1); ax.set_ylim(y1, y0); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(PathPatch(compound(cut, 0, 0), fc="#FFFFFF", ec="none", lw=0))
    for fill, rs in art:
        ax.add_patch(PathPatch(compound(rs, 0, 0), fc=fill, ec="none", lw=0))

    name = f"{out_stem}-{cw:.0f}mm.png" if abs(cw - ch) < 0.5 else f"{out_stem}-{cw:.0f}x{ch:.0f}mm.png"
    fig.savefig(os.path.join(PRINT, name), dpi=DPI, transparent=True)
    plt.close(fig)
    return name


if __name__ == "__main__":
    for svg, stem in ((f"wingtip-{WINGTIP}.svg", f"believer-roundel-{WINGTIP}"),
                      (f"id-{SIDE_ID}.svg", f"believer-side-id-{SIDE_ID}")):
        print("wrote", os.path.join("out", "print", render(svg, stem)))
