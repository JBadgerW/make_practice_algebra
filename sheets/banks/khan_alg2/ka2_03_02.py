"""Khan Algebra 2, Lesson 3-2: Greatest common factor of monomials, from the
old app's Alg2_03_02 (twelve of Khan's, without answers).

The greatest common factor of 3 x^4, 15 x^3, and 21 x^2: three monomials
in one letter, in any order, built on a common factor (Khan's 3 x^2, 5 b,
4 a, 7 y^4, 2) times numbers with no further common factor. Now and then a
constant term, as Khan's 6 a, 8 a^2, and 14.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "3 x^4, 15 x^3, 21 x^2"
    answer  "3 x^2"
check() computes the greatest common factor with sympy (gcd of the
coefficients, the least exponent) and requires the answer to be it.
"""
import math
from functools import reduce
import sympy as sp
from ... import gen
from ...gen import need
from ...check import to_sympy
from ...typmath import tx, text as plain
from . import courses
from .ka2_03_01 import mono

NAME = FAMILY = "ka2_03_02"
FIXED = False
TITLE = "Lesson 3-2: Greatest common factor of monomials"
INSTRUCTIONS = "What is the greatest common factor of the monomials?"
COURSES = courses(3)

TYPES = [
    dict(key="1", title="GCF of Three Monomials",
         look="Three monomials in the same letter.",
         move="The greatest common factor of the numbers, times the letter to the smallest power that appears."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS)
    g, e = r.randint(1, 12), r.randint(0, 4)
    ks = [r.randint(1, 9) for _ in range(3)]
    need(math.gcd(*ks) == 1 and len(set(ks)) > 1)
    constant = e == 0 and r.random() < 0.5                         # Khan's 6 a, 8 a^2, 14
    exps = [r.randint(e, e + 3) for _ in range(3)]
    if not constant:
        exps[r.randrange(3)] = e
    else:
        exps = [r.randint(1, 3), r.randint(1, 3), 0]
    need(any(x > 0 for x in exps) and g * max(ks) <= 99)
    terms = [mono(g * k, v, x) for k, x in zip(ks, exps)]
    need(len(set(terms)) == 3)
    prompt = ", ".join(terms)
    return dict(prompt=prompt, answer=gcf(prompt))

def gcf(prompt):
    return tx(reduce(sp.gcd, [to_sympy(t) for t in prompt.split(",")]))

def check(p):
    try:
        return "checked" if sp.expand(to_sympy(p["answer"]) - to_sympy(gcf(p["prompt"]))) == 0 else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(gcf, check, "3 x^4, 15 x^3, 21 x^2", "3 x^2")

def typst(p, gap="0.3em"):
    *first, last = [f"${t.strip()}$" for t in p["prompt"].split(",")]
    return ", ".join(first) + f", and {last}"

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    return plain(p["prompt"])

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.3

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
