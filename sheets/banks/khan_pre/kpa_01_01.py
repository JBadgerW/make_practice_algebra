"""Khan Prealgebra, Lesson 1-1: Factor pairs, from the old app's PreAlg_01_01
(twenty-two of Khan's, without answers).

Type 1: which of five pairs are factor pairs for n? Choose all that apply;
Khan's pairs go up by first factor (1 and 16, 2 and 8, 2 and 16, 3 and 6,
4 and 4), the wrong ones a near miss. Type 2: a rectangle's area; which of
four length-and-width pairs could it have? Type 3: complete a table of
factor pairs, a story's (32 marbles in bags: number of bags, marbles per
bag) or every factor pair of n, some cells left blank.

A problem: dict(type, n, ..., answer, source).
    Types 1, 2  pairs [[1, 16], [2, 8], [2, 16], [3, 6], [4, 4]], choices, answer "A, B, E"
    Type 3      story "marbles" or "", rows [[1, 32], [2, 16], [4, 8]], blanks [[0, 1], [1, 0], [2, 1]],
                answer "1 and 32, 2 and 16, 4 and 8"
check(): Types 1 and 2 multiply each pair; Type 3 reads the answer's pairs:
each a factor pair of n, agreeing with the cells shown, and for "all the
factor pairs" table, every pair there is.
"""
import re
from ... import gen
from ...gen import need
from . import courses
from .numbers import pairs

NAME = FAMILY = "kpa_01_01"
FIXED = False
TITLE = "Lesson 1-1: Factor pairs"
INSTRUCTIONS = ""
COURSES = courses(1)

TYPES = [
    dict(key="1", title="Which Are Factor Pairs?", instructions="Choose all answers that apply.",
         look="A number and five pairs of numbers.",
         move="A factor pair multiplies to the number. Multiply each pair and check.", width="full"),
    dict(key="2", title="A Rectangle's Sides", instructions="Choose all answers that apply.",
         look="A rectangle's area and four length-and-width pairs.",
         move="Area = length × width, so the sides are a factor pair of the area."),
    dict(key="3", title="Complete the Table", instructions="Use what you know about factor pairs to complete each table.",
         look="A table of factor pairs with some cells blank.",
         move="Each row multiplies to the number. Divide the number by the factor you have to find the other."),
]
T = gen.Types(TYPES, "", space="0.25in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

# story: (sentence, first column, second column)
STORIES = {
    "marbles": ("{name} has {n} marbles to put into bags, the same number in each bag, none left over.",
                "Number of bags", "Marbles per bag"),
    "cars": ("{name} is putting away {n} toy cars, every car in a bin, the same number in each bin.",
             "Number of bins", "Cars per bin"),
    "trip": ("{n} students are going on a field trip. Every student is in a group, and all the groups are the same size.",
             "Number of groups", "Students per group"),
    "seeds": ("{name} has {n} flower seeds to plant in pots, every seed planted, the same number in each pot.",
              "Number of pots", "Seeds per pot"),
    "unicorns": ("There are {n} unicorns at magic camp, every one in a field, the same number in each field.",
                 "Number of fields", "Unicorns per field"),
    "tag": ("A group of {n} friends is making teams to play tag, every player on a team, the same number on each team.",
            "Number of teams", "Players per team"),
}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["n"], str(p.get("pairs") or p.get("rows")), str(p.get("blanks")))

def near_miss(r, n, a):
    """A pair (a, b) with a b close to n but not n: Khan's 2 and 23 for 49."""
    b = n // a + r.choice((-1, 0, 1, 2))
    need(b >= a and a * b != n)
    return [a, b]

def choose_pairs(r, n, count):
    right = pairs(n)
    need(len(right) >= 2)
    k = r.randint(max(1, count - 3), min(len(right), count - 1))
    chosen = sorted(r.sample(right, k))
    firsts = {a for a, _ in chosen}
    wrong = []
    for a in r.sample(range(1, max(3, int(n ** 0.5) + 2)), min(max(3, int(n ** 0.5) + 2) - 1, 6)):
        if len(wrong) == count - k:
            break
        if n % a and a not in firsts or a in firsts and r.random() < 0.3:
            try:
                wrong.append(near_miss(r, n, a))
            except gen.Redraw:
                continue
    need(len(wrong) == count - k)
    allp = sorted([list(p) for p in chosen] + wrong)
    need(len({tuple(p) for p in allp}) == count)
    return allp

def draw(entry, r, tpl):
    if entry in "12":
        n = r.randint(8, 99) if entry == "1" else r.randint(6, 90)
        ps = choose_pairs(r, n, 5 if entry == "1" else 4)
        unit = "" if entry == "1" else " cm"
        choices = [f"${a}${unit} and ${b}${unit}" for a, b in ps]
        right = [c for c, (a, b) in zip(choices, ps) if a * b == n]
        choices, answer = gen.in_order(choices, right)
        return dict(n=n, pairs=ps, choices=choices, answer=answer)
    story = r.choice(list(STORIES) + ["", ""])
    n = r.randint(12, 99)
    rows = [list(p) for p in pairs(n)]
    need(3 <= len(rows) <= 6)
    if story:                                                     # Khan's story tables show the first few
        rows = rows[:r.randint(3, len(rows))]
    blanks = [[i, r.randint(0, 1)] for i in range(len(rows)) if r.random() < 0.7]
    need(len(blanks) >= 2)
    return dict(n=n, story=story, name=r.choice(gen.NAMES), rows=rows, blanks=blanks,
                answer=", ".join(f"{a} and {b}" for a, b in rows))

PAIR = re.compile(r"(\d+)\s*(?:and|×|x|\*)\s*(\d+)")

def check(p):
    try:
        n = p["n"]
        if p["type"] in "12":
            right = [gen.ABC[i] for i, (a, b) in enumerate(p["pairs"]) if a * b == n]
            return "checked" if right == gen.letters_of(p["answer"]) else "failed"
        got = [tuple(map(int, m)) for m in PAIR.findall(p["answer"])]
        blank = {tuple(b) for b in p["blanks"]}
        ok = (len(got) == len(p["rows"]) and all(a * b == n for a, b in got) and len(set(got)) == len(got)
              and all(got[i][j] == p["rows"][i][j] for i in range(len(got)) for j in (0, 1) if (i, j) not in blank))
        if not p["story"]:
            ok = ok and len(got) == len(pairs(n))
        return "checked" if ok else "failed"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: 1)

def table(p, filled=False):
    blank = {tuple(b) for b in p["blanks"]}
    cell = lambda i, j: (f"*{p['rows'][i][j]}*" if filled else "") if (i, j) in blank else str(p["rows"][i][j])
    if p["story"]:
        _, first, second = STORIES[p["story"]]
        head = f"[*{first}*], [*{second}*]"
        body = ", ".join(f"[{cell(i, 0)}], [{cell(i, 1)}]" for i in range(len(p["rows"])))
        cols = 2
    else:
        head = "[*First factor*], [], [*Second factor*]"
        body = ", ".join(f"[{cell(i, 0)}], [and], [{cell(i, 1)}]" for i in range(len(p["rows"])))
        cols = 3
    return (f"#table(columns: {cols}, inset: 5pt, align: center, fill: (_, row) => if row == 0 {{ luma(230) }}, "
            f"{head}, {body})")

def typst(p, gap="0.3em"):
    n = p["n"]
    if p["type"] == "1":
        return f"Which of the following are factor pairs for ${n}$? \\\n    {gen.choices_typst(p['choices'], 'linear')}"
    if p["type"] == "2":
        return (f"A rectangle has an area of ${n}$ square centimeters. Which of the following could be the rectangle's "
                f"length and width? \\\n    {gen.choices_typst(p['choices'], 'grid')}")
    if p["story"]:
        intro = STORIES[p["story"]][0].format(name=p["name"], n=n)
        return f"{intro} \\\n    {table(p)}"
    return f"Complete the table to find all the factor pairs of ${n}$. \\\n    {table(p)}"

def answer_typst(p):
    return gen.choice_answer_typst(p) if p["type"] in "12" else table(p, filled=True)

def text(p):
    if p["type"] in "12":
        return f"{p['n']}: " + gen.choices_text([c.replace("$", "") for c in p["choices"]])
    blank = {tuple(b) for b in p["blanks"]}
    return f"{p['n']}: " + ", ".join(" × ".join("__" if (i, j) in blank else str(v) for j, v in enumerate(row))
                                    for i, row in enumerate(p["rows"]))

def answer_text(p):
    return gen.choice_answer_typst(p).replace("$", "") if p["type"] in "12" else p["answer"]

def height(p):
    return {"1": 0.6, "2": 1.0}.get(p["type"], 0.6 + 0.3 * len(p.get("rows", [])))

def edit_text(p):
    return str(p["n"])

def from_edit(t, old):
    raise ValueError("reroll for a new number; you can edit the answer")

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    if p["type"] in "12":
        return gen.with_letters(p, t, check)
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
