"""Lesson 2-3: Forms of Linear Equations: every type draws, checks, shows, and edits; every
problem keeps its type's rules; each form is read strictly, as the key writes it; the word
problems (Types 5 to 12) check from their words, and the teacher's own problems give their keys.

    python3 tests/test_forms_2_3.py
"""
import random
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import forms_2_3 as B

lib = library.current()
assert "forms_2_3" in dict(lib.view("Algebra 1"))["Lessons"]
assert B.heading("4") == "Type 4: To Intercept Form"

# ---- the forms, as written and read back
m, b = F(2, 3), F(-4)
assert B.slope_intercept(m, b) == "y = 2/3 x - 4"
assert B.standard(m, b) == "2 x - 3 y = 12"
assert B.general(m, b) == "2 x - 3 y - 12 = 0"
assert B.intercept(m, b) == "x/6 - y/4 = 1"
assert B.intercept(F(5, 2), F(5)) == "-x/2 + y/5 = 1"
assert B.standard(F(-1), F(7)) == "x + y = 7" and B.general(F(1), F(-3)) == "x - y - 3 = 0"
assert B.standard(F(2, 3), F(-17, 3)) == "2 x - 3 y = 17"
for f in ("si", "std", "gen", "int"):
    assert B.read(f, B.write(f, m, b)) == (m, b), f
assert B.read("ps", "y + 3 = 2/3 (x - 4)") == (F(2, 3), F(-17, 3))
for f, bad in (("std", "-2 x + 3 y = -12"), ("std", "4 x - 6 y = 24"), ("std", "1 x - y = 3"), ("std", "2 x + -3 y = 12"),
               ("std", "2 x - 3 y - 12 = 0"), ("std", "-3 y + 2 x = 12"), ("gen", "-2 x + 3 y + 12 = 0"),
               ("gen", "2 x - 3 y = 12"), ("gen", "4 x - 6 y - 24 = 0"), ("int", "x/6 + y/(-4) = 1"),
               ("int", "x/6 - y/4 = 2"), ("int", "x/12 - y/8 = 2"), ("si", "y = 4/6 x - 4"), ("ps", "y = 2/3 x - 4")):
    assert B.read(f, bad) is None or B.read(f, bad) != (m, b), (f, bad)
assert B.read("std", "2 x - 3 y = 13") == (F(2, 3), F(-13, 3)), "a different line, read as itself"
assert B.form_of("x/6 - y/4 = 1") == "int" and B.form_of("y - 2 = 3 (x + 1)") == "ps" and B.form_of("2 x = 3 y") is None

# ---- every type: drawn, checked, in its rules, its starting forms spread evenly
rng = random.Random(11)
for k in B.FORM_TYPES:
    seen, forms = set(), Counter()
    for _ in range(200):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert p["form"] in B.SOURCES[k] and p["form"] != B.TARGET[k]
        forms[p["form"]] += 1
        m, b = B.read(p["form"], p["prompt"])
        assert m != 0 and b != 0 and p["answer"] == B.write(B.TARGET[k], m, b)
        if "int" in (p["form"], B.TARGET[k]):
            xi, yi = B.intercepts(m, b)
            assert xi.denominator == yi.denominator == 1 and 0 < abs(xi) <= 10 and 0 < abs(yi) <= 10
        else:
            assert abs(b) <= 20
        if p["form"] == "ps":
            g = B.ps.read_point_slope(p["prompt"])
            assert g and 0 not in g[1:] and abs(g[1]) <= 10 and abs(g[2]) <= 10
    assert set(forms) == set(B.SOURCES[k]) and max(forms.values()) - min(forms.values()) <= 1, forms

# ---- the check: the type's form, the prompt's line
p = dict(type="2", form="ps", prompt="y + 3 = 2/3 (x - 4)", answer="2 x - 3 y = 17")
assert B.check(p) == "checked"
for wrong in ("-2 x + 3 y = -17", "4 x - 6 y = 34", "2 x - 3 y = -17", "2 x - 3 y - 17 = 0", "y = 2/3 x - 17/3"):
    assert B.check(dict(p, answer=wrong)) == "failed", wrong
assert B.check(dict(p, form="si")) == "failed", "the prompt isn't in the form it claims"
assert B.check(dict(p, type="1", form="si", prompt="y = 2/3 x - 4", answer="y = 2/3 x - 4")) == "failed", "a type's own form"
assert B.check(dict(type="4", form="std", prompt="2 x - 3 y = 0", answer="x/0 - y/0 = 1")) == "failed"

# ---- showing
q = dict(type="4", form="si", prompt="y = 5/2 x + 5", answer="-x/2 + y/5 = 1")
assert B.check(q) == "checked"
assert B.typst(q) == "$display(y = display(5/2) x + 5)$"
assert B.answer_typst(q) == "$display(-display(x/2) + display(y/5) = 1)$"
assert B.text(q) == "y = 5/2 x + 5" and B.answer_text(q) == "−x/2 + y/5 = 1" and B.height(q) == 0.55

# ---- editing: hand-typed spacing is tidied; a prompt in the type's own form or with no intercept form is refused
assert B.tidy("y+3=2/3(x-4)") == "y + 3 = 2/3 (x - 4)" and B.tidy("-x/2+y/5=1") == "-x/2 + y/5 = 1"
new, status = B.from_edit("3x+4y=12", dict(type="4", form="si", prompt="", answer=""))
assert new["prompt"] == "3 x + 4 y = 12" and new["form"] == "std" and new["answer"] == "x/4 + y/3 = 1" and status == "checked"
new, status = B.from_edit("y−5=−(x+2)", dict(type="3", form="si", prompt="", answer=""))
assert new["form"] == "ps" and new["answer"] == "x + y - 3 = 0" and status == "checked"
for t, k in (("y = 2 x + 1", "1"), ("y = 2 x + 1", "4"), ("2 x = 3 y + 1 + x", "2")):
    try:
        B.from_edit(t, dict(type=k, prompt="", answer=""))
        raise AssertionError(t)
    except ValueError:
        pass
new, status = B.from_edit("y = 3 x", dict(type="2", form="si", prompt="", answer=""))
assert status == "failed", "a line through the origin keeps the old answer, which the check marks"
new, status = B.with_answer(dict(type="3", form="std", prompt="3 x + 4 y = 10", answer=""), "3x+4y-10=0")
assert new["answer"] == "3 x + 4 y - 10 = 0" and status == "checked"

# ---- Types 5 to 12: the word problems, one type for each of the teacher's, in order
import re
W = B.W
assert B.KEYS[4:] == list(B.WORDS) == [str(k) for k in range(5, 13)]
assert all(B.ENTRY[k]["width"] == "full" for k in B.WORDS)
for typ in B.WORDS:
    rng, seen = random.Random(40 + int(typ)), set()
    stories = Counter()
    for _ in range(60):
        p = B.generate(typ, rng, seen)
        stories[p["story"]] += 1
        assert B.check(p) == "checked"
        assert "Let x be" in p["prompt"] or "with x the" in p["prompt"] or typ == "11", "x and y are named"
        assert not re.search(r"\b(he|she|his|her|him)\b", p["prompt"], re.I), "no pronouns: the name is repeated"
        new, status = B.from_edit(B.edit_text(p), p)
        assert status == "checked" and new["source"] == "edited", (p, new)
        assert typ in W.CHOICE or new["answer"] == p["answer"]
        assert B.text(p) and B.answer_text(p) and B.answer_typst(p) and B.typst(p)
        if typ not in W.CHOICE:
            assert all(";" not in t for t in W.split(p)) and len(W.split(p)) == len(W.labeled(p))
    assert len(stories) == W.stories(typ), f"Type {typ} draws all its stories"

fill = lambda typ, story, **v: W.gen.fill(W.template(typ, story), **v)
def key(typ, story, **v):
    p = dict(type=typ, story=story, prompt=fill(typ, story, **v))
    p["answer"] = W.answer_of(typ, story, p["prompt"])
    assert B.check(p) == "checked", p
    return p
# 1: $150, reserved $25, general $10; 3: $12, green $3, red $2
p = key("5", "a", who="Hanna", c="150", a="25", b="10")
assert p["answer"] == "25 x + 10 y = 150"
assert B.check(dict(p, answer="5 x + 2 y = 30")) == "checked", "a whole-number multiple is the same line"
for wrong in ("10 x + 25 y = 150", "25 x + 10 y = 15", "25 x + 10 y + 150 = 0", "y = -5/2 x + 15", "2.5 x + y = 15"):
    assert B.check(dict(p, answer=wrong)) == "failed", wrong
assert key("5", "b", who="Deondra", c="12", a="3", b="2")["answer"] == "3 x + 2 y = 12"
# 2: $30, almonds $10, cashews $12, about the same of each
p = key("6", "a", who="Tamira", c="30", a="10", b="12")
assert p["answer"] == ("10 x + 12 y = 30; Put y = x into the equation: 10 x + 12 x = 30, so 22 x = 30 and x = 15/11 ≈ "
                       "1.36. Buy about 1.36 lb of almonds and about 1.36 lb of cashews.")
# 4: $30, Cheddar $3, Swiss $5
p = key("7", "a", who="Keisha", c="30", a="3", b="5")
assert W.split(p)[0].startswith("10 lb: ") and W.split(p)[1].startswith("6 lb: ") and W.split(p)[3] == "3 x + 5 y = 30"
assert "5 lb of Cheddar and 3 lb of Swiss: 3(5) + 5(3) = 30." in p["answer"]
assert B.check(dict(p, answer=p["answer"].replace("10 lb", "6 lb", 1))) == "failed"
# 5: a 50 ft by 50 ft pen, goats 100 ft², chickens 20 ft², about 3 times as many chickens
p = key("8", "a", who="Diya", l="50", g="100", h="20", k="3")
a = W.split(p)
assert a[0] == "100 x + 20 y = 2500" and "(12.5, 62.5) or (26, -5)" in a[1]
assert a[2].startswith("15 goats and 45 chickens: ") and "x = 15.625" in a[2] and "= 2400 ft², which fits" in a[2]
# 6: $300, shirts $20, caps $12
p = key("9", "a", who="Paxton", c="300", a="20", b="12")
assert W.split(p)[0] == "20 x + 12 y = 300"
assert "(0, 25), (3, 20), (6, 15), (9, 10), (12, 5), and (15, 0)" in p["answer"] and "(1, 23 1/3)" in p["answer"]
# 7: $50, oranges $2.50, pineapple $4: the source's four choices
v = W.read("10", "a", fill("10", "a", who="Darren", c="50", a="2.50", b="4"))
choices, ans = W.choices_10(random.Random(1), W.facts("10", "a", v))
assert sorted(choices) == sorted(["y - 5 = 100 (x - 8)", "100 y = 8 x + 5", "5 x + 8 y = 100", "100 x + 5 y = 8"])
p = dict(type="10", story="a", prompt=fill("10", "a", who="Darren", c="50", a="2.50", b="4"), choices=choices, answer=ans)
assert B.check(p) == "checked" and W.gen.chosen(p) == ["5 x + 8 y = 100"]
assert B.check(dict(p, answer=next(l for l in "ABCD" if l != ans))) == "failed"
# 8: 3/8 x + 2/3 y = 5: the source's five choices
f = W.facts("11", "a", W.read("11", "a", "3/8 x + 2/3 y = 5"))
choices, ans = W.choices_11(random.Random(1), f)
assert sorted(choices) == sorted(["y = -9/16 x + 15/2", "y + 3/2 = -9/16 (x - 16)", "3/8 x + 2/3 y = 5",
                                  "3 x + 16/3 y = 40", "9 x + 16 y = 120"])
p = dict(type="11", story="a", prompt="3/8 x + 2/3 y = 5", choices=choices, answer=ans)
assert B.check(p) == "checked" and W.gen.chosen(p) == ["9 x + 16 y = 120"]
new, status = B.from_edit("1/2x+2/3y=3", p)
assert status == "checked" and W.gen.chosen(new) == ["3 x + 4 y = 18"]
# 9: $8; mango $0.50, pineapple $0.75, strawberry $1.00; at least 12 cups
p = key("12", "a", who="Fatima", c="8", p1="0.50", p2="0.75", p3="1.00", T="12")
a = W.split(p)
assert a[:3] == ["Mango and pineapple: 2 x + 3 y = 32", "Mango and strawberry: x + 2 y = 16",
                 "Pineapple and strawberry: 3 x + 4 y = 32"]
assert a[3] == "Mango and pineapple: from 10 2/3 cups (all pineapple) to 16 cups (all mango)."
assert a[6].startswith("Mango and pineapple, and mango and strawberry: ") and "at most 8 cups" not in a[6]
assert "Pineapple and strawberry can make at most 10 2/3 cups, less than 12." in a[6]
assert B.check(dict(p, answer=p["answer"].replace("Mango and strawberry: x + 2 y = 16", "Mango and strawberry: 2 x + y = 16"))) == "failed"
assert B.check(dict(p, answer=p["answer"].replace("x + 2 y = 16", "2 x + 4 y = 32"))) == "checked"

B.selftest(200, 2)
print("all forms_2_3 tests passed")
