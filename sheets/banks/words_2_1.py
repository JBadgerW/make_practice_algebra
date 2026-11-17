"""Lesson 2-1's word problems, Steps 11 to 18: not a bank of its own (no NAME), but
the part of slope_intercept_2_1 that writes, checks, and shows them. Each step is
one of the teacher's word problems (~/Documents/alg1/unit_2/
lesson_2-1_Slope-Intercept_Form/2-1_word_problems.txt), with the same logic in
four stories ("a" is the source's own setting) and new numbers every draw.

    Step  source  the logic                                         the key
    11    1a      a starting balance and a later one, a set number  y = -2.75 x + 45.15; what the slope and
                  of rides between (2 a day): the cost a ride        the y-intercept mean; how many rides
    12    1b      two balances, after n1 and after n2 purchases      y = -3.15 x + 26; what they mean
    13    2       a route's length and a steady rate                 y = -4 x + 25; what they mean
    14    3       two payment plans: down payment + weekly payment   each plan's equation; which pays off first
    15    4       a race's length and a steady speed                 y = -6 x + 8
    16    5       two readings of distance left; a second person     y = -7.5 x + 15; the second person's speed
                  who lives k miles closer must arrive at the same time
    17    6       a table at x = 0, 1, 2, 3: select every true        letters
                  statement about the slope and the y-intercept
    18    7       three readings of a level used at a constant rate  y = -5/8 x + 15; full is x = 0;
                                                                     whether it runs out before closing

Every story says what x and y stand for, so the key's equation is checkable;
equations are in slope-intercept form (money and decimal rates as decimals,
money with its cents: y = -1.50 x + 45.10; a rate in eighths as a fraction).
Names are drawn from gen.NAMES, and no pronoun is used: a name is repeated.

A problem: dict(type, form=None, story, prompt, answer[, choices], source).
    story   "a" to "d"
    prompt  the story's words, plain text, numbers filled in
    answer  its parts, separated by "; ": an equation (Typst math) or a sentence;
            Step 17: letters, "B, D", with choices, the statements as plain text
check() reads the numbers back out of the prompt with the story's own
template and solves forward from them (a slope from two readings, the time to
arrive from the line), and compares: each equation's value (read with to_sympy)
and form, each sentence word for word (an interpretation can only be confirmed
to fit the story's numbers), each choice by reading what it says.
"""
import re
from decimal import Decimal
from fractions import Fraction as F
from .. import gen
from ..gen import need
from ..check import to_sympy

STEPS = ("11", "12", "13", "14", "15", "16", "17", "18")
STORIES = "abcd"
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
WORDS = ("who", "who2", "day1", "day2")       # placeholders read as words, not numbers

TYPES = [
    dict(key="11", title="Word Problems: A Card's Balance",
         instructions="Answer each part. Write each equation in the form y = mx + b.",
         look="A card's balance before the first ride and again some days later, with the same cost each way, twice a day.",
         move="Count the rides between the two balances, 2 a day: Monday morning to Thursday evening is 8. The slope "
              "is the change in balance over the rides: (23.15 − 45.15)/8 = −2.75. The y-intercept is the balance "
              "before the first ride. For the rides it pays for, divide the starting balance by the cost of a ride "
              "and round down.",
         width="full", space="1.6in"),
    dict(key="12", title="Word Problems: Balance from Two Readings",
         instructions="Answer each part. Write each equation in the form y = mx + b.",
         look="A gift card's balance after two different numbers of purchases, each the same price.",
         move="The slope is the change in balance over the change in purchases: (13.40 − 19.70)/(4 − 2) = −3.15. "
              "Put a reading into y = mx + b to find b, the card's starting balance.",
         width="full", space="1.4in"),
    dict(key="13", title="Word Problems: Distance Left to Go",
         instructions="Answer each part. Write each equation in the form y = mx + b.",
         look="A route of a given length, traveled at a steady rate; y is the distance still to go.",
         move="The distance left starts at the route's length (the y-intercept) and goes down by the rate each hour "
              "(the slope is the rate, negative): y = −4x + 25.",
         width="full", space="1.2in"),
    dict(key="14", title="Word Problems: Payment Plans",
         instructions="Answer each question. Write each equation in the form y = mx + b, then explain.",
         look="A price, and two plans: a down payment and then the same payment each week.",
         move="The amount paid is y = (weekly payment)x + (down payment). Set each plan's y equal to the price and "
              "solve for x, the weeks; the plan with fewer weeks pays it off first.",
         width="full", space="1.6in"),
    dict(key="15", title="Word Problems: Distance Left in a Race",
         instructions="Write each equation in the form y = mx + b.",
         look="A race of a given length, at a steady average speed; y is the distance left.",
         move="The distance left starts at the race's length and goes down by the speed each hour: y = −6x + 8.",
         width="full", space="0.8in"),
    dict(key="16", title="Word Problems: Arriving Together",
         instructions="Answer each part. Write each equation in the form y = mx + b.",
         look="Two readings of the distance one person has left, and a second person who lives closer "
              "and must arrive at the same time.",
         move="The slope is the change in distance left over the change in time; b is the whole distance. "
              "The first person arrives when y = 0. The second person's speed is their distance over that same time.",
         width="full", space="1.8in"),
    dict(key="17", title="Word Problems: A Model from a Table",
         instructions="Select all the statements that describe a model for the data.",
         look="A table starting at x = 0, going up by the same amount each step, and statements about the slope and "
              "the y-intercept.",
         move="The y-intercept is the value at x = 0, the starting amount. The slope is the change each step, "
              "the rate. A statement is true only when both its number and its meaning fit.",
         width="full", space="0.3in"),
    dict(key="18", title="Word Problems: Constant Rate from Readings",
         instructions="Answer each part. Write each equation in the form y = mx + b.",
         look="Three readings of a level going down at a constant rate, and a question about when it runs out.",
         move="The slope is the change in level over the change in hours: (10 − 11 7/8)/(8 − 5) = −5/8. Put a "
              "reading into y = mx + b to find b, the full level (x = 0). It runs out when y = 0.",
         width="full", space="1.8in"),
]

# ------------------------------------------------------------------
# Numbers as the stories write them
# ------------------------------------------------------------------
def num(q):
    """q exactly as a decimal: 2.5, 45.15, 8; or a fraction, 5/8, if it doesn't end."""
    q = F(q)
    if q.denominator == 1:
        return str(q.numerator)
    d = q.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    if d != 1:
        return f"{q.numerator}/{q.denominator}"
    s = format((Decimal(q.numerator) / Decimal(q.denominator)).normalize(), "f")
    return s

def cents(q):
    """Money: 45.15, 28.60, 26.00."""
    return f"{Decimal(q.numerator) / Decimal(q.denominator):.2f}"

def dollars(q):
    """Money in an equation or a sentence: 26 when whole, else with cents: 28.60."""
    return str(q.numerator) if q.denominator == 1 else cents(q)

def mixed(q):
    """11 7/8, 3/4, 10."""
    if q.denominator == 1 or abs(q) < 1:
        return str(q)
    whole, part = divmod(abs(q), 1)
    return f"{'-' if q < 0 else ''}{whole} {part}"

def number(s):
    """A number read out of the words: 45.15, 840, 5/8, 11 7/8."""
    s = s.strip()
    if "." in s:
        return F(s)
    whole, _, part = s.rpartition(" ")
    if not whole:
        return F(part)
    if "/" not in part or not 0 < F(part) < 1:
        raise ValueError("a mixed number is a whole number and a fraction less than 1: 11 7/8")
    return int(whole) + F(part) if not whole.startswith("-") else int(whole) - F(part)

def plural(n, one, many):
    return f"{n} {one if n == 1 else many}"

def money(v, *ks):
    return {k: cents(v[k]) for k in ks}

# ------------------------------------------------------------------
# Equations: y = m x + b, as the key writes it, and read back strictly
# ------------------------------------------------------------------
def fraction(q):
    return str(q)

def equation(m, b, cash=False, frac=False):
    """y = -2.75 x + 45.15 (cash: cents kept, 1.50), y = -5/8 x + 15 (frac), y = 70 x, y = -x + 4."""
    show = dollars if cash else fraction if frac else num
    out = "y = " + ("-" if m < 0 else "") + ("" if abs(m) == 1 else show(abs(m)) + " ") + "x"
    if b:
        out += (" - " if b < 0 else " + ") + show(abs(b))
    return out

NUMERAL = r"\d+(?:\.\d+)?(?:/\d+)?"
EQUATION = re.compile(rf"y = (?P<m>-?(?:{NUMERAL} )?)x(?: (?P<sign>[+-]) (?P<b>{NUMERAL}))?")

def read_equation(t):
    """(m, b) of an answer written y = m x + b: a slope of ±1 written x, a fraction in lowest
    terms, no "+ 0"; the value read with to_sympy, so the text is what's checked. None if not."""
    t = " ".join(t.replace("−", "-").split())
    g = EQUATION.fullmatch(t)
    if not g:
        return None
    ms, bs = g["m"].strip(), g["b"]
    if ms in ("1", "-1") or (bs is not None and F(bs) == 0):
        return None
    for s in (ms.lstrip("-"), bs or ""):
        if "/" in s and ("." in s or str(F(s)) != s or F(s).denominator == 1):
            return None                              # 4/6, 6/3, 2.5/2: not in lowest terms
    import sympy as sp
    e = sp.nsimplify(to_sympy(t.partition("=")[2]), rational=True)
    x = sp.Symbol("x")
    if e.free_symbols != {x} or sp.degree(e, x) != 1:
        return None
    m, b = sp.Rational(e.coeff(x, 1)), sp.Rational(e.subs(x, 0))
    return F(int(m.p), int(m.q)), F(int(b.p), int(b.q))

# ------------------------------------------------------------------
# The stories. text has {placeholders} for names and numbers; the rest of a
# story's fields are its fixed words.
# ------------------------------------------------------------------
ASK_11 = (" Let x be the number of {units} and y the balance {on} the {card}, in dollars."
          " A. Write an equation for the balance {on} the {card}."
          " B. What do the slope and the y-intercept mean in this situation?"
          " C. How many {units} can {{who}} take before adding money to the {card}?")
S11 = {
    "a": dict(unit="ride", units="rides", card="fare card", on="on", lo=225, hi=350,
              text="{who} takes the subway to a summer job and back home every day. A ride costs the same in both "
                   "directions. The balance on {who}'s fare card was ${B} on {day1} morning, before the first ride, "
                   "and ${B2} on {day2} evening, after the ride home."),
    "b": dict(unit="ride", units="rides", card="bus pass", on="on", lo=125, hi=275,
              text="{who} rides the city bus to school and back home every school day, and each ride costs the same. "
                   "{who}'s bus pass had ${B} on it on {day1} morning, before the first ride, and ${B2} on {day2} "
                   "afternoon, after the ride home."),
    "c": dict(unit="crossing", units="crossings", card="ferry card", on="on", lo=250, hi=600,
              text="{who} takes the ferry across the harbor to work and back home every day. A crossing costs the "
                   "same in both directions. The balance on {who}'s ferry card was ${B} on {day1} morning, before the "
                   "first crossing, and ${B2} on {day2} evening, after the crossing home."),
    "d": dict(unit="crossing", units="crossings", card="toll account", on="in", lo=150, hi=700,
              text="{who} drives over a toll bridge to work and back home every day, and the toll is the same in both "
                   "directions. {who}'s toll account had ${B} in it on {day1} morning, before the first crossing, and "
                   "${B2} on {day2} evening, after the drive home."),
}
for _s in S11.values():
    _s["ask"] = ASK_11.format(**_s).replace(" take before", " make before" if _s["unit"] == "crossing" else " take before")

ASK_12 = (" Let x be the number of {units} and y the balance on the card, in dollars."
          " A. Write an equation for the balance on the {card}."
          " B. What do the slope and the y-intercept mean in this situation?")
S12 = {
    "a": dict(unit="coffee", units="coffees", card="gift card", lo=225, hi=550,
              text="{who} has a gift card for a coffee shop, and every coffee {who} buys costs the same. After {n1} "
                   "coffees, the balance on the card is ${B1}, and after {n2} coffees, the balance is ${B2}."),
    "b": dict(unit="smoothie", units="smoothies", card="gift card", lo=350, hi=750,
              text="{who} has a gift card for a smoothie bar, and every smoothie {who} buys costs the same. After {n1} "
                   "smoothies, the balance on the card is ${B1}, and after {n2} smoothies, the balance is ${B2}."),
    "c": dict(unit="car wash", units="car washes", card="car wash card", lo=600, hi=1500,
              text="{who} has a prepaid card for a car wash, and every wash costs the same. After {n1} car washes, the "
                   "balance on the card is ${B1}, and after {n2} car washes, the balance is ${B2}."),
    "d": dict(unit="ticket", units="tickets", card="gift card", lo=800, hi=1400,
              text="{who} has a gift card for a movie theater, and every ticket {who} buys costs the same. After {n1} "
                   "tickets, the balance on the card is ${B1}, and after {n2} tickets, the balance is ${B2}."),
}
for _s in S12.values():
    _s["ask"] = ASK_12.format(**_s)

ASK_13 = (" Let x be the number of hours {{who}} has {done} and y the distance, in miles, {{who}} still has to {verb}."
          " A. Write a linear equation for the distance {{who}} still has to {verb} after x hours."
          " B. What do the slope and the y-intercept of the equation represent?")
S13 = {
    "a": dict(verb="hike", done="hiked", does="hikes", route="trail", rates=("2", "2.5", "3", "3.5", "4"), L=(6, 25),
              text="{who} will hike a trail that is {L} miles long, at a rate of {r} mi/h."),
    "b": dict(verb="paddle", done="paddled", does="paddles", route="river route", rates=("3", "3.5", "4", "4.5", "5"),
              L=(8, 30), text="{who} will paddle a kayak down a river route that is {L} miles long, at a rate of {r} mi/h."),
    "c": dict(verb="ride", done="ridden", does="rides", route="bike path", rates=("8", "9", "10", "12", "14", "15"),
              L=(15, 60), text="{who} will ride a bike path that is {L} miles long, at a rate of {r} mi/h."),
    "d": dict(verb="walk", done="walked", does="walks", route="charity walk", rates=("2.5", "3", "3.5", "4"), L=(5, 15),
              text="{who} will walk a charity walk that is {L} miles long, at a rate of {r} mi/h."),
}
for _s in S13.values():
    _s["ask"] = ASK_13.format(**_s)

ASK_14 = (" Let x be the number of weeks and y the total amount paid, in dollars."
          " Which plan should {{who}} choose to pay off the {item} as quickly as possible? Explain.")
S14 = {
    "a": dict(item="computer", P=(600, 1200)),
    "b": dict(item="electric bike", P=(800, 1500)),
    "c": dict(item="guitar", P=(300, 900)),
    "d": dict(item="drum set", P=(500, 1100)),
}
for _s in S14.values():
    _s["text"] = ("{who} wants to buy a new " + _s["item"] + " for ${P}, and is considering two payment plans that "
                  "require weekly payments. Plan A: ${DA} down and ${WA} a week. Plan B: ${DB} down and ${WB} a week.")
    _s["ask"] = ASK_14.format(**_s)

ASK_15 = (" Let x be the number of hours since the start and y the distance, in miles, {{who}} has left to {verb}."
          " Write a linear equation for the distance {{who}} has left to {verb}.")
S15 = {
    "a": dict(verb="run", rates=("5", "5.5", "6", "6.5", "7", "7.5", "8"), L=("3.1", "5", "6", "6.2", "8", "10", "13.1"),
              text="{who} is running a road race that is {L} mi long, at an average speed of {r} mi/h."),
    "b": dict(verb="ride", rates=("14", "15", "16", "18", "20", "22"), L=("20", "25", "30", "40", "50", "62"),
              text="{who} is riding in a bike race that is {L} mi long, at an average speed of {r} mi/h."),
    "c": dict(verb="swim", rates=("1.5", "1.8", "2", "2.2", "2.5", "3"), L=("0.5", "1", "1.2", "1.5", "2", "2.4", "3", "5"),
              text="{who} is swimming an open-water race that is {L} mi long, at an average speed of {r} mi/h."),
    "d": dict(verb="walk", rates=("3.5", "4", "4.5", "5", "5.5", "6"), L=("3.1", "5", "6.2", "10", "12.4", "13.1"),
              text="{who} is in a race-walking event that is {L} mi long, walking at an average speed of {r} mi/h."),
}
for _s in S15.values():
    _s["ask"] = ASK_15.format(**_s)

ASK_16 = (" Let x be the number of hours {{who}} has {done} and y the distance, in miles, {{who}} has left."
          " A. Write a linear equation to represent {{who}}'s trip from home to the {place}."
          " B. If {{who2}} lives {{k}} miles closer to the {place} than {{who}}, what average speed must {{who2}} keep for "
          "the plan to work?")
S16 = {
    "a": dict(place="beach", done="ridden", going="riding their bicycles", rates=("6", "7.5", "8", "9", "10", "12", "12.5"),
              T=("1", "1.25", "1.5", "2", "2.5")),
    "b": dict(place="park", done="walked", going="walking", rates=("2.5", "3", "3.5", "4"),
              T=("0.5", "0.75", "1", "1.25", "1.5")),
    "c": dict(place="lake", done="jogged", going="jogging", rates=("5", "5.5", "6", "6.5", "7", "7.5", "8"),
              T=("0.5", "0.75", "1", "1.25", "1.5")),
    "d": dict(place="stadium", done="driven", going="driving", rates=("30", "35", "40", "45", "48", "50", "55", "60"),
              T=("0.5", "0.75", "1", "1.25", "1.5")),
}
for _s in S16.values():
    _s["text"] = ("{who} and {who2} are " + _s["going"] + " to the " + _s["place"] + " from their own homes. {who} "
                  "proposes that they leave home at the same time and arrive at the " + _s["place"] + " at the same "
                  "time. After {t1} h, {who} has {d1} miles left, and after {t2} h, {who} has {d2} miles left.")
    _s["ask"] = ASK_16.format(**_s)

S17 = {
    "a": dict(intro="The table shows the hourly pay rate for a restaurant employee for a given number of years of experience.",
              xs="Years", ys="Pay rate", cash=True, start=(800, 1600), step=(25, 150),
              slope="the amount of the pay raise each year", intercept="the starting hourly rate of pay",
              x="the number of years of experience", y="the hourly rate of pay"),
    "b": dict(intro="The table shows the total cost of a gym membership for a given number of months.",
              xs="Months", ys="Total cost", cash=True, start=(2000, 9900), step=(1500, 6000),
              slope="the monthly fee", intercept="the sign-up fee",
              x="the number of months", y="the total cost of the membership"),
    "c": dict(intro="The table shows the height, in centimeters, of a plant for a given number of weeks.",
              xs="Weeks", ys="Height (cm)", cash=False, start=(20, 150), step=(5, 40),
              slope="the growth in height each week", intercept="the plant's height at the start",
              x="the number of weeks", y="the height of the plant"),
    "d": dict(intro="The table shows the balance in a savings account for a given number of weeks.",
              xs="Weeks", ys="Balance", cash=True, start=(2500, 20000), step=(500, 4000),
              slope="the amount deposited each week", intercept="the starting balance",
              x="the number of weeks", y="the balance in the account"),
}
for _s in S17.values():
    d = "${y0}, ${y1}, ${y2}, ${y3}" if _s["cash"] else "{y0}, {y1}, {y2}, {y3}"
    _s["data"] = f"{_s['xs']}: 0, 1, 2, 3. {_s['ys']}: {d}."
    _s["text"] = _s["intro"] + " " + _s["data"]
    _s["ask"] = " Which statements describe a model for the data? Select all that apply."

ASK_18 = (" Assume the {stuff} is used at a constant rate. Let x be the number of hours since the {item} was filled and "
          "y the level of {stuff}, in inches."
          " A. Write a linear equation that can be used to find the level of {stuff} in the {item} after x hours."
          " B. How can you use the equation from Part A to find the level of {stuff} when the {item} is full?"
          " C. If {{who}} fills the {item} just before the {place} opens, and the {place} is open for {{H}} hours, will "
          "the {item} need to be refilled before closing time? Explain.")
S18 = {
    "a": dict(stuff="ketchup", item="ketchup dispenser", place="snack bar"),
    "b": dict(stuff="mustard", item="mustard pump", place="concession stand"),
    "c": dict(stuff="coffee", item="coffee urn", place="diner"),
    "d": dict(stuff="water", item="water cooler", place="gym"),
}
for _s in S18.values():
    _s["text"] = ("After filling the " + _s["item"] + " at the " + _s["place"] + " where {who} works, {who} measures "
                  "the level of " + _s["stuff"] + " at different times: after {h1} h, it is {L1} in; after {h2} h, "
                  "{L2} in; after {h3} h, {L3} in.")
    _s["ask"] = ASK_18.format(**_s)

STORY = {"11": S11, "12": S12, "13": S13, "14": S14, "15": S15, "16": S16, "17": S17, "18": S18}

def template(step, story):
    st = STORY[step][story]
    return st["text"] + st["ask"]

# ------------------------------------------------------------------
# Drawing: built backward from the answer
# ------------------------------------------------------------------
def steps(lo, hi, by):
    lo, hi, by = F(lo), F(hi), F(by)
    return [lo + by * i for i in range(int((hi - lo) / by) + 1)]

def names(r, n=1):
    return r.sample(gen.NAMES, n)

def draw_11(r, st):
    f = F(r.randrange(st["lo"], st["hi"] + 1, 5), 100)
    k = r.randint(10, 30)
    rem = F(r.randrange(5, int(f * 100), 5), 100)
    B = k * f + rem
    i = r.randrange(0, 4)
    j = r.randrange(i + 1, 5)
    rides = 2 * (j - i + 1)
    need(B <= 90 and rides <= k - 2)
    return dict(who=names(r)[0], B=B, B2=B - rides * f, day1=DAYS[i], day2=DAYS[j]), dict(m=-f, b=B, k=k)

def draw_12(r, st):
    p = F(r.randrange(st["lo"], st["hi"] + 1, 5), 100)
    B = F(r.choice((15, 20, 25, 30, 40, 50, 75, 100)))
    n1 = r.randint(2, 5)
    n2 = n1 + r.randint(1, 5)
    need(B - n2 * p >= 1)
    return dict(who=names(r)[0], n1=F(n1), n2=F(n2), B1=B - n1 * p, B2=B - n2 * p), dict(m=-p, b=B)

def draw_13(r, st):
    rate = F(r.choice(st["rates"]))
    L = F(r.randint(*st["L"]))
    need(L >= 2 * rate)
    return dict(who=names(r)[0], L=L, r=rate), dict(m=-rate, b=L)

def draw_14(r, st):
    P = F(r.randrange(st["P"][0], st["P"][1] + 1, 10))
    plans = []
    for _ in range(2):                               # weeks, then a weekly payment that leaves a down payment
        weeks = r.randint(6, 26)                     # of $0, or $50 to 2/5 of the price, in tens
        fits = [w for w in range(5, int(P), 5) if (P - w * weeks) % 10 == 0
                and (P - w * weeks == 0 or 50 <= P - w * weeks <= P * 2 / 5)]
        need(fits)
        week = F(r.choice(fits))
        plans.append((P - week * weeks, week, weeks))
    (DA, WA, wa), (DB, WB, wb) = plans
    need(wa != wb and (DA - DB) * (WA - WB) < 0)    # a bigger down payment, a smaller weekly one: a real choice
    return dict(who=names(r)[0], P=P, DA=DA, WA=WA, DB=DB, WB=WB), dict(weeks=(wa, wb))

def draw_15(r, st):
    rate, L = F(r.choice(st["rates"])), F(r.choice(st["L"]))
    need(L > rate / 2)
    return dict(who=names(r)[0], L=L, r=rate), dict(m=-rate, b=L)

def two_places(*qs):
    need(all((q * 100).denominator == 1 for q in qs))

def draw_16(r, st):
    rate, T = F(r.choice(st["rates"])), F(r.choice(st["T"]))
    D = rate * T
    tenths = [t for t in steps(F(1, 10), T - F(1, 10), F(1, 10))]
    need(len(tenths) >= 3)
    t1, t2 = sorted(r.sample(tenths, 2))
    need(t2 - t1 >= F(2, 10))
    k = F(r.randint(2, max(2, int(D * 3 / 5))))
    v2 = (D - k) / T
    two_places(D, D - rate * t1, D - rate * t2, v2)
    need(v2 * 10 % 1 == 0 and v2 >= rate / 2)
    who, who2 = names(r, 2)
    return (dict(who=who, who2=who2, t1=t1, d1=D - rate * t1, t2=t2, d2=D - rate * t2, k=k),
            dict(m=-rate, b=D, speed=v2))

def draw_17(r, st):
    scale = 100 if st["cash"] else 10
    s = F(r.randrange(st["start"][0], st["start"][1] + 1, 5 if st["cash"] else 1), scale)
    d = F(r.randrange(st["step"][0], st["step"][1] + 1, 5 if st["cash"] else 1), scale)
    need(s != d)
    return dict(y0=s, y1=s + d, y2=s + 2 * d, y3=s + 3 * d), dict(m=d, b=s)

def draw_18(r, st):
    rate = F(r.randint(1, 8), 8)
    full = F(r.randint(8, 20))
    gap = r.randint(2, 4)
    h1 = r.randint(1, 5)
    hs = [h1, h1 + gap, h1 + 2 * gap]
    need(full - rate * hs[2] >= 1 and any((rate * h).denominator > 1 for h in hs))
    H = r.randint(8, 24)
    empty = full / rate
    need(abs(empty - H) >= 1 and F(3, 5) * H <= empty <= F(8, 5) * H and (2 * empty).denominator == 1)
    need((empty < H) == (r.random() < 0.5))        # about half need a refill
    v = dict(who=names(r)[0], H=F(H), **{f"h{i + 1}": F(h) for i, h in enumerate(hs)},
             **{f"L{i + 1}": full - rate * h for i, h in enumerate(hs)})
    return v, dict(m=-rate, b=full, refill=empty < H)

DRAW = {"11": draw_11, "12": draw_12, "13": draw_13, "14": draw_14, "15": draw_15, "16": draw_16,
        "17": draw_17, "18": draw_18}
CASH = {"11": ("B", "B2"), "12": ("B1", "B2"), "14": ("P", "DA", "WA", "DB", "WB")}

def words(step, story, v):
    """v's values written as the story writes them."""
    cash = set(CASH.get(step, ()))
    if step == "17" and STORY["17"][story]["cash"]:
        cash |= {"y0", "y1", "y2", "y3"}
    out = {}
    for k, x in v.items():
        if isinstance(x, str):
            out[k] = x
        elif step == "14" and k in cash:
            out[k] = f"{x.numerator:,}"             # the plans are in whole dollars: $1,010
        elif k in cash:
            out[k] = cents(x)
        elif step == "18" and k.startswith("L"):
            out[k] = mixed(x)
        else:
            out[k] = num(x)
    return out

def draw(step, r, tpl):
    """tpl, 0 to 3, is the story: chosen once by gen.generator, so a story that redraws often isn't rarer."""
    story = STORIES[tpl]
    st = STORY[step][story]
    v, built = DRAW[step](r, st)
    prompt = gen.fill(template(step, story), **words(step, story, v))
    f = facts(step, story, read(step, story, prompt))   # forward, from the words
    for k, x in built.items():
        need(f.get(k) == x)                          # the forward solve agrees with the build
    p = dict(form=None, story=story, prompt=prompt)
    if step == "17":
        p["choices"], p["answer"] = statements(r, story, f)
    else:
        p["answer"] = "; ".join(parts(step, story, read(step, story, prompt), f))
    return p

# ------------------------------------------------------------------
# Reading the words back, and solving forward from them
# ------------------------------------------------------------------
def read(step, story, prompt):
    """The story's placeholders from the prompt: names and days as words, the rest as Fractions."""
    got = gen.read(template(step, story), prompt)
    out = {}
    for k, s in got.items():
        if k in WORDS:
            if not s.strip() or len(s.split()) > 2:
                raise ValueError("a name is one or two words")
            out[k] = s
        else:
            out[k] = number(s.replace(",", ""))
    if any(x <= 0 for k, x in out.items() if not isinstance(x, str) and not k.startswith("D")):
        raise ValueError("the numbers must be positive")
    return out

def through(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2:
        raise ValueError("two readings at the same time")
    m = (y2 - y1) / (x2 - x1)
    return m, y1 - m * x1

def facts(step, story, v):
    """What the words say, solved forward: the line's m and b, and each step's own answers."""
    if step == "11":
        if v["day1"] not in DAYS or v["day2"] not in DAYS or DAYS.index(v["day2"]) <= DAYS.index(v["day1"]):
            raise ValueError("the second day is a later weekday")
        rides = 2 * (DAYS.index(v["day2"]) - DAYS.index(v["day1"]) + 1)
        m, b = through((0, v["B"]), (rides, v["B2"]))
        if m >= 0:
            raise ValueError("the balance goes down")
        k = int(b // -m)
        return dict(m=m, b=b, k=k, left=b + k * m)
    if step == "12":
        if v["n1"].denominator != 1 or v["n2"].denominator != 1:
            raise ValueError("whole numbers of purchases")
        m, b = through((v["n1"], v["B1"]), (v["n2"], v["B2"]))
        if m >= 0:
            raise ValueError("the balance goes down")
        return dict(m=m, b=b)
    if step in ("13", "15"):
        return dict(m=-v["r"], b=v["L"])
    if step == "14":
        weeks = []
        for d, w in (("DA", "WA"), ("DB", "WB")):
            if v[d] < 0 or v[d] >= v["P"]:
                raise ValueError("a down payment less than the price")
            weeks.append(-(-(v["P"] - v[d]) // v[w]))       # rounded up: the last payment finishes it
        return dict(lines=((v["WA"], v["DA"]), (v["WB"], v["DB"])), weeks=tuple(int(w) for w in weeks))
    if step == "16":
        m, b = through((v["t1"], v["d1"]), (v["t2"], v["d2"]))
        if m >= 0 or v["k"] >= b:
            raise ValueError("the distance left goes down, and the second home is on the way")
        T = b / -m
        return dict(m=m, b=b, T=T, speed=(b - v["k"]) / T)
    if step == "17":
        ys = [v[f"y{i}"] for i in range(4)]
        diffs = {b - a for a, b in zip(ys, ys[1:])}
        if len(diffs) != 1:
            raise ValueError("the table must go up by the same amount each time")
        return dict(m=diffs.pop(), b=ys[0])
    if step == "18":
        pts = [(v[f"h{i}"], v[f"L{i}"]) for i in (1, 2, 3)]
        m, b = through(pts[0], pts[2])
        if m * pts[1][0] + b != pts[1][1] or m >= 0:
            raise ValueError("the three readings must go down at a constant rate")
        empty = b / -m
        return dict(m=m, b=b, empty=empty, refill=empty < v["H"], at=m * v["H"] + b)
    raise KeyError(step)

# ------------------------------------------------------------------
# The key's parts
# ------------------------------------------------------------------
def meaning(slope, of, intercept, card):
    """Step 11 and 12's interpretation."""
    return (f"The slope, -{slope}, is the cost of one {of}: the balance goes down ${slope} with each {of}. "
            f"The y-intercept, {intercept}, is the balance before the first {of}: the {card} started with ${intercept}.")

def parts(step, story, v, f):
    """The answer's parts, from the facts solved forward."""
    st = STORY[step][story]
    who = v.get("who")
    if step in ("11", "12"):
        eq = equation(f["m"], f["b"], cash=True)
        say = meaning(cents(-f["m"]), st["unit"], dollars(f["b"]), st["card"])
        if step == "12":
            return [eq, say]
        units = plural(f["k"], st["unit"], st["units"])
        return [eq, say, f"{units}: after {units}, ${cents(f['left'])} is left, less than one {st['unit']} costs."]
    if step == "13":
        rate, L = num(-f["m"]), num(f["b"])
        return [equation(f["m"], f["b"]),
                f"The slope, -{rate}, means {who} {st['does']} {rate} miles each hour: the distance left goes down "
                f"{rate} miles every hour. The y-intercept, {L}, is the length of the {st['route']}: {L} miles are "
                f"left at the start."]
    if step == "15":
        return [equation(f["m"], f["b"])]
    if step == "14":
        (wa, wb), (la, lb) = f["weeks"], f["lines"]
        best, other = ("A", "B") if wa < wb else ("B", "A")
        wk = dict(A=wa, B=wb)
        return [equation(*la), equation(*lb),
                f"Plan {best}: with Plan {best}, y reaches {v['P'].numerator} after {plural(wk[best], 'week', 'weeks')}, "
                f"and with Plan {other}, after {plural(wk[other], 'week', 'weeks')}."]
    if step == "16":
        return [equation(f["m"], f["b"]),
                f"{num(f['speed'])} mi/h: {who} arrives when y = 0, after {num(f['T'])} h, so {v['who2']} must go "
                f"{num(f['b'] - v['k'])} miles in {num(f['T'])} h."]
    if step == "18":
        b = mixed(f["b"])
        full = f"Find y when x = 0, the y-intercept: when the {st['item']} is full, the level is {b} in."
        e, H = mixed(f["empty"]), v["H"].numerator
        if f["refill"]:
            close = f"Yes: y = 0 when x = {e}, so it runs out after {e} hours, before closing at {H} hours."
        else:
            close = (f"No: when x = {H}, y = {mixed(f['at'])}, so after {H} hours the level is still above 0. "
                     f"It would run out after {e} hours.")
        return [equation(f["m"], f["b"], frac=True), full, close]
    raise KeyError(step)

# Step 17: statements about the slope and the y-intercept
STATEMENT = re.compile(r"The (slope|y-intercept) is (\$?)(\d+(?:\.\d+)?) and is (.+)\.")

def statement(st, what, value, mean):
    return f"The {what} is {'$' if st['cash'] else ''}{cents(value) if st['cash'] else num(value)} and is {st[mean]}."

def statements(r, story, f):
    """(choices, letters): one or two true statements (the slope's and the y-intercept's numbers with
    their meanings) among false ones that swap a number or a meaning; four in all."""
    st, m, b = STORY["17"][story], f["m"], f["b"]
    right = [statement(st, "slope", m, "slope"), statement(st, "y-intercept", b, "intercept")]
    wrong = [statement(st, "slope", b, "x"), statement(st, "y-intercept", m, "y"),
             statement(st, "slope", m, "intercept"), statement(st, "y-intercept", b, "slope"),
             statement(st, "slope", b, "slope")]
    n = r.choice((1, 2, 2))
    return gen.lettered(r, r.sample(right, n), r.sample(wrong, 4 - n))

def true_statement(st, f, text):
    """Is the statement true of the table? Read from its words."""
    g = STATEMENT.fullmatch(text)
    if not g or bool(g[2]) != st["cash"]:
        raise ValueError("a statement reads: The slope is $0.55 and is ...")
    what, value, mean = g[1], F(g[3]), g[4]
    return (what == "slope" and value == f["m"] and mean == st["slope"]) or \
           (what == "y-intercept" and value == f["b"] and mean == st["intercept"])

# ------------------------------------------------------------------
# Checking
# ------------------------------------------------------------------
KINDS = {"11": "eq text text", "12": "eq text", "13": "eq text", "14": "eq eq text", "15": "eq",
         "16": "eq text", "18": "eq text text"}

def check(p):
    try:
        step, story = p["type"], p["story"]
        v = read(step, story, p["prompt"])
        f = facts(step, story, v)
        if step == "17":
            st = STORY["17"][story]
            truth = [gen.ABC[i] for i, c in enumerate(p["choices"]) if true_statement(st, f, c)]
            return "checked" if truth and ", ".join(truth) == p["answer"] else "failed"
        got = [s.strip() for s in p["answer"].split(";")]
        kinds = KINDS[step].split()
        if len(got) != len(kinds):
            return "failed"
        want = parts(step, story, v, f)
        lines = f["lines"] if step == "14" else [(f["m"], f["b"])]
        for i, (kind, g, w) in enumerate(zip(kinds, got, want)):
            if kind == "eq":
                if read_equation(g) != lines[i]:
                    return "failed"
            elif g != w:
                return "failed"
        return "checked"
    except Exception:
        return "unchecked"

def answer_of(step, story, prompt):
    v = read(step, story, prompt)
    return "; ".join(parts(step, story, v, facts(step, story, v)))

def seen_key(p):
    """The story and its numbers: a new name alone isn't a new problem."""
    try:
        v = read(p["type"], p["story"], p["prompt"])
        return (p["story"],) + tuple((k, str(x)) for k, x in sorted(v.items()) if k not in ("who", "who2"))
    except (ValueError, KeyError):
        return (p.get("story"), p["prompt"])

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
LETTER = re.compile(r"(?<![\w\-\\$])([xy])(?![\w\-$])")
PART = re.compile(r"(?<=[.?]) (?=[ABC]\. )")

def math_letters(t):
    """x and y standing alone in the words, in math: "Let $x$ be"."""
    return LETTER.sub(r"$\1$", t)

def typst(p):
    from ..typst import esc
    step = p["type"]
    if step == "17":
        return table_typst(p)
    return math_letters(PART.sub(" \\\n", esc(p["prompt"])))

def table_typst(p):
    from ..typst import esc
    st = STORY["17"][p["story"]]
    try:
        v = read("17", p["story"], p["prompt"])
    except ValueError:
        body = esc(p["prompt"])
    else:
        show = (lambda q: "\\$" + cents(q)) if st["cash"] else num
        cells = ", ".join(f"[{c}]" for c in [st["xs"], "0", "1", "2", "3",
                                            esc(st["ys"])] + [show(v[f"y{i}"]) for i in range(4)])
        body = (f"{esc(st['intro'])} #v(0.2em) #align(center, table(columns: 5, inset: 4pt, align: center, {cells}))"
                f" #v(0.2em) {esc(st['ask'].strip())}")
    return math_letters(body) + " " + gen.choices_typst([esc(c) for c in p.get("choices", ())])

def answer_typst(p):
    from ..typst import esc
    from ..typmath import display, dfrac
    step = p["type"]
    if step == "17":
        return " \\\n".join(f"{a}. {esc(c)}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))
    bits = [s.strip() for s in p["answer"].split(";")]
    kinds = KINDS[step].split()
    labels = {"14": ("Plan A:", "Plan B:", "")}.get(step, ("A.", "B.", "C.") if len(bits) > 1 else ("",))
    out = []
    for i, b in enumerate(bits):
        shown = display(dfrac(b)) if i < len(kinds) and kinds[i] == "eq" else math_letters(esc(b))
        lab = labels[i] if i < len(labels) else ""
        out.append(f"{lab} {shown}".strip())
    return " \\\n".join(out)

def text(p):
    if p["type"] == "17":
        return p["prompt"] + "   " + gen.choices_text(p.get("choices", ()))
    return p["prompt"]

def answer_text(p):
    if p["type"] == "17":
        return "   ".join(f"{a}. {c}" for a, c in zip(gen.letters_of(p["answer"]), gen.chosen(p)))
    return p["answer"].replace("; ", "  |  ")

def height(p):
    lines = 0.2 * (1 + len(p["prompt"]) // 95)
    return lines + (1.4 if p["type"] == "17" else 0)

# ------------------------------------------------------------------
# Editing: the story's own words, with new names or numbers
# ------------------------------------------------------------------
def from_edit(t, old):
    t = " ".join(t.split())
    step, story = old["type"], old["story"]
    v = read(step, story, t)
    f = facts(step, story, v)
    new = dict(old, prompt=t, source="edited")
    if step == "17":
        st = STORY["17"][story]
        # the statements' numbers follow the table's: the same choices, rewritten
        old_f = facts(step, story, read(step, story, old["prompt"]))
        swap = {cents(old_f["m"]) if st["cash"] else num(old_f["m"]): f["m"],
                cents(old_f["b"]) if st["cash"] else num(old_f["b"]): f["b"]}
        def renum(c):
            g = STATEMENT.fullmatch(c)
            if not g or g[3] not in swap:
                return c
            return statement(st, g[1], swap[g[3]], next(k for k in ("slope", "intercept", "x", "y") if st[k] == g[4]))
        new["choices"] = [renum(c) for c in old["choices"]]
        new["answer"] = ", ".join(gen.ABC[i] for i, c in enumerate(new["choices"]) if true_statement(st, f, c))
    else:
        new["answer"] = "; ".join(parts(step, story, v, f))
    return new, check(new)

def with_answer(p, t, check):
    if p["type"] == "17":
        return gen.with_letters(p, t, check)
    t = " ".join(t.replace("−", "-").replace("|", ";").split())
    new = dict(p, answer="; ".join(s.strip() for s in t.split(";")))
    return new, check(new)
