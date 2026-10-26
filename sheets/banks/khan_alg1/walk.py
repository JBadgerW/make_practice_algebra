"""Graphs through lattice points for the Khan Algebra 1 Unit 8 lessons
(8-2, 8-3, 8-5): a function that steps up and down from one integer x to
the next, drawn as straight pieces. (Not a bank.)

    walk(r, x0, x1, y0, y1)   the y's at x0, x0 + 1, ..., x1 (the old app's weighted steps:
                              mostly up or down 1, sometimes 0 or 2, rarely 3 or 4)
    value(ys, x0, x)          the function at any x (straight between the points)
    solutions(ys, x0, k)      every real x with f(x) = k, as Fractions, or "many" (a flat piece at k)
    draw(g, ys, x0, ...)      the graph on a Graph, closed dots at both ends
"""
from fractions import Fraction as F

STEPS = [(-4, 1), (-3, 2), (-2, 6), (-1, 35), (0, 12), (1, 35), (2, 6), (3, 2), (4, 1)]

def walk(r, x0=-8, x1=8, y0=-8, y1=8):
    lo, hi = y0 + (y1 - y0) // 4, y1 - (y1 - y0) // 4
    ys = [r.randint(lo, hi)]
    deltas, weights = zip(*STEPS)
    for _ in range(x1 - x0):
        y = ys[-1] + r.choices(deltas, weights=weights)[0]
        ys.append(min(max(y, y0 + 1), y1 - 1))                 # the old app's clamp: one inside the edge
    return ys

def value(ys, x0, x):
    x = F(x)
    i = int(x - x0) if x < x0 + len(ys) - 1 else len(ys) - 2
    if not 0 <= x - x0 <= len(ys) - 1:
        raise ValueError(f"{x} is outside the domain")
    t = x - x0 - i
    return ys[i] + (ys[i + 1] - ys[i]) * t

def solutions(ys, x0, k):
    out = set()
    for i, (a, b) in enumerate(zip(ys, ys[1:])):
        if a == b == k:
            return "many"
        if a == k:
            out.add(F(x0 + i))
        if b == k:
            out.add(F(x0 + i + 1))
        if min(a, b) < k < max(a, b):
            out.add(x0 + i + F(k - a, b - a))
    return sorted(out)

def draw(g, ys, x0, color="blue", dash=None):
    return g.polyline([(x0 + i, y) for i, y in enumerate(ys)], color=color, dash=dash, ends="closed")
