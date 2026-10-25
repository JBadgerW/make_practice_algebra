"""Khan Algebra 1, Lesson 11-5: Roots of decimals & fractions, from the old
app's Alg1_11_05 (twelve generated slots).

sqrt(49/144) = 7/12 and sqrt(0.36) = 0.6. Fractions: the root's numerator
and denominator 2 to 15, in lowest terms. Decimals: the root 0.1 to 2.5
in tenths, not 1 or 2.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "sqrt(49/144)", "sqrt(0.36)"
    answer  "7/12", "0.6"
check() compares the values exactly and reads the answer's form: a
fraction in lowest terms, or a decimal.
"""
import math, re
import sympy as sp
from ... import gen, linear
from ...gen import need
from . import courses

NAME = FAMILY = "ka1_11_05"
FIXED = False
TITLE = "Lesson 11-5: Roots of decimals & fractions"
INSTRUCTIONS = "Find each square root."
COURSES = courses(11)

TYPES = [
    dict(key="1", title="Fractions",
         look="The square root of a fraction whose top and bottom are perfect squares.",
         move="Take the square root of the top and of the bottom."),
    dict(key="2", title="Decimals",
         look="The square root of a decimal.",
         move="Think of the decimal as a fraction over 100 (0.36 = 36/100), or ask which tenth, times itself, makes it."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
FORM = {"1": re.compile(r"(\d+)/(\d+)"), "2": re.compile(r"\d*\.\d+")}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    if entry == "1":
        a, b = r.sample(range(2, 16), 2)
        need(math.gcd(a, b) == 1)
        return dict(prompt=f"sqrt({a * a}/{b * b})", answer=f"{a}/{b}")
    t = gen.except_(r, 1, 25, 10, 20)                # a tenth: 0.1 to 2.5, not 1 or 2
    root = linear.as_decimal(sp.Rational(t, 10))
    return dict(prompt=f"sqrt({linear.as_decimal(sp.Rational(t * t, 100))})", answer=root)

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: 1)

def check(p):
    try:
        a = p["answer"].replace(" ", "")
        m = FORM[p["type"]].fullmatch(a)
        form = m and (p["type"] == "2" or math.gcd(int(m.group(1)), int(m.group(2))) == 1)
        return "checked" if form and linear.exact(p["prompt"]) == linear.exact(a) else "failed"
    except Exception:
        return "unchecked"

def answer_of(prompt):
    v = linear.exact(prompt)
    if not v.is_Rational:
        raise ValueError("not a perfect square")
    return linear.as_decimal(v) if "." in prompt else str(v)

typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "sqrt(49/144)", "7/12")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=20)    # 24 decimals
