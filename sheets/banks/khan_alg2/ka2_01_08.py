"""Khan Algebra 2, Lesson 1-8: Multiply monomials by polynomials, from the old app's Alg2_01_08
(fifteen of Khan's, without answers).

3x(x^2 - 5x + 6), 2x^2(9x^2 - 16): a monomial (degree 1 or 2, coefficient
-6 to 6) times a polynomial of two or three terms.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "3 x (x^2 - 5 x + 6)"
    answer  "3 x^3 - 15 x^2 + 18 x"
check() requires the answer to be the same polynomial as the prompt,
multiplied out and written in standard form (khan_alg1/polybank).
"""
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, signed_except, written
from ...typmath import display, dfrac, text as plain
from . import courses
from ..khan_alg1.polybank import expand_check, expand_answer_of, expand_edits

NAME = FAMILY = "ka2_01_08"
FIXED = False
TITLE = "Lesson 1-8: Multiply monomials by polynomials"
INSTRUCTIONS = "Expand. Write each answer as a polynomial in standard form."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Monomial Times Polynomial",
         look="A monomial times a polynomial in parentheses.",
         move="Multiply the monomial by each term: multiply coefficients, add exponents."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def poly_in(r, v, degrees, hi=9):
    """A polynomial with terms of these degrees, coefficients -hi..hi (not 0), descending."""
    return written(*[(signed(r, 1, hi), "" if d == 0 else v if d == 1 else f"{v}^{d}") for d in sorted(degrees, reverse=True)])

def degrees(r, top=3, n=None):
    n = n or r.randint(2, 3)
    return r.sample(range(0, top + 1), min(n, top + 1))

def t_mono_poly(r, v):
    m = written((signed(r, 1, 6), v if r.random() < 0.5 else f"{v}^2"))
    return f"{m} ({poly_in(r, v, degrees(r, 3), 10)})"

TEMPLATES = {"1": [t_mono_poly]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    answer = expand_answer_of(prompt)
    need(answer != "0")
    return dict(prompt=prompt, answer=answer)

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("3 x (x^2 - 5 x + 6)", "3 x^3 - 15 x^2 + 18 x")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
