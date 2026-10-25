"""Khan Algebra 1, Lesson 13-7: Multiply perfect squares of binomials, from the old app's Alg1_13_07
(twelve generated slots).

(x + e)^2, (d x + e)^2, or written as a product, (x - 4)(x - 4).

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(3 x - 4)^2"
    answer  "9 x^2 - 24 x + 16"
check() expands the prompt and requires the answer to be the same
polynomial, written in standard form (no parentheses, degrees descending).
"""
from ... import gen
from ...gen import signed
from . import courses
from .polybank import binomial, expand_check, expand_edits, expand_answer_of

NAME = FAMILY = "ka1_13_07"
FIXED = False
TITLE = "Lesson 13-7: Multiply perfect squares of binomials"
INSTRUCTIONS = "Expand. Combine like terms."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Square of a Binomial",
         look="A binomial squared, or a binomial times itself.",
         move="(a + b)^2 = a^2 + 2 a b + b^2: square the first term, double the product of the terms, square the last."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t_square(r, v):                            # (x - 4)^2
    return binomial(1, signed(r, 1, 9), v) + "^2"

def t_square_coefficient(r, v):                # (3x - 4)^2
    return binomial(r.randint(2, 9), signed(r, 1, 9), v) + "^2"

def t_product(r, v):                           # (x - 4)(x - 4), (3x + 1)(3x + 1)
    b = binomial(r.choice((1, r.randint(2, 9))), signed(r, 1, 9), v)
    return f"{b} {b}"

TEMPLATES = {"1": [t_square, t_square_coefficient, t_product]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    return dict(prompt=prompt, answer=expand_answer_of(prompt))

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("(3 x - 4)^2", "9 x^2 - 24 x + 16")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
