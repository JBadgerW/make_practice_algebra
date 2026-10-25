"""Direct and inverse variation (Advanced Math), from the old app's set
AdvMath_18_03: one quantity varies directly as a power of a second and
inversely as a power of a third, r = k b^p / g^q, told with three things of
one kind (apples, bananas, cherries; its twenty groups of items).

    Type 1   r = k b^2 / g        Type 2   r = k b^3 / g        Type 3   r = k b / g^2

A type's templates ask for a different quantity: r (as the old set did),
then b, then g. Every number in the story and in the answer is a whole
number, as the old set made sure.

A problem: dict(type, story, prompt, answer, source); story is the template
("r", "b", or "g": what is asked); prompt and answer are words:
    answer  "48 apples"
check() reads the numbers back out of the words, finds k from the first
situation, solves for what is asked, and compares with the answer's number.
"""
import math
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need

NAME = FAMILY = "adv_variation"
FIXED = False
TITLE = "Direct and Inverse Variation"
INSTRUCTIONS = "Solve."
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Directly as a Square, Inversely as Another",
         look="\"... varied directly as B squared and inversely as G.\"",
         move="Write R = k B^2/G. Put in the first situation's numbers to find k. Then use k with the second "
              "situation's numbers and solve for what's asked."),
    dict(key="2", title="Directly as a Cube, Inversely as Another",
         look="\"... varied directly as B cubed and inversely as G.\"",
         move="Write R = k B^3/G. Find k from the first situation, then solve the second for what's asked."),
    dict(key="3", title="Directly as One, Inversely as a Square",
         look="\"... varied directly as B and inversely as G squared.\"",
         move="Write R = k B/G^2. Find k from the first situation, then solve the second for what's asked."),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1.5in", width="full")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
POWERS = {"1": (2, 1), "2": (3, 1), "3": (1, 2)}         # r = k b^p / g^q
KS = (2, 3, 4, 5, 6, 8, 9, 10, 12)                       # the old set's constants of variation
BIG = 2000

ITEM_GROUPS = [
    ["apples", "bananas", "cherries"], ["brooms", "shovels", "rakes"], ["cars", "trucks", "motorcycles"],
    ["dogs", "cats", "parrots"], ["eagles", "falcons", "owls"], ["fans", "air conditioners", "heaters"],
    ["gloves", "mittens", "scarves"], ["hats", "caps", "bonnets"], ["ice creams", "sorbets", "gelatos"],
    ["jackets", "sweaters", "vests"], ["keys", "locks", "vaults"], ["laptops", "tablets", "phones"],
    ["mugs", "cups", "glasses"], ["notebooks", "pencils", "erasers"], ["streams", "rivers", "lakes"],
    ["paintings", "sculptures", "drawings"], ["quilts", "blankets", "throws"],
    ["rockets", "satellites", "shuttles"], ["shoes", "boots", "sandals"], ["timers", "clocks", "stopwatches"],
]

LEAD = {"1": "{R} varied directly as {bn} squared and inversely as {gn}.",
        "2": "{R} varied directly as {bn} cubed and inversely as {gn}.",
        "3": "{R} varied directly as {bn} and inversely as {gn} squared."}
GIVEN = " When there were {r1} {rn}, there were {b1} {bn} and {g1} {gn}."
ASK = {"r": " How many {rn} were there when there were {b2} {bn} and {g2} {gn}?",
       "b": " How many {bn} were there when there were {r2} {rn} and {g2} {gn}?",
       "g": " How many {gn} were there when there were {r2} {rn} and {b2} {bn}?"}
ANSWER = {"r": "{r2} {rn}", "b": "{b2} {bn}", "g": "{g2} {gn}"}
STORIES = ("r", "b", "g")

def template(typ, story):
    return LEAD[typ] + GIVEN + ASK[story]

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Drawing: whole numbers by construction, as the old set did
# ------------------------------------------------------------------
def situation(r, k, p, q):
    """(r, b, g), whole numbers with r = k b^p / g^q, each at least 2."""
    if q == 1:                                          # g divides k b^p
        b = r.randint(2, 12 if p == 2 else 6)
        g = gen.proper_divisor(r, k * b ** p)
        val = (b, g)
    else:                                               # b = r g^2 / k
        g = r.randint(2, 6)
        rr = r.randint(1, 6) * (k // math.gcd(k, g * g))
        val = (rr * g * g // k, g)
    b, g = val
    rr = F(k * b ** p, g ** q)
    need(rr.denominator == 1 and 2 <= rr <= BIG and 2 <= b <= 200 and g >= 2)    # never "1 parrots"
    return int(rr), b, g

def draw(entry, r, tpl):
    story = STORIES[tpl]
    p, q = POWERS[entry]
    k = r.choice(KS)
    r1, b1, g1 = situation(r, k, p, q)
    r2, b2, g2 = situation(r, k, p, q)
    need(len({(r1, b1, g1), (r2, b2, g2)}) == 2 and b1 != b2)
    rn, bn, gn = r.sample(r.choice(ITEM_GROUPS), 3)
    v = dict(R=rn.capitalize(), rn=rn, bn=bn, gn=gn, r1=r1, b1=b1, g1=g1, r2=r2, b2=b2, g2=g2)
    return dict(story=story, prompt=gen.fill(template(entry, story), **v), answer=gen.fill(ANSWER[story], **v))

generate = gen.generator(NAME, draw, lambda p: check(p), seen_key, lambda e: len(STORIES))

# ------------------------------------------------------------------
# Checking: from the words alone
# ------------------------------------------------------------------
def exact_root(x, n):
    """The positive n-th root of a Fraction, if it's rational; ValueError if not."""
    v = sp.root(sp.Rational(x.numerator, x.denominator), n)
    if not v.is_Rational:
        raise ValueError(f"the {n}th root of {x} isn't a whole number")
    return F(int(v.p), int(v.q))

def solve(typ, story, v):
    """What's asked, from the story's numbers v (strings)."""
    p, q = POWERS[typ]
    n = {key: gen.number(v[key]) for key in ("r1", "b1", "g1") if key in v}
    k = n["r1"] * n["g1"] ** q / n["b1"] ** p
    if story == "r":
        return k * gen.number(v["b2"]) ** p / gen.number(v["g2"]) ** q
    if story == "b":
        return exact_root(gen.number(v["r2"]) * gen.number(v["g2"]) ** q / k, p)
    return exact_root(k * gen.number(v["b2"]) ** p / gen.number(v["r2"]), q)

def answer_of(typ, story, prompt):
    v = gen.read(template(typ, story), prompt)
    x = solve(typ, story, v)
    return gen.fill(ANSWER[story], **{story + "2": x, "rn": v["rn"], "bn": v["bn"], "gn": v["gn"]})

def check(p):
    try:
        v = gen.read(template(p["type"], p["story"]), p["prompt"])
        got = gen.read(ANSWER[p["story"]], p["answer"])
        want = solve(p["type"], p["story"], v)
        unit = {"r": "rn", "b": "bn", "g": "gn"}[p["story"]]
        ok = gen.number(got[p["story"] + "2"]) == want and got[unit] == v[unit]
    except (ValueError, KeyError, ZeroDivisionError):
        return "unchecked"
    return "checked" if ok else "failed"

# ------------------------------------------------------------------
# Showing and editing: change the numbers or the items; keep the words
# ------------------------------------------------------------------
typst, answer_typst, text, answer_text, height = gen.text_shown()

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    new = dict(old, prompt=t, answer=answer_of(old["type"], old["story"], t), source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
