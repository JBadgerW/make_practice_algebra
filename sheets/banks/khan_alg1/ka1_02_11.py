"""Khan Algebra 1, Lesson 2-11: Compound inequalities, from the old app's
Alg1_02_11 (thirty-two of Khan's; the seventeen answered are right).

Solve a x + b < c AND (or OR) d x + e > f. Khan's choices are three sets
and "There are no solutions" and "All values of x are solutions". The
wrong sets are the real mistakes: each inequality's set alone, the answer
with the other word (AND for OR), a sign not flipped, and the segment
between the two boundaries. Boundaries are integers or
fractions (-19/13, 4/3); a quarter of the time the two share a boundary,
which gives Khan's special answers: x = -3, x < -1 or x > -1, no
solutions, and all values.

A problem: dict(type, prompt, choices, answer, source).
    prompt   "-6 x + 14 < -28 or 9 x + 15 <= -12"
    choices  ["x <= -3 or x > 7", "-3 <= x < 7", "x < 7", NONE, ALL]  (Typst math, or words)
    answer   "A"
check() solves the prompt and reads every choice as a set; the answer
must be the one choice equal to the solution.
"""
from fractions import Fraction as F
import sympy as sp
from ... import gen, ineq
from ...gen import need, signed, written
from ...typmath import display, dfrac, text as plain
from . import courses

NAME = FAMILY = "ka1_02_11"
FIXED = False
TITLE = "Lesson 2-11: Compound inequalities"
INSTRUCTIONS = "Solve for x."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="AND",
         look="Two inequalities joined by AND.",
         move="Solve each one. The answer is where both are true: the overlap. No overlap: no solutions."),
    dict(key="2", title="OR",
         look="Two inequalities joined by OR.",
         move="Solve each one. The answer is where either is true: both pieces. If they cover the whole line, "
              "every value is a solution."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in", width="full")     # one line, choices in two columns
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
NONE, ALL = "There are no solutions", "All values of x are solutions"
JOIN = {"1": "and", "2": "or"}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Drawing: each inequality from its boundary
# ------------------------------------------------------------------
def boundary(r):
    if r.random() < 0.6:
        return F(signed(r, 1, 8))
    q = r.randint(2, 13)
    return F(signed(r, 1, 2 * q), q)

def one(r, beta):
    """a x + b op c with boundary beta: a is a multiple of beta's denominator."""
    a = signed(r, 1, max(1, 25 // beta.denominator)) * beta.denominator
    need(abs(a) > 1)
    b = signed(r, 1, 90)
    c = a * beta + b
    need(c.denominator == 1 and abs(c) <= 120)
    return f"{written((a, 'x'), (b, ''))} {r.choice(('<', '>', '<=', '>='))} {int(c)}"

def flipped(ray):
    """A ray with its sign the wrong way round (not flipped after dividing by a negative): x > 2 -> x < 2."""
    if ray.start == -sp.oo:
        return sp.Interval(ray.end, sp.oo, left_open=ray.right_open)
    return sp.Interval(-sp.oo, ray.start, right_open=ray.left_open)

def draw(entry, r, tpl):
    b1 = boundary(r)
    b2 = b1 if r.random() < 0.25 else boundary(r)
    first, second = one(r, b1), one(r, b2)
    prompt = f"{first} {JOIN[entry]} {second}"
    s, s1, s2 = (ineq.solution(t) for t in (prompt, first, second))
    other = ineq.solution(f"{first} {'or' if entry == '1' else 'and'} {second}")
    lo, hi = sorted((b1, b2))
    between = sp.Interval(sp.Rational(lo.numerator, lo.denominator), sp.Rational(hi.numerator, hi.denominator))
    sets = []
    for c in (s, s1, s2, other, flipped(s1), flipped(s2), between):
        w = ineq.written(c, "x")
        if w not in (ineq.NONE, ineq.ALL) and w not in sets:
            sets.append(w)
    need(len(sets) >= 3)
    sets = sets[:3]
    r.shuffle(sets)
    choices = sets + [NONE, ALL]
    right = ineq.written(s, "x")
    right = {ineq.NONE: NONE, ineq.ALL: ALL}.get(right, right)
    return dict(prompt=prompt, choices=choices, answer=gen.ABC[choices.index(right)])

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: 1)

def check(p):
    try:
        s = ineq.solution(p["prompt"])
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if ineq.same(ineq.solution(c), s)]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def choice_typst(c):
    if c == ALL:
        return "All values of $x$ are solutions"
    return c if c == NONE else display(dfrac(ineq.typst(c)))

def typst(p, gap="0.3em"):
    return (f"{display(dfrac(ineq.typst(p['prompt'], upper=True)))} \\\n    "
            f"{gen.choices_typst([choice_typst(c) for c in p['choices']], 'grid')}")

def answer_typst(p):
    a = gen.letters_of(p["answer"])[0]
    return f"{a}. {choice_typst(p['choices'][gen.ABC.index(a)])}"

def text(p):
    return plain(p["prompt"].replace(" or ", " OR ").replace(" and ", " AND ")) + "      " + \
        gen.choices_text(p["choices"], plain)

def answer_text(p):
    a = gen.letters_of(p["answer"])[0]
    return f"{a}. {plain(p['choices'][gen.ABC.index(a)])}"

def height(p):
    return 1.4

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").replace(" OR ", " or ").replace(" AND ", " and ").split())
    try:
        s = ineq.solution(t, ineq.letter_of(t))
    except Exception:
        raise ValueError("write two inequalities in x joined by and or or: 2 x + 3 >= 7 or 2 x + 9 > 11") from None
    right = ineq.written(s, "x")
    right = {ineq.NONE: NONE, ineq.ALL: ALL}.get(right, right)
    choices = old["choices"] if right in old["choices"] else [right] + old["choices"][1:]
    new = dict(old, prompt=t, choices=choices, answer=gen.ABC[choices.index(right)], source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
