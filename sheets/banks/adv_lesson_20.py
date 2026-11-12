"""Lesson 20 (Advanced Math): two special triangles. From the Saxon lesson and
its deck (~/Documents/adv_math/problem_sets/ps_020/slides/deck_020.typ):
examples 20.1-20.4 and Problem Set 20, problems 9-11.

    1  a whole number times a trig value:    tan 30°,  7 sin 45°,  4 tan 60°
    2  a radical times a trig value:         4 sqrt(3) cos 60°,  6 sqrt(2) cos 30°,  6 sqrt(3) sin 45°
    3  a fraction with a radical below:      (10/sqrt(5)) tan 45°

Every angle is 30°, 45°, or 60°, so the value comes from the 30-60-90 or the
45-45-90 reference triangle, which the student draws. The key writes the
exact value as the deck does: one fraction, the denominator rationalized,
each radical simplified: tan 30° = sqrt(3)/3, 7 sin 45° = (7 sqrt(2))/2,
6 sqrt(2) cos 30° = 3 sqrt(6), (10/sqrt(5)) tan 45° = 2 sqrt(5).

check() works the prompt out again with sympy and compares values exactly,
then checks the form: no radical below, no square factor under a radical,
and the fraction in lowest terms.

A problem: dict(type, prompt, answer, source), in Typst math; sin(30 degree)
is shown sin 30°, as the deck writes it.
    prompt  "6 sqrt(2) cos(30 degree)"
    answer  "3 sqrt(6)"
"""
import math, re
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, same_value, simplest_form
from ..typmath import single, fr, display
from .adv_trig import shown, readable

NAME = FAMILY = "adv_lesson_20"
FIXED = False
TITLE = "Lesson 20: Two Special Triangles"
INSTRUCTIONS = "Draw the necessary reference triangle and evaluate. Do not use a calculator."
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="A Whole Number Times a Trig Value",
         look="sin, cos, or tan of 30°, 45°, or 60°, alone or times a whole number.",
         move="Draw the triangle: 45° uses the 45-45-90 triangle (sides 1, 1, sqrt(2)); 30° and 60° use the "
              "30-60-90 triangle (sides 1, sqrt(3), 2). Read opp/hyp, adj/hyp, or opp/adj, rationalize "
              "(1/sqrt(3) = sqrt(3)/3), and multiply."),
    dict(key="2", title="A Radical Times a Trig Value",
         look="A coefficient with a square root, like 6 sqrt(2) cos 30°.",
         move="Find the trig value from the triangle. Multiply the whole numbers together and the radicals "
              "together (sqrt(2) sqrt(3) = sqrt(6)), then simplify the fraction."),
    dict(key="3", title="A Fraction with a Radical Below",
         look="A coefficient like 10/sqrt(5).",
         move="Find the trig value from the triangle and multiply. Rationalize: multiply top and bottom by the "
              "radical below, then reduce: (10 sqrt(5))/5 = 2 sqrt(5).", space="1.25in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

FUNCS = ("sin", "cos", "tan")
ANGLES = (30, 45, 60)
RADICANDS = (2, 3, 5, 6, 7)                                     # under a coefficient's radical

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def trig(r):
    return f"{r.choice(FUNCS)}({r.choice(ANGLES)} degree)"

def value(f):
    """f(angle)'s exact value, rationalized: the triangle's ratio."""
    return sp.radsimp(to_sympy(f))

def radicand(r):
    """2 and 3 most often: they meet the triangles' sqrt(2) and sqrt(3)."""
    return r.choice((2, 2, 3, 3) + RADICANDS)

# ------------------------------------------------------------------
# Type 1: tan 30°, 7 sin 45°, 4 tan 60°
# ------------------------------------------------------------------
def t1(r):
    """Alone a quarter of the time (example 20.1; only 9 of those), else times
    a whole number (example 20.2, problem 11)."""
    return trig(r) if r.random() < 0.25 else f"{r.randint(2, 12)} {trig(r)}"

# ------------------------------------------------------------------
# Type 2: 4 sqrt(3) cos 60°, 6 sqrt(2) cos 30°, 6 sqrt(3) sin 45°
# ------------------------------------------------------------------
def root(k, m):
    return f"sqrt({m})" if k == 1 else f"{k} sqrt({m})"

def t2_even(r):                                                 # the deck's: the 2 below cancels
    return f"{root(2 * r.randint(1, 6), radicand(r))} {trig(r)}"

def t2_any(r):
    return f"{root(r.randint(1, 12), radicand(r))} {trig(r)}"

# ------------------------------------------------------------------
# Type 3: (10/sqrt(5)) tan 45°
# ------------------------------------------------------------------
def t3_multiple(r):                                             # the deck's: the radicand divides the top
    m = radicand(r)
    return f"{fr(str(m * r.randint(1, 4)), f'sqrt({m})')} {trig(r)}"

def t3_any(r):
    m = radicand(r)
    a = r.randint(1, 12)
    need(a % m)
    return f"{fr(str(a), f'sqrt({m})')} {trig(r)}"

TEMPLATES = {
    "1": [t1],
    "2": [t2_even, t2_even, t2_any],
    "3": [t3_multiple, t3_any],
}

# ------------------------------------------------------------------
# Solving and checking
# ------------------------------------------------------------------
def answer_of(prompt):
    return single(sp.radsimp(to_sympy(prompt)))

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r)
    return dict(prompt=prompt, answer=answer_of(prompt))

def squarefree(n):
    return n > 1 and all(n % (p * p) for p in range(2, math.isqrt(n) + 1))

def simplest(t):
    """The deck's form: no trig left, no radical below, radicands square-free; simplest_form
    rejects an unreduced fraction."""
    if re.search(r"\b(sin|cos|tan)\b", t) or not simplest_form(t):
        return False
    if re.search(r"/\s*\(?[^/]*sqrt", t):                       # a radical below
        return False
    rads = re.findall(r"sqrt\(([^)]*)\)", t)
    if not all(x.strip().isdigit() and squarefree(int(x)) for x in rads):
        return False
    return True

def check(p):
    try:
        ok = same_value(p["prompt"], p["answer"]) and simplest(p["answer"])
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: sin(30 degree) as sin 30°
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    return display(shown(p["prompt"]))

def answer_typst(p):
    return display(shown(p["answer"]))

def text(p):
    return readable(p["prompt"])

def answer_text(p):
    return readable(p["answer"])

def height(p):
    return 0.55 if "/" in p["prompt"] else 0.3

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
def clean(t):
    return " ".join(t.replace("−", "-").replace("°", " degree").split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    try:
        answer = answer_of(t)
    except Exception:
        raise ValueError("write it in Typst math, like 6 sqrt(2) cos(30 degree)") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
