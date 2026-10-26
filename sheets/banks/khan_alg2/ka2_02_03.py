"""Khan Algebra 2, Lesson 2-3: Parts of complex numbers, from the old app's
Alg2_02_03 (thirty of Khan's, without answers).

z = 14 i + 12.1: Khan writes the parts in either order, with whole numbers
or decimals. Type 1: write Re(z) and Im(z). Type 2: choose 1 of four;
the wrong ones are the misreadings in Khan's choices: the parts traded,
the i kept on the imaginary part, or both.

A problem: dict(type, prompt, answer or (choices, answer), source).
    prompt   "14 i + 12.1"
    Type 1   answer "Re(z) = 12.1, Im(z) = 14"
    Type 2   choices ["Re(z) = 12.1 and Im(z) = 14 i", ...]   answer "C"
check() reads the parts of z with sympy.
"""
import re
from ... import gen
from ...gen import need
from ...typmath import display, text as plain
from . import courses
from . import cx

NAME = FAMILY = "ka2_02_03"
FIXED = False
TITLE = "Lesson 2-3: Parts of complex numbers"
INSTRUCTIONS = ""
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Name the Parts", instructions="Find the real and imaginary parts of each.",
         look="A complex number z, its parts in either order.",
         move="Re(z) is the number without i. Im(z) is the number multiplying i: a real number, written without the i."),
    dict(key="2", title="Which Parts?", instructions="Choose 1 answer.",
         look="A complex number z and four ways to read its parts.",
         move="The real part has no i. The imaginary part is the coefficient of i, without the i.", width="full"),
]
T = gen.Types(TYPES, "", space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def reading(re_, im):
    return f"Re(z) = {re_} and Im(z) = {im}"

READING = re.compile(r"Re\(z\) = (.+) and Im\(z\) = (.+)")

def draw(entry, r, tpl):
    a = cx.number(r, -99, 99, r.choice((0, 0, 1, 2)))
    b = cx.number(r, -99, 99, r.choice((0, 0, 1)))
    need(abs(a) != abs(b))
    prompt = cx.written(a, b, imaginary_first=r.random() < 0.5)
    ra, rb = cx.num(a), cx.num(b)
    if entry == "1":
        return dict(prompt=prompt, answer=f"Re(z) = {ra}, Im(z) = {rb}")
    right = reading(ra, rb)
    wrong = [reading(rb, ra), reading(ra, f"{rb} i"), reading(f"{rb} i", ra)]
    choices, answer = gen.lettered(r, right, wrong)
    return dict(prompt=prompt, choices=choices, answer=answer)

def answer_parts(p):
    if p["type"] == "1":
        m = re.fullmatch(r"Re\(z\) = (.+), Im\(z\) = (.+)", p["answer"].strip())
    else:
        m = READING.fullmatch(gen.chosen(p)[0]) if len(gen.letters_of(p["answer"])) == 1 else None
    return m.groups() if m else None

def check(p):
    try:
        got = answer_parts(p)
        if not got or "i" in got[0] + got[1]:
            return "failed"
        return "checked" if tuple(cx.value(g) for g in got) == cx.parts(p["prompt"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def math(reading_):
    """"Re(z) = 3 and Im(z) = -6 i" with its math set as math."""
    m = READING.fullmatch(reading_)
    return f"$op(\"Re\")(z) = {m.group(1)}$ and $op(\"Im\")(z) = {m.group(2)}$"

def typst(p, gap="0.3em"):
    z = display(f"z = {p['prompt']}")
    if p["type"] == "1":
        return f'{z} \\\n    $op("Re")(z) =$ #h(4em) $op("Im")(z) =$'
    return f"{z} \\\n    What are the real and imaginary parts of $z$? \\\n    {gen.choices_typst([math(c) for c in p['choices']])}"

def answer_typst(p):
    if p["type"] == "1":
        re_, im = answer_parts(p) or ("?", "?")
        return f'$op("Re")(z) = {re_}$, $op("Im")(z) = {im}$'
    a = gen.letters_of(p["answer"])
    return "; ".join(f"{x}. {math(p['choices'][gen.ABC.index(x)])}" for x in a)

def text(p):
    z = f"z = {plain(p['prompt'])}"
    return z if p["type"] == "1" else z + "   " + gen.choices_text(p["choices"], plain)

def answer_text(p):
    return plain(p["answer"]) if p["type"] == "1" else gen.choice_answer_typst(p)

def height(p):
    return 0.6 if p["type"] == "1" else 1.5

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        a, b = cx.parts(t)
    except Exception:
        raise ValueError("write a complex number, like 14 i + 12.1") from None
    new = dict(old, prompt=t, source="edited")
    if old["type"] == "1":
        new["answer"] = f"Re(z) = {cx.num(a)}, Im(z) = {cx.num(b)}"
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] == "2":
        return gen.with_letters(p, t, check)
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
