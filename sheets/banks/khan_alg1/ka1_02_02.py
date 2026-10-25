"""Khan Algebra 1, Lesson 2-2: Equations with variables on both sides:
decimals & fractions, from the old app's Alg1_02_02 (twenty-one of Khan's,
answered; no. 18, 2 - 1/2 n = 3n + 16, had n = 4 where n = -4).

Khan's decimals are halves, quarters, and tenths (0.5s + 1 = 7 + 4.5s,
12.6 + 4m = 9.6 + 8m), with the numbers to at most one decimal place; its
fractions have denominators 2 to 5 and numerators to 20 (16 - 3p = 2/3 p + 5). Solutions are integers or short decimals
(-1.5, 0.75) with decimals, integers or simple fractions (-1/2, -1/4) with
fractions. The key writes the answer the way the prompt writes its numbers.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "0.5 s + 1 = 7 + 4.5 s"
    answer  "s = -1.5"
check() substitutes the answer into the prompt (decimals read exactly),
requires exactly one solution, and reads the answer's form: a decimal for
Type 1, a fraction in lowest terms for Type 2.
"""
from decimal import Decimal as D
from fractions import Fraction as F
from ... import gen, linear
from ...gen import need, written
from . import courses
from .numbers import decimal, short, fraction, simple

NAME = FAMILY = "ka1_02_02"
FIXED = False
TITLE = "Lesson 2-2: Equations with variables on both sides: decimals & fractions"
INSTRUCTIONS = "Solve each equation."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Decimals",
         look="Decimal coefficients or numbers, with the variable on both sides.",
         move="Gather the variable terms on one side and the numbers on the other, then divide. "
              "Or multiply both sides by 10 or 100 first to clear the decimals."),
    dict(key="2", title="Fractions",
         look="Fraction coefficients or numbers, with the variable on both sides.",
         move="Multiply both sides by the common denominator to clear the fractions. Then solve as before."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
FORM = {"1": "decimal", "2": "fraction"}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing: the solution, then a x + b = c x + d around it
# ------------------------------------------------------------------
def decimals(r):
    if r.random() < 0.6:
        x = D(r.choice((-1, 1)) * r.randint(1, 12))
    else:
        x = D(r.choice(("0.5", "1.5", "2.5", "0.25", "0.75", "1.25", "0.2", "0.6", "0.8"))) * r.choice((-1, 1))
    a = decimal(r, 9, ("0.5", "0.25"), whole=True)
    c = decimal(r, 9, ("0.5", "0.25"), whole=True)
    b = decimal(r, 20, ("0.5", "0.1", "1"), whole=True)
    need(a != c)
    d = (a - c) * x + b
    short(b, d, most=1)                           # Khan's numbers: 12.6, 7.2, 16.5
    need(d != 0 and abs(d) <= 20 and any(n != int(n) for n in (a, b, c, d)))
    return x, a, b, c, d

def fractions(r):
    x = F(r.choice((-1, 1)) * r.randint(1, 9)) if r.random() < 0.75 else fraction(r, 3, (2, 4))
    a = fraction(r, 3, whole=True)
    c = fraction(r, 3, whole=True) if a.denominator != 1 else fraction(r, 3)
    need(a != c)
    b = F(r.choice((-1, 1)) * r.randint(1, 16)) if r.random() < 0.6 else fraction(r, 9, (a.denominator,), whole=True)
    d = (a - c) * x + b
    simple(d)
    need(d != 0 and abs(d) <= 20 and all(abs(n.numerator) <= 20 for n in (a, b, c, d)))
    return x, a, b, c, d

def orders(r, v, kind):
    x, a, b, c, d = (decimals if kind == "1" else fractions)(r)
    return [written((a, v), (b, "")) + " = " + written((c, v), (d, "")),       # 0.5s + 1 = 4.5s + 7
            written((b, ""), (a, v)) + " = " + written((c, v), (d, "")),       # 16 - 3p = 2/3 p + 5
            written((a, v), (b, "")) + " = " + written((d, ""), (c, v)),       # 0.5s + 1 = 7 + 4.5s
            written((b, ""), (a, v)) + " = " + written((d, ""), (c, v))]       # 2 + 1.25f = 10 - 2.75f

TEMPLATES = {k: [lambda r, v, k=k, i=i: orders(r, v, k)[i] for i in range(4)] for k in KEYS}

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS)
    prompt = TEMPLATES[entry][tpl](r, v)
    return dict(prompt=prompt, answer=linear.answer_of(prompt, decimals=entry == "1"))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    try:
        return "checked" if linear.solves(p["prompt"], p["answer"], FORM[p["type"]]) else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    lambda t: linear.answer_of(t, decimals="." in t), check, "0.5 s + 1 = 7 + 4.5 s", "s = -1.5")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
