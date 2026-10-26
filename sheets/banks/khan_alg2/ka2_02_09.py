"""Khan Algebra 2, Lesson 2-9: Solve quadratic equations: complex solutions,
from the old app's Alg2_02_09 (thirty of Khan's, without answers; each has
exactly one right choice, checked).

x^2 - 5 x - 10 = 0: find the solutions, choose 1 of four. Most of Khan's
have complex solutions, some real ones; here about seven in ten are
complex. The discriminant is never 0 or a perfect square, so the answer
keeps a root. Khan's choices: -b/(2a) ± sqrt(|D|)/(2a), with i when D < 0,
reduced. The wrong ones are Khan's: the sign of the real part flipped, the
i dropped (or added), both, every part over a instead of 2a, or the
discriminant taken as b^2 + 4ac. Khan wrote ∓ when a < 0; the same two
numbers are written ± here.

A problem: dict(type, prompt, choices, answer, source).
    prompt   "x^2 - 5 x - 10 = 0"
    choices  ["5/2 plus.minus sqrt(65)/2", ...]    answer "D"
check() solves the equation with sympy and reads both numbers out of each
choice: exactly the answer's choice is the solution set.
"""
from fractions import Fraction as F
import sympy as sp
from ... import gen, radicals
from ...gen import need, signed
from ...check import to_sympy
from ...typmath import display, dfrac, text as plain
from . import courses

NAME = FAMILY = "ka2_02_09"
FIXED = False
TITLE = "Lesson 2-9: Solve quadratic equations: complex solutions"
INSTRUCTIONS = "Find the solutions of each quadratic equation."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="The Quadratic Formula",
         look="A quadratic equation = 0 that doesn't factor.",
         move="x = (-b ± sqrt(b^2 - 4ac))/(2a). If b^2 - 4ac is negative, sqrt(-n) = sqrt(n) i: the solutions are "
              "complex. Simplify the root and reduce both fractions.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def fraction(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"

def written(real, d, over, i):
    """real ± sqrt(d)/over, with i after the root if i: reduced, the root simplified."""
    k, m = radicals.squarefree(d)
    c = F(k, over)
    if m == 1:
        rad = fraction(c)
    else:
        top = f"sqrt({m})" if c.numerator == 1 else f"{c.numerator} sqrt({m})"
        rad = top if c.denominator == 1 else f"{top}/{c.denominator}" if c.numerator == 1 else f"({top})/{c.denominator}"
    rad = rad + " i" if i else rad
    return f"{fraction(real)} plus.minus {rad}" if real else f"plus.minus {rad}"

def solutions(a, b, c):
    """The right choice and Khan's misreadings."""
    D = b * b - 4 * a * c
    real, over = F(-b, 2 * a), 2 * abs(a)
    right = written(real, abs(D), over, D < 0)
    wrong = [written(-real, abs(D), over, D < 0), written(real, abs(D), over, D > 0),
             written(-real, abs(D), over, D > 0), written(2 * real, abs(D), abs(a), D < 0)]
    E = b * b + 4 * a * c
    if E:
        wrong.append(written(real, abs(E), over, E < 0))
    return right, wrong

def draw(entry, r, tpl):
    a, b = signed(r, 1, 14), signed(r, 1, 11)
    complex_ = r.random() < 0.7
    c = r.randint(1, 17) * (1 if (a > 0) == complex_ else -1)       # ac > 0 to make D < 0 likely
    if not complex_ and r.random() < 0.5:
        c = signed(r, 1, 17)
    D = b * b - 4 * a * c
    need((D < 0) == complex_ and D and radicals.squarefree(abs(D))[1] != 1 and abs(D) <= 600)
    right, wrong = solutions(a, b, c)
    wrong = list(dict.fromkeys(w for w in wrong if w != right))
    need(len(wrong) >= 3)
    first, rest = wrong[:2], wrong[2:]                              # the sign and the i, always; one more at random
    choices, answer = gen.lettered(r, right, first + [r.choice(rest)])
    prompt = gen.written((a, "x^2"), (b, "x"), (c, "")) + " = 0"
    return dict(prompt=prompt, choices=choices, answer=answer)

def roots(choice):
    left, _, right = choice.partition("plus.minus")
    p = to_sympy(left, imaginary=True) if left.strip() else 0
    q = to_sympy(right, imaginary=True)
    return {sp.nsimplify(sp.expand(p + q)), sp.nsimplify(sp.expand(p - q))}

def solves(prompt, choice):
    x = sp.Symbol("x")
    l, rhs = prompt.split("=")
    want = set(sp.solve(sp.Eq(to_sympy(l), to_sympy(rhs)), x))
    got = roots(choice)
    return len(want) == len(got) == 2 and all(any(sp.simplify(g - w) == 0 for w in want) for g in got)

def check(p):
    try:
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if solves(p["prompt"], c)]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    return f"{display(p['prompt'])} \\\n    {gen.choices_typst([display(dfrac(c)) for c in p['choices']], 'linear')}"

def answer_typst(p):
    return "; ".join(f"{a}. {display(dfrac(c))}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))

def text(p):
    return plain(p["prompt"]) + "   " + gen.choices_text(p["choices"], lambda c: plain(c).replace("plus.minus", "±"))

def answer_text(p):
    return gen.choice_answer_typst(p).replace("plus.minus", "±")

def height(p):
    return 1.0

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new equation; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
