"""Khan Algebra 1, Lesson 8-14: Relative maxima and minima, from the old
app's Alg1_08_14 (fourteen of Khan's graphs as screenshots, without
answers).

Write all the relative maximum (Type 1) or minimum (Type 2) points of the
graph: a smooth curve with closed ends whose turns are at lattice points
(curves.py), two to four of each. The ends are not relative extrema.

A problem: dict(type, ks, answer, source).
    ks  the curve's knots [[-6, 2], [-4, -3], ...]    answer "(-2, 3), (1, 4)"
check() finds the relative maxima (minima) of the curve: the knots above
(below) both neighbors; the answer must list exactly those.
"""
from ... import gen
from ...gen import need
from ...graphs import PREAMBLE
from . import courses
from . import curves, extrema

NAME = FAMILY = "ka1_08_14"
FIXED = False
TITLE = "Lesson 8-14: Relative maxima and minima"
INSTRUCTIONS = "Write the coordinates of all the points asked for."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="Relative Maxima",
         look="A curve with several hills.",
         move="A relative maximum is a hilltop: higher than the points just around it. The ends don't count.",
         width="full"),
    dict(key="2", title="Relative Minima",
         look="A curve with several valleys.",
         move="A relative minimum is a valley bottom: lower than the points just around it. The ends don't count.",
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
    return curves.maxima(ks) if p["type"] == "1" else curves.minima(ks)

def draw(entry, r, tpl):
    ks = extrema.curve(r)
    p = dict(type=entry, ks=ks)
    need(2 <= len(wanted(p)) <= 4)
    return dict(ks=ks, answer=extrema.written(wanted(p)))

def check(p):
    try:
        return "checked" if extrema.read_points(p["answer"]) == sorted(wanted(p)) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def question(p):
    return f"Write all the relative {'maximum' if p['type'] == '1' else 'minimum'} points of the graph."

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
