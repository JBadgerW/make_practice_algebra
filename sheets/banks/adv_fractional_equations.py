"""Fractional equations (Advanced Math), from Lesson 6 (problem set 6,
~/Documents/adv_math/problem_sets/ps_006/fractional_equations.typ) and its deck.

The set's nine problems are three types:

    1  (1-6)  numbers and one fraction with the unknown below:  4/7 + 3/(x + 2) = 5/3
              (6: a number factor in that denominator, 1/(2x - 8)). Clearing gives a
              linear equation; the answer is usually a fraction, 17/23.
    2  (7)    denominators x and x - 1, already factored:  (x + 1)/(x - 1) - 1/x = 2/(x(x - 1))
    3  (8-9)  trinomial denominators to factor:  (x - 6)/(x^2 - 9x + 20) = 2/(x - 4) - x/(x - 5)

The set's choice: the lesson writes the unacceptable values first ("x != -2"),
then multiplies by the least common multiple of the denominators. In Types 2
and 3 clearing gives a quadratic, and one of its two roots is an unacceptable
value, so writing them first is what catches it. Type 1 never lands on one.

The key writes the solution, x = 17/23 (the unknown is the problem's letter),
and in Types 2 and 3 names the root that is excluded: x = -1 (x = 1 is excluded).

check() is independent of the build: it clears the equation with sympy, finds
every root of what is left, drops those that make a denominator zero, and
requires the key's value to be the one root left, in lowest terms.

A problem: dict(type, prompt, answer, source), in Typst math.
    prompt  "4/7 + 3/(x + 2) = 5/3"
    answer  "x = 17/23"
"""
import functools, re
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, simplest_form, _evaluated
from ..typmath import tx, fr, display, dfrac, text as plain

NAME = FAMILY = "adv_fractional_equations"
FIXED = False
TITLE = "Fractional Equations"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="One Fraction with the Unknown Below",
         look="Number fractions and one fraction with the unknown in its denominator.",
         move="Write the value the unknown can't be. Multiply every term by the least common multiple of the "
              "denominators, cancel, and solve the linear equation.", space="1.25in"),
    dict(key="2", title="Factored Denominators",
         look="Denominators like x, x − 1, and x(x − 1).",
         move="Write the values the unknown can't be. Multiply by the least common multiple, solve the "
              "quadratic, and reject a root that is one of those values.", space="1.75in", width="full"),
    dict(key="3", title="Trinomial Denominators",
         look="A denominator like x² − 9x + 20.",
         move="Factor each trinomial and write the values the unknown can't be. Multiply by the least common "
              "multiple, solve the quadratic, and reject a root that is one of those values.",
         space="2in", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Solving, independently of how a problem was built
# ------------------------------------------------------------------
def letter_of(prompt):
    names = set(re.findall(r"\b[a-z]\b", prompt))
    if len(names) != 1:
        raise ValueError("an equation in one letter")
    return sp.Symbol(names.pop())

@functools.lru_cache(maxsize=512)
def roots(prompt):
    """(the letter, the solutions, the excluded roots): every root of the cleared
    equation, split by whether it makes a denominator zero."""
    x = letter_of(prompt)
    left, right = prompt.split("=")
    e = to_sympy(left) - to_sympy(right)
    lcm = sp.Integer(1)
    for t in sp.Add.make_args(e):              # the least common multiple of the denominators
        lcm = sp.lcm(lcm, sp.denom(sp.together(t)))
    n = sp.expand(sp.cancel(lcm * e))          # the equation, cleared
    if not n.is_polynomial(x) or not n.has(x):
        raise ValueError("no single solution")
    found = [v for v in sp.roots(sp.Poly(n, x)) if v.is_real]
    ok = sorted(v for v in found if lcm.subs(x, v) != 0)
    return x, tuple(ok), tuple(sorted(v for v in found if v not in ok))

def answer_of(prompt):
    x, ok, _ = roots(prompt)
    if len(ok) != 1:
        raise ValueError("not exactly one solution")
    return f"{x} = {tx(ok[0])}"

def check(p):
    try:
        x, ok, _ = roots(p["prompt"])
        name, value = (s.strip() for s in p["answer"].split("="))
        good = name == str(x) and len(ok) == 1 and to_sympy(value) == ok[0] and simplest_form(value)
    except Exception:
        return "unchecked"
    return "checked" if good else "failed"

def excluded_note(p):
    """The roots the key names as excluded: "x = 1"; empty if none."""
    try:
        x, _, bad = roots(p["prompt"])
    except Exception:
        return []
    return [f"{x} = {tx(b)}" for b in bad]

# ------------------------------------------------------------------
# Writing a prompt
# ------------------------------------------------------------------
def letter(r):
    return sp.Symbol(r.choice(gen.LETTERS))

def P(e):
    return tx(sp.expand(e))

def num(p, q):
    """p/q as written in the prompt, in lowest terms."""
    g = sp.Rational(p, q)
    return str(g.p) if g.q == 1 else f"{g.p}/{g.q}"

def proper(r, lo=2, hi=9):
    """A fraction p/q in lowest terms, not a whole number."""
    q = r.randint(lo, hi)
    p = r.choice([n for n in range(1, 2 * q) if sp.gcd(n, q) == 1 and n % q])
    return p, q

def nice(v, big=40):
    """The set's answers: a whole number or a fraction like 17/23, -38/13."""
    v = sp.Rational(v)
    need(v != 0 and abs(v.p) <= big * 3 and v.q <= big)

# ------------------------------------------------------------------
# Type 1 (1-6): a number fraction, one fraction with the unknown, a number fraction
# ------------------------------------------------------------------
def t1_core(r, x, sign, den, k):
    """p/q +- k/den = s/t, solved for x (den is linear in x)."""
    p, q = proper(r)
    s, t = proper(r)
    need(q != t and sp.Rational(p, q) != sp.Rational(s, t))
    lhs = sp.Rational(p, q) + sign * k / den
    v = sp.solve(sp.Eq(lhs, sp.Rational(s, t)), x)
    need(len(v) == 1)
    nice(v[0])
    op = " + " if sign > 0 else " - "
    return f"{num(p, q)}{op}{fr(str(k), P(den))} = {num(s, t)}"

def t1_plus(r):                                # 4/7 + 3/(x + 2) = 5/3
    x = letter(r)
    return t1_core(r, x, 1, x + gen.signed(r, 1, 9), r.randint(1, 5))

def t1_minus(r):                               # 5/3 - 2/(x - 4) = 1/2
    x = letter(r)
    return t1_core(r, x, -1, x + gen.signed(r, 1, 9), r.randint(1, 5))

def t1_unit(r):                                # 1/(x - 7) + 1/4 = 1/3: a whole-number answer
    x = letter(r)
    q, s = r.choice([(q, s) for q in range(2, 10) for s in range(2, 10)
                     if q != s and (q * s) % (q - s) == 0])
    a = gen.signed(r, 1, 9)
    v = sp.Rational(q * s, q - s) - a
    nice(v)
    return f"{fr('1', P(x + a))} + 1/{q} = 1/{s}"

def t1_number_factor(r):                       # 1/(2x - 8) + 1/5 = 1/7
    x = letter(r)
    c, a = r.randint(2, 3), gen.signed(r, 1, 6)
    q, s = r.sample(range(2, 10), 2)
    den = c * x + c * a                        # c (x + a), written multiplied out
    v = sp.solve(sp.Eq(1 / den + sp.Rational(1, q), sp.Rational(1, s)), x)
    need(len(v) == 1)
    nice(v[0])
    return f"{fr('1', P(den))} + 1/{q} = 1/{s}"

# ------------------------------------------------------------------
# Type 2 (7): (x + b)/(x - c) - d/x = e/(x (x - c)); one root is c or 0
# ------------------------------------------------------------------
def t2_build(r, extraneous_zero, swapped=False):
    x = letter(r)
    c = gen.signed(r, 1, 5)
    s = gen.signed_except(r, 1, 6, c)          # the solution
    d = r.randint(1, 4)
    # clearing: x (x + b) - d (x - c) = e, i.e. x^2 + (b - d) x + d c - e = 0
    bad = 0 if extraneous_zero else c
    b = d - bad - s                            # the roots add to bad + s
    e = d * c - bad * s                        # and multiply to bad s
    need(e > 0 and s != 0)
    first, third = fr(P(x + b), P(x - c)), fr(str(e), f"{x} ({P(x - c)})")
    if swapped:                                # third + d/x = first
        return f"{third} + {d}/{x} = {first}"
    return f"{first} - {d}/{x} = {third}"

def t2_excludes_c(r):                          # (x + 1)/(x - 1) - 1/x = 2/(x (x - 1)): x = 1 is excluded
    return t2_build(r, False)

def t2_excludes_zero(r):                       # the other root is 0
    return t2_build(r, True)

def t2_swapped(r):                             # d/x + ... on the other side: e/(x (x - c)) + d/x = (x + b)/(x - c)
    return t2_build(r, r.random() < 0.5, swapped=True)

# ------------------------------------------------------------------
# Type 3 (8-9): trinomial denominators
# ------------------------------------------------------------------
def t3_one_trinomial(r):                       # (x - 6)/(x^2 - 9x + 20) = 2/(x - 4) - x/(x - 5)
    x = letter(r)
    p, q = r.sample([n for n in range(-6, 7) if n], 2)
    e = r.choice((p, q))                       # the excluded root
    s = gen.signed_except(r, 1, 9, p, q)       # the solution
    A = r.randint(1, 4)
    # clearing: m x + n0 = A (x - q) - x (x - p): x^2 + (m - A - p) x + n0 + A q = 0
    m = A + p - e - s
    n0 = e * s - A * q
    need(0 < m <= 9 and abs(n0) <= 20)
    D = sp.expand((x - p) * (x - q))
    return f"{fr(P(m * x + n0), P(D))} = {fr(str(A), P(x - p))} - {fr(str(x), P(x - q))}"

def t3_two_trinomials(r):                      # (x + 2)/(x^2 - 3x + 2) - (x - 6)/(x^2 - 5x + 6) = 1/(x - 1)
    x = letter(r)
    p, q, t = r.sample([n for n in range(-5, 6) if n], 3)
    e = q          # the shared factor's root: were it p or t, a numerator would cancel its own denominator
    s = gen.signed_except(r, 1, 9, p, q, t)
    # clearing: (x + a)(x - t) - (x + b)(x - p) = (x - q)(x - t)
    #   roots add to p + q + a - b, multiply to q t + a t - b p
    top = e * s - q * t - p * (e + s - p - q)
    need(top % (t - p) == 0)
    a = top // (t - p)
    b = a - (e + s - p - q)
    need(a != 0 and b != 0 and abs(a) <= 9 and abs(b) <= 9)
    D1, D2 = sp.expand((x - p) * (x - q)), sp.expand((x - q) * (x - t))
    return f"{fr(P(x + a), P(D1))} - {fr(P(x + b), P(D2))} = {fr('1', P(x - p))}"

def t3_swapped(r):                             # the one-trinomial problem, its sides swapped
    left, right = t3_one_trinomial(r).split(" = ")
    return f"{right} = {left}"

TEMPLATES = {
    "1": [t1_plus, t1_minus, t1_unit, t1_number_factor],
    "2": [t2_excludes_c, t2_excludes_zero, t2_swapped],
    "3": [t3_one_trinomial, t3_two_trinomials, t3_swapped],
}

def fractions_reduced(prompt):
    """No fraction in the prompt reduces by a factor with the letter."""
    found = []
    def walk(e):
        if isinstance(e, sp.Mul):
            over = [a for a in e.args if isinstance(a, sp.Pow) and a.exp == -1]
            if over:
                top = sp.Mul(*[_evaluated(a) for a in e.args if not any(a is o for o in over)])
                found.append((top, sp.Mul(*[_evaluated(o.base) for o in over])))
                return
        for a in e.args:
            walk(a)
    for side in prompt.split("="):
        walk(to_sympy(side, evaluate=False))
    return all(sp.gcd(n, d).is_Number for n, d in found)

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r)
    need(fractions_reduced(prompt))
    try:
        _, ok, bad = roots(prompt)
    except ValueError:
        raise gen.Redraw
    need(len(ok) == 1 and len(bad) == (0 if entry == "1" else 1))
    nice(ok[0])
    return dict(prompt=prompt, answer=answer_of(prompt))

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    return display(dfrac(p["prompt"]))

def answer_typst(p):
    note = excluded_note(p)
    tail = "".join(f" #h(0.6em) ($display({b})$ is excluded)" for b in note)
    return display(dfrac(p["answer"])) + tail

def text(p):
    return plain(p["prompt"])

def answer_text(p):
    return plain(p["answer"]) + "".join(f"  ({plain(b)} is excluded)" for b in excluded_note(p))

def height(p):
    return 0.55

edit_text, from_edit, answer_edit_text, with_answer = gen.edits(
    answer_of, check, "4/7 + 3/(x + 2) = 5/3", "x = 17/23",
    parse=lambda t: [to_sympy(side) for side in t.split("=")])

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
