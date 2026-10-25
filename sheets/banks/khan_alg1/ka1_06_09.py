"""Khan Algebra 1, Lesson 6-9: Systems of equations with elimination challenge, from the old app's Alg1_06_09
(thirty generated slots, four templates).

No coefficient is the opposite (or the same) of the other equation's, so one
or both equations must be multiplied first. Type 1: one coefficient is a
multiple of the other's (multiply one equation); Type 2: neither is
(multiply both). Some are written "a x + b y - c = 0". Solutions -12 to 12,
coefficients -15 to 15, the six numbers at most 110 in size.

A problem: dict(type, prompt, answer, source); prompt "eq1 ; eq2".
check() substitutes the answer into both equations, and requires that
the system has exactly one solution.
"""
from ... import gen
from ...gen import need, signed, signed_except, written
from ...typmath import text as plain
from . import courses, twovar
from .twovar import standard

NAME = FAMILY = "ka1_06_09"
FIXED = False
TITLE = "Lesson 6-9: Systems of equations with elimination challenge"
INSTRUCTIONS = "Solve each system of equations using elimination."
COURSES = courses(6)

TYPES = [
    dict(key="1", title="Multiply One Equation",
         look="One coefficient is a multiple of the other equation's, like 2x and 6x.",
         move="Multiply that equation so the coefficients are opposites. Then add, solve, and put the value back."),
    dict(key="2", title="Multiply Both Equations",
         look="No coefficient is a multiple of the other equation's.",
         move="Multiply each equation so one letter's coefficients become opposites (use their least common multiple). Then add."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p.get("point"))

def written_eq(a, b, c, zero, y_first):
    if zero:                                   # 2x + 3y - 12 = 0
        left = written((b, "y"), (a, "x"), (-c, "")) if y_first else written((a, "x"), (b, "y"), (-c, ""))
        return f"{left} = 0"
    return standard(a, b, c, v_first=y_first)

def system(r, one, zero, y_first):
    x, y = r.randint(-12, 12), r.randint(-12, 12)
    a, b = signed(r, 2, 15), signed(r, 2, 15)
    if one:                                    # one letter's coefficients: a and k a
        k = signed_except(r, 2, 4, 1, -1)
        d, e = (k * a, signed_except(r, 2, 15, b, -b)) if r.random() < 0.5 else (signed_except(r, 2, 15, a, -a), k * b)
    else:
        d, e = signed_except(r, 2, 15, a, -a), signed_except(r, 2, 15, b, -b)
        need(d % a and a % d and e % b and b % e)
    need(a * e != b * d)
    c, f = a * x + b * y, d * x + e * y
    need(sum(map(abs, (a, b, c, d, e, f))) <= 110)
    return f"{written_eq(a, b, c, zero, y_first)} ; {written_eq(d, e, f, zero, y_first)}"

TEMPLATES = {k: [lambda r, k=k, z=z, s=s: system(r, k == "1", z, s) for z in (False, True) for s in (False, True)]
             for k in ("1", "2")}

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
    twovar.answer_of, check, "2 x + 3 y = 12 ; 6 x - 5 y = 8", "x = 3, y = 2")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
