"""Khan Algebra 1, Lesson 11-1: Multiply & divide powers (integer exponents),
from the old app's Alg1_11_01 (twenty generated slots).

Rewrite (7^(-3))(7^5), 7^(-3) · 7^5, or 7^9/7^4 in the form b^n. Bases are
2 to 9 or a letter; exponents are -12 to 12, not -1 to 1. The answer is
never b^0 or b^1 (the old no. 6 could give b^0: it excluded no exponent).

A problem: dict(type, prompt, answer, source), in Typst math; a product
with a dot is stored with *, shown as a dot.
    prompt  "7^(-3) * 7^5"
    answer  "7^2"
check() compares the values and reads the answer's form: the prompt's
base to one integer power.
"""
import re
import sympy as sp
from ... import gen
from ...gen import need, signed
from ...check import same_value, to_sympy
from ...typmath import display, dfrac, fr, text as plain
from ..adv_exponents import pw
from . import courses

NAME = FAMILY = "ka1_11_01"
FIXED = False
TITLE = "Lesson 11-1: Multiply & divide powers (integer exponents)"
INSTRUCTIONS = "Rewrite each expression in the form b^n."
COURSES = courses(11)

TYPES = [
    dict(key="1", title="Multiply Powers",
         look="Two powers of the same base multiplied.",
         move="Keep the base and add the exponents: b^m · b^n = b^(m + n)."),
    dict(key="2", title="Divide Powers",
         look="A power over a power of the same base.",
         move="Keep the base and subtract the exponents: b^m / b^n = b^(m - n)."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def base(r):
    return str(r.randint(2, 9)) if r.random() < 0.6 else r.choice(gen.LETTERS)

def exponents(r):
    return signed(r, 2, 12), signed(r, 2, 12)

def t1_parentheses(r, b):                     # (7^(-3))(7^5)
    m, n = exponents(r)
    return f"({pw(b, m)}) ({pw(b, n)})", m + n

def t1_dot(r, b):                             # 7^(-3) · 7^5
    m, n = exponents(r)
    return f"{pw(b, m)} * {pw(b, n)}", m + n

def t2_quotient(r, b):                        # 7^9/7^4
    m, n = exponents(r)
    return fr(pw(b, m), pw(b, n)), m - n

TEMPLATES = {"1": [t1_parentheses, t1_dot], "2": [t2_quotient]}

def draw(entry, r, tpl):
    b = base(r)
    prompt, n = TEMPLATES[entry][tpl](r, b)
    need(n not in (0, 1))
    return dict(prompt=prompt, answer=pw(b, n))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

FORM = re.compile(r"(\w+)\^(-?\d+|\(-\d+\))")

def check(p):
    try:
        m = FORM.fullmatch(p["answer"].replace(" ", ""))
        b = re.match(r"\(?(\w+)", p["prompt"]).group(1)
        ok = m and m.group(1) == b and same_value(p["prompt"].replace("*", ""), p["answer"])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

def typst(p, gap="0.3em"):
    return display(dfrac(p["prompt"].replace("*", "dot")))

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    return plain(p["prompt"].replace("*", "·"))

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.5 if "/" in p["prompt"] else 0.3

def answer_of(prompt):
    b = re.match(r"\(?(\w+)", prompt).group(1)
    e = to_sympy(prompt.replace("*", ""))
    n = sp.log(e, int(b)) if b.isdigit() else sp.powsimp(e).as_base_exp()[1]
    return pw(b, int(sp.nsimplify(n)))

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "7^(-3) * 7^5", "7^2")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
