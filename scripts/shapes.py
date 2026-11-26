"""Geometry helpers: build glyphs from simple shapes plus boolean operations.

Every helper returns a pathops.Path. Combine them with U (union),
D (difference) and I (intersection). Units are font units (1000 per em).
"""
import math
import pathops
from pathops import Path, PathOp, LineCap, LineJoin

K = 0.5522847498  # cubic Bezier handle length for a quarter circle


def _poly_path(points):
    p = Path()
    p.moveTo(*points[0])
    for pt in points[1:]:
        p.lineTo(*pt)
    p.close()
    return p


def U(*paths):
    out = Path()
    for p in paths:
        if p is None:
            continue
        out = pathops.op(out, p, PathOp.UNION)
    return out


def D(a, *cuts):
    for c in cuts:
        a = pathops.op(a, c, PathOp.DIFFERENCE)
    return a


def I(a, b):
    return pathops.op(a, b, PathOp.INTERSECTION)


def rect(x0, y0, x1, y1):
    return _poly_path([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def poly(*points):
    return _poly_path(list(points))


def rrect(x0, y0, x1, y1, r):
    """Rounded rectangle. r is one radius or a tuple (bottom-left, bottom-right, top-right, top-left)."""
    if not isinstance(r, (tuple, list)):
        r = (r, r, r, r)
    w, h = x1 - x0, y1 - y0
    lim = min(w, h) / 2
    bl, br, tr, tl = (max(0, min(v, lim)) for v in r)
    p = Path()
    p.moveTo(x0 + bl, y0)
    p.lineTo(x1 - br, y0)
    if br:
        p.cubicTo(x1 - br + br * K, y0, x1, y0 + br - br * K, x1, y0 + br)
    p.lineTo(x1, y1 - tr)
    if tr:
        p.cubicTo(x1, y1 - tr + tr * K, x1 - tr + tr * K, y1, x1 - tr, y1)
    p.lineTo(x0 + tl, y1)
    if tl:
        p.cubicTo(x0 + tl - tl * K, y1, x0, y1 - tl + tl * K, x0, y1 - tl)
    p.lineTo(x0, y0 + bl)
    if bl:
        p.cubicTo(x0, y0 + bl - bl * K, x0 + bl - bl * K, y0, x0 + bl, y0)
    p.close()
    return p


def ring(x0, y0, x1, y1, r, wv, wh, ri=None):
    """Hollow rounded box: side walls wv thick, top/bottom walls wh thick.
    ri sets the counter's corner radii (defaults to r minus the wall, min 20)."""
    if not isinstance(r, (tuple, list)):
        r = (r, r, r, r)
    if ri is None:
        ri = tuple(max(v - wv, 20) if v > 0 else 0 for v in r)
    outer = rrect(x0, y0, x1, y1, r)
    inner = rrect(x0 + wv, y0 + wh, x1 - wv, y1 - wh, ri)
    return D(outer, inner)


def disk(cx, cy, r):
    return rrect(cx - r, cy - r, cx + r, cy + r, r)


def diag(xb, yb, xt, yt, w):
    """Straight stroke of perpendicular width w from (xb,yb) to (xt,yt), ends cut horizontally."""
    dx, dy = xt - xb, yt - yb
    L = math.hypot(dx, dy)
    hw = (w / 2) * L / abs(dy)
    return _poly_path([(xb - hw, yb), (xb + hw, yb), (xt + hw, yt), (xt - hw, yt)])


def seg(x0, y0, x1, y1, w):
    """Straight stroke of width w with square (perpendicular) ends."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return _poly_path([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)])


def rotate(p, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    # translate to origin, rotate, translate back
    return p.transform(c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy)


def move(p, dx, dy):
    return p.transform(1, 0, 0, 1, dx, dy)


def mirror_x(p, cx):
    return p.transform(-1, 0, 0, 1, 2 * cx, 0)


def _offset(p, d):
    s = Path(p)
    s.stroke(abs(d) * 2, LineCap.ROUND_CAP, LineJoin.ROUND_JOIN, 4)
    s.convertConicsToQuads()
    if d > 0:
        return pathops.op(p, s, PathOp.UNION)
    return pathops.op(p, s, PathOp.DIFFERENCE)


def soften(p, convex=42, concave=16):
    """Round every corner: concave corners via close (grow then shrink),
    convex corners via open (shrink then grow)."""
    if concave:
        p = _offset(_offset(p, concave), -concave)
    if convex:
        p = _offset(_offset(p, -convex), convex)
    return pathops.simplify(p, clockwise=False)
