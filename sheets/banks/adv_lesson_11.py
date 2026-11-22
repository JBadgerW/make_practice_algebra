"""Lesson 11 (Advanced Math): circles (properties of circles), the quadratic
formula. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_011/slides/deck_011.typ): examples
11.1-11.6 and Problem Set 11, problems 5-7, 9, and 10.

    1  equal inscribed angles:        46°, (x + 10)°; 30°, (y + 20)°            x = 36, y = 10
    2  an inscribed quadrilateral:    angles 75°, 80°, x°, y°; arcs 50°, z°     x = 100, y = 105, z = 110
    3  an inscribed triangle:         angles 35°, 75°; arcs x°, y°, z°         x = 150, y = 70, z = 140
    4  intersecting chords:           15 and x + 10; 20 and x + 5              x = 10
    5  tangent segments:              x + 4, 6; x + y, 10; x, x                x = 2, y = 8
    6  the quadratic formula:         3 x^2 - 2 x + 5 = 0                       x = 1/3 plus.minus sqrt(14)/3 i

The problem types file puts examples 11.1-11.3 under one heading; they are
Types 1-3 here, because each has its own figure and its own move: angles that
intercept the same arc are equal (11.1, problem 5); opposite angles of an
inscribed quadrilateral sum to 180° and an arc is twice the inscribed angle
(11.2); the three arcs of an inscribed triangle are twice the opposite angles
(11.3). Types 2 and 3 have no Problem Set item.

Every figure is drawn from the problem's data with its unknowns solved first,
so it is true: the angles and arcs are the real ones, the chords cut each
other in the given lengths, and the circle is the triangle's incircle. (The
book's figures are not to scale: problem 7's triangle is drawn right-angled,
but its tangent lengths 7, 19, 4 make an angle of about 93°.) A figure turns
one of four ways (its pose), or for chords one of eight.

The key writes what the deck writes: each unknown as letter = value, in
alphabetical order (the deck's 11.1 gives y first; here x first, as Lesson
3 does), with no degree sign: x = 36, y = 10. Type 6 writes its roots as
Lesson 10 does (the deck's own forms): x = 4/3 or x = -1, the larger first;
x = -1/3 plus.minus sqrt(14)/3 i. Its letter is drawn at random, as in
Lesson 10.

check() works from the prompt's data, not from how it was built: the answer's
values are put into the lesson's facts. Type 1: each pair of angles that
intercept one arc is equal. Type 2: opposite angles sum to 180, and z plus the
given arc is twice the angle across from them; every arc is positive. Type 3:
x and y are twice the angles across from them, and x + y + z = 360. Type 4:
the products of the chords' parts are equal, each part positive. Type 5: the
two tangent segments from each vertex are equal, each positive. Type 6:
Lesson 10's check, each root put back into the equation. Every value is a
whole number or a fraction in lowest terms, and the letters are exactly the
problem's, in order.

Skipped sources: problem 8, "Begin with ax^2 + bx + c = 0 and derive the
quadratic formula." It is a derivation (a proof), with nothing to draw.

A problem: dict(type, prompt, answer, source). The prompt is the figure's data,
and it is what an edit changes; "pose k" turns the figure.
    1  "46, x + 10; 30, y + 20; pose 0"    two pairs of angles, each pair on one arc
    2  "75, 80; 50; pose 0"                the angles across from y and from x, then the arc beside z
    3  "35, 75; pose 0"                    the angles across from arcs y and x
    4  "15, x + 10; 20, x + 5; pose 0"     each chord's two parts
    5  "x + 4, 6; x + y, 10; x, x; pose 0" each vertex's two tangent segments
    6  "3 x^2 - 2 x + 5 = 0"
"""
import math, re
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need, written
from ..check import to_sympy
from ..typmath import display, dfrac, text as plain
from ..graphs import clip
from . import lesson_figures as fig
from . import adv_lesson_10 as L10

NAME = FAMILY = "adv_lesson_11"
FIXED = False
TITLE = "Lesson 11: Circles, Properties of Circles, The Quadratic Formula"
INSTRUCTIONS = ""              # each type has its own; a sheet of one type shows it at the top
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

TYPES = [
    dict(key="1", title="Inscribed Angles on the Same Arc", instructions="Find x and y.",
         look="Two chords crossing inside a circle, and four inscribed angles at their ends.",
         move="Angles that intercept the same arc are equal. Pair each angle with the one across the figure "
              "on the same arc: $y + 20 = 30$, so $y = 10$."),
    dict(key="2", title="An Inscribed Quadrilateral", instructions="Find x, y, and z.",
         look="A quadrilateral inscribed in a circle, with two of its angles and an arc given.",
         move="Opposite angles of an inscribed quadrilateral sum to $180 degree$: $x + 80 = 180$. An intercepted "
              "arc is twice the inscribed angle: $z + 50 = 2 times 80$."),
    dict(key="3", title="An Inscribed Triangle", instructions="Find x, y, and z.",
         look="A triangle inscribed in a circle, with two of its angles given and its three arcs unknown.",
         move="Each arc is twice the inscribed angle across from it: $x = 2 times 75 = 150$. The third arc is "
              "the rest of the circle: $z = 360 - x - y$."),
    dict(key="4", title="Intersecting Chords", instructions="Find x.",
         look="Two chords crossing inside a circle, each cut into two parts.",
         move="The products of the parts of the two chords are equal: $20(x + 5) = 15(x + 10)$. Multiply out and "
              "solve."),
    dict(key="5", title="Tangent Segments to an Inscribed Circle", instructions="Find x and y.",
         look="A circle inscribed in a triangle, tangent to its three sides; the tangent segments are labeled.",
         move="The two tangent segments from a point outside a circle are equal. Start at the vertex with one "
              "letter: $x + 4 = 6$. Then use $x$ at the other: $x + y = 10$."),
    dict(key="6", title="The Quadratic Formula", instructions="Use the quadratic formula to solve.",
         look="A quadratic equation.",
         move="Write it as $a x^2 + b x + c = 0$. Then $x = (-b plus.minus sqrt(b^2 - 4 a c))/(2 a)$. Simplify the "
              "radical; a negative under it gives $i$.", space="1.75in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

FIGURES = ("1", "2", "3", "4", "5")
LETTERS = {"1": "xy", "2": "xyz", "3": "xyz", "4": "x", "5": "xy"}
SYM = {v: sp.Symbol(v) for v in "xyz"}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], re.sub(r"; pose \d+$", "", p["prompt"]))   # the same numbers turned is no new problem

# ------------------------------------------------------------------
# Reading a prompt
# ------------------------------------------------------------------
POSE = re.compile(r";\s*pose\s+(\d+)\s*$")

def split(prompt):
    """([[item, ...], ...], pose) from "46, x + 10; 30, y + 20; pose 0"."""
    t = " ".join(prompt.replace("−", "-").split())
    m = POSE.search(t)
    pose = int(m.group(1)) if m else 0
    t = POSE.sub("", t) if m else t
    return [[i.strip() for i in part.split(",")] for part in t.split(";")], pose

def value(t):
    """A label: a number (Fraction) or an expression in x, y, z (sympy)."""
    e = to_sympy(t)
    if e.free_symbols - set(SYM.values()):
        raise ValueError("only x, y, and z")
    return F(int(e.p), int(e.q)) if e.is_Rational else e

def number(t):
    v = value(t)
    if not isinstance(v, F):
        raise ValueError("a number")
    return v

def solve(eqs, letters):
    """{letter: Fraction}: the one solution of the equations (sympy expressions, each = 0)."""
    syms = [SYM[v] for v in letters]
    sol = sp.solve(eqs, syms, dict=True)
    if len(sol) != 1 or set(sol[0]) != set(syms) or not all(sol[0][s].is_Rational for s in syms):
        raise ValueError("no single solution")
    return {v: F(int(sol[0][SYM[v]].p), int(sol[0][SYM[v]].q)) for v in letters}

def written_values(vals):
    return ", ".join(f"{v} = {vals[v]}" for v in sorted(vals))

ANSWER_PART = re.compile(r"([a-z]) = (-?\d+(?:/\d+)?)")

def read_answer(ans, letters):
    """{letter: Fraction} from "x = 36, y = 10", the letters exactly these, in order, each
    value whole or a fraction in lowest terms; None if it isn't."""
    parts = [s.strip() for s in " ".join(ans.split()).split(",")]
    got = [ANSWER_PART.fullmatch(s) for s in parts]
    if not all(got) or [g.group(1) for g in got] != list(letters):
        return None
    out = {}
    for g in got:
        v = F(g.group(2))
        if str(v) != g.group(2):
            return None                                       # 4/2, or 3/1
        out[g.group(1)] = v
    return out

# ------------------------------------------------------------------
# Type 1: two pairs of equal inscribed angles (example 11.1, problem 5)
# ------------------------------------------------------------------
ANGLE1 = range(30, 71)                # a known angle
SHIFT1 = range(5, 26)                 # c in (x + c)°
ORDERS = ("known first", "letter first")
POSES = range(4)

def t1_ok(k1, c1, k2, c2, l1, o1, o2, pose):
    return (k1 in ANGLE1 and k2 in ANGLE1 and c1 in SHIFT1 and c2 in SHIFT1 and k1 - c1 >= 5 and k2 - c2 >= 5
            and k1 + k2 <= 120 and l1 in ("x", "y") and o1 in ORDERS and o2 in ORDERS and pose in POSES)

def t1_pick(r):
    return dict(k1=r.choice(ANGLE1), c1=r.choice(SHIFT1), k2=r.choice(ANGLE1), c2=r.choice(SHIFT1),
                l1=r.choice("xy"), o1=r.choice(ORDERS), o2=r.choice(ORDERS), pose=r.choice(POSES))

def pair(k, expr, order):
    return f"{k}, {expr}" if order == "known first" else f"{expr}, {k}"

def t1(k1, c1, k2, c2, l1, o1, o2, pose):
    need(t1_ok(k1, c1, k2, c2, l1, o1, o2, pose))
    l2 = "y" if l1 == "x" else "x"
    prompt = f"{pair(k1, f'{l1} + {c1}', o1)}; {pair(k2, f'{l2} + {c2}', o2)}; pose {pose}"
    need(drawable("1", prompt))
    return prompt

def t1_data(prompt):
    """((a1, a2), (b1, b2), pose, alpha, beta): the two pairs' labels and their angles in degrees."""
    parts, pose = split(prompt)
    if len(parts) != 2 or any(len(p) != 2 for p in parts):
        raise ValueError("two pairs of angles")
    vals = solve([value(a) - value(b) for a, b in parts], "xy")
    alpha, beta = (float(sp.sympify(value(p[0])).subs({SYM[v]: vals[v] for v in vals})) for p in parts)
    if not (0 < alpha and 0 < beta and alpha + beta < 180):
        raise ValueError("not a figure")
    return parts, pose, alpha, beta, vals

# ------------------------------------------------------------------
# Type 2: an inscribed quadrilateral (example 11.2)
# ------------------------------------------------------------------
ANGLE2 = range(50, 115, 5)            # the two given angles
ARC2 = range(40, 130, 10)             # the given arc
MIN_ARC = 40

def quad_arcs(v1, v4, a2):
    """The four arcs: top (z), right (given), bottom, left."""
    a1, a3 = 2 * v4 - a2, 2 * v1 - a2
    return a1, a2, a3, 360 - a1 - a2 - a3

def t2_ok(v1, v4, a2, pose):
    if not (v1 in ANGLE2 and v4 in ANGLE2 and a2 in ARC2 and pose in POSES):
        return False
    return min(quad_arcs(v1, v4, a2)) >= MIN_ARC and v1 != v4

def t2_pick(r):
    return dict(v1=r.choice(ANGLE2), v4=r.choice(ANGLE2), a2=r.choice(ARC2), pose=r.choice(POSES))

def t2(v1, v4, a2, pose):
    need(t2_ok(v1, v4, a2, pose))
    prompt = f"{v1}, {v4}; {a2}; pose {pose}"
    need(drawable("2", prompt))
    return prompt

def t2_data(prompt):
    parts, pose = split(prompt)
    if [len(p) for p in parts] != [2, 1]:
        raise ValueError("two angles and an arc")
    v1, v4 = (number(t) for t in parts[0])
    a2 = number(parts[1][0])
    arcs = quad_arcs(v1, v4, a2)
    if min(arcs) <= 0:
        raise ValueError("not a figure")
    return v1, v4, a2, pose, arcs

# ------------------------------------------------------------------
# Type 3: an inscribed triangle (example 11.3)
# ------------------------------------------------------------------
ANGLE3 = range(30, 90, 5)

def t3_ok(a, b, pose):
    return a in ANGLE3 and b in ANGLE3 and 180 - a - b >= 30 and a != b and pose in POSES

def t3_pick(r):
    return dict(a=r.choice(ANGLE3), b=r.choice(ANGLE3), pose=r.choice(POSES))

def t3(a, b, pose):
    need(t3_ok(a, b, pose))
    prompt = f"{a}, {b}; pose {pose}"
    need(drawable("3", prompt))
    return prompt

def t3_data(prompt):
    parts, pose = split(prompt)
    if [len(p) for p in parts] != [2]:
        raise ValueError("two angles")
    a, b = (number(t) for t in parts[0])
    if not (a > 0 and b > 0 and a + b < 180):
        raise ValueError("not a triangle")
    return a, b, pose

# ------------------------------------------------------------------
# Type 4: intersecting chords (example 11.4, problem 6)
# ------------------------------------------------------------------
PART4 = range(4, 31)                  # a part that is a number
SHIFT4 = range(1, 21)                 # k in x + k
X4 = range(2, 16)                     # the answer
POSES4 = range(8)
MIN_CROSS = 35                        # degrees between the chords, drawn
MIN_PART = 0.7                        # cm: the shortest part of a chord, drawn

def t4_ok(n1, k1, n2, k2, o1, o2, pose):
    if not (n1 in PART4 and n2 in PART4 and k1 in SHIFT4 and k2 in SHIFT4 and n1 != n2
            and o1 in ORDERS and o2 in ORDERS and pose in POSES4):
        return False
    x = F(n2 * k2 - n1 * k1, n1 - n2)
    return x.denominator == 1 and x in X4

def t4_pick(r):
    x, n1, n2, k1 = r.choice(X4), r.choice(PART4), r.choice(PART4), r.choice(SHIFT4)
    need(n1 != n2 and (n1 * (x + k1)) % n2 == 0)
    return dict(n1=n1, k1=k1, n2=n2, k2=n1 * (x + k1) // n2 - x, o1=r.choice(ORDERS), o2=r.choice(ORDERS),
                pose=r.choice(POSES4))

def t4(n1, k1, n2, k2, o1, o2, pose):
    need(t4_ok(n1, k1, n2, k2, o1, o2, pose))
    prompt = f"{pair(n1, f'x + {k1}', o1)}; {pair(n2, f'x + {k2}', o2)}; pose {pose}"
    need(drawable("4", prompt))
    return prompt

def t4_data(prompt):
    """(parts, (p1, q1, p2, q2) lengths, pose, x)."""
    parts, pose = split(prompt)
    if len(parts) != 2 or any(len(p) != 2 for p in parts):
        raise ValueError("two chords, two parts each")
    (a, b), (c, d) = ([value(t) for t in p] for p in parts)
    vals = solve([sp.sympify(a) * b - sp.sympify(c) * d], "x")
    at = {SYM["x"]: vals["x"]}
    lengths = tuple(float(sp.sympify(t).subs(at)) for t in (a, b, c, d))
    if min(lengths) <= 0:
        raise ValueError("a part that isn't positive")
    return parts, lengths, pose, vals

# ------------------------------------------------------------------
# Type 5: tangent segments to an inscribed circle (example 11.5, problem 7)
# ------------------------------------------------------------------
N1 = range(5, 16)                     # the number at the vertex with x + a
N2 = range(6, 26)                     # the number at the vertex with x + y

def t5_ok(a, n1, n2, f1, f2, pose):
    if not (n1 in N1 and n2 in N2 and 1 <= a <= n1 - 2 and f1 in (0, 1) and f2 in (0, 1) and pose in POSES):
        return False
    x = n1 - a
    return n2 - x >= 2 and triangle_ok(n1, n2, x)

def t5_pick(r):
    n1 = r.choice(N1)
    return dict(a=r.randint(1, n1 - 2), n1=n1, n2=r.choice(N2), f1=r.choice((0, 1)), f2=r.choice((0, 1)),
                pose=r.choice(POSES))

def t5(a, n1, n2, f1, f2, pose):
    need(t5_ok(a, n1, n2, f1, f2, pose))
    v1 = [f"x + {a}", str(n1)]
    v2 = ["x + y", str(n2)]
    if f1:
        v1.reverse()
    if f2:
        v2.reverse()
    prompt = f"{', '.join(v1)}; {', '.join(v2)}; x, x; pose {pose}"
    need(drawable("5", prompt))
    return prompt

def t5_data(prompt):
    """(parts, (t1, t2, t3) tangent lengths, pose, values)."""
    parts, pose = split(prompt)
    if len(parts) != 3 or any(len(p) != 2 for p in parts):
        raise ValueError("three vertices, two tangent segments each")
    vs = [[value(t) for t in p] for p in parts]
    eqs = [sp.sympify(a) - b for a, b in vs]
    letters = "".join(sorted({str(s) for v in vs for t in v for s in sp.sympify(t).free_symbols}))
    vals = solve([e for e in eqs if e != 0], letters)
    at = {SYM[v]: vals[v] for v in vals}
    ts = tuple(float(sp.sympify(p[0]).subs(at)) for p in vs)
    if min(ts) <= 0:
        raise ValueError("a segment that isn't positive")
    return parts, ts, pose, vals

def triangle_angles(t1, t2, t3):
    """The angles (degrees) at the vertices with tangent lengths t1, t2, t3."""
    a, b, c = t2 + t3, t1 + t3, t1 + t2           # sides across from vertices 1, 2, 3
    ang = lambda opp, s1, s2: math.degrees(math.acos((s1 * s1 + s2 * s2 - opp * opp) / (2 * s1 * s2)))
    return ang(a, b, c), ang(b, a, c), ang(c, a, b)

def triangle_ok(t1, t2, t3):
    angs = triangle_angles(t1, t2, t3)
    return min(angs) >= 22 and max(angs) <= 120     # problem 7 has 25.0°

# ------------------------------------------------------------------
# Type 6: the quadratic formula (example 11.6, problems 9-10)
# ------------------------------------------------------------------
A6 = range(1, 7)
B6 = range(1, 10)
C6 = range(1, 13)
MAX_DISC = 250

def t6_ok(v, a, b, c):
    D = b * b - 4 * a * c
    return (v in gen.LETTERS and a in A6 and abs(b) in B6 and abs(c) in C6 and D != 0 and abs(D) <= MAX_DISC
            and math.gcd(math.gcd(a, abs(b)), abs(c)) == 1)

def t6_pick(r):
    return dict(v=r.choice(gen.LETTERS), a=r.choice((1, 2, 2, 3, 3, 4, 5, 6)), b=gen.signed(r, 1, 9),
                c=gen.signed(r, 1, 12))

def t6_moved_pick(r):
    d = t6_pick(r)
    d["s"] = r.choice((1, -1))
    return d

def t6(v, a, b, c):                   # 11.6, problem 9: 3 x^2 - 2 x + 5 = 0
    need(t6_ok(v, a, b, c))
    return f"{written((a, f'{v}^2'), (b, v), (c, ''))} = 0"

def t6_moved(v, a, b, c, s):          # problem 10: -x = -3 x^2 + 4, the x term alone on the left
    need(t6_ok(v, a, b, c) and s in (1, -1))
    return f"{written((-s * b, v))} = {written((s * a, f'{v}^2'), (s * c, ''))}"

# ------------------------------------------------------------------
# The templates
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick, t1)],
    "2": [(t2_pick, t2)],
    "3": [(t3_pick, t3)],
    "4": [(t4_pick, t4)],
    "5": [(t5_pick, t5)],
    "6": [(t6_pick, t6), (t6_moved_pick, t6_moved)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3: t3_ok, t4: t4_ok, t5: t5_ok, t6: t6_ok,
          t6_moved: lambda s, **p: t6_ok(**p) and s in (1, -1)}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# Solving (for draws and edits)
# ------------------------------------------------------------------
def answer_of(prompt, typ):
    if typ == "1":
        return written_values(t1_data(prompt)[4])
    if typ == "2":
        v1, v4, a2, _, arcs = t2_data(prompt)
        return written_values(dict(x=180 - v4, y=180 - v1, z=arcs[0]))
    if typ == "3":
        a, b, _ = t3_data(prompt)
        return written_values(dict(x=2 * b, y=2 * a, z=360 - 2 * a - 2 * b))
    if typ == "4":
        return written_values(t4_data(prompt)[3])
    if typ == "5":
        return written_values(t5_data(prompt)[3])
    return L10.square_answer(*L10.quadratic(prompt))

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt, entry))

# ------------------------------------------------------------------
# Checking: the answer's values put into the lesson's facts
# ------------------------------------------------------------------
def at(t, vals):
    return sp.sympify(value(t)).subs({SYM[v]: vals[v] for v in vals})

def check_figure(p):
    typ = p["type"]
    vals = read_answer(p["answer"], LETTERS[typ])
    if vals is None:
        return False
    parts, _ = split(p["prompt"])
    if typ == "1":                                  # angles on the same arc are equal
        angles = [[at(t, vals) for t in pr] for pr in parts]
        return (len(parts) == 2 and all(a == b and a > 0 for a, b in angles)
                and angles[0][0] + angles[1][0] < 180)
    if typ == "2":
        v1, v4 = (number(t) for t in parts[0])
        a2 = number(parts[1][0])
        x, y, z = vals["x"], vals["y"], vals["z"]
        a3 = 2 * v1 - a2                            # the arc the given angle at V1 takes, beyond a2
        return (x + v4 == 180 and y + v1 == 180 and z + a2 == 2 * v4
                and min(z, a2, a3, 360 - z - a2 - a3) > 0)
    if typ == "3":
        a, b = (number(t) for t in parts[0])
        return vals["x"] == 2 * b and vals["y"] == 2 * a and sum(vals.values()) == 360 and a + b < 180
    if typ == "4":                                  # the products of the parts are equal
        (a, b), (c, d) = ([at(t, vals) for t in pr] for pr in parts)
        return a * b == c * d and min(a, b, c, d) > 0
    segs = [[at(t, vals) for t in pr] for pr in parts]   # Type 5: tangent segments from a vertex are equal
    return len(segs) == 3 and all(a == b and a > 0 for a, b in segs)

def check(p):
    try:
        if p["type"] == "6":
            ok = L10.check_square(p)
        else:
            ok = check_figure(p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Figures: every coordinate in cm, worked out here; lesson_figures.circled draws
# ------------------------------------------------------------------
RC = 1.9                              # the circle's radius in Types 1-3
RC4 = 2.2                             # and in Type 4, where a short part must hold its label
TEXT_H = 0.46                         # a label's height (cm, 12 pt, with its padding)
# widths (cm) of what a label is made of, set in 12 pt math, measured in Typst
WIDTH = {"digit": 0.21, "letter": 0.24, "op": 0.52, "paren": 0.15, "degree": 0.19}
PAD = 0.2                             # the label's padding, both sides, and a margin

def on_circle(deg, r=RC):
    return (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))

def turn(pts, pose, quarter=True):
    """Turn and mirror points about the origin: pose 0-3 (a quarter turn, then a mirror),
    or with quarter=False pose 0-7 (eighth turns)."""
    if quarter:
        ang, mirror = (-90 if pose % 2 else 0), pose >= 2
    else:
        ang, mirror = 45 * pose, False
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    out = []
    for x, y in pts:
        x, y = x * c - y * s, x * s + y * c
        out.append((-x, y) if mirror else (x, y))
    return out

def unit(p, q):
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    return ((q[0] - p[0]) / L, (q[1] - p[1]) / L)

def deg(t):
    """A label in degrees: 46°, (x + 10)°."""
    t = t.strip()
    return f"${t} degree$" if re.fullmatch(r"[\w.]+", t) else f"$({t}) degree$"

def size(markup):
    """A label's (width, height) in cm: the widths of its pieces as set, and its padding."""
    t = markup.replace("$", "")
    w = WIDTH["degree"] * t.count("degree")
    t = t.replace("degree", "")
    w += WIDTH["op"] * len(re.findall(r"[+-]", t)) + WIDTH["paren"] * len(re.findall(r"[()]", t))
    w += WIDTH["digit"] * len(re.findall(r"\d", t)) + WIDTH["letter"] * len(re.findall(r"[a-z]", t))
    return w + PAD, TEXT_H

def rect(c, wh):
    return (c[0] - wh[0] / 2, c[0] + wh[0] / 2, c[1] - wh[1] / 2, c[1] + wh[1] / 2)

def rect_dist(pt, b):
    dx = max(b[0] - pt[0], 0, pt[0] - b[1])
    dy = max(b[2] - pt[1], 0, pt[1] - b[3])
    return math.hypot(dx, dy)

def crosses_circle(b, center, r):
    near = rect_dist(center, b)
    far = max(math.dist(center, (x, y)) for x in b[:2] for y in b[2:])
    return near < r < far

def overlap(a, b, pad=0.06):
    return not (a[1] + pad <= b[0] or b[1] + pad <= a[0] or a[3] + pad <= b[2] or b[3] + pad <= a[2])

class Placer:
    """Labels set one by one, each at the first of its candidate centers whose box crosses no
    line, no circle, no other label, and no angle's arc; `clean` stays True while every
    label finds such a place (else the best one is taken, and the draw is redrawn)."""
    def __init__(self, segments, circles, corners=()):
        self.segments, self.circles, self.corners = segments, circles, corners
        self.taken, self.labels, self.leaders, self.clean = [], [], [], True

    def put(self, cands, markup):
        """cands: centers, or (center, target) for a label set off with a leader to target."""
        wh, best = size(markup), None
        for i, c in enumerate(cands):
            c, target = c if isinstance(c[0], tuple) else (c, None)
            b = rect(c, wh)
            bad = (sum(clip(p, q, b) is not None for p, q in self.segments)
                   + sum(crosses_circle(b, o, r) for o, r in self.circles)
                   + sum(overlap(b, t) for t in self.taken)
                   + sum(rect_dist(v, b) < 0.32 for v in self.corners))
            if best is None or (bad, i) < best[0]:
                best = ((bad, i), c, b, target)
            if bad == 0:
                break
        (bad, _), c, b, target = best
        self.clean = self.clean and bad == 0
        self.taken.append(b)
        self.labels.append((c[0], c[1], markup))
        if target is not None:
            self.leaders.append((edge_toward(c, wh, target), target))

def edge_toward(c, wh, target):
    """Where the line from a label's center toward target leaves the label's box."""
    dx, dy = target[0] - c[0], target[1] - c[1]
    t = min(wh[0] / 2 / abs(dx) if dx else 9e9, wh[1] / 2 / abs(dy) if dy else 9e9) + 0.04 / math.hypot(dx, dy)
    return (c[0] + t * dx, c[1] + t * dy)

def along(v, d, dists):
    return [(v[0] + t * d[0], v[1] + t * d[1]) for t in dists]

def angle_cands(v, p, q, markup, center=(0, 0), r=RC):
    """Centers along the bisector of the angle at v, near to far; then, as the book sets a long
    label, outside the circle beside v, a leader to the angle's arc."""
    u1, u2 = unit(v, p), unit(v, q)
    b = (u1[0] + u2[0], u1[1] + u2[1])
    n = math.hypot(*b)
    b = (b[0] / n, b[1] / n)
    inside = along(v, b, [0.3 + 0.07 * i for i in range(14)])
    w, h = size(markup)
    target = (v[0] + 0.24 * b[0], v[1] + 0.24 * b[1])
    a0 = math.degrees(math.atan2(v[1] - center[1], v[0] - center[0]))
    outside = []
    for da in (0, 12, -12, 24, -24, 36, -36):
        a = math.radians(a0 + da)
        out = (math.cos(a), math.sin(a))
        off = r + 0.12 + abs(out[0]) * w / 2 + abs(out[1]) * h / 2
        for extra in (0, 0.15):
            outside.append(((center[0] + (off + extra) * out[0], center[1] + (off + extra) * out[1]), target))
    return inside + outside

def arc_cands(mid, center=(0, 0), r=RC):
    """Centers outside the circle near an arc's middle (degrees, before any turn)."""
    return [on_circle(mid + da, r + dr) for dr in (0.32, 0.45, 0.6) for da in (0, 7, -7, 14, -14)]

def side_cands(a, b, markup, inside=None):
    """Centers beside segment a-b, set off just past the label's own half-size; the side away
    from `inside` first, when given."""
    w, h = size(markup)
    u = unit(a, b)
    n = (-u[1], u[0])
    off = 0.07 + abs(n[0]) * w / 2 + abs(n[1]) * h / 2
    sides = (1, -1)
    if inside is not None:
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if (inside[0] - m[0]) * n[0] + (inside[1] - m[1]) * n[1] > 0:
            sides = (-1, 1)
    out = []
    for s in sides:
        for t in (0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.8):
            for extra in (0, 0.1, 0.2, 0.3):
                m = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
                out.append((m[0] + s * (off + extra) * n[0], m[1] + s * (off + extra) * n[1]))
    return out

def segments_of(chains):
    return [(c[i], c[i + 1]) for c in chains for i in range(len(c) - 1)]

def inscribed(pts_deg, chain_idx, corners, arcs_lab, pose):
    """Types 1-3: points on the circle at degrees, the chain through them (indices), corners:
    (vertex, p, q, text) by index, arcs_lab: (mid degree, text). Returns (figure args, clean)."""
    pts = turn([on_circle(a) for a in pts_deg], pose)
    chain = [pts[i] for i in chain_idx]
    pl = Placer(segments_of([chain]), [((0, 0), RC)], corners=[pts[v] for v, _, _, _ in corners])
    for v, p, q, t in corners:
        pl.put(angle_cands(pts[v], pts[p], pts[q], deg(t)), deg(t))
    for mid, t in arcs_lab:
        pl.put(turn(arc_cands(mid), pose), deg(t))
    return ((0, 0), RC, [chain], [(pts[v], pts[p], pts[q]) for v, p, q, _ in corners], pl.labels, pl.leaders), pl.clean

def fig1_parts(prompt):
    parts, pose, alpha, beta, _ = t1_data(prompt)
    rest = 180 - alpha - beta                     # the top arc, and the bottom
    P, A = 90 + rest / 2, 90 - rest / 2
    B = A - 2 * alpha                             # arc AB = 2 alpha, intercepted at P and R
    R_ = B - rest                                 # arc RP = 2 beta, intercepted at A and B
    corners = [(0, 1, 2, parts[0][0]), (3, 1, 2, parts[0][1]), (1, 0, 3, parts[1][0]), (2, 0, 3, parts[1][1])]
    return inscribed((P, A, B, R_), (1, 0, 2, 3, 1), corners, (), pose)

def fig2_parts(prompt):
    v1, v4, a2, pose, arcs = t2_data(prompt)
    a1, _, a3, _ = (float(a) for a in arcs)
    V1, V2 = 90 + a1 / 2, 90 - a1 / 2
    V3 = V2 - float(a2)
    V4 = V3 - a3
    texts = split(prompt)[0]
    corners = [(0, 1, 3, texts[0][0]), (1, 0, 2, "x"), (2, 1, 3, "y"), (3, 2, 0, texts[0][1])]
    return inscribed((V1, V2, V3, V4), (0, 1, 2, 3, 0), corners, ((90, "z"), (V2 - float(a2) / 2, texts[1][0])), pose)

def fig3_parts(prompt):
    a, b, pose = t3_data(prompt)
    ta, tb = split(prompt)[0][0]
    a, b = float(a), float(b)
    Tt = 90.0
    Rt = Tt - 2 * b                               # arc x, across from the angle b at L
    L = Rt - 2 * a                                # arc y, across from the angle a at T
    arcs = (((Tt + Rt) / 2, "x"), ((Rt + L) / 2, "y"), ((L + Tt - 360) / 2, "z"))
    return inscribed((Tt, Rt, L), (0, 1, 2, 0), [(0, 2, 1, ta), (2, 0, 1, tb)], arcs, pose)

def chord_geometries(p1, q1, p2, q2):
    """Two chords through X (the origin) in a circle: chord i runs p_i along u_i and q_i back.
    Every (center, R, u1, u2), in the parts' own units, whose chords cross at MIN_CROSS degrees
    or more, the smallest circle first (its short parts drawn longest, the crossing nearest the
    middle), then the widest crossing. The circle can be any size that holds the longer chord."""
    L1, L2 = p1 + q1, p2 + q2
    out = []
    for f in (1.03, 1.08, 1.15, 1.25, 1.4, 1.6, 1.85):
        R = max(L1, L2) / 2 * f
        h1, h2 = math.sqrt(R * R - L1 * L1 / 4), math.sqrt(R * R - L2 * L2 / 4)
        m1, m2 = (p1 - q1) / 2, (p2 - q2) / 2
        for s2 in (1, -1):
            v_ang = math.atan2(h1, m1)            # the center, from X, measured from u1 (taken as 0)
            t2 = v_ang - math.atan2(s2 * h2, m2)  # u2's direction
            cross = abs(math.degrees(t2)) % 180
            cross = min(cross, 180 - cross)
            if cross >= MIN_CROSS and min(p1, q1, p2, q2) * RC4 / R >= MIN_PART:
                d = math.hypot(m1, h1)
                out.append((R, -cross, (d * math.cos(v_ang), d * math.sin(v_ang)), R, (1.0, 0.0),
                            (math.cos(t2), math.sin(t2))))
    return [g[2:] for g in sorted(out)]

def chord_figure(parts, lengths, pose, geo):
    center, R, u1, u2 = geo
    p1, q1, p2, q2 = lengths
    k = RC4 / R
    raw = [(0.0, 0.0), (p1 * u1[0], p1 * u1[1]), (-q1 * u1[0], -q1 * u1[1]),
           (p2 * u2[0], p2 * u2[1]), (-q2 * u2[0], -q2 * u2[1])]
    X, E1, F1, E2, F2 = turn([((x - center[0]) * k, (y - center[1]) * k) for x, y in raw], pose, quarter=False)
    chains = [[E1, F1], [E2, F2]]
    pl = Placer(segments_of(chains), [((0, 0), RC4)])
    for end, text in ((E1, parts[0][0]), (F1, parts[0][1]), (E2, parts[1][0]), (F2, parts[1][1])):
        pl.put(side_cands(X, end, f"${text}$"), f"${text}$")
    return ((0, 0), RC4, chains, [], pl.labels, []), pl.clean

def fig4_parts(prompt):
    """The first circle and crossing (chord_geometries' order) that sets every label clear."""
    parts, lengths, pose, _ = t4_data(prompt)
    geos = chord_geometries(*lengths)
    if not geos:
        raise ValueError("chords too close to parallel to draw")
    first = None
    for geo in geos:
        got = chord_figure(parts, lengths, pose, geo)
        if got[1]:
            return got
        first = first or got
    return first

def fig5_parts(prompt, wide=4.6, tall=2.9):
    parts, ts, pose, _ = t5_data(prompt)
    t = list(ts)
    side = lambda i, j: t[i] + t[j]
    i, j = sorted(range(3), key=lambda n: t[n])[1:]   # the longest side joins the two longest tangents
    k_ = 3 - i - j
    base = side(i, j)
    u = (side(i, k_) ** 2 - side(j, k_) ** 2 + base ** 2) / (2 * base)
    w = math.sqrt(max(side(i, k_) ** 2 - u * u, 0.0))
    V = {i: (0.0, 0.0), j: (base, 0.0), k_: (u, w)}
    s = min(wide / base, tall / w if w else 9e9)
    V = {n: (x * s - base * s / 2, y * s - w * s / 2) for n, (x, y) in V.items()}
    # pose: 0 as built, 1 mirrored, 2 upside down, 3 both (a quarter turn would stand the long side up)
    q = [(-x if pose % 2 else x, -y if pose >= 2 else y) for x, y in (V[0], V[1], V[2])]
    a, b, c = (math.dist(q[1], q[2]), math.dist(q[0], q[2]), math.dist(q[0], q[1]))
    per = a + b + c
    I = ((a * q[0][0] + b * q[1][0] + c * q[2][0]) / per, (a * q[0][1] + b * q[1][1] + c * q[2][1]) / per)
    area = abs((q[1][0] - q[0][0]) * (q[2][1] - q[0][1]) - (q[2][0] - q[0][0]) * (q[1][1] - q[0][1])) / 2
    r = 2 * area / per
    chains = [[q[0], q[1], q[2], q[0]]]
    pl = Placer(segments_of(chains), [(I, r)])
    others = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
    for n in range(3):
        for slot, m in enumerate(others[n]):
            uu = unit(q[n], q[m])
            end = (q[n][0] + uu[0] * t[n] * s, q[n][1] + uu[1] * t[n] * s)   # the tangent point
            markup = f"${parts[n][slot]}$"
            pl.put(side_cands(q[n], end, markup, inside=I), markup)
    return (I, r, chains, [], pl.labels, []), pl.clean

FIGURE_PARTS = {"1": fig1_parts, "2": fig2_parts, "3": fig3_parts, "4": fig4_parts, "5": fig5_parts}

def drawable(typ, prompt):
    """Does the figure place every label cleanly? (False if it can't be drawn at all.)"""
    try:
        return FIGURE_PARTS[typ](prompt)[1]
    except ValueError:
        return False

def figure(p, unit_="1cm"):
    args, _ = FIGURE_PARTS[p["type"]](p["prompt"])
    center, r, chains, arcs, labels, leaders = args
    return fig.circled(center, r, chains, arcs=arcs, labels=labels, leaders=leaders, unit=unit_)

# ------------------------------------------------------------------
# Showing: each problem says what to do (EXTENDING.md 3.10)
# ------------------------------------------------------------------
ASK = {
    "1": "Find $x$ and $y$.",
    "2": "Find $x$, $y$, and $z$.",
    "3": "Find $x$, $y$, and $z$.",
    "4": "Find $x$.",
    "5": "The triangle and the circle are tangent at three points, as shown. Find $x$ and $y$.",
}
LEAD6 = "Use the quadratic formula to solve:"

def statement(p):
    return ASK[p["type"]]

def typst(p, gap="0.3em"):
    if p["type"] == "6":
        return f"{LEAD6} #h(0.5em) " + L10.shown(p["prompt"])
    try:
        f = figure(p)
    except Exception:
        return f"{statement(p)} #h(0.5em) [{plain(p['prompt'])}]"   # an edit that makes no figure; check() marks it
    return f"{statement(p)} #v(0.4em) #align(center)[{f}]"

def answer_typst(p):
    return f"${dfrac(p['answer'])}$" if p["type"] != "6" else L10.shown(p["answer"])

SLIDE_UNIT = "1.9cm"

def slide_typst(p, key=False):
    """A figure's slide: the words (and the answer, hidden on the question slide) beside the
    figure drawn larger; the figure never moves. None for Type 6."""
    if p["type"] == "6":
        return None
    try:
        f = figure(p, SLIDE_UNIT)
    except Exception:
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return (f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, "
            f"[{statement(p)} #v(0.8em) {shown}], [{f}])")

def text(p):
    if p["type"] == "6":
        return f"{LEAD6} {plain(p['prompt'])}"
    return f"{plain(statement(p).replace('$', ''))}   [figure: {p['prompt']}]"

def answer_text(p):
    return plain(p["answer"]).replace("plus.minus", "±")

def height(p):
    return 0.3 if p["type"] == "6" else (2.4 if p["type"] == "5" else 3.6)

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
EXAMPLE = {
    "1": "46, x + 10; 30, y + 20; pose 0", "2": "75, 80; 50; pose 0", "3": "35, 75; pose 0",
    "4": "15, x + 10; 20, x + 5; pose 0", "5": "x + 4, 6; x + y, 10; x, x; pose 0", "6": "3 x^2 - 2 x + 5 = 0",
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
        if typ in FIGURES:
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
