"""Lesson 27 (Advanced Math): related angles, signs of trigonometric
functions. From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_027/slides/deck_027.typ): examples
27.1-27.3 and Problem Set 27, problems 16 and 18.

    1  a positive angle outside the first quadrant:   4 cos 135°,  (5/3) cos 300°,  3 cos 300°
    2  a negative angle:                              -2 cos(-150°)
    3  a function's value at such an angle:           If f(x) = -2 cos x, find f(-300°).

Every angle has a related angle of 30°, 45°, or 60°: the value is the
related angle's (from the 30-60-90 or 45-45-90 triangle) with the sign of the
quadrant the angle ends in. Type 2's angles are measured clockwise; some end
in the first quadrant (-300°, as problem 18's does). The types file's one
heading is split by its closing note: a positive angle (27.1, 27.3, problem
16), a negative one (27.2), and problem 18's function notation, which
Lesson 21 made its own move.

Problem 17 (sin 60° + (sqrt(3)/2) sin 30°) has first-quadrant angles only;
it is Lesson 20's review, not a source here, as the types file says.

The key writes the exact value as the deck does (and as Lesson 20): one
fraction, the denominator rationalized, each radicand square-free, a minus
in front: 4 cos 135° = -2 sqrt(2), -2 cos(-150°) = sqrt(3), (5/3) cos 300° =
5/6, 3 cos 300° = 3/2. A function's value names what it finds, as Lesson 21's
do: "f(-300°) = -1" (the deck writes -1).

check() works the prompt out again with sympy and compares values exactly,
then checks the form with Lesson 20's rules: no trig left, no radical below,
radicands square-free, lowest terms. Type 3's answer must name the value
asked for.

No skipped sources: Lesson 27 has no proofs.

A problem: dict(type, prompt, answer, source), in Typst math. Types 1-2:
    prompt  "-2 cos(-150 degree)"                  shown  -2 cos(-150°)
    answer  "sqrt(3)"
Type 3, the rule and the value asked for:
    prompt  "f(x) = -2 cos(x); f(-300 degree)"     shown  If f(x) = -2 cos x, find f(-300°).
    answer  "f(-300 degree) = -1"
"""
import math, re
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, same_value
from ..typmath import single, fr, display, dfrac, text as plain
from .adv_lesson_20 import simplest

NAME = FAMILY = "adv_lesson_27"
FIXED = False
TITLE = "Lesson 27: Related Angles, Signs of Trigonometric Functions"
INSTRUCTIONS = "Draw the necessary reference triangles and evaluate. Do not use a calculator."
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="A Positive Angle Outside the First Quadrant",
         look="sin, cos, or tan of an angle like $135 degree$, $210 degree$, or $300 degree$, times a number.",
         move="Sketch the angle. The related angle is the acute angle to the $x$ axis: $135 degree$ has "
              "related angle $45 degree$. Take its value from the triangle, then the sign of the quadrant: "
              "cosine is negative in the second, so $cos 135 degree = -cos 45 degree = -1/sqrt(2)$. Multiply "
              "and rationalize."),
    dict(key="2", title="A Negative Angle",
         look="An angle like $-150 degree$: measured clockwise from the positive $x$ axis.",
         move="Measure the angle clockwise to find its quadrant: $-150 degree$ ends in the third. The related "
              "angle is the acute angle to the $x$ axis, $30 degree$. Use its value with the quadrant's sign: "
              "$cos(-150 degree) = -cos 30 degree = -sqrt(3)/2$."),
    dict(key="3", title="A Function's Value at Such an Angle",
         instructions="Do not use a calculator.",
         look="$f(x) = -2 cos x$, and $f$ of an angle outside the first quadrant, or a negative one.",
         move="Replace $x$ with the angle: $f(-300 degree) = -2 cos(-300 degree)$. Find the quadrant and the "
              "related angle ($-300 degree$ ends in the first, related angle $60 degree$), take the value with "
              "its sign, and multiply."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

FUNCS = ("sin", "cos", "tan")
WEIGHTED = ("cos", "cos", "sin", "tan")                 # the lesson's examples are all cosines
RELATED = (30, 45, 60)
POSITIVE = tuple(sorted(a for q in (180, 360) for r in RELATED for a in (q - r, q + r) if a < 360))
NEGATIVE = tuple(-a for a in sorted(set(POSITIVE) | set(RELATED)))     # -30° to -330°, every quadrant
WHOLE = tuple(n for n in range(-12, 13) if n)            # a whole-number coefficient
TOPS, BOTTOMS = range(1, 10), range(2, 7)                # a fraction's
LETTERS = ("f", "g", "h")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def quadrant(a):
    a %= 360
    return 1 + a // 90

def related(a):
    a %= 360
    return min(a % 180, 180 - a % 180)

# ------------------------------------------------------------------
# Builds: the coefficient n/d (d = 1: a whole number), the function, the angle
# ------------------------------------------------------------------
def coefficient(n, d):
    if d == 1:
        return {1: "", -1: "-"}.get(n, f"{n} ")
    return ("-" if n < 0 else "") + fr(str(abs(n)), str(d)) + " "

def term(n, d, f, a, x=None):
    return f"{coefficient(n, d)}{f}({x if x else f'{a} degree'})"

def coef_ok(n, d):
    if d == 1:
        return n in WHOLE
    return abs(n) in TOPS and d in BOTTOMS and math.gcd(n, d) == 1

def t1(n, d, f, a):
    return term(n, d, f, a)

def t1_ok(n, d, f, a):
    return coef_ok(n, d) and f in FUNCS and a in POSITIVE

def t2(n, d, f, a):
    return term(n, d, f, a)

def t2_ok(n, d, f, a):
    return coef_ok(n, d) and f in FUNCS and a in NEGATIVE

def t3(g, n, d, f, a):
    return f"{g}(x) = {term(n, d, f, a, x='x')}; {g}({a} degree)"

def t3_ok(g, n, d, f, a):
    return g in LETTERS and coef_ok(n, d) and f in FUNCS and a in POSITIVE + NEGATIVE

def whole(r):
    return dict(n=r.choice(WHOLE), d=1)

def fraction(r):
    n, d = r.choice(TOPS), r.choice(BOTTOMS)
    need(math.gcd(n, d) == 1)
    return dict(n=n * r.choice((1, 1, -1)), d=d)

def pick(angles, coef, letter=False):
    def p(r):
        out = dict(coef(r), f=r.choice(WEIGHTED), a=r.choice(angles))
        if letter:
            out["g"] = r.choice(LETTERS)
        return out
    return p

TEMPLATES = {
    "1": [(pick(POSITIVE, whole), t1), (pick(POSITIVE, whole), t1), (pick(POSITIVE, fraction), t1)],
    "2": [(pick(NEGATIVE, whole), t2), (pick(NEGATIVE, whole), t2), (pick(NEGATIVE, fraction), t2)],
    "3": [(pick(NEGATIVE, whole, True), t3), (pick(POSITIVE, whole, True), t3),
          (pick(POSITIVE + NEGATIVE, fraction, True), t3)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3: t3_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# Solving and checking
# ------------------------------------------------------------------
def parts(prompt):
    """Type 3's (letter, rule, the value asked for): "f(x) = -2 cos(x); f(-300 degree)"."""
    rule, ask = (s.strip() for s in prompt.split(";"))
    m = re.fullmatch(r"(\w)\(x\) = (.+)", rule)
    a = re.fullmatch(rf"{m.group(1)}\((.+)\)", ask)
    return m.group(1), m.group(2), ask, a.group(1)

def worked(prompt):
    """What to evaluate, in Typst math: Type 3's rule with x replaced, f(-300°) = -2 cos(-300°)."""
    if ";" in prompt:
        _, rule, _, arg = parts(prompt)
        return re.sub(r"\bx\b", arg, rule)
    return prompt

def value(prompt):
    return to_sympy(worked(prompt))

def answer_of(prompt):
    v = single(sp.radsimp(value(prompt)))
    return f"{parts(prompt)[2]} = {v}" if ";" in prompt else v

def draw(entry, r, tpl):
    pk, build = TEMPLATES[entry][tpl]
    prompt = build(**pk(r))
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        prompt, answer = p["prompt"], " ".join(p["answer"].split())
        if ";" in prompt:
            ask, eq, answer = answer.partition(" = ")
            if not eq or ask != parts(prompt)[2]:
                return "failed"
        ok = same_value(worked(prompt), answer) and simplest(answer)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: cos 135°, cos(-150°) (a negative angle keeps its parentheses), cos x
# ------------------------------------------------------------------
TRIG = re.compile(r"\b(sin|cos|tan)\((-?)(\d+|x)( degree)?\)")

def shown(t):
    return dfrac(TRIG.sub(lambda m: f"{m.group(1)}({m.group(2)}{m.group(3)}{m.group(4) or ''})" if m.group(2)
                          else f"{m.group(1)} {m.group(3)}{m.group(4) or ''}", t))

def readable(t):
    return plain(TRIG.sub(lambda m: f"{m.group(1)}({m.group(2)}{m.group(3)}{'°' if m.group(4) else ''})"
                          if m.group(2) else f"{m.group(1)} {m.group(3)}{'°' if m.group(4) else ''}", t)
                 .replace(" degree", "°"))

def typst(p, gap="0.3em"):
    if p["type"] == "3":
        _, rule, ask, _ = parts(p["prompt"])
        g = ask[0]
        return f"If ${g}(x) = {shown(rule)}$, find ${shown(ask)}$."
    return "Evaluate: #h(0.5em) " + display(shown(p["prompt"]))

def answer_typst(p):
    return display(shown(p["answer"]))

def text(p):
    if p["type"] == "3":
        _, rule, ask, _ = parts(p["prompt"])
        return f"If {ask[0]}(x) = {readable(rule)}, find {readable(ask)}."
    return "Evaluate: " + readable(p["prompt"])

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
        raise ValueError("write it in Typst math, like 4 cos(135 degree), or f(x) = -2 cos(x); f(-300 degree)") \
            from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
