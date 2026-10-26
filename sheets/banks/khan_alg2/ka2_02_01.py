"""Khan Algebra 2, Lesson 2-1: Simplify roots of negative numbers, from the
old app's Alg2_02_01 (ten of Khan's, without answers).

±sqrt(-49) = ±7 i; ±sqrt(-24) = ±2 sqrt(6) i. Type 1: a perfect square
under the root (Khan's -4, -9, -49). Type 2: not one (Khan's -14, -24, -48,
-80): k^2 m with m square-free, at most 150.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "sqrt(-24)"
    answer  "2 sqrt(6) i"     (the positive root; the sheet shows ± on both sides)
check() squares the answer back to the number under the root and reads its
form: a positive multiple of i, the root simplified (radicals.simplest).
"""
import sympy as sp
from ... import gen, radicals
from ...gen import need
from ...check import to_sympy
from ...typmath import display, text as plain
from . import courses

NAME = FAMILY = "ka2_02_01"
FIXED = False
TITLE = "Lesson 2-1: Simplify roots of negative numbers"
INSTRUCTIONS = "Write each with the imaginary unit i, in simplest form."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Perfect Squares",
         look="The square root of a negative perfect square.",
         move="sqrt(-n) = sqrt(n) i. Take the square root of the number, then write i after it."),
    dict(key="2", title="Not Perfect Squares",
         look="The square root of a negative number that isn't a perfect square.",
         move="sqrt(-n) = sqrt(n) i. Take the largest perfect square out of sqrt(n); the i goes last."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def number(prompt):
    """The number under the root: "sqrt(-24)" -> -24."""
    return int(prompt.strip()[len("sqrt("):-1].replace(" ", ""))

def answer_of(prompt):
    n = number(prompt)
    if n >= 0:
        raise ValueError("a negative number under the root")
    k, m = radicals.squarefree(-n)
    body = radicals.written(k, {}, m, {})
    return "i" if body == "1" else f"{body} i"

def draw(entry, r, tpl):
    if entry == "1":
        n = r.randint(1, 20) ** 2
    else:
        n = r.randint(1, 6) ** 2 * r.choice([m for m in range(2, 40) if radicals.squarefree(m)[0] == 1])
        need(n <= 150 and radicals.squarefree(n)[1] != 1)
    prompt = f"sqrt(-{n})"
    return dict(prompt=prompt, answer=answer_of(prompt))

def check(p):
    try:
        a, n = p["answer"].strip(), number(p["prompt"])
        e = to_sympy(a, imaginary=True)
        root = a[:-1].strip() or "1"
        ok = (sp.expand(e ** 2) == n and sp.im(e) > 0 and a.endswith("i") and "i" not in root[:-1]
              and radicals.simplest(root))
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "sqrt(-24)", "2 sqrt(6) i", imaginary=True)

def typst(p, gap="0.3em"):
    return display(f"plus.minus {p['prompt']} = ")

def answer_typst(p):
    return display(f"plus.minus {p['answer']}")

def text(p):
    return f"±{plain(p['prompt'])}"

def answer_text(p):
    return f"±{plain(p['answer'])}"

def height(p):
    return 0.3

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
