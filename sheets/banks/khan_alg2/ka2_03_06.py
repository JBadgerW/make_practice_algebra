"""Khan Algebra 2, Lesson 3-6: Factorization with substitution, from the old
app's Alg2_03_06 (sixteen of Khan's, without answers; each has exactly one
right choice, checked).

We can factor (x - 5)^2 + 2 y^3 (x - 5) + y^6 as (U + V)^2. (a) What are U
and V? Choose 1 of six: Khan's, U or its square (or a slip, 8 x^3 for
4 x^3) with V or its square (or a slip). (b) Factor the expression:
(x - 5 + y^3)^2. The patterns are (U + V)^2, (U - V)^2, and (U + V)(U - V);
U and V are k x^n or (x + h), and y^m, (y + h), or a number, at most one
of them a binomial, with no common factor to take out first.

A problem: dict(type, prompt, pattern, choices, answer, source).
    prompt   "(x - 5)^2 + 2 y^3 (x - 5) + y^6"    pattern "(U+V)^2"
    choices  ["$U = (x - 5)$ and $V = y$", ...]
    answer   "C; (x - 5 + y^3)^2"
check(): (a) exactly the answer's choice makes the pattern equal the
expression; (b) the factored form is the same polynomial, factored
completely over the integers.
"""
import math, re
import sympy as sp
from ... import gen, poly
from ...gen import need, signed
from ...check import to_sympy
from ...typmath import display, text as plain
from . import courses
from .patterns import mono, binomial, square_text, difference_text, sum_text

NAME = FAMILY = "ka2_03_06"
FIXED = False
TITLE = "Lesson 3-6: Factorization with substitution"
INSTRUCTIONS = "U and V are either constant integers or single-variable expressions."
COURSES = courses(3)
PATTERNS = {"(U+V)^2": 1, "(U-V)^2": -1, "(U+V)(U-V)": 0}

TYPES = [
    dict(key="1", title="Find U and V, Then Factor",
         look="An expression and the pattern it fits: (U + V)^2, (U - V)^2, or (U + V)(U - V).",
         move="U^2 and V^2 are the squares in the expression, so U and V are their square roots: halve the "
              "exponents, take the root of the numbers. Then write the pattern with U and V.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def slip(r, P):
    """A wrong U or V, Khan's: the number doubled (8 x^3 for 4 x^3, 14 for 7) or the exponent wrong."""
    options = [mono(2 * P.k, P.v, P.n)]
    if P.v and P.n > 1:
        options.append(mono(P.k, P.v, 1))
    if P.v:
        options.append(mono(P.k, P.v, 2 * P.n))
    return r.choice(options)

def options(r, P, three):
    return [P, P.power(2)] + ([slip(r, P)] if three else [])

def choice(U, V):
    return f"$U = {U.text()}$ and $V = {V.text()}$"

def draw(entry, r, tpl):
    pattern = r.choice(list(PATTERNS))
    s = PATTERNS[pattern]
    U = binomial("x", signed(r, 1, 9)) if r.random() < 0.4 else mono(r.randint(1, 9), "x", r.randint(1, 4))
    roll = r.random()
    if roll < 0.3:
        V = mono(r.randint(1, 9))
    elif roll < 0.45 and U.kind == "mono":                          # at most one binomial
        V = binomial("y", signed(r, 1, 5))
    else:
        V = mono(r.randint(1, 6), "y", r.randint(1, 5))
    need(math.gcd(U.k, V.k) == 1)
    prompt = difference_text(U, V) if s == 0 else square_text(U, V, s)
    factored = (f"({sum_text(U, V, 1)}) ({sum_text(U, V, -1)})" if s == 0 else f"({sum_text(U, V, s)})^2")
    need(all(" " in t for t in re.findall(r"\(([^()]*)\)", factored)))       # not (x)^2
    need(poly.completely_factored(factored, prompt))
    us = options(r, U, U.kind == "mono")                            # 2 x 3 choices: the slip on one side
    vs = options(r, V, U.kind == "bin" and V.kind == "mono")
    choices = [choice(u, v) for u in us for v in vs]
    need(len(set(choices)) == 6)
    right = choice(U, V)
    order = sorted(range(6), key=lambda i: r.random())
    choices = [choices[i] for i in order]
    letter = gen.ABC[choices.index(right)]
    return dict(prompt=prompt, pattern=pattern, choices=choices, answer=f"{letter}; {factored}")

CHOICE = re.compile(r"\$U = (.+)\$ and \$V = (.+)\$")

def fits(prompt, pattern, c):
    U, V = [to_sympy(t) for t in CHOICE.fullmatch(c).groups()]
    s = PATTERNS[pattern]
    made = U ** 2 - V ** 2 if s == 0 else (U + s * V) ** 2
    return sp.expand(made - to_sympy(prompt)) == 0

def parts_of(p):
    letter, _, factored = p["answer"].partition(";")
    return letter.strip(), factored.strip()

def check(p):
    try:
        letter, factored = parts_of(p)
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if fits(p["prompt"], p["pattern"], c)]
        ok = right == [letter] and poly.completely_factored(factored, p["prompt"])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def pattern_typst(pattern):
    return pattern.replace("+", " + ").replace("-", " - ")

def typst(p, gap="0.3em"):
    return (f"{display(p['prompt'])} \\\n    We can factor the expression as ${pattern_typst(p['pattern'])}$.\n"
            f"    #parts([What are $U$ and $V$? #pad(left: 1em, top: 0.4em, "
            f"{gen.choices_typst(p['choices'], 'grid')[1:]})], [Factor the expression.])")

def answer_typst(p):
    letter, factored = parts_of(p)
    return f"(a) {letter}. {p['choices'][gen.ABC.index(letter)]} (b) ${factored}$"

def text(p):
    return f"{plain(p['prompt'])} as {p['pattern']}   " + gen.choices_text([c.replace("$", "") for c in p["choices"]])

def answer_text(p):
    letter, factored = parts_of(p)
    return f"(a) {letter}. {p['choices'][gen.ABC.index(letter)].replace('$', '')}  (b) {plain(factored)}"

def height(p):
    return 2.0

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new expression; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    letter, _, factored = t.partition(";")
    letter = letter.strip().upper()
    if letter not in gen.ABC[:len(p["choices"])] or not factored.strip():
        raise ValueError("write the letter, then ; and the factored form: C; (x - 5 + y^3)^2")
    new = dict(p, answer=f"{letter}; {' '.join(factored.replace('−', '-').split())}")
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
