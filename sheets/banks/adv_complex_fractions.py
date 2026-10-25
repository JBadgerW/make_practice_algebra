"""Complex fractions (Advanced Math), from the old app's set AdvMath_16_01
(16_A_1, 16_A_2, 24_19) and Test 5, no. 10.

The key's answer is one fraction in lowest terms, its numerator and
denominator multiplied out, with no fraction inside it:
(a d + b c)/(a d - b c). The fractions in a prompt are in lowest terms
(the old 16_A_1 printed 4/6 but solved 2/3).

check() reads the prompt and the answer back with to_sympy, compares their
values at random points, and reads the answer's form from its text.

A problem: dict(type, prompt, answer, source), both in Typst math.
    prompt  "(3/x + 2/y)/(1/x - 4/y)"
    answer  "(2 x + 3 y)/(y - 4 x)"   (the order of its terms is the key's)
"""
import math
import sympy as sp
from .. import gen
from ..gen import need, signed
from ..check import to_sympy, same_value, simplest_form, denominators
from ..typmath import single, fr

NAME = FAMILY = "adv_complex_fractions"
FIXED = False
TITLE = "Complex Fractions"
INSTRUCTIONS = "Simplify."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="A Sum over a Sum",
         look="Two fractions added or subtracted on top, and two on the bottom.",
         move="Multiply the top and the bottom by the least common denominator of all four fractions. "
              "Then simplify."),
    dict(key="2", title="Nested Fractions",
         look="A fraction inside a fraction inside a fraction.",
         move="Start with the innermost fraction: rewrite the expression it sits in as one fraction. "
              "Work outward, one level at a time.", space="1.5in"),
    dict(key="3", title="Fractions with Powers",
         look="Fractions whose denominators have powers, like 1/x^2 or 1/(x y).",
         move="Multiply the top and the bottom by the least common denominator, using the highest power of "
              "each letter. Factor and cancel if you can.", space="1.5in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
BIG, TERMS = 300, 6                   # the answer's numbers, and its terms on top and on bottom

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def answer_of(prompt):
    e = sp.cancel(sp.together(to_sympy(prompt)))
    need(e != 0 and not e.has(sp.zoo, sp.nan))
    return single(e)

def sign(r):
    return r.choice((" + ", " - "))

# ------------------------------------------------------------------
# Type 1 (16_A_1): each place is a letter or a number
# ------------------------------------------------------------------
def frac(top, bottom):
    """top/bottom, reduced when both are numbers (and never a whole number)."""
    if isinstance(top, int) and isinstance(bottom, int):
        top, bottom = gen.reduced(top, bottom)
        need(bottom != 1)
    return fr(str(top), str(bottom))

def t1_mixed(r):                              # 16_A_1
    ls = iter(gen.letters(r, 8))
    slot = [(r.randint(1, 9) if r.random() < 0.5 else next(ls)) for _ in range(4)]
    under = [(r.randint(2, 9) if r.random() < 0.5 else next(ls)) for _ in range(4)]
    need(any(isinstance(s, str) for s in slot + under))
    a, c, e, g = slot
    b, d, f, h = under
    return fr(frac(a, b) + sign(r) + frac(c, d), frac(e, f) + sign(r) + frac(g, h))

def t1_numbers_over_letters(r):
    x, y = gen.letters(r, 2)
    a, b, c, d = (r.randint(1, 9) for _ in range(4))
    return fr(f"{a}/{x}{sign(r)}{b}/{y}", f"{c}/{x}{sign(r)}{d}/{y}")

def t1_letters_over_numbers(r):
    x, y = gen.letters(r, 2)
    a, b, c, d = (r.randint(2, 9) for _ in range(4))
    return fr(f"{x}/{a}{sign(r)}{y}/{b}", f"{x}/{c}{sign(r)}{y}/{d}")

# ------------------------------------------------------------------
# Type 2 (16_A_2, Test 5 no. 10)
# ------------------------------------------------------------------
def t2_three_letters(r):                      # 16_A_2
    c, t, z = gen.letters(r, 3)
    k1, k2, k3 = r.sample((1, 2, 3, 4, 5), 3)
    k2c = c if k2 == 1 else f"{k2} {c}"
    return fr(str(k1), f"{k2c} + {fr(t, f'1 + {fr(str(k3), z)}')}")

def t2_one_letter(r):
    x, = gen.letters(r, 1)
    a, b, c = (r.randint(1, 6) for _ in range(3))
    return fr(str(a), f"1{sign(r)}{fr(str(b), f'1{sign(r)}{fr(str(c), x)}')}")

def t2_repeated_letter(r):                    # Test 5, no. 10: m/(m/(m/y + x) + m)
    m, x, y = r.sample(gen.LETTERS, 3)
    return fr(m, f"{fr(m, f'{fr(m, y)} + {x}')} + {m}")

# ------------------------------------------------------------------
# Type 3 (24_19, smaller)
# ------------------------------------------------------------------
def t3_powers(r):
    x, y = gen.letters(r, 2)
    a, b, c, d = (r.randint(1, 9) for _ in range(4))
    return fr(f"{a}/{x}^2{sign(r)}{b}/({x} {y})", f"{c}/{y}^2{sign(r)}{d}/{x}")

def t3_difference_of_squares(r):
    x, y = gen.letters(r, 2)
    a, b = r.randint(1, 5), r.randint(1, 5)
    return fr(f"{a * a}/{x}^2 - {b * b}/{y}^2", f"{a}/{x}{sign(r)}{b}/{y}")

def t3_four_letters(r):                       # 24_19
    a, m, x, y = gen.letters(r, 4)
    c1, c2, c3, c4 = (r.randint(1, 9) for _ in range(4))
    e1, e2 = r.randint(2, 3), r.randint(2, 3)
    k1, k2 = (f"{c} " if c != 1 else "" for c in (c1, c2))
    top = f"{k1}{a}/({x}^{e1} {y}){sign(r)}{k2}{m}/({x} {y}^{e2})"
    return fr(top, f"{c3}/{x}^{e1}{sign(r)}{c4}/{y}^{e2}")

TEMPLATES = {
    "1": [t1_mixed, t1_numbers_over_letters, t1_letters_over_numbers],
    "2": [t2_three_letters, t2_one_letter, t2_repeated_letter],
    "3": [t3_powers, t3_difference_of_squares, t3_four_letters],
}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r)
    answer = answer_of(prompt)
    e = to_sympy(answer)
    need(e.free_symbols and simplest_form(answer) and len(denominators(answer)) <= 1)
    n, d = sp.fraction(sp.together(e))
    need(len(sp.Add.make_args(sp.expand(n))) <= TERMS and len(sp.Add.make_args(sp.expand(d))) <= TERMS)
    need(all(abs(a) <= BIG for a in sp.preorder_traversal(e) if a.is_Rational))
    return dict(prompt=prompt, answer=answer)

def check(p):
    try:
        a = p["answer"]
        ok = same_value(p["prompt"], a) and simplest_form(a) and len(denominators(a)) <= 1
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "(3/x + 2/y)/(1/x - 4/y)", "(2 x + 3 y)/(y - 4 x)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
