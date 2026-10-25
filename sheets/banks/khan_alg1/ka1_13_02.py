"""Khan Algebra 1, Lesson 13-2: Multiply monomials by polynomials (basic):
area model, from the old app's Alg1_13_02 (twelve generated slots).

A rectangle's height is a monomial (a number, or a number times x) and its
width a polynomial with up to three terms (x^2 + b x + c, a x^2 + b x,
b x + c); the area model shows a box per term. The area is the product,
expanded. Every coefficient is positive, 1 to 6: each box is a length (the
old template allowed -6, which no side can be).

A problem: dict(type, height, width, prompt, answer, source), in Typst math.
    height  "3"          width  "x^2 - 2 x + 5"
    prompt  "3 (x^2 - 2 x + 5)"   (the product, for the check and for editing)
    answer  "3 x^2 - 6 x + 15"
check() expands the prompt and requires the answer to be the same
polynomial in standard form.
"""
from ... import gen
from ...gen import written
from ...typst import esc
from ...typmath import text as plain
from . import courses
from .figures import PREAMBLE, area_model
from .polybank import expand_check, expand_answer_of, term_list

NAME = FAMILY = "ka1_13_02"
FIXED = False
TITLE = "Lesson 13-2: Multiply monomials by polynomials (basic): area model"
INSTRUCTIONS = "Express the area of the entire rectangle. The expression should be expanded."
COURSES = courses(13)

TYPES = [
    dict(key="1", title="A Number Times a Polynomial",
         look="The rectangle's height is a number.",
         move="Multiply the height by each term of the width: one box at a time. Add the boxes."),
    dict(key="2", title="An x Term Times a Polynomial",
         look="The rectangle's height is a number times x.",
         move="Multiply the height by each term of the width: the x's add to the exponents. Add the boxes."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def c(r):
    """A width's coefficient: positive, since every box is a length (the old template drew -6 to 6)."""
    return r.randint(1, 6)

WIDTHS = [lambda r: written((r.choice((1, 1, c(r))), "x^2"), (c(r), "x"), (c(r), "")),   # x^2 - 2 x + 5
          lambda r: written((c(r), "x^2"), (c(r), "x")),                                  # 3 x^2 - 4 x
          lambda r: written((c(r), "x^2"), (c(r), "")),                                   # x^2 + 5
          lambda r: written((c(r), "x"), (c(r), ""))]                                     # -4 x + 6

def draw(entry, r, tpl):
    width = WIDTHS[tpl](r)
    height = str(r.randint(2, 6)) if entry == "1" else written((r.randint(1, 3), "x"))   # a length: positive
    prompt = f"{height} ({width})"
    return dict(height=height, width=width, prompt=prompt, answer=expand_answer_of(prompt))

check = expand_check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(WIDTHS))

def typst(p, gap="0.3em"):
    return (f"A rectangle has a height of ${p['height']}$ and a width of ${p['width']}$. \\\n    "
            f"{area_model(term_list(p['width']), term_list(p['height']))}")

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    return f"height {plain(p['height'])}, width {plain(p['width'])}"

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 1.2

def edit_text(p):
    return f"{p['height']} ; {p['width']}"

def from_edit(t, old):
    h, _, w = t.replace("−", "-").partition(";")
    h, w = " ".join(h.split()), " ".join(w.split())
    if not h or not w:
        raise ValueError("write the height, then ; and the width: 3 ; x^2 - 2 x + 5")
    prompt = f"{h} ({w})"
    new = dict(old, height=h, width=w, prompt=prompt, answer=expand_answer_of(prompt), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
