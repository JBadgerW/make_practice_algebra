"""Khan Prealgebra, Lesson 1-2: Identify factors, from the old app's
PreAlg_01_02a (twelve of Khan's, without answers).

Type 1: list all the factors of n, choose 1 of Khan's three: the right
list, a list with a factor missing and a non-factor in its place (1, 2, 4,
6, 8, 10, 12, 24 for 24), and the multiples (24, 48, 72, 96). Type 2:
which equation shows that a is a factor of n? n = a × b (or b = n ÷ a),
among Khan's misreadings: n = (n + a) - a, n = (n - a) + a,
n = (a n) ÷ a, a = n × b. Type 3: which of four numbers is a factor of n?

A problem: dict(type, n, a, choices, answer, source).
check(): Type 1 computes the factors; Type 2 evaluates each equation and
requires the right one to be a product (or quotient) with a in it; Type 3
divides.
"""
import re
from ... import gen
from ...gen import need
from . import courses
from .numbers import factors

NAME = FAMILY = "kpa_01_02"
FIXED = False
TITLE = "Lesson 1-2: Identify factors"
INSTRUCTIONS = "Choose 1 answer."
COURSES = courses(1)

TYPES = [
    dict(key="1", title="List All the Factors",
         look="A number and three lists.",
         move="Find the factor pairs, starting with 1. Every number in the list must divide evenly, and none may be missing."),
    dict(key="2", title="Which Equation Shows a Factor?",
         look="Four equations with the number and a possible factor.",
         move="a is a factor of n when n = a × (a whole number), or n ÷ a is a whole number. Adding or subtracting "
              "shows nothing about factors.", width="full"),
    dict(key="3", title="Which Number Is a Factor?",
         look="A number and four smaller numbers.",
         move="Divide: a factor goes in evenly, with no remainder."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["n"], p.get("a"))

def listed(ns):
    return ", ".join(str(x) for x in sorted(ns))

def draw(entry, r, tpl):
    if entry == "1":
        n = r.choice([m for m in range(12, 100) if len(factors(m)) >= 6])
        fs = factors(n)
        middle = sorted(fs - {1, n})
        gone = r.choice(middle)
        extra = r.choice([d for d in range(2, n // 2 + 1) if d not in fs])     # a plausible one: 10 for 24
        mixed = (fs - {gone}) | {extra}
        wrong = [listed(mixed), listed(n * k for k in range(1, 5))]
        if r.random() < 0.5:
            wrong[1] = listed(fs - {1, n})                       # 1 and n left out
        choices, answer = gen.lettered(r, listed(fs), wrong)
        return dict(n=n, choices=[f"${c}$" for c in choices], answer=answer)
    if entry == "2":
        a, b = r.randint(2, 9), r.randint(3, 12)
        n = a * b
        right = r.choice([f"{n} = {a} times {b}", f"{b} = {n} div {a}"])
        wrong = [f"{n} = {n + a} - {a}", f"{n} = {n - a} + {a}", f"{n} = {n * a} div {a}", f"{a} = {n} times {b}"]
        choices, answer = gen.lettered(r, right, r.sample(wrong, 3))
        return dict(n=n, a=a, choices=[f"${c}$" for c in choices], answer=answer)
    n = r.randint(20, 99)
    fs = [d for d in range(2, 10) if n % d == 0]
    need(fs and len([d for d in range(2, 10) if n % d]) >= 3)
    right = r.choice(fs)
    choices, answer = gen.lettered(r, f"${right}$", [f"${d}$" for d in r.sample([d for d in range(2, 10) if n % d], 3)])
    return dict(n=n, choices=choices, answer=answer)

def value(side):
    return eval(side.replace("times", "*").replace("div", "/"))

def shows_factor(c, n, a):
    """n = a × b or b = n ÷ a, true, with whole numbers."""
    left, right = c.strip("$").split("=")
    if not abs(value(left) - value(right)) < 1e-9:
        return False
    nums = [int(x) for x in re.findall(r"\d+", c)]
    if "times" in c:
        return nums[0] == n and a in nums[1:]
    if "div" in c:
        return nums[1] == n and nums[2] == a
    return False

def check(p):
    try:
        n = p["n"]
        if p["type"] == "1":
            right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if c.strip("$") == listed(factors(n))]
        elif p["type"] == "2":
            right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if shows_factor(c, n, p["a"])]
        else:
            right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if n % int(c.strip("$")) == 0]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def typst(p, gap="0.3em"):
    n = p["n"]
    q = {"1": f"List all the factors of ${n}$.", "2": f"Which equation shows that ${p.get('a')}$ is a factor of ${n}$?",
         "3": f"Which of the following numbers is a factor of ${n}$?"}[p["type"]]
    return f"{q} \\\n    {gen.choices_typst(p['choices'], 'vertical' if p['type'] == '1' else 'linear')}"

def answer_typst(p):
    return gen.choice_answer_typst(p)

def plain(c):
    return c.strip("$").replace("times", "×").replace("div", "÷")

def text(p):
    return f"{p['n']}{' (' + str(p['a']) + ')' if p.get('a') else ''}: " + gen.choices_text(p["choices"], plain)

def answer_text(p):
    return "; ".join(f"{a}. {plain(c)}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))

def height(p):
    return 1.3 if p["type"] == "1" else 0.6

def edit_text(p):
    return str(p["n"])

def from_edit(t, old):
    raise ValueError("reroll for a new number; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
