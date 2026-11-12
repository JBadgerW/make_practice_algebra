"""Lesson 2 (Advanced Math): more on area; cylinders and prisms; cones and
pyramids; spheres. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_002/slides/deck_002.typ): examples
2.1-2.6 and Problem Set 2, problems 25-28.

    1  surface area, cylinder on a capped base:   5 x 6 with a semicircle, 10 high     342.53 cm^2
    2  surface area, prism on a base of squares:  a cross of five 2 x 2 squares, 6 long  184 square units
    3  volume, cylinder on a capped base:         11 x 10 with two semicircles, 9 high  2757.15 cm^3
    4  volume, cone on a capped base:             3 x 2 with a semicircle, 6 high       15.14 m^3
    5  surface area of a right circular cone:     r = 8, slant 10                       144 pi cm^2
    6  a dimension from the volume:               cone 6 pi, h = 2: r = 3;  cylinder 588 pi, r = 7: H = 12;
                                                   triangle-and-sector base 9 pi: H = 2
    7  surface area of a regular pyramid:         square side 4, slant 5                56 cm^2

A "capped base" is a rectangle with a semicircle on one or both of its
sides; on the left, the semicircle may be taller than the rectangle, standing
on its bottom (problem 28). Problem 28's three parts are three problems:
28a Type 3, 28b Type 1, 28c Type 4. Spheres, in the lesson's title, have no
example and no problem here.

Answer conventions, from the deck. A capped base has pi in it, and the deck
answers in decimals to two places, rounding each part as it goes: the base's
area to two places (5 x 6 + pi 3^2/2 = 44.14), then the lateral area (the
perimeter times the height: 254.25), then the total 44.14 + 44.14 + 254.25 =
342.53 cm^2 (example 2.1; the exact 220 + 39 pi is 342.52). A cone's volume
is a third of the rounded base times the height: (1/3)(7.57)(6) = 15.14 m^3
(example 2.3). Without a capped base the answer is exact: 184 square units,
144 pi cm^2, 3 cm, 56 cm^2. A unit goes after the number: 342.53 "cm"^2;
example 2.2 is in "square units". Problems 25-28 have no answers in the deck;
they follow the examples' forms (chosen here): 12 cm, 2 cm, 117.71 m^3 (27,
from the rounded base 44.14), and 28a-c 2757.15 cm^3, 1324.82 cm^2, 919.05 cm^3.

check() works from the problem's data, not from how it was built:
  1, 3, 4  the base's area and perimeter measured on its outline (a polygon
           of thousands of points along the arcs); the answer within the
           rounding the deck's method allows (half a hundredth per rounded
           part, times what it's multiplied by), written to two places with
           the unit squared (area) or cubed (volume).
  2        the base's area by its squares and its perimeter as 4 per square
           less 2 per shared side; the answer exactly.
  5        the lateral area as a sector of the slant-height circle (arc 2 pi r
           of 2 pi l); the answer exactly, a whole number times pi.
  6        the answer put back into the volume formula (the triangle's area
           by the shoelace formula).
  7        each face's area by Heron's formula from its sides; exactly.

No sources are skipped: Lesson 2 has no proofs.

A problem: dict(type, prompt, answer, source). The prompt is the problem's
data in a short form, and it is what an edit changes:
    1  "cylinder area: base 5 x 6, right semicircle; height 10 cm"           '342.53 "cm"^2'
    2  "prism area: plus, side 2, length 6 units"                            '184 "square units"'
    3  "cylinder volume: base 11 x 10, right semicircle, left semicircle 20; height 9 cm"
    4  "cone volume: base 3 x 2, right semicircle; height 6 m"               '15.14 "m"^3'
    5  "cone area: radius 8, slant 10 cm"                                    '144 pi "cm"^2'
    6  "cone radius: volume 6 pi, height 2 cm"                               '3 "cm"'
       "cylinder height: radius 7, volume 588 pi cm"                         '12 "cm"'
       "wedge height: legs 2 pi and 3, sector 60, volume 9 pi cm"            '2 "cm"'
    7  "pyramid area: side 4, slant 5 cm"                                    '56 "cm"^2'
"""
import math, re
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy
from ..typmath import text as plain
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_2"
FIXED = False
TITLE = "Lesson 2: More on Area, Cylinders and Prisms, Cones and Pyramids, Spheres"
INSTRUCTIONS = "Solve each problem. Include units."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

ROUND = "Round each area and volume to two decimal places as you go. Include units."

TYPES = [
    dict(key="1", title="Surface Area of a Cylinder on a Capped Base",
         look="The base of a right cylinder: a rectangle with a semicircle on a side, and the cylinder's height.",
         move="Base: the rectangle plus each half circle (pi r^2/2). Lateral area: the perimeter of the base "
              "(straight sides plus each half circumference, pi r) times the height. Total: two bases plus "
              "the lateral area.", instructions=ROUND, space="1.75in"),
    dict(key="2", title="Surface Area of a Prism on a Base of Squares",
         look="A right prism whose base is made of equal squares, like a cross.",
         move="Base: the number of squares times one square. Lateral area: one rectangle (side times "
              "length) for each edge around the base. Total: two bases plus the lateral area.",
         space="1.75in"),
    dict(key="3", title="Volume of a Cylinder on a Capped Base",
         look="The base of a right cylinder, a rectangle with semicircles, and the height; find the volume.",
         move="Volume = area of the base times the height. The base is the rectangle plus each half circle.",
         instructions=ROUND, space="1.5in"),
    dict(key="4", title="Volume of a Cone on a Capped Base",
         look="The base of a cone, a rectangle with semicircles, and the cone's height.",
         move="Volume = (1/3) times the area of the base times the height. Find the base first: the "
              "rectangle plus each half circle.", instructions=ROUND, space="1.5in"),
    dict(key="5", title="Surface Area of a Right Circular Cone",
         look="A cone's radius and slant height.",
         move="Surface area = base + lateral area = pi r^2 + pi r l, with l the slant height.",
         space="1in"),
    dict(key="6", title="A Dimension from the Volume",
         look="The volume is given; a radius or a height is asked for.",
         move="Write the volume formula (cylinder: base times height; cone: one third of that), put in "
              "what's known, and solve: 6 pi = (1/3)(pi r^2)(2) gives r^2 = 9, r = 3.",
         space="1.5in"),
    dict(key="7", title="Surface Area of a Regular Pyramid",
         look="A pyramid with a square base; the side and the slant height are given.",
         move="Base: side squared. Each of the 4 triangular faces: (1/2)(side)(slant height). Add them.",
         space="1in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

UNITS = ("cm", "m", "ft", "in")
WORDS = {"cm": "centimeters", "m": "meters", "ft": "feet", "in": "inches", "units": "units"}

def unit_power(unit, n):
    """The unit squared or cubed, as the key writes it: "cm"^2, "square units"."""
    if unit == "units":
        return '"square units"' if n == 2 else '"cubic units"'
    return f'"{unit}"^{n}'

def r2(x):
    """x rounded to two places, half up, as a Decimal."""
    return Decimal(repr(float(x))).quantize(Decimal("0.01"), ROUND_HALF_UP)

# ------------------------------------------------------------------
# Types 1, 3, 4: a capped base. A w-by-h rectangle; a semicircle on the
# right (diameter h); on the left none, a semicircle (diameter h), or a
# taller one (diameter d > h) standing on the bottom.
# ------------------------------------------------------------------
WIDTHS = range(2, 13)
SIDES = range(2, 13, 2)                        # h: even, so each radius is whole
HEIGHTS = range(2, 13)                         # the solid's height
CAPS = ("right", "left", "both", "tall")       # tall: right, and a taller left semicircle

def caps_of(h, caps, d):
    """(right?, left diameter)."""
    return {"right": (True, 0), "left": (False, h), "both": (True, h), "tall": (True, d)}[caps]

def cap_text(w, h, right, left):
    parts = [f"base {w} x {h}"]
    if right:
        parts.append("right semicircle")
    if left:
        parts.append("left semicircle" + ("" if left == h else f" {left}"))
    return ", ".join(parts)

def cap_build(kind, w, h, caps, d, height, unit):
    return f"{kind}: {cap_text(w, h, *caps_of(h, caps, d))}; height {height} {unit}"

def t1_build(w, h, caps, d, height, unit):
    return cap_build("cylinder area", w, h, caps, d, height, unit)

def t3_build(w, h, caps, d, height, unit):
    return cap_build("cylinder volume", w, h, caps, d, height, unit)

def t4_build(w, h, caps, d, height, unit):
    return cap_build("cone volume", w, h, caps, d, height, unit)

def proportioned(w, h):
    """The rectangle no flatter than the book's: width from half the height to 2.5 times it."""
    return 2 * w >= h and 2 * w <= 5 * h

def cap_pick(r):
    h = r.choice(SIDES)
    caps = r.choice(("right", "right", "left", "both", "tall"))
    d = r.choice(range(h + 2, 2 * h + 1, 2)) if caps == "tall" else 0
    w = r.choice([w for w in WIDTHS if proportioned(w, h)])
    return dict(w=w, h=h, caps=caps, d=d, height=r.choice(HEIGHTS), unit=r.choice(UNITS))

def cap_ok(w, h, caps, d, height, unit):
    return (w in WIDTHS and h in SIDES and proportioned(w, h) and caps in CAPS and height in HEIGHTS and unit in UNITS
            and (d in range(h + 2, 2 * h + 1, 2) if caps == "tall" else d == 0))

CAP_RE = re.compile(r"^(cylinder area|cylinder volume|cone volume): base (\d+) x (\d+)"
                    r"((?:, (?:right semicircle|left semicircle(?: \d+)?))*); height (\d+) (cm|m|ft|in)$")

def read_cap(prompt):
    """(kind, w, h, right?, left diameter, height, unit)."""
    m = CAP_RE.match(prompt)
    if not m:
        raise ValueError("write it like: cylinder area: base 5 x 6, right semicircle; height 10 cm")
    kind, w, h, caps, height, unit = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4), int(m.group(5)), m.group(6)
    right = "right semicircle" in caps
    lm = re.search(r"left semicircle(?: (\d+))?", caps)
    left = 0 if not lm else int(lm.group(1) or h)
    if not (w and h and height) or (left and left < h) or caps.count("right") > 1 or caps.count("left") > 1:
        raise ValueError("a left semicircle is at least as tall as the rectangle")
    if not (right or left):
        raise ValueError("give the base a semicircle")
    return kind, w, h, right, left, height, unit

def cap_parts(w, h, right, left):
    """The base's area and perimeter, from the pieces (the build's way, as the deck works it)."""
    area = w * h + (math.pi * (h / 2) ** 2 / 2 if right else 0) + (math.pi * (left / 2) ** 2 / 2 if left else 0)
    per = 2 * w + (math.pi * h / 2 if right else h) + (math.pi * left / 2 + (left - h) if left else h)
    return area, per

def cap_answer(prompt):
    kind, w, h, right, left, height, unit = read_cap(prompt)
    area, per = cap_parts(w, h, right, left)
    base = r2(area)
    if kind == "cylinder area":
        return f"{2 * base + r2(per * height)} {unit_power(unit, 2)}"
    if kind == "cylinder volume":
        return f"{r2(base * height)} {unit_power(unit, 3)}"
    return f"{r2(base * height / 3)} {unit_power(unit, 3)}"

def outline(w, h, right, left, n=4000):
    """The base's outline as a polygon, counterclockwise from the bottom-left corner."""
    pts = [(0.0, 0.0), (float(w), 0.0)]
    if right:
        pts += [(w + h / 2 * math.cos(t), h / 2 + h / 2 * math.sin(t))
                for t in (-math.pi / 2 + math.pi * i / n for i in range(1, n))]
    pts += [(float(w), float(h)), (0.0, float(h))]
    if left:
        if left > h:
            pts.append((0.0, float(left)))
        pts += [(left / 2 * math.cos(t), left / 2 + left / 2 * math.sin(t))
                for t in (math.pi / 2 + math.pi * i / n for i in range(1, n))]
    return pts

def measured(pts):
    """(area, perimeter) of a polygon."""
    a = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1])) / 2
    per = sum(math.dist(p, q) for p, q in zip(pts, pts[1:] + pts[:1]))
    return abs(a), per

DECIMAL_ANSWER = re.compile(r'^(\d+\.\d\d) "(cm|m|ft|in)"\^([23])$')

def check_cap(p):
    kind, w, h, right, left, height, unit = read_cap(p["prompt"])
    m = DECIMAL_ANSWER.match(p["answer"])
    if not m or m.group(2) != unit or int(m.group(3)) != (2 if kind == "cylinder area" else 3):
        return False
    area, per = measured(outline(w, h, right, left))
    want = {"cylinder area": 2 * area + per * height, "cylinder volume": area * height,
            "cone volume": area * height / 3}[kind]
    slack = 0.005 * {"cylinder area": 3, "cylinder volume": height + 1, "cone volume": height / 3 + 1}[kind]
    return abs(float(m.group(1)) - want) <= slack + 1e-4

# ------------------------------------------------------------------
# Type 2: a prism on a base of squares
# ------------------------------------------------------------------
SHAPES = {                                      # the squares, (column, row)
    "plus": ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    "T": ((0, 1), (1, 1), (2, 1), (1, 0)),
    "L": ((0, 0), (0, 1), (0, 2), (1, 0)),
    "S": ((0, 0), (1, 0), (1, 1), (2, 1)),
    "U": ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1)),
    "step": ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2)),
}
SQUARE = range(1, 6)
LENGTHS = range(2, 13)

def t2_build(shape, side, length, unit):
    return f"prism area: {shape}, side {side}, length {length} {unit}"

def t2_pick(r):
    return dict(shape=r.choice(("plus", "plus") + tuple(SHAPES)), side=r.choice(SQUARE),
                length=r.choice(LENGTHS), unit=r.choice(("units", "units") + UNITS))

PRISM_RE = re.compile(r"^prism area: (\w+), side (\d+), length (\d+) (units|cm|m|ft|in)$")

def read_prism(prompt):
    m = PRISM_RE.match(prompt)
    if not m or m.group(1) not in SHAPES or not (int(m.group(2)) and int(m.group(3))):
        raise ValueError(f"write it like: prism area: plus, side 2, length 6 units (shapes: {', '.join(SHAPES)})")
    return m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)

def boundary_edges(cells):
    cs = set(cells)
    return sum((c + dc, r + dr) not in cs for c, r in cs for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)))

def prism_answer(prompt):
    shape, s, L, unit = read_prism(prompt)
    cells = SHAPES[shape]
    return f"{2 * len(cells) * s * s + boundary_edges(cells) * s * L} {unit_power(unit, 2)}"

def check_prism(p):
    shape, s, L, unit = read_prism(p["prompt"])
    cells = set(SHAPES[shape])
    shared = sum((c + 1, r) in cells for c, r in cells) + sum((c, r + 1) in cells for c, r in cells)
    per = (4 * len(cells) - 2 * shared) * s
    return p["answer"] == f"{2 * len(cells) * s * s + per * L} {unit_power(unit, 2)}"

# ------------------------------------------------------------------
# Type 5: a cone's surface area; Type 7: a square pyramid's
# ------------------------------------------------------------------
RADII = range(2, 13)
SLANTS = range(3, 25)

def t5_build(r, l, unit):
    return f"cone area: radius {r}, slant {l} {unit}"

def t5_pick(r):
    rad = r.choice(RADII)
    return dict(r=rad, l=r.choice(range(rad + 1, rad + 13)), unit=r.choice(UNITS))

CONE_RE = re.compile(r"^cone area: radius (\d+), slant (\d+) (cm|m|ft|in)$")

def read_cone(prompt):
    m = CONE_RE.match(prompt)
    if not m or not int(m.group(1)) < int(m.group(2)):
        raise ValueError("write it like: cone area: radius 8, slant 10 cm (the slant longer than the radius)")
    return int(m.group(1)), int(m.group(2)), m.group(3)

def cone_answer(prompt):
    r, l, unit = read_cone(prompt)
    return f"{r * (r + l)} pi {unit_power(unit, 2)}"

def check_cone(p):
    r, l, unit = read_cone(p["prompt"])
    m = re.match(r'^(\d+) pi "(cm|m|ft|in)"\^2$', p["answer"])
    if not m or m.group(2) != unit:
        return False
    lateral = sp.Rational(2 * r, 2 * l) * sp.pi * l ** 2         # the net: a sector of the slant circle
    return sp.simplify(int(m.group(1)) * sp.pi - (sp.pi * r ** 2 + lateral)) == 0

PYR_SIDES = range(2, 13)

def t7_build(s, l, unit):
    return f"pyramid area: side {s}, slant {l} {unit}"

def t7_pick(r):
    s = r.choice(PYR_SIDES)
    return dict(s=s, l=r.choice([l for l in SLANTS if 2 * l > s and l <= 15]), unit=r.choice(UNITS))

PYR_RE = re.compile(r"^pyramid area: side (\d+), slant (\d+) (cm|m|ft|in)$")

def read_pyramid(prompt):
    m = PYR_RE.match(prompt)
    if not m or not 0 < int(m.group(1)) < 2 * int(m.group(2)):
        raise ValueError("write it like: pyramid area: side 4, slant 5 cm (the slant more than half the side)")
    return int(m.group(1)), int(m.group(2)), m.group(3)

def pyramid_answer(prompt):
    s, l, unit = read_pyramid(prompt)
    return f"{s * s + 2 * s * l} {unit_power(unit, 2)}"

def heron(a, b, c):
    q = (a + b + c) / 2
    return sp.sqrt(sp.expand(q * (q - a) * (q - b) * (q - c)))

def check_pyramid(p):
    s, l, unit = read_pyramid(p["prompt"])
    m = re.match(r'^(\d+) "(cm|m|ft|in)"\^2$', p["answer"])
    if not m or m.group(2) != unit:
        return False
    edge = sp.sqrt(l ** 2 + sp.Rational(s, 2) ** 2)                # a lateral edge, from the slant height
    face = sp.nsimplify(sp.radsimp(heron(sp.Integer(s), edge, edge)))
    return sp.simplify(int(m.group(1)) - (s * s + 4 * face)) == 0

# ------------------------------------------------------------------
# Type 6: a dimension from the volume
# ------------------------------------------------------------------
CONE_R = range(1, 10)
CONE_H = range(1, 13)
CYL_R = range(2, 11)
CYL_H = range(2, 16)
LEG_PI = range(1, 5)                           # the triangle's long leg: k pi
WEDGE_R = range(2, 7)
SECTOR = (30, 45, 60, 90, 120)
WEDGE_H = range(1, 13)

def t6_cone_build(r, h, unit):
    return f"cone radius: volume {r * r * h // 3} pi, height {h} {unit}"

def t6_cone(r):
    rad, h = r.choice(CONE_R), r.choice(CONE_H)
    need(rad * rad * h % 3 == 0)
    return dict(r=rad, h=h, unit=r.choice(UNITS))

def t6_cyl_build(r, H, unit):
    return f"cylinder height: radius {r}, volume {r * r * H} pi {unit}"

def t6_cyl(r):
    return dict(r=r.choice(CYL_R), H=r.choice(CYL_H), unit=r.choice(UNITS))

def wedge_area(k, b, angle):
    """The base over pi: the triangle (1/2)(k pi)(b) and the sector (angle/360) pi b^2."""
    return F(k * b, 2) + F(angle * b * b, 360)

def t6_wedge_build(k, b, angle, H, unit):
    v = wedge_area(k, b, angle) * H
    return f"wedge height: legs {'' if k == 1 else f'{k} '}pi and {b}, sector {angle}, volume {v} pi {unit}"

def t6_wedge(r):
    k, b, angle, H = r.choice(LEG_PI), r.choice(WEDGE_R), r.choice(SECTOR), r.choice(WEDGE_H)
    need((wedge_area(k, b, angle) * H).denominator == 1)
    return dict(k=k, b=b, angle=angle, H=H, unit=r.choice(UNITS))

DIM_RE = {
    "cone radius": re.compile(r"^cone radius: volume (\d+) pi, height (\d+) (cm|m|ft|in)$"),
    "cylinder height": re.compile(r"^cylinder height: radius (\d+), volume (\d+) pi (cm|m|ft|in)$"),
    "wedge height": re.compile(r"^wedge height: legs (\d*) ?pi and (\d+), sector (\d+), volume (\d+) pi (cm|m|ft|in)$"),
}

def read_dimension(prompt):
    """(kind, numbers, unit)."""
    for kind, rx in DIM_RE.items():
        m = rx.match(prompt)
        if m:
            g = m.groups()
            nums = [int(x) if x else 1 for x in g[:-1]]
            if not all(nums) or (kind == "wedge height" and not 0 < nums[2] < 180):
                raise ValueError("every number is positive; the sector's angle is under 180")
            return kind, nums, g[-1]
    raise ValueError("write it like: cone radius: volume 6 pi, height 2 cm")

def dimension_answer(prompt):
    kind, nums, unit = read_dimension(prompt)
    if kind == "cone radius":
        v, h = nums
        r2_ = F(3 * v, h)
        need(r2_.denominator == 1 and math.isqrt(int(r2_)) ** 2 == r2_)
        x = math.isqrt(int(r2_))
    elif kind == "cylinder height":
        r, v = nums
        x = F(v, r * r)
    else:
        k, b, angle, v = nums
        x = F(v) / wedge_area(k, b, angle)
    need(F(x).denominator == 1)
    return f'{x} "{unit}"'

def check_dimension(p):
    kind, nums, unit = read_dimension(p["prompt"])
    m = re.match(r'^(\d+) "(cm|m|ft|in)"$', p["answer"])
    if not m or m.group(2) != unit:
        return False
    x = sp.Integer(m.group(1))
    if kind == "cone radius":
        v, h = nums
        return sp.Rational(1, 3) * sp.pi * x ** 2 * h == v * sp.pi
    if kind == "cylinder height":
        r, v = nums
        return sp.pi * r ** 2 * x == v * sp.pi
    k, b, angle, v = nums
    tri = [(0, 0), (k * sp.pi, 0), (k * sp.pi, b)]                 # legs k pi along the bottom, b up
    t = abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(tri, tri[1:] + tri[:1]))) / 2
    return sp.simplify((t + sp.Rational(angle, 360) * sp.pi * b ** 2) * x - v * sp.pi) == 0

# ------------------------------------------------------------------
# Templates and ranges
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(cap_pick, t1_build)],
    "2": [(t2_pick, t2_build)],
    "3": [(cap_pick, t3_build)],
    "4": [(cap_pick, t4_build)],
    "5": [(t5_pick, t5_build)],
    "6": [(t6_cone, t6_cone_build), (t6_cyl, t6_cyl_build), (t6_wedge, t6_wedge_build)],
    "7": [(t7_pick, t7_build)],
}

RANGES = {
    t1_build: cap_ok, t3_build: cap_ok, t4_build: cap_ok,
    t2_build: lambda shape, side, length, unit: (shape in SHAPES and side in SQUARE and length in LENGTHS
                                                 and unit in ("units",) + UNITS),
    t5_build: lambda r, l, unit: r in RADII and l in range(r + 1, r + 13) and unit in UNITS,
    t7_build: lambda s, l, unit: s in PYR_SIDES and l in SLANTS and l <= 15 and 2 * l > s and unit in UNITS,
    t6_cone_build: lambda r, h, unit: r in CONE_R and h in CONE_H and r * r * h % 3 == 0 and unit in UNITS,
    t6_cyl_build: lambda r, H, unit: r in CYL_R and H in CYL_H and unit in UNITS,
    t6_wedge_build: lambda k, b, angle, H, unit: (k in LEG_PI and b in WEDGE_R and angle in SECTOR and H in WEDGE_H
                                                  and (wedge_area(k, b, angle) * H).denominator == 1
                                                  and unit in UNITS),
}

def in_range(build, params):
    """Can a random draw pick these parameters for this build?"""
    return RANGES[build](**params)

# ------------------------------------------------------------------
# Solving and checking
# ------------------------------------------------------------------
KIND = {"1": "cylinder area", "2": "prism area", "3": "cylinder volume", "4": "cone volume",
        "5": "cone area", "6": ("cone radius", "cylinder height", "wedge height"), "7": "pyramid area"}

def kind(prompt):
    return prompt.split(":")[0].strip()

def solver(k):
    return {"prism area": (prism_answer, check_prism), "cone area": (cone_answer, check_cone),
            "pyramid area": (pyramid_answer, check_pyramid)}.get(
        k, (cap_answer, check_cap) if k in ("cylinder area", "cylinder volume", "cone volume")
        else (dimension_answer, check_dimension))

def answer_of(prompt):
    return solver(kind(prompt))[0](prompt)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt))

def kind_fits(typ, prompt):
    k, want = kind(prompt), KIND[typ]
    return k in want if isinstance(want, tuple) else k == want

def check(p):
    try:
        if not kind_fits(p["type"], p["prompt"]):
            return "failed"
        ok = solver(kind(p["prompt"]))[1](p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def cube(unit, n):
    return f"{unit}#super[{n}]" if unit != "units" else f"{'square' if n == 2 else 'cubic'} units"

def statement(p):
    """The problem's words (Typst markup), without its figure."""
    pr, k = p["prompt"], kind(p["prompt"])
    if k in ("cylinder area", "cylinder volume", "cone volume"):
        _, w, h, right, left, height, unit = read_cap(pr)
        u = WORDS[unit]
        if k == "cylinder area":
            return (f"The base of a right cylinder {height} {u} high is shown. Find the surface area of the "
                    f"right cylinder. Dimensions are in {u}.")
        if k == "cylinder volume":
            return (f"The figure shows the base of a right cylinder that is {height} {u} high. Find the "
                    f"volume of the right cylinder. Dimensions are in {u}.")
        return (f"The base of a cone is shown. The dimensions are in {u}. If the cone is {height} {u} high, "
                f"what is its volume?")
    if k == "prism area":
        _, _, _, unit = read_prism(pr)
        return "Find the surface area of this right prism." + ("" if unit == "units" else f" Dimensions are in {WORDS[unit]}.")
    if k == "cone area":
        r, l, unit = read_cone(pr)
        return (f"The radius of the base of a right circular cone is {r} {unit}. The slant height of the cone "
                f"is {l} {unit}. Find the surface area of the cone.")
    if k == "pyramid area":
        s, l, unit = read_pyramid(pr)
        return (f"The base of a regular pyramid is a square with each side measuring {s} {unit}. The slant "
                f"height of the pyramid is {l} {unit}. Find the surface area of the pyramid.")
    kd, nums, unit = read_dimension(pr)
    if kd == "cone radius":
        v, h = nums
        return (f"The volume of a right circular cone is ${v} pi$ {cube(unit, 3)}. The height of this right "
                f"circular cone is {h} {unit}. Find the radius of the base of the cone.")
    if kd == "cylinder height":
        r, v = nums
        return (f"The volume of this circular cylinder is ${v} pi$ {cube(unit, 3)}. What is the height of "
                f"the circular cylinder? Dimensions are in {WORDS[unit]}.")
    k_, b, angle, v = nums
    return (f"The base of a right cylinder is a right triangle joined by a ${angle}°$ sector of a circle, as "
            f"shown. The volume of this right cylinder is ${v} pi$ {cube(unit, 3)}. What is the height of the "
            f"right cylinder? Dimensions are in {WORDS[unit]}.")

def figure(p, unit="1cm"):
    """The figure, drawn from the prompt's data; "" when the words are enough."""
    pr, k = p["prompt"], kind(p["prompt"])
    if k in ("cylinder area", "cylinder volume", "cone volume"):
        _, w, h, right, left, height, _u = read_cap(pr)
        labels = dict(top=f"${w}$", bottom=f"${w}$", radius=f"${h // 2 if right else left // 2}$")
        if not (right and left):
            labels["side"] = f"${h}$"
        if left > h:
            labels["rise"] = f"${left - h}$"
            labels["radius"] = f"${h // 2}$"
        return fig.capped_base(w, h, right, left, labels, unit=unit)
    if k == "prism area":
        shape, s, L, _u = read_prism(pr)
        return fig.prism(SHAPES[shape], f"${s}$", f"${L}$", unit=unit)
    if k in DIM_RE:
        kd, nums, _u = read_dimension(pr)
        if kd == "cylinder height":
            return fig.oblique_cylinder(f"${nums[0]}$", "$H$", unit=unit)
        if kd == "wedge height":
            kk, b, angle, _v = nums
            return fig.wedge_base((kk * math.pi, f"${'' if kk == 1 else kk} pi$"), (b, f"${b}$"), angle, unit=unit)
    return ""

def typst(p, gap="0.3em"):
    try:
        s, f = statement(p), figure(p)
    except ValueError:
        return p["prompt"]
    return s if not f else f"{s} #v(0.4em) #align(center)[{f}]"

def answer_typst(p):
    return "$" + p["answer"].replace(' "', ' thin "') + "$"

SLIDE_UNIT = "2cm"

def slide_typst(p, key=False):
    """A figure's slide: the words (and the answer, hidden on the question slide)
    beside the figure drawn larger; the figure never moves. None without a figure."""
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
        s, f = statement(p), figure(p)
    except ValueError:
        return p["prompt"]
    s = s.replace("$", "").replace("#super[2]", "²").replace("#super[3]", "³").replace(" pi", "π")
    return plain(s) + ("   [figure]" if f else "")

def answer_text(p):
    a = p["answer"].replace('"', "").replace("^2", "²").replace("^3", "³").replace(" pi", "π")
    return plain(a)

def height(p):
    try:
        return 2.4 if figure(p) else 0.5
    except ValueError:
        return 0.5

# ------------------------------------------------------------------
# Editing: the prompt is the problem's data, in its short form
# ------------------------------------------------------------------
EXAMPLE = {"1": "cylinder area: base 5 x 6, right semicircle; height 10 cm",
           "2": "prism area: plus, side 2, length 6 units",
           "3": "cylinder volume: base 11 x 10, right semicircle, left semicircle 20; height 9 cm",
           "4": "cone volume: base 3 x 2, right semicircle; height 6 m",
           "5": "cone area: radius 8, slant 10 cm",
           "6": "cone radius: volume 6 pi, height 2 cm",
           "7": "pyramid area: side 4, slant 5 cm"}

def clean(t):
    return " ".join(t.replace("π", " pi").replace("−", "-").split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    try:
        if not kind_fits(old["type"], t):
            raise ValueError
        answer = answer_of(t)
    except (ValueError, gen.Redraw, KeyError):
        raise ValueError(f"write it like: {EXAMPLE[old['type']]}") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
