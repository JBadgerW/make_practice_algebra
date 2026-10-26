"""Khan Algebra 2, Lesson 3-5: Identify quadratic patterns, from the old app's
Alg2_03_05 (sixteen of Khan's, without answers).

Which pattern can we use to factor the expression: (U + V)^2 or (U - V)^2,
(U + V)(U - V), or none? U and V are constant integers or single-variable
expressions, as Khan says: k x^n, (x + h), (x + h)^2, y^m, a number. The
"none" expressions are Khan's near misses: a sum of squares (9 x^4 + 4 y^2,
x^4 + 9), a middle term that isn't 2 U V (x^4 + 3 x^2 y + 9 y^2,
(x - 1)^2 + (x - 1) + 4), a middle term of the wrong power (x^4 + 10 x + 25),
or a term that isn't a square (x^3 - 25, 3 x^2 - 16 y^5). Khan's choices,
in Khan's order; the three answers are spread evenly over a sheet.

A problem: dict(type, prompt, U, V, sign, choices, answer, source).
    prompt  "(x + 7)^2 + 2 y (x + 7) + y^2"   U "(x + 7)"  V "y"  sign 1   answer "A"
check(): for A, (U + sign V)^2 is the expression; for B, U^2 - V^2 is; for
C, the expression has no factor over the integers at all.
"""
import math
import sympy as sp
from ... import gen
from ...gen import need, signed
from ...check import to_sympy
from ...typmath import display, text as plain
from . import courses
from .patterns import mono, binomial, square_text, difference_text, irreducible

NAME = FAMILY = "ka2_03_05"
FIXED = False
TITLE = "Lesson 3-5: Identify quadratic patterns"
INSTRUCTIONS = ("Which pattern can we use to factor each expression? U and V are either constant integers or "
                "single-variable expressions.")
COURSES = courses(3)
CHOICES = ["$(U+V)^2$ or $(U-V)^2$", "$(U+V)(U-V)$", "We can't use any of the patterns."]

TYPES = [
    dict(key="1", title="Which Pattern?",
         look="An expression with a square first: two terms or three.",
         move="Two squares with a minus between: (U + V)(U - V). Three terms, the outer two squares and the middle "
              "one 2 U V: (U ± V)^2. A plus between two squares, or a middle term that isn't 2 U V: no pattern.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p["answer"])

def part_x(r, power=False):
    if r.random() < 0.35:
        return binomial("x", signed(r, 1, 9), 2 if power and r.random() < 0.3 else 1)
    return mono(r.randint(1, 9), "x", r.randint(1, 4))

def part_y(r, binomials=False):
    roll = r.random()
    if roll < 0.35:
        return mono(r.randint(1, 9))
    if binomials and roll < 0.55:
        return binomial("y", signed(r, 1, 5), r.choice((1, 2)))
    return mono(r.randint(1, 6), "y", r.randint(1, 5))

def near_miss(r):
    """An expression no pattern fits."""
    U, V = part_x(r), part_y(r)
    U2, V2 = U.power(2), V.power(2)
    kind = r.choice(("sum", "middle", "power", "square"))
    if kind == "sum":
        return gen.written((U2.k, U2.body()), (V2.k, V2.body()))
    if kind == "middle":
        c = signed(r, 1, 4 * U.k * V.k)
        need(abs(c) != 2 * U.k * V.k)
        from .patterns import product_body
        return gen.written((U2.k, U2.body()), (c, product_body(U, V)), (V2.k, V2.body()))
    if kind == "power":                                             # x^4 + 10 x + 25
        need(U.kind == "mono" and U.n >= 2 and V.kind == "mono" and not V.v)
        n = r.choice([m for m in range(1, 2 * U.n) if m != U.n])
        mid = "x" if n == 1 else f"x^{n}"
        return gen.written((U2.k, U2.body()), (signed(r, 1, 1) * 2 * U.k * V.k, mid), (V2.k, V2.body()))
    a = r.choice((2, 3, 5, 6, 7, 8, 10, 1, 4, 9, 16, 25))           # x^3 - 25, 3 x^2 - 16 y^5
    e = r.randint(2, 7)
    other = V2 if r.random() < 0.5 else mono(V2.k, V.v or "y", r.choice((3, 5, 7)))
    return gen.written((a, f"x^{e}" if e > 1 else "x"), (-other.k, other.body()))

def draw(entry, r, tpl, want=None):
    outcome = want or r.choice("ABC")
    if outcome == "A":
        U, V, s = part_x(r), part_y(r), r.choice((1, -1))
        prompt = square_text(U, V, s)
        p = dict(U=U.text(), V=V.text(), sign=s)
    elif outcome == "B":
        U, V = part_x(r, power=True), part_y(r, binomials=True)
        need(not (U.kind == "bin" and V.kind == "bin" and U.n != V.n))
        prompt = difference_text(U, V)
        p = dict(U=U.text(), V=V.text(), sign=-1)
    else:
        prompt = near_miss(r)
        need(irreducible(prompt))
        p = {}
    if "U" in p:
        need(math.gcd(U.k, V.k) == 1)                              # no common factor to take out first
    need(len(prompt) < 60)
    choices, answer = gen.in_order(CHOICES, CHOICES["ABC".index(outcome)])
    return dict(p, prompt=prompt, choices=choices, answer=answer)

def fits(p):
    """The pattern the stored U and V make, if they make the expression; else None."""
    e = sp.expand(to_sympy(p["prompt"]))
    if "U" not in p:
        return None
    U, V = to_sympy(p["U"]), to_sympy(p["V"])
    if sp.expand((U + p["sign"] * V) ** 2 - e) == 0:
        return "A"
    if sp.expand(U ** 2 - V ** 2 - e) == 0:
        return "B"
    return None

def check(p):
    try:
        a = gen.letters_of(p["answer"])
        if a == ["C"]:
            return "checked" if irreducible(p["prompt"]) else "failed"
        return "checked" if len(a) == 1 and fits(p) == a[0] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1,
                         balance=("ABC", lambda k: k[2] if k[0] == NAME and len(k) == 3 else None))

def typst(p, gap="0.3em"):
    return f"{display(p['prompt'])} \\\n    {gen.choices_typst(p['choices'], 'linear')}"

def answer_typst(p):
    a = gen.choice_answer_typst(p)
    if "U" in p and gen.letters_of(p["answer"]) != ["C"]:
        a += f" ($U = {p['U']}$, $V = {p['V']}$)"
    return a

def text(p):
    return plain(p["prompt"]) + "   " + gen.choices_text([c.replace("$", "") for c in p["choices"]])

def answer_text(p):
    return gen.choice_answer_typst(p).replace("$", "")

def height(p):
    return 0.7

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new expression; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
