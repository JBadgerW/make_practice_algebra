"""Khan Algebra 1, Lesson 8-20: Average rate of change word problems, from the
old app's Alg1_08_20 (twenty of Khan's, the graphs as screenshots, without
answers).

A story's graph, its points on the grid lines (each story its own scale):
the temperature by the hour, a plant's length by the week, the fuel left
by the kilometer, a hiker's altitude, a video's views, the price of a pack
of bulbs. Type 1: when did it increase (decrease) faster, over one interval
or the next, or at the same rate? Khan's three choices. Type 2: the
average rate of change over an interval, choose 1 of four; the wrong ones
are the usual misreadings: the change in input over the change in output,
the change alone, or an end read off by a grid line. Names only, no
pronouns.

A problem: dict(type, story, ys, ..., choices, answer, source).
    ys  the values at the grid x's (in the story's units)    Type 1: a, b, c (x's)   Type 2: a, b
check() computes the rates from the graph's points.
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need
from ...graphs import Graph, PREAMBLE
from ...typst import esc
from . import courses

NAME = FAMILY = "ka1_08_20"
FIXED = False
TITLE = "Lesson 8-20: Average rate of change word problems"
INSTRUCTIONS = "Choose 1 answer."
COURSES = courses(8)

# story: (quantity, x name, y name, x0, x1, xstep, y1, ystep, steps allowed, x words, rate unit, setup)
STORIES = {
    "temperature": ("the temperature", "Hours after midnight", "Temperature (°C)", 0, 24, 2, 32, 2, (-2, -1, 0, 1, 2),
                    lambda x: (f"{x % 12 or 12} {'am' if x < 12 else 'pm'}" if x != 24 else "midnight"),
                    "degrees Celsius per hour", "The graph shows the temperature in a town over one day."),
    "plant": ("the plant's length", "Weeks", "Length (cm)", 0, 20, 2, 60, 5, (0, 1, 1, 2, 3),
              lambda x: f"week {x}", "centimeters per week", "The graph shows a plant's length as it grows."),
    "fuel": ("the fuel in the tank", "Distance (km)", "Fuel (L)", 0, 500, 50, 60, 5, (-3, -2, -1, -1, 0),
             lambda x: f"{x} km", "liters per kilometer", "{name} drove a truck. The graph shows the fuel left in "
             "the tank by the distance driven."),
    "hike": ("{name}'s altitude", "Hours", "Altitude (m)", 0, 12, 1, 800, 50, (-2, -1, 0, 1, 2, 3),
             lambda x: f"hour {x}", "meters per hour", "{name} went hiking. The graph shows {name}'s altitude "
             "(meters above sea level) by the hour."),
    "views": ("the number of views", "Hours", "Views (thousands)", 0, 24, 2, 50, 2, (0, 1, 2, 3),
              lambda x: f"hour {x}", "thousand views per hour", "{name} posted a funny video. The graph shows its "
              "views (in thousands) by the hour since it went up."),
    "bulbs": ("the price of a pack", "Bulbs in a pack", "Price ($)", 0, 24, 2, 30, 2, (0, 1, 1, 2),
              lambda x: f"{x} bulbs", "dollars per bulb", "The graph shows the price of a pack of light bulbs at a "
              "store by the number of bulbs in the pack."),
}

TYPES = [
    dict(key="1", title="When Was It Faster?",
         look="A story's graph and two intervals one after the other.",
         move="Find the change over each interval and divide by its length. The bigger rate (in size) is faster; "
              "the same rate means the graph is one straight line there.", width="full"),
    dict(key="2", title="The Average Rate",
         look="A story's graph and an interval.",
         move="Read the values at both ends. Rate = (change in output)/(change in input), in the story's units.",
         width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["story"], str(p["ys"]), p.get("a"), p.get("b"), p.get("c"))

def xs_of(story):
    _, _, _, x0, x1, step, *_ = STORIES[story]
    return list(range(x0, x1 + 1, step))

def at(p, x):
    return F(p["ys"][xs_of(p["story"]).index(x)])

def rate(p, a, b):
    return (at(p, b) - at(p, a)) / (b - a)

def number(q):
    """A rate as Khan writes it: 4, 1.5, 0.25, or 1/6."""
    q = F(q)
    if q.denominator == 1:
        return str(q.numerator)
    if all(d in (2, 5) for d in factors(q.denominator)):
        return f"{float(q):g}"
    return f"{q.numerator}/{q.denominator}"

def factors(n):
    out, d = [], 2
    while n > 1:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    return out

def values(r, story):
    _, _, _, x0, x1, step, y1, ystep, steps, *_ = STORIES[story]
    n = (x1 - x0) // step + 1
    top = y1 // ystep
    start = top - 1 if min(steps) < 0 and max(steps) <= 0 else (1 if min(steps) >= 0 else r.randint(top // 4, 3 * top // 4))
    ys = [start]
    for _ in range(n - 1):
        ys.append(min(top - 1, max(1, ys[-1] + r.choice(steps))))
    return [y * ystep for y in ys]

def draw(entry, r, tpl):
    story = r.choice(list(STORIES))
    p = dict(story=story, name=r.choice(gen.NAMES), ys=values(r, story))
    xs = xs_of(story)
    phrase = STORIES[story][9]
    if entry == "1":
        i = r.randint(0, len(xs) - 3)
        j = r.randint(i + 1, min(len(xs) - 2, i + 3))
        k = r.randint(j + 1, min(len(xs) - 1, j + 3))
        a, b, c = xs[i], xs[j], xs[k]
        r1, r2 = rate(p, a, b), rate(p, b, c)
        need(r1 != 0 and r2 != 0 and (r1 > 0) == (r2 > 0))       # both up or both down
        up = r1 > 0
        word = "increased" if up else "decreased"
        choices = [f"Between {phrase(a)} and {phrase(b)}", f"Between {phrase(b)} and {phrase(c)}",
                   f"It {word} at the same rate over both intervals"]
        faster = 2 if abs(r1) == abs(r2) else (0 if abs(r1) > abs(r2) else 1)
        choices, answer = gen.in_order(choices, choices[faster])
        return dict(p, a=a, b=b, c=c, up=up, choices=choices, answer=answer)
    i = r.randint(0, len(xs) - 2)
    j = r.randint(i + 1, min(len(xs) - 1, i + 5))
    a, b = xs[i], xs[j]
    q = rate(p, a, b)
    need(q != 0)
    unit = STORIES[story][10]
    right = f"{number(abs(q))} {unit}"
    dy = abs(at(p, b) - at(p, a))
    wrong = [f"{number(F(b - a) / dy)} {unit}", f"{number(dy)} {unit}"]
    if j + 1 < len(xs):
        wrong.append(f"{number(abs(rate(p, a, xs[j + 1])))} {unit}")
    if i > 0:
        wrong.append(f"{number(abs(rate(p, xs[i - 1], b)))} {unit}")
    wrong = [w for w in dict.fromkeys(wrong) if w != right]
    need(len(wrong) >= 3)
    choices, answer = gen.lettered(r, right, r.sample(wrong, 3))
    return dict(p, a=a, b=b, up=q > 0, choices=choices, answer=answer)

def check(p):
    try:
        if p["type"] == "1":
            r1, r2 = rate(p, p["a"], p["b"]), rate(p, p["b"], p["c"])
            ok = (r1 > 0) == (r2 > 0) == p["up"] and r1 != 0
            faster = 2 if abs(r1) == abs(r2) else (0 if abs(r1) > abs(r2) else 1)
            ok = ok and gen.letters_of(p["answer"]) == [gen.ABC[faster]]
        else:
            q = rate(p, p["a"], p["b"])
            said = gen.chosen(p)
            ok = (q > 0) == p["up"] and len(said) == 1 and \
                said[0].split()[0] == number(abs(q)) and \
                [c.split()[0] for c in p["choices"]].count(number(abs(q))) == 1
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def graph(p):
    _, xl, yl, x0, x1, step, y1, ystep, *_ = STORIES[p["story"]]
    g = Graph(x=(x0, x1), y=(0, y1), width=5.6, height=4.4, step=(step, ystep), xlabel=xl, ylabel=yl.replace("$", "\\$"))
    g.polyline(list(zip(xs_of(p["story"]), p["ys"])), ends=None)
    for x, y in zip(xs_of(p["story"]), p["ys"]):
        g.point(x, y, color="blue")
    return g.typst()

def question(p):
    quantity = STORIES[p["story"]][0].format(name=p["name"])
    word = "increase" if p["up"] else "decrease"
    phrase = STORIES[p["story"]][9]
    if p["type"] == "1":
        return f"When did {quantity} {word} faster?"
    return (f"What is the average rate at which {quantity} {word}s from {phrase(p['a'])} to {phrase(p['b'])}?"
            .replace("{name}", p["name"]))

def typst(p, gap="0.3em"):
    setup = STORIES[p["story"]][11].format(name=p["name"])
    left = f"{esc(setup)} {esc(question(p))} #v(0.3em) {gen.choices_typst([esc(c) for c in p['choices']])}"
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{left}], [{graph(p)}])"

def answer_typst(p):
    return esc(gen.choice_answer_typst(p))

def text(p):
    return f"{question(p)}  points {list(zip(xs_of(p['story']), p['ys']))}   " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 2.4

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
