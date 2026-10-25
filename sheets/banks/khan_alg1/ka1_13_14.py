"""Khan Algebra 1, Lesson 13-14: Perfect squares intro, from the old app's
Alg1_13_14 (sixteen slots, two templates).

x^2 + 2 r x + r^2 = (x + r)^2, r -12 to 12, not 0, sometimes written
constant first. Type 2 is Khan's square: its area, and the length of one
side.

A problem: as Lesson 13-9's (ka1_13_09); Type 2's shape is "square".
"""
import sympy as sp
from ... import gen, poly
from ...gen import signed, written
from . import courses
from .figures import PREAMBLE
from .polybank import factor_check, factor_answer_of, side_check
from .ka1_13_09 import initial_seen, typst, answer_typst, text, answer_text, height, edit_text, answer_edit_text, \
    with_answer, from_edit

NAME = FAMILY = "ka1_13_14"
FIXED = False
TITLE = "Lesson 13-14: Perfect squares intro"
INSTRUCTIONS = ""
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Factor a Perfect Square", instructions="Factor as the product of two binomials.",
         look="x^2, a perfect square, and a middle term twice the product of their roots.",
         move="x^2 + 2 r x + r^2 = (x + r)^2. Find r from the constant, and check the middle term."),
    dict(key="2", title="The Side of a Square", instructions="Answer each question.",
         look="A square whose area is a perfect square trinomial.",
         move="Factor the area as (x + r)^2. Each side is x + r.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS) if entry == "1" else "x"
    k = signed(r, 1, 12)
    first = r.random() < 0.6
    area = written((1, f"{v}^2"), (2 * k, v), (k * k, "")) if first else written((k * k, ""), (2 * k, v), (1, f"{v}^2"))
    if entry == "1":
        return dict(prompt=area, answer=factor_answer_of(area))
    return dict(prompt=area, shape="square", area=area, answer=written((1, v), (k, "")))

def check(p):
    return factor_check(p) if p["type"] == "1" else side_check(p)

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
