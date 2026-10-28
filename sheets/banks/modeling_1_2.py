"""Lesson 1-2: Modeling. Word problems taken one modeling decision at a
time, from the teacher's Lesson 1-2 modeling bank
(~/Documents/alg1/unit_1/lesson_1-2/lesson_1-2_modeling_bank.json, 100
problems drawn from the Savvas 1-2 word problems). Each problem asks for ONE
expression or equation, never a solved value: the modeling step is the task.

The types are the bank's difficulty levels, 1 to 5; each entry is one of the
bank's categories at that level ("3b" is the Level 3 consecutive-integer
problems). Every problem of the bank is one some story here can draw, word
for word; the stories also draw new numbers, letters, names, and items.

    Level 1   direct translation: 15h, n + 1
    Level 2   two operations, or an order reversed from the words: 15h + 25, x - 8
    Level 3   one inference the words don't state: 25 - x, 0.10x, d/2, n - 1
    Level 4   a quantity built, then multiplied or grouped: 4(p - 15), 3/8 (n - 1)
    Level 5   two inferences in one statement: 8t + 2(t + 6) = 37

Stories name people; a pronoun is used only for the person the source story
used it for (Terrence, he), and any other name is repeated instead.

A problem: dict(type, story, prompt, answer, alt, source).
    story   the story that wrote it: "3b.2" (entry 3b, its third story)
    prompt  Typst markup: words with inline math, money as \\$15
    answer  Typst math in the bank's form: "4(p - 15) = 108", "6(20000)"
    alt     other forms the key also accepts, shown "(or ...)": ["120000"]
check() reads the numbers, words, and letters back out of the prompt with
the story's own template, works out the quantity from them with sympy, and
compares it with the answer and every alternate (an equation: the same
equation, up to a nonzero multiple).
"""
import re
from decimal import Decimal
from fractions import Fraction as F
from types import SimpleNamespace
import sympy as sp
from .. import gen
from ..gen import need, written
from ..check import to_sympy
from ..typmath import display, dfrac, text as plain

NAME = FAMILY = "modeling_1_2"
FIXED = False
TITLE = "Lesson 1-2: Modeling"
INSTRUCTIONS = "Write the expression or equation each problem asks for. You don't need to solve it."
COURSES = {"Algebra 1": "Lessons"}

TYPES = [
    dict(key="1", title="Direct Translation",
         look="One operation, and the words come in the same order as the symbols: cost per hour times hours, the next integer after n.",
         move="Write each phrase as its symbol, in order: 15 dollars per hour for h hours is 15h."),
    dict(key="2", title="Two Operations or a Reversed Order",
         look="Two operations in one expression, or a subtraction or division whose order is the reverse of the words: 8 less than x, a rate plus a flat fee.",
         move="Find the operations first. \"8 less than x\" starts at x: x − 8. A rate times the count, plus the fee: 15h + 25."),
    dict(key="3", title="One Inference",
         look="One quantity the words don't state: \"the rest of the 25 L,\" a percent, a time from distance and rate, \"every row but the last.\"",
         move="Name the hidden quantity before writing: the rest is 25 − x, 10% is 0.10, time is distance ÷ rate, all but the last is n − 1."),
    dict(key="4", title="Build a Quantity, Then Group It",
         look="A quantity that must be built and then multiplied or grouped: the discounted price of 4 tickets, 2 of a fish that costs 6 dollars more.",
         move="Write the one-item quantity first (p − 15), then put it in parentheses and multiply: 4(p − 15)."),
    dict(key="5", title="Two Inferences Combined",
         look="Two modeled quantities in one statement: a relationship inside a grouping, or two quantities added and set equal to a total.",
         move="Model each quantity on its own, then combine them: 8t + 2(t + 6) = 37."),
]
TYPE = {t["key"]: t for t in TYPES}
KEYS = [t["key"] for t in TYPES]

# Entries: a level and one of the bank's categories.
ENTRY_TITLES = {                          # entry: (title, the category in the bank file)
    "1a": ("Cost at a Rate", "rate-quantity"),
    "1b": ("Distance at a Rate", "distance-rate-time"),
    "1c": ("Consecutive Integers", "consecutive-integers"),
    "1d": ("Rows and Stacks", "counting-structure"),
    "1e": ("Equal Shares", "sharing"),
    "1f": ("Converting Units", "unit-conversion"),
    "1g": ("Verbal Phrases", "verbal-phrase"),
    "2a": ("Budget Equations", "budget-equation"),
    "2b": ("Consecutive Integers", "consecutive-integers"),
    "2c": ("Discounts", "discount"),
    "2d": ("Round Trips", "distance-rate-time"),
    "2e": ("Mixtures", "mixture-percent"),
    "2f": ("Percent of a Number", "percent-of-total"),
    "2g": ("Rate Plus a Fee", "rate-plus-fee"),
    "2h": ("Totals from an Average", "rate-quantity"),
    "2i": ("What's Left", "remaining-amount"),
    "2j": ("Equal Shares", "sharing"),
    "2k": ("Related Prices", "two-item-cost"),
    "2l": ("Converting Units", "unit-conversion"),
    "2m": ("Verbal Phrases", "verbal-phrase"),
    "3a": ("Budget Equations with a Fee", "budget-equation"),
    "3b": ("Consecutive Integers", "consecutive-integers"),
    "3c": ("All but the Last", "counting-structure"),
    "3d": ("Time from Distance and Rate", "distance-rate-time"),
    "3e": ("Groups", "grouping"),
    "3f": ("Mixtures", "mixture-percent"),
    "3g": ("Percent Equations", "percent-of-total"),
    "3h": ("Salary Plus Bonuses", "rate-plus-fee"),
    "3i": ("What's Left", "remaining-amount"),
    "3j": ("Averages", "sharing"),
    "3k": ("Times That Add Up", "time-sum"),
    "3l": ("Mixed Units", "unit-conversion"),
    "3m": ("Verbal Phrases", "verbal-phrase"),
    "4a": ("Earnings Equations", "budget-equation"),
    "4b": ("Mortar Layers", "counting-structure"),
    "4c": ("Discounts", "discount"),
    "4d": ("Percent of a Total", "percent-of-total"),
    "4e": ("Related Prices", "two-item-cost"),
    "4f": ("Converting Units", "unit-conversion"),
    "5a": ("Brick Walls", "counting-structure"),
    "5b": ("Groups", "grouping"),
    "5c": ("Mixture Equations", "mixture-percent"),
    "5d": ("Trip Times", "time-sum"),
    "5e": ("Two Items, One Total", "two-item-cost"),
}
SPACE = {"1": "0.5in", "2": "0.6in", "3": "0.6in", "4": "0.75in", "5": "0.9in"}
ENTRIES = [dict(key=k, type=k[0], kind="numbers", title=t, category=c, width="half", space=SPACE[k[0]])
           for k, (t, c) in ENTRY_TITLES.items()]
ENTRY = {e["key"]: e for e in ENTRIES}

def label(t):
    return "Level " + t["key"]

def entry_key(text):
    t = text.strip().lower()
    return t if t in ENTRY else None

def type_of(entry):
    return ENTRY[entry]["type"]

def heading(typ):
    return f"{label(TYPE[typ])}: {TYPE[typ]['title']}"

def hint(typ):
    t = TYPE[typ]
    return label(t), t["title"], t["look"], t["move"]

def special(typ):
    return False

def type_instructions(typ):
    return INSTRUCTIONS

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

# ------------------------------------------------------------------
# Values: how a number is written in the words and in the math
# ------------------------------------------------------------------
class Mixed(F):
    """A fraction written as a mixed number: 1 1/8."""

class Word(int):
    """A count written as a word: Four (cap) or four."""
    def __new__(cls, n, cap=False):
        w = int.__new__(cls, n)
        w.cap = cap
        return w

WORDS = "zero one two three four five six seven eight nine ten eleven twelve".split()

def words(lo, hi, cap=False):
    return tuple(Word(n, cap) for n in range(lo, hi + 1))

def decs(lo, hi, step):
    """Decimals lo to hi by step, as written (2.5, and 2 for a whole number)."""
    lo, hi, step = F(lo), F(hi), F(step)
    out, x = [], lo
    while x <= hi:
        out.append(int(x) if x.denominator == 1 else Decimal(gen.decimal(x, 4)))
        x += step
    return tuple(out)

def frac(x):
    return f"{x.numerator}/{x.denominator}"

def mixed(x):
    w, r = divmod(x, 1)
    return frac(r) if not w else str(w) if not r else f"{w} {frac(r)}"

def shown(x):
    """A value in the words: 20,000; Four; 1 1/8; 375/8; 1.202."""
    if isinstance(x, Word):
        return WORDS[x].capitalize() if x.cap else WORDS[x]
    if isinstance(x, Mixed):
        return mixed(x)
    if isinstance(x, F):
        return frac(x) if x.denominator != 1 else f"{x.numerator:,}"
    if isinstance(x, int):
        return f"{x:,}"
    return str(x)

def M(x):
    """A value in the math: 20000, 4, 1 1/8, 375/8, 1.202."""
    if isinstance(x, Mixed):
        return mixed(x)
    if isinstance(x, F):
        return frac(x) if x.denominator != 1 else str(x.numerator)
    return str(int(x)) if isinstance(x, int) else str(x)

def pct(p):
    """A percent as the decimal the bank writes: 15 -> 0.15, 10 -> 0.10."""
    return str((Decimal(p) / 100).quantize(Decimal("0.01")))

def short(q, places=3):
    """q as a decimal if it ends within places, else None: 90/60 -> "1.5"."""
    q = F(q)
    return gen.decimal(q, places) if (q * 10 ** places).denominator == 1 else None

LETTER = re.compile(r"v\d?")             # a placeholder named v, v2, ... is a letter

def parsed(name, s):
    """A placeholder's text read back as the value it was written from."""
    if LETTER.fullmatch(name):
        return s
    if name.endswith("_w"):
        return Word(WORDS.index(s.lower()), cap=s[:1].isupper())
    if re.fullmatch(r"\d{1,3}(,\d{3})+|\d+", s):
        return int(s.replace(",", ""))
    if re.fullmatch(r"\d*\.\d+", s):
        return Decimal(s)
    m = re.fullmatch(r"(\d+) (\d+)/(\d+)", s)
    if m:
        w, a, b = map(int, m.groups())
        return Mixed(w * b + a, b)
    m = re.fullmatch(r"(\d+)/(\d+)", s)
    return F(int(m.group(1)), int(m.group(2))) if m else s

def exact(x):
    """A value for the check: a sympy number (exact), a Symbol, or the words."""
    if isinstance(x, (F, int)):
        return sp.Rational(F(x).numerator, F(x).denominator)
    if isinstance(x, Decimal):
        return sp.Rational(str(x))
    return x

# ------------------------------------------------------------------
# Stories: a template, its draws, its answer, and how to work it out
# ------------------------------------------------------------------
class Story:
    """text: the prompt with {placeholders}; draws: name -> the choices
    (a tuple or range), a list of dicts (one is chosen and merged), or a
    function (r, d) of the values so far. answer(d) and alt(d) write the key
    from the values; truth(n) works the quantity out from the values read
    back out of the prompt (numbers exact, letters Symbols): an expression,
    or (left, right) for an equation."""
    def __init__(self, text, answer, truth, alt=None, need=None, **draws):
        self.text, self.answer, self.truth = text, answer, truth
        self.alt, self.need, self.draws = alt or (lambda d: []), need, draws

def fill(text, d):
    return re.sub(r"\{(\w+)\}", lambda m: shown(d[m.group(1)]), text)

def drawn(st, r):
    d = {}
    for k, how in st.draws.items():
        if callable(how):
            d[k] = how(r, SimpleNamespace(**d))
        elif isinstance(how, list) and isinstance(how[0], dict):
            d.update(r.choice(how))
        else:
            d[k] = r.choice(how)
    letters = [v for k, v in d.items() if LETTER.fullmatch(k)]
    need(len(set(letters)) == len(letters))
    need(st.need is None or st.need(SimpleNamespace(**d)))
    return d

def read_back(st, prompt):
    """The values a prompt was written from, read with its story's template."""
    return {k: parsed(k, s) for k, s in gen.read(st.text, prompt).items()}

def keyed(st, d):
    ns = SimpleNamespace(**d)
    return st.answer(ns), st.alt(ns)

def worked(st, d):
    return st.truth(SimpleNamespace(**{k: sp.Symbol(v) if LETTER.fullmatch(k) else exact(v)
                                        for k, v in d.items()}))

# People: the source story's person keeps the pronoun the source used; others are named again.
def people(name, subj, poss):
    return ([dict(name=name, ref=subj, Ref=subj.capitalize(), poss=poss)]
            + [dict(name=n, ref=n, Ref=n, poss=f"{n}'s") for n in gen.NAMES if n != name])

def named(name):
    return (name,) + tuple(n for n in gen.NAMES if n != name)

def article(n):
    """a or an before a dollar amount: an $8,000, an $11,000, a $5,000."""
    lead = f"{n:,}".split(",")[0]
    return "an" if lead.startswith("8") or lead in ("11", "18") else "a"

def an(key, cap=False):
    """A draw: the article before the value drawn as key."""
    return lambda r, d: article(getattr(d, key)).capitalize() if cap else article(getattr(d, key))

def sum_of(v, k, step=1):
    """n + (n + 1) + (n + 2), and its simplified form 3n + 3."""
    terms = [v] + [f"({v} + {step * i})" for i in range(1, k)]
    return " + ".join(terms), f"{k}{v} + {step * k * (k - 1) // 2}"

def consecutive(n, k, step=1):
    return sum(n.v + step * i for i in range(k))

LETTERS = tuple(v for v in gen.LETTERS if v != "j")   # 7j would read as a complex number
LET = LETTERS                                          # a number
HOURS = ("h", "t", "k", "x")
FISH = [dict(one="tetra", many="tetras", v="t"), dict(one="rainbow fish", many="rainbow fish", v="r"),
        dict(one="guppy", many="guppies", v="g"), dict(one="goldfish", many="goldfish", v="g"),
        dict(one="clownfish", many="clownfish", v="c"), dict(one="molly", many="mollies", v="m"),
        dict(one="snail", many="snails", v="s")]
# (cheaper, plural, letter, dearer, plural, letter)
PAIRS = [("tetra", "tetras", "t", "rainbow fish", "rainbow fish", "r"),
         ("guppy", "guppies", "g", "clownfish", "clownfish", "c"),
         ("snail", "snails", "s", "goldfish", "goldfish", "f"),
         ("molly", "mollies", "m", "betta", "bettas", "b")]
CHEAP_V = [dict(cheap=a, cheaps=b, v=c, dear=d, dears=e) for a, b, c, d, e, f in PAIRS]
DEAR_V = [dict(cheap=a, cheaps=b, dear=d, dears=e, v=f) for a, b, c, d, e, f in PAIRS]
RENTALS = [dict(rental="kayak", item="single kayak"), dict(rental="kayak", item="double kayak"),
           dict(rental="kayak", item="sea kayak"), dict(rental="canoe", item="canoe"),
           dict(rental="bike", item="tandem bike"), dict(rental="paddleboard", item="paddleboard")]
BOATS = ("single kayak", "single sea kayak", "sea kayak", "double kayak", "canoe", "paddleboard", "rowboat")
PLACES = [dict(place="bike shop", place2="shop"), dict(place="library", place2="library"),
          dict(place="park", place2="park"), dict(place="grocery store", place2="store"),
          dict(place="post office", place2="post office")]
THINGS = ("concert tickets", "a pizza order", "a cabin rental", "a gift", "a taxi ride")
TIMES = {"twice": 2, "three times": 3, "four times": 4, "five times": 5, "six times": 6}
NTH = {"second": 1, "third": 2}
NEXT = {"next integer": 1, "second integer after @": 2, "third integer after @": 3,
        "integer just before @": -1, "second integer before @": -2}
# (smaller unit, larger unit) -> how many of the smaller make one larger
PER = {("inches", "feet"): 12, ("feet", "yards"): 3, ("minutes", "hours"): 60, ("seconds", "minutes"): 60,
       ("hours", "days"): 24, ("ounces", "pounds"): 16, ("quarts", "gallons"): 4, ("days", "weeks"): 7}
UNITS = [dict(small=s, big=b) for s, b in PER]
CLOCK = [dict(small=s, big=b) for s, b in PER if s in ("minutes", "seconds", "hours")]
METRIC = {"milliliters": ("L", "1 L = 1000 mL", 1000), "grams": ("kg", "1 kg = 1000 g", 1000),
          "centimeters": ("m", "1 m = 100 cm", 100), "millimeters": ("cm", "1 cm = 10 mm", 10)}
SMALL = decs("0.001", "0.009", "0.001") + decs("0.01", "0.09", "0.01") + decs("0.1", "0.9", "0.1") + decs(1, 9, "0.5")
PCT = range(5, 100, 5)

def eq(left, right):
    return (left, right)

S = Story
STORIES = {
    # ---------------- Level 1: direct translation ----------------
    "1a": [
        S("A {item} rents for \\${rate} per hour. Write an expression for the cost, in dollars, of renting it for ${v}$ hours.",
          lambda d: f"{d.rate}{d.v}", lambda n: n.rate * n.v,
          item=BOATS, rate=range(8, 41), v=HOURS),
        S("{Items} cost \\${price} each. Write an expression for the cost of ${v}$ {items}.",
          lambda d: f"{d.price}{d.v}", lambda n: n.price * n.v,
          kind=[dict(Items="Concert tickets", items="tickets"), dict(Items="Movie tickets", items="tickets"),
                dict(Items="Museum passes", items="passes"), dict(Items="Team jerseys", items="jerseys")],
          price=range(5, 61), v=("n", "k", "m", "x")),
        S("A {one} costs ${v}$ dollars. Write an expression for the cost of {k} {many}.",
          lambda d: f"{d.k}{d.v}", lambda n: n.k * n.v,
          fish=FISH, k=range(2, 13)),
        S("A pitcher's salary is \\${s} per year. Write an expression for her total salary over {y} years.",
          lambda d: f"{d.y}({d.s})", lambda n: n.y * n.s, alt=lambda d: [str(d.y * d.s)],
          s=range(10000, 50001, 1000), y=range(2, 11)),
        S("A pitcher earns {an_b} \\${b} bonus for each game that attracts {fans} or more fans. Write an expression for her bonus pay if ${v}$ games attract that many fans.",
          lambda d: f"{d.b}{d.v}", lambda n: n.b * n.v,
          b=range(1000, 15001, 500), an_b=an("b"), fans=(100, 200, 500, 1000, 5000), v=("b", "g", "n")),
    ],
    "1b": [
        S("A {vehicle} travels at {rate} mi/h. Write an expression for the distance it travels in ${v}$ hours.",
          lambda d: f"{d.rate}{d.v}", lambda n: n.rate * n.v,
          vehicle=("bus", "train", "car", "ferry", "truck", "motorcycle"), rate=range(20, 71, 5), v=("h", "t", "x")),
        S("{name} {moves} at {rate} mi/h. Write an expression for the distance {ref} {moves} in ${v}$ hours.",
          lambda d: f"{d.rate}{d.v}", lambda n: n.rate * n.v,
          need=lambda d: d.rate in {"walks": (2, 3, 4), "jogs": (5, 6, 7), "bikes": range(8, 16)}[d.moves],
          who=people("Terrence", "he", "his"), moves=("walks", "jogs", "bikes"), rate=range(2, 16), v=("t", "h", "x")),
    ],
    "1c": [
        S("Let ${v}$ be an integer. Write an expression for the {which}.",
          lambda d: written((1, d.v), (NEXT[d.which.replace(f"${d.v}$", "@")], "")),
          lambda n: n.v + NEXT[n.which.replace(f"${n.v}$", "@")],
          v=LET, which=lambda r, d: r.choice(list(NEXT)).replace("@", f"${d.v}$")),
    ],
    "1d": [
        S("A mason lays ${v}$ rows of bricks, and each brick is {h} in. tall. Write an expression for the total height of the bricks alone.",
          lambda d: f"{d.h}{d.v}", lambda n: n.h * n.v,
          v=("n", "r", "k", "x", "m", "y", "b"), h=range(2, 10)),
        S("A stack has ${v}$ {boxes}, and each one is {h} in. tall. Write an expression for the height of the stack.",
          lambda d: f"{d.h}{d.v}", lambda n: n.h * n.v,
          v=("n", "b", "k", "x"), boxes=("boxes", "crates", "books", "trays"), h=range(2, 13)),
    ],
    "1e": [
        S("{k_w} friends share the \\${total} cost of {things} equally. Write an expression for each friend's share.",
          lambda d: f"{d.total} / {int(d.k_w)}", lambda n: n.total / n.k_w,
          k_w=words(2, 8, cap=True), total=range(20, 301), things=THINGS),
    ],
    "1f": [
        S("Each drop of {liquid} has a volume of {vol} mL. Write an expression for the volume, in milliliters, of ${v}$ drops.",
          lambda d: f"{d.vol}{d.v}", lambda n: n.vol * n.v,
          liquid=("acid", "water", "dye", "food coloring"), vol=decs("0.02", "0.1", "0.01"), v=("n", "d", "k")),
        S("Write an expression for the number of {small} in {q} {big}.",
          lambda d: f"{M(d.q)}({PER[d.small, d.big]})", lambda n: n.q * PER[n.small, n.big],
          units=UNITS, q=decs(2, 10, "0.5")),
    ],
    "1g": [
        S("Write an expression for {k} more than a number ${v}$.",
          lambda d: f"{d.v} + {d.k}", lambda n: n.v + n.k, k=range(2, 21), v=LET),
        S("Write an expression for the sum of a number ${v}$ and {k}.",
          lambda d: f"{d.v} + {d.k}", lambda n: n.v + n.k, k=range(2, 21), v=LET),
        S("Write an expression for {k} times a number ${v}$.",
          lambda d: f"{d.k}{d.v}", lambda n: n.k * n.v, k=range(2, 21), v=LET),
    ],
    # ---------------- Level 2: two operations, or a reversed order ----------------
    "2a": [
        S("{name} budgeted \\${B} for a {rental} rental. A {item} costs \\${rate} per hour. Write an equation to find the number of hours ${v}$ {ref} can rent it.",
          lambda d: f"{d.rate}{d.v} = {d.B}", lambda n: eq(n.rate * n.v, n.B), need=lambda d: d.B > 2 * d.rate,
          who=people("Joshua", "he", "his"), kind=RENTALS, B=range(30, 201, 5), rate=range(8, 41), v=("h", "t", "x")),
        S("{k_w} friends paid \\${total} in all for {k2_w} {items} that each cost ${v}$ dollars. Write an equation to find ${v}$.",
          lambda d: f"{int(d.k2_w)}{d.v} = {d.total}", lambda n: eq(n.k2_w * n.v, n.total),
          k_w=words(2, 8, cap=True), k2_w=lambda r, d: Word(d.k_w), price=range(5, 61),
          total=lambda r, d: d.k_w * d.price,
          items=("concert tickets", "movie tickets", "museum passes", "game tickets"), v=("p", "c", "x")),
    ],
    "2b": [
        S("Let ${v}$ be the {least} of {count_w} consecutive integers. Write an expression for their sum.",
          lambda d: sum_of(d.v, d.count_w)[0], lambda n: consecutive(n, int(n.count_w)),
          alt=lambda d: [sum_of(d.v, d.count_w)[1]],
          size=[dict(least="lesser", count_w=Word(2)), dict(least="least", count_w=Word(3)),
                dict(least="least", count_w=Word(4))], v=LET),
        S("Let ${v}$ be an {kind} integer. Write an expression for the {which} {kind} integer.",
          lambda d: written((1, d.v), ({"next": 2, "previous": -2}[d.which], "")),
          lambda n: n.v + {"next": 2, "previous": -2}[n.which],
          kind=("even", "odd"), which=("next", "previous"), v=LET),
    ],
    "2c": [
        S("A {item} has a regular price of ${v}$ dollars. A coupon takes \\${off} off each {unit}. Write an expression for the discounted price of one {unit}.",
          lambda d: f"{d.v} - {d.off}", lambda n: n.v - n.off,
          kind=[dict(item="concert ticket", unit="ticket"), dict(item="movie ticket", unit="ticket"),
                dict(item="shirt", unit="shirt"), dict(item="video game", unit="game"),
                dict(item="pair of shoes", unit="pair")], off=range(2, 31), v=("p", "x", "c")),
    ],
    "2d": [
        S("{name} walks from {poss} house to the {place} and back. The {place2} is ${v}$ miles from {poss} house. Write an expression for the total distance {ref} walks.",
          lambda d: f"2{d.v}", lambda n: n.v + n.v,
          who=people("LaTanya", "she", "her"), where=PLACES, v=("d", "m", "x")),
    ],
    "2e": [
        S("Write an expression for the number of liters of {what} in {L} L of a solution that is {p}% {what}.",
          lambda d: f"{pct(d.p)}({d.L})", lambda n: n.p / 100 * n.L,
          what=("acid", "alcohol"), L=range(5, 61), p=PCT),
        S("{an_L} {L}-liter mixture contains ${v}$ liters of {a} and the rest is {b}. Write an expression for the number of liters of {b}.",
          lambda d: f"{d.L} - {d.v}", lambda n: n.L - n.v,
          L=range(5, 61), mix=[dict(a="water", b="juice"), dict(a="sparkling water", b="lemonade"),
                              dict(a="water", b="antifreeze"), dict(a="milk", b="cream")], v=("x", "w", "a"), an_L=an("L", cap=True)),
        S("A technician mixes ${v}$ liters of {an_p1} {p1}% acid solution with ${v2}$ liters of {an_p2} {p2}% acid solution to get {L} L in all. Write an equation about the number of liters.",
          lambda d: f"{d.v} + {d.v2} = {d.L}", lambda n: eq(n.v + n.v2, n.L), need=lambda d: d.p1 < d.p2,
          vs=[dict(v="x", v2="y"), dict(v="a", v2="b"), dict(v="m", v2="n"), dict(v="p", v2="q")],
          p1=PCT, p2=PCT, L=range(5, 61), an_p1=an("p1"), an_p2=an("p2")),
    ],
    "2f": [
        S("Write an expression for {p}% of a number ${v}$.",
          lambda d: f"{pct(d.p)}{d.v}", lambda n: n.p / 100 * n.v, p=PCT, v=LET),
    ],
    "2g": [
        S("A {item} rents for \\${rate} per hour, plus {an_fee} \\${fee} equipment fee. Write an expression for the total cost of renting for ${v}$ hours.",
          lambda d: f"{d.rate}{d.v} + {d.fee}", lambda n: n.rate * n.v + n.fee,
          item=("single kayak", "sea kayak", "double kayak", "canoe", "paddleboard"), rate=range(8, 41),
          fee=range(5, 51), v=HOURS, an_fee=an("fee")),
        S("A {shop} charges {an_fee} \\${fee} delivery fee plus \\${rate} for each mile driven. Write an expression for the cost of a delivery of ${v}$ miles.",
          lambda d: f"{d.rate}{d.v} + {d.fee}", lambda n: n.fee + n.rate * n.v,
          shop=("shop", "florist", "bakery", "furniture store"), fee=range(5, 41), rate=range(2, 10), v=("m", "d", "x"), an_fee=an("fee")),
        S("A {club} charges \\${fee} to join plus \\${rate} each month. Write an expression for the cost of a membership that lasts ${v}$ months.",
          lambda d: f"{d.rate}{d.v} + {d.fee}", lambda n: n.fee + n.rate * n.v,
          club=("gym", "climbing gym", "swim club", "tennis club"), fee=range(10, 101, 5), rate=range(10, 61), v=("m", "t", "x")),
    ],
    "2h": [
        S("A pitcher averages ${v}$ bonus games each year for {y} years. Write an expression for her total number of bonus games.",
          lambda d: f"{d.y}{d.v}", lambda n: n.y * n.v, y=range(2, 13), v=("a", "b", "g", "n")),
        S("{name} reads an average of ${v}$ books each month for {y} months. Write an expression for the total number of books {name} reads.",
          lambda d: f"{d.y}{d.v}", lambda n: n.y * n.v, name=gen.NAMES, y=range(2, 13), v=("a", "b", "n")),
    ],
    "2i": [
        S("{name} has \\${total} and spends part of it on {k} {many} costing ${v}$ dollars each. Write an expression for the money {ref} has left.",
          lambda d: f"{d.total} - {d.k}{d.v}", lambda n: n.total - n.k * n.v,
          who=people("Anna", "she", "her"), total=range(20, 101), k=range(2, 13), fish=FISH),
        S("{name} has {T} minutes. Walking to the {place} and back takes ${v}$ minutes. Write an expression for the number of minutes {ref} can spend at the {place2}.",
          lambda d: f"{d.T} - {d.v}", lambda n: n.T - n.v,
          who=people("LaTanya", "she", "her"), T=range(30, 181, 5), where=PLACES, v=("w", "t", "m")),
        S("A scientist adds ${v}$ liters of acid to {W} L of water. Write an expression for the final volume of the solution.",
          lambda d: f"{d.W} + {d.v}", lambda n: n.W + n.v, W=decs("0.5", 3, "0.1"), v=("a", "x")),
    ],
    "2j": [
        S("A group of ${v}$ friends shares the \\${total} cost of {things} equally. Write an expression for each friend's share.",
          lambda d: f"{d.total} / {d.v}", lambda n: n.total / n.v, v=("n", "f", "k"), total=range(20, 301), things=THINGS),
    ],
    "2k": [
        S("A {cheap} costs ${v}$ dollars, and a {dear} costs \\${diff} more than a {cheap}. Write an expression for the cost of one {dear}.",
          lambda d: f"{d.v} + {d.diff}", lambda n: n.v + n.diff, fish=CHEAP_V, diff=range(1, 16)),
        S("A {dear} costs ${v}$ dollars, and a {cheap} costs \\${diff} less than a {dear}. Write an expression for the cost of one {cheap}.",
          lambda d: f"{d.v} - {d.diff}", lambda n: n.v - n.diff, fish=DEAR_V, diff=range(1, 16)),
    ],
    "2l": [
        S("Write an expression for the number of {big} in {q} {small}.",
          lambda d: f"{d.q} / {PER[d.small, d.big]}", lambda n: n.q / PER[n.small, n.big],
          alt=lambda d: [x for x in [short(F(d.q, PER[d.small, d.big]))] if x],
          need=lambda d: d.q > PER[d.small, d.big], units=UNITS, q=range(10, 241, 5)),
        S("Write an expression for the number of {small} in {q} {abbr}. ({rule})",
          lambda d: f"{d.q}({METRIC[d.small][2]})", lambda n: n.q * METRIC[n.small][2],
          metric=[dict(small=k, abbr=a, rule=t) for k, (a, t, _) in METRIC.items()], q=SMALL),
        S("Write an expression for the number of {big} in {a} {big} {b} {small}.",
          lambda d: f"{d.a} + {d.b}/{PER[d.small, d.big]}", lambda n: n.a + n.b / PER[n.small, n.big],
          alt=lambda d: [x for x in [short(d.a + F(d.b, PER[d.small, d.big]))] if x],
          need=lambda d: d.b < PER[d.small, d.big], units=UNITS, a=range(2, 10), b=range(2, 60)),
        S("A {event} takes ${v}$ {big}. Write an expression for its length in {small}.",
          lambda d: f"{PER[d.small, d.big]}{d.v}", lambda n: PER[n.small, n.big] * n.v,
          event=("trip", "movie", "flight", "bus ride", "hike", "game"), units=CLOCK, v=("t", "h", "x", "n")),
        S("A {board} is ${v}$ feet long. Write an expression for its length in inches.",
          lambda d: f"12{d.v}", lambda n: 12 * n.v,
          board=("board", "rope", "pipe", "table", "hallway", "garden"), v=("f", "x", "d", "n", "b", "s", "w")),
    ],
    "2m": [
        S("Write an expression for {k} less than a number ${v}$.",
          lambda d: f"{d.v} - {d.k}", lambda n: n.v - n.k, k=range(2, 21), v=LET),
        S("Write an expression for {times} a number ${v}$, {op} by {k}.",
          lambda d: f"{TIMES[d.times]}{d.v} {'+' if d.op == 'increased' else '-'} {d.k}",
          lambda n: TIMES[n.times] * n.v + (n.k if n.op == "increased" else -n.k),
          times=tuple(TIMES), op=("increased", "decreased"), k=range(2, 21), v=LET),
        S("Write an expression for the quotient of a number ${v}$ and {k}.",
          lambda d: f"{d.v} / {d.k}", lambda n: n.v / n.k, k=range(2, 21), v=LET),
        S("A number ${v}$ {op} by {k} is {c}. Write an equation.",
          lambda d: f"{d.v} {'-' if d.op == 'decreased' else '+'} {d.k} = {d.c}",
          lambda n: eq(n.v + (-n.k if n.op == "decreased" else n.k), n.c),
          op=("decreased", "increased"), k=range(2, 31), c=range(2, 100), v=LET),
    ],
    # ---------------- Level 3: one inference ----------------
    "3a": [
        S("{name} budgeted \\${B} for a {rental} rental. A {item} costs \\${rate} per hour plus {an_fee} \\${fee} equipment fee. Write an equation to find the number of hours ${v}$ {ref} can rent it.",
          lambda d: f"{d.rate}{d.v} + {d.fee} = {d.B}", lambda n: eq(n.fee + n.rate * n.v, n.B),
          need=lambda d: d.B > d.fee + d.rate,
          who=people("Joshua", "he", "his"), kind=RENTALS, B=range(30, 201, 5), rate=range(8, 41), fee=range(5, 51), v=("h", "t", "x"), an_fee=an("fee")),
        S("{name} has \\${B} to spend on a {club} membership. The {club} charges \\${fee} to join plus \\${rate} each month. Write an equation to find the number of months ${v}$ {name} can be a member.",
          lambda d: f"{d.rate}{d.v} + {d.fee} = {d.B}", lambda n: eq(n.fee + n.rate * n.v, n.B),
          need=lambda d: d.B > d.fee + 2 * d.rate,
          name=gen.NAMES, club=("gym", "climbing gym", "swim club", "tennis club"), B=range(100, 1001, 25),
          fee=range(10, 101, 5), rate=range(10, 61), v=("m", "t", "x")),
    ],
    "3b": [
        S("The sum of {count_w} consecutive integers is {S}. Let ${v}$ be the least of the {count_w}. Write an equation.",
          lambda d: f"{sum_of(d.v, d.count_w)[0]} = {d.S}", lambda n: eq(consecutive(n, int(n.count_w)), n.S),
          need=lambda d: (d.S - d.count_w * (d.count_w - 1) // 2) % d.count_w == 0,
          count_w=(Word(3), Word(4)), S=range(12, 301), v=LET),
        S("Let ${v}$ be the {least} of {count_w} consecutive {kind} integers. Write an expression for their sum.",
          lambda d: sum_of(d.v, d.count_w, 2)[0], lambda n: consecutive(n, int(n.count_w), 2),
          alt=lambda d: [sum_of(d.v, d.count_w, 2)[1]],
          size=[dict(least="lesser", count_w=Word(2)), dict(least="least", count_w=Word(3))],
          kind=("odd", "even"), v=LET),
        S("Let ${v}$ be the middle one of three consecutive integers whose sum is {S}. Write an equation.",
          lambda d: f"({d.v} - 1) + {d.v} + ({d.v} + 1) = {d.S}", lambda n: eq(3 * n.v, n.S),
          need=lambda d: d.S % 3 == 0, S=range(12, 301), v=LET),
        S("Let ${v}$ be the least of three consecutive integers. Write an expression for {times} the {nth} integer.",
          lambda d: f"{TIMES[d.times]}({d.v} + {NTH[d.nth]})", lambda n: TIMES[n.times] * (n.v + NTH[n.nth]),
          times=("twice", "three times", "four times", "five times"), nth=tuple(NTH), v=LET),
    ],
    "3c": [
        S("A mason lays ${v}$ rows of {bricks} and spreads mortar on top of every row but the last. Write an expression for the number of mortar layers.",
          lambda d: f"{d.v} - 1", lambda n: n.v - 1, v=LETTERS, bricks=("bricks", "blocks", "stones")),
        S("A {thing} has ${v}$ {posts} in a line, with one {rail} between each pair of neighboring {posts}. Write an expression for the number of {rails}.",
          lambda d: f"{d.v} - 1", lambda n: n.v - 1, v=LETTERS,
          kind=[dict(thing="fence", posts="posts", rail="rail", rails="rails"),
                dict(thing="fence", posts="posts", rail="board", rails="boards"),
                dict(thing="walkway", posts="lampposts", rail="banner", rails="banners")]),
        S("{name} cuts a {board} into ${v}$ pieces. Write an expression for the number of cuts {name} makes.",
          lambda d: f"{d.v} - 1", lambda n: n.v - 1, name=gen.NAMES, board=("board", "rope", "ribbon", "log"),
          v=("n", "p", "k", "x")),
    ],
    "3d": [
        S("{name} walks the {dist} mi to the {place} at a pace of ${v}$ mi/h. Write an expression for the time, in hours, the walk takes.",
          lambda d: f"{d.dist} / {d.v}", lambda n: n.dist / n.v,
          name=named("LaTanya"), dist=decs("0.5", 4, "0.1"), place=("bike shop", "library", "park", "store"),
          v=("r", "s", "x")),
        S("{name} walks to the {place} at {rate} mi/h. The {place} is ${v}$ miles away. Write an expression for the time, in hours, the walk takes.",
          lambda d: f"{d.v} / {d.rate}", lambda n: n.v / n.rate,
          name=named("Terrence"), place=("theater", "library", "park", "museum", "stadium"), rate=(2, 3, 4),
          v=("d", "m", "x")),
        S("{name} rides the {vehicle} the ${v}$ miles home from the {place} at {rate} mi/h. Write an expression for the time, in hours, the ride takes.",
          lambda d: f"{d.v} / {d.rate}", lambda n: n.v / n.rate,
          name=named("Terrence"), vehicle=("bus", "train", "ferry"), place=("theater", "museum", "stadium", "mall"),
          rate=range(15, 61, 5), v=("d", "m", "x")),
        S("{name} walks {dist} mi to the {place} and {dist} mi home, both at {rate} mi/h. Write an expression for {poss} total walking time, in hours.",
          lambda d: f"({d.dist} + {d.dist}) / {d.rate}", lambda n: 2 * n.dist / n.rate,
          who=people("LaTanya", "she", "her"), dist=decs("0.5", 4, "0.1"),
          place=("bike shop", "library", "park", "store"), rate=(2, 3, 4)),
    ],
    "3e": [
        S("{k_w} people each rent a {item} at \\${rate} per hour for ${v}$ hours. Write an expression for their total cost.",
          lambda d: f"{int(d.k_w)}({d.rate}{d.v})", lambda n: n.k_w * n.rate * n.v,
          k_w=words(2, 6, cap=True), item=("single kayak", "canoe", "paddleboard", "tandem bike"),
          rate=range(8, 41), v=HOURS),
    ],
    "3f": [
        S("A technician pours ${v}$ liters of a solution that is {p}% acid. Write an expression for the number of liters of acid in it.",
          lambda d: f"{pct(d.p)}{d.v}", lambda n: n.p / 100 * n.v, p=PCT, v=("x", "y", "a", "b")),
        S("A technician needs {L} L of solution in all. She uses ${v}$ liters of the {p1}% solution and the rest is the {p2}% solution. Write an expression for the number of liters of the {p2}% solution.",
          lambda d: f"{d.L} - {d.v}", lambda n: n.L - n.v, need=lambda d: d.p1 != d.p2,
          L=range(5, 61), v=("x", "a", "y"), p1=PCT, p2=PCT),
    ],
    "3g": [
        S("Let ${v}$ be a percent written as a decimal. Write an equation stating that ${v}$ of {whole} is {part}.",
          lambda d: f"{d.whole}{d.v} = {d.part}", lambda n: eq(n.v * n.whole, n.part), need=lambda d: d.part < d.whole,
          v=("p", "r", "x"), whole=range(10, 201), part=range(1, 200)),
    ],
    "3h": [
        S("A pitcher earns \\${s} per year for {y} years, plus \\${b} for each of ${v}$ bonus games. Write an expression for her total earnings.",
          lambda d: f"{d.y}({d.s}) + {d.b}{d.v}", lambda n: n.s * n.y + n.b * n.v,
          s=range(10000, 50001, 1000), y=range(2, 11), b=range(1000, 15001, 500), v=("b", "g", "n")),
        S("A salesperson earns \\${s} per month for {y} months, plus \\${b} for each of ${v}$ cars sold. Write an expression for the total earnings.",
          lambda d: f"{d.y}({d.s}) + {d.b}{d.v}", lambda n: n.s * n.y + n.b * n.v,
          s=range(1000, 4001, 100), y=range(2, 13), b=range(100, 1001, 50), v=("c", "n", "x")),
    ],
    "3i": [
        S("{name} budgeted \\${B} for a {rental} rental that costs \\${rate} per hour. Write an expression for the money {ref} has left after renting for ${v}$ hours.",
          lambda d: f"{d.B} - {d.rate}{d.v}", lambda n: n.B - n.rate * n.v, need=lambda d: d.B > d.rate,
          who=people("Joshua", "he", "his"), rental=("kayak", "canoe", "bike", "paddleboard"), B=range(30, 201, 5),
          rate=range(8, 41), v=("h", "t", "x")),
        S("A scientist adds ${v}$ liters of acid to {W} L of water, and the final volume is {T} L. Write an equation to find ${v}$.",
          lambda d: f"{d.W} + {d.v} = {d.T}", lambda n: eq(n.W + n.v, n.T),
          W=decs("0.5", 3, "0.1"), a=decs("0.001", "0.05", "0.001"), T=lambda r, d: d.W + d.a, v=("a", "x")),
    ],
    "3j": [
        S("A pitcher is paid for ${v}$ bonus games over {y} years. Write an expression for the average number of bonus games per year.",
          lambda d: f"{d.v} / {d.y}", lambda n: n.v / n.y, y=range(2, 13), v=("b", "g", "n")),
        S("{name} reads ${v}$ pages over {y} days. Write an expression for the average number of pages per day.",
          lambda d: f"{d.v} / {d.y}", lambda n: n.v / n.y, name=gen.NAMES, y=range(2, 15), v=("p", "n", "x")),
    ],
    "3k": [
        S("{name} has {T} h before {ref} must be home. {Ref} spends ${v}$ hours walking and ${v2}$ hours at the {place}. Write an equation that uses all of {poss} time.",
          lambda d: f"{d.v} + {d.v2} = {d.T}", lambda n: eq(n.v + n.v2, n.T),
          who=people("LaTanya", "she", "her"), T=decs(1, 4, "0.25"),
          vs=[dict(v="w", v2="s"), dict(v="a", v2="b"), dict(v="x", v2="y"), dict(v="w", v2="t")],
          place=("shop", "library", "park", "store")),
        S("{name}'s whole trip takes {T} h: ${v}$ hours walking, {M} h at the movie, and ${v2}$ hours on the bus. Write an equation.",
          lambda d: f"{d.v} + {d.M} + {d.v2} = {d.T}", lambda n: eq(n.v + n.M + n.v2, n.T), need=lambda d: d.M <= d.T - 1,
          name=named("Terrence"), T=decs(2, 6, "0.25"), M=decs("1.5", 3, "0.25"),
          vs=[dict(v="w", v2="b"), dict(v="a", v2="b"), dict(v="x", v2="y")]),
    ],
    "3l": [
        S("A {thing} is ${a}$ inches {cmp} than {f} feet {dim}. Write an expression for its {noun} in inches.",
          lambda d: f"{d.f}(12) {'-' if d.cmp == 'less' else '+'} {mixed(d.a)}",
          lambda n: 12 * n.f + (-n.a if n.cmp == "less" else n.a),
          alt=lambda d: [f"{12 * d.f} {'-' if d.cmp == 'less' else '+'} {frac(F(d.a))}",
                         frac(12 * d.f + (-F(d.a) if d.cmp == "less" else F(d.a)))],
          kind=[dict(thing="wall", dim="high", noun="height"), dict(thing="shelf", dim="long", noun="length"),
                dict(thing="door", dim="tall", noun="height"), dict(thing="table", dim="wide", noun="width")],
          a=tuple(Mixed(k, 8) for k in range(9, 48) if k % 8), cmp=("less", "more"), f=range(2, 8)),
    ],
    "3m": [
        S("Write an expression for {k} {cmp} than {part} of a number ${v}$.",
          lambda d: f"{d.v}/{PART[d.part]} {'-' if d.cmp == 'less' else '+'} {d.k}",
          lambda n: n.v / PART[n.part] + (-n.k if n.cmp == "less" else n.k),
          k=range(2, 21), cmp=("less", "more"), part=("half", "one third", "one fourth"), v=LET),
        S("Write an expression for the product of {k} and the {op} of a number ${v}$ and {c}.",
          lambda d: f"{d.k}({d.v} {'+' if d.op == 'sum' else '-'} {d.c})",
          lambda n: n.k * (n.v + (n.c if n.op == "sum" else -n.c)),
          k=range(2, 13), op=("sum", "difference"), c=range(1, 21), v=LET),
        S("The sum of a number ${v}$ and {c} is {k} times the number. Write an equation.",
          lambda d: f"{d.v} + {d.c} = {d.k}{d.v}", lambda n: eq(n.v + n.c, n.k * n.v),
          c=range(2, 21), k=range(2, 10), v=LET),
        S("{c_w} less than {k} times a number ${v}$ is {t}. Write an equation.",
          lambda d: f"{d.k}{d.v} - {int(d.c_w)} = {d.t}", lambda n: eq(n.k * n.v - n.c_w, n.t),
          c_w=words(2, 12, cap=True), k=range(2, 10), t=range(2, 100), v=LET),
        S("Write an expression for {part} of the {op} of a number ${v}$ and {c}.",
          lambda d: f"({d.v} {'+' if d.op == 'sum' else '-'} {d.c}) / {PART[d.part]}",
          lambda n: (n.v + (n.c if n.op == "sum" else -n.c)) / PART[n.part],
          part=("half", "one third", "one fourth"), op=("sum", "difference"), c=range(2, 21), v=LET),
    ],
    # ---------------- Level 4: build a quantity, then group it ----------------
    "4a": [
        S("A pitcher earns \\${s} per year for {y} years plus \\${b} for each of ${v}$ bonus games. Write an equation for the case in which she earns \\${T} in all.",
          lambda d: f"{d.y}({d.s}) + {d.b}{d.v} = {d.T}", lambda n: eq(n.s * n.y + n.b * n.v, n.T),
          need=lambda d: d.T > d.y * d.s,
          s=range(10000, 50001, 1000), y=range(2, 11), b=range(1000, 15001, 500),
          T=range(100000, 2000001, 50000), v=("b", "g", "n")),
        S("A salesperson earns \\${s} per month for {y} months plus \\${b} for each of ${v}$ cars sold. Write an equation for the case in which the salesperson earns \\${T} in all.",
          lambda d: f"{d.y}({d.s}) + {d.b}{d.v} = {d.T}", lambda n: eq(n.s * n.y + n.b * n.v, n.T),
          need=lambda d: d.T > d.y * d.s,
          s=range(1000, 4001, 100), y=range(2, 13), b=range(100, 1001, 50), T=range(5000, 80001, 1000), v=("c", "n", "x")),
    ],
    "4b": [
        S("A mason spreads ${t}$ in. of mortar on each of ${v} - 1$ layers. Write an expression for the total thickness of the mortar.",
          lambda d: f"{frac(d.t)} ({d.v} - 1)", lambda n: n.t * (n.v - 1),
          t=(F(1, 4), F(3, 8), F(1, 2), F(5, 8), F(3, 4)), v=LETTERS),
        S("A baker spreads ${t}$ in. of frosting between each pair of the ${v}$ layers of a cake, which makes ${v} - 1$ layers of frosting. Write an expression for the total thickness of the frosting.",
          lambda d: f"{frac(d.t)} ({d.v} - 1)", lambda n: n.t * (n.v - 1),
          t=(F(1, 4), F(3, 8), F(1, 2), F(5, 8), F(3, 4)), v=LETTERS),
    ],
    "4c": [
        S("A {item} has a regular price of ${v}$ dollars, and a coupon takes \\${off} off each {unit}. Write an expression for the cost of {k} {units} at the discounted price.",
          lambda d: f"{d.k}({d.v} - {d.off})", lambda n: n.k * (n.v - n.off),
          kind=[dict(item="concert ticket", unit="ticket", units="tickets"),
                dict(item="movie ticket", unit="ticket", units="tickets"),
                dict(item="video game", unit="game", units="games"), dict(item="shirt", unit="shirt", units="shirts")],
          off=range(2, 31), k=range(2, 9), v=("p", "x", "c")),
        S("{k_w} friends used a coupon that took \\${off} off each ticket and paid \\${total} for {k2_w} tickets. Let ${v}$ be the regular price of one ticket. Write an equation.",
          lambda d: f"{int(d.k2_w)}({d.v} - {d.off}) = {d.total}", lambda n: eq(n.k2_w * (n.v - n.off), n.total),
          need=lambda d: d.price > d.off,
          k_w=words(2, 8, cap=True), k2_w=lambda r, d: Word(d.k_w), off=range(2, 31), price=range(10, 61),
          total=lambda r, d: d.k_w * (d.price - d.off), v=("p", "x", "c")),
        S("A {item} has a regular price of ${v}$ dollars, and every {item} is marked down \\${off}. Write an expression for the cost of {k} {items} at the sale price.",
          lambda d: f"{d.k}({d.v} - {d.off})", lambda n: n.k * (n.v - n.off),
          kind=[dict(item="shirt", items="shirts"), dict(item="jacket", items="jackets"),
                dict(item="lamp", items="lamps"), dict(item="backpack", items="backpacks")],
          off=range(2, 21), k=range(2, 9), v=("s", "p", "c")),
        S("A coupon takes {p}% off a price of ${v}$ dollars. Write an expression for the amount you pay.",
          lambda d: f"{d.v} - {pct(d.p)}{d.v}", lambda n: n.v - n.p / 100 * n.v,
          alt=lambda d: [f"{pct(100 - d.p)}{d.v}"], p=PCT, v=("p", "x", "c", "d")),
    ],
    "4d": [
        S("An {what} solution has a total volume of {T} L, and {a} L of that is {what}. Write an expression for the percent of the solution that is {what}.",
          lambda d: f"({d.a} / {d.T})(100)", lambda n: n.a / n.T * 100,
          what=("acid", "alcohol"), W=decs("0.5", 3, "0.1"), a=decs("0.001", "0.05", "0.001"), T=lambda r, d: d.W + d.a),
        S("A class has {T} students, and {a} of them walk to school. Write an expression for the percent of the class that walks to school.",
          lambda d: f"({d.a} / {d.T})(100)", lambda n: n.a / n.T * 100,
          need=lambda d: d.a < d.T, T=range(12, 36), a=range(1, 35)),
    ],
    "4e": [
        S("A {cheap} costs ${v}$ dollars, and a {dear} costs \\${diff} more. Write an expression for the cost of {k} {dears}.",
          lambda d: f"{d.k}({d.v} + {d.diff})", lambda n: n.k * (n.v + n.diff), fish=CHEAP_V, diff=range(1, 16), k=range(2, 10)),
        S("A {cheap} costs ${v}$ dollars and a {dear} costs \\${diff} more. Write an expression for the cost of one {dear} and {k} {cheaps}.",
          lambda d: f"({d.v} + {d.diff}) + {d.k}{d.v}", lambda n: n.v + n.diff + n.k * n.v,
          fish=CHEAP_V, diff=range(1, 16), k=range(2, 10)),
        S("A {dear} costs ${v}$ dollars, and a {cheap} costs \\${diff} less. Write an expression for the cost of {k} {cheaps}.",
          lambda d: f"{d.k}({d.v} - {d.diff})", lambda n: n.k * (n.v - n.diff), fish=DEAR_V, diff=range(1, 16), k=range(2, 10)),
    ],
    "4f": [
        S("Each drop of {liquid} has a volume of {vol} mL. Write an expression for the volume, in liters, of ${v}$ drops. (1 L = 1000 mL)",
          lambda d: f"{d.vol}{d.v} / 1000", lambda n: n.vol * n.v / 1000,
          liquid=("acid", "water", "dye", "food coloring"), vol=decs("0.02", "0.1", "0.01"), v=("n", "d", "k")),
        S("Each {sheet} is {th} mm thick. Write an expression for the thickness, in centimeters, of a stack of ${v}$ {sheets}. (1 cm = 10 mm)",
          lambda d: f"{d.th}{d.v} / 10", lambda n: n.th * n.v / 10,
          kind=[dict(sheet="sheet of paper", sheets="sheets"), dict(sheet="card", sheets="cards"),
                dict(sheet="coin", sheets="coins")], th=decs("0.1", 2, "0.1"), v=("n", "s", "k")),
    ],
    # ---------------- Level 5: two inferences combined ----------------
    "5a": [
        S("A wall has ${v}$ rows of bricks that are {h} in. tall, with ${t}$ in. of mortar on top of every row but the last. Write an expression for the height of the wall.",
          lambda d: f"{d.h}{d.v} + {frac(d.t)} ({d.v} - 1)", lambda n: n.h * n.v + n.t * (n.v - 1),
          v=("n", "r", "k", "x"), h=range(2, 9), t=(F(1, 4), F(3, 8), F(1, 2), F(5, 8))),
        S("A wall of ${v}$ rows of {h}-in. bricks, with ${t}$ in. of mortar on top of every row but the last, is ${H}$ in. high. Write an equation to find ${v}$.",
          lambda d: f"{d.h}{d.v} + {frac(d.t)} ({d.v} - 1) = {M(d.H)}", lambda n: eq(n.h * n.v + n.t * (n.v - 1), n.H),
          v=("n", "r", "k", "x"), h=range(2, 9), t=(F(1, 4), F(3, 8), F(1, 2), F(5, 8)),
          rows=range(5, 31), H=lambda r, d: d.h * d.rows + d.t * (d.rows - 1)),
        S("A mason turns the bricks so the {h}-in. edge is vertical and lays ${v}$ rows, with ${t}$ in. of mortar on top of every row but the last. Write an expression for the height of the wall.",
          lambda d: f"{d.h}{d.v} + {frac(d.t)} ({d.v} - 1)", lambda n: n.h * n.v + n.t * (n.v - 1),
          h=range(2, 9), v=("n", "r", "k", "x"), t=(F(1, 4), F(3, 8), F(1, 2), F(5, 8))),
    ],
    "5b": [
        S("{k_w} friends each rent a {item} at \\${rate} per hour for ${v}$ hours, and each pays {an_fee} \\${fee} equipment fee. Write an expression for their total cost.",
          lambda d: f"{int(d.k_w)}({d.rate}{d.v} + {d.fee})", lambda n: n.k_w * n.rate * n.v + n.k_w * n.fee,
          k_w=words(2, 6, cap=True), item=("kayak", "canoe", "paddleboard", "bike"), rate=range(8, 41),
          fee=range(5, 51), v=HOURS, an_fee=an("fee")),
        S("A pitcher earns \\${s} in salary each year plus \\${b} for each of ${v}$ bonus games that year. Write an expression for her total earnings over {y} years.",
          lambda d: f"{d.y}({d.s} + {d.b}{d.v})", lambda n: n.y * n.s + n.y * n.b * n.v,
          s=range(10000, 50001, 1000), b=range(1000, 15001, 500), y=range(2, 11), v=("a", "g", "n")),
        S("A pitcher earns \\${s} in salary each year plus \\${b} for each of ${v}$ bonus games that year, and she earns \\${T} over {y} years. Write an equation to find ${v}$.",
          lambda d: f"{d.y}({d.s} + {d.b}{d.v}) = {d.T}", lambda n: eq(n.y * n.s + n.y * n.b * n.v, n.T),
          need=lambda d: d.T > d.y * d.s,
          s=range(10000, 50001, 1000), b=range(1000, 15001, 500), T=range(100000, 2000001, 50000), y=range(2, 11),
          v=("a", "g", "n")),
    ],
    "5c": [
        S("A technician mixes ${v}$ liters of {an_p1} {p1}% acid solution with ${L} - {v}$ liters of {an_p2} {p2}% acid solution. Write an expression for the total number of liters of acid in the mixture.",
          lambda d: f"{pct(d.p1)}{d.v} + {pct(d.p2)}({d.L} - {d.v})", lambda n: n.p1 / 100 * n.v + n.p2 / 100 * (n.L - n.v),
          need=lambda d: d.p1 < d.p2, v=("x", "a", "y"), p1=PCT, L=range(5, 61), p2=PCT, an_p1=an("p1"), an_p2=an("p2")),
        S("A technician mixes ${v}$ liters of {an_p1} {p1}% acid solution with ${L} - {v}$ liters of {an_p2} {p2}% acid solution to get {L} L that is {p3}% acid. Write an equation.",
          lambda d: f"{pct(d.p1)}{d.v} + {pct(d.p2)}({d.L} - {d.v}) = {pct(d.p3)}({d.L})",
          lambda n: eq(n.p1 / 100 * n.v + n.p2 / 100 * (n.L - n.v), n.p3 / 100 * n.L),
          need=lambda d: d.p1 < d.p3 < d.p2, v=("x", "a", "y"), p1=PCT, L=range(5, 61), p2=PCT, p3=PCT, an_p1=an("p1"), an_p2=an("p2")),
    ],
    "5d": [
        S("{name} walks ${v}$ miles to the {place} at {w} mi/h and rides the {vehicle} back along the same route at {b} mi/h. Write an expression for {poss} total travel time, in hours.",
          lambda d: f"{d.v}/{d.w} + {d.v}/{d.b}", lambda n: n.v / n.w + n.v / n.b,
          who=people("Terrence", "he", "his"), place=("theater", "museum", "library", "stadium"), w=(2, 3, 4),
          vehicle=("bus", "train"), b=range(15, 61, 5), v=("d", "m", "x")),
        S("{name}'s whole trip takes {T} h: {ref} walks ${v}$ miles at {w} mi/h, watches a movie for {M} h, then rides the {vehicle} back ${v}$ miles at {b} mi/h. Write an equation.",
          lambda d: f"{d.v}/{d.w} + {d.M} + {d.v}/{d.b} = {d.T}", lambda n: eq(n.v / n.w + n.M + n.v / n.b, n.T),
          need=lambda d: d.M <= d.T - 1,
          who=people("Terrence", "he", "his"), T=decs(2, 6, "0.25"), v=("d", "m", "x"), w=(2, 3, 4),
          M=decs("1.5", 3, "0.25"), vehicle=("bus", "train"), b=range(15, 61, 5)),
    ],
    "5e": [
        S("{name} bought {k1} {cheaps} and {k2} {dears} for \\${total} in all, and a {dear} costs \\${diff} more than a {cheap}. Let ${v}$ be the cost of a {cheap}. Write an equation.",
          lambda d: f"{d.k1}{d.v} + {d.k2}({d.v} + {d.diff}) = {d.total}",
          lambda n: eq(n.k1 * n.v + n.k2 * (n.v + n.diff), n.total),
          need=lambda d: d.total > (d.k1 + d.k2) + d.k2 * d.diff,
          name=named("Anna"), fish=CHEAP_V, k1=range(2, 11), k2=range(2, 11), diff=range(1, 11), total=range(20, 151)),
        S("{name} bought {k1} {cheaps} and {k2} {dears} for \\${total} in all, and a {cheap} costs \\${diff} less than a {dear}. Let ${v}$ be the cost of a {dear}. Write an equation.",
          lambda d: f"{d.k1}({d.v} - {d.diff}) + {d.k2}{d.v} = {d.total}",
          lambda n: eq(n.k1 * (n.v - n.diff) + n.k2 * n.v, n.total),
          need=lambda d: d.total > (d.k1 + d.k2) + d.k2 * d.diff,
          name=named("Anna"), fish=DEAR_V, k1=range(2, 11), k2=range(2, 11), diff=range(1, 11), total=range(20, 151)),
    ],
}
PART = {"half": 2, "one third": 3, "one fourth": 4}

def story_of(p):
    entry, _, i = p["story"].partition(".")
    return STORIES[entry][int(i)]

# ------------------------------------------------------------------
# Drawing and checking
# ------------------------------------------------------------------
def draw(entry, r, tpl):
    st = STORIES[entry][tpl]
    d = drawn(st, r)
    answer, alt = keyed(st, d)
    return dict(story=f"{entry}.{tpl}", prompt=fill(st.text, d), answer=answer, alt=alt)

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(STORIES[e]))

def value(t):
    """Typst math -> sympy, exactly: decimals as fractions, 1 1/8 as 1 + 1/8."""
    t = re.sub(r"(?<![\d.])(\d+) (\d+)/(\d+)", r"(\1 + \2/\3)", t)
    t = re.sub(r"\d*\.\d+", lambda m: f"({str(sp.Rational(m.group()))})", t)
    return sp.sympify(to_sympy(t))

def agrees(answer, truth):
    """The answer is the quantity; an equation is the same equation, up to a nonzero multiple."""
    if isinstance(truth, tuple):
        if answer.count("=") != 1:
            return False
        left, right = answer.split("=")
        q = sp.simplify((value(left) - value(right)) / (truth[0] - truth[1]))
        return bool(q.is_number and q != 0)
    return "=" not in answer and sp.simplify(value(answer) - truth) == 0

def check(p):
    """Read the prompt back with its story, work the quantity out, and compare the answer and every alternate."""
    try:
        st = story_of(p)
        truth = worked(st, read_back(st, p["prompt"]))
        ok = all(agrees(a, truth) for a in [p["answer"]] + list(p.get("alt", [])))
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    return p["prompt"]

def answer_typst(p):
    alt = p.get("alt") or []
    return display(dfrac(p["answer"])) + (" (or " + ", ".join(display(dfrac(a)) for a in alt) + ")" if alt else "")

def text(p):
    return plain(re.sub(r"(?<!\\)\$", "", p["prompt"]).replace("\\$", "$"))

def answer_text(p):
    alt = p.get("alt") or []
    return plain(p["answer"]) + (" (or " + ", ".join(plain(a) for a in alt) + ")" if alt else "")

def height(p):
    """Inches the prompt takes in a half-width column, roughly."""
    return 0.2 * (1 + len(text(p)) // 45)

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    """The story's words with new numbers, names, or letters: the key is written again from them."""
    t = " ".join(t.split())
    st = story_of(old)
    try:
        d = read_back(st, t)
        answer, alt = keyed(st, d)
    except (ValueError, KeyError, IndexError):
        raise ValueError("keep the story's words; change only its numbers, names, and letters") from None
    new = dict(old, prompt=t, answer=answer, alt=alt, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    t = " ".join(t.replace("−", "-").split())
    try:
        value(t.replace("=", "-"))
    except Exception:
        raise ValueError("write the answer in Typst math, like 4(p - 15) = 108") from None
    new = dict(p, answer=t, alt=[])
    return new, check(new)

def selftest(n, seed):
    import random
    rng = random.Random(seed)
    for e in ENTRIES:
        seen = set()
        for i in range(n):
            if i % 25 == 0:
                seen = set()
            generate(e["key"], rng, seen)
    print(f"{NAME} {len(ENTRIES)} entries, {n} drawn of each, all verified")
    return True
