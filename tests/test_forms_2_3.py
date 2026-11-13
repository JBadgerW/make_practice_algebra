"""Lesson 2-3: Forms of Linear Equations: every type draws, checks, shows, and edits; every
problem keeps its type's rules; each form is read strictly, as the key writes it.

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
for k in B.KEYS:
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

B.selftest(200, 2)
print("all forms_2_3 tests passed")
