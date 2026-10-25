"""Khan Algebra 1, Lesson 11-6: Cube roots, from the old app's Alg1_11_06
(ten of Khan's, answered, every answer right: the cube roots of 27 to 1728).

The cube roots of the perfect cubes 1 to 1728.

A problem: dict(type, prompt, answer, source).
    prompt  "root(3, 216)"     (Typst's cube root)
    answer  "6"
check() cubes the answer.
"""
import re
from ... import gen
from ...typmath import display
from . import courses

NAME = FAMILY = "ka1_11_06"
FIXED = False
TITLE = "Lesson 11-6: Cube roots"
INSTRUCTIONS = "Find each cube root."
COURSES = courses(11)

TYPES = [
    dict(key="1", title="Perfect Cubes",
         look="The cube root of a perfect cube.",
         move="Find the number that, used as a factor three times, makes the number under the root."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
ROOT = re.compile(r"root\(3,\s*(\d+)\)")

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def draw(entry, r, tpl):
    n = r.randint(1, 12)
    return dict(prompt=f"root(3, {n ** 3})", answer=str(n))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: 1)

def radicand(prompt):
    m = ROOT.fullmatch(prompt.strip())
    if not m:
        raise ValueError("write a cube root as root(3, 216)")
    return int(m.group(1))

def check(p):
    try:
        a = p["answer"].strip()
        return "checked" if a.isdigit() and int(a) ** 3 == radicand(p["prompt"]) else "failed"
    except Exception:
        return "unchecked"

def typst(p, gap="0.3em"):
    return display(p["prompt"])

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    return f"∛{radicand(p['prompt'])}"

def answer_text(p):
    return p["answer"]

def height(p):
    return 0.3

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    n = radicand(t)
    k = round(n ** (1 / 3))
    answer = str(k) if k ** 3 == n else old["answer"]
    new = dict(old, prompt=f"root(3, {n})", answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=t.strip())
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=6)     # only twelve
