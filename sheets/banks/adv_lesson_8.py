"""Lesson 8 (Advanced Math): statements of similarity, proportional segments,
angle bisectors and side ratios. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_008/slides/deck_008.typ): examples
8.1-8.4 and Problem Set 8, problems 9-11.

    1  two ratios equal, by similar triangles:   altitude BD to the hypotenuse AC of right triangle ABC;
                                                 show AD/AB = AB/AC
                                                     △ADB ~ △ABC;  AD/AB = DB/BC = AB/AC
    2  parallel lines cut transversals:          x + 1 over 13 on one transversal, x + 4 over 19 on the
                                                 other                                 x = 11/2
    3  an angle bisector and the side ratios:    AB = 10, BC = 15; BD bisects angle B; AD = x, DC = 12
                                                                                       x = 8

Every type has a figure, drawn from the problem's own data (lesson_figures):
Type 1's right triangle with its altitude, Type 2's lines spaced in the ratio of
the segments at the solution, Type 3's triangle to scale with x solved.

The key writes what the deck writes:
  1  the similarity statement, then the three ratios in the book's order (first
     two letters, last two, first and last), the left triangle's sides on top:
     "△ADB ~ △ABC" and "AD/AB = DB/BC = AB/AC" (8.1). The statement is the one
     that makes the asked-for equation the first and last ratios: the left
     triangle holds the numerators, its first vertex the one they share. For
     problem 9 (XY/XM = YZ/MY) that is △YXZ ~ △MXY; the deck takes △XMY ~ △YMZ
     and rearranges, which needs a step more.
  2, 3  x = the value, a whole number or a fraction in lowest terms: x = 11/2,
     x = 3 (8.2, problem 10); x = 8, x = 60/7, x = 16/3 (8.3, 8.4, problem 11).

check() works from the problem's data, independently of how it was built:
  1  the figure's points are computed for two different right triangles; the
     key's two triangles must be triangles of the figure, their corresponding
     angles equal in both, its three ratios each a side of the left triangle over
     the matching side of the right one (all equal, in the book's order), and the
     asked-for equation must be two of them, and true.
  2  the key's x put back into upper/lower = upper/lower, exactly; every segment
     positive; the fraction in lowest terms.
  3  the key's x put back into VP/VQ = PD/DQ, exactly; the sides make a triangle.

No skipped sources: Type 1 ("show the following") is a short derivation, not a
two-column proof, and the types file lists it as a type.

A problem: dict(type, prompt, answer, source); the prompt is the problem's data:
  1  "altitude A B C D; (A D)/(A B) = (A B)/(A C)"   (left, right-angle vertex, right, foot)
     answer "triangle A D B tilde triangle A B C; (A D)/(A B) = (D B)/(B C) = (A B)/(A C)"
  2  "parallel x + 1, 13; x + 4, 19"   (each transversal's upper, lower segment)   answer "x = 11/2"
  3  "bisect A B C, B, D; 10, 15, x, 12"   (the triangle, the bisected vertex V, the foot D;
     VP, VQ, PD, DQ, with P, Q the other two vertices in the name's order)        answer "x = 8"
"""
import itertools, math, re
from fractions import Fraction as F
from .. import gen
from ..gen import need
from ..typmath import dfrac
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_8"
FIXED = False
TITLE = "Lesson 8: Statements of Similarity, Proportional Segments, Angle Bisectors and Side Ratios"
INSTRUCTIONS = "Solve each problem."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

EXACT = "Find x. Write it as a whole number or a fraction in lowest terms."
TYPES = [
    dict(key="1", title="Showing Two Ratios Are Equal",
         look="A right triangle, the altitude to its hypotenuse, and two ratios to show equal.",
         move="Look for similar triangles. Find the two triangles whose sides are in the ratios, and write the "
              "similarity with the vertices in matching order, like $triangle A D B tilde triangle A B C$. Write "
              "the three ratios with the left triangle's sides on top: $(A D)/(A B)$, $(D B)/(B C)$, "
              "$(A B)/(A C)$. All are equal; equate the two you need.",
         instructions="Use similar triangles to show that the ratios are equal.", space="1.4in"),
    dict(key="2", title="Parallel Lines Cut Transversals Proportionally",
         look="Three parallel lines (arrowheads) cut by two transversals, the segments labeled.",
         move="Parallel lines cut proportional segments: upper over lower on one transversal equals upper over "
              "lower on the other, like $(x + 1)/13 = (x + 4)/19$. Cross multiply and solve.",
         instructions=EXACT),
    dict(key="3", title="An Angle Bisector and the Side Ratios",
         look="A triangle with one angle bisected; two sides and the two pieces of the opposite side labeled.",
         move="The bisector divides the opposite side into segments proportional to the other two sides: side "
              "over side equals the segment next to the first over the segment next to the second, like "
              "$x/12 = 10/15$. Cross multiply and solve.",
         instructions=EXACT),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# letters: a triangle's three, and a fourth for the foot (8.1: A B C, D; problem 9: X Y Z, M)
TRIPLES = ("ABC", "DEF", "JKL", "PQR", "RST", "XYZ", "LMN", "UVW")
FEET = "DEHMNPQSTKG"

def letters(r):
    t = r.choice(TRIPLES)
    f = r.choice([c for c in FEET if c not in t])
    return tuple(t), f

def frac(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"

# ------------------------------------------------------------------
# Type 1: the altitude to the hypotenuse
# ------------------------------------------------------------------
def roles(L, T_, R, D):
    """Each of the figure's three right triangles as (the vertex whose angle equals the
    angle at L, the one whose angle equals the angle at R, the right angle's vertex)."""
    return {"big": (L, R, T_), "left": (L, T_, D), "right": (T_, R, D)}

def seg(a, b):
    return f"({a} {b})"

def ratio(n, d):
    return f"{seg(*n)}/{seg(*d)}"

def t1_build(names, pair, order, swap, spell):
    """pair: (left triangle, right triangle) of "big", "left", "right"; order: the left
    triangle's vertices as a permutation of its roles; swap: the equation's sides
    exchanged; spell: four flags, each segment of the equation spelled backward."""
    L, T_, R, D = names
    ro = roles(*names)
    v = [ro[pair[0]][i] for i in order]
    w = [ro[pair[1]][i] for i in order]
    n1, d1, n2, d2 = (v[0], v[1]), (w[0], w[1]), (v[0], v[2]), (w[0], w[2])
    segs = [s[::-1] if f else s for s, f in zip((n1, d1, n2, d2), spell)]
    a, b = ratio(segs[0], segs[1]), ratio(segs[2], segs[3])
    if swap:
        a, b = b, a
    return f"altitude {L} {T_} {R} {D}; {a} = {b}"

PAIRS1 = [p for p in itertools.permutations(("big", "left", "right"), 2)]
ORDERS = list(itertools.permutations(range(3)))

def t1_ok(names, pair, order, swap, spell):
    return (len(names) == 4 and len(set(names)) == 4 and all(n.isupper() and len(n) == 1 for n in names)
            and "".join(names[:3]) in TRIPLES and names[3] in FEET and tuple(pair) in PAIRS1
            and tuple(order) in ORDERS and swap in (True, False) and len(spell) == 4
            and all(f in (True, False) for f in spell))

def t1_pick(r):
    t, f = letters(r)
    p = dict(names=t + (f,), pair=r.choice(PAIRS1), order=r.choice(ORDERS), swap=r.random() < 0.25,
             spell=tuple(r.random() < 0.25 for _ in range(4)))
    need(t1_ok(**p))
    return p

SEG = r"\((\w) (\w)\)"
RATIO = SEG + "/" + SEG

def read_alt(prompt):
    m = re.fullmatch(r"altitude (\w) (\w) (\w) (\w); " + RATIO + " = " + RATIO, " ".join(prompt.split()))
    if not m:
        raise ValueError("write it like: altitude A B C D; (A D)/(A B) = (A B)/(A C)")
    g = m.groups()
    names = g[:4]
    if len(set(names)) != 4:
        raise ValueError("four different points")
    segs = [frozenset(g[i:i + 2]) for i in (4, 6, 8, 10)]
    if any(len(s) != 2 or not s <= set(names) for s in segs):
        raise ValueError("each segment joins two of the figure's points")
    return names, [g[i:i + 2] for i in (4, 6, 8, 10)]

def answer1(prompt):
    names, (n1, d1, n2, d2) = read_alt(prompt)
    tris = [set(t) for t in roles(*names).values()]
    v0 = set(n1) & set(n2)
    w0 = set(d1) & set(d2)
    if len(v0) != 1 or len(w0) != 1:
        raise ValueError("the numerators (and the denominators) must share a vertex")
    v0, w0 = v0.pop(), w0.pop()
    v = [v0, (set(n1) - {v0}).pop(), (set(n2) - {v0}).pop()]
    w = [w0, (set(d1) - {w0}).pop(), (set(d2) - {w0}).pop()]
    if set(v) not in tris or set(w) not in tris or set(v) == set(w):
        raise ValueError("no two triangles of the figure hold these sides")
    sides = [ratio((v[i], v[j]), (w[i], w[j])) for i, j in ((0, 1), (1, 2), (0, 2))]
    return f"triangle {' '.join(v)} tilde triangle {' '.join(w)}; " + " = ".join(sides)

def points(names, a, b):
    """The figure's points for legs a, b: the hypotenuse on the x-axis."""
    L, T_, R, D = names
    c = math.hypot(a, b)
    return {L: (0.0, 0.0), R: (c, 0.0), D: (a * a / c, 0.0), T_: (a * a / c, a * b / c)}

def angle(P, v, p, q):
    (vx, vy), (px, py), (qx, qy) = P[v], P[p], P[q]
    u, w = (px - vx, py - vy), (qx - vx, qy - vy)
    return math.acos((u[0] * w[0] + u[1] * w[1]) / (math.hypot(*u) * math.hypot(*w)))

def length(P, s):
    (ax, ay), (bx, by) = P[s[0]], P[s[1]]
    return math.hypot(ax - bx, ay - by)

def check1(p):
    names, target = read_alt(p["prompt"])
    m = re.fullmatch(r"triangle (\w) (\w) (\w) tilde triangle (\w) (\w) (\w); (.+)", " ".join(p["answer"].split()))
    if not m:
        return "failed"
    v, w = m.groups()[:3], m.groups()[3:6]
    tris = [set(t) for t in roles(*names).values()]
    if set(v) not in tris or set(w) not in tris or set(v) == set(w) or len(set(v)) < 3 or len(set(w)) < 3:
        return "failed"
    ratios = m.group(7).split(" = ")
    want = [((v[i], v[j]), (w[i], w[j])) for i, j in ((0, 1), (1, 2), (0, 2))]
    got = []
    for r_ in ratios:
        mm = re.fullmatch(RATIO, r_)
        if not mm:
            return "failed"
        got.append(((mm.group(1), mm.group(2)), (mm.group(3), mm.group(4))))
    same = lambda x, y: frozenset(x[0]) == frozenset(y[0]) and frozenset(x[1]) == frozenset(y[1])
    if len(got) != 3 or not all(same(g, w_) for g, w_ in zip(got, want)):
        return "failed"
    for a, b in ((1.0, 1.8), (1.3, 0.7)):                        # two shapes: nothing holds by accident
        P = points(names, a, b)
        if any(abs(angle(P, v[i], v[(i + 1) % 3], v[(i + 2) % 3]) - angle(P, w[i], w[(i + 1) % 3], w[(i + 2) % 3]))
               > 1e-9 for i in range(3)):
            return "failed"                                       # not a similarity
        vals = [length(P, n) / length(P, d) for n, d in got]
        if max(vals) - min(vals) > 1e-9:
            return "failed"
        t = [length(P, s) for s in target]
        if abs(t[0] / t[1] - t[2] / t[3]) > 1e-9:
            return "failed"                                       # the asked-for equation is false
    pairs = [(frozenset(target[0]), frozenset(target[1])), (frozenset(target[2]), frozenset(target[3]))]
    listed = [(frozenset(n), frozenset(d)) for n, d in got]
    return "checked" if all(x in listed for x in pairs) else "failed"

# ------------------------------------------------------------------
# Type 2: parallel lines and two transversals
# ------------------------------------------------------------------
COEF = range(1, 5)
CONST = [c for c in range(-6, 13) if c]
SEGS = range(4, 31)

def linear(a, b):
    """3x - 1, x + 4."""
    head = "x" if a == 1 else f"{a}x"
    return head if b == 0 else f"{head} {'+' if b > 0 else '-'} {abs(b)}"

def read_linear(s):
    """(a, b) for a x + b, or (0, n) for a number."""
    s = " ".join(s.split())
    m = re.fullmatch(r"(\d*)x(?: ([+-]) (\d+))?", s)
    if m:
        a = int(m.group(1) or 1)
        b = int(m.group(3) or 0) * (-1 if m.group(2) == "-" else 1)
        return F(a), F(b)
    m = re.fullmatch(r"\d+(?:\.\d+)?", s)
    if m:
        return F(0), F(s)
    raise ValueError("a segment is a number or like 3x - 1")

def t2_build(a, b, n1, c, d, n2, row="upper"):
    """Left transversal: a x + b and n1; right: c x + d and n2; the expressions on the
    upper segments (8.2, problem 10) or the lower."""
    e1, e2 = linear(a, b), linear(c, d)
    if row == "upper":
        return f"parallel {e1}, {n1}; {e2}, {n2}"
    return f"parallel {n1}, {e1}; {n2}, {e2}"

def solve2(prompt):
    segs = read_parallel(prompt)
    (a1, b1), (a2, b2), (a3, b3), (a4, b4) = segs        # u1 / l1 = u2 / l2:  u1 l2 = u2 l1
    # (a1 x + b1)(a4 x + b4) = (a3 x + b3)(a2 x + b2): linear when each product has one x
    if (a1 and a4) or (a3 and a2):
        raise ValueError("an x on both segments of a transversal makes a quadratic")
    A = a1 * b4 + b1 * a4 - a3 * b2 - b3 * a2
    B = b1 * b4 - b3 * b2
    if A == 0:
        raise ValueError("no single x")
    return -B / A

def read_parallel(prompt):
    m = re.fullmatch(r"parallel (.+?), (.+?); (.+?), (.+)", " ".join(prompt.split()))
    if not m:
        raise ValueError("write it like: parallel x + 1, 13; x + 4, 19")
    return [read_linear(g) for g in m.groups()]

def t2_ok(a, b, n1, c, d, n2, row="upper"):
    if not (a in COEF and c in COEF and b in CONST and d in CONST and n1 in SEGS and n2 in SEGS
            and row in ("upper", "lower")):
        return False
    try:
        x = solve2(t2_build(a, b, n1, c, d, n2, row))
    except ValueError:
        return False
    e1, e2 = a * x + b, c * x + d
    return (0 < x <= 20 and x.denominator <= 10 and 0 < e1 <= 60 and 0 < e2 <= 60
            and 0.25 <= (e1 / n1 if row == "upper" else n1 / e1) <= 4)

def t2_pick(row):
    def pick(r):
        p = dict(a=r.choice((1, 1, 2, 3, 4)), b=r.choice(CONST), n1=r.choice(SEGS), c=r.choice((1, 1, 2, 3, 4)),
                 d=r.choice(CONST), n2=r.choice(SEGS), row=row)
        need((p["a"], p["b"]) != (p["c"], p["d"]) and t2_ok(**p))
        return p
    return pick

def answer2(prompt):
    x = solve2(prompt)
    if x <= 0:
        raise ValueError("x is not positive")
    return f"x = {frac(x)}"

ANSWER_X = re.compile(r"x = (-?\d+)(?:/(\d+))?")

def read_x(answer):
    m = ANSWER_X.fullmatch(" ".join(answer.split()))
    if not m:
        raise ValueError("write x = 11/2")
    num, den = int(m.group(1)), int(m.group(2) or 1)
    if den == 0 or math.gcd(num, den) != 1 or den == 1 and m.group(2):
        return None                                               # not in lowest terms
    return F(num, den)

def check2(p):
    segs = read_parallel(p["prompt"])
    x = read_x(p["answer"])
    if x is None:
        return "failed"
    u1, l1, u2, l2 = (a * x + b for a, b in segs)
    return "checked" if min(u1, l1, u2, l2) > 0 and u1 * l2 == u2 * l1 else "failed"

# ------------------------------------------------------------------
# Type 3: an angle bisector
# ------------------------------------------------------------------
SIDES = range(4, 31)
PIECES = range(3, 21)

def t3_build(names, V, D, VP, VQ, PD, DQ):
    """names: the triangle's three letters; V the bisected vertex; one of the four lengths is "x"."""
    return f"bisect {' '.join(names)}, {V}, {D}; {VP}, {VQ}, {PD}, {DQ}"

def read_bisect(prompt):
    m = re.fullmatch(r"bisect (\w) (\w) (\w), (\w), (\w); (\S+), (\S+), (\S+), (\S+)", " ".join(prompt.split()))
    if not m:
        raise ValueError("write it like: bisect A B C, B, D; 10, 15, x, 12")
    names, V, D = m.groups()[:3], m.group(4), m.group(5)
    if V not in names or D in names or len(set(names)) != 3:
        raise ValueError("bisect a vertex of the triangle; name the foot with a new letter")
    vals = list(m.groups()[5:])
    if vals.count("x") != 1:
        raise ValueError("exactly one length is x")
    return names, V, D, [v if v == "x" else F(v) for v in vals]

def solve3(prompt):
    """x from VP DQ = VQ PD."""
    _, _, _, vals = read_bisect(prompt)
    i = vals.index("x")
    VP, VQ, PD, DQ = vals
    x = {0: lambda: VQ * PD / DQ, 1: lambda: VP * DQ / PD, 2: lambda: VP * DQ / VQ, 3: lambda: VQ * PD / VP}[i]()
    return x

def is_triangle(VP, VQ, PQ):
    return VP + VQ > PQ and VP + PQ > VQ and VQ + PQ > VP

def tall_enough(VP, VQ, PQ):
    """The apex well above the base, so the figure reads."""
    s = (VP + VQ + PQ) / 2
    area2 = s * (s - VP) * (s - VQ) * (s - PQ)
    return area2 > 0 and 2 * math.sqrt(area2) / PQ >= 0.25 * PQ

def t3_ok(names, V, D, VP, VQ, PD, DQ):
    vals = [VP, VQ, PD, DQ]
    if not ("".join(names) in TRIPLES and V in names and D in FEET and D not in names and vals.count("x") == 1):
        return False
    i = vals.index("x")
    known = [v for v in vals if v != "x"]
    if not all(isinstance(v, int) for v in known):
        return False
    if not all((v in SIDES) if j < 2 else (v in PIECES) for j, v in enumerate(vals) if v != "x"):
        return False
    x = solve3(t3_build(names, V, D, *vals))
    full = [x if v == "x" else F(v) for v in vals]
    PQ = full[2] + full[3]
    return (x.denominator <= 9 and full[0] != full[1] and is_triangle(full[0], full[1], PQ)
            and PQ >= F(3, 5) * max(full[0], full[1])                 # broad, as the book's are
            and tall_enough(*map(float, (full[0], full[1], PQ))))

def t3_pick(where):
    """where: "piece" (x a segment, 8.3, problem 11) or "side" (8.4)."""
    def pick(r):
        t, D = letters(r)
        V = r.choice(t)
        vals = [r.choice(SIDES), r.choice(SIDES), r.choice(PIECES), r.choice(PIECES)]
        vals[r.choice((2, 3) if where == "piece" else (0, 1))] = "x"
        p = dict(names=t, V=V, D=D, VP=vals[0], VQ=vals[1], PD=vals[2], DQ=vals[3])
        need(t3_ok(**p))
        return p
    return pick

def answer3(prompt):
    x = solve3(prompt)
    if x <= 0:
        raise ValueError("x is not positive")
    return f"x = {frac(x)}"

def check3(p):
    _, _, _, vals = read_bisect(p["prompt"])
    x = read_x(p["answer"])
    if x is None or x <= 0:
        return "failed"
    VP, VQ, PD, DQ = (x if v == "x" else v for v in vals)
    return "checked" if VP * DQ == VQ * PD and is_triangle(VP, VQ, PD + DQ) else "failed"

# ------------------------------------------------------------------
# Templates: (pick, build)
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick, t1_build)],
    "2": [(t2_pick("upper"), t2_build), (t2_pick("upper"), t2_build), (t2_pick("lower"), t2_build)],
    "3": [(t3_pick("piece"), t3_build), (t3_pick("piece"), t3_build), (t3_pick("side"), t3_build)],
}
RANGES = {t1_build: t1_ok, t2_build: t2_ok, t3_build: t3_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

ANSWER = {"1": answer1, "2": answer2, "3": answer3}
CHECK = {"1": check1, "2": check2, "3": check3}
KIND = {"1": "altitude", "2": "parallel", "3": "bisect"}

def answer_of(prompt):
    return ANSWER[kind(prompt)](prompt)

def kind(prompt):
    w = prompt.split(" ", 1)[0]
    for k, v in KIND.items():
        if v == w:
            return k
    raise ValueError("start with altitude, parallel, or bisect")

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        return CHECK[p["type"]](p)
    except (ValueError, KeyError, AttributeError, TypeError, ZeroDivisionError):
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Figures and words
# ------------------------------------------------------------------
def mathx(s):
    return f"${s}$"

def figure(p, unit="1cm"):
    k = p["type"]
    if k == "1":
        names, _ = read_alt(p["prompt"])
        return fig.altitude(names, unit=unit)
    if k == "2":
        m = re.fullmatch(r"parallel (.+?), (.+?); (.+?), (.+)", " ".join(p["prompt"].split()))
        texts = m.groups()
        segs = read_parallel(p["prompt"])
        try:
            x = solve2(p["prompt"])
        except ValueError:
            x = F(1)
        u1, l1 = (a * x + b for a, b in segs[:2])
        ratio = float(u1 / l1) if u1 > 0 and l1 > 0 else 1.0
        return fig.transversals([mathx(t) for t in texts], min(max(ratio, 0.25), 4), unit=unit)
    names, V, D, vals = read_bisect(p["prompt"])
    P, Q = [n for n in names if n != V]
    try:
        x = solve3(p["prompt"])
    except (ValueError, ZeroDivisionError):
        x = F(1)
    full = [float(x if v == "x" else v) for v in vals]
    if not is_triangle(full[0], full[1], full[2] + full[3]):
        full = [3, 4, 2, 2.5]                                     # an edit that makes no triangle: a sketch
    return fig.bisector((V, P, Q, D), full, [mathx(v) for v in vals], unit=unit)

def spaced(names):
    return " ".join(names)

def statement(p):
    k = p["type"]
    if k == "1":
        (L, T_, R, D), (n1, d1, n2, d2) = read_alt(p["prompt"])
        eq = f"{ratio(n1, d1)} = {ratio(n2, d2)}"
        return (f"In $triangle {L} {T_} {R}$, segment ${T_} {D}$ is the altitude to the hypotenuse ${L} {R}$. "
                f"Show the following: #v(0.3em) #h(2em) ${dfrac(eq)}$")
    if k == "2":
        return "Find $x$."
    names, V, D, _ = read_bisect(p["prompt"])
    return (f"In $triangle {spaced(names)}$, segment ${V} {D}$ is the angle bisector of angle ${V}$. "
            "Find $x$.")

def typst(p, gap="0.3em"):
    try:
        s, f = statement(p), figure(p)
    except ValueError:
        return p["prompt"]
    return f"{s} #v(0.4em) #align(center)[{f}]"

def answer_typst(p):
    if p["type"] == "1" and ";" in p["answer"]:
        sim, ratios = p["answer"].split(";", 1)
        return f"${sim.strip()}$ \\ ${dfrac(ratios.strip())}$"
    return f"${dfrac(p['answer'])}$"

SLIDE_UNIT = "1.9cm"

def slide_typst(p, key=False):
    """The words (and the answer, hidden on the question slide) beside the figure drawn
    larger; the figure never moves."""
    try:
        f, s = figure(p, SLIDE_UNIT), statement(p)
    except ValueError:
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{s} #v(0.8em) {shown}], [{f}])"

def plain(s):
    s = re.sub(r"\((\w) (\w)\)", r"\1\2", s)
    s = re.sub(r"triangle (\w) (\w) (\w)", r"triangle \1\2\3", s)
    return s.replace("triangle ", "△").replace(" tilde ", " ~ ").replace("display", "")

def text(p):
    try:
        s = statement(p)
    except ValueError:
        return p["prompt"]
    s = re.sub(r"#h\([^)]*\)\s*", "", s).replace("$", "")
    s = re.sub(r"\b([A-Z]) ([A-Z])(?: ([A-Z]))?\b", lambda m: "".join(g for g in m.groups() if g), s)
    return plain(s) + "   [figure]"

def answer_text(p):
    return plain(p["answer"]).replace("; ", "\n")

def height(p):
    return 2.6

# ------------------------------------------------------------------
# Editing: the prompt is the problem's data
# ------------------------------------------------------------------
EXAMPLE = {"1": "altitude A B C D; (A D)/(A B) = (A B)/(A C)", "2": "parallel x + 1, 13; x + 4, 19",
           "3": "bisect A B C, B, D; 10, 15, x, 12"}

def clean(t):
    return " ".join(t.replace("−", "-").split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    try:
        if kind(t) != old["type"]:
            raise ValueError
        answer = answer_of(t)
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"write it like: {EXAMPLE[old['type']]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)
