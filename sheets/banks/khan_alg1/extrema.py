"""What 8-14 (relative) and 8-15 (absolute maxima and minima) share: a
smooth curve with closed ends (curves.py), and points written as
coordinates. Khan's "mark the points on the graph" is "write the points"
here; the key marks them in red. (Not a bank.)
"""
import re
from ... import gen
from ...graphs import Graph
from . import curves

POINT = re.compile(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)")

def read_points(t):
    return sorted((int(a), int(b)) for a, b in POINT.findall(t.replace("−", "-")))

def written(pts):
    return ", ".join(f"({x}, {y})" for x, y in sorted(pts))

def curve(r):
    ks = curves.knots(r, r.randint(-7, -5), r.randint(5, 7), -7, 7, gap=(2, 3))
    return [list(k) for k in ks]

def graph(ks, marks=()):
    g = Graph(x=(-8, 8), y=(-8, 8), width=5.2)
    curves.draw(g, [tuple(k) for k in ks], ends="closed")
    for x, y in marks:
        g.point(x, y, color="red")
    return g.typst()

def typst(question, ks, marks=()):
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{question}], [{graph(ks, marks)}])"
