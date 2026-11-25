"""Lesson 28 (Advanced Math): factorial notation, abstract rate problems.
Every source is reachable from in-range parameters and checks with the deck's
answer; wrong and unfinished answers fail; every type draws, checks, and keeps
its shape; edits solve again.

    python3 tests/test_adv_lesson_28.py
"""
import random, re
import sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_28 as B

lib = library.current()
assert "adv_lesson_28" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 28: Factorial Notation, Abstract Rate Problems"
assert B.type_instructions("2") == "Evaluate without using a calculator."
assert B.type_instructions("3") == "Use the factorial key on a calculator to help evaluate."
assert B.type_instructions("4") == B.type_instructions("5") == "Solve."

# ---- every source: the deck's answer, and checked (wording as the docstring says)
SOURCES = [   # (id, type, story, prompt, deck answer)
    ("ex 28.1", "1", "", "5!", "120"),
    ("ex 28.2", "2", "", "(9!)/(3! thin 5!)", "504"),
    ("ex 28.3", "2", "", "(14!)/(6! thin 11!)", "91/30"),
    ("ex 28.4", "3", "", "11 dot 10 dot 9 dot 8", "(11!)/(7!) = 7920"),
    ("ex 28.5", "4", "late",
     "The train traveled m miles at p miles per hour and still arrived 1 hour late. How fast should the train have "
     "traveled to have arrived on time?", '(m p)/(m - p) "mi"/"hr"'),
    ("ex 28.6", "5", "distance",
     "The boat traveled k miles in t hours and was 40 miles short of the goal when the gun went off. If the skipper "
     "tried again and increased the rate of travel by 10 mph, how long would it take to reach the goal?",
     '((k + 40) t)/(k + 10 t) "hours"'),
    ("PS 1", "4", "late",
     "The bus traveled x miles at p miles per hour and still arrived 2 hours late. How fast should the bus have "
     "traveled to have arrived on time?", '(p x)/(x - 2 p) "mi"/"hr"'),
    ("PS 2", "5", "rate",
     "Redig ran for T hours at R miles per hour but ended up 20 miles short of the goal. If Redig tried again and "
     "increased the speed by 5 miles per hour, how long would it take Redig to reach the goal?",
     '(R T + 20)/(R + 5) "hours"'),
    ("PS 6", "2", "", "(8!)/(2! thin 4!)", "840"),
    ("PS 7", "2", "", "(9!)/(3! thin 3!)", "10080"),                    # the deck: 10,080
]
prompt_of = {s[0]: s[3] for s in SOURCES}
for sid, typ, story, prompt, answer in SOURCES:
    assert B.answer_of(typ, story, prompt) == answer, (sid, B.answer_of(typ, story, prompt), answer)
    assert B.check(dict(type=typ, story=story, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 28.1": (B.t1, dict(n=5)),
    "ex 28.2": (B.t2, dict(n=9, a=3, b=5)),
    "ex 28.3": (B.t2, dict(n=14, a=6, b=11)),
    "ex 28.4": (B.t3, dict(n=11, k=4)),
    "ex 28.5": (B.t4, dict(story="late", v="train", d="m", r="p", h=1)),
    "ex 28.6": (B.t5, dict(story="distance", who="skipper", s=40, u=10, t="t", d="k")),
    "PS 1": (B.t4, dict(story="late", v="bus", d="x", r="p", h=2)),
    "PS 2": (B.t5, dict(story="rate", who="Redig", s=20, u=5, t="T", r="R")),
    "PS 6": (B.t2, dict(n=8, a=2, b=4)),
    "PS 7": (B.t2, dict(n=9, a=3, b=3)),
}
assert set(REACH) == set(prompt_of)                                    # nothing left out
TYPE_OF = {s[0]: s[1] for s in SOURCES}
for sid, (build, params) in REACH.items():
    out = build(**params)
    prompt = out if isinstance(out, str) else out[1]
    assert prompt == prompt_of[sid], (sid, prompt)
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert sorted(set(TYPE_OF.values())) == B.KEYS                          # every type has a source
# out of range
assert not B.in_range(B.t1, dict(n=12))                                 # too big by hand
assert not B.in_range(B.t2, dict(n=13, a=10, b=8))                      # 143/3360
assert not B.in_range(B.t2, dict(n=15, a=3, b=3))                       # twelve factors left above
assert not B.in_range(B.t3, dict(n=11, k=2))
assert not B.in_range(B.t4, dict(story="late", v="train", d="m", r="m", h=1))     # one letter for both
assert not B.in_range(B.t4, dict(story="late", v="train", d="a", r="p", h=1))     # "traveled a miles"
assert not B.in_range(B.t5, dict(story="distance", who="Redig", s=40, u=10, t="t", d="k"))

# ---- wrong or unfinished answers fail
src = {s[0]: dict(type=s[1], story=s[2], prompt=s[3], answer=s[4]) for s in SOURCES}
WRONG = [
    ("ex 28.1", "60"),
    ("ex 28.2", "3024"),                                # 9!/5! only
    ("ex 28.3", "182/60"),                              # not in lowest terms
    ("ex 28.3", "30/91"),
    ("ex 28.4", "7920"),                                # no quotient
    ("ex 28.4", "(11!)/(8!) = 990"),
    ("ex 28.4", "(11!)/(7!) = 7921"),
    ("ex 28.5", '(m p)/(m + p) "mi"/"hr"'),             # late taken as early
    ("ex 28.5", '(m p)/(m - p)'),                       # no unit
    ("ex 28.5", 'm/(m/p - 1) "mi"/"hr"'),               # a fraction inside a fraction
    ("ex 28.5", '(2 m p)/(2 m - 2 p) "mi"/"hr"'),       # not in lowest terms
    ("PS 1", '(p x)/(x - p) "mi"/"hr"'),                # 1 hour, not 2
    ("ex 28.6", '(k + 40)/(k/t + 10) "hours"'),
    ("ex 28.6", '((k + 40) t)/(k + 10 t) "mi"/"hr"'),   # the wrong unit
    ("ex 28.6", '(k t)/(k + 10 t) "hours"'),            # the 40 miles short forgotten
    ("PS 2", '(R T + 20)/(R - 5) "hours"'),
    ("PS 2", '(R T)/(R + 5) "hours"'),
]
for sid, answer in WRONG:
    got = B.check(dict(src[sid], answer=answer))
    assert got != "checked", (sid, answer, got)

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^\d+!$",
    "2": r"^\((\d+)!\)/\((\d+)! thin (\d+)!\)$",
    "3": r"^\d+( dot \d+){2,}$",
    "4": r"^The \w+ traveled [A-Za-z] miles at [A-Za-z] miles per hour and (still arrived \d hours? late|arrived \d "
         r"hours? early)\. How fast should the \w+ have traveled to have arrived (exactly )?on time\?$",
    "5": r"^(The \w+ traveled [A-Za-z] miles in [A-Za-z] hours and was \d+ miles short|.+ ran for [A-Za-z] hours at "
         r"[A-Za-z] miles per hour but ended up \d+ miles short)",
}
ANSWER = {
    "1": r"^\d+$", "2": r"^\d+(/\d+)?$", "3": r"^\(\d+!\)/\(\d+!\) = \d+$",
    "4": r'^\(\w \w\)/\(\w [-+] (\d )?\w\) "mi"/"hr"$',
    "5": r'^(\(\(\w \+ \d+\) \w\)/\(\w \+ \d+ \w\)|\(\w \w \+ \d+\)/\(\w \+ \d+\)) "hours"$',
}
rng = random.Random(28)
stories = {k: set() for k in B.KEYS}
for k in B.KEYS:
    seen = set()
    for i in range(150):
        if i % 6 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.search(SHAPE[k], p["prompt"]), p
        assert re.search(ANSWER[k], p["answer"]), p
        assert B.answer_of(k, p["story"], p["prompt"]) == p["answer"], p
        assert not re.search(r"\b(he|she|his|her|him|they|their)\b", p["prompt"], re.I), p
        stories[k].add(p["story"])
        if k == "2":
            n, a, b = (int(x) for x in re.match(SHAPE[k], p["prompt"]).groups())
            assert n - max(a, b) <= B.LEFT and F(p["answer"]).denominator <= 120, p
assert stories["4"] == {"late", "early"} and stories["5"] == {"distance", "rate"}, stories

# ---- showing: factorials and fractions in math; a story's letters in math
assert B.typst(src["ex 28.3"]) == "Evaluate: #h(0.5em) $display(display((14!)/(6! thin 11!)))$"
assert B.text(src["ex 28.4"]) == "Evaluate: 11 · 10 · 9 · 8"
t = B.typst(src["ex 28.5"])
assert t.startswith("The train traveled $m$ miles at $p$ miles per hour") and "1 hour late" in t, t
assert B.answer_text(src["ex 28.5"]) == "(m p)/(m − p) mi/hr"
assert B.answer_text(src["PS 2"]) == "(R T + 20)/(R + 5) hours"

# ---- editing: new numbers are solved again
p, status = B.from_edit("(10!)/(3! thin 5!)", dict(src["ex 28.2"], source="template"))
assert status == "checked" and p["answer"] == "5040", p
p, status = B.from_edit(prompt_of["PS 1"].replace("2 hours", "3 hours"), src["PS 1"])
assert status == "checked" and p["answer"] == '(p x)/(x - 3 p) "mi"/"hr"', p
p, status = B.with_answer(src["ex 28.6"], '((k + 40) t)/(k + 10 t) "hours"')
assert status == "checked", p
p, status = B.with_answer(src["ex 28.6"], '((k + 40) t)/(k + 10) "hours"')
assert status == "failed", p
try:
    B.from_edit("The train was late.", src["ex 28.5"]); raise AssertionError("unreadable")
except ValueError:
    pass

print("adv_lesson_28: ok")
