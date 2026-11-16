"""Lesson 2-4: Parallel and Perpendicular Lines: every type draws, checks, shows, and edits; the
given line is read strictly in its form, the answer strictly in slope-intercept form.

    python3 tests/test_parallel_perp_2_4.py
"""
import random
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import parallel_perp_2_4 as B

lib = library.current()
assert "parallel_perp_2_4" in dict(lib.view("Algebra 1"))["Lessons"]
assert B.TITLE == "Lesson 2-4: Parallel and Perpendicular Lines"
assert B.heading("4") == "Type 4: Perpendicular, From Another Form"

# ---- every type: drawn, checked, in its rules, its given forms spread evenly
rng = random.Random(11)
for k in B.KEYS:
    seen, forms = set(), Counter()
    for _ in range(200):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert p["form"] in B.SOURCES[k]
        forms[p["form"]] += 1
        (m0, b0), (x1, y1) = B.given_of(p["prompt"], p["form"])
        assert m0 != 0 and x1 != 0 and y1 != 0 and abs(x1) <= 9 and abs(y1) <= 9
        if p["form"] in ("si", "std", "gen"):
            assert b0.denominator == 1 and abs(b0) <= 9 and (b0 != 0 or p["form"] == "si")
        elif p["form"] == "int":
            xi, yi = B.fm.intercepts(m0, b0)
            assert xi.denominator == yi.denominator == 1 and 0 < abs(xi) <= 10 and 0 < abs(yi) <= 10
        else:
            g = B.ps.read_point_slope(B.split(p["prompt"])[0])
            assert 0 not in g[1:] and abs(g[1]) <= 9 and abs(g[2]) <= 9 and g[1:] != (x1, y1)
            assert b0 != 0 and abs(b0) <= 20
        m, b = B.line_of(p)
        assert m == (m0 if k in B.PARALLEL else -1 / m0) and abs(b) <= 20 and y1 == m * x1 + b
        if k in B.PARALLEL:
            assert b != b0, "never the given line"
        assert p["answer"] == B.slope_intercept(m, b)
    assert set(forms) == set(B.SOURCES[k]) and max(forms.values()) - min(forms.values()) <= 1, forms

# ---- the check
p = dict(type="1", form="si", prompt="y = 2/3 x - 4; (3, 5)", answer="y = 2/3 x + 3")
assert B.check(p) == "checked"
for wrong in ("y = 2/3 x - 4", "y = 4/6 x + 3", "y = -3/2 x + 19/2", "y - 5 = 2/3 (x - 3)", "2 x - 3 y = -9"):
    assert B.check(dict(p, answer=wrong)) == "failed", wrong
q = dict(type="2", form="si", prompt="y = 2/3 x - 4; (4, -1)", answer="y = -3/2 x + 5")
assert B.check(q) == "checked"
assert B.check(dict(q, answer="y = 3/2 x - 7")) == "failed", "the reciprocal without the sign"
assert B.check(dict(q, answer="y = -2/3 x + 5/3")) == "failed", "the opposite without the reciprocal"
r3 = dict(type="3", form="std", prompt="3 x - 2 y = 20; (-2, 5)", answer="y = 3/2 x + 8")
assert B.check(r3) == "checked"
for wrong in ("y - 5 = 3/2 (x + 2)", "3 x - 2 y = -16", "y = -3/2 x + 8"):
    assert B.check(dict(r3, answer=wrong)) == "failed", wrong
for form, line in (("ps", "y + 4 = 3/2 (x - 4)"), ("gen", "3 x - 2 y - 20 = 0"), ("int", "x/(20/3) - y/10 = 1")):
    r = dict(r3, form=form, prompt=f"{line}; (-2, 5)")
    assert B.check(r) == ("checked" if form != "int" else "failed"), (form, line)   # intercepts must be whole
assert B.check(dict(type="4", form="int", prompt="x/6 - y/4 = 1; (4, 1)", answer="y = -3/2 x + 7")) == "checked"
assert B.check(dict(r3, form="si")) == "failed", "the prompt isn't in the form it claims"
assert B.check(dict(r3, form="si", prompt="y = 3/2 x - 10; (-2, 5)")) == "failed", "Type 3 never gives slope-intercept form"
assert B.check(dict(r3, form="std", prompt="-3 x + 2 y = -20; (-2, 5)")) == "failed", "standard form as Lesson 2-3 writes it"
assert B.check(dict(p, prompt="y = 2/3 x - 4; (3, -2)", answer="y = 2/3 x - 4")) == "failed", "the point on the line"
assert B.check(dict(q, prompt="y = 5; (4, -1)", answer="x = 4")) == "failed", "no slope"

# ---- showing
assert B.typst(r3) == ("Find the equation of the line parallel to $display(3 x - 2 y = 20)$ that passes through "
                       "point $display((-2, 5))$.")
assert B.text(q) == "Find the equation of the line perpendicular to y = 2/3 x − 4 that passes through point (4, −1)."
assert B.answer_typst(q) == "#pad(top: 0.6em)[$display(y = -display(3/2) x + 5)$]" and B.answer_text(q) == "y = −3/2 x + 5"
assert B.height(p) == 0.55 and B.ENTRY["1"]["width"] == "full"

# ---- editing: Types 1 and 2 take any form and write it in slope-intercept form; 3 and 4 keep the form typed
for t in ("y=2/3x-4, (3,5)", "2x - 3y = 12 through (3, 5).", "y = 2/3 x - 4; (3, 5)", "y + 2 = 2/3 (x - 3) (3, 5)"):
    new, status = B.from_edit(t, dict(type="2", prompt="", answer=""))
    assert new["prompt"] == "y = 2/3 x - 4; (3, 5)" and new["form"] == "si" and new["answer"] == "y = -3/2 x + 19/2" \
        and status == "checked", t
new, status = B.from_edit("3x-2y=20, (-2,5)", dict(type="3", form="ps", prompt="", answer=""))
assert new["prompt"] == "3 x - 2 y = 20; (-2, 5)" and new["form"] == "std" and new["answer"] == "y = 3/2 x + 8" \
    and status == "checked"
new, status = B.from_edit("x/6 - y/4 = 1 through (4, 1)", dict(type="4", prompt="", answer=""))
assert new["form"] == "int" and new["answer"] == "y = -3/2 x + 7" and status == "checked"
new, status = B.from_edit("y = 2 x + 1; (1, 3)", dict(type="1", prompt="", answer="y = 2 x + 5"))
assert status == "failed" and new["answer"] == "y = 2 x + 5", "the point on the line keeps the old answer"
for t, k in (("y = 5; (1, 2)", "2"), ("y = 2 x + 1", "2"), ("y = 2 x + 1; (1/2, 3)", "2"),
             ("y = 3/2 x - 10; (-2, 5)", "3"), ("2 x = 3 y + 12; (1, 1)", "4")):
    try:
        B.from_edit(t, dict(type=k, prompt="", answer=""))
        raise AssertionError(t)
    except ValueError:
        pass
new, status = B.with_answer(dict(r3, answer=""), "y=3/2x+8")
assert new["answer"] == "y = 3/2 x + 8" and status == "checked"

B.selftest(200, 2)
print("all parallel_perp_2_4 tests passed")
