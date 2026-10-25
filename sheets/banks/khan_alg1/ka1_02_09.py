"""Khan Algebra 1, Lesson 2-9: Multi-step linear inequalities, from the old
app's Alg1_02_09 (twenty-four of Khan's; the four answered are right).

Khan's are all a x + b < c x + d, with the variable on both sides,
coefficients and constants to 98, and the answer a fraction in lowest
terms (y > 5/6, b >= -34/3): "Reduce any fractions to lowest terms. Don't
round, and don't use mixed numbers." Whether the sign flips depends on
which side a student gathers the variable on, so it isn't a type of its own.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "5 y + 3 > -7 y + 13"
    answer  "y > 5/6"
check() solves the prompt and reads the answer as a set, compares the two,
and reads the answer's form: the letter, a sign, and an integer or a
fraction in lowest terms.
"""
import re
import sympy as sp
from ... import gen, ineq
from ...gen import need, signed, signed_except, written
from . import courses

NAME = FAMILY = "ka1_02_09"
FIXED = False
TITLE = "Lesson 2-9: Multi-step linear inequalities"
INSTRUCTIONS = "Solve each inequality. Reduce any fractions to lowest terms; don't use mixed numbers."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Variables on Both Sides",
         look="An inequality with a variable term and a number on each side.",
         move="Solve as an equation: gather the variable terms on one side and the numbers on the other. "
              "If you multiply or divide both sides by a negative number, flip the sign."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
FORM = re.compile(r"[a-z] (<=|>=|<|>) -?(\d+)(?:/(\d+))?")     # y > 5/6, b >= -34/3, x < 4

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def parts(r):
    hi = r.choice((20, 50, 99))                   # Khan mixes small numbers and large ones
    a = signed(r, 1, hi)
    c = signed_except(r, 1, hi, a)
    return a, signed(r, 1, hi), c, signed(r, 1, hi), r.choice(("<", ">", "<=", ">="))

def t_terms_first(r, v):                      # 4x + 4 <= 9x + 8
    a, b, c, d, op = parts(r)
    return f"{written((a, v), (b, ''))} {op} {written((c, v), (d, ''))}"

def t_number_first_left(r, v):                # 33 - 42v < 8v + 91
    a, b, c, d, op = parts(r)
    return f"{written((b, ''), (a, v))} {op} {written((c, v), (d, ''))}"

def t_number_first_right(r, v):               # 5y + 3 > 13 - 7y
    a, b, c, d, op = parts(r)
    return f"{written((a, v), (b, ''))} {op} {written((d, ''), (c, v))}"

TEMPLATES = {"1": [t_terms_first, t_number_first_left, t_number_first_right]}

def draw(entry, r, tpl):
    v = r.choice(gen.LETTERS)
    prompt = TEMPLATES[entry][tpl](r, v)
    s = ineq.solution(prompt)
    answer = ineq.written(s, v)
    need(sp.Rational(answer.split()[-1]).q <= 99)  # Khan's go to -34/3 and 38/17
    return dict(prompt=prompt, answer=answer)

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    try:
        m = FORM.fullmatch(" ".join(p["answer"].split()))
        form = m and (not m.group(3) or (int(m.group(3)) > 1 and sp.gcd(int(m.group(2)), int(m.group(3))) == 1))
        ok = ineq.same(ineq.solution(p["prompt"]), ineq.solution(p["answer"]))
        return "checked" if ok and form else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, height = gen.shown()

def answer_of(prompt):
    return ineq.written(ineq.solution(prompt), ineq.letter_of(prompt))

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "5 y + 3 > -7 y + 13", "y > 5/6")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
