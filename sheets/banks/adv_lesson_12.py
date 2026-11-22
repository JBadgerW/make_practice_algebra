"""Lesson 12 (Advanced Math): polygons, angles and diagonals in polygons. From
the Saxon lesson and its deck (~/Documents/adv_math/problem_sets/ps_012/slides/deck_012.typ):
example 12.1 and Problem Set 12, problems 4 and 5.

    1  interior and exterior angle sums:   a seven-sided convex polygon      900 degree; 360 degree
    2  the number of diagonals:            a nine-sided convex polygon       27

Type 1 shows the polygon, as the deck does for example 12.1; the key draws it split
into triangles from one vertex and numbers them, the deck's answer figure. The polygon
is regular, a vertex at the left. Type 2 is problem 5, which the problem types file
lists apart: no example works it, but it practices the lesson's diagonal formula.
Its prompt has no figure, as the deck's has none.

The key writes what the deck writes: (a) 900°, (b) 360° ("900 degree; 360 degree",
interior first; problem 4 asks for the same two sums without the letters), and
27 diagonals ("27"). The sides run 3 to 10 in Type 1 (each triangle on the key still holds its number)
and 4 to 15 in Type 2; a number of sides up to twelve is written as a word,
"seven-sided", as the book does, and 13 and up as "13-sided".

check() doesn't use the formulas. Type 1 measures the drawn polygon: it adds its
interior angles, and its exterior angles (each 180° less the interior one), from the
vertices' coordinates. Type 2 counts the pairs of vertices that aren't neighbors.

Skipped sources: examples 12.2, 12.3, and 12.4, the proofs of Cases I, II, and III
of the chord-tangent theorem. They are proofs; no Problem Set item matches them.

A problem: dict(type, prompt, answer, source); the prompt is the number of sides.
    prompt  "7"         answer  "900 degree; 360 degree"      (Type 1)
    prompt  "9"         answer  "27"                          (Type 2)
"""
import math, re
from .. import gen
from ..gen import need
from . import lesson_figures as fig

NAME = FAMILY = "adv_lesson_12"
FIXED = False
TITLE = "Lesson 12: Polygons, Angles and Diagonals in Polygons, Proof of the Chord-Tangent Theorem"
INSTRUCTIONS = ""              # each type has its own
COURSES = {"Advanced Math": "Lessons"}
PREAMBLE = fig.PREAMBLE

TYPES = [
    dict(key="1", title="Interior and Exterior Angle Sums", instructions="Find the angle sums.",
         look="A convex polygon with a given number of sides.",
         move="Draw the diagonals from one vertex: they cut the polygon into $N - 2$ triangles, so the interior "
              "angles sum to $(N - 2) 180 degree$. The exterior angles of any convex polygon sum to $360 degree$."),
    dict(key="2", title="Diagonals of a Polygon", instructions="Find the number of diagonals.",
         look="A convex polygon with a given number of sides.",
         move="Each of the $N$ vertices has a diagonal to every vertex but itself and its two neighbors, $N - 3$; "
              "each diagonal is counted from both ends, so there are $(N(N - 3))/2$."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

SIDES = {"1": range(3, 11), "2": range(4, 16)}
WORDS = dict(zip(range(3, 13), ("three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")))

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# The templates: the number of sides
# ------------------------------------------------------------------
def t1_pick(r):
    return dict(n=r.choice(SIDES["1"]))

def t1(n):
    need(n in SIDES["1"])
    return str(n)

def t2_pick(r):
    return dict(n=r.choice(SIDES["2"]))

def t2(n):
    need(n in SIDES["2"])
    return str(n)

TEMPLATES = {"1": [(t1_pick, t1)], "2": [(t2_pick, t2)]}
RANGES = {t1: lambda n: n in SIDES["1"], t2: lambda n: n in SIDES["2"]}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

# ------------------------------------------------------------------
# Solving, and checking without the formulas
# ------------------------------------------------------------------
def sides(prompt):
    t = prompt.strip()
    if not re.fullmatch(r"\d+", t) or int(t) < 3:
        raise ValueError("a number of sides, 3 or more")
    return int(t)

def answer_of(prompt, typ):
    n = sides(prompt)
    if typ == "1":
        return f"{(n - 2) * 180} degree; 360 degree"
    if n < 4:
        raise ValueError("a polygon with diagonals")
    return str(n * (n - 3) // 2)

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    prompt = build(**pick(r))
    return dict(prompt=prompt, answer=answer_of(prompt, entry))

def measured(n):
    """The drawn polygon's interior angle sum and exterior angle sum, in degrees, from its vertices."""
    P = fig.polygon_points(n)
    inner = 0.0
    for i in range(n):
        a, v, b = P[i - 1], P[i], P[(i + 1) % n]
        u = (a[0] - v[0], a[1] - v[1])
        w = (b[0] - v[0], b[1] - v[1])
        inner += math.degrees(math.acos((u[0] * w[0] + u[1] * w[1]) / (math.hypot(*u) * math.hypot(*w))))
    return inner, n * 180 - inner

ANSWER1 = re.compile(r"(\d+) degree; (\d+) degree")

def check(p):
    try:
        n = sides(p["prompt"])
        ans = " ".join(p["answer"].split())
        if p["type"] == "1":
            m = ANSWER1.fullmatch(ans)
            inner, outer = measured(n)
            ok = bool(m) and abs(int(m.group(1)) - inner) < 1e-6 and abs(int(m.group(2)) - outer) < 1e-6
        else:
            pairs = sum(1 for i in range(n) for j in range(i + 1, n) if (j - i) % n not in (1, n - 1))
            ok = re.fullmatch(r"\d+", ans) is not None and int(ans) == pairs and n >= 4
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: each problem says what to do (EXTENDING.md 3.10)
# ------------------------------------------------------------------
def sided(n):
    return f"{WORDS.get(n, n)}-sided"

def statement(p):
    try:
        n = sides(p["prompt"])
    except ValueError:
        return p["prompt"]
    if p["type"] == "1":
        return (f"Find the sum of the measures of (a) the interior angles and (b) the exterior angles of a "
                f"{sided(n)} convex polygon.")
    return f"How many diagonals can be drawn in a {sided(n)} convex polygon?"

def figure(p, key=False, unit="1cm"):
    """Type 1's polygon (triangulated on the key); None for Type 2 or a polygon too big to draw."""
    try:
        n = sides(p["prompt"])
    except ValueError:
        return None
    if p["type"] != "1" or n > 12:
        return None
    return fig.polygon(n, triangulated=key, unit=unit)

def _prompt(p, key):
    f = figure(p, key)
    s = statement(p)
    return s if f is None else f"{s} #v(0.4em) #align(center)[{f}]"

def typst(p, gap="0.3em"):
    return _prompt(p, False)

def key_typst(p, gap="0.3em"):
    """The key's prompt: the polygon split into numbered triangles."""
    return _prompt(p, True)

def answer_typst(p):
    m = ANSWER1.fullmatch(" ".join(p["answer"].split()))
    if p["type"] == "1" and m:
        return f"(a) ${m.group(1)} degree$ #h(1em) (b) ${m.group(2)} degree$"
    if p["type"] == "2":
        return f"${p['answer']}$ diagonals"
    return f"${p['answer']}$"

SLIDE_UNIT = "1.9cm"

def slide_typst(p, key=False):
    """Type 1: the words (and the answer, hidden on the question slide) beside the polygon drawn
    larger, triangulated on the answer slide. None for Type 2."""
    f = figure(p, key, SLIDE_UNIT)
    if f is None:
        return None
    ans = answer_typst(p)
    shown = f"#text(fill: red)[{ans}]" if key else f"#hide[{ans}]"
    return f"#grid(columns: (1fr, auto), column-gutter: 1.5em, align: horizon, [{statement(p)} #v(0.8em) {shown}], [{f}])"

def text(p):
    return statement(p) + ("   [figure: the polygon]" if figure(p) is not None else "")

def answer_text(p):
    m = ANSWER1.fullmatch(" ".join(p["answer"].split()))
    if p["type"] == "1" and m:
        return f"(a) {m.group(1)}°   (b) {m.group(2)}°"
    return f"{p['answer']} diagonals" if p["type"] == "2" else p["answer"]

def height(p):
    return 2.3 if figure(p) is not None else 0.45

# ------------------------------------------------------------------
# Editing: the prompt is the number of sides
# ------------------------------------------------------------------
def edit_text(p):
    return p["prompt"]

def answer_edit_text(p):
    return p["answer"]

def from_edit(t, old):
    t = " ".join(t.split())
    typ = old.get("type", "1")
    try:
        answer = answer_of(t, typ)
    except ValueError:
        raise ValueError("write the number of sides, like 7") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def with_answer(p, t):
    t = " ".join(t.replace("°", " degree").replace(",", ";").split())
    new = dict(p, answer=t)
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=8)
