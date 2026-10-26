"""Khan Algebra 2, Lesson 3-7: Factor polynomials using structure, from the
old app's Alg2_03_07 (eighteen of Khan's, without answers).

Factor completely. Type 1: a difference of squares, 16 x^2 - 49 y^2,
16 x^6 - 81, 81 p^8 - 100. Type 2: a perfect square, 9 m^2 + 30 m n + 25 n^2,
49 m^4 + 140 m^2 + 100, 64 y^6 - 48 y^3 + 9. Khan's letter pairs (x, y),
(m, n), (p, q), (c, d), or one letter and a number. The numbers have no
common factor, and the factors don't factor again (16 x^4 - 81 would).

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "16 x^2 - 49 y^2"
    answer  "(4 x + 7 y) (4 x - 7 y)"
check() requires the answer to be the same polynomial, factored completely
over the integers (poly.completely_factored).
"""
import math
import sympy as sp
from ... import gen, poly
from ...gen import need
from ...check import to_sympy
from ...typmath import tx
from . import courses
from .patterns import mono, square_text, difference_text, sum_text

NAME = FAMILY = "ka2_03_07"
FIXED = False
TITLE = "Lesson 3-7: Factor polynomials using structure"
INSTRUCTIONS = "Factor completely."
COURSES = courses(3)
PAIRS = [("x", "y"), ("m", "n"), ("p", "q"), ("c", "d"), ("a", "b")]

TYPES = [
    dict(key="1", title="Difference of Squares",
         look="Two squares with a minus between them.",
         move="U^2 - V^2 = (U + V)(U - V). U and V are the square roots: root the numbers, halve the exponents."),
    dict(key="2", title="Perfect Squares",
         look="Three terms: the first and last are squares, the middle one twice their product.",
         move="U^2 ± 2 U V + V^2 = (U ± V)^2. Find U and V from the squares, then check the middle term."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    u, v = r.choice(PAIRS)
    U = mono(r.randint(1, 11), u, r.randint(1, 4))
    V = mono(r.randint(1, 11)) if r.random() < 0.4 else mono(r.randint(1, 11), v, r.randint(1, 4))
    need(math.gcd(U.k, V.k) == 1 and U.k * V.k > 1)
    if entry == "1":
        prompt, answer = difference_text(U, V), f"({sum_text(U, V)}) ({sum_text(U, V, -1)})"
    else:
        s = r.choice((1, -1))
        prompt, answer = square_text(U, V, s), f"({sum_text(U, V, s)})^2"
    need(poly.completely_factored(answer, prompt))
    return dict(prompt=prompt, answer=answer)

def answer_of(prompt):
    return tx(sp.factor(to_sympy(prompt)))

def check(p):
    try:
        return "checked" if poly.completely_factored(p["answer"], p["prompt"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "16 x^2 - 49 y^2", "(4 x + 7 y) (4 x - 7 y)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
