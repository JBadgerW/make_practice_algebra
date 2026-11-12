"""Lesson 1 (Advanced Math): geometry review. From the Saxon lesson and its
deck (~/Documents/adv_math/problem_sets/ps_001/slides/deck_001.typ):
examples 1.1-1.5 and Problem Set 1, problems 20, 26, and 30.

    1  the area of a shaded sector:          shaded 40°, r = 3 sqrt(3) m             3 pi m^2
    2  the shaded rest of a circle:          unshaded 126°, r = 2 sqrt(5) m          13 pi m^2
    3  compare expressions under conditions: x > 0, y < 0;  A. x + y  B. x - y       B
    4  find the angles at crossing lines:    A°, (2B)°, (3C)°, 60°                   A = 120, B = 30, C = 40
    5  compare angles at crossing lines:     A. (k + l + m)°  B. (180 - n)°          A
    6  triangles between parallel lines:     A. Area of triangle WXY  B. Area of triangle ZXY   C

Types 1, 2, 4, 5, and 6 have a figure (lesson_figures), drawn from the
problem's own data. Type 2 is split from Type 1 for its extra move: the
shaded region is the circle less the labeled sector (360° - 126° = 234°).

Answer conventions. The deck answers 1.1 as 13 pi m^2, so a sector's area is
a multiple of pi with the unit squared after it: 13 pi "m"^2, and (chosen
here; the deck has none) a fraction as (9 pi)/2 "cm"^2. A comparison
(examples 1.2-1.5, problem 30) is answered by a letter, as the deck does: A
if quantity A is greater, B if quantity B is greater, C if they are equal, D
if the information given can't decide. Problem 20's answer, which the deck
doesn't give, is each letter's value in order (chosen here): A = 120, B = 30,
C = 40, the degrees left off as the figure's labels (A°) carry them.

check() works from the problem's data, not from how it was built:
  1, 2  the area (shaded angle)/360 * pi r^2, exactly, against the answer's
        value; the answer a rational multiple of pi in lowest terms, with the
        prompt's unit squared.
  3     the difference A - B at points sampled across the conditions (near
        each end of an interval, small and large values of an unbounded one):
        always positive A, always negative B, zero as an expression C, else D.
        (The build reads the difference's range off the conditions instead.)
  4     the answer's values put into the labels: opposite angles equal,
        adjacent ones adding to 180, every angle positive, every letter given.
  5     the angles written in one unknown t: the left and right angles are t,
        the top and bottom 180 - t; A - B sampled across 0 < t < 180.
  6     each triangle's area by the shoelace formula, from the coordinates
        the figure is drawn at.
Types 3, 5, and 6 also check that the answer is one letter, A to D.

No sources are skipped: Lesson 1 has no proofs.

A problem: dict(type, prompt, answer, source). The prompt is the problem's
data in a short form, and it is what an edit changes:
    1  "shaded 40, r = 3 sqrt(3) m"                 answer  '3 pi "m"^2'
    2  "unshaded 126, r = 2 sqrt(5) m"              answer  '13 pi "m"^2'
    3  "x > 0, y < 0; x + y; x - y"                 answer  "B"
       "1 < x < 6, 1 < y < 6; x - y; y - x"         answer  "D"
    4  "top A, left 2B, bottom 3C, right 60"        answer  "A = 120, B = 30, C = 40"
    5  "left k, top l, right m, bottom n; k + l + m; 180 - n"     answer  "A"
    6  "ZW || XY; WXY; ZXY"                         answer  "C"
       "ZW || XV, XY = 4, YV = 6; ZXY; WYV"         answer  "B"
"""
import math, re
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, simplest_form
from ..typmath import fr, text as plain
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_1"
FIXED = False
TITLE = "Lesson 1: Geometry Review"
INSTRUCTIONS = "Solve each problem."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

COMPARE = ("Compare the quantities. Answer A if quantity A is greater, B if quantity B is greater, "
           "C if they are equal, or D if not enough information is given.")
SECTOR = "Leave each area in terms of π."

TYPES = [
    dict(key="1", title="The Area of a Shaded Sector",
         look="A circle with one sector shaded; its central angle and the circle's radius are given.",
         move="The sector is its angle's share of the circle: (angle/360) pi r^2. Square the radius "
              "(a radical squares to a whole number: (3 sqrt(3))^2 = 27) and reduce.",
         instructions=SECTOR, space="1.5in"),
    dict(key="2", title="The Shaded Rest of a Circle",
         look="The labeled sector is the unshaded one; the shaded region is the rest of the circle.",
         move="The shaded region's central angle is 360° less the labeled one (360 - 126 = 234). Then "
              "(angle/360) pi r^2, as for a sector.",
         instructions=SECTOR, space="1.5in"),
    dict(key="3", title="Comparing Expressions Under Conditions",
         look="Two expressions in x and y, with the signs of x and y or the intervals they lie in.",
         move="Subtract B from A and simplify. If the difference is positive for every allowed x and y, "
              "the answer is A; negative, B; zero, C. If it can be either (try the cases x < y, x > y, "
              "x = y), the answer is D.",
         instructions=COMPARE, space="1.25in"),
    dict(key="4", title="Finding the Angles at Crossing Lines",
         look="Two crossing lines; one angle is a number, the others are letters times a number.",
         move="Vertical (opposite) angles are equal, and angles side by side on a line add to 180°. "
              "Find each angle, then divide by the letter's number: 3C = 120, so C = 40.",
         instructions="Find the unknowns.", space="1.25in"),
    dict(key="5", title="Comparing Angles at Crossing Lines",
         look="Two crossing lines with angles named by letters, and two sums of them to compare.",
         move="Angles side by side on a line add to 180 (a straight angle); vertical angles are equal; "
              "all four add to 360. Rewrite A and B with these, then compare. Nothing tells a single "
              "angle's size.",
         instructions=COMPARE, space="1.25in"),
    dict(key="6", title="Triangles Between Parallel Lines",
         look="Triangles with their bases on one line and their tops on a parallel line.",
         move="A triangle's area is (1/2) base times altitude. Between parallel lines every altitude is "
              "the same, so the triangles compare as their bases do; on the same base they are equal.",
         instructions=COMPARE, space="1.25in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Types 1 and 2: a sector's area. r = a sqrt(b) (b = 1: a whole number)
# ------------------------------------------------------------------
UNITS = ("m", "cm", "ft", "in")
RADICANDS = (1, 2, 3, 5, 6, 7)
COEF = range(1, 13)                      # a whole radius 2..12; a radical's coefficient 1..6
SHADED = range(10, 301)                  # Type 1: the shaded sector's angle
UNSHADED = range(30, 331)                # Type 2: the labeled, unshaded sector's angle
DENOMS = (1, 2, 3, 4)                    # the coefficient of pi: whole (mostly) or over 2, 3, 4

def radius_ok(a, b):
    return a >= 2 if b == 1 else a <= 6

def radius(a, b):
    return str(a) if b == 1 else f"sqrt({b})" if a == 1 else f"{a} sqrt({b})"

def area_coef(shaded, a, b):
    """The area over pi: (shaded/360) r^2."""
    return F(shaded * a * a * b, 360)

def t1_build(angle, a, b, unit):
    return f"shaded {angle}, r = {radius(a, b)} {unit}"

def t2_build(angle, a, b, unit):
    return f"unshaded {angle}, r = {radius(a, b)} {unit}"

def sector_pick(angles, shaded_of, whole):
    def pick(r):
        b = r.choice(RADICANDS + (2, 3, 5))          # radicals twice as often as whole radii
        a = r.choice([n for n in COEF if radius_ok(n, b)])
        ok = [t for t in angles
              if (q := area_coef(shaded_of(t), a, b)).denominator in ((1,) if whole else DENOMS[1:])]
        need(ok)
        return dict(angle=r.choice(ok), a=a, b=b, unit=r.choice(UNITS))
    return pick

t1_whole = sector_pick(SHADED, lambda t: t, True)
t1_part = sector_pick(SHADED, lambda t: t, False)
t2_whole = sector_pick(UNSHADED, lambda t: 360 - t, True)
t2_part = sector_pick(UNSHADED, lambda t: 360 - t, False)

SECTOR_RE = re.compile(r"^(shaded|unshaded) (\d+), r = (.+) (m|cm|ft|in)$")

def read_sector(prompt):
    """(shaded?, the labeled angle, the radius as Typst math, unit)."""
    m = SECTOR_RE.match(prompt)
    if not m:
        raise ValueError("write it like: shaded 40, r = 3 sqrt(3) m")
    angle = int(m.group(2))
    if not 0 < angle < 360:
        raise ValueError("the angle is between 0 and 360")
    to_sympy(m.group(3))
    return m.group(1) == "shaded", angle, m.group(3), m.group(4)

def sector_answer(prompt):
    shaded, angle, r, unit = read_sector(prompt)
    q = sp.nsimplify(to_sympy(r) ** 2) * sp.Rational(angle if shaded else 360 - angle, 360)
    n, d = sp.fraction(sp.Rational(q))
    need(n > 0)
    top = "pi" if n == 1 else f"{n} pi"
    return f'{top if d == 1 else fr(top, str(d))} "{unit}"^2'

ANSWER_UNIT = re.compile(r'^(.*\S)\s+"(m|cm|ft|in)"\^2$')

def check_sector(p):
    shaded, angle, r, unit = read_sector(p["prompt"])
    m = ANSWER_UNIT.match(p["answer"])
    if not m or m.group(2) != unit:
        return False
    value = m.group(1)
    want = sp.Rational(angle if shaded else 360 - angle, 360) * sp.pi * to_sympy(r) ** 2
    got = to_sympy(value)
    if sp.simplify(got - want) != 0:
        return False
    # The form: a rational multiple of pi, written with pi once, in lowest terms.
    return (value.count("pi") == 1 and not re.search(r"sqrt|degree|\.|\^", value)
            and (got / sp.pi).is_Rational and simplest_form(value))

# ------------------------------------------------------------------
# Type 3: compare two expressions in x and y under conditions
# ------------------------------------------------------------------
# Each form with its coefficients (of x, of y, the constant): the build works the range out from these.
FORMS = {"x + y": (1, 1, 0), "x - y": (1, -1, 0), "y - x": (-1, 1, 0), "y + x": (1, 1, 0),
         "x": (1, 0, 0), "y": (0, 1, 0), "2 x": (2, 0, 0), "2 y": (0, 2, 0), "-x": (-1, 0, 0),
         "-y": (0, -1, 0), "-x - y": (-1, -1, 0), "0": (0, 0, 0)}
CONSTANTS = {str(n): (0, 0, n) for n in range(1, 13)}
SIGNS = (">", "<")
BOUNDS = range(-5, 13)                  # an interval's ends
WIDE = 8                                # an interval at most this wide

def coefs(form):
    return FORMS.get(form) or CONSTANTS[form]

def t3_sign_build(sx, sy, A, B):
    return f"x {sx} 0, y {sy} 0; {A}; {B}"

def t3_box_build(x0, x1, y0, y1, A, B):
    return f"{x0} < x < {x1}, {y0} < y < {y1}; {A}; {B}"

def pair(r, constants=False):
    A = r.choice(list(FORMS))
    B = r.choice(list(FORMS) + (list(CONSTANTS) if constants and r.random() < 0.3 else []))
    need(A != B and coefs(A) != coefs(B))            # not the same expression twice
    return A, B

def t3_sign(r):
    A, B = pair(r)
    return dict(sx=r.choice(SIGNS), sy=r.choice(SIGNS), A=A, B=B)

def t3_box(r):
    x0, y0 = r.choice(BOUNDS), r.choice(BOUNDS)
    x1, y1 = x0 + r.randint(1, WIDE), y0 + r.randint(1, WIDE)
    if r.random() < 0.4:                              # the same interval for both, as in example 1.3
        y0, y1 = x0, x1
    need(x1 in BOUNDS and y1 in BOUNDS)
    A, B = pair(r, constants=True)
    return dict(x0=x0, x1=x1, y0=y0, y1=y1, A=A, B=B)

def sign_letter(lo, hi):
    """The answer from the range (lo, hi) of A - B: lo == hi is a constant difference."""
    if lo == hi:
        return "A" if lo > 0 else "B" if lo < 0 else "C"
    return "A" if lo >= 0 else "B" if hi <= 0 else "D"

def linear_range(c, lo, hi):
    """The range of c v for lo < v < hi (ends may be infinite)."""
    if c == 0:
        return 0, 0
    a, b = c * lo, c * hi
    return min(a, b), max(a, b)

COND = re.compile(r"^\s*(?:(-?\d+)\s*<\s*)?([xy])\s*([<>])\s*(-?\d+)\s*$")

def read_conditions(text):
    """{var: (lo, hi)} from "x > 0, y < 0" or "1 < x < 6, 1 < y < 6"."""
    out = {}
    for part in text.split(","):
        m = COND.match(part)
        if not m:
            raise ValueError("write the conditions like x > 0, y < 0 or 1 < x < 6, 1 < y < 6")
        lo, v, op, n = m.groups()
        n = int(n)
        if lo is not None:
            if op != "<" or int(lo) >= n:
                raise ValueError("an interval is written lo < x < hi")
            out[v] = (int(lo), n)
        else:
            out[v] = (n, math.inf) if op == ">" else (-math.inf, n)
    if set(out) != {"x", "y"}:
        raise ValueError("give a condition on x and one on y")
    return out

def read_compare3(prompt):
    parts = [s.strip() for s in prompt.split(";")]
    if len(parts) != 3:
        raise ValueError("write it like: x > 0, y < 0; x + y; x - y")
    conds = read_conditions(parts[0])
    for e in parts[1:]:
        if not to_sympy(e).free_symbols <= {sp.Symbol("x"), sp.Symbol("y")}:
            raise ValueError("the expressions are in x and y")
    return conds, parts[1], parts[2]

def compare3_answer(prompt):
    conds, A, B = read_compare3(prompt)
    if A in FORMS | CONSTANTS and B in FORMS | CONSTANTS:      # the build's own forms: integers only
        (ax, ay, a0), (bx, by, b0) = coefs(A), coefs(B)
        cx, cy, c0 = ax - bx, ay - by, a0 - b0
    else:                                                     # an edit: the coefficients from sympy
        x, y = sp.symbols("x y")
        d = sp.Poly(sp.expand(to_sympy(A) - to_sympy(B)), x, y)
        if d.total_degree() > 1:
            raise ValueError("the expressions are linear in x and y, like 2 x - y")
        cx, cy, c0 = (int(d.coeff_monomial(m)) for m in (x, y, 1))
    xl, xh = linear_range(cx, *conds["x"])
    yl, yh = linear_range(cy, *conds["y"])
    return sign_letter(xl + yl + c0, xh + yh + c0)

def samples(lo, hi):
    """Values inside lo < v < hi: near each end, and between."""
    lo, hi = sp.Rational(lo) if lo != -math.inf else None, sp.Rational(hi) if hi != math.inf else None
    eps = sp.Rational(1, 10**6)
    if lo is not None and hi is not None:
        return [lo + (hi - lo) * t for t in (eps, sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), 1 - eps)]
    if lo is not None:
        return [lo + t for t in (eps, 1, 10**3, 10**6)]
    return [hi - t for t in (eps, 1, 10**3, 10**6)]

def letter_of_signs(diff, points):
    """A, B, C, or D from the values of diff at the points."""
    if sp.expand(diff) == 0:
        return "C"
    vals = [diff.subs(pt) for pt in points]
    return "A" if all(v > 0 for v in vals) else "B" if all(v < 0 for v in vals) else "D"

def check_compare3(p):
    conds, A, B = read_compare3(p["prompt"])
    x, y = sp.symbols("x y")
    pts = [{x: a, y: b} for a in samples(*conds["x"]) for b in samples(*conds["y"])]
    return p["answer"] == letter_of_signs(to_sympy(A) - to_sympy(B), pts)

# ------------------------------------------------------------------
# Type 4: crossing lines, find A, B, C
# ------------------------------------------------------------------
POS = ("top", "left", "bottom", "right")          # the letters go A, B, C in this order
OPPOSITE = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
KNOWN = range(20, 161, 5)                          # the angle given as a number
MULT = range(1, 6)                                 # a letter's number: 3C

def t4_build(where, k, ca, cb, cc):
    cs, out = iter((ca, cb, cc)), []
    letters = iter("ABC")
    for pos in POS:
        if pos == where:
            out.append(f"{pos} {k}")
        else:
            c, L = next(cs), next(letters)
            out.append(f"{pos} {'' if c == 1 else c}{L}")
    return ", ".join(out)

def angle_at(where, k, pos):
    return k if pos in (where, OPPOSITE[where]) else 180 - k

def fits(angle, c):
    """c times a letter makes the angle, the letter a multiple of 5 (as the book's are: B = 30, C = 40)."""
    return angle % (5 * c) == 0

def t4_pick(r):
    where, k = r.choice(POS), r.choice(KNOWN)
    need(k != 90)
    others = [p for p in POS if p != where]
    cs = [r.choice([c for c in MULT if fits(angle_at(where, k, p), c)]) for p in others]
    need(max(cs) > 1)
    return dict(where=where, k=k, ca=cs[0], cb=cs[1], cc=cs[2])

LABEL = re.compile(r"^(top|left|bottom|right) (?:(\d+)|(\d*)([A-Z]))$")

def read_angles(prompt):
    """{pos: (coefficient, letter or None)}: "right 60" -> (60, None), "left 2B" -> (2, "B")."""
    out = {}
    for part in prompt.split(","):
        m = LABEL.match(part.strip())
        if not m:
            raise ValueError("write it like: top A, left 2B, bottom 3C, right 60")
        pos, num, c, L = m.groups()
        out[pos] = (int(num), None) if num else (int(c or 1), L)
    if set(out) != set(POS) or sum(L is None for _, L in out.values()) < 1:
        raise ValueError("label all four angles, at least one with a number")
    letters = [L for _, L in out.values() if L]
    if len(set(letters)) != len(letters):
        raise ValueError("use each letter once")
    return out

def angles_answer(prompt):
    labels = read_angles(prompt)
    known = {pos: c for pos, (c, L) in labels.items() if L is None}
    pos, k = next(iter(known.items()))
    vals = {}
    for p, (c, L) in labels.items():
        if L:
            v = F(angle_at(pos, k, p), c)
            need(v.denominator == 1)
            vals[L] = int(v)
    return ", ".join(f"{L} = {vals[L]}" for L in sorted(vals))

def read_values(answer):
    out = {}
    for part in answer.split(","):
        m = re.match(r"^\s*([A-Z])\s*=\s*(\d+)\s*$", part)
        if not m:
            raise ValueError("write the answer like A = 120, B = 30, C = 40")
        out[m.group(1)] = int(m.group(2))
    return out

def check_angles(p):
    labels = read_angles(p["prompt"])
    vals = read_values(p["answer"])
    if set(vals) != {L for _, L in labels.values() if L}:
        return False
    deg = {pos: c * (vals[L] if L else 1) for pos, (c, L) in labels.items()}
    return (all(d > 0 for d in deg.values()) and deg["top"] == deg["bottom"] and deg["left"] == deg["right"]
            and deg["top"] + deg["left"] == 180)

# ------------------------------------------------------------------
# Type 5: crossing lines, compare sums of the angles
# ------------------------------------------------------------------
CLOCK = ("left", "top", "right", "bottom")        # the letters go around clockwise
NAMES = ("klmn", "abcd", "pqrs", "wxyz")
EXPRS = ("{0}", "{1}", "{2}", "{3}",
         "{0} + {1}", "{1} + {2}", "{2} + {3}", "{0} + {3}", "{0} + {2}", "{1} + {3}",
         "{0} + {1} + {2}", "{1} + {2} + {3}", "{0} + {2} + {3}", "{0} + {1} + {3}",
         "180 - {0}", "180 - {1}", "180 - {2}", "180 - {3}", "360 - {0}", "360 - {3}",
         "90", "180", "360")
DRAWN = 75                                         # the left and right angles as drawn

def t5_build(names, start, A, B):
    where = ", ".join(f"{CLOCK[(start + i) % 4]} {names[i]}" for i in range(4))
    order = sorted(where.split(", "), key=lambda s: CLOCK.index(s.split()[0]))
    return f"{', '.join(order)}; {A.format(*names)}; {B.format(*names)}"

def t5_pick(r):
    A, B = r.sample(EXPRS, 2)
    need(not (A.isdigit() and B.isdigit()))
    return dict(names=r.choice(NAMES), start=r.randrange(4), A=A, B=B)

def read_compare5(prompt):
    parts = [s.strip() for s in prompt.split(";")]
    if len(parts) != 3:
        raise ValueError("write it like: left k, top l, right m, bottom n; k + l + m; 180 - n")
    at = {}
    for s in parts[0].split(","):
        m = re.match(r"^(left|top|right|bottom) ([a-z])$", s.strip())
        if not m:
            raise ValueError("name the angles like: left k, top l, right m, bottom n")
        at[m.group(1)] = m.group(2)
    if set(at) != set(CLOCK) or len(set(at.values())) != 4:
        raise ValueError("name all four angles, each with its own letter")
    for e in parts[1:]:
        if not {str(s) for s in to_sympy(e).free_symbols} <= set(at.values()):
            raise ValueError("compare sums of the named angles")
    return at, parts[1], parts[2]

def in_t(at):
    """Each letter as c + s t: the left and right angles are t, the top and bottom 180 - t."""
    return {L: (0, 1) if pos in ("left", "right") else (180, -1) for pos, L in at.items()}

def compare5_answer(prompt):
    at, A, B = read_compare5(prompt)
    lin = in_t(at)
    x = sp.expand(to_sympy(A) - to_sympy(B))
    c0 = int(x.subs({sp.Symbol(L): 0 for L in lin}))
    c, s = c0, 0
    for L, (a, b) in lin.items():
        k = int(x.coeff(sp.Symbol(L)))
        c, s = c + k * a, s + k * b
    return sign_letter(*sorted((c, c + 180 * s))) if s else sign_letter(c, c)

def check_compare5(p):
    at, A, B = read_compare5(p["prompt"])
    t = sp.Symbol("t")
    diff = (to_sympy(A) - to_sympy(B)).subs({sp.Symbol(L): (t if pos in ("left", "right") else 180 - t)
                                            for pos, L in at.items()})
    eps = sp.Rational(1, 10**6)
    return p["answer"] == letter_of_signs(diff, [{t: v} for v in (eps, 30, 90, 150, 180 - eps)])

# ------------------------------------------------------------------
# Type 6: triangles between parallel lines
# ------------------------------------------------------------------
POINT_NAMES = "ABCDEFGHJKLMNPQRSTUVWXYZ"
LENGTHS = range(2, 10)

def t6_shared_build(names, first):
    """names: top left, top right, bottom left, bottom right; quantity A's top point is names[first]."""
    tl, tr, b0, b1 = names
    a, b = (tl, tr) if first == 0 else (tr, tl)
    return f"{tl}{tr} || {b0}{b1}; {a}{b0}{b1}; {b}{b0}{b1}"

def t6_bases_build(names, p, q, swap):
    """names: top left, top right, bottom three left to right; triangles tl b0 b1 and tr b1 b2."""
    tl, tr, b0, b1, b2 = names
    one, two = f"{tl}{b0}{b1}", f"{tr}{b1}{b2}"
    a, b = (two, one) if swap else (one, two)
    return f"{tl}{tr} || {b0}{b2}, {b0}{b1} = {p}, {b1}{b2} = {q}; {a}; {b}"

def t6_shared(r):
    return dict(names="".join(r.sample(POINT_NAMES, 4)), first=r.randrange(2))

def t6_bases(r):
    return dict(names="".join(r.sample(POINT_NAMES, 5)), p=r.choice(LENGTHS), q=r.choice(LENGTHS),
                swap=r.randrange(2))

PARALLEL = re.compile(r"^([A-Z])([A-Z]) \|\| ([A-Z])([A-Z])(?:, ([A-Z])([A-Z]) = (\d+), ([A-Z])([A-Z]) = (\d+))?"
                      r"; ([A-Z]{3}); ([A-Z]{3})$")

def read_parallel(prompt):
    """(top {name: x}, bottom {name: x}, the lengths labeled {(a, b): n}, triangle A, triangle B)."""
    m = PARALLEL.match(prompt)
    if not m:
        raise ValueError("write it like: ZW || XY; WXY; ZXY")
    tl, tr, b0, b2, s0, s1, p, s2, s3, q, A, B = m.groups()
    top = {tl: 0.0, tr: 6.0}
    if p is None:
        bottom, below = {b0: 2.6, b2: 5.4}, {}
    else:
        b1 = s1
        if (s0, s3) != (b0, b2) or s2 != b1:
            raise ValueError("label the two pieces of the bottom segment, left to right")
        p, q = int(p), int(q)
        if not (p and q):
            raise ValueError("the lengths are whole numbers")
        k = 5.0 / (p + q)
        bottom, below = {b0: 0.6, b1: 0.6 + k * p, b2: 0.6 + k * (p + q)}, {(b0, b1): p, (b1, b2): q}
    names = list(top) + list(bottom)
    if len(set(names)) != len(names):
        raise ValueError("give each point its own letter")
    for t in (A, B):
        if not (sum(c in top for c in t) == 1 and sum(c in bottom for c in t) == 2 and len(set(t)) == 3):
            raise ValueError("each triangle has one top point and two bottom points")
    return top, bottom, below, A, B

HEIGHT = 2.0

def parallel_sides(top, bottom, A, B):
    """The segments the figure draws: each triangle's two sides to its top point."""
    out = []
    for t in (A, B):
        apex = next(c for c in t if c in top)
        out += [(apex, c) for c in t if c in bottom]
    return out

def parallel_answer(prompt):
    top, bottom, below, A, B = read_parallel(prompt)
    if not below:
        return "C" if sorted(A[1:]) == sorted(B[1:]) else "D"
    base = {frozenset(k): n for k, n in below.items()}
    a, b = base[frozenset(A[1:])], base[frozenset(B[1:])]
    return "A" if a > b else "B" if a < b else "C"

def shoelace(pts):
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))) / 2

def check_parallel(p):
    top, bottom, below, A, B = read_parallel(p["prompt"])
    # Exact coordinates: the bottom points spaced by the labeled lengths.
    at = {n: (F(0) if x == 0 else F(6), F(2)) for n, x in top.items()}
    if below:
        names = list(bottom)
        lens = list(below.values())
        xs = [F(0), F(lens[0]), F(lens[0] + lens[1])]
        at |= {n: (x, F(0)) for n, x in zip(names, xs)}
    else:
        at |= {n: (F(x).limit_denominator(), F(0)) for n, x in bottom.items()}
    a, b = shoelace([at[c] for c in A]), shoelace([at[c] for c in B])
    return p["answer"] == ("A" if a > b else "B" if a < b else "C")

# ------------------------------------------------------------------
# Templates and ranges
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_whole, t1_build), (t1_whole, t1_build), (t1_part, t1_build)],
    "2": [(t2_whole, t2_build), (t2_whole, t2_build), (t2_part, t2_build)],
    "3": [(t3_sign, t3_sign_build), (t3_box, t3_box_build)],
    "4": [(t4_pick, t4_build)],
    "5": [(t5_pick, t5_build)],
    "6": [(t6_shared, t6_shared_build), (t6_shared, t6_shared_build), (t6_bases, t6_bases_build)],
}

def _sector_range(angles, shaded_of):
    return lambda angle, a, b, unit: (angle in angles and b in RADICANDS and a in COEF and radius_ok(a, b)
                                      and unit in UNITS
                                      and area_coef(shaded_of(angle), a, b).denominator in DENOMS)

RANGES = {
    t1_build: _sector_range(SHADED, lambda t: t),
    t2_build: _sector_range(UNSHADED, lambda t: 360 - t),
    t3_sign_build: lambda sx, sy, A, B: sx in SIGNS and sy in SIGNS and A in FORMS and B in FORMS
                                         and coefs(A) != coefs(B),
    t3_box_build: lambda x0, x1, y0, y1, A, B: (all(v in BOUNDS for v in (x0, x1, y0, y1))
                                                and 0 < x1 - x0 <= WIDE and 0 < y1 - y0 <= WIDE
                                                and A in FORMS and B in FORMS | CONSTANTS and coefs(A) != coefs(B)),
    t4_build: lambda where, k, ca, cb, cc: (where in POS and k in KNOWN and k != 90 and max(ca, cb, cc) > 1
                                            and all(c in MULT and fits(angle_at(where, k, p), c)
                                                    for c, p in zip((ca, cb, cc), [p for p in POS if p != where]))),
    t5_build: lambda names, start, A, B: names in NAMES and start in range(4) and A in EXPRS and B in EXPRS
                                         and A != B and not (A.isdigit() and B.isdigit()),
    t6_shared_build: lambda names, first: (len(names) == 4 == len(set(names)) and set(names) <= set(POINT_NAMES)
                                           and first in (0, 1)),
    t6_bases_build: lambda names, p, q, swap: (len(names) == 5 == len(set(names)) and set(names) <= set(POINT_NAMES)
                                               and p in LENGTHS and q in LENGTHS and swap in (0, 1)),
}

def in_range(build, params):
    """Can a random draw pick these parameters for this build?"""
    return RANGES[build](**params)

# ------------------------------------------------------------------
# Solving and checking
# ------------------------------------------------------------------
def kind(prompt):
    """Which reader a prompt takes: sector, compare3, angles, compare5, parallel."""
    if SECTOR_RE.match(prompt):
        return "sector"
    if "||" in prompt:
        return "parallel"
    if re.match(r"^(top|left|bottom|right) ", prompt):
        return "compare5" if ";" in prompt else "angles"
    return "compare3"

SOLVE = {"sector": sector_answer, "compare3": compare3_answer, "angles": angles_answer,
         "compare5": compare5_answer, "parallel": parallel_answer}
CHECK = {"sector": check_sector, "compare3": check_compare3, "angles": check_angles,
         "compare5": check_compare5, "parallel": check_parallel}
KIND = {"1": "sector", "2": "sector", "3": "compare3", "4": "angles", "5": "compare5", "6": "parallel"}

def answer_of(prompt):
    return SOLVE[kind(prompt)](prompt)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        k = kind(p["prompt"])
        if k != KIND[p["type"]] or (k == "sector" and p["prompt"].startswith("un") != (p["type"] == "2")):
            return "failed"
        if k in ("compare3", "compare5", "parallel") and p["answer"] not in ("A", "B", "C", "D"):
            return "failed"
        ok = CHECK[k](p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def deg(e):
    """An angle expression with its degree sign: k°, (k + l + m)°, 60°."""
    e = e.strip()
    return f"{e}°" if re.fullmatch(r"\w+", e) else f"({e})°"

def letter_label(c, L):
    return f"${c}°$" if L is None else f"${L}°$" if c == 1 else f"$({c} {L})°$"

def listing(names):
    """$A$, $B$, and $C$ (two: $A$ and $B$)."""
    ms = [f"${n}$" for n in names]
    return ms[0] if len(ms) == 1 else " and ".join(ms) if len(ms) == 2 else ", ".join(ms[:-1]) + ", and " + ms[-1]

def choices(a, b):
    """A. a   B. b, each kept on one line."""
    return f"#box[A. #h(0.3em) {a}] #h(1.5em) #box[B. #h(0.3em) {b}]"

def statement(p):
    """The problem's words (Typst markup), without its figure."""
    k = kind(p["prompt"])
    if k == "sector":
        shaded, angle, r, unit = read_sector(p["prompt"])
        u = {"m": "m.", "cm": "cm.", "ft": "ft.", "in": "in."}[unit]       # the unit ends the sentence
        if shaded:
            return (f"The central angle of the shaded sector measures ${angle}°$. The radius of the "
                    f"circle is ${r}$ {u} Find the area of the shaded sector.")
        return (f"The measure of the central angle of the unshaded sector is ${angle}°$. The radius of the "
                f"circle is ${r}$ {u} Find the area of the shaded region of the circle.")
    if k == "compare3":
        conds, A, B = [s.strip() for s in p["prompt"].split(";")]
        cx, cy = [c.strip() for c in conds.split(",")]
        return (f"Let $x$ and $y$ be real numbers. If ${cx}$ and ${cy}$, compare: \\\n"
                f"{choices(f'${A}$', f'${B}$')}")
    if k == "angles":
        return f"Find {listing(sorted(L for _, L in read_angles(p['prompt']).values() if L))}."
    if k == "compare5":
        at, A, B = read_compare5(p["prompt"])
        return (f"Given two intersecting lines with angles {listing(sorted(at.values()))}, as shown, "
                f"compare: \\\n{choices(f'${deg(A)}$', f'${deg(B)}$')}")
    top, bottom, below, A, B = read_parallel(p["prompt"])
    t, b = list(top), list(bottom)
    seg = lambda u, v: f"$overline({u} {v})$"
    given = f"Given {seg(*t)} and {seg(b[0], b[-1])} are parallel"
    if below:
        (s0, n0), (s1, n1) = below.items()
        given += f", ${s0[0]} {s0[1]} = {n0}$, and ${s1[0]} {s1[1]} = {n1}$, as shown, compare:"
    else:
        given += ", as shown. Compare:"
    tri = lambda T: f"Area of $triangle {' '.join(T)}$"
    return f"{given} \\\n{choices(tri(A), tri(B))}"

def figure(p, unit="1cm"):
    """The figure, drawn from the prompt's data; "" for Type 3."""
    k = kind(p["prompt"])
    if k == "sector":
        shaded, angle, r, unit_ = read_sector(p["prompt"])
        return fig.sector(angle, shaded, f"${angle}°$", unit)
    if k == "angles":
        labels = read_angles(p["prompt"])
        pos, (c, _) = next((q, v) for q, v in labels.items() if v[1] is None)
        drawn = c if pos in ("left", "right") else 180 - c
        return fig.crossing(drawn, {q: letter_label(*v) for q, v in labels.items()}, unit)
    if k == "compare5":
        at, _, _ = read_compare5(p["prompt"])
        return fig.crossing(DRAWN, {q: f"${L}°$" for q, L in at.items()}, unit)
    if k == "parallel":
        top, bottom, below, A, B = read_parallel(p["prompt"])
        return fig.parallel(top, bottom, parallel_sides(top, bottom, A, B),
                            {k_: f"${n}$" for k_, n in below.items()}, HEIGHT, unit)
    return ""

def typst(p, gap="0.3em"):
    try:
        s, f = statement(p), figure(p)
    except ValueError:
        return f"${p['prompt']}$"
    return s if not f else f"{s} #v(0.4em) #align(center)[{f}]"

def answer_typst(p):
    if p["type"] in ("1", "2"):
        spaced = p["answer"].replace(' "', ' thin "')                  # 13 pi m^2, the unit set apart
        return f"$display({spaced})$"
    return f"${p['answer']}$" if p["type"] == "4" else f"*{p['answer']}*"

SLIDE_UNIT = {"sector": "2.4cm", "angles": "2.2cm", "compare5": "2.2cm", "parallel": "1.9cm"}

def slide_typst(p, key=False):
    """A figure's slide: the words (and the answer, hidden on the question
    slide) beside the figure drawn larger; the figure never moves. None for Type 3."""
    try:
        f = figure(p, SLIDE_UNIT.get(kind(p["prompt"]), "1cm"))
        s = statement(p)
    except ValueError:
        return None
    if not f:
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{s} #v(0.8em) {shown}], [{f}])"

def text(p):
    try:
        s = statement(p)
    except ValueError:
        return plain(p["prompt"])
    s = re.sub(r"#h\([^)]*\)\s*|#box\[|\]", "", s).replace(" \\\n", "   ").replace("$", "")
    s = re.sub(r"overline\((\w) (\w)\)", r"\1\2", s).replace("triangle ", "△")
    return plain(s.replace("sqrt", "√")) + ("" if p["type"] == "3" else "   [figure]")

def answer_text(p):
    return plain(p["answer"].replace('"', "").replace(" pi", "π").replace("pi", "π"))

def height(p):
    return 0.55 if p["type"] == "3" else 2.3

# ------------------------------------------------------------------
# Editing: the prompt is the problem's data, in its short form
# ------------------------------------------------------------------
EXAMPLE = {"1": "shaded 40, r = 3 sqrt(3) m", "2": "unshaded 126, r = 2 sqrt(5) m",
           "3": "x > 0, y < 0; x + y; x - y", "4": "top A, left 2B, bottom 3C, right 60",
           "5": "left k, top l, right m, bottom n; k + l + m; 180 - n", "6": "ZW || XY; WXY; ZXY"}

def clean(t):
    return " ".join(t.replace("−", "-").replace("°", "").split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    try:
        if kind(t) != KIND[old["type"]] or (kind(t) == "sector" and t.startswith("un") != (old["type"] == "2")):
            raise ValueError
        answer = answer_of(t)
    except (ValueError, gen.Redraw, SyntaxError, TypeError, KeyError):
        raise ValueError(f"write it like: {EXAMPLE[old['type']]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    t = clean(t)
    if p["type"] in ("3", "5", "6"):
        t = t.upper()
    new = dict(p, answer=t)
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
