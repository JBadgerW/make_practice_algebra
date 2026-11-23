"""Lesson 13 (Advanced Math): secants and tangents. Intersecting secants,
intersecting secants and tangents, products of chord segments, products of
secant and tangent segments. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_013/slides/deck_013.typ): examples 13.5,
13.6, 13.8, 13.10, 13.12 and Problem Set 13, problems 4-7.

    1  secants crossing inside:          arcs 30°, 70°                          x = 50
    2  an angle outside, arcs given:     two secants; far 80°, near 30°          x = 25
    3  an angle outside, an arc missing: a tangent and a secant; far 170°, 120°  x = 50
    4  products of chord segments:       30 and x + 20; 40 and x + 10           x = 20
    5  products of secant segments:      5 and 7; 6 and x                       x = 4
    6  secant segments, a quadratic:     3 and x; x and 3                       x = 3
    7  secant and tangent segments:      x and 12; tangent 8                    x = 4

The problem types file puts the angle problems (examples 13.5, 13.6, problems 4
and 5) under one heading. They are Types 1-3 here: an angle inside is half the
sum of its arcs (problem 4); an angle outside is half the difference (13.5,
problem 5); and 13.6 gives the far arc and the arc that isn't intercepted, so
the near arc must be found from 360° first, a step students miss. Type 2 also
draws a tangent and a secant with both arcs given (the theorem of 13.3), and
Type 3 two tangents with one arc given (13.4's theorem). Products of secant
segments is two types: problem 7 is linear, and 13.10 (an x on both secants)
is a quadratic with a negative root to reject. Type 7 is 13.12, a secant and a
tangent, with x the external part (a quadratic, as in the book), the tangent,
or the internal part.

Every figure is drawn from the problem's data, to scale. An angle figure puts
its points on the circle by their arcs, so the angle at the crossing is the
true one; a segment figure sets the circle and the lines' directions so each
part has its length (the power of the point is the same along every line).
Labels are set by Lesson 11's placer, clear of every line, the circle, and each
other. A figure is mirrored one of four ways (its pose); chord figures are
Lesson 11's, turned one of eight.

The key writes what the deck writes: x = 25, x = 27/5 (a fraction in lowest
terms), with no degree sign. A quadratic's negative root is rejected, so the key
gives the one positive length.

check() works from the prompt's data, not from how the answer was built. Types
1-3 measure the angle in the figure itself, from the points on the circle (no
arc theorem used), and compare it with the answer. Types 4-7 put the answer into
the lesson's products (chord parts, whole secant times external part, tangent
squared), require every length positive, and require that sympy finds no other
positive solution. The answer must be "x = value", whole or in lowest terms.

Skipped sources: examples 13.1-13.4 (the angle theorems), 13.7 (products of
chord segments), 13.9 (secant segments), and 13.11 (secant and tangent
segments). They are proofs; their theorems are the moves of Types 1-7.

A problem: dict(type, prompt, answer, source). The prompt is the figure's data,
and it is what an edit changes; "pose k" mirrors the figure.
    1  "30, 70; pose 0"                               the two intercepted arcs
    2  "secants; far 80, near 30; pose 0"             also "tangent and secant; far 100, near 40"
    3  "tangent and secant; far 170, back 120; pose 0"   back: the arc not intercepted;
                                                      also "tangents; far 240", "tangents; near 120"
    4  "30, x + 20; 40, x + 10; pose 0"               each chord's two parts (Lesson 11's form)
    5  "5, 7; 6, x; pose 0"                           each secant: external part, internal part
    6  "3, x; x, 3; pose 0"
    7  "x, 12; 8; pose 0"                             the secant (external, internal); the tangent
"""
import math, re
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need
from ..typmath import dfrac, text as plain
from . import lesson_figures as fig
from . import adv_lesson_11 as L11

NAME = FAMILY = "adv_lesson_13"
FIXED = False
TITLE = ("Lesson 13: Secants and Tangents, Intersecting Secants, Intersecting Secants and Tangents, "
         "Products of Chord Segments, Products of Secant and Tangent Segments")
INSTRUCTIONS = "Find x."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

TYPES = [
    dict(key="1", title="Secants Intersecting Inside a Circle", instructions="Find x.",
         look="Two secants crossing inside a circle; the arcs across from the angle $x$ and its vertical angle "
              "are given.",
         move="An angle formed inside a circle is half the sum of the two arcs it and its vertical angle "
              "intercept: $x = 1/2 (30 + 70) = 50$."),
    dict(key="2", title="An Angle Outside a Circle", instructions="Find x.",
         look="Two secants, or a tangent and a secant, meeting outside a circle; the far arc and the near arc "
              "are both given.",
         move="An angle formed outside a circle is half the difference of the intercepted arcs, the far arc "
              "less the near one: $x = 1/2 (80 - 30) = 25$."),
    dict(key="3", title="An Angle Outside, an Arc to Find First", instructions="Find x.",
         look="A tangent and a secant (or two tangents) meeting outside a circle; one of the arcs the angle "
              "intercepts isn't labeled.",
         move="The arcs of a circle sum to $360 degree$, so find the missing arc first: $360 - 170 - 120 = 70$. "
              "Then take half the difference, far less near: $x = 1/2 (170 - 70) = 50$."),
    dict(key="4", title="Products of Chord Segments", instructions="Find x.",
         look="Two chords crossing inside a circle, each cut into two parts.",
         move="The products of the parts of the two chords are equal: $30(x + 20) = 40(x + 10)$. Multiply out "
              "and solve."),
    dict(key="5", title="Products of Secant Segments", instructions="Find x.",
         look="Two secants drawn to a circle from one point outside; each has its external part and its part "
              "inside the circle labeled.",
         move="The whole secant times its external part is the same for both secants: $5(5 + 7) = 6(6 + x)$."),
    dict(key="6", title="Secant Segments That Give a Quadratic", instructions="Find x.",
         look="Two secants from one point, with $x$ in an external part, so $x$ is multiplied by itself.",
         move="Write whole secant times external part for both: $3(x + 3) = x(x + 3)$. Solve the quadratic; a "
              "length is positive, so reject the negative root."),
    dict(key="7", title="Products of Secant and Tangent Segments", instructions="Find x.",
         look="A secant and a tangent drawn to a circle from one point outside.",
         move="The whole secant times its external part equals the square of the tangent: $x(x + 12) = 8^2$. "
              "Solve, and reject a negative root."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

FIGURES = tuple(KEYS)                 # every type is a figure
X = sp.Symbol("x")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], re.sub(r"; pose \d+$", "", p["prompt"]))   # the same numbers mirrored is no new problem

split, value, read_answer = L11.split, L11.value, L11.read_answer

def answer_text_of(v):
    return f"x = {v}"

# ------------------------------------------------------------------
# Reading an angle prompt
# ------------------------------------------------------------------
KINDS = ("secants", "tangent and secant", "tangents")
ARC_PART = re.compile(r"(far|near|back)\s+(\d+)")

def whole(t):
    v = L11.number(t)
    if v.denominator != 1:
        raise ValueError("arcs in whole degrees")
    return int(v)

def angle_data(prompt, typ):
    """Type 1: ("inside", {"left": a, "right": b}, pose). Types 2-3: (kind, {"far": .., "near": ..,
    "back": ..}, pose), every arc known (a missing one found from 360), each positive."""
    parts, pose = split(prompt)
    if typ == "1":
        if [len(p) for p in parts] != [2]:
            raise ValueError("two arcs")
        a, b = (whole(t) for t in parts[0])
        if not (a > 0 and b > 0 and a + b < 360):
            raise ValueError("not a figure")
        return "inside", dict(left=a, right=b), pose
    if len(parts) != 2 or len(parts[0]) != 1 or parts[0][0] not in KINDS:
        raise ValueError("secants, tangent and secant, or tangents")
    kind = parts[0][0]
    given = {}
    for t in parts[1]:
        m = ARC_PART.fullmatch(t)
        if not m or m.group(1) in given:
            raise ValueError("far, near, back arcs")
        given[m.group(1)] = int(m.group(2))
    if kind == "tangents":
        if "back" in given or len(given) != 1:
            raise ValueError("one arc")
        far = given.get("far", 360 - given.get("near", 0))
        arcs = dict(far=far, near=360 - far)
    else:
        if len(given) != 2:
            raise ValueError("two arcs")
        if kind == "secants" and "back" in given:
            raise ValueError("far and near arcs")      # two secants leave two back arcs
        arcs = dict(given)
        missing = ({"far", "near", "back"} - set(arcs)).pop()
        arcs[missing] = 360 - sum(arcs.values())
        if kind == "secants":
            arcs.pop("back")
    if min(arcs.values()) <= 0 or arcs["far"] <= arcs["near"] or sum(arcs.values()) > 360:
        raise ValueError("not a figure")
    return kind, arcs, pose

# ------------------------------------------------------------------
# Type 1: secants intersecting inside (problem 4)
# ------------------------------------------------------------------
ARC1 = range(20, 170, 10)
POSES = range(4)                      # bit 0 mirrors left-right, bit 1 top-bottom

def t1_ok(a, b, pose):
    return a in ARC1 and b in ARC1 and a != b and a + b <= 260 and pose in POSES

def t1_pick(r):
    return dict(a=r.choice(ARC1), b=r.choice(ARC1), pose=r.choice(POSES))

def t1(a, b, pose):
    need(t1_ok(a, b, pose))
    prompt = f"{a}, {b}; pose {pose}"
    need(drawable("1", prompt))
    return prompt

# ------------------------------------------------------------------
# Type 2: an angle outside, both arcs given (example 13.5, problem 5)
# ------------------------------------------------------------------
FAR2 = range(60, 260, 10)
NEAR2 = range(20, 130, 10)
MIN_DIFF = 30                         # far less near: x at least 15, as in problem 5
MIN_BACK = 40                         # an arc that isn't intercepted

def t2_secants_ok(far, near, pose):
    return (far in FAR2 and near in NEAR2 and far - near >= MIN_DIFF and 360 - far - near >= 2 * MIN_BACK + 20
            and pose in POSES)

def t2_tangent_ok(far, near, pose):
    return (far in FAR2 and near in NEAR2 and far - near >= MIN_DIFF and 360 - far - near >= MIN_BACK
            and pose in POSES)

def t2_pick(r):
    return dict(far=r.choice(FAR2), near=r.choice(NEAR2), pose=r.choice(POSES))

def t2_secants(far, near, pose):
    need(t2_secants_ok(far, near, pose))
    prompt = f"secants; far {far}, near {near}; pose {pose}"
    need(drawable("2", prompt))
    return prompt

def t2_tangent(far, near, pose):
    need(t2_tangent_ok(far, near, pose))
    prompt = f"tangent and secant; far {far}, near {near}; pose {pose}"
    need(drawable("2", prompt))
    return prompt

# ------------------------------------------------------------------
# Type 3: an angle outside, the near arc to find (example 13.6)
# ------------------------------------------------------------------
FAR3 = range(100, 260, 10)
BACK3 = range(40, 200, 10)
NEAR3 = range(20, 130, 10)            # the arc found
FAR3T = range(220, 260, 5)            # two tangents: x = far - 180, 40 to 75
GIVEN3T = ("far", "near")              # the arc labeled; the other is found

def t3_tangent_ok(far, back, pose):
    near = 360 - far - back
    return far in FAR3 and back in BACK3 and near in NEAR3 and far - near >= MIN_DIFF and pose in POSES

def t3_tangent_pick(r):
    return dict(far=r.choice(FAR3), back=r.choice(BACK3), pose=r.choice(POSES))

def t3_tangent(far, back, pose):
    need(t3_tangent_ok(far, back, pose))
    prompt = f"tangent and secant; far {far}, back {back}; pose {pose}"
    need(drawable("3", prompt))
    return prompt

def t3_tangents_ok(far, given, pose):
    return far in FAR3T and given in GIVEN3T and pose in POSES

def t3_tangents_pick(r):
    return dict(far=r.choice(FAR3T), given=r.choice(GIVEN3T), pose=r.choice(POSES))

def t3_tangents(far, given, pose):
    need(t3_tangents_ok(far, given, pose))
    prompt = f"tangents; {given} {far if given == 'far' else 360 - far}; pose {pose}"
    need(drawable("3", prompt))
    return prompt

# ------------------------------------------------------------------
# Type 4: products of chord segments (example 13.8, problem 6)
# ------------------------------------------------------------------
ORDERS = L11.ORDERS
PART4 = range(4, 41)                  # a part that is a number, beside x + k
SHIFT4 = range(1, 21)                 # k in x + k
X4 = range(2, 21)                     # the answer
NUM4 = range(2, 16)                   # the three numbers when x stands alone
POSES4 = range(8)

def t4_linear_ok(n1, k1, n2, k2, o1, o2, pose):
    if not (n1 in PART4 and n2 in PART4 and k1 in SHIFT4 and k2 in SHIFT4 and n1 != n2
            and o1 in ORDERS and o2 in ORDERS and pose in POSES4):
        return False
    x = F(n2 * k2 - n1 * k1, n1 - n2)
    return x.denominator == 1 and x in X4

def t4_linear_pick(r):
    x, n1, n2, k1 = r.choice(X4), r.choice(PART4), r.choice(PART4), r.choice(SHIFT4)
    need(n1 != n2 and (n1 * (x + k1)) % n2 == 0)
    return dict(n1=n1, k1=k1, n2=n2, k2=n1 * (x + k1) // n2 - x, o1=r.choice(ORDERS), o2=r.choice(ORDERS),
                pose=r.choice(POSES4))

def t4_linear(n1, k1, n2, k2, o1, o2, pose):      # 13.8: 30, x + 20; 40, x + 10
    need(t4_linear_ok(n1, k1, n2, k2, o1, o2, pose))
    prompt = f"{L11.pair(n1, f'x + {k1}', o1)}; {L11.pair(n2, f'x + {k2}', o2)}; pose {pose}"
    need(drawable("4", prompt))
    return prompt

def t4_plain_ok(a, b, c, o, pose):
    if not (a in NUM4 and b in NUM4 and c in NUM4 and c not in (a, b) and o in ORDERS and pose in POSES4):
        return False
    x = F(a * b, c)
    return 1 <= x <= 25 and x.denominator <= 5       # 27/5 at most: no 108/7

def t4_plain_pick(r):
    return dict(a=r.choice(NUM4), b=r.choice(NUM4), c=r.choice(NUM4), o=r.choice(ORDERS), pose=r.choice(POSES4))

def t4_plain(a, b, c, o, pose):                   # problem 6: 3, 9; 5, x
    need(t4_plain_ok(a, b, c, o, pose))
    prompt = f"{a}, {b}; {L11.pair(c, 'x', o)}; pose {pose}"
    need(drawable("4", prompt))
    return prompt

# ------------------------------------------------------------------
# Type 5: two secants, linear (problem 7)
# ------------------------------------------------------------------
EXT = range(2, 13)                    # an external part
INT = range(2, 16)                    # an internal part
X5 = range(1, 21)

def t5_ok(e1, i1, e2, flip, pose):
    if not (e1 in EXT and i1 in INT and e2 in EXT and e1 != e2 and flip in (0, 1) and pose in POSES):
        return False
    x = F(e1 * (e1 + i1), e2) - e2
    return x.denominator == 1 and x in X5

def t5_pick(r):
    return dict(e1=r.choice(EXT), i1=r.choice(INT), e2=r.choice(EXT), flip=r.choice((0, 1)), pose=r.choice(POSES))

def t5(e1, i1, e2, flip, pose):
    need(t5_ok(e1, i1, e2, flip, pose))
    s = [f"{e1}, {i1}", f"{e2}, x"]
    if flip:
        s.reverse()
    prompt = f"{s[0]}; {s[1]}; pose {pose}"
    need(drawable("5", prompt))
    return prompt

# ------------------------------------------------------------------
# Type 6: two secants, a quadratic (example 13.10)
# ------------------------------------------------------------------
A6 = range(2, 13)                     # a in "a, x"
B6 = range(1, 31)                     # b in "x, b"
X6 = range(2, 13)                     # x as an external part

def positive_root(b, c):
    """The positive whole root of x^2 + b x + c = 0 when c < 0, else None."""
    d = b * b - 4 * c
    s = math.isqrt(d)
    if c >= 0 or s * s != d or (s - b) % 2:
        return None
    return (s - b) // 2

def t6_cross_root(a, b):
    """a(a + x) = x(x + b): x^2 + (b - a) x - a^2 = 0."""
    return positive_root(b - a, -a * a)

SAME6 = [(a, a) for a in range(2, 7)]  # 13.10's 3, x; x, 3, where x is always a: kept, but drawn a quarter of the time
CROSS6 = [(a, b) for a in A6 for b in B6 if a != b and t6_cross_root(a, b) and t6_cross_root(a, b) <= 20]

def t6_cross_ok(a, b, flip, pose):
    return ((a, b) in CROSS6 or (a, b) in SAME6) and flip in (0, 1) and pose in POSES

def t6_cross_pick(r):
    a, b = r.choice(SAME6 if r.random() < 0.25 else CROSS6)
    return dict(a=a, b=b, flip=r.choice((0, 1)), pose=r.choice(POSES))

def t6_cross(a, b, flip, pose):                  # 13.10: 3, x; x, 3
    need(t6_cross_ok(a, b, flip, pose))
    s = [f"{a}, x", f"x, {b}"]
    if flip:
        s.reverse()
    prompt = f"{s[0]}; {s[1]}; pose {pose}"
    need(drawable("6", prompt))
    return prompt

def t6_one_ok(x, i1, e2, flip, pose):
    if not (x in X6 and i1 in INT and e2 in EXT and x != e2 and flip in (0, 1) and pose in POSES):
        return False
    i2 = F(x * (x + i1), e2) - e2
    return i2.denominator == 1 and i2 in INT

def t6_one_pick(r):
    x, i1, e2 = r.choice(X6), r.choice(INT), r.choice(EXT)
    need(e2 != 0 and (x * (x + i1)) % e2 == 0)
    return dict(x=x, i1=i1, e2=e2, flip=r.choice((0, 1)), pose=r.choice(POSES))

def t6_one(x, i1, e2, flip, pose):               # x, 5; 4, 10
    need(t6_one_ok(x, i1, e2, flip, pose))
    s = [f"x, {i1}", f"{e2}, {x * (x + i1) // e2 - e2}"]
    if flip:
        s.reverse()
    prompt = f"{s[0]}; {s[1]}; pose {pose}"
    need(drawable("6", prompt))
    return prompt

# ------------------------------------------------------------------
# Type 7: a secant and a tangent (example 13.12)
# ------------------------------------------------------------------
TAN = range(2, 31)                    # the tangent
INT7 = range(2, 31)                   # an internal part
X7 = range(1, 16)                     # x as the external part

def square_root(n):
    s = math.isqrt(n)
    return s if s * s == n else None

EXTERNAL7 = [(x, i) for x in X7 for i in INT7 if square_root(x * (x + i)) in TAN]

def t7_external_ok(x, i, pose):
    return (x, i) in EXTERNAL7 and pose in POSES

def t7_external_pick(r):
    x, i = r.choice(EXTERNAL7)
    return dict(x=x, i=i, pose=r.choice(POSES))

def t7_external(x, i, pose):                     # 13.12: x, 12; 8
    need(t7_external_ok(x, i, pose))
    prompt = f"x, {i}; {square_root(x * (x + i))}; pose {pose}"
    need(drawable("7", prompt))
    return prompt

def t7_tangent_ok(e, i, pose):
    return e in EXT and i in INT7 and square_root(e * (e + i)) in TAN and pose in POSES

def t7_tangent_pick(r):
    return dict(e=r.choice(EXT), i=r.choice(INT7), pose=r.choice(POSES))

def t7_tangent(e, i, pose):                      # 4, 12; x
    need(t7_tangent_ok(e, i, pose))
    prompt = f"{e}, {i}; x; pose {pose}"
    need(drawable("7", prompt))
    return prompt

def t7_internal_ok(e, t, pose):
    if not (e in EXT and t in TAN and pose in POSES):
        return False
    x = F(t * t, e) - e
    return x.denominator == 1 and x in INT7

def t7_internal_pick(r):
    return dict(e=r.choice(EXT), t=r.choice(range(2, 21)), pose=r.choice(POSES))

def t7_internal(e, t, pose):                     # 4, x; 8
    need(t7_internal_ok(e, t, pose))
    prompt = f"{e}, x; {t}; pose {pose}"
    need(drawable("7", prompt))
    return prompt

# ------------------------------------------------------------------
# The templates
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick, t1)],
    "2": [(t2_pick, t2_secants), (t2_pick, t2_secants), (t2_pick, t2_tangent)],
    "3": [(t3_tangent_pick, t3_tangent), (t3_tangent_pick, t3_tangent), (t3_tangent_pick, t3_tangent),
          (t3_tangents_pick, t3_tangents)],
    "4": [(t4_linear_pick, t4_linear), (t4_plain_pick, t4_plain)],
    "5": [(t5_pick, t5)],
    "6": [(t6_cross_pick, t6_cross), (t6_one_pick, t6_one)],
    "7": [(t7_external_pick, t7_external), (t7_external_pick, t7_external), (t7_tangent_pick, t7_tangent),
          (t7_internal_pick, t7_internal)],
}
RANGES = {t1: t1_ok, t2_secants: t2_secants_ok, t2_tangent: t2_tangent_ok, t3_tangent: t3_tangent_ok,
          t3_tangents: t3_tangents_ok, t4_linear: t4_linear_ok, t4_plain: t4_plain_ok, t5: t5_ok,
          t6_cross: t6_cross_ok, t6_one: t6_one_ok, t7_external: t7_external_ok, t7_tangent: t7_tangent_ok,
          t7_internal: t7_internal_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# Lengths: Types 4-7
# ------------------------------------------------------------------
def length_parts(prompt, typ):
    """(parts, pose, relation): relation is a sympy expression in x that is 0 when the lesson's
    products agree. Type 4: two chords; Types 5-6: two secants (external, internal); Type 7: a
    secant (external, internal) and a tangent."""
    parts, pose = split(prompt)
    shape = [2, 1] if typ == "7" else [2, 2]
    if [len(p) for p in parts] != shape:
        raise ValueError("the parts of each line")
    v = [[sp.sympify(value(t)) for t in p] for p in parts]
    if any(e.free_symbols - {X} for p in v for e in p) or not any(e.free_symbols for p in v for e in p):
        raise ValueError("lengths in x")
    if typ == "4":
        rel = v[0][0] * v[0][1] - v[1][0] * v[1][1]
    elif typ == "7":
        rel = v[0][0] * (v[0][0] + v[0][1]) - v[1][0] ** 2
    else:
        rel = v[0][0] * (v[0][0] + v[0][1]) - v[1][0] * (v[1][0] + v[1][1])
    return parts, pose, v, sp.expand(rel)

def lengths_at(v, x):
    return [[e.subs(X, x) for e in p] for p in v]

def length_solutions(v, rel):
    """Every real x that makes the products agree with every length positive."""
    if rel == 0:
        raise ValueError("every x works")
    sols = [s for s in sp.solve(rel, X) if s.is_real]
    return [s for s in sols if all(e > 0 for p in lengths_at(v, s) for e in p)]

def length_value(prompt, typ):
    _, _, v, rel = length_parts(prompt, typ)
    sols = length_solutions(v, rel)
    if len(sols) != 1 or not sols[0].is_Rational:
        raise ValueError("no single length")
    return F(int(sols[0].p), int(sols[0].q))

def numeric_lengths(prompt, typ):
    """The figure's lengths, floats: [[p, q], [r, s]] (or [[e, i], [t]])."""
    _, _, v, _ = length_parts(prompt, typ)
    x = length_value(prompt, typ)
    return [[float(e) for e in p] for p in lengths_at(v, sp.Rational(x.numerator, x.denominator))]

# ------------------------------------------------------------------
# Solving (for draws and edits)
# ------------------------------------------------------------------
def answer_of(prompt, typ):
    if typ in ("1", "2", "3"):
        kind, arcs, _ = angle_data(prompt, typ)
        x = F(arcs["left"] + arcs["right"], 2) if kind == "inside" else F(arcs["far"] - arcs["near"], 2)
        return answer_text_of(x)
    return answer_text_of(length_value(prompt, typ))

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt, entry))

# ------------------------------------------------------------------
# Angle figures, in units of the radius: points placed on the circle by their arcs
# ------------------------------------------------------------------
def cpt(d):
    return (math.cos(math.radians(d)), math.sin(math.radians(d)))

def meet(p, u, q, w):
    """Where the line through p along u meets the line through q along w."""
    den = u[0] * w[1] - u[1] * w[0]
    if abs(den) < 1e-12:
        raise ValueError("parallel lines")
    s = ((q[0] - p[0]) * w[1] - (q[1] - p[1]) * w[0]) / den
    return (p[0] + s * u[0], p[1] + s * u[1])

def angle_at(v, p, q):
    """The angle at v between the rays toward p and q, in degrees."""
    a = math.atan2(p[1] - v[1], p[0] - v[0]) - math.atan2(q[1] - v[1], q[0] - v[0])
    a = abs(math.degrees(a)) % 360
    return min(a, 360 - a)

TILT = 0.2                            # how much the arcs that aren't intercepted differ, so no figure is symmetric

def inside_geometry(arcs):
    """Type 1, on the unit circle: the chords A-C and B-D cross at Xc; arc AB (right) and arc CD
    (left) are the intercepted arcs. Turned so the angle AXB's bisector is level, where the
    labels of x fit best. Returns the points (and in degrees) and the crossing."""
    a, b = arcs["right"], arcs["left"]
    rest = 360 - a - b
    A, B = a / 2, -a / 2
    D = A + rest / 2 * (1 + TILT)
    C = D + b
    deg = dict(A=A, B=B, C=C, D=D)
    for _ in range(2):                                # the second pass finds the turn level
        P = {k: cpt(d) for k, d in deg.items()}
        Xc = meet(P["A"], (P["C"][0] - P["A"][0], P["C"][1] - P["A"][1]),
                  P["B"], (P["D"][0] - P["B"][0], P["D"][1] - P["B"][1]))
        a1, a2 = (math.atan2(P[k][1] - Xc[1], P[k][0] - Xc[0]) for k in "AB")
        turn = -math.degrees(math.atan2(math.sin(a1) + math.sin(a2), math.cos(a1) + math.cos(a2)))
        deg = {k: d + turn for k, d in deg.items()}
    return dict(deg=deg, pts=P, X=Xc)

def outside_geometry(kind, arcs):
    """Types 2-3, on the unit circle, turned so the meeting point P is on the left and its angle
    opens to the right, its bisector level (where a label fits best in a narrow angle).
    rays: for each line, the point the ray from P runs toward (a secant's far point, or the
    tangent point), and its near point (None on a tangent). labels: arc name -> mid (degrees),
    span."""
    far, near = arcs["far"], arcs["near"]
    if kind == "secants":
        rest = 360 - far - near
        F1, F2 = far / 2, -far / 2
        N1 = F1 + rest / 2 * (1 + TILT)
        N2 = N1 + near
        lines = [(F1, N1), (F2, N2)]
        mids = dict(far=(0, far), near=(N1 + near / 2, near))
    elif kind == "tangent and secant":
        Fp, Tp = -far / 2, far / 2
        Np = Tp + near
        lines = [(Tp, None), (Fp, Np)]
        back = 360 - far - near
        mids = dict(far=(0, far), near=(Tp + near / 2, near), back=(Np + back / 2, back))
    else:
        T1, T2 = far / 2, -far / 2
        lines = [(T1, None), (T2, None)]
        mids = dict(far=(0, far), near=(180, near))

    def line_of(f, n):
        p = cpt(f)
        if n is None:
            return p, (-p[1], p[0])                   # the tangent at f
        q = cpt(n)
        return p, (q[0] - p[0], q[1] - p[1])
    (p1, u1), (p2, u2) = (line_of(*l) for l in lines)
    P = meet(p1, u1, p2, u2)
    a1, a2 = (math.atan2(cpt(f)[1] - P[1], cpt(f)[0] - P[0]) for f, _ in lines)
    turn = -math.degrees(math.atan2(math.sin(a1) + math.sin(a2), math.cos(a1) + math.cos(a2)))
    rays = [(f + turn, None if n is None else n + turn) for f, n in lines]
    c, s = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    return dict(P=(P[0] * c - P[1] * s, P[0] * s + P[1] * c), d=math.hypot(*P), rays=rays,
                mids={k: (m + turn, s_) for k, (m, s_) in mids.items()})

def measured_angle(prompt, typ):
    """The figure's angle x, measured from its points (no arc theorem)."""
    kind, arcs, _ = angle_data(prompt, typ)
    if kind == "inside":
        g = inside_geometry(arcs)
        return angle_at(g["X"], g["pts"]["A"], g["pts"]["B"])
    g = outside_geometry(kind, arcs)
    (f1, _), (f2, _) = g["rays"]
    return angle_at(g["P"], cpt(f1), cpt(f2))

# ------------------------------------------------------------------
# Checking
# ------------------------------------------------------------------
def check_problem(p):
    typ = p["type"]
    vals = read_answer(p["answer"], "x")
    if vals is None:
        return False
    x = vals["x"]
    if typ in ("1", "2", "3"):
        return x > 0 and abs(measured_angle(p["prompt"], typ) - float(x)) < 1e-6
    _, _, v, rel = length_parts(p["prompt"], typ)
    xs = sp.Rational(x.numerator, x.denominator)
    if rel.subs(X, xs) != 0 or not all(e > 0 for q in lengths_at(v, xs) for e in q):
        return False
    return length_solutions(v, rel) == [xs]          # no other positive length

def check(p):
    try:
        ok = check_problem(p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Figures: every coordinate in cm; lesson_figures.circled draws
# ------------------------------------------------------------------
R1 = 2.2                              # Type 1's circle
RMAX, RMIN = 1.7, 0.8                # an outside figure's circle, largest and smallest
WMAX = 7.2                            # an outside figure's width
BEHIND = 0.3                          # a line drawn past P
PAST = 0.45                           # a secant drawn past the circle; a tangent past its point: 0.7
MIN_SEG = 0.55                        # the shortest drawn part of a segment figure

def mirror(pt, pose):
    x, y = pt
    return (-x if pose & 1 else x, -y if pose & 2 else y)

def scaled(p, k):
    return (p[0] * k, p[1] * k)

def bisector_cands(v, p, q, stop, start=0.35, step=0.06):
    u1, u2 = L11.unit(v, p), L11.unit(v, q)
    b = (u1[0] + u2[0], u1[1] + u2[1])
    n = math.hypot(*b)
    b = (b[0] / n, b[1] / n)
    out, t = [], start
    while t <= stop or not out:                       # at least one, so a cramped angle is marked unclean
        out.append((v[0] + t * b[0], v[1] + t * b[1]))
        t += step
    return out

def arc_cands(mid, span, r, markup, inside_first=False):
    """Centers just outside (or inside) the circle of radius r about the origin, near an arc's
    middle, never past its ends."""
    w, h = L11.size(markup)
    outs, ins = [], []
    for da in (0, 6, -6, 12, -12, 18, -18, 25, -25):
        if abs(da) > span / 2 - 4 and da:
            continue
        u = cpt(mid + da)
        reach = abs(u[0]) * w / 2 + abs(u[1]) * h / 2
        for extra in (0, 0.12, 0.25):
            outs.append(((r + 0.1 + reach + extra) * u[0], (r + 0.1 + reach + extra) * u[1]))
        for extra in (0, 0.1):
            ins.append(((r - 0.1 - reach - extra) * u[0], (r - 0.1 - reach - extra) * u[1]))
    return ins + outs if inside_first else outs

def deg_label(t):
    return f"${t} degree$"

def angle_mark(v, placer):
    """The arc marking the angle at v, just inside its label (the last one placed)."""
    b = placer.taken[-1]
    return max(0.24, L11.rect_dist(v, b) - 0.08)

def fig_inside(prompt):
    kind, arcs, pose = angle_data(prompt, "1")
    g = inside_geometry(arcs)
    pts = {k: scaled(p, R1) for k, p in g["pts"].items()}
    Xc = scaled(g["X"], R1)
    chains = [[pts["A"], pts["C"]], [pts["B"], pts["D"]]]
    pl = L11.Placer(L11.segments_of(chains), [((0, 0), R1)], corners=[Xc])
    marks = []
    for p, q in (("A", "B"), ("C", "D")):
        stop = min(math.dist(Xc, pts[p]), math.dist(Xc, pts[q])) - 0.15
        pl.put(bisector_cands(Xc, pts[p], pts[q], stop), deg_label("x"))
        marks.append((Xc, pts[p], pts[q], angle_mark(Xc, pl)))
    d = g["deg"]
    left, right = split(prompt)[0][0]
    pl.put(arc_cands((d["C"] + d["D"]) / 2, arcs["left"], R1, deg_label(left)), deg_label(left))
    pl.put(arc_cands((d["A"] + d["B"]) / 2, arcs["right"], R1, deg_label(right)), deg_label(right))
    return finish((0, 0), R1, chains, marks, pl, pose)

def finish(center, r, chains, marks, pl, pose):
    m = lambda p: mirror(p, pose)
    chains = [[m(p) for p in c] for c in chains]
    marks = [(m(v), m(p), m(q), rr) for v, p, q, rr in marks]
    labels = [(*m((x, y)), t) for x, y, t in pl.labels]
    return (m(center), r, chains, marks, labels, []), pl.clean

def fig_outside(prompt, typ):
    kind, arcs, pose = angle_data(prompt, typ)
    g = outside_geometry(kind, arcs)
    k = min(RMAX, WMAX / (g["d"] + 1 + 0.5))
    if k < RMIN:
        raise ValueError("too far out to draw")
    P = scaled(g["P"], k)
    chains, ends = [], []
    for f, n in g["rays"]:
        end = scaled(cpt(f), k)
        u = L11.unit(P, end)
        past = PAST if n is not None else 0.7
        chains.append([(P[0] - BEHIND * u[0], P[1] - BEHIND * u[1]), (end[0] + past * u[0], end[1] + past * u[1])])
        ends.append(end)
    pl = L11.Placer(L11.segments_of(chains), [((0, 0), k)], corners=[P])
    gap = g["d"] * k - k                               # P to the circle
    pl.put(bisector_cands(P, ends[0], ends[1], gap), deg_label("x"))
    marks = [(P, ends[0], ends[1], angle_mark(P, pl))]
    given = dict(t.split() for t in split(prompt)[0][1])
    for name in ("far", "near", "back"):
        if name in given:
            mid, span = g["mids"][name]
            mk = deg_label(given[name])
            pl.put(arc_cands(mid, span, k, mk, inside_first=(name == "near")), mk)
    return finish((0, 0), k, chains, marks, pl, pose)

def secant_geometries(lens, tangent):
    """(R, d, phi1, phi2) in the parts' units: two secants (or a secant and a tangent) from
    P at the origin, the circle's center at (d, 0); line 1 runs up at phi1, line 2 down at
    phi2. Every circle that holds the longer chord, with the lines 24° to 70° apart, smallest
    circle first."""
    (e1, i1), second = lens
    pw = e1 * (e1 + i1)
    chords = [i1] if tangent else [i1, second[1]]
    out = []
    for f in (1.02, 1.08, 1.15, 1.25, 1.4, 1.6, 1.85, 2.2):
        R = max(chords) / 2 * f
        d = math.sqrt(pw + R * R)
        phi1 = math.asin(math.sqrt(R * R - i1 * i1 / 4) / d)
        phi2 = math.asin(R / d) if tangent else math.asin(math.sqrt(R * R - second[1] ** 2 / 4) / d)
        if 24 <= math.degrees(phi1 + phi2) <= 70:
            out.append((R, d, phi1, phi2))
    return out

def fig_segments(prompt, typ):
    parts, pose = split(prompt)
    lens = numeric_lengths(prompt, typ)
    tangent = typ == "7"
    geos = secant_geometries(lens, tangent)
    if not geos:
        raise ValueError("lines too close together to draw")
    first = None
    for geo in geos:
        got = segment_figure(parts, lens, pose, geo, tangent)
        if got is None:
            continue
        if got[1]:
            return got
        first = first or got
    if first is None:
        raise ValueError("parts too short to draw")
    return first

def segment_figure(parts, lens, pose, geo, tangent):
    R, d, phi1, phi2 = geo
    (e1, i1), second = lens
    span = d + R
    k = min(WMAX / span, RMAX * 1.3 / R)
    if min([e1, i1] + list(second)) * k < MIN_SEG:
        return None
    O = (d * k, 0.0)
    P = (0.0, 0.0)
    u1 = (math.cos(phi1), math.sin(phi1))
    u2 = (math.cos(phi2), -math.sin(phi2))
    N1, F1 = scaled(u1, e1 * k), scaled(u1, (e1 + i1) * k)
    if tangent:
        T = scaled(u2, second[0] * k)
        chains = [[P, F1], [P, T]]
        pieces = [(P, N1, parts[0][0]), (N1, F1, parts[0][1]), (P, T, parts[1][0])]
    else:
        e2, i2 = second
        N2, F2 = scaled(u2, e2 * k), scaled(u2, (e2 + i2) * k)
        chains = [[P, F1], [P, F2]]
        pieces = [(P, N1, parts[0][0]), (N1, F1, parts[0][1]), (P, N2, parts[1][0]), (N2, F2, parts[1][1])]
    pl = L11.Placer(L11.segments_of(chains), [(O, R * k)])
    for a, b, t in pieces:                          # an external part labeled outside the angle, an
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)  # internal one inside the circle, as the book does
        away = O if a == P else (2 * m[0] - O[0], 2 * m[1] - O[1])
        pl.put(L11.side_cands(a, b, f"${t}$", inside=away), f"${t}$")
    shift = (-O[0], 0.0)                               # the circle at the origin
    mv = lambda p: (p[0] + shift[0], p[1] + shift[1])
    chains = [[mv(p) for p in c] for c in chains]
    pl.labels = [(x + shift[0], y + shift[1], t) for x, y, t in pl.labels]
    return finish((0, 0), R * k, chains, [], pl, pose)

def fig_parts(typ, prompt):
    if typ == "1":
        return fig_inside(prompt)
    if typ in ("2", "3"):
        return fig_outside(prompt, typ)
    if typ == "4":
        return L11.fig4_parts(prompt)
    return fig_segments(prompt, typ)

def drawable(typ, prompt):
    """Does the figure place every label cleanly? (False if it can't be drawn at all.)"""
    try:
        return fig_parts(typ, prompt)[1]
    except (ValueError, ZeroDivisionError):
        return False

def figure(p, unit_="1cm"):
    center, r, chains, arcs, labels, leaders = fig_parts(p["type"], p["prompt"])[0]
    return fig.circled(center, r, chains, arcs=arcs, labels=labels, leaders=leaders, unit=unit_)

# ------------------------------------------------------------------
# Showing: each problem says what to do (EXTENDING.md 3.10)
# ------------------------------------------------------------------
def statement(p):
    return "Find $x$."

def typst(p, gap="0.3em"):
    try:
        f = figure(p)
    except Exception:
        return f"{statement(p)} #h(0.5em) [{plain(p['prompt'])}]"   # an edit that makes no figure; check() marks it
    return f"{statement(p)} #v(0.4em) #align(center)[{f}]"

def answer_typst(p):
    return f"${dfrac(p['answer'])}$"

SLIDE_UNIT = "1.9cm"

def slide_typst(p, key=False):
    """The words (and the answer, hidden on the question slide) beside the figure drawn
    larger; the figure never moves."""
    try:
        f = figure(p, SLIDE_UNIT)
    except Exception:
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return (f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, "
            f"[{statement(p)} #v(0.8em) {shown}], [{f}])")

def text(p):
    return f"Find x.   [figure: {p['prompt']}]"

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 1.9

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
EXAMPLE = {
    "1": "30, 70; pose 0", "2": "secants; far 80, near 30; pose 0",
    "3": "tangent and secant; far 170, back 120; pose 0", "4": "30, x + 20; 40, x + 10; pose 0",
    "5": "5, 7; 6, x; pose 0", "6": "3, x; x, 3; pose 0", "7": "x, 12; 8; pose 0",
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
        figure(dict(old, type=typ, prompt=t))
    except Exception:
        raise ValueError(f"write it like {EXAMPLE[typ]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
