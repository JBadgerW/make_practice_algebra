"""Khan Algebra 1, Lesson 2-6: Number of solutions to equations, from the
old app's Alg1_02_06 (twenty-nine of Khan's, without answers, and one
generated slot, which was always "infinitely many").

Khan's equations come in two shapes, a(x + b) = c x + d and
a x + b + c x = d x + e; the types follow the shape, not the answer, so a
section header never gives the answer away. Each problem is equally likely
to have no solution, one, or infinitely many. A no-solution equation keeps
the coefficient and changes the constant the way a mistake would: the
constant not distributed, its sign flipped, or off by a little.

A problem: dict(type, prompt, choices, answer, source).
    prompt   "-17 (y - 2) = -17 y + 64"
    choices  ["No solutions", "Exactly one solution", "Infinitely many solutions"]
    answer   "A"
check() solves the prompt with sympy and compares the count with the choice.
"""
from ... import gen, linear
from ...gen import need, signed, signed_except, written
from ...typmath import display, dfrac, text as plain
from . import courses

NAME = FAMILY = "ka1_02_06"
FIXED = False
TITLE = "Lesson 2-6: Number of solutions to equations"
INSTRUCTIONS = "How many solutions does each equation have?"
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Distribute First",
         look="A number times a sum on one side, like -6(x + 7).",
         move="Distribute and simplify. Different coefficients of x: exactly one solution. The same coefficient: "
              "no solution if the numbers differ, infinitely many if they match."),
    dict(key="2", title="Combine Like Terms First",
         look="Two x terms on one side, like 5x + 8 - 7x.",
         move="Combine like terms on each side, then compare as in Type 1."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
CHOICES = ["No solutions", "Exactly one solution", "Infinitely many solutions"]
COUNT = dict(zip(("none", "one", "all"), CHOICES))

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing: how many solutions first, then the equation
# ------------------------------------------------------------------
def right_side(r, n, c, d, outcome):
    """c x + d for an equation whose left side simplifies to c x + d: the same
    (all), the constant changed (none), or the coefficient changed (one)."""
    if outcome == "all":
        return c, d
    if outcome == "none":
        return c, r.choice([e for e in (n, -d, d + signed(r, 1, 9), 2 * d) if e != d])
    return signed_except(r, 1, 20, c, 0), signed(r, 1, 60)

def t1_distribute(r, v, outcome, flip=False):  # -17(y - 2) = -17y + 64
    a, b = signed_except(r, 2, 15, 0), signed(r, 1, 9)
    c, d = right_side(r, b, a, a * b, outcome)
    left = written((a, f"({written((1, v), (b, ''))})"))
    right = written((d, ""), (c, v)) if flip else written((c, v), (d, ""))
    return f"{left} = {right}"

def t1_distribute_flipped(r, v, outcome):     # 3(x + 5) = 8 - 4x
    return t1_distribute(r, v, outcome, flip=True)

def t1_distribute_right(r, v, outcome):       # -4x - 2 = -6(x + 7)
    left, _, right = t1_distribute(r, v, outcome).partition(" = ")
    return f"{right} = {left}"

def t2_combine(r, v, outcome, flip=False):    # 12z - 6 + 15z = 27z - 5
    a1, a2 = signed(r, 1, 40), signed(r, 1, 40)
    need(a1 + a2 != 0)
    b = signed(r, 1, 50)
    c, d = right_side(r, b, a1 + a2, b, outcome)
    left = written((a1, v), (b, ""), (a2, v))
    right = written((d, ""), (c, v)) if flip else written((c, v), (d, ""))
    return f"{left} = {right}"

def t2_combine_flipped(r, v, outcome):        # -4x - 7 + 10x = -7 + 6x
    return t2_combine(r, v, outcome, flip=True)

def t2_number_first(r, v, outcome):           # 50 + 23y + 27y = 50y + 50
    a1, a2 = signed(r, 1, 40), signed(r, 1, 40)
    need(a1 + a2 != 0)
    b = signed(r, 1, 50)
    c, d = right_side(r, b, a1 + a2, b, outcome)
    return f"{written((b, ''), (a1, v), (a2, v))} = {written((c, v), (d, ''))}"

TEMPLATES = {
    "1": [t1_distribute, t1_distribute_flipped, t1_distribute_right],
    "2": [t2_combine, t2_combine_flipped, t2_number_first],
}

def draw(entry, r, tpl):
    v = r.choice(("x", "y", "z", "a", "b", "m", "n", "p", "t"))
    outcome = r.choice(("none", "one", "all"))
    prompt = TEMPLATES[entry][tpl](r, v, outcome)
    need(linear.count(prompt) == outcome)          # a changed coefficient can't land back on the same one
    choices, answer = gen.in_order(CHOICES, COUNT[outcome])
    return dict(prompt=prompt, choices=choices, answer=answer)

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    try:
        return "checked" if gen.chosen(p) == [COUNT[linear.count(p["prompt"])]] else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    return f"{display(dfrac(p['prompt']))} \\\n    {gen.choices_typst(p['choices'])}"

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    return plain(p["prompt"]) + "      " + gen.choices_text(p["choices"])

def answer_text(p):
    return "; ".join(f"{a}. {c}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))

def height(p):
    return 0.9

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        n = linear.count(t)
    except Exception:
        raise ValueError("write a linear equation in Typst math, like -6 (x + 7) = -4 x - 2") from None
    new = dict(old, prompt=t, answer=gen.in_order(CHOICES, COUNT[n])[1], source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
