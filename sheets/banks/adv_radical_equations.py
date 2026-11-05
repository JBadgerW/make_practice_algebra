"""Radical equations (Advanced Math), from Lesson 6 (problem set 6,
~/Documents/adv_math/problem_sets/ps_006/radical_equations.typ) and its deck.

The set's ten problems are four types:

    1  (1)     a cube root:                          root(3, x - 5) - 2 = 2
    2  (5-6)   one radical and the root of a number:  sqrt(2x - 7) + sqrt(25) = 7
    3  (2-4)   two radicals, sqrt(s - k) + sqrt(s) = n
    4  (7-10)  two radicals with a coefficient:      sqrt(3x - 5) + sqrt(3x) = 5,
               sqrt(3x + 6) + sqrt(3x - 1) = 7

The set's choices: isolate a radical, then raise both sides to its power
(the cube for a cube root); with two radicals, isolate one, square, isolate
the other, and square again. Type 2 sits beside Type 4 on purpose:
sqrt(2x - 7) + sqrt(25) = 7 looks like sqrt(2x - 7) + sqrt(2x) = 7, but
sqrt(25) is only 5, so one squaring does it. Every answer checks in the
original equation (the deck checks each one: squaring can add a solution),
and the two-radical answers come from whole-number radicals: sqrt(49) and
sqrt(1) in sqrt(s - 48) + sqrt(s) = 8.

The key writes the solution in the problem's letter, s = 49; it may be a
fraction, x = 11/2.

check() puts the key's value into the original equation and requires both
sides to be equal exactly (a radicand below zero fails). The left side
increases with the unknown in every type, so that value is the only solution.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "sqrt(s - 48) + sqrt(s) = 8"
    answer  "s = 49"
"""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from .. import gen
from ..gen import need
from ..check import TR, to_sympy, simplest_form
from ..typmath import tx

NAME = FAMILY = "adv_radical_equations"
FIXED = False
TITLE = "Radical Equations"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="A Cube Root",
         look="A cube root and numbers.",
         move="Get the cube root alone. Cube both sides, solve, and check."),
    dict(key="2", title="One Radical and the Root of a Number",
         look="A radical with the unknown, and the square root of a number, like √25.",
         move="The root of the number is a number: √25 = 5. Get the radical alone, square both sides once, "
              "solve, and check.", space="1.25in"),
    dict(key="3", title="Two Radicals: √(s − k) + √s",
         look="Two radicals, one of them the unknown alone: √(s − 48) + √s = 8.",
         move="Get √(s − 48) alone and square; the s terms cancel. Get √s alone and square again. Check.",
         space="1.75in"),
    dict(key="4", title="Two Radicals with a Coefficient",
         look="Two radicals with the same multiple of the unknown: √(3x − 5) + √(3x) = 5.",
         move="Get one radical alone and square; the 3x terms cancel. Get the other radical alone and square "
              "again. Check.", space="1.75in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Reading an equation: Typst math with sqrt(...) and root(3, ...)
# ------------------------------------------------------------------
def parse(t, numeric=False):
    """Typst math -> sympy; root(n, e) is the real n-th root, so a cube root of a negative is
    negative (numeric: written sign(e) abs(e)^(1/n), which lambdify can evaluate)."""
    t = t.replace("−", "-")
    names = {n: sp.Symbol(n) for n in re.findall(r"\b[a-z]\b", t)}
    real = ((lambda n, e: sp.sign(e) * sp.Abs(e) ** sp.Rational(1, n)) if numeric
            else (lambda n, e: sp.real_root(e, n)))
    names.update(sqrt=sp.sqrt, root=real)
    return parse_expr(t, transformations=TR, local_dict=names)

def letter_of(prompt):
    names = set(re.findall(r"\b[a-z]\b", prompt))
    if len(names) != 1:
        raise ValueError("an equation in one letter")
    return sp.Symbol(names.pop())

def holds(prompt, v):
    """The equation is true, exactly, when its letter is v."""
    x = letter_of(prompt)
    left, right = (parse(s).subs(x, v) for s in prompt.split("="))
    if any(a.has(sp.I) for a in (left, right)):  # a radicand below zero
        return False
    return sp.simplify(left - right) == 0

def answer_of(prompt):
    """Solve an edited prompt: sympy's real solutions that check."""
    x = letter_of(prompt)
    left, right = (parse(s) for s in prompt.split("="))
    try:
        found = [v for v in sp.solve(sp.Eq(left, right), x) if v.is_real and holds(prompt, v)]
    except NotImplementedError:                # sympy can't solve a real cube root: the left side
        l, r = (parse(s, numeric=True) for s in prompt.split("="))   # increases: halve an interval, check exactly
        f = sp.lambdify(x, l - r, [{"sign": lambda v: (v > 0) - (v < 0)}, "math"])
        lo, hi = -1e6, 1e6
        if not f(lo) < 0 < f(hi):
            raise ValueError("no solution found") from None
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
        v = sp.nsimplify(lo, rational=True, tolerance=1e-7)
        found = [v] if holds(prompt, v) else []
    if len(found) != 1:
        raise ValueError("not exactly one solution")
    return f"{x} = {tx(sp.nsimplify(found[0]))}"

def check(p):
    try:
        name, value = (s.strip() for s in p["answer"].split("="))
        v = to_sympy(value)
        good = (name == str(letter_of(p["prompt"])) and v.is_Rational and simplest_form(value)
                and holds(p["prompt"], v))
    except Exception:
        return "unchecked"
    return "checked" if good else "failed"

# ------------------------------------------------------------------
# Writing a prompt
# ------------------------------------------------------------------
def letter(r):
    return sp.Symbol(r.choice(gen.LETTERS))

def P(e):
    return tx(sp.expand(e))

def sq(e):
    return f"sqrt({P(e)})"

def answer(x, v):
    v = sp.Rational(v)
    need(v != 0 and v.q <= 9 and abs(v) <= 200)
    return f"{x} = {tx(v)}"

# ------------------------------------------------------------------
# Type 1 (1): root(3, x - a) - c = d
# ------------------------------------------------------------------
def t1_minus(r):                               # root(3, x - 5) - 2 = 2: x - 5 = 64
    x = letter(r)
    v = r.randint(2, 5)                        # the cube root
    a, c = gen.signed(r, 1, 9), r.randint(1, 9)
    need(v != c)
    return f"root(3, {P(x + a)}) - {c} = {v - c}", answer(x, v ** 3 - a)

def t1_plus_negative(r):                       # root(3, x + 4) + 5 = 2: the cube root is -3
    x = letter(r)
    v = -r.randint(1, 4)
    a, c = gen.signed(r, 1, 9), r.randint(1, 9)
    return f"root(3, {P(x + a)}) + {c} = {v + c}", answer(x, v ** 3 - a)

def t1_coefficient(r):                         # 3 + root(3, 2x + 1) = 6
    x = letter(r)
    v = gen.signed(r, 2, 4)
    k, b = r.randint(2, 4), gen.signed(r, 1, 9)
    need((v ** 3 - b) % k == 0)
    c = r.randint(1, 9)
    need(v + c != 0)
    return f"{c} + root(3, {P(k * x + b)}) = {v + c}", answer(x, sp.Rational(v ** 3 - b, k))

# ------------------------------------------------------------------
# Type 2 (5-6): sqrt(a x + b) + sqrt(q^2) = n
# ------------------------------------------------------------------
def t2_parts(r):
    x = letter(r)
    a, b = r.randint(1, 4), gen.signed(r, 1, 9)
    q, t = r.randint(2, 9), r.randint(1, 5)    # sqrt(q^2) = q; the radical is t
    return x, a, b, q, t, answer(x, sp.Rational(t * t - b, a))

def t2_plus(r):                                # sqrt(2x - 7) + sqrt(25) = 7
    x, a, b, q, t, ans = t2_parts(r)
    return f"{sq(a * x + b)} + sqrt({q * q}) = {q + t}", ans

def t2_number_first(r):                        # sqrt(9) + sqrt(3x + 1) = 7
    x, a, b, q, t, ans = t2_parts(r)
    return f"sqrt({q * q}) + {sq(a * x + b)} = {q + t}", ans

def t2_minus(r):                               # sqrt(3x + 1) - sqrt(9) = 1
    x, a, b, q, t, ans = t2_parts(r)
    need(t > q)
    return f"{sq(a * x + b)} - sqrt({q * q}) = {t - q}", ans

# ------------------------------------------------------------------
# Type 3 (2-4): sqrt(s - k) + sqrt(s) = n, with sqrt(s) = m and sqrt(s - k) = j whole numbers
# ------------------------------------------------------------------
def t3_parts(r):
    x = letter(r)
    m, j = r.randint(2, 9), r.randint(1, 8)
    return x, m, j

def t3_minus(r):                               # sqrt(s - 48) + sqrt(s) = 8: s = 49
    x, m, j = t3_parts(r)
    need(m > j)
    return f"{sq(x - (m * m - j * j))} + sqrt({x}) = {m + j}", answer(x, m * m)

def t3_plus(r):                                # sqrt(s + 9) + sqrt(s) = 9: s = 16
    x, m, j = t3_parts(r)
    need(j > m)
    return f"{sq(x + (j * j - m * m))} + sqrt({x}) = {m + j}", answer(x, m * m)

def t3_bare_first(r):                          # sqrt(s) + sqrt(s - 27) = 9
    x, m, j = t3_parts(r)
    need(m != j)
    return f"sqrt({x}) + {sq(x + (j * j - m * m))} = {m + j}", answer(x, m * m)

# ------------------------------------------------------------------
# Type 4 (7-10): sqrt(a x + b) + sqrt(a x) = n, and sqrt(a x + b) + sqrt(a x + c) = n
# ------------------------------------------------------------------
def t4_bare_parts(r):
    """sqrt(a x + b), sqrt(a x), n, and the answer: a x = m^2, a whole x; sqrt(a x + b) = j."""
    x = letter(r)
    a = r.randint(2, 5)
    m = r.choice([n for n in range(1, 9) if (n * n) % a == 0])
    j = r.choice([n for n in range(1, 9) if n != m])
    return sq(a * x + j * j - m * m), sq(a * x), m + j, answer(x, sp.Rational(m * m, a))

def t4_bare(r):                                # sqrt(3x - 5) + sqrt(3x) = 5: 3x = 9
    other, bare, n, ans = t4_bare_parts(r)
    return f"{other} + {bare} = {n}", ans

def t4_both_constants(r):                      # sqrt(3x + 6) + sqrt(3x - 1) = 7: 3x = 10
    x = letter(r)
    a = r.randint(2, 5)
    j, m = r.sample(range(1, 8), 2)            # the two radicals, at the solution
    u = r.randint(2, 30)                       # a x at the solution
    b, c = j * j - u, m * m - u
    need(b != 0 and c != 0 and u not in (j * j, m * m))
    return f"{sq(a * x + b)} + {sq(a * x + c)} = {m + j}", answer(x, sp.Rational(u, a))

def t4_bare_first(r):                          # sqrt(2x) + sqrt(2x + 20) = 10
    other, bare, n, ans = t4_bare_parts(r)
    return f"{bare} + {other} = {n}", ans

TEMPLATES = {
    "1": [t1_minus, t1_plus_negative, t1_coefficient],
    "2": [t2_plus, t2_number_first, t2_minus],
    "3": [t3_minus, t3_plus, t3_bare_first],
    "4": [t4_bare, t4_both_constants, t4_bare_first],
}

def draw(entry, r, tpl):
    prompt, ans = TEMPLATES[entry][tpl](r)
    return dict(prompt=prompt, answer=ans)

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

typst, answer_typst, text, answer_text, height = gen.shown()
height = lambda p: 0.4

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "sqrt(s - 48) + sqrt(s) = 8", "s = 49",
    parse=lambda t: [parse(side) for side in t.split("=")])

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
