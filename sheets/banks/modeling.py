"""Modeling compound inequalities with word problems: a total that must stay
between two numbers, made of a fixed part plus some count of a smaller item.

    low <= (amount)(each fixed unit) + (each item)(count) <= high

Every situation is the same model; only the story changes, so students set
the inequality up rather than recognize a story. The types differ only in the
amount of the fixed part:
    Type 1   one unit (1 serving, 1 hour, 1 mile, 1 bottle)
    Type 2   a whole number of units (2, 3, 4)
    Type 3   halves: 1/2, 1 1/2, 2, 2 1/2

An entry is a type and a story: "1a" is Type 1 about a dog's diet. Versions
redraw the same entry, so they are parallel: same story, new numbers.

Problems are built backward from the answer: pick the fewest and the most
items, then the bounds. check() reads the numbers back out of the prompt's
text, finds every whole-number count that fits by trying them, and compares
that and the solved inequality with the key, and solves the key's model.

A problem: dict(type, story, prompt, answer, source).
    prompt  the word problem as plain text; fractions as "1 1/2" or "1/2"
    answer  "model; solved": "510 <= 1.5(320) + 15t <= 540; 2 <= t <= 4"
"""
import math, random, re
from fractions import Fraction
import sympy as sp

NAME = FAMILY = "modeling"
FIXED = False
TITLE = "Lesson 1-6: Compound Inequalities"
INSTRUCTIONS = ("Write a compound inequality that models each situation. "
                "Solve it, then answer the question.")
COURSES = ["Algebra 1"]

TYPES = [
    dict(key="1", title="One Serving",
         look="A total between two numbers: one serving (or hour, mile, bottle) of something, plus some number of a smaller item.",
         move="Let a letter be the number of items. Write low ≤ fixed part + (each item)·n ≤ high. Subtract the fixed part from all three parts, then divide all three by the size of one item."),
    dict(key="2", title="Whole-Number Servings",
         look="The same model, but the fixed part comes in 2, 3, or 4 servings.",
         move="The fixed part is servings times the amount in one serving. Write it as 2(320) in the model, then solve as before."),
    dict(key="3", title="Fractional Servings",
         look="The same model, with ½, 1½, or 2½ servings.",
         move="The fixed part is still servings times the amount in one: 1½ servings of 320 is 1.5(320) = 480. Then solve as before."),
]
TYPE = {t["key"]: t for t in TYPES}
KEYS = [t["key"] for t in TYPES]
AMOUNTS = {"1": [Fraction(1)],
           "2": None,                                    # the story's own whole numbers
           "3": [Fraction(1, 2), Fraction(3, 2), Fraction(2), Fraction(5, 2)]}

NAMES = ["Enrique", "Maya", "Darnell", "Priya", "Tomás", "Grace", "Kenji", "Amara", "Luis", "Hannah",
         "Mateo", "Aaliyah", "Owen", "Sofia", "Isaiah", "Mei", "Caleb", "Fatima", "Noah", "Lucia"]
PETS = ["River", "Biscuit", "Scout", "Maple", "Rocket", "Juniper", "Bear", "Pepper", "Ziggy", "Hazel"]

# A story: its text, with {L} {U} the bounds, {n} the fixed amount with its
# unit, {B} one unit's size, {s} one item's size; who and pet are names.
# B, s, and the fewest items (lo) are drawn from their lists; the most is lo + gap.
# Both bounds are multiples of round, and whole is Type 2's amounts.
STORIES = [
    dict(key="a", title="Dog food and treats", var="t", item=("treat", "treats"), unit=("serving", "servings"),
         B=range(280, 401, 20), s=(10, 15, 20, 25), lo=range(1, 7), gap=range(2, 6), round=10, whole=(2, 3),
         text="{who} is planning a diet for a dog named {pet}. {pet} should get between {L} and {U} "
              "Calories each day. {pet} eats {n} of dog food each day, and the rest of the Calories come "
              "from treats. A serving of dog food has {B} Calories, and a treat has {s} Calories. "
              "How many treats can {pet} have each day?"),
    dict(key="b", title="Party budget", var="g", item=("guest", "guests"), unit=("hour", "hours"),
         B=(30, 40, 50, 60, 70, 80), s=(6, 8, 9, 10, 12, 15), lo=range(8, 17), gap=range(4, 11), round=5,
         whole=(2, 3, 4),
         text="{who} wants to spend between ${L} and ${U} on a birthday party at the park. Renting a "
              "picnic pavilion costs ${B} per hour, and {who} will rent it for {n}. Food for each guest "
              "costs ${s}. How many guests can {who} invite?"),
    dict(key="c", title="Workout time", var="c", item=("circuit", "circuits"), unit=("mile", "miles"),
         B=(8, 9, 10, 11, 12), s=(3, 4, 5, 6), lo=range(2, 7), gap=range(2, 5), round=1, whole=(2, 3, 4),
         text="{who} is planning a workout that will last between {L} and {U} minutes. {who} will start "
              "by running {n} at a pace of {B} minutes per mile. Then {who} will finish with exercise "
              "circuits that take {s} minutes each. How many circuits can {who} do?"),
    dict(key="d", title="Punch recipe", var="c", item=("can", "cans"), unit=("bottle", "bottles"),
         B=(32, 48, 64), s=(8, 12), lo=range(2, 9), gap=range(2, 6), round=4, whole=(2, 3),
         text="{who} is making punch for a class party and wants to make between {L} and {U} fluid "
              "ounces. The recipe uses {n} of fruit juice, and each bottle holds {B} fluid ounces. The "
              "rest of the punch is sparkling water from {s}-ounce cans. How many cans should {who} use?"),
]
STORY = {s["key"]: s for s in STORIES}

WIDTH, SPACE = "full", "1.75in"
ENTRIES = [dict(key=k + s["key"], type=k, kind="numbers", title=s["title"], width=WIDTH, space=SPACE)
           for k in KEYS for s in STORIES]
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

def hint(typ):
    t = TYPE[typ]
    return label(t), t["title"], t["look"], t["move"]

def special(typ):
    return False

def initial_seen():
    return set()

def seen_key(p):
    return ("modeling", p["story"], numbers_key(p["prompt"], p["story"]))

def numbers_key(prompt, story):
    """The numbers a prompt uses, so a new name alone doesn't make a new problem."""
    try:
        return tuple(str(v) for v in read_prompt(prompt, story))
    except ValueError:
        return prompt

# ------------------------------------------------------------------
# Writing numbers
# ------------------------------------------------------------------
def mixed(q):
    """Fraction(3, 2) -> "1 1/2", Fraction(1, 2) -> "1/2", Fraction(2) -> "2"."""
    w, r = divmod(q.numerator, q.denominator)
    if not r:
        return str(w)
    return f"{w} {r}/{q.denominator}" if w else f"{r}/{q.denominator}"

def decimal(q):
    """Fraction(3, 2) -> "1.5"; only for fractions that end (here, halves)."""
    if q.denominator == 1:
        return str(q.numerator)
    s = f"{float(q):.6f}".rstrip("0").rstrip(".")
    assert Fraction(s) == q, q
    return s

def bound(q):
    """A solved bound: whole, a decimal that ends, or a fraction."""
    try:
        return decimal(q) if q.denominator in (1, 2, 4, 5, 8, 10) else f"{q.numerator}/{q.denominator}"
    except AssertionError:
        return f"{q.numerator}/{q.denominator}"

def commas(n):
    return f"{n:,}"

def amount(n, unit):
    return f"{mixed(n)} {unit[0] if n <= 1 else unit[1]}"

def fill(text, **v):
    return re.sub(r"\{(\w+)\}", lambda m: str(v[m.group(1)]), text)

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
class Redraw(Exception):
    pass

def need(ok):
    if not ok:
        raise Redraw

def draw(entry, r):
    typ, st = ENTRY[entry]["type"], STORY[entry[-1]]
    n = r.choice(AMOUNTS[typ] or [Fraction(k) for k in st["whole"]])
    B, s = r.choice(st["B"]), r.choice(st["s"])
    lo = r.choice(st["lo"])
    hi = lo + r.choice(st["gap"])
    fixed = n * B
    need(fixed.denominator == 1)
    L, U = int(fixed) + s * lo, int(fixed) + s * hi
    need(L % st["round"] == 0 and U % st["round"] == 0)
    prompt = fill(st["text"], who=r.choice(NAMES), pet=r.choice(PETS), L=commas(L), U=commas(U),
                  n=amount(n, st["unit"]), B=B, s=s)
    return dict(type=typ, story=st["key"], prompt=prompt, answer=answer_for(st, L, U, n, B, s),
                source="template")

def answer_for(st, L, U, n, B, s):
    """The key's model and solved inequality, from the numbers as the prompt states them."""
    v = st["var"]
    fixed = str(B) if n == 1 else f"{decimal(n)}({B})"
    lo, hi = (Fraction(L) - n * B) / s, (Fraction(U) - n * B) / s
    return f"{L} <= {fixed} + {s}{v} <= {U}; {bound(lo)} <= {v} <= {bound(hi)}"

def generate(entry, rng, seen, tries=400):
    for _ in range(tries):
        try:
            p = draw(entry, rng)
        except Redraw:
            continue
        if seen_key(p) in seen:
            continue
        if check(p) != "checked":                    # the independent check must agree with the build
            raise AssertionError(f"modeling {entry}: {p}")
        seen.add(seen_key(p))
        return p
    raise RuntimeError(f"could not draw a modeling {entry} problem; check its story")

# ------------------------------------------------------------------
# Checking: read the numbers back out of the prompt, count the items that
# fit by trying every whole number, and solve the key's model with sympy
# ------------------------------------------------------------------
NUM = r"(\d[\d,]*)"
AMT = r"(\d+ \d+/\d+|\d+/\d+|\d+)"

def pattern(st):
    """The story's text as a regex: the names match any name, the numbers are read."""
    out, groups = "", []
    for piece in re.split(r"(\{\w+\})", st["text"]):
        m = re.fullmatch(r"\{(\w+)\}", piece)
        if not m:
            out += re.escape(piece)
        elif m.group(1) in ("who", "pet"):
            out += r"[^\s.,]+(?: [^\s.,]+)?"
        elif m.group(1) == "n":
            out += AMT + rf" (?:{st['unit'][0]}|{st['unit'][1]})"
            groups.append("n")
        else:
            out += NUM
            groups.append(m.group(1))
    return re.compile(out), groups

PATTERN = {k: pattern(st) for k, st in STORY.items()}

def read_prompt(prompt, story):
    """(L, U, n, B, s) as Fractions; ValueError if the prompt isn't its story's text."""
    rx, groups = PATTERN[story]
    m = rx.fullmatch(" ".join(prompt.split()))
    if not m:
        raise ValueError(f"keep the wording of the story; change only names and numbers")
    v = {}
    for name, g in zip(groups, m.groups()):
        q = sum(Fraction(x) for x in g.replace(",", "").split()) if name == "n" else Fraction(g.replace(",", ""))
        if name in v and v[name] != q:
            raise ValueError(f"{name} is written two ways")
        v[name] = q
    if v["s"] <= 0 or v["B"] <= 0 or v["n"] <= 0 or v["L"] > v["U"]:
        raise ValueError("sizes must be positive, and the low bound comes first")
    return v["L"], v["U"], v["n"], v["B"], v["s"]

REL = re.compile(r"\s*(?:<=|≤)\s*")

def normal(text):
    return text.replace("−", "-").replace("·", "*")

def read_answer(answer, var):
    """"model; solved" -> (model's bounds on var, solved bounds), each (lo, hi) Fractions."""
    from ..check import to_sympy
    model, _, solved = normal(answer).partition(";")
    v = sp.Symbol(var)
    out = []
    for part in (model, solved):
        bits = REL.split(part.strip())
        if len(bits) != 3:
            raise ValueError("write each as low <= ... <= high")
        lo, mid, hi = (sp.nsimplify(to_sympy(b), rational=True) for b in bits)
        if lo.free_symbols or hi.free_symbols or mid.free_symbols != {v}:
            raise ValueError(f"use only {var}, in the middle")
        if not sp.Poly(mid, v).degree() == 1:
            raise ValueError("the model should be linear")
        a, c = sp.Poly(mid, v).all_coeffs()             # a wrong sign gives bounds that won't match
        out.append(tuple(Fraction(str((x - c) / a)) for x in (lo, hi)))
    return out

def counts(L, U, n, B, s):
    """Every whole number of items that keeps the total between L and U, by trying them."""
    return [k for k in range(0, math.floor(U / s) + 1) if L <= n * B + s * k <= U]

def check(p):
    st = STORY.get(p.get("story"))
    try:
        L, U, n, B, s = read_prompt(p["prompt"], st["key"])
        model, solved = read_answer(p["answer"], st["var"])
    except (ValueError, KeyError, TypeError, AttributeError, sp.SympifyError, SyntaxError):
        return "unchecked"
    ks = counts(L, U, n, B, s)
    exact = ((L - n * B) / s, (U - n * B) / s)
    ok = (model == exact and solved == exact and ks
          and ks == list(range(max(0, math.ceil(exact[0])), math.floor(exact[1]) + 1)))
    return "checked" if ok else "failed"

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
FRAC = re.compile(r"\b(?:(\d+) )?(\d+)/(\d+)\b")

def typst(p, gap="0.3em"):
    from ..typst import esc
    return FRAC.sub(lambda m: f"${m.group(1) + ' ' if m.group(1) else ''}{m.group(2)}/{m.group(3)}$",
                    esc(p["prompt"]))

def sentence(p):
    """The answer to the question: "2 to 4 treats"."""
    st = STORY[p["story"]]
    try:
        ks = counts(*read_prompt(p["prompt"], st["key"]))
    except ValueError:
        return ""
    noun = lambda k: st["item"][0] if k == 1 else st["item"][1]
    if not ks:
        return f"no number of {st['item'][1]} works"
    if len(ks) == 1:
        return f"exactly {ks[0]} {noun(ks[0])}"
    return f"{ks[0]} to {ks[-1]} {noun(ks[-1])}"

def answer_typst(p):
    model, _, solved = p["answer"].partition(";")
    s = sentence(p)
    return f"${model.strip()}$ \\ ${solved.strip()}$" + (f" \\ {s}" if s else "")

def pretty(s):
    s = s.replace("<=", "≤").replace(" - ", " − ")
    return FRAC.sub(lambda m: (m.group(1) or "") + {"1/2": "½"}.get(f"{m.group(2)}/{m.group(3)}",
                                                                    f" {m.group(2)}/{m.group(3)}"), s)

def text(p):
    return pretty(p["prompt"])

def answer_text(p):
    model, _, solved = p["answer"].partition(";")
    return f"{pretty(model.strip())}  →  {pretty(solved.strip())}  ({sentence(p)})"

def height(p):
    """Inches the prompt takes on the page, for page estimates."""
    return 0.75

# ------------------------------------------------------------------
# Hand editing: the prompt, in the story's own words with new names or numbers
# ------------------------------------------------------------------
def edit_text(p):
    return p["prompt"]

def from_edit(text, old):
    t = " ".join(text.split())
    st = STORY[old["story"]]
    L, U, n, B, s = read_prompt(t, st["key"])
    if L.denominator > 1 or U.denominator > 1 or (n * B).denominator > 1:
        raise ValueError("the bounds and the fixed part must be whole numbers")
    new = dict(old, prompt=t, answer=answer_for(st, int(L), int(U), n, int(B), int(s)), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, text):
    if ";" not in text:
        raise ValueError("write the model, then ;, then the solved inequality")
    new = dict(p, answer=" ".join(text.split()))
    return new, check(new)

def selftest(n, seed):
    rng = random.Random(seed)
    for e in ENTRIES:
        seen = set()
        for i in range(n):
            if i % 100 == 0:                         # a story's pool can be under 200
                seen = set()
            generate(e["key"], rng, seen)
        print(f"modeling {e['key']:3} {e['title']:22} {n} drawn, all verified")
    return True
