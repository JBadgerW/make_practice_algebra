"""Khan Algebra 1, Lesson 8-17: Increasing and decreasing intervals, from the
old app's Alg1_08_17 (twenty of Khan's graphs as screenshots, without
answers).

Select all the intervals where f is increasing (or decreasing): three
intervals and "None of the above", as Khan's. The curve (curves.py) turns
at its knots, some at halves (Khan's -2.5 < x < 1.75 has quarters; halves
here), so it rises or falls all the way across a piece; an interval is
right if the curve goes the asked way all across it. Some intervals cross
a turn, and sometimes none is right.

A problem: dict(type, ks, way, choices, answer, source).
    ks  knots (x's as strings, "2.5")    way 1 (increasing) or -1
    choices [["-5", "-2.5"], ["-2.5", "1"], ["1", "3"], "None of the above"]    answer "A, C"
check() asks the curve which way it goes on each interval (curves.rising).
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need
from ...graphs import Graph, PREAMBLE
from . import courses
from . import curves

NAME = FAMILY = "ka1_08_17"
FIXED = False
TITLE = "Lesson 8-17: Increasing and decreasing intervals"
INSTRUCTIONS = "Choose all answers that apply."
COURSES = courses(8)
NONE = "None of the above"

TYPES = [
    dict(key="1", title="Increasing or Decreasing?",
         look="The graph of a function and three intervals.",
         move="Read left to right. Increasing means going up the whole way across the interval; decreasing, down. "
              "An interval with a turn in it is neither.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, str(p["ks"]), p["way"], str(p["choices"]))

def num(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else f"{float(q):g}"

def kn(p):
    return [(F(x), y) for x, y in p["ks"]]

def draw(entry, r, tpl):
    raw = curves.knots(r, -12, 12, -5, 5, gap=(3, 6))           # in halves
    ks = [(F(x, 2), y) for x, y in raw]
    way = r.choice((1, -1))
    xs = [x for x, _ in ks]
    pool = []
    for i in range(len(xs) - 1):
        pool.append((xs[i], xs[i + 1]))                           # a whole piece
        if i + 2 < len(xs):
            pool.append((xs[i], xs[i + 2]))                       # across a turn
        mid = (xs[i] + xs[i + 1]) / 2
        pool.append((xs[i], F(int(mid * 2), 2)) if F(int(mid * 2), 2) > xs[i] else (xs[i], xs[i + 1]))
    pool = [s for s in dict.fromkeys(pool) if s[0] < s[1]]
    need(len(pool) >= 3)
    chosen = sorted(r.sample(pool, 3))
    need(len({a for a, _ in chosen}) == 3)
    choices = [[num(a), num(b)] for a, b in chosen] + [NONE]
    good = [c for c in choices[:3] if curves.rising(ks, F(c[0]), F(c[1])) == way] or [NONE]
    choices, answer = gen.in_order(choices, good)
    return dict(ks=[[num(x), y] for x, y in ks], way=way, choices=choices, answer=answer)

def check(p):
    try:
        ks = kn(p)
        right = [gen.ABC[i] for i, c in enumerate(p["choices"][:3]) if curves.rising(ks, F(c[0]), F(c[1])) == p["way"]]
        return "checked" if gen.letters_of(p["answer"]) == (right or [gen.ABC[3]]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def graph(p):
    g = Graph(x=(-7, 7), y=(-7, 7), width=5.2)
    curves.draw(g, [(float(x), y) for x, y in kn(p)], ends="closed")
    return g.typst()

def interval(c):
    return c if c == NONE else f"${c[0]} < x < {c[1]}$"

def typst(p, gap="0.3em"):
    q = f"Select all the intervals where $f$ is {'increasing' if p['way'] > 0 else 'decreasing'}."
    left = f"{q} #v(0.3em) {gen.choices_typst([interval(c) for c in p['choices']])}"
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{left}], [{graph(p)}])"

def answer_typst(p):
    return "; ".join(f"{a}. {interval(p['choices'][gen.ABC.index(a)])}" for a in gen.letters_of(p["answer"]))

def text(p):
    return (f"{'increasing' if p['way'] > 0 else 'decreasing'}: knots {p['ks']}   "
            + gen.choices_text([interval(c).replace("$", "") for c in p["choices"]]))

def answer_text(p):
    return answer_typst(p).replace("$", "")

def height(p):
    return 2.4

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new graph; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
