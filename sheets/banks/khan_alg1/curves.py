"""Smooth curves with known features, for the Khan Algebra 1 Unit 8 graph
lessons (8-8, 8-14 to 8-17, ...). (Not a bank.)

A curve is its knots, [(x, y), ...] with x increasing. Between two knots it
eases with a cosine, y = y0 + (y1 - y0)(1 - cos(pi t))/2, so it's level at
every knot and goes straight up or down between them: every relative
maximum or minimum is at a knot, the curve never leaves the knots' range,
and it rises or falls on each piece as its knots say.

    knots(r, a, b, lo, hi, gap)    knots from x = a to b, alternating up and down
    value(ks, x)                   the curve at x
    maxima(ks), minima(ks)         the relative ones: interior knots above (below) both neighbors
    rising(ks, a, b)               +1 increasing on all of a..b, -1 decreasing, 0 neither
    sign_on(ks, a, b)              +1 positive on all of a < x < b, -1 negative, 0 neither
    zeros(ks)                      where the curve crosses (or touches) y = 0
    draw(g, ks, ends)              on a Graph, sampled finely
"""
import math
from fractions import Fraction as F

def knots(r, a, b, lo, hi, gap=(1, 3)):
    """Knots from a to b, x's apart by gap, each a turn: up, down, up, ... (or the reverse)."""
    xs = [a]
    while xs[-1] < b:
        xs.append(min(b, xs[-1] + r.randint(*gap)))
    ys = [r.randint(lo, hi)]
    up = r.random() < 0.5
    for _ in xs[1:]:
        options = [y for y in range(lo, hi + 1) if (y > ys[-1] if up else y < ys[-1])]
        if not options:
            up = not up
            options = [y for y in range(lo, hi + 1) if (y > ys[-1] if up else y < ys[-1])]
        ys.append(r.choice(options))
        up = not up
    return list(zip(xs, ys))

def value(ks, x):
    for (x0, y0), (x1, y1) in zip(ks, ks[1:]):
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + (y1 - y0) * (1 - math.cos(math.pi * t)) / 2
    raise ValueError(f"{x} is outside the curve")

def maxima(ks):
    return [ks[i] for i in range(1, len(ks) - 1) if ks[i][1] > ks[i - 1][1] and ks[i][1] > ks[i + 1][1]]

def minima(ks):
    return [ks[i] for i in range(1, len(ks) - 1) if ks[i][1] < ks[i - 1][1] and ks[i][1] < ks[i + 1][1]]

def rising(ks, a, b):
    """+1 if the curve increases on all of a..b, -1 if it decreases, 0 otherwise (a turn inside, or flat)."""
    dirs = set()
    for (x0, y0), (x1, y1) in zip(ks, ks[1:]):
        if x1 > a and x0 < b:                                   # this piece overlaps a..b
            dirs.add((y1 > y0) - (y1 < y0))
    return dirs.pop() if len(dirs) == 1 else 0

def zeros(ks):
    out = []
    for (x0, y0), (x1, y1) in zip(ks, ks[1:]):
        if y0 == 0:
            out.append(F(x0))
        if (y0 < 0 < y1) or (y1 < 0 < y0):
            t = math.acos(1 - 2 * (0 - y0) / (y1 - y0)) / math.pi
            out.append(x0 + (x1 - x0) * t)
    if ks[-1][1] == 0:
        out.append(F(ks[-1][0]))
    return out

def sign_on(ks, a, b):
    """+1 if the curve is positive on all of a < x < b, -1 if negative, 0 otherwise."""
    if any(a < z < b for z in zeros(ks)):
        return 0
    y = value(ks, (a + b) / 2)
    return (y > 0) - (y < 0)

def draw(g, ks, ends="closed", color="blue", per=24):
    pts = []
    for (x0, y0), (x1, y1) in zip(ks, ks[1:]):
        for k in range(per):
            t = k / per
            pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * (1 - math.cos(math.pi * t)) / 2))
    pts.append(ks[-1])
    return g.polyline(pts, color=color, ends=ends)
