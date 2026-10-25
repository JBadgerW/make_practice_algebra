"""Khan Algebra 1, Lesson 6-5: Systems of equations with substitution, from the old app's Alg1_06_05
(twenty generated slots, two templates).

a x + b y = c with x = e y + f (or y = d x + f): one equation already solved for
a letter. Solutions -12 to 12, coefficients -15 to 15, and the six numbers
adding to at most 80 in size, as the old templates had them.

A problem: dict(type, prompt, answer, source); prompt "eq1 ; eq2".
    prompt  "3 x - 2 y = 16 ; y = -4 x + 3"
    answer  "x = 2, y = -5"
check() substitutes the answer into both equations, and requires that
the system has exactly one solution.
"""
from ... import gen
from ...gen import need, signed, signed_except, written
from ...typmath import text as plain
from . import courses, twovar
from .twovar import standard

NAME = FAMILY = "ka1_06_05"
FIXED = False
TITLE = "Lesson 6-5: Systems of equations with substitution"
INSTRUCTIONS = "Solve each system of equations using the substitution method."
COURSES = courses(6)

TYPES = [
    dict(key="1", title="Solved for y",
         look="One equation is y = ... .",
         move="Put that expression in for y in the other equation. Solve for x, then find y."),
    dict(key="2", title="Solved for x",
         look="One equation is x = ... .",
         move="Put that expression in for x in the other equation. Solve for y, then find x."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p.get("point"))

def parts(r):
    x, y = r.randint(-12, 12), r.randint(-12, 12)
    a, b = signed(r, 1, 15), signed(r, 1, 15)
    return x, y, a, b, a * x + b * y

def t_for_y(r):                               # 3x - 2y = 16; y = -4x + 3
    x, y, a, b, c = parts(r)
    m = signed(r, 1, 15)
    k = y - m * x
    need(abs(a) + abs(b) + abs(c) + 1 + abs(m) + abs(k) <= 80 and m * b != -a)
    eqs = [standard(a, b, c), f"y = {written((m, 'x'), (k, ''))}"]
    r.shuffle(eqs)
    return " ; ".join(eqs)

def t_for_x(r):                               # 3x - 2y = 16; x = 5y - 4
    x, y, a, b, c = parts(r)
    m = signed(r, 1, 15)
    k = x - m * y
    need(abs(a) + abs(b) + abs(c) + 1 + abs(m) + abs(k) <= 80 and m * a != -b)
    eqs = [standard(a, b, c), f"x = {written((m, 'y'), (k, ''))}"]
    r.shuffle(eqs)
    return " ; ".join(eqs)

TEMPLATES = {"1": [t_for_y], "2": [t_for_x]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r)
    return dict(prompt=prompt, answer=twovar.answer_of(prompt))

check = twovar.check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

def typst(p, gap="0.3em"):
    return twovar.system_typst(p["prompt"])

def answer_typst(p):
    return f"${p['answer']}$"

text = twovar.text

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.7

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    twovar.answer_of, check, "3 x - 2 y = 16 ; y = -4 x + 3", "x = 2, y = -5")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
