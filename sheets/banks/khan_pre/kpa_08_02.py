"""Khan Prealgebra, Lesson 8-2: Percent problems, from the old app's
PreAlg_08_02 (sixteen generated stories). Old errors, fixed here: the iris
story asked how many more blooms and keyed the total; the hiking, carbs,
spider, and test stories took 33% (and 67%) as exactly 1/3 (2/3), so
their numbers didn't fit (the hiking one could key 2 km as 33% less than
2 km); the percent-change stories rounded to a tenth without saying so.
Every percent here is exact, and so is every answer. Names only, no
pronouns.

Type 1: the new amount, or the change (spider bugs, a bottle, iris blooms,
reading minutes, video game points). Type 2: the original amount (height
last year, raked leaves, cheese in a recipe, a timed test, a hike). Type 3:
the percent change (a carved pumpkin, an evaporating pool, iron in
cereal). Type 4: did they meet a goal of at least p%, and by how much?
(Whole grains, painting a house.)

A problem: dict(type, story, nums, prompt, answer, source).
    nums  the story's numbers, {"last": 40, "p": 25}
    answer  "50 bugs", "Yes, 12 square meters more than the goal"
check() works the story's percent out again from nums, exactly, and
requires nums to be the prompt's numbers.
"""
import math, re
from fractions import Fraction as F
from ... import gen
from ...gen import need
from . import courses

NAME = FAMILY = "kpa_08_02"
FIXED = False
TITLE = "Lesson 8-2: Percent problems"
INSTRUCTIONS = "Answer each question."
COURSES = courses(8)

TYPES = [
    dict(key="1", title="The New Amount or the Change",
         look="An amount and a percent more or less.",
         move="p% of the amount is the change. Add it (more) or subtract it (less) for the new amount.", width="full"),
    dict(key="2", title="The Original Amount",
         look="The amount after a percent change; the amount before is unknown.",
         move="p% more means the new amount is (100 + p)% of the original: divide by 1 + p/100 (or 1 - p/100 "
              "for less).", width="full"),
    dict(key="3", title="The Percent Change",
         look="An amount before and after.",
         move="Percent change = (the change ÷ the original) × 100.", width="full"),
    dict(key="4", title="Did They Meet the Goal?",
         look="A goal of at least p% of a whole, and what was done.",
         move="Find p% of the whole, then compare: more or less than the goal, and by how much.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def num(x):
    x = F(x)
    return f"{int(x):,}" if x.denominator == 1 else f"{float(x):.4f}".rstrip("0").rstrip(".")

def whole(r, p, lo, hi):
    """A whole number from lo to hi of which p% is whole."""
    step = 100 // math.gcd(p, 100)
    need(hi // step >= max(1, -(-lo // step)))
    return step * r.randint(max(1, -(-lo // step)), hi // step)

# Each story: draw(r, name) -> (prompt, nums, unit); solve(nums) -> the answer, from the numbers alone.
def spider(r, n):
    p = r.choice((20, 25, 40, 50, 60))
    last = whole(r, p, 5, 40)
    return (f"A spider ate {p}% more bugs this month than last month. The spider ate {last} bugs last month. How many "
            f"bugs did the spider eat this month?", dict(p=p, last=last), "bugs")

def bottle(r, n):
    p = r.choice((25, 50, 75))
    fam = whole(r, p, 8, 40)
    product = r.choice(("sunscreen", "lotion", "shampoo"))
    return (f"The family size bottle of {product} holds {fam} fluid ounces. The regular bottle holds {p}% less. How "
            f"many fewer fluid ounces does the regular bottle hold?", dict(p=p, fam=fam), "fluid ounces")

def blooms(r, n):
    p = r.choice((5, 10, 15, 20, 25))
    last = whole(r, p, 20, 80)
    return (f"{n} had {last} iris blooms last year and {p}% more this year. How many more iris blooms did {n} have "
            f"this year?", dict(p=p, last=last), "blooms")

def reading(r, n):
    p = r.choice((10, 15, 20, 25, 30, 40, 50))
    m = whole(r, p, 400, 600)
    return (f"{n} read for {m} minutes this month and plans to read {p}% more minutes next month. If {n} does, how "
            f"many minutes will {n} read in all during the two months?", dict(p=p, m=m), "minutes")

def game(r, n):
    other = r.choice([x for x in gen.NAMES if x != n])
    p = r.choice((10, 15, 20, 25, 30, 40, 50))
    pts = whole(r, p, 500, 1500)
    return (f"In a video game, {n} scored {p}% fewer points than {other}. {other} scored {num(pts)} points. How many "
            f"points did {n} score?", dict(p=p, pts=pts), "points")

def height(r, n):
    p = r.choice((5, 10))
    last = whole(r, p, 120, 180)
    now = last * (100 + p) // 100
    return (f"{n} was {now} cm tall on the first day of school this year, {p}% taller than on the first day of "
            f"school last year. How tall was {n} on the first day of school last year?", dict(p=p, now=now), "cm")

def leaves(r, n):
    other = r.choice([x for x in gen.NAMES if x != n])
    p = r.choice((4, 5, 8, 10, 12, 15))
    them = whole(r, p, 250, 500)
    mine = them * (100 + p) // 100
    return (f"{n} raked {p}% more leaves than {other}. {n} raked {mine} liters of leaves. How many liters of leaves "
            f"did {other} rake?", dict(p=p, more=mine), "liters")

def cheese(r, n):
    p = r.choice((20, 25, 40, 50, 60, 80))
    orig = whole(r, p, 30, 100)
    used = orig * (100 + p) // 100
    return (f"{n} increased every ingredient in a recipe by {p}% and used {used} grams of cheese. How much cheese did "
            f"the recipe call for?", dict(p=p, more=used), "grams")

def test(r, n):
    other = r.choice([x for x in gen.NAMES if x != n])
    p = r.choice((5, 10, 15, 20, 25, 30))
    theirs = whole(r, p, 60, 200)
    mine = theirs * (100 - p) // 100
    return (f"{n} took {p}% fewer seconds than {other} to finish a multiplication test. {n} took {mine} seconds. How "
            f"many seconds did {other} take?", dict(p=p, less=mine), "seconds")

def hike(r, n):
    p = r.choice((10, 20, 25, 40, 50))
    am = whole(r, p, 4, 20)
    pm = am * (100 - p) // 100
    return (f"{n} hiked several kilometers in the morning, then only {pm} kilometers in the afternoon, {p}% less than "
            f"in the morning. How many kilometers did {n} hike in all?", dict(p=p, pm=pm), "kilometers")

def pumpkin(r, n):
    p = r.randint(20, 50)
    before = F(r.randint(55, 90), 10)
    after = before * (100 - p) / 100
    need(after * 100 == int(after * 100))
    return (f"{n}'s pumpkin had a mass of {num(before)} kilograms before carving and {num(after)} kilograms after. "
            f"What was the percent decrease in the mass of the pumpkin?", dict(before=str(before), after=str(after)), "%")

def pool(r, n):
    p = r.randint(5, 30)
    before = F(r.randint(20, 30), 10)
    after = before * (100 - p) / 100
    need(after * 100 == int(after * 100))
    return (f"A swimming pool held {num(before)} million liters of water. Some evaporated, and then it held "
            f"{num(after)} million liters. What percent of the water evaporated?",
            dict(before=str(before), after=str(after)), "%")

def cereal(r, n):
    p = r.randint(10, 50)
    before = F(r.randint(10, 25), 10)
    after = before * (100 + p) / 100
    need(after * 100 == int(after * 100))
    return (f"A cereal had {num(before)} milligrams of iron per serving. A new recipe has {num(after)} milligrams. "
            f"What was the percent increase in iron?", dict(before=str(before), after=str(after)), "%")

def grains(r, n):
    g = r.choice((20, 25, 30, 40, 50))
    total = whole(r, g, 200, 300)
    ate = total * g // 100 + r.choice((-1, 0, 1)) * r.randint(5, 15)
    return (f"{n} aims to get at least {g}% of the day's carbohydrates from whole grains. Today {n} ate {total} grams "
            f"of carbohydrates, {ate} grams of them from whole grains. Did {n} meet the goal? By how much?",
            dict(g=g, total=total, done=ate), "grams")

def painting(r, n):
    g = r.choice((50, 60, 70, 75, 80))
    total = whole(r, g, 300, 600)
    done = total * g // 100 + r.choice((-1, 1)) * r.randint(3, 20)
    return (f"{n} aimed to paint at least {g}% of the {total} square meters of a house's walls by today, and painted "
            f"{done} square meters. Did {n} meet the goal? By how much?", dict(g=g, total=total, done=done),
            "square meters")

def pct(x):
    return F(x, 100)

SOLVE = {
    "spider": lambda d: d["last"] * (1 + pct(d["p"])),
    "bottle": lambda d: d["fam"] * pct(d["p"]),
    "blooms": lambda d: d["last"] * pct(d["p"]),
    "reading": lambda d: d["m"] + d["m"] * (1 + pct(d["p"])),
    "game": lambda d: d["pts"] * (1 - pct(d["p"])),
    "height": lambda d: d["now"] / (1 + pct(d["p"])),
    "leaves": lambda d: d["more"] / (1 + pct(d["p"])),
    "cheese": lambda d: d["more"] / (1 + pct(d["p"])),
    "test": lambda d: d["less"] / (1 - pct(d["p"])),
    "hike": lambda d: d["pm"] / (1 - pct(d["p"])) + d["pm"],
    "pumpkin": lambda d: (F(d["before"]) - F(d["after"])) / F(d["before"]) * 100,
    "pool": lambda d: (F(d["before"]) - F(d["after"])) / F(d["before"]) * 100,
    "cereal": lambda d: (F(d["after"]) - F(d["before"])) / F(d["before"]) * 100,
    "grains": lambda d: d["done"] - d["total"] * pct(d["g"]),
    "painting": lambda d: d["done"] - d["total"] * pct(d["g"]),
}
STORIES = {"1": [spider, bottle, blooms, reading, game], "2": [height, leaves, cheese, test, hike],
           "3": [pumpkin, pool, cereal], "4": [grains, painting]}

def goal_answer(diff, unit):
    if diff == 0:
        return "Yes, exactly the goal"
    return f"{'Yes' if diff > 0 else 'No'}, {num(abs(diff))} {unit} {'more' if diff > 0 else 'less'} than the goal"

def draw(entry, r, tpl):
    make = STORIES[entry][tpl]
    prompt, nums, unit = make(r, r.choice(gen.NAMES))
    x = SOLVE[make.__name__](nums)
    need(F(x).denominator == 1 and x > 0 if entry != "4" else True)
    answer = goal_answer(x, unit) if entry == "4" else (f"{num(x)}%" if unit == "%" else f"{num(x)} {unit}")
    return dict(story=make.__name__, nums=nums, unit=unit, prompt=prompt, answer=answer)

def check(p):
    try:
        x = SOLVE[p["story"]](p["nums"])
        shown = all(num(v) in p["prompt"] for v in p["nums"].values())
        if p["type"] == "4":
            ok = p["answer"].strip().rstrip(".") == goal_answer(x, p["unit"])
        else:
            got = F(re.match(r"[\d,.]+", p["answer"].strip()).group(0).replace(",", ""))
            ok = got == x
        return "checked" if ok and shown else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(STORIES[e]))

def typst(p, gap="0.3em"):
    return p["prompt"].replace("%", "\\%")

def answer_typst(p):
    return p["answer"].replace("%", "\\%")

def text(p):
    return p["prompt"]

def answer_text(p):
    return p["answer"]

def height(p):
    return 0.8

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    raise ValueError("reroll for a new story; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
