"""Lesson 2-2: Point-Slope Form. Six types:

    1  Slope from two points        (2, -3) and (5, 9)            m = 4
    2  Point-slope to slope-intercept   y + 3 = 2/3 (x - 4)       y = 2/3 x - 17/3
    3  Slope and a point            m = 2/3, through (4, -3)      y + 3 = 2/3 (x - 4); y = 2/3 x - 17/3
    4  Two points                   (2, -3) and (5, 9)            m = 4; y + 3 = 4 (x - 2); y = 4 x - 11
    5  Graph point-slope form       y + 3 = 2/3 (x - 4), a blank graph; the key draws the line
    6  A table of five points       x and y columns, a point to a row  y - 5 = -1/2 (x + 2); y = -1/2 x + 4

Point-slope form is y - y1 = m (x - x1), the signs worked out: y + 3 = 2/3 (x - 4).
A slope of 1 is left off, y - 3 = x - 1; a slope of -1 is a minus sign, y - 3 = -(x - 1).
Every point written in point-slope form has non-zero coordinates (so both sides keep their
number); the key uses the given point (Type 3), the first point (Type 4), or the table's
first column (Type 6). An edited answer through any of the problem's points is accepted.

The numbers:
    - A drawn slope (Types 2, 3, 6) is a whole number 1 to 6 or a fraction in lowest terms,
      denominator 2 to 5, numerator up to 7, either sign; about two in five are whole.
    - Types 1 and 4: integer points from -10 to 10 that differ in x and in y (no horizontal or
      vertical line), the slope's denominator at most 6; in Type 4, no coordinate is 0 and the
      y-intercept is at most 20 either way.
    - Types 2 and 3: the point's coordinates are -9 to 9, not 0; the y-intercept, often a
      fraction, is at most 20 either way.
    - Type 5: as Lesson 2-1's lines, a slope a/c, c 1 to 6, |a| up to 9 (up to 5 when whole);
      the point is from -8 to 8, not 0, and the line crosses another lattice point on the
      -10 to 10 graph.
    - Type 6: the x's go up by the same step, the slope's denominator times 1 or 2 (or 1, 2, 3
      for a whole slope), the first from -8 to 8; every x and y is from -20 to 20, the first
      column's not 0; the y-intercept is at most 20 either way.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  1, 4: "(2, -3), (5, 9)"    2, 5: "y + 3 = 2/3 (x - 4)"    3: "m = 2/3, (4, -3)"
            6: "(-2, 5), (0, 4), (2, 3), (4, 2), (6, 1)"
    answer  its parts, "; " between: "m = 4; y + 3 = 4 (x - 2); y = 4 x - 11"
            (Type 5's is y = m x + b, which the key graphs; the graph is its answer.)
check() reads each part back from its text, independently of how it was written, and
compares it with the line the prompt gives: the slope must be in lowest terms, point-slope
form must be through one of the problem's points (the given one in Type 3) with the
problem's slope, and slope-intercept form is read as Lesson 2-1 reads it.
"""
import math
import re
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need, written
from ..check import to_sympy
from ..graphs import Graph, PREAMBLE
from ..typmath import display, dfrac, text as plain
from . import slope_intercept_2_1 as si

NAME = FAMILY = "point_slope_2_2"
FIXED = False
TITLE = "Lesson 2-2: Point-Slope Form"
INSTRUCTIONS = ""              # each type has its own; a sheet of one type shows it at the top
COURSES = {"Algebra 1": "Lessons"}

TYPES = [
    dict(key="1", title="Slope From Two Points", instructions="Find the slope of the line through each pair of points.",
         look="Two points: (2, -3) and (5, 9).",
         move="m = (y2 - y1)/(x2 - x1) = (9 - (-3))/(5 - 2) = 12/3 = 4. Subtract in the same order "
              "on top and bottom, and write the slope in lowest terms.",
         space="1in"),
    dict(key="2", title="Point-Slope to Slope-Intercept", instructions="Write each equation in slope-intercept form.",
         look="An equation in point-slope form: y + 3 = 2/3 (x - 4).",
         move="Distribute the slope: y + 3 = 2/3 x - 8/3. Then get y alone: subtract 3 (as 9/3) from "
              "both sides: y = 2/3 x - 17/3."),
    dict(key="3", title="Slope and a Point",
         instructions="Write the equation of the line with the given slope through the given point in "
                      "point-slope form, then in slope-intercept form.",
         look="A slope and a point: m = 2/3, through (4, -3).",
         move="Put the point and the slope into y - y1 = m(x - x1): y - (-3) = 2/3 (x - 4), so "
              "y + 3 = 2/3 (x - 4). Then distribute and get y alone: y = 2/3 x - 17/3.",
         space="1.5in"),
    dict(key="4", title="Two Points to Both Forms",
         instructions="Find the slope of the line through each pair of points. Then write its equation in "
                      "point-slope form, and then in slope-intercept form.",
         look="Two points: (2, -3) and (5, 9).",
         move="Slope first: m = (9 - (-3))/(5 - 2) = 4. Put the first point into point-slope form: "
              "y + 3 = 4 (x - 2). Distribute and get y alone: y = 4x - 11.",
         space="1.75in"),
    dict(key="5", title="Graph Point-Slope Form", instructions="Graph each line.",
         look="An equation in point-slope form, y + 3 = 2/3 (x - 4), and a blank graph.",
         move="Read the point: (4, -3), the opposites of the numbers with x and y. Plot it. From it, "
              "rise the slope's numerator and run its denominator (a negative slope goes down as it "
              "goes right) to plot more points. Draw the line through them.",
         space="0in"),
    dict(key="6", title="Equation From a Table",
         instructions="Write the equation of the line through the points in each table, in point-slope form "
                      "and then in slope-intercept form.",
         look="A table of five points on a line: x is -2, 0, 2, 4, 6 and y is 5, 4, 3, 2, 1.",
         move="Slope from any two columns: m = (4 - 5)/(0 - (-2)) = -1/2. Put a point, like the first, "
              "into point-slope form: y - 5 = -1/2 (x + 2). Distribute and get y alone: y = -1/2 x + 4.",
         space="1.5in"),
]

T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

WINDOW = 10                    # Types 1, 4, 5: coordinates and the graph, -10 to 10
POINT = 9                      # Types 2, 3: the point's coordinates, -9 to 9
GRAPH_POINT = 8                # Type 5: the point, -8 to 8
INTERCEPT = 20                 # Types 2, 3: the y-intercept at most this
SLOPE_DENOMINATOR = 6          # Type 4: the slope's denominator at most this
TABLE = 20                     # Type 6: every x and y at most this
TABLE_START = 8                # Type 6: the first x from -8 to 8
ROWS = 5                       # Type 6: a table's points
TWO = ("1", "4")               # a prompt of two points
EQUATION = ("2", "5")          # a prompt in point-slope form
PARTS = {"1": ("m",), "2": ("si",), "3": ("ps", "si"), "4": ("m", "ps", "si"), "5": ("si",), "6": ("ps", "si")}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Writing
# ------------------------------------------------------------------
def less(v, n):
    """v - n, written: "y - 3", "x + 4", "y" when n is 0."""
    return written((1, v), (-n, ""))

def point_slope(m, x1, y1):
    """y - y1 = m (x - x1) as the key writes it: "y + 3 = 2/3 (x - 4)", "y - 3 = x - 1",
    "y - 3 = -(x - 1)"; m a Fraction, not 0."""
    inner = less("x", x1)
    if m == 1 or x1 == 0:
        right = written((m, inner if m == 1 else "x"))
    elif m == -1:
        right = f"-({inner})"
    else:
        right = written((m, f"({inner})"))
    return f"{less('y', y1)} = {right}"

def slope_eq(m):
    return f"m = {written((m, ''))}"

slope_intercept = si.slope_intercept

def points_text(pts):
    """"(2, -3), (5, 9)"."""
    return ", ".join(f"({x}, {y})" for x, y in pts)

def given_text(m, pt):
    """Type 3's prompt: "m = 2/3, (4, -3)"."""
    return f"{slope_eq(m)}, ({pt[0]}, {pt[1]})"

def answer(typ, m, pt):
    """The key's answer: the type's parts, "; " between; pt the point it writes point-slope form through."""
    b = pt[1] - m * pt[0]
    part = dict(m=lambda: slope_eq(m), ps=lambda: point_slope(m, *pt), si=lambda: slope_intercept(m, b))
    return "; ".join(part[k]() for k in PARTS[typ])

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def slope(r):
    """A whole number 1 to 6, or a fraction in lowest terms (denominator 2 to 5, numerator up to 7); either sign."""
    if r.random() < 0.4:
        return F(gen.signed(r, 1, 6))
    c, a = r.randint(2, 5), gen.signed(r, 1, 7)
    need(math.gcd(a, c) == 1)
    return F(a, c)

def nonzero(r, n):
    return gen.signed(r, 1, n)

def draw(entry, r, tpl):
    if entry in TWO:
        pts = [(r.randint(-WINDOW, WINDOW), r.randint(-WINDOW, WINDOW)) for _ in range(2)]
        need(two_keep_rules(entry, pts))
        m, _ = si.through([(F(x), F(y)) for x, y in pts])
        return dict(prompt=points_text(pts), answer=answer(entry, m, pts[0]))
    if entry in ("2", "3"):
        m, pt = slope(r), (nonzero(r, POINT), nonzero(r, POINT))
        need(abs(pt[1] - m * pt[0]) <= INTERCEPT)
        prompt = point_slope(m, *pt) if entry == "2" else given_text(m, pt)
        return dict(prompt=prompt, answer=answer(entry, m, pt))
    if entry == "5":
        c, a = r.randint(1, 6), gen.signed(r, 1, 9)
        need(math.gcd(a, c) == 1 and (c > 1 or abs(a) <= 5))
        m, pt = F(a, c), (nonzero(r, GRAPH_POINT), nonzero(r, GRAPH_POINT))
        need(graph_keeps_rules(m, pt))
        return dict(prompt=point_slope(m, *pt), answer=answer(entry, m, pt))
    m = slope(r)                                              # Type 6
    dx = m.denominator * r.choice((1, 2, 3) if m.denominator == 1 else (1, 2))
    x0, y0 = r.randint(-TABLE_START, TABLE_START), r.randint(-TABLE, TABLE)
    pts = [(x0 + i * dx, y0 + m * i * dx) for i in range(ROWS)]
    need(table_keeps_rules(pts))
    return dict(prompt=points_text([(x, int(y)) for x, y in pts]), answer=answer(entry, m, (x0, int(y0))))

def two_keep_rules(entry, pts):
    """Types 1 and 4: integer points from -10 to 10, differing in x and in y, the slope's
    denominator at most 6; in Type 4, no coordinate 0 and the y-intercept at most 20 either way."""
    (x1, y1), (x2, y2) = pts
    if x1 == x2 or y1 == y2 or any(v != int(v) or abs(v) > WINDOW for p in pts for v in p):
        return False
    m = F(y2 - y1) / (x2 - x1)
    if m.denominator > SLOPE_DENOMINATOR:
        return False
    if entry == "4":
        return all(v != 0 for p in pts for v in p) and abs(y1 - m * x1) <= INTERCEPT
    return True

def graph_keeps_rules(m, pt):
    """Type 5: the point on the graph and not on an axis, and another lattice point on the graph."""
    x1, y1 = pt
    if x1 == 0 or y1 == 0 or abs(x1) > GRAPH_POINT or abs(y1) > GRAPH_POINT:
        return False
    return any((x, y) != (x1, y1) for x, y in si.lattice_points(m, y1 - m * x1))

def table_keeps_rules(pts):
    """Type 6: five integer points on one line (not horizontal), the x's going up by the same step;
    every coordinate from -20 to 20, the first point's not 0; the y-intercept at most 20 either way."""
    if len(pts) != ROWS or any(F(v).denominator != 1 or abs(v) > TABLE for p in pts for v in p):
        return False
    dx = pts[1][0] - pts[0][0]
    if dx <= 0 or pts[0][0] == 0 or pts[0][1] == 0:
        return False
    m = F(pts[1][1] - pts[0][1], dx)
    if m == 0 or abs(pts[0][1] - m * pts[0][0]) > INTERCEPT:
        return False
    return all(x == pts[0][0] + i * dx and y == pts[0][1] + m * i * dx for i, (x, y) in enumerate(pts))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: 1)

# ------------------------------------------------------------------
# Reading back and checking
# ------------------------------------------------------------------
X, Y = sp.Symbol("x"), sp.Symbol("y")
INT = r"\d+"
FRAC = r"\d+/\d+|\d+"
SLOPE = re.compile(rf"m = (?P<m>-?(?:{FRAC}))")
SIDE = re.compile(rf"(?P<v>[xy])(?: (?P<s>[+-]) (?P<n>{INT}))?")
RIGHT = re.compile(rf"(?P<c>-?(?:{FRAC}) |-)?(?:\((?P<inner>x [+-] {INT})\)|(?P<bare>x(?: [+-] {INT})?))")

def lowest(t):
    """A number written in lowest terms ("4", "-2/3"), as a Fraction; None if it isn't (4/2, 3/1, -0)."""
    try:
        v = F(t)
    except (ValueError, ZeroDivisionError):
        return None
    return v if str(v) == t else None

def read_slope(t):
    g = SLOPE.fullmatch(" ".join(t.split()))
    return None if g is None else lowest(g["m"])

def side(t, v):
    """"y + 3" -> -3 (the y1 of y - y1); None if it isn't v - n written as the key writes it."""
    g = SIDE.fullmatch(t)
    if not g or g["v"] != v or g["n"] == "0":
        return None
    return F(0) if g["n"] is None else F(int(g["n"])) * (1 if g["s"] == "-" else -1)

def read_point_slope(t):
    """(m, x1, y1) of an equation written y - y1 = m (x - x1) (signs worked out, m in lowest terms,
    1 and -1 as the key writes them); None if it isn't. Its text must also say what it was read as."""
    t = " ".join(t.replace("−", "-").split())
    lhs, eq, rhs = t.partition(" = ")
    y1 = side(lhs, "y")
    g = RIGHT.fullmatch(rhs)
    if not eq or y1 is None or not g:
        return None
    c, inner = (g["c"] or "").strip(), g["inner"] or g["bare"]
    x1 = side(inner, "x")
    if x1 is None:
        return None
    if g["bare"] is not None:                    # 2 x, x - 4, -x: m (x - x1) with nothing to wrap
        if (x1 != 0 and c != "") or c in ("1", "-1"):
            return None
        m = F(-1) if c == "-" else F(1) if c == "" else lowest(c)
    else:                                        # 2/3 (x - 4), -(x - 4)
        m = F(-1) if c == "-" else None if c in ("", "1", "-1") else lowest(c)
    if m is None or m == 0:
        return None
    try:
        e = to_sympy(lhs) - to_sympy(rhs)
        want = (Y - sp.Rational(y1.numerator, y1.denominator)) - sp.Rational(m.numerator, m.denominator) * (
            X - sp.Rational(x1.numerator, x1.denominator))
        if sp.expand(e - want) != 0:
            return None
    except Exception:
        return None
    return m, x1, y1

def read_slope_intercept(t):
    """(m, b) of y = m x + b, read as Lesson 2-1 reads it, and its text saying the same; None if not."""
    got = si.written_form(t)
    if got is None:
        return None
    m, b = got
    if sp.expand(to_sympy(t.partition("=")[2]) - (sp.Rational(m.numerator, m.denominator) * X + b)) != 0:
        return None
    return m, b

def points_of(prompt):
    """The points of a prompt "(2, -3), (5, 9)", as Fractions; ValueError if there are none to read."""
    t = " ".join(prompt.replace("−", "-").split())
    pts = si.POINT.findall(t)
    if not pts or si.POINT.sub("", t).replace(",", "").replace("and", "").strip():
        raise ValueError("write points, like (2, -3), (5, 9)")
    return [(si.number(a), si.number(b)) for a, b in pts]

def given_of(prompt):
    """Type 3's (m, point) from "m = 2/3, (4, -3)"; ValueError if it isn't."""
    t = " ".join(prompt.replace("−", "-").split())
    head, _, rest = t.partition(", (")
    m = read_slope(head)
    pts = points_of("(" + rest) if rest else []
    if m is None or m == 0 or len(pts) != 1:
        raise ValueError("write a slope and a point, like m = 2/3, (4, -3)")
    return m, pts[0]

def line_of(p):
    """(m, b, points) of the line the prompt gives, worked out from the prompt alone; points are those
    point-slope form may go through. ValueError if the prompt breaks its type's rules."""
    typ = p["type"]
    if typ in TWO:
        pts = points_of(p["prompt"])
        if len(pts) != 2 or not two_keep_rules(typ, pts):
            raise ValueError("two points that differ in x and in y")
        m, b = si.through(pts)
        return m, b, pts
    if typ in EQUATION:
        got = read_point_slope(p["prompt"])
        if got is None:
            raise ValueError("write it in point-slope form, like y + 3 = 2/3 (x - 4)")
        m, b = si.solved(p["prompt"])            # sympy solves it for y: the prompt's line, independently
        if m != got[0] or got[2] != m * got[1] + b:
            raise ValueError("the equation doesn't say what it was read as")
        if typ == "5" and not graph_keeps_rules(m, got[1:]):
            raise ValueError("the line breaks Type 5's rules")
        return m, b, [got[1:]]
    if typ == "3":
        m, pt = given_of(p["prompt"])
        return m, pt[1] - m * pt[0], [pt]
    pts = points_of(p["prompt"])
    if not table_keeps_rules(pts):
        raise ValueError("five points on a line, the x's going up by the same step")
    m, b = si.through(pts[:2])
    return m, b, pts

def check(p):
    try:
        try:
            m, b, pts = line_of(p)
        except ValueError:
            return "failed"                          # the prompt breaks its type's rules
        parts = p["answer"].split(";")
        if len(parts) != len(PARTS[p["type"]]):
            return "failed"
        for kind, t in zip(PARTS[p["type"]], (s.strip() for s in parts)):
            if kind == "m" and read_slope(t) != m:
                return "failed"
            if kind == "si" and read_slope_intercept(t) != (m, b):
                return "failed"
            if kind == "ps":
                got = read_point_slope(t)
                if got is None or got[0] != m or got[1:] not in [tuple(q) for q in pts]:
                    return "failed"
        if p["type"] in ("2", "3") and (abs(b) > INTERCEPT or not all(v != 0 for v in pts[0])):
            return "failed"
        return "checked"
    except Exception:
        return "unchecked"

def answer_of(prompt, typ):
    """The key's answer for a prompt of that type, through its (first) point."""
    m, _, pts = line_of(dict(type=typ, prompt=prompt))
    return answer(typ, m, pts[0])

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
SHEET_WIDTH = si.SHEET_WIDTH
SHEET_GAP = si.SHEET_GAP
SLIDE_WIDTH = si.SLIDE_WIDTH
SLIDE_NUMBERS = si.SLIDE_NUMBERS
ASKED = "Graph: "

def graph(p, key=False, width=SHEET_WIDTH, size=6, every=None):
    """Type 5's -10 to 10 graph: blank, or on the key, the line through its lattice points."""
    g = Graph(x=(-WINDOW, WINDOW), y=(-WINDOW, WINDOW), width=width, size=size, label=every)
    edge = WINDOW + 1.5            # a fixed frame, so a line's arrow past the grid never moves the graph
    g.cmds.append(f"rect({g.c(-edge, -edge)}, {g.c(edge, edge)}, stroke: none)")
    got = read_slope_intercept(p["answer"]) if key else None
    if got:
        m, b = got
        g.line(float(m), float(b), color="red")
        for x, y in si.lattice_points(m, b):
            g.point(x, float(y), color="red")
    return g.typst()

def table_typst(pts):
    """A table of the points, down the page: x and y heading two columns, a point to a row."""
    cells = ["[$x$]", "[$y$]"] + [f"[${x}$], [${y}$]" for x, y in pts]
    return ("#table(columns: (2.2em, 2.2em), align: center, inset: (x: 6pt, y: 3pt), "
            "fill: (c, r) => if r == 0 { luma(230) }, " + ", ".join(cells) + ")")

def eq_typst(t):
    return display(dfrac(t))

def typst(p, gap="0.3em", key=False):
    typ = p["type"]
    try:
        if typ in TWO:
            a, b = (eq_typst(f"({x}, {y})") for x, y in points_of(p["prompt"]))
            return f"{a} and {b}"
        if typ == "3":
            m, (x, y) = given_of(p["prompt"])
            return f"{eq_typst(slope_eq(m))}, through {eq_typst(f'({x}, {y})')}"
        if typ == "6":
            return table_typst(points_of(p["prompt"]))
    except ValueError:
        pass
    if typ == "5":
        return f"{ASKED}{eq_typst(p['prompt'])} #v({SHEET_GAP}) #align(center)[{graph(p, key)}]"
    return eq_typst(p["prompt"])

def key_typst(p, gap="0.3em"):
    return typst(p, gap, key=p["type"] == "5")

def answer_typst(p):
    """Each part on its own line; Type 5's answer is the graph alone (key_typst)."""
    if p["type"] == "5":
        return ""
    parts = [eq_typst(s.strip()) for s in p["answer"].split(";")]
    if len(parts) == 1:
        return parts[0]
    # Each line as tall as its fractions really are, so a line of fractions never runs into the next.
    return ('#[#set text(top-edge: "bounds", bottom-edge: "bounds"); #stack(spacing: 0.4em, '
            + ", ".join(f"align(right)[{t}]" for t in parts) + ")]")

def slide_typst(p, key=False):
    """Type 5's slide: the graph, larger, beside the equation; it never moves when the key draws the line.
    None for the others, which show as usual."""
    if p["type"] != "5":
        return None
    g = graph(p, key, width=SLIDE_WIDTH, size=SLIDE_NUMBERS, every=2)
    return f"#grid(columns: 2, column-gutter: 1.5em, align: horizon, [{ASKED}{eq_typst(p['prompt'])}], [{g}])"

def text(p):
    typ = p["type"]
    if typ in TWO:
        return plain(p["prompt"].replace("), (", ") and ("))
    if typ == "3":
        return plain(p["prompt"].replace(", (", ", through ("))
    if typ == "5":
        return ASKED + plain(p["prompt"]) + "   [graph]"
    if typ == "6":
        try:
            pts = points_of(p["prompt"])
            return "x: " + "  ".join(str(x) for x, _ in pts) + "   y: " + "  ".join(str(y) for _, y in pts)
        except ValueError:
            return plain(p["prompt"])
    return plain(p["prompt"])

def answer_text(p):
    if p["type"] == "5":
        got = read_slope_intercept(p["answer"])
        if got:
            pts = ", ".join(f"({x}, {y})" for x, y in si.lattice_points(*got))
            return plain(p["answer"]) + "   graphed through " + pts
    return "   ".join(plain(s.strip()) for s in p["answer"].split(";"))

def height(p):
    return 2.6 if p["type"] == "5" else 1.4 if p["type"] == "6" else 0.55 if "/" in p["prompt"] else 0.3

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
EXAMPLE = {"1": "(2, -3), (5, 9)", "2": "y + 3 = 2/3 (x - 4)", "3": "m = 2/3, (4, -3)",
           "4": "(2, -3), (5, 9)", "5": "y + 3 = 2/3 (x - 4)", "6": "(-2, 5), (0, 4), (2, 3), (4, 2), (6, 1)"}

def edit_text(p):
    return p["prompt"]

def answer_edit_text(p):
    return p["answer"]

def from_edit(t, old):
    """An edited prompt, its answer worked out again (one that breaks the type's rules keeps the
    old answer, which check() marks)."""
    typ = old.get("type")
    t = " ".join(t.replace("−", "-").split())
    try:
        if typ in TWO or typ == "6":
            pts = points_of(t)
            t = points_text([(si.mixed(x), si.mixed(y)) for x, y in pts])
        elif typ == "3":
            m, (x, y) = given_of(t)
            t = given_text(m, (si.mixed(x), si.mixed(y)))
        else:
            si._equation(t, EXAMPLE[typ])
    except ValueError:
        raise ValueError(f"write it like {EXAMPLE[typ]}") from None
    try:
        ans = answer_of(t, typ)
    except (ValueError, gen.Redraw):
        ans = old["answer"]
    new = dict(old, prompt=t, answer=ans, source="edited")
    return new, check(new)

def with_answer(p, t):
    new = dict(p, answer="; ".join(" ".join(s.replace("−", "-").split()) for s in t.split(";")))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
