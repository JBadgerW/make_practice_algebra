"""Lesson 2-2's word problems, Types 7 to 12: not a bank of its own (no NAME), but the
part of point_slope_2_2 that writes, checks, and shows them. Each type is one of the
teacher's word problems (~/Documents/alg1/unit_2/lesson_2-2_Point-Slope_Form/
2-2_world_problems.md), with the same logic in four stories ("a" is the source's own
setting) and new numbers every draw.

    Type  source  the logic                                         the key
    7     Ex. 4a  prices for two party sizes; is a budget enough     y - 725 = 12 (x - 50); yes or no, and the price
                  for a third?
    8     35      a rate per hour and one total: the one-time fee    y - 93.75 = 12.50 (x - 5.5); the fee is b
    9     36      what is owed after w1 and after w2 weeks           the amount borrowed (b), the weekly payment
                                                                     (the slope), what each form shows
    10    37      a table of job sizes and prices                    both forms; the slope is the cost each; the
                                                                     y-intercept, in slope-intercept form, the fee
    11    38      a table at x = 0, 1, 2, 3: which context fits?     one letter
    12    40      two readings of a level rising at a constant rate  point-slope form, the rate is its slope;
                                                                     slope-intercept form, the start is b

Every story says what x and y stand for. Point-slope form goes through the story's
first reading (an edited answer through any of its readings is accepted) and is
written as Lesson 2-2 writes it, y - 725 = 12 (x - 50), with money as dollars and
cents (y - 93.75 = 12.50 (x - 5.5)) and other decimals as decimals; slope-intercept
form is read as in Lesson 2-1's word problems (words_2_1.read_equation). No pronouns:
a name is repeated.

A problem: dict(type, story, prompt, answer[, choices], source), as in words_2_1: the
prompt is the story's words; the answer its parts, "; " between (Type 11: a letter).
check() reads the numbers back out of the words with the story's own template, solves
forward from them, and compares each equation's value and form, each sentence word for
word, and (Type 11) each choice by reading what it says.
"""
import re
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy
from .words_2_1 import (num, cents, dollars, number, plural, equation, read_equation, through,
                        math_letters, PART)

TYPES_ = ("7", "8", "9", "10", "11", "12")
STORIES = "abcd"
WORDS = ("who",)

TYPES = [
    dict(key="7", title="Word Problems: Is the Budget Enough?",
         instructions="Write each equation in point-slope form, then answer the question.",
         look="Prices for two sizes of the same kind of party, and a budget for a third size.",
         move="The two prices are two points (guests, price). The slope is the change in price over the change in "
              "guests: (1925 − 725)/(150 − 50) = 12. Write y − 725 = 12(x − 50), then put in the new number of "
              "guests and compare the price with the budget.",
         width="full", space="1.4in"),
    dict(key="8", title="Word Problems: Finding the One-Time Fee",
         instructions="Answer each part. Write each equation in the form the problem asks for.",
         look="An hourly rate, a one-time fee you aren't told, and one rental's total.",
         move="The rental is a point (hours, total) and the hourly rate is the slope: y − 93.75 = 12.50(x − 5.5). "
              "The fee is the cost at 0 hours, the y-intercept: write it in slope-intercept form, y = 12.50x + 25.",
         width="full", space="1.4in"),
    dict(key="9", title="Word Problems: Paying Back a Loan",
         instructions="Answer each part.",
         look="What someone owes after two different numbers of weeks, paying the same amount each week.",
         move="The two readings are points (weeks, owed). The slope is the change in what's owed each week: "
              "(228 − 456)/(5 − 2) = −76, so the payment is 76 dollars. The amount borrowed is the y-intercept: "
              "y = −76x + 608.",
         width="full", space="1.8in"),
    dict(key="10", title="Word Problems: Two Forms from a Table",
         instructions="Answer each part. Write each equation in the form the problem asks for.",
         look="A table of job sizes and prices that go up by the same amount, with a one-time set-up fee.",
         move="Slope from two rows: (140 − 100)/(50 − 25) = 1.60, the cost of each. Point-slope form through a row: "
              "y − 100 = 1.60(x − 25). Slope-intercept form shows the set-up fee as b: y = 1.60x + 60.",
         width="full", space="1.8in"),
    dict(key="11", title="Word Problems: Matching a Context to a Table",
         instructions="Choose the real-world context that matches the data in each table.",
         look="A table at x = 0, 1, 2, 3, and contexts that describe a starting amount and an amount each.",
         move="The value at x = 0 is the starting amount, and the change from one row to the next is the amount "
              "each. Pick the context with that start and that amount each.",
         width="full", space="0.3in"),
    dict(key="12", title="Word Problems: Rising at a Constant Rate",
         instructions="Answer each part. Write each equation in the form the problem asks for.",
         look="Two readings of a height rising at a constant rate, and a question about where it started.",
         move="The readings are points (time, height). The slope is the rate: (20 − 9)/(42 − 14.5) = 0.4. "
              "Write y − 9 = 0.4(x − 14.5). Slope-intercept form shows the start as b: y = 0.4x + 3.2.",
         width="full", space="1.8in"),
]

# ------------------------------------------------------------------
# Point-slope form with decimals: y - 93.75 = 12.50 (x - 5.5)
# ------------------------------------------------------------------
def point_slope(m, x1, y1, cash=False):
    """y - y1 = m (x - x1), signs worked out; cash: m and y1 as dollars (12.50, 93.75)."""
    show = dollars if cash else num
    left = "y" if y1 == 0 else f"y {'-' if y1 > 0 else '+'} {show(abs(y1))}"
    inner = "x" if x1 == 0 else f"x {'-' if x1 > 0 else '+'} {num(abs(x1))}"
    if m == 1:
        right = inner
    elif m == -1:
        right = f"-({inner})" if x1 else "-x"
    else:
        right = f"{'-' if m < 0 else ''}{show(abs(m))} " + (f"({inner})" if x1 else "x")
    return f"{left} = {right}"

N = r"\d+(?:\.\d+)?(?:/\d+)?"
PS_LEFT = re.compile(rf"y(?: (?P<s>[+-]) (?P<n>{N}))?")
PS_RIGHT = re.compile(rf"(?P<c>-?{N} |-)?\(x (?P<s>[+-]) (?P<n>{N})\)|(?P<bare>x (?P<s2>[+-]) (?P<n2>{N}))")
X, Y = sp.Symbol("x"), sp.Symbol("y")

def lowest(s):
    return "/" not in s or ("." not in s and str(F(s)) == s and F(s).denominator != 1)

def read_point_slope(t):
    """(m, x1, y1) of an answer written y - y1 = m (x - x1), signs worked out, a slope of 1 or -1 as
    x - 4 and -(x - 4), fractions in lowest terms; the text must say what it was read as. None if not."""
    t = " ".join(t.replace("−", "-").split())
    lhs, eq, rhs = t.partition(" = ")
    gl, gr = PS_LEFT.fullmatch(lhs), PS_RIGHT.fullmatch(rhs)
    if not eq or not gl or not gr or gl["n"] is None:
        return None
    y1 = F(gl["n"]) * (1 if gl["s"] == "-" else -1)
    if gr["bare"]:
        m, s, n = F(1), gr["s2"], gr["n2"]
    else:
        c = (gr["c"] or "").strip()
        if c in ("", "1", "-1"):
            return None
        m, s, n = (F(-1) if c == "-" else F(c)), gr["s"], gr["n"]
    if any(not lowest(x) for x in (gl["n"], n, (gr["c"] or "").strip().lstrip("-"))):
        return None
    x1 = F(n) * (1 if s == "-" else -1)
    if y1 == 0 or x1 == 0 or m == 0:
        return None
    try:
        r = lambda q: sp.Rational(q.numerator, q.denominator)
        e = sp.nsimplify(to_sympy(lhs) - to_sympy(rhs), rational=True)
        if sp.expand(e - ((Y - r(y1)) - r(m) * (X - r(x1)))) != 0:
            return None
    except Exception:
        return None
    return m, x1, y1

def money(q):
    """Dollars as the stories write them: 1,925, 93.75, 12.50."""
    return f"{q.numerator:,}" if q.denominator == 1 else cents(q)

# ------------------------------------------------------------------
# The stories
# ------------------------------------------------------------------
ASK_7 = (" Let x be the number of {units} and y the price, in dollars. Write an equation in point-slope form for the "
         "price of a {event}. Will the budget be enough? Explain.")
S7 = {
    "a": dict(event="party", units="guests", cap=250, per=(10, 25), base=(50, 400), step=25,
              text="An event hall can hold up to {cap} people. The price of a party includes the room rental plus the "
                   "cost of a meal for each guest. The hall advertises ${c1} for a party of {n1} guests and ${c2} for "
                   "a party of {n2} guests. {who}'s family is planning a quinceañera for {n} guests and has budgeted "
                   "${budget}."),
    "b": dict(event="party", units="guests", cap=150, per=(15, 35), base=(50, 300), step=10,
              text="A restaurant's banquet room holds up to {cap} people. The price of a graduation party includes a "
                   "room fee plus the cost of a buffet for each guest. The restaurant charges ${c1} for {n1} guests "
                   "and ${c2} for {n2} guests. {who} is planning a graduation party for {n} guests with a budget of "
                   "${budget}."),
    "c": dict(event="party", units="bowlers", cap=40, per=(8, 20), base=(25, 120), step=2,
              text="A bowling alley hosts parties of up to {cap} people. The price of a party includes a lane fee "
                   "plus a charge for each bowler. A party of {n1} bowlers costs ${c1}, and a party of {n2} bowlers "
                   "costs ${c2}. {who} is planning a birthday party for {n} bowlers and has ${budget} to spend."),
    "d": dict(units="passengers", event="trip", cap=56, per=(15, 40), base=(100, 500), step=4,
              text="A charter bus holds up to {cap} passengers. The price of a trip includes a flat fee for the bus "
                   "plus a ticket for each passenger. A trip for {n1} passengers costs ${c1}, and a trip for {n2} "
                   "passengers costs ${c2}. {who}'s club is planning a trip for {n} passengers with a budget of "
                   "${budget}."),
}
for _s in S7.values():
    _s["ask"] = ASK_7.format(**_s)

ASK_8 = (" Let x be the number of hours and y the total cost, in dollars."
         " A. Write an equation in point-slope form that models the cost of renting a {thing} for x hours."
         " B. How can {{who}} use the equation to find the one-time service fee?")
S8 = {
    "a": dict(thing="pedal board", rate=(800, 1600)),
    "b": dict(thing="kayak", rate=(1000, 2000)),
    "c": dict(thing="paddleboard", rate=(1200, 2500)),
    "d": dict(thing="tandem bike", rate=(600, 1400)),
}
for _s in S8.values():
    _s["text"] = ("{who} rented a " + _s["thing"] + " for {h} hours and paid a total of ${T}. Renting a " +
                  _s["thing"] + " costs ${r} an hour plus a one-time service fee.")
    _s["ask"] = ASK_8.format(**_s)

ASK_9 = (" Let x be the number of weeks and y the amount {who} owes, in dollars."
         " A. What was the original amount {who} borrowed?"
         " B. How much does {who} pay each week?"
         " C. How useful are equations in point-slope form and in slope-intercept form for answering each question?")
S9 = {
    "a": dict(text="{who} borrowed money from an older brother to buy a new phone, and is paying back the same "
                   "amount each week. After {w1} weeks, {who} will owe ${A1}, and after {w2} weeks, {who} will owe "
                   "${A2}.", pay=(20, 90)),
    "b": dict(text="{who} borrowed money from a grandmother to buy a used bike, and is paying back the same amount "
                   "each week. After {w1} weeks, {who} will owe ${A1}, and after {w2} weeks, {who} will owe ${A2}.",
              pay=(10, 40)),
    "c": dict(text="{who} borrowed money from an aunt to buy a laptop, and is paying back the same amount each week. "
                   "After {w1} weeks, {who} will owe ${A1}, and after {w2} weeks, {who} will owe ${A2}.",
              pay=(25, 100)),
    "d": dict(text="{who} borrowed money from a cousin to buy concert tickets, and is paying back the same amount "
                   "each week. After {w1} weeks, {who} will owe ${A1}, and after {w2} weeks, {who} will owe ${A2}.",
              pay=(10, 30)),
}
for _s in S9.values():
    _s["ask"] = ASK_9

ASK_10 = (" Let x be the number of {units} and y the total price, in dollars."
          " A. Write equations in point-slope form and in slope-intercept form to model the situation."
          " B. What part of the equations represents the cost per {unit}?"
          " C. Which form is easier to use to find information about the set-up fee? Explain.")
S10 = {
    "a": dict(unit="invitation", units="invitations", shop="a print shop", start=(10, 25), per=(50, 300),
              intro="The total price of a printing job at {shop} includes a cost for each {unit} plus a one-time "
                    "set-up fee."),
    "b": dict(unit="T-shirt", units="T-shirts", shop="a screen-printing shop", start=(6, 12), per=(400, 1200),
              intro="The total price of an order at {shop} includes a cost for each {unit} plus a one-time "
                    "set-up fee."),
    "c": dict(unit="mug", units="mugs", shop="a gift shop", start=(5, 12), per=(300, 800),
              intro="The total price of an order of engraved mugs at {shop} includes a cost for each {unit} plus a "
                    "one-time set-up fee."),
    "d": dict(unit="poster", units="posters", shop="a copy center", start=(10, 20), per=(100, 500),
              intro="The total price of a poster job at {shop} includes a cost for each {unit} plus a one-time "
                    "set-up fee."),
}
for _s in S10.values():
    _s["intro"] = _s["intro"].format(**_s)
    _s["data"] = ("Prices: {n1} " + _s["units"] + ", ${c1}; {n2} " + _s["units"] + ", ${c2}; {n3} " + _s["units"] +
                  ", ${c3}; {n4} " + _s["units"] + ", ${c4}.")
    _s["text"] = _s["intro"] + " " + _s["data"]
    _s["ask"] = ASK_10.format(**_s)

S11 = {k: dict(text="x: 0, 1, 2, 3. y: {y0}, {y1}, {y2}, {y3}.",
               ask=" Choose the real-world context that matches the data in the table.") for k in STORIES}
CONTEXTS = [("Admission to a theme park", "major attraction within the park"),
            ("The sign-up fee at a climbing gym", "visit"),
            ("The base fare for a taxi ride", "mile"),
            ("The price of a plain pizza", "topping"),
            ("The fee to enter a county fair", "ride ticket"),
            ("The cost to join a bowling league", "game")]
TOTALS = [("meals", "meal"), ("movie tickets", "movie ticket"), ("concert tickets", "concert ticket"), ("lunches", "lunch")]
LENGTHS = [("sailboats", "sailboat", "ft"), ("train cars", "train car", "ft"), ("stacked boxes", "box", "in")]

ASK_12 = (" Let x be the number of {time}s since {since} and y {its} {level}, in {units}."
          " A. Write an equation in point-slope form to represent the {level} of {it} in terms of time. How can you "
          "use the equation to find the rate at which the {level} increases, in {units} per {time}?"
          " B. At what {level} does {it} start? Write a linear equation in a form that gives this information as part "
          "of the equation. Explain your reasoning.")
S12 = {
    "a": dict(it="the train", its="its", level="elevation", units="meters", u="m", time="second", t="s",
              rates=(2, 20), top=(30, 90), since="the train started", times=(4, 120),
              text="A railway on a hillside moves passengers at a constant rate up to an elevation of {top} m. The "
                   "train is at an elevation of {e1} m after {t1} s and {e2} m after {t2} s."),
    "b": dict(it="the elevator", its="its", level="height", units="meters", u="m", time="second", t="s",
              rates=(5, 30), top=(40, 120), since="the elevator started", times=(4, 80),
              text="A glass elevator on the outside of a tower rises at a constant rate to an observation deck "
                   "{top} m up. The elevator is {e1} m up after {t1} s and {e2} m up after {t2} s."),
    "c": dict(it="the balloon", its="its", level="height", units="feet", u="ft", time="minute", t="min",
              rates=(50, 250), top=(800, 3000), since="the balloon started rising", times=(2, 30),
              text="A hot-air balloon rises at a constant rate to a height of {top} ft. The balloon is {e1} ft up "
                   "after {t1} min and {e2} ft up after {t2} min."),
    "d": dict(it="the water", its="its", level="level", units="feet", u="ft", time="minute", t="min",
              rates=(3, 15), top=(15, 40), since="the lock started filling", times=(2, 160),
              text="The water in a canal lock rises at a constant rate to a level of {top} ft. The water is {e1} ft "
                   "deep after {t1} min and {e2} ft deep after {t2} min."),
}
for _s in S12.values():
    _s["ask"] = ASK_12.format(**_s)

STORY = {"7": S7, "8": S8, "9": S9, "10": S10, "11": S11, "12": S12}

def template(typ, story):
    st = STORY[typ][story]
    return st["text"] + st["ask"]

# ------------------------------------------------------------------
# Drawing: built backward from the answer
# ------------------------------------------------------------------
def draw_7(r, st):
    per, base = F(r.randint(*st["per"])), F(r.randrange(st["base"][0], st["base"][1] + 1, 25))
    s, cap = st["step"], st["cap"]
    ns = sorted(r.sample(range(s, cap + 1, s), 3))
    n1, n2 = sorted(r.sample([ns[0], ns[2]], 2))
    n = ns[1]
    cost = base + per * n
    over = r.random() < 0.5
    budget = F(round(int(cost) * (r.uniform(0.75, 0.95) if over else r.uniform(1.05, 1.3)) / 50) * 50)
    need(budget > 0 and abs(budget - cost) >= 25 and (budget < cost) == over)
    v = dict(who=r.choice(gen.NAMES), cap=F(cap), c1=base + per * n1, n1=F(n1), c2=base + per * n2, n2=F(n2),
             n=F(n), budget=budget)
    return v, dict(m=per, b=base)

def draw_8(r, st):
    rate = F(r.randrange(st["rate"][0], st["rate"][1] + 1, 25), 100)
    fee = F(r.randrange(500, 4001, 250), 100)
    h = F(r.randint(3, 16), 2)
    need(h.denominator == 2 or r.random() < 0.3)
    return dict(who=r.choice(gen.NAMES), h=h, T=fee + rate * h, r=rate), dict(m=rate, b=fee)

def draw_9(r, st):
    pay = F(r.randint(*st["pay"]))
    K = r.randint(6, 20)
    w1 = r.randint(1, K - 3)
    w2 = r.randint(w1 + 1, K - 1)
    B = pay * K
    return dict(who=r.choice(gen.NAMES), w1=F(w1), A1=B - pay * w1, w2=F(w2), A2=B - pay * w2), dict(m=-pay, b=B)

def draw_10(r, st):
    step = F(r.randrange(st["start"][0], st["start"][1] + 1, 5 if st["start"][1] > 12 else 1))
    per = F(r.randrange(st["per"][0], st["per"][1] + 1, 5), 100)
    fee = F(r.randrange(20, 101, 5))
    v = {}
    for i in range(4):
        v[f"n{i + 1}"] = step * (i + 1)
        v[f"c{i + 1}"] = fee + per * step * (i + 1)
    return v, dict(m=per, b=fee)

def draw_11(r, st):
    y0 = F(r.randrange(500, 10001, 5), 100)
    d = F(r.randrange(100, 3001, 5), 100)
    need(d != y0 and abs(d - y0) >= 1)
    return dict(**{f"y{i}": y0 + i * d for i in range(4)}), dict(m=d, b=y0)

def draw_12(r, st):
    lo, hi = st["rates"]
    rate = F(r.randint(lo, hi), 10) if hi <= 30 else F(r.randrange(lo, hi + 1, 10))
    start = F(r.randint(10, 80), 10) if hi <= 30 else F(r.randrange(50, 301, 10))
    halves = [F(k, 2) for k in range(*st["times"])]
    t1, t2 = sorted(r.sample(halves, 2))
    e1, e2 = start + rate * t1, start + rate * t2
    top = F(r.randint(*st["top"]))
    need(e2 < top - 1 and t2 - t1 >= 2 and (e1 * 100).denominator == 1 and (e2 * 100).denominator == 1)
    return dict(top=top, e1=e1, t1=t1, e2=e2, t2=t2), dict(m=rate, b=start)

DRAW = {"7": draw_7, "8": draw_8, "9": draw_9, "10": draw_10, "11": draw_11, "12": draw_12}
CASH = {"7": ("c1", "c2", "budget"), "8": ("T", "r"), "9": ("A1", "A2"), "10": ("c1", "c2", "c3", "c4"),
        "11": ("y0", "y1", "y2", "y3")}

def words(typ, v):
    out = {}
    for k, x in v.items():
        if isinstance(x, str):
            out[k] = x
        elif k in CASH.get(typ, ()):
            out[k] = cents(x) if typ in ("8", "11") else money(x)
        else:
            out[k] = num(x)
    return out

def draw(typ, r, tpl):
    story = STORIES[tpl]
    st = STORY[typ][story]
    v, built = DRAW[typ](r, st)
    prompt = gen.fill(template(typ, story), **words(typ, v))
    v = read(typ, story, prompt)
    f = facts(typ, story, v)                         # forward, from the words
    for k, x in built.items():
        need(f.get(k) == x)                          # the forward solve agrees with the build
    p = dict(story=story, prompt=prompt)
    if typ == "11":
        p["choices"], p["answer"] = contexts(r, f)
    else:
        p["answer"] = "; ".join(parts(typ, story, v, f))
    return p

# ------------------------------------------------------------------
# Reading the words back, and solving forward
# ------------------------------------------------------------------
def read(typ, story, prompt):
    got = gen.read(template(typ, story), prompt)
    out = {}
    for k, s in got.items():
        if k in WORDS:
            if not s.strip() or len(s.split()) > 2:
                raise ValueError("a name is one or two words")
            out[k] = s
        else:
            out[k] = number(s.replace(",", ""))
            if out[k] <= 0:
                raise ValueError("the numbers must be positive")
    return out

def facts(typ, story, v):
    """What the words say, solved forward: the line's m and b, its points, and the type's own answers."""
    if typ == "7":
        pts = [(v["n1"], v["c1"]), (v["n2"], v["c2"])]
        m, b = through(*pts)
        if m <= 0 or b < 0 or max(v["n1"], v["n2"], v["n"]) > v["cap"]:
            raise ValueError("the price goes up with each guest, and the party fits")
        cost = m * v["n"] + b
        if cost == v["budget"]:
            raise ValueError("the budget is exactly the price")
        return dict(m=m, b=b, pts=pts, cost=cost)
    if typ == "8":
        pts = [(v["h"], v["T"])]
        b = v["T"] - v["r"] * v["h"]
        if b <= 0:
            raise ValueError("the fee is more than 0")
        return dict(m=v["r"], b=b, pts=pts)
    if typ == "9":
        pts = [(v["w1"], v["A1"]), (v["w2"], v["A2"])]
        m, b = through(*pts)
        if m >= 0:
            raise ValueError("what's owed goes down")
        return dict(m=m, b=b, pts=pts)
    if typ == "10":
        pts = [(v[f"n{i}"], v[f"c{i}"]) for i in range(1, 5)]
        m, b = through(pts[0], pts[1])
        if any(m * x + b != y for x, y in pts) or m <= 0 or b <= 0:
            raise ValueError("the prices go up at a constant rate from a set-up fee")
        return dict(m=m, b=b, pts=pts)
    if typ == "11":
        ys = [v[f"y{i}"] for i in range(4)]
        diffs = {q - p for p, q in zip(ys, ys[1:])}
        if len(diffs) != 1:
            raise ValueError("the table must go up by the same amount each time")
        return dict(m=diffs.pop(), b=ys[0], y3=ys[3])
    if typ == "12":
        pts = [(v["t1"], v["e1"]), (v["t2"], v["e2"])]
        m, b = through(*pts)
        if m <= 0 or b < 0 or v["e2"] > v["top"]:
            raise ValueError("it rises, from a start at or above 0, to the top")
        return dict(m=m, b=b, pts=pts)
    raise KeyError(typ)

KINDS = {"7": "ps text", "8": "ps si text", "9": "text text text", "10": "ps si text text", "12": "ps text si text"}

def parts(typ, story, v, f):
    st = STORY[typ][story]
    who = v.get("who")
    m, b, pts = f["m"], f["b"], f.get("pts")
    if typ == "7":
        cost, budget = f["cost"], v["budget"]
        n = num(v["n"])
        yes = "Yes" if cost <= budget else "No"
        than = "less" if cost <= budget else "more"
        return [point_slope(m, *pts[0], cash=True),
                f"{yes}: when x = {n}, y = {money(cost)}, so a {st['event']} for {n} {st['units']} costs ${money(cost)}, "
                f"{than} than the ${money(budget)} budget."]
    if typ == "8":
        return [point_slope(m, *pts[0], cash=True), equation(m, b, cash=True),
                f"Write the equation in slope-intercept form (or find y when x = 0): the y-intercept, "
                f"{dollars(b)}, is the service fee, ${dollars(b)}."]
    if typ == "9":
        ps, si = point_slope(m, *pts[0], cash=True), equation(m, b, cash=True)
        return [f"${money(b)}: in slope-intercept form, {si}, the y-intercept is the amount owed at x = 0.",
                f"${money(-m)}: the slope, {dollars(m)}, is the change in what {who} owes each week.",
                f"Point-slope form, {ps}, comes straight from a reading and shows the weekly payment as its slope; "
                f"slope-intercept form, {si}, also shows the amount borrowed, as its y-intercept."]
    if typ == "10":
        return [point_slope(m, *pts[0], cash=True), equation(m, b, cash=True),
                f"The slope, {dollars(m)}, is the cost per {st['unit']}, ${cents(m)}.",
                f"Slope-intercept form: its y-intercept, {dollars(b)}, is the set-up fee, ${money(b)}. "
                f"Point-slope form doesn't show the fee."]
    if typ == "12":
        rate, start = num(m), num(b)
        return [point_slope(m, *pts[0]),
                f"The slope, {rate}, is the rate: the {st['level']} goes up {rate} {st['u']} each {st['time']}.",
                equation(m, b),
                f"{start} {st['u']}: in slope-intercept form the y-intercept is the {st['level']} at x = 0, "
                f"when {st['since']}."]
    raise KeyError(typ)

# Type 11: contexts
RIGHT = re.compile(r"(?P<start>.+) is \$(?P<a>\d+\.\d\d)\. The cost of each (?P<each>.+) is \$(?P<b>\d+\.\d\d)\.")
TOTAL = re.compile(r"The cost of 3 .+ is \$\d+\.\d\d\. The cost of each additional .+ is \$\d+\.\d\d\.")
LENGTH = re.compile(r"The (?:length|height) of 3 .+ is \d+\.\d\d (?:ft|in)\. The (?:length|height) of the first .+ "
                    r"is \d+\.\d\d (?:ft|in)\.")
STARTS = [c[0] for c in CONTEXTS]

def context(start, each, a, b):
    return f"{start} is ${cents(a)}. The cost of each {each} is ${cents(b)}."

def contexts(r, f):
    """(choices, letter): the context with the table's start and amount each, among three that aren't:
    another context with the two numbers swapped, a total of 3 with the start as each additional one,
    and a length of 3 with the start as the first's."""
    m, b, y3 = f["m"], f["b"], f["y3"]
    (s1, e1), (s2, e2) = r.sample(CONTEXTS, 2)
    totals, total = r.choice(TOTALS)
    many, one, unit = r.choice(LENGTHS)
    word = "height" if unit == "in" else "length"
    wrong = [context(s2, e2, m, b),
             f"The cost of 3 {totals} is ${cents(y3)}. The cost of each additional {total} is ${cents(b)}.",
             f"The {word} of 3 {many} is {cents(y3)} {unit}. The {word} of the first {one} is {cents(b)} {unit}."]
    return gen.lettered(r, context(s1, e1, b, m), wrong)

def true_context(f, text):
    """Does the context match the table? Read from its words: only a starting amount and an amount each can,
    with the table's numbers."""
    if TOTAL.fullmatch(text) or LENGTH.fullmatch(text):
        return False
    g = RIGHT.fullmatch(text)
    if not g or g["start"] not in STARTS:
        raise ValueError("a context reads: Admission to a theme park is $75.75. The cost of each ... is $15.25.")
    return F(g["a"]) == f["b"] and F(g["b"]) == f["m"]

# ------------------------------------------------------------------
# Checking
# ------------------------------------------------------------------
def check(p):
    try:
        typ, story = p["type"], p["story"]
        v = read(typ, story, p["prompt"])
        f = facts(typ, story, v)
        if typ == "11":
            truth = [gen.ABC[i] for i, c in enumerate(p["choices"]) if true_context(f, c)]
            return "checked" if len(truth) == 1 and truth[0] == p["answer"] else "failed"
        got = [s.strip() for s in p["answer"].split(";")]
        kinds = KINDS[typ].split()
        if typ == "9":                               # its sentences hold "; " themselves
            got = [s.strip() for s in re.split(r"; (?=\$|Point-slope)", p["answer"])]
        if len(got) != len(kinds):
            return "failed"
        want = parts(typ, story, v, f)
        for kind, g, w in zip(kinds, got, want):
            if kind == "ps":
                ps = read_point_slope(g)
                if ps is None or ps[0] != f["m"] or ps[1:] not in [tuple(q) for q in f["pts"]]:
                    return "failed"
            elif kind == "si":
                if read_equation(g) != (f["m"], f["b"]):
                    return "failed"
            elif g != w:
                return "failed"
        return "checked"
    except Exception:
        return "unchecked"

def seen_key(p):
    try:
        v = read(p["type"], p["story"], p["prompt"])
        return (p["story"],) + tuple((k, str(x)) for k, x in sorted(v.items()) if k not in WORDS)
    except (ValueError, KeyError):
        return (p.get("story"), p["prompt"])

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def split(p):
    """The answer's parts (Type 9's sentences hold "; " themselves)."""
    if p["type"] == "9":
        return [s.strip() for s in re.split(r"; (?=\$|Point-slope)", p["answer"])]
    return [s.strip() for s in p["answer"].split(";")]

def table(head, rows):
    from ..typst import esc
    cells = ", ".join(f"[{esc(c)}]" for c in head + [x for row in rows for x in row])
    return (f"#align(center, table(columns: {len(head)}, inset: 4pt, align: center, "
            f"fill: (c, r) => if r == 0 {{ luma(230) }}, {cells}))")

def typst(p):
    from ..typst import esc
    typ, story = p["type"], p["story"]
    try:
        v = read(typ, story, p["prompt"])
    except ValueError:
        v = None
    if typ == "11":
        body = esc(p["prompt"])
        if v:
            body = (table(["x", "0", "1", "2", "3"], [["y"] + [cents(v[f"y{i}"]) for i in range(4)]]) +
                    " #v(0.2em) " + esc(S11[story]["ask"].strip()))
        return math_letters(body) + " " + gen.choices_typst([esc(c) for c in p.get("choices", ())])
    if typ == "10" and v:
        st = S10[story]
        rows = [[num(v[f"n{i}"]), "$" + money(v[f"c{i}"])] for i in range(1, 5)]
        ask = PART.sub(" \\\n", esc(st["ask"].strip()))
        return math_letters(f"{esc(st['intro'])} #v(0.2em) " + table([st["units"].capitalize(), "Price"], rows) +
                            f" #v(0.2em) {ask}")
    return math_letters(PART.sub(" \\\n", esc(p["prompt"])))

LABELS = {"7": ("", ""), "8": ("A.", "B.", "B."), "9": ("A.", "B.", "C."), "10": ("A.", "A.", "B.", "C."),
          "12": ("A.", "A.", "B.", "B.")}

def answer_typst(p):
    from ..typst import esc
    from ..typmath import display, dfrac
    if p["type"] == "11":
        return " \\\n".join(f"{a}. {esc(c)}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))
    kinds, labels = KINDS[p["type"]].split(), LABELS[p["type"]]
    out = []
    for i, b in enumerate(split(p)):
        shown = display(dfrac(b)) if i < len(kinds) and kinds[i] in ("ps", "si") else math_letters(esc(b))
        out.append(f"{labels[i] if i < len(labels) else ''} {shown}".strip())
    return " \\\n".join(out)

def text(p):
    if p["type"] == "11":
        return p["prompt"] + "   " + gen.choices_text(p.get("choices", ()))
    return p["prompt"]

def answer_text(p):
    if p["type"] == "11":
        return "   ".join(f"{a}. {c}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))
    return "  |  ".join(split(p))

def height(p):
    return 0.2 * (1 + len(p["prompt"]) // 95) + (1.2 if p["type"] in ("10", "11") else 0)

# ------------------------------------------------------------------
# Editing: the story's own words, with new names or numbers
# ------------------------------------------------------------------
def from_edit(t, old):
    t = " ".join(t.split())
    typ, story = old["type"], old["story"]
    v = read(typ, story, t)
    f = facts(typ, story, v)
    new = dict(old, prompt=t, source="edited")
    if typ == "11":
        of = facts(typ, story, read(typ, story, old["prompt"]))
        swap = {cents(of["m"]): f["m"], cents(of["b"]): f["b"], cents(of["y3"]): f["y3"]}
        new["choices"] = [re.sub(r"\d+\.\d\d", lambda g: cents(swap[g[0]]) if g[0] in swap else g[0], c)
                          for c in old["choices"]]
        truth = [gen.ABC[i] for i, c in enumerate(new["choices"]) if true_context(f, c)]
        new["answer"] = truth[0] if len(truth) == 1 else old["answer"]
    else:
        new["answer"] = "; ".join(parts(typ, story, v, f))
    return new, check(new)

def with_answer(p, t, check):
    if p["type"] == "11":
        return gen.with_letters(p, t, check)
    t = " ".join(t.replace("−", "-").replace("|", ";").split())
    new = dict(p, answer=t.replace(" ;", ";"))
    return new, check(new)

def answer_of(typ, story, prompt):
    v = read(typ, story, prompt)
    return "; ".join(parts(typ, story, v, facts(typ, story, v)))
