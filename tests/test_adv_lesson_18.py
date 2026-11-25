"""Lesson 18 (Advanced Math): advanced word problems. Every source is
reachable from in-range parameters and checks with the deck's answer; wrong
answers fail; every type draws, checks, and keeps its shape; edits solve again.

    python3 tests/test_adv_lesson_18.py
"""
import random, re
import sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_18 as B

lib = library.current()
assert "adv_lesson_18" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 18: Advanced Word Problems"
assert all(B.type_instructions(k) == "Solve." for k in B.KEYS)

# ---- every source: the deck's answer, and checked (the book's wording, word for word)
SOURCES = [   # (id, type, story, prompt, deck answer)
    ("ex 18.1", "1", "past",
     "The number of blues was 4 less than the sum of the whites and the greens. Also, the number of greens "
     "equaled the sum of the blues and the whites. How many of each were there if there were twice as many blues "
     "as whites?", "4 blues, 2 whites, 6 greens"),
    ("ex 18.2", "2", "coins",
     "The quarters, nickels, and dimes totaled 20, and their value was $1.90. How many of each kind were there if "
     "there were 4 times as many nickels as quarters?", "2 quarters, 8 nickels, 10 dimes"),
    ("ex 18.3", "3", "2,1",
     "Reds varied directly as blues squared and inversely as greens. When there were 80 reds, there were 4 blues "
     "and 2 greens. How many reds were there when there were 8 blues and 10 greens?", "64 reds"),
    ("ex 18.4", "4", "number",
     "The sum of the digits of a two-digit counting number is 5. When the digits are reversed, the number is 9 "
     "greater than the original number. What was the original number?", "23"),
    ("ex 18.5", "5", "total",
     "To get 1000 gallons (gal) of a mixture that was 56% alcohol, it was necessary to mix a quantity of 20% "
     "alcohol solution with a quantity of 80% alcohol solution. How much of each was required?",
     "400 gal of 20% alcohol, 600 gal of 80% alcohol"),
    ("ex 18.6", "6", "many",
     "How many liters of a 64% glycol solution must be added to 77 liters of a 23% glycol solution to get a 42% "
     "glycol solution?", "66.5 liters"),
    ("ex 18.7", "7", "compound",
     "The weight of the carbon (C) in the container of C3H7Cl was 113 grams. What was the total weight of the "
     "compound? (C = 12; H = 1; Cl = 35)", "244.83 grams"),
    ("PS 1", "1", "present",
     "The number of blues is 7 less than the sum of the whites and the greens. The number of greens is 1 greater "
     "than the sum of the blues and the whites. How many of each kind are there if there are 3 times as many "
     "greens as blues?", "2 blues, 3 whites, 6 greens"),
    ("PS 2", "2", "coins",
     "The quarters, nickels, and dimes totaled 20, and their value was $2.05. How many of each kind were there if "
     "there were 3 times as many dimes as quarters?", "3 quarters, 8 nickels, 9 dimes"),
    ("PS 3", "3", "1,2",
     "Reds varied directly as blues and inversely as greens squared. When there were 5 reds, there were 2 blues "
     "and 4 greens. How many reds were there when there were 4 blues and 4 greens?", "10 reds"),
    ("PS 5", "4", "new",
     "The sum of the digits of a two-digit counting number is 13. When the digits are reversed, the new number is "
     "45 greater than the original number. What was the original number?", "49"),
    ("PS 6", "6", "much",
     "How much of a 14% iodine solution should be added to 89 ounces of a 47% iodine solution to get a 29% "
     "solution?", "106.8 ounces"),
    ("PS 7", "7", "compound",
     "The weight of the chlorine (Cl) in the container of C3H7Cl was 400 grams. What was the total weight of the "
     "compound? (C = 12; H = 1; Cl = 35)", "891.43 grams"),
]
prompt_of = {s[0]: s[3] for s in SOURCES}
for sid, typ, story, prompt, answer in SOURCES:
    assert B.answer_of(typ, story, prompt) == answer, (sid, B.answer_of(typ, story, prompt), answer)
    assert B.check(dict(type=typ, story=story, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 18.1": (B.t1, dict(tense="past", X="blues", Y="whites", Z="greens", P="blues", Q="whites", k=2,
                           x=4, y=2, z=6)),
    "ex 18.2": (B.t2, dict(c1="quarters", c2="nickels", c3="dimes", A="nickels", B="quarters", k=4,
                           n1=2, n2=8, n3=10)),
    "ex 18.3": (B.t3, dict(key="2,1", R="reds", B="blues", G="greens", k=10, b1=4, g1=2, b2=8, g2=10)),
    "ex 18.4": (B.t4, dict(story="number", t=2, u=3)),
    "ex 18.5": (B.t5, dict(unit1="gallons (gal)", ing="alcohol", lp=20, hp=80, L=400, H=600)),
    "ex 18.6": (B.t6, dict(story="many", unit="liters", ing="glycol", ap=64, A=77, bp=23, tp=42)),
    "ex 18.7": (B.t7, dict(formula="C3H7Cl", sym="C", w=113)),
    "PS 1": (B.t1, dict(tense="present", X="blues", Y="whites", Z="greens", P="greens", Q="blues", k=3,
                        x=2, y=3, z=6)),
    "PS 2": (B.t2, dict(c1="quarters", c2="nickels", c3="dimes", A="dimes", B="quarters", k=3, n1=3, n2=8, n3=9)),
    "PS 3": (B.t3, dict(key="1,2", R="reds", B="blues", G="greens", k=40, b1=2, g1=4, b2=4, g2=4)),
    "PS 5": (B.t4, dict(story="new", t=4, u=9)),
    "PS 6": (B.t6, dict(story="much", unit="ounces", ing="iodine", ap=14, A=89, bp=47, tp=29)),
    "PS 7": (B.t7, dict(formula="C3H7Cl", sym="Cl", w=400)),
}
assert set(REACH) == set(prompt_of)                                    # nothing left out
TYPE_OF = {s[0]: s[1] for s in SOURCES}
for sid, (build, params) in REACH.items():
    story, prompt, answer = build(**params)
    assert prompt == prompt_of[sid], (sid, prompt)
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid  # the type's own template
assert sorted(set(TYPE_OF.values())) == B.KEYS                          # every type has a source
# the book's shapes have their own templates
assert B.BOOK_PAIRS == ((0, 1), (2, 0)) and set(B.T1_TEXT) == {"past", "present"}
assert {"2,1", "1,2"} <= set(B.POWERS) and set(B.T4_TEXT) == {"number", "new"} and set(B.T6_TEXT) == {"many", "much"}
# out of range
assert not B.in_range(B.t1, dict(REACH["ex 18.1"][1], x=5))            # blues no longer twice the whites
assert not B.in_range(B.t1, dict(REACH["ex 18.1"][1], P="blues", Q="blues"))
assert not B.in_range(B.t2, dict(REACH["ex 18.2"][1], c3="pennies"))
assert not B.in_range(B.t3, dict(REACH["PS 3"][1], b2=3))              # 120/16 reds
assert not B.in_range(B.t4, dict(REACH["ex 18.4"][1], u=2))            # reversed, the same number
assert not B.in_range(B.t5, dict(REACH["ex 18.5"][1], L=410, H=590))   # 55.4% is not whole
assert not B.in_range(B.t6, dict(REACH["ex 18.6"][1], tp=70))          # stronger than both
assert not B.in_range(B.t7, dict(REACH["ex 18.7"][1], sym="H"))        # hydrogen is 7 of 78: too small a part

# ---- wrong answers fail
src = {s[0]: dict(type=s[1], story=s[2], prompt=s[3], answer=s[4]) for s in SOURCES}
WRONG = [
    ("ex 18.1", "2 blues, 4 whites, 6 greens"),         # blues and whites swapped
    ("ex 18.1", "2 whites, 4 blues, 6 greens"),         # not the story's order
    ("ex 18.1", "4 blues, 2 whites, 7 greens"),
    ("PS 1", "2 blues, 3 whites, 5 greens"),            # the "1 greater" dropped
    ("PS 1", "2 blue, 3 whites, 6 greens"),             # singular for 2
    ("ex 18.2", "8 quarters, 2 nickels, 10 dimes"),     # 4 times the other way
    ("ex 18.2", "2 quarters, 8 nickels, 9 dimes"),      # 19 coins
    ("PS 2", "3 quarters, 9 nickels, 8 dimes"),
    ("ex 18.3", "64 blues"),
    ("ex 18.3", "1600 reds"),                           # inversely made directly
    ("PS 3", "20 reds"),                                # greens not squared
    ("ex 18.4", "32"),                                  # the reversed number
    ("PS 5", "94"),
    ("PS 5", "049"),
    ("ex 18.5", "600 gal of 20% alcohol, 400 gal of 80% alcohol"),     # amounts swapped
    ("ex 18.5", "400 gallons of 20% alcohol, 600 gallons of 80% alcohol"),
    ("ex 18.6", "66.50 liters"),                        # a trailing zero
    ("ex 18.6", "143.5 liters"),                        # the final amount, 77 + 66.5
    ("ex 18.6", "66.5 ounces"),
    ("PS 6", "106.8 liters"),
    ("PS 6", "107 ounces"),
    ("ex 18.7", "244.8 grams"),                         # one place
    ("ex 18.7", "244.84 grams"),
    ("ex 18.7", "52.31 grams"),                         # 113 times 36/78
    ("PS 7", "891.42 grams"),                           # rounded down
]
for sid, answer in WRONG:
    got = B.check(dict(src[sid], answer=answer))
    assert got != "checked", (sid, answer, got)
# a story's words that don't fit
bad = dict(src["ex 18.6"], prompt=prompt_of["ex 18.6"].replace("a 42%", "an 42%"))
assert B.check(bad) != "checked"
bad = dict(src["ex 18.7"], prompt=prompt_of["ex 18.7"].replace("Cl = 35", "Cl = 36"))
assert B.check(bad) == "failed"                         # weighed with the story's own atomic weights

# ---- helpers
assert B.article(8) == B.article(18) == B.article(82) == B.article(11) == "an" and B.article(64) == "a"
assert B.parts("C3H7Cl") == [("C", 3), ("H", 7), ("Cl", 1)] and B.parts("NaHCO3")[-1] == ("O", 3)
assert B.rounded(F(733, 3)) == "244.33" and B.rounded(F(133, 2)) == "66.5"

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^The number of (\w+) (was|is|equal).* the sum of the (\w+) and the (\w+)\. (Also, the|The) number of "
         r"\4 .* the sum of the \1 and the \3\. How many of each (were there|kind are there) if there (were|are) "
         r"(twice|\d times) as many \w+ as \w+\?$",
    "2": r"^The (quarters|nickels|dimes), (quarters|nickels|dimes), and (quarters|nickels|dimes) totaled \d+, and "
         r"their value was \$\d+\.\d\d\. How many of each kind were there if there were (twice|\d times) as many ",
    "3": r"^[A-Z]\w+ varied directly as \w+( squared)? and inversely as \w+( squared)?\. When there were \d+ \w+, "
         r"there were \d+ \w+ and \d+ \w+\. How many \w+ were there when there were \d+ \w+ and \d+ \w+\?$",
    "4": r"^The sum of the digits of a two-digit counting number is \d+\. When the digits are reversed, the (new )?"
         r"number is \d+ (greater|less) than the original number\. What was the original number\?$",
    "5": r"^To get \d+ \w+ \(\w+\) of a mixture that was \d+% \w+, it was necessary to mix a quantity of \d+% ",
    "6": r"^How (many \w+|much) of an? \d+% \w+ solution (must|should) be added to \d+ \w+ of an? \d+% \w+ "
         r"solution to get an? \d+% (\w+ )?solution\?$",
    "7": r"^The weight of the \w+ \(\w+\) in the container of \w+ was \d+ grams\. What was the total weight of the "
         r"compound\? \((\w+ = \d+(; )?)+\)$",
}
ANSWER = {
    "1": r"^\d+ \w+, \d+ \w+, \d+ \w+$",
    "2": r"^\d+ \w+, \d+ \w+, \d+ \w+$",
    "3": r"^\d+ \w+s$",
    "4": r"^[1-9][1-9]$",
    "5": r"^\d+ \w+ of \d+% \w+, \d+ \w+ of \d+% \w+$",
    "6": r"^\d+(\.\d\d?)? \w+$",
    "7": r"^\d+(\.\d\d?)? grams$",
}
rng = random.Random(18)
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
        assert not re.search(r"(?<![\d.])1 (?!less\b)\w+s\b", p["prompt"] + " " + p["answer"]), p      # 1 blue, 1 dime
        assert not re.search(r"(?<![\d.])0 ", p["prompt"] + " " + p["answer"]), p
        assert B.answer_of(k, p["story"], p["prompt"]) == p["answer"], p
        stories[k].add(p["story"])
        nums = [F(x) for x in re.findall(r"\d+(?:\.\d+)?", p["answer"])]
        if k in "123":
            assert all(n.denominator == 1 and n >= 1 for n in nums), p
        if k == "5":
            assert nums[0] + nums[2] == F(re.search(r"To get (\d+)", p["prompt"]).group(1)), p
        if k == "6":
            given = F(re.search(r"added to (\d+)", p["prompt"]).group(1))
            assert given / 4 - 1 <= nums[0] <= 3 * given, p
assert stories["1"] == {"past", "present"} and stories["4"] == {"number", "new"}, stories
assert stories["3"] == set(B.POWERS) and stories["6"] == {"many", "much"}, stories

# ---- showing: escaped words, the formula as the deck's math
p = src["ex 18.7"]
assert '$"C"_3"H"_7"Cl"$' in B.typst(p) and "(C~=~12; H~=~1; Cl~=~35)" in B.typst(p), B.typst(p)
assert "\\$1.90" in B.typst(src["ex 18.2"])
assert B.typst(src["ex 18.6"]) == prompt_of["ex 18.6"]
assert B.text(p) == p["prompt"] and B.answer_text(p) == p["answer"]

# ---- editing: new numbers are solved again; the words stay
p, status = B.from_edit(prompt_of["ex 18.4"].replace("is 5.", "is 7."), dict(src["ex 18.4"], source="template"))
assert status == "checked" and p["answer"] == "34", p
p, status = B.from_edit(prompt_of["PS 2"].replace("$2.05", "$1.70"), src["PS 2"])
assert status == "checked" and p["answer"] == "2 quarters, 12 nickels, 6 dimes", p
p, status = B.from_edit(prompt_of["PS 2"].replace("$2.05", "$2.55"), src["PS 2"])
assert status != "checked", p                           # 35 quarters' worth: no whole answer
p, status = B.from_edit(prompt_of["ex 18.3"].replace("10 greens", "16 greens"), src["ex 18.3"])
assert status == "checked" and p["answer"] == "40 reds", p
p, status = B.from_edit(prompt_of["ex 18.7"].replace("113", "120"), src["ex 18.7"])
assert status == "checked" and p["answer"] == "260 grams", p
p, status = B.with_answer(src["ex 18.6"], "66.5 liters")
assert status == "checked", p
p, status = B.with_answer(src["ex 18.6"], "66 liters")
assert status == "failed", p
try:
    B.from_edit("How many liters of glycol?", src["ex 18.6"]); raise AssertionError("unreadable")
except ValueError:
    pass

print("adv_lesson_18: ok")
