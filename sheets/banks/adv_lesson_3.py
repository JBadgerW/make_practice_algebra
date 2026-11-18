"""Lesson 3 (Advanced Math): the Pythagorean theorem, similar triangles. From
the Saxon lesson and its deck (~/Documents/adv_math/problem_sets/ps_003/slides/deck_003.typ):
examples 3.1-3.5 and Problem Set 3, problems 5-10.

    1  right, acute, or obtuse from the sides:   7, 5, 4                         obtuse
    2  similar triangles and scale factors:      5, 4, x ~ 7, y, 6 (a bowtie)    x = 30/7, y = 28/5
    3  similar right triangles at vertical angles: hyp 7 | hyp 10, legs z, 8     x = 21/5, y = 28/5, z = 6
    4  a right triangle inside a right triangle: base 6 + 4, inner leg 4         A = 2 sqrt(13), B = (4 sqrt(13))/3, C = 20/3
    5  the altitude to the hypotenuse:           hypotenuse cut into 4 and 8     a = 4 sqrt(3), b = 4 sqrt(6), h = 4 sqrt(2)

Types 2-5 have a figure (lesson_figures), drawn to scale from the problem's own
data: every unknown is worked out first, so the triangles drawn are the real
ones (two similar triangles' sizes are kept within a factor of about 2 of each
other, so a small one stays readable; their shapes are exact). Type 2's
triangles stand apart, each turned its own way (problems 6 and 7), or meet at
a vertex with their vertical angles marked (example 3.2); the arcs on the
angles say which sides correspond. Type 3 is split from Type 2 for its extra
move, the Pythagorean theorem in the triangle with two sides given.

Answer conventions. Each unknown as letter = value, in alphabetical order,
the way the deck answers example 3.2 (y = 28/5, x = 30/7, here x first). A
value is exact: a whole number, a fraction in lowest terms (28/5, 7/2, 84/5,
as the deck writes them), or a simplified radical with a whole or fractional
coefficient, written as one fraction: 2 sqrt(13), (4 sqrt(13))/3, sqrt(70),
3 sqrt(14). The deck writes example 3.3's 5.6 and 4.2 as decimals (the book
does); the key writes 28/5 and 21/5, as it does for problem 8 (chosen here, so
every key has one form). Problem 6 also asks for the scale factors: the key
puts them first, "right to left" = 2, "left to right" = 1/2, then x and y.
Type 1 answers right, acute, or obtuse; the key shows the comparison of
squares the deck shows: obtuse, 7^2 > 5^2 + 4^2.

check() works from the problem's data, not from how it was built:
  1     the largest angle's cosine by the law of cosines (negative obtuse, zero
        right, positive acute), the sides first checked to make a triangle.
  2, 3  the answer's values put into the two triangles: every pair of
        corresponding sides in the same ratio, the triangle inequality, and
        (Type 3) a^2 + b^2 = c^2 in both; the scale factors the sides' ratios.
  4     the values put into the two right triangles: the Pythagorean theorem
        in each and the ratio of their legs.
  5     the values put into the three right triangles: a^2 = h^2 + m^2,
        b^2 = h^2 + n^2, and a^2 + b^2 = (m + n)^2.
Every value in Types 2-5 is also checked for its form: a number, positive,
in lowest terms, no radical below, every radicand square-free.

No sources are skipped: Lesson 3 has no proofs.

A problem: dict(type, prompt, answer, source). The prompt is the problem's
data in a short form, and it is what an edit changes. A triangle's sides are
listed opposite its vertices in the order: unmarked angle, one arc, two arcs
(Type 2), or hypotenuse, far leg, leg at the crossing (Type 3); the second
triangle's sides correspond in the same order. The numbers after "apart" are
the two triangles' poses (0-11), after "bowtie" which way it's flipped.
    1  "7, 5, 4"   "7 cm, 12 cm, 6 cm"                      answer  "obtuse"
    2  "bowtie 0; 5, 4, x; 7, y, 6"                         answer  "x = 30/7, y = 28/5"
       "apart 9 2, factors; 6, 7, x; 3, y, 4"               answer  '"right to left" = 2, "left to right" = 1/2, x = 8, y = 7/2'
    3  "right bowtie 0; 7, x, y; 10, z, 8"                  answer  "x = 21/5, y = 28/5, z = 6"
    4  "base 6 + 4, leg 4; A, B, C"   (A, B up the hypotenuse, C the big leg)
                                                            answer  "A = 2 sqrt(13), B = (4 sqrt(13))/3, C = 20/3"
       "hyp 13 + 26, leg 5; a, b, c"  (a, b along the base, c the big leg)
                                                            answer  "a = 12, b = 24, c = 15"
    5  "4 + 8; a, b, h"   (the leg at the first piece, the other leg, the altitude)
                                                            answer  "a = 4 sqrt(3), b = 4 sqrt(6), h = 4 sqrt(2)"
"""
import math, re
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, parts
from ..typmath import single, display, dfrac, pretty, text as plain
from .adv_lesson_20 import simplest
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_3"
FIXED = False
TITLE = "Lesson 3: Pythagorean Theorem, Similar Triangles"
INSTRUCTIONS = "Solve each problem."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

EXACT = ("Find the unknown lengths. Write each one exactly: a whole number, a fraction in lowest terms, "
         "or a simplified radical.")

TYPES = [
    dict(key="1", title="Right, Acute, or Obtuse from the Sides",
         look="The three side lengths of a triangle, in no particular order.",
         move="Square the longest side and compare it with the sum of the squares of the other two. Equal: "
              "right; less: acute; greater: obtuse (7^2 = 49 > 5^2 + 4^2 = 41).",
         instructions="Compare the square of the longest side with the sum of the squares of the other two sides.",
         space="0.8in"),
    dict(key="2", title="Similar Triangles and Scale Factors",
         look="Two triangles with matching angle marks; one pair of matching sides is given in both.",
         move="Sides opposite equal angles correspond. The known pair gives the scale factor (7/5 from left to "
              "right, 5/7 back). Multiply a side by the factor to get its partner in the other triangle.",
         instructions=EXACT, space="1.6in"),
    dict(key="3", title="Similar Right Triangles at Vertical Angles",
         look="Two right triangles crossing at a point; one has two sides given, the other one.",
         move="Vertical angles are equal and both have a right angle, so the triangles are similar. Find the "
              "third side of the triangle with two sides given (10^2 = 8^2 + z^2), then use the ratio of the "
              "hypotenuses for the other triangle's sides.",
         instructions=EXACT, space="1.6in"),
    dict(key="4", title="A Right Triangle Inside a Right Triangle",
         look="A perpendicular cuts a small right triangle off a big one; they share the marked angle.",
         move="Draw the two triangles separately. The Pythagorean theorem finds the small triangle's third "
              "side; the ratio of matching sides (small/big) finds the big triangle's sides; subtract to get "
              "a piece (B = (A + B) - A).",
         instructions=EXACT, space="1.6in"),
    dict(key="5", title="The Altitude to the Hypotenuse",
         look="A right triangle with the altitude from its right angle; the hypotenuse is cut into two pieces.",
         move="The altitude makes three similar right triangles. Each leg is the geometric mean of the whole "
              "hypotenuse and its own piece (a/4 = 12/a), and the altitude of the two pieces (4/h = h/8). "
              "Simplify each radical.",
         instructions=EXACT, space="1.6in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    """The problem without its layout: the same triangles turned another way are the same problem."""
    return (NAME, p["type"], re.sub(r"^(apart \d+ \d+|bowtie \d|right bowtie \d)", lambda m: m.group(0).split()[0],
                                    p["prompt"]))

def is_square(n):
    return n >= 0 and math.isqrt(n) ** 2 == n

# A triangle is drawn only if every angle is at least this (a sliver can't carry its marks).
MIN_ANGLE = 22

def angles(a, b, c):
    """The angles (degrees) opposite sides a, b, c; None if they don't make a triangle."""
    a, b, c = float(a), float(b), float(c)
    if not (a + b > c and a + c > b and b + c > a):
        return None
    A = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
    B = math.degrees(math.acos((a * a + c * c - b * b) / (2 * a * c)))
    return A, B, 180 - A - B

def drawable(a, b, c):
    t = angles(a, b, c)
    return t is not None and min(t) >= MIN_ANGLE

# ------------------------------------------------------------------
# Type 1: right, acute, or obtuse from the sides
# ------------------------------------------------------------------
SIDES1 = range(2, 21)
UNITS = ("", "", "cm", "m", "in", "ft")
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]
RIGHT1 = sorted({(k * a, k * b, k * c) for a, b, c in TRIPLES for k in range(1, 8) if k * c <= 20})
KINDS = ("right", "acute", "obtuse")

def classify(a, b, c):
    a, b, c = sorted((a, b, c))
    d = c * c - (a * a + b * b)
    return "right" if d == 0 else "acute" if d < 0 else "obtuse"

def t1_build(a, b, c, unit):
    u = f" {unit}" if unit else ""
    return f"{a}{u}, {b}{u}, {c}{u}"

def t1_order(r, sides):
    s = list(sides)
    r.shuffle(s)
    return s

def t1_right(r):
    a, b, c = t1_order(r, r.choice(RIGHT1))
    return dict(a=a, b=b, c=c, unit=r.choice(UNITS))

def t1_kind(kind, near):
    def pick(r):
        a, b, c = sorted(r.choice(SIDES1) for _ in range(3))
        need(a + b > c and not a == b == c and classify(a, b, c) == kind)
        if near:                                     # c^2 close to a^2 + b^2: the eye can't tell
            need(abs(c * c - a * a - b * b) <= 0.2 * (a * a + b * b))
        a, b, c = t1_order(r, (a, b, c))
        return dict(a=a, b=b, c=c, unit=r.choice(UNITS))
    return pick

SIDES_RE = re.compile(r"^(\d+)(?: (cm|m|in|ft))?, (\d+)(?: (cm|m|in|ft))?, (\d+)(?: (cm|m|in|ft))?$")

def read_sides(prompt):
    m = SIDES_RE.match(prompt)
    if not m:
        raise ValueError("write the three sides like: 7, 5, 4 or 7 cm, 12 cm, 6 cm")
    a, ua, b, ub, c, uc = m.groups()
    if not ua == ub == uc:
        raise ValueError("give every side the same unit")
    a, b, c = int(a), int(b), int(c)
    s = sorted((a, b, c))
    if not s[0] > 0 or s[0] + s[1] <= s[2]:
        raise ValueError("these sides don't make a triangle: the two shorter add to more than the longest")
    return (a, b, c), ua or ""

def classify_answer(prompt):
    (a, b, c), _ = read_sides(prompt)
    return classify(a, b, c)

def check_classify(p):
    (a, b, c), _ = read_sides(p["prompt"])
    s = sorted((a, b, c))
    if s[0] + s[1] <= s[2] or p["answer"] not in KINDS:
        return False
    # The largest angle by the law of cosines.
    x, y, z = (sp.Integer(v) for v in s)
    cos = (x ** 2 + y ** 2 - z ** 2) / (2 * x * y)
    return p["answer"] == ("right" if cos == 0 else "acute" if cos > 0 else "obtuse")

# ------------------------------------------------------------------
# Types 2 and 3: two similar triangles, read from the prompt
# ------------------------------------------------------------------
LETTER = re.compile(r"^[a-zA-Z]$")
TRI_RE = re.compile(r"^(apart (\d+) (\d+)|bowtie ([01])|right bowtie ([01]))(, factors)?; ([^;]+); ([^;]+)$")
POSES = range(12)

def read_list(t):
    out = []
    for s in t.split(","):
        s = s.strip()
        if LETTER.match(s):
            out.append(s)
        elif re.fullmatch(r"\d+", s) and int(s) > 0:
            out.append(sp.Integer(int(s)))
        else:
            raise ValueError("give each side as a whole number or a letter")
    if len(out) != 3:
        raise ValueError("list each triangle's three sides")
    return out

def read_pair(prompt):
    """(layout, poses or flip, factors?, left sides, right sides): a side a number or a letter."""
    m = TRI_RE.match(prompt)
    if not m:
        raise ValueError("write it like: bowtie 0; 5, 4, x; 7, y, 6")
    head, p1, p2, f1, f2, factors, left, right = m.groups()
    layout = "right" if head.startswith("right") else head.split()[0]
    if layout == "apart":
        poses = (int(p1), int(p2))
        if not all(q in POSES for q in poses):
            raise ValueError("a pose is 0 to 11")
    else:
        poses = int(f1 if f1 is not None else f2)
    L, R = read_list(left), read_list(right)
    letters = [s for s in L + R if isinstance(s, str)]
    if len(set(letters)) != len(letters) or not letters:
        raise ValueError("use each letter once")
    return layout, poses, bool(factors), L, R

def leg_or_hyp(T, i):
    """The missing side i of a right triangle (hypotenuse first) from the other two."""
    if i == 0:
        return sp.sqrt(T[1] ** 2 + T[2] ** 2)
    other = T[3 - i]
    if not T[0] > other:
        raise ValueError("the hypotenuse is the longest side")
    return sp.sqrt(T[0] ** 2 - other ** 2)

def solve_pair(L, R, right):
    """Every side's value: from the ratio of a pair known in both, and (right) the Pythagorean theorem."""
    L, R = list(L), list(R)
    known = lambda v: not isinstance(v, str)
    for _ in range(6):
        if right:
            for T in (L, R):
                miss = [i for i in range(3) if not known(T[i])]
                if len(miss) == 1:
                    T[miss[0]] = leg_or_hyp(T, miss[0])
        pairs = [i for i in range(3) if known(L[i]) and known(R[i])]
        if pairs:
            k = R[pairs[0]] / L[pairs[0]]
            for i in range(3):
                if known(L[i]) and not known(R[i]):
                    R[i] = L[i] * k
                elif known(R[i]) and not known(L[i]):
                    L[i] = R[i] / k
        if all(map(known, L + R)):
            break
    if not all(map(known, L + R)):
        raise ValueError("give a pair of matching sides in both triangles")
    return L, R

def pair_values(prompt):
    """{letter: value}, the scale factors, and both triangles' sides, from the prompt."""
    layout, poses, factors, L, R = read_pair(prompt)
    Lv, Rv = solve_pair(L, R, layout == "right")
    vals = {s: v for T, Tv in ((L, Lv), (R, Rv)) for s, v in zip(T, Tv) if isinstance(s, str)}
    if any(not v > 0 for v in vals.values()):
        raise ValueError("every side is positive")
    if angles(*Lv) is None:
        raise ValueError("these sides don't make a triangle")
    if layout == "right" and any(T[0] ** 2 != T[1] ** 2 + T[2] ** 2 for T in (Lv, Rv)):
        raise ValueError("the sides given don't make a right triangle")
    if any(sp.simplify(Lv[i] * Rv[0] - Lv[0] * Rv[i]) != 0 for i in (1, 2)):
        raise ValueError("the sides given aren't in one ratio")
    return vals, Lv[0] / Rv[0], Lv, Rv

def values_answer(vals, factors=None):
    parts = []
    if factors is not None:
        parts = [f'"right to left" = {single(factors)}', f'"left to right" = {single(1 / factors)}']
    return ", ".join(parts + [f"{s} = {single(vals[s])}" for s in sorted(vals)])

def pair_answer(prompt):
    layout, poses, factors, L, R = read_pair(prompt)
    vals, rl, _, _ = pair_values(prompt)
    return values_answer(vals, rl if factors else None)

NAME_RE = re.compile(r'^\s*("right to left"|"left to right"|[a-zA-Z])\s*=\s*(.+?)\s*$')

def read_answer(answer):
    """{name: (text, value)} from "x = 30/7, y = 28/5"; every value a number in the key's form."""
    out = {}
    for part in answer.split(","):
        m = NAME_RE.match(part)
        if not m:
            raise ValueError("write the answer like x = 30/7, y = 28/5")
        name, t = m.group(1).strip('"'), m.group(2)
        v = to_sympy(t)
        if name in out or v.free_symbols or not v.is_positive:
            raise ValueError("give each unknown once, as a positive number")
        out[name] = (t, v)
    return out

def exact_form(t):
    """A whole number, a reduced fraction, or a simplified radical over a whole number: no decimals."""
    return "." not in t and simplest(t) and not ("/" in t and parts(t)[1] == 1)       # not 4 sqrt(2)/1

def check_pair(p):
    layout, poses, factors, L, R = read_pair(p["prompt"])
    got = read_answer(p["answer"])
    letters = {s for s in L + R if isinstance(s, str)}
    names = letters | ({"right to left", "left to right"} if factors else set())
    if set(got) != names or not all(exact_form(t) for t, _ in got.values()):
        return False
    sub = lambda T: [got[s][1] if isinstance(s, str) else s for s in T]
    Lv, Rv = sub(L), sub(R)
    # Corresponding sides in one ratio: L_i R_j = L_j R_i for every pair.
    if any(sp.simplify(Lv[i] * Rv[j] - Lv[j] * Rv[i]) != 0 for i in range(3) for j in range(i + 1, 3)):
        return False
    s = sorted(Lv, key=float)
    if not sp.simplify(s[0] + s[1] - s[2]) > 0:
        return False
    if layout == "right" and any(sp.simplify(T[0] ** 2 - T[1] ** 2 - T[2] ** 2) != 0 for T in (Lv, Rv)):
        return False
    if factors and (sp.simplify(got["right to left"][1] - Lv[0] / Rv[0]) != 0
                    or sp.simplify(got["left to right"][1] - Rv[0] / Lv[0]) != 0):
        return False
    return True

# ---- Type 2's draws: u in the left triangle and v in the right are the pair known in both
SIDES2 = range(2, 17)

def t2_build(layout, pose, u, v, a, b, i, j, first, factors):
    """The pair (u, v) at place i; a, the left triangle's other known side, at place j; b, the
    right triangle's, at the third place; the left triangle's unknown is `first` (x or y)."""
    m = 3 - i - j
    second = "y" if first == "x" else "x"
    L, R = [None] * 3, [None] * 3
    L[i], R[i] = u, v
    L[j], R[j] = a, second
    L[m], R[m] = first, b
    head = f"apart {pose[0]} {pose[1]}" if layout == "apart" else f"bowtie {pose}"
    return f"{head}{', factors' if factors else ''}; {', '.join(map(str, L))}; {', '.join(map(str, R))}"

def t2_sides(u, v, a, b, i, j):
    """The left triangle's sides, the unknown worked out."""
    m = 3 - i - j
    L = [0] * 3
    L[i], L[j], L[m] = u, a, sp.Rational(b * u, v)
    return L

MAX_DEN = 12                         # Types 2 and 3: an answer's denominator at most this (the book's: 2, 3, 5, 7)
BOWTIE_MAX = 100                     # a bowtie's crossing angle (opposite side 1) at most this

def t2_ok(u, v, a, b, i, j, layout="apart"):
    L = t2_sides(u, v, a, b, i, j)
    if layout == "bowtie" and angles(*L) and angles(*L)[1] > BOWTIE_MAX:
        return False
    return (u != v and i != j and drawable(*L) and len(set(L)) == 3
            and len({u, v, a, b}) >= 3                       # not one number over and over
            and sp.Rational(u, v).q <= MAX_DEN and sp.Rational(v, u).q <= MAX_DEN
            and sp.Rational(b * u, v) not in (a, b) and sp.Rational(a * v, u) not in (a, b))

def t2_pick(layout, factors):
    def pick(r):
        u, v = r.sample(list(SIDES2), 2)
        a, b = r.choice(SIDES2), r.choice(SIDES2)
        i, j = r.sample(range(3), 2)
        need(t2_ok(u, v, a, b, i, j, layout))
        pose = tuple(r.sample(list(POSES), 2)) if layout == "apart" else r.randrange(2)
        return dict(layout=layout, pose=pose, u=u, v=v, a=a, b=b, i=i, j=j,
                    first=r.choice("xy"), factors=factors)
    return pick

# ---- Type 3's draws: a right triangle with two sides known, and its partner with one
RIGHT3 = sorted({(k * c, k * a, k * b) for a, b, c in TRIPLES for k in range(1, 6) if k * c <= 25}
                | {(k * c, k * b, k * a) for a, b, c in TRIPLES for k in range(1, 6) if k * c <= 25})
OTHER3 = range(3, 26)
LETTERS3 = ("xyz", "abc")

def t3_build(flip, full_left, full, gap, pos, w, letters):
    """full: the hypotenuse, far leg, and crossing leg of the triangle with two sides
    given, its side `gap` unknown; the other triangle's side at `pos` is w. The letters go
    to the unknowns in order: left far leg, crossing leg, hypotenuse, then the right's."""
    F = list(full)
    F[gap] = None
    O = [None] * 3
    O[pos] = w
    L, R = (F, O) if full_left else (O, F)
    names = iter(letters)
    for T in (L, R):
        for k in (1, 2, 0):
            if T[k] is None:
                T[k] = next(names)
    return f"right bowtie {flip}; {', '.join(map(str, L))}; {', '.join(map(str, R))}"

def crossing_angle(full):
    """The angle at the crossing: between the hypotenuse and the crossing leg."""
    return math.degrees(math.acos(full[2] / full[0]))

def t3_ok(full, gap, pos, w):
    return (full in RIGHT3 and w in OTHER3 and w != full[pos] and gap in range(3) and pos in range(3)
            and 20 <= crossing_angle(full) <= 70 and 0.4 <= w / full[pos] <= 2.5
            and sp.Rational(w, full[pos]).q <= MAX_DEN)

def t3_pick(source_like):
    def pick(r):
        full = r.choice(RIGHT3)
        gap = r.choice((1, 2)) if source_like else r.randrange(3)
        pos = 0 if source_like else r.randrange(3)
        w = r.choice(OTHER3)
        need(t3_ok(full, gap, pos, w))
        return dict(flip=r.randrange(2), full_left=r.random() < 0.5, full=full, gap=gap, pos=pos, w=w,
                    letters=r.choice(LETTERS3))
    return pick

# ------------------------------------------------------------------
# Type 4: a right triangle inside a right triangle
# ------------------------------------------------------------------
LEN4 = range(2, 13)
PIECE4 = range(2, 31)
ANY4 = range(2, 9)                   # a radical template's legs (base) ...
ANY4_HYP = range(3, 16)              # ... or hypotenuse (hyp): its radicals stay hand-sized, like sqrt(52)
LETTERS4 = ("ABC", "abc", "xyz")
NEST_RE = re.compile(r"^(base|hyp) (\d+) \+ (\d+), leg (\d+); ([a-zA-Z]), ([a-zA-Z]), ([a-zA-Z])$")
LEG_TRIPLES = sorted({(k * a, k * b) for a, b, c in TRIPLES for k in range(1, 5) if k * c <= 20}
                     | {(k * b, k * a) for a, b, c in TRIPLES for k in range(1, 5) if k * c <= 20})
HYP_TRIPLES = sorted({(k * c, k * a) for a, b, c in TRIPLES for k in range(1, 5) if k * c <= 20}
                     | {(k * c, k * b) for a, b, c in TRIPLES for k in range(1, 5) if k * c <= 20})

def t4_base_build(p, q, h, letters):
    return f"base {p} + {q}, leg {h}; {', '.join(letters)}"

def t4_hyp_build(s, t, h, letters):
    return f"hyp {s} + {t}, leg {h}; {', '.join(letters)}"

def base_angle(kind, x, h):
    """The shared angle: the inner leg h over the small base (base) or hypotenuse (hyp)."""
    return math.degrees(math.atan(h / x) if kind == "base" else math.asin(h / x))

def t4_ok(kind, x, y, h):
    if kind == "hyp" and not x > h:
        return False
    return 20 <= base_angle(kind, x, h) <= 55 and x != y and sp.Rational(y, x).q <= MAX_DEN

def t4_base(triple):
    def pick(r):
        p, h = r.choice(LEG_TRIPLES) if triple else (r.choice(ANY4), r.choice(ANY4))
        q = r.choice(LEN4)
        need(p in LEN4 and h in LEN4 and t4_ok("base", p, q, h))
        return dict(p=p, q=q, h=h, letters=r.choice(LETTERS4))
    return pick

def t4_hyp(triple, whole):
    def pick(r):
        s, h = r.choice(HYP_TRIPLES) if triple else (r.choice(ANY4_HYP), r.choice(LEN4))
        t = s * r.choice((2, 3)) if whole else r.choice(PIECE4)
        need(s in PIECE4 and t in PIECE4 and h in LEN4 and t4_ok("hyp", s, t, h))
        need(triple or not is_square(s * s - h * h))          # the radical template keeps its radical
        return dict(s=s, t=t, h=h, letters=r.choice(LETTERS4))
    return pick

def read_nest(prompt):
    m = NEST_RE.match(prompt)
    if not m:
        raise ValueError("write it like: base 6 + 4, leg 4; A, B, C")
    kind, x, y, h, *letters = m.groups()
    x, y, h = int(x), int(y), int(h)
    if not (x and y and h) or len(set(letters)) != 3:
        raise ValueError("whole-number lengths, and three different letters")
    if kind == "hyp" and not x > h:
        raise ValueError("the hypotenuse is longer than the leg")
    return kind, x, y, h, letters

def nest_values(prompt):
    """{letter: value}: base -> the two hypotenuse pieces and the big leg; hyp -> the two base pieces and the big leg."""
    kind, x, y, h, (l1, l2, l3) = read_nest(prompt)
    if kind == "base":
        first = sp.sqrt(x * x + h * h)
    else:
        first = sp.sqrt(x * x - h * h)
    return {l1: first, l2: first * sp.Rational(y, x), l3: h * sp.Rational(x + y, x)}

def nest_answer(prompt):
    return values_answer(nest_values(prompt))

def check_nest(p):
    kind, x, y, h, letters = read_nest(p["prompt"])
    got = read_answer(p["answer"])
    if set(got) != set(letters) or not all(exact_form(t) for t, _ in got.values()):
        return False
    a, b, c = (got[L][1] for L in letters)
    if kind == "base":            # small: legs x, h, hypotenuse a; big: legs x + y, c, hypotenuse a + b
        eqs = [a ** 2 - x ** 2 - h ** 2, (a + b) ** 2 - (x + y) ** 2 - c ** 2, c * x - h * (x + y)]
    else:                         # small: legs a, h, hypotenuse x; big: legs a + b, c, hypotenuse x + y
        eqs = [x ** 2 - a ** 2 - h ** 2, (x + y) ** 2 - (a + b) ** 2 - c ** 2, c * a - h * (a + b)]
    return all(sp.simplify(e) == 0 for e in eqs)

# ------------------------------------------------------------------
# Type 5: the altitude to the hypotenuse
# ------------------------------------------------------------------
PIECE5 = range(1, 17)
SUM5 = 18                            # the whole hypotenuse at most this: radicands stay hand-sized
SUM5_WHOLE = 25                      # ... or this when the altitude is whole (9 + 16)
LETTERS5 = ("abh", "xyz")
ALT_RE = re.compile(r"^(\d+) \+ (\d+); ([a-zA-Z]), ([a-zA-Z]), ([a-zA-Z])$")

def t5_build(m, n, letters):
    return f"{m} + {n}; {', '.join(letters)}"

def t5_ok(m, n):
    return m != n and max(m, n) <= 5 * min(m, n) and m + n <= (SUM5_WHOLE if is_square(m * n) else SUM5)

def t5_pick(square):
    def pick(r):
        m, n = r.choice(PIECE5), r.choice(PIECE5)
        need(t5_ok(m, n) and (is_square(m * n) if square else not is_square(m * n)))
        return dict(m=m, n=n, letters=r.choice(LETTERS5))
    return pick

def read_alt(prompt):
    mt = ALT_RE.match(prompt)
    if not mt:
        raise ValueError("write it like: 4 + 8; a, b, h")
    m, n, *letters = mt.groups()
    m, n = int(m), int(n)
    if not (m and n) or len(set(letters)) != 3:
        raise ValueError("whole-number pieces, and three different letters")
    return m, n, letters

def alt_answer(prompt):
    m, n, (a, b, h) = read_alt(prompt)
    return values_answer({a: sp.sqrt(m * (m + n)), b: sp.sqrt(n * (m + n)), h: sp.sqrt(m * n)})

def check_alt(p):
    m, n, letters = read_alt(p["prompt"])
    got = read_answer(p["answer"])
    if set(got) != set(letters) or not all(exact_form(t) for t, _ in got.values()):
        return False
    a, b, h = (got[L][1] for L in letters)
    eqs = [a ** 2 - h ** 2 - m ** 2, b ** 2 - h ** 2 - n ** 2, a ** 2 + b ** 2 - (m + n) ** 2]
    return all(sp.simplify(e) == 0 for e in eqs)

# ------------------------------------------------------------------
# Templates and ranges
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_right, t1_build), (t1_kind("acute", True), t1_build), (t1_kind("acute", False), t1_build),
          (t1_kind("obtuse", True), t1_build), (t1_kind("obtuse", False), t1_build)],
    "2": [(t2_pick("apart", False), t2_build), (t2_pick("apart", False), t2_build),
          (t2_pick("apart", True), t2_build), (t2_pick("bowtie", False), t2_build),
          (t2_pick("bowtie", False), t2_build)],
    "3": [(t3_pick(True), t3_build), (t3_pick(True), t3_build), (t3_pick(False), t3_build)],
    "4": [(t4_base(False), t4_base_build), (t4_base(True), t4_base_build),
          (t4_hyp(True, True), t4_hyp_build), (t4_hyp(True, False), t4_hyp_build),
          (t4_hyp(False, False), t4_hyp_build)],
    "5": [(t5_pick(False), t5_build), (t5_pick(False), t5_build), (t5_pick(True), t5_build)],
}

def _t1_range(a, b, c, unit):
    x, y, z = sorted((a, b, c))
    if not (all(n in SIDES1 for n in (a, b, c)) and unit in UNITS):
        return False
    if classify(a, b, c) == "right":
        return (x, y, z) in RIGHT1
    return x + y > z and not x == y == z

def _t2_range(layout, pose, u, v, a, b, i, j, first, factors):
    pose_ok = (len(pose) == 2 and pose[0] != pose[1] and all(q in POSES for q in pose)) if layout == "apart" \
        else pose in (0, 1)
    return (layout in ("apart", "bowtie") and pose_ok and all(n in SIDES2 for n in (u, v, a, b))
            and i in range(3) and j in range(3) and first in "xy" and factors in (True, False)
            and t2_ok(u, v, a, b, i, j, layout))

RANGES = {
    t1_build: _t1_range,
    t2_build: _t2_range,
    t3_build: lambda flip, full_left, full, gap, pos, w, letters: (flip in (0, 1) and full_left in (True, False)
                                                                   and letters in LETTERS3 and t3_ok(full, gap, pos, w)),
    t4_base_build: lambda p, q, h, letters: (((p, h) in LEG_TRIPLES or (p in ANY4 and h in ANY4))
                                             and all(n in LEN4 for n in (p, q, h)) and letters in LETTERS4
                                             and t4_ok("base", p, q, h)),
    t4_hyp_build: lambda s, t, h, letters: (((s, h) in HYP_TRIPLES or (s in ANY4_HYP and not is_square(s * s - h * h)))
                                            and s in PIECE4 and t in PIECE4 and h in LEN4 and letters in LETTERS4
                                            and t4_ok("hyp", s, t, h)),
    t5_build: lambda m, n, letters: m in PIECE5 and n in PIECE5 and letters in LETTERS5 and t5_ok(m, n),
}

def in_range(build, params):
    """Can a random draw pick these parameters for this build?"""
    return RANGES[build](**params)

# ------------------------------------------------------------------
# Solving and checking
# ------------------------------------------------------------------
def kind(prompt):
    """Which reader a prompt takes: sides, similar, right, nest, alt."""
    if prompt.startswith(("apart", "bowtie")):
        return "similar"
    if prompt.startswith("right bowtie"):
        return "right"
    if prompt.startswith(("base", "hyp")):
        return "nest"
    if "+" in prompt:
        return "alt"
    return "sides"

SOLVE = {"sides": classify_answer, "similar": pair_answer, "right": pair_answer, "nest": nest_answer,
         "alt": alt_answer}
CHECK = {"sides": check_classify, "similar": check_pair, "right": check_pair, "nest": check_nest,
         "alt": check_alt}
KIND = {"1": "sides", "2": "similar", "3": "right", "4": "nest", "5": "alt"}

def answer_of(prompt):
    return SOLVE[kind(prompt)](prompt)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        if kind(p["prompt"]) != KIND[p["type"]]:
            return "failed"
        ok = CHECK[KIND[p["type"]]](p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Figures: worked out here from the solved sides; lesson_figures draws them
# ------------------------------------------------------------------
def place(s, base, mirror, down):
    """A triangle with sides s (s[i] opposite vertex i), side `base` along the bottom: its vertices."""
    b1, b2 = (base + 1) % 3, (base + 2) % 3
    c, l1, l2 = s[base], s[b2], s[b1]                     # |V_b1 V_b| = s[b2], |V_b2 V_b| = s[b1]
    x = (l1 * l1 - l2 * l2 + c * c) / (2 * c)
    y = math.sqrt(max(l1 * l1 - x * x, 0))
    V = [None] * 3
    V[b1], V[b2], V[base] = (0.0, 0.0), (c, 0.0), (x, y)
    if mirror:
        V = [(c - px, py) for px, py in V]
    if down:
        V = [(px, -py) for px, py in V]
    return V

def tri(V, s_labels, marks):
    """A triangle for fig.triangles: label s_labels[i] on the side opposite vertex i."""
    # fig.triangles labels side i from pts[i] to pts[i+1], which is opposite pts[i+2].
    return dict(pts=V, labels={(i + 1) % 3: s_labels[i] for i in range(3)}, marks=marks)

def clamp(k, lo=0.55, hi=1.8):
    return min(max(k, lo), hi)

def mark(s):
    return f"${s}$"

def similar_figure(prompt, unit="1cm"):
    layout, poses, factors, L, R = read_pair(prompt)
    _, _, Lv, Rv = pair_values(prompt)
    Ls = [float(v) for v in Lv]
    k = float(Rv[0] / Lv[0])
    shown_k = clamp(k)
    ll, rl = [mark(s) for s in L], [mark(s) for s in R]
    if layout == "apart":
        tris = []
        x_at = 0.0
        for n, (pose, scale, labels) in enumerate(((poses[0], 1.0, ll), (poses[1], shown_k, rl))):
            V = place([v * scale for v in Ls], pose // 4, (pose // 2) % 2, pose % 2)
            lo = min(x for x, _ in V)
            V = [(x - lo + x_at, y - (min(yy for _, yy in V))) for x, y in V]
            x_at = max(x for x, _ in V) + 0.35 * max(Ls)
            tris.append(tri(V, labels, {1: 1, 2: 2}))
        return fig.triangles(tris, unit=unit)
    # Meeting at a vertex O. The sides are listed opposite the vertices (U, O, D): for Type 2
    # U unmarked, O one arc (the vertical angles), D two arcs; for Type 3 U the right angle.
    # Either way sides 0 and 2 run from the crossing O, and side 1 is the far side.
    s0, s1, s2 = Ls                                       # |O D| = s0, |D U| = s1, |O U| = s2
    th = math.acos((s0 * s0 + s2 * s2 - s1 * s1) / (2 * s0 * s2))
    up = 1 if poses == 0 else -1
    D = (s0 * math.cos(math.pi - up * th / 2), s0 * math.sin(math.pi - up * th / 2))
    U = (s2 * math.cos(math.pi + up * th / 2), s2 * math.sin(math.pi + up * th / 2))
    O = (0.0, 0.0)
    D2, U2 = (-shown_k * D[0], -shown_k * D[1]), (-shown_k * U[0], -shown_k * U[1])
    marks = {0: "right"} if layout == "right" else {1: 1, 2: 2}
    return fig.triangles([tri([U, O, D], ll, marks), tri([U2, O, D2], rl, marks)], unit=unit)

def nest_figure(prompt, unit="1cm"):
    kind_, x, y, h, (l1, l2, l3) = read_nest(prompt)
    vals = {k: float(v) for k, v in nest_values(prompt).items()}
    if kind_ == "base":
        p, q = x, y
    else:
        p = vals[l1]
        q = vals[l2]
    H = h * (p + q) / p
    A, foot, top, C, Ctop = (0, 0), (p, 0), (p, h), (p + q, 0), (p + q, H)
    inside = ((p + q) * 0.7, H * 0.25)
    if kind_ == "base":
        labels = [(A, foot, top, f"${x}$"), (foot, C, Ctop, f"${y}$"), (foot, top, (p - 1, h / 2), f"${h}$"),
                  (A, top, C, mark(l1)), (top, Ctop, C, mark(l2)), (C, Ctop, A, mark(l3))]
    else:
        labels = [(A, foot, top, mark(l1)), (foot, C, Ctop, mark(l2)), (foot, top, (p - 1, h / 2), f"${h}$"),
                  (A, top, C, f"${x}$"), (top, Ctop, C, f"${y}$"), (C, Ctop, A, mark(l3))]
    marks = [(1, A, C, Ctop), ("right", foot, A, top), ("right", C, A, Ctop)]
    return fig.nested((A, C, Ctop), foot, top, labels, marks, unit=unit)

def alt_figure(prompt, unit="1cm"):
    m, n, (a, b, h) = read_alt(prompt)
    H = math.sqrt(m * n)
    L, Rt, foot, top = (0, 0), (m + n, 0), (m, 0), (m, H)
    # The altitude's label on the side of the longer piece, its right-angle mark on the other.
    side = 1 if n >= m else -1
    labels = [(L, foot, top, f"${m}$"), (foot, Rt, top, f"${n}$"), (L, top, Rt, mark(a)),
              (top, Rt, L, mark(b)), (foot, top, (m - side, H / 2), mark(h))]
    marks = [("right", foot, L if side == 1 else Rt, top), ("right", top, L, Rt)]
    return fig.nested((L, Rt, top), foot, top, labels, marks, unit=unit)

def figure(p, unit="1cm"):
    k = kind(p["prompt"])
    if k in ("similar", "right"):
        return similar_figure(p["prompt"], unit)
    if k == "nest":
        return nest_figure(p["prompt"], unit)
    if k == "alt":
        return alt_figure(p["prompt"], unit)
    return ""

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def listing(names):
    """$x$ and $y$; $x$, $y$, and $z$."""
    ms = [f"${n}$" for n in names]
    return ms[0] if len(ms) == 1 else " and ".join(ms) if len(ms) == 2 else ", ".join(ms[:-1]) + ", and " + ms[-1]

def unknowns(p):
    k = kind(p["prompt"])
    if k in ("similar", "right"):
        _, _, _, L, R = read_pair(p["prompt"])
        return sorted(s for s in L + R if isinstance(s, str))
    if k == "nest":
        return sorted(read_nest(p["prompt"])[4])
    return sorted(read_alt(p["prompt"])[2])

def statement(p):
    """The problem's words (Typst markup), without its figure."""
    k = kind(p["prompt"])
    if k == "sides":
        (a, b, c), unit = read_sides(p["prompt"])
        u = f" {unit}" if unit else ""
        return (f"The lengths of the sides of a triangle are {a}{u}, {b}{u}, and {c}{u}, respectively. Is the "
                f"triangle a right triangle, an acute triangle, or an obtuse triangle?")
    names = listing(unknowns(p))
    if k == "similar" and read_pair(p["prompt"])[2]:
        return ("In the two triangles shown, find the scale factor from right to left. What is the scale "
                f"factor from left to right? Using scale factors, find {names}.")
    return f"Find {names}."

def typst(p, gap="0.3em"):
    try:
        s, f = statement(p), figure(p)
    except ValueError:
        return p["prompt"]
    return s if not f else f"{s} #v(0.4em) #align(center)[{f}]"

def comparison(prompt):
    """7^2 > 5^2 + 4^2: the longest side's square against the others', in the prompt's order."""
    (a, b, c), _ = read_sides(prompt)
    s = [a, b, c]
    big = s.index(max(s))
    rest = [v for i, v in enumerate(s) if i != big]
    d = max(s) ** 2 - rest[0] ** 2 - rest[1] ** 2
    op = "=" if d == 0 else "<" if d < 0 else ">"
    return f"{max(s)}^2 {op} {rest[0]}^2 + {rest[1]}^2"

def answer_typst(p):
    if p["type"] == "1":
        try:
            return f"*{p['answer']} triangle* #h(1em) ${comparison(p['prompt'])}$"
        except ValueError:
            return f"*{p['answer']}*"
    parts = [dfrac(part.strip()) for part in p["answer"].split(",")]
    if parts[0].startswith('"right to left"'):              # the scale factors on a line of their own
        return "$" + ", quad ".join(parts[:2]) + " \\ " + ", quad ".join(parts[2:]) + "$"
    return "$" + ", quad ".join(parts) + "$"

SLIDE_UNIT = "1.9cm"

def slide_typst(p, key=False):
    """A figure's slide: the words (and the answer, hidden on the question slide)
    beside the figure drawn larger; the figure never moves. None for Type 1."""
    try:
        f, s = figure(p, SLIDE_UNIT), statement(p)
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
    return s.replace("$", "") + ("" if p["type"] == "1" else "   [figure]")

def answer_text(p):
    if p["type"] == "1":
        return f"{p['answer']} triangle"
    out = []
    for part in p["answer"].split(","):
        name, _, value = part.partition("=")
        out.append(f"{name.strip().strip(chr(34))} = {pretty(value.strip())}")
    return ", ".join(out)

def height(p):
    return 0.5 if p["type"] == "1" else 2.6

# ------------------------------------------------------------------
# Editing: the prompt is the problem's data, in its short form
# ------------------------------------------------------------------
EXAMPLE = {"1": "7, 5, 4", "2": "bowtie 0; 5, 4, x; 7, y, 6", "3": "right bowtie 0; 7, x, y; 10, z, 8",
           "4": "base 6 + 4, leg 4; A, B, C", "5": "4 + 8; a, b, h"}

def clean(t):
    return " ".join(t.replace("−", "-").replace("√", "sqrt").split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    try:
        if kind(t) != KIND[old["type"]]:
            raise ValueError
        answer = answer_of(t)
    except (ValueError, gen.Redraw, SyntaxError, TypeError, KeyError, ZeroDivisionError):
        raise ValueError(f"write it like: {EXAMPLE[old['type']]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    t = clean(t)
    if p["type"] == "1":
        t = t.lower().removesuffix(" triangle").strip()
    new = dict(p, answer=t)
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)
