"""Lesson 10 (Advanced Math): equation of a line, rational denominators,
completing the square. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_010/slides/deck_010.typ): examples
10.1-10.6 and Problem Set 10, problems 5, 6, and 9-13.

    1  a line through two points:        (-3, 2), (4, -3)                  y = -5/7 x - 1/7
    2  through a point, parallel:        y = 2 x - 1; (4, 1)               y = 2 x - 7
    3  through a point, perpendicular:   3 y + 4 x = 2; (-2, 5)            y = 3/4 x + 13/2
    4  lines (a) and (b) from a graph:   y = -2; (-6, -5), (-1, 6)         y = -2; y = 11/5 x + 41/5
    5  a radical binomial below:         (4 + sqrt(3))/(2 - 3 sqrt(3))     (-17 - 14 sqrt(3))/23
    6  dividing complex numbers:         (2 - i^3 + 2 i^5)/(-2 i + 4)      1/10 + 4/5 i
    7  completing the square:            -x + 3 x^2 = -5                   x = 1/6 plus.minus sqrt(59)/6 i

The problem types file puts examples 10.2 (perpendicular) and problem 6
(parallel) under one heading; they are Types 2 and 3 here, because the
perpendicular one has a move of its own (the negative reciprocal). Type 4 is
example 10.3 alone (no problem reads lines from a graph): one graph with a
horizontal or vertical line (a) and a slanted line (b) through two whole-number
points. Both lines run across the whole graph, arrowheads on their ends (the
book's (b) stops at its two points; the teacher asked for the full line). Line (a) is horizontal in the book; a vertical
one is drawn a third of the time ("neither horizontal nor vertical", the deck
says of (b)).

The key writes what the deck writes:
    - a line in slope-intercept form, lowest terms, a slope of 1 or -1 written x
      or -x, b left off when 0 (Lesson 2-1's slope_intercept): y = -5/7 x - 1/7,
      y = -x + 1, y = 3/4 x + 13/2; a horizontal line y = -2, a vertical one x = 3.
      Type 4's answer is the two lines, (a) first, separated by ";".
    - a radical answer as the deck's bold one: the number first, then the radical,
      over one positive denominator, in lowest terms: (-17 - 14 sqrt(3))/23; no
      denominator when it divides: -4 - 2 sqrt(3).
    - a complex answer in standard form, each part its own fraction: 1/10 + 4/5 i,
      4/13 + 7/13 i.
    - completing the square: the letter and its two values, the larger first, when
      they are rational (x = 6 or x = -2); otherwise the rational part plus or minus the
      radical part, each in lowest terms, with i after an imaginary one:
      x = 1/6 plus.minus sqrt(59)/6 i, x = -1/6 plus.minus sqrt(59)/6 i.

check() is independent of how a problem was built:
    - Types 1-3: the answer is read strictly as slope-intercept form (Lesson 2-1's
      reader); its slope is worked out again from the prompt (two points, or the
      given line solved for y with sympy, then the same or the negative reciprocal
      slope), and the point(s) must lie on it.
    - Type 4: (a) must be the prompt's horizontal or vertical line, (b) the line
      through the prompt's two points, read strictly as above.
    - Types 5-6: the answer equals the prompt exactly (sympy), and its text has the
      key's form: one radical over a whole number, or a + b i, lowest terms, no
      radical or i below, radicands square-free. The minus-in-front form,
      -(17 + 14 sqrt(3))/23, is accepted too.
    - Type 7: each value is put back into the equation exactly; there must be two;
      rational values written with "or", others with plus.minus, radicands square-free,
      no square root of a negative (the i written out).

Skipped sources: none. Lesson 10's examples have no proofs.

A problem: dict(type, prompt, answer, source), in Typst math. Lines' prompts:
    Type 1  "(-3, 2), (4, -3)"            Type 2-3  "3 y + 4 x = 2; (-2, 5)"
    Type 4  "y = -2; (-6, -5), (-1, 6)"   (line (a); two points on line (b))
"""
import math, re
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need, written
from ..check import to_sympy, simplest_form
from ..graphs import Graph, PREAMBLE as GRAPH_PREAMBLE
from ..typmath import fr, display, dfrac, text as plain
from . import slope_intercept_2_1 as si
from . import point_slope_2_2 as ps
from .adv_rationalize import term, ipow

NAME = FAMILY = "adv_lesson_10"
FIXED = False
TITLE = "Lesson 10: Equation of a Line, Rational Denominators, Completing the Square"
INSTRUCTIONS = ""              # each type has its own; a sheet of one type shows it at the top
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = GRAPH_PREAMBLE

LINE = "Write each equation in slope-intercept form."
SIMPLIFY = "Simplify. Leave no radical and no i in a denominator."   # plain: instructions are escaped text
TYPES = [
    dict(key="1", title="A Line Through Two Points", instructions=LINE,
         look="Two points, and the line through them.",
         move="Slope: change in $y$ over change in $x$, $m = (-5)/(+7) = -5/7$. Put $m$ in $y = m x + b$, "
              "use one point for $x$ and $y$, and solve for $b$: $2 = -5/7 (-3) + b$, so $b = -1/7$."),
    dict(key="2", title="Through a Point, Parallel to a Line", instructions=LINE,
         look="A point, and a line the answer is parallel to.",
         move="Solve the given line for $y$ if it isn't already. Parallel lines have equal slopes. Put the "
              "slope and the point in $y = m x + b$: $1 = 2(4) + b$, so $b = -7$."),
    dict(key="3", title="Through a Point, Perpendicular to a Line", instructions=LINE,
         look="A point, and a line the answer is perpendicular to.",
         move="Solve the given line for $y$: $3 y + 4 x = 2$ gives $y = -4/3 x + 2/3$. Perpendicular slopes are "
              "negative reciprocals, so $m = 3/4$. Put it and the point in $y = m x + b$ and solve for $b$."),
    dict(key="4", title="Equations of Lines from a Graph", instructions="Find the equations of the lines.",
         look="A graph with a horizontal or vertical line (a) and a slanted line (b).",
         move="A horizontal line is $y = k$; a vertical one is $x = h$. For (b), read two points, find the "
              "slope from them, and use one point in $y = m x + b$.", space="0.5in"),
    dict(key="5", title="A Radical Binomial Below", instructions=SIMPLIFY,
         look="A denominator like $2 - 3 sqrt(3)$.",
         move="Multiply above and below by the conjugate, $2 + 3 sqrt(3)$. Below: $4 - 27 = -23$. Multiply out "
              "the top, and reduce.", space="1.5in"),
    dict(key="6", title="Dividing Complex Numbers", instructions=SIMPLIFY,
         look="A complex number below, maybe with powers of $i$.",
         move="Write both in standard form ($i^3 = -i$, $i^5 = i$). Multiply above and below by the conjugate "
              "of the denominator: below, $(4 - 2 i)(4 + 2 i) = 20$. Write $a + b i$.", space="1.5in"),
    dict(key="7", title="Completing the Square", instructions="Solve by completing the square.",
         look="A quadratic equation.",
         move="Write it in standard form and divide by the coefficient of $x^2$. Move the constant right, add "
              "$(1/2 dot b)^2$ to both sides, write the left side as a square, and take the square root of both "
              "sides: $(x - 1/6)^2 = -59/36$.", space="1.75in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

X, Y = sp.symbols("x y")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Lines
# ------------------------------------------------------------------
COORD = range(-9, 10)                 # a point's coordinates
BIG_B = 20                            # the answer's y-intercept, at most this either way
POINT = re.compile(r"\((-?\d+), (-?\d+)\)")

def point(x, y):
    return f"({x}, {y})"

def points_of(t):
    """The whole-number points written in t, as Fractions."""
    return [(F(int(a)), F(int(b))) for a, b in POINT.findall(t)]

def line_through(p, q):
    """(m, b) of the line through two points with different x."""
    m = (q[1] - p[1]) / (q[0] - p[0])
    return m, p[1] - m * p[0]

# ---- Type 1: (-3, 2), (4, -3) (example 10.1, problem 5)
def t1_ok(x1, y1, x2, y2):
    return (all(v in COORD for v in (x1, y1, x2, y2)) and x1 != x2 and y1 != y2
            and abs(line_through((F(x1), F(y1)), (F(x2), F(y2)))[1]) <= BIG_B)

def t1_pick(r):
    return dict(x1=r.choice(COORD), y1=r.choice(COORD), x2=r.choice(COORD), y2=r.choice(COORD))

def t1(x1, y1, x2, y2):
    need(t1_ok(x1, y1, x2, y2))
    return f"{point(x1, y1)}, {point(x2, y2)}"

# ---- Types 2-3: a given line and a point (example 10.2, problem 6)
FORMS = ("si", "y first", "x first")  # y = 2 x - 1;  3 y + 4 x = 2;  4 x + 3 y = 2
TOP = range(1, 7)                     # |a|: the slope's numerator, or the x coefficient
BOTTOM = range(1, 7)                  # c: the slope's denominator, or the y coefficient
CONST = range(-9, 10)                 # k: the y-intercept, or the constant on the right

def given(form, a, c, k):
    """The given line: y = (a/c) x + k, or c y + a x = k with the y or the x term first."""
    if form == "si":
        return si.slope_intercept(F(a, c), F(k))
    terms = ((c, "y"), (a, "x")) if form == "y first" else ((a, "x"), (c, "y"))
    return f"{written(*terms)} = {k}"

def given_slope(form, a, c):
    return F(a, c) if form == "si" else F(-a, c)

def wanted_slope(typ, m):
    return m if typ == "2" else -1 / m

def lines_ok(typ, form, a, c, k, px, py):
    if not (form in FORMS and abs(a) in TOP and c in BOTTOM and k in CONST and px in COORD and py in COORD):
        return False
    if form == "si":
        ok = math.gcd(abs(a), c) == 1 and c <= 5
    else:
        ok = k != 0 and math.gcd(math.gcd(abs(a), c), abs(k)) == 1
    m = given_slope(form, a, c)
    on = (py == m * px + k) if form == "si" else (c * py + a * px == k)
    w = wanted_slope(typ, m)
    return ok and not (typ == "2" and on) and abs(py - w * px) <= BIG_B

def lines_pick(r):
    form = r.choice(FORMS)
    return dict(form=form, a=gen.signed(r, 1, 6), c=r.choice((1, 1, 2, 3, 4, 5) if form == "si" else BOTTOM),
                k=r.choice(CONST), px=r.choice(COORD), py=r.choice(COORD))

def t2(form, a, c, k, px, py):
    need(lines_ok("2", form, a, c, k, px, py))
    return f"{given(form, a, c, k)}; {point(px, py)}"

def t3(form, a, c, k, px, py):
    need(lines_ok("3", form, a, c, k, px, py))
    return f"{given(form, a, c, k)}; {point(px, py)}"

# ---- Type 4: line (a) and line (b) through two points, on a -6 to 6 graph (example 10.3)
GRID = 6
LEVEL = tuple(v for v in range(-5, 6) if v)       # (a): y = k or x = k, not an axis
END = tuple(v for v in range(-GRID, GRID + 1) if v)

def t4_ok(kind, k, x1, y1, x2, y2):
    if not (kind in ("y", "x") and k in LEVEL and all(v in END for v in (x1, y1, x2, y2))):
        return False
    dx, dy = x2 - x1, y2 - y1
    on_a = (lambda x, y: (y if kind == "y" else x) == k)
    return (dx >= 2 and abs(dy) >= 2 and dx * dx + dy * dy >= 36 and not on_a(x1, y1) and not on_a(x2, y2)
            and abs(line_through((F(x1), F(y1)), (F(x2), F(y2)))[1]) <= BIG_B)

def t4_pick(r):
    return dict(kind=r.choice(("y", "y", "x")), k=r.choice(LEVEL),
                x1=r.choice(END), y1=r.choice(END), x2=r.choice(END), y2=r.choice(END))

def t4(kind, k, x1, y1, x2, y2):
    need(t4_ok(kind, k, x1, y1, x2, y2))
    need(labels(f"{kind} = {k}", [(x1, y1), (x2, y2)]) is not None)
    return f"{kind} = {k}; {point(x1, y1)}, {point(x2, y2)}"

# ------------------------------------------------------------------
# Type 5: (a + b sqrt(c))/(d + e sqrt(c)) (example 10.4, problem 11)
# ------------------------------------------------------------------
RADICANDS = (2, 3, 5, 6, 7)
TOP5 = range(1, 10)                   # a, the top's number
COEF5 = range(1, 7)                   # |b|, d, |e|
BIG5 = 120                            # the answer's numbers

def t5_parts(a, b, d, e, c):
    """(P, Q, D): the answer (P + Q sqrt(c))/D in lowest terms, D > 0."""
    P, Q, D = a * d - b * e * c, b * d - a * e, d * d - e * e * c
    g = math.gcd(math.gcd(P, Q), D) * (1 if D > 0 else -1)
    return P // g, Q // g, D // g

def t5_ok(a, b, d, e, c):
    if not (a in TOP5 and abs(b) in COEF5 and d in COEF5 and abs(e) in COEF5 and c in RADICANDS):
        return False
    if a * e == b * d:
        return False                      # top a multiple of the bottom: a whole number
    P, Q, D = t5_parts(a, b, d, e, c)
    return P != 0 and Q != 0 and max(abs(P), abs(Q), D) <= BIG5

def t5_negative_pick(r):              # the deck's 10.4: below, 4 - 27 = -23
    c = r.choice((2, 3, 3, 5))
    d, e = r.randint(1, 4), gen.signed(r, 2, 3)
    need(d * d < e * e * c)
    return dict(a=r.randint(1, 5), b=gen.signed(r, 1, 3), d=d, e=e, c=c)

def t5_reduces_pick(r):               # problem 11: the denominator divides, -4 - 2 sqrt(3)
    c = r.choice((2, 3, 3, 5))
    d, e = r.randint(1, 3), gen.signed(r, 1, 2)
    A, B = gen.signed(r, 1, 5), gen.signed(r, 1, 3)
    return dict(a=A * d + B * e * c, b=A * e + B * d, d=d, e=e, c=c)

def t5_any_pick(r):
    return dict(a=r.choice(TOP5), b=gen.signed(r, 1, 6), d=r.choice(COEF5), e=gen.signed(r, 1, 6),
                c=r.choice(RADICANDS))

def t5(a, b, d, e, c):
    need(t5_ok(a, b, d, e, c))
    return fr(term(a, "", True) + term(b, f"sqrt({c})"), term(d, "", True) + term(e, f"sqrt({c})"))

def radical_answer(P, Q, D, c):
    top = written((P, ""), (Q, f"sqrt({c})"))
    return top if D == 1 else f"({top})/{D}"

# ------------------------------------------------------------------
# Type 6: complex division, powers of i allowed (example 10.5, problems 9-10)
# ------------------------------------------------------------------
I_POWER = {0: 1, 1: sp.I, 3: -sp.I, 5: sp.I}
POWERS = tuple(I_POWER)
COEF6 = range(1, 7)
TERMS6 = (2, 3)                       # terms above; below, always 2

def standard(terms):
    """(real, imaginary) of a sum of c i^k terms, as ints."""
    z = sum(c * I_POWER[k] for c, k in terms)
    return int(sp.re(z)), int(sp.im(z))

def t6_ok(top, bottom):
    if not (len(top) in TERMS6 and len(bottom) == 2):
        return False
    if not all(abs(c) in COEF6 and k in POWERS for c, k in top + bottom):
        return False
    if len({k for _, k in top}) != len(top) or len({k for _, k in bottom}) != 2:
        return False                      # no two terms with the same power on a side
    a, b = standard(top)
    c, d = standard(bottom)
    return (a != 0 and b != 0 and c != 0 and d != 0 and c * c + d * d <= 61
            and a * c + b * d != 0 and b * c - a * d != 0)     # both parts of the answer

def t6_plain_pick(r):                 # problem 9: (2 + i)/(3 - 2 i)
    return dict(top=((r.randint(1, 6), 0), (gen.signed(r, 1, 6), 1)),
                bottom=((gen.signed(r, 1, 6), 0), (gen.signed(r, 1, 6), 1)))

def t6_powers_pick(r):                # 10.5 and problem 10: (2 - i^3 + 2 i^5)/(-2 i + 4), i term below first
    k1, k2 = r.sample((1, 3, 5), 2)
    top = ((r.randint(1, 5), 0), (gen.signed(r, 1, 3), k1), (gen.signed(r, 1, 3), k2))
    c, d, k = gen.signed(r, 1, 5), gen.signed(r, 1, 4), r.choice((1, 1, 3, 5))
    bottom = ((d, k), (c, 0)) if r.random() < 0.75 else ((c, 0), (d, k))
    return dict(top=top, bottom=bottom)

def side(terms):
    return "".join(term(c, ipow(k) if k else "", i == 0) for i, (c, k) in enumerate(terms))

def t6(top, bottom):
    need(t6_ok(top, bottom))
    return fr(side(top), side(bottom))

def number(q):
    return str(F(q))

def complex_answer(re_, im_):
    """a + b i, each part its own fraction: 1/10 + 4/5 i, 2 - i."""
    re_, im_ = F(re_), F(im_)
    if im_ == 0:
        return number(re_)
    body = "i" if abs(im_) == 1 else f"{number(abs(im_))} i"
    if re_ == 0:
        return ("-" if im_ < 0 else "") + body
    return f"{number(re_)} {'-' if im_ < 0 else '+'} {body}"

# ------------------------------------------------------------------
# Type 7: completing the square (example 10.6, problems 12-13)
# ------------------------------------------------------------------
B7 = range(1, 11)                     # |b|, monic
C7 = range(1, 21)                     # |c|, monic
LEAD = range(2, 6)                    # a, otherwise
B7A = range(1, 10)                    # |b| with a leading coefficient
C7A = range(1, 13)                    # |c|, or |k| on the right
ROOT7 = range(-9, 10)                 # a monic problem built from whole roots

def t7_ok(a, b, c):
    return b != 0 and c != 0 and b * b - 4 * a * c != 0 and math.gcd(math.gcd(a, abs(b)), abs(c)) == 1

def t7_monic_ok(v, b, c):
    return v in gen.LETTERS and abs(b) in B7 and abs(c) in C7 and t7_ok(1, b, c)

def t7_lead_ok(v, a, b, c):
    return v in gen.LETTERS and a in LEAD and abs(b) in B7A and abs(c) in C7A and t7_ok(a, b, c)

def t7_monic_pick(r):
    return dict(v=r.choice(gen.LETTERS), b=gen.signed(r, 1, 10), c=gen.signed(r, 1, 20))

def t7_roots_pick(r):                 # problem 12: x^2 - 4 x - 12 = 0, whole roots
    p, q = r.sample(ROOT7, 2)
    return dict(v=r.choice(gen.LETTERS), b=-(p + q), c=p * q)

def t7_lead_pick(r):
    return dict(v=r.choice(gen.LETTERS), a=r.choice(LEAD), b=gen.signed(r, 1, 9), c=gen.signed(r, 1, 12))

def t7_monic(v, b, c):
    need(t7_monic_ok(v, b, c))
    return f"{written((1, f'{v}^2'), (b, v), (c, ''))} = 0"

def t7_lead(v, a, b, c):
    need(t7_lead_ok(v, a, b, c))
    return f"{written((a, f'{v}^2'), (b, v), (c, ''))} = 0"

def t7_scrambled(v, a, b, c):         # 10.6, problem 13: -x + 3 x^2 = -5, so c = 5
    need(t7_lead_ok(v, a, b, c))
    return f"{written((b, v), (a, f'{v}^2'))} = {-c}"

def square_free(n):
    """(f, m): n = f^2 m, m square-free."""
    f, m = 1, n
    for p in range(2, math.isqrt(n) + 1):
        while m % (p * p) == 0:
            m //= p * p
            f *= p
    return f, m

def square_answer(v, a, b, c):
    """The two values of a v^2 + b v + c = 0 (integers, a > 0), as the deck writes them."""
    D = b * b - 4 * a * c
    h = F(-b, 2 * a)
    f, m = square_free(abs(D))
    s = F(f, 2 * a)                   # the radical part is s sqrt(m)
    if D > 0 and m == 1:
        return f"{v} = {number(h + s)} or {v} = {number(h - s)}"
    if m == 1:
        rad = "" if s == 1 else number(s) + " "
    else:
        body = f"sqrt({m})" if s.numerator == 1 else f"{s.numerator} sqrt({m})"
        rad = (body if s.denominator == 1 else fr(body, str(s.denominator))) + " "
    rad = rad + "i" if D < 0 else rad.strip()
    return f"{v} = {number(h)} plus.minus {rad}".rstrip()

# ------------------------------------------------------------------
# The templates
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick, t1)],
    "2": [(lines_pick, t2)],
    "3": [(lines_pick, t3)],
    "4": [(t4_pick, t4)],
    "5": [(t5_negative_pick, t5), (t5_reduces_pick, t5), (t5_any_pick, t5)],
    "6": [(t6_plain_pick, t6), (t6_powers_pick, t6), (t6_powers_pick, t6)],
    "7": [(t7_roots_pick, t7_monic), (t7_monic_pick, t7_monic), (t7_lead_pick, t7_lead),
          (t7_lead_pick, t7_scrambled), (t7_lead_pick, t7_scrambled)],
}
RANGES = {
    t1: t1_ok,
    t2: lambda **p: lines_ok("2", **p),
    t3: lambda **p: lines_ok("3", **p),
    t4: t4_ok, t5: t5_ok, t6: t6_ok,
    t7_monic: t7_monic_ok, t7_lead: t7_lead_ok, t7_scrambled: t7_lead_ok,
}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# Solving (for draws and edits)
# ------------------------------------------------------------------
def split_line(t):
    """("y = 2 x - 1", [(4, 1)]) from "y = 2 x - 1; (4, 1)"."""
    head, _, rest = t.partition(";")
    return head.strip(), points_of(rest)

def slope_of_given(t):
    """The slope of a line in x and y, solved for y with sympy; ValueError if it has none."""
    lhs, eq, rhs = t.partition("=")
    if not eq:
        raise ValueError("no equation")
    e = sp.expand(to_sympy(lhs) - to_sympy(rhs))
    if e.free_symbols - {X, Y} or sp.Poly(e, X, Y).total_degree() != 1:
        raise ValueError("not a line in x and y")
    cy, cx = e.coeff(Y), e.coeff(X)
    if cy == 0 or cx == 0:
        raise ValueError("no slope, or a slope of 0")
    m = -cx / cy
    return F(int(m.p), int(m.q))

def quadratic(prompt):
    """(letter, a, b, c) of a quadratic equation, integers, a > 0; ValueError if it isn't one."""
    lhs, eq, rhs = prompt.partition("=")
    if not eq:
        raise ValueError("no equation")
    e = sp.expand(to_sympy(lhs) - to_sympy(rhs))
    if len(e.free_symbols) != 1:
        raise ValueError("one letter")
    v = next(iter(e.free_symbols))
    poly = sp.Poly(e, v)
    if poly.degree() != 2:
        raise ValueError("not quadratic")
    cs = [sp.Rational(k) for k in poly.all_coeffs()]
    lcm = math.lcm(*(int(k.q) for k in cs))
    a, b, c = (int(k * lcm) for k in cs)
    if a < 0:
        a, b, c = -a, -b, -c
    return str(v), a, b, c

def answer_of(prompt, typ):
    if typ == "1":
        pts = points_of(prompt)
        if len(pts) != 2 or pts[0][0] == pts[1][0]:
            raise ValueError("two points with different x")
        return si.slope_intercept(*line_through(*pts))
    if typ in ("2", "3"):
        head, pts = split_line(prompt)
        if len(pts) != 1:
            raise ValueError("one point")
        m = wanted_slope(typ, slope_of_given(head))
        (px, py), = pts
        return si.slope_intercept(m, py - m * px)
    if typ == "4":
        head, pts = split_line(prompt)
        if not LEVEL_LINE.fullmatch(head) or len(pts) != 2 or pts[0][0] == pts[1][0]:
            raise ValueError("a line and two points")
        return f"{head}; {si.slope_intercept(*line_through(*pts))}"
    if typ == "5":
        e = sp.expand(sp.radsimp(to_sympy(prompt)))
        roots = [p for p in e.atoms(sp.Pow) if p.exp == sp.S.Half]
        if len(roots) != 1:
            raise ValueError("one radical")
        Q = e.coeff(roots[0])
        P = sp.expand(e - Q * roots[0])
        if not (P.is_Rational and Q.is_Rational):
            raise ValueError("not a number")
        L = math.lcm(int(P.q), int(Q.q))
        return radical_answer(int(P * L), int(Q * L), L, int(roots[0].base))
    if typ == "6":
        z = sp.expand(sp.radsimp(to_sympy(prompt, imaginary=True)))
        re_, im_ = sp.re(z), sp.im(z)
        if not (re_.is_Rational and im_.is_Rational):
            raise ValueError("not a complex number")
        return complex_answer(F(int(re_.p), int(re_.q)), F(int(im_.p), int(im_.q)))
    if typ == "7":
        return square_answer(*quadratic(prompt))
    raise ValueError(typ)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt, entry))

# ------------------------------------------------------------------
# Checking, independently of the build
# ------------------------------------------------------------------
LEVEL_LINE = re.compile(r"[xy] = -?\d+")

def read_line(t):
    """(m, b) of an answer read strictly as slope-intercept form; None if it isn't."""
    try:
        return ps.read_slope_intercept(" ".join(t.split()))
    except Exception:
        return None

def on(mb, pt):
    m, b = mb
    return pt[1] == m * pt[0] + b

def check_line(p):
    typ, ans = p["type"], p["answer"]
    if typ == "1":
        pts = points_of(p["prompt"])
        got = read_line(ans)
        return len(pts) == 2 and got is not None and all(on(got, q) for q in pts)
    if typ in ("2", "3"):
        head, pts = split_line(p["prompt"])
        got = read_line(ans)
        return (len(pts) == 1 and got is not None and got[0] == wanted_slope(typ, slope_of_given(head))
                and on(got, pts[0]))
    head, pts = split_line(p["prompt"])
    a, _, b = ans.partition(";")
    got = read_line(b.strip())
    return (" ".join(a.split()) == head and LEVEL_LINE.fullmatch(head) is not None and len(pts) == 2
            and got is not None and all(on(got, q) for q in pts))

def reduced_fractions(t):
    """Every written fraction a/b in lowest terms, b not 1 (simplest_form doesn't look at each term)."""
    return all(math.gcd(int(a), int(b)) == 1 and b != "1" for a, b in re.findall(r"(\d+)/(\d+)", t))

def squarefree_radicands(t):
    whole = re.findall(r"sqrt\((\d+)\)", t)
    return len(whole) == t.count("sqrt(") and all(square_free(int(n))[0] == 1 for n in whole)

NUM5 = r"-?\d+ [+-] (?:\d+ )?sqrt\(\d+\)"
FORM5 = re.compile(rf"{NUM5}|-?\({NUM5}\)/(?!1\b)\d+")
PART = r"\d+(?:/\d+)?"
FORM6 = re.compile(rf"-?{PART} [+-] (?:{PART} )?i|-?(?:{PART} )?i|-?{PART}")

def check_simplify(p):
    imaginary = p["type"] == "6"
    ans = " ".join(p["answer"].split())
    form = FORM6 if imaginary else FORM5
    if not form.fullmatch(ans) or not simplest_form(ans, imaginary) or not squarefree_radicands(ans):
        return False
    if not reduced_fractions(ans):
        return False
    d = to_sympy(p["prompt"], imaginary) - to_sympy(ans, imaginary)
    return sp.expand(sp.radsimp(d)) == 0

def check_square(p):
    v, a, b, c = quadratic(p["prompt"])
    ans = " ".join(p["answer"].split())
    if not reduced_fractions(ans):
        return False
    lhs, _, rhs = p["prompt"].partition("=")
    eq = to_sympy(lhs) - to_sympy(rhs)
    s = sp.Symbol(v)
    pm = re.fullmatch(rf"{v} = (.+) plus\.minus ?(.*?)(?: ?(i))?", ans)
    two = re.fullmatch(rf"{v} = (.+) or {v} = (.+)", ans)
    if two:
        texts = two.groups()
        if any("sqrt" in t or "i" in t or not simplest_form(t) for t in texts):
            return False
        roots = [to_sympy(t) for t in texts]
        if not all(r.is_Rational for r in roots):
            return False
    elif pm:
        h, rad, i = pm.groups()
        if "sqrt" in h or not h.strip() or not simplest_form(h) or (rad and not simplest_form(rad)):
            return False
        if not squarefree_radicands(rad) or "i" in rad.replace("sqrt", ""):
            return False
        H, R = to_sympy(h), (to_sympy(rad) if rad else sp.Integer(1))
        if not H.is_Rational or not R.is_positive or (not i and R.is_Rational):
            return False              # whole or fractional real values are written with "or"
        R = R * sp.I if i else R
        roots = [H + R, H - R]
    else:
        return False
    if roots[0] == roots[1]:
        return False
    return all(sp.expand(sp.radsimp(eq.subs(s, r))) == 0 for r in roots)

def check(p):
    try:
        if p["type"] in ("1", "2", "3", "4"):
            ok = check_line(p)
        elif p["type"] in ("5", "6"):
            ok = check_simplify(p)
        else:
            ok = check_square(p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# The graph of Type 4: lines (a) and (b) across the graph, arrowheads on
# their ends, each labeled in a white box clear of the other and of the axes
# ------------------------------------------------------------------
SHEET_WIDTH = 5.2                     # cm
SLIDE_WIDTH = 10.0                    # cm on a slide (Graph's slide_width)

def line_dist(pt, p, q):
    """How far pt is from the whole line through p and q."""
    (x, y), (x1, y1), (x2, y2) = pt, p, q
    dx, dy = x2 - x1, y2 - y1
    return abs(dy * (x - x1) - dx * (y - y1)) / math.hypot(dx, dy)

def labels(head, pts):
    """Where (a) and (b) go: ((xa, ya), (xb, yb)), or None if there's no clear place."""
    kind, k = head[0], int(head.split("=")[1])
    p, q = [(float(x), float(y)) for x, y in pts]
    def clear(pt):
        """How far the label is from everything else: the axes, the other line, the edge."""
        return min(abs(pt[0]), abs(pt[1]), GRID - 0.5 - abs(pt[0]), GRID - 0.5 - abs(pt[1]))
    best_a = None
    for t in (-4.5, -3.5, -2.5, 2.5, 3.5, 4.5):
        pt = (t, k) if kind == "y" else (k, t)
        score = min(line_dist(pt, p, q), abs(t) - 0.5)
        if best_a is None or score > best_a[0]:
            best_a = (score, pt)
    a_line = (lambda pt: abs(pt[1] - k)) if kind == "y" else (lambda pt: abs(pt[0] - k))
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    best_b = None
    for t in (0.1, 0.3, 0.5, 0.7, 0.9):
        for sgn in (1, -1):
            pt = (p[0] + t * dx - sgn * 0.9 * dy / n, p[1] + t * dy + sgn * 0.9 * dx / n)
            score = min(clear(pt), a_line(pt), math.dist(pt, best_a[1]) - 1)
            if best_b is None or score > best_b[0]:
                best_b = (score, pt)
    if best_a[0] < 0.9 or best_b[0] < 0.45:
        return None
    return best_a[1], best_b[1]

def figure(p, width=SHEET_WIDTH, size=6, slide_width=SLIDE_WIDTH):
    head, pts = split_line(p["prompt"])
    g = Graph(x=(-GRID, GRID), y=(-GRID, GRID), width=width, size=size, label=1, slide_width=slide_width)
    edge = GRID + 1.0
    g.cmds.append(f"rect({g.c(-edge, -edge)}, {g.c(edge, edge)}, stroke: none)")
    kind, k = head[0], int(head.split("=")[1])
    if kind == "y":
        g.line(0, k, color="black")
    else:
        g.vertical(k, color="black")
    g.through(*pts, color="black")                  # the whole line, arrowheads at the graph's edge
    spots = labels(head, pts)
    if spots:
        for name, (x, y) in zip("ab", spots):
            g.cmds.append(f"content({g.c(x, y)}, box(fill: white, inset: 1.5pt, "
                          f"text(size: {g._pt(8)})[({name})]))")
    return g.typst()

# ------------------------------------------------------------------
# Showing: each problem says what to do (EXTENDING.md 3.10)
# ------------------------------------------------------------------
THROUGH = "Find the equation of the line that passes through "
GRAPH_ASK = "Find the equations of lines (a) and (b)."
LEADIN = {"5": "Simplify:", "6": "Simplify:", "7": "Solve by completing the square:"}

def shown(t):
    """Display math in a box, so an equation never breaks across lines."""
    return f"#box[{display(dfrac(t))}]"

def sentence(p, math_=shown):
    typ = p["type"]
    if typ == "1":
        pts = POINT.findall(p["prompt"])
        if len(pts) == 2:
            a, b = (math_(f"({x}, {y})") for x, y in pts)
            return f"{THROUGH}{a} and {b}."
        return THROUGH + math_(p["prompt"]) + "."
    if typ in ("2", "3"):
        head, _, rest = p["prompt"].partition(";")
        how = "parallel" if typ == "2" else "perpendicular"
        return f"{THROUGH}{math_(rest.strip())} and is {how} to the line {math_(head.strip())}."
    if typ == "4":
        return GRAPH_ASK
    return None

def typst(p, gap="0.3em"):
    s = sentence(p)
    if p["type"] == "4":
        return f"{s} #v({gap}) #align(center)[{safe_figure(p)}]"
    if s is not None:
        return s
    return f"{LEADIN[p['type']]} #h(0.5em) " + shown(p["prompt"])

def safe_figure(p, **kw):
    try:
        return figure(p, **kw)
    except Exception:
        return "[graph]"              # an edited prompt that can't be drawn; check() marks it

def answer_typst(p):
    if p["type"] == "4":
        a, _, b = p["answer"].partition(";")
        return f"(a) {shown(a.strip())} #h(1em) (b) {shown(b.strip())}"
    return shown(p["answer"])

def slide_typst(p, key=False):
    """Type 4's slide: the question and its answer (hidden on the question slide) beside the
    larger graph, which is the same on both slides; None for the others."""
    parts = slide_parts(p, key)
    if parts is None:
        return None
    left, g = parts
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{left}], [{g}])"

def slide_parts(p, key=False):
    if p["type"] != "4":
        return None
    ans = f"#text(fill: red)[{answer_typst(p)}]"
    left = f"{GRAPH_ASK} #v(0.8em) " + (ans if key else f"#hide[{ans}]")
    return left, safe_figure(p)

def text(p):
    s = sentence(p, plain)
    if p["type"] == "4":
        head, pts = split_line(p["prompt"])
        two = " and ".join(f"({x}, {y})" for x, y in pts)
        return f"{s}   [graph: (a) the line {head}; (b) the line through {two}]"
    if s is not None:
        return s
    return f"{LEADIN[p['type']]} {plain(p['prompt'])}"

def answer_text(p):
    if p["type"] == "4":
        a, _, b = p["answer"].partition(";")
        return f"(a) {plain(a.strip())}   (b) {plain(b.strip())}"
    return plain(p["answer"]).replace("plus.minus", "±")

def height(p):
    if p["type"] == "4":
        return 2.2
    if p["type"] in ("5", "6"):
        return 0.55
    return 0.3

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
EXAMPLE = {
    "1": "(-3, 2), (4, -3)", "2": "y = 2 x - 1; (4, 1)", "3": "3 y + 4 x = 2; (-2, 5)",
    "4": "y = -2; (-6, -5), (-1, 6)", "5": "(4 + sqrt(3))/(2 - 3 sqrt(3))",
    "6": "(2 + i)/(3 - 2 i)", "7": "x^2 - 4 x - 12 = 0",
}

def clean(t):
    return " ".join(t.replace("−", "-").split())

def edit_text(p):
    return p["prompt"]

def answer_edit_text(p):
    return p["answer"]

def from_edit(t, old):
    t = clean(t)
    typ = old.get("type", "1")
    try:
        answer = answer_of(t, typ)
    except Exception:
        raise ValueError(f"write it like {EXAMPLE[typ]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
