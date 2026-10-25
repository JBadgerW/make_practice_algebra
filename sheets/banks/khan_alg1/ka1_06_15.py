"""Khan Algebra 1, Lesson 6-15: Systems of equations word problems (with zero
and infinite solutions), from the old app's Alg1_06_15 (sixteen stories; no.
6 marked two choices correct, "many solutions", which was right, and "no
solution").

A story's system may have one solution, none, or infinitely many: each
problem draws which, and its numbers to match (the second purchase a
multiple of the first, or not). Type 1 asks Khan's way, "Can we find a
unique price?": Yes with values, "No; the system has no solution", or "No;
the system has many solutions". Type 2 asks for the values, with "There is
not enough information" and "The given information describes an impossible
situation" among the choices. Wrong value choices: the right values swapped,
or values that fit only the first equation.

A problem: dict(type, story, prompt, choices, answer, source).
check() reads the numbers back out of the story, solves its system, and
requires the one choice that says what the system does.
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need
from ...typst import esc
from . import courses
from .stories import money, show, fill_story, solve_story, numbers

NAME = FAMILY = "ka1_06_15"
FIXED = False
TITLE = "Lesson 6-15: Systems of equations word problems (with zero and infinite solutions)"
INSTRUCTIONS = "Choose 1 answer."
COURSES = courses(6)
NONE1, MANY1 = "No; the system has no solution.", "No; the system has many solutions."
IMPOSSIBLE = "The given information describes an impossible situation."

TYPES = [
    dict(key="1", title="Is There a Unique Answer?",
         look="Two purchases (or two days, two machines) of the same two things.",
         move="Write the system. If one equation is a multiple of the other, there are many solutions; if only the "
              "left sides are multiples, none. Otherwise solve it.", width="full"),
    dict(key="2", title="Enough Information?",
         look="A story whose two facts may not pin down the answer.",
         move="Write the system. The same equation twice: not enough information. Contradictory equations: an "
              "impossible situation. Otherwise solve it.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def two_purchases(r, outcome, lo=1, hi=9, price=lambda r: r.randint(2, 9)):
    """Counts (a1, b1), (a2, b2) and totals for prices (u, v): the second row a multiple of the first
    (with its total too: many; without: none), or not (one)."""
    u, v = price(r), price(r)
    a1, b1 = r.randint(lo, hi), r.randint(lo, hi)
    t1 = a1 * u + b1 * v
    if outcome == "one":
        a2, b2 = r.randint(lo, hi), r.randint(lo, hi)
        need(a1 * b2 != a2 * b1)
        t2 = a2 * u + b2 * v
    else:
        k = r.choice((2, 3)) if r.random() < 0.6 or a1 % 2 or b1 % 2 else F(1, 2)
        a2, b2, t2 = a1 * k, b1 * k, t1 * k
        if outcome == "none":
            t2 += r.choice((-1, 1)) * r.randint(1, 3) * (u if isinstance(u, int) else F(1, 4))
        need(int(a2) == a2 and int(b2) == b2 and t2 > 0)
    return dict(a1=a1, b1=b1, t1=t1, a2=int(a2), b2=int(b2), t2=t2)

def d_fruit(r, outcome):
    n = two_purchases(r, outcome, 2, 9, lambda r: F(r.randint(2, 12), 4))
    return dict(n, t1=money(n["t1"]), t2=money(n["t2"]))

def d_denarius(r, outcome):
    return two_purchases(r, outcome, 2, 12, lambda r: r.randint(1, 6))

def d_rockets(r, outcome):
    return two_purchases(r, outcome, 2, 8, lambda r: r.randint(2, 6))

def d_books(r, outcome):
    n = two_purchases(r, outcome, 2, 15, lambda r: F(r.randint(4, 16), 4))
    return dict(n, name=r.choice(gen.NAMES), t1=money(n["t1"]), t2=money(n["t2"]))

def d_buttons(r, outcome):
    return two_purchases(r, outcome, 2, 9, lambda r: r.randint(3, 10))

def d_essays(r, outcome):
    n = two_purchases(r, outcome, 2, 6, lambda r: r.randint(4, 20))
    return n

def d_skydive(r, outcome):
    ki, kp = r.randint(2, 5), r.randint(2, 5)            # never "1 times"
    if outcome == "one":
        need(ki != kp)
    else:
        kp = ki
    i, p = r.randint(2, 15), r.randint(2, 15)
    visits, dives = i + p, ki * i + kp * p
    if outcome == "none":
        dives += r.choice((-1, 1)) * r.randint(1, ki)
    return dict(name=r.choice(gen.NAMES), ki=ki, kp=kp, visits=visits, dives=dives)

def d_phone(r, outcome):
    need(outcome != "many")                     # many would be "gained 0 percentage points"
    rc, ru = r.randint(1, 3), r.randint(2, 6)
    if outcome == "one":
        need(ru != 2 * rc)
    else:
        ru = 2 * rc
    t = r.randint(8, 12)
    delta = rc * 2 * t - ru * t
    if outcome == "none":
        delta += r.choice((-1, 1)) * r.randint(2, 10)
    need(delta != 0)
    return dict(name=r.choice(gen.NAMES), rc=rc, ru=ru, did="gained" if delta > 0 else "lost", change=abs(delta))

STORIES = [
    dict(key="a", type="1", text="A fruit stand needs ${t1} for {a1} apples and {b1} oranges. It also needs ${t2} for {a2} "
         "apples and {b2} oranges, at the same prices.",
         ask="Can we find a unique price for an apple and for an orange?",
         answer="Yes; they should charge ${u} for an apple and ${v} for an orange.", fmt=money, draw=d_fruit),
    dict(key="b", type="1", text="The denarius was a unit of money in ancient Rome. Suppose it costs the Roman government "
         "{t1} denarii a day to support {a1} legionaries and {b1} archers, and {t2} denarii a day to support {a2} "
         "legionaries and {b2} archers.",
         ask="Can we find a unique daily cost for each kind of soldier?",
         answer="Yes; a legionary costs {u} denarii a day and an archer {v} denarii.", draw=d_denarius),
    dict(key="c", type="1", text="A company makes rocket ships. Machine A and Machine B both make cockpits and propulsion "
         "systems, each at the same rates. Machine A ran for {t1} hours and made {a1} cockpits and {b1} propulsion "
         "systems. Machine B ran for {t2} hours and made {a2} cockpits and {b2} propulsion systems.",
         ask="Can we find a unique number of hours to make a cockpit and to make a propulsion system?",
         answer="Yes; a cockpit takes {u} hours and a propulsion system {v} hours.", draw=d_rockets),
    dict(key="d", type="2", text="{name}'s bookstore sold {a1} notebooks and {b1} newspapers for ${t1}. A day later, it sold "
         "{a2} notebooks and {b2} newspapers at the same prices, for ${t2}.",
         ask="How much does a notebook cost, and how much does a newspaper cost?", what="the prices",
         answer="A notebook costs ${u} and a newspaper costs ${v}.", fmt=money, draw=d_books),
    dict(key="e", type="2", text="Fiona's Fashion Store is known for its buttoned uniforms. {a1} shirts and {b1} jackets "
         "have {t1} buttons in all; {a2} shirts and {b2} jackets have {t2} buttons. Each shirt has the same number of "
         "buttons, and so does each jacket.",
         ask="How many buttons are on a shirt, and how many on a jacket?", what="the number of buttons",
         answer="A shirt has {u} buttons and a jacket has {v} buttons.", draw=d_buttons),
    dict(key="f", type="2", text="The Capulet and Montague families love writing. Last year, each Capulet wrote {a1} essays "
         "and each Montague {b1}, {t1} essays in all. This year, each Capulet wrote {a2} essays and each Montague "
         "{b2}, {t2} in all.",
         ask="How many Capulets and how many Montagues are there?", what="the number of Capulets and Montagues",
         answer="There are {u} Capulets and {v} Montagues.", draw=d_essays),
    dict(key="g", type="2", text="{name} skydives {ki} times on every island visited and {kp} times on every peninsula. In "
         "the last decade, {name} went skydiving {dives} times on the {visits} islands and peninsulas visited.",
         ask="How many islands and how many peninsulas did {name} visit?", what="the number of islands and peninsulas",
         answer="{name} visited {u} islands and {v} peninsulas.", draw=d_skydive),
    dict(key="h", type="2", text="When {name}'s phone charges, it gains {rc} percentage points each minute; when {name} uses "
         "it, it loses {ru} percentage points each minute. Once, {name} used the phone for some time, then charged it "
         "for twice as long. In the end, the phone had {did} {change} percentage points.",
         ask="How long did {name} use the phone, and how long did {name} charge it?", what="the times",
         answer="{name} used the phone for {u} minutes and charged it for {v} minutes.", draw=d_phone),
]
MODELS = {
    "a": lambda n: ((n["a1"], n["b1"], n["t1"]), (n["a2"], n["b2"], n["t2"])),
    "h": lambda n: ((-n["ru"], n["rc"], n["change"] if n["did"] == "gained" else -n["change"]), (2, -1, 0)),
    "g": lambda n: ((1, 1, n["visits"]), (n["ki"], n["kp"], n["dives"])),
}
for st in STORIES:
    st["model"] = MODELS.get(st["key"], MODELS["a"])
STORY = {s["key"]: s for s in STORIES}
BY_TYPE = {k: [s for s in STORIES if s["type"] == k] for k in KEYS}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def values(st, w, u, v):
    return gen.fill(st["answer"], **{k: x for k, x in w.items() if isinstance(x, str)},
                    u=st.get("fmt", show)(u), v=st.get("fmt", show)(v))

def not_enough(st, w):
    return gen.fill(f"There is not enough information to determine {st['what']}.", **w)

def right_choice(st, prompt):
    """The choice that says what the story's system does."""
    s = solve_story(st, prompt)
    w = {k: x for k, x in numbers(st, prompt).items() if isinstance(x, str)}
    if isinstance(s, tuple):
        return values(st, w, *s)
    if st["type"] == "1":
        return NONE1 if s == "none" else MANY1
    return IMPOSSIBLE if s == "none" else not_enough(st, w)

def decoys(st, prompt, r):
    """Two wrong value choices: the right values swapped, or values that fit only the first equation."""
    n = numbers(st, prompt)
    w = {k: x for k, x in n.items() if isinstance(x, str)}
    (a, b, c), _ = st["model"](n)
    s = solve_story(st, prompt)
    out = []
    if isinstance(s, tuple):
        out.append(values(st, w, s[1], s[0]))
    for _ in range(20):                                   # fits the first equation, nice numbers
        u = F(r.randint(1, 12)) if st.get("fmt") is not money else F(r.randint(2, 40), 4)
        if b and (c - a * u) / b > 0:
            v = (c - a * u) / b
            if v.denominator <= 4:
                out.append(values(st, w, u, v))
                if len(out) >= 2:
                    break
    return list(dict.fromkeys(out))

def draw(entry, r, tpl):
    st = BY_TYPE[entry][tpl]
    outcome = r.choice(("one", "none", "many"))
    prompt = fill_story(st, st["draw"](r, outcome))
    right = right_choice(st, prompt)
    vals = [right] if outcome == "one" else []
    vals += [d for d in decoys(st, prompt, r) if d != right]
    need(len(vals) >= 2)
    vals = vals[:2]
    r.shuffle(vals)
    w = {k: x for k, x in numbers(st, prompt).items() if isinstance(x, str)}
    words = [NONE1, MANY1] if entry == "1" else [not_enough(st, w), IMPOSSIBLE]
    choices = vals + words if entry == "1" else words + vals
    return dict(story=st["key"], prompt=prompt, choices=choices, answer=gen.ABC[choices.index(right)])

def check(p):
    try:
        right = right_choice(STORY[p["story"]], p["prompt"])
        return "checked" if p["choices"].count(right) == 1 and gen.chosen(p) == [right] else "failed"
    except (ValueError, KeyError):
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(BY_TYPE[e]))

def typst(p, gap="0.3em"):
    return f"{esc(p['prompt'])} \\\n    {gen.choices_typst([esc(c) for c in p['choices']])}"

def answer_typst(p):
    return esc(gen.choice_answer_typst(p))

def text(p):
    return p["prompt"] + "      " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 0.2 * (6 + len(p["prompt"]) // 90)

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
