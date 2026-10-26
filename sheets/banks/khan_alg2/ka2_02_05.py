"""Khan Algebra 2, Lesson 2-5: Plot numbers on the complex plane, from the
old app's Alg2_02_05 (twenty-four generated slots, drawn in TikZ; the old
key read only "TikZ graph").

Type 1: plot a + b i in the complex plane (a and b -9 to 9, not both 0, as
the old app drew them); the key plots it in red. Type 2, the reverse: a
point is plotted; what number does it represent? Written a + b i.

A problem: dict(type, z, answer, source).
    Type 1  z "3 - 7 i", answer "(3, -7)"     (the point: real part across, imaginary part up)
    Type 2  z "3 - 7 i", answer "3 - 7 i"
check(): Type 1, the answer's point is (Re z, Im z); Type 2, the answer is
z, written in a + b i form (cx.standard).
"""
import re
from ... import gen
from ...gen import need
from ...graphs import Graph, PREAMBLE
from ...typmath import display, text as plain
from . import courses
from . import cx

NAME = FAMILY = "ka2_02_05"
FIXED = False
TITLE = "Lesson 2-5: Plot numbers on the complex plane"
INSTRUCTIONS = ""
COURSES = courses(2)

TYPES = [
    dict(key="1", title="Plot the Number", instructions="Plot each number in the complex plane.",
         look="A complex number a + b i and an empty complex plane.",
         move="The real part a goes across (the Re axis), the imaginary part b goes up or down (the Im axis): "
              "plot the point (a, b).", width="full"),
    dict(key="2", title="Name the Point", instructions="Write the number each point represents, in the form a + bi.",
         look="A point plotted in the complex plane.",
         move="Read across for the real part and up or down for the imaginary part: a + b i.", width="full"),
]
T = gen.Types(TYPES, "", space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["z"])

def draw(entry, r, tpl):
    a, b = r.randint(-9, 9), r.randint(-9, 9)
    need(a or b)
    z = cx.written(a, b)
    return dict(z=z, answer=f"({a}, {b})" if entry == "1" else z)

POINT = re.compile(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)")

def check(p):
    try:
        a, b = cx.parts(p["z"])
        if p["type"] == "1":
            m = POINT.fullmatch(p["answer"].replace("−", "-").strip())
            ok = m and (int(m.group(1)), int(m.group(2))) == (a, b)
        else:
            ok = cx.parts(p["answer"]) == (a, b) and cx.standard(p["answer"])
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def plane(p, key=False):
    g = Graph(x=(-10, 10), y=(-10, 10), width=5.6, xlabel="Re", ylabel="Im")
    a, b = (int(v) for v in cx.parts(p["z"]))
    if p["type"] == "2":
        g.point(a, b, color="blue", label="*P*")
    elif key:
        g.point(a, b, color="red", label=f"${p['z']}$")
    return g.typst()

def typst(p, gap="0.3em", key=False):
    q = f"Plot ${p['z']}$ in the complex plane." if p["type"] == "1" else "What number does point $P$ represent?"
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{q}], [{plane(p, key)}])"

def key_typst(p, gap="0.3em"):
    return typst(p, gap, key=True)

def answer_typst(p):
    return f"${p['answer']}$"

def text(p):
    return f"plot {plain(p['z'])}" if p["type"] == "1" else f"point at {tuple(int(v) for v in cx.parts(p['z']))}: which number?"

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 2.6

def edit_text(p):
    return p["z"]

def from_edit(t, old):
    t = " ".join(t.replace("−", "-").split())
    try:
        a, b = cx.parts(t)
    except Exception:
        raise ValueError("write a complex number, like 3 - 7 i") from None
    if a != int(a) or b != int(b) or max(abs(a), abs(b)) > 9:
        raise ValueError("whole-number parts from -9 to 9, so it fits on the grid")
    z = cx.written(int(a), int(b))
    new = dict(old, z=z, answer=f"({a}, {b})" if old["type"] == "1" else z, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.replace("−", "-").split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
