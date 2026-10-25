"""Literal equations with fractions (Advanced Math), from the old app's set
AdvMath_00_04_literal_eq: its eleven equations, sorted by where the unknown
is: in a numerator, in a denominator, or in two places.

As in the old set, each problem draws its letters at random and gives them
to the equation's roles in alphabetical order. The key's answer is
"unknown = one fraction", in lowest terms, multiplied out.

A problem: dict(type, prompt, target, answer, source), like the Algebra 1
literal bank's: prompt is the equation in Typst math, target the letter to
solve for, answer "g = (b n p r)/(a p + d n)". check() works as that bank's
does: the unknown must be gone from the right side, and substituting the
answer into the equation must make it true at random values of the letters.
"""
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, holds, syms_of, simplest_form
from ..typmath import single, fr, display, dfrac, text as plain

NAME = FAMILY = "adv_literal"
FIXED = False
TITLE = "Literal Equations with Fractions"
INSTRUCTIONS = "Solve each equation for the indicated variable."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="The Unknown in a Numerator",
         look="A fraction times a difference of fractions; the unknown is on top of one of them.",
         move="Clear the fraction outside the parentheses by multiplying both sides. Then add to get the "
              "unknown's term alone, and multiply by its denominator."),
    dict(key="2", title="The Unknown in a Denominator",
         look="The unknown is in the denominator of a fraction inside parentheses.",
         move="Divide by the factor outside the parentheses. Get the unknown's fraction alone, combine the "
              "other side into one fraction, and take the reciprocal of both sides.", space="1.5in"),
    dict(key="3", title="The Unknown in Two Places",
         look="The unknown is in the numerator and in the denominator of one fraction.",
         move="Multiply both sides by the denominator. Gather the unknown's terms on one side, factor the "
              "unknown out, and divide."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"], p["target"])

def k_(c, body):
    """c times body as written: k_(1, "t") = "t", k_(3, "t") = "3 t"."""
    return body if c == 1 else f"{c} {body}"

def roles(r, n):
    """n letters at random, in alphabetical order, for the roles in theirs."""
    return gen.letters(r, n)

# ------------------------------------------------------------------
# Type 1: the unknown in a numerator (F_15, 02_17)
# ------------------------------------------------------------------
def f15(r):                                   # k^e1 = 1/(b c) (x/c1 - c2 y^e2/d); x
    b, c, d, k, x, y = roles(r, 6)
    c1, c2, e1, e2 = r.randint(2, 9), r.randint(2, 9), r.randint(2, 4), r.randint(2, 4)
    return f"{k}^{e1} = {fr('1', f'{b} {c}')} ({fr(x, str(c1))} - {fr(f'{c2} {y}^{e2}', d)})", x

def s0217(r):                                 # c1 t = 1/(c2 s^e) ((c3 z)/c4 - (c5 m)/n); z
    m, n, s, t, z = roles(r, 5)
    c1, c2, c5, e = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6), r.randint(2, 4)
    c3, c4 = gen.reduced(r.randint(2, 6), gen.except_(r, 2, 6))
    need(c4 != 1)
    return f"{k_(c1, t)} = {fr('1', f'{c2} {s}^{e}')} ({fr(k_(c3, z), str(c4))} - {fr(k_(c5, m), n)})", z

def product_numerator(r):                     # y = (m/c1)(x/a - b); x
    a, b, m, x, y = roles(r, 5)
    return f"{y} = {fr(m, str(r.randint(2, 9)))} ({fr(x, a)} - {b})", x

# ------------------------------------------------------------------
# Type 2: the unknown in a denominator (test_04, D_9, D_10, E_11, E_12,
# 01_16, 03_18, 04_18)
# ------------------------------------------------------------------
def test04(r):                                # a = n (b r/g - d/p); g
    a, b, d, g, n, p, rr = roles(r, 7)
    return f"{a} = {n} ({fr(f'{b} {rr}', g)} - {fr(d, p)})", g

def d9(r):                                    # y = v (a/x + b/(m c)); c
    a, b, c, m, v, x, y = roles(r, 7)
    return f"{y} = {v} ({fr(a, x)} + {fr(b, f'{m} {c}')})", c

def d10(r):                                   # x = p m (1/y + a/(b d)); d
    a, b, d, m, p, x, y = roles(r, 7)
    return f"{x} = {p} {m} ({fr('1', y)} + {fr(a, f'{b} {d}')})", d

def e11(r):                                   # x = k b (1/c - a/x); c
    a, b, c, k, x = roles(r, 5)
    return f"{x} = {k} {b} ({fr('1', c)} - {fr(a, x)})", c

def e12(r):                                   # m c = p (a/(c m) + K/(k c)); k
    a, c, k, m, p = roles(r, 5)
    return f"{m} {c} = {p} ({fr(a, f'{c} {m}')} + {fr(str(r.randint(2, 9)), f'{k} {c}')})", k

def s0116(r):                                 # s^e1 = 1/(d f) (c1 y/c2 - c3 x^e2/g); g
    d, f, g, s, x, y = roles(r, 6)
    c1, c2 = gen.reduced(r.randint(2, 9), r.randint(2, 9))
    need(c2 != 1)
    c3, e1, e2 = r.randint(2, 9), r.randint(2, 4), r.randint(2, 4)
    return f"{s}^{e1} = {fr('1', f'{d} {f}')} ({fr(k_(c1, y), str(c2))} - {fr(f'{c3} {x}^{e2}', g)})", g

def s0318(r):                                 # c1 z = (c2 m/n)(c3 s/t - c4 l/k); t
    k, l, m, n, s, t, z = roles(r, 7)
    c1, c2, c3, c4 = (r.randint(2, 6) for _ in range(4))
    return f"{k_(c1, z)} = {fr(k_(c2, m), n)} ({fr(k_(c3, s), t)} - {fr(k_(c4, l), k)})", t

def s0418(r):                                 # c1 s = (c2 z/m)(a t^2/c3 - c4 m/h); h
    a, h, m, s, t, z = roles(r, 6)
    c1, c2, c3, c4 = (r.randint(2, 6) for _ in range(4))
    return f"{k_(c1, s)} = {fr(k_(c2, z), m)} ({fr(f'{a} {t}^2', str(c3))} - {fr(k_(c4, m), h)})", h

# ------------------------------------------------------------------
# Type 3: the unknown in two places (21_23)
# ------------------------------------------------------------------
def s2123(r):                                 # r = (d + c1)/(c2 d - w); d
    d, rr, w = roles(r, 3)
    c1, c2 = r.randint(1, 5), r.randint(1, 5)
    return f"{rr} = {fr(f'{d} + {c1}', f'{k_(c2, d)} - {w}')}", d

def over_plus(r):                             # y = (a x - c1)/(x + b); x
    a, b, x, y = roles(r, 4)
    return f"{y} = {fr(f'{a} {x} - {r.randint(1, 9)}', f'{x} + {b}')}", x

def two_letters(r):                           # m = (c1 p + q)/(p - c2 q); p
    m, p, q = roles(r, 3)
    c1, c2 = r.randint(2, 6), r.randint(2, 6)
    return f"{m} = {fr(f'{c1} {p} + {q}', f'{p} - {c2} {q}')}", p

TEMPLATES = {
    "1": [f15, s0217, product_numerator],
    "2": [test04, d9, d10, e11, e12, s0116, s0318, s0418],
    "3": [s2123, over_plus, two_letters],
}

def solve(prompt, target):
    """The key's answer: "target = one fraction"; ValueError if there isn't exactly one solution."""
    left, right = prompt.split("=")
    v = syms_of(prompt)[target]
    sols = sp.solve(sp.Eq(to_sympy(left), to_sympy(right)), v)
    if len(sols) != 1:
        raise ValueError(f"{len(sols)} solutions for {target}")
    return f"{target} = {single(sols[0])}"

def draw(entry, r, tpl):
    prompt, target = TEMPLATES[entry][tpl](r)
    answer = solve(prompt, target)
    need(simplest_form(answer.split("=", 1)[1]))
    return dict(prompt=prompt, target=target, answer=answer)

def check(p):
    lhs, sep, rhs = p["answer"].partition("=")
    if not sep or lhs.strip() != p["target"]:
        return "unchecked"
    try:
        rhs = rhs.strip()
        if syms_of(p["prompt"])[p["target"]] in to_sympy(rhs).free_symbols:
            return "failed"                           # the unknown is still in it
        holds(p["prompt"], p["prompt"], p["target"], rhs)
        return "checked" if simplest_form(rhs) else "failed"
    except AssertionError:
        return "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing and editing, as the Algebra 1 literal bank: "equation ; letter"
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    return f"{display(dfrac(p['prompt']))}; #h({gap}) ${p['target']}$"

def answer_typst(p):
    return display(dfrac(p["answer"]))

def text(p):
    return f"{plain(p['prompt'])};  {p['target']}"

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.55

def edit_text(p):
    return f"{p['prompt']} ; {p['target']}"

def from_edit(t, old):
    eq, _, target = t.replace("−", "-").partition(";")
    eq, target = " ".join(eq.split()), target.strip() or old["target"]
    if eq.count("=") != 1:
        raise ValueError("write one equation, then ; and the letter: y = v (a/x + b/(m c)) ; c")
    try:
        syms = syms_of(eq)
    except Exception:
        raise ValueError("write the equation in Typst math, like y = v (a/x + b/(m c)) ; c") from None
    if target not in syms:
        raise ValueError(f"{target} isn't in the equation")
    new = dict(old, prompt=eq, target=target, source="edited")
    try:
        new["answer"] = solve(eq, target)
    except Exception:
        new["answer"] = old["answer"] if old["target"] == target else f"{target} = ?"
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
