"""Lesson 21 (Advanced Math): evaluating functions, domain and range, types of
functions, tests for functions. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_021/slides/deck_021.typ): examples
21.1-21.11 and Problem Set 21, problems 7-12.

     1  evaluating a function:              f(x) = x^2 + x - 10, find f(5)                f(5) = 20
     2  substituting an expression:         f(x) = x^2 + 1, find f(x + 2)                 f(x + 2) = x^2 + 4 x + 5
     3  a trig function, reference triangle: g(θ) = 4 sqrt(3) cos θ, find g(60°)         g(60°) = 2 sqrt(3)
     4  the domain: a square root           f(x) = sqrt(10 - x)                           {x ∈ ℝ | x <= 10}
     5  the domain: a denominator, or none  g(x) = 1/(x - 2);  f(x) = x^2 - 3             {x ∈ ℝ | x != 2};  {x ∈ ℝ}
     6  domain, range, and graph of sqrt    y = sqrt(x + 4)                               {x ∈ ℝ | x >= -4}, {y ∈ ℝ | y >= 0}
     7  domain and range, root over linear  f(x) = sqrt(x)/(x - 2)                        {x ∈ ℝ | x >= 0, x != 2}, {y ∈ ℝ}
     8  a mapping diagram                   domain {7, 5}, range {3, 4}: 7->3, 5->3, 5->4 not a function: 5 has two images
     9  sets of ordered pairs               four sets, (a)-(d)                            (a), (c), (d)
    10  a graph: function? one-to-one?      the vertical and horizontal line tests        function, not one-to-one

Types 4 and 5 split the deck's "domain" heading by its move: a square root
gives an inequality to solve (and 10 - x >= 0 flips to x <= 10); a
denominator gives numbers to leave out; a polynomial (problem 9a) has no
restriction, which a student finds by looking for both and seeing neither.
Types 6 and 7 split the domain-and-range examples: 21.6 and 21.7 graph a
square root, read the range off it, and the student draws the graph (on
axes the sheet gives); 21.8's range, all reals, is read from a graph with an
asymptote, which the key draws as the deck does. Example 21.9's four
diagrams, problem 8's two, and example 21.11's four graphs are each one
problem a diagram or graph; example 21.10's and problem 7's four sets stay
together as one problem, as comparing them is the point.

Answer conventions, from the deck:
  - An evaluation names what it finds (the approved convention of the
    adv_* function banks): f(5) = 20, f(x + 2) = x^2 + 4 x + 5 (multiplied
    out, by descending degree), 4 sqrt(3) h(30°) = 2 sqrt(3). The value is
    exact, rationalized, radicands square-free (Lesson 20's form).
  - A domain or range in set-builder notation, as the deck writes it:
    {x ∈ ℝ | x <= 10}, {x ∈ ℝ | x != 2}, {x ∈ ℝ | x >= 0, x != 2}, and with
    no restriction {x ∈ ℝ} (problem 9a), {y ∈ ℝ} (21.8). The bound comes
    first, then the numbers left out, smallest first.
  - Type 6's key is the domain, the range, and the graph through the deck's
    points (where the radicand is 0, 1, 4, 9): 21.7's (-4, 0), (0, 2), (5, 3).
  - A diagram: "function", or "not a function" with the member at fault, as
    the deck explains it: "5 has two images", "m has no image".
  - Sets of ordered pairs: the letters of the functions, "(a), (c), (d)".
  - A graph: "not a function", "function, one-to-one", or "function, not
    one-to-one" (21.11's words).

check() works from the problem's data, not from how the answer was made:
  1, 2  the function read from the prompt and evaluated (adv_functions); the
        answer's value compared at random points, and multiplied out.
  3     the trig function evaluated at the angle; the answer's value compared,
        and its form (Lesson 20's: no trig left, rationalized, square-free).
  4-7   the answer's sets read back; each set tested at every point where the
        function can change (the zeros of what is under a root or below,
        the set's own ends and holes), between them, and beyond: a number is
        in the domain exactly when f is a real number there. Type 6's range
        is [f(e), oo) for the domain's end e (the root grows without bound);
        Type 7's, all reals: f is 0 at the domain's end and falls without
        bound toward the asymptote, then comes down from without bound to 0,
        and is continuous between (the intermediate value theorem).
  8     the arrows counted for each member of the domain.
  9     the ordered pairs read back: a set is a function when no first number
        has two different second numbers.
  10    the vertical and horizontal line tests run on the pieces the graph is
        drawn from: lines at every end, every level, and a fine grid, the
        points on each counted exactly (polynomial roots by Sturm's count).
        The key is made the other way: by the pieces' intervals overlapping
        and by each piece's slope changing sign.

No sources are skipped: Lesson 21's proofs (problems 14 and 26) are outside
its types, as are the review problems (1-6, 13, 15-30), which other banks
cover.

A problem: dict(type, prompt, answer, source). The prompt is the problem's
data in a short form, and it is what an edit changes:
    1  "f(x) = x^2 + x - 10; f(5)"                    "f(5) = 20"
    2  "f(x) = x^2 + 1; f(x + 2)"                     "f(x + 2) = x^2 + 4 x + 5"
    3  "h(theta) = sin(theta); 4 sqrt(3) h(30 degree)"  "4 sqrt(3) h(30 degree) = 2 sqrt(3)"
    4  "f(x) = sqrt(10 - x); domain"                  "{x in RR | x <= 10}"
    5  "g(x) = 1/(x - 2); domain"                     "{x in RR | x != 2}"
    6  "y = sqrt(x + 4)"                              "{x in RR | x >= -4}; {y in RR | y >= 0}"
    7  "f(x) = sqrt(x)/(x - 2)"                       "{x in RR | x >= 0, x != 2}; {y in RR}"
    8  "domain 7, 5; range 3, 4; 7 -> 3, 5 -> 3, 5 -> 4"  "not a function: 5 has two images"
       "x in RR -> x + 2"                             "function"
    9  "{(1, 2), (2, 3)}; {(1, 2), (1, 3)}; ..."      "a, c, d"
   10  "y = 1, x in (-oo, 1]; y = -1, x in (1, oo)"   "function, not one-to-one"
       "x = 3 y - y^3, y in (-oo, oo)"                "not a function"
"""
import math, re
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, same_value
from ..graphs import Graph, PREAMBLE as GRAPH_PREAMBLE
from ..typmath import tx, fr, single, display, dfrac, text as plain
from . import adv_functions as AF
from . import adv_lesson_20 as L20
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_21"
FIXED = False
TITLE = "Lesson 21: Evaluating Functions, Domain and Range, Types of Functions, Tests for Functions"
INSTRUCTIONS = "Solve each problem."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = GRAPH_PREAMBLE

TYPES = [
    dict(key="1", title="Evaluating a Function",
         look="f(x) is a formula, and you're asked for f of a number.",
         move="Replace x everywhere with the number, in parentheses: f(5) = (5)^2 + (5) - 10. "
              "Then follow the order of operations."),
    dict(key="2", title="Substituting an Expression",
         look="f of an expression, like f(x + 2).",
         move="Replace x everywhere with the whole expression, in parentheses: (x + 2)^2 + 1. "
              "Multiply out and combine like terms."),
    dict(key="3", title="A Trig Function and a Reference Triangle",
         instructions="Draw the necessary reference triangle and evaluate. Do not use a calculator.",
         look="A function of θ made with sin, cos, or tan, at 30°, 45°, or 60°.",
         move="Replace θ with the angle. Draw the 30-60-90 triangle (sides 1, sqrt(3), 2) or the 45-45-90 "
              "triangle (sides 1, 1, sqrt(2)), read the ratio, and multiply: 4 sqrt(3) (1/2) = 2 sqrt(3)."),
    dict(key="4", title="The Domain: a Square Root",
         instructions="Find the domain of each function.",
         look="x under a square root.",
         move="The quantity under the radical can't be negative: solve inside ≥ 0. "
              "10 - x >= 0 gives x <= 10. Write the domain as {x ∈ ℝ | x <= 10}."),
    dict(key="5", title="The Domain: a Denominator, or No Restriction",
         instructions="Find the domain of each function.",
         look="x in a denominator, or a polynomial with no denominator and no root.",
         move="A denominator can't be zero: leave out each x that makes it 0, {x ∈ ℝ | x != 2}. "
              "With no denominator and no square root, every real number works: {x ∈ ℝ}."),
    dict(key="6", title="Domain, Range, and Graph of a Square Root",
         instructions="Find the domain and range of each function, and graph the function.",
         look="y = sqrt(x + a): find the domain and range, and draw the graph.",
         move="Domain: inside ≥ 0. Make a table where inside is 0, 1, 4, and 9, plot the points, and draw "
              "the curve from the first one. A square root is never negative: the range is {y ∈ ℝ | y >= 0}.",
         space="0.4in"),
    dict(key="7", title="Domain and Range: a Root Over a Linear Factor",
         instructions="Find the domain and range of each function.",
         look="A square root over x - a.",
         move="Domain: the root's inside ≥ 0, and leave out the zero of the denominator. Near that zero the "
              "graph falls without bound on one side and rises on the other, so the range is all reals, {y ∈ ℝ}.",
         space="1.25in"),
    dict(key="8", title="Does a Mapping Diagram Designate a Function?",
         instructions="Determine whether or not each diagram designates a function.",
         look="Two ovals, the domain and the range, with arrows from one to the other.",
         move="A function maps each member of the domain to exactly one image. Two arrows from one member, "
              "or none: not a function. Two members may share an image.", space="0.5in"),
    dict(key="9", title="Which Sets of Ordered Pairs Are Functions?",
         instructions="Which of the following sets of ordered pairs are functions?",
         look="Four sets of ordered pairs, (a) to (d).",
         move="Look for a first number that repeats with a different second number: (1, 2) and (1, 3) is not "
              "a function. A pair written twice, like (4, 3) and (4, 3), is the same pair: still a function.",
         width="full", space="0.5in"),
    dict(key="10", title="The Vertical and Horizontal Line Tests",
         instructions="Determine if each graph represents the graph of a function. If so, determine whether "
                      "it is the graph of a one-to-one function.",
         look="A graph with no scale; solid points are on it, open points are not.",
         move="Vertical line test: a function if no vertical line meets the graph more than once. Then the "
              "horizontal line test: one-to-one if no horizontal line meets it more than once.",
         space="0.5in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
X, Y = sp.Symbol("x"), sp.Symbol("y")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

NAMES = ("f", "g", "h")

def poly(*cs):
    """Coefficients, highest power first, as Typst: poly(1, 1, -10) = "x^2 + x - 10"."""
    return AF.poly(*cs)

# ------------------------------------------------------------------
# Type 1: f(x) = x^2 + x - 10, find f(5)
# ------------------------------------------------------------------
LEAD = (1, 1, 1, -1, 2, 3)                      # x^2's coefficient: 1 most often, as in the book
B1 = range(-9, 10)
C1 = range(-12, 13)
ARGS = [n for n in range(-6, 7) if n]           # the number put in

def t1_build(name, a, b, c, n):
    return f"{name}(x) = {poly(a, b, c)}; {name}({n})"

def t1_pick(r):
    c = r.choice([v for v in C1 if v])
    return dict(name=r.choice(NAMES), a=r.choice(LEAD), b=r.choice(B1), c=c, n=r.choice(ARGS))

CUBE = (1, -1, 2)

def t1_cubic_build(name, a, b, c, n):
    return f"{name}(x) = {poly(a, 0, b, c)}; {name}({n})"

def t1_cubic_pick(r):
    return dict(name=r.choice(NAMES), a=r.choice(CUBE), b=gen.signed(r, 1, 6), c=gen.signed(r, 1, 9),
                n=r.choice([n for n in range(-3, 4) if n]))

# ------------------------------------------------------------------
# Type 2: f(x) = x^2 + 1, find f(x + 2)
# ------------------------------------------------------------------
B2 = range(-6, 7)
C2 = [v for v in range(-9, 10) if v]
SHIFT = [k for k in range(-6, 7) if k]

def t2_build(name, a, b, c, k):
    return f"{name}(x) = {poly(a, b, c)}; {name}({tx(X + k)})"

def t2_pick(r):
    return dict(name=r.choice(NAMES), a=r.choice((1, 1, 1, -1, 2)), b=r.choice(B2), c=r.choice(C2),
                k=r.choice(SHIFT))

def t2_square_pick(r):                          # the book's: no x term, x^2 + 1
    return dict(t2_pick(r), b=0)

# ------------------------------------------------------------------
# Type 3: h(θ) = sin θ, find 4 sqrt(3) h(30°); g(θ) = 4 sqrt(3) cos θ, find g(60°)
# ------------------------------------------------------------------
FUNCS = L20.FUNCS
ANGLES = L20.ANGLES
K3 = range(1, 13)
RAD3 = (1,) + L20.RADICANDS                      # 1: a whole-number coefficient

def coef(k, m):
    return L20.root(k, m) if m != 1 else str(k)

def t3_build(name, k, m, func, angle, inside):
    """inside: the coefficient is in the function (problems 11, 12); else in front of it (21.3)."""
    c = coef(k, m)
    if inside:
        return f"{name}(theta) = {c} {func}(theta); {name}({angle} degree)"
    return f"{name}(theta) = {func}(theta); {c} {name}({angle} degree)"

def t3_pick(inside):
    def pick(r):
        m = r.choice((1, 1, 1, 2, 2, 3, 3) + L20.RADICANDS)
        k = r.choice([v for v in K3 if v > 1 or m > 1])
        return dict(name=r.choice(NAMES), k=k, m=m, func=r.choice(FUNCS), angle=r.choice(ANGLES), inside=inside)
    return pick

# ------------------------------------------------------------------
# Type 4: the domain of a square root
# ------------------------------------------------------------------
K4 = (1, 1, 1, 1, 2, 3, 4)                      # x's coefficient under the root
A4 = [a for a in range(-12, 13) if a]

def inside(k, a, flip):
    """k x + a, or (flip) a - k x."""
    kx = "x" if k == 1 else f"{k} x"
    if flip:
        return f"{a} - {kx}"
    return f"{kx} + {a}" if a > 0 else f"{kx} - {-a}"

def t4_build(name, k, a, flip):
    return f"{name}(x) = sqrt({inside(k, a, flip)}); domain"

def t4_pick(flip):
    def pick(r):
        k = r.choice(K4)
        a = r.choice([v for v in A4 if v % k == 0 and (v > 0 or not flip)])
        return dict(name=r.choice(NAMES), k=k, a=a, flip=flip)
    return pick

# ------------------------------------------------------------------
# Type 5: the domain with a denominator, or none
# ------------------------------------------------------------------
TOP = range(1, 10)
ZERO = [v for v in range(-9, 10) if v]

def t5_build(name, n, a):
    return f"{name}(x) = {fr(str(n), tx(X - a))}; domain"

def t5_pick(r):
    return dict(name=r.choice(NAMES), n=r.choice((1, 1) + tuple(TOP)), a=r.choice(ZERO))

def t5_two_build(name, n, a, b):
    return f"{name}(x) = {n}/(({tx(X - a)})({tx(X - b)})); domain"

def t5_two_pick(r):
    a, b = sorted(r.sample(ZERO, 2))
    return dict(name=r.choice(NAMES), n=r.choice(TOP), a=a, b=b)

def t5_poly_build(name, a, b, c):
    return f"{name}(x) = {poly(a, b, c)}; domain"

def t5_poly_pick(r):
    return dict(name=r.choice(NAMES), a=r.choice((1, 1, -1, 2)), b=r.choice((0, 0) + tuple(B2)),
                c=r.choice(C2))

# ------------------------------------------------------------------
# Type 6: y = sqrt(x + a): domain, range, graph
# ------------------------------------------------------------------
A6 = range(-6, 7)                                # sqrt(x + a); a = 0 is sqrt(x)
A6_FLIP = range(-2, 7)                           # sqrt(a - x)

def t6_build(a, flip):
    return f"y = sqrt({inside(1, a, True)})" if flip else ("y = sqrt(x)" if a == 0 else f"y = sqrt({inside(1, a, False)})")

def t6_pick(r):
    return dict(a=r.choice(A6), flip=False)

def t6_flip_pick(r):
    return dict(a=r.choice([v for v in A6_FLIP if v]), flip=True)

# ------------------------------------------------------------------
# Type 7: f(x) = sqrt(x - b)/(x - a), a > b
# ------------------------------------------------------------------
B7 = range(-4, 4)
GAP7 = range(1, 6)

def t7_build(name, b, gap):
    top = "sqrt(x)" if b == 0 else f"sqrt({tx(X - b)})"
    return f"{name}(x) = {fr(top, tx(X - (b + gap)))}"

def t7_pick(r):
    return dict(name=r.choice(NAMES), b=r.choice((0, 0) + tuple(B7)), gap=r.choice(GAP7))

# ------------------------------------------------------------------
# Type 8: mapping diagrams
# ------------------------------------------------------------------
DIGITS = tuple(str(n) for n in range(1, 10))
LETTER_SETS = ("abc", "xyz", "pqr", "mnk", "stu")
RULES = ("x + 2", "x - 3", "2 x", "3 x", "x^2", "2 x + 1", "x + 5", "x^2 - 1", "-x", "x - 1")

def t8_build(domain, range_, arrows):
    """arrows: (domain member, range member) pairs."""
    return f"domain {', '.join(domain)}; range {', '.join(range_)}; " + ", ".join(f"{a} -> {b}" for a, b in arrows)

def t8_rule_build(rule):
    return f"x in RR -> {rule}"

def members(r, n):
    """n members of a domain: digits, letters, or digits with one letter (as 21.9(c))."""
    kind = r.choice(("digits", "digits", "letters", "mixed"))
    if kind == "letters":
        return list(r.choice(LETTER_SETS)[:n]) if n <= 3 else r.sample(gen.LETTERS, n)
    ds = r.sample(DIGITS, n)
    if kind == "mixed":
        ds[r.randrange(n)] = r.choice("mkpt")
    return ds

def arrows_in_order(domain, range_, arrows):
    return sorted(set(arrows), key=lambda e: (domain.index(e[0]), range_.index(e[1])))

def t8_pick(defect):
    """defect: None (a function), "two" (a member with two images), "none" (a member with no image)."""
    def pick(r):
        n = r.choice((2, 3, 3, 4))
        domain = members(r, n)
        m = r.randint(1, n) if defect != "two" else r.randint(2, min(n + 1, 4))
        range_ = r.sample(DIGITS, m)
        maps = {d: [r.choice(range_)] for d in domain}
        odd = r.choice(domain)
        if defect == "two":
            maps[odd].append(r.choice([v for v in range_ if v not in maps[odd]]))
        if defect == "none":
            maps[odd] = []
        arrows = arrows_in_order(domain, range_, [(d, v) for d, vs in maps.items() for v in vs])
        need({v for _, v in arrows} == set(range_))                  # every member of the range is an image
        return dict(domain=domain, range_=range_, arrows=arrows)
    return pick

def t8_rule_pick(r):
    return dict(rule=r.choice(RULES))

# ------------------------------------------------------------------
# Type 9: sets of ordered pairs
# ------------------------------------------------------------------
V9 = range(-3, 10)
SIZES = (3, 4, 4, 4, 5)

def t9_build(rels):
    return "; ".join("{" + ", ".join(f"({a}, {b})" for a, b in rel) + "}" for rel in rels)

def relation(r, kind):
    """kind: "function", "repeat" (a function with a pair written twice, as 21.10(c)), or "not"."""
    n = r.choice(SIZES)
    if kind == "function":
        xs = r.sample(V9, n)
        return [(a, r.choice(V9)) for a in xs]
    if kind == "repeat":
        xs = r.sample(V9, n - 1)
        ps = [(a, r.choice(V9)) for a in xs]
        ps.insert(r.randint(1, n - 1), ps[r.randrange(n - 1)])
        return ps
    xs = r.sample(V9, n - 1)
    ps = [(a, r.choice(V9)) for a in xs]
    a, b = r.choice(ps)
    ps.insert(r.randint(1, n - 1), (a, r.choice([v for v in V9 if v != b])))   # a first number with a second image
    return ps

def t9_pick(r):
    kinds = [r.choice(("function", "function", "repeat", "not", "not")) for _ in range(4)]
    need(any(k != "not" for k in kinds) and "not" in kinds)
    return dict(rels=[relation(r, k) for k in kinds])

# ------------------------------------------------------------------
# Type 10: graphs. A graph is pieces: "y = f(x), x in [a, b)" or "x = g(y), y in (-oo, oo)";
# a bracket is a solid point, a parenthesis an open one, oo an arrow (the graph goes on).
# ------------------------------------------------------------------
SIDEWAYS = ("y^2 - 2", "2 - y^2", "3 y - y^3", "y^3 - 3 y", "y^2 - 2 y - 1", "1 - y^2 + 2 y", "y^2")
ONE_TO_ONE = ("x", "x + 1", "2 x - 1", "1 - x", "-2 x + 1", "x^3", "x^3 - 1", "-x^3 + 1", "(x - 1)^3",
              "2^x - 1", "2 - 2^(-x)", "1 - 2^x")
NOT_ONE_TO_ONE = ("x^2 - 2", "2 - x^2", "x^3 - 3 x", "3 x - x^3", "(x - 1)^2 - 2", "x^2 + 2 x - 1",
                  "-(x + 1)^2 + 2", "x^2")
JUMP_AT = (-1, 0, 1)
SLOPES = (-1, 0, 1)
LEVELS = range(-2, 3)
DOTS = (("]", "("), ("]", "["), (")", "["))         # the left ray's end, the right ray's start

def t10_curve_build(expr, sideways):
    return f"x = {expr}, y in (-oo, oo)" if sideways else f"y = {expr}, x in (-oo, oo)"

def t10_curve_pick(pool, sideways):
    return lambda r: dict(expr=r.choice(pool), sideways=sideways)

def line(m, c, y):
    """The line of slope m through (c, y), as Typst: y = m x + (y - m c)."""
    return tx(m * X + (y - m * c))

def t10_jump_build(c, m1, y1, m2, y2, dots):
    """Two rays meeting at x = c: the left one ends at (c, y1), the right one starts at (c, y2)."""
    end, start = dots
    return (f"y = {line(m1, c, y1)}, x in (-oo, {c}{end}; "
            f"y = {line(m2, c, y2)}, x in {start}{c}, oo)")

def t10_jump_pick(r):
    y1, y2 = r.sample(LEVELS, 2)
    return dict(c=r.choice(JUMP_AT), m1=r.choice(SLOPES), y1=y1, m2=r.choice(SLOPES), y2=y2, dots=r.choice(DOTS))

# ------------------------------------------------------------------
# Templates and ranges
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick, t1_build), (t1_pick, t1_build), (t1_cubic_pick, t1_cubic_build)],
    "2": [(t2_pick, t2_build), (t2_square_pick, t2_build)],
    "3": [(t3_pick(False), t3_build), (t3_pick(True), t3_build), (t3_pick(True), t3_build)],
    "4": [(t4_pick(True), t4_build), (t4_pick(True), t4_build), (t4_pick(False), t4_build)],
    "5": [(t5_pick, t5_build), (t5_pick, t5_build), (t5_two_pick, t5_two_build), (t5_poly_pick, t5_poly_build)],
    "6": [(t6_pick, t6_build), (t6_pick, t6_build), (t6_flip_pick, t6_build)],
    "7": [(t7_pick, t7_build)],
    "8": [(t8_pick(None), t8_build), (t8_pick("two"), t8_build), (t8_pick("none"), t8_build),
          (t8_rule_pick, t8_rule_build)],
    "9": [(t9_pick, t9_build)],
    "10": [(t10_curve_pick(SIDEWAYS, True), t10_curve_build), (t10_curve_pick(ONE_TO_ONE, False), t10_curve_build),
           (t10_curve_pick(NOT_ONE_TO_ONE, False), t10_curve_build), (t10_jump_pick, t10_jump_build),
           (t10_jump_pick, t10_jump_build)],
}

def _mapping_ok(domain, range_, arrows):
    ok_members = all(d in DIGITS or (len(d) == 1 and d.isalpha()) for d in domain) and set(range_) <= set(DIGITS)
    images = {d: sum(1 for a, _ in arrows if a == d) for d in domain}
    faults = [d for d, k in images.items() if k != 1]
    return (ok_members and 2 <= len(domain) <= 4 and 1 <= len(range_) <= 4
            and len(set(domain)) == len(domain) and len(set(range_)) == len(range_)
            and {b for _, b in arrows} == set(range_)
            and all(a in domain for a, _ in arrows) and len(faults) <= 1 and max(images.values()) <= 2
            and arrows == arrows_in_order(domain, range_, arrows))

def _relations_ok(rels):
    kinds = [AF.is_function(rel) for rel in rels]
    return (len(rels) == 4 and all(len(rel) in SIZES and all(a in V9 and b in V9 for a, b in rel) for rel in rels)
            and any(kinds) and not all(kinds))

RANGES = {
    t1_build: lambda name, a, b, c, n: name in NAMES and a in LEAD and b in B1 and c in C1 and c != 0 and n in ARGS,
    t1_cubic_build: lambda name, a, b, c, n: (name in NAMES and a in CUBE and 1 <= abs(b) <= 6 and 1 <= abs(c) <= 9
                                              and n != 0 and abs(n) <= 3),
    t2_build: lambda name, a, b, c, k: name in NAMES and a in (1, -1, 2) and b in B2 and c in C2 and k in SHIFT,
    t3_build: lambda name, k, m, func, angle, inside: (name in NAMES and k in K3 and m in RAD3 and (k, m) != (1, 1)
                                                      and func in FUNCS and angle in ANGLES and inside in (True, False)),
    t4_build: lambda name, k, a, flip: name in NAMES and k in K4 and a in A4 and a % k == 0 and (a > 0 or not flip),
    t5_build: lambda name, n, a: name in NAMES and n in TOP and a in ZERO,
    t5_two_build: lambda name, n, a, b: name in NAMES and n in TOP and a in ZERO and b in ZERO and a < b,
    t5_poly_build: lambda name, a, b, c: name in NAMES and a in (1, -1, 2) and b in B2 and c in C2,
    t6_build: lambda a, flip: a in A6_FLIP and a != 0 if flip else a in A6,
    t7_build: lambda name, b, gap: name in NAMES and b in B7 and gap in GAP7,
    t8_build: _mapping_ok,
    t8_rule_build: lambda rule: rule in RULES,
    t9_build: _relations_ok,
    t10_curve_build: lambda expr, sideways: expr in (SIDEWAYS if sideways else ONE_TO_ONE + NOT_ONE_TO_ONE),
    t10_jump_build: lambda c, m1, y1, m2, y2, dots: (c in JUMP_AT and m1 in SLOPES and m2 in SLOPES and y1 in LEVELS
                                                     and y2 in LEVELS and y1 != y2 and dots in DOTS),
}

def in_range(build, params):
    """Can a random draw pick these parameters for this build?"""
    return RANGES[build](**params)

# ------------------------------------------------------------------
# Reading prompts
# ------------------------------------------------------------------
TRIG_DEF = re.compile(r"^([a-z])\(theta\)\s*=\s*(.+)$")
TRIG_ASK = re.compile(r"^(?:(.+?)\s+)?([a-z])\((-?\d+) degree\)$")
FUNC_DEF = re.compile(r"^(?:([a-z])\(x\)|y)\s*=\s*(.+)$")

def kind(prompt):
    """Which reader a prompt takes."""
    p = prompt.strip()
    if p.startswith("{"):
        return "pairs"
    if p.startswith("domain ") or "->" in p:
        return "mapping"
    if re.search(r"\b[xy] in [\[(]", p):
        return "graph"
    if "theta" in p:
        return "trig"
    if p.endswith("; domain"):
        return "domain"
    if ";" in p:
        return "evaluate"
    return "root" if p.startswith("y") else "quotient"

KIND = {"1": "evaluate", "2": "evaluate", "3": "trig", "4": "domain", "5": "domain", "6": "root",
        "7": "quotient", "8": "mapping", "9": "pairs", "10": "graph"}

def read_trig(prompt):
    """(name, the function's expression in theta, the coefficient in front or "", angle)."""
    parts = [s.strip() for s in prompt.split(";")]
    m, a = (TRIG_DEF.match(parts[0]), TRIG_ASK.match(parts[1])) if len(parts) == 2 else (None, None)
    if not (m and a) or m.group(1) != a.group(2):
        raise ValueError("write it like: g(theta) = 4 sqrt(3) cos(theta); g(60 degree)")
    e = to_sympy(m.group(2))
    if e.free_symbols != {sp.Symbol("theta")}:
        raise ValueError("the function is in theta")
    c = a.group(1) or ""
    if c:
        to_sympy(c)
    return m.group(1), e, c, int(a.group(3))

def trig_value(prompt):
    name, e, c, angle = read_trig(prompt)
    v = e.subs(sp.Symbol("theta"), angle * sp.pi / 180)
    return sp.radsimp(v * (to_sympy(c) if c else 1))

def read_function(prompt):
    """(name or "y", f as sympy in x) from "f(x) = ..." or "y = ...", with ; domain dropped."""
    m = FUNC_DEF.match(prompt.split(";")[0].strip())
    if not m:
        raise ValueError("write it like: f(x) = sqrt(10 - x)")
    f = to_sympy(m.group(2))
    if not f.free_symbols <= {X}:
        raise ValueError("the function is in x")
    return m.group(1) or "y", f

# ------------------------------------------------------------------
# Sets in set-builder notation: {x in RR | x >= 0, x != 2}
# ------------------------------------------------------------------
SET = re.compile(r"^\{\s*([xy])\s+in\s+RR\s*(?:\|\s*(.+?))?\s*\}$")

def set_text(var, lo=None, hi=None, holes=(), lo_open=False):
    conds = []
    if lo is not None:
        conds.append(f"{var} {'>' if lo_open else '>='} {tx(lo)}")
    if hi is not None:
        conds.append(f"{var} <= {tx(hi)}")
    conds += [f"{var} != {tx(h)}" for h in sorted(holes)]
    return "{" + f"{var} in RR" + (" | " + ", ".join(conds) if conds else "") + "}"

def read_set(text, var):
    m = SET.match(" ".join(text.replace("≠", "!=").replace("≥", ">=").replace("≤", "<=").split()))
    if not m or m.group(1) != var:
        raise ValueError(f"write it like {{{var} in RR | {var} >= 0}}")
    if not m.group(2):
        return sp.S.Reals
    conds = m.group(2)
    if var == "y":
        if "x" in conds:
            raise ValueError("a range is in y")
        conds = conds.replace("y", "x")
    return AF.domain_read(conds)

def radicands(f):
    return [a.base for a in sp.preorder_traversal(f) if isinstance(a, sp.Pow) and a.exp == sp.Rational(1, 2)]

def below(f):
    return [a.base for a in sp.preorder_traversal(f) if isinstance(a, sp.Pow) and a.exp.is_number and a.exp < 0]

def domain_answer(f):
    """The domain, worked out: each radicand >= 0 (linear in x), each denominator's zeros left out."""
    lo = hi = None
    for inner in radicands(f):
        p = sp.Poly(inner, X)
        if p.degree() > 1:
            raise ValueError("this bank's roots hold a linear expression")
        if p.degree() == 1:
            k, a = p.all_coeffs()
            b = -a / k
            if k > 0:
                lo = b if lo is None else max(lo, b)
            else:
                hi = b if hi is None else min(hi, b)
    holes = set()
    for d in below(f):
        for z in sp.Poly(d, X).real_roots():
            if not z.is_Rational:
                raise ValueError("this bank's denominators have whole-number zeros")
            if (lo is None or z >= lo) and (hi is None or z <= hi):
                holes.add(z)
    if lo is not None and hi is not None and lo > hi:
        raise ValueError("this function has no domain")
    lo_open = lo in holes
    holes.discard(lo)
    if hi in holes:
        raise ValueError("a domain this bank doesn't write")
    return set_text("x", lo, hi, holes, lo_open)

def defined(f, t):
    v = f.subs(X, t)
    return bool(v.is_finite and v.is_real)

def domain_holds(f, S):
    """S is f's domain: tested at every point where f can change (the zeros of each radicand
    and each denominator, S's own ends and holes), between them, and beyond them."""
    crit = set()
    for e in radicands(f) + below(f):
        crit |= {z for z in sp.Poly(e, X).real_roots()}
    crit |= {b for b in S.boundary if b.is_finite}
    pts = sorted(crit)
    tests = [sp.Integer(0)] if not pts else (
        [pts[0] - 1, pts[-1] + 1] + pts + [(a + b) / 2 for a, b in zip(pts, pts[1:])])
    return all(defined(f, t) == bool(S.contains(t)) for t in tests)

# ------------------------------------------------------------------
# Types 6 and 7: the domain's end, and the range
# ------------------------------------------------------------------
def root_end(f):
    """f = sqrt(k x + a): (the domain's end e, +1 if the domain runs right of e, else -1)."""
    rs = radicands(f)
    if len(rs) != 1 or sp.Poly(rs[0], X).degree() != 1 or f != sp.sqrt(rs[0]):
        raise ValueError("write a square root of a linear expression, like y = sqrt(x + 4)")
    k, a = sp.Poly(rs[0], X).all_coeffs()
    return -a / k, (1 if k > 0 else -1)

def root_answer(f):
    e, side = root_end(f)
    return f"{domain_answer(f)}; {set_text('y', f.subs(X, e))}"

def quotient_shape(f):
    """f = sqrt(x - b)/(x - a) with a > b: (b, a)."""
    num, den = sp.fraction(sp.together(f))
    rs = radicands(num)
    if (len(rs) != 1 or num != sp.sqrt(rs[0]) or sp.Poly(rs[0], X).degree() != 1 or sp.Poly(den, X).degree() != 1
            or sp.Poly(rs[0], X).LC() != 1 or sp.Poly(den, X).LC() != 1):
        raise ValueError("write a root over a linear factor, like f(x) = sqrt(x)/(x - 2)")
    b, a = -sp.Poly(rs[0], X).TC(), -sp.Poly(den, X).TC()
    if not a > b:
        raise ValueError("the denominator's zero is past the root's end, so the range isn't all reals")
    return b, a

def quotient_answer(f):
    quotient_shape(f)
    return f"{domain_answer(f)}; {set_text('y')}"

def split_answer(answer):
    parts = [s.strip() for s in answer.split(";")]
    if len(parts) != 2:
        raise ValueError("write the domain, then the range: {x in RR | x >= -4}; {y in RR | y >= 0}")
    return read_set(parts[0], "x"), read_set(parts[1], "y")

def root_range_holds(f, S, R):
    """R is [f(e), oo): f is a root of a linear expression, 0 at the domain's end e, and grows
    past every bound (tested far out) as x moves into the domain."""
    e, side = root_end(f)
    far = [f.subs(X, e + side * d) for d in (1, 4, 100, 10**6)]
    return (S.contains(e) and R == sp.Interval(f.subs(X, e), sp.oo) and all(a < b for a, b in zip(far, far[1:]))
            and far[-1] > 100)

def quotient_range_holds(f, S, R):
    """R is all reals: f is 0 at the domain's end b, falls past every bound toward the asymptote
    x = a from the left and comes down from past every bound on the right, toward 0 far out;
    f is continuous between, so every real number is a value."""
    b, a = quotient_shape(f)
    eps = sp.Rational(1, 10**6)
    return (R == sp.S.Reals and S.contains(b) and f.subs(X, b) == 0 and f.subs(X, a - eps) < -100
            and f.subs(X, a + eps) > 100 and 0 < f.subs(X, a + 10**6) < 1)

# ------------------------------------------------------------------
# Type 8: mapping diagrams
# ------------------------------------------------------------------
MAP_RE = re.compile(r"^domain ([^;]+); range ([^;]+); (.+)$")
RULE_RE = re.compile(r"^x in RR -> (.+)$")

def read_mapping(prompt):
    """("rule", expression) or ("map", domain, range, arrows)."""
    p = " ".join(prompt.split())
    m = RULE_RE.match(p)
    if m:
        e = to_sympy(m.group(1))
        if not e.free_symbols <= {X}:
            raise ValueError("a rule is in x, like x in RR -> x + 2")
        return ("rule", m.group(1))
    m = MAP_RE.match(p)
    if not m:
        raise ValueError("write it like: domain 7, 5; range 3, 4; 7 -> 3, 5 -> 3, 5 -> 4")
    domain = [s.strip() for s in m.group(1).split(",")]
    range_ = [s.strip() for s in m.group(2).split(",")]
    arrows = []
    for s in m.group(3).split(","):
        a, _, b = s.partition("->")
        a, b = a.strip(), b.strip()
        if a not in domain or b not in range_:
            raise ValueError(f"an arrow goes from the domain to the range: not {s.strip()}")
        arrows.append((a, b))
    if len(set(domain)) != len(domain) or len(set(range_)) != len(range_):
        raise ValueError("list each member once")
    return ("map", domain, range_, arrows)

COUNT = {0: "no image", 2: "two images", 3: "three images", 4: "four images"}

def mapping_answer(prompt):
    m = read_mapping(prompt)
    if m[0] == "rule":
        return "function"
    _, domain, _, arrows = m
    for d in domain:
        k = len({b for a, b in arrows if a == d})
        if k != 1:
            return f"not a function: {d} has {COUNT[k]}"
    return "function"

def mapping_holds(p):
    m = read_mapping(p["prompt"])
    if m[0] == "rule":
        return p["answer"] == "function"
    _, domain, _, arrows = m
    images = {d: set() for d in domain}
    for a, b in arrows:
        images[a].add(b)
    if all(len(v) == 1 for v in images.values()):
        return p["answer"] == "function"
    got = re.match(r"^not a function: (\S+) has (no|two|three|four) images?$", p["answer"])
    words = {"no": 0, "two": 2, "three": 3, "four": 4}
    return bool(got) and got.group(1) in images and len(images[got.group(1)]) == words[got.group(2)] != 1

# ------------------------------------------------------------------
# Type 9: sets of ordered pairs
# ------------------------------------------------------------------
def read_pairs(prompt):
    rels = AF.split_top(prompt, ";")
    if len(rels) < 2 or not all(r.startswith("{") and r.endswith("}") and AF.pairs(r) for r in rels):
        raise ValueError("write the sets like {(1, 2), (2, 3)}; {(1, 2), (1, 3)}")
    return [AF.pairs(r) for r in rels]

def pairs_answer(prompt):
    rels = read_pairs(prompt)
    out = [chr(97 + i) for i, rel in enumerate(rels) if len({a for a, _ in rel}) == len(set(rel))]
    return ", ".join(out) if out else "none"

def pairs_holds(p):
    rels = read_pairs(p["prompt"])
    got = [a.strip() for a in p["answer"].split(",")]
    want = [chr(97 + i) for i, rel in enumerate(rels) if AF.is_function(rel)]
    return got == (want or ["none"])

# ------------------------------------------------------------------
# Type 10: graphs
# ------------------------------------------------------------------
PIECE = re.compile(r"^([xy])\s*=\s*(.+?),\s*([xy]) in ([\[(])\s*(-?oo|-?\d+)\s*,\s*(-?oo|-?\d+)\s*([\])])$")
EXP = re.compile(r"\d+\^\(?-?x\)?")

def end_value(s):
    return -sp.oo if s == "-oo" else sp.oo if s == "oo" else sp.Integer(int(s))

def read_graph(prompt):
    """[(var, expression, interval)]: var "y" for y = f(x) on an x interval, "x" for x = g(y)."""
    out = []
    for part in prompt.split(";"):
        m = PIECE.match(" ".join(part.split()))
        if not m:
            raise ValueError("write each piece like: y = 1, x in (-oo, 1]  or  x = 3 y - y^3, y in (-oo, oo)")
        var, e, ivar, lb, lo, hi, rb = m.groups()
        if (var, ivar) not in (("y", "x"), ("x", "y")):
            raise ValueError("y = f(x) runs over x; x = g(y) over y")
        lo, hi = end_value(lo), end_value(hi)
        if lo == -sp.oo and lb != "(" or hi == sp.oo and rb != ")" or not lo < hi:
            raise ValueError("an interval runs from lo to hi, with ( at oo")
        expr = to_sympy(e)
        other = Y if var == "x" else X
        if not expr.free_symbols <= {other}:
            raise ValueError(f"{var} = an expression in {other}")
        out.append((var, expr, sp.Interval(lo, hi, lb == "(", rb == ")")))
    if sum(v == "x" for v, _, _ in out) and len(out) > 1:
        raise ValueError("a sideways curve stands alone")
    return out

def exp_parts(e, v):
    """e = A + B c^(s v): (A, B, c, s), or None if e is a polynomial."""
    if e.is_polynomial(v):
        return None
    A, rest = e.as_independent(v, as_Add=True)
    B, pw = rest.as_independent(v, as_Mul=True)
    if not (isinstance(pw, sp.Pow) and pw.base.is_number and pw.base > 1 and (pw.exp / v).is_number):
        raise ValueError("this bank draws polynomials and 2^x")
    return A, B, pw.base, pw.exp / v

def changes_direction(e, v, I):
    """Does e turn around (its slope change sign) inside I? A constant counts: it isn't one-to-one."""
    if exp_parts(e, v) is not None:
        return False
    p = sp.Poly(e, v)
    if p.degree() < 1:
        return I.measure > 0
    d = sp.Poly(sp.diff(e, v), v)
    if d.degree() < 1:
        return False
    return any(m % 2 == 1 and z.is_real and I.contains(z) and z not in I.boundary for z, m in sp.roots(d).items())

def image(e, I):
    """The values of a monotone piece on I: from its ends, the open and closed kept."""
    def at(t, side):
        if t.is_finite:
            return e.subs(X, t)
        return sp.limit(e, X, t)
    a, b = at(I.start, 1), at(I.end, -1)
    lo_open, hi_open = I.left_open, I.right_open
    if a > b:
        a, b, lo_open, hi_open = b, a, hi_open, lo_open
    return sp.Interval(a, b, lo_open or not a.is_finite, hi_open or not b.is_finite)

def graph_answer(prompt):
    """The key, from the pieces: a sideways curve that turns is not a function; y-pieces whose
    x intervals overlap are not; a function is one-to-one when no piece turns or is flat and
    no two pieces share a value."""
    pieces = read_graph(prompt)
    if pieces[0][0] == "x":
        var, g, J = pieces[0]
        if not changes_direction(g, Y, J):
            raise ValueError("a sideways curve that doesn't turn is a function of x; write it as y = f(x)")
        return "not a function"
    for i, (_, _, I) in enumerate(pieces):
        for _, _, K in pieces[i + 1:]:
            if I.intersect(K) != sp.S.EmptySet:
                return "not a function"
    if any(changes_direction(e, X, I) for _, e, I in pieces):
        return "function, not one-to-one"
    if len(pieces) == 1:
        return "function, one-to-one"
    ims = [image(e, I) for _, e, I in pieces]
    for i, a in enumerate(ims):
        for b in ims[i + 1:]:
            if a.intersect(b) != sp.S.EmptySet:
                return "function, not one-to-one"
    return "function, one-to-one"

GRID = [sp.Rational(n, 4) for n in range(-24, 25)]

def hits(e, v, I, level):
    """How many points of the piece e(v), v in I, have the value `level`: 2 means two or more."""
    ex = exp_parts(e, v)
    if ex is not None:
        A, B, c, s = ex
        q = (level - A) / B
        if q <= 0:
            return 0
        t = sp.log(q, c) / s
        return 1 if I.contains(t) else 0
    p = sp.Poly(e - level, v)
    if p.is_zero:
        return 2 if I.measure > 0 else 1
    lo, hi = I.start, I.end
    n = p.count_roots(lo if lo.is_finite else None, hi if hi.is_finite else None)
    for t, op in ((lo, I.left_open), (hi, I.right_open)):
        if op and t.is_finite and p.eval(t) == 0:
            n -= 1
    return min(n, 2)

def graph_holds(p):
    """The vertical and horizontal line tests, run on the pieces: at every end and level, and on a grid."""
    pieces = read_graph(p["prompt"])
    xs = set(GRID) | {t for _, _, I in pieces for t in I.boundary if t.is_finite}
    ys = set(GRID)
    for var, e, I in pieces:
        if var == "y":
            ys |= {e.subs(X, t) for t in I.boundary if t.is_finite}
            if e.is_number:
                ys.add(e)
    def vertical(x0):
        n = 0
        for var, e, I in pieces:
            n += (1 if I.contains(x0) else 0) if var == "y" else hits(e, Y, I, x0)
        return n
    if any(vertical(x0) > 1 for x0 in xs):
        return p["answer"] == "not a function"
    one = all(sum(hits(e, X, I, y0) for _, e, I in pieces) <= 1 for y0 in ys)
    return p["answer"] == ("function, one-to-one" if one else "function, not one-to-one")

# ------------------------------------------------------------------
# Solving and checking
# ------------------------------------------------------------------
def answer_of(prompt):
    k = kind(prompt)
    if k == "evaluate":
        defs, asks = AF.read(prompt)
        if len(defs) != 1 or len(asks) != 1:
            raise ValueError("write it like: f(x) = x^2 + x - 10; f(5)")
        return AF.answer_of(prompt)
    if k == "trig":
        name, e, c, angle = read_trig(prompt)
        ask = prompt.split(";")[1].strip()
        return f"{ask} = {single(trig_value(prompt))}"
    if k == "domain":
        return domain_answer(read_function(prompt)[1])
    if k == "root":
        return root_answer(read_function(prompt)[1])
    if k == "quotient":
        return quotient_answer(read_function(prompt)[1])
    if k == "mapping":
        return mapping_answer(prompt)
    if k == "pairs":
        return pairs_answer(prompt)
    return graph_answer(prompt)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt))

def evaluate_holds(p):
    defs, asks = AF.read(p["prompt"])
    lhs, _, rhs = p["answer"].partition("=")
    if " ".join(lhs.split()) != " ".join(asks[0].split()) or "(" in rhs.replace("sqrt(", ""):
        return False                                  # names what it finds; multiplied out
    want = tx(AF.value(defs, asks[0]))
    return same_value(rhs, want)

def trig_holds(p):
    lhs, _, rhs = p["answer"].partition("=")
    ask = p["prompt"].split(";")[1].strip()
    return (" ".join(lhs.split()) == ask and L20.simplest(rhs.strip())
            and same_value(rhs, tx(trig_value(p["prompt"]))))

def check(p):
    try:
        k = kind(p["prompt"])
        if k != KIND[p["type"]]:
            return "failed"
        if k == "evaluate":
            x_arg = "x" in AF.read(p["prompt"])[1][0]
            ok = x_arg == (p["type"] == "2") and evaluate_holds(p)
        elif k == "trig":
            ok = trig_holds(p)
        elif k == "domain":
            f = read_function(p["prompt"])[1]
            rooted = bool(radicands(f))
            ok = rooted == (p["type"] == "4") and domain_holds(f, read_set(p["answer"], "x"))
        elif k in ("root", "quotient"):
            f = read_function(p["prompt"])[1]
            S, R = split_answer(p["answer"])
            ranged = root_range_holds if k == "root" else quotient_range_holds
            ok = domain_holds(f, S) and ranged(f, S, R)
        elif k == "mapping":
            ok = mapping_holds(p)
        elif k == "pairs":
            ok = pairs_holds(p)
        else:
            ok = graph_holds(p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]), tries=600)

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def math_(t):
    return f"${dfrac(t)}$"

def trig_shown(t):
    t = re.sub(r"\b(sin|cos|tan)\(theta\)", r"\1 theta", t)
    return L20.shown(t)

def set_shown(t):
    return f"${t}$"

def statement(p):
    """The problem's words (Typst markup), without a figure."""
    k, prompt = kind(p["prompt"]), p["prompt"]
    if k == "evaluate":
        d, ask = [s.strip() for s in prompt.split(";")]
        return f"If {math_(d)}, find {math_(ask)}."
    if k == "trig":
        d, ask = [s.strip() for s in prompt.split(";")]
        return f"If ${trig_shown(d)}$, find ${trig_shown(ask)}$."
    if k == "domain":
        return math_(prompt.split(";")[0].strip())
    if k in ("root", "quotient"):
        return math_(prompt)
    if k == "pairs":
        rels = AF.split_top(prompt, ";")
        return " #h(1.5em) ".join(f"#box[({chr(97 + i)}) #h(0.2em) ${rel}$]" for i, rel in enumerate(rels))
    return ""

def mapping_figure(prompt, unit="1cm"):
    m = read_mapping(prompt)
    if m[0] == "rule":
        return fig.rule_mapping("$x in RR$", f"${m[1]}$", f"$y = {m[1]}$", unit)
    _, domain, range_, arrows = m
    mark = lambda s: f"${s}$"
    return fig.mapping([mark(d) for d in domain], [mark(v) for v in range_],
                       [(domain.index(a), range_.index(b)) for a, b in arrows], unit=unit)

WINDOW = 3

def sketch(prompt, width=2.6, slide_width=None):
    """A graph with no scale, as the book draws for the line tests."""
    g = Graph(x=(-WINDOW, WINDOW), y=(-WINDOW, WINDOW), width=width, grid=False, numbers=False,
              slide_width=slide_width)
    far = WINDOW + 2
    for var, e, I in read_graph(prompt):
        lo = I.start if I.start.is_finite else -far
        hi = I.end if I.end.is_finite else far
        kind_of = lambda t, op: "arrow" if not t.is_finite else ("open" if op else "closed")
        ends = (kind_of(I.start, I.left_open), kind_of(I.end, I.right_open))
        fn = sp.lambdify(X if var == "y" else Y, e, "math")
        n = 240
        ts = [float(lo) + (float(hi) - float(lo)) * i / n for i in range(n + 1)]
        pts = [(t, fn(t)) for t in ts] if var == "y" else [(fn(t), t) for t in ts]
        g.polyline(pts, color="black", width=1.8, ends=ends)
    return g.typst()

def root_graph(f, drawn, width=None, slide_width=None):
    """Type 6's axes, and (drawn) the curve through the points where the radicand is 0, 1, 4, 9."""
    e, side = root_end(f)
    xs = [e + side * d for d in (0, 1, 4, 9)]
    x0 = int(min(min(xs), 0)) - 1
    x1 = int(max(max(xs), 0)) + 1
    width = width or 0.42 * (x1 - x0)
    g = Graph(x=(x0, x1), y=(-1, 4), width=width, slide_width=slide_width or 2 * width)
    if drawn:
        fn = sp.lambdify(X, f, "math")
        far = x1 + 1 if side > 0 else x0 - 1
        n = 200
        ts = [float(e) + (far - float(e)) * i / n for i in range(n + 1)]
        g.polyline([(t, fn(t)) for t in ts], color="blue", width=1.4, ends=("closed", "arrow"))
        for t in xs[1:]:
            g.point(float(t), float(f.subs(X, t)), color="blue")
    return g.typst()

def quotient_graph(f, width=4.0, slide_width=None):
    """Type 7's graph, for the key: the root's end, the dashed asymptote, both branches."""
    b, a = quotient_shape(f)
    x0, x1 = int(min(b, 0)) - 1, int(a) + 6
    g = Graph(x=(x0, x1), y=(-5, 5), width=width, step=1, slide_width=slide_width or 2 * width)
    g.vertical(float(a), color="gray", width=0.9, dash="dashed", ends=None)
    fn = sp.lambdify(X, f, "math")
    n = 300
    left = [float(b) + (float(a) - 1e-4 - float(b)) * i / n for i in range(n + 1)]
    right = [float(a) + 1e-4 + (x1 + 1 - float(a)) * (i / n) ** 2 for i in range(n + 1)]
    g.polyline([(t, fn(t)) for t in left], color="blue", width=1.4, ends=("closed", "arrow"))
    g.polyline([(t, fn(t)) for t in right], color="blue", width=1.4, ends="arrow")
    return g.typst()

def figure(p, key=False, slide=False):
    """The figure the problem carries, or that its key draws; "" for none."""
    k = kind(p["prompt"])
    if k == "mapping":
        return mapping_figure(p["prompt"], "2.2cm" if slide else "1cm")
    if k == "graph":
        return sketch(p["prompt"], width=7 if slide else 2.6)
    if k == "root":
        f = read_function(p["prompt"])[1]
        return root_graph(f, key)
    if k == "quotient" and key:
        return quotient_graph(read_function(p["prompt"])[1])
    return ""

def _prompt(p, key):
    try:
        s, f = statement(p), figure(p, key)
    except (ValueError, KeyError, SyntaxError, TypeError):
        return f"${p['prompt']}$"
    if not f:
        return s
    if not s:
        return f"#align(center)[{f}]"
    return f"#grid(columns: (auto, auto), column-gutter: 1.5em, align: horizon, [{s}], [{f}])"

def typst(p, gap="0.3em"):
    return _prompt(p, False)

def key_typst(p, gap="0.3em"):
    """The key's prompt: Type 6's curve drawn on its axes, Type 7's graph beside it."""
    return _prompt(p, True)

SENTENCE = {"function": "Function", "not a function": "Not a function", "function, one-to-one": "Function, one-to-one",
            "function, not one-to-one": "Function, not one-to-one"}

def letters_shown(answer):
    ls = [f"({a.strip()})" for a in answer.split(",")]
    if ls == ["(none)"]:
        return "none"
    return ls[0] if len(ls) == 1 else " and ".join(ls) if len(ls) == 2 else ", ".join(ls[:-1]) + ", and " + ls[-1]

def answer_typst(p):
    a, k = p["answer"], KIND.get(p["type"])
    if k == "evaluate":
        return display(dfrac(a))
    if k == "trig":
        return display(trig_shown(a))
    if k == "domain":
        return set_shown(a)
    if k in ("root", "quotient"):
        try:
            d, r = [s.strip() for s in a.split(";")]
        except ValueError:
            return f"${a}$"
        return f'$"Domain" = {d}$ \\\n$"Range" = {r}$'
    if k == "mapping":
        head, _, why = a.partition(": ")
        return f"*{SENTENCE.get(head, head)}*" + (f": ${why.split()[0]}$ {' '.join(why.split()[1:])}" if why else "")
    if k == "pairs":
        return f"*{letters_shown(a)}*"
    return f"*{SENTENCE.get(a, a)}*"

SLIDE = {"8", "10", "6", "7"}

def slide_typst(p, key=False):
    """A figure's slide: the words and the answer (hidden on the question slide) beside the
    figure, drawn larger; for Types 6 and 7 the graph is part of the answer, hidden too, so
    nothing moves when the answer shows. None for the other types."""
    if p["type"] not in SLIDE:
        return None
    try:
        s = statement(p)
        k = kind(p["prompt"])
        if k == "root":
            f = root_graph(read_function(p["prompt"])[1], key)
        elif k == "quotient":
            f = quotient_graph(read_function(p["prompt"])[1])
            f = f if key else f"#hide[{f}]"
        else:
            f = figure(p, slide=True)
    except (ValueError, KeyError, SyntaxError, TypeError):
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    left = f"{s} #v(0.8em) {shown}" if s else shown
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{left}], [{f}])"

def text(p):
    k = kind(p["prompt"])
    if k == "evaluate":
        d, ask = [s.strip() for s in p["prompt"].split(";")]
        return f"If {plain(d)}, find {plain(ask)}."
    if k == "trig":
        d, ask = [s.strip() for s in p["prompt"].split(";")]
        t = lambda s: L20.readable(re.sub(r"\b(sin|cos|tan)\(theta\)", r"\1 θ", s).replace("theta", "θ"))
        return f"If {t(d)}, find {t(ask)}."
    if k == "domain":
        return plain(p["prompt"].split(";")[0])
    if k in ("root", "quotient"):
        return plain(p["prompt"])
    if k == "pairs":
        return "   ".join(f"({chr(97 + i)}) {rel}" for i, rel in enumerate(AF.split_top(p["prompt"], ";")))
    return plain(p["prompt"].replace("RR", "ℝ").replace(" in ", " ∈ ")) + "   [figure]"

def answer_text(p):
    a = p["answer"]
    if p["type"] == "9":
        return letters_shown(a)
    if p["type"] == "3":
        return L20.readable(a)
    return plain(a.replace(" in RR", " ∈ ℝ"))

def height(p):
    return {"6": 1.9, "8": 1.5, "9": 0.5, "10": 1.0, "7": 0.5}.get(p["type"], 0.4)

# ------------------------------------------------------------------
# Editing: the prompt is the problem's data, in its short form
# ------------------------------------------------------------------
EXAMPLE = {"1": "f(x) = x^2 + x - 10; f(5)", "2": "f(x) = x^2 + 1; f(x + 2)",
           "3": "g(theta) = 4 sqrt(3) cos(theta); g(60 degree)", "4": "f(x) = sqrt(10 - x); domain",
           "5": "g(x) = 1/(x - 2); domain", "6": "y = sqrt(x + 4)", "7": "f(x) = sqrt(x)/(x - 2)",
           "8": "domain 7, 5; range 3, 4; 7 -> 3, 5 -> 3, 5 -> 4", "9": "{(1, 2), (2, 3)}; {(1, 2), (1, 3)}",
           "10": "y = 1, x in (-oo, 1]; y = -1, x in (1, oo)"}

def clean(t):
    t = t.replace("−", "-").replace("°", " degree").replace("θ", "theta").replace("ℝ", "RR").replace("∈", "in")
    t = t.replace("→", "->").replace("∞", "oo").replace("≠", "!=").replace("≥", ">=").replace("≤", "<=")
    return " ".join(t.split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    try:
        if kind(t) != KIND[old["type"]]:
            raise ValueError
        answer = answer_of(t)
        new = dict(old, prompt=t, answer=answer, source="edited")
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
    if p["type"] == "9":
        t = ", ".join(re.findall(r"[a-z]+", t.lower()))
    elif p["type"] in ("8", "10"):
        t = t.lower()
    new = dict(p, answer=t)
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)
