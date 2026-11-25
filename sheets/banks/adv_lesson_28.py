"""Lesson 28 (Advanced Math): factorial notation, abstract rate problems.
From the Saxon lesson and its deck
(~/Documents/adv_math/problem_sets/ps_028/slides/deck_028.typ): examples
28.1-28.6 and Problem Set 28, problems 1, 2, 6, and 7.

    1  one factorial:                       5!                                  120
    2  a quotient of factorials:            9!/(3! 5!),  14!/(6! 11!)           504,  91/30
    3  a product as a quotient (a calculator's factorial key):
                                            11 · 10 · 9 · 8                     11!/7! = 7920
    4  abstract rate, a new rate:           The train traveled m miles at p miles per hour and still arrived
                                            1 hour late. How fast ...?          (m p)/(m - p) mi/hr
    5  abstract rate, a new time:           The boat traveled k miles in t hours and was 40 miles short ...
                                                                                ((k + 40) t)/(k + 10 t) hours

The types file's examples without a Problem Set item (28.1, 28.4) are types
too. Type 2's templates are the deck's two shapes: everything below cancels
into the top (28.2, problems 6 and 7) and a fraction is left (28.3).

Type 4 also has an "early" template (the new time is longer, so the
denominator is a sum); Type 5 has the deck's two shapes: a distance and a
time given (28.6), or a time and a rate (problem 2).

Stories keep the book's words except for pronouns, which are taken out as in
Lesson 25:
  28.6     "If the skipper tried again, how long would it take to reach the goal if she increased
           the rate of travel by 10 mph?" is written "If the skipper tried again and increased the
           rate of travel by 10 mph, how long would it take to reach the goal?"
  PS 2     "If he tried again and increased his speed by 5 miles per hour, how long would it take him
           to reach the goal?" is written "If Redig tried again and increased the speed by 5 miles
           per hour, how long would it take Redig to reach the goal?"
The letters are drawn at random (the book's are reachable).

The key writes what the deck writes:
  1, 2  the number, or a fraction in lowest terms: 120, 504, 91/30, 840, 10080
        (the deck writes "10,080"; the key has no thousands comma).
  3     the quotient, then its value: "(11!)/(7!) = 7920".
  4     one fraction in lowest terms, the product over the new time's numerator, then the unit:
        (m p)/(m - p) "mi"/"hr" (28.5), (p x)/(x - 2 p) "mi"/"hr" (problem 1); letters in a
        product alphabetical, the distance first in a sum.
  5     the same, in hours: ((k + 40) t)/(k + 10 t) "hours" (28.6, the deck's factored top),
        (R T + 20)/(R + 5) "hours" (problem 2).

check():
  1-3  the factorials are read from the prompt's text and computed exactly; the answer's number
       must be the value, in lowest terms (Type 3: and its quotient must be n!/m! with the
       prompt's top and the factor below its last).
  4-5  the story's numbers and letters are read back; the new rate (distance over the new time)
       or the new time (the new distance over the new rate) is built from them, and the
       answer's expression must have the same value at random points, be one fraction with
       no fraction inside, in lowest terms, and carry the unit.

No skipped sources: Lesson 28 has no proofs.

A problem: dict(type, story, prompt, answer, source). Types 1-3: prompt and answer in Typst math,
story "". Types 4-5: the prompt is words, the answer Typst math:
    story   "late"
    prompt  "The train traveled m miles at p miles per hour and still arrived 1 hour late. How fast
             should the train have traveled to have arrived on time?"
    answer  '(m p)/(m - p) "mi"/"hr"'
"""
import math, re
from fractions import Fraction as F
import sympy as sp
from .. import gen
from ..gen import need
from ..check import to_sympy, same_value, lowest_terms
from ..typmath import tx, display, dfrac
from ..typst import esc

NAME = FAMILY = "adv_lesson_28"
FIXED = False
TITLE = "Lesson 28: Factorial Notation, Abstract Rate Problems"
INSTRUCTIONS = "Evaluate."
COURSES = {"Advanced Math": "Lessons"}

TYPES = [
    dict(key="1", title="One Factorial",
         look="A whole number followed by $!$, like $5!$.",
         move="Write out the factors from the number down to 1 and multiply: $5! = 5 dot 4 dot 3 dot 2 dot 1 = 120$."),
    dict(key="2", title="A Quotient of Factorials",
         instructions="Evaluate without using a calculator.",
         look="Factorials above and below, like $(9!)/(3! thin 5!)$.",
         move="Write the top factorial down to the larger one below, $14! = 14 dot 13 dot 12 dot 11!$, and cancel "
              "it. Write out the other one below and cancel what you can before you multiply."),
    dict(key="3", title="A Product as a Quotient of Factorials",
         instructions="Use the factorial key on a calculator to help evaluate.",
         look="A product of whole numbers that count down by 1, like $11 dot 10 dot 9 dot 8$.",
         move="Multiply above and below by the factorial of the next number down: $(11 dot 10 dot 9 dot 8 dot 7!)"
              "/(7!) = (11!)/(7!)$. Find both factorials on the calculator and divide."),
    dict(key="4", title="Abstract Rate Problems: A New Rate",
         instructions="Solve.",
         look="A distance and a rate in letters, and a number of hours late (or early).",
         move="Time is distance over rate: $m/p$ hours. The new time is $m/p - 1 = (m - p)/p$ hours. The new rate "
              "is the same distance over the new time: $m/((m - p)/p) = (m p)/(m - p)$ miles per hour.",
         width="full", space="1.75in"),
    dict(key="5", title="Abstract Rate Problems: A New Time",
         instructions="Solve.",
         look="A first try that falls short of the goal by some miles, then a faster try.",
         move="Find the first rate (distance over time, $k/t$) or the first distance (rate times time, $R T$). "
              "The new distance adds the miles short; the new rate adds the increase: $k/t + 10 = (k + 10 t)/t$. "
              "Time is the new distance over the new rate.",
         width="full", space="1.75in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

def frac(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"

# ------------------------------------------------------------------
# Type 1: n!
# ------------------------------------------------------------------
SINGLE = range(2, 9)                    # up to 8! = 40320, by hand

def t1(n):
    return f"{n}!"

def t1_ok(n):
    return n in SINGLE

def t1_pick(r):
    return dict(n=r.choice(SINGLE))

# ------------------------------------------------------------------
# Type 2: n!/(a! b!)
# ------------------------------------------------------------------
TOPS = range(5, 16)
LEFT = 6                                 # at most this many factors left above, after the larger one below cancels

def t2(n, a, b):
    return f"({n}!)/({a}! thin {b}!)"

def t2_value(n, a, b):
    return F(math.factorial(n), math.factorial(a) * math.factorial(b))

def t2_ok(n, a, b):
    v = t2_value(n, a, b) if n in TOPS and 2 <= a < n and 2 <= b < n else F(0)
    return (n in TOPS and 2 <= a < n and 2 <= b < n and n - max(a, b) <= LEFT
            and v.numerator <= 200000 and v.denominator <= 120)       # 91/30 (28.3); no 143/3360

def t2_pick(whole):
    def pick(r):
        n = r.choice(TOPS)
        a, b = r.randint(2, n - 1), r.randint(2, n - 1)
        need((a + b <= n) == whole)                     # 28.2: everything below cancels; 28.3: a fraction
        p = dict(n=n, a=a, b=b)
        need(t2_ok(**p) and (t2_value(**p).denominator == 1) == whole)
        return p
    return pick

# ------------------------------------------------------------------
# Type 3: n (n - 1) ... (m + 1) = n!/m!
# ------------------------------------------------------------------
PRODUCT_TOPS = range(7, 16)
LENGTHS = range(3, 7)

def t3(n, k):
    """k factors counting down from n."""
    return " dot ".join(str(n - i) for i in range(k))

def t3_ok(n, k):
    return n in PRODUCT_TOPS and k in LENGTHS and n - k >= 2

def t3_pick(r):
    p = dict(n=r.choice(PRODUCT_TOPS), k=r.choice(LENGTHS))
    need(t3_ok(**p))
    return p

# ------------------------------------------------------------------
# Factorial answers: worked from the prompt's text, and checked
# ------------------------------------------------------------------
def factorial_value(prompt):
    """The prompt's exact value, read from its text."""
    if m := re.fullmatch(r"(\d+)!", prompt):
        return F(math.factorial(int(m.group(1))))
    if m := re.fullmatch(r"\((\d+)!\)/\((\d+)! thin (\d+)!\)", prompt):
        return t2_value(*(int(x) for x in m.groups()))
    factors = [int(x) for x in prompt.split(" dot ")]
    if any(b != a - 1 for a, b in zip(factors, factors[1:])):
        raise ValueError("factors that count down by 1")
    return F(math.prod(factors))

def factorial_answer(prompt):
    v = frac(factorial_value(prompt))
    if " dot " in prompt:
        factors = [int(x) for x in prompt.split(" dot ")]
        return f"({factors[0]}!)/({factors[-1] - 1}!) = {v}"
    return v

def factorial_check(p):
    prompt, ans = p["prompt"], " ".join(p["answer"].split())
    want = factorial_value(prompt)
    if " dot " in prompt:
        m = re.fullmatch(r"\((\d+)!\)/\((\d+)!\) = (\d+)", ans)
        if not m:
            return False
        top, below, v = (int(x) for x in m.groups())
        factors = [int(x) for x in prompt.split(" dot ")]
        return (top == factors[0] and below == factors[-1] - 1
                and F(math.factorial(top), math.factorial(below)) == want == v)
    m = re.fullmatch(r"(\d+)(?:/(\d+))?", ans)
    if not m:
        return False
    got = F(int(m.group(1)), int(m.group(2) or 1))
    return got == want and ans == frac(got)                 # lowest terms

# ------------------------------------------------------------------
# Types 4 and 5: stories in letters
# ------------------------------------------------------------------
VEHICLES = ("train", "bus", "car", "truck", "boat", "plane")
HOURS = range(1, 6)
LETTERS = tuple(c for c in gen.LETTERS if c != "a")      # "traveled a miles" reads as an article
UPPER = tuple(c.upper() for c in LETTERS)

T4_TEXT = {
    "late": "The {v} traveled {d} miles at {r} miles per hour and still arrived {h} {hrs} late. How fast should "
            "the {v} have traveled to have arrived on time?",
    "early": "The {v} traveled {d} miles at {r} miles per hour and arrived {h} {hrs} early. How fast should the "
             "{v} have traveled to have arrived exactly on time?",
}
RATE_UNIT = '"mi"/"hr"'
TIME_UNIT = '"hours"'

def letters_ok(*ls):
    return len(set(ls)) == len(ls) and (all(c in LETTERS for c in ls) or all(c in UPPER for c in ls))

def coef(n, x):
    return x if n == 1 else f"{n} {x}"

def product(*ls):
    return " ".join(sorted(ls))

def t4_answer(story, d, r, h):
    """d over the new time (d -+ h r)/r: (d r)/(d - h r)."""
    sign = "-" if story == "late" else "+"
    return f"({product(d, r)})/({d} {sign} {coef(h, r)}) {RATE_UNIT}"

def t4(story, v, d, r, h):
    text = gen.fill(T4_TEXT[story], v=v, d=d, r=r, h=h, hrs="hour" if h == 1 else "hours")
    return story, text, t4_answer(story, d, r, h)

def t4_ok(story, v, d, r, h):
    return story in T4_TEXT and v in VEHICLES and letters_ok(d, r) and h in HOURS

def t4_pick(story):
    def pick(r):
        d, rate = r.sample(r.choice((LETTERS, LETTERS, UPPER)), 2)
        return dict(story=story, v=r.choice(VEHICLES), d=d, r=rate, h=r.choice(HOURS))
    return pick

SHORT = range(5, 101, 5)
FASTER = range(2, 21)
T5_TEXT = {
    "distance": "The {craft} traveled {d} miles in {t} hours and was {s} miles short of the goal when the gun went "
                "off. If the {who} tried again and increased the rate of travel by {u} mph, how long would it take "
                "to reach the goal?",
    "rate": "{who} ran for {t} hours at {r} miles per hour but ended up {s} miles short of the goal. If {who} tried "
            "again and increased the speed by {u} miles per hour, how long would it take {who} to reach the goal?",
}
CRAFT = {"skipper": "boat", "pilot": "plane", "driver": "truck", "rider": "motorcycle", "captain": "ship"}
WHO = {"distance": tuple(CRAFT),
       "rate": ("Redig", "Marisol", "Okonkwo", "Bettina", "Hiroshi") + gen.NAMES}

def t5_answer(story, s, u, t, d=None, r=None):
    if story == "distance":                 # (d + s)/(d/t + u) = ((d + s) t)/(d + u t)
        return f"(({d} + {s}) {t})/({d} + {coef(u, t)}) {TIME_UNIT}"
    return f"({product(r, t)} + {s})/({r} + {u}) {TIME_UNIT}"

def t5(story, who, s, u, t, d=None, r=None):
    text = gen.fill(T5_TEXT[story], who=who, craft=CRAFT.get(who), d=d, t=t, r=r, s=s, u=u)
    return story, text, t5_answer(story, s, u, t, d, r)

def t5_ok(story, who, s, u, t, d=None, r=None):
    other = d if story == "distance" else r
    return (story in T5_TEXT and who in WHO[story] and s in SHORT and u in FASTER and letters_ok(t, other)
            and (d is None) == (story == "rate") and (r is None) == (story == "distance"))

def t5_pick(story):
    def pick(r_):
        a, b = r_.sample(r_.choice((LETTERS, LETTERS, UPPER)), 2)
        p = dict(story=story, who=r_.choice(WHO[story]), s=r_.choice(SHORT), u=r_.choice(FASTER), t=b)
        p["d" if story == "distance" else "r"] = a
        return p
    return pick

def rate_story(typ, story, v):
    """The answer's value, as sympy, from the story's letters and numbers (as read)."""
    if typ == "4":
        d, r, h = sp.Symbol(v["d"]), sp.Symbol(v["r"]), int(v["h"])
        if v["hrs"] != ("hour" if h == 1 else "hours"):
            raise ValueError("hour or hours")
        return d / (d / r + (-h if story == "late" else h))
    s, u, t = int(v["s"]), int(v["u"]), sp.Symbol(v["t"])
    if story == "distance" and CRAFT.get(v["who"]) != v["craft"]:
        raise ValueError("the craft and who runs it")
    if story == "distance":
        d = sp.Symbol(v["d"])
        return (d + s) / (d / t + u)
    r = sp.Symbol(v["r"])
    return (r * t + s) / (r + u)

def rate_check(typ, story, prompt, answer):
    v = gen.read(T4_TEXT[story] if typ == "4" else T5_TEXT[story], prompt)
    unit = RATE_UNIT if typ == "4" else TIME_UNIT
    if not answer.endswith(" " + unit):
        return False
    expr = answer[: -len(unit) - 1]
    raw = to_sympy(expr, evaluate=False)
    below = [a for a in sp.preorder_traversal(raw) if isinstance(a, sp.Pow) and a.exp.is_negative]
    return (same_value(expr, tx(rate_story(typ, story, v))) and len(below) == 1      # one fraction, none inside
            and lowest_terms(expr))

# ------------------------------------------------------------------
# Templates: (pick, build); factorial builds return the prompt, story builds (story, prompt, answer)
# ------------------------------------------------------------------
TEMPLATES = {
    "1": [(t1_pick, t1)],
    "2": [(t2_pick(True), t2), (t2_pick(True), t2), (t2_pick(False), t2)],
    "3": [(t3_pick, t3)],
    "4": [(t4_pick("late"), t4), (t4_pick("late"), t4), (t4_pick("early"), t4)],
    "5": [(t5_pick("distance"), t5), (t5_pick("rate"), t5)],
}
RANGES = {t1: t1_ok, t2: t2_ok, t3: t3_ok, t4: t4_ok, t5: t5_ok}

def in_range(build, params):
    """Every parameter inside its named range: the random draw can pick these."""
    return bool(RANGES[build](**params))

def draw(entry, r, tpl):
    pick, build = TEMPLATES[entry][tpl]
    out = build(**pick(r))
    if entry in "123":
        return dict(story="", prompt=out, answer=factorial_answer(out))
    story, prompt, answer = out
    return dict(story=story, prompt=prompt, answer=answer)

def answer_of(typ, story, prompt):
    """The key's answer, worked again from the prompt (the story's words read back)."""
    if typ in "123":
        return factorial_answer(prompt)
    v = gen.read(T4_TEXT[story] if typ == "4" else T5_TEXT[story], prompt)
    if typ == "4":
        return t4_answer(story, v["d"], v["r"], int(v["h"]))
    return t5_answer(story, int(v["s"]), int(v["u"]), v["t"], v.get("d"), v.get("r"))

def check(p):
    try:
        typ, ans = p["type"], " ".join(p["answer"].split())
        ok = factorial_check(dict(p, answer=ans)) if typ in "123" else rate_check(typ, p["story"], p["prompt"], ans)
    except Exception:
        return "unchecked"
    return "checked" if ok else "failed"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing: factorials as math; stories as words with their letters in math
# ------------------------------------------------------------------
LEAD = {"1": "Evaluate:", "2": "Evaluate:", "3": "Evaluate:"}
SINGLE_LETTER = re.compile(r"(?<![\w'])([A-Za-z])(?![\w'])")

def story_typst(text):
    """Escaped words; each lone letter (not "a" or "I") in math: m miles is $m$ miles."""
    return SINGLE_LETTER.sub(lambda m: m.group(1) if m.group(1) in "aI" else f"${m.group(1)}$", esc(text))

def typst(p, gap="0.3em"):
    if p["type"] in "123":
        return f"{LEAD[p['type']]} #h(0.5em) " + display(dfrac(p["prompt"]))
    return story_typst(p["prompt"])

def answer_typst(p):
    return display(dfrac(p["answer"]))

def plain(t):
    return (t.replace(" thin ", " ").replace(" dot ", " · ").replace('"mi"/"hr"', "mi/hr")
            .replace('"hours"', "hours").replace("-", "−"))

def text(p):
    return f"{LEAD[p['type']]} {plain(p['prompt'])}" if p["type"] in "123" else p["prompt"]

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.2 * (1 + len(p["prompt"]) // 90) if p["type"] in "45" else 0.55 if "/" in p["prompt"] else 0.3

# ------------------------------------------------------------------
# Editing
# ------------------------------------------------------------------
def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = " ".join(t.split())
    try:
        answer = answer_of(old["type"], old["story"], t)
    except (ValueError, KeyError, AttributeError):
        raise ValueError("keep the problem's form; change only its numbers and letters, like 9!/(3! thin 5!)") \
            from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=" ".join(t.split()))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed, reset=6)   # 7 single factorials
