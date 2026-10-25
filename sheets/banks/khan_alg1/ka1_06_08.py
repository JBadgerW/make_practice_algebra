"""Khan Algebra 1, Lesson 6-8: Systems of equations with elimination, from the old app's Alg1_06_08
(twenty generated slots, two templates).

Two equations in standard form whose x terms (or y terms) are opposites, so
adding them eliminates a letter. Solutions -12 to 12, coefficients -15 to 15,
the six numbers at most 80 in size; some write the y term first.

A problem: dict(type, prompt, answer, source); prompt "eq1 ; eq2".
    prompt  "2 x + 3 y = 12 ; -2 x + y = 4"
    answer  "x = 0, y = 4"
check() substitutes the answer into both equations, and requires that
the system has exactly one solution.
"""
from ... import gen
from ...gen import need, signed, signed_except, written
from ...typmath import text as plain
from . import courses, twovar
from .twovar import standard

NAME = FAMILY = "ka1_06_08"
FIXED = False
TITLE = "Lesson 6-8: Systems of equations with elimination"
INSTRUCTIONS = "Solve each system of equations using the elimination method."
COURSES = courses(6)

TYPES = [
    dict(key="1", title="Opposite Coefficients",
         look="The x terms (or the y terms) are opposites, like 2x and -2x.",
         move="Add the equations: that letter drops out. Solve for the other letter, then put it back into either equation."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p.get("point"))

def system(r, opposite_x, y_first):
    x, y = r.randint(-12, 12), r.randint(-12, 12)
    a, b = signed(r, 1, 15), signed(r, 1, 15)
    d, e = (-a, signed_except(r, 1, 15, -b, b)) if opposite_x else (signed_except(r, 1, 15, -a, a), -b)
    c, f = a * x + b * y, d * x + e * y
    need(sum(map(abs, (a, b, c, d, e, f))) <= 80)
    return f"{standard(a, b, c, v_first=y_first)} ; {standard(d, e, f, v_first=y_first)}"

TEMPLATES = {"1": [lambda r: system(r, True, False), lambda r: system(r, False, False),
                   lambda r: system(r, True, True), lambda r: system(r, False, True)]}

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
    twovar.answer_of, check, "2 x + 3 y = 12 ; -2 x + y = 4", "x = 0, y = 4")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
