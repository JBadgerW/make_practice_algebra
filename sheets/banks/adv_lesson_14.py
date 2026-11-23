"""Lesson 14 (Advanced Math): sine, cosine, and tangent; angles of elevation and
depression; rectangular and polar coordinates; coordinate conversion. From the
Saxon lesson and its deck (~/Documents/adv_math/problem_sets/ps_014/slides/deck_014.typ):
examples 14.1-14.6 and Problem Set 14, problems 4-8.

    1  legs from the hypotenuse and an angle:  hypotenuse 6, angle 36°          A = 4.85, B = 3.53
    2  an angle and a leg from two sides:      hypotenuse 7, leg 3 across M     M = 25.38°, x = 6.32
    3  angle of elevation:                     a man 6 feet tall, 200 feet from a tree, 11°    44.88 ft
    4  angle of depression:                    altitude 3000 feet, 26°                         6843.52 ft
    5  rectangular to polar, four forms:       -3 î + 2 ĵ      √13/146.31°, √13/-213.69°, -√13/-33.69°, -√13/326.31°
    6  polar to rectangular:                   -13/-253°       (3.80, -12.43) or 3.80 î - 12.43 ĵ

Each heading of the problem types file is a type, and examples 14.1-14.3, which
have no Problem Set item, are types too. Type 2 has a second shape beside 14.2's
(the known leg next to the angle, found with the cosine); Type 6 draws a negative
magnitude (14.6, problem 7) two times in three, a positive one (problem 8) the rest.

Types 1 and 2 show the triangle, drawn to scale as the deck draws it: the right
angle at the lower left, the angle at the lower right (or mirrored, pose 1). The
word problems (Types 3, 4) and the conversions (Types 5, 6) have no figure, as
the deck's questions have none (its answers sketch one).

The stories keep the book's words, with names of things only and no pronouns:
14.3's "and he measures" is written "and measures" (no comma). A story's person
(a man, a woman, a surveyor, a student), its object (a tree, a flagpole, a
building, a tower), and its aircraft (an airplane, a helicopter) are drawn.

The key writes what the deck writes, every decimal to two places (half up):
  1  each leg, letter = value, in alphabetical order: A = 4.85, B = 3.53.
  2  the angle in degrees, then the side: M = 25.38°, x = 6.32.
  3, 4  the height or the slant range in feet: 44.88 ft, 6843.52 ft.
  5  four forms, in the deck's order: r at the angle between -180° and 180°; r at
     that angle less (or plus) 360°; -r at the angle 180° from the first, again
     between -180° and 180°; -r at that less (or plus) 360°. With whole-number
     components r is exact and simplified (√13, 2√2, 5), else to two places
     (4.11). The angles are found from the first, so their digits agree.
  6  (x, y) or x î + y ĵ, both, as the deck gives both.
Polar coordinates are written as the book writes them, r/θ°: "-13/-253 degree"
in a prompt, shown with the angle underlined.

check() works from the problem's numbers, not from how the answer was built:
  1  each leg within rounding: the adjacent one from the cosine, the other from
     the Pythagorean theorem; two places exactly.
  2  the angle from the arctangent of the two legs (the build uses the arcsine or
     the arccosine), the side from the Pythagorean theorem.
  3  the story's numbers read back out of its words: the height less the eye
     height, over the distance, is the tangent of the angle, within rounding.
  4  the slant range times the sine of the angle of depression is the altitude.
  5  every form, turned back into x and y, is the point (within rounding); the
     forms come in the deck's order (signs of r, where the angles fall), and an
     exact r is a simplified radical.
  6  both forms of the answer agree and are r cos θ and r sin θ, within rounding.

No skipped sources: Lesson 14 has no proofs.

A problem: dict(type, prompt, answer, source).
    1  "6, 36; A, B; pose 0"             hypotenuse, angle; the adjacent leg's letter, the opposite one's
    2  "7, 3 opposite; M, x; pose 0"     hypotenuse, the known leg and where it is; the angle's letter, the side's
    3, 4  the story's words
    5  "-3 hat(dotless.i) + 2 hat(dotless.j)"
    6  "-13/-253 degree"
"""
import math, re
from decimal import Decimal, ROUND_HALF_UP
from .. import gen
from ..gen import need
from ..typst import esc
from . import lesson_figures as fig
from .adv_trig import I, J

NAME = FAMILY = "adv_lesson_14"
FIXED = False
TITLE = ("Lesson 14: Sine, Cosine, and Tangent, Angles of Elevation and Depression, "
         "Rectangular and Polar Coordinates, Coordinate Conversion")
INSTRUCTIONS = ""              # each type has its own
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

TYPES = [
    dict(key="1", title="Legs of a Right Triangle", instructions="Find the sides.",
         look="A right triangle with its hypotenuse and one acute angle given; the two legs are letters.",
         move="The leg next to the angle is the hypotenuse times the cosine, the leg across from it the "
              "hypotenuse times the sine: $A = 6 cos 36 degree$, $B = 6 sin 36 degree$."),
    dict(key="2", title="An Angle and a Side of a Right Triangle", instructions="Find the angle and the side.",
         look="A right triangle with its hypotenuse and one leg given; an angle and the other leg are letters.",
         move="The leg across from the angle over the hypotenuse is its sine (the leg beside it, its cosine): "
              "$sin M = 3/7$, so $M = sin^(-1)(3/7)$. Then the Pythagorean theorem: $x^2 + 3^2 = 7^2$."),
    dict(key="3", title="Angle of Elevation", instructions="Solve.",
         look="Someone looks up at the top of a tall object from a known distance, at a given angle of elevation.",
         move="Draw the triangle from eye level: the rise $y$ is the distance times the tangent, "
              "$y = 200 tan 11 degree$. Then add the eye height: the object is $y + 6$ feet tall.",
         width="full"),
    dict(key="4", title="Angle of Depression", instructions="Solve.",
         look="A pilot at a given altitude sights an object on the ground at an angle of depression.",
         move="The angle of depression equals the angle of elevation from the object, so the altitude is "
              "across from it: $sin 26 degree = 3000/s$, $s = 3000/(sin 26 degree)$. (The deck uses the "
              "angle at the airplane, $cos 64 degree$: the same.)", width="full"),
    dict(key="5", title="Rectangular to Polar, Four Forms", instructions="Convert to polar coordinates. "
         "Write four forms.",
         look="A point $x hat(i) + y hat(j)$.",
         move="$r = sqrt(x^2 + y^2)$. Find the angle with the $x$ axis from $tan theta = abs(y)/abs(x)$, then the "
              "polar angle in the point's quadrant. Write $r$ at that angle and at it $minus.plus 360 degree$, "
              "and $-r$ at the angle $180 degree$ away and at that $minus.plus 360 degree$.",
         width="full", space="1in"),
    dict(key="6", title="Polar to Rectangular", instructions="Convert to rectangular coordinates.",
         look="A point in polar form, $r slash theta$, maybe with a negative $r$ or $theta$.",
         move="Draw the angle; a negative $r$ backs up from it, into the opposite quadrant. Then "
              "$x = r cos theta$ and $y = r sin theta$, with the signs of that quadrant.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

FIGURES = ("1", "2")
STORIES = ("3", "4")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], re.sub(r"; pose \d+$", "", p["prompt"]))   # mirrored is no new problem

def two(x):
    """x to two places, half up: 3.80, -12.43."""
    q = Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return "0.00" if q == 0 else str(q)

def plain_number(hundredths):
    """A number given in hundredths, written without trailing zeros: 730 -> "7.3", 1300 -> "13"."""
    s = str(Decimal(hundredths) / 100)
    return s.rstrip("0").rstrip(".") if "." in s else s

def sin_d(a):
    return math.sin(math.radians(a))

def cos_d(a):
    return math.cos(math.radians(a))

TWO = r"-?\d+\.\d\d"
POSE = re.compile(r";\s*pose\s+(\d+)\s*$")

def split(prompt):
    t = " ".join(prompt.replace("−", "-").split())
    m = POSE.search(t)
    pose = int(m.group(1)) if m else 0
    t = POSE.sub("", t) if m else t
    return [[i.strip() for i in part.split(",")] for part in t.split(";")], pose

LETTER = re.compile(r"[A-Za-z]")

# ------------------------------------------------------------------
# Type 1: the legs from the hypotenuse and an angle (example 14.1)
# ------------------------------------------------------------------
HYP1 = range(2, 21)
ANGLE1 = range(15, 76)
LEGS1 = (("A", "B"), ("x", "y"), ("a", "b"))
POSES = range(2)

def t1_ok(h, a, legs, swap, pose):
    return h in HYP1 and a in ANGLE1 and legs in LEGS1 and swap in (0, 1) and pose in POSES

def t1_pick(r):
    return dict(h=r.choice(HYP1), a=r.choice(ANGLE1), legs=r.choice(LEGS1), swap=r.choice((0, 1)),
                pose=r.choice(POSES))

def t1(h, a, legs, swap, pose):
    need(t1_ok(h, a, legs, swap, pose))
    adj, opp = legs[::-1] if swap else legs
    return f"{h}, {a}; {adj}, {opp}; pose {pose}"

def t1_data(prompt):
    parts, pose = split(prompt)
    if [len(p) for p in parts] != [2, 2]:
        raise ValueError("hypotenuse, angle; two letters")
    h, a = float(parts[0][0]), float(parts[0][1])
    adj, opp = parts[1]
    if not (h > 0 and 0 < a < 90 and LETTER.fullmatch(adj) and LETTER.fullmatch(opp) and adj != opp):
        raise ValueError("not a right triangle")
    return h, a, adj, opp, pose

# ------------------------------------------------------------------
# Type 2: an angle and a leg from the hypotenuse and a leg (example 14.2)
# ------------------------------------------------------------------
HYP2 = range(3, 21)
WHERE = ("opposite", "adjacent")
ANGLES2 = ("M", "A", "K", "P")
SIDES2 = ("x", "y")

def t2_ok(h, leg, where, angle, side, pose):
    if not (h in HYP2 and 1 <= leg < h and where in WHERE and angle in ANGLES2 and side in SIDES2
            and pose in POSES):
        return False
    m = math.degrees(math.asin(leg / h) if where == "opposite" else math.acos(leg / h))
    return 15 <= m <= 75

def t2_pick(r):
    h = r.choice(HYP2)
    return dict(h=h, leg=r.randint(1, h - 1), where=r.choice(("opposite", "opposite", "adjacent")),
                angle=r.choice(ANGLES2), side=r.choice(SIDES2), pose=r.choice(POSES))

def t2(h, leg, where, angle, side, pose):
    need(t2_ok(h, leg, where, angle, side, pose))
    return f"{h}, {leg} {where}; {angle}, {side}; pose {pose}"

def t2_data(prompt):
    parts, pose = split(prompt)
    if [len(p) for p in parts] != [2, 2]:
        raise ValueError("hypotenuse, leg; two letters")
    m = re.fullmatch(r"(\d+(?:\.\d+)?) (opposite|adjacent)", parts[0][1])
    if not m:
        raise ValueError("the leg, opposite or adjacent")
    h, leg, where = float(parts[0][0]), float(m.group(1)), m.group(2)
    angle, side = parts[1]
    if not (0 < leg < h and LETTER.fullmatch(angle) and LETTER.fullmatch(side) and angle != side):
        raise ValueError("not a right triangle")
    return h, leg, where, angle, side, pose

# ------------------------------------------------------------------
# Type 3: angle of elevation (example 14.3)
# ------------------------------------------------------------------
T3_TEXT = ("A {person} {h} feet tall is {d} feet from a {thing} and measures the angle of elevation to the top "
           "of the {thing} as {a}°. How tall is the {thing}?")
PEOPLE = ("man", "woman", "surveyor", "student")
THINGS = ("tree", "flagpole", "building", "tower")
EYE3 = (5, 6)
DIST3 = range(50, 301, 10)
ANGLE3 = range(5, 36)                 # with DIST3, nothing taller than about 216 ft

def t3_ok(person, h, d, thing, a):
    return person in PEOPLE and h in EYE3 and d in DIST3 and thing in THINGS and a in ANGLE3

def t3_pick(r):
    return dict(person=r.choice(PEOPLE), h=r.choice(EYE3), d=r.choice(DIST3), thing=r.choice(THINGS),
                a=r.choice(ANGLE3))

def t3(person, h, d, thing, a):
    need(t3_ok(person, h, d, thing, a))
    return gen.fill(T3_TEXT, person=person, h=h, d=d, thing=thing, a=a)

# ------------------------------------------------------------------
# Type 4: angle of depression (example 14.4, problem 4)
# ------------------------------------------------------------------
T4_TEXT = ("{craft} is flying at an altitude of {alt} feet above the ground. The pilot sights an object on the "
           "ground at an angle of depression of {a}°. What is the slant range from the {vehicle} to the object?")
CRAFT = {"airplane": "An airplane", "helicopter": "A helicopter"}
ALT4 = range(1000, 10001, 500)
ANGLE4 = range(10, 71)

def t4_ok(vehicle, alt, a):
    return vehicle in CRAFT and alt in ALT4 and a in ANGLE4

def t4_pick(r):
    return dict(vehicle=r.choice(("airplane", "airplane", "helicopter")), alt=r.choice(ALT4), a=r.choice(ANGLE4))

def t4(vehicle, alt, a):
    need(t4_ok(vehicle, alt, a))
    return gen.fill(T4_TEXT, craft=CRAFT[vehicle], alt=alt, a=a, vehicle=vehicle)

def story_numbers(prompt, typ):
    v = gen.read(T3_TEXT if typ == "3" else T4_TEXT, prompt)
    if typ == "4" and CRAFT.get(v["vehicle"]) != v["craft"]:
        raise ValueError("the same aircraft")
    nums = {k: float(gen.number(v[k])) for k in (("h", "d", "a") if typ == "3" else ("alt", "a"))}
    if not (0 < nums["a"] < 90 and all(x > 0 for x in nums.values())):
        raise ValueError("not a triangle")
    return nums

# ------------------------------------------------------------------
# Type 5: rectangular to polar, four forms (example 14.5, problems 5 and 6)
# ------------------------------------------------------------------
WHOLE5 = range(1, 13)                 # whole components, 14.5
HUND5 = range(50, 1000)               # components in hundredths, 3.06 and 7.3

def rect(xs, ys):
    """The point x î + y ĵ from the components as written."""
    sign = "-" if ys.startswith("-") else "+"
    return f"{xs} {I} {sign} {ys.lstrip('-')} {J}"

def t5_whole_ok(x, y):
    return abs(x) in WHOLE5 and abs(y) in WHOLE5

def t5_whole_pick(r):
    return dict(x=gen.signed(r, 1, 12), y=gen.signed(r, 1, 12))

def t5_whole(x, y):                   # 14.5: -3 î + 2 ĵ
    need(t5_whole_ok(x, y))
    return rect(str(x), str(y))

def t5_decimal_ok(x, y):
    return abs(x) in HUND5 and abs(y) in HUND5 and (abs(x) % 100 or abs(y) % 100)   # not both whole

def t5_decimal_pick(r):
    return dict(x=r.choice((1, -1)) * r.choice(HUND5), y=r.choice((1, -1)) * r.choice(HUND5))

def t5_decimal(x, y):                 # problems 5 and 6: 3.06 î - 2.75 ĵ, -2.41 î + 7.3 ĵ
    need(t5_decimal_ok(x, y))
    return rect(plain_number(x), plain_number(y))

RECT = re.compile(rf"^(-?\d+(?:\.\d+)?) {re.escape(I)} ([+-]) (\d+(?:\.\d+)?) {re.escape(J)}$")

def read_rect(t):
    """(x, y, whole) from "-3 î + 2 ĵ" as Typst writes it."""
    m = RECT.match(" ".join(t.replace("−", "-").split()))
    if not m:
        raise ValueError(f"write it like -3 {I} + 2 {J}")
    xs, ys = m.group(1), ("-" if m.group(2) == "-" else "") + m.group(3)
    x, y = float(xs), float(ys)
    if x == 0 or y == 0:
        raise ValueError("a point off the axes")
    return x, y, "." not in xs + ys

def radical(n):
    """sqrt(n) simplified, as text: 13 -> "sqrt(13)", 8 -> "2 sqrt(2)", 25 -> "5"."""
    k = max(d for d in range(1, math.isqrt(n) + 1) if n % (d * d) == 0)
    m = n // (k * k)
    return str(k) if m == 1 else (f"sqrt({m})" if k == 1 else f"{k} sqrt({m})")

def neg(r):
    return r[1:] if r.startswith("-") else "-" + r

def other(theta):
    """The same direction one turn the other way: 146.31 -> -213.69, -41.95 -> 318.05."""
    return theta - 360 if theta > 0 else theta + 360

def polar(r, theta):
    return f"{r}/{theta} degree"

def forms_of(prompt):
    x, y, whole = read_rect(prompt)
    r = radical(int(x * x + y * y)) if whole else two(math.hypot(x, y))
    th = Decimal(two(math.degrees(math.atan2(y, x))))
    back = th - 180 if th > 0 else th + 180
    return [(r, th), (r, other(th)), (neg(r), back), (neg(r), other(back))]

# ------------------------------------------------------------------
# Type 6: polar to rectangular (example 14.6, problems 7 and 8)
# ------------------------------------------------------------------
HUND6 = range(100, 2001)              # |r| in hundredths: 13, 8.6, 7.42
ANGLE6 = [t for t in range(-359, 360) if t % 90]

def t6_ok(r, theta):
    if not (abs(r) in HUND6 and theta in ANGLE6):
        return False
    x, y = polar_xy(r / 100, theta)
    return two(x) != "0.00" and two(y) != "0.00"

def t6_pick(r):
    places = r.choice((0, 1, 2))
    mag = r.choice(HUND6)
    mag = mag - mag % (100 if places == 0 else 10 if places == 1 else 1)
    sign = r.choice((-1, -1, 1))
    return dict(r=sign * max(mag, 100), theta=r.choice(ANGLE6))

def t6(r, theta):                      # 14.6: -13/-253 degree; problems 7, 8: -8.6/265, 7.42/-143
    need(t6_ok(r, theta))
    return polar(plain_number(r), theta)

POLAR = re.compile(r"^(-?\d+(?:\.\d+)?)\s*/\s*(-?\d+(?:\.\d+)?) degree$")

def read_polar(t):
    m = POLAR.match(" ".join(t.replace("−", "-").split()))
    if not m:
        raise ValueError("write it like -13/-253 degree")
    return float(m.group(1)), float(m.group(2))

def polar_xy(r, theta):
    return r * cos_d(theta), r * sin_d(theta)

def rect_answer(x, y):
    xs, ys = two(x), two(y)
    return f"({xs}, {ys}) or {rect(xs, ys)}"

# ------------------------------------------------------------------
# The templates
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick, t1)],
    "2": [(t2_pick, t2)],
    "3": [(t3_pick, t3)],
    "4": [(t4_pick, t4)],
    "5": [(t5_whole_pick, t5_whole), (t5_decimal_pick, t5_decimal), (t5_decimal_pick, t5_decimal)],
    "6": [(t6_pick, t6)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3: t3_ok, t4: t4_ok, t5_whole: t5_whole_ok, t5_decimal: t5_decimal_ok,
          t6: t6_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# Solving (for draws and edits)
# ------------------------------------------------------------------
def answer_of(prompt, typ):
    if typ == "1":
        h, a, adj, opp, _ = t1_data(prompt)
        vals = {adj: two(h * cos_d(a)), opp: two(h * sin_d(a))}
        return ", ".join(f"{k} = {vals[k]}" for k in sorted(vals))
    if typ == "2":
        h, leg, where, angle, side, _ = t2_data(prompt)
        m = math.degrees(math.asin(leg / h) if where == "opposite" else math.acos(leg / h))
        return f"{angle} = {two(m)} degree, {side} = {two(math.sqrt(h * h - leg * leg))}"
    if typ == "3":
        n = story_numbers(prompt, "3")
        return f"{two(n['d'] * math.tan(math.radians(n['a'])) + n['h'])} ft"
    if typ == "4":
        n = story_numbers(prompt, "4")
        return f"{two(n['alt'] / sin_d(n['a']))} ft"
    if typ == "5":
        return ", ".join(polar(r, th) for r, th in forms_of(prompt))
    r, th = read_polar(prompt)
    x, y = polar_xy(r, th)
    if two(x) == "0.00" or two(y) == "0.00":
        raise ValueError("a point off the axes")
    return rect_answer(x, y)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt, entry))

# ------------------------------------------------------------------
# Checking
# ------------------------------------------------------------------
TOL = 0.005 + 1e-9                    # half a hundredth: a value rounded to two places

def values(ans, names):
    """{name: float} from "A = 4.85, B = 3.53", the names exactly these, in order, each to two places."""
    parts = [s.strip() for s in ans.split(",")]
    out = {}
    if len(parts) != len(names):
        return None
    for part, (name, unit) in zip(parts, names):
        m = re.fullmatch(rf"{re.escape(name)} = ({TWO}){unit}", part)
        if not m:
            return None
        out[name] = float(m.group(1))
    return out

RADICAL = re.compile(r"^(-?)(?:(\d+) )?sqrt\((\d+)\)$|^(-?)(\d+)$")

def check_forms(prompt, answer):
    x, y, whole = read_rect(prompt)
    parts = [s.strip() for s in answer.split(",")]
    if len(parts) != 4:
        return False
    got = []
    for f in parts:
        m = re.fullmatch(rf"(.+)/({TWO}) degree", f)
        if not m:
            return False
        rt, th = m.group(1), float(m.group(2))
        if whole:                                   # exact, a simplified radical
            k = RADICAL.match(rt)
            if not k:
                return False
            if k.group(3):
                c, n = int(k.group(2) or 1), int(k.group(3))
                if any(n % (d * d) == 0 for d in range(2, math.isqrt(n) + 1)) or n == 1:
                    return False
                r2, sign = c * c * n, k.group(1)
            else:
                r2, sign = int(k.group(5)) ** 2, k.group(4)
            if r2 != round(x * x + y * y):
                return False
            r = (-1 if sign else 1) * math.sqrt(r2)
        else:
            if not re.fullmatch(TWO, rt) or abs(abs(float(rt)) - math.hypot(x, y)) > TOL:
                return False
            r = float(rt)
        got.append((r, th))
    for r, th in got:                               # each is the point (the angle within rounding)
        want = math.degrees(math.atan2(y, x) if r > 0 else math.atan2(-y, -x))
        if abs((th - want + 180) % 360 - 180) > TOL:
            return False
    signs = [r > 0 for r, _ in got]
    inside = [-180 < th <= 180 for _, th in got]
    return signs == [True, True, False, False] and inside == [True, False, True, False]

def check_rect(prompt, answer):
    r, th = read_polar(prompt)
    m = re.fullmatch(rf"\(({TWO}), ({TWO})\) or ({TWO}) {re.escape(I)} ([+-]) (\d+\.\d\d) {re.escape(J)}", answer)
    if not m:
        return False
    x, y = float(m.group(1)), float(m.group(2))
    x2, y2 = float(m.group(3)), float(m.group(5)) * (-1 if m.group(4) == "-" else 1)
    wx, wy = polar_xy(r, th)
    return x == x2 and y == y2 and abs(x - wx) <= TOL and abs(y - wy) <= TOL

def check_problem(p):
    typ, prompt, ans = p["type"], p["prompt"], " ".join(p["answer"].split())
    if typ == "1":
        h, a, adj, opp, _ = t1_data(prompt)
        v = values(ans, sorted([(adj, ""), (opp, "")]))
        if v is None:
            return False
        A = h * cos_d(a)
        return abs(v[adj] - A) <= TOL and abs(v[opp] - math.sqrt(h * h - A * A)) <= TOL
    if typ == "2":
        h, leg, where, angle, side, _ = t2_data(prompt)
        v = values(ans, [(angle, " degree"), (side, "")])
        if v is None:
            return False
        other_leg = math.sqrt(h * h - leg * leg)
        opp, adj = (leg, other_leg) if where == "opposite" else (other_leg, leg)
        return abs(v[angle] - math.degrees(math.atan2(opp, adj))) <= TOL and abs(v[side] - other_leg) <= TOL
    if typ in STORIES:
        m = re.fullmatch(r"(\d+\.\d\d) ft", ans)
        if not m:
            return False
        got, n = float(m.group(1)), story_numbers(prompt, typ)
        if typ == "3":                              # the rise over the run is the tangent
            return abs((got - n["h"]) - n["d"] * math.tan(math.radians(n["a"]))) <= TOL
        return abs(got * sin_d(n["a"]) - n["alt"]) <= TOL * sin_d(n["a"])   # the slant range drops the altitude
    if typ == "5":
        return check_forms(prompt, ans)
    return check_rect(prompt, ans)

def check(p):
    try:
        ok = check_problem(p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Figures: the right triangle to scale, the right angle at the lower left
# ------------------------------------------------------------------
def triangle(p, unit_="1cm"):
    """The triangle: vertex 0 the right angle (lower left), 1 the angle (lower right, or at the
    top when it is over 45°, so the longer leg lies along the bottom), 2 the third corner;
    side 0 the leg beside the angle, side 1 the hypotenuse, side 2 the leg across from it."""
    if p["type"] == "1":
        h, a, adj, opp, pose = t1_data(p["prompt"])
        sides = {0: f"${adj}$", 2: f"${opp}$"}
        mark = f"${a:g} degree$"
    else:
        h, leg, where, angle, side, pose = t2_data(p["prompt"])
        known = f"${leg:g}$"
        sides = {0: known if where == "adjacent" else f"${side}$", 1: f"${h:g}$",
                 2: known if where == "opposite" else f"${side}$"}
        a = math.degrees(math.asin(leg / h) if where == "opposite" else math.acos(leg / h))
        mark = f"${angle}$"
    sides[1] = f"${h:g}$"
    if a <= 45:                                     # the longer leg along the bottom
        pts = [(0.0, 0.0), (cos_d(a), 0.0), (0.0, sin_d(a))]
    else:                                           # the angle at the top
        pts = [(0.0, 0.0), (0.0, cos_d(a)), (sin_d(a), 0.0)]
    if pose:
        pts = [(-x, y) for x, y in pts]
    return fig.triangles([dict(pts=pts, labels=sides, marks={0: "right", 1: 1}, angles={1: mark})],
                         wide=4.6, tall=2.6, unit=unit_)

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
ASK = {"1": "Find {a} and {b}.", "2": "Find angle {a} and side {b}."}
LEAD = {"5": "Convert to polar coordinates. (Write four forms.)", "6": "Convert to rectangular coordinates:"}

def statement(p):
    parts, _ = split(p["prompt"])
    a, b = parts[1] if p["type"] == "2" else sorted(parts[1])
    return ASK[p["type"]].format(a=f"${a}$", b=f"${b}$")

def polar_math(t):
    """ "-13/-253 degree" as the book shows it: -13 with /-253° underlined."""
    r, _, th = t.partition("/")
    th = th.strip()
    th = f'class("unary", -) {th[1:]}' if th.startswith("-") else th
    return f"{r.strip()} underline(\\/ {th})"

def math_of(p, t):
    if p["type"] == "5" and "/" in t:
        return ", #h(0.6em) ".join(f"${polar_math(f.strip())}$" for f in t.split(","))
    if p["type"] == "6" and "/" in t:
        return f"${polar_math(t)}$"
    if " or " in t:
        a, b = t.split(" or ")
        return f"${a}$ #h(0.4em) or #h(0.4em) ${b}$"
    return f"${t}$"

def typst(p, gap="0.3em"):
    typ = p["type"]
    if typ in STORIES:
        return esc(p["prompt"])
    if typ in FIGURES:
        try:
            f = triangle(p)
        except Exception:
            return f"{statement(p) if ';' in p['prompt'] else 'Find the sides.'} #h(0.5em) [{esc(p['prompt'])}]"
        return f"{statement(p)} #v(0.4em) #align(center)[{f}]"
    return f"{LEAD[typ]} #h(0.5em) {math_of(p, p['prompt'])}"

def answer_typst(p):
    if p["type"] in STORIES:
        return esc(p["answer"])
    return math_of(p, p["answer"])

SLIDE_UNIT = "1.9cm"

def slide_typst(p, key=False):
    """A triangle's slide: the words (and the answer, hidden on the question slide) beside the
    triangle drawn larger; it never moves. None for the other types."""
    if p["type"] not in FIGURES:
        return None
    try:
        f = triangle(p, SLIDE_UNIT)
    except Exception:
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return (f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, "
            f"[{statement(p)} #v(0.8em) {shown}], [{f}])")

def readable(t):
    t = (t.replace(f" {I}", "î").replace(f" {J}", "ĵ").replace(" degree", "°").replace("sqrt", "√"))
    return t

def text(p):
    typ = p["type"]
    if typ in STORIES:
        return p["prompt"]
    if typ in FIGURES:
        return f"{statement(p).replace('$', '')}   [figure: {p['prompt']}]"
    return f"{LEAD[typ]} {readable(p['prompt'])}"

def answer_text(p):
    return readable(p["answer"])

def height(p):
    return 1.4 if p["type"] in FIGURES else 0.6 if p["type"] in STORIES else 0.4

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
EXAMPLE = {
    "1": "6, 36; A, B; pose 0", "2": "7, 3 opposite; M, x; pose 0", "3": "the story, with new numbers",
    "4": "the story, with new numbers", "5": f"-3 {I} + 2 {J}", "6": "-13/-253 degree",
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
            triangle(dict(old, type=typ, prompt=t))
    except Exception:
        raise ValueError(f"write it like {EXAMPLE[typ]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
