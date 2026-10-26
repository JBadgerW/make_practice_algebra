"""Khan Algebra 2, Lesson 3-9: Geometric series formula, from the old app's
Alg2_03_09 (twelve of Khan's, without answers).

S_n = a (1 - r^n)/(1 - r). Type 1: the first term and the common ratio;
the sum of the first n terms. Type 2: the series written out,
1024 + 512 + 256 + ...; the sum of the first n terms ("Do not round").
Type 3: the sum of the first n terms and the ratio; the first term. The
ratio is a whole number (2 to 5) or a fraction (1/2, 1/3, 2/3, 1/4, 3/4,
some written 0.5, 0.75), and the first term makes every term a whole
number, so every answer is a whole number, as in Khan's.

A problem: dict(type, a, r, n, prompt, answer, source).
    a 64   r "0.75"   n 4   answer "175"
check() computes a (1 - r^n)/(1 - r) exactly (Type 3: solves it for a)
and requires the numbers to be the ones in the prompt.
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need
from . import courses

NAME = FAMILY = "ka2_03_09"
FIXED = False
TITLE = "Lesson 3-9: Geometric series formula"
INSTRUCTIONS = "Answer each question."
COURSES = courses(3)
RATIOS = ["2", "3", "4", "5", "1/2", "0.5", "1/3", "2/3", "1/4", "3/4", "0.75"]

TYPES = [
    dict(key="1", title="The Sum from a and r",
         look="The first term a, the common ratio r, and how many terms.",
         move="S_n = a (1 - r^n)/(1 - r). Put in a, r, and n.", width="full"),
    dict(key="2", title="The Sum of a Written Series",
         look="A geometric series written out: a + a r + a r^2 + ...",
         move="The first term is a; divide the second term by the first to get r. Then S_n = a (1 - r^n)/(1 - r).",
         width="full"),
    dict(key="3", title="The First Term",
         look="The sum of the first n terms and the common ratio.",
         move="Put the sum, r, and n into S_n = a (1 - r^n)/(1 - r), and solve for a.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def ratio(t):
    return F(t)

def total(a, r, n):
    return a * (1 - r ** n) / (1 - r)

def num(x):
    """A whole number with commas, as Khan writes it: 15,624."""
    return f"{int(x):,}"

def math_num(x):
    """A number in Typst math: "1,024" quoted, so the comma isn't spaced as punctuation."""
    return f'"{num(x)}"' if x >= 1000 else num(x)

def math_ratio(t):
    return f"${t}$"

def draw(entry, r, tpl):
    rt = r.choice(RATIOS)
    q = ratio(rt)
    n = r.randint(3, 10)
    a = r.randint(1, 9) * q.denominator ** (n - 1)                       # every term whole
    need(1 < a <= 5000 and total(a, q, n) <= 500000 and a * q ** (n - 1) >= 1)
    s = total(a, q, n)
    if entry == "1":
        prompt = (f"The first term in a geometric series is {num(a)} and the common ratio is {math_ratio(rt)}. "
                  f"Find the sum of the first {n} terms in the series.")
        answer = s
    elif entry == "2":
        terms = " + ".join(math_num(a * q ** k) for k in range(3))
        prompt = f"Find the sum of the first {n} terms in this geometric series (do not round): ${terms} + dots$"
        answer = s
    else:
        prompt = (f"The sum of the first {n} terms of a geometric series is {num(s)} and the common ratio is "
                  f"{math_ratio(rt)}. What is the first term of the series?")
        answer = a
    need(answer.denominator == 1 if isinstance(answer, F) else True)
    return dict(a=a, r=rt, n=n, prompt=prompt, answer=num(answer))

def check(p):
    try:
        a, q, n = F(p["a"]), ratio(p["r"]), p["n"]
        got = F(p["answer"].replace(",", ""))
        if p["type"] == "3":
            ok = got * (1 - q ** n) / (1 - q) == F(num(total(a, q, n)).replace(",", "")) and num(total(a, q, n)) in p["prompt"]
        else:
            ok = got == total(a, q, n) and (num(a) in p["prompt"] or p["type"] == "2")
        return "checked" if ok and f"first {n} terms" in p["prompt"] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    return p["prompt"]

def answer_typst(p):
    return p["answer"]

def text(p):
    return p["prompt"].replace("$", "").replace('"', "").replace("dots", "...")

def answer_text(p):
    return p["answer"]

def height(p):
    return 0.6

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new series; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=t.strip())
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
