"""Single-step equations, from the Precision Teaching: Algebra game of the
same name (~/GitHub/precision_teaching_algebra, js/games/single-step.js),
with its add-ons 13, 14 and 15 always on.

Each problem is built from one basic fact on the numbers 1 to 15: addition
and subtraction from a + b = c, multiplication and division from a × b = c.
The equation shows two of the fact's numbers and hides the third:

    Addition        x + a = c, a + x = c        x + 9 = 23
    Subtraction     x - a = b, c - x = a        x - 14 = 8, 22 - x = 14
    Multiplication  a x = c                     13 x = 169
    Division        x/a = b, c/x = a            x/7 = 12, 84/x = 7

Answers are whole numbers from 1 up. A number by the x is never 1 in
multiplication or division (1 x = 7, x/1 = 7, 7/x = 1 aren't shown); the
other number of the fact may be.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "x - 14 = 8"
    answer  "x = 22"
check() solves the prompt with sympy and compares (sheets/linear.py: key, keyed).
"""
from .. import gen, linear
from ..gen import need

NAME = FAMILY = "single_step"
FIXED = False
TITLE = "Single-Step Equations"
INSTRUCTIONS = "Solve each equation."
COURSES = {"Prealgebra": "Additional Practice"}
FACTS = range(1, 16)                       # the numbers of the basic facts

TYPES = [
    dict(key="1", title="Addition",
         look="A number added to x: x + 9 = 23, 9 + x = 23.",
         move="Subtract the number from both sides."),
    dict(key="2", title="Subtraction",
         look="A number subtracted from x, or x subtracted from a number: x - 14 = 8, 22 - x = 14.",
         move="x - a: add the number to both sides. c - x: x is what's left when you take a away from c."),
    dict(key="3", title="Multiplication",
         look="A number times x: 13x = 169.",
         move="Divide both sides by the number."),
    dict(key="4", title="Division",
         look="x divided by a number, or a number divided by x: x/7 = 12, 84/x = 7.",
         move="x/a: multiply both sides by the number. c/x: x is what c is divided by to give a."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# The forms: a fact (a, b, c) as an equation, and its answer
# ------------------------------------------------------------------
def fact(r):
    return r.choice(FACTS), r.choice(FACTS)

def t1_after(r):                           # x + a = c
    a, b = fact(r)
    return f"x + {a} = {a + b}", b

def t1_before(r):                          # a + x = c
    a, b = fact(r)
    return f"{a} + x = {a + b}", b

def t2_take(r):                            # x - a = b
    a, b = fact(r)
    return f"x - {a} = {b}", a + b

def t2_from(r):                            # c - x = a
    a, b = fact(r)
    return f"{a + b} - x = {a}", b

def t3_times(r):                           # a x = c
    a, b = fact(r)
    need(a != 1)
    return f"{a} x = {a * b}", b

def t4_over(r):                            # x/a = b
    a, b = fact(r)
    need(a != 1)
    return f"x/{a} = {b}", a * b

def t4_into(r):                            # c/x = a
    a, b = fact(r)
    need(a != 1)
    return f"{a * b}/x = {a}", b

TEMPLATES = {
    "1": [t1_after, t1_before],
    "2": [t2_take, t2_from],
    "3": [t3_times],
    "4": [t4_over, t4_into],
}

def draw(entry, r, tpl):
    prompt, x = TEMPLATES[entry][tpl](r)
    return dict(prompt=prompt, answer=f"x = {x}")

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    """sympy solves the prompt again: the key's x, a whole number from 1 up, is its one solution."""
    try:
        x = p["answer"].partition("=")[2].strip()
        return "checked" if x.isdigit() and int(x) >= 1 and linear.keyed(p["prompt"], p["answer"]) else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, height = gen.shown()

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    linear.key, check, "x - 14 = 8", "x = 22")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
