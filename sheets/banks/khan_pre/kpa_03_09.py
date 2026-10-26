"""Khan Prealgebra, Lesson 3-9: Equivalent ratio word problems, from the old
app's PreAlg_03_09_Eq_ratios_word (sixteen generated stories, answers
computed, right). Names only, no pronouns.

Type 1: a rate in a story and a new amount; the matching amount: meat for
pet dragons, a camel's tea, a candle burning, touchdown celebrations, party
snacks, reward points, chicken wings, paint batches, reading, video editing,
cherry pies. Type 2: complete the ratio, "For every 1 red bike, there are
3 ...", from a list of counts (bikes, a fruit basket, a pet groomer, a
garden): exactly one item fits.

A problem: dict(type, prompt, ..., answer, source).
    Type 1  a1 4, b1 30, a2 6 (a1 of one thing goes with b1 of the other), answer "45 kilograms"
    Type 2  counts {"red": 3, "blue": 9, ...}, first "red", p 1, q 3, answer "blue bikes"
check(): Type 1, the answer times a1 is b1 times a2, and a1, b1, a2 are the
prompt's numbers; Type 2, the answer's count over the first's is q/p, and
no other item's is.
"""
import math, re
from fractions import Fraction as F
from ... import gen
from ...gen import need
from . import courses

NAME = FAMILY = "kpa_03_09"
FIXED = False
TITLE = "Lesson 3-9: Equivalent ratio word problems"
INSTRUCTIONS = "Answer each question."
COURSES = courses(3)

TYPES = [
    dict(key="1", title="Find the Amount",
         look="Two amounts that go together, and a new amount of one of them.",
         move="Find how many times bigger (or smaller) the new amount is, and scale the other amount the same way. "
              "Or find the amount for 1 first.", width="full"),
    dict(key="2", title="Complete the Ratio",
         look="A list of counts and a ratio with its second item missing.",
         move="Scale the counts down by the same number until the first matches the ratio; the item whose count "
              "matches the second number is the answer.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"])

def num(x):
    return f"{int(x):,}" if F(x).denominator == 1 else f"{float(x):g}"

def two(r, lo, hi):
    a, b = r.sample(range(lo, hi + 1), 2)
    return a, b

# each: r, name -> (prompt, a1, b1, a2, unit of the answer)
def dragons(r, n):
    each = F(r.randint(6, 12) * 5, 2)
    d1, d2 = r.sample([2, 4, 6, 8, 10], 2)
    return (f"{n} needs {num(d1 * each)} kilograms of meat each day to feed {d1} pet dragons. Each dragon eats the "
            f"same amount. How many kilograms of meat does {n} need each day to feed {d2} pet dragons?",
            d1, d1 * each, d2, "kilograms")

def camel(r, n):
    each, (t1, t2) = r.randint(30, 50) * 5, two(r, 2, 10)
    return (f"{n} the camel drinks tea (so classy!): {num(t1 * each)} liters every {t1} days, the same amount each "
            f"day. How many liters of tea does {n} drink every {t2} days?", t1, t1 * each, t2, "liters")

def candle(r, n):
    L, h, k = r.randint(10, 20), r.randint(3, 9), r.randint(2, 5)
    return (f"{n} is a candle maker. Each {L} cm candle burns evenly for {h} hours. If {n} makes a {L * k} cm "
            f"candle, how long will it burn?", L, h, L * k, "hours")

def touchdowns(r, n):
    flips, cannons, t = r.randint(2, 6), r.randint(2, 8), r.randint(2, 5)
    need(flips != cannons)
    if r.random() < 0.5:
        what, each = f"the mascot did {flips * t} back flips", flips
    else:
        what, each = f"the cheerleaders set off {cannons * t} confetti cannons", cannons
    return (f"Each time the Timberwolves score 1 touchdown, the mascot does {flips} back flips and the cheerleaders "
            f"set off {cannons} confetti cannons. How many touchdowns did the Timberwolves score if {what}?",
            each, 1, each * t, "touchdowns")

def snacks(r, n):
    g = r.randint(1, 4) * 2
    amounts = dict(zip(["fruit skewers", "popcorn balls", "liters of milkshake"], [2 * k for k in r.sample(range(1, 10), 3)]))
    s1, s2 = r.sample(list(amounts), 2)
    k = r.randint(2, 9)
    (x, vx), (y, vy), (z, vz) = amounts.items()
    listed = f"{vx} {x}, {vy} {y}, and {vz} {z}"
    return (f"{n} is throwing a party. For every {g} guests, {n} makes {listed}. If {n} makes {amounts[s1] * k} "
            f"{s1}, how many {s2} does {n} make?", amounts[s1], amounts[s2], amounts[s1] * k, s2)

def points(r, n):
    per, (d1, d2) = r.randint(4, 9), two(r, 2, 9)
    return (f"{n} has a new debit card and earns {num(d1 * 100 * per)} reward points for spending "
            f"${num(d1 * 100)}. At this rate, how much money did {n} spend to earn {num(d2 * 100 * per)} points?",
            d1 * 100 * per, d1 * 100, d2 * 100 * per, "dollars")

def wings(r, n):
    rate, (m1, m2) = r.randint(2, 5), two(r, 2, 9)
    return (f"{n} can eat {rate * m1} chicken wings in {m1} minutes, at a constant rate. How many chicken wings can "
            f"{n} eat in {m2} minutes?", m1, rate * m1, m2, "wings")

def paint(r, n):
    y, red, b = r.randint(2, 8), r.randint(2, 8), r.randint(2, 12)
    need(y != red)
    color, per = r.choice((("yellow", y), ("red", red)))
    other = "red" if color == "yellow" else "yellow"
    return (f"{n} makes 1 batch of a favorite orange paint by mixing {y} liters of yellow paint and {red} liters of "
            f"red paint. How many batches can {n} make with {per * b} liters of {color} paint? ({n} has all the "
            f"{other} paint needed.)", per, 1, per * b, "batches")

def reading(r, n):
    pages, k1, k2 = r.randint(2, 9), *two(r, 2, 7)
    minutes = pages + r.randint(1, 4)
    return (f"{n} reads {pages * k1 * 10} pages in {minutes * k1 * 10} minutes. At this rate, how long will it take "
            f"{n} to read {pages * k2} pages?", pages * k1 * 10, minutes * k1 * 10, pages * k2, "minutes")

def editing(r, n):
    h, v, k = r.randint(2, 6), r.randint(2, 10), r.randint(2, 6)
    need(h != v)
    return (f"{n} spends {h} hours editing a {v}-minute video, working at a constant rate. How long will {n} spend "
            f"editing a {v * k}-minute video?", v, h, v * k, "hours")

def cherries(r, n):
    per, pies, k = r.randint(5, 9) * 10, r.randint(2, 5), r.randint(2, 5)
    return (f"According to {n}, perfect cherry pies have a ratio of {num(per * pies)} cherries to {pies} pies. How "
            f"many cherries does {n} need to make {pies * k} perfect cherry pies?", pies, per * pies, pies * k, "cherries")

STORIES = [dragons, camel, candle, touchdowns, snacks, points, wings, paint, reading, editing, cherries]

# Type 2: (intro, the items, their noun, "there are" or the verb)
LISTS = {
    "bikes": ("A bike shop has", ["red", "blue", "orange", "silver"], "bikes", "there are"),
    "fruit": ("A fruit basket holds", ["bananas", "oranges", "apples", "kiwis"], "", "there are"),
    "groomer": ("A pet groomer gave", ["baths", "nail trims", "brush-outs", "ear cleanings"], "", "the groomer gave"),
    "garden": ("{name}'s garden has", ["tomato", "pepper", "squash", "pumpkin"], "plants", "there are"),
}

def item(word, noun):
    return f"{word} {noun}".strip()

def complete(r):
    key = r.choice(list(LISTS))
    intro, words, noun, verb = LISTS[key]
    first, second = r.sample(words, 2)
    k = r.randint(2, 5)
    p, q = r.sample(range(2, 7), 2)                                 # plurals on both sides: "for every 2 apples"
    need(math.gcd(p, q) == 1)
    counts = {first: p * k, second: q * k}
    for w in words:
        if w not in counts:
            counts[w] = r.randint(2, 30)
    fits = [w for w in words if w != first and F(counts[w], counts[first]) == F(q, p)]
    need(fits == [second] and len(set(counts.values())) == 4)
    listed = ", ".join(f"{counts[w]} {item(w, noun)}" for w in words[:-1]) + f", and {counts[words[-1]]} {item(words[-1], noun)}"
    prompt = (f"{intro.format(name=r.choice(gen.NAMES))} {listed}. Complete the ratio: for every {p} "
              f"{item(first, noun)}, {verb} {q} ...")
    return dict(prompt=prompt, counts=counts, first=first, p=p, q=q, noun=noun, answer=item(second, noun))

def draw(entry, r, tpl):
    if entry == "2":
        return complete(r)
    prompt, a1, b1, a2, unit = STORIES[tpl](r, r.choice(gen.NAMES))
    b2 = F(b1) * a2 / F(a1)
    need(b2.denominator == 1 and a1 != a2)
    return dict(prompt=prompt, a1=str(a1), b1=str(b1), a2=str(a2), answer=f"{num(b2)} {unit}")

def check(p):
    try:
        if p["type"] == "1":
            got = F(re.match(r"[\d,.]+", p["answer"]).group(0).replace(",", ""))
            a1, b1, a2 = F(p["a1"]), F(p["b1"]), F(p["a2"])
            ok = got * a1 == b1 * a2 and all(num(x) in p["prompt"] for x in (a1, b1, a2))
            return "checked" if ok else "failed"
        c, first = p["counts"], p["first"]
        said = p["answer"].strip()
        fits = [w for w in c if w != first and F(c[w], c[first]) == F(p["q"], p["p"])]
        return "checked" if fits and [item(w, p["noun"]) for w in fits] == [said] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(STORIES) if e == "1" else 1)

def typst(p, gap="0.3em"):
    return p["prompt"].replace("$", "\\$")

def answer_typst(p):
    return p["answer"]

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
