"""Khan Algebra 2, Lesson 1-11: Polynomial special products: difference of squares, from the old app's Alg2_01_11
(twelve of Khan's, without answers).

(4b^2 + 3)(4b^2 - 3), (2x^4 + 3x^3)(2x^4 - 3x^3): a sum times a difference, with
higher powers; sometimes number first, (5 - 2x^4)(5 + 2x^4). The key follows the
prompt: 25 - 4 x^8 when the binomials lead with numbers.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "(4 b^2 + 3) (4 b^2 - 3)"
    answer  "16 b^4 - 9"
check() requires the answer to be the same polynomial as the prompt,
multiplied out, its degrees in order (khan_alg1/polybank).
"""
import sympy as sp
from ... import gen, poly
from ...gen import need, signed, signed_except, written
from ...typmath import display, dfrac, text as plain
from . import courses
from ..khan_alg1.polybank import checker, expand_answer_of, expand_edits

NAME = FAMILY = "ka2_01_11"
FIXED = False
TITLE = "Lesson 1-11: Polynomial special products: difference of squares"
INSTRUCTIONS = "Expand and combine like terms."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Sum Times Difference",
         look="(A + B)(A - B), where A and B are monomials.",
         move="The middle terms cancel: A^2 - B^2. Square each monomial: square the coefficient, double the exponent."),
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

def mono(r, v, k=None):
    e = r.randint(1, 7)
    return (signed(r, 1, 9) if k is None else k, f"{v}^{e}" if e > 1 else v)

def t_letters(r, v):                           # (2x^4 + 3x^3)(2x^4 - 3x^3) or (4b^2 + 3)(4b^2 - 3)
    a = (r.randint(1, 9), f"{v}^{r.randint(2, 7)}")
    b = (r.randint(1, 9), "") if r.random() < 0.5 else (r.randint(1, 9), f"{v}^{r.randint(1, 7)}")
    need(a[1] != b[1])
    pair = [f"({written(a, b)})", f"({written(a, (-b[0], b[1]))})"]
    r.shuffle(pair)
    return " ".join(pair)

def t_number_first(r, v):                      # (5 - 2x^4)(5 + 2x^4)
    k, a = r.randint(2, 9), (r.randint(1, 9), f"{v}^{r.randint(2, 7)}")
    pair = [f"({written((k, ''), a)})", f"({written((k, ''), (-a[0], a[1]))})"]
    r.shuffle(pair)
    return " ".join(pair)

TEMPLATES = {"1": [t_letters, t_number_first]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r, r.choice(gen.LETTERS))
    answer = expand_answer_of(prompt, follow=True)       # 25 - 4 x^8 for (5 - 2 x^4)(5 + 2 x^4)
    need(answer != "0")
    return dict(prompt=prompt, answer=answer)

check = checker(True)
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = expand_edits("(4 b^2 + 3) (4 b^2 - 3)", "16 b^4 - 9", follow=True)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
