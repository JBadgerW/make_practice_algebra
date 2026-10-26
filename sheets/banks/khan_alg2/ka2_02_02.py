"""Khan Algebra 2, Lesson 2-2: Powers of the imaginary unit, from the old
app's Alg2_02_02 (thirty of Khan's, i^8 to i^38, without answers).

Which is equivalent to i^n? Khan's four choices in Khan's order: 1, i, -1,
-i. n is 5 to 60; the four answers are spread evenly over a sheet.

A problem: dict(type, prompt, choices, answer, source).
    prompt  "i^26"    choices ["1", "i", "-1", "-i"]    answer "C"
check() computes i^n with sympy.
"""
import sympy as sp
from ... import gen
from ...check import to_sympy
from ...typmath import display
from . import courses

NAME = FAMILY = "ka2_02_02"
FIXED = False
TITLE = "Lesson 2-2: Powers of the imaginary unit"
INSTRUCTIONS = "Which is equivalent to each power of i?"
COURSES = courses(2)
CHOICES = ["1", "i", "-1", "-i"]

TYPES = [
    dict(key="1", title="Powers of i",
         look="i to a whole-number power.",
         move="The powers of i repeat every 4: i, -1, -i, 1. Divide the exponent by 4; the remainder says where you land "
              "(remainder 0 is 1)."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p["answer"])

def exponent(prompt):
    return int(prompt.split("^")[1].strip("() "))

def power(n):
    return CHOICES[[0, 1, 2, 3].index(n % 4)]

def draw(entry, r, tpl, want=None):
    n = r.randint(5, 60)
    if want:
        n += (gen.ABC.index(want) - n) % 4                 # the same remainder as the wanted choice
    choices, answer = gen.in_order(CHOICES, power(n))
    return dict(prompt=f"i^({n})" if n > 9 else f"i^{n}", choices=choices, answer=answer)

def check(p):
    try:
        right = sp.I ** exponent(p["prompt"])
        return "checked" if [to_sympy(c, imaginary=True) for c in gen.chosen(p)] == [right] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1,
                         balance=("ABCD", lambda k: k[2] if k[0] == NAME and len(k) == 3 else None))

def typst(p, gap="0.3em"):
    return f"{display(p['prompt'])} \\\n    {gen.choices_typst([f'${c}$' for c in p['choices']], 'linear')}"

def answer_typst(p):
    return "; ".join(f"{a}. ${c}$" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))

def text(p):
    return p["prompt"].replace("(", "").replace(")", "") + "   " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 0.6

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    try:
        n = exponent(t)
    except (ValueError, IndexError):
        raise ValueError("write a power of i, like i^26") from None
    new = dict(old, prompt=f"i^({n})" if n > 9 else f"i^{n}", answer=gen.in_order(CHOICES, power(n))[1], source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
