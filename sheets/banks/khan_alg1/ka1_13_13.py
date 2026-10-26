"""Khan Algebra 1, Lesson 13-13: Difference of squares, from the old app's Alg1_13_13
(sixteen slots, two templates).

d^2 x^2 - e^2 with d 2 to 9 and e 1 to 9 in lowest terms, or written
constant first (e^2 - d^2 x^2); Type 2 has a common factor that isn't a
square in front (2, 3, 5, 6, 7, 10), and d and e at most 6.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "9 x^2 - 49"
    answer  "(3 x - 7) (3 x + 7)"
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

NAME = FAMILY = "ka1_13_13"
FIXED = False
TITLE = "Lesson 13-13: Difference of squares"
INSTRUCTIONS = "Factor completely."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Difference of Squares",
         look="A square minus a square.",
         move="a^2 - b^2 = (a - b)(a + b): find what was squared, then write the two binomials."),
    dict(key="2", title="A Common Factor First",
         look="A difference of squares times a number.",
         move="Take out the greatest common factor first. What's left is a difference of squares."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def squares(r, hi=9):
    d, e = r.randint(2, hi), r.randint(1, hi)
    need(math.gcd(d, e) == 1)
    return d * d, e * e

def t_square_first(r, v, k=1):                 # 9 x^2 - 49, 2 (9 x^2 - 49) multiplied out
    a, b = squares(r, 9 if k == 1 else 6)
    return written((k * a, f"{v}^2"), (-k * b, ""))

def t_number_first(r, v, k=1):                 # 49 - 9 x^2
    a, b = squares(r, 9 if k == 1 else 6)
    return written((k * b, ""), (-k * a, f"{v}^2"))

def common(r):
    return r.choice((2, 3, 5, 6, 7, 10))

TEMPLATES = {"1": [t_square_first, t_number_first],
             "2": [lambda r, v: t_square_first(r, v, common(r)), lambda r, v: t_number_first(r, v, common(r))]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    return dict(prompt=prompt, answer=factor_answer_of(prompt))

check = factor_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = factor_edits("9 x^2 - 49", "(3 x - 7) (3 x + 7)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
