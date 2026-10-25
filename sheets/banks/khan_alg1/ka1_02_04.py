"""Khan Algebra 1, Lesson 2-4: Equations with parentheses: decimals &
fractions, from the old app's Alg1_02_04 (twenty of Khan's, answered, every
answer right).

Khan's products are a decimal or fraction times whole numbers
(0.75(8b + 4), 1/2(12f - 2)) or a whole number times decimals or fractions
(10(0.4 + 0.5g), 4(-3 - 3/4 t)), sometimes with another number beside them
(3 + 0.5(4a + 8) = 9 - 2a). The other numbers are whole, or have one
decimal place, or are fractions like 1/2. Solutions are mostly integers; some are short
decimals (2.5, 0.25) or simple fractions (-4/3). The key writes the
answer the way the prompt writes its numbers.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "0.75 (8 b + 4) - 1 = 4 b + 14"
    answer  "b = 6"
check() substitutes the answer into the prompt (decimals read exactly),
requires exactly one solution, and reads the answer's form.
"""
from decimal import Decimal as D
from fractions import Fraction as F
from ... import gen, linear
from ...gen import need, signed, written
from . import courses
from .numbers import decimal, short, fraction, simple

NAME = FAMILY = "ka1_02_04"
FIXED = False
TITLE = "Lesson 2-4: Equations with parentheses: decimals & fractions"
INSTRUCTIONS = "Solve each equation."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Decimals",
         look="A product to distribute, with decimals outside or inside the parentheses.",
         move="Distribute (multiply the decimals carefully), combine like terms, and solve."),
    dict(key="2", title="Fractions",
         look="A product to distribute, with fractions outside or inside the parentheses.",
         move="Distribute: the whole number often cancels the denominators. Combine like terms and solve."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
FORM = {"1": "decimal", "2": "fraction"}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing: the solution, a product, and the side that makes x the solution
# ------------------------------------------------------------------
def solution(r, kind):
    if r.random() < 0.75:
        return gen.except_(r, -9, 12, 0)
    if kind == "1":
        return D(r.choice(("0.5", "2.5", "0.25", "0.8", "1.5"))) * r.choice((-1, 1))
    return fraction(r, 2, (2, 3, 4))

def product(r, v, x, kind, outside):
    """(text, value at x, coefficient of v): a decimal or fraction times whole numbers
    (outside), or a whole number times decimals or fractions."""
    if outside:
        m = D(r.choice(("0.2", "0.25", "0.5", "0.75", "1.5", "2.5"))) * r.choice((-1, 1)) if kind == "1" \
            else fraction(r, 1, (2, 3, 4))
        b, c = signed(r, 1, 10), signed(r, 1, 12)
    else:
        m = signed(r, 2, 12)
        if kind == "1":
            b, c = decimal(r, 2, ("0.5", "0.25", "0.4"), whole=True), decimal(r, 3, ("0.5", "0.25", "0.2"), whole=True)
            need(b != int(b) or c != int(c))
        else:
            q = r.choice([d for d in (2, 3, 4, 5, 7) if abs(m) % d == 0] or [2])   # 10(3/5 p - 2), 7(2/7 - 3/7 h)
            b, c = fraction(r, 2, (q,)), F(signed(r, 1, 6)) if r.random() < 0.5 else fraction(r, 2, (q,))
    inner = written((b, v), (c, "")) if r.random() < 0.6 else written((c, ""), (b, v))
    return written((m, f"({inner})")), m * (b * x + c), m * b

def other(r, v, x, kind, value, avoid):
    """k v + e whose value at x is `value`, k != avoid; e short and small."""
    k = signed(r, 1, 12) if r.random() < 0.6 or kind == "2" else decimal(r, 3, ("0.5", "0.25"))
    need(k != avoid)
    e = value - k * x
    if kind == "1":
        short(e, most=1)                          # Khan's: 8, -16, 7, 2, 14
    else:
        need(e.denominator == 1 or (e.denominator <= 4 and abs(e.numerator) <= 12))
    need(abs(e) <= 30)
    return written((k, v), (e, "")) if r.random() < 0.6 else written((e, ""), (k, v))

def t_product(r, v, kind, outside):           # 0.2(10 - 5c) = 5c - 16; 10(0.4 + 0.5g) = 4g
    x = solution(r, kind)
    text, val, coef = product(r, v, x, kind, outside)
    return f"{text} = {other(r, v, x, kind, val, coef)}"

def t_product_right(r, v, kind, outside):     # 4 + 2p = 10(3/5 p - 2)
    left, _, right = t_product(r, v, kind, outside).partition(" = ")
    return f"{right} = {left}"

def t_number_beside(r, v, kind, outside):     # 3 + 0.5(4a + 8) = 9 - 2a; 12(2/3 g - 1) + 11
    x, q = solution(r, kind), signed(r, 1, 12)
    text, val, coef = product(r, v, x, kind, outside)
    left = f"{q} + {text}".replace("+ -", "- ") if r.random() < 0.5 else written((1, text), (q, ""))
    return f"{left} = {other(r, v, x, kind, val + q, coef)}"

TEMPLATES = {k: [lambda r, v, k=k, t=t, o=o: t(r, v, k, o)
                 for t in (t_product, t_product_right, t_number_beside) for o in (True, False)] for k in KEYS}

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS)
    prompt = TEMPLATES[entry][tpl](r, v)
    answer = linear.answer_of(prompt, decimals=entry == "1")
    need(len(answer) <= 12)                       # x = -4/3, x = 0.25: no long decimals
    return dict(prompt=prompt, answer=answer)

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
    lambda t: linear.answer_of(t, decimals="." in t), check, "0.75 (8 b + 4) - 1 = 4 b + 14", "b = 6")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
