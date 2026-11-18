"""Lesson 4 (Advanced Math): construction. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_004/slides/deck_004.typ, with its CeTZ
answer figures in constructions.typ): the lesson's ten constructions
(Constructions 1-10 in the deck; the book doesn't number them) and Problem
Set 4, problems 7-11.

     1  measure angles with a protractor     O; A 0, B 45, C 180          m∠BOA = 45°, m∠COB = 135°
     2  copy a segment                       AB = 4                        XP = AB = 4 cm
     3  copy an angle                        PQR = 30, QR at -15           m∠P'XY = m∠PQR = 30°
     4  bisect an angle                      BAC = 40, AC at 0             m∠BAD = m∠DAC = 20°
     5  the perpendicular bisector           MN = 6                        MD = DN = 3 cm
     6  a perpendicular at a point on a line segment RS = 6.5, P at 2.5   PD ⊥ RS
     7  a perpendicular from a point to a line  line EF = 7.2, P at 3.6, 2.2 above   PD ⊥ EF, PD = 2.2 cm
     8  a triangle from its three sides      a = 2, b = 3, c = 4           a = 2 cm, b = 3 cm, c = 4 cm
     9  a parallel through a point           line 7, P at 2.5, 2.5 above   PQ ∥ the given line
    10  divide a segment into equal parts    AB = 6, 3 parts               AX = XY = YB = 2 cm

One type for each construction, in the lesson's order. Constructions 1, 4, 7,
9, and 10 have no Problem Set item; they are still types.

The figure is the problem. Every figure is drawn from the prompt's data in
centimeters, at true size on a sheet (lengths print as given, so a compass
and ruler work on the page; the book's figures carry no numbers, so the
sources' lengths and angles were measured off the scans). The key draws the
construction on the given figure, its arcs and new lines in red, as the
deck's answer slides draw them; the question's figure leaves the same room
blank (an invisible box around the whole construction), so the student has
room to construct and nothing moves between the question and answer slides.

Answer conventions (chosen here: the deck's answers are the construction
steps and a sentence, "XP = AB, so XP ≅ AB", "∠P'XY ≅ ∠PQR"). The key states
what the construction makes, with the measure a ruler or protractor checks
it by, and names the new points the way the deck does:
  1  each asked angle's measure, in the order asked: m∠BOA = 45°, m∠COB = 135°
  2  XP = AB = 4 cm: the copy on ray XY ends at P (the given ray's own
     letters when the problem draws it)
  3  m∠P'XY = m∠PQR = 30°: the copy's vertex X, its side XY, the new side
     through P' (the first letter of the angle, primed); the arcs cross the
     sides at M and N (deck PS 8), the copy's arc meets XY at Z
  4  m∠BAD = m∠DAC = 20°: the arcs meet at D (the first free letter)
  5  MD = DN = 3 cm: the bisector meets the segment at its midpoint D
  6  PD ⊥ RS (a line: PD ⊥ AC, written with the line's arrow): the arcs
     about P cross at M and N, the arcs about M and N meet at D
  7  PD ⊥ EF, PD = 2.2 cm: the arcs about P cross the line at R and S, the
     foot of the perpendicular is D
  8  each side's length, in the order given: a = 2 cm, b = 3 cm, c = 4 cm;
     the longest is laid down first, the middle one swung from its left end
  9  PQ ∥ the given line: the transversal from X on the line, angle A copied
     at P, the new line through P and Q
 10  AX = XY = YB = 2 cm: equal steps R, S, T along ray AP, parallels to TB
(Letters already in the problem are skipped: a new point takes the next free
letter of its list.)

check() works from the problem's data, not from how the key was made. It reads
the answer's names and numbers back from its text and requires the names the
construction draws and the measure taken off the drawn figure (the distance
between the placed points, the angle between the placed rays). Then it checks
the key's construction by what makes it right, from its points: the copied
segment's end is on the ray at the original's length; the copied angle's
vertex angle equals the original's, its arc of radius MN; the bisector halves
the angle and its arcs' crossing is equidistant from the two side points;
each perpendicular's arcs meet at points equidistant from the two centers,
the line through them is at right angles and through the right point; the
triangle's three vertices are the three lengths apart; the parallel's
direction is the line's, its point the copied arc's end; the division points
are on the segment, each parallel to TB, equally spaced. Every pair of arcs
that must cross does, clearly (a draw where they would barely meet is
rejected).

Skipped: none. Lesson 4 has no proofs; Problem Set 4's other problems are
other lessons' types.

A problem: dict(type, prompt, answer, source). The prompt is the figure's data
in a short form, and it is what an edit changes:
    1  "O; A 0, B 45, C 180"     (each ray's direction on the protractor; the angles between
                                  consecutive rays are asked)
    2  "AB = 4", "AB = 4.5, tilt 20", "AB = 4; ray XY"
    3  "PQR = 30, QR at -15"     (the angle, its measure, the direction of its second side)
    4  "BAC = 40, AC at 0"
    5  "MN = 6", "MN = 5, tilt -20"
    6  "segment RS = 6.5, P at 2.5", "line AC = 6, P at 2"
    7  "line EF = 7.2, P at 3.6, 2.2 above"   (P's foot 3.6 cm from E, P 2.2 cm off the line)
    8  "a = 2, b = 3, c = 4", "BC = 3, AX = 4, MN = 5"
    9  "line 7, P at 2.5, 2.5 above"
   10  "AB = 6, 3 parts"
"""
import math, re
from .. import gen
from ..gen import need
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_4"
FIXED = False
TITLE = "Lesson 4: Construction"
INSTRUCTIONS = "Use a compass and a straightedge. Leave the construction marks."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

TYPES = [
    dict(key="1", title="Measuring Angles with a Protractor",
         look="Rays from the center of a protractor's baseline; find the angles between them.",
         move="The vertex is under the origin and one side lies along the baseline. Read where the other "
              "ray crosses the scale that starts at 0 on the first ray's side: the inner scale from the "
              "right, the outer from the left. Between two rays off the baseline, subtract their readings.",
         instructions="Find each angle's measure.", width="full", space="0.3in"),
    dict(key="2", title="Copying a Line Segment",
         look="One segment to copy.",
         move="Draw a ray XY. Open the compass from A to B. Without changing it, put the point on X and "
              "draw an arc crossing the ray at P. Then XP = AB.", space="0.2in"),
    dict(key="3", title="Copying an Angle",
         look="One angle to copy, its vertex in the middle of its name.",
         move="Draw ray XY. An arc about the vertex crosses the sides at M and N; the same arc about X "
              "crosses XY at Z. Set the compass to MN and swing it from Z to cross the arc at P'. Draw "
              "ray XP'.", width="full", space="0.2in"),
    dict(key="4", title="Bisecting an Angle",
         look="One angle to cut in half.",
         move="An arc about the vertex crosses both sides. Equal arcs about those two points meet inside "
              "the angle. The ray from the vertex through that crossing is the bisector.", space="0.2in"),
    dict(key="5", title="The Perpendicular Bisector of a Segment",
         look="One segment; bisect it with a perpendicular.",
         move="With centers at the two ends, draw equal arcs that meet above and below the segment (the "
              "radius more than half the segment, or they won't meet). The line through the two "
              "crossings is the perpendicular bisector.", space="0.2in"),
    dict(key="6", title="A Perpendicular at a Point on a Line",
         look="A segment or line with a point P on it.",
         move="Equal arcs about P cross the line at M and N. Widen the compass: equal arcs about M and N "
              "meet at D. Line PD is perpendicular to the line at P, because PM = PN.", space="0.2in"),
    dict(key="7", title="A Perpendicular from a Point to a Line",
         look="A line and a point P off it.",
         move="An arc about P crosses the line at R and S. Construct the perpendicular bisector of RS: "
              "equal arcs about R and S meet on the far side. It passes through P, because PR = PS.",
         width="full", space="0.2in"),
    dict(key="8", title="A Triangle from Its Three Sides",
         look="Three segments: the sides of the triangle.",
         move="Mark off the longest side on a ray. From its left end swing an arc the length of one other "
              "side, from its right end an arc the length of the third. Where the arcs cross is the third "
              "vertex. (They cross because the two shorter sides add to more than the longest.)",
         space="0.2in"),
    dict(key="9", title="A Parallel Through a Point",
         look="A line and a point P off it.",
         move="Draw a line from P to a point X on the line; it makes angle A with the line. Copy angle A "
              "at P on the same side. The corresponding angles are equal, so the new line is parallel.",
         width="full", space="0.2in"),
    dict(key="10", title="Dividing a Segment into Equal Parts",
         look="A segment to divide into a given number of equal parts.",
         move="Draw a ray from A at an angle. With the compass, step off equal lengths along it (R, S, T). "
              "Connect the last mark to B and draw parallels to that segment through the other marks. "
              "Parallels cut transversals proportionally, so the pieces of AB are equal.", space="0.2in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.2in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Plane geometry, in centimeters
# ------------------------------------------------------------------
def u(deg):
    return (math.cos(math.radians(deg)), math.sin(math.radians(deg)))

def add(p, q, k=1.0):
    return (p[0] + k * q[0], p[1] + k * q[1])

def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])

def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def normal(v):
    return (-v[1], v[0])

def direction(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))

def angle_at(v, p, q):
    """The angle pvq in degrees, 0 to 180."""
    a, b = sub(p, v), sub(q, v)
    return math.degrees(math.atan2(abs(cross(a, b)), dot(a, b)))

def meet(c1, r1, c2, r2):
    """The two points where circles (c1, r1) and (c2, r2) cross: left, then right of c1 -> c2."""
    d = dist(c1, c2)
    need(abs(r1 - r2) < d < r1 + r2)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    e = ((c2[0] - c1[0]) / d, (c2[1] - c1[1]) / d)
    m = add(c1, e, a)
    n = normal(e)
    return add(m, n, h), add(m, n, -h)

def crosses(c1, r1, c2, r2, margin=0.12):
    """Do the circles cross clearly: not nearly tangent, so the drawn arcs plainly meet?"""
    d = dist(c1, c2)
    return abs(r1 - r2) + margin < d < r1 + r2 - margin

TOL = 1e-6

def close(a, b, tol=TOL):
    return abs(a - b) < tol

def on_segment(p, a, b, tol=TOL):
    return abs(cross(sub(b, a), sub(p, a))) / dist(a, b) < tol and -tol <= dot(sub(p, a), sub(b, a)) <= dist(a, b) ** 2 + tol

# ------------------------------------------------------------------
# Numbers and letters
# ------------------------------------------------------------------
def num(x):
    """4, 4.5, 2.75: no trailing zeros."""
    s = f"{round(x, 2):.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s

NUM = r"-?\d+(?:\.\d+)?"

def tenths(lo, hi, step=0.5):
    """lo..hi by step, as floats rounded to tenths."""
    n = round((hi - lo) / step)
    return tuple(round(lo + i * step, 2) for i in range(n + 1))

def is_in(x, values):
    return any(abs(x - v) < 1e-9 for v in values)

def free(used, pool, n=1):
    """The first n letters of pool not in used."""
    out = [c for c in pool if c not in used][:n]
    need(len(out) == n)
    return out

def names(s):
    """'P Q R' for 'PQR': Typst math names a point by its letter, and a segment by its two."""
    return " ".join(s)

# A label set off from its point: below a point on a line (as the book prints them).
LAB = 0.38

def lab(p, off, text, who="given"):
    return ("label", add(p, off), f"${text}$", who)

# ------------------------------------------------------------------
# Type 1: measuring angles with a protractor
# ------------------------------------------------------------------
DIRS = tuple(range(0, 181, 5))
NAMES1 = (("O", "A", "B", "C"), ("O", "X", "Y", "Z"), ("V", "P", "Q", "R"), ("K", "L", "M", "N"),
          ("E", "D", "F", "G"))
GAP1 = 15                                              # the narrowest angle between rays

P1 = re.compile(r"^([A-Z]); ([A-Z]) (\d+), ([A-Z]) (\d+), ([A-Z]) (\d+)$")

def read1(prompt):
    m = P1.match(prompt)
    if not m:
        raise ValueError("write it like: O; A 0, B 45, C 180")
    v, a, da, b, db, c, dc = m.groups()
    rays = [(a, int(da)), (b, int(db)), (c, int(dc))]
    if len({v, a, b, c}) != 4 or not all(0 <= d <= 180 for _, d in rays):
        raise ValueError("four different letters; directions 0 to 180")
    return v, rays

def asked1(prompt):
    """The two angles asked, (name, measure): each ray with the one before it, as the book asks
    for BOA and COB."""
    v, rays = read1(prompt)
    return [(f"{rays[i + 1][0]}{v}{rays[i][0]}", abs(rays[i + 1][1] - rays[i][1])) for i in range(2)]

def t1_build(letters, dirs):
    v, a, b, c = letters
    return f"{v}; {a} {dirs[0]}, {b} {dirs[1]}, {c} {dirs[2]}"

def t1_ok(letters, dirs):
    d0, d1, d2 = dirs
    return (letters in NAMES1 and all(d in DIRS for d in dirs) and d0 in (0, 180)
            and (d0 < d1 < d2 if d0 == 0 else d0 > d1 > d2)
            and abs(d1 - d0) >= GAP1 and abs(d2 - d1) >= GAP1)

def t1_line(r):                                        # the book's: the third ray on the baseline too
    d0 = r.choice((0, 0, 180))
    d1 = r.choice([d for d in DIRS if GAP1 <= d <= 180 - GAP1 and d != 90])
    return dict(letters=r.choice(NAMES1 + (NAMES1[0],) * 2), dirs=(d0, d1, 180 - d0))

def t1_between(r):                                     # two rays off the baseline: subtract the readings
    d0 = r.choice((0, 180))
    d1, d2 = sorted(r.sample([d for d in DIRS if GAP1 <= d <= 180 - GAP1], 2))
    need(d2 - d1 >= GAP1)
    if d0 == 180:
        d1, d2 = d2, d1
    return dict(letters=r.choice(NAMES1), dirs=(d0, d1, d2))

def answer1(prompt):
    return ", ".join(f"m angle {names(n)} = {m} degree" for n, m in asked1(prompt))

def figure1(prompt, key, unit="1cm", text_scale=1.0):
    v, rays = read1(prompt)
    return fig.protractor([(d, f"${n}$") for n, d in rays], f"${v}$", unit=unit, text_scale=text_scale)

ANS1 = re.compile(r"^m angle ([A-Z]) ([A-Z]) ([A-Z]) = (\d+) degree, m angle ([A-Z]) ([A-Z]) ([A-Z]) = (\d+) degree$")

def check1(prompt, answer):
    v, rays = read1(prompt)
    m = ANS1.match(answer)
    if not m:
        return False
    g = m.groups()
    got = [("".join(g[0:3]), int(g[3])), ("".join(g[4:7]), int(g[7]))]
    want = asked1(prompt)
    # The measure taken off the rays as drawn: the angle between their directions.
    at = {n: u(d) for n, d in rays}
    for (name, val), (wname, _) in zip(got, want):
        if name != wname or name[1] != v:
            return False
        if not close(angle_at((0, 0), at[name[0]], at[name[2]]), val, 1e-6):
            return False
    return True

# ------------------------------------------------------------------
# Shared: segments, possibly tilted
# ------------------------------------------------------------------
SEGS = ("AB", "CD", "MN", "PQ", "RS", "JK", "EF", "GH", "BK", "UV")
TILTS = (-35, -30, -25, -20, -15, 15, 20, 25, 30, 35)

def tilt_text(t):
    return f", tilt {t}" if t else ""

# ------------------------------------------------------------------
# Type 2: copying a segment
# ------------------------------------------------------------------
LEN2 = tenths(2, 6)
RAYS2 = ("XY", "ST", "UV", "DE")
P2 = re.compile(rf"^([A-Z])([A-Z]) = ({NUM})(?:, tilt (-?\d+))?(?:; ray ([A-Z])([A-Z]))?$")

def read2(prompt):
    m = P2.match(prompt)
    if not m:
        raise ValueError("write it like: AB = 4, AB = 4.5, tilt 20, or AB = 4; ray XY")
    a, b, L, t, x, y = m.groups()
    L, t = float(L), int(t or 0)
    if a == b or L <= 0 or (x and len({a, b, x, y}) != 4):
        raise ValueError("different letters, a positive length")
    return a, b, L, t, (x, y) if x else None

def t2_build(seg, L, tilt=0, ray=None):
    return f"{seg} = {num(L)}{tilt_text(tilt)}" + (f"; ray {ray}" if ray else "")

def t2_ok(seg, L, tilt=0, ray=None):
    return (seg in SEGS and is_in(L, LEN2) and (tilt == 0 or tilt in TILTS)
            and (ray is None or (ray in RAYS2 and not set(ray) & set(seg))) and not (tilt and L > 5.5))

def t2_plain(r):                                       # problem 7
    return dict(seg=r.choice(SEGS[:6] + ("AB",) * 3), L=r.choice(LEN2))

def t2_tilted(r):
    return dict(seg=r.choice(SEGS), L=r.choice([v for v in LEN2 if v <= 5.5]), tilt=r.choice(TILTS))

def t2_ray(r):                                         # construction 2: on a ray XY that's given
    seg = r.choice(SEGS)
    ray = r.choice([q for q in RAYS2 if not set(q) & set(seg)])
    return dict(seg=seg, L=r.choice(LEN2), ray=ray)

def names2(prompt):
    a, b, L, t, ray = read2(prompt)
    x, y = ray or free({a, b}, "XYSTUV", 2)
    (p,) = free({a, b, x, y}, "PQWZ")
    return x, y, p

def build2(prompt):
    a, b, L, t, ray = read2(prompt)
    x, y, p = names2(prompt)
    e = u(t)
    A = (0.0, 0.0)
    B = add(A, e, L)
    low = min(A[1], B[1])
    X = (0.0, low - 1.5)
    Y = add(X, (1, 0), L + 1.0)
    P = add(X, (1, 0), L)
    n = normal(e)
    prims = [("seg", A, B, "", "given"), ("dot", A, "given"), ("dot", B, "given"),
             lab(A, add((0, 0), n, -LAB), a), lab(B, add((0, 0), n, -LAB), b)]
    who = "given" if ray else "key"
    prims += [("seg", X, add(Y, (1, 0), 0.6), "end", who), ("dot", X, who), ("dot", Y, who),
              lab(X, (0, -LAB), x, who), lab(Y, (0, -LAB), y, who),
              ("arc", X, L, -9, 9, "key"), ("dot", P, "key"), lab(P, (-0.25, -LAB), p, "key")]
    return prims, dict(A=A, B=B, X=X, Y=Y, P=P, arc=(X, L))

def answer2(prompt):
    a, b, L, _, _ = read2(prompt)
    x, _, p = names2(prompt)
    return f"{x} {p} = {a} {b} = {num(L)} \"cm\""

ANS2 = re.compile(rf'^([A-Z]) ([A-Z]\'?) = ([A-Z]) ([A-Z]) = ({NUM}) "cm"$')

def check2(prompt, answer):
    a, b, L, _, _ = read2(prompt)
    m = ANS2.match(answer)
    if not m:
        return False
    x, p, a2, b2, v = m.groups()
    _, g = build2(prompt)
    X, Y, P, A, B = g["X"], g["Y"], g["P"], g["A"], g["B"]
    return ((x, p) == names2(prompt)[::2] and {a2, b2} == {a, b}
            and close(float(v), dist(A, B), 0.005)                       # the original, as drawn
            and on_segment(P, X, add(Y, sub(Y, X), 1.0))                 # P on ray XY
            and close(dist(X, P), dist(A, B))                            # at the compass's opening
            and close(dist(g["arc"][0], P), g["arc"][1]))               # on the arc drawn

# ------------------------------------------------------------------
# Types 3 and 4: an angle (copied or bisected)
# ------------------------------------------------------------------
ANGLES = ("PQR", "BAC", "DEF", "KLM", "STU", "GHJ", "ABC", "RST")
MEAS3 = tuple(range(20, 121, 5))
MEAS4 = tuple(range(30, 161, 10))
SIDE_DIRS = tuple(range(-80, 81, 5))
SIDE = 3.0                                             # a drawn side's length
PT = 2.4                                               # where its letter's point is
P34 = re.compile(r"^([A-Z])([A-Z])([A-Z]) = (\d+), ([A-Z])([A-Z]) at (-?\d+)$")

def read_angle(prompt):
    """(first, vertex, last, measure, direction of the vertex-to-last side)."""
    m = P34.match(prompt)
    if not m:
        raise ValueError("write it like: PQR = 30, QR at -15")
    p, q, r_, meas, s0, s1, d = m.groups()
    if len({p, q, r_}) != 3 or (s0, s1) != (q, r_) or not 0 < int(meas) < 180:
        raise ValueError("the side after 'at' is the vertex and the last letter, like QR")
    return p, q, r_, int(meas), int(d)

def angle_build(name, meas, d):
    return f"{name} = {meas}, {name[1]}{name[2]} at {d}"

def bisector_ok(meas, d, lo, hi):
    return lo <= d + meas / 2 <= hi

def angle_given(prompt):
    """The given angle, its vertex at the origin: (prims, Q, the point on the first side, on the last)."""
    p, q, r_, meas, d = read_angle(prompt)
    Q = (0.0, 0.0)
    e1, e2 = u(d + meas), u(d)
    Pp, Rp = add(Q, e1, PT), add(Q, e2, PT)
    bis = u(d + meas / 2)
    prims = [("seg", Q, add(Q, e1, SIDE), "end", "given"), ("seg", Q, add(Q, e2, SIDE), "end", "given"),
             ("dot", Q, "given"), ("dot", Pp, "given"), ("dot", Rp, "given"),
             lab(Q, (-LAB * bis[0], -LAB * bis[1]), q),
             lab(Pp, add((0, 0), normal(e1), LAB), p),
             lab(Rp, add((0, 0), normal(e2), -LAB), r_)]
    return prims, Q, Pp, Rp

def t3_pick(r):
    meas = r.choice(MEAS3)
    d = r.choice([s for s in SIDE_DIRS if bisector_ok(meas, s, -30, 45)])
    return dict(name=r.choice(ANGLES), meas=meas, d=d)

def t3_sym(r):                                         # problem 8: the angle opens to the right, level
    meas = r.choice([m for m in MEAS3 if m % 10 == 0])
    return dict(name=r.choice(ANGLES), meas=meas, d=-meas // 2)

def t3_ok(name, meas, d):
    return name in ANGLES and meas in MEAS3 and d in SIDE_DIRS and bisector_ok(meas, d, -30, 45)

R3 = 1.5                                               # the compass's first opening
COPY_SIDE = 3.2

def names3(prompt):
    p, q, r_, _, _ = read_angle(prompt)
    used = {p, q, r_}
    x, y = free(used, "XYSTUVW", 2)
    m, n = free(used | {x, y}, "MNKLGH", 2)
    (z,) = free(used | {x, y, m, n}, "ZWJ")
    return x, y, m, n, z, p + "'"

def build3(prompt):
    p, q, r_, meas, d = read_angle(prompt)
    x, y, mm, nn, z, pp = names3(prompt)
    prims, Q, Pp, Rp = angle_given(prompt)
    xs = [pt[1][0] for pt in prims if pt[0] in ("seg", "dot")] + [pt[2][0] for pt in prims if pt[0] == "seg"]
    ys = [pt[1][1] for pt in prims if pt[0] in ("seg", "dot")] + [pt[2][1] for pt in prims if pt[0] == "seg"]
    X = (max(xs) + 1.0 + max(0.0, -math.cos(math.radians(meas))) * COPY_SIDE, min(ys))
    M, N = add(Q, u(d), R3), add(Q, u(d + meas), R3)
    Z = add(X, (1, 0), R3)
    mn = dist(M, N)
    P2 = add(X, u(meas), R3)
    Y = add(X, (1, 0), COPY_SIDE - 0.5)
    prims += [("arc", Q, R3, d - 10, d + meas + 10, "key"), lab(M, add((0, 0), normal(u(d)), -0.3), mm, "key"),
              lab(N, add((0, 0), normal(u(d + meas)), 0.3), nn, "key"),
              ("seg", X, add(X, (1, 0), COPY_SIDE), "end", "key"), ("seg", X, add(X, u(meas), COPY_SIDE), "end", "key"),
              ("dot", X, "key"), ("dot", Y, "key"), lab(X, (-0.3, -0.25), x, "key"), lab(Y, (0, -LAB), y, "key"),
              ("arc", X, R3, -10, meas + 12, "key"), ("arc", Z, mn, direction(Z, P2) - 14, direction(Z, P2) + 14, "key"),
              ("dot", Z, "key"), ("dot", P2, "key"), lab(Z, (0.25, -0.3), z, "key"),
              lab(P2, add((0, 0), u(meas + 90), 0.4), pp, "key")]
    return prims, dict(Q=Q, P=Pp, R=Rp, X=X, Y=Y, Z=Z, P2=P2, M=M, N=N, r=R3, mn=mn)

def answer3(prompt):
    p, q, r_, meas, _ = read_angle(prompt)
    x, y, _, _, _, pp = names3(prompt)
    return f"m angle {pp} {x} {y} = m angle {p} {q} {r_} = {meas} degree"

ANS3 = re.compile(r"^m angle ([A-Z]') ([A-Z]) ([A-Z]) = m angle ([A-Z]) ([A-Z]) ([A-Z]) = (\d+) degree$")

def check3(prompt, answer):
    p, q, r_, meas, _ = read_angle(prompt)
    m = ANS3.match(answer)
    if not m:
        return False
    pp, x, y, a, b, c, v = m.groups()
    nm = names3(prompt)
    if (pp, x, y) != (nm[5], nm[0], nm[1]) or (a, b, c) not in ((p, q, r_), (r_, q, p)):
        return False
    _, g = build3(prompt)
    orig = angle_at(g["Q"], g["P"], g["R"])
    return (close(int(v), orig, 1e-6)
            and close(dist(g["Q"], g["M"]), g["r"]) and close(dist(g["Q"], g["N"]), g["r"])
            and close(dist(g["X"], g["Z"]), g["r"]) and close(dist(g["X"], g["P2"]), g["r"])
            and close(dist(g["Z"], g["P2"]), dist(g["M"], g["N"]))     # the arc of radius MN
            and close(angle_at(g["X"], g["P2"], g["Y"]), orig)
            and g["mn"] > 0.5)                                          # arcs far enough apart to read

def t4_pick(r):
    meas = r.choice(MEAS4)
    d = r.choice([s for s in SIDE_DIRS if bisector_ok(meas, s, -30, 60)])
    return dict(name=r.choice(ANGLES), meas=meas, d=d)

def t4_ok(name, meas, d):
    return name in ANGLES and meas in MEAS4 and d in SIDE_DIRS and bisector_ok(meas, d, -30, 60)

R4 = 1.4

def names4(prompt):
    p, q, r_, _, _ = read_angle(prompt)
    (dd,) = free({p, q, r_}, "DEFGHJ")
    return dd

def build4(prompt):
    p, q, r_, meas, d = read_angle(prompt)
    dd = names4(prompt)
    prims, Q, Pp, Rp = angle_given(prompt)
    S1, S2 = add(Q, u(d), R4), add(Q, u(d + meas), R4)
    w = dist(S1, S2)
    r2 = max(1.1, 0.8 * w)
    D = max(meet(S1, r2, S2, r2), key=lambda c: dist(Q, c))   # the crossing beyond the first arc
    need(crosses(S1, r2, S2, r2))
    reach = max(SIDE + 0.3, dist(Q, D) + 0.6)
    bis = u(d + meas / 2)
    prims += [("arc", Q, R4, d - 8, d + meas + 8, "key"),
              ("arc", S1, r2, direction(S1, D) - 12, direction(S1, D) + 12, "key"),
              ("arc", S2, r2, direction(S2, D) - 12, direction(S2, D) + 12, "key"),
              ("seg", Q, add(Q, bis, reach), "end", "key"), ("dot", D, "key"),
              lab(D, add((0, 0), normal(bis), 0.35), dd, "key")]
    return prims, dict(Q=Q, P=Pp, R=Rp, S1=S1, S2=S2, D=D, r=R4, r2=r2)

def answer4(prompt):
    p, q, r_, meas, _ = read_angle(prompt)
    dd = names4(prompt)
    return f"m angle {p} {q} {dd} = m angle {dd} {q} {r_} = {num(meas / 2)} degree"

ANS4 = re.compile(rf"^m angle ([A-Z]) ([A-Z]) ([A-Z]) = m angle ([A-Z]) ([A-Z]) ([A-Z]) = ({NUM}) degree$")

def check4(prompt, answer):
    p, q, r_, meas, _ = read_angle(prompt)
    m = ANS4.match(answer)
    if not m:
        return False
    a, b, c, e, f, g_, v = m.groups()
    dd = names4(prompt)
    if (a, b, c, e, f, g_) != (p, q, dd, dd, q, r_):
        return False
    _, g = build4(prompt)
    whole = angle_at(g["Q"], g["P"], g["R"])
    half1, half2 = angle_at(g["Q"], g["P"], g["D"]), angle_at(g["Q"], g["D"], g["R"])
    return (close(float(v), whole / 2, 1e-6) and close(half1, half2) and close(half1 + half2, whole)
            and close(dist(g["Q"], g["S1"]), dist(g["Q"], g["S2"]))
            and close(dist(g["S1"], g["D"]), dist(g["S2"], g["D"])))

# ------------------------------------------------------------------
# Type 5: the perpendicular bisector
# ------------------------------------------------------------------
LEN5 = tenths(3, 6.5)
P5 = re.compile(rf"^([A-Z])([A-Z]) = ({NUM})(?:, tilt (-?\d+))?$")

def read5(prompt):
    m = P5.match(prompt)
    if not m:
        raise ValueError("write it like: MN = 6, or MN = 5, tilt -20")
    a, b, L, t = m.groups()
    if a == b or float(L) <= 0:
        raise ValueError("two different letters, a positive length")
    return a, b, float(L), int(t or 0)

def t5_build(seg, L, tilt=0):
    return f"{seg} = {num(L)}{tilt_text(tilt)}"

def t5_ok(seg, L, tilt=0):
    return seg in SEGS and is_in(L, LEN5) and (tilt == 0 or tilt in TILTS)

def t5_plain(r):                                       # construction 5, problem 9
    return dict(seg=r.choice(SEGS + ("MN", "BK")), L=r.choice(LEN5))

def t5_tilted(r):
    return dict(seg=r.choice(SEGS), L=r.choice(LEN5), tilt=r.choice(TILTS))

def names5(prompt):
    a, b, _, _ = read5(prompt)
    return free({a, b}, "DOEFGH")[0]

def build5(prompt):
    a, b, L, t = read5(prompt)
    dd = names5(prompt)
    e = u(t)
    n = normal(e)
    M = (0.0, 0.0)
    N = add(M, e, L)
    r = 0.72 * L
    U, V = meet(M, r, N, r)                             # above, below
    mid = add(M, e, L / 2)
    prims = [("seg", M, N, "", "given"), ("dot", M, "given"), ("dot", N, "given"),
             lab(M, add((0, 0), e, -LAB), a), lab(N, add((0, 0), e, LAB), b)]
    for c in (M, N):
        for t_ in (U, V):
            prims.append(("arc", c, r, direction(c, t_) - 10, direction(c, t_) + 10, "key"))
    prims += [("seg", add(V, n, -0.5), add(U, n, 0.5), "", "key"), ("box", mid, e, n, "key"),
              ("dot", mid, "key"), lab(mid, add(add((0, 0), e, -0.3), n, -0.32), dd, "key")]
    return prims, dict(M=M, N=N, U=U, V=V, D=mid, r=r)

def answer5(prompt):
    a, b, L, _ = read5(prompt)
    dd = names5(prompt)
    return f"{a} {dd} = {dd} {b} = {num(L / 2)} \"cm\""

ANS5 = re.compile(rf'^([A-Z]) ([A-Z]) = ([A-Z]) ([A-Z]) = ({NUM}) "cm"$')

def check5(prompt, answer):
    a, b, L, _ = read5(prompt)
    m = ANS5.match(answer)
    if not m:
        return False
    a2, d1, d2, b2, v = m.groups()
    if (a2, b2) != (a, b) or d1 != d2 or d1 != names5(prompt):
        return False
    _, g = build5(prompt)
    M, N, U, V, D = g["M"], g["N"], g["U"], g["V"], g["D"]
    return (close(dist(U, M), dist(U, N)) and close(dist(V, M), dist(V, N))   # on the bisector
            and g["r"] > dist(M, N) / 2                                        # the arcs meet
            and close(dot(sub(U, V), sub(N, M)), 0)                            # at right angles
            and on_segment(D, U, V) and on_segment(D, M, N)                     # D where they cross
            and close(float(v), dist(M, D), 0.005) and close(dist(M, D), dist(D, N)))

# ------------------------------------------------------------------
# Type 6: a perpendicular at a point on a line
# ------------------------------------------------------------------
LEN6 = tenths(5, 7)
AT6 = tenths(2, 5)
SEG6 = ("RS", "AC", "EF", "GH", "JK", "MN", "TV")
POINT6 = ("P", "Q", "B", "O")
P6 = re.compile(rf"^(segment|line) ([A-Z])([A-Z]) = ({NUM}), ([A-Z]) at ({NUM})(?:, tilt (-?\d+))?$")

def read6(prompt):
    m = P6.match(prompt)
    if not m:
        raise ValueError("write it like: segment RS = 6.5, P at 2.5, or line AC = 6, P at 2")
    kind, a, b, L, p, x, t = m.groups()
    L, x = float(L), float(x)
    if len({a, b, p}) != 3 or not 0 < x < L:
        raise ValueError("three different letters; the point between the ends")
    return kind, a, b, L, p, x, int(t or 0)

def t6_build(kind, seg, L, p, x, tilt=0):
    return f"{kind} {seg} = {num(L)}, {p} at {num(x)}{tilt_text(tilt)}"

def t6_ok(kind, seg, L, p, x, tilt=0):
    return (kind in ("segment", "line") and seg in SEG6 and p in POINT6 and p not in seg and is_in(L, LEN6)
            and is_in(x, AT6) and 2 <= x <= L - 2 and (kind == "segment" or L <= 6) and (tilt == 0 or (tilt in TILTS and kind == "segment")))

def t6_pick(kind, tilted=False):
    def pick(r):
        seg = r.choice(SEG6)
        L = r.choice(LEN6 if kind == "segment" else [v for v in LEN6 if v <= 6])   # a line's arrows need room
        return dict(kind=kind, seg=seg, L=L, p=r.choice([q for q in POINT6 + ("P",) * 3 if q not in seg]),
                    x=r.choice([v for v in AT6 if 2 <= v <= L - 2]),
                    tilt=r.choice(TILTS) if tilted else 0)
    return pick

def names6(prompt):
    _, a, b, _, p, _, _ = read6(prompt)
    used = {a, b, p}
    m, n = free(used, "MNKLGH", 2)
    (d,) = free(used | {m, n}, "DEFQTW")
    return m, n, d

def build6(prompt):
    kind, a, b, L, p, x, t = read6(prompt)
    mm, nn, dd = names6(prompt)
    e = u(t)
    n = normal(e)
    A = (0.0, 0.0)
    B = add(A, e, L)
    P = add(A, e, x)
    d = min(1.3, 0.6 * min(x, L - x))
    M, N = add(P, e, -d), add(P, e, d)
    r = 1.7 * d
    D, _ = meet(M, r, N, r)
    if kind == "line":
        prims = [("seg", add(A, e, -0.4), add(B, e, 0.4), "both", "given")]
    else:
        prims = [("seg", A, B, "", "given")]
    off = add((0, 0), n, -LAB)
    prims += [("dot", A, "given"), ("dot", B, "given"), ("dot", P, "given"),
              lab(A, off, a), lab(B, off, b), lab(P, add(off, e, 0.12), p),
              ("arc", P, d, direction(P, M) - 16, direction(P, M) + 16, "key"),
              ("arc", P, d, direction(P, N) - 16, direction(P, N) + 16, "key"),
              lab(M, add(add((0, 0), n, LAB), e, -0.2), mm, "key"), lab(N, add(add((0, 0), n, LAB), e, 0.2), nn, "key"),
              ("arc", M, r, direction(M, D) - 11, direction(M, D) + 11, "key"),
              ("arc", N, r, direction(N, D) - 11, direction(N, D) + 11, "key"),
              ("seg", P, add(D, n, 0.6), "", "key"), ("box", P, e, n, "key"), ("dot", D, "key"),
              lab(D, add((0, 0), e, 0.35), dd, "key")]
    return prims, dict(A=A, B=B, P=P, M=M, N=N, D=D)

def answer6(prompt):
    kind, a, b, _, p, _, _ = read6(prompt)
    _, _, dd = names6(prompt)
    wrap = "overline" if kind == "segment" else "arrow.l.r"
    return f"overline({p} {dd}) perp {wrap}({a} {b})"

ANS6 = re.compile(r"^overline\(([A-Z]) ([A-Z])\) perp (overline|arrow\.l\.r)\(([A-Z]) ([A-Z])\)$")

def check6(prompt, answer):
    kind, a, b, _, p, _, _ = read6(prompt)
    m = ANS6.match(answer)
    if not m:
        return False
    p2, d2, wrap, a2, b2 = m.groups()
    if (p2, d2) != (p, names6(prompt)[2]) or {a2, b2} != {a, b} or (wrap == "overline") != (kind == "segment"):
        return False
    _, g = build6(prompt)
    A, B, P, M, N, D = (g[k] for k in "ABPMND")
    return (on_segment(P, A, B) and on_segment(M, A, B) and on_segment(N, A, B)   # the arcs cross the drawn segment
            and close(dist(P, M), dist(P, N)) and close(dist(D, M), dist(D, N))
            and dist(D, M) > dist(P, M) + 0.3                                    # wider than the first arcs
            and close(dot(sub(D, P), sub(B, A)), 0) and dist(D, P) > 0.5)

# ------------------------------------------------------------------
# Types 7 and 9: a line and a point off it
# ------------------------------------------------------------------
LINE7 = tuple(round(6 + 0.1 * i, 1) for i in range(13))     # 6.0 to 7.2
OFF7 = tuple(round(1.2 + 0.1 * i, 1) for i in range(15))    # 1.2 to 2.6 off the line
LINES7 = ("EF", "AB", "CD", "GH", "LM", "JK")
P7 = re.compile(rf"^line ([A-Z])([A-Z]) = ({NUM}), ([A-Z]) at ({NUM}), ({NUM}) (above|below)$")

def read7(prompt):
    m = P7.match(prompt)
    if not m:
        raise ValueError("write it like: line EF = 7.2, P at 3.6, 2.2 above")
    a, b, L, p, x, h, side = m.groups()
    L, x, h = float(L), float(x), float(h)
    if len({a, b, p}) != 3 or not 0 < x < L or h <= 0:
        raise ValueError("three different letters; P's foot between E and F, a distance off the line")
    return a, b, L, p, x, h if side == "above" else -h

def t7_build(line, L, p, x, h):
    return f"line {line} = {num(L)}, {p} at {num(x)}, {num(abs(h))} {'above' if h > 0 else 'below'}"

def t7_ok(line, L, p, x, h):
    return (line in LINES7 and p in POINT6 and p not in line and L in LINE7 and abs(h) in OFF7
            and round(x * 10) == x * 10 and 2.0 <= x <= L - 2.0)

def t7_pick(r):
    L = r.choice(LINE7)
    line = r.choice(LINES7 + ("EF",))
    return dict(line=line, L=L, p=r.choice([q for q in POINT6 + ("P",) * 3 if q not in line]),
                x=round(r.randint(20, round(L * 10) - 20) / 10, 1),
                h=r.choice(OFF7) * (1 if r.random() < 0.7 else -1))

def names7(prompt):
    a, b, _, p, _, _ = read7(prompt)
    used = {a, b, p}
    r_, s = free(used, "RSTUVW", 2)
    (d,) = free(used | {r_, s}, "DOGHKN")
    return r_, s, d

def build7(prompt):
    a, b, L, p, x, h = read7(prompt)
    rr, ss, dd = names7(prompt)
    E, F = (0.0, 0.0), (L, 0.0)
    P = (x, h)
    D = (x, 0.0)
    rad = 1.3 * abs(h)
    w = math.sqrt(rad * rad - h * h)
    R, S = (x - w, 0.0), (x + w, 0.0)
    r2 = rad
    up = 1 if h > 0 else -1
    Q = (x, -up * math.sqrt(r2 * r2 - w * w))           # the second arcs, across the line from P
    below = (0, -LAB) if h > 0 else (0, LAB)
    prims = [("seg", (-0.7, 0.0), (L + 0.7, 0.0), "both", "given"), ("dot", E, "given"), ("dot", F, "given"),
             ("dot", P, "given"), lab(E, below, a), lab(F, below, b), lab(P, (0.35, 0.1), p),
             ("arc", P, rad, direction(P, R) - 9, direction(P, R) + 9, "key"),
             ("arc", P, rad, direction(P, S) - 9, direction(P, S) + 9, "key"),
             lab(R, (-0.2, below[1]), rr, "key"), lab(S, (0.2, below[1]), ss, "key"),
             ("arc", R, r2, direction(R, Q) - 10, direction(R, Q) + 10, "key"),
             ("arc", S, r2, direction(S, Q) - 10, direction(S, Q) + 10, "key"),
             ("seg", add(P, (0, up), 0.3), add(Q, (0, -up), 0.4), "", "key"), ("box", D, (1, 0), (0, up), "key"),
             lab(D, (-0.3, -below[1]), dd, "key")]
    return prims, dict(E=E, F=F, P=P, D=D, R=R, S=S, Q=Q)

def answer7(prompt):
    a, b, _, p, _, h = read7(prompt)
    _, _, dd = names7(prompt)
    return f"overline({p} {dd}) perp arrow.l.r({a} {b}), {p} {dd} = {num(abs(h))} \"cm\""

ANS7 = re.compile(rf'^overline\(([A-Z]) ([A-Z])\) perp arrow\.l\.r\(([A-Z]) ([A-Z])\), ([A-Z]) ([A-Z]) = ({NUM}) "cm"$')

def check7(prompt, answer):
    a, b, _, p, _, _ = read7(prompt)
    m = ANS7.match(answer)
    if not m:
        return False
    p1, d1, a2, b2, p2, d2, v = m.groups()
    dd = names7(prompt)[2]
    if (p1, d1, p2, d2) != (p, dd, p, dd) or {a2, b2} != {a, b}:
        return False
    _, g = build7(prompt)
    E, F, P, D, R, S, Q = (g[k] for k in "EFPDRSQ")
    line = lambda X: abs(cross(sub(F, E), sub(X, E))) < TOL
    return (line(R) and line(S) and line(D) and close(dist(P, R), dist(P, S))
            and close(dist(Q, R), dist(Q, S)) and abs(cross(sub(Q, P), sub(D, P))) < TOL   # P, D, Q in a line
            and close(dot(sub(P, D), sub(F, E)), 0) and dist(R, S) > 1.0
            and close(float(v), dist(P, D), 0.005) and -0.7 < R[0] and S[0] < F[0] + 0.7)

LINE9 = tenths(6, 7)
OFF9 = tenths(1.5, 3)
AT9 = tenths(2.5, 5)
P9 = re.compile(rf"^line ({NUM}), ([A-Z]) at ({NUM}), ({NUM}) (above|below)$")

def read9(prompt):
    m = P9.match(prompt)
    if not m:
        raise ValueError("write it like: line 7, P at 2.5, 2.5 above")
    L, p, x, h, side = m.groups()
    L, x, h = float(L), float(x), float(h)
    if not 0 < x < L or h <= 0:
        raise ValueError("P's foot on the line, a distance off it")
    return L, p, x, h if side == "above" else -h

def t9_build(L, p, x, h):
    return f"line {num(L)}, {p} at {num(x)}, {num(abs(h))} {'above' if h > 0 else 'below'}"

def t9_ok(L, p, x, h):
    return p in POINT6 and is_in(L, LINE9) and is_in(abs(h), OFF9) and is_in(x, AT9) and x <= L - 1.5

def t9_pick(r):
    L = r.choice(LINE9)
    return dict(L=L, p=r.choice(POINT6 + ("P",) * 3), x=r.choice([v for v in AT9 if v <= L - 1.5]),
                h=r.choice(OFF9) * (1 if r.random() < 0.7 else -1))

TRANSVERSAL = 60                                      # the key's angle A, at X

def names9(prompt):
    _, p, _, _ = read9(prompt)
    x, q = free({p}, "XQYZ", 2)
    return x, q

def build9(prompt):
    L, p, xp, h = read9(prompt)
    xx, qq = names9(prompt)
    up = 1 if h > 0 else -1
    P = (xp, h)
    w = u(TRANSVERSAL * up)                            # X to P
    X = (xp - abs(h) / math.tan(math.radians(TRANSVERSAL)), 0.0)
    r = 0.9
    X1, X2 = add(X, (1, 0), r), add(X, w, r)            # angle A's arc about X: on the line, on XP
    P2 = add(P, w, r)                                   # the same arc about P, on the transversal beyond P
    # The arc of radius X1X2 about P2 crosses the arc about P twice; angle A copied is the crossing
    # on the same side of the transversal as X1.
    Q = min(meet(P, r, P2, dist(X1, X2)), key=lambda c: cross(w, sub(c, P)) * cross(w, sub(X1, X)) < 0)
    end = lambda pt, k: add(pt, w, k)
    a0, a1 = sorted((0, TRANSVERSAL * up))
    prims = [("seg", (0.0, 0.0), (L, 0.0), "both", "given"), ("dot", P, "given"),
             lab(P, (-0.35, 0.25 * up), p),
             ("seg", end(X, -0.9), end(P, 1.1), "", "key"), ("dot", X, "key"), lab(X, (-0.3, -0.3 * up), xx, "key"),
             ("arc", X, r, a0 - 8, a1 + 8, "key"), ("arc", P, r, a0 - 8, a1 + 8, "key"),
             ("arc", P2, dist(X1, X2), direction(P2, Q) - 14, direction(P2, Q) + 14, "key"),
             lab(add(X, u(TRANSVERSAL * up / 2), 0.55), (0, 0), "A", "key"),
             lab(add(P, u(TRANSVERSAL * up / 2), 0.55), (0, 0), "A", "key"),
             ("seg", (P[0] - xp, h), (P[0] - xp + L, h), "both", "key"), ("dot", Q, "key"),
             lab(Q, (0.3, 0.3 * up), qq, "key")]
    return prims, dict(P=P, X=X, X1=X1, X2=X2, P2=P2, Q=Q, line=((0.0, 0.0), (L, 0.0)))

def answer9(prompt):
    _, p, _, _ = read9(prompt)
    _, qq = names9(prompt)
    return f"arrow.l.r({p} {qq}) parallel \"the given line\""

ANS9 = re.compile(r'^arrow\.l\.r\(([A-Z]) ([A-Z])\) parallel "the given line"$')

def check9(prompt, answer):
    _, p, _, _ = read9(prompt)
    m = ANS9.match(answer)
    if not m or m.groups() != (p, names9(prompt)[1]):
        return False
    _, g = build9(prompt)
    (L0, L1), P, X, X1, X2, P2, Q = g["line"], g["P"], g["X"], g["X1"], g["X2"], g["P2"], g["Q"]
    d = sub(L1, L0)
    return (abs(cross(d, sub(X, L0))) < TOL and 0 < X[0] < L1[0]                       # X on the line, as drawn
            and abs(cross(sub(P, X), sub(P2, X))) < TOL                                   # P2 on line XP
            and close(dist(P, Q), dist(X, X1)) and close(dist(P2, Q), dist(X1, X2))     # the copied arc
            and close(angle_at(P, Q, P2), angle_at(X, X1, X2))                          # angle A again
            and abs(cross(d, sub(Q, P))) < TOL and dist(P, Q) > 0.5)                     # so PQ is parallel

# ------------------------------------------------------------------
# Type 8: a triangle from its three sides
# ------------------------------------------------------------------
SIDES8 = tenths(1.5, 6)
SMALL8 = (("a", "b", "c"), ("x", "y", "z"), ("p", "q", "r"))
BIG8 = (("BC", "AX", "MN"), ("AB", "CD", "EF"), ("PQ", "RS", "TU"), ("GH", "JK", "LM"))
MARGIN8 = 0.8                                          # the two shorter sides add to this much more than the longest
MIN_ANGLE8 = 20
P8 = re.compile(rf"^([a-z]|[A-Z][A-Z]) = ({NUM}), ([a-z]|[A-Z][A-Z]) = ({NUM}), ([a-z]|[A-Z][A-Z]) = ({NUM})$")

def read8(prompt):
    m = P8.match(prompt)
    if not m:
        raise ValueError("write it like: a = 2, b = 3, c = 4, or BC = 3, AX = 4, MN = 5")
    g = m.groups()
    sides = [(g[i], float(g[i + 1])) for i in (0, 2, 4)]
    ns = [n for n, _ in sides]
    if len(set(ns)) != 3 or len({len(n) for n in ns}) != 1 or (len(ns[0]) == 2 and len(set("".join(ns))) != 6):
        raise ValueError("three different names, all one small letter or all two capitals")
    return sides

def tri_angles(a, b, c):
    """The smallest angle, None if the sides don't make a triangle."""
    if not (a + b > c and a + c > b and b + c > a):
        return None
    A = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
    B = math.degrees(math.acos((a * a + c * c - b * b) / (2 * a * c)))
    return min(A, B, 180 - A - B)

def t8_build(labels, lengths):
    return ", ".join(f"{n} = {num(v)}" for n, v in zip(labels, lengths))

def t8_fits(lengths):
    x, y, z = sorted(lengths)
    small = tri_angles(x, y, z)
    return small is not None and x + y - z >= MARGIN8 - 1e-9 and small >= MIN_ANGLE8

def t8_ok(labels, lengths):
    return (labels in SMALL8 + BIG8 and all(is_in(v, SIDES8) for v in lengths)
            and list(lengths) == sorted(lengths) and len(set(lengths)) == 3 and t8_fits(lengths))

def t8_pick(big):
    def pick(r):
        lengths = sorted(r.sample(SIDES8, 3))
        need(t8_fits(lengths))
        return dict(labels=r.choice(BIG8 if big else SMALL8 + (("a", "b", "c"),) * 2), lengths=tuple(lengths))
    return pick

GAP8 = 0.85                                            # between the given segments (more with letters below)

def build8(prompt):
    sides = read8(prompt)
    small = len(sides[0][0]) == 1
    prims, y = [], 0.0
    for n, v in sides:
        A, B = (0.0, y), (v, y)
        prims += [("seg", A, B, "", "given"), ("dot", A, "given"), ("dot", B, "given")]
        if small:
            prims.append(lab((v / 2, y), (0, 0.3), n))
        else:
            prims += [lab(A, (0, -0.33), n[0]), lab(B, (0, -0.33), n[1])]
        y -= GAP8 if small else 1.0
    # The key: the longest laid down, the middle one swung from its left end, the shortest from its right.
    order = sorted(range(3), key=lambda i: sides[i][1])
    (na, a), (nb, b), (nc, c) = (sides[i] for i in order)
    base = y - 0.4 - max(a, b) * 0.95
    V1, V2 = (0.0, base), (c, base)
    V3, _ = meet(V1, b, V2, a)                          # above the base
    need(crosses(V1, b, V2, a, margin=0.2))
    prims += [("seg", V1, (c + 0.8, base), "end", "key"), ("seg", V1, V3, "", "key"), ("seg", V2, V3, "", "key"),
              ("dot", V1, "key"), ("dot", V2, "key"), ("dot", V3, "key"),
              ("arc", V1, b, direction(V1, V3) - 13, direction(V1, V3) + 13, "key"),
              ("arc", V2, a, direction(V2, V3) - 18, direction(V2, V3) + 18, "key")]
    for (p, q), n in (((V1, V2), nc), ((V1, V3), nb), ((V2, V3), na)):
        mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        e = sub(q, p)
        k = 1 / math.hypot(*e)
        out = normal((e[0] * k, e[1] * k))
        cen = ((V1[0] + V2[0] + V3[0]) / 3, (V1[1] + V2[1] + V3[1]) / 3)
        if dot(out, sub(cen, mid)) > 0:
            out = (-out[0], -out[1])
        prims.append(lab(mid, (0.32 * out[0], 0.32 * out[1]), side_name(n), "key"))
    return prims, dict(V=(V1, V2, V3), sides={nc: (V1, V2), nb: (V1, V3), na: (V2, V3)})

def side_name(n):
    return n if len(n) == 1 else names(n)

def answer8(prompt):
    return ", ".join(f"{side_name(n)} = {num(v)} \"cm\"" for n, v in read8(prompt))

ANS8_ITEM = re.compile(rf'^([a-z]|[A-Z] [A-Z]) = ({NUM}) "cm"$')

def check8(prompt, answer):
    sides = read8(prompt)
    items = [ANS8_ITEM.match(s.strip()) for s in answer.split(",")]
    if len(items) != 3 or not all(items):
        return False
    got = [(m.group(1).replace(" ", ""), float(m.group(2))) for m in items]
    if [n for n, _ in got] != [n for n, _ in sides]:
        return False
    _, g = build8(prompt)
    # The given segments as drawn are the lengths; the key's triangle has them for its sides.
    return all(close(v, w, 0.005) and close(dist(*g["sides"][n]), w) for (n, v), (_, w) in zip(got, sides))

# ------------------------------------------------------------------
# Type 10: dividing a segment into equal parts
# ------------------------------------------------------------------
LEN10 = tenths(3, 7)
PARTS = (2, 3, 4, 5)
WORDS = {2: "two", 3: "three", 4: "four", 5: "five"}
SEG10 = ("AB", "CD", "MN", "PQ", "JK", "EF")
P10 = re.compile(rf"^([A-Z])([A-Z]) = ({NUM}), (\d) parts$")
RAY10 = -30                                            # the ray from A, in degrees from AB

def read10(prompt):
    m = P10.match(prompt)
    if not m:
        raise ValueError("write it like: AB = 6, 3 parts")
    a, b, L, n = m.groups()
    if a == b or float(L) <= 0 or not 2 <= int(n) <= 9:
        raise ValueError("two different letters, a positive length, 2 to 9 parts")
    return a, b, float(L), int(n)

def t10_build(seg, L, n):
    return f"{seg} = {num(L)}, {n} parts"

def nice10(L, n):
    return round(L * 10) % n == 0 and L / n >= 1.0

def t10_ok(seg, L, n):
    return seg in SEG10 and is_in(L, LEN10) and n in PARTS and nice10(L, n)

def t10_pick(r):
    n = r.choice(PARTS + (3, 3))
    L = r.choice([v for v in LEN10 if nice10(v, n)] or [None])
    need(L is not None)
    return dict(seg=r.choice(SEG10 + ("AB",) * 2), L=L, n=n)

def names10(prompt):
    a, b, _, n = read10(prompt)
    marks = free({a, b}, "RSTUVW", n)
    (p,) = free({a, b} | set(marks), "PQOZ")
    pts = free({a, b, p} | set(marks), "XYZWDEFGH", n - 1)
    return marks, p, pts

def build10(prompt):
    a, b, L, n = read10(prompt)
    marks, pp, pts = names10(prompt)
    A, B = (0.0, 0.0), (L, 0.0)
    e = u(RAY10)
    s = 0.95 * L / n
    M = [add(A, e, s * k) for k in range(1, n + 1)]
    Tn = M[-1]
    tb = sub(B, Tn)
    Xs = []
    for k in range(n - 1):
        R = M[k]
        t = -R[1] / tb[1]                               # R + t (B - T) on AB (y = 0)
        Xs.append(add(R, tb, t))
    prims = [("seg", A, B, "", "given"), ("dot", A, "given"), ("dot", B, "given"),
             lab(A, (-0.35, 0.1), a), lab(B, (0.35, 0.1), b),
             ("seg", A, add(A, e, s * n + 0.9), "end", "key"), ("dot", add(A, e, s * n + 0.5), "key"),
             lab(add(A, e, s * n + 0.5), (0.3, 0.25), pp, "key"), ("seg", Tn, B, "", "key")]
    prev = A
    for k, (R, m) in enumerate(zip(M, marks)):
        prims += [("arc", prev, s, RAY10 - 9, RAY10 + 9, "key"), ("dot", R, "key"),
                  lab(R, (-0.15, -0.38), m, "key")]
        prev = R
    for R, X, m in zip(M, Xs, pts):
        prims += [("seg", R, X, "", "key"), ("dot", X, "key"), lab(X, (0, 0.33), m, "key")]
    return prims, dict(A=A, B=B, M=M, T=Tn, X=Xs, s=s)

def answer10(prompt):
    a, b, L, n = read10(prompt)
    _, _, pts = names10(prompt)
    chain = [a] + pts + [b]
    return " = ".join(f"{chain[i]} {chain[i + 1]}" for i in range(n)) + f" = {num(L / n)} \"cm\""

def check10(prompt, answer):
    a, b, L, n = read10(prompt)
    *pairs, last = [s.strip() for s in answer.split("=")]
    m = re.match(rf'^({NUM}) "cm"$', last)
    if not m or len(pairs) != n or not all(re.match(r"^[A-Z] [A-Z]$", s) for s in pairs):
        return False
    chain = [pairs[0][0]] + [s[2] for s in pairs]
    if any(pairs[i][2] != pairs[i + 1][0] for i in range(n - 1)) or chain != [a] + names10(prompt)[2] + [b]:
        return False
    _, g = build10(prompt)
    A, B, M, Tn, Xs, s = g["A"], g["B"], g["M"], g["T"], g["X"], g["s"]
    pts = [A] + Xs + [B]
    pieces = [dist(pts[i], pts[i + 1]) for i in range(n)]
    tb = sub(B, Tn)
    return (all(close(dist(A, R), s * (k + 1)) for k, R in enumerate(M))           # equal compass steps
            and all(on_segment(X, A, B) for X in Xs)
            and all(abs(cross(sub(X, R), tb)) < TOL for R, X in zip(M, Xs))       # each parallel to TB
            and all(close(q, pieces[0]) for q in pieces) and close(float(m.group(1)), pieces[0], 0.005))

# ------------------------------------------------------------------
# Templates and ranges
# ------------------------------------------------------------------
def t3_build(name, meas, d):
    return angle_build(name, meas, d)

def t4_build(name, meas, d):
    return angle_build(name, meas, d)

TEMPLATES = {
    "1": [(t1_line, t1_build), (t1_line, t1_build), (t1_between, t1_build)],
    "2": [(t2_plain, t2_build), (t2_tilted, t2_build), (t2_ray, t2_build)],
    "3": [(t3_sym, t3_build), (t3_pick, t3_build), (t3_pick, t3_build)],
    "4": [(t4_pick, t4_build)],
    "5": [(t5_plain, t5_build), (t5_plain, t5_build), (t5_tilted, t5_build)],
    "6": [(t6_pick("segment"), t6_build), (t6_pick("segment", True), t6_build), (t6_pick("line"), t6_build)],
    "7": [(t7_pick, t7_build)],
    "8": [(t8_pick(False), t8_build), (t8_pick(False), t8_build), (t8_pick(True), t8_build)],
    "9": [(t9_pick, t9_build)],
    "10": [(t10_pick, t10_build)],
}

RANGES = {t1_build: t1_ok, t2_build: t2_ok, t3_build: t3_ok, t4_build: t4_ok, t5_build: t5_ok,
          t6_build: t6_ok, t7_build: t7_ok, t8_build: t8_ok, t9_build: t9_ok, t10_build: t10_ok}

def in_range(build, params):
    """Can a random draw pick these parameters for this build?"""
    return RANGES[build](**params)

# ------------------------------------------------------------------
# Solving, drawing, and checking, by type
# ------------------------------------------------------------------
BY = {"1": (answer1, None, check1, read1), "2": (answer2, build2, check2, read2),
      "3": (answer3, build3, check3, read_angle), "4": (answer4, build4, check4, read_angle),
      "5": (answer5, build5, check5, read5), "6": (answer6, build6, check6, read6),
      "7": (answer7, build7, check7, read7), "8": (answer8, build8, check8, read8),
      "9": (answer9, build9, check9, read9), "10": (answer10, build10, check10, read10)}

MAX_WIDE = {"half": 7.6, "full": 15.0}                 # cm a figure may take

def extent(typ, prompt):
    """(width, height) of the figure in centimeters, the construction's room included."""
    if typ == "1":
        return 7.6, 4.6
    prims, _ = BY[typ][1](prompt)
    xs, ys = [], []
    for pr in prims:
        if pr[0] == "seg":
            pts = [pr[1], pr[2]]
        elif pr[0] == "arc":
            (cx, cy), r, a0, a1 = pr[1:5]
            pts = [add((cx, cy), u(a0 + (a1 - a0) * i / 8), r) for i in range(9)]
        else:
            pts = [pr[1]]
        xs += [p[0] for p in pts]
        ys += [p[1] for p in pts]
    return max(xs) - min(xs) + 0.7, max(ys) - min(ys) + 0.7

def answer_of(prompt, typ):
    return BY[typ][0](prompt)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    if entry != "1":
        BY[entry][1](prompt)                            # its arcs must meet (need) ...
        need(extent(entry, prompt)[0] <= MAX_WIDE[ENTRY[entry]["width"]])   # ... and it must fit the page
    return dict(prompt=prompt, answer=answer_of(prompt, entry))

def check(p):
    try:
        ok = BY[p["type"]][2](p["prompt"], p["answer"])
    except gen.Redraw:
        return "failed"                                 # the construction's arcs don't meet
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def statement(p):
    """The problem's words (Typst markup), without its figure."""
    t, pr = p["type"], p["prompt"]
    if t == "1":
        (n1, _), (n2, _) = asked1(pr)
        return f"Use the protractor to find the measures of $angle {names(n1)}$ and $angle {names(n2)}$."
    if t == "2":
        a, b, _, _, ray = read2(pr)
        if ray:
            return f"Construct a segment on ray ${names(''.join(ray))}$ that is congruent to $overline({a} {b})$."
        return f"Construct a segment congruent to $overline({a} {b})$."
    if t == "3":
        p_, q, r_, _, _ = read_angle(pr)
        return f"Construct an angle which is congruent to $angle {p_} {q} {r_}$."
    if t == "4":
        p_, q, r_, _, _ = read_angle(pr)
        return f"Bisect $angle {p_} {q} {r_}$."
    if t == "5":
        a, b, _, _ = read5(pr)
        return f"Construct the perpendicular bisector of segment ${a} {b}$."
    if t == "6":
        kind, a, b, _, p_, _, _ = read6(pr)
        wrap = "overline" if kind == "segment" else "arrow.l.r"
        return f"Construct a perpendicular to ${wrap}({a} {b})$ at ${p_}$."
    if t == "7":
        a, b, _, p_, _, _ = read7(pr)
        return f"Construct a perpendicular from line ${a} {b}$ to point ${p_}$."
    if t == "8":
        sides = read8(pr)
        ns = [f"${side_name(n)}$" for n, _ in sides]
        if len(sides[0][0]) == 1:
            return f"Construct a triangle whose sides have lengths {ns[0]}, {ns[1]}, and {ns[2]}."
        return f"Given segments {ns[0]}, {ns[1]}, and {ns[2]}, construct a triangle whose sides have these lengths."
    if t == "9":
        _, p_, _, _ = read9(pr)
        return f"Construct a line through point ${p_}$ that is parallel to the given line."
    a, b, _, n = read10(pr)
    return f"Divide $overline({a} {b})$ into {WORDS.get(n, str(n))} segments of equal length."

def figure(p, key=False, unit="1cm", text_scale=1.0):
    if p["type"] == "1":
        return figure1(p["prompt"], key, unit, text_scale)
    prims, _ = BY[p["type"]][1](p["prompt"])
    return fig.construction(prims, key, unit)

READ_ERRORS = (ValueError, gen.Redraw, KeyError, TypeError, IndexError, AttributeError, ZeroDivisionError)

def _prompt(p, key):
    try:
        s, f = statement(p), figure(p, key)
    except READ_ERRORS:
        return p["prompt"]
    return f"{s} #v(0.3em) #align(center)[{f}]"

def typst(p, gap="0.3em"):
    return _prompt(p, False)

def key_typst(p, gap="0.3em"):
    """The key's prompt: the construction drawn on the given figure."""
    return _prompt(p, True)

def answer_typst(p):
    return "$" + p["answer"].replace(", ", ", quad ") + "$"

def steps(p):
    """The construction's steps with this problem's letters, as the deck's answer slides list them."""
    t, pr = p["type"], p["prompt"]
    if t == "1":
        return "Put the vertex under the origin, one side along the baseline; read where the other ray crosses the scale that starts at 0 on that side."
    if t == "2":
        a, b, _, _, _ = read2(pr)
        x, y, pp = names2(pr)
        return (f"+ Draw ray ${x} {y}$.\n+ Open the compass to length ${a} {b}$.\n"
                f"+ With center ${x}$, draw an arc crossing ray ${x} {y}$ at ${pp}$.")
    if t == "3":
        p_, q, r_, _, _ = read_angle(pr)
        x, y, mm, nn, z, pp = names3(pr)
        return (f"+ Draw ray ${x} {y}$. An arc about ${q}$ crosses the sides at ${mm}$ and ${nn}$; the same arc "
                f"about ${x}$ crosses ray ${x} {y}$ at ${z}$.\n+ An arc of radius ${mm} {nn}$ about ${z}$ crosses "
                f"it at ${pp}$.\n+ Draw ray ${x} {pp}$.")
    if t == "4":
        p_, q, r_, _, _ = read_angle(pr)
        dd = names4(pr)
        return (f"+ An arc about ${q}$ crosses both sides.\n+ Equal arcs about those two points meet at ${dd}$.\n"
                f"+ Draw ray ${q} {dd}$, the bisector.")
    if t == "5":
        a, b, _, _ = read5(pr)
        return (f"+ With centers ${a}$ and ${b}$, draw equal arcs (radius more than $1/2 {a} {b}$) that meet "
                f"above and below.\n+ Draw the line through the two crossings. It meets ${a} {b}$ at its midpoint.")
    if t == "6":
        _, a, b, _, p_, _, _ = read6(pr)
        mm, nn, dd = names6(pr)
        return (f"+ Equal arcs about ${p_}$ cross ${a} {b}$ at ${mm}$ and ${nn}$.\n+ Widen the compass: equal arcs "
                f"about ${mm}$ and ${nn}$ meet at ${dd}$.\n+ Draw line ${p_} {dd}$.")
    if t == "7":
        a, b, _, p_, _, _ = read7(pr)
        rr, ss, dd = names7(pr)
        return (f"+ An arc about ${p_}$ crosses line ${a} {b}$ at ${rr}$ and ${ss}$.\n+ Construct the perpendicular "
                f"bisector of ${rr} {ss}$; it passes through ${p_}$ and meets the line at ${dd}$.")
    if t == "8":
        sides = sorted(read8(pr), key=lambda s: s[1])
        (na, _), (nb, _), (nc, _) = [(side_name(n), v) for n, v in sides]
        return (f"+ Draw a ray and mark off length ${nc}$ on it.\n+ From the left end, an arc of radius ${nb}$; "
                f"from the right end, an arc of radius ${na}$.\n+ Connect their crossing to both ends.")
    if t == "9":
        _, p_, _, _ = read9(pr)
        xx, qq = names9(pr)
        return (f"+ Pick ${xx}$ on the line and draw line ${p_} {xx}$; it makes angle $A$.\n"
                f"+ Copy angle $A$ at ${p_}$. Line ${p_} {qq}$ is parallel: corresponding angles are equal.")
    a, b, _, n = read10(pr)
    marks, pp, pts = names10(pr)
    return (f"+ Draw ray ${a} {pp}$ and step off {WORDS.get(n, str(n))} equal lengths on it.\n"
            f"+ Connect ${marks[-1]}$ to ${b}$, and draw parallels to ${marks[-1]} {b}$ through the other marks.")

SLIDE_SCALE, SLIDE_TALL, SLIDE_WIDE = 1.5, 8.0, 15.0   # a slide figure: cm to a cm, its most cm tall and wide

def slide_typst(p, key=False):
    """The words, then the steps and answer (hidden on the question slide), beside the figure
    drawn larger; the figure is the same size on both slides, so nothing moves."""
    try:
        w, h = extent(p["type"], p["prompt"])
        k = min(SLIDE_SCALE, SLIDE_TALL / h, SLIDE_WIDE / w)   # as large as fits beside the words
        f, s = figure(p, key, f"{k:.2f}cm", 1.5), statement(p)
        st = steps(p)
    except READ_ERRORS:
        return None
    ans = f"#text(size: 0.8em)[{st}] #v(0.4em) {answer_typst(p)}"
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{s} #v(0.8em) {shown}], [{f}])"

def plain(t):
    """An answer as text: m∠BOA = 45°, PD ⊥ RS, AB ∥ the given line."""
    t = t.replace("m angle ", "m∠").replace(" degree", "°").replace(' "cm"', " cm").replace('"', "")
    t = re.sub(r"(?:overline|arrow\.l\.r)\(([^)]*)\)", r"\1", t)
    t = t.replace(" perp ", " ⊥ ").replace(" parallel ", " ∥ ")
    return re.sub(r"(?<=[A-Z'∠]) (?=[A-Z])", "", t)

def text(p):
    try:
        s = statement(p)
    except READ_ERRORS:
        return p["prompt"]
    s = re.sub(r"\$(?:overline|arrow\.l\.r)\(([^)]*)\)\$", r"$\1$", s).replace("$angle ", "∠$")
    s = re.sub(r"\$([^$]*)\$", lambda m: m.group(1).replace(" ", ""), s)
    return s + "   [figure]"

def answer_text(p):
    return plain(p["answer"])

def height(p):
    """Inches the problem takes on the page: its words and its figure."""
    try:
        return 0.35 + extent(p["type"], p["prompt"])[1] / 2.54
    except READ_ERRORS:
        return 0.3

# ------------------------------------------------------------------
# Editing: the prompt is the figure's data
# ------------------------------------------------------------------
EXAMPLE = {"1": "O; A 0, B 45, C 180", "2": "AB = 4", "3": "PQR = 30, QR at -15", "4": "BAC = 40, AC at 0",
           "5": "MN = 6", "6": "segment RS = 6.5, P at 2.5", "7": "line EF = 7.2, P at 3.6, 2.2 above",
           "8": "a = 2, b = 3, c = 4", "9": "line 7, P at 2.5, 2.5 above", "10": "AB = 6, 3 parts"}

def clean(t):
    return " ".join(t.replace("−", "-").replace("°", "").replace("∠", "").split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    typ = old["type"]
    try:
        BY[typ][3](t)
        answer = answer_of(t, typ)
        if typ != "1":
            BY[typ][1](t)
    except READ_ERRORS:
        raise ValueError(f"write it like: {EXAMPLE[typ]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)
