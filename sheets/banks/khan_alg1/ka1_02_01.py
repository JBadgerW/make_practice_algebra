"""Khan Algebra 1, Lesson 2-1: Equations with variables on both sides, from
the old app's Alg1_02_01 (three generated slots and seventeen of Khan's).

Khan's equations have integer solutions from -5 to 6, coefficients to 14,
and constants to 17; half of them have like terms to combine first
(-7 + 4m + 10 = 15 - 2m, 16 - 2r = -3r + 6r + 1). The old generator drew
solutions from -20 to 20; here they are -9 to 9, not 0, with coefficients
from -9 to 9 and constants to 40.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "12 c - 4 = 14 c - 10"
    answer  "c = 3"
check() substitutes the answer into the prompt and requires that the
equation has exactly one solution.
"""
from ... import gen, linear
from ...gen import need, signed, signed_except, written
from . import courses

NAME = FAMILY = "ka1_02_01"
FIXED = False
TITLE = "Lesson 2-1: Equations with variables on both sides"
INSTRUCTIONS = "Solve each equation."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Variables on Both Sides",
         look="A variable term and a number on each side.",
         move="Add or subtract to get the variable terms on one side and the numbers on the other. Then divide."),
    dict(key="2", title="Combine Like Terms First",
         look="One side has two variable terms, or two numbers, to combine.",
         move="Combine the like terms on each side first. Then solve as in Type 1."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing: the solution first, then the coefficients around it
# ------------------------------------------------------------------
def parts(r):
    """x, and a x + b = c x + d with a != c, every number small."""
    x = signed(r, 1, 9)
    a = signed(r, 1, 9)
    c = signed_except(r, 1, 9, a)
    b = signed(r, 1, 20)
    d = (a - c) * x + b
    need(d != 0 and abs(d) <= 40)
    return x, a, b, c, d

def t1_terms_first(r, v):                     # 12c - 4 = 14c - 10
    x, a, b, c, d = parts(r)
    return written((a, v), (b, "")) + " = " + written((c, v), (d, ""))

def t1_number_first_left(r, v):               # 2 - 2n = 3n + 17
    x, a, b, c, d = parts(r)
    return written((b, ""), (a, v)) + " = " + written((c, v), (d, ""))

def t1_number_first_right(r, v):              # 2d + 4 = 10 + 5d
    x, a, b, c, d = parts(r)
    return written((a, v), (b, "")) + " = " + written((d, ""), (c, v))

def t1_numbers_first(r, v):                   # 8 - 4s = 13 + s
    x, a, b, c, d = parts(r)
    return written((b, ""), (a, v)) + " = " + written((d, ""), (c, v))

def split(r, n, lo=1, hi=20):
    """n as two nonzero numbers, neither n itself: 7 -> (-3, 10)."""
    p = signed_except(r, lo, hi, n)
    need(n - p != 0 and abs(n - p) <= hi)
    return p, n - p

def t2_two_numbers(r, v):                     # -7 + 4m + 10 = 15 - 2m
    x, a, b, c, d = parts(r)
    b1, b2 = split(r, b)
    return written((b1, ""), (a, v), (b2, "")) + " = " + written((d, ""), (c, v))

def t2_two_numbers_end(r, v):                 # 4h + 17 + 2 = 1 - 5h
    x, a, b, c, d = parts(r)
    b1, b2 = split(r, b)
    return written((a, v), (b1, ""), (b2, "")) + " = " + written((c, v), (d, ""))

def t2_two_variables(r, v):                   # 16 - 2r = -3r + 6r + 1
    x, a, b, c, d = parts(r)
    c1, c2 = split(r, c, 1, 9)
    return written((b, ""), (a, v)) + " = " + written((c1, v), (c2, v), (d, ""))

def t2_variables_around(r, v):                # 9e + 4 = -5e + 14 + 13e
    x, a, b, c, d = parts(r)
    c1, c2 = split(r, c, 1, 9)
    return written((a, v), (b, "")) + " = " + written((c1, v), (d, ""), (c2, v))

TEMPLATES = {
    "1": [t1_terms_first, t1_number_first_left, t1_number_first_right, t1_numbers_first],
    "2": [t2_two_numbers, t2_two_numbers_end, t2_two_variables, t2_variables_around],
}

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS)
    prompt = TEMPLATES[entry][tpl](r, v)
    return dict(prompt=prompt, answer=linear.answer_of(prompt))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    try:
        return "checked" if linear.solves(p["prompt"], p["answer"]) else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    linear.answer_of, check, "12 c - 4 = 14 c - 10", "c = 3")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
