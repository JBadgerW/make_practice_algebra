"""Khan Algebra 2, Lesson 1-4: Subtract polynomials (intro), from the old app's Alg2_01_04
(twenty of Khan's, without answers).

(2k^3 + 6k + 1) - (2k^2 + 1): the second polynomial subtracted, every sign
inside it changed. Degree up to 4, coefficients -10 to 10.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(2 k^3 + 6 k + 1) - (2 k^2 + 1)"
    answer  "2 k^3 - 2 k^2 + 6 k"
check() requires the answer to be the same polynomial as the prompt,
multiplied out and written in standard form (khan_alg1/polybank).
"""
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, signed_except, written
from ...typmath import display, dfrac, text as plain
from . import courses
from ..khan_alg1.polybank import expand_check, expand_answer_of, expand_edits

NAME = FAMILY = "ka2_01_04"
FIXED = False
TITLE = "Lesson 1-4: Subtract polynomials (intro)"
INSTRUCTIONS = "Subtract. Write each answer as a polynomial in standard form."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Subtract Polynomials",
         look="One polynomial minus another in parentheses.",
         move="Change the sign of every term in the second polynomial, then combine like terms."),
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

def t_sub(r, v):
    return f"({poly_in(r, v, degrees(r, r.choice((2, 3, 4))), 10)}) - ({poly_in(r, v, degrees(r, r.choice((2, 3, 4))), 10)})"

TEMPLATES = {"1": [t_sub]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    answer = expand_answer_of(prompt)
    need(answer != "0")
    return dict(prompt=prompt, answer=answer)

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("(2 k^3 + 6 k + 1) - (2 k^2 + 1)", "2 k^3 - 2 k^2 + 6 k")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
