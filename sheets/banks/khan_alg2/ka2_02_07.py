"""Khan Algebra 2, Lesson 2-7: Multiply complex numbers (basic), from the
old app's Alg2_02_07 (generated: a real or an imaginary number times a
complex number).

-4 dot (2 + 3 i), 5 i dot (3 - 2 i): Khan's dot, numbers -12 to 12. Type 1:
a real number times. Type 2: an imaginary number times, so i^2 = -1 comes in.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "5 i dot (3 - 2 i)"
    answer  "10 + 15 i"
check() (cx.check) compares the values and requires the answer in a + b i form.
"""
from ... import gen
from ...gen import need, signed
from ...typmath import display
from . import courses
from . import cx

NAME = FAMILY = "ka2_02_07"
FIXED = False
TITLE = "Lesson 2-7: Multiply complex numbers (basic)"
INSTRUCTIONS = "Multiply. Write each answer in the form a + bi."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="A Real Number Times",
         look="A real number times a complex number.",
         move="Distribute: multiply the real part and the imaginary part by the number."),
    dict(key="2", title="An Imaginary Number Times",
         look="A multiple of i times a complex number.",
         move="Distribute, then replace i^2 with -1 and write the real part first."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    k = signed(r, 2, 12) if entry == "1" else signed(r, 1, 12)
    first = cx.written(k, 0) if entry == "1" else cx.written(0, k)
    prompt = f"{first} dot ({cx.written(signed(r, 1, 12), signed(r, 1, 12))})"
    return dict(prompt=prompt, answer=cx.answer_of(prompt))

check = cx.check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(cx.answer_of, check, "5 i dot (3 - 2 i)", "10 + 15 i", imaginary=True)

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
