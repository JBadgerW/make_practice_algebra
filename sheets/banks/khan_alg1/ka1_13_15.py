"""Khan Algebra 1, Lesson 13-15: Perfect squares, from the old app's Alg1_13_15
(sixteen slots, one template).

(d x + e)^2 multiplied out, or a (x + e)^2 with a common factor a, sometimes
written constant first. d and e are in lowest terms: the old template
didn't reduce them, so (2 x + 4)^2, which is 4 (x + 2)^2, was keyed as
factored completely.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "4 x^2 - 12 x + 9"
    answer  "(2 x - 3)^2"
check() requires the answer to be the same polynomial, factored completely:
the content in front, every factor left irreducible over the integers.
"""
import math
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, signed_except, written
from ...check import to_sympy
from . import courses
from .polybank import factor_check, factor_answer_of, factor_edits

NAME = FAMILY = "ka1_13_15"
FIXED = False
TITLE = "Lesson 13-15: Perfect squares"
INSTRUCTIONS = "Factor completely."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Perfect Square Trinomials",
         look="A trinomial whose first and last terms are squares, its middle term twice their product.",
         move="a^2 + 2 a b + b^2 = (a + b)^2: find a and b, and check the middle term."),
    dict(key="2", title="A Common Factor First",
         look="A perfect square trinomial times a number.",
         move="Take out the greatest common factor first. What's left is a perfect square trinomial."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t_square(r, v, reverse=False):              # 4 x^2 - 12 x + 9
    d, e = r.randint(1, 9), signed(r, 1, 12)
    need(math.gcd(d, abs(e)) == 1)
    x = sp.Symbol(v)
    q = sp.expand((d * x + e) ** 2)
    return reversed_text(q, v) if reverse else poly.expanded(q)

def t_common(r, v, reverse=False):             # 3 x^2 + 12 x + 12
    a, e = r.randint(2, 8), signed(r, 1, 12)
    x = sp.Symbol(v)
    q = sp.expand(a * (x + e) ** 2)
    return reversed_text(q, v) if reverse else poly.expanded(q)

def reversed_text(q, v):
    """Constant first: 9 - 12 x + 4 x^2."""
    c = sp.Poly(q, sp.Symbol(v)).all_coeffs()[::-1]
    return written(*[(int(k), "" if i == 0 else v if i == 1 else f"{v}^{i}") for i, k in enumerate(c)])

TEMPLATES = {"1": [t_square, lambda r, v: t_square(r, v, True)],
             "2": [t_common, lambda r, v: t_common(r, v, True)]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    return dict(prompt=prompt, answer=factor_answer_of(prompt))

check = factor_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = factor_edits("4 x^2 - 12 x + 9", "(2 x - 3)^2")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
