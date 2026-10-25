"""Khan Algebra 1, Lesson 13-11: Factor quadratics by grouping, from the old app's Alg1_13_11
(ten slots, one template).

(d x + e)(f x + g), multiplied out, with no common factor: d 2 to 9 (or\n-9 to -9), f 1 most of the time, e and g -9 to 9 (not -1 to 1), and\n|d e f g| at most 72, as the old template had it.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "2 x^2 + x - 15"
    answer  "(x + 3) (2 x - 5)"
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

NAME = FAMILY = "ka1_13_11"
FIXED = False
TITLE = "Lesson 13-11: Factor quadratics by grouping"
INSTRUCTIONS = "Factor completely."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Leading Coefficient Not 1",
         look="A quadratic a x^2 + b x + c whose a isn't 1, with no common factor.",
         move="Find two numbers that multiply to a c and add to b. Split the middle term with them, then factor by grouping."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t_grouping(r, v):                          # 2 x^2 + x - 15
    d = signed(r, 2, 9) if r.random() < 0.5 else r.randint(2, 9)
    e, g = signed(r, 2, 9), signed(r, 2, 9)
    f = gen.except_(r, 2, 9, d) if r.random() < 0.25 else 1
    need(abs(d * e * f * g) <= 72)
    x = sp.Symbol(v)
    q = sp.expand((d * x + e) * (f * x + g))
    need(poly.content(q) == 1)
    return poly.expanded(q)

TEMPLATES = {"1": [t_grouping]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    return dict(prompt=prompt, answer=factor_answer_of(prompt))

check = factor_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = factor_edits("2 x^2 + x - 15", "(x + 3) (2 x - 5)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
