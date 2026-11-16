"""
A4 sheet of the chosen Believer stickers for printing on home vinyl sticker paper
and cutting by hand.

Reads the 1:1 print files written by print_stickers.py (out/print/wingtip-<X>.svg and
id-<XN>.svg) and lays out one wingtip roundel and two side IDs on an A4 portrait page,
with a thin light-grey cut guide and a 100 mm check bar. The roundel guide is the
print-and-cut outline (a circle 2.5 mm outside the artwork); the side-ID guide is the
convex hull of its outline, so it has no notches between letters and is easy to cut
with a ruler and scissors. Print the sheet twice for the pair of roundels and two spare IDs.

Writes out/print/home-print-A4-<wingtip>-<id>.pdf. Needs only numpy and matplotlib.
"""
from __future__ import annotations
import os
import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path

HERE = os.path.dirname(os.path.abspath(__file__))
PRINT = os.path.join(HERE, "out", "print")

WINGTIP, SIDE_ID = "C", "C1"      # chosen livery (AI-context/project-notes.md, 2026-11-16)
PAGE_W, PAGE_H = 210.0, 297.0     # A4 portrait, mm
GUIDE = "#A0A0A0"                 # cut guide colour
GUIDE_LW = 0.2                    # cut guide width, mm
PAD = 2.0                         # margin print_stickers.py leaves outside the cut line in each SVG


def read_svg(path):
    """(width, height, [(fill, rings)], cut_rings) in the SVG's own mm frame, y down."""
    s = open(path, encoding="utf-8").read()
    w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())

    def rings(d):
        out = []
        for sub in re.findall(r"M([^MZ]+)Z", d):
            pts = [tuple(map(float, p.split(","))) for p in re.split(r"\s*L\s*|\s+", sub.strip()) if p]
            out.append(np.array(pts))
        return out

    art = [(fill, rings(d)) for fill, d in re.findall(r'<path fill="(#[0-9A-Fa-f]{6})"[^>]* d="([^"]+)"', s)]
    cut = rings(re.search(r'stroke="#EC008C"[^>]* d="([^"]+)"', s).group(1))
    return w, h, art, cut


def _signed_area(r):
    x, y = r[:, 0], r[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


def compound(rs, dx, dy):
    """One matplotlib Path with the SVG's even-odd fill: each ring is oriented by how many
    other rings enclose it, so the non-zero rule matplotlib uses gives the same holes."""
    paths = [Path(r) for r in rs]
    verts, codes = [], []
    for i, r in enumerate(rs):
        depth = sum(paths[j].contains_point(r[0]) for j in range(len(rs)) if j != i)
        ccw = _signed_area(r) > 0
        if ccw != (depth % 2 == 0):
            r = r[::-1]
        verts += [(x + dx, y + dy) for x, y in r] + [(0, 0)]
        codes += [Path.MOVETO] + [Path.LINETO] * (len(r) - 1) + [Path.CLOSEPOLY]
    return Path(verts, codes)


def hull(rs):
    """Convex hull of the cut outline: straight edges that are easy to cut by hand."""
    pts = sorted(set(map(tuple, np.vstack(rs))))
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    h = np.array(lower[:-1] + upper[:-1])
    return [np.vstack([h, h[:1]])]


def place(ax, svg, x, y, convex=False):
    """Draw a sticker with the top-left of its cut outline at (x, y) mm on the page."""
    w, h, art, cut = svg
    dx, dy = x - PAD, y - PAD
    for fill, rs in art:
        ax.add_patch(PathPatch(compound(rs, dx, dy), fc=fill, ec="none", lw=0))
    for r in (hull(cut) if convex else cut):
        ax.plot(r[:, 0] + dx, r[:, 1] + dy, color=GUIDE, lw=GUIDE_LW * 72 / 25.4,
                solid_joinstyle="round")
    return w - 2 * PAD, h - 2 * PAD          # cut outline size


def sheet():
    wt = read_svg(os.path.join(PRINT, f"wingtip-{WINGTIP}.svg"))
    sid = read_svg(os.path.join(PRINT, f"id-{SIDE_ID}.svg"))

    fig = plt.figure(figsize=(PAGE_W / 25.4, PAGE_H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, PAGE_W); ax.set_ylim(PAGE_H, 0); ax.set_aspect("equal"); ax.axis("off")

    m = 12.0
    rw, rh = place(ax, wt, m, m)
    iw, ih = sid[0] - 2 * PAD, sid[1] - 2 * PAD
    ix = (PAGE_W - iw) / 2
    y1 = m + rh + 10
    place(ax, sid, ix, y1, convex=True)
    place(ax, sid, ix, y1 + ih + 10, convex=True)

    # notes and a vertical 100 mm check bar beside the roundel
    tx = m + rw + 8
    notes = [
        ("Believer stickers", 9, "bold"),
        (f"Wingtip roundel {WINGTIP} x1", 7, "normal"),
        (f"Side ID {SIDE_ID} x2", 7, "normal"),
        ("Print this sheet twice.", 7, "normal"),
        ("", 7, "normal"),
        ("Print at 100%", 7, "bold"),
        ("(Actual size, not", 7, "normal"),
        ("Fit to page).", 7, "normal"),
        ("Check the bar is", 7, "normal"),
        ("100 mm.", 7, "normal"),
        ("", 7, "normal"),
        ("Laminate, then cut", 7, "bold"),
        ("on the grey line.", 7, "normal"),
    ]
    for i, (t, fs, wgt) in enumerate(notes):
        ax.text(tx, m + 4 + i * 4.2, t, fontsize=fs, weight=wgt, va="top")
    bx, by0 = PAGE_W - m - 2, m + 30
    ax.plot([bx, bx], [by0, by0 + 100], color="k", lw=1.0)
    for yy in (by0, by0 + 100):
        ax.plot([bx - 2, bx + 2], [yy, yy], color="k", lw=1.0)
    ax.text(bx - 3, by0 + 50, "100 mm", fontsize=7, rotation=90, ha="right", va="center")

    name = f"home-print-A4-{WINGTIP}-{SIDE_ID}.pdf"
    fig.savefig(os.path.join(PRINT, name))
    return fig, name


if __name__ == "__main__":
    fig, name = sheet()
    prev = os.environ.get("PREVIEW_PNG")
    if prev:
        fig.savefig(prev, dpi=150)
    plt.close(fig)
    print("wrote", os.path.join("out", "print", name))
