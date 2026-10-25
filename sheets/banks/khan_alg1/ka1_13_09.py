"""Khan Algebra 1, Lesson 13-9: Factoring quadratics intro, from the old
app's Alg1_13_09 (eighteen generated slots).

x^2 + b x + c = (x - r)(x - s), r and s -12 to 12, not 0, r != s, and r != -s (so
there is an x term). Type 2 is Khan's rectangle: its area x^2 + b x + c
and one side x - s; the other side is x - r.

A problem: dict(type, prompt, answer, source); Type 2 adds shape, area,
side, and ask ("length" or "width"). Typst math.
    Type 1  prompt "x^2 + 2 x - 15", answer "(x - 3) (x + 5)"
    Type 2  area "x^2 + 2 x - 15", side "x + 5", ask "length", answer "x - 3"
check(): Type 1, the same polynomial factored completely; Type 2, the
answer times the given side is the area.
"""
from ... import gen, poly
from ...gen import need, signed, signed_except
from ...check import to_sympy
from . import courses
from .figures import PREAMBLE
from .polybank import factor_check, factor_answer_of, factor_edits, side_check, side_typst, side_text

NAME = FAMILY = "ka1_13_09"
FIXED = False
TITLE = "Lesson 13-9: Factoring quadratics intro"
INSTRUCTIONS = ""
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Factor the Trinomial", instructions="Factor as the product of two binomials.",
         look="A quadratic that starts with x^2.",
         move="Find two numbers that multiply to the constant and add to the x coefficient. "
              "They are the numbers in the two binomials."),
    dict(key="2", title="A Missing Side", instructions="Answer each question.",
         look="A rectangle's area, a quadratic, and one of its sides.",
         move="Factor the area. One factor is the side you know; the other is the side you want.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"], p.get("side"))

def roots(r):
    a = signed(r, 1, 12)
    return a, signed_except(r, 1, 12, -a, a)       # an x term; not a perfect square (13-14)

def draw(entry, r, tpl):
    x = to_sympy(r.choice(gen.LETTERS)) if entry == "1" else to_sympy("x")
    a, b = roots(r)
    area = poly.expanded((x - a) * (x - b))
    if entry == "1":
        return dict(prompt=area, answer=factor_answer_of(area))
    ask = r.choice(("length", "width"))
    return dict(prompt=area, shape="rectangle", area=area, side=poly.expanded(x - b), ask=ask,
                answer=poly.expanded(x - a))

def check(p):
    return factor_check(p) if p["type"] == "1" else side_check(p)

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

_typst, _answer_typst, _text, _answer_text, _height = gen.shown()

def typst(p, gap="0.3em"):
    return _typst(p, gap) if p["type"] == "1" else side_typst(p)

def answer_typst(p):
    return _answer_typst(p)

def text(p):
    return _text(p) if p["type"] == "1" else side_text(p)

def answer_text(p):
    return _answer_text(p)

def height(p):
    return 0.3 if p["type"] == "1" else 1.4

edit_text, _from_edit, answer_edit_text, with_answer = factor_edits("x^2 + 2 x - 15", "(x - 3) (x + 5)")

def from_edit(t, old):
    if old["type"] == "1":
        return _from_edit(t, old)
    raise ValueError("edit the answer instead; reroll for a new rectangle")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
