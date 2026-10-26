"""Khan Algebra 2, Lesson 1-10: Multiply binomials by polynomials, from the old app's Alg2_01_10
(twenty-four of Khan's, without answers).

(3c + 2)(c^2 - 6c - 4), (x^2 + 4)(x^2 - 6): a binomial (linear or in x^2,
sometimes number first) times a trinomial (Type 1) or two binomials in
x^2 (Type 2); either order.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(3 c + 2) (c^2 - 6 c - 4)"
    answer  "3 c^3 - 16 c^2 - 24 c - 8"
check() requires the answer to be the same polynomial as the prompt,
multiplied out and written in standard form (khan_alg1/polybank).
"""
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, signed_except, written
from ...typmath import display, dfrac, text as plain
from . import courses
from ..khan_alg1.polybank import expand_check, expand_answer_of, expand_edits

NAME = FAMILY = "ka2_01_10"
FIXED = False
TITLE = "Lesson 1-10: Multiply binomials by polynomials"
INSTRUCTIONS = "Expand. Write each answer as a polynomial in standard form."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Binomial Times Trinomial",
         look="A binomial times a polynomial with three terms.",
         move="Multiply each term of the binomial by each term of the trinomial (six products), then combine like terms."),
    dict(key="2", title="Two Binomials in x^2",
         look="Two binomials like (x^2 + 4)(x^2 - 6).",
         move="Multiply as two binomials: first, outer, inner, last. The middle terms are x^2 terms."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def poly_in(r, v, degrees, hi=9):
    """A polynomial with terms of these degrees, coefficients -hi..hi (not 0), descending."""
    return written(*[(signed(r, 1, hi), "" if d == 0 else v if d == 1 else f"{v}^{d}") for d in sorted(degrees, reverse=True)])

def degrees(r, top=3, n=None):
    n = n or r.randint(2, 3)
    return r.sample(range(0, top + 1), min(n, top + 1))

def binom(r, v, squared=False):
    a, b = signed(r, 1, 8), signed(r, 1, 9)
    t = f"{v}^2" if squared else v
    return f"({written((b, ''), (a, t)) if r.random() < 0.25 else written((a, t), (b, ''))})"

def t_bin_tri(r, v):
    pair = [binom(r, v, r.random() < 0.3), f"({poly_in(r, v, [2, 1, 0], 7)})"]
    r.shuffle(pair)
    return " ".join(pair)

def t_bin_bin(r, v):
    return f"{binom(r, v, True)} {binom(r, v, True)}"

TEMPLATES = {"1": [t_bin_tri], "2": [t_bin_bin]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    answer = expand_answer_of(prompt)
    need(answer != "0")
    return dict(prompt=prompt, answer=answer)

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("(3 c + 2) (c^2 - 6 c - 4)", "3 c^3 - 16 c^2 - 24 c - 8")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
