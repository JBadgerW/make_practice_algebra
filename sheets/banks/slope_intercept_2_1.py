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
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need, written
from ..check import to_sympy
from ..graphs import Graph, PREAMBLE
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
         space="0.25in"),
    dict(key="3", title="Solve for y, Then Graph", instructions="Solve each equation for y, then graph it.",
         look="A linear equation that isn't solved for y, and a blank graph: 3y - 2x = -12.",
         move="Solve for y as in Step 1: y = 2/3 x - 4. Then graph it as in Step 2: plot (0, -4), "
              "rise 2 and run 3, and draw the line.",
         space="0.25in"),
    dict(key="4", title="Write the Equation", instructions="Write the equation of each line in the form y = mx + b.",
         look="A line drawn on a graph, and no equation.",
         move="Find where the line crosses the y-axis: that's b. From there, count the rise and the run to "
              "another point where the line crosses grid lines exactly: the slope m is rise over run "
              "(negative if the line goes down to the right). Write y = mx + b.",
         space="0.25in"),
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

def coordinate(entry, r):
    d = r.choice(DENOMINATORS[entry])
    return F(r.randint(-WINDOW * d, WINDOW * d), d)  # in lowest terms: 4/2 is 2

def mixed(v):
    """A coordinate as a student reads it on a graph: 3, 1/2, -3/4, 4 1/3, -2 3/4."""
    if v.denominator == 1 or abs(v) < 1:
        return str(v)
    whole, part = divmod(abs(v), 1)
    return f"{'-' if v < 0 else ''}{whole} {part}"

def point_prompt(pts):
    """"(1/2, -3), (4, 1 3/4)": each coordinate in lowest terms, an integer as an integer,
    a mixed number past 1."""
    return ", ".join(f"({mixed(x)}, {mixed(y)})" for x, y in pts)

NUMBER = r"-?\d+ \d+/\d+|-?\d+/\d+|-?\d+"   # 4 1/3, 13/3, 4
POINT = re.compile(rf"\(\s*({NUMBER})\s*,\s*({NUMBER})\s*\)")

def number(s):
    """A coordinate's value: "4 1/3" is 13/3, "-4 1/3" is -13/3; a fraction in lowest
    terms (a mixed number's part proper too); ValueError otherwise."""
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
    pts = [(coordinate(entry, r), coordinate(entry, r)) for _ in range(2)]
    need(points_keep_rules(entry, pts))
    m, b = through(pts)
    return dict(form=None, prompt=point_prompt(pts), answer=slope_intercept(m, b))

def draw(entry, r, tpl, want=None):
    if entry in POINTS:
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
        if p.get("type") in POINTS:
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
    if step in POINTS:
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
GRAPHED = ("2", "3", "4")               # the steps with a graph
DRAWN = ("4",)                          # the steps whose graph shows the line, with no equation
SLIDE_WIDTH = 8.0                       # the graph on a slide, in cm (5.5 on the sheet)
SLIDE_NUMBERS = 14                      # its axis numbers, in pt (6 on the sheet), every 2

def graph(p, key=False, width=5.5, size=6, every=None):
    """The -10 to 10 graph: blank, or on the key, the answer's line through its lattice points;
    in Step 4, the prompt's line, the same on the sheet and the key."""
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

ASKED = "Graph: "                       # before the equation in Steps 2 and 3, so the problem says what to do

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
    return f"{ASKED}{eq} #v(0.6em) #align(center)[{graph(p, key)}]"

def key_typst(p, gap="0.3em"):
    """The key's prompt: the line drawn on the graph."""
    return typst(p, gap, key=p["type"] in GRAPHED and written_form(p["answer"]) is not None)

def slide_typst(p, key=False):
    """On a slide, the graph is larger and sits beside the equation (with the key's
    answer under it); None for a step without a graph, which shows as usual.
    The question's slide holds the answer too, hidden, so the two slides lay out
    alike: the graph never moves when the answer shows."""
    if p["type"] not in GRAPHED:
        return None
    drawn = key and written_form(p["answer"]) is not None
    left = "" if p["type"] in DRAWN else ASKED + display(dfrac(p["prompt"]))
    if answer_typst(p):
        ans = f"#text(fill: red)[{answer_typst(p)}]"
        left += f" #v(0.8em) " if left else ""
        left += ans if key else f"#hide[{ans}]"
    return (f"#grid(columns: 2, column-gutter: 1.5em, align: horizon, [{left}], "
            f"[{graph(p, drawn, width=SLIDE_WIDTH, size=SLIDE_NUMBERS, every=2)}])")

def answer_typst(p):
    """Step 2's answer is the graph alone (key_typst); the others give y = m x + b."""
    return "" if p["type"] == "2" else display(dfrac(p["answer"]))

def text(p):
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
    if p["type"] not in GRAPHED or p["type"] in DRAWN or got is None:
        return plain(p["answer"])
    m, b = got
    pts = ", ".join(f"({x}, {y})" for x, y in lattice_points(m, b))
    return plain(p["answer"]) + "   graphed through " + pts

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
    if step in POINTS:
        t = point_prompt(points_of(t))
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
