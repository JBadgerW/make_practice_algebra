"""Khan Algebra 2, Lesson 1-5: Add & subtract polynomials, from the old app's
Alg2_01_05 (sixteen of Khan's, without answers).

Type 1: two named quadratics, P = -4b^2 + 6b - 9 and Q = 7b^2 - 2b - 5; find
P - Q, Q - P, or P + Q. Type 2: "Subtract 9a^2 - 6a + 5 from 10a^2 + 3a + 25",
where the order is the trap. Coefficients -11 to 11, constants to 25.

A problem: dict(type, prompt, names, polys, answer, source).
    prompt  "(-4 b^2 + 6 b - 9) - (7 b^2 - 2 b - 5)"   (the expression itself)
    names   ["P", "Q"]  polys  the two quadratics   (how the page shows them)
check() requires the answer to be the prompt's polynomial in standard form.
"""
from ... import gen
from ...gen import need, signed, written
from ...typmath import display, dfrac, text as plain
from . import courses
from ..khan_alg1.polybank import expand_check, expand_answer_of

NAME = FAMILY = "ka2_01_05"
FIXED = False
TITLE = "Lesson 1-5: Add & subtract polynomials"
INSTRUCTIONS = "Write each answer as a polynomial in standard form."
COURSES = courses(1)
LETTER_PAIRS = [("P", "Q"), ("T", "N"), ("E", "F"), ("A", "B"), ("G", "P"), ("X", "Y"), ("C", "D"), ("M", "T")]

TYPES = [
    dict(key="1", title="Named Polynomials",
         look="Two polynomials with names, and a sum or difference of them.",
         move="Put each polynomial in parentheses, in the order asked. For a difference, change every sign in the second."),
    dict(key="2", title="Subtract One from Another",
         look="Subtract A from B.",
         move="\"Subtract A from B\" means B - A: write B first. Then change every sign in A and combine."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def quadratic(r, v):
    return written((signed(r, 1, 11), f"{v}^2"), (signed(r, 1, 11), v), (signed(r, 1, 25), ""))

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS)
    a, b = quadratic(r, v), quadratic(r, v)
    if entry == "1":
        names = list(r.choice(LETTER_PAIRS))
        op = r.choice(("+", "-", "rev"))
        prompt = f"({b}) - ({a})" if op == "rev" else f"({a}) {op} ({b})"
        p = dict(prompt=prompt, names=names, polys=[a, b], op=op)
    else:
        p = dict(prompt=f"({b}) - ({a})", names=[], polys=[a, b], op="from")
    p["answer"] = expand_answer_of(p["prompt"])
    need(p["answer"] != "0")
    return p

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def asked(p):
    """The question, in letters or words."""
    (x, y), op = p["names"] or ("", ""), p["op"]
    return {"+": f"{x} + {y}", "-": f"{x} - {y}", "rev": f"{y} - {x}"}.get(op)

def typst(p, gap="0.3em"):
    a, b = p["polys"]
    if p["op"] == "from":
        return f"Subtract {display(dfrac(a))} from {display(dfrac(b))}."
    x, y = p["names"]
    return (f"#grid(columns: 2, column-gutter: 0.3em, row-gutter: 0.6em, [${x} =$], [${a}$], [${y} =$], [${b}$]) \\\n    "
            f"${asked(p)} = $")

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    a, b = p["polys"]
    if p["op"] == "from":
        return f"Subtract {plain(a)} from {plain(b)}"
    x, y = p["names"]
    return f"{x} = {plain(a)};  {y} = {plain(b)};  {asked(p)} = ?"

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.7

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for new polynomials; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
