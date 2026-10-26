"""Khan Algebra 1, Lesson 8-13: Recognize functions from tables, from the old
app's Alg1_08_13 (eighteen of Khan's, without answers).

Can the second column be represented as a function of the first? Khan's
contexts, with numbers (planned and actual attendance, fuel and distance)
or with words (main course and side dish, hats and flowers). A table that
isn't a function repeats an input with a different output; a third of the
tables that are repeat an input with the same output, Khan's trap. Yes and
No are spread evenly over a sheet.

A problem: dict(type, context, rows, prompt, choices, answer, source).
    rows     [["150", "130"], ["220", "200"], ...]   (input, output)
    choices  ["Yes", "No"]
check() reads the rows: a function unless some input has two different outputs.
"""
from ... import gen
from ...gen import need
from ...typst import esc
from . import courses

NAME = FAMILY = "ka1_08_13"
FIXED = False
TITLE = "Lesson 8-13: Recognize functions from tables"
INSTRUCTIONS = "Answer each question."
COURSES = courses(8)
CHOICES = ["Yes", "No"]

TYPES = [
    dict(key="1", title="Numbers",
         look="A table of two quantities.",
         move="Look for an input that appears twice. If it has two different outputs, it isn't a function; "
              "the same output twice is fine."),
    dict(key="2", title="Words",
         look="A table pairing things: a main course and a side dish, a hat and a flower.",
         move="The same test: an input listed twice with different outputs means it isn't a function."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

# (key, story, input, output, question, input numbers, output numbers)
NUMBERS = [
    ("attendance", "{name} is an event promoter. The table compares the number of people who said they would attend "
     "and the number who did, for the last few events.", "Planned attendance", "Actual attendance",
     "the actual attendance", "the planned attendance", (100, 400, 10), (80, 380, 10)),
    ("fuel", "The table compares the fuel in {name}'s car at the start of several trips and the distance driven.",
     "Fuel (liters)", "Distance (kilometers)", "the distance", "the fuel", (20, 50, 5), (60, 200, 10)),
    ("heights", "The table compares the heights and weights of {name}'s friends.", "Height (centimeters)",
     "Weight (kilograms)", "weight", "height", (150, 185, 1), (45, 85, 1)),
    ("park", "The table compares the daily average temperature in a park and the number of people who visited "
     "that day.", "Temperature (degrees Celsius)", "Visitors", "the number of visitors", "the temperature",
     (8, 30, 1), (5, 60, 1)),
    ("homework", "The table compares the number of homework questions {name} assigned and the number of students "
     "who finished, on several days.", "Questions", "Students who finished", "the number of students who finished",
     "the number of questions", (4, 20, 1), (15, 32, 1)),
    ("bus", "The table compares the time {name} got on the bus to school (minutes after 8 am) and how long the "
     "ride took, on several days.", "Time (minutes after 8 am)", "Ride (minutes)", "the length of the ride",
     "the time {name} got on", (10, 40, 1), (25, 50, 1)),
    ("songs", "The table compares the number of songs and the number of videos {name}'s friends keep on their "
     "phones.", "Songs", "Videos", "the number of videos", "the number of songs", (50, 400, 1), (5, 150, 1)),
]
WORDS = [
    ("dinner", "The table compares the main course and the side dish each person in {name}'s family ordered at a "
     "restaurant.", "Main course", "Side dish", "the side dish", "the main course",
     ["Pasta", "Fish", "Burger", "Chicken", "Tacos", "Steak", "Curry"], ["Salad", "Rice", "Fries", "Soup", "Beans", "Bread"]),
    ("hats", "The table compares the hat each customer in a flower shop wore and the flowers each bought.",
     "Hat", "Flowers", "the flowers", "the hat",
     ["Beret", "Panama", "Cloche", "Bowler", "Fedora", "Cap"], ["Daffodils", "Sunflowers", "Violets", "Irises", "Tulips"]),
    ("shoes", "The table compares the shoes each customer in an ice cream shop wore and the flavor each picked.",
     "Shoes", "Flavor", "the flavor", "the shoes",
     ["Boots", "Loafers", "Sandals", "Sneakers", "Slippers", "Clogs"], ["Strawberry", "Vanilla", "Chocolate", "Mint", "Banana"]),
    ("hobbies", "A group of teachers listed their hobbies by the subject each teaches.", "Subject", "Hobby",
     "a teacher's hobby", "the subject", ["English", "History", "Math", "Gym", "Art", "Music"],
     ["Surfing", "Cards", "Climbing", "Chess", "Hiking", "Baking"]),
    ("students", "The table lists students at an international summer school and the countries they come from.",
     "Name", "Country", "the country", "the name", list(gen.NAMES[:10]),
     ["USA", "Nigeria", "India", "Mexico", "Japan", "Brazil", "Kenya"]),
]
CONTEXT = {c[0]: c for c in NUMBERS + WORDS}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["prompt"], tuple(map(tuple, p["rows"])), p["answer"])

def is_function(rows):
    out = {}
    for x, y in rows:
        if out.setdefault(x, y) != y:
            return False
    return True

def draw(entry, r, tpl, want=None):
    ctx = (NUMBERS if entry == "1" else WORDS)[tpl]
    key, story, xh, yh, y_words, x_words, xs, ys = ctx
    name = r.choice(gen.NAMES)
    n = r.randint(5, 6)
    if entry == "1":
        xpool = list(range(*xs)) if len(xs) == 3 else xs
        inputs = [str(x) for x in r.sample(xpool, n - 1)]
        out = lambda: str(r.randrange(*ys))
    else:
        inputs = r.sample(xs, n - 1)
        out = lambda: r.choice(ys)
    rows = [[x, out()] for x in inputs]
    yes = (want or r.choice("AB")) == "A"
    dup = r.choice(rows)
    if yes and r.random() < 0.35:                 # the same input, the same output: still a function
        rows.append(list(dup))
    elif yes:
        rows.append([str(r.choice([x for x in (range(*xs) if entry == "1" else xs) if str(x) not in inputs])), out()])
    else:
        other = out()
        need(other != dup[1])
        rows.append([dup[0], other])
    r.shuffle(rows)
    need(is_function(rows) == yes)
    prompt = gen.fill(f"{story} Can {y_words} be represented as a function of {x_words}?", name=name)
    choices, answer = gen.in_order(CHOICES, "Yes" if yes else "No")
    return dict(context=key, rows=rows, prompt=prompt, choices=choices, answer=answer)

def check(p):
    try:
        return "checked" if gen.chosen(p) == ["Yes" if is_function(p["rows"]) else "No"] else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(NUMBERS if e == "1" else WORDS),
                         balance=("AB", lambda k: k[3] if k[0] == NAME and len(k) == 4 else None))

def typst(p, gap="0.3em"):
    _, _, xh, yh, *_ = CONTEXT[p["context"]]
    cells = ", ".join(f"[{esc(x)}], [{esc(y)}]" for x, y in p["rows"])
    return (f"{esc(p['prompt'])} \\\n    #table(columns: 2, inset: 5pt, align: center, fill: (_, row) => "
            f"if row == 0 {{ luma(230) }}, [*{esc(xh)}*], [*{esc(yh)}*], {cells}) \\\n    "
            f"{gen.choices_typst(p['choices'], 'linear')}")

def answer_typst(p):
    return gen.choice_answer_typst(p)

def text(p):
    return p["prompt"] + "   " + "; ".join(f"{x} → {y}" for x, y in p["rows"])

def answer_text(p):
    return gen.choice_answer_typst(p)

def height(p):
    return 2.0

def edit_text(p):
    return "; ".join(f"{x}, {y}" for x, y in p["rows"])

def from_edit(t, old):
    rows = [[c.strip() for c in row.split(",")] for row in t.split(";") if row.strip()]
    if not rows or any(len(row) != 2 for row in rows):
        raise ValueError("write the rows as input, output; input, output; ...")
    new = dict(old, rows=rows, answer=gen.in_order(CHOICES, "Yes" if is_function(rows) else "No")[1], source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    return gen.with_letters(p, t, check)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
