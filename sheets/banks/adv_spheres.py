"""Spheres (Advanced Math), from the 2025-26 midterm: find the surface area
from the volume, or the volume from the surface area, in exact form with π.

A problem: dict(type, story, prompt, answer, source). The prompt is words
with its math between dollar signs, as Typst writes it:
    prompt  "A sphere has a volume of $(500 pi)/3$ cubic feet. Find the surface area of the sphere."
    answer  "$100 pi$ square feet"
The radius is a whole number, 1 to 10, as on the midterm. check() reads the
given value back out of the words, finds the radius from it (it must come
out rational), works out the other measure, and compares it exactly with
the answer's, units included.
"""
import re
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, simplest_form
from ..typmath import tx, display, dfrac, text as plain
from ..typst import esc

NAME = FAMILY = "adv_spheres"
FIXED = False
TITLE = "Spheres"
INSTRUCTIONS = "Give each answer in exact form, in terms of π."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Volume to Surface Area",
         look="A sphere's volume; its surface area is asked for.",
         move="V = (4/3) π r^3: solve for r (multiply by 3/(4π), then take the cube root). Then S = 4 π r^2."),
    dict(key="2", title="Surface Area to Volume",
         look="A sphere's surface area; its volume is asked for.",
         move="S = 4 π r^2: solve for r (divide by 4π, then take the square root). Then V = (4/3) π r^3."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

UNITS = ("feet", "inches", "yards", "miles", "meters", "centimeters", "kilometers", "light-years")   # the midterm's
STORIES = {
    "1": [
        dict(key="a", units=UNITS,             # the midterm
             text="A sphere has a volume of ${V}$ cubic {u}. Find the surface area of the sphere.",
             answer="${S}$ square {u}"),
        dict(key="b", units=("inches", "centimeters"),
             text="A ball holds ${V}$ cubic {u} of air. How much material covers its surface?",
             answer="${S}$ square {u}"),
        dict(key="c", units=("feet", "meters"),
             text="A spherical water tank holds ${V}$ cubic {u}. What is the area of its outside surface?",
             answer="${S}$ square {u}"),
    ],
    "2": [
        dict(key="a", units=UNITS,             # the midterm
             text="A sphere has a surface area of ${S}$ square {u}. Find the volume of the sphere.",
             answer="${V}$ cubic {u}"),
        dict(key="b", units=("inches", "centimeters"),
             text="It takes ${S}$ square {u} of leather to cover a ball. How much space is inside the ball?",
             answer="${V}$ cubic {u}"),
        dict(key="c", units=("feet", "meters"),
             text="The outside of a spherical tank has an area of ${S}$ square {u}. How much does the tank hold?",
             answer="${V}$ cubic {u}"),
    ],
}
STORY = {(t, s["key"]): s for t, ss in STORIES.items() for s in ss}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def volume(r):
    return sp.Rational(4, 3) * sp.pi * r ** 3

def area(r):
    return 4 * sp.pi * r ** 2

def draw(entry, r, tpl):
    st = STORIES[entry][tpl]
    rad = r.randint(1, 10)
    v = dict(V=tx(volume(rad)), S=tx(area(rad)), u=r.choice(st["units"]))
    return dict(story=st["key"], prompt=gen.fill(st["text"], **v), answer=gen.fill(st["answer"], **v))

def solve(typ, v):
    """The other measure, from the given one: the radius must come out rational."""
    if typ == "1":
        rad = sp.root(3 * to_sympy(v["V"]) / (4 * sp.pi), 3)
    else:
        rad = sp.sqrt(to_sympy(v["S"]) / (4 * sp.pi))
    rad = sp.nsimplify(sp.simplify(rad))
    if not rad.is_Rational or rad <= 0:
        raise ValueError("that measure doesn't give a rational radius")
    return {"S": area(rad)} if typ == "1" else {"V": volume(rad)}

def check(p):
    try:
        st = STORY[(p["type"], p["story"])]
        v = gen.read(st["text"], p["prompt"])
        got = gen.read(st["answer"], p["answer"])
        (k, want), = solve(p["type"], v).items()
        ok = sp.simplify(to_sympy(got[k]) - want) == 0 and simplest_form(got[k]) and got["u"] == v["u"]
    except (ValueError, KeyError, TypeError):
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(STORIES[e]))

# ------------------------------------------------------------------
# Showing: words escaped, the math between dollar signs in display style
# ------------------------------------------------------------------
MATH = re.compile(r"\$([^$]*)\$")

def marked(t):
    out, i = "", 0
    for m in MATH.finditer(t):
        out += esc(t[i:m.start()]) + display(dfrac(m.group(1)))
        i = m.end()
    return out + esc(t[i:])

def readable(t):
    return MATH.sub(lambda m: plain(m.group(1)).replace("pi", "π"), t)

def typst(p, gap="0.3em"):
    return marked(p["prompt"])

def answer_typst(p):
    return marked(p["answer"])

def text(p):
    return readable(p["prompt"])

def answer_text(p):
    return readable(p["answer"])

def height(p):
    return 0.4

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    st = STORY[(old["type"], old["story"])]
    v = gen.read(st["text"], t)
    v.update({k: tx(x) for k, x in solve(old["type"], v).items()})
    new = dict(old, prompt=t, answer=gen.fill(st["answer"], **v), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=10)   # ten radii
