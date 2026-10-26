"""Khan Algebra 2, Lesson 1-12: Polynomial special products: perfect square, from the old app's Alg2_01_12
(sixteen of Khan's, without answers).

(4 + 7a^2)^2, (6y^2 + 5y^4)^2, (9n^7 - 1)^2: a binomial of monomials, squared;
sometimes number first, and then the key is too: 16 + 56 a^2 + 49 a^4.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(9 n^7 - 1)^2"
    answer  "81 n^14 - 18 n^7 + 1"
check() requires the answer to be the same polynomial as the prompt,
multiplied out, its degrees in order (khan_alg1/polybank).
"""
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, signed_except, written
from ...typmath import display, dfrac, text as plain
from . import courses
from ..khan_alg1.polybank import checker, expand_answer_of, expand_edits

NAME = FAMILY = "ka2_01_12"
FIXED = False
TITLE = "Lesson 1-12: Polynomial special products: perfect square"
INSTRUCTIONS = "Expand and combine like terms."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Square of a Binomial",
         look="(A + B)^2, where A and B are monomials.",
         move="(A + B)^2 = A^2 + 2 A B + B^2: square each term, and double their product for the middle."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
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

def t_letters(r, v):                           # (6y^2 + 5y^4)^2, (9n^7 - 1)^2
    a = (r.randint(1, 9), f"{v}^{r.randint(2, 7)}")
    b = (signed(r, 1, 9), "") if r.random() < 0.5 else (signed(r, 1, 9), f"{v}^{r.randint(1, 7)}")
    need(a[1] != b[1])
    return f"({written(a, b)})^2"

def t_number_first(r, v):                      # (4 + 7a^2)^2, (3 - 8w^2)^2
    return f"({written((r.randint(1, 9), ''), (signed(r, 1, 9), f'{v}^{r.randint(2, 7)}'))})^2"

TEMPLATES = {"1": [t_letters, t_number_first]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    answer = expand_answer_of(prompt, follow=True)       # 25 - 4 x^8 for (5 - 2 x^4)(5 + 2 x^4)
    need(answer != "0")
    return dict(prompt=prompt, answer=answer)

check = checker(True)
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("(9 n^7 - 1)^2", "81 n^14 - 18 n^7 + 1", follow=True)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
