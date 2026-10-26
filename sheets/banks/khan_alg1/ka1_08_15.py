"""Khan Algebra 1, Lesson 8-15: Absolute maxima and minima, from the old
app's Alg1_08_15 (fourteen of Khan's graphs as screenshots, without
answers).

Write the absolute maximum (Type 1) or minimum (Type 2) point of the graph:
a smooth curve with closed ends (curves.py). The highest (lowest) point
may be an end, as in Khan's; it is always one point, never a tie.

A problem: dict(type, ks, answer, source).
    ks  the curve's knots    answer "(1, 6)"
check() finds the highest (lowest) point of the curve, which is always a
knot (curves.py); the answer must be exactly it.
"""
from ... import gen
from ...gen import need
from ...graphs import PREAMBLE
from . import courses
from . import curves, extrema

NAME = FAMILY = "ka1_08_15"
FIXED = False
TITLE = "Lesson 8-15: Absolute maxima and minima"
INSTRUCTIONS = "Write the coordinates of the point asked for."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="Absolute Maximum",
         look="A curve with closed ends.",
         move="The absolute maximum is the highest point of the whole graph. Check the hilltops and the ends.",
         width="full"),
    dict(key="2", title="Absolute Minimum",
         look="A curve with closed ends.",
         move="The absolute minimum is the lowest point of the whole graph. Check the valleys and the ends.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], str(p["ks"]))

def wanted(p):
    ks = [tuple(k) for k in p["ks"]]
    best = max(y for _, y in ks) if p["type"] == "1" else min(y for _, y in ks)
    return [k for k in ks if k[1] == best]

def draw(entry, r, tpl):
    ks = extrema.curve(r)
    p = dict(type=entry, ks=ks)
    need(len(wanted(p)) == 1)
    if r.random() < 0.3:                                          # an end as the answer, as some of Khan's
        need(wanted(p)[0] in (tuple(ks[0]), tuple(ks[-1])))
    return dict(ks=ks, answer=extrema.written(wanted(p)))

def check(p):
    try:
        return "checked" if extrema.read_points(p["answer"]) == sorted(wanted(p)) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def question(p):
    return f"Write the absolute {'maximum' if p['type'] == '1' else 'minimum'} point of the graph."

def typst(p, gap="0.3em"):
    return extrema.typst(question(p), p["ks"])

def key_typst(p, gap="0.3em"):
    return extrema.typst(question(p), p["ks"], wanted(p))

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    return f"{question(p)}   knots {p['ks']}"

def answer_text(p):
    return p["answer"]

def height(p):
    return 2.4

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new graph; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
