"""Lesson 2-4: Parallel and Perpendicular Lines. A line and a point; write the line parallel or
perpendicular to it through the point, in slope-intercept form. Four types:

    1  Parallel, from slope-intercept form        y = 2/3 x - 4; (3, 5)       y = 2/3 x + 3
    2  Perpendicular, from slope-intercept form   y = 2/3 x - 4; (4, -1)      y = -3/2 x + 5
    3  Parallel, from another form                3 x - 2 y = 20; (-2, 5)     y = 3/2 x + 8
    4  Perpendicular, from another form           3 x - 2 y = 20; (6, -1)     y = -2/3 x + 3

Each problem reads "Find the equation of the line parallel to 3 x - 2 y = 20 that passes through
point (-2, 5)." Every answer is slope-intercept form, written as Lesson 2-1 writes it (lowest
terms, a slope of 1 left off).

In Types 3 and 4 the given line is in point-slope, standard, general, or intercept form, written
as Lesson 2-3 writes them; a sheet's problems of one type are spread evenly over the four
(gen.generator's balance). Types 1 and 2 give it in slope-intercept form.

The numbers:
    - The given slope is Lesson 2-2's: a whole number 1 to 6, or a fraction in lowest terms
      (denominator 2 to 5, numerator up to 7), either sign; never 0, so the perpendicular
      slope, -1/m, always exists.
    - The given line's y-intercept: in slope-intercept, standard, and general form, a whole
      number from -9 to 9 (not 0 in standard and general form, so neither goes through the
      origin). In intercept form, both intercepts are whole numbers, -10 to 10, not 0. In
      point-slope form, the line goes through a point whose coordinates are -9 to 9, not 0, and
      its y-intercept, often a fraction, is not 0 and at most 20 either way.
    - The point asked about: coordinates -9 to 9, not 0, and not the point in a point-slope
      prompt. In a parallel problem it is off the given line (otherwise the answer is the
      given line).
    - The answer's y-intercept, often a fraction, is at most 20 either way.

A problem: dict(type, form, prompt, answer, source), in Typst math; form is the given line's.
    prompt  "3 x - 2 y = 20; (-2, 5)"      answer  "y = 3/2 x + 8"
check() reads the given line back from the prompt strictly in its form (and has sympy agree),
works out the wanted line from it and the point alone, and reads the answer strictly as
slope-intercept form.
"""
import re
from fractions import Fraction as F
from .. import gen
from ..gen import need
from ..typmath import display, dfrac, text as plain
from . import slope_intercept_2_1 as si
from . import point_slope_2_2 as ps
from . import forms_2_3 as fm

NAME = FAMILY = "parallel_perp_2_4"
FIXED = False
TITLE = "Lesson 2-4: Parallel and Perpendicular Lines"
INSTRUCTIONS = ""              # each type has its own; a sheet of one type shows it at the top
COURSES = {"Algebra 1": "Lessons"}

ASKED = "Write each equation in slope-intercept form."
TYPES = [
    dict(key="1", title="Parallel, From Slope-Intercept Form", instructions=ASKED,
         look="A line in slope-intercept form, y = 2/3 x - 4, a point, (3, 5), and the parallel line asked for.",
         move="Parallel lines have the same slope: m = 2/3. Put it and the point into y = m x + b: "
              "5 = 2/3 (3) + b, so 5 = 2 + b and b = 3. The line is y = 2/3 x + 3."),
    dict(key="2", title="Perpendicular, From Slope-Intercept Form", instructions=ASKED,
         look="A line in slope-intercept form, y = 2/3 x - 4, a point, (4, -1), and the perpendicular line asked for.",
         move="A perpendicular slope is the opposite reciprocal: flip 2/3 and change its sign, m = -3/2. "
              "Put it and the point into y = m x + b: -1 = -3/2 (4) + b, so -1 = -6 + b and b = 5. "
              "The line is y = -3/2 x + 5."),
    dict(key="3", title="Parallel, From Another Form", instructions=ASKED,
         look="A line in another form, like 3 x - 2 y = 20, a point, (-2, 5), and the parallel line asked for.",
         move="Find the given line's slope: solve it for y (-2 y = -3 x + 20, so y = 3/2 x - 10) and read "
              "m = 3/2. The parallel line has the same slope. Put it and the point into y = m x + b: "
              "5 = 3/2 (-2) + b, so 5 = -3 + b and b = 8. The line is y = 3/2 x + 8."),
    dict(key="4", title="Perpendicular, From Another Form", instructions=ASKED,
         look="A line in another form, like 3 x - 2 y = 20, a point, (6, -1), and the perpendicular line asked for.",
         move="Find the given line's slope: solve it for y (y = 3/2 x - 10) and read m = 3/2. The "
              "perpendicular slope is its opposite reciprocal, -2/3. Put it and the point into "
              "y = m x + b: -1 = -2/3 (6) + b, so -1 = -4 + b and b = 3. The line is y = -2/3 x + 3."),
]

T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

PARALLEL = ("1", "3")          # the rest are perpendicular
OTHER_FORMS = ("ps", "std", "gen", "int")
SOURCES = {"1": ("si",), "2": ("si",), "3": OTHER_FORMS, "4": OTHER_FORMS}
GIVEN_INTERCEPT = 9            # the given line's y-intercept in si, std, gen form: -9 to 9
INTERCEPTS = 10                # intercept form: each intercept -10 to 10, not 0
POINT = 9                      # a point's coordinates, -9 to 9, not 0
INTERCEPT = 20                 # the answer's y-intercept (and a point-slope prompt's) at most this

def initial_seen():
    return set()

def relation(typ):
    return "parallel" if typ in PARALLEL else "perpendicular"

def seen_key(p):
    # Types 1 and 3 (and 2 and 4) never share a prompt on a sheet; the form and type, for spreading the forms
    return (NAME, relation(p["type"]), p["prompt"], p.get("form"), p["type"])

# ------------------------------------------------------------------
# Writing
# ------------------------------------------------------------------
slope_intercept = si.slope_intercept

def prompt_text(line_text, pt):
    """"3 x - 2 y = 20; (-2, 5)"."""
    return f"{line_text}; ({pt[0]}, {pt[1]})"

def wanted_slope(typ, m0):
    return m0 if typ in PARALLEL else -1 / m0

def answer(typ, m0, pt):
    """The key's answer, in slope-intercept form."""
    m = wanted_slope(typ, m0)
    return slope_intercept(m, pt[1] - m * pt[0])

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def given_line(r, form):
    """(m0, b0, point-slope form's point or None) of a given line that form can show."""
    if form == "int":
        xi, yi = gen.signed(r, 1, INTERCEPTS), gen.signed(r, 1, INTERCEPTS)
        return F(-yi, xi), F(yi), None
    m0 = ps.slope(r)
    if form == "ps":
        q = (gen.signed(r, 1, POINT), gen.signed(r, 1, POINT))
        b0 = q[1] - m0 * q[0]
        need(b0 != 0 and abs(b0) <= INTERCEPT)
        return m0, b0, q
    if form in ("std", "gen"):                   # not through the origin
        return m0, F(gen.signed(r, 1, GIVEN_INTERCEPT)), None
    return m0, F(r.randint(-GIVEN_INTERCEPT, GIVEN_INTERCEPT)), None

def draw(entry, r, tpl, want=None):
    form = want or r.choice(SOURCES[entry])
    m0, b0, q = given_line(r, form)
    pt = (gen.signed(r, 1, POINT), gen.signed(r, 1, POINT))
    need(pt != q and keeps_rules(entry, m0, b0, pt))
    return dict(form=form, prompt=prompt_text(fm.write(form, m0, b0, q), pt), answer=answer(entry, m0, pt))

def keeps_rules(typ, m0, b0, pt):
    """The point off the given line in a parallel problem; the answer's y-intercept at most 20 either way."""
    m = wanted_slope(typ, m0)
    x1, y1 = pt
    if typ in PARALLEL and y1 == m0 * x1 + b0:
        return False
    return abs(y1 - m * x1) <= INTERCEPT

def _type(entry):
    """A type's own generator: its given forms are spread over the sheet's problems of that type only."""
    return gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: 1,
                         balance=(SOURCES[entry], lambda k: k[3] if k[0] == NAME and len(k) == 5 and k[4] == entry else None))
TYPE_GENERATE = {k: _type(k) for k in KEYS}

def generate(entry, rng, seen):
    return TYPE_GENERATE[entry](entry, rng, seen)

# ------------------------------------------------------------------
# Reading back and checking
# ------------------------------------------------------------------
clean = fm.clean

def split(prompt):
    """(the given line, the point) as written in a prompt "3 x - 2 y = 20; (-2, 5)"; ValueError if
    there's no point after a ";"."""
    eq, sep, pt = clean(prompt).rpartition(";")
    if not sep or not eq.strip():
        raise ValueError("write a line and a point, like 3 x - 2 y = 20; (-2, 5)")
    return eq.strip(), pt.strip()

def given_of(prompt, form):
    """((m0, b0), (x1, y1)) of a prompt, the line read strictly in that form, sympy agreeing, its
    slope not 0; the point whole numbers. ValueError if it isn't."""
    eq, pt = split(prompt)
    line = fm.read(form, eq)
    g = si.POINT.fullmatch(pt)
    if line is None or g is None or line[0] == 0 or line != si.solved(eq):
        raise ValueError(f"write the line in {fm.FORM_NAME.get(form, '?')} form, and a point")
    x1, y1 = si.number(g[1]), si.number(g[2])
    if x1.denominator != 1 or y1.denominator != 1:
        raise ValueError("the point's coordinates are whole numbers")
    return line, (x1, y1)

def line_of(p):
    """(m, b) of the line the problem asks for, worked out from the prompt alone; ValueError if
    the prompt breaks the rules (its form isn't the type's, no slope, or a parallel problem's
    point on the given line)."""
    form = p.get("form", "si")
    if form not in SOURCES[p["type"]]:
        raise ValueError("not a form this type gives")
    (m0, b0), (x1, y1) = given_of(p["prompt"], form)
    if p["type"] in PARALLEL:
        if y1 == m0 * x1 + b0:
            raise ValueError("the point is on the line, so the parallel line is the line itself")
        m = m0
    else:
        m = F(-m0.denominator, m0.numerator)     # flip it and change its sign
        if m * m0 != -1:
            raise ValueError("no perpendicular slope")
    return m, y1 - m * x1

def check(p):
    try:
        try:
            want = line_of(p)
        except ValueError:
            return "failed"
        return "checked" if ps.read_slope_intercept(clean(p["answer"])) == want else "failed"
    except Exception:
        return "unchecked"

def answer_of(prompt, typ, form="si"):
    """The key's answer for a prompt of that type; ValueError if the prompt breaks the rules."""
    line_of(dict(type=typ, form=form, prompt=prompt))
    (m0, _), pt = given_of(prompt, form)
    return answer(typ, m0, pt)

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def eq_typst(t):
    return display(dfrac(t))

def sentence(p, show):
    try:
        line, pt = split(p["prompt"])
    except ValueError:
        return show(p["prompt"])
    return f"Find the equation of the line {relation(p['type'])} to {show(line)} that passes through point {show(pt)}."

def typst(p, gap="0.3em"):
    return sentence(p, eq_typst)

def answer_typst(p):
    """Set a little lower than usual: the prompt is a sentence that can run to the right edge, where
    the key's answer floats, and a fraction in the answer would ride up into it."""
    return f"#pad(top: 0.6em)[{eq_typst(p['answer'])}]"

def text(p):
    return sentence(p, plain)

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.55 if "/" in p["prompt"] or "/" in p["answer"] else 0.3

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
EXAMPLE = {"1": "y = 2/3 x - 4; (3, 5)", "2": "y = 2/3 x - 4; (3, 5)",
           "3": "3 x - 2 y = 20; (-2, 5)", "4": "3 x - 2 y = 20; (-2, 5)"}
TRAILING_POINT = re.compile(rf"[\s;,]*(?:through|point)?\s*(\(\s*(?:{si.NUMBER})\s*,\s*(?:{si.NUMBER})\s*\))\s*\.?\s*$")

def edit_text(p):
    return p["prompt"]

def answer_edit_text(p):
    return p["answer"]

def from_edit(t, old):
    """An edited prompt, its answer worked out again. In Types 1 and 2 the line may be typed in any
    form, and is written back in slope-intercept form; in Types 3 and 4 it must be in point-slope,
    standard, general, or intercept form, as Lesson 2-3 writes them. A prompt that breaks the
    rules keeps the old answer, which check() marks."""
    typ = old.get("type")
    t = clean(t)
    g = TRAILING_POINT.search(t)
    bad = ValueError(f"write a line with a slope and a point with whole-number coordinates, like {EXAMPLE[typ]}")
    if g is None:
        raise bad
    eq = fm.tidy(t[:g.start()])
    try:
        x1, y1 = (si.number(v) for v in si.POINT.fullmatch(g[1]).groups())
        m0, b0 = si.solved(eq)
    except Exception:
        raise bad from None
    if m0 == 0 or x1.denominator != 1 or y1.denominator != 1:
        raise bad
    if SOURCES[typ] == ("si",):
        form, eq = "si", slope_intercept(m0, b0)
    else:
        form = fm.form_of(eq)
        if form == "si":
            raise ValueError("that's slope-intercept form; this type gives the line in another form")
        if form not in SOURCES[typ]:
            raise ValueError("write the line in point-slope, standard, general, or intercept form, "
                             f"like {EXAMPLE[typ]}")
    prompt = prompt_text(eq, (int(x1), int(y1)))
    try:
        ans = answer_of(prompt, typ, form)
    except ValueError:
        ans = old["answer"]
    new = dict(old, prompt=prompt, form=form, answer=ans, source="edited")
    return new, check(new)

def with_answer(p, t):
    new = dict(p, answer=fm.tidy(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
