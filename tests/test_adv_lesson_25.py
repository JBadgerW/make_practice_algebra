"""Lesson 25 (Advanced Math): age problems, rate problems. Every source is
reachable from in-range parameters and checks with the deck's answer; wrong
answers fail; every type draws, checks, and keeps its shape; edits solve again.

    python3 tests/test_adv_lesson_25.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_25 as B

lib = library.current()
assert "adv_lesson_25" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 25: Age Problems, Rate Problems"
assert all(B.type_instructions(k) == "Solve." for k in B.KEYS)

# ---- every source: the deck's answer, and checked (wording as the docstring says)
SOURCES = [   # (id, type, story, prompt, deck answer)
    ("ex 25.1", "1", "ago:ratio|ahead:diff|0",
     "Ten years ago, Thomas was twice as old as Patricia. Five years from now, Thomas will be 10 years older "
     "than Patricia. How old are both people now?", "Patricia is 20, Thomas is 30"),
    ("ex 25.2", "2", "together",
     "Joe Frank can wash 3 cars in 5 hours and Myrl can wash 4 cars in 3 hours. Fifteen cars need to be washed. "
     "If Joe Frank works for 2 hours and is then joined by Myrl, how long will Myrl and Joe Frank have to work "
     "together to finish washing the 15 cars?", "207/29 hr ≈ 7.14 hr"),
    ("ex 25.3", "3", "joint",
     "Mayha could empty 2 bottles in 3 hours. Working together, Mayha and Wilbur could empty 4 bottles in 3 "
     "hours. What was Wilbur's rate of emptying bottles?", "2/3 bottle/hr"),
    ("ex 25.4", "4", "if",
     "If 5 workers can do 1 job in 8 days, how many workers would it take to do 3 jobs in 7 days?",
     "17.14 workers"),
    ("ex 25.5", "5", "supplies",
     "Mary had 252 gallons (gal) of milk. This would feed 42 infants for 12 days. Then 14 more infants were "
     "placed in the nursery and 48 more gallons were provided. How long would the milk last now?", "10.71 days"),
    ("PS 1", "1", "ago:ratio|ahead:ratio|1",
     "Five years ago, Orville was twice as old as Wilbur. Five years from now, Orville will be 1 1/2 times as "
     "old as Wilbur. How old are both now?", "Wilbur is 15, Orville is 25"),
    ("PS 2", "2", "together",
     "Emerson can dig 2 holes in 3 hours and Johnna can dig 3 holes in 2 hours. Six holes need to be dug. If "
     "Emerson works for 1 hour and is then joined by Johnna, how long will Johnna and Emerson have to work "
     "together to finish digging the 6 holes?", "32/13 hr ≈ 2.46 hr"),
    ("PS 3", "3", "joint",
     "Sandra could build 3 sandcastles in 5 hours. Working together, Sandra and Frederick could build 3 "
     "sandcastles in 3 hours. What was Frederick's rate of building sandcastles?", "2/5 sandcastle/hr"),
    ("PS 4", "4", "then",
     "Six men can do 1 job in 9 days. How many men would it take to do 15 jobs in 5 days?", "162 men"),
]
prompt_of = {s[0]: s[3] for s in SOURCES}
for sid, typ, story, prompt, answer in SOURCES:
    assert B.answer_of(typ, story, prompt) == answer, (sid, B.answer_of(typ, story, prompt), answer)
    assert B.check(dict(type=typ, story=story, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 25.1": (B.t1, dict(A="Thomas", B="Patricia", a=30, b=20, w1="ago", r1="ratio", t1=10, w2="ahead",
                           r2="diff", t2=5, q=0)),
    "ex 25.2": (B.t2, dict(P="Joe Frank", Q="Myrl", job="cars", a=3, b=5, c=4, d=3, N=15, t=2)),
    "ex 25.3": (B.t3, dict(P="Mayha", Q="Wilbur", job="bottles", a=2, b=3, c=4, d=3)),
    "ex 25.4": (B.t4, dict(story="if", crew="workers", W1=5, J1=1, D1=8, J2=3, D2=7)),
    "ex 25.5": (B.t5, dict(P="Mary", supply="milk", G1=252, I1=42, D1=12, I2=14, G2=48)),
    "PS 1": (B.t1, dict(A="Orville", B="Wilbur", a=25, b=15, w1="ago", r1="ratio", t1=5, w2="ahead",
                        r2="ratio", t2=5, q=1)),
    "PS 2": (B.t2, dict(P="Emerson", Q="Johnna", job="holes", a=2, b=3, c=3, d=2, N=6, t=1)),
    "PS 3": (B.t3, dict(P="Sandra", Q="Frederick", job="sandcastles", a=3, b=5, c=3, d=3)),
    "PS 4": (B.t4, dict(story="then", crew="men", W1=6, J1=1, D1=9, J2=15, D2=5)),
}
assert set(REACH) == set(prompt_of)                                    # nothing left out
TYPE_OF = {s[0]: s[1] for s in SOURCES}
for sid, (build, params) in REACH.items():
    story, prompt, answer = build(**params)
    assert prompt == prompt_of[sid], (sid, prompt)
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid  # the type's own template
assert sorted(set(TYPE_OF.values())) == B.KEYS                          # every type has a source
# 25.1 and problem 1 are each their own template's shape
assert B.BOOK_SHAPES == [(("ago", "ratio"), ("ahead", "diff"))]
assert B.RATIO_SHAPES == [(("ago", "ratio"), ("ahead", "ratio"))]
# out of range
assert not B.in_range(B.t1, dict(REACH["PS 1"][1], a=22))              # 17/10 is no multiplier
assert not B.in_range(B.t1, dict(REACH["ex 25.1"][1], r1="diff"))      # no ratio: no single answer
assert not B.in_range(B.t2, dict(REACH["PS 2"][1], N=1))               # done before the other joins
assert not B.in_range(B.t3, dict(REACH["PS 3"][1], c=1))               # the other's rate would be negative
assert not B.in_range(B.t4, dict(REACH["PS 4"][1], D2=9, J2=1))        # the same situation
assert not B.in_range(B.t5, dict(REACH["ex 25.5"][1], G1=250))         # 250/504 gal per infant-day

# ---- wrong answers fail
src = {s[0]: dict(type=s[1], story=s[2], prompt=s[3], answer=s[4]) for s in SOURCES}
WRONG = [
    ("ex 25.1", "Patricia is 30, Thomas is 20"),        # ages swapped
    ("ex 25.1", "Thomas is 30, Patricia is 20"),        # the older first
    ("ex 25.1", "Patricia is 20, Thomas is 31"),
    ("PS 1", "Wilbur is 10, Orville is 20"),            # their ages five years ago
    ("ex 25.2", "207/29 hr"),                           # no decimal
    ("ex 25.2", "414/58 hr ≈ 7.14 hr"),                 # not in lowest terms
    ("ex 25.2", "207/29 hr ≈ 7.1 hr"),                  # one place
    ("ex 25.2", "207/29 hr = 7.14 hr"),                 # not exact
    ("ex 25.2", "15/29 hr ≈ 0.52 hr"),                  # forgot the 6/5 car done alone... and the rest
    ("PS 2", "16/3 hr ≈ 5.33 hr"),                      # the holes left, not the hours
    ("ex 25.3", "2/3 bottles/hr"),                      # plural below 1
    ("ex 25.3", "4/3 bottles/hr"),                      # the joint rate
    ("PS 3", "6/5 sandcastles/hr"),
    ("ex 25.4", "17.15 workers"),
    ("ex 25.4", "18 workers"),                          # rounded up to whole workers
    ("ex 25.4", "17.14 men"),
    ("PS 4", "162 workers"),
    ("ex 25.5", "10.72 days"),
    ("ex 25.5", "10.7 days"),
]
for sid, answer in WRONG:
    got = B.check(dict(src[sid], answer=answer))
    assert got != "checked", (sid, answer, got)

# ---- rounding: half up, two places unless exact
from fractions import Fraction as F
assert B.rounded(F(1, 8)) == "0.13" and B.rounded(F(53, 10)) == "5.3" and B.rounded(F(530, 100)) == "5.3"
assert B.rounded(F(228, 43)) == "5.30" and B.rounded(F(162)) == "162"
assert B.hours(F(5, 2)) == "5/2 hr = 2.5 hr" and B.hours(F(3)) == "3 hr"

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^.*(years ago|is now|years from now).*(years ago|is now|years from now).* How old are both( people)? now\?$",
    "2": r"^.+ can \w+ \d+ \w+ in \d+ hours? and .+ can \w+ \d+ \w+ in \d+ hours?\. [A-Z][a-z-]+ \w+ need to be ",
    "3": r"^.+ could \w+ \d+ \w+ in \d+ hours?\. Working together, .+ What was .+'s rate of \w+ \w+\?$",
    "4": r"^(If \d+|[A-Z][a-z-]+) \w+ can do \d+ jobs? in \d+ days[,.] [Hh]ow many \w+ would it take",
    "5": r"^.+ had \d+ .+ of .+\. This would feed \d+ \w+ for \d+ days\. Then \d+ more ",
}
ANSWER = {
    "1": r"^.+ is \d+, .+ is \d+$",
    "2": r"^\d+ hr$|^\d+/\d+ hr (= \d+\.\d{1,2}|≈ \d+\.\d\d) hr$",
    "3": r"^\d+(/\d+)? \w+/hr$",
    "4": r"^\d+(\.\d\d?)? \w+$",
    "5": r"^\d+(\.\d\d?)? days$",
}
rng = random.Random(25)
stories = {k: set() for k in B.KEYS}
for k in B.KEYS:
    seen = set()
    for i in range(300):
        if i % 50 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.search(SHAPE[k], p["prompt"]), p
        assert re.search(ANSWER[k], p["answer"]), p
        assert not re.search(r"\b(he|she|his|her|him|they|their)\b", p["prompt"], re.I), p
        assert not re.search(r"\b1 (hours|days|jobs|\w+s)\b", p["prompt"]), p          # 1 hour, 1 job
        assert B.answer_of(k, p["story"], p["prompt"]) == p["answer"], p
        stories[k].add(p["story"])
        if k == "1":
            a, b = (int(x) for x in re.findall(r"\d+", p["answer"]))
            assert a < b <= 80, p
assert len(stories["1"]) >= 10 and stories["4"] == {"if", "then", "days"}, stories

# ---- showing: fractions in math, the rest escaped words
p = src["PS 1"]
assert "$1 display(1/2)$ times" in B.typst(p), B.typst(p)
assert B.answer_typst(src["ex 25.2"]) == "$display(207/29)$ hr ≈ 7.14 hr"
assert B.answer_typst(src["ex 25.3"]) == "$display(2/3)$ bottle/hr"
assert B.text(p) == p["prompt"] and B.answer_text(p) == p["answer"]

# ---- editing: new numbers are solved again; the words stay
p, status = B.from_edit(prompt_of["PS 4"].replace("15 jobs", "10 jobs"), dict(src["PS 4"], source="template"))
assert status == "checked" and p["answer"] == "108 men", p
p, status = B.from_edit(prompt_of["ex 25.1"].replace("Ten years", "Eight years"), src["ex 25.1"])
assert status == "checked" and p["answer"] == "Patricia is 18, Thomas is 28", p
p, status = B.with_answer(src["ex 25.3"], "2/3 bottle/hr")
assert status == "checked", p
p, status = B.with_answer(src["ex 25.3"], "1 bottle/hr")
assert status == "failed", p
try:
    B.from_edit("Six men can do one job.", src["PS 4"]); raise AssertionError("unreadable")
except ValueError:
    pass

print("adv_lesson_25: ok")
