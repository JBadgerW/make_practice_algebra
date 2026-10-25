"""Mixture problems (Advanced Math), from the old app's set AdvMath_18_05
(its twelve contexts) and the 2025-26 midterm (adding water).

The old set picked the percents and the total, then rounded the amounts, so
its answers didn't quite make the target percent. Here the amounts come
first, on a grid of whole numbers, and the target percent is drawn only
when it comes out whole: every answer is exact.

    Type 1   both amounts, given the total
    Type 2   one amount, given the total
    Type 3   one amount, given the other
    Type 4   water or a pure ingredient added, or water boiled off

A problem: dict(type, story, prompt, answer, source); prompt and answer are
words. check() reads the numbers back out of the story, solves the mixture
equation with exact fractions, and compares with the answer's numbers.
"""
from fractions import Fraction as F
from .. import gen
from ..gen import need

NAME = FAMILY = "adv_mixtures"
FIXED = False
TITLE = "Mixture Problems"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Both Amounts, Given the Total",
         look="Two solutions of different strengths, the total wanted, and its strength.",
         move="Let x be one amount; the other is total - x. The ingredient adds up: "
              "(low %)x + (high %)(total - x) = (target %)(total). Solve, then find the other."),
    dict(key="2", title="One Amount, Given the Total",
         look="The same, but only one of the amounts is asked for.",
         move="Set it up as in Type 1, with x the amount asked for."),
    dict(key="3", title="One Amount, Given the Other",
         look="One amount is known; the total isn't.",
         move="Let x be the unknown amount. (low %)(low amount) + (high %)(high amount) = "
              "(target %)(low amount + high amount). Solve for x."),
    dict(key="4", title="Water or a Pure Ingredient",
         look="Water added, water boiled off, or a pure (100%) ingredient added.",
         move="Water is 0% of the ingredient and a pure ingredient is 100%. Boiling off water takes it away. "
              "The ingredient before equals the ingredient after."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.75in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

INGREDIENTS = [("liters", "acid"), ("liters", "alcohol"), ("mL", "salt"), ("gallons", "antifreeze"),
               ("mL", "iodine"), ("ounces", "vinegar")]

# Each story: its words, the answer's, what the problem gives, and how its
# numbers are drawn: pct = (step, low, high) for the two percents; amt = (step,
# most) for the two amounts; cap = the largest target percent.
STORIES = {
    "1": [
        dict(key="a", words=True,              # 18_05 no. 1
             text="To get {T} {unit} of a mixture that was {tp}% {ing}, it was necessary to mix a quantity of "
                  "{lp}% {ing} solution with a quantity of {hp}% {ing} solution. How much of each was required?",
             answer="{L} {unit} of {lp}%, {H} {unit} of {hp}%", pct=(10, 10, 90), amt=(5, 80)),
        dict(key="b",                           # no. 2, the chemist
             text="A chemist needs {T} mL of a {tp}% acid solution. The lab has a {lp}% solution and a {hp}% "
                  "solution. How much of each should the chemist mix?",
             answer="{L} mL of the {lp}%, {H} mL of the {hp}%", pct=(10, 10, 90), amt=(10, 300)),
        dict(key="c",                           # no. 5, paint
             text="Paint A contains {hp}% pigment, while Paint B contains {lp}% pigment. How many gallons of "
                  "each paint must be combined to make {T} gallons of a paint mixture that is {tp}% pigment?",
             answer="{H} gallons of Paint A, {L} gallons of Paint B", pct=(10, 10, 90), amt=(5, 60)),
    ],
    "2": [
        dict(key="a", ask="H",                  # no. 3, saline
             text="To make {T} liters of saline that is {tp}% salt, a lab technician combines some {lp}% "
                  "saline with some {hp}% saline. How many liters of the stronger saline are needed?",
             answer="{H} liters", pct=(1, 1, 20), amt=(2, 40)),
        dict(key="b", ask="L",                  # no. 4, fertilizer
             text="A gardener blends fertilizer solutions to make {T} gallons of a mixture that is {tp}% "
                  "nitrogen, from a {lp}% nitrogen solution and a {hp}% nitrogen solution. How many gallons "
                  "of the weaker solution go into the mixture?",
             answer="{L} gallons", pct=(5, 5, 50), amt=(10, 200)),
        dict(key="c", ask="H", cap=15,          # no. 6, the pharmacist
             text="A pharmacist wants {T} grams of an ointment that is {tp}% active ingredient, made from "
                  "ointments that are {lp}% and {hp}% active ingredient. How many grams of the "
                  "higher-percent ointment are needed?",
             answer="{H} grams", pct=(2, 2, 20), amt=(10, 200)),
        dict(key="d", ask="L",                  # no. 9, the alloy
             text="A metalworker wants {T} ounces of an alloy that is {tp}% copper, made from a {lp}% copper "
                  "alloy and a {hp}% copper alloy. How many ounces of the {lp}% alloy are needed?",
             answer="{L} ounces", pct=(10, 10, 90), amt=(5, 80)),
        dict(key="e", ask="H",                  # no. 12, the biologist
             text="A biologist prepares {T} mL of a solution that is {tp}% nutrient by combining a {lp}% "
                  "solution and a {hp}% solution. How much of the {hp}% solution is needed?",
             answer="{H} mL", pct=(10, 10, 90), amt=(10, 300)),
    ],
    "3": [
        dict(key="a", give="L",                 # no. 7, sugar
             text="A solution that is {tp}% sugar is made by mixing a {lp}% sugar solution with a {hp}% "
                  "sugar solution. If {L} mL of the {lp}% solution is used, how much of the {hp}% solution "
                  "must be added?",
             answer="{H} mL", pct=(5, 5, 60), amt=(10, 300)),
        dict(key="b", give="H",                 # no. 8, coolant
             text="A machine coolant is made by mixing a {lp}% antifreeze fluid and a {hp}% antifreeze fluid. "
                  "A technician wants a {tp}% mixture and already has {H} liters of the {hp}% fluid. How much "
                  "of the {lp}% fluid should be added?",
             answer="{L} liters", pct=(10, 10, 90), amt=(5, 80)),
        dict(key="c", give="H",                 # no. 10, the beekeeper
             text="A beekeeper mixes two syrups: one is {lp}% sugar and one is {hp}% sugar. To make a {tp}% "
                  "sugar syrup using {H} quarts of the {hp}% syrup, how many quarts of the {lp}% syrup must "
                  "be added?",
             answer="{L} quarts", pct=(2, 20, 70), amt=(2, 40)),
        dict(key="d", give="L", cap=15,         # no. 11, the janitor
             text="To make a disinfectant, a janitor mixes a {lp}% bleach solution with a {hp}% bleach "
                  "solution. If {L} gallons of the weaker solution are used and the mixture is {tp}% bleach, "
                  "how many gallons of the stronger solution are in the mixture?",
             answer="{H} gallons", pct=(1, 1, 20), amt=(1, 20)),
    ],
    "4": [
        dict(key="a", water=+1,                 # the 2025-26 midterm
             text="How much water should be added to {A} liters of a {p}% saccharin solution to get a {q}% "
                  "saccharin solution?",
             answer="{W} liters of water"),
        dict(key="b", water=0,
             text="How many liters of pure antifreeze must be added to {A} liters of a {p}% antifreeze "
                  "solution to make a {q}% antifreeze solution?",
             answer="{W} liters of antifreeze"),
        dict(key="c", water=-1,
             text="How many ounces of water must be boiled off from {A} ounces of a {p}% salt solution to "
                  "make a {q}% salt solution?",
             answer="{W} ounces of water"),
    ],
}
STORY = {(t, s["key"]): s for t, ss in STORIES.items() for s in ss}

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Drawing: amounts first, then a target percent that comes out whole
# ------------------------------------------------------------------
def two_solutions(r, st):
    step, lo, hi = st["pct"]
    lp, hp = sorted(r.sample(range(lo, hi + 1, step), 2))
    astep, most = st["amt"]
    L, H = (astep * r.randint(1, most // astep) for _ in range(2))
    tp = F(lp * L + hp * H, L + H)
    need(L != H and tp.denominator == 1 and lp < tp < hp and tp <= st.get("cap", 100))    # not halfway
    return dict(lp=lp, hp=hp, L=L, H=H, T=L + H, tp=int(tp))

def water(r, st):
    """A amount at p% becomes q%: water added (+1), boiled off (-1), or pure ingredient added (0)."""
    A, W = 5 * r.randint(1, 20), 5 * r.randint(1, 20)
    p = 5 * r.randint(1, 18)
    if st["water"] == 1:
        q = F(A * p, A + W)
    elif st["water"] == -1:
        need(W < A)
        q = F(A * p, A - W)
    else:
        q = F(A * p + 100 * W, A + W)
    need(q.denominator == 1 and 0 < q < 100 and q != p)
    return dict(A=A, W=W, p=p, q=int(q))

def draw(entry, r, tpl):
    st = STORIES[entry][tpl]
    v = water(r, st) if entry == "4" else two_solutions(r, st)
    if st.get("words"):
        v["unit"], v["ing"] = r.choice(INGREDIENTS)
    return dict(story=st["key"], prompt=gen.fill(st["text"], **v), answer=gen.fill(st["answer"], **v))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(STORIES[e]))

# ------------------------------------------------------------------
# Checking: the mixture equation, from the story's numbers
# ------------------------------------------------------------------
def solve(typ, st, v):
    """The amounts the answer gives, from the story's numbers (strings)."""
    n = {k: gen.number(x) for k, x in v.items() if k not in ("unit", "ing")}
    if typ == "4":
        A, p, q = n["A"], n["p"], n["q"]
        if st["water"] == 1:
            return {"W": A * p / q - A}
        if st["water"] == -1:
            return {"W": A - A * p / q}
        return {"W": A * (q - p) / (100 - q)}
    lp, hp, tp = n["lp"], n["hp"], n["tp"]
    if "T" in n:                                         # L + H = T and lp L + hp H = tp T
        H = n["T"] * (tp - lp) / (hp - lp)
        return {"L": n["T"] - H, "H": H}
    if "L" in n:
        return {"H": n["L"] * (tp - lp) / (hp - tp)}
    return {"L": n["H"] * (hp - tp) / (tp - lp)}

def check(p):
    try:
        st = STORY[(p["type"], p["story"])]
        v = gen.read(st["text"], p["prompt"])
        got = gen.read(st["answer"], p["answer"])
        want = solve(p["type"], st, v)
        ok = all(gen.number(got[k]) == x for k, x in want.items() if k in got) and \
            any(k in got for k in want) and all(got[k] == v[k] for k in got if k not in want)
    except (ValueError, KeyError, ZeroDivisionError):
        return "unchecked"
    return "checked" if ok else "failed"

# ------------------------------------------------------------------
# Showing and editing: change the numbers; keep the words
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, height = gen.text_shown()

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    st = STORY[(old["type"], old["story"])]
    v = gen.read(st["text"], t)
    v.update(solve(old["type"], st, v))
    new = dict(old, prompt=t, answer=gen.fill(st["answer"], **v), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
