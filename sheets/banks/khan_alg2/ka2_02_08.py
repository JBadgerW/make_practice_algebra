"""Khan Algebra 2, Lesson 2-8: Multiply complex numbers, from the old app's
Alg2_02_08 (generated: two complex numbers, each with both parts).

(4 - 3 i) dot (2 + 5 i): Khan's dot, numbers -12 to 12 (the first real part
at least 2 in size, as the old app drew it).

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(4 - 3 i) dot (2 + 5 i)"
    answer  "23 + 14 i"
check() (cx.check) compares the values and requires the answer in a + b i form.
"""
from ... import gen
from ...gen import need, signed
from ...typmath import display
from . import courses
from . import cx

NAME = FAMILY = "ka2_02_08"
FIXED = False
TITLE = "Lesson 2-8: Multiply complex numbers"
INSTRUCTIONS = "Multiply. Write each answer in the form a + bi."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Two Complex Numbers",
         look="Two complex numbers multiplied, each with a real and an imaginary part.",
         move="Multiply each part by each part (FOIL), replace i^2 with -1, and combine: real parts, then imaginary."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    x = cx.written(signed(r, 2, 12), signed(r, 1, 12))
    y = cx.written(signed(r, 1, 12), signed(r, 1, 12))
    prompt = f"({x}) dot ({y})"
    answer = cx.answer_of(prompt)
    need(answer != "0")
    return dict(prompt=prompt, answer=answer)

check = cx.check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(cx.answer_of, check, "(4 - 3 i) dot (2 + 5 i)", "23 + 14 i", imaginary=True)

def typst(p, gap="0.3em"):
    return display(p["prompt"])

def answer_typst(p):
    return display(p["answer"])

def text(p):
    return cx.plain(p["prompt"])

def answer_text(p):
    return cx.plain(p["answer"])

def height(p):
    return 0.3

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
