"""Khan Algebra 1, Lesson 15-1: Classify numbers: rational & irrational,
from the old app's Alg1_15_01 (thirty of Khan's, without answers).

Is the number rational or irrational? Khan's numbers: terminating decimals
(0.692, 9.0), repeating ones (0.overline(151), 6.overline(6)), fractions and
mixed numbers (-501/502, 6 1/2), quotients of decimals (0.4/0.8), square roots
of perfect squares and of other numbers (sqrt(64), sqrt(32)), and numbers
with pi (-3 + pi, pi/5, pi sqrt(4)). One type, every kind mixed: a header
naming the kind would give the answer away.

A problem: dict(type, prompt, choices, answer, source).
    prompt   "0.overline(151)" (Typst math)
    choices  ["Rational", "Irrational"]
    answer   "A"
check() computes the number exactly (rationality.value): rational if it's a fraction.
"""
import math
from ... import gen
from ...gen import need, signed
from ...typmath import display, text as plain
from . import courses
from .rationality import rational

NAME = FAMILY = "ka1_15_01"
FIXED = False
TITLE = "Lesson 15-1: Classify numbers: rational & irrational"
INSTRUCTIONS = "Is each number rational or irrational?"
COURSES = courses(15)
CHOICES = ["Rational", "Irrational"]

TYPES = [
    dict(key="1", title="Rational or Irrational?",
         look="A decimal, a fraction, a square root, or a number with pi.",
         move="Rational: it can be written as a fraction of integers (terminating and repeating decimals, "
              "square roots of perfect squares). Irrational: it can't (square roots of other numbers, pi)."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

NONSQUARE = [n for n in range(2, 210) if int(n ** 0.5) ** 2 != n]

def d(r, lo=1, hi=9):
    return r.randint(lo, hi)

def mixed(r):
    """A mixed number, its fraction proper and in lowest terms: 6 1/2."""
    q = r.randint(2, 9)
    n = r.randint(1, q - 1)
    need(math.gcd(n, q) == 1)
    return f"{d(r)} {n}/{q}"

TEMPLATES = {"1": [
    lambda r: f"{d(r, 0)}.{r.randint(1, 999):03d}".rstrip("0"),                     # 0.692
    lambda r: f"{r.randint(1, 99)}.0",                                               # 9.0
    lambda r: f"{'-' if r.random() < 0.3 else ''}{d(r, 0)}.overline({r.randint(1, 99)})",   # 0.overline(151)
    lambda r: f"{'-' if r.random() < 0.5 else ''}{r.randint(1, 600)}/{r.randint(2, 600)}",  # -501/502
    lambda r: mixed(r),                                                              # 6 1/2
    lambda r: f"({d(r, 0)}.{d(r)})/({d(r, 0)}.{d(r)})",                                              # 0.4/0.8
    lambda r: f"sqrt({r.randint(2, 14) ** 2})",                                     # sqrt(64)
    lambda r: f"sqrt({r.choice(NONSQUARE)})",                                        # sqrt(32)
    lambda r: f"{signed(r, 1, 30)} + pi".replace("+ -", "- "),                       # -3 + pi
    lambda r: f"pi/{d(r, 2, 30)}",                                                       # pi/5
    lambda r: f"{r.choice(('-', ''))}{d(r, 2, 15)} pi",                              # -11 pi
    lambda r: f"pi - {d(r, 1, 30)}",                                                         # pi - 1
    lambda r: f"{d(r, 0)}.{d(r)} pi",                                                        # 0.3 pi
    lambda r: f"{r.choice(('', '-'))}pi sqrt({d(r, 2, 12) ** 2})",                                         # pi sqrt(4)
]}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r)
    choices, answer = gen.in_order(CHOICES, "Rational" if rational(prompt) else "Irrational")
    return dict(prompt=prompt, choices=choices, answer=answer)

def check(p):
    try:
        return "checked" if gen.chosen(p) == ["Rational" if rational(p["prompt"]) else "Irrational"] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

def typst(p, gap="0.3em"):
    return f"{display(p['prompt'])} #h(1.5em) {gen.choices_typst(p['choices'], 'linear')}"

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    return plain(p["prompt"]) + "      " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 0.4

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        answer = gen.in_order(CHOICES, "Rational" if rational(t) else "Irrational")[1]
    except Exception:
        raise ValueError("write a number in Typst math, like 0.overline(151) or sqrt(32)") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
