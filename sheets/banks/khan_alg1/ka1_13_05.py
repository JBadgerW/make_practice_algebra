"""Khan Algebra 1, Lesson 13-5: Multiply binomials, from the old app's Alg1_13_05
(twenty-four generated slots).

(d x + e)(f x + g), any coefficients -9 to 9, not 0; about one in six is 1,\nas in Khan's lesson (the old app's note). The number comes first in some\nbinomials: (3 - 2 x)(x + 4).

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(2 x + 3) (3 x - 5)"
    answer  "6 x^2 - x - 15"
check() expands the prompt and requires the answer to be the same
polynomial, written in standard form (no parentheses, degrees descending).
"""
from ... import gen
from ...gen import signed_except
from . import courses
from .polybank import binomial, expand_check, expand_edits, expand_answer_of

NAME = FAMILY = "ka1_13_05"
FIXED = False
TITLE = "Lesson 13-5: Multiply binomials"
INSTRUCTIONS = "Expand. Write each answer as a polynomial in standard form."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="Two Binomials",
         look="Two binomials with any coefficients.",
         move="Multiply each term of the first by each term of the second, then combine like terms. Write the x^2 term first."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def c(r):
    """A coefficient: 1 about one time in six (Khan's), else -9 to 9, not -1, 0, or 1."""
    return 1 if r.random() < 0.18 else signed_except(r, 1, 9, 1, -1)

def t_both_x_first(r, v):                      # (2x + 3)(3x - 5)
    return binomial(c(r), c(r), v) + " " + binomial(c(r), c(r), v)

def t_second_number_first(r, v):               # (2x + 3)(-5 + 3x)
    return binomial(c(r), c(r), v) + " " + binomial(c(r), c(r), v, True)

def t_both_number_first(r, v):                 # (3 - 2x)(4 + x)
    return binomial(c(r), c(r), v, True) + " " + binomial(c(r), c(r), v, True)

TEMPLATES = {"1": [t_both_x_first, t_second_number_first, t_both_number_first]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    return dict(prompt=prompt, answer=expand_answer_of(prompt))

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("(2 x + 3) (3 x - 5)", "6 x^2 - x - 15")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
