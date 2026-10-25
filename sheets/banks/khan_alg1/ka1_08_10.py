"""Khan Algebra 1, Lesson 8-10: Determine the domain of functions, from the old
app's Alg1_08_10 (twelve of Khan's, without answers; the same functions as
8-9).

What is the domain of f? Khan's five choices: all real values of x such
that x != a, x >= a, x != b, x <= b, and all real values of x, where a and b
are the function's special number and a decoy (the top's zero, or 0). The
functions are 8-9's (khan_alg1/domains.py). One type, the kinds mixed.

A problem: dict(type, prompt, choices, answer, source).
    prompt   "f(x) = (x - 3)/(x + 2)"
    choices  conditions, "x != -2", "x >= -2", ..., or "all"
    answer   "A"
check() computes the domain with sympy and compares it with every choice's.
"""
import sympy as sp
from ... import gen
from ...gen import need
from ...linear import exact
from ...typmath import display, dfrac, text as plain, tx
from ..adv_functions import domain_read
from . import courses
from .domains import function, domain

NAME = FAMILY = "ka1_08_10"
FIXED = False
TITLE = "Lesson 8-10: Determine the domain of functions"
INSTRUCTIONS = "What is the domain of each function?"
COURSES = courses(8)
ALL = "all"

TYPES = [
    dict(key="1", title="Domains",
         look="A function: a fraction, a square root, or a polynomial.",
         move="A denominator can't be 0; the inside of a square root can't be negative; anything else is every number."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def body_of(prompt):
    return prompt.partition("=")[2].strip()

def as_set(choice):
    return sp.S.Reals if choice == ALL else domain_read(choice)

def draw(entry, r, tpl):
    body, s, kind = function(r)
    prompt = f"{r.choice('fgh')}(x) = {body}"
    zero = sp.solve(exact(body.split("/")[0]) if "/" in body else exact(body), sp.Symbol("x"))
    decoy = next((z for z in zero if z != s and z.is_real), sp.Integer(0) if s != 0 else sp.Integer(1))
    a, b = tx(s), tx(decoy)
    flip = r.random() < 0.5 if kind == "polynomial" else kind == "root" and domain(body).sup == s
    conditions = [f"x != {a}", f"x {'<=' if flip else '>='} {a}", f"x != {b}", f"x {'>=' if flip else '<='} {b}"]
    r.shuffle(conditions)
    choices = conditions + [ALL]                    # "All real values of x" last, as Khan's
    right = [c for c in choices if as_set(c) == domain(body)]
    need(len(right) == 1)
    return dict(prompt=prompt, choices=choices, answer=gen.ABC[choices.index(right[0])])

def check(p):
    try:
        d = domain(body_of(p["prompt"]))
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if as_set(c) == d]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def words(c):
    if c == ALL:
        return "All real values of $x$"
    return f"All real values of $x$ such that ${c}$"

def typst(p, gap="0.3em"):
    return f"{display(dfrac(p['prompt']))} \\\n    {gen.choices_typst([words(c) for c in p['choices']])}"

def answer_typst(p):
    a = gen.letters_of(p["answer"])[0]
    return f"{a}. {words(p['choices'][gen.ABC.index(a)])}"

def text(p):
    return plain(p["prompt"]) + "      " + gen.choices_text(p["choices"], lambda c: plain(c.replace("!=", "≠")))

def answer_text(p):
    a = gen.letters_of(p["answer"])[0]
    return f"{a}. {plain(p['choices'][gen.ABC.index(a)].replace('!=', '≠'))}"

def height(p):
    return 1.4

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new function; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
