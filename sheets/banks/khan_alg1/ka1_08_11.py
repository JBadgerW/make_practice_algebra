"""Khan Algebra 1, Lesson 8-11: Function domain word problems, from the old
app's Alg1_08_11 (ten of Khan's, without answers).

Which number type is more appropriate for the domain: integers or real
numbers? Khan's ten stories, retold with names and no pronouns and drawn
with new numbers: time, height, distance, weight, and temperature are real
numbers; house numbers, seasons, dice sums, ladder steps, and month numbers
are integers. The other two choices are Khan's: intervals made from other
numbers in the story (the outputs' range, say), never the domain itself.
Integers and Real numbers are spread evenly over a sheet.

The answer is a judgment about the story, so this check is weaker than
most: it requires the key to be the story's number type, so a key edited
out of step is caught.

A problem: dict(type, story, prompt, choices, answer, source).
"""
from ... import gen
from ...gen import need
from ...typst import esc
from . import courses

NAME = FAMILY = "ka1_08_11"
FIXED = False
TITLE = "Lesson 8-11: Function domain word problems"
INSTRUCTIONS = "Which number type is more appropriate for each function's domain?"
COURSES = courses(8)
INTEGERS, REALS = "Integers", "Real numbers"

TYPES = [
    dict(key="1", title="Integers or Real Numbers?",
         look="A story, and a function whose input is a count, a label, or a measurement.",
         move="Can the input take any value in between, like a time or a length? Real numbers. Only whole steps, "
              "like a house number or a month? Integers.", width="full"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def plant(r):
    a, b, c = r.randint(2, 6), r.randint(60, 120), r.randint(20, 40)
    return (f"{{name}}'s plant began sprouting {a} days before {{name}} bought it, and {{name}} kept it {b} days, until "
            f"it died. At its tallest, it was {c} centimeters tall. h(t) models the plant's height (in centimeters) t "
            f"days after {{name}} bought it.", "h", REALS, (f"0 <= t <= {c}", f"0 <= t <= {a + b}"))

def walk(r):
    m, k = r.randint(12, 30), r.randint(10, 25) / 10
    return (f"{{name}} walked {m} minutes from home to a friend's house {k} kilometers away. d(t) models the "
            f"distance left to walk (in kilometers) t minutes after {{name}} left home.", "d", REALS,
            (f"{k} <= t <= {m}", f"0 <= t <= {k}"))

def houses(r):
    n = r.randint(40, 120)
    return (f"The house numbers on a street go from 1 to {n}. B(n) models the type of building at number n: 0 for "
            f"a home, 1 for a store, 2 for a government building, and 3 for anything else.", "B", INTEGERS,
            ("0 <= n <= 3", f"3 <= n <= {n}"))

def homeruns(r):
    lo, hi = r.randint(45, 55), r.randint(60, 73)
    return (f"H(y) models the most home runs any National League player hit in season y, from 2000 to 2010. "
            f"The most in a season was {hi}, the fewest {lo}.", "H", INTEGERS, (f"{lo} <= y <= {hi}", "0 <= y <= 10"))

def egg(r):
    low, high = r.randint(190, 200), r.randint(205, 215)
    return (f"How long an egg takes to boil depends on the altitude. At the edge of the Dead Sea (-418 meters) it "
            f"takes {low} seconds; on top of Mount Everest (8848 meters), {high} seconds. T(a) models the time (in "
            f"seconds) at an altitude of a meters.", "T", REALS, (f"{low} <= a <= {high}", f"{low} <= a <= 8848"))

def spice(r):
    low, high = r.randint(4, 8), r.randint(1500, 2500)
    return (f"{{name}} sells any amount of cumin seeds from 1 kilogram to 1000 kilograms, charging ${low} for 1 "
            f"kilogram and ${high} for 1000 kilograms. p(w) models the price (in dollars) of w kilograms.", "p", REALS,
            (f"1 <= w <= {high}", f"{low} <= w <= 1000"))

def dice(r):
    return ("{name} rolls a pair of 6-sided dice. P(n) models the probability that the dice add up to n.", "P",
            INTEGERS, ("1/36 <= n <= 6/36", "0 <= n <= 36"))

def climate(r):
    lo, hi = r.randint(-10, -2), r.randint(25, 35)
    up, down = r.randint(5, 15), r.randint(10, 25)
    return (f"{{name}} studies climate and heart disease. H(t) models how much more (or less) likely heart disease "
            f"is than average, in percent, where the temperature is t degrees Celsius. The model runs from {lo} "
            f"degrees, where it is {up}% above average, to {hi} degrees, where it is {down}% below.", "H", REALS,
            (f"-{down} <= t <= {up}", f"{up} <= t <= {hi}"))

def ladder(r):
    on, steps, gap = r.randint(3, 7), r.randint(12, 20), r.choice((0.25, 0.5))
    return (f"{{name}} stands on step {on} of a ladder with {steps} steps, {gap} meters apart. h(n) models the height "
            f"of {{name}}'s feet above the ground (in meters) after moving n steps (n is negative going down).", "h",
            INTEGERS, (f"{-on * gap} <= n <= {on}", f"0 <= n <= {steps * gap}"))

def rainfall(r):
    lo, hi = r.randint(100, 150), r.randint(160, 200)
    return (f"r(m) models the average rainfall (in millimeters) in Tanzania in month number m, for the years 1900 "
            f"to 2009. The wettest month averages {hi} mm, the driest {lo} mm.", "r", INTEGERS,
            (f"{lo} <= m <= {hi}", "1900 <= m <= 2009"))

STORIES = {"plant": plant, "walk": walk, "houses": houses, "homeruns": homeruns, "egg": egg, "spice": spice,
           "dice": dice, "climate": climate, "ladder": ladder, "rainfall": rainfall}
TYPE_OF = {"plant": REALS, "walk": REALS, "egg": REALS, "spice": REALS, "climate": REALS,
           "houses": INTEGERS, "homeruns": INTEGERS, "dice": INTEGERS, "ladder": INTEGERS, "rainfall": INTEGERS}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], p["answer"])

def draw(entry, r, tpl, want=None):
    kind = {"A": INTEGERS, "B": REALS}[want] if want else r.choice((INTEGERS, REALS))
    story = r.choice([s for s in STORIES if TYPE_OF[s] == kind])
    text, f, right, intervals = STORIES[story](r)
    prompt = text.replace("{name}", r.choice(gen.NAMES)) + \
        f" Which number type is more appropriate for the domain of {f}?"
    choices = [INTEGERS, REALS, *intervals]
    return dict(story=story, prompt=prompt, choices=choices, answer=gen.ABC[choices.index(right)])

def check(p):
    try:
        return "checked" if gen.chosen(p) == [TYPE_OF[p["story"]]] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1,
                         balance=("AB", lambda k: k[2] if k[0] == NAME and len(k) == 3 else None))

def math(c):
    return c if c in (INTEGERS, REALS) else f"${c}$"

def typst(p, gap="0.3em"):
    return f"{esc(p['prompt'])} \\\n    {gen.choices_typst([math(c) for c in p['choices']], 'grid')}"

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    return p["prompt"] + "   " + gen.choices_text(p["choices"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 1.4

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    new = dict(old, prompt=" ".join(t.split()), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
