"""Khan Algebra 2, Lesson 3-4: Factor higher degree polynomials, from the old
app's Alg2_03_04 (twelve of Khan's, without answers).

Factor completely. Type 1: a common factor k x^m first, then a trinomial,
a difference of squares, or a perfect square (Khan's 2 x^4 + 4 x^3 - 30 x^2,
3 x^5 - 75 x^3, 5 x^4 - 20 x^3 + 20 x^2). Type 2: a product of two
quadratics, each to factor (Khan's (x^2 - 5 x + 4)(x^2 - 9),
(3 x^2 - 12 x)(x^2 - 2 x + 1)). Type 3: four terms, by grouping (Khan's
x^3 - 8 x^2 - 2 x + 16 = (x - 8)(x^2 - 2), x^4 + 5 x^3 + 4 x + 20).

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "2 x^4 + 4 x^3 - 30 x^2"
    answer  "2 x^2 (x - 3) (x + 5)"
check() requires the answer to be the same polynomial, factored completely
over the integers (khan_alg1/polybank.factor_check).
"""
import math
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, signed_except
from ...typmath import tx
from . import courses
from ..khan_alg1.polybank import factor_check, factor_answer_of, factor_edits

NAME = FAMILY = "ka2_03_04"
FIXED = False
TITLE = "Lesson 3-4: Factor higher degree polynomials"
INSTRUCTIONS = "Factor completely."
COURSES = courses(3)
x = sp.Symbol("x")

TYPES = [
    dict(key="1", title="A Common Factor First",
         look="Every term shares a number and a power of x.",
         move="Take out the greatest common factor, k x^m. Then factor what's left: a trinomial, a difference "
              "of squares, or a perfect square."),
    dict(key="2", title="A Product of Quadratics",
         look="Two quadratics multiplied.",
         move="Don't multiply out. Factor each quadratic, then write all the factors together."),
    dict(key="3", title="Grouping",
         look="Four terms, the first two and the last two sharing a factor.",
         move="Factor the first pair and the last pair. The same binomial is left in both: factor it out."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def common(r):
    """k x^m: Khan's 2 x^2, 7 x^3, 3 x^3, 5 x^2."""
    return r.randint(1, 7) * x ** r.randint(1, 3)

def t_trinomial(r):
    a = signed(r, 1, 7)
    return common(r) * (x - a) * (x - signed_except(r, 1, 7, a, -a))

def t_squares(r):
    return common(r) * (x ** 2 - r.randint(1, 9) ** 2)

def t_perfect(r):
    return common(r) * (x - signed(r, 1, 7)) ** 2

def quadratic(r):
    kind = r.choice(("roots", "squares", "perfect", "common"))
    if kind == "roots":
        a = signed(r, 1, 6)
        return (x - a) * (x - signed_except(r, 1, 6, a, -a))
    if kind == "squares":
        return x ** 2 - r.randint(1, 6) ** 2
    if kind == "perfect":
        return (x - signed(r, 1, 5)) ** 2
    return r.randint(1, 4) * x * (x - signed(r, 1, 6))              # Khan's 3 x^2 - 12 x, 2 x^2 + 4 x

def t_product(r):
    f, g = quadratic(r), quadratic(r)
    need(sp.expand(f - g) != 0)
    return f"({poly.expanded(f)})({poly.expanded(g)})"

def t_grouping(r):
    a = signed(r, 1, 9)
    n = r.choice((2, 2, 3, 4))
    b = signed(r, 1, 12)
    rest = x ** n + b
    need(len(sp.factor_list(rest)[1]) == 1 and sp.factor_list(rest)[1][0][1] == 1)   # x^2 - 2 doesn't factor
    return (x + a) * rest

TEMPLATES = {"1": [t_trinomial, t_squares, t_perfect], "2": [t_product], "3": [t_grouping]}

def draw(entry, r, tpl):
    e = TEMPLATES[entry][tpl](r)
    prompt = e if isinstance(e, str) else poly.expanded(e)
    if entry == "3":
        need(len(sp.Add.make_args(sp.expand(e))) == 4)
    return dict(prompt=prompt, answer=factor_answer_of(prompt))

check = factor_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = factor_edits("2 x^4 + 4 x^3 - 30 x^2", "2 x^2 (x - 3) (x + 5)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
