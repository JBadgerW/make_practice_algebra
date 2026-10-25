"""Khan Algebra 1, Lesson 8-22: Finding inverses of linear functions, from
the old app's Alg1_08_22 (twelve of Khan's, without answers).

Khan's functions: a x + b (f(x) = 3 x - 2, f(x) = -6 x - 7), a fraction times
x plus a number (g(x) = -2/3 x - 5), and a number times a sum (g(x) = 5 (x - 2),
f(x) = -1/2 (x + 3)). The key writes the inverse in slope-intercept form,
fractions as written: f^(-1)(x) = 1/3 x + 2/3.

A problem: dict(type, prompt, answer, source).
    prompt  "f(x) = 3 x - 2"
    answer  "f^(-1)(x) = 1/3 x + 2/3"
check() composes the function with the answer: f(answer) must be x.
"""
import re
from fractions import Fraction as F
import sympy as sp
from ... import gen
from ...gen import need, signed, signed_except, written
from ...linear import exact
from ...typmath import display, dfrac, text as plain
from .ka1_08_06 import slope_intercept
from . import courses

NAME = FAMILY = "ka1_08_22"
FIXED = False
TITLE = "Lesson 8-22: Finding inverses of linear functions"
INSTRUCTIONS = "Find the inverse of each function."
COURSES = courses(8)
X = sp.Symbol("x")
DEF = re.compile(r"\s*(\w)\(x\)\s*=\s*(.+)")

TYPES = [
    dict(key="1", title="Whole-Number Coefficients",
         look="f(x) = a x + b.",
         move="Write y = a x + b, swap x and y, and solve for y: subtract b, then divide by a."),
    dict(key="2", title="A Fraction Coefficient",
         look="f(x) = (p/q) x + b.",
         move="Swap x and y, subtract b, then multiply by the reciprocal q/p."),
    dict(key="3", title="A Number Times a Sum",
         look="f(x) = k (x + c).",
         move="Swap x and y, divide by k, then subtract c."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t1(r):                                    # 3 x - 2
    return written((signed_except(r, 1, 9, 1, -1), "x"), (signed(r, 1, 12), ""))

def t2(r):                                    # -2/3 x - 5
    q = r.randint(2, 5)
    p = gen.except_(r, 1, 3 * q, *range(0, 3 * q + 1, q))
    return written((F(p, q) * r.choice((-1, 1)), "x"), (signed(r, 1, 12), ""))

def t3(r):                                    # 5 (x - 2), -1/2 (x + 3)
    k = signed_except(r, 1, 6, 1, -1) if r.random() < 0.7 else F(r.choice((-1, 1)) * r.randint(1, 3), r.choice((2, 3, 4)))
    need(abs(k) != 1)
    return written((k, f"({written((1, 'x'), (signed(r, 1, 12), ''))})"))

TEMPLATES = {"1": [t1], "2": [t2], "3": [t3]}

def parts(prompt):
    f, body = DEF.match(prompt).groups()
    return f, exact(body)

def answer_of(prompt):
    f, e = parts(prompt)
    y = sp.Symbol("y")
    inv = sp.solve(e.subs(X, y) - X, y)
    if len(inv) != 1:
        raise ValueError("not one-to-one")
    return f"{f}^(-1)(x) = {slope_intercept(inv[0], 'x')}"

def draw(entry, r, tpl):
    prompt = f"{r.choice('fgh')}(x) = {TEMPLATES[entry][tpl](r)}"
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        f, e = parts(p["prompt"])
        lhs, _, rhs = p["answer"].partition("=")
        if lhs.replace(" ", "") != f"{f}^(-1)(x)":
            return "failed"
        return "checked" if sp.simplify(e.subs(X, exact(rhs)) - X) == 0 else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

def typst(p, gap="0.3em"):
    return display(dfrac(p["prompt"]))

def answer_typst(p):
    return display(dfrac(p["answer"]))

def text(p):
    return plain(p["prompt"])

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.5

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "f(x) = 3 x - 2", "f^(-1)(x) = 1/3 x + 2/3")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
