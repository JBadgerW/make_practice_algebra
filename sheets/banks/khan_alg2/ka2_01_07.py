"""Khan Algebra 2, Lessons 1-7 and 1-9: area models of a monomial (1-7) or a
binomial (1-9) times a polynomial, from the old app's Alg2_01_07 and Alg2_01_09
(generated, one template each; 1-9 is its own bank, ka2_01_09, built from
this one).

The rectangle's height is d x^2 or d x (1-7) or a binomial (1-9), and its
width a polynomial of two or three terms; the area model shows a box for
each pair of terms (khan_alg1/figures.py). Every coefficient is positive:
the boxes are lengths. The answer is the area, expanded in standard form.

A problem: dict(type, height, width, prompt, answer, source), as Khan
Algebra 1's 13-2 (ka1_13_02), whose showing and editing these use.
check() requires the answer to be the product in standard form.
"""
from ... import gen
from ...gen import need, written
from . import courses
from ..khan_alg1.figures import PREAMBLE
from ..khan_alg1.polybank import expand_check, expand_answer_of
from ..khan_alg1.ka1_13_02 import typst, answer_typst, text, answer_text, height, edit_text, from_edit, \
    answer_edit_text, with_answer

NAME = FAMILY = "ka2_01_07"
FIXED = False
TITLE = "Lesson 1-7: Multiply monomials by polynomials: area model"
INSTRUCTIONS = "Express the area of the entire rectangle. Write it as a polynomial in standard form."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Monomial Times Polynomial",
         look="An area model whose height is one term, like 3 x^2.",
         move="Multiply the height by each term of the width (one box each): multiply coefficients, add exponents. Add the boxes."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def c(r):
    return r.randint(1, 6)

def width(r, top=2):
    terms = [(c(r), f"x^{d}" if d > 1 else "x" if d == 1 else "") for d in sorted(r.sample(range(0, top + 1), r.randint(2, 3)), reverse=True)]
    return written(*terms)

def draw(entry, r, tpl):
    h = written((c(r), r.choice(("x", "x^2"))))
    w = width(r)
    prompt = f"{h} ({w})"
    return dict(height=h, width=w, prompt=prompt, answer=expand_answer_of(prompt))

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
