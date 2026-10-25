"""Khan Algebra 1, Lesson 0-1: First introduction to algebra, from the old
app's Alg1_00_01 (four generated slots: x + a = b, x - a = b, a x = b,
x/a = b, every number 1 to 12).

One-step equations with whole-number solutions. Filed under Unit 1.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "x/4 = 7"
    answer  "x = 28"
check() substitutes the answer into the prompt.
"""
from ... import gen, linear
from ...gen import written
from . import courses

NAME = FAMILY = "ka1_00_01"
FIXED = False
TITLE = "Lesson 0-1: First introduction to algebra"
INSTRUCTIONS = "Solve each equation."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Add or Subtract",
         look="A number added to or subtracted from the variable.",
         move="Do the opposite to both sides: subtract what was added, add what was subtracted."),
    dict(key="2", title="Multiply or Divide",
         look="The variable multiplied or divided by a number.",
         move="Do the opposite to both sides: divide by what multiplies it, multiply by what divides it."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t1_plus(r, v):                            # x + 5 = 12
    x, a = r.randint(1, 12), r.randint(1, 12)
    return f"{written((1, v), (a, ''))} = {x + a}"

def t1_minus(r, v):                           # x - 4 = 9
    a, b = r.randint(1, 12), r.randint(1, 12)
    return f"{written((1, v), (-a, ''))} = {b}"

def t1_plus_first(r, v):                      # 5 + x = 12
    x, a = r.randint(1, 12), r.randint(1, 12)
    return f"{a} + {v} = {x + a}"

def t2_times(r, v):                           # 3 x = 21
    x, a = r.randint(1, 12), r.randint(2, 12)
    return f"{a} {v} = {a * x}"

def t2_divide(r, v):                          # x/4 = 7
    a, b = r.randint(2, 12), r.randint(1, 12)
    return f"{v}/{a} = {b}"

TEMPLATES = {"1": [t1_plus, t1_minus, t1_plus_first], "2": [t2_times, t2_divide]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    return dict(prompt=prompt, answer=linear.answer_of(prompt))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    try:
        return "checked" if linear.solves(p["prompt"], p["answer"], "fraction") else "failed"
    except Exception:
        return "unchecked"

typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(linear.answer_of, check, "x/4 = 7", "x = 28")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
