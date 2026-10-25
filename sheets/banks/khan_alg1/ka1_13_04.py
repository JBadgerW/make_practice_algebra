"""Khan Algebra 1, Lesson 13-4: Multiply binomials intro, from the old app's Alg1_13_04
(sixteen generated slots).

(x + c)(x + f): both binomials lead with x, the numbers -9 to 9, not 0.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(x + 3) (x - 5)"
    answer  "x^2 - 2 x - 15"
check() expands the prompt and requires the answer to be the same
polynomial, written in standard form (no parentheses, degrees descending).
"""
from ... import gen
from ...gen import signed
from . import courses
from .polybank import binomial, expand_check, expand_edits, expand_answer_of

NAME = FAMILY = "ka1_13_04"
FIXED = False
TITLE = "Lesson 13-4: Multiply binomials intro"
INSTRUCTIONS = "Expand. Write each answer as a polynomial in standard form."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Two Binomials",
         look="Two binomials, each x plus or minus a number.",
         move="Multiply each term of the first by each term of the second (or use an area model), then combine the x terms."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t_sum_first(r, v):                         # (x + 3)(x - 5)
    return binomial(1, signed(r, 1, 9), v) + " " + binomial(1, signed(r, 1, 9), v)

TEMPLATES = {"1": [t_sum_first]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    return dict(prompt=prompt, answer=expand_answer_of(prompt))

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("(x + 3) (x - 5)", "x^2 - 2 x - 15")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
