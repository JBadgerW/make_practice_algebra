"""Khan Algebra 1, Lesson 11-4: Square roots, from the old app's Alg1_11_04
(nine of Khan's, answered, every answer right: sqrt(9) to sqrt(144)).

The square roots of the perfect squares 1 to 400.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "sqrt(144)"
    answer  "12"
check() compares the values exactly.
"""
from ... import gen
from ...check import to_sympy
from . import courses

NAME = FAMILY = "ka1_11_04"
FIXED = False
TITLE = "Lesson 11-4: Square roots"
INSTRUCTIONS = "Find each square root."
COURSES = courses(11)

TYPES = [
    dict(key="1", title="Perfect Squares",
         look="The square root of a perfect square.",
         move="Find the number that, times itself, makes the number under the root."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    n = r.randint(1, 20)
    return dict(prompt=f"sqrt({n * n})", answer=str(n))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: 1)

def answer_of(prompt):
    v = to_sympy(prompt)
    if not v.is_Integer:
        raise ValueError("not a perfect square")
    return str(v)

def check(p):
    try:
        return "checked" if to_sympy(p["prompt"]) == to_sympy(p["answer"]) and p["answer"].strip().isdigit() else "failed"
    except Exception:
        return "unchecked"

typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "sqrt(144)", "12")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)    # only twenty
