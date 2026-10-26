"""Khan Algebra 1, Lesson 13-10: Factoring quadratics with a common factor, from the old app's Alg1_13_10
(twelve generated slots).

a(x - r)(x - s), multiplied out: a is -7 to 7 (not -1 to 1), r and s -8 to 8,
not 0, r != -s. The key takes out the common factor, with the leading
term's sign: -2 (x - 3) (x + 5).

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "2 x^2 + 4 x - 30"
    answer  "2 (x - 3) (x + 5)"
check() requires the answer to be the same polynomial, factored completely:
the content in front, every factor left irreducible over the integers.
"""
import math
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, signed_except, written
from ...check import to_sympy
from . import courses
from .polybank import factor_check, factor_answer_of, factor_edits

NAME = FAMILY = "ka1_13_10"
FIXED = False
TITLE = "Lesson 13-10: Factoring quadratics with a common factor"
INSTRUCTIONS = "Factor completely."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Common Factor First",
         look="A quadratic whose coefficients share a factor.",
         move="Take out the greatest common factor (negative if the leading coefficient is). Then factor the trinomial left inside."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t_common(r, v):                            # 2 x^2 + 4 x - 30
    a, s = signed(r, 2, 7), signed(r, 1, 8)
    t = signed_except(r, 1, 8, -s)
    x = sp.Symbol(v)
    return poly.expanded(a * (x - s) * (x - t))

TEMPLATES = {"1": [t_common]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    return dict(prompt=prompt, answer=factor_answer_of(prompt))

check = factor_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = factor_edits("2 x^2 + 4 x - 30", "2 (x - 3) (x + 5)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
