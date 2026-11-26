"""Turn the drawings in glyphs.py into a UFO source (sources/AncoHeist-Black.ufo).

Run:  python scripts/generate.py
Then: ./scripts/build.sh   (compiles the UFO into TTF / OTF / WOFF2)
"""
import os
import sys

import ufoLib2
import pathops

sys.path.insert(0, os.path.dirname(__file__))
from shapes import I, rect, move, soften  # noqa: E402
from glyphs import G, CAP, XH, ASC, DESC, DIGIT_ADV  # noqa: E402
from tuning import SOFT_CONVEX, SOFT_CONCAVE  # noqa: E402

FAMILY = "Anco Heist"
STYLE = "Black"
VERSION = (1, 0)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sources", "AncoHeist-Black.ufo")

KERNING = {
    ("A", "V"): -60, ("A", "W"): -50, ("A", "Y"): -60, ("A", "T"): -50,
    ("V", "A"): -60, ("W", "A"): -50, ("Y", "A"): -60, ("T", "A"): -50,
    ("L", "T"): -70, ("L", "V"): -70, ("L", "W"): -60, ("L", "Y"): -70, ("L", "quotesingle"): -70,
    ("P", "A"): -45, ("F", "A"): -40, ("P", "period"): -70, ("P", "comma"): -70,
    ("T", "o"): -55, ("T", "a"): -55, ("T", "e"): -55, ("T", "c"): -55, ("T", "s"): -45,
    ("T", "period"): -60, ("T", "comma"): -60, ("V", "period"): -50, ("Y", "period"): -60,
    ("V", "o"): -35, ("V", "a"): -35, ("V", "e"): -35, ("Y", "o"): -50, ("Y", "a"): -50, ("Y", "e"): -50,
    ("r", "period"): -40, ("r", "comma"): -40, ("v", "period"): -30, ("y", "period"): -30,
    ("f", "f"): -10, ("quoteright", "s"): -30,
}


def to_glyph(path, glyph):
    """Write a pathops Path into a UFO glyph as cubic curves with whole-number points."""
    path.convertConicsToQuads()
    pen = glyph.getPen()
    R = lambda p: (round(p[0]), round(p[1]))  # noqa: E731
    cur = start = None
    open_contour = False
    for verb, pts in path.segments:
        if verb == "qCurveTo" and not open_contour:
            continue
        if verb == "moveTo":
            cur = start = R(pts[0])
            pen.moveTo(cur)
            open_contour = True
        elif verb == "lineTo":
            p = R(pts[0])
            if p != cur:
                pen.lineTo(p)
                cur = p
        elif verb == "curveTo":
            p = [R(x) for x in pts]
            if p[-1] != cur:
                pen.curveTo(*p)
                cur = p[-1]
        elif verb == "qCurveTo":
            for (q, end) in pathops.decompose_quadratic_segment(pts):
                p0 = cur
                c1 = (p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1]))
                c2 = (end[0] + 2 / 3 * (q[0] - end[0]), end[1] + 2 / 3 * (q[1] - end[1]))
                e = R(end)
                if e != cur:
                    pen.curveTo(R(c1), R(c2), e)
                    cur = e
        elif verb in ("closePath", "endPath"):
            if open_contour:
                pen.closePath()
            open_contour = False
            cur = start


def main():
    font = ufoLib2.Font()
    info = font.info
    info.familyName = FAMILY
    info.styleName = STYLE
    info.versionMajor, info.versionMinor = VERSION
    info.unitsPerEm = 1000
    info.capHeight, info.xHeight = CAP, XH
    info.ascender, info.descender = ASC + 190, DESC - 60
    info.openTypeHheaAscender, info.openTypeHheaDescender, info.openTypeHheaLineGap = 950, -260, 0
    info.openTypeOS2TypoAscender, info.openTypeOS2TypoDescender, info.openTypeOS2TypoLineGap = 950, -260, 0
    info.openTypeOS2WinAscent, info.openTypeOS2WinDescent = 1000, 300
    info.openTypeOS2WeightClass = 900
    info.copyright = "Copyright 2026 Mehmet Esat Comlekci"
    info.openTypeNameDesigner = "Mehmet Esat Comlekci"
    info.openTypeNameLicense = "This Font Software is licensed under the SIL Open Font License, Version 1.1."
    info.openTypeNameLicenseURL = "https://openfontlicense.org"
    info.postscriptUnderlinePosition, info.postscriptUnderlineThickness = -150, 80

    order = []
    for name, g in G.items():
        glyph = font.newGlyph(name)
        if g["uni"] is not None:
            glyph.unicodes = [g["uni"]]
        order.append(name)
        path = g["fn"]()
        if path is None:  # space
            glyph.width = 260
            continue
        if g["clip"]:
            x0, y0, x1, y1 = g["clip"]
            path = I(path, rect(x0, y0, x1, y1))
        path = soften(path, SOFT_CONVEX, SOFT_CONCAVE)
        xmin, ymin, xmax, ymax = path.bounds
        if name in ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"):
            ink = xmax - xmin
            shift = round((DIGIT_ADV - ink) / 2 - xmin)
            path = move(path, shift, 0)
            glyph.width = DIGIT_ADV
        else:
            shift = round(g["lsb"] - xmin)
            path = move(path, shift, 0)
            glyph.width = round(xmax + shift + g["rsb"])
        to_glyph(path, glyph)

    font.glyphOrder = order
    font.lib["public.glyphOrder"] = order
    for (l, r), v in KERNING.items():
        if l in font and r in font:
            font.kerning[(l, r)] = v
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    font.save(OUT, overwrite=True)
    print(f"wrote {OUT} with {len(order)} glyphs")


if __name__ == "__main__":
    main()
