"""Khan Algebra 2, Lesson 1-9: Multiply binomials by polynomials: area model,
from the old app's Alg2_01_09: as Lesson 1-7 (ka2_01_07), with a binomial for
the height (x^2 + 3, 2 x + 5) and a width of two or three terms; every
coefficient positive.
"""
from ... import gen
from ...gen import written
from . import courses
from ..khan_alg1.figures import PREAMBLE
from ..khan_alg1.polybank import expand_check, expand_answer_of
from .ka2_01_07 import width, c, typst, answer_typst, text, answer_text, height, edit_text, from_edit, \
    answer_edit_text, with_answer, initial_seen

NAME = FAMILY = "ka2_01_09"
FIXED = False
TITLE = "Lesson 1-9: Multiply binomials by polynomials: area model"
INSTRUCTIONS = "Express the area of the entire rectangle. Write it as a polynomial in standard form."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Binomial Times Polynomial",
         look="An area model whose height has two terms.",
         move="Find each box's area (a row for each term of the height), then add the boxes and combine like terms."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    h = written((c(r), r.choice(("x", "x^2"))), (c(r), ""))
    w = width(r)
    prompt = f"({h}) ({w})"
    return dict(height=h, width=w, prompt=prompt, answer=expand_answer_of(prompt))

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
