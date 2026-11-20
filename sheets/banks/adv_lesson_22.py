"""Lesson 22 (Advanced Math): absolute value, reciprocal functions. From the
Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_022/slides/deck_022.typ): examples
22.1-22.5 and Problem Set 22, problems 6-8.

     1  within k of a (one piece)          {x ∈ ℝ | |x - 5| < 2}                   3 < x < 7
     2  farther than k from a (two rays)   {x ∈ ℝ | |x + 2| >= 3}                  x <= -5 or x >= 1
     3  isolate the absolute value first   |x| - 2 < 0                             -2 < x < 2
     4  sketch an absolute value           y = |x|                                 (-2, 2), (0, 0), (2, 2)
     5  sketch the reciprocal of a square  y = 1/x^2                               x = 0; (-2, 0.25), (-1, 1), ...
     6  sketch the reciprocal of a line    f(x) = x + 3 shown; g(x) = 1/(x + 3)    x = -3; (-2, 1), (-4, -1)

Types 1 and 2 split the heading "graphing absolute value inequalities" by
its picture: less than is one piece between two circles, greater than is two
rays pointing away (problem 6 sets them side by side). Type 3 is example
22.1's extra move, isolating the absolute value before reading the distance.
Types 5 and 6 split "sketching a reciprocal function": example 22.5 is
graphed from a table and never goes below the x axis; problem 8 gives the
line's graph, its points at y = 1 and -1, and the asymptote.

Types 1-3 print a blank number line (the integers it shows are the
problem's `line`, the graph's ends one to three in from its ends), and the
key draws the graph on it. Types 4 and 5 print blank axes and the key draws
the curve through the answer's points. Type 6 prints the line f with its two
dots and the dotted asymptote, as the book does; the key turns f gray and
draws g over it, as the deck does.

Answer conventions, from the deck:
  - One piece: 3 < x < 7, the smaller end first. Two rays: x <= -5 or
    x >= 1, the left ray first. The circles are the signs: < and > open,
    <= and >= solid.
  - A sketch is its marked points. y = |x|: the deck's table, the vertex and
    the points two to each side, left to right: (-2, 2), (0, 0), (2, 2).
  - A reciprocal names its asymptote first: x = 0. Example 22.5's table is
    the points 2, 1, and 0.5 to each side of it, left to right, in decimals
    as the deck writes them: (-2, 0.25), (-1, 1), (-0.5, 4), (0.5, 4),
    (1, 1), (2, 0.25). Problem 8's points are the two the line and its
    reciprocal share, y = 1 first, as the book lists them: (-2, 1), (-4, -1).

check() works from the problem's data, not from how the answer was made:
  1-3   the answer's set read back from its text, and the prompt's
        inequality tested as written at every point where either can
        change (where the two sides are equal, by sympy; the answer's own
        ends), between them, and beyond them: a number is in the answer
        exactly when it makes the inequality true. The answer's form is
        read from its text (one piece, or two rays left first), and the
        graph's ends must be inside the number line.
  4     each point is on the graph; the middle one is the vertex (the graph
        is the same height at equal distances to each side of it, and not
        flat); the others are two to each side.
  5     the asymptote is the one place the function has no value; the six
        points are 2, 1, and 0.5 to each side of it, each on the graph,
        written in decimals.
  6     g is the reciprocal of f (their product is 1 wherever f isn't 0); the
        asymptote is where f is 0; the points are on both graphs, y = 1 then
        y = -1.

No sources are skipped. Lesson 22's proofs (problems 15, 25, 26) are outside
its types, as are the review problems (1-5, 9-30), which other banks cover.

A problem: dict(type, prompt, answer, source), and for Types 1-3 line, the
integers [lo, hi] its number line shows. The prompt is what an edit changes:
    1  "abs(x - 5) < 2"                      "3 < x < 7"
    2  "abs(x + 2) >= 3"                     'x <= -5 "or" x >= 1'
    3  "abs(x) - 2 < 0"                      "-2 < x < 2"
    4  "y = abs(x)"                          "(-2, 2), (0, 0), (2, 2)"
    5  "y = 1/x^2"                           "x = 0; (-2, 0.25), (-1, 1), (-0.5, 4), (0.5, 4), (1, 1), (2, 0.25)"
    6  "f(x) = x + 3; g(x) = 1/(x + 3)"      "x = -3; (-2, 1), (-4, -1)"
"""
import re
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy
from ..graphs import Graph, PREAMBLE as GRAPH_PREAMBLE
from ..typmath import fr, dfrac, text as plain
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_22"
FIXED = False
TITLE = "Lesson 22: Absolute Value, Reciprocal Functions"
INSTRUCTIONS = "Solve each problem."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = GRAPH_PREAMBLE

TYPES = [
    dict(key="1", title="Within k of a Number",
         instructions="Graph each set on the real number line.",
         look="The absolute value of $x$ minus a number is less than $k$.",
         move="$|x - a|$ is the distance from $x$ to $a$. Less than $k$: the numbers within $k$ of $a$, one "
              "piece from $a - k$ to $a + k$. $|x - 5| < 2$ gives $3 < x < 7$. Open circles for $<$, solid "
              "circles for $<=$. Rewrite $|x + 2|$ as $|x - (-2)|$: the center is $-2$.",
         space="0.5in"),
    dict(key="2", title="Farther Than k from a Number",
         instructions="Graph each set on the real number line.",
         look="The absolute value of $x$ minus a number is greater than $k$.",
         move="$|x - a|$ is the distance from $x$ to $a$. Greater than $k$: the numbers farther than $k$ from "
              "$a$, two rays pointing away from $a$. $|x + 2| >= 3$ is $|x - (-2)| >= 3$: $x <= -5$ or $x >= "
              "1$. Open circles for $>$, solid circles for $>=$.",
         space="0.5in"),
    dict(key="3", title="Isolate the Absolute Value First",
         instructions="Graph each inequality on the real number line.",
         look="A number added to or subtracted from the absolute value.",
         move="Get the absolute value alone: $|x| - 2 < 0$ becomes $|x| < 2$. Then read it as a distance: less "
              "than is one piece, greater than is two rays.",
         space="0.6in"),
    dict(key="4", title="Sketch an Absolute Value Function",
         instructions="Sketch the graph of each function.",
         look="$y$ is the absolute value of an expression in $x$.",
         move="Make a table: the $x$ where the inside is $0$, and $2$ to each side. An absolute value is never "
              "negative, so the graph turns back up: a V with its vertex where the inside is $0$.",
         space="0.5in"),
    dict(key="5", title="Sketch the Reciprocal of a Square",
         instructions="Sketch the graph of each function.",
         look="$1$ over a square, like $1/x^2$.",
         move="We can't divide by zero: a vertical asymptote where the bottom is $0$. Make a table $0.5$, $1$, "
              "and $2$ to each side of it. A square is positive, so the graph never goes below the $x$ axis: a "
              "volcano.",
         space="0.9in"),
    dict(key="6", title="Sketch the Reciprocal of a Line",
         instructions="Each graph shows a function f, with dots where y is 1 or -1 and a dotted line where "
                      "f crosses the x axis. Sketch the graph of the reciprocal function g.",
         look="The graph of a line $f$, and $g(x) = 1/f(x)$.",
         move="The reciprocal of $1$ is $1$ and of $-1$ is $-1$: $g$ passes through the dots. Where $f$ "
              "crosses the $x$ axis, $g$ has a vertical asymptote. Where $f$ is large, $g$ is near zero; where "
              "$f$ is near zero, $g$ is large.",
         space="0.7in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
X = sp.Symbol("x")

def initial_seen():
    return set()

def seen_key(p):
    """A function is the same problem whatever it's called: y = |x| and f(x) = |x| are one."""
    return (NAME, p["type"], re.sub(r"^(y|[a-z]\(x\)) = ", "", p["prompt"]) if p["type"] in ("4", "5") else p["prompt"])

def shift(a):
    """x - a as the book writes it: x, x - 5, x + 2."""
    return "x" if a == 0 else f"x - {a}" if a > 0 else f"x + {-a}"

def plus(c):
    return "" if c == 0 else f" + {c}" if c > 0 else f" - {-c}"

# ------------------------------------------------------------------
# Types 1 and 2: |x - a| < k (one piece), |x - a| > k (two rays)
# ------------------------------------------------------------------
CENTER = range(-9, 10)                          # a; 0 is the distance from the origin
CENTERS = [a for a in CENTER if a]
K = range(1, 7)                                 # the distance
LESS, GREATER = ("<", "<="), (">", ">=")

def t1_build(a, k, op):
    return f"abs({shift(a)}) {op} {k}"

t2_build = lambda a, k, op: t1_build(a, k, op)   # its own name: its own signs (RANGES)

def t12_pick(ops, origin):
    def pick(r):
        return dict(a=0 if origin else r.choice(CENTERS), k=r.choice(K), op=r.choice(ops))
    return pick

# ------------------------------------------------------------------
# Type 3: |x - a| + c < d
# ------------------------------------------------------------------
C3 = [c for c in range(-9, 10) if c]            # what's added to the absolute value
D3 = range(-9, 13)                              # the other side

def t3_build(a, c, op, d):
    return f"abs({shift(a)}){plus(c)} {op} {d}"

def t3_zero_pick(r):                            # the book's: zero on the other side, |x| - 2 < 0
    k = r.choice(K)
    return dict(a=r.choice((0, 0) + tuple(CENTERS)), c=-k, op=r.choice(LESS + GREATER), d=0)

def t3_pick(r):
    k, c = r.choice(K), r.choice(C3)
    need(c + k in D3)
    return dict(a=r.choice((0,) + tuple(CENTERS)), c=c, op=r.choice(LESS + GREATER), d=c + k)

# ------------------------------------------------------------------
# Type 4: y = |x|, and its shifts
# ------------------------------------------------------------------
NAMES = ("y", "f", "g", "h")
MOVE4 = [v for v in range(-5, 6) if v]

def left(name):
    return "y" if name == "y" else f"{name}(x)"

def t4_build(name, a, c):
    return f"{left(name)} = abs({shift(a)}){plus(c)}"

def t4_plain_pick(r):                           # the book's: y = |x|, f(x) = |x|
    return dict(name=r.choice(NAMES), a=0, c=0)

def t4_side_pick(r):
    return dict(name=r.choice(NAMES), a=r.choice(MOVE4), c=0)

def t4_up_pick(r):
    return dict(name=r.choice(NAMES), a=0, c=r.choice(MOVE4))

# ------------------------------------------------------------------
# Type 5: y = 1/x^2, and its shifts
# ------------------------------------------------------------------
MOVE5 = [v for v in range(-5, 6) if v]

def t5_build(name, a):
    return f"{left(name)} = 1/" + ("x^2" if a == 0 else f"({shift(a)})^2")

def t5_plain_pick(r):                           # the book's: y = 1/x^2
    return dict(name=r.choice(NAMES), a=0)

def t5_side_pick(r):
    return dict(name=r.choice(NAMES), a=r.choice(MOVE5))

# ------------------------------------------------------------------
# Type 6: f(x) = x + b shown; sketch g(x) = 1/(x + b)
# ------------------------------------------------------------------
B6 = range(-4, 5)                               # f(x) = x + b; 0 is the lesson's y = x and y = 1/x
B6_DOWN = range(1, 5)                           # f(x) = b - x

def t6_build(b, down):
    f = f"{b} - x" if down else shift(-b)
    return f"f(x) = {f}; g(x) = {fr('1', f)}"

def t6_pick(r):
    return dict(b=r.choice(B6), down=False)

def t6_down_pick(r):
    return dict(b=r.choice(B6_DOWN), down=True)

# ------------------------------------------------------------------
# Templates and ranges
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t12_pick(LESS, False), t1_build), (t12_pick(LESS, False), t1_build), (t12_pick(LESS, True), t1_build)],
    "2": [(t12_pick(GREATER, False), t2_build), (t12_pick(GREATER, False), t2_build),
          (t12_pick(GREATER, True), t2_build)],
    "3": [(t3_zero_pick, t3_build), (t3_zero_pick, t3_build), (t3_pick, t3_build)],
    "4": [(t4_plain_pick, t4_build), (t4_side_pick, t4_build), (t4_up_pick, t4_build)],
    "5": [(t5_plain_pick, t5_build), (t5_side_pick, t5_build), (t5_side_pick, t5_build)],
    "6": [(t6_pick, t6_build), (t6_pick, t6_build), (t6_down_pick, t6_build)],
}

RANGES = {
    t1_build: lambda a, k, op: a in CENTER and k in K and op in LESS,
    t2_build: lambda a, k, op: a in CENTER and k in K and op in GREATER,
    t3_build: lambda a, c, op, d: a in CENTER and c in C3 and d in D3 and d - c in K and op in LESS + GREATER,
    t4_build: lambda name, a, c: name in NAMES and a in (0,) + tuple(MOVE4) and c in (0,) + tuple(MOVE4) and not (a and c),
    t5_build: lambda name, a: name in NAMES and a in (0,) + tuple(MOVE5),
    t6_build: lambda b, down: b in B6_DOWN if down else b in B6,
}

def in_range(build, params):
    """Can a random draw pick these parameters for this build?"""
    return RANGES[build](**params)

# ------------------------------------------------------------------
# Reading prompts
# ------------------------------------------------------------------
INEQ = re.compile(r"^abs\((x(?: [+-] \d+)?)\)( [+-] \d+)? (<=|>=|<|>) (-?\d+)$")
FUNC = re.compile(r"^(y|[a-z]\(x\)) = (.+)$")
PAIR = re.compile(r"^f\(x\) = ([^;]+); g\(x\) = ([^;]+)$")
KIND = {"1": "within", "2": "farther", "3": "isolate", "4": "abs", "5": "square", "6": "line"}
NUMBER_LINE = ("1", "2", "3")

def kind(prompt):
    """Which type a prompt is, from how it is written."""
    p = prompt.strip()
    m = INEQ.match(p)
    if m:
        return "isolate" if m.group(2) else "within" if m.group(3) in LESS else "farther"
    if PAIR.match(p):
        return "line"
    if FUNC.match(p):
        return "abs" if "abs(" in p else "square"
    raise ValueError("not a Lesson 22 problem")

def read_function(prompt):
    """(what the prompt calls it, the function as sympy in x) from "y = ..." or "f(x) = ..."."""
    m = FUNC.match(prompt.strip())
    if not m:
        raise ValueError("write it like: y = abs(x)")
    f = to_sympy(m.group(2))
    if f.free_symbols != {X}:
        raise ValueError("the function is in x")
    return m.group(1), f

def read_pair(prompt):
    """(f, g) as sympy from "f(x) = x + 3; g(x) = 1/(x + 3)"."""
    m = PAIR.match(prompt.strip())
    if not m:
        raise ValueError("write it like: f(x) = x + 3; g(x) = 1/(x + 3)")
    f, g = to_sympy(m.group(1)), to_sympy(m.group(2))
    if f.free_symbols != {X} or g.free_symbols != {X}:
        raise ValueError("f and g are in x")
    return f, g

# ------------------------------------------------------------------
# Types 1-3: the answer, and the test of it
# ------------------------------------------------------------------
FLIP = {">": "<", ">=": "<="}

def ends(prompt):
    """(lo, hi, sign) of |x - a| + c op d: the two numbers at distance d - c from a."""
    m = INEQ.match(prompt.strip())
    if not m:
        raise ValueError("write it like: abs(x - 5) < 2")
    inner, c, op, d = m.groups()
    a = -int(inner[1:].replace(" ", "")) if len(inner) > 1 else 0
    k = int(d) - (int(c.replace(" ", "")) if c else 0)
    if k <= 0:
        raise ValueError("the distance must be positive: an absolute value is never negative")
    return a - k, a + k, op

def inequality_answer(prompt):
    lo, hi, op = ends(prompt)
    if op in LESS:
        return f"{lo} {op} x {op} {hi}"
    return f'x {FLIP[op]} {lo} "or" x {op} {hi}'

WITHIN = re.compile(r"^(-?\d+) (<=|<) x (<=|<) (-?\d+)$")
FARTHER = re.compile(r'^x (<=|<) (-?\d+) "or" x (>=|>) (-?\d+)$')

def read_graph(answer):
    """The answer's set, and how the number line shows it: (set, pieces, dots).
    pieces: (a, b), None for a ray off that end; dots: (x, solid?)."""
    t = " ".join(answer.split())
    m = WITHIN.match(t)
    if m:
        lo, hi = int(m.group(1)), int(m.group(4))
        closed = (m.group(2) == "<=", m.group(3) == "<=")
        return (sp.Interval(lo, hi, not closed[0], not closed[1]), [(lo, hi)], [(lo, closed[0]), (hi, closed[1])])
    m = FARTHER.match(t)
    if m:
        lo, hi = int(m.group(2)), int(m.group(4))
        closed = (m.group(1) == "<=", m.group(3) == ">=")
        s = sp.Union(sp.Interval(-sp.oo, lo, True, not closed[0]), sp.Interval(hi, sp.oo, not closed[1], True))
        return s, [(None, lo), (hi, None)], [(lo, closed[0]), (hi, closed[1])]
    raise ValueError('write it like 3 < x < 7 or x <= -5 "or" x >= 1')

REL = re.compile(r"\s*(<=|>=|<|>)\s*")
OPS = {"<": lambda a, b: a < b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b, ">=": lambda a, b: a >= b}

def inequality_holds(p):
    """The answer's set is the inequality's: tested, with the inequality as written, at every
    point where the two sides are equal, at the answer's own ends, between them, and beyond."""
    left_, op, right_ = REL.split(p["prompt"].strip())
    lhs, rhs = to_sympy(left_), to_sympy(right_)
    S, _, dots = read_graph(p["answer"])
    equal = sp.solveset(lhs - rhs, X, sp.S.Reals)
    if not isinstance(equal, sp.FiniteSet):
        return False
    pts = sorted(set(equal) | {sp.Integer(v) for v, _ in dots})
    if not pts:
        return False
    tests = pts + [(a + b) / 2 for a, b in zip(pts, pts[1:])] + [pts[0] - 1, pts[-1] + 1]
    same = all(bool(OPS[op](lhs.subs(X, t), rhs.subs(X, t))) == bool(S.contains(t)) for t in tests)
    return same and dots[0][0] < dots[1][0] and fits(p)

def fits(p):
    """The graph's ends are inside the number line (a problem with no line gets one when shown)."""
    if "line" not in p:
        return True
    lo, hi = p["line"]
    return all(lo < v < hi for v, _ in read_graph(p["answer"])[2])

def window(r, lo, hi):
    """The number line's integers: the graph's ends one to three in from its ends, so the
    line doesn't give them away."""
    return [lo - r.randint(1, 3), hi + r.randint(1, 3)]

def line_of(p):
    if "line" in p:
        return p["line"]
    lo, hi, _ = ends(p["prompt"])
    return [lo - 2, hi + 2]

# ------------------------------------------------------------------
# Types 4-6: the answer (the points the key marks), and the test of it
# ------------------------------------------------------------------
def num(v):
    """A coordinate as the deck writes it: whole, or a decimal (0.25, -0.5)."""
    v = F(int(sp.numer(v)), int(sp.denom(v)))
    return gen.decimal(v, 4)

def points_text(pts):
    return ", ".join(f"({num(a)}, {num(b)})" for a, b in pts)

def vertex(f):
    """Where the inside of f's absolute value is 0."""
    inside = [a.args[0] for a in f.atoms(sp.Abs)]
    if len(inside) != 1 or not inside[0].is_polynomial(X) or sp.Poly(inside[0], X).degree() != 1:
        raise ValueError("write the absolute value of a linear expression, like y = abs(x - 2)")
    return sp.solve(inside[0], X)[0]

def abs_answer(prompt):
    _, f = read_function(prompt)
    v = vertex(f)
    pts = [(t, f.subs(X, t)) for t in (v - 2, v, v + 2)]
    if not all(a.is_Integer and b.is_Integer for a, b in pts):
        raise ValueError("this bank marks whole-number points: write it like y = abs(x - 2) + 1")
    return points_text(pts)

def asymptote(g):
    """The one x where g has no value."""
    zeros = sp.Poly(sp.denom(sp.together(g)), X).real_roots()
    if len(set(zeros)) != 1:
        raise ValueError("this bank draws one asymptote")
    return zeros[0]

SIDES = (-2, -1, -sp.Rational(1, 2), sp.Rational(1, 2), 1, 2)

def square_answer(prompt):
    _, g = read_function(prompt)
    v = asymptote(g)
    if sp.simplify(g - 1 / (X - v) ** 2) != 0 or not v.is_Integer:
        raise ValueError("write 1 over a square, like y = 1/(x - 2)^2")
    return f"x = {num(v)}; " + points_text([(v + s, g.subs(X, v + s)) for s in SIDES])

def line_parts(prompt):
    """(f, g, slope, where f is 0) for f(x) = x + b or b - x and its reciprocal g."""
    f, g = read_pair(prompt)
    if not f.is_polynomial(X) or sp.Poly(f, X).degree() != 1:
        raise ValueError("f is a line, like f(x) = x + 3")
    m, b = sp.Poly(f, X).all_coeffs()
    if abs(m) != 1 or not b.is_Integer:
        raise ValueError("this bank draws lines of slope 1 or -1, like f(x) = x + 3 or f(x) = 3 - x")
    if sp.simplify(f * g - 1) != 0:
        raise ValueError("g is the reciprocal of f: g(x) = 1/(x + 3)")
    return f, g, m, -b / m

def line_answer(prompt):
    f, g, m, v = line_parts(prompt)
    return f"x = {num(v)}; " + points_text([(v + y / m, sp.Integer(y)) for y in (1, -1)])

NUM = r"-?\d+(?:\.\d+)?"
POINT = re.compile(rf"\(\s*({NUM})\s*,\s*({NUM})\s*\)")
POINTS = re.compile(rf"^\({NUM}, {NUM}\)(, \({NUM}, {NUM}\))*$")
ASYMPTOTE = re.compile(rf"^x = ({NUM})$")

def rational(s):
    q = F(s)
    return sp.Rational(q.numerator, q.denominator)

def read_points(text):
    t = " ".join(text.split())
    if not POINTS.match(t):
        raise ValueError("write the points like (-2, 2), (0, 0), (2, 2)")
    return [(rational(a), rational(b)) for a, b in POINT.findall(t)]

def read_sketch(answer):
    """(asymptote, points) from "x = -3; (-2, 1), (-4, -1)"."""
    parts = [s.strip() for s in answer.split(";")]
    m = ASYMPTOTE.match(parts[0]) if len(parts) == 2 else None
    if not m:
        raise ValueError("write the asymptote, then the points: x = -3; (-2, 1), (-4, -1)")
    return rational(m.group(1)), read_points(parts[1])

def on(f, pts):
    return all(f.subs(X, a) == b for a, b in pts)

def abs_holds(p):
    _, f = read_function(p["prompt"])
    pts = read_points(p["answer"])
    if len(pts) != 3 or not f.has(sp.Abs):
        return False
    v = pts[1][0]
    mirror = all(f.subs(X, v - t) == f.subs(X, v + t) for t in (sp.Rational(1, 2), 1, 3, 7))
    return (on(f, pts) and mirror and f.subs(X, v + 1) != f.subs(X, v)
            and [a for a, _ in pts] == [v - 2, v, v + 2])

def square_holds(p):
    _, g = read_function(p["prompt"])
    v, pts = read_sketch(p["answer"])
    no_value = sp.singularities(g, X)
    return (no_value == sp.FiniteSet(v) and [a for a, _ in pts] == [v + s for s in SIDES] and on(g, pts)
            and all(b > 0 for _, b in pts))

def line_holds(p):
    f, g = read_pair(p["prompt"])
    v, pts = read_sketch(p["answer"])
    product = all(f.subs(X, t) * g.subs(X, t) == 1 for t in (v - 7, v - sp.Rational(1, 3), v + 2, v + 11))
    return (product and f.subs(X, v) == 0 and sp.singularities(g, X) == sp.FiniteSet(v)
            and [b for _, b in pts] == [1, -1] and on(f, pts) and on(g, pts))

# ------------------------------------------------------------------
# Solving and checking
# ------------------------------------------------------------------
ANSWER = {"within": inequality_answer, "farther": inequality_answer, "isolate": inequality_answer,
          "abs": abs_answer, "square": square_answer, "line": line_answer}
HOLDS = {"within": inequality_holds, "farther": inequality_holds, "isolate": inequality_holds,
         "abs": abs_holds, "square": square_holds, "line": line_holds}

def answer_of(prompt):
    return ANSWER[kind(prompt)](prompt)

STRAY = 0.2         # how often a draw takes another of its type's templates

def draw(entry, r, tpl):
    """Some templates hold few problems (y = |x| is one), so a draw sometimes strays to another
    of its type's templates: a long sheet uses the whole type before it runs dry."""
    if r.random() < STRAY:
        tpl = r.randrange(len(TEMPLATES[entry]))
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    out = dict(prompt=prompt, answer=answer_of(prompt))
    if entry in NUMBER_LINE:
        lo, hi, _ = ends(prompt)
        out["line"] = window(r, lo, hi)
    return out

def check(p):
    try:
        k = kind(p["prompt"])
        if k != KIND[p["type"]]:
            return "failed"
        ok = HOLDS[k](p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]), tries=600)

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def math_(t):
    return f"${dfrac(t)}$"

def statement(p):
    """The problem's words (Typst markup), without its figure: its own task (EXTENDING.md 3.10)."""
    k, prompt = kind(p["prompt"]), p["prompt"].strip()
    if k in ("within", "farther"):
        return f"Graph the set ${{x in RR | {prompt}}}$ on the number line."
    if k == "isolate":
        return f"Graph {math_(prompt)} on the number line."
    if k == "line":
        f, g = [s.strip() for s in prompt.split(";")]
        return f"Sketch the graph of {math_(g)}, the reciprocal of {math_(f)}."
    return f"Sketch the graph of {math_(prompt)}."

def number_line(p, key):
    lo, hi = line_of(p)
    if not key:
        return fig.number_line(lo, hi)
    _, pieces, dots = read_graph(p["answer"])
    return fig.number_line(lo, hi, pieces, dots, ink="red")

CM = 0.4                                         # a graph's centimeters to a unit, on a sheet

def axes(xs, ys):
    """A window holding the xs, the ys, and the origin, with one unit of room."""
    x0, x1 = int(min(xs + [0])) - 1, int(max(xs + [0])) + 1
    y0, y1 = int(min(ys + [0])) - 1, int(max(ys + [0])) + 1
    width = CM * (x1 - x0)
    return Graph(x=(x0, x1), y=(y0, y1), width=width, slide_width=2 * width)

def branch(g, fn, v, side, far):
    """One side of a reciprocal's curve, from far out in to its asymptote x = v."""
    n = 140
    ds = [far * (0.04 / far) ** (i / n) for i in range(n + 1)]
    g.polyline([(float(v) + side * d, fn(float(v) + side * d)) for d in ds], color="blue", width=1.4, ends="arrow")

def dotted(g, v):
    """An asymptote: a dotted line the height of the window."""
    g.polyline([(float(v), g.y0), (float(v), g.y1)], color="gray", width=0.9, dash="dashed", ends=None)

def abs_graph(p, key):
    _, f = read_function(p["prompt"])
    v = vertex(f)
    far = [v - 4, v, v + 4]
    g = axes(far, [f.subs(X, t) for t in far])
    if key:
        out = [v - 30, v, v + 30]
        g.polyline([(float(t), float(f.subs(X, t))) for t in out], color="blue", width=1.4, ends="arrow")
        for a, b in read_points(p["answer"]):
            g.point(float(a), float(b), color="blue")
    return g.typst()

def square_graph(p, key):
    _, fn_ = read_function(p["prompt"])
    v = asymptote(fn_)
    g = axes([v - 4, v + 4], [0, 4])
    if key:
        fn = sp.lambdify(X, fn_, "math")
        dotted(g, v)
        for side in (-1, 1):
            branch(g, fn, v, side, 12)
        for a, b in read_sketch(p["answer"])[1]:
            g.point(float(a), float(b), color="blue")
    return g.typst()

def label_place(v, x, y):
    """Where Type 6 names the dot (x, y), y = 1 or -1: across the dotted line x = v, as the book
    does, or (when that would sit on the y axis) out past the dot. (x, y, anchor) for label_at."""
    away = 1 if x < v else -1                        # from the dot toward the dotted line and past it
    near, far = v + 0.1 * away, v + 2.7 * away
    if min(near, far) < 0 < max(near, far):
        return x - 0.4 * away, 0.7 * y, "east" if away > 0 else "west"
    return near, 1.4 * y, "west" if away > 0 else "east"

def line_graph(p, key):
    """Type 6's figure: the line f, its dots at y = 1 and -1 (named), and the dotted asymptote;
    on the key f is gray and g is drawn over it."""
    f, g_, m, v = line_parts(p["prompt"])
    x0, x1 = int(min(v - 3, -5)), int(max(v + 3, 5))
    g = Graph(x=(x0, x1), y=(-5, 5), width=CM * (x1 - x0), slide_width=2 * CM * (x1 - x0))
    dotted(g, v)
    fl = sp.lambdify(X, f, "math")
    g.polyline([(float(v) - 30, fl(float(v) - 30)), (float(v) + 30, fl(float(v) + 30))],
               color="gray" if key else "black", width=1.0 if key else 1.6)
    if key:
        fn = sp.lambdify(X, g_, "math")
        for side in (-1, 1):
            branch(g, fn, v, side, 14)
    for y in (1, -1):
        x = v + y / m
        g.point(float(x), y, color="blue" if key else "black")
        if not key:
            lx, ly, anchor = label_place(float(v), float(x), y)
            g.label_at(lx, ly, f"#box(fill: white, outset: 1pt)[$({num(x)}, {y})$]", anchor=anchor)
    return g.typst()

FIGURE = {"within": number_line, "farther": number_line, "isolate": number_line,
          "abs": abs_graph, "square": square_graph, "line": line_graph}

def figure(p, key=False):
    return FIGURE[kind(p["prompt"])](p, key)

def _prompt(p, key):
    try:
        k, s, f = kind(p["prompt"]), statement(p), figure(p, key)
    except (ValueError, KeyError, SyntaxError, TypeError, IndexError, sp.PolynomialError):
        return f"${p['prompt']}$"
    if k in ("within", "farther", "isolate"):
        return f"{s} \\\n    #v(0.5em)\n    {f}"
    return f"{s} \\\n    #v(0.3em)\n    #align(center)[{f}]"     # the sentence over its figure

def typst(p, gap="0.3em"):
    return _prompt(p, False)

def key_typst(p, gap="0.3em"):
    """The key's prompt: the graph drawn on the number line or the axes the sheet gives."""
    return _prompt(p, True)

def table(pts):
    """A table of points, x over y, as the deck's."""
    cells = ", ".join(f"[${num(v)}$]" for v in [a for a, _ in pts] + [b for _, b in pts])
    n = len(pts)
    return (f"#box(baseline: 40%, table(columns: {n + 1}, inset: (x: 0.4em, y: 0.25em), stroke: 0.5pt, align: center, "
            f"table.cell(x: 0, y: 0)[$x$], table.cell(x: 0, y: 1)[$y$], {cells}))")

def answer_typst(p):
    a, k = p["answer"], KIND.get(p["type"])
    try:
        if k == "abs":
            return f"${a}$"
        if k == "line":
            v, pts = read_sketch(a)
            return (f"Asymptote: $x = {num(v)}$ \\\nThrough $({num(pts[0][0])}, {num(pts[0][1])})$ and "
                    f"$({num(pts[1][0])}, {num(pts[1][1])})$")
        if k == "square":
            v, pts = read_sketch(a)
            return f"Asymptote: $x = {num(v)}$ \\\n#text(size: 0.85em)[{table(pts)}]"
    except (ValueError, IndexError):
        pass
    return f"${a}$"

SLIDE = {"4", "5", "6"}

def slide_typst(p, key=False):
    """A sketch's slide: the function and the answer (hidden on the question slide) beside the
    axes, which are the same on both slides, so nothing moves when the curve is drawn.
    None for Types 1-3, whose number line is in the prompt."""
    if p["type"] not in SLIDE:
        return None
    try:
        s, f = statement(p), figure(p, key)
    except (ValueError, KeyError, SyntaxError, TypeError, IndexError, sp.PolynomialError):
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{s} #v(0.8em) {shown}], [{f}])"

def bars(t):
    """abs(x - 5) as |x − 5|, for the terminal."""
    return re.sub(r"abs\(([^()]*)\)", r"|\1|", t)

def text(p):
    try:
        k = kind(p["prompt"])
    except ValueError:
        return p["prompt"]
    t = plain(bars(p["prompt"]))
    if k in ("within", "farther"):
        return "Graph the set {x ∈ ℝ | " + t + "} on the number line."
    if k == "isolate":
        return f"Graph {t} on the number line."
    if k == "line":
        f, g = [s.strip() for s in t.split(";")]
        return f"Sketch the graph of {g}, the reciprocal of {f}.   [graph of f]"
    return f"Sketch the graph of {t}."

def answer_text(p):
    return plain(p["answer"]).replace('"or"', "or")

def height(p):
    """Inches the prompt takes on the page, for page estimates."""
    if p["type"] in NUMBER_LINE:
        return 0.75
    try:
        k = kind(p["prompt"])
        if k == "line":
            return 2.0
        _, f = read_function(p["prompt"])
        return 1.5 if k == "square" else 1.5 + 0.16 * abs(float(f.subs(X, vertex(f))))
    except Exception:
        return 1.5

# ------------------------------------------------------------------
# Editing: the prompt is the problem's data, in its short form
# ------------------------------------------------------------------
EXAMPLE = {"1": "abs(x - 5) < 2", "2": "abs(x + 2) >= 3", "3": "abs(x) - 2 < 0", "4": "y = abs(x)",
           "5": "y = 1/x^2", "6": "f(x) = x + 3; g(x) = 1/(x + 3)"}

def clean(t):
    t = t.replace("−", "-").replace("≥", ">=").replace("≤", "<=")
    t = re.sub(r"\|([^|]*)\|", r"abs(\1)", t)
    return " ".join(t.split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    t = re.sub(r"\s*(<=|>=|<|>)\s*", r" \1 ", t)
    try:
        if kind(t) != KIND[old["type"]]:
            raise ValueError
        new = dict(old, prompt=t, answer=answer_of(t), source="edited")
        if old["type"] in NUMBER_LINE:
            lo, hi, _ = ends(t)
            if not fits(new):                       # the old line can't show it: a new one around it
                new["line"] = [lo - 2, hi + 2]
        status = check(new)
        if status == "unchecked":
            raise ValueError
    except (ValueError, gen.Redraw, SyntaxError, TypeError, KeyError, IndexError, AttributeError,
            sp.PolynomialError):
        raise ValueError(f"write it like: {EXAMPLE[old['type']]}") from None
    return new, status

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    t = clean(t)
    if p["type"] in NUMBER_LINE:
        t = re.sub(r"\s*(<=|>=|<|>)\s*", r" \1 ", t)
        t = re.sub(r'\s*"?\bor\b"?\s*', ' "or" ', t)
    new = dict(p, answer=t)
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)
