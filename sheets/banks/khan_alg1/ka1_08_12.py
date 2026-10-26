"""Khan Algebra 1, Lesson 8-12: Recognize functions from graphs, from the old
app's Alg1_08_12 (twenty-eight of Khan's graphs as screenshots, without
answers).

The figure shows the entire graph of a relationship: does it represent a
function? Yes or No, spread evenly over a sheet. The graphs are Khan's
kinds: a curve, a line, a parabola, separate points, and two pieces that
meet (functions when no x gets two y's: an open dot under a closed one);
a circle, a sideways parabola, a vertical segment, points sharing an x, or
pieces stacked over the same x (not functions).

A problem: dict(type, pieces, choices, answer, source).
    pieces  [{"kind": "seg", "p": [-6, 2], "q": [1, 5], "ends": ["closed", "open"]}, ...]
check() runs the vertical line test on the pieces, exactly: a piece that
has two y's at one x (circle, sideways parabola, vertical segment), two
pieces over the same x's, or two closed ends (or points) one above the
other means not a function.
"""
from fractions import Fraction as F
import math
from ... import gen
from ...gen import need, signed
from ...graphs import Graph, PREAMBLE
from . import courses
from . import curves

NAME = FAMILY = "ka1_08_12"
FIXED = False
TITLE = "Lesson 8-12: Recognize functions from graphs"
INSTRUCTIONS = "Choose 1 answer."
COURSES = courses(8)
CHOICES = ["Yes", "No"]
W = 8                                                            # the window: -8..8

TYPES = [
    dict(key="1", title="Function or Not?",
         look="The entire graph of a relationship.",
         move="The vertical line test: if any vertical line meets the graph more than once, it isn't a function. "
              "Look closely where pieces meet: an open dot doesn't count.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, str(p["pieces"]), p["answer"])

# ------------------------------------------------------------------
# The vertical line test, exactly
# ------------------------------------------------------------------
def span(pc):
    """(a, b, a closed?, b closed?) of x's a single-valued piece covers; None for all x (a line, a parabola)."""
    k = pc["kind"]
    if k in ("line", "parab"):
        return None
    if k == "knots":
        e = pc["ends"]
        return (pc["ks"][0][0], pc["ks"][-1][0], e == "closed", e == "closed")
    if k == "seg":
        (x0, _), (x1, _) = pc["p"], pc["q"]
        c0, c1 = (e == "closed" for e in pc["ends"])
        return (x0, x1, c0, c1) if x0 <= x1 else (x1, x0, c1, c0)
    raise ValueError(k)

def y_at(pc, x):
    k = pc["kind"]
    if k == "line":
        return F(pc["m"]) * x + F(pc["b"])
    if k == "parab":
        return F(pc["a"]) * (x - pc["h"]) ** 2 + pc["k"]
    if k == "seg":
        (x0, y0), (x1, y1) = pc["p"], pc["q"]
        return F(y0) + F(y1 - y0, x1 - x0) * (x - x0)
    if k == "knots":
        for kx, ky in pc["ks"]:
            if kx == x:
                return F(ky)
        return None                                              # between knots: not needed (overlaps decide)
    raise ValueError(k)

def covers(pc, x):
    s = span(pc)
    if s is None:
        return True
    a, b, ca, cb = s
    return a < x < b or (x == a and ca) or (x == b and cb)

def is_function(pieces):
    pts, curves_ = [], []
    for pc in pieces:
        if pc["kind"] in ("circle", "sideways") or pc["kind"] == "vseg" and pc["y0"] != pc["y1"]:
            return False
        if pc["kind"] == "pts":
            pts += [tuple(q) for q in pc["pts"]]
        else:
            curves_.append(pc)
    xs = [x for x, _ in pts]
    if len(set(pts)) != len(set(xs)):                            # two points at one x
        return False
    for i, P in enumerate(curves_):
        for Q in curves_[i + 1:]:
            sp, sq = span(P), span(Q)
            if sp is None or sq is None:
                return False                                     # a whole-window curve and another piece
            lo, hi = max(sp[0], sq[0]), min(sp[1], sq[1])
            if lo < hi:
                return False                                     # stacked over the same x's
            if lo == hi and covers(P, lo) and covers(Q, lo) and y_at(P, lo) != y_at(Q, lo):
                return False                                     # two closed ends, one above the other
    for x, y in pts:
        for P in curves_:
            if covers(P, F(x)) and y_at(P, F(x)) != y:
                return False
    return True

# ------------------------------------------------------------------
# Drawing graphs of each kind
# ------------------------------------------------------------------
def function_graph(r):
    kind = r.choice(("knots", "line", "parab", "pts", "pieces"))
    if kind == "knots":
        return [dict(kind="knots", ks=[list(k) for k in curves.knots(r, -7, 7, -6, 6, gap=(2, 4))],
                     ends=r.choice(("closed", "arrow")))]
    if kind == "line":
        return [dict(kind="line", m=str(F(signed(r, 1, 4), r.randint(1, 3))), b=r.randint(-5, 5))]
    if kind == "parab":
        return [dict(kind="parab", a=str(F(signed(r, 1, 2), r.randint(1, 3))), h=r.randint(-4, 4), k=r.randint(-5, 5))]
    if kind == "pts":
        xs = r.sample(range(-7, 8), r.randint(4, 7))
        return [dict(kind="pts", pts=[[x, r.randint(-7, 7)] for x in sorted(xs)])]
    c = r.randint(-3, 3)                                          # two pieces meeting at x = c
    y1, y2 = r.sample(range(-6, 7), 2)
    left_end = r.choice(("closed", "open"))
    right_end = "open" if left_end == "closed" else r.choice(("closed", "open"))
    return [dict(kind="seg", p=[-7, r.randint(-6, 6)], q=[c, y1], ends=["closed", left_end]),
            dict(kind="seg", p=[c, y2], q=[7, r.randint(-6, 6)], ends=[right_end, "closed"])]

def relation_graph(r):
    kind = r.choice(("circle", "sideways", "vseg", "pts", "stacked", "both_closed"))
    if kind == "circle":
        return [dict(kind="circle", h=r.randint(-3, 3), k=r.randint(-3, 3), r=r.randint(2, 4))]
    if kind == "sideways":
        return [dict(kind="sideways", a=str(F(signed(r, 1, 2), r.randint(1, 3))), h=r.randint(-4, 4), k=r.randint(-3, 3))]
    if kind == "vseg":
        x = signed(r, 2, 6)                                       # off the y-axis, where it would hide
        y0, y1 = sorted(r.sample(range(-6, 7), 2))
        need(y1 - y0 >= 3)
        return [dict(kind="vseg", x=x, y0=y0, y1=y1)]
    if kind == "pts":
        xs = r.sample(range(-7, 8), r.randint(3, 5))
        pts = [[x, r.randint(-7, 7)] for x in xs]
        x = r.choice(xs)
        y = next(v for v in range(-7, 8) if [x, v] not in pts and r.random() < 0.2 or v == 7)
        need([x, y] not in pts)
        return [dict(kind="pts", pts=sorted(pts + [[x, y]]))]
    if kind == "stacked":                                         # two pieces over the same x's
        a = r.randint(-6, -1)
        b = r.randint(a + 3, 6)
        return [dict(kind="seg", p=[a, r.randint(1, 6)], q=[b, r.randint(1, 6)], ends=["closed", "closed"]),
                dict(kind="seg", p=[a + r.randint(0, 2), r.randint(-6, -1)], q=[b + r.randint(-2, 0), r.randint(-6, -1)],
                     ends=["closed", "closed"])]
    c = r.randint(-3, 3)                                          # both ends closed at x = c, different y's
    y1, y2 = r.sample(range(-6, 7), 2)
    return [dict(kind="seg", p=[-7, r.randint(-6, 6)], q=[c, y1], ends=["closed", "closed"]),
            dict(kind="seg", p=[c, y2], q=[7, r.randint(-6, 6)], ends=["closed", "closed"])]

def draw(entry, r, tpl, want=None):
    yes = (want or r.choice("AB")) == "A"
    pieces = function_graph(r) if yes else relation_graph(r)
    need(is_function(pieces) == yes)
    choices, answer = gen.in_order(CHOICES, "Yes" if yes else "No")
    return dict(pieces=pieces, choices=choices, answer=answer)

def check(p):
    try:
        return "checked" if gen.chosen(p) == ["Yes" if is_function(p["pieces"]) else "No"] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1,
                         balance=("AB", lambda k: k[2] if k[0] == NAME and len(k) == 3 else None))

def graph(p):
    g = Graph(x=(-W, W), y=(-W, W), width=5.2)
    for pc in p["pieces"]:
        k = pc["kind"]
        if k == "knots":
            curves.draw(g, [tuple(q) for q in pc["ks"]], ends=pc["ends"])
        elif k == "line":
            g.line(float(F(pc["m"])), pc["b"])
        elif k == "parab":
            a, h, kk = float(F(pc["a"])), pc["h"], pc["k"]
            g.function(lambda x: a * (x - h) ** 2 + kk)
        elif k == "sideways":
            a, h, kk = float(F(pc["a"])), pc["h"], pc["k"]
            g.polyline([(a * (y - kk) ** 2 + h, y) for y in [-12 + i * 0.1 for i in range(241)]])
        elif k == "circle":
            h, kk, rad = pc["h"], pc["k"], pc["r"]
            g.polyline([(h + rad * math.cos(t * math.pi / 60), kk + rad * math.sin(t * math.pi / 60)) for t in range(121)],
                       ends=None)
        elif k == "vseg":
            g.segment((pc["x"], pc["y0"]), (pc["x"], pc["y1"]))
        elif k == "seg":
            g.segment(tuple(pc["p"]), tuple(pc["q"]), ends=tuple(pc["ends"]))
        elif k == "pts":
            for x, y in pc["pts"]:
                g.point(x, y, color="blue")
    return g.typst()

def typst(p, gap="0.3em"):
    left = (f"The figure shows the entire graph of a relationship. Does the graph represent a function? #v(0.3em) "
            f"{gen.choices_typst(p['choices'], 'linear')}")
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{left}], [{graph(p)}])"

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    return f"{p['pieces']}   function?"

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 2.4

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new graph; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
