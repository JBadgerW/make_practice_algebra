"""Lesson 2-4: Parallel and Perpendicular Lines. A line and a point; write the line parallel or
perpendicular to it through the point, in slope-intercept form; or two lines, and whether they
are parallel, perpendicular, or neither. Five types:

    1  Parallel, from slope-intercept form        y = 2/3 x - 4; (3, 5)       y = 2/3 x + 3
    2  Perpendicular, from slope-intercept form   y = 2/3 x - 4; (4, -1)      y = -3/2 x + 5
    3  Parallel, from another form                3 x - 2 y = 20; (-2, 5)     y = 3/2 x + 8
    4  Perpendicular, from another form           3 x - 2 y = 20; (6, -1)     y = -2/3 x + 3
    5  Parallel, perpendicular, or neither        y = 2 x + 6; x - 2 y = -6   neither

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

Type 5 reads "Are the lines y = 2 x + 6 and x - 2 y = -6 parallel, perpendicular, or neither?"
Each line is in any of the five forms, drawn at random (the same rules as the given line above,
with an intercept-form line's intercepts made to fit its slope). If the first slope is a/b (Lesson
2-2's slope), the second is one of
    a/b    parallel          (the lines distinct)
    -b/a   perpendicular
    b/a    neither           (a/b never 1 or -1 here, or it would be parallel or perpendicular)
    -a/b   neither
and the two slopes are as often one way round as the other. A sheet's Type 5 problems are spread
evenly over the four (gen.generator's balance), so half its answers are "neither". Its form is
the two lines' forms, "si,std"; its answer is the word.

A problem: dict(type, form, prompt, answer, source), in Typst math; form is the given line's.
    prompt  "3 x - 2 y = 20; (-2, 5)"      answer  "y = 3/2 x + 8"
    prompt  "y = 2 x + 6; x - 2 y = -6"    answer  "neither"            (Type 5, form "si,std")
check() reads the given line back from the prompt strictly in its form (and has sympy agree),
works out the wanted line from it and the point alone, and reads the answer strictly as
slope-intercept form. In Type 5 it reads both lines strictly in their forms, works out the
answer from their slopes, and fails a pair whose slopes aren't one of the four above.
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
    dict(key="5", title="Parallel, Perpendicular, or Neither",
         instructions="Tell whether each pair of lines is parallel, perpendicular, or neither.",
         look="Two lines, each in any of the five forms, like y = 2 x + 6 and x - 2 y = -6.",
         move="Find each line's slope: y = 2 x + 6 has m = 2; solve x - 2 y = -6 for y (y = 1/2 x + 3) "
              "and read m = 1/2. The same slope is parallel; opposite reciprocals (flipped, the sign "
              "changed) are perpendicular; anything else is neither. 2 and 1/2 are reciprocals, but "
              "the sign is the same, so the lines are neither."),
]

T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

PARALLEL = ("1", "3")          # 2 and 4 are perpendicular
WHICH = "5"                    # parallel, perpendicular, or neither
OTHER_FORMS = ("ps", "std", "gen", "int")
SOURCES = {"1": ("si",), "2": ("si",), "3": OTHER_FORMS, "4": OTHER_FORMS, WHICH: fm.FORMS}
CASES = ("parallel", "perpendicular", "reciprocal", "opposite")     # Type 5's second slope: a/b, -b/a, b/a, -a/b
VERDICT = dict(parallel="parallel", perpendicular="perpendicular", reciprocal="neither", opposite="neither")
GIVEN_INTERCEPT = 9            # the given line's y-intercept in si, std, gen form: -9 to 9
INTERCEPTS = 10                # intercept form: each intercept -10 to 10, not 0
POINT = 9                      # a point's coordinates, -9 to 9, not 0
INTERCEPT = 20                 # the answer's y-intercept (and a point-slope prompt's) at most this

def initial_seen():
    return set()

def relation(typ):
    return "parallel" if typ in PARALLEL else "perpendicular"

def seen_key(p):
    # Types 1 and 3 (and 2 and 4) never share a prompt on a sheet; the form and type, for spreading the forms;
    # in Type 5, the case, for spreading the four
    if p["type"] == WHICH:
        try:
            case = case_of(p)
        except Exception:
            case = None
        return (NAME, "which", p["prompt"], case, WHICH)
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
def given_line(r, form, m0=None):
    """(m0, b0, point-slope form's point or None) of a given line that form can show; its slope m0
    if given, else drawn."""
    if form == "int":
        if m0 is None:
            xi, yi = gen.signed(r, 1, INTERCEPTS), gen.signed(r, 1, INTERCEPTS)
            return F(-yi, xi), F(yi), None
        # y-intercept k |a|, x-intercept -k |a| / m0 = ∓ k b: both whole and at most 10 either way
        most = min(INTERCEPTS // abs(m0.numerator), INTERCEPTS // m0.denominator)
        need(most >= 1)
        return m0, F(gen.signed(r, 1, most) * abs(m0.numerator)), None
    m0 = ps.slope(r) if m0 is None else m0
    if form == "ps":
        q = (gen.signed(r, 1, POINT), gen.signed(r, 1, POINT))
        b0 = q[1] - m0 * q[0]
        need(b0 != 0 and abs(b0) <= INTERCEPT)
        return m0, b0, q
    if form in ("std", "gen"):                   # not through the origin
        return m0, F(gen.signed(r, 1, GIVEN_INTERCEPT)), None
    return m0, F(r.randint(-GIVEN_INTERCEPT, GIVEN_INTERCEPT)), None

def second_slope(case, m):
    return dict(parallel=m, perpendicular=-1 / m, reciprocal=1 / m, opposite=-m)[case]

def draw_which(r, case):
    m = ps.slope(r)
    need(case in ("parallel", "perpendicular") or abs(m) != 1)
    slopes = [m, second_slope(case, m)]
    r.shuffle(slopes)
    lines = []
    for m in slopes:
        form = r.choice(fm.FORMS)
        lines.append((form, *given_line(r, form, m)))
    need(lines[0][1:3] != lines[1][1:3])                        # two lines, not one
    return dict(form=",".join(f for f, *_ in lines), prompt="; ".join(fm.write(*l) for l in lines),
                answer=VERDICT[case])

def draw(entry, r, tpl, want=None):
    if entry == WHICH:
        return draw_which(r, want or r.choice(CASES))
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
    """A type's own generator: its given forms (in Type 5, its cases) are spread over the sheet's
    problems of that type only."""
    return gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: 1,
                         balance=(CASES if entry == WHICH else SOURCES[entry],
                                  lambda k: k[3] if k[0] == NAME and len(k) == 5 and k[4] == entry else None))
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

def split_two(prompt):
    """The two lines of a Type 5 prompt "y = 2 x + 6; x - 2 y = -6"; ValueError if it isn't two."""
    eqs = [e.strip() for e in clean(prompt).split(";")]
    if len(eqs) != 2 or not all(eqs):
        raise ValueError("write two lines, like y = 2 x + 6; x - 2 y = -6")
    return eqs

def lines_of(p):
    """[(m, b), (m, b)] of a Type 5 prompt, each line read strictly in its form, sympy agreeing,
    its slope not 0; ValueError if it isn't."""
    forms = p.get("form", "").split(",")
    eqs = split_two(p["prompt"])
    if len(forms) != 2 or not set(forms) <= set(fm.FORMS):
        raise ValueError("not two of the five forms")
    lines = []
    for form, eq in zip(forms, eqs):
        line = fm.read(form, eq)
        if line is None or line[0] == 0 or line != si.solved(eq):
            raise ValueError(f"write {eq} in {fm.FORM_NAME[form]} form, with a slope")
        lines.append(line)
    return lines

def case_of(p):
    """Which of the four a Type 5 prompt's slopes are, from the prompt alone; ValueError if the
    lines are one line or their slopes are none of the four."""
    (m1, b1), (m2, b2) = lines_of(p)
    if (m1, b1) == (m2, b2):
        raise ValueError("that's one line twice")
    case = next((c for c in CASES if second_slope(c, m1) == m2), None)
    if case is None:
        raise ValueError("the slopes are a/b and a/b, -b/a, b/a, or -a/b")
    return case

def word(t):
    """"Neither." -> "neither"."""
    return clean(t).lower().rstrip(".")

def check(p):
    try:
        try:
            if p["type"] == WHICH:
                return "checked" if word(p["answer"]) == VERDICT[case_of(p)] else "failed"
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
    if p["type"] == WHICH:
        try:
            one, two = split_two(p["prompt"])
        except ValueError:
            return show(p["prompt"])
        return f"Are the lines {show(one)} and {show(two)} parallel, perpendicular, or neither?"
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
    a = p["answer"]
    return f"#pad(top: 0.6em)[{a if p['type'] == WHICH and a.isalpha() else eq_typst(a)}]"

def text(p):
    return sentence(p, plain)

def answer_text(p):
    return p["answer"] if p["type"] == WHICH else plain(p["answer"])

def height(p):
    return 0.55 if "/" in p["prompt"] or "/" in p["answer"] else 0.3

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
EXAMPLE = {"1": "y = 2/3 x - 4; (3, 5)", "2": "y = 2/3 x - 4; (3, 5)",
           "3": "3 x - 2 y = 20; (-2, 5)", "4": "3 x - 2 y = 20; (-2, 5)", WHICH: "y = 2 x + 6; x - 2 y = -6"}
NUMBERED = re.compile(r"\(\s*[12]\s*\)")      # "(1) y = 2 x + 6, (2) ..." as a teacher might type it
TRAILING_POINT = re.compile(rf"[\s;,]*(?:through|point)?\s*(\(\s*(?:{si.NUMBER})\s*,\s*(?:{si.NUMBER})\s*\))\s*\.?\s*$")

def edit_text(p):
    return p["prompt"]

def answer_edit_text(p):
    return p["answer"]

def from_edit(t, old):
    """An edited prompt, its answer worked out again. In Types 1 and 2 the line may be typed in any
    form, and is written back in slope-intercept form; in Types 3 and 4 it must be in point-slope,
    standard, general, or intercept form, as Lesson 2-3 writes them. A prompt that breaks the
    rules keeps the old answer, which check() marks. In Type 5, two lines, each in any of the five
    forms as Lesson 2-3 writes them, between ";", ",", or "and"; the forms are kept as typed."""
    typ = old.get("type")
    if typ == WHICH:
        return which_from_edit(t, old)
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

def which_from_edit(t, old):
    bad = ValueError(f"write two lines, each in one of the five forms and with a slope, like {EXAMPLE[WHICH]}")
    t = NUMBERED.sub(" ", clean(t)).strip().rstrip(".?")
    eqs = [fm.tidy(e) for e in re.split(r";|,|\band\b", t) if e.strip()]
    if len(eqs) != 2:
        raise bad
    forms = [fm.form_of(e) for e in eqs]
    if None in forms:
        raise bad
    new = dict(old, prompt="; ".join(eqs), form=",".join(forms), source="edited")
    try:
        new["answer"] = VERDICT[case_of(new)]
    except ValueError:
        if lines_of_or_none(new) is None:
            raise bad from None
    return new, check(new)

def lines_of_or_none(p):
    try:
        return lines_of(p)
    except ValueError:
        return None

def with_answer(p, t):
    new = dict(p, answer=word(t) if p["type"] == WHICH else fm.tidy(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
