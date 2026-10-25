"""Khan Algebra 1, Lesson 2-8: Linear equations with unknown coefficients,
from the old app's Alg1_02_08 (twenty of Khan's, without answers).

Solve for x, y, or z when some coefficients and constants are letters
(-px + r = -8x - 2, ax + 3x = bx + 5, w(-4 + z) = mz + 17); the equation
is assumed to have a solution. Khan's numbers go to 93. The key writes the
answer as one fraction, its denominator led by a plus sign, as the Advanced
Math literal equations do: -p x + r = -8 x - 2 gives x = (r + 2)/(p - 8).

A letter times parentheses is shown with a dot, w ⋅ (-4 + z), as Khan
does, so it can't be read as a function; the prompt itself is plain Typst
math, "w (-4 + z) = m z + 17".

A problem: dict(type, prompt, target, answer, source), as adv_literal's,
and checked the same way: the answer, substituted for the target at random
values of the other letters, makes the equation true, and it is one
fraction in lowest terms without the target in it.
"""
import re
from ... import gen
from ...gen import need, signed, written
from ...check import simplest_form
from ...typmath import display, dfrac, text as plain
from .. import adv_literal
from . import courses

NAME = FAMILY = "ka1_02_08"
FIXED = False
TITLE = "Lesson 2-8: Linear equations with unknown coefficients"
INSTRUCTIONS = "Solve for the indicated variable. Assume each equation has a solution."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Letters for Numbers",
         look="Variable terms on both sides, with letters as some coefficients or constants.",
         move="Gather the terms with the variable on one side and the rest on the other. Factor the "
              "variable out of its terms, then divide by what's left."),
    dict(key="2", title="Like Terms to Combine",
         look="Two variable terms on one side, like a x + 3 x.",
         move="Gather every variable term on one side, factor the variable out, and divide."),
    dict(key="3", title="Distribute First",
         look="A letter or number times parentheses that hold the variable.",
         move="Distribute first. Then gather, factor out the variable, and divide."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p["target"])

# ------------------------------------------------------------------
# Drawing: L, M are letters; n, m numbers
# ------------------------------------------------------------------
def n(r, hi=60):
    return signed(r, 2, hi)

def t1_letter_both(r, v, L, M):               # p y + 7 = 6 y + q
    return f"{written((1, f'{L} {v}'), (n(r), ''))} = {written((n(r, 20), v), (1, M))}"

def t1_letter_coefficient(r, v, L, M):        # -p x + r = -8 x - 2
    return f"{written((r.choice((-1, 1)), f'{L} {v}'), (1, M))} = {written((n(r, 20), v), (n(r), ''))}"

def t1_letter_constants(r, v, L, M):          # 12 y + d = -19 y + t
    return f"{written((n(r, 20), v), (1, L))} = {written((n(r, 20), v), (r.choice((-1, 1)), M))}"

def t1_letters_right(r, v, L, M):             # -4 z + 1 = b z + c
    return f"{written((n(r, 20), v), (n(r), ''))} = {written((1, f'{L} {v}'), (1, M))}"

def t2_letter_and_number(r, v, L, M):         # a x + 3 x = b x + 5
    return f"{written((1, f'{L} {v}'), (n(r, 20), v))} = {written((1, f'{M} {v}'), (n(r), ''))}"

def t2_number_and_letter(r, v, L, M):         # 19 x + r x = -37 x + w
    return f"{written((n(r, 40), v), (1, f'{L} {v}'))} = {written((n(r, 40), v), (1, M))}"

def t2_two_letters(r, v, L, M):               # p y + q y = -4 y + 8
    return f"{written((1, f'{L} {v}'), (1, f'{M} {v}'))} = {written((n(r, 20), v), (n(r), ''))}"

def t2_two_numbers(r, v, L, M):               # 16 z + 29 z = p z - v
    return f"{written((n(r, 30), v), (n(r, 30), v))} = {written((1, f'{L} {v}'), (r.choice((-1, 1)), M))}"

def inside(r, v, first):
    return f"({written((first, ''), (1, v))})" if not isinstance(first, str) else f"({first} + {v})"

def t3_letter_times(r, v, L, M):              # w (-4 + z) = m z + 17
    return f"{written((1, f'{L} {inside(r, v, n(r, 20))}'))} = {written((1, f'{M} {v}'), (n(r), ''))}"

def t3_letters_inside(r, v, L, M):            # -p (d + z) = -2 z + 59
    return f"{written((r.choice((-1, 1)), f'{L} {inside(r, v, M)}'))} = {written((n(r, 20), v), (n(r), ''))}"

def t3_minus_inside(r, v, L, M):              # a (5 - x) = b x - 8
    k = n(r, 20)
    return f"{L} ({written((abs(k), ''), (-1, v))}) = {written((1, f'{M} {v}'), (n(r), ''))}"

TEMPLATES = {
    "1": [t1_letter_both, t1_letter_coefficient, t1_letter_constants, t1_letters_right],
    "2": [t2_letter_and_number, t2_number_and_letter, t2_two_letters, t2_two_numbers],
    "3": [t3_letter_times, t3_letters_inside, t3_minus_inside],
}

def draw(entry, r, tpl):
    v = r.choice("xyz")
    L, M = r.sample([c for c in gen.LETTERS if c not in "xyz"], 2)
    prompt = TEMPLATES[entry][tpl](r, v, L, M)
    try:
        answer = adv_literal.solve(prompt, v)
    except (KeyError, ValueError):                # the variable cancelled: 12 y + d = 12 y + t
        raise gen.Redraw from None
    need(simplest_form(answer.split("=", 1)[1]))
    return dict(prompt=prompt, target=v, answer=answer)

check = adv_literal.check
generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing and editing, as adv_literal: "equation ; letter"
# ------------------------------------------------------------------
DOT = re.compile(r"\b([A-Za-z]) \(")

def dotted(t):
    """A letter times parentheses with a dot: "w (-4 + z)" -> "w dot (-4 + z)"."""
    return DOT.sub(r"\1 dot (", t)

def typst(p, gap="0.3em"):
    return f"{display(dfrac(dotted(p['prompt'])))}; #h({gap}) ${p['target']}$"

def text(p):
    return f"{plain(p['prompt']).replace(' (', ' · (')};  {p['target']}"

answer_typst, answer_text, height = adv_literal.answer_typst, adv_literal.answer_text, adv_literal.height
edit_text, from_edit = adv_literal.edit_text, adv_literal.from_edit
answer_edit_text, with_answer = adv_literal.answer_edit_text, adv_literal.with_answer

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
