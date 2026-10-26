"""Khan Algebra 2, Lesson 1-6: Multiply monomials, from the old app's Alg2_01_06
(sixteen of Khan's, without answers).

(3y^5)(5y^4): coefficients -9 to 9 (Khan's include -1 and 1, written as a
sign), exponents 2 to 9.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(3 y^5) (5 y^4)"
    answer  "15 y^9"
check() requires the answer to be the same polynomial as the prompt,
multiplied out and written in standard form (khan_alg1/polybank).
"""
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, signed_except, written
from ...typmath import display, dfrac, text as plain
from . import courses
from ..khan_alg1.polybank import expand_check, expand_answer_of, expand_edits

NAME = FAMILY = "ka2_01_06"
FIXED = False
TITLE = "Lesson 1-6: Multiply monomials"
INSTRUCTIONS = "Multiply. Write each answer as a monomial in standard form."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Multiply Monomials",
         look="Two monomials multiplied.",
         move="Multiply the coefficients and add the exponents: (a x^m)(b x^n) = a b x^(m + n)."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
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

def t_mono(r, v):
    a, b = signed(r, 1, 9), signed(r, 1, 9)
    need(abs(a) + abs(b) > 2)
    return f"({written((a, f'{v}^{r.randint(2, 9)}'))}) ({written((b, f'{v}^{r.randint(2, 9)}'))})"

TEMPLATES = {"1": [t_mono]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    answer = expand_answer_of(prompt)
    need(answer != "0")
    return dict(prompt=prompt, answer=answer)

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("(3 y^5) (5 y^4)", "15 y^9")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
