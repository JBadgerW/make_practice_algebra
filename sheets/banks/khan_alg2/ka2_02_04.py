"""Khan Algebra 2, Lesson 2-4: Classify complex numbers, from the old app's
Alg2_02_04 (thirty of Khan's, without answers).

What type of number is 3.75 i + 7? Choose all that apply: Real, Purely
imaginary, Complex. Khan's choice reads "Imaginary"; the standard term for
a real multiple of i (no real part) is "purely imaginary", since some
books call any non-real number imaginary. A real number has no imaginary
part; every number here is complex. So 7 is Real and Complex, -91 i is
Purely imaginary and Complex, and 3.75 i + 7 is only Complex. The three
kinds are spread evenly over a sheet.

A problem: dict(type, prompt, choices, answer, source).
    prompt  "3.75 i + 7"    choices ["Real", "Purely imaginary", "Complex"]    answer "C"
check() reads the parts of the number with sympy.
"""
from ... import gen
from ...typmath import display, text as plain
from . import courses
from . import cx

NAME = FAMILY = "ka2_02_04"
FIXED = False
TITLE = "Lesson 2-4: Classify complex numbers"
INSTRUCTIONS = "What type of number is each? Choose all answers that apply."
COURSES = courses(2)
CHOICES = ["Real", "Purely imaginary", "Complex"]
KINDS = {"real": ["Real", "Complex"], "imaginary": ["Purely imaginary", "Complex"], "complex": ["Complex"]}
OUTCOMES = {"A, C": "real", "B, C": "imaginary", "C": "complex"}

TYPES = [
    dict(key="1", title="Real, Purely Imaginary, or Complex?",
         look="A number: a real part, an imaginary part, or both.",
         move="No i: real. Only a multiple of i, with no real part: purely imaginary. Every one of them is also "
              "complex (a + bi), so Complex is always one of the answers."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p["answer"])

def kind(prompt):
    a, b = cx.parts(prompt)
    return "imaginary" if a == 0 and b != 0 else "real" if b == 0 else "complex"

def draw(entry, r, tpl, want=None):
    k = OUTCOMES[want] if want else r.choice(list(KINDS))
    places = lambda: r.choice((0, 0, 1, 2))
    a = cx.number(r, -999, 999, places()) if r.random() < 0.3 else cx.number(r, -99, 99, places())
    b = cx.number(r, -99, 99, places())
    if k == "real":
        b = 0
    elif k == "imaginary":
        a = 0
    prompt = cx.written(a, b, imaginary_first=r.random() < 0.5)
    choices, answer = gen.in_order(CHOICES, KINDS[k])
    return dict(prompt=prompt, choices=choices, answer=answer)

def check(p):
    try:
        return "checked" if gen.chosen(p) == KINDS[kind(p["prompt"])] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1,
                         balance=(tuple(OUTCOMES), lambda k: k[2] if k[0] == NAME and len(k) == 3 else None))

def typst(p, gap="0.3em"):
    return f"What type of number is ${p['prompt']}$? \\\n    {gen.choices_typst(p['choices'], 'linear')}"

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    return plain(p["prompt"]) + "   " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 0.6

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        k = kind(t)
    except Exception:
        raise ValueError("write a number, like 3.75 i + 7") from None
    new = dict(old, prompt=t, answer=gen.in_order(CHOICES, KINDS[k])[1], source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
