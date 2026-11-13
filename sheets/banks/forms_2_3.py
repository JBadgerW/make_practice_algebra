"""Lesson 2-3: Forms of Linear Equations. A line is given in one form; write it in another.
Four types, one for each target form:

    1  To slope-intercept form   2 x - 3 y = 12            y = 2/3 x - 4
    2  To standard form          y + 3 = 2/3 (x - 4)       2 x - 3 y = 17
    3  To general form           x/6 - y/4 = 1             2 x - 3 y - 12 = 0
    4  To intercept form         y = 2/3 x - 4             x/6 - y/4 = 1

The five forms, as the key writes them:
    si   slope-intercept   y = m x + b                    y = 2/3 x - 17/3, y = -x + 4
    ps   point-slope       y - y1 = m (x - x1)            y + 3 = 2/3 (x - 4)  (as Lesson 2-2)
    std  standard          A x + B y = C                  2 x - 3 y = 17
    gen  general           A x + B y + C = 0              2 x - 3 y - 17 = 0
    int  intercept         x/a + y/b = 1                  x/6 - y/4 = 1, -x/2 + y/5 = 1
In standard and general form, A, B, and C are integers with no common factor, and A > 0;
a coefficient of 1 is left off. In intercept form, a and b are the x- and y-intercepts,
whole numbers, written with their signs in front of the fractions (x/1 keeps its 1).
Point-slope form is a starting form only: it has too many right answers to be a target.

A type's starting form is any of the other four (point-slope among them); a sheet's
problems of one type are spread evenly over its four starting forms (gen.generator's balance).

The lines: every line has a slope that isn't 0 and doesn't go through the origin (so no
horizontal, vertical, or origin lines, and all five forms exist).
    - A problem that shows or asks for intercept form (Type 4, or an intercept-form prompt)
      has whole-number intercepts, -10 to 10, not 0. Its point-slope prompt goes through a
      lattice point with both coordinates non-zero and from -10 to 10.
    - Any other: Lesson 2-2's slope (a whole number 1 to 6, or a fraction in lowest terms,
      denominator 2 to 5, numerator up to 7; either sign) through a point whose coordinates
      are -9 to 9, not 0; the y-intercept, often a fraction, is at most 20 either way.

A problem: dict(type, form, prompt, answer, source), in Typst math; form is the prompt's form.
check() reads the prompt in its form and the answer in the type's form, strictly as the key
writes them, and confirms each text says what it was read as by solving it for y with sympy.
"""
import math
import re
from fractions import Fraction as F
from .. import gen
from ..gen import need, written
from . import slope_intercept_2_1 as si
from . import point_slope_2_2 as ps

NAME = FAMILY = "forms_2_3"
FIXED = False
TITLE = "Lesson 2-3: Forms of Linear Equations"
INSTRUCTIONS = ""              # each type has its own; a sheet of one type shows it at the top
COURSES = {"Algebra 1": "Lessons"}

TYPES = [
    dict(key="1", title="To Slope-Intercept Form", instructions="Write each equation in slope-intercept form.",
         look="A line in another form, like 2 x - 3 y = 12, and slope-intercept form, y = m x + b, asked for.",
         move="Get y alone. Move the x term to the other side (-3 y = -2 x + 12), then divide every "
              "term by y's coefficient: y = 2/3 x - 4."),
    dict(key="2", title="To Standard Form", instructions="Write each equation in standard form.",
         look="A line in another form, like y + 3 = 2/3 (x - 4), and standard form, A x + B y = C, asked for.",
         move="Clear fractions by multiplying both sides by the denominator: 3 y + 9 = 2 (x - 4). "
              "Put x and y on the left and the number on the right: -2 x + 3 y = -17. "
              "Make A positive (multiply by -1) and divide out any common factor: 2 x - 3 y = 17."),
    dict(key="3", title="To General Form", instructions="Write each equation in general form.",
         look="A line in another form, like x/6 - y/4 = 1, and general form, A x + B y + C = 0, asked for.",
         move="Clear fractions (multiply by 12: 2 x - 3 y = 12), then move everything to the left so "
              "the right side is 0: 2 x - 3 y - 12 = 0. A is positive, with no common factor."),
    dict(key="4", title="To Intercept Form", instructions="Write each equation in intercept form.",
         look="A line in another form, like y = 2/3 x - 4, and intercept form, x/a + y/b = 1, asked for.",
         move="Find the intercepts: y = 0 gives x = 6, and x = 0 gives y = -4. Then write "
              "x/6 + y/(-4) = 1, with the sign out front: x/6 - y/4 = 1. Or: get the number alone "
              "on the right, 2 x - 3 y = 12, and divide every term by it."),
]

T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

FORMS = ("si", "ps", "std", "gen", "int")
FORM_NAME = dict(si="slope-intercept", ps="point-slope", std="standard", gen="general", int="intercept")
TARGET = {"1": "si", "2": "std", "3": "gen", "4": "int"}
SOURCES = {k: tuple(f for f in FORMS if f != t) for k, t in TARGET.items()}
INTERCEPTS = 10                # intercept form: each intercept -10 to 10, not 0
LATTICE = 10                   # its point-slope prompt's point: -10 to 10, not 0
POINT = 9                      # any other line: its point -9 to 9, not 0
Y_INTERCEPT = 20               # any other line: the y-intercept at most this

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p.get("form"), p["type"])   # the form and type, for spreading each type's forms

# ------------------------------------------------------------------
# Writing: a line is (m, b), Fractions, m and b not 0
# ------------------------------------------------------------------
slope_intercept = si.slope_intercept
point_slope = ps.point_slope

def coefficients(m, b):
    """(A, B, C), integers, of A x + B y = C for y = m x + b: A > 0, no common factor."""
    n = math.lcm(m.denominator, b.denominator)
    a, bb, c = int(-m * n), n, int(b * n)
    if a < 0:
        a, bb, c = -a, -bb, -c
    g = math.gcd(a, bb, c)
    return a // g, bb // g, c // g

def standard(m, b):
    """"2 x - 3 y = 17"."""
    a, bb, c = coefficients(m, b)
    return f"{written((a, 'x'), (bb, 'y'))} = {c}"

def general(m, b):
    """"2 x - 3 y - 17 = 0"."""
    a, bb, c = coefficients(m, b)
    return f"{written((a, 'x'), (bb, 'y'), (-c, ''))} = 0"

def intercepts(m, b):
    """(x-intercept, y-intercept), Fractions."""
    return -b / m, b

def intercept(m, b):
    """"x/6 - y/4 = 1", "-x/2 + y/5 = 1"; the intercepts must be whole numbers."""
    xi, yi = intercepts(m, b)
    if xi.denominator != 1 or yi.denominator != 1:
        raise ValueError("intercept form needs whole-number intercepts")
    first = f"{'-' if xi < 0 else ''}x/{abs(xi)}"
    return f"{first} {'-' if yi < 0 else '+'} y/{abs(yi)} = 1"

def write(form, m, b, pt=None):
    """The line in that form; point-slope form goes through pt."""
    if form == "ps":
        return point_slope(m, *pt)
    return dict(si=slope_intercept, std=standard, gen=general, int=intercept)[form](m, b)

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def lattice(m, b, n=LATTICE):
    """The integer points of the line with both coordinates non-zero and from -n to n."""
    return [(x, int(m * x + b)) for x in range(-n, n + 1)
            if x != 0 and (m * x + b).denominator == 1 and m * x + b != 0 and abs(m * x + b) <= n]

def draw(entry, r, tpl, want=None):
    form = want or r.choice(SOURCES[entry])
    target = TARGET[entry]
    if "int" in (form, target):
        xi, yi = gen.signed(r, 1, INTERCEPTS), gen.signed(r, 1, INTERCEPTS)
        m, b = F(-yi, xi), F(yi)
        pt = None
        if form == "ps":
            pts = lattice(m, b)
            need(pts)
            pt = r.choice(pts)
    else:
        m, pt = ps.slope(r), (gen.signed(r, 1, POINT), gen.signed(r, 1, POINT))
        b = pt[1] - m * pt[0]
        need(b != 0 and abs(b) <= Y_INTERCEPT)
    prompt, answer = write(form, m, b, pt), write(target, m, b)
    need(prompt != answer)
    return dict(form=form, prompt=prompt, answer=answer)

def _type(entry):
    """A type's own generator: its starting forms are spread over the sheet's problems of that type only."""
    return gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: 1,
                         balance=(SOURCES[entry], lambda k: k[2] if k[0] == NAME and len(k) == 4 and k[3] == entry else None))
TYPE_GENERATE = {k: _type(k) for k in KEYS}

def generate(entry, rng, seen):
    return TYPE_GENERATE[entry](entry, rng, seen)

# ------------------------------------------------------------------
# Reading back and checking
# ------------------------------------------------------------------
COEF = r"(?:[1-9]\d* )?"                       # "", "2 ": a coefficient, 1 left off
STANDARD = re.compile(rf"(?P<a>{COEF})x (?P<s>[+-]) (?P<b>{COEF})y = (?P<c>-?(?:0|[1-9]\d*))")
GENERAL = re.compile(rf"(?P<a>{COEF})x (?P<s>[+-]) (?P<b>{COEF})y (?P<t>[+-]) (?P<c>[1-9]\d*) = 0")
INTERCEPT = re.compile(r"(?P<sx>-?)x/(?P<p>[1-9]\d*) (?P<s>[+-]) y/(?P<q>[1-9]\d*) = 1")

def clean(t):
    return " ".join(t.replace("−", "-").split())

def tidy(t):
    """Hand-typed math spaced as the key spaces it: "3x+4y=10" -> "3 x + 4 y = 10",
    "y+3=2/3(x-4)" -> "y + 3 = 2/3 (x - 4)". A minus at the start, or after =, (, +, or -, stays a sign."""
    t = clean(t).replace(" ", "")
    t = re.sub(r"(\d)([xy(])", r"\1 \2", t)
    t = re.sub(r"(?<=[\w)])([+\-=])", r" \1 ", t)
    t = re.sub(r"=(?=\S)", "= ", t)
    return clean(t)

def coef(t):
    """"" is 1, "2 " is 2; None for "1 " (1 is left off)."""
    t = t.strip()
    return 1 if t == "" else None if t == "1" else int(t)

def says(t, m, b):
    """(m, b) if the text, solved for y with sympy, is that line; None if not."""
    try:
        return (m, b) if si.solved(t) == (m, b) else None
    except Exception:
        return None

def read_si(t):
    return ps.read_slope_intercept(t)

def read_ps(t):
    """(m, b) of point-slope form, its point's coordinates not 0 (as Lesson 2-2 writes it)."""
    got = ps.read_point_slope(t)
    if got is None or 0 in got[1:]:
        return None
    m, x1, y1 = got
    return m, y1 - m * x1

def read_std(t):
    g = STANDARD.fullmatch(t)
    if not g:
        return None
    a, bb, c = coef(g["a"]), coef(g["b"]), int(g["c"])
    if a is None or bb is None or math.gcd(a, bb, c) != 1:
        return None
    bb = -bb if g["s"] == "-" else bb
    return says(t, F(-a, bb), F(c, bb))

def read_gen(t):
    g = GENERAL.fullmatch(t)
    if not g:
        return None
    a, bb, c = coef(g["a"]), coef(g["b"]), int(g["c"])
    if a is None or bb is None or math.gcd(a, bb, c) != 1:
        return None
    bb, c = (-bb if g["s"] == "-" else bb), (-c if g["t"] == "-" else c)
    return says(t, F(-a, bb), F(-c, bb))

def read_int(t):
    g = INTERCEPT.fullmatch(t)
    if not g:
        return None
    xi = -int(g["p"]) if g["sx"] else int(g["p"])
    yi = -int(g["q"]) if g["s"] == "-" else int(g["q"])
    return says(t, F(-yi, xi), F(yi))

READ = dict(si=read_si, ps=read_ps, std=read_std, gen=read_gen, int=read_int)

def read(form, t):
    """(m, b) of the text read strictly in that form, or None."""
    try:
        return READ[form](clean(t))
    except Exception:
        return None

def form_of(t):
    """The form a prompt is written in, or None."""
    return next((f for f in FORMS if read(f, t) is not None), None)

def check(p):
    try:
        typ, form = p["type"], p.get("form")
        if form not in SOURCES[typ]:
            return "failed"
        got = read(form, p["prompt"])
        if got is None or got != si.solved(clean(p["prompt"])):     # the prompt in its form, and sympy agrees
            return "failed"
        m, b = got
        if m == 0 or b == 0:
            return "failed"
        return "checked" if read(TARGET[typ], p["answer"]) == (m, b) else "failed"
    except Exception:
        return "unchecked"

def answer_of(prompt, typ):
    """The key's answer for a prompt in any of the type's starting forms; ValueError if it isn't one."""
    form = form_of(prompt)
    if form is None or form not in SOURCES[typ]:
        raise ValueError
    m, b = read(form, prompt)
    if m == 0 or b == 0:
        raise ValueError("a horizontal line, or one through the origin")
    return form, write(TARGET[typ], m, b)

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, _height = gen.shown()

def height(p):
    return 0.55 if "/" in p["prompt"] or "/" in p["answer"] else 0.3

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
EXAMPLE = "2 x - 3 y = 12"

def edit_text(p):
    return p["prompt"]

def answer_edit_text(p):
    return p["answer"]

def from_edit(t, old):
    """An edited prompt in one of the type's starting forms, its answer worked out again. A prompt
    in the type's own form, or in none of the forms, is refused."""
    typ = old.get("type")
    t = tidy(t)
    form = form_of(t)
    if form is None:
        raise ValueError(f"write it in slope-intercept, point-slope, standard, general, or intercept form, like {EXAMPLE}")
    if form == TARGET[typ]:
        raise ValueError(f"that's already in {FORM_NAME[form]} form")
    try:
        _, ans = answer_of(t, typ)
    except ValueError:
        m, b = read(form, t)
        if TARGET[typ] == "int" and m != 0 and b != 0:
            raise ValueError("its intercepts aren't whole numbers, so it has no intercept form here") from None
        ans = old["answer"]                  # a horizontal line, or one through the origin: check() marks it
    new = dict(old, prompt=t, form=form, answer=ans, source="edited")
    return new, check(new)

def with_answer(p, t):
    new = dict(p, answer=tidy(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
