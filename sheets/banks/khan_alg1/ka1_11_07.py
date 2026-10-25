"""Khan Algebra 1, Lessons 11-7 and 11-8: Simplify square roots, without and
with a variable, from the old app's Alg1_11_07 and Alg1_11_08 (sixteen
and fourteen generated slots).

sqrt(72) = 6 sqrt(2); sqrt(72 x^5) = 6 x^2 sqrt(2 x). The radicand is
k^2 m, at most 450, with k 2 to 15 and m square-free. The old list of
"not perfect squares" for m held 8 and 12, so a key like 3 sqrt(8) was
never finished; m is square-free here. The variable's exponent is 1 to 9.
11-8 is its own bank (ka1_11_08) built from this one.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "sqrt(72 x^5)"
    answer  "6 x^2 sqrt(2 x)"
check() compares the values (letters positive) and reads the answer's
form with radicals.simplest: nothing left inside the root to take out.
"""
from ... import gen, radicals
from ...gen import need
from ...check import same_value, to_sympy
from . import courses

NAME = FAMILY = "ka1_11_07"
FIXED = False
TITLE = "Lesson 11-7: Simplify square roots"
INSTRUCTIONS = "Simplify. Remove all perfect squares from inside the square root."
COURSES = courses(11)
SQUAREFREE = (2, 3, 5, 6, 7, 10, 11, 13, 14, 15)

TYPES = [
    dict(key="1", title="Numbers",
         look="The square root of a number with a perfect-square factor.",
         move="Find the largest perfect square that divides the number. Its root comes out front; the rest stays inside."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def radicand(r):
    k, m = r.randint(2, 15), r.choice(SQUAREFREE)
    need(k * k * m <= 450)
    return k * k * m

def draw_with(powers):
    def draw(entry, r, tpl):
        n = radicand(r)
        pw = powers(r)
        inside = radicals.monomial(n, pw)
        return dict(prompt=f"sqrt({inside})", answer=radicals.written(*radicals.simplify(1, n, pw)))
    return draw

def check(p):
    try:
        ok = same_value(p["prompt"], p["answer"]) and radicals.simplest(p["answer"])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

def answer_of(prompt):
    e = to_sympy(prompt[len("sqrt("):-1])
    c, rest = e.as_coeff_Mul()
    return radicals.written(*radicals.simplify(1, int(c), {str(b): int(x) for b, x in rest.as_powers_dict().items() if b != 1}))

draw = draw_with(lambda r: {})
generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)
typst, answer_typst, text, answer_text, height = gen.shown()
edit_text, from_edit, answer_edit_text, with_answer = gen.edits(answer_of, check, "sqrt(72)", "6 sqrt(2)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
