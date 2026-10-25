"""Khan Algebra 1, Lesson 2-7a: Number of solutions to equations challenge,
from the old app's Alg1_02_07a (twenty-one of Khan's; one answered, right).

Which of four equations have exactly one solution (or no solutions, or
infinitely many)? Choose all that apply. Khan builds the four from two
numbers, p and q, moved around and given signs (33x + 25 = 33x + 25,
33x - 33 = 33x + 25, 33x - 25 = 33x + 25, ...), so the equations look
alike and only the coefficients and constants decide. The templates are
Khan's three ways: the left side fixed, the right side fixed, or both
sides drawn from the same numbers.

A problem: dict(type, prompt, ask, choices, answer, source).
    ask      "one", "none", or "all"
    prompt   the question, in words
    choices  four equations, Typst math in $...$
    answer   the letters of every one with that many solutions: "A, C"
check() counts each equation's solutions with sympy.
"""
from ... import gen, linear
from ...gen import need, written
from ...typmath import text as plain
from . import courses

NAME = FAMILY = "ka1_02_07a"
FIXED = False
TITLE = "Lesson 2-7a: Number of solutions to equations challenge"
INSTRUCTIONS = "Choose all that apply."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Which Equations?",
         look="Four equations that look alike, built from the same two numbers.",
         move="Compare the x coefficients first: different, exactly one solution. The same: compare the "
              "constants: different, no solution; the same, infinitely many."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
ASK = {"one": "exactly one solution", "none": "no solutions", "all": "infinitely many solutions"}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["ask"], tuple(sorted(p["choices"])))

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def numbers(r):
    """Khan's two numbers: 2..99, different."""
    return r.sample(range(2, 100), 2) if r.random() < 0.5 else r.sample(range(2, 40), 2)

def side(r, ns, x="x"):
    a, b = r.choice(ns) * r.choice((-1, 1)), r.choice(ns) * r.choice((-1, 1))
    return written((a, x), (b, ""))

def left_fixed(r):                            # -60x + 32 = ... four right sides
    ns = numbers(r)
    left = side(r, ns)
    return [f"{left} = {side(r, ns)}" for _ in range(12)]

def right_fixed(r):                           # ... = 29x - 11, the same x coefficient throughout
    p, q = numbers(r)
    right = written((p, "x"), (-q, ""))
    return [f"{written((p, 'x'), (r.choice((p, q)) * r.choice((-1, 1)), ''))} = {right}" for _ in range(12)]

def both_sides(r):                            # 6x + 35 = -6x - 35, -6x + 35 = -6x + 35
    ns = numbers(r)
    return [f"{side(r, ns)} = {side(r, ns)}" for _ in range(12)]

TEMPLATES = {"1": [left_fixed, right_fixed, both_sides]}

def draw(entry, r, tpl):
    pool = list(dict.fromkeys(TEMPLATES[entry][tpl](r)))          # distinct, in order drawn
    ask = r.choice(list(ASK))
    yes = [e for e in pool if linear.count(e) == ask]
    no = [e for e in pool if linear.count(e) != ask]
    ks = [n for n in (1, 2, 3) if n <= len(yes) and 4 - n <= len(no)]
    need(ks)
    k = r.choice(ks)
    right, wrong = yes[:k], no[:4 - k]
    choices, letters = gen.lettered(r, [f"${e}$" for e in right], [f"${e}$" for e in wrong])
    return dict(ask=ask, prompt=f"Which of the following equations have {ASK[ask]}?",
                choices=choices, answer=letters)

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(TEMPLATES[e]))

def check(p):
    try:
        want = [gen.ABC[i] for i, c in enumerate(p["choices"]) if linear.count(c.strip("$")) == p["ask"]]
        return "checked" if want and gen.letters_of(p["answer"]) == want else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing: the question's kind, then the four equations
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    return f"{p['prompt']} \\\n    {gen.choices_typst(p['choices'])}"

def answer_typst(p):
    return p["answer"]

def text(p):
    return p["prompt"] + "   " + gen.choices_text(p["choices"], lambda c: plain(c.strip("$")))

def answer_text(p):
    return p["answer"]

def height(p):
    return 1.2

def edit_text(p):
    return f"{p['ask']}: " + " ; ".join(c.strip("$") for c in p["choices"])

def from_edit(t, old):
    ask, _, eqs = t.replace("−", "-").partition(":")
    ask, eqs = ask.strip(), [" ".join(e.split()) for e in eqs.split(";") if e.strip()]
    if ask not in ASK or len(eqs) < 2:
        raise ValueError("write one, none, or all, a colon, and the equations: none: 2 x + 1 = 2 x ; 3 x = x")
    try:
        right = [gen.ABC[i] for i, e in enumerate(eqs) if linear.count(e) == ask]
    except Exception:
        raise ValueError("write each equation in Typst math, like 2 x - 31 = -2 x - 31") from None
    new = dict(old, ask=ask, prompt=f"Which of the following equations have {ASK[ask]}?",
               choices=[f"${e}$" for e in eqs], answer=", ".join(right), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
