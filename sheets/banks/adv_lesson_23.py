"""Lesson 23 (Advanced Math): the exponential function, sketching
exponentials. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_023/slides/deck_023.typ): examples
23.1-23.3 and Problem Set 23, problems 7 and 8.

    1  base greater than 1       y = 2^x,  f(x) = 5^x        (0, 1), (1, 2), (2, 4), (3, 8)
    2  base between 0 and 1      y = 0.25^x,  g(x) = (1/2)^x  (-1, 4), (0, 1)

The types are the two headings of problem_types.txt. A base greater than 1
rises to the right, its tail on the left; a base between 0 and 1 falls to
the right, its tail on the right. Type 2 has two templates, the base as a
decimal (example 23.3, 0.25^x: the move is 1/0.25 = 4) and as a fraction
(problem 8, (1/2)^x).

Both types print blank axes, the same window for every problem (x from -4
to 4, y from -1 to 11), so the window gives nothing away, and the key draws
the curve with its marked points. On a slide the axes stand beside the
function, the answer hidden on the question slide, so nothing moves.

Answer conventions, from the deck's "To sketch" rule ("every curve passes
through (0, 1), and the tail hugs the x axis. Draw the tail, then find one
or two points on the other side"):
  - A sketch is its marked points: (0, 1), then the whole-number points on
    the steep side, out to the last one at most 10 high, left to right.
    5^x: (0, 1), (1, 5) (example 23.2's one point, 25 is off the graph).
    0.25^x: (-1, 4), (0, 1) (example 23.3: "(-2, 16) falls off the graph").
    2^x: (0, 1), (1, 2), (2, 4), (3, 8) (problem 7). (1/2)^x: (-3, 8),
    (-2, 4), (-1, 2), (0, 1) (problem 8).
  - Example 23.1's slide makes a table at x = -3, -2, 0, 2, 3 instead; the
    key keeps the one rule, the same as problem 7 (the same function). The
    tail's points (1/8, 1/4) are not marked: the tail hugs the axis.
  - Every coordinate is a whole number: the bases are whole numbers (Type 1)
    or 1 over one (Type 2).

check() works from the problem's data, not from how the answer was made: it
reads the function back from the prompt with sympy (a decimal base as the
exact fraction), requires a constant base to the power x, greater than 1
for Type 1 and between 0 and 1 for Type 2, and reads the answer's points.
Each point is on the curve; (0, 1) is one of them; the others are on the
side where the curve is above 1, at consecutive whole numbers out from 0,
none higher than 10, and the next one out is higher than 10 (none left
out); the points are left to right.

No sources are skipped. Lesson 23 has no proofs among its types; the review
problems (1-6, 9-30) are other lessons' types.

A problem: dict(type, prompt, answer, source). The prompt is what an edit
changes:
    1  "f(x) = 5^x"          "(0, 1), (1, 5)"
    2  "g(x) = (1/2)^x"      "(-3, 8), (-2, 4), (-1, 2), (0, 1)"
"""
import re
from functools import lru_cache
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy
from ..graphs import Graph, PREAMBLE as GRAPH_PREAMBLE
from ..typmath import fr, dfrac, text as plain

NAME = FAMILY = "adv_lesson_23"
FIXED = False
TITLE = "Lesson 23: The Exponential Function, Sketching Exponentials"
INSTRUCTIONS = "Sketch the graph of each function."
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = GRAPH_PREAMBLE

TYPES = [
    dict(key="1", title="Sketch an Exponential, Base Greater Than 1",
         look="A whole number greater than $1$ to the power $x$, like $2^x$ or $5^x$.",
         move="The base is greater than $1$, so $y$ increases as $x$ increases. Every curve passes through "
              "$(0, 1)$. Draw the tail on the left, hugging the $x$ axis, then find one or two points on the "
              "right: $2^1 = 2$, $2^2 = 4$, $2^3 = 8$.",
         space="0.5in"),
    dict(key="2", title="Sketch an Exponential, Base Between 0 and 1",
         look="A base between $0$ and $1$, like $0.25^x$ or $(1/2)^x$.",
         move="The base is less than $1$, so $y$ decreases as $x$ increases: the tail is on the right. The "
              "curve passes through $(0, 1)$. Find points on the left with negative exponents: $(0.25)^(-1) = "
              "1/0.25 = 4$, $(1/2)^(-2) = 2^2 = 4$.",
         space="0.5in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
X = sp.Symbol("x")
CAP = 10                                        # the highest point the key marks

def initial_seen():
    return set()

def seen_key(p):
    """A function is the same problem whatever it's called, and 0.5^x is (1/2)^x."""
    try:
        return (NAME, p["type"], base_of(p["prompt"]))
    except (ValueError, KeyError):
        return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Templates and ranges
# ------------------------------------------------------------------
NAMES = ("y", "f", "g", "h")
BASES = range(2, 11)                            # Type 1: b^x
SMALL = (2, 3, 4, 5)                            # the book's bases, and the ones with the most points
RECIPROCALS = range(2, 11)                      # Type 2: (1/k)^x
DECIMALS = {2: "0.5", 4: "0.25", 5: "0.2", 10: "0.1"}   # 1/k as a decimal, where it ends soon

def left(name):
    return "y" if name == "y" else f"{name}(x)"

def t1_build(name, b):
    return f"{left(name)} = {b}^x"

def t1_small_pick(r):                           # the book's: 2^x, 5^x
    return dict(name=r.choice(NAMES), b=r.choice(SMALL))

def t1_any_pick(r):
    return dict(name=r.choice(NAMES), b=r.choice(BASES))

def t2_build(name, k, decimal):
    base = DECIMALS[k] if decimal else f"({fr('1', str(k))})"
    return f"{left(name)} = {base}^x"

def t2_fraction_pick(r):                        # problem 8: (1/2)^x
    return dict(name=r.choice(NAMES), k=r.choice(SMALL + tuple(RECIPROCALS)), decimal=False)

def t2_decimal_pick(r):                         # example 23.3: 0.25^x
    return dict(name=r.choice(NAMES), k=r.choice(tuple(DECIMALS)), decimal=True)

TEMPLATES = {
    "1": [(t1_small_pick, t1_build), (t1_small_pick, t1_build), (t1_any_pick, t1_build)],
    "2": [(t2_fraction_pick, t2_build), (t2_decimal_pick, t2_build)],
}

RANGES = {
    t1_build: lambda name, b: name in NAMES and b in BASES,
    t2_build: lambda name, k, decimal: name in NAMES and (k in DECIMALS if decimal else k in RECIPROCALS),
}

def in_range(build, params):
    """Can a random draw pick these parameters for this build?"""
    return RANGES[build](**params)

# ------------------------------------------------------------------
# Reading prompts
# ------------------------------------------------------------------
FUNC = re.compile(r"^(y|[a-z]\(x\)) = (.+)$")
KIND = {"1": "grows", "2": "decays"}
HINT = "write it like y = 2^x, y = 0.25^x, or g(x) = (1/2)^x"

@lru_cache(maxsize=512)
def read_function(prompt):
    """(what the prompt calls it, the function as exact sympy in x). Cached: a type holds few
    prompts, and a draw near the end of one asks for the same ones again and again."""
    m = FUNC.match(" ".join(prompt.split()))
    if not m:
        raise ValueError(HINT)
    f = sp.nsimplify(to_sympy(m.group(2)), rational=True)
    if f.free_symbols != {X}:
        raise ValueError("the function is in x")
    return m.group(1), f

def base_of(prompt):
    """b, for a prompt b^x: a positive constant other than 1."""
    _, f = read_function(prompt)
    if not (f.is_Pow and f.exp == X and f.base.is_Rational and f.base > 0 and f.base != 1):
        raise ValueError(HINT)
    return f.base

def kind(prompt):
    b = base_of(prompt)
    return "grows" if b > 1 else "decays"

# ------------------------------------------------------------------
# The answer: the points the key marks
# ------------------------------------------------------------------
def points_text(pts):
    return ", ".join(f"({a}, {b})" for a, b in pts)

def answer_of(prompt):
    b = F(int(sp.numer(base_of(prompt))), int(sp.denom(base_of(prompt))))
    step = 1 if b > 1 else -1                   # toward the steep side
    if (b if b > 1 else 1 / b).denominator != 1:
        raise ValueError("this bank marks whole-number points: a whole-number base, or 1 over one")
    pts, n = [(0, 1)], step
    while b ** n <= CAP:
        pts.append((n, int(b ** n)))
        n += step
    return points_text(sorted(pts))

NUM = r"-?\d+"
POINT = re.compile(rf"\(\s*({NUM})\s*,\s*({NUM})\s*\)")
POINTS = re.compile(rf"^\({NUM}, {NUM}\)(, \({NUM}, {NUM}\))*$")

def read_points(text):
    t = " ".join(text.split())
    if not POINTS.match(t):
        raise ValueError("write the points like (0, 1), (1, 2), (2, 4)")
    return [(sp.Integer(a), sp.Integer(b)) for a, b in POINT.findall(t)]

def holds(p):
    _, f = read_function(p["prompt"])
    pts = read_points(p["answer"])
    xs = [a for a, _ in pts]
    if xs != sorted(xs) or (0, 1) not in pts or not all(f.subs(X, a) == b for a, b in pts):
        return False
    side = [a for a in xs if a != 0]
    if not side or not all(f.subs(X, a) > 1 and f.subs(X, a) <= CAP for a in side):
        return False                            # only the steep side, none off the graph
    step = 1 if side[0] > 0 else -1
    far = sorted(side, key=abs)
    return (far == [step * (i + 1) for i in range(len(far))]   # 1, 2, 3 out from 0: none skipped
            and f.subs(X, far[-1] + step) > CAP)                # the next one out is off the graph

STRAY = 0.25        # how often a draw takes another of its type's templates

def draw(entry, r, tpl):
    """A type holds nine problems and a template as few as four, so a draw sometimes strays to
    another of its type's templates: a long sheet uses the whole type before it runs dry."""
    if r.random() < STRAY:
        tpl = r.randrange(len(TEMPLATES[entry]))
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        if kind(p["prompt"]) != KIND[p["type"]]:
            return "failed"
        ok = holds(p)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]), tries=2000)

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
CM = 0.4                                        # a graph's centimeters to a unit, on a sheet
WINDOW = dict(x=(-4, 4), y=(-1, CAP + 1))

def statement(p):
    return f"${dfrac(p['prompt'])}$"

def figure(p, key=False):
    """The same axes for every problem; on the key, the curve and its marked points."""
    name, f = read_function(p["prompt"])
    (x0, x1), (y0, y1) = WINDOW["x"], WINDOW["y"]
    g = Graph(x=(x0, x1), y=(y0, y1), width=CM * (x1 - x0), height=CM * (y1 - y0),
              step=(1, 1), label=2, ylabel="y" if name == "y" else f"${name}$",
              slide_width=2 * CM * (x1 - x0))
    if key:
        fn = sp.lambdify(X, f, "math")
        g.function(fn, x0 - 0.5, x1 + 0.5, color="blue", width=1.4, n=320)
        for a, b in read_points(p["answer"]):
            g.point(float(a), float(b), color="blue")
    return g.typst()

def _prompt(p, key):
    try:
        s, f = statement(p), figure(p, key)
    except (ValueError, KeyError, SyntaxError, TypeError, IndexError, AttributeError):
        return f"${p['prompt']}$"
    return f"#grid(columns: (auto, auto), column-gutter: 1.5em, align: horizon, [{s}], [{f}])"

def typst(p, gap="0.3em"):
    return _prompt(p, False)

def key_typst(p, gap="0.3em"):
    """The key's prompt: the curve drawn on the axes the sheet gives."""
    return _prompt(p, True)

def answer_typst(p):
    return f"${p['answer']}$"

def slide_typst(p, key=False):
    """The function and the answer (hidden on the question slide) beside the axes, which are the
    same on both slides, so nothing moves when the curve is drawn."""
    try:
        s, f = statement(p), figure(p, key)
    except (ValueError, KeyError, SyntaxError, TypeError, IndexError, AttributeError):
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{s} #v(0.8em) {shown}], [{f}])"

def text(p):
    return plain(p["prompt"])

def answer_text(p):
    return plain(p["answer"])

def height(p):
    """Inches the prompt takes on the page, for page estimates: the axes are 4.8 cm tall."""
    return 2.1

# ------------------------------------------------------------------
# Editing: the prompt is the problem's data
# ------------------------------------------------------------------
EXAMPLE = {"1": "y = 2^x", "2": "g(x) = (1/2)^x"}

def clean(t):
    t = t.replace("−", "-")
    t = re.sub(r"\s*\^\s*", "^", t)
    return " ".join(t.split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    if not FUNC.match(t):
        t = f"y = {t}"                          # a bare 2^x is y = 2^x
    try:
        if kind(t) != KIND[old["type"]]:
            raise ValueError
        new = dict(old, prompt=t, answer=answer_of(t), source="edited")
        status = check(new)
        if status == "unchecked":
            raise ValueError
    except (ValueError, gen.Redraw, SyntaxError, TypeError, KeyError, IndexError, AttributeError):
        raise ValueError(f"write it like: {EXAMPLE[old['type']]}") from None
    return new, status

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=8)
