"""Khan Algebra 1, Lesson 13-3: Multiply binomials: area model, from the
old app's Alg1_13_03 (twelve generated slots).

An area model of (x + c)(x + f), c and f 1 to 9: the side lengths are its
labels; the area is the product, expanded.

A problem: dict(type, height, width, prompt, answer, source), as 13-2's
(ka1_13_02), with binomials for both sides.
"""
from ... import gen
from ...gen import written
from . import courses
from .figures import PREAMBLE, area_model
from .polybank import expand_check, expand_answer_of, term_list
from .ka1_13_02 import answer_typst, text, answer_text, height, edit_text, from_edit, answer_edit_text, with_answer

NAME = FAMILY = "ka1_13_03"
FIXED = False
TITLE = "Lesson 13-3: Multiply binomials: area model"
INSTRUCTIONS = "Express the area of the entire rectangle. Write it as a polynomial in standard form."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Two Binomials",
         look="An area model with x and a number on each side.",
         move="Find the area of each of the four boxes, then add them and combine the two x terms."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    w, h = written((1, "x"), (r.randint(1, 9), "")), written((1, "x"), (r.randint(1, 9), ""))
    prompt = f"({h}) ({w})"
    return dict(height=h, width=w, prompt=prompt, answer=expand_answer_of(prompt))

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    return area_model(term_list(p["width"]), term_list(p["height"]))

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=20)    # 81 in all
