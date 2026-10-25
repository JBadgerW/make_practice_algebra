"""Khan Algebra 1, Lesson 6-3: Creating systems in context, from the old app's
Alg1_06_03 (twelve generated stories, every key right).

Which system of equations represents the situation? Khan's twelve stories:
chocolate blends, yarn for hats and scarves, walks and rides at two speeds,
and ages, each with its letters defined. The wrong systems are the old
ones: the rates or the totals traded, the multiple on the wrong letter, a
difference the wrong way round. Names only, no pronouns.

A problem: dict(type, story, prompt, choices, answer, source).
    choices  four systems, each "eq1 ; eq2" in the story's letters
check() reads the numbers back out of the story, builds the right system,
and finds the choices whose equations are each a multiple of one of its
equations: exactly one, the answer's.
"""
import re
from decimal import Decimal as D
from fractions import Fraction as F
from ... import gen
from ...gen import need, written
from ...typst import esc
from ...typmath import text as plain
from . import courses, twovar

NAME = FAMILY = "ka1_06_03"
FIXED = False
TITLE = "Lesson 6-3: Creating systems in context"
INSTRUCTIONS = "Which system of equations represents each situation?"
COURSES = courses(6)
TIMES = {2: "twice", 3: "three times", 4: "four times", 5: "five times"}
TIMES_OF = {w: k for k, w in TIMES.items()}
WORDS = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
WORDS_OF = {w: k for k, w in WORDS.items()}

TYPES = [
    dict(key="1", title="Two Totals",
         look="A total amount and a total cost (or time and distance, items and weight).",
         move="One equation adds the two amounts; the other adds each amount times its rate.", width="full"),
    dict(key="2", title="A Total and a Comparison",
         look="A total, and a sentence comparing the two amounts: twice as much, 15 more, equal distances.",
         move="One equation for the total; the other says the comparison in symbols. Check which letter gets the multiple.",
         width="full"),
    dict(key="3", title="Ages",
         look="Two people's ages: times as old, years older, years ago.",
         move="Write each sentence as an equation in the two ages. Years ago, subtract from both ages.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def eq(left, right):
    return f"{left} = {right}"

def lin(*terms):
    return written(*terms)

def sys(e1, e2):
    return f"{e1} ; {e2}"

# ------------------------------------------------------------------
# Stories: draw(r) -> the words; right(n) -> the system; wrong(n) -> three systems
# ------------------------------------------------------------------
def d_blend(r):
    dw, mw = r.randint(3, 7) * 10, r.randint(3, 7) * 10
    dc, mc = r.randint(10, 14), r.randint(8, 12)
    need(dc != mc)
    return dict(name=r.choice(gen.NAMES), w=dw + mw, dc=dc, mc=mc, cost=dw * dc + mw * mc)

def d_walk(r):
    bs, ps = r.randint(2, 6), r.randint(2, 6)
    need(bs != ps)
    bt, pt = r.randint(1, 4), r.randint(1, 4)
    return dict(name=r.choice(gen.NAMES), bs=bs, ps=ps, time=bt + pt, dist=bs * bt + ps * pt)

def d_yarn(r):
    hw, sw = D(r.randint(1, 5)) / 10, D(r.randint(1, 5)) / 10
    need(hw != sw)
    hn, sn = r.randint(5, 15), r.randint(5, 15)
    return dict(name=r.choice(gen.NAMES), hw=hw, sw=sw, weight=gen.coef(hw * hn + sw * sn), items=hn + sn)

def d_twice(r):
    m = r.randint(30, 50)
    k = r.randint(2, 3)
    return dict(name=r.choice(gen.NAMES), w=m * (k + 1), k=TIMES[k])

def d_more(r):
    diff, m = r.randint(2, 6) * 5, r.randint(12, 16) * 5
    return dict(name=r.choice(gen.NAMES), diff=diff, w=2 * m + diff)

def d_skate(r):
    bs, ps = r.randint(8, 10), r.randint(5, 7)
    return dict(name=r.choice(gen.NAMES), bs=bs, ps=ps, dist=r.randint(18, 24))

def d_yarn_times(r):
    hw, sw = D(r.randint(1, 4)) / 10, D(r.randint(1, 4)) / 10
    need(hw != sw)
    return dict(name=r.choice(gen.NAMES), hw=hw, sw=sw, k=TIMES[r.randint(2, 4)], weight=r.randint(4, 8))

def d_bike(r):
    bs, ps = r.randint(15, 20), r.randint(15, 20)
    need(bs != ps)
    return dict(name=r.choice(gen.NAMES), bs=bs, ps=ps, time=r.randint(2, 3))

def d_yarn_twice(r):
    hw, sw = D(r.randint(1, 5)) / 10, D(r.randint(1, 5)) / 10
    need(hw != sw)
    return dict(name=r.choice(gen.NAMES), hw=hw, sw=sw, k=TIMES[r.randint(2, 3)], items=r.randint(15, 25))

def initials(r):
    a, b = r.sample(gen.NAMES, 2)
    need(a[0] != b[0] and a[0].lower() not in "eio" and b[0].lower() not in "eio")
    return a, b, a[0].lower(), b[0].lower()

def d_ages_times(r):
    a, b, x, y = initials(r)
    age, k = r.randint(7, 12), r.randint(3, 5)
    return dict(a=a, b=b, x=x, y=y, k=TIMES[k], diff=age * k - age)

def d_ages_ago(r):
    a, b, x, y = initials(r)
    past, k = r.randint(2, 5), r.randint(2, 5)
    young = r.randint(1, 5)
    return dict(a=a, b=b, x=x, y=y, diff=young * k - young, ago=WORDS[past], k=TIMES[k])

def d_ages_sum(r):
    a, b, x, y = initials(r)
    la, ma, past = r.randint(15, 23), r.randint(24, 30), r.randint(2, 6)
    return dict(a=a, b=b, x=x, y=y, diff=ma - la, ago=WORDS[past], sum=la + ma - 2 * past)

def n_(n, k):
    return n[k] if not isinstance(n[k], F) else gen.coef(n[k])

STORIES = [
    dict(key="a", type="1", draw=d_blend,
         text="{name} blends dark chocolate and milk chocolate for an ice cream topping and needs {w} kg of chocolate "
              "in all. Dark chocolate costs ${dc} per kg and milk chocolate ${mc} per kg, and {name} will spend "
              "${cost}. Let d be the kilograms of dark chocolate and m the kilograms of milk chocolate.",
         right=lambda n: sys(eq(lin((1, "d"), (1, "m")), n_(n, "w")), eq(lin((n["dc"], "d"), (n["mc"], "m")), n_(n, "cost"))),
         wrong=lambda n: [sys(eq(lin((1, "d"), (1, "m")), n_(n, "cost")), eq(lin((n["dc"], "d"), (n["mc"], "m")), n_(n, "w"))),
                          sys(eq(lin((1, "d"), (1, "m")), n_(n, "w")), eq(lin((n["mc"], "d"), (n["dc"], "m")), n_(n, "cost"))),
                          sys(eq(lin((1, "d"), (1, "m")), n_(n, "cost")), eq(lin((n["mc"], "d"), (n["dc"], "m")), n_(n, "w")))]),
    dict(key="b", type="1", draw=d_walk,
         text="{name} walked from home to the beach at {bs} km/h, then from the beach to the park at {ps} km/h. The "
              "walk took {time} hours and covered {dist} km. Let b be the hours walking to the beach and p the hours "
              "walking to the park.",
         right=lambda n: sys(eq(lin((1, "b"), (1, "p")), n_(n, "time")), eq(lin((n["bs"], "b"), (n["ps"], "p")), n_(n, "dist"))),
         wrong=lambda n: [sys(eq(lin((n["bs"], "b"), (n["ps"], "p")), n_(n, "time")), eq(lin((1, "b"), (1, "p")), n_(n, "dist"))),
                          sys(eq(lin((1, "b"), (1, "p")), n_(n, "time")), eq(lin((n["ps"], "b"), (n["bs"], "p")), n_(n, "dist"))),
                          sys(eq(lin((1, "b"), (1, "p")), n_(n, "dist")), eq(lin((n["ps"], "b"), (n["bs"], "p")), n_(n, "time")))]),
    dict(key="c", type="1", draw=d_yarn,
         text="{name} is knitting hats and scarves. Each hat uses {hw} kg of yarn and each scarf {sw} kg. {name} "
              "wants to use {weight} kg of yarn to make {items} items in all. Let h be the number of hats and s the "
              "number of scarves.",
         right=lambda n: sys(eq(lin((n["hw"], "h"), (n["sw"], "s")), n_(n, "weight")), eq(lin((1, "h"), (1, "s")), n_(n, "items"))),
         wrong=lambda n: [sys(eq(lin((n["hw"], "h"), (n["sw"], "s")), n_(n, "items")), eq(lin((1, "h"), (1, "s")), n_(n, "weight"))),
                          sys(eq(lin((n["sw"], "h"), (n["hw"], "s")), n_(n, "weight")), eq(lin((1, "h"), (1, "s")), n_(n, "items"))),
                          sys(eq(lin((n["sw"], "h"), (n["hw"], "s")), n_(n, "items")), eq(lin((1, "h"), (1, "s")), n_(n, "weight")))]),
    dict(key="d", type="2", draw=d_twice,
         text="{name} blends dark chocolate and milk chocolate for an ice cream topping and needs {w} kg in all. The "
              "recipe calls for {k} as much dark chocolate as milk chocolate. Let d be the kilograms of dark chocolate "
              "and m the kilograms of milk chocolate.",
         right=lambda n: sys(eq(lin((1, "d"), (1, "m")), n_(n, "w")), eq("d", lin((TIMES_OF[n["k"]], "m")))),
         wrong=lambda n: [sys(eq(lin((1, "d"), (1, "m")), n_(n, "w")), eq(lin((TIMES_OF[n["k"]], "d")), "m")),
                          sys(eq(lin((TIMES_OF[n["k"]], "d"), (1, "m")), n_(n, "w")), eq(lin((TIMES_OF[n["k"]], "d")), "m")),
                          sys(eq(lin((1, "d"), (TIMES_OF[n["k"]], "m")), n_(n, "w")), eq("d", lin((TIMES_OF[n["k"]], "m"))))]),
    dict(key="e", type="2", draw=d_more,
         text="{name} blends dark chocolate and milk chocolate for an ice cream topping. {name} wants {diff} kg more "
              "dark chocolate than milk chocolate, and needs {w} kg in all. Let d be the kilograms of dark chocolate "
              "and m the kilograms of milk chocolate.",
         right=lambda n: sys(eq("d", lin((1, "m"), (n["diff"], ""))), eq(lin((1, "d"), (1, "m")), n_(n, "w"))),
         wrong=lambda n: [sys(eq("m", lin((1, "d"), (n["diff"], ""))), eq(lin((1, "d"), (1, "m")), n_(n, "w"))),
                          sys(eq("d", lin((n["diff"], "m"))), eq(lin((1, "d"), (1, "m")), n_(n, "w"))),
                          sys(eq("m", lin((n["diff"], "d"))), eq(lin((1, "d"), (1, "m")), n_(n, "w")))]),
    dict(key="f", type="2", draw=d_skate,
         text="{name} skated from home to the beach at {bs} km/h, then from the beach to the park at {ps} km/h. The "
              "whole trip was {dist} km, and the second part took twice as long as the first. Let b be the hours "
              "skating to the beach and p the hours skating to the park.",
         right=lambda n: sys(eq(lin((n["bs"], "b"), (n["ps"], "p")), n_(n, "dist")), eq("p", lin((2, "b")))),
         wrong=lambda n: [sys(eq(lin((n["bs"], "b"), (n["ps"], "p")), n_(n, "dist")), eq("b", lin((2, "p")))),
                          sys(eq(lin((n["ps"], "b"), (n["bs"], "p")), n_(n, "dist")), eq("p", lin((2, "b")))),
                          sys(eq(lin((n["ps"], "b"), (n["bs"], "p")), n_(n, "dist")), eq("b", lin((2, "p"))))]),
    dict(key="g", type="2", draw=d_yarn_times,
         text="{name} is knitting hats and scarves. Each hat uses {hw} kg of yarn and each scarf {sw} kg. {name} "
              "wants to make {k} as many scarves as hats and use {weight} kg of yarn. Let h be the number of hats "
              "and s the number of scarves.",
         right=lambda n: sys(eq("s", lin((TIMES_OF[n["k"]], "h"))), eq(lin((n["sw"], "s"), (n["hw"], "h")), n_(n, "weight"))),
         wrong=lambda n: [sys(eq("h", lin((TIMES_OF[n["k"]], "s"))), eq(lin((n["sw"], "s"), (n["hw"], "h")), n_(n, "weight"))),
                          sys(eq("s", lin((TIMES_OF[n["k"]], "h"))), eq(lin((n["sw"], "h"), (n["hw"], "s")), n_(n, "weight"))),
                          sys(eq("h", lin((TIMES_OF[n["k"]], "s"))), eq(lin((n["sw"], "h"), (n["hw"], "s")), n_(n, "weight")))]),
    dict(key="h", type="2", draw=d_bike,
         text="{name} biked from home to the beach at {bs} km/h, then from the beach to the park at {ps} km/h. The "
              "rides took {time} hours in all, and the two distances were equal. Let b be the hours riding to the "
              "beach and p the hours riding to the park.",
         right=lambda n: sys(eq(lin((1, "b"), (1, "p")), n_(n, "time")), eq(lin((n["bs"], "b")), lin((n["ps"], "p")))),
         wrong=lambda n: [sys(eq(lin((1, "b"), (1, "p")), n_(n, "time")), eq(lin((n["ps"], "b")), lin((n["bs"], "p")))),
                          sys(eq("b", lin((1, "p"), (n["time"], ""))), eq(lin((n["bs"], "b")), lin((n["ps"], "p")))),
                          sys(eq("b", lin((1, "p"), (n["time"], ""))), eq(lin((n["ps"], "b")), lin((n["bs"], "p"))))]),
    dict(key="i", type="2", draw=d_yarn_twice,
         text="{name} is knitting hats and scarves. Each hat uses {hw} kg of yarn and each scarf {sw} kg. {name} "
              "wants to use {k} as much yarn for scarves as for hats, and to make {items} items in all. Let h be the "
              "number of hats and s the number of scarves.",
         right=lambda n: sys(eq(lin((n["sw"], "s")), lin((TIMES_OF[n["k"]] * n["hw"], "h"))), eq(lin((1, "h"), (1, "s")), n_(n, "items"))),
         wrong=lambda n: [sys(eq(lin((n["hw"], "h")), lin((TIMES_OF[n["k"]] * n["sw"], "s"))), eq(lin((1, "h"), (1, "s")), n_(n, "items"))),
                          sys(eq(lin((n["sw"], "s"), (n["hw"], "h")), n_(n, "items")), eq("s", lin((TIMES_OF[n["k"]], "h")))),
                          sys(eq(lin((n["sw"], "s"), (n["hw"], "h")), n_(n, "items")), eq("h", lin((TIMES_OF[n["k"]], "s"))))]),
    dict(key="j", type="3", draw=d_ages_times,
         text="{b} is {k} as old as {a} and is also {diff} years older than {a}. Let {y} be {b}'s age and {x} be "
              "{a}'s age.",
         right=lambda n: sys(eq(n["y"], lin((TIMES_OF[n["k"]], n["x"]))), eq(n["y"], lin((1, n["x"]), (n["diff"], "")))),
         wrong=lambda n: [sys(eq(n["x"], lin((TIMES_OF[n["k"]], n["y"]))), eq(n["x"], lin((1, n["y"]), (n["diff"], "")))),
                          sys(eq(lin((TIMES_OF[n["k"]], n["y"])), n["x"]), eq(n["y"], lin((1, n["x"]), (n["diff"], "")))),
                          sys(eq(n["y"], lin((TIMES_OF[n["k"]], n["x"]))), eq(n["y"], lin((1, n["x"]), (-n["diff"], ""))))]),
    dict(key="k", type="3", draw=d_ages_ago,
         text="{a} is {diff} years older than {b}. {ago} years ago, {a} was {k} as old as {b}. Let {x} be {a}'s age "
              "and {y} be {b}'s age.",
         right=lambda n: sys(eq(n["x"], lin((1, n["y"]), (n["diff"], ""))),
                             eq(lin((1, n["x"]), (-WORDS_OF[n["ago"]], "")), lin((TIMES_OF[n["k"]], f"({lin((1, n['y']), (-WORDS_OF[n['ago']], ''))})")))),
         wrong=lambda n: [sys(eq(n["y"], lin((1, n["x"]), (n["diff"], ""))),
                              eq(lin((1, n["y"]), (-WORDS_OF[n["ago"]], "")), lin((TIMES_OF[n["k"]], f"({lin((1, n['x']), (-WORDS_OF[n['ago']], ''))})")))),
                          sys(eq(n["x"], lin((1, n["y"]), (n["diff"], ""))),
                              eq(lin((1, n["x"]), (-WORDS_OF[n["ago"]], "")), lin((TIMES_OF[n["k"]], n["y"])))),
                          sys(eq(n["x"], lin((1, n["y"]), (n["diff"], ""))),
                              eq(lin((1, n["x"]), (WORDS_OF[n["ago"]], "")), lin((TIMES_OF[n["k"]], f"({lin((1, n['y']), (WORDS_OF[n['ago']], ''))})"))))]),
    dict(key="l", type="3", draw=d_ages_sum,
         text="{a} is {diff} years younger than {b}. {ago} years ago, the sum of their ages was {sum}. Let {x} be "
              "{a}'s age and {y} be {b}'s age.",
         right=lambda n: sys(eq(n["x"], lin((1, n["y"]), (-n["diff"], ""))),
                             eq(lin((1, f"({lin((1, n['x']), (-WORDS_OF[n['ago']], ''))})"), (1, f"({lin((1, n['y']), (-WORDS_OF[n['ago']], ''))})")), n_(n, "sum"))),
         wrong=lambda n: [sys(eq(n["x"], lin((1, n["y"]), (n["diff"], ""))),
                              eq(lin((1, f"({lin((1, n['x']), (-WORDS_OF[n['ago']], ''))})"), (1, f"({lin((1, n['y']), (-WORDS_OF[n['ago']], ''))})")), n_(n, "sum"))),
                          sys(eq(lin((1, n["x"]), (-WORDS_OF[n["ago"]], "")), lin((1, f"({lin((1, n['y']), (-WORDS_OF[n['ago']], ''))})"), (-n["diff"], ""))),
                              eq(lin((1, n["x"]), (1, n["y"])), n_(n, "sum"))),
                          sys(eq(n["x"], lin((1, n["y"]), (-n["diff"], ""))), eq(lin((1, n["x"]), (1, n["y"])), n_(n, "sum")))]),
]
STORY = {s["key"]: s for s in STORIES}
BY_TYPE = {k: [s for s in STORIES if s["type"] == k] for k in KEYS}
LETTERS = {"a": ("d", "m"), "b": ("b", "p"), "c": ("h", "s"), "d": ("d", "m"), "e": ("d", "m"), "f": ("b", "p"),
           "g": ("h", "s"), "h": ("b", "p"), "i": ("h", "s")}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def letters_of(st, n):
    return LETTERS.get(st["key"]) or (n["x"], n["y"])

def read(st, prompt):
    """The story's numbers and names, read back from its words."""
    out = {}
    for k, s in gen.read(st["text"], prompt).items():
        try:
            out[k] = D(s.replace("$", "").replace(",", "")) if "." in s else int(s.replace("$", "").replace(",", ""))
        except ValueError:
            out[k] = s
    return out

def matches(system, right, u, v):
    """Every equation of system is a multiple of one of right's, and right's both appear."""
    def triple(q):
        return twovar.coefficients(q, u, v)
    def proportional(p, q):
        return all(p[i] * q[j] == p[j] * q[i] for i in range(3) for j in range(3))
    rs = [triple(q) for q in twovar.equations(right)]
    cs = [triple(q) for q in twovar.equations(system)]
    return all(any(proportional(c, r) for r in rs) for c in cs) and all(any(proportional(c, r) for c in cs) for r in rs)

def draw(entry, r, tpl):
    st = BY_TYPE[entry][tpl]
    w = st["draw"](r)
    prompt = gen.fill(st["text"], **{k: (gen.coef(x) if isinstance(x, D) else x) for k, x in w.items()})
    n = read(st, prompt)
    right, wrong = st["right"](n), st["wrong"](n)
    u, v = letters_of(st, n)
    need(not any(matches(s, right, u, v) for s in wrong) and len(set(wrong)) == 3)
    choices, letter = gen.lettered(r, right, wrong)
    return dict(story=st["key"], prompt=prompt, choices=choices, answer=letter)

def check(p):
    try:
        st = STORY[p["story"]]
        n = read(st, p["prompt"])
        u, v = letters_of(st, n)
        right = [gen.ABC[i] for i, c in enumerate(p["choices"]) if matches(c, st["right"](n), u, v)]
        return "checked" if right == gen.letters_of(p["answer"]) else "failed"
    except (ValueError, KeyError):
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(BY_TYPE[e]))

LET = re.compile(r"(Let |and )([a-z])( be | the )")

def typst(p, gap="0.3em"):
    story = LET.sub(r"\1$\2$\3", esc(p["prompt"]))            # Let $h$ be ... and $s$ the ...
    return f"{story} \\\n    {gen.choices_typst([twovar.system_typst(c) for c in p['choices']], 'grid')}"

def answer_typst(p):
    a = gen.letters_of(p["answer"])[0]
    return f"{a}. {twovar.system_typst(p['choices'][gen.ABC.index(a)])}"

def text(p):
    return p["prompt"] + "      " + gen.choices_text(p["choices"], plain)

def answer_text(p):
    return f"{p['answer']}. {plain(gen.chosen(p)[0])}"

def height(p):
    return 0.2 * (8 + len(p["prompt"]) // 90)

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new story; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
