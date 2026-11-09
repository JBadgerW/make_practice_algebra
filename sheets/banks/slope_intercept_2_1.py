"""Lesson 2-1: Slope-Intercept Form, taught as a sequence of steps; each
step is an entry ("1" is Step 1). More steps will follow.

Steps 1 to 4: every line is built backward from the answer, y = (a/c) x + b:
    - the slope a/c is in lowest terms, a != 0: a fraction (c 2 to 6, |a| up to 9)
      or a whole number (c = 1, |a| up to 5);
    - the y-intercept b is an integer, -9 to 9;
    - on the graph from -10 to 10 on both axes, the line passes through
      (0, b) and at least one other lattice point.

Step 1: Solve for y. The line starts in one of six forms (a sheet's
Step 1 problems are spread evenly over them, apart from its Step 3
problems; gen.generator's balance):
    A   c y = a x + c b              3 y = 2 x - 12
    B   c y - a x = c b              3 y - 2 x = -12
    C   a x = c y - c b              2 x = 3 y + 12
    D   x = (c/a) y - c b/a          x = 3/2 y + 6
    E   (c/a) y = x + c b/a          3/2 y = x - 6
    F   c b/a = (c/a) y - x          -6 = 3/2 y - x
Fractions in D, E, and F are in lowest terms (an integer when a divides).
A form that comes out already solved for y (A, or E with slope 1, when
c = 1) is drawn again.

Step 2: Graph. The line is given as y = m x + b, with a blank graph, -10 to
10 on both axes; the key draws the line through its lattice points.

Step 3: Solve for y, then graph. A Step 1 form (spread over the six the
same way) with a blank graph; the key gives y = m x + b and draws the line.
Steps 2 and 3 show "Graph: " before the equation, so a problem says what to
do without its step's instructions (the prompt itself is the equation alone).

Step 4: Write the equation. The line is drawn on the graph, with no
equation; the key gives y = m x + b. The prompt holds the line's own
y = m x + b, which draws it; the graph is the same on the sheet and the key.

Steps 5 to 7: Write the equation through two points. The prompt is two
points, "(2, 3), (5, 9)" (shown "Through (2, 3) and (5, 9)"); the key gives
y = m x + b, b a fraction in lowest terms when it isn't whole. Every
coordinate is from -10 to 10 and not 0 (neither point is an intercept); the
points differ in x and in y (no vertical or horizontal line).
    Step 5  integer points; the y-intercept a non-zero integer from -10 to 10,
            on the graph (easy scaffolding)
    Step 6  integer points; any y-intercept
    Step 7  each coordinate n/2 or n/4 in lowest terms (no thirds: halves and
            fourths read as decimals, 2.5 and 1.75), or an integer
            (written 3, never 3/1), shown as a mixed number past 1:
            "(4 1/2, -2 3/4)", read as 9/2 and -11/4; the slope's and the intercept's
            denominators are at most 12, and the intercept is from -10 to 10

Steps 8 to 10: Estimation Graphs. Two points, "(2.5, -7), (-4, 3.5)" (shown
"Sketch: (2.5, -7) and (-4, 3.5)"), and
bare axes, square, named x and y: no grid, no frame, no tick marks. The
student sketches: tick marks numbered at the middle and the end of each
axis, the two points, the line out to the edges, the rise-over-run triangle
between the points with its rise and run labeled, and the y-intercept marked
and estimated. The key draws all of it (answer_typst is empty: the graph is
the answer); the answer field holds y = m x + b, exact, for the check.
Each axis runs from -S to S, S one of 1, 10, 100, 1000, 10000, with ticks
at S/2 and S; a coordinate on that axis is a multiple of its grain:
    S       1     10    100   1000  10000
    grain   0.1   0.5   1     10    100
written as a decimal (2.5, -0.3, 4500). S is not stored: an axis's S is the
smallest that holds its two coordinates, so a drawn point always reaches
past S/10. Every coordinate is not 0, the points are at least S/5 apart on
each axis (a triangle big enough to label), and the y-intercept is on the graph.
    Step 8   integer points, S = 10 on both axes (ticks at 5 and 10)
    Step 9   the same S on both axes, any of the five
    Step 10  a different S on each axis

A problem: dict(type, form, prompt, answer, source), in Typst math.
    form    "A" to "F", as above (None in Steps 2, 4, 5, 6, 7)
    prompt  "x = 3/2 y + 6"; in Steps 2 and 4, "y = 2/3 x - 4"; in 5 to 7, "(1/2, -3), (4, 1 2/3)"
    answer  "y = 2/3 x - 4", "y = -1/2 x", "y = 5/3 x + 1", "y = 2 x - 7/2"
check() solves the prompt for y with sympy and compares it with the answer
read back from its text; the answer must be written y = m x + b (m a
fraction in lowest terms), and the line must keep the lesson's rules:
an integer intercept from -9 to 9 and another lattice point on the graph
(in Steps 5 to 7, the line through the prompt's points, which keep the step's rules).
In Steps 2 and 4 the prompt itself must be written y = m x + b. The key's graph is
drawn from the answer as check() reads it, so it shows the line checked.
"""
import math
import re
from decimal import Decimal
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need, written
from ..check import to_sympy
from ..graphs import Graph, PREAMBLE, INK
from ..typmath import display, dfrac, text as plain

NAME = FAMILY = "slope_intercept_2_1"
FIXED = False
TITLE = "Lesson 2-1: Slope-Intercept Form"
INSTRUCTIONS = ""              # each step has its own; a sheet of one step shows it at the top
COURSES = {"Algebra 1": "Lessons"}

TYPES = [
    dict(key="1", title="Solve for y", instructions="Solve each equation for y. Write it in the form y = mx + b.",
         look="A linear equation in x and y that isn't solved for y: 3y - 2x = -12, x = 3/2 y + 6, -6 = 3/2 y - x.",
         move="Get the y term alone on one side (add or subtract the x term and the number), then divide every term "
              "by y's coefficient (or multiply by its reciprocal). Write the x term first: y = 2/3 x - 4."),
    dict(key="2", title="Graph", instructions="Graph each line.",
         look="A line in slope-intercept form, y = m x + b, and a blank graph: y = 2/3 x - 4.",
         move="Plot the y-intercept (0, b). From it, rise the slope's numerator and run its denominator "
              "(a negative slope goes down as it goes right) to plot more points. Draw the line through them.",
         space="0in"),
    dict(key="3", title="Solve for y, Then Graph", instructions="Solve each equation for y, then graph it.",
         look="A linear equation that isn't solved for y, and a blank graph: 3y - 2x = -12.",
         move="Solve for y as in Step 1: y = 2/3 x - 4. Then graph it as in Step 2: plot (0, -4), "
              "rise 2 and run 3, and draw the line.",
         space="0in"),
    dict(key="4", title="Write the Equation", instructions="Write the equation of each line in the form y = mx + b.",
         look="A line drawn on a graph, and no equation.",
         move="Find where the line crosses the y-axis: that's b. From there, count the rise and the run to "
              "another point where the line crosses grid lines exactly: the slope m is rise over run "
              "(negative if the line goes down to the right). Write y = mx + b.",
         space="0in"),
    dict(key="5", title="Points to Equation, Integer b",
         instructions="Write the equation of the line through each pair of points in the form y = mx + b.",
         look="Two points, neither on an axis: (2, 3) and (5, 9). The y-intercept comes out a whole number.",
         move="Slope first: m = (y2 - y1)/(x2 - x1) = (9 - 3)/(5 - 2) = 2. Put m and one point into "
              "y = mx + b and solve for b: 3 = 2(2) + b, so b = -1. Write y = 2x - 1."),
    dict(key="6", title="Points to Equation, Any b",
         instructions="Write the equation of the line through each pair of points in the form y = mx + b.",
         look="Two points, neither on an axis: (1, 4) and (3, 5). The y-intercept may be a fraction.",
         move="Slope first: m = (5 - 4)/(3 - 1) = 1/2. Put m and one point into y = mx + b and solve "
              "for b: 4 = 1/2 (1) + b, so b = 7/2. Write y = 1/2 x + 7/2."),
    dict(key="7", title="Fractional Coordinates",
         instructions="Write the equation of the line through each pair of points in the form y = mx + b.",
         look="Two points with fractions or mixed numbers for coordinates: (1/2, 3) and (2 1/2, -1).",
         move="Slope first; write a mixed number as a fraction (2 1/2 = 5/2) and subtract with a common "
              "denominator: m = (-1 - 3)/(5/2 - 1/2) = -4/2 = -2. Put m and one point into y = mx + b and solve for b: 3 = -2(1/2) + b, so b = 4. "
              "Write y = -2x + 4."),
    dict(key="8", title="Estimation Graphs 1",
         instructions="Sketch the line through each pair of points. Mark and number the axes at -10, -5, 5, and 10; "
                      "plot the points and draw the line to the edges. Draw the rise and run between the points and "
                      "label them, then mark the y-intercept and estimate it.",
         look="Two points, (2, 4) and (-4, -5), and bare axes.",
         move="Number the axes at -10, -5, 5, 10. Plot the points by eye; draw the line to the edges. "
              "Draw the run and rise between them and label them: run 6, rise 9. Mark the y-intercept: about 1.",
         space="0in"),
    dict(key="9", title="Estimation Graphs 2",
         instructions="Sketch the line through each pair of points. Choose a scale that fits both points, mark and "
                      "number each axis at its middle and its end; plot the points and draw the line to the edges. "
                      "Draw the rise and run between the points and label them, then mark the y-intercept and estimate it.",
         look="Two points, all coordinates the same size: (450, -200) and (-700, 900).",
         move="The scale is the smallest of 1, 10, 100, 1000, 10000 that holds them: 1000. Number both axes "
              "at -1000, -500, 500, 1000, then sketch as in Estimation Graphs 1.",
         space="0in"),
    dict(key="10", title="Estimation Graphs 3",
         instructions="Sketch the line through each pair of points. Choose a scale for each axis that fits its "
                      "coordinates, mark and number each axis at its middle and its end; plot the points and draw "
                      "the line to the edges. Draw the rise and run between the points and label them, then mark "
                      "the y-intercept and estimate it.",
         look="Two points whose x's and y's are different sizes: (0.4, 650) and (-0.9, -300).",
         move="Scale each axis on its own: x to 1, y to 1000. Then sketch as in Estimation Graphs 1; "
              "the run and rise are in each axis's units: run 1.3, rise 950.",
         space="0in"),
]

class Steps(gen.Types):
    def label(self, t):
        return "Step " + t["key"]

T = Steps(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

WINDOW = 10                    # the graph: -10 to 10 on both axes
INTERCEPT = 9                  # the y-intercept: -9 to 9
FORMS = "ABCDEF"
GIVEN = ("2", "4")             # the steps whose prompt is already y = m x + b
POINTS = ("5", "6", "7")       # the steps whose prompt is two points
DENOMINATORS = {"5": (1,), "6": (1,), "7": (1, 2, 4)}   # a coordinate's denominator, in lowest terms
KEY_DENOMINATOR = 12           # Step 7: the slope's and the intercept's denominators at most this
ESTIMATE = ("8", "9", "10")    # the estimation graphs: two points and bare axes
TWO_POINTS = POINTS + ESTIMATE
GRAIN = {1: F(1, 10), 10: F(1, 2), 100: F(1), 1000: F(10), 10000: F(100)}   # an axis's S: its coordinates' multiple

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p.get("form"), p["type"])   # the form and step, for spreading each step's forms

# ------------------------------------------------------------------
# The line
# ------------------------------------------------------------------
def lattice_points(m, b, window=WINDOW):
    """The integer points (x, y) of y = m x + b with |x|, |y| <= window."""
    return [(x, m * x + b) for x in range(-window, window + 1)
            if (m * x + b).denominator == 1 and abs(m * x + b) <= window]

def fits(m, b):
    """The lesson's rules: m not 0, b an integer from -9 to 9,
    and a lattice point on the graph besides (0, b)."""
    return (m != 0 and b.denominator == 1 and abs(b) <= INTERCEPT
            and any(x != 0 for x, _ in lattice_points(m, b)))

def line(r):
    """(a, c, b): slope a/c in lowest terms, c 1 to 6, |a| 1 to 9 (1 to 5 for a whole number); intercept b."""
    c, a, b = r.randint(1, 6), gen.signed(r, 1, 9), r.randint(-INTERCEPT, INTERCEPT)
    need(math.gcd(a, c) == 1 and (c > 1 or abs(a) <= 5) and fits(F(a, c), F(b)))
    return a, c, b

# ------------------------------------------------------------------
# Step 1: the six starting forms
# ------------------------------------------------------------------
def form_a(a, c, b):                       # c y = a x + c b
    return f"{written((c, 'y'))} = {written((a, 'x'), (c * b, ''))}"

def form_b(a, c, b):                       # c y - a x = c b
    return f"{written((c, 'y'), (-a, 'x'))} = {c * b}"

def form_c(a, c, b):                       # a x = c y - c b
    return f"{written((a, 'x'))} = {written((c, 'y'), (-c * b, ''))}"

def form_d(a, c, b):                       # x = (c/a) y - c b/a
    return f"x = {written((F(c, a), 'y'), (-F(c * b, a), ''))}"

def form_e(a, c, b):                       # (c/a) y = x + c b/a
    return f"{written((F(c, a), 'y'))} = {written((1, 'x'), (F(c * b, a), ''))}"

def form_f(a, c, b):                       # c b/a = (c/a) y - x
    return f"{written((F(c * b, a), ''))} = {written((F(c, a), 'y'), (-1, 'x'))}"

FORM = dict(zip(FORMS, (form_a, form_b, form_c, form_d, form_e, form_f)))

def slope_intercept(m, b):
    """y = m x + b as the key writes it: "y = 2/3 x - 4", "y = -1/2 x"."""
    return f"y = {written((m, 'x'), (b, ''))}"

# ------------------------------------------------------------------
# Steps 5 to 7: two points
# ------------------------------------------------------------------
def through(pts):
    """(m, b), Fractions, of the line through two points with different x."""
    (x1, y1), (x2, y2) = pts
    m = (y2 - y1) / (x2 - x1)
    return m, y1 - m * x1

def points_keep_rules(entry, pts):
    """The step's rules for its two points (Fractions): see the docstring."""
    if entry in ESTIMATE:
        return estimate_keeps_rules(entry, pts)
    if len(pts) != 2 or pts[0][0] == pts[1][0] or pts[0][1] == pts[1][1]:
        return False
    for x, y in pts:
        for v in (x, y):
            if v == 0 or abs(v) > WINDOW or v.denominator not in DENOMINATORS[entry]:
                return False
    m, b = through(pts)
    if entry == "5":
        return b.denominator == 1 and b != 0 and abs(b) <= WINDOW   # the intercept on the graph
    if entry == "7":
        return m.denominator <= KEY_DENOMINATOR and b.denominator <= KEY_DENOMINATOR and abs(b) <= WINDOW
    return True

def scales(entry, pts):
    """(Sx, Sy), each axis's S in Steps 8 to 10: 10 in Step 8, else the smallest that holds
    the axis's coordinates; None past 10000."""
    if entry == "8":
        return 10, 10
    def s(vs):
        return next((k for k in GRAIN if max(abs(v) for v in vs) <= k), None)
    return s([x for x, _ in pts]), s([y for _, y in pts])

def estimate_keeps_rules(entry, pts):
    """Steps 8 to 10: see the docstring."""
    if len(pts) != 2:
        return False
    sx, sy = scales(entry, pts)
    if sx is None or sy is None or (entry == "9" and sx != sy) or (entry == "10" and sx == sy):
        return False
    for i, (s, grain) in enumerate(((sx, F(1) if entry == "8" else GRAIN[sx]), (sy, F(1) if entry == "8" else GRAIN[sy]))):
        vs = [p[i] for p in pts]
        if any(v == 0 or abs(v) > s or v % grain for v in vs) or abs(vs[0] - vs[1]) < F(s, 5):
            return False
    _, b = through(pts)
    return abs(b) <= sy

def draw_estimate(entry, r):
    if entry == "8":
        sx = sy = 10
    elif entry == "9":
        sx = sy = r.choice(list(GRAIN))
    else:
        sx, sy = r.sample(list(GRAIN), 2)
    def coord(s):
        grain = F(1) if entry == "8" else GRAIN[s]
        n = int(s / grain)
        return r.randint(-n, n) * grain
    pts = [(coord(sx), coord(sy)) for _ in range(2)]
    need(estimate_keeps_rules(entry, pts) and scales(entry, pts) == (sx, sy))
    m, b = through(pts)
    return dict(form=None, prompt=point_prompt(pts, entry), answer=slope_intercept(m, b))

def decimal(v):
    """A coordinate in Steps 8 to 10, exactly, as a decimal: 2.5, -0.3, 4500, 7."""
    s = format((Decimal(v.numerator) / Decimal(v.denominator)).normalize(), "f")
    return "0" if s == "-0" else s

def coordinate(entry, r):
    d = r.choice(DENOMINATORS[entry])
    return F(r.randint(-WINDOW * d, WINDOW * d), d)  # in lowest terms: 4/2 is 2

def mixed(v):
    """A coordinate as a student reads it on a graph: 3, 1/2, -3/4, 4 1/3, -2 3/4."""
    if v.denominator == 1 or abs(v) < 1:
        return str(v)
    whole, part = divmod(abs(v), 1)
    return f"{'-' if v < 0 else ''}{whole} {part}"

def point_prompt(pts, entry=None):
    """"(1/2, -3), (4, 1 3/4)": each coordinate in lowest terms, an integer as an integer,
    a mixed number past 1; in Steps 8 to 10, decimals: "(2.5, -7), (-4, 3.5)"."""
    shown = decimal if entry in ESTIMATE else mixed
    return ", ".join(f"({shown(x)}, {shown(y)})" for x, y in pts)

NUMBER = r"-?\d+ \d+/\d+|-?\d+\.\d+|-?\d+/\d+|-?\d+"   # 4 1/3, 2.5, 13/3, 4
POINT = re.compile(rf"\(\s*({NUMBER})\s*,\s*({NUMBER})\s*\)")

def number(s):
    """A coordinate's value: "4 1/3" is 13/3, "-4 1/3" is -13/3; a fraction in lowest
    terms (a mixed number's part proper too); ValueError otherwise."""
    if "." in s:
        return F(s)
    whole, _, part = s.rpartition(" ")
    if str(F(part)) != part:
        raise ValueError("write each coordinate in lowest terms")
    if not whole:
        return F(part)
    if not 0 < F(part) < 1:
        raise ValueError("a mixed number's fraction is less than 1")
    w = int(whole)
    return w - F(part) if whole.startswith("-") else w + F(part)

def points_of(prompt):
    """The two points, as Fractions, of a prompt "(1/2, -3), (4, 1 3/4)"; ValueError if it isn't
    two points, each coordinate written in lowest terms."""
    t = " ".join(prompt.replace("−", "-").split())
    pts = POINT.findall(t)
    if len(pts) != 2 or POINT.sub("", t).replace(",", "").replace("and", "").strip():
        raise ValueError("write two points, like (1/2, -3), (4, 1 3/4)")
    out = []
    for xs, ys in pts:
        out.append((number(xs), number(ys)))
    return out

def draw_points(entry, r):
    if entry in ESTIMATE:
        return draw_estimate(entry, r)
    pts = [(coordinate(entry, r), coordinate(entry, r)) for _ in range(2)]
    need(points_keep_rules(entry, pts))
    m, b = through(pts)
    return dict(form=None, prompt=point_prompt(pts), answer=slope_intercept(m, b))

def draw(entry, r, tpl, want=None):
    if entry in TWO_POINTS:
        return draw_points(entry, r)
    a, c, b = line(r)
    answer = slope_intercept(F(a, c), F(b))
    if entry in GIVEN:
        return dict(form=None, prompt=answer, answer=answer)
    form = want or r.choice(FORMS)
    prompt = FORM[form](a, c, b)
    need(written_form(prompt) is None)             # not already solved for y: 1 y = 3 x + 2
    return dict(form=form, prompt=prompt, answer=answer)

def _step(entry):
    """A step's own generator: its forms are spread over the sheet's problems of that step only."""
    return gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: 1,
                         balance=(FORMS, lambda k: k[2] if k[0] == NAME and len(k) == 4 and k[3] == entry else None))
STEP_GENERATE = {k: _step(k) for k in KEYS}

def generate(entry, rng, seen):
    return STEP_GENERATE[entry](entry, rng, seen)

# ------------------------------------------------------------------
# Checking: solve the prompt for y, read the answer back
# ------------------------------------------------------------------
X, Y = sp.Symbol("x"), sp.Symbol("y")
ANSWER = re.compile(r"y = (?P<m>-?(\d+/\d+ |\d+ )?)x( (?P<sign>[+-]) (?P<b>\d+(/\d+)?))?")

def solved(prompt):
    """(m, b), Fractions, for a prompt that is a line in x and y with a slope; ValueError otherwise."""
    lhs, _, rhs = prompt.partition("=")
    if not rhs:
        raise ValueError("an equation needs an =")
    e = sp.nsimplify(to_sympy(lhs) - to_sympy(rhs), rational=True)
    if not e.free_symbols <= {X, Y}:
        raise ValueError("use only x and y")
    sol = sp.solve(e, Y)
    if len(sol) != 1:
        raise ValueError("the equation can't be solved for y")
    p = sp.Poly(sol[0], X)
    if p.degree() > 1 or not all(k.is_Rational for k in p.all_coeffs()):
        raise ValueError("the equation isn't a line with a number slope")
    m, b = (p.all_coeffs() if p.degree() == 1 else [0, p.all_coeffs()[0]])
    return F(int(sp.Rational(m).p), int(sp.Rational(m).q)), F(int(sp.Rational(b).p), int(sp.Rational(b).q))

def written_form(answer):
    """(m, b) read from an answer written y = m x + b, m in lowest terms; None if it isn't."""
    g = ANSWER.fullmatch(" ".join(answer.split()))
    if not g:
        return None
    t = g["m"].strip()
    m = F(-1 if t == "-" else 1) if t in ("", "-") else F(t)
    if "/" in t and (m.denominator != int(t.split("/")[1]) or m.denominator == 1):
        return None                                  # not in lowest terms
    if t in ("1", "-1"):
        return None                                  # x, not 1 x
    if g["b"] is not None and (g["b"] == "0" or str(F(g["b"])) != g["b"]):
        return None                                  # b in lowest terms, not 0 or 4/2
    b = F(0) if g["b"] is None else F(g["b"]) * (-1 if g["sign"] == "-" else 1)
    return m, b

def check(p):
    try:
        got = written_form(p["answer"])
        if got is None:
            return "failed"
        m, b = got
        if sp.simplify(to_sympy(p["answer"].partition("=")[2]) - (sp.Rational(m.numerator, m.denominator) * X + b)) != 0:
            return "failed"                          # the text says what it was read as
        if p.get("type") in TWO_POINTS:
            pts = points_of(p["prompt"])
            return "checked" if points_keep_rules(p["type"], pts) and through(pts) == (m, b) else "failed"
        if (m, b) != solved(p["prompt"]):
            return "failed"
        if p.get("type") in GIVEN and written_form(p["prompt"]) != (m, b):
            return "failed"                          # Steps 2 and 4 start in slope-intercept form
        return "checked" if fits(m, b) else "failed"
    except Exception:
        return "unchecked"

def answer_of(prompt, step=None):
    if step in TWO_POINTS:
        pts = points_of(prompt)
        if pts[0][0] == pts[1][0]:
            raise ValueError("a vertical line")
        m, b = through(pts)
    else:
        m, b = solved(prompt)
    if m == 0:
        raise ValueError("a horizontal line")
    return slope_intercept(m, b)

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
GRAPHED = ("2", "3", "4") + ESTIMATE    # the steps with a graph
DRAWN = ("4",)                          # the steps whose graph shows the line, with no equation
SHEET_WIDTH = 4.9                       # the graph on the sheet, in cm
SHEET_GAP = "0.3em"                     # between a graph and the equation over it
SLIDE_WIDTH = 8.0                       # the graph on a slide, in cm
SLIDE_NUMBERS = 14                      # its axis numbers, in pt (6 on the sheet), every 2

def graph(p, key=False, width=SHEET_WIDTH, size=6, every=None):
    """The -10 to 10 graph: blank, or on the key, the answer's line through its lattice points;
    in Step 4, the prompt's line, the same on the sheet and the key."""
    if p["type"] in ESTIMATE:
        return estimate_graph(p, key, width, size)
    g = Graph(x=(-WINDOW, WINDOW), y=(-WINDOW, WINDOW), width=width, size=size, label=every)
    edge = WINDOW + 1.5            # a fixed frame, so a line's arrow past the grid never moves the graph
    g.cmds.append(f"rect({g.c(-edge, -edge)}, {g.c(edge, edge)}, stroke: none)")
    if p["type"] in DRAWN:
        try:
            m, b = solved(p["prompt"])
            g.line(float(m), float(b), color="blue")
        except Exception:
            pass                   # an edited prompt that isn't a line: a blank graph, and check() marks it
    elif key:
        m, b = written_form(p["answer"])
        g.line(float(m), float(b), color="red")
        for x, y in lattice_points(m, b):
            g.point(x, float(y), color="red")
    return g.typst()

PT = 2.54 / 72                          # a point, in cm

def _label_box(cx, cy, words, anchor, size, pad):
    """The cm box (x0, y0, x1, y1) a label takes, generously: an anchor point, its text at size pt,
    and pad pt around it. A character is taken as 0.62 em, wider than any of these really are."""
    w = len(words) * 0.62 * size * PT + 2 * pad * PT
    h = 1.3 * size * PT + 2 * pad * PT
    x0 = {"north": cx - w / 2, "south": cx - w / 2, "east": cx - w}.get(anchor, cx)        # west: from cx
    y0 = {"north": cy - h, "north-west": cy - h, "east": cy - h / 2, "west": cy - h / 2}.get(anchor, cy)
    return x0, y0, x0 + w, y0 + h

def estimate_graph(p, key=False, width=SHEET_WIDTH, size=6):
    """Steps 8 to 10: bare square axes, named x and y; on the key, the sketch: ticks numbered at
    S/2 and S, the points, the line to the edges, the rise-over-run triangle labeled, and the
    y-intercept marked with its estimate.
    The question and the key draw the same invisible frame, big enough for every label the key
    writes, so the graph is the same size in both and never moves when the answer shows (a slide's
    graph sits beside the question, and a wider one would rewrap it)."""
    try:
        pts = sorted(points_of(p["prompt"]))
        sx, sy = scales(p["type"], pts)
        sx, sy = sx or 10, sy or 10
    except ValueError:
        pts, sx, sy = None, 10, 10
    if pts and pts[0][0] == pts[1][0]:
        pts = None                                   # a vertical line, edited in: a blank graph, and check() marks it
    g = Graph(x=(-sx, sx), y=(-sy, sy), width=width, height=width, grid=False, numbers=False, size=size)
    cm = lambda x, y: (float(x) * g.kx, float(y) * g.ky)            # the origin is the middle
    minus = lambda v: decimal(F(v)).replace("-", "−")
    tx, ty = 0.09 / g.kx, 0.09 / g.ky               # half a tick, in each axis's units
    labels = []                                      # (x, y, words, anchor, size, pad, box: the white patch's color)
    if pts:
        for v in (-sx, F(-sx, 2), F(sx, 2), sx):
            labels.append((v, -ty, minus(v), "north", size, 1.5, None))
        for v in (-sy, F(-sy, 2), F(sy, 2), sy):
            labels.append((-tx, v, minus(v), "east", size, 1.5, None))
        (x1, y1), (x2, y2) = pts
        m, b = through(pts)
        labels += [((x1 + x2) / 2, y1, f"run {minus(x2 - x1)}", "north" if y2 > y1 else "south", size + 1, 3, "green"),
                   (x2, (y1 + y2) / 2, f"rise {minus(y2 - y1)}", "west", size + 1, 3, "green"),
                   (0, b, "b " + display_b(p).replace("-", "−"), "north-west" if m > 0 else "south-west", size + 1, 3, "purple")]
    half = 1.15 * width / 2                          # the axes, their arrows, and a little room
    x0, y0, x1_, y1_ = -half, -half, half, half
    for x, y, words, anchor, sz, pad, _ in labels:
        a, b_, c, d = _label_box(*cm(x, y), words, anchor, sz, pad)
        x0, y0, x1_, y1_ = min(x0, a), min(y0, b_), max(x1_, c), max(y1_, d)
    g.cmds.append(f"rect({g.c(x0 / g.kx, y0 / g.ky)}, {g.c(x1_ / g.kx, y1_ / g.ky)}, stroke: none)")
    if not key or not pts:
        return g.typst()
    for v in (-sx, F(-sx, 2), F(sx, 2), sx):
        g.cmds.append(f"line({g.c(v, -ty)}, {g.c(v, ty)}, stroke: 0.7pt)")
    for v in (-sy, F(-sy, 2), F(sy, 2), sy):
        g.cmds.append(f"line({g.c(-tx, v)}, {g.c(tx, v)}, stroke: 0.7pt)")
    (x1, y1), (x2, y2) = pts
    g.through((float(x1), float(y1)), (float(x2), float(y2)), color="red")
    g.polyline([(x1, y1), (x2, y1), (x2, y2)], color="green", width=1, dash="dashed", ends=None)
    for x, y in pts:
        g.point(float(x), float(y), color="red")
    g.point(0, float(through(pts)[1]), color="purple")
    for x, y, words, anchor, sz, pad, color in labels:
        if color is None:                            # a tick's number
            g.cmds.append(f"content({g.c(x, y)}, anchor: \"{anchor}\", padding: {pad}pt, text(size: {sz}pt)[{words}])")
        else:                                        # on a white patch, so it reads over a line or a tick
            g.cmds.append(f"content({g.c(x, y)}, anchor: \"{anchor}\", padding: 2pt, box(fill: white, inset: 1pt, "
                          f"text(size: {sz}pt, fill: {INK[color]})[{words}]))")
    return g.typst()

ASKED = "Graph: "                       # before the equation in Steps 2 and 3, so the problem says what to do
SKETCH = "Sketch: "                     # Steps 8 to 10

def asked(p):
    """What a graphed problem says beside its graph (Step 4's says nothing: the graph is all of it)."""
    if p["type"] in ESTIMATE:
        try:
            a, b = (display(f"({decimal(x)}, {decimal(y)})") for x, y in points_of(p["prompt"]))
        except ValueError:
            return SKETCH + display(p["prompt"])
        return f"{SKETCH}{a} and {b}"
    return "" if p["type"] in DRAWN else ASKED + display(dfrac(p["prompt"]))

def through_typst(p):
    """Steps 5 to 7: "Through (2, 3) and (5, 9)", each point in display math."""
    try:
        pts = points_of(p["prompt"])
    except ValueError:
        return display(dfrac(p["prompt"]))
    a, b = (display(dfrac(f"({mixed(x)}, {mixed(y)})")) for x, y in pts)
    return f"Through {a} and {b}"

def typst(p, gap="0.3em", key=False):
    if p["type"] in POINTS:
        return through_typst(p)
    eq = display(dfrac(p["prompt"]))
    if p["type"] not in GRAPHED:
        return eq
    if p["type"] in DRAWN:
        return f"#align(center)[{graph(p)}]"
    return f"{asked(p)} #v({SHEET_GAP}) #align(center)[{graph(p, key)}]"

def key_typst(p, gap="0.3em"):
    """The key's prompt: the line drawn on the graph."""
    return typst(p, gap, key=p["type"] in GRAPHED and written_form(p["answer"]) is not None)

def slide_parts(p, key=False):
    """A graphed problem's slide in two parts, (text, graph): the equation with the
    key's answer under it, and the larger graph; None for a step without a graph.
    The question's text holds the answer too, hidden, so the two slides lay out
    alike: the graph never moves when the answer shows."""
    if p["type"] not in GRAPHED:
        return None
    drawn = key and written_form(p["answer"]) is not None
    left = asked(p)
    if answer_typst(p):
        ans = f"#text(fill: red)[{answer_typst(p)}]"
        left += f" #v(0.8em) " if left else ""
        left += ans if key else f"#hide[{ans}]"
    return left, graph(p, drawn, width=SLIDE_WIDTH, size=SLIDE_NUMBERS, every=2)

def slide_typst(p, key=False):
    """On a slide, the graph sits beside the equation (slide_parts); None for a
    step without a graph, which shows as usual. The board presenter stacks them."""
    parts = slide_parts(p, key)
    if parts is None:
        return None
    left, g = parts
    return f"#grid(columns: 2, column-gutter: 1.5em, align: horizon, [{left}], [{g}])"

def answer_typst(p):
    """The answer of Step 2 and Steps 8 to 10 is the graph alone (key_typst); the others give y = m x + b."""
    return "" if p["type"] in ("2",) + ESTIMATE else display(dfrac(p["answer"]))

def text(p):
    if p["type"] in ESTIMATE:
        try:
            shown = point_prompt(points_of(p["prompt"]), p["type"])
        except ValueError:
            shown = p["prompt"]
        return SKETCH + plain(shown).replace("), (", ") and (") + "   [axes]"
    if p["type"] in POINTS:
        try:
            shown = point_prompt(points_of(p["prompt"]))
        except ValueError:
            shown = p["prompt"]
        return "Through " + plain(shown).replace("), (", ") and (")
    if p["type"] in DRAWN:
        return f"[graph of {plain(p['prompt'])}]"
    if p["type"] in GRAPHED:
        return ASKED + plain(p["prompt"]) + "   [graph]"
    return plain(p["prompt"])

def answer_text(p):
    got = written_form(p["answer"])
    if p["type"] in ESTIMATE and got is not None:
        try:
            (x1, y1), (x2, y2) = sorted(points_of(p["prompt"]))
            minus = lambda v: plain(decimal(v))
            return (f"run {minus(x2 - x1)}, rise {minus(y2 - y1)}; y-intercept {plain(display_b(p))}"
                    f"   ({plain(p['answer'])})")
        except ValueError:
            pass
    if p["type"] not in GRAPHED or p["type"] in DRAWN or got is None:
        return plain(p["answer"])
    m, b = got
    pts = ", ".join(f"({x}, {y})" for x, y in lattice_points(m, b))
    return plain(p["answer"]) + "   graphed through " + pts

def display_b(p):
    """The key's y-intercept, to a hundredth of the y-axis: "= 4", "≈ 2.33"."""
    pts = points_of(p["prompt"])
    _, sy = scales(p["type"], pts)
    _, b = through(pts)
    q = F(sy or 10, 100)
    near = round(b / q) * q
    return f"{'=' if near == b else '≈'} {decimal(near)}"

def height(p):
    return 2.6 if p["type"] in GRAPHED else (0.55 if "/" in p["prompt"] else 0.3)
def _equation(t, example):
    """t cleaned, if it is an equation whose sides read as Typst math; ValueError otherwise."""
    t = " ".join(t.replace("−", "-").split())
    lhs, eq, rhs = t.partition("=")
    try:
        if not eq:
            raise ValueError
        to_sympy(lhs), to_sympy(rhs)
    except Exception:
        raise ValueError(f"write it in Typst math, like {example}") from None
    return t

def edit_text(p):
    return p["prompt"]

def answer_edit_text(p):
    return p["answer"]

def from_edit(t, old):
    """An edited prompt, solved for y again (a prompt that isn't a line keeps the old answer, which check() marks);
    in Steps 5 to 7, two points, and the line through them."""
    step = old.get("type")
    if step in TWO_POINTS:
        t = point_prompt(points_of(t), step)
    else:
        t = _equation(t, "x = 3/2 y + 6")
    try:
        answer = answer_of(t, step)
    except (ValueError, gen.Redraw):
        answer = old["answer"]
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def with_answer(p, t):
    new = dict(p, answer=_equation(t, "y = 2/3 x - 4"))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
