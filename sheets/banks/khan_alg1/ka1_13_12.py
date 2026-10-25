"""Khan Algebra 1, Lesson 13-12: Difference of squares intro, from the old
app's Alg1_13_12 (fourteen generated slots; no. 8 asked for the width but
labeled its blank "Length =").

x^2 - r^2 = (x - r)(x + r), r 1 to 12, or constant first: r^2 - x^2 =
(r - x)(r + x). Type 2 is Khan's rectangle with that area and one side.

A problem: as Lesson 13-9's (ka1_13_09).
"""
import sympy as sp
from ... import gen
from ...gen import written
from . import courses
from .figures import PREAMBLE
from .polybank import factor_check, factor_answer_of, side_check
from .ka1_13_09 import initial_seen, typst, answer_typst, text, answer_text, height, edit_text, answer_edit_text, \
    with_answer, from_edit

NAME = FAMILY = "ka1_13_12"
FIXED = False
TITLE = "Lesson 13-12: Difference of squares intro"
INSTRUCTIONS = ""
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Factor a Difference of Squares", instructions="Factor as the product of two binomials.",
         look="x^2 minus a perfect square, or a perfect square minus x^2.",
         move="a^2 - b^2 = (a - b)(a + b). The middle terms cancel when you multiply back."),
    dict(key="2", title="A Missing Side", instructions="Answer each question.",
         look="A rectangle whose area is a difference of squares, and one of its sides.",
         move="Factor the area. One factor is the side you know; the other is the side you want.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def seen_key(p):
    return (NAME, p["type"], p["prompt"], p.get("side"))

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS) if entry == "1" else "x"
    k, first = r.randint(1, 12), r.random() < 0.6
    area = written((1, f"{v}^2"), (-k * k, "")) if first else written((k * k, ""), (-1, f"{v}^2"))
    if entry == "1":
        return dict(prompt=area, answer=factor_answer_of(area))
    s = r.choice((-1, 1))
    side, other = (written((1, v), (s * k, "")), written((1, v), (-s * k, ""))) if first else \
        (written((k, ""), (s, v)), written((k, ""), (-s, v)))
    return dict(prompt=area, shape="rectangle", area=area, side=side, ask=r.choice(("length", "width")), answer=other)

def check(p):
    return factor_check(p) if p["type"] == "1" else side_check(p)

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
