"""Khan Algebra 2, Lesson 2-6: Add & subtract complex numbers, from the old
app's Alg2_02_06 (thirty of Khan's, without answers).

(8 - 10 i) - (-16 + 2 i): parts -99 to 99, and now and then a number with
one part, as Khan's (9 + 52 i) - (1).

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(8 - 10 i) - (-16 + 2 i)"
    answer  "24 - 12 i"
check() (cx.check) compares the values and requires the answer in a + b i form.
"""
from ... import gen
from ...gen import need
from ...typmath import display
from . import courses
from . import cx

NAME = FAMILY = "ka2_02_06"
FIXED = False
TITLE = "Lesson 2-6: Add & subtract complex numbers"
INSTRUCTIONS = "Write each answer in the form a + bi."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Add",
         look="Two complex numbers added.",
         move="Add the real parts, then add the imaginary parts."),
    dict(key="2", title="Subtract",
         look="One complex number minus another.",
         move="Distribute the minus to both parts of the second number, then combine the real parts and the "
              "imaginary parts."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def operand(r):
    a, b = cx.number(r, -99, 99), cx.number(r, -99, 99)
    roll = r.random()
    return cx.written(a if roll > 0.1 else 0, b if roll < 0.1 or roll > 0.2 else 0)

def draw(entry, r, tpl):
    x, y = operand(r), operand(r)
    need(cx.STANDARD.fullmatch(x).group(3) or cx.STANDARD.fullmatch(y).group(3))   # one of them has both parts
    prompt = f"({x}) {'+' if entry == '1' else '-'} ({y})"
    answer = cx.answer_of(prompt)
    need(answer != "0")
    return dict(prompt=prompt, answer=answer)

check = cx.check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(cx.answer_of, check, "(8 - 10 i) - (-16 + 2 i)",
                                                                "24 - 12 i", imaginary=True)

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
