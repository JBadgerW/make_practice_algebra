"""Khan Algebra 1, Lesson 11-9: Simplify square-root expressions, from the
old app's Alg1_11_09 (fifteen of Khan's, without answers).

Khan's are one root with two letters (sqrt(75 y z^2), sqrt(81 a^5 b)) or
a product of two or three roots of one letter (2 sqrt(7 x) · 3 sqrt(14 x^2),
sqrt(12) · sqrt(y^3) · sqrt(6 y)), whose radicands share factors so the
product has a perfect square to take out.

A problem: dict(type, prompt, answer, source), in Typst math; a product is
stored with *, shown as a dot.
    prompt  "2 sqrt(7 x) * 3 sqrt(14 x^2)"
    answer  "42 x sqrt(2 x)"
check() compares the values (letters positive) and reads the answer's
form with radicals.simplest.
"""
from ... import gen, radicals
from ...gen import need
from ...check import same_value, to_sympy
from ...typmath import display, dfrac, text as plain
from . import courses

NAME = FAMILY = "ka1_11_09"
FIXED = False
TITLE = "Lesson 11-9: Simplify square-root expressions"
INSTRUCTIONS = "Simplify. Remove all perfect squares from inside the square roots. Assume each variable is positive."
COURSES = courses(11)
RADICANDS = (2, 3, 5, 6, 7, 8, 10, 12, 14, 15, 18, 20, 21, 24, 30, 35, 40)     # Khan's

TYPES = [
    dict(key="1", title="One Root",
         look="One square root of a number and two letters.",
         move="Take out the largest perfect square from the number, and half of each even exponent; "
              "an odd exponent leaves one factor inside."),
    dict(key="2", title="Multiply Roots",
         look="Two or three square roots multiplied.",
         move="Multiply the numbers outside, and multiply everything inside into one root. Then simplify it."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def t1_one_root(r):                           # sqrt(72 x^3 z^3)
    k, m = r.randint(2, 9), r.choice((1, 2, 3, 5, 6, 7, 10, 14, 15, 21, 42))
    x, y = sorted(r.sample(gen.LETTERS, 2))
    pw = {x: r.randint(1, 6), y: r.randint(1, 6)}
    n = k * k * m
    need(n <= 200)                                # Khan's: 75, 81, 72, 42
    return f"sqrt({radicals.monomial(n, pw)})", (1, n, pw)

def t2_roots(r, count):                       # 2 sqrt(7 x) * 3 sqrt(14 x^2)
    v = r.choice(gen.LETTERS)
    c, n, e, parts = 1, 1, 0, []
    for _ in range(count):
        ci = r.randint(2, 6) if count == 2 else 1
        ni = r.choice(RADICANDS + ((1,) if count == 3 else ()))
        ei = r.randint(0, 4)
        need(ni != 1 or ei)
        c, n, e = c * ci, n * ni, e + ei
        root = radicals.monomial(ni, {v: ei})
        parts.append(f"{'' if ci == 1 else f'{ci} '}sqrt({root})")
    need(radicals.squarefree(n)[0] > 1 and n <= 2000 and c * radicals.squarefree(n)[0] <= 150)
    return " * ".join(parts), (c, n, {v: e} if e else {})

TEMPLATES = {"1": [t1_one_root], "2": [lambda r: t2_roots(r, 2), lambda r: t2_roots(r, 3)]}

def draw(entry, r, tpl):
    prompt, (c, n, pw) = TEMPLATES[entry][tpl](r)
    return dict(prompt=prompt, answer=radicals.written(*radicals.simplify(c, n, pw)))

def check(p):
    try:
        ok = same_value(p["prompt"].replace("*", ""), p["answer"]) and radicals.simplest(p["answer"])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

def answer_of(prompt):
    e = to_sympy(prompt.replace("*", "")) ** 2                  # the square of the whole product: c^2 n x^k
    num, rest = e.as_coeff_Mul()
    k, m = radicals.squarefree(int(num))
    powers = {str(b): int(x) for b, x in rest.as_powers_dict().items() if b != 1}
    return radicals.written(*radicals.simplify(k, m, powers))

def typst(p, gap="0.3em"):
    return display(dfrac(p["prompt"].replace("*", "dot")))

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    return plain(p["prompt"].replace("*", "·"))

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.3

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "2 sqrt(7 x) * 3 sqrt(14 x^2)", "42 x sqrt(2 x)")

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
