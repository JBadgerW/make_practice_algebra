"""Khan Algebra 1, Lesson 8-18: Graph interpretation word problems, from the
old app's Alg1_08_18 (thirteen of Khan's, the graphs as screenshots,
without answers).

A story, the graph of its function, and three statements about it: match
each with the feature it describes, Khan's three: (A) a relative maximum or
minimum, (B) a positive or negative interval, (C) an increasing or
decreasing interval. Khan's stories where the sign means something: a
gym's net worth, a spice seller's profit, an elevator's altitude, a town's
temperature, a savings balance. Each statement is true of the graph (a
smooth curve whose turns and crossings are exactly known, curves.py), and
the three are in random order. Names only, no pronouns.

A problem: dict(type, story, name, ks, statements, answer, source).
    statements  [["min", 6], ["sign", -1, 2, 5], ["rise", 1, 6, 9]]   (kind, then its numbers)
    answer  "1-A, 2-B, 3-C"
check() tests each statement against the curve (the knot is a relative
extremum of that kind; the curve has that sign, or rises or falls, all
across the interval) and requires the key to match it to its feature.
"""
import re
from ... import gen
from ...gen import need
from ...graphs import Graph, PREAMBLE
from ...typst import esc
from . import courses
from . import curves

NAME = FAMILY = "ka1_08_18"
FIXED = False
TITLE = "Lesson 8-18: Graph interpretation word problems"
INSTRUCTIONS = "Match each statement with the feature of the graph it describes."
COURSES = courses(8)
FEATURES = ["Relative maximum or minimum", "Positive or negative interval", "Increasing or decreasing interval"]
FEATURE_OF = {"max": "A", "min": "A", "sign": "B", "rise": "C"}

# story: (function, its input, the setup, x unit, statements: max, min, positive, negative, rising, falling)
STORIES = {
    "gym": ("N", "t", "{name} opened a new martial arts gym. $N(t)$ models the gym's net worth (in thousands of dollars) "
            "$t$ months after it opened.", "months",
            {"max": "The gym's net worth reached a peak at {x} months.",
             "min": "The gym's net worth hit a low point at {x} months.",
             "pos": "The gym was worth more than nothing between {a} and {b} months.",
             "neg": "The gym's losses exceeded its profits between {a} and {b} months.",
             "up": "The gym's net worth grew from {a} to {b} months.",
             "down": "The gym's net worth shrank from {a} to {b} months."}),
    "spice": ("P", "w", "{name} sells ground paprika. $P(w)$ models the weekly profit (in dollars; a negative profit "
              "is a loss) when {name} sells $w$ kilograms in a week.", "kilograms",
              {"max": "Profit is at a peak when {name} sells {x} kilograms.",
               "min": "Profit is at a low point when {name} sells {x} kilograms.",
               "pos": "{name} makes money selling between {a} and {b} kilograms.",
               "neg": "{name} loses money selling between {a} and {b} kilograms.",
               "up": "Profit goes up as sales go from {a} to {b} kilograms.",
               "down": "Profit goes down as sales go from {a} to {b} kilograms."}),
    "elevator": ("A", "t", "{name} runs an elevator in a tall hotel with underground parking. $A(t)$ models the "
                 "elevator's altitude (in meters relative to the ground) $t$ minutes into a shift.", "minutes",
                 {"max": "The elevator reached a high point at {x} minutes.",
                  "min": "The elevator reached a low point at {x} minutes.",
                  "pos": "The elevator was above the ground from {a} to {b} minutes.",
                  "neg": "The elevator was below the ground from {a} to {b} minutes.",
                  "up": "The elevator was going up from {a} to {b} minutes.",
                  "down": "The elevator was going down from {a} to {b} minutes."}),
    "weather": ("T", "h", "$T(h)$ models the temperature (in degrees Celsius) in a mountain town $h$ hours after "
                "midnight on a winter day.", "hours",
                {"max": "The temperature peaked {x} hours after midnight.",
                 "min": "The temperature bottomed out {x} hours after midnight.",
                 "pos": "It was above freezing from {a} to {b} hours after midnight.",
                 "neg": "It was below freezing from {a} to {b} hours after midnight.",
                 "up": "It was warming up from {a} to {b} hours after midnight.",
                 "down": "It was cooling down from {a} to {b} hours after midnight."}),
    "savings": ("B", "m", "$B(m)$ models {name}'s bank balance (in dollars; negative means overdrawn) $m$ months into "
                "the year.", "months",
                {"max": "The balance reached a high point at {x} months.",
                 "min": "The balance reached a low point at {x} months.",
                 "pos": "{name}'s account had money in it from {a} to {b} months.",
                 "neg": "{name}'s account was overdrawn from {a} to {b} months.",
                 "up": "The balance was growing from {a} to {b} months.",
                 "down": "The balance was shrinking from {a} to {b} months."}),
}

TYPES = [
    dict(key="1", title="Match Statements to Features",
         look="A story, its graph, and three statements.",
         move="A high or low point: relative maximum or minimum. Above or below the horizontal axis for a while: "
              "positive or negative interval. Going up or down for a while: increasing or decreasing.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["story"], str(p["ks"]), str(p["statements"]))

def holds(ks, s):
    """Is the statement true of the curve?"""
    if s[0] in ("max", "min"):
        turns = curves.maxima(ks) if s[0] == "max" else curves.minima(ks)
        return any(x == s[1] for x, _ in turns)
    if s[0] == "sign":
        return curves.sign_on(ks, s[2], s[3]) == s[1]
    return curves.rising(ks, s[2], s[3]) == s[1]

def draw(entry, r, tpl):
    story = r.choice(list(STORIES))
    ks = curves.knots(r, 0, r.randint(12, 16), -8, 8, gap=(2, 4))
    need(any(y > 0 for _, y in ks) and any(y < 0 for _, y in ks))
    ext = r.choice([("max", x) for x, _ in curves.maxima(ks)] + [("min", x) for x, _ in curves.minima(ks)])
    signs = [(s, a, b) for s in (1, -1) for a in range(ks[0][0], ks[-1][0]) for b in range(a + 2, ks[-1][0] + 1)
             if curves.sign_on(ks, a, b) == s]
    need(signs)
    sign = max(signs, key=lambda t: (t[2] - t[1], r.random()))   # the longest stretch, as Khan's
    rises = [(d, x0, x1) for (x0, y0), (x1, y1) in zip(ks, ks[1:]) for d in [(y1 > y0) - (y1 < y0)] if d]
    rise = r.choice(rises)
    statements = [list(ext), ["sign", *sign], ["rise", *rise]]
    r.shuffle(statements)
    answer = ", ".join(f"{i}-{FEATURE_OF[s[0]]}" for i, s in enumerate(statements, 1))
    return dict(story=story, name=r.choice(gen.NAMES), ks=[list(k) for k in ks], statements=statements, answer=answer)

PAIR = re.compile(r"(\d)\s*-\s*([ABC])")

def check(p):
    try:
        ks = [tuple(k) for k in p["ks"]]
        said = dict(PAIR.findall(p["answer"].upper()))
        ok = len(said) == len(p["statements"]) and all(
            holds(ks, s) and said.get(str(i)) == FEATURE_OF[s[0]] for i, s in enumerate(p["statements"], 1))
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def sentence(p, s):
    words = STORIES[p["story"]][4]
    if s[0] in ("max", "min"):
        t = words[s[0]].format(x=s[1], name=p["name"])
    elif s[0] == "sign":
        t = words["pos" if s[1] > 0 else "neg"].format(a=s[2], b=s[3], name=p["name"])
    else:
        t = words["up" if s[1] > 0 else "down"].format(a=s[2], b=s[3], name=p["name"])
    return t

def graph(p):
    f, v = STORIES[p["story"]][:2]
    x1 = p["ks"][-1][0]
    g = Graph(x=(0, x1 + 1), y=(-9, 9), width=5.2, height=4.4, xlabel=v, ylabel=f"{f}({v})")
    curves.draw(g, [tuple(k) for k in p["ks"]], ends="closed")
    return g.typst()

def typst(p, gap="0.3em"):
    setup = STORIES[p["story"]][2].format(name=p["name"])
    rows = ", ".join(f"[({i})], [{esc(sentence(p, s))}]" for i, s in enumerate(p["statements"], 1))
    feats = ", ".join(f"[{a}.], [{f}]" for a, f in zip("ABC", FEATURES))
    left = (f"{setup} #v(0.4em) *Statements* #v(0.2em) #grid(columns: (auto, 1fr), gutter: 0.5em, {rows}) "
            f"#v(0.4em) *Features* #v(0.2em) #grid(columns: (auto, 1fr), gutter: 0.5em, {feats})")
    return f"#grid(columns: (1fr, auto), column-gutter: 1em, [{left}], [{graph(p)}])"

def answer_typst(p):
    return p["answer"]

def text(p):
    return STORIES[p["story"]][2].format(name=p["name"]).replace("$", "") + "  " + \
        "  ".join(f"{i}. {sentence(p, s)}" for i, s in enumerate(p["statements"], 1))

def answer_text(p):
    return p["answer"]

def height(p):
    return 3.2

def edit_text(p):
    return text(p)

def from_edit(t, old):
    raise ValueError("reroll for a new story; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=", ".join(f"{i}-{a}" for i, a in PAIR.findall(t.upper())))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
