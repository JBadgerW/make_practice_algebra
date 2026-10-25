"""Khan Algebra 1, Lesson 8-1: Evaluate functions, from the old app's
Alg1_08_01 (twelve generated slots).

f(x) = 3 x + 4; f(5) = ? Type 1: a x + b or b + a x, coefficients to 15,
constants to 100, inputs -10 to 10. Type 2: a fraction or a half,
a + t/b at a multiple of b, a + 0.5 x at an even x. Function names f, g,
h, k; letters x, t, r. Answers are integers.

A problem: dict(type, prompt, answer, source).
    prompt  "f(x) = 3 x + 4 ; f(5)"
    answer  "f(5) = 19"
check() substitutes the input into the definition.
"""
import re
from ... import gen
from ...gen import need, signed, written
from ...linear import exact
from ...typmath import display, dfrac, text as plain, tx
from . import courses

NAME = FAMILY = "ka1_08_01"
FIXED = False
TITLE = "Lesson 8-1: Evaluate functions"
INSTRUCTIONS = "Evaluate each function."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="Linear Functions",
         look="A function like f(x) = 3 x + 4, and an input.",
         move="Put the input in for the letter everywhere it appears, then compute."),
    dict(key="2", title="With a Fraction or a Decimal",
         look="A function with x/4 or 0.5 x in it.",
         move="Put the input in and compute; the input is chosen so the fraction comes out whole."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
DEF = re.compile(r"\s*(\w)\((\w)\)\s*=\s*(.+)")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def name(r):
    return r.choice("fghk"), r.choice("xtr")

def t1_ax_b(r):                               # f(x) = 3 x + 4
    a, b, x = signed(r, 2, 15), signed(r, 1, 20 if r.random() < 0.7 else 100), signed(r, 1, 10)
    return written((a, "{v}"), (b, "")), x

def t1_b_ax(r):                               # g(r) = 12 - 5 r
    a, b, x = signed(r, 2, 10), signed(r, 2, 50), signed(r, 1, 10)
    return written((b, ""), (a, "{v}")), x

def t2_fraction(r):                           # k(t) = 7 - t/3 at t = 9
    a, b, c = signed(r, 2, 50), signed(r, 2, 10), signed(r, 1, 10)
    return f"{a} {'+' if b > 0 else '-'} {{v}}/{abs(b)}", c * b

def t2_half(r):                               # f(x) = 12 + 0.5 x at x = 8
    a, x = signed(r, 2, 50), signed(r, 1, 10) * 2
    return f"{a} {r.choice('+-')} 0.5 {{v}}", x

TEMPLATES = {"1": [t1_ax_b, t1_b_ax], "2": [t2_fraction, t2_half]}

def value(prompt):
    definition, _, call = prompt.partition(";")
    f, v, body = DEF.match(definition).groups()
    x = re.fullmatch(rf"\s*{f}\((.+)\)\s*", call).group(1)
    return f, x, exact(body).subs(exact(v), exact(x))

def answer_of(prompt):
    f, x, y = value(prompt)
    return f"{f}({x}) = {tx(y)}"

def draw(entry, r, tpl):
    f, v = name(r)
    body, x = TEMPLATES[entry][tpl](r)
    prompt = f"{f}({v}) = {body.format(v=v)} ; {f}({x})"
    need(value(prompt)[2].is_integer)
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        f, x, y = value(p["prompt"])
        lhs, _, rhs = p["answer"].partition("=")
        ok = " ".join(lhs.split()) == f"{f}({x})" and exact(rhs) == y
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

def typst(p, gap="0.3em"):
    definition, _, call = p["prompt"].partition(";")
    return f"{display(dfrac(definition.strip()))} \\\n    ${call.strip()} = $"

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    return plain(p["prompt"])

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.5

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "f(x) = 3 x + 4 ; f(5)", "f(5) = 19")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
