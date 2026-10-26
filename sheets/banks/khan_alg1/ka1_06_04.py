"""Khan Algebra 1, Lesson 6-4: Interpret points relative to a system, from
the old app's Alg1_06_04 (sixteen generated slots, drawn in TikZ).

A story, a system of two lines for it, and a point on the graph: what does
the point represent? Khan's four stories: a corn blend (the cost and the
amount), whipping cream and milk (the butterfat and the volume), two
library subscriptions (a fee or a price per book), and two skaters (one
with a head start). The answer is where the point sits: on a line, at the
crossing, or above or below each one. Choose 1 of four. Names only, no
pronouns.

The old cream story said "the intended percent of butterfat" for line a,
0.18 x + 0.04 y = 0.10 (500); that line fixes the amount of butterfat (50
mL), and off the volume line the percent differs, so it reads "the
intended amount of butterfat" here.

A problem: dict(type, story, names, lines, point, mark, choices, answer, source).
    lines  ["0.25 x + 0.5 y = 20", "x + y = 50"]   (line a, line b, Typst math)
    point  [20, 25]    mark "P"
check() reads the two equations, puts the point in each, and works out
the statement it stands for; exactly the answer's choice says that.
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need, written
from ...graphs import Graph, PREAMBLE
from ...typst import esc
from . import courses
from .twovar import coefficients

NAME = FAMILY = "ka1_06_04"
FIXED = False
TITLE = "Lesson 6-4: Interpret points relative to a system"
INSTRUCTIONS = "Choose 1 answer."
COURSES = courses(6)

TYPES = [
    dict(key="1", title="What Does the Point Mean?",
         look="A story, the graph of its two equations, and a point.",
         move="Is the point on line a, on line b, on both (the crossing), or on neither? Above a line means more "
              "than that equation allows; below means less. Then say it in the story's words.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["story"], str(p["lines"]), str(p["point"]))

def money(q):
    return f"{float(q):.2f}"

def fit(lines, step):
    """A first-quadrant window around two falling lines: both intercepts in, a little room."""
    top = lambda v: int(-(-float(v) * 1.15 // step) * step)
    xs, ys = [], []
    for eq in lines:
        a, b, c = coefficients(eq)
        xs.append(c / a)
        ys.append(c / b)
    return [0, top(max(xs)), 0, top(max(ys)), step]

def dec(q):
    q = F(q)
    s = f"{float(q):.4f}".rstrip("0").rstrip(".")
    assert F(s) == q, q
    return s

def side(eq, x, y):
    """-1, 0, 1: the point below, on, or above the line (more of the left side than the equation allows)."""
    a, b, c = coefficients(eq)
    v = a * F(x) + b * F(y) - c
    return (v > 0) - (v < 0)

def y_on(eq, x):
    a, b, c = coefficients(eq)
    return (c - a * F(x)) / b

# ------------------------------------------------------------------
# The stories: (draw(r) -> story dict), and what a point means in it
# ------------------------------------------------------------------
AMOUNT = {-1: "less than the intended", 0: "the intended", 1: "more than the intended"}

def corn(r):
    w, v = r.choice((F(1, 5), F(1, 4), F(3, 10))), r.choice((F(2, 5), F(9, 20), F(1, 2), F(3, 5)))
    white = r.choice(range(10, 45, 5))
    cost = w * white + v * (50 - white)
    lines = [f"{dec(w)} x + {dec(v)} y = {dec(cost)}", "x + y = 50"]
    return dict(story="corn", names=[r.choice(gen.NAMES)], lines=lines, window=fit(lines, 10),
                words=dict(w=money(w), v=money(v), cost=money(cost)))

def cream(r):
    c, m = r.randint(16, 20), r.randint(3, 5)
    p = r.randint(m + 3, c - 3)
    lines = [f"{dec(F(c, 100))} x + {dec(F(m, 100))} y = {dec(F(p, 100))} (500)", "x + y = 500"]
    return dict(story="cream", names=[r.choice(gen.NAMES)], lines=lines, window=fit(lines, 100), words=dict(c=c, m=m, p=p))

def library(r):
    fee, per = r.randint(9, 11) * 10, r.randint(2, 4)
    return dict(story="library", names=[r.choice(gen.NAMES)], lines=[f"y = {per} x", f"y = {fee}"],
                window=[0, 70, 0, 200, 10, 20], words=dict(fee=fee, per=per))

def race(r):
    b = r.randint(1, 2)
    g = r.randint(b + 1, 4)
    t = r.randint(10, 15)
    head = (g - b) * t
    names = r.sample(gen.NAMES, 2)
    return dict(story="race", names=names, lines=[f"y = {g} x", f"y = {head} + {b} x" if b > 1 else f"y = {head} + x"],
                window=[0, 30, 0, 100, 5, 10], words=dict(g=g, b=b, head=head))

STORIES = {"corn": corn, "cream": cream, "library": library, "race": race}

def intro(p):
    w, (n, *rest) = p["words"], p["names"]
    if p["story"] == "corn":
        return (f"{n} blends white corn and yellow corn to make tortilla chips, and needs 50 kg of corn in all for the "
                f"next order. White corn costs \\${w['w']} per kilogram, yellow corn \\${w['v']} per kilogram, and {n} "
                f"wants to spend \\${w['cost']} in all. In the graph, $x$ is the kilograms of white corn and $y$ the "
                f"kilograms of yellow corn.")
    if p["story"] == "cream":
        return (f"{n} has whipping cream that is {w['c']}% butterfat and milk that is {w['m']}% butterfat, and wants to "
                f"mix 500 mL that is {w['p']}% butterfat. In the graph, $x$ is the mL of cream and $y$ the mL of milk.")
    if p["story"] == "library":
        return (f"{n} is choosing a subscription to an online library: one charges a \\${w['fee']} annual fee, the "
                f"other \\${w['per']} per book borrowed. In the graph, $x$ is the number of books and $y$ the cost in "
                f"dollars.")
    g, b = n, rest[0]
    return (f"{g} and {b} started skating at the same time in the same direction, {b} with a head start "
            f"{w['head']} meters past the starting line. {g} skated {w['g']} meters per second and {b} "
            f"{w['b']} meter{'s' if w['b'] > 1 else ''} per second. In the graph, $x$ is the seconds since they started "
            f"and $y$ the distance in meters from the starting line.")

def meaning(p, x, y):
    """The statement the point stands for, worked out from the equations."""
    a, b = p["lines"]
    sa, sb = side(a, x, y), side(b, x, y)
    n, *rest = p["names"]
    if p["story"] == "corn":
        return f"{n} spends {AMOUNT[sa]} amount of money and buys {AMOUNT[sb]} amount of corn."
    if p["story"] == "cream":
        return f"The mixture has {AMOUNT[sb]} volume and {AMOUNT[sa]} amount of butterfat."
    if sa == 0 and sb == 0:
        return {"library": "A number of books where both subscriptions cost the same, and that cost.",
                "race": f"The time and distance where {n} catches up to {rest[0] if rest else ''}."}[p["story"]]
    if sa != 0 and sb != 0:
        return {"library": "A number of books and a cost that isn't possible with either subscription.",
                "race": f"A time and a distance from the starting line that neither {n} nor {rest[0] if rest else ''} "
                        f"has at that time."}[p["story"]]
    on, other = (a, b) if sa == 0 else (b, a)
    below = side(other, x, y) < 0                                  # less than the other line at this x
    if p["story"] == "library":
        plan = "annual-fee" if on == b else "per-book"
        return f"A number of books and the cost of the {plan} subscription, where it costs {'less' if below else 'more'}."
    who, them = (n, rest[0]) if on == a else (rest[0], n)
    return f"{who}'s distance from the starting line at a time when {who} is {'behind' if below else 'ahead of'} {them}."

def place(r, p):
    """A point: on line a, on line b, at the crossing, or on neither, inside the window."""
    a, b = p["lines"]
    x0, x1, y0, y1, step = p["window"][:5]
    ystep = p["window"][5] if len(p["window"]) > 5 else step
    where = r.choice(("a", "b", "both", "none"))
    if where == "both":
        (a1, b1, c1), (a2, b2, c2) = coefficients(a), coefficients(b)
        det = a1 * b2 - a2 * b1
        return [(c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det]
    if where == "none":
        return [F(r.randint(1, (x1 - x0) // step - 1) * step), F(r.randint(1, (y1 - y0) // ystep - 1) * ystep)]
    x = F(r.randint(1, 2 * (x1 - x0) // step - 1) * step, 2)
    return [x, y_on(a if where == "a" else b, x)]

def draw(entry, r, tpl):
    p = STORIES[r.choice(list(STORIES))](r)
    pt = place(r, p)
    x0, x1, y0, y1 = p["window"][:4]
    need(0 < pt[0] < x1 and 0 < pt[1] < y1 * F(19, 20))
    right = meaning(p, *pt)
    others = set()
    for _ in range(60):
        q = [F(r.randint(1, 19) * x1, 20), F(r.randint(1, 19) * y1, 20)] if r.random() < 0.5 else place(r, p)
        if 0 < q[0] < x1 and 0 < q[1] < y1:
            others.add(meaning(p, *q))
    others.discard(right)
    need(len(others) >= 3)
    choices, answer = gen.lettered(r, right, r.sample(sorted(others), 3))
    return dict(p, point=[dec(pt[0]) if pt[0].denominator in (1, 2, 4, 5, 10) else str(pt[0]),
                          dec(pt[1]) if pt[1].denominator in (1, 2, 4, 5, 10) else str(pt[1])],
                mark=r.choice("PQRS"), choices=choices, answer=answer)

def check(p):
    try:
        x, y = (F(v) for v in p["point"])
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if c == meaning(p, x, y)]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

AXES = {"corn": ("White (kg)", "Yellow (kg)"), "cream": ("Cream (mL)", "Milk (mL)"),
        "library": ("Books", "Cost (\\$)"), "race": ("Time (s)", "Distance (m)")}

def graph(p):
    x0, x1, y0, y1, step = p["window"][:5]
    ystep = p["window"][5] if len(p["window"]) > 5 else step
    xl, yl = AXES[p["story"]]
    g = Graph(x=(x0, x1), y=(y0, y1), width=5.6, height=5.0, step=(step, ystep), xlabel=xl, ylabel=yl)
    for eq, color, name in zip(p["lines"], ("blue", "red"), "ab"):
        a, b, c = coefficients(eq)
        if b == 0:
            g.vertical(float(c / a), color=color)
        else:
            m, k = float(-a / b), float(c / b)
            g.line(m, k, color=color)
            spots = [x1 * t / 20 for t in range(2, 19)]             # a's label toward the left, b's toward the right
            for lx in (spots if name == "a" else spots[::-1]):
                ly = m * lx + k
                if 0.06 * y1 < ly < 0.9 * y1:
                    g.label_at(lx, ly, f"*{name}*", anchor="south-west", color=color, size=9)
                    break
    x, y = (float(F(v)) for v in p["point"])
    g.point(x, y, label=f"*{p['mark']}*", anchor="south-west")
    return g.typst()

def typst(p, gap="0.3em"):
    eqs = f"line $a$: ${p['lines'][0]}$ \\\n    line $b$: ${p['lines'][1]}$"
    question = f"What does point {p['mark']} represent?"
    left = f"{intro(p)} \\\n    {eqs} #v(0.4em) {question} #v(0.3em) {gen.choices_typst([esc(c) for c in p['choices']])}"
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{left}], [{graph(p)}])"

def answer_typst(p):
    return esc(gen.choice_answer_typst(p))

def text(p):
    return f"{intro(p)}  a: {p['lines'][0]}  b: {p['lines'][1]}  point {p['mark']} {tuple(p['point'])}   " + \
        gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 3.4

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new story; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
