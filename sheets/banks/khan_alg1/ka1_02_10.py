"""Khan Algebra 1, Lesson 2-10: Using inequalities to solve problems, from
the old app's Alg1_02_10 (twelve of Khan's stories; five answered).

Every story is one model: a starting amount plus a rate times a count,
kept at most (or under, or at least) a limit. (a) Which inequality
describes it? (b) The largest or smallest whole count that works, or one
more step from it: pancakes from stacks, the cost of the rolls. Khan's
twelve stories are kept, retold with names and no pronouns. The wrong
choices are Khan's: the right expression and one mistaken one (the rate
left off, the numbers swapped, a price for a capacity, another number in
the story for the limit), each with the sign both ways.

The old key for the plumber (no. 9) had 65 + 28H >= 250; "no more than
$250" is <=.

A problem: dict(type, story, prompt, choices, answer, source).
    prompt   the story and its letter, in words
    choices  four inequalities, Typst math
    answer   "C; 4 boxes": part (a)'s letter, then part (b)
check() reads the numbers back out of the story, builds the model, and
searches every whole count for part (b).
"""
from fractions import Fraction as F
from ... import gen
from ...gen import need
from ...typst import esc
from ...typmath import text as plain
from . import courses

NAME = FAMILY = "ka1_02_10"
FIXED = False
TITLE = "Lesson 2-10: Using inequalities to solve problems"
INSTRUCTIONS = "Answer both parts."
COURSES = courses(2)

TYPES = [
    dict(key="1", title="How Many?",
         look="A starting amount, a rate per item, and a limit; the question asks for the number of items.",
         move="Write start + rate · n with ≤ (at most, no more than) or ≥ (at least). Solve, then round to a "
              "whole number the way the story allows: down for at most, up for at least.", width="full"),
    dict(key="2", title="One More Step",
         look="The same model, but the question asks for something that comes from the count: slices, "
              "pancakes, dollars.",
         move="Find the whole-number count as in Type 1. Then use it: multiply by the pieces in each pack or "
              "the price of each.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.75in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
QUESTION_A = "Which inequality describes this scenario?"

# start + rate * n  op  limit. wrong: the mistaken expression, from the story's
# numbers ("one": the rate left off; "swap": start and rate traded; or the
# name of another number that takes the rate's or the limit's place).
STORIES = [
    dict(key="a", type="1", letter="S", op="<=", wrong="one", unit="box", units="boxes",
         text="{name} goes to the market with ${limit} to buy eggs and sugar. A package of 12 eggs costs ${start}. "
              "After getting the eggs, {name} wants to buy as much sugar as possible with the money left. The "
              "sugar comes in boxes that cost ${rate} each. Let S be the number of boxes of sugar {name} buys.",
         ask="How many boxes of sugar can {name} afford?"),
    dict(key="b", type="1", letter="F", op=">=", wrong="swap", unit="bag", units="bags",
         text="{name} runs a bakery and needs at least {limit} kilograms of flour for holiday orders. The bakery "
              "has {start} kilograms of flour, and flour comes in bags of {rate} kilograms each. {name} wants to "
              "buy as few bags as possible. Let F be the number of bags of flour {name} buys.",
         ask="What is the smallest number of bags {name} can buy?"),
    dict(key="c", type="1", letter="S", op="<=", wrong="limit:km", unit="stop", units="stops",
         text="A train ticket costs ${start} plus ${rate} per stop. {name} has ${limit} and would like to travel "
              "{km} kilometers. Let S be the number of stops on {name}'s ticket.",
         ask="What is the largest number of stops {name} can afford?"),
    dict(key="d", type="1", letter="C", op=">=", wrong="one", unit="class", units="classes",
         text="A yoga studio charges each customer a one-time fee of ${start} plus ${rate} per class. {name}, the "
              "manager, wants each customer to spend at least ${limit} at the studio. Let C be the number of "
              "classes a customer takes.",
         ask="What is the smallest number of classes a customer can take to meet {name}'s goal?"),
    dict(key="e", type="1", letter="H", op="<=", wrong="swap", unit="hour", units="hours",
         text="A plumber charges a fee of ${start} plus ${rate} per hour, and charges only for whole hours. "
              "{name} wants to spend no more than ${limit}. Let H be the number of hours the plumber works.",
         ask="What is the largest number of hours {name} can afford?"),
    dict(key="f", type="1", letter="B", op=">=", wrong="limit:off", unit="paintball", units="paintballs",
         text="A paintball field charges an entrance fee of ${start} and ${rate} per paintball. Anyone who "
              "spends ${limit} or more gets ${off} off. Let B be the number of paintballs {name} buys.",
         ask="What is the smallest number of paintballs {name} can buy, with the entrance fee, to get the discount?"),
    dict(key="g", type="1", letter="B", op=">=", wrong="one", unit="block", units="blocks",
         text="{name} is reserving hotel rooms for a company trip and needs at least {limit} rooms. {start} "
              "rooms are already reserved. The hotel reserves rooms in blocks of {rate} rooms, at ${price} a "
              "block. Let B be the number of additional blocks {name} reserves.",
         ask="What is the smallest number of additional blocks {name} can reserve?"),
    dict(key="h", type="2", letter="B", op="<=", wrong="rate:per", unit="avocado", units="avocados", times="per",
         text="{name} brings ${limit} to the market and buys eggs that cost ${start}. The store sells avocados "
              "only in bags of {per} for ${rate}, and {name} wants as many avocados as the money left will buy. "
              "Let B be the number of bags of avocados {name} buys.",
         ask="What is the largest number of avocados {name} can afford?"),
    dict(key="i", type="2", letter="S", op="<=", wrong="one", unit="pancake", units="pancakes", times="per",
         text="{name} orders chocolate milk that costs ${start}, then wants as many pancakes as possible with "
              "the bill at most ${limit} before tax. The restaurant sells pancakes only in stacks of {per} for "
              "${rate}. Let S be the number of stacks of pancakes {name} buys.",
         ask="What is the largest number of pancakes {name} can buy?"),
    dict(key="j", type="2", letter="P", op="<", wrong="swap", unit="slice", units="slices", times="per",
         text="{name} is ordering pizzas for an office party. The restaurant charges a ${start} delivery fee and "
              "${rate} per pizza, and the total must stay under ${limit}. Each pizza is cut into {per} slices. "
              "Let P be the number of pizzas {name} buys.",
         ask="What is the largest number of slices {name} can buy?"),
    dict(key="k", type="2", letter="C", op=">=", wrong="rate:price", unit="dollar", units="dollars", times="price",
         text="{name} needs at least {limit} gigabytes (GB) of storage for vacation photos. {name}'s phone has "
              "{start} GB free, and memory cards hold {rate} GB each and cost ${price}. Let C be the number of "
              "memory cards {name} buys.",
         ask="What is the least {name} can spend on memory cards?"),
    dict(key="l", type="2", letter="R", op=">=", wrong="swap", unit="dollar", units="dollars", times="price",
         text="{name} needs at least {limit} pieces of sushi for a meeting and has already ordered {start} "
              "pieces. Sushi comes in rolls of {rate} pieces that cost ${price} each. Let R be the number of "
              "additional rolls {name} orders.",
         ask="What is the least {name} can spend on the additional rolls?"),
]
STORY = {s["key"]: s for s in STORIES}
BY_TYPE = {k: [s for s in STORIES if s["type"] == k] for k in KEYS}
FLIP = {"<=": ">=", ">=": "<=", "<": ">", ">": "<"}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def money(x):
    """$ amounts as Khan writes them: 55, 2.75, 11.50, 0.08."""
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{float(x):.2f}"

# ------------------------------------------------------------------
# Drawing: start, rate, and limit, with the count from 2 to 15 (paintballs: hundreds)
# ------------------------------------------------------------------
def numbers(r, st):
    k = st["key"]
    cents = lambda lo, hi, step=25: F(r.randrange(lo, hi + 1, step), 100)
    if k in "aih":                                     # dollars and cents at the market
        v = dict(start=cents(150, 450), rate=cents(300, 1200, 50))
        if k in "hi":                                  # avocados in bags, pancakes in stacks
            v["per"] = r.randint(2, 6)
    elif k == "c":
        v = dict(start=F(r.randint(2, 8)), rate=cents(125, 400), km=r.randrange(20, 80, 5))
    elif k == "d":
        v = dict(start=F(r.randrange(20, 60, 5)), rate=F(r.randint(8, 20)))
    elif k == "e":
        v = dict(start=F(r.randrange(40, 100, 5)), rate=F(r.randint(20, 45)))
    elif k == "f":
        v = dict(start=F(r.randint(12, 25)), rate=F(r.randint(5, 12), 100), off=r.choice((5, 10, 15)))
    elif k in "bgl":                                    # amounts already in hand, packs of a size
        v = dict(start=F(r.randint(10, 40)), rate=F(r.randint(5, 25)))
        if k != "b":
            v["price"] = F(r.randint(5, 12)) if k == "l" else F(r.randrange(400, 1200, 50))
    elif k == "j":
        v = dict(start=cents(300, 900, 50), rate=F(r.randint(10, 18)), per=r.choice((6, 8, 10, 12)))
    else:                                               # k: storage
        v = dict(start=F(r.randint(20, 200)), rate=F(r.choice((64, 128, 256))), price=F(r.randint(8, 30)))
    n = r.randint(150, 900) if k == "f" else r.randint(2, 15)     # Khan's paintballs: 713
    if st["op"] in ("<=", "<"):                        # the limit lands between n and n + 1 (or on n, for <=)
        v["limit"] = v["start"] + v["rate"] * n + (v["rate"] * r.randint(0, 9) / 10 if st["op"] == "<=" else v["rate"] / 2)
    else:                                               # between n - 1 and n (or on n)
        v["limit"] = v["start"] + v["rate"] * n - v["rate"] * r.randint(0, 9) / 10
    v["limit"] = F(round(v["limit"])) if k not in "aih" else F(int(v["limit"]))
    need(v["limit"] > v["start"])
    return v

def shown(v):
    """The story's numbers as written."""
    return {k: money(x) if isinstance(x, F) else x for k, x in v.items()}

def expressions(st, w):
    """(right, wrong) expressions for part (a), from the story's numbers as written."""
    L, s, rt = st["letter"], w["start"], w["rate"]
    right = f"{s} + {rt} {L}"
    kind, _, other = st["wrong"].partition(":")
    if kind == "one":
        wrong = f"{s} + {L}"
    elif kind == "swap":
        wrong = f"{rt} + {s} {L}"
    elif kind == "rate":
        wrong = f"{s} + {w[other]} {L}"
    else:                                              # limit: the same expression, another number as the limit
        wrong = right
    return right, wrong

def model(st, w):
    """(right inequality, the four choices) from the story's numbers as written."""
    right, wrong = expressions(st, w)
    kind, _, other = st["wrong"].partition(":")
    limit, wrong_limit = w["limit"], (w[other] if kind == "limit" else w["limit"])
    op = st["op"]
    good = f"{right} {op} {limit}"
    if kind == "limit":
        return good, [good, f"{right} {FLIP[op]} {limit}", f"{wrong} {op} {wrong_limit}", f"{wrong} {FLIP[op]} {wrong_limit}"]
    return good, [good, f"{right} {FLIP[op]} {limit}", f"{wrong} {op} {limit}", f"{wrong} {FLIP[op]} {limit}"]

def count(st, n_of):
    """The largest (<=, <) or smallest (>=) whole count that works, from the model's numbers."""
    start, rate, limit = (gen.number(n_of[k]) for k in ("start", "rate", "limit"))
    ok = {"<=": lambda n: start + rate * n <= limit, "<": lambda n: start + rate * n < limit,
          ">=": lambda n: start + rate * n >= limit}[st["op"]]
    top = int(abs(limit - start) / rate) + 3
    fits = [n for n in range(0, top + 1) if ok(n)]
    return max(fits) if st["op"] in ("<=", "<") else min(fits)

def part_b(st, n_of):
    n = count(st, n_of)
    if st.get("times") == "per":
        n *= int(n_of["per"])
    elif st.get("times") == "price":
        return f"${money(n * gen.number(n_of['price']))}"
    return f"{n} {st['unit'] if n == 1 else st['units']}"

def draw(entry, r, tpl):
    st = BY_TYPE[entry][tpl]
    w = dict(shown(numbers(r, st)), name=r.choice(gen.NAMES))
    good, choices = model(st, w)
    need(len(set(choices)) == 4)
    r.shuffle(choices)
    prompt = gen.fill(st["text"], **w)
    return dict(story=st["key"], prompt=prompt, choices=choices,
                answer=f"{gen.ABC[choices.index(good)]}; {part_b(st, w)}")

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(BY_TYPE[e]))

# ------------------------------------------------------------------
# Checking: from the story's words
# ------------------------------------------------------------------
def check(p):
    try:
        st = STORY[p["story"]]
        w = gen.read(st["text"], p["prompt"])
        good, _ = model(st, w)
        letter, _, b = p["answer"].partition(";")
        ok = p["choices"][gen.ABC.index(letter.strip())] == good and b.strip() == part_b(st, w)
        return "checked" if ok and p["choices"].count(good) == 1 else "failed"
    except (ValueError, KeyError, IndexError):
        return "unchecked"

# ------------------------------------------------------------------
# Showing and editing: change the numbers and names; keep the words
# ------------------------------------------------------------------
def typst(p, gap="0.3em"):
    st = STORY[p["story"]]
    name = gen.read(st["text"], p["prompt"])["name"]
    ask = esc(gen.fill(st["ask"], name=name))
    story = esc(p["prompt"]).replace(f"Let {st['letter']} be", f"Let ${st['letter']}$ be")
    return (f"{story}\n    #parts([{QUESTION_A} #pad(left: 1em, top: 0.4em, "
            f"{gen.choices_typst([f'${c}$' for c in p['choices']], 'grid')[1:]})], [{ask}])")

def answer_typst(p):
    letter, _, b = p["answer"].partition(";")
    return f"(a) {letter.strip()}. ${p['choices'][gen.ABC.index(letter.strip())]}$ (b) {esc(b.strip())}"

def text(p):
    return p["prompt"] + "   " + gen.choices_text(p["choices"], plain)

def answer_text(p):
    letter, _, b = p["answer"].partition(";")
    return f"(a) {letter.strip()}. {plain(p['choices'][gen.ABC.index(letter.strip())])}  (b) {b.strip()}"

def height(p):
    return 0.2 * (3 + len(p["prompt"]) // 90)

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    st = STORY[old["story"]]
    w = gen.read(st["text"], t)
    good, choices = model(st, w)
    new = dict(old, prompt=t, choices=choices, answer=f"A; {part_b(st, w)}", source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
