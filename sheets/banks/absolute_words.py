"""Word problems for absolute value inequalities: an amount that must stay
within a tolerance of a target,

    |amount - target| <= tolerance

Type 1 is the phrases alone ("125, give or take 20"): write |x - 125| <= 20.
Types 2-4 are stories (a-h), and each type asks for more of the same story:
    Type 2   model the amount itself:            |d - 80| <= 10
    Type 3   write the amount as an expression:  |25t - 80| <= 10
    Type 4   model it, solve, and answer:        |25t - 80| <= 10; 2.8 <= t <= 3.6; 2.8 to 3.6 hours
Story e (phone cases) has no expression to substitute, so it has no Type 3.

An entry is "1", or a type and a story: "3a" is Type 3 about a boat. Versions
redraw the same entry, so they are parallel: same story, new numbers.

Problems are built from numbers chosen so that every solved bound is a
decimal with at most two places. check() doesn't use how they were built: it
reads the numbers back out of the prompt's words, solves the key's
inequalities with sympy, and compares their solution sets with the one the
prompt describes; Type 4's answer (which hotels, which cases, how many
guests) is found again by trying each choice.

A problem: dict(type, story, prompt, answer, source); story is "" for Type 1.
    prompt  plain text
    answer  Typst math: "abs(x - 125) <= 20"; Type 4: "model; solved; sentence"
"""
import math, random, re
from fractions import Fraction as F
import sympy as sp

NAME = FAMILY = "absolute_words"
FIXED = False
TITLE = "Lesson 1-7: Word Problems"
INSTRUCTIONS = ""                     # each type has its own (type_instructions)
COURSES = {"Algebra 1": "Lessons"}

TYPES = [
    dict(key="1", title="Phrases for a Tolerance",
         instructions="Write an absolute value inequality for each description.",
         look="A number, give or take a tolerance: \"125, plus or minus 20,\" \"within 20 of 125,\" \"no more than 20 off from 125.\"",
         move="The distance between x and the target is at most the tolerance: |x − target| ≤ tolerance. \"Less than\" leaves out the ends: <."),
    dict(key="2", title="Modeling the Amount",
         instructions="Write an absolute value inequality that models each situation.",
         look="A story with an amount that must stay within a tolerance of a target.",
         move="Find the target and the tolerance. Write |amount − target| ≤ tolerance, with the letter the problem gives for the amount."),
    dict(key="3", title="Writing the Amount as an Expression",
         instructions="Write an absolute value inequality that models each situation.",
         look="The same stories, but the letter is what makes up the amount: the hours, the guests, the gallons.",
         move="Write the amount in terms of the letter (distance = rate · time, cost = price · count, perimeter = 2ℓ + 2w). Put that expression in place of the amount in |amount − target| ≤ tolerance."),
    dict(key="4", title="Modeling and Solving",
         instructions="Write an absolute value inequality that models each situation. Solve it, then answer the question.",
         look="The same stories, with a question to answer.",
         move="Write the inequality as in Type 3. Rewrite it as −tolerance ≤ expression − target ≤ tolerance and solve all three parts. Then answer the question in words."),
]
TYPE = {t["key"]: t for t in TYPES}
KEYS = [t["key"] for t in TYPES]

NAMES = ["Enrique", "Maya", "Darnell", "Priya", "Tomás", "Grace", "Kenji", "Amara", "Luis", "Hannah",
         "Mateo", "Aaliyah", "Owen", "Sofia", "Isaiah", "Mei", "Caleb", "Fatima", "Noah", "Lucia"]
SPORTS = ["soccer", "volleyball", "basketball", "swim", "wrestling", "tennis", "lacrosse", "track"]
FUELS = ["regular", "plus", "premium"]

# ------------------------------------------------------------------
# Type 1: the phrases. n is the target, e the tolerance.
# ------------------------------------------------------------------
PHRASES = [
    ("x is {n}, give or take {e}.", "<="),
    ("x is {n}, plus or minus {e}.", "<="),
    ("x is {n}, with a tolerance of {e}.", "<="),
    ("x is {n}, with a margin of error of {e}.", "<="),
    ("x is {n}, with an allowable variation of {e}.", "<="),
    ("x is within {e} of {n}.", "<="),
    ("x is at most {e} away from {n}.", "<="),
    ("x is no more than {e} off from {n}.", "<="),
    ("The difference between x and {n} is at most {e}.", "<="),
    ("The difference between x and {n} is less than {e}.", "<"),
]

# ------------------------------------------------------------------
# Types 2-4: the stories. In text, {T} is the target and {e} the tolerance;
# money is the placeholders written with a $. amount is Type 2's letter and
# what it stands for; unknown is Types 3 and 4's. inner(v) is the amount in
# terms of the unknown as the key writes it, and total(v, u) is the same
# amount computed from the numbers (the check's). ask is Type 4's question,
# and kind says how it's answered: "range" (unit), "count" (whole numbers),
# "hotels", or "cases".
# ------------------------------------------------------------------
STORIES = [
    dict(key="a", title="Boat trip",
         text="The cruising speed of {who}'s boat is {r} mi/h. {who} plans to travel at this speed for a "
              "distance either {e} miles before or after the {T}-mile point.",
         amount=("d", "the distance, in miles, that {who} travels"),
         unknown=("t", "the number of hours {who} travels"),
         inner=lambda v: f"{num(v['r'])}t", total=lambda v, u: v["r"] * u,
         ask="For how many hours will {who} travel?", kind="range", unit="hours"),
    dict(key="b", title="Team hotel", money=("T", "e", "A", "B", "C"),
         text="Members of the {sport} team are traveling to a tournament, where they will stay in a hotel "
              "for {N} nights. The total cost for each member must be within ${e} of ${T}. The hotels' "
              "rates are the following: A. ${A}/night; B. ${B}/night; C. ${C}/night.",
         amount=("c", "the total cost, in dollars, for each member"),
         unknown=("r", "a hotel's rate, in dollars per night"),
         inner=lambda v: f"{num(v['N'])}r", total=lambda v, u: v["N"] * u,
         ask="Which hotels can the team stay in?", kind="hotels"),
    dict(key="c", title="Road trip",
         text="On a road trip, {who} plans to use the cruise control for {T} mi, plus or minus {e} mi. "
              "The cruise control is set at {r} mi/h.",
         amount=("d", "the distance, in miles, that {who} drives with the cruise control on"),
         unknown=("t", "the number of hours {who} uses the cruise control"),
         inner=lambda v: f"{num(v['r'])}t", total=lambda v, u: v["r"] * u,
         ask="For how many hours will {who} use the cruise control?", kind="range", unit="hours"),
    dict(key="d", title="Rectangle perimeter",
         text="{who} wants to model a situation where the perimeter of the rectangle below is {T} ft plus or "
              "minus {e} ft. The width of the rectangle is {w} ft.",
         amount=("P", "the perimeter of the rectangle, in feet"),
         unknown=("x", "the length of the rectangle, in feet"),
         inner=lambda v: f"2x + 2({num(v['w'])})", total=lambda v, u: 2 * u + 2 * v["w"],
         ask="What lengths can the rectangle have?", kind="range", unit="ft"),
    dict(key="e", title="Phone cases", types=("2", "4"),
         text="A company manufactures cell phone cases. The length of a certain case must be within {e} mm "
              "of {T} mm. All cases with lengths outside of this range are removed from the inventory. "
              "Four cases measure {m1} mm, {m2} mm, {m3} mm, and {m4} mm.",
         amount=("ell", "the length of a case, in millimeters"),
         unknown=("ell", "the length of a case, in millimeters"),
         inner=lambda v: "ell", total=lambda v, u: u,
         ask="Which of the four cases are removed?", kind="cases"),
    dict(key="f", title="Party budget", money=("T", "e", "r"),
         text="{who} is hosting a party at an event space. {who} plans to spend ${T}, plus or minus ${e}, "
              "at a cost of ${r} per guest.",
         amount=("c", "the total cost of the party, in dollars"),
         unknown=("g", "the number of guests"),
         inner=lambda v: f"{num(v['r'])}g", total=lambda v, u: v["r"] * u,
         ask="How many guests can {who} invite?", kind="count", unit=("guest", "guests")),
    dict(key="g", title="Gas purchase", money=("T", "e"), cents=("p1", "p2", "p3", "p4"),
         text="{who} is pumping {fuel} gas into a truck. {who} intends to put in ${T}, give or take ${e}. "
              "Gas prices per gallon are as follows. Regular: ${p1}; Plus: ${p2}; Premium: ${p3}; "
              "Diesel: ${p4}.",
         amount=("c", "the cost, in dollars, of the gas {who} pumps"),
         unknown=("g", "the number of gallons {who} pumps"),
         inner=lambda v: f"{cents(price(v))}g", total=lambda v, u: price(v) * u,
         ask="How many gallons will {who} pump?", kind="range", unit="gallons", places=3),
    dict(key="h", title="Running",
         text="{who} runs at an average speed of {r} mi/h. The length of {who}'s typical run is within "
              "{e} mi of {T} mi.",
         amount=("d", "the length, in miles, of {who}'s typical run"),
         unknown=("t", "the number of hours {who}'s typical run lasts"),
         inner=lambda v: f"{num(v['r'])}t", total=lambda v, u: v["r"] * u,
         ask="How long does {who}'s typical run last?", kind="range", unit="hours"),
]
STORY = {s["key"]: s for s in STORIES}
HOTELS = ("A", "B", "C")
CASES = ("m1", "m2", "m3", "m4")

def price(v):
    """The price per gallon of the fuel being pumped."""
    return v[f"p{FUELS.index(v['fuel']) + 1}"]

WIDTH = {"1": "half", "2": "full", "3": "full", "4": "full"}
SPACE = {"1": "0.6in", "2": "0.75in", "3": "1in", "4": "2in"}
ENTRIES = ([dict(key="1", type="1", kind="numbers", title=TYPE["1"]["title"], width=WIDTH["1"], space=SPACE["1"])]
           + [dict(key=k + s["key"], type=k, kind="numbers", title=s["title"], width=WIDTH[k], space=SPACE[k])
              for k in KEYS[1:] for s in STORIES if k in s.get("types", KEYS)])
ENTRY = {e["key"]: e for e in ENTRIES}

def label(t):
    return "Type " + t["key"]

def entry_key(text):
    t = text.strip().lower()
    return t if t in ENTRY else None

def type_of(entry):
    return ENTRY[entry]["type"]

def heading(typ):
    return f"{label(TYPE[typ])}: {TYPE[typ]['title']}"

def type_instructions(typ):
    return TYPE[typ]["instructions"]

def hint(typ):
    t = TYPE[typ]
    return label(t), t["title"], t["look"], t["move"]

def special(typ):
    return False

def initial_seen():
    return set()

def seen_key(p):
    """The numbers a prompt uses (and Type 1's phrase), so a new name alone doesn't make a new problem."""
    try:
        if p["type"] == "1":
            i, n, e = read_phrase(p["prompt"])
            return (NAME, "1", i, str(n), str(e))
        v = read_prompt(p["prompt"], p["type"], p["story"])
        return (NAME, p["type"], p["story"], tuple(str(v[k]) for k in sorted(v) if k not in ("who", "sport")))
    except ValueError:
        return (NAME, p["type"], p.get("story", ""), p["prompt"])

# ------------------------------------------------------------------
# Writing numbers
# ------------------------------------------------------------------
def places(q):
    """Decimal places q needs; None if it doesn't end."""
    for k in range(7):
        if (q * 10 ** k).denominator == 1:
            return k
    return None

def num(q):
    """F(14, 5) -> "2.8", F(3) -> "3"."""
    k = places(q)
    assert k is not None, q
    return f"{float(q):.{k}f}" if k else str(q.numerator)

def money(q):
    """Dollars: whole, or with cents: "25", "0.50", "2.75"."""
    return str(q.numerator) if q.denominator == 1 else f"{float(q):.2f}"

def cents(q):
    """Dollars and cents: "4.00", "2.75"."""
    return f"{float(q):.2f}"

def fill(text, **v):
    return re.sub(r"\{(\w+)\}", lambda m: str(v[m.group(1)]), text)

def template(typ, st):
    """A story's prompt for a type, with the letters filled in and the numbers and names still {holes}."""
    if typ == "2":
        q, what = st["amount"]
        ask = f"Let {show(q)} be {what}. Write an absolute value inequality for {show(q)}."
    elif typ == "3":
        u, what = st["unknown"]
        ask = f"Let {show(u)} be {what}. Write an absolute value inequality in terms of {show(u)}."
    else:
        u, what = st["unknown"]
        ask = f"Let {show(u)} be {what}. {st['ask']}"
    return st["text"] + " " + ask

def show(var):
    return "ℓ" if var == "ell" else var

def words(v, st):
    """The numbers in v written as the prompt writes them."""
    out = {}
    for k, x in v.items():
        out[k] = (x if isinstance(x, str) else money(x) if k in st.get("money", ()) else
                  cents(x) if k in st.get("cents", ()) else num(x))
    return out

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
class Redraw(Exception):
    pass

def need(ok):
    if not ok:
        raise Redraw

def two_places(*qs):
    need(all(places(q) is not None and places(q) <= 2 for q in qs))

def steps(lo, hi, by):
    """Fractions lo, lo + by, ..., hi."""
    lo, hi, by = F(lo), F(hi), F(by)
    return [lo + by * i for i in range(int((hi - lo) / by) + 1)]

def bounds(st, v):
    """The unknown's low and high ends, from the amount's own arithmetic."""
    b = st["total"](v, F(0))
    a = st["total"](v, F(1)) - b
    return (v["T"] - v["e"] - b) / a, (v["T"] + v["e"] - b) / a

def draw_a(r):
    v = dict(r=F(r.choice((12, 15, 18, 20, 24, 25, 30, 32, 35, 40))), T=F(r.randrange(40, 201, 5)),
             e=F(r.choice((5, 10, 15, 20, 25))))
    need(v["e"] * 3 <= v["T"])
    return v

def draw_b(r):
    v = dict(N=F(r.randint(2, 5)), T=F(r.randrange(120, 401, 5)), e=F(r.choice((10, 15, 20, 25, 30))))
    lo, hi = (v["T"] - v["e"]) / v["N"], (v["T"] + v["e"]) / v["N"]
    two_places(lo, hi)
    rates = [F(x) for x in range(30, 201, 5) if lo - 25 <= x <= hi + 25 and x not in (lo, hi)]
    picked = sorted(r.sample(rates, 3))
    inside = [lo < x < hi for x in picked]
    need(any(inside) and not all(inside))
    return dict(v, A=picked[0], B=picked[1], C=picked[2])

def draw_c(r):
    return dict(r=F(r.randrange(50, 76, 5)), T=F(r.randrange(60, 301, 5)), e=F(r.choice((10, 15, 20, 25, 30))))

def draw_d(r):
    v = dict(T=r.choice(steps(4, 20, F(1, 2))), e=r.choice(steps(F(1, 2), 2, F(1, 2))),
             w=r.choice(steps(F(1, 2), 3, F(1, 2))))
    need(v["T"] - v["e"] - 2 * v["w"] >= F(1, 2))
    return v

def draw_e(r):
    v = dict(T=F(r.randint(60, 180)), e=r.choice((F(1, 10), F(1, 5), F(1, 4), F(3, 10), F(1, 2))))
    offs = [x for x in steps(-2 * v["e"], 2 * v["e"], F(1, 20)) if abs(x) != v["e"]]
    ms = sorted(v["T"] + x for x in r.sample(offs, 4))
    kept = [abs(m - v["T"]) < v["e"] for m in ms]
    need(any(kept) and not all(kept))
    return dict(v, **dict(zip(CASES, ms)))

def draw_f(r):
    rate = F(r.choice((8, 10, 12, 15, 18, 20, 25, 30, 35, 40)))
    lo = r.randint(5, 40)
    hi = lo + 2 * r.randint(1, 5)
    v = dict(r=rate, T=rate * (lo + hi) / 2, e=rate * (hi - lo) / 2)
    need(v["T"] % 10 == 0 and v["e"] % 5 == 0 and v["T"] <= 1000 and 5 * v["e"] <= v["T"])
    return v

def draw_g(r):
    """The pumped fuel's price first, then the rest around it; gallons may have three places, as on a pump."""
    fuel, p = r.choice(FUELS), r.choice([F(x) / 100 for x in (200, 240, 250, 300, 320, 375, 400)])
    up = (r.choice((F(1, 5), F(1, 4), F(3, 10))), r.choice(steps(F(2, 5), F(3, 4), F(1, 20))))
    i = FUELS.index(fuel)
    ps = [p - sum(up[k] for k in range(j, i)) if j <= i else p + sum(up[k] for k in range(i, j)) for j in range(3)]
    v = dict(fuel=fuel, p1=ps[0], p2=ps[1], p3=ps[2], p4=ps[0] + r.choice(steps(0, 1, F(1, 20))),
             T=F(r.randrange(15, 81, 5)), e=r.choice((F(1, 4), F(1, 2), F(3, 4), F(1), F(3, 2), F(2))))
    need(ps[0] >= 2 and v["e"] * 10 <= v["T"])
    return v

def draw_h(r):
    v = dict(r=r.choice([F(x) for x in ("5", "5.5", "6", "6.25", "6.5", "7", "7.5", "8")]),
             T=r.choice(steps(3, 12, F(1, 2))), e=r.choice(steps(F(1, 2), 2, F(1, 2))))
    need(v["T"] - v["e"] >= 2)
    return v

DRAW = dict(a=draw_a, b=draw_b, c=draw_c, d=draw_d, e=draw_e, f=draw_f, g=draw_g, h=draw_h)

def draw_phrase(r, i):
    if r.random() < 0.7:
        n = F(r.choice([*range(5, 100), *range(100, 501, 5)]))
        e = F(r.randint(1, max(1, min(25, int(n) // 3))))
    else:
        n = F(r.randint(20, 400), 10)
        e = r.choice([x for x in steps(F(1, 10), 3, F(1, 10)) if 3 * x <= n])
    return fill(PHRASES[i][0], n=num(n), e=num(e)), phrase_answer(i, n, e)

def phrase_answer(i, n, e):
    return f"abs(x - {num(n)}) {PHRASES[i][1]} {num(e)}"

def draw(entry, r, seen):
    typ = type_of(entry)
    if typ == "1":
        used = {k[2] for k in seen if k[:2] == (NAME, "1")}
        i = r.choice([i for i in range(len(PHRASES)) if i not in used] or range(len(PHRASES)))
        prompt, answer = draw_phrase(r, i)
        return dict(type="1", story="", prompt=prompt, answer=answer, source="template")
    st = STORY[entry[-1]]
    v = DRAW[st["key"]](r)
    need(all(places(x) is not None and places(x) <= st.get("places", 2) for x in bounds(st, v)))
    prompt = fill(template(typ, st), who=r.choice(NAMES), sport=r.choice(SPORTS), **words(v, st))
    return dict(type=typ, story=st["key"], prompt=prompt, answer=answer_for(typ, st, v), source="template")

def answer_for(typ, st, v):
    """The key, from the numbers as the prompt states them."""
    w = words(v, st)                                 # as the prompt writes them: $0.50 is 0.50
    T, e = w["T"], w["e"]
    if typ == "2":
        return f"abs({st['amount'][0]} - {T}) <= {e}"
    model = f"abs({st['inner'](v)} - {T}) <= {e}"
    if typ == "3":
        return model
    lo, hi = bounds(st, v)
    u = st["unknown"][0]
    return f"{model}; {num(lo)} <= {u} <= {num(hi)}; {sentence(st, v)}"

def sentence(st, v):
    """Type 4's answer in words, found by trying each choice where there are choices."""
    ok = lambda u: abs(st["total"](v, u) - v["T"]) <= v["e"]
    if st["kind"] == "hotels":
        names = [h for h in HOTELS if ok(v[h])]
        if not names:
            return "none of the hotels"
        return "Hotel " + names[0] if len(names) == 1 else "Hotels " + " and ".join(names)
    if st["kind"] == "cases":
        out = [num(v[m]) + " mm" for m in CASES if not ok(v[m])]
        if not out:
            return "none of the cases"
        return f"the {out[0]} case" if len(out) == 1 else "the " + ", ".join(out[:-1]) + \
            ("," if len(out) > 2 else "") + f" and {out[-1]} cases"
    if st["kind"] == "count":
        top = math.floor((v["T"] + v["e"]) / v["r"]) + 1
        ks = [k for k in range(0, top + 1) if ok(F(k))]
        one, many = st["unit"]
        if not ks:
            return f"no number of {many} works"
        return f"exactly {ks[0]} {one if ks[0] == 1 else many}" if len(ks) == 1 else f"{ks[0]} to {ks[-1]} {many}"
    lo, hi = interval(st, v)
    return f"{num(lo)} to {num(hi)} {st['unit']}"

def interval(st, v):
    """The unknown's range, solved by sympy from the amount's formula."""
    u = sp.Symbol("u")
    tot = st["total"]({k: rat(x) for k, x in v.items()}, u)
    s = between(tot, rat(v["T"] - v["e"]), rat(v["T"] + v["e"]), u)
    return F(str(s.start)), F(str(s.end))

def between(expr, lo, hi, u):
    """The u with lo <= expr <= hi."""
    return relation(expr - lo, ">=", u) & relation(expr - hi, "<=", u)

def relation(expr, op, u):
    """The real u with expr op 0, for expr linear in u apart from bars around linear parts.
    Between the points where a bar's inside or expr is 0, whether it holds can't change,
    so it's tried at each such point and between them (sympy's solveset is far slower)."""
    def linear(e):
        if e.free_symbols - {u} or not e.is_polynomial(u) or sp.degree(e, u) > 1:
            raise ValueError("the inequality must be linear inside and outside the bars")
        a, b = sp.Poly(e, u).all_coeffs() if sp.degree(e, u) == 1 else (0, e)
        return a, b
    def root(e):
        a, b = linear(e)
        return [-b / a] if a else []
    bars = list(expr.atoms(sp.Abs))
    kinks = sorted({r for x in bars for r in root(x.args[0])})
    tests = [kinks[0] - 1] if kinks else [0]
    tests += [(x + y) / 2 for x, y in zip(kinks, kinks[1:])] + ([kinks[-1] + 1] if kinks else [])
    points = set(kinks)
    for m in tests:                                  # on each piece, drop the bars by their signs there
        piece = expr.subs({x: x.args[0] * sp.sign(x.args[0].subs(u, m)) for x in bars})
        points |= set(root(sp.expand(piece)))
    points = sorted(points)
    holds = lambda x: bool(OPS[op](expr.subs(u, x), 0))
    if not points:
        return sp.S.Reals if holds(0) else sp.S.EmptySet
    edges = [-sp.oo, *points, sp.oo]
    out = []
    for lo, hi in zip(edges, edges[1:]):
        mid = hi - 1 if lo == -sp.oo else lo + 1 if hi == sp.oo else (lo + hi) / 2
        if holds(mid):
            out.append(sp.Interval.open(lo, hi))
    out += [sp.FiniteSet(x) for x in points if holds(x)]
    return sp.Union(*out)

def rat(x):
    return sp.Rational(x.numerator, x.denominator) if isinstance(x, F) else x

def generate(entry, rng, seen, tries=400):
    for _ in range(tries):
        try:
            p = draw(entry, rng, seen)
        except Redraw:
            continue
        if seen_key(p) in seen:
            continue
        if check(p) != "checked":                    # the independent check must agree with the build
            raise AssertionError(f"absolute_words {entry}: {p}")
        seen.add(seen_key(p))
        return p
    raise RuntimeError(f"could not draw a Lesson 1-7 word problem {entry}; check its story")

# ------------------------------------------------------------------
# Checking: read the numbers back out of the prompt, then compare the
# solution sets of the key's inequalities with the one the prompt describes
# ------------------------------------------------------------------
NUM = r"(\d[\d,]*(?:\.\d+)?)"
WORD = r"[^\s.,']+(?: [^\s.,']+)?"

def pattern(text):
    """A template as a regex: names and words match, numbers are read."""
    out, groups = "", []
    for piece in re.split(r"(\{\w+\})", text):
        m = re.fullmatch(r"\{(\w+)\}", piece)
        if not m:
            out += re.escape(piece)
        elif m.group(1) in ("who", "sport"):
            out += WORD
        elif m.group(1) == "fuel":
            out += "(" + "|".join(FUELS) + ")"
            groups.append("fuel")
        else:
            out += NUM
            groups.append(m.group(1))
    return re.compile(out), groups

PATTERN = {(k, s["key"]): pattern(template(k, s)) for k in KEYS[1:] for s in STORIES}
PHRASE_PATTERN = [pattern(t) for t, _ in PHRASES]

def read_groups(rx, groups, text):
    m = rx.fullmatch(" ".join(text.split()))
    if not m:
        return None
    v = {}
    for name, g in zip(groups, m.groups()):
        x = g if name == "fuel" else F(g.replace(",", ""))
        if name in v and v[name] != x:
            raise ValueError(f"{name} is written two ways")
        v[name] = x
    return v

def read_phrase(prompt):
    """(phrase index, n, e); ValueError if the prompt isn't one of the phrases."""
    for i, (rx, groups) in enumerate(PHRASE_PATTERN):
        v = read_groups(rx, groups, prompt)
        if v is not None:
            if v["e"] <= 0:
                raise ValueError("the tolerance must be positive")
            return i, v["n"], v["e"]
    raise ValueError("use one of the phrases, like: x is 125, give or take 20.")

def read_prompt(prompt, typ, story):
    """The story's numbers as Fractions (the fuel as a word); ValueError if the prompt isn't its story's text."""
    v = read_groups(*PATTERN[(typ, story)], prompt)
    if v is None:
        raise ValueError("keep the wording of the story; change only names and numbers")
    if v["e"] <= 0 or any(x <= 0 for k, x in v.items() if not isinstance(x, str)):
        raise ValueError("the numbers must be positive")
    return v

REL = re.compile(r"\s*(<=|>=|<|>)\s*")
OPS = {"<=": sp.Le, ">=": sp.Ge, "<": sp.Lt, ">": sp.Gt}

def normal(text):
    """Unicode signs to ASCII, |u| to abs(u), ℓ to ell."""
    t = (text.replace("≤", "<=").replace("≥", ">=").replace("−", "-").replace("·", "*")
         .replace("ℓ", "ell"))
    return re.sub(r"\|([^|]+)\|", r"abs(\1)", t)

def symbol(var):
    return sp.Symbol("L_" if var == "ell" else var)

def solset(text, var):
    """The set of var that make a chain like "abs(d - 80) <= 10" or "70 <= d <= 90" true."""
    from ..check import to_sympy
    bits = REL.split(normal(text).strip())
    if len(bits) not in (3, 5):
        raise ValueError("write one or two signs")
    v = symbol(var)
    try:
        exprs = [sp.nsimplify(to_sympy(b), rational=True) for b in bits[0::2]]
    except Exception as e:
        raise ValueError(f"can't read it: {e}") from None
    if any(e.free_symbols - {v} for e in exprs) or not any(e.free_symbols for e in exprs):
        raise ValueError(f"use the letter {show(var)}")
    s = sp.S.Reals
    for i, op in enumerate(bits[1::2]):
        s = s & relation(exprs[i] - exprs[i + 1], op, v)
    return s

def same(a, b):
    return a.symmetric_difference(b) == sp.S.EmptySet

def truth(p):
    """The set the prompt describes, in the letter the key must use."""
    if p["type"] == "1":
        i, n, e = read_phrase(p["prompt"])
        lo, hi = rat(n - e), rat(n + e)
        return "x", sp.Interval.open(lo, hi) if PHRASES[i][1] == "<" else sp.Interval(lo, hi)
    st = STORY[p["story"]]
    v = read_prompt(p["prompt"], p["type"], st["key"])
    var = st["amount" if p["type"] == "2" else "unknown"][0]
    tot = st["total"]({k: rat(x) for k, x in v.items()}, symbol(var)) if p["type"] != "2" else symbol(var)
    T, e = rat(v["T"]), rat(v["e"])
    return var, between(tot, T - e, T + e, symbol(var))

def parts(p):
    bits = [b.strip() for b in p["answer"].split(";")]
    if len(bits) != (3 if p["type"] == "4" else 1):
        raise ValueError("Type 4 is model; solved; answer" if p["type"] == "4" else "write one inequality")
    return bits

def check(p):
    try:
        var, want = truth(p)
        bits = parts(p)
        model = bits[0]
        ok = "abs" in normal(model) and same(solset(model, var), want)
        if p["type"] == "4":
            st = STORY[p["story"]]
            v = read_prompt(p["prompt"], "4", st["key"])
            ok = ok and "abs" not in normal(bits[1]) and same(solset(bits[1], var), want) \
                and bits[2] == sentence(st, v)
    except (ValueError, KeyError, TypeError, AttributeError, IndexError, sp.SympifyError, SyntaxError):
        return "unchecked"
    return "checked" if ok else "failed"

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    """The prompt, with its letters in math."""
    from ..typst import esc
    t = esc(p["prompt"])
    t = re.sub(r"(?<=Let )(\S+)(?= be)|(?<=terms of )(\S+)(?=\.)|(?<=inequality for )(\S+)(?=\.)"
               r"|^x(?= is)|(?<=between )x(?= and)",
               lambda m: f"${m.group(0)}$", t)
    return t + rectangle(p) if p.get("story") == "d" else t

def rectangle(p):
    """Story d's figure: the rectangle, its length x along the bottom and its width up the side (not to scale)."""
    try:
        w = num(read_prompt(p["prompt"], p["type"], "d")["w"])
    except ValueError:
        return ""
    return ("\n    #align(center, grid(columns: 2, column-gutter: 6pt, row-gutter: 5pt, align: horizon,\n"
            "      rect(width: 1.5in, height: 0.6in, stroke: 0.8pt), [$" + w + "$ ft],\n"
            "      align(center)[$x$], []))")

def answer_typst(p):
    bits = [b.strip() for b in p["answer"].split(";")]
    out = [f"${b}$" for b in bits[:2]] + bits[2:]
    return " \\ ".join(out)

def pretty(s):
    s = s.replace("<=", "≤").replace(">=", "≥").replace("ell", "ℓ")
    out, i = "", 0
    while (j := s.find("abs(", i)) >= 0:              # abs(u) -> |u|
        depth, n = 0, j + 3
        while True:
            depth += {"(": 1, ")": -1}.get(s[n], 0)
            if depth == 0:
                break
            n += 1
        out += s[i:j] + "|" + s[j + 4:n] + "|"
        i = n + 1
    return (out + s[i:]).replace(" - ", " − ")

def text(p):
    return p["prompt"]

def answer_text(p):
    bits = [b.strip() for b in p["answer"].split(";")]
    out = "  →  ".join(pretty(b) for b in bits[:2])
    return out + (f"  ({bits[2]})" if len(bits) > 2 else "")

def height(p):
    """Inches the prompt takes on the page, for page estimates."""
    lines = 0.2 * math.ceil(len(p["prompt"]) / (45 if p["type"] == "1" else 95))
    return lines + (0.9 if p.get("story") == "d" else 0)            # the rectangle

# ------------------------------------------------------------------
# Hand editing: the prompt, in the phrase's or story's own words with new
# names or numbers
# ------------------------------------------------------------------
def edit_text(p):
    return p["prompt"]

def from_edit(text, old):
    t = " ".join(text.split())
    if old["type"] == "1":
        i, n, e = read_phrase(t)
        answer = phrase_answer(i, n, e)
    else:
        st = STORY[old["story"]]
        answer = answer_for(old["type"], st, read_prompt(t, old["type"], st["key"]))
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, text):
    t = " ".join(normal(text).split())
    if p["type"] == "4" and t.count(";") != 2:
        raise ValueError("write the model, then ;, then the solved inequality, then ;, then the answer")
    new = dict(p, answer=t)
    return new, check(new)

def selftest(n, seed):
    rng = random.Random(seed)
    for e in ENTRIES:
        seen = set()
        for i in range(n):
            if i % 50 == 0:                          # some stories' pools are small
                seen = set()
            generate(e["key"], rng, seen)
        print(f"absolute_words {e['key']:3} {e['title']:24} {n} drawn, all verified")
    return True
