"""Lesson 2-2: Point-Slope Form: every type draws, checks, shows, and edits; every
problem keeps its type's rules; the check reads each part of an answer back.

    python3 tests/test_point_slope_2_2.py
"""
import random
import sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import point_slope_2_2 as B

lib = library.current()
assert "point_slope_2_2" in dict(lib.view("Algebra 1"))["Lessons"]
assert B.heading("4") == "Type 4: Two Points to Both Forms"

# ---- point-slope form, as written and read back
assert B.point_slope(F(2, 3), 4, -3) == "y + 3 = 2/3 (x - 4)"
assert B.point_slope(F(-2), -1, 5) == "y - 5 = -2 (x + 1)"
assert B.point_slope(F(1), 9, 5) == "y - 5 = x - 9"
assert B.point_slope(F(-1), 4, -1) == "y + 1 = -(x - 4)"
for m, x1, y1 in ((F(2, 3), 4, -3), (F(-2), -1, 5), (F(1), 9, 5), (F(-1), 4, -1), (F(-7, 4), -2, 6)):
    assert B.read_point_slope(B.point_slope(m, x1, y1)) == (m, x1, y1)
for bad in ("y + 3 = 4/6 (x - 4)", "y + 3 = 1 (x - 4)", "y - -3 = 2 (x - 4)", "y + 3 = 2/3 x - 8/3",
            "y = 2/3 x - 17/3", "y + 3 = (x - 4)", "y + 0 = 2 (x - 4)"):
    assert B.read_point_slope(bad) is None, bad

# ---- every type: drawn, checked, in its rules
rng = random.Random(11)
for k in B.KEYS:
    seen = set()
    for _ in range(150):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        m, b, pts = B.line_of(p)
        parts = p["answer"].split("; ")
        assert len(parts) == len(B.PARTS[k])
        assert m != 0 and parts[-1] == B.slope_intercept(m, b) or k == "1"
        if k == "1":
            assert parts == [B.slope_eq(m)] and m.denominator <= 6
        if k in ("2", "3", "6"):
            assert abs(b) <= 20 and all(v != 0 for v in pts[0])
        if k in ("3", "4", "6"):
            assert parts[-2] == B.point_slope(m, *pts[0]), "the key goes through the first point"
        if k == "4":
            assert all(v != 0 and abs(v) <= 10 for q in pts for v in q)
        if k == "5":
            ps = B.read_point_slope(p["prompt"])
            assert ps and abs(ps[1]) <= 8 and abs(ps[2]) <= 8
            assert len(B.si.lattice_points(m, b)) >= 2
        if k == "6":
            xs = [x for x, _ in pts]
            assert len(pts) == 5 and len({b2 - a for a, b2 in zip(xs, xs[1:])}) == 1 and xs[1] > xs[0]
            assert all(abs(v) <= 20 for q in pts for v in q)

# ---- the check reads every part
p = dict(type="4", prompt="(2, -3), (5, 9)", answer="m = 4; y + 3 = 4 (x - 2); y = 4 x - 11")
assert B.check(p) == "checked"
assert B.check(dict(p, answer="m = 4; y - 9 = 4 (x - 5); y = 4 x - 11")) == "checked", "either point"
for wrong in ("m = 12/3; y + 3 = 4 (x - 2); y = 4 x - 11", "m = 4; y - 3 = 4 (x - 2); y = 4 x - 11",
              "m = 4; y + 3 = 4 (x - 2); y = 4 x + 11", "m = 4; y + 3 = 4 (x - 2)",
              "m = 4; y + 3 = 4 (x - 1); y = 4 x - 11", "m = 4; y + 3 = 4 x - 8; y = 4 x - 11"):
    assert B.check(dict(p, answer=wrong)) == "failed", wrong
p3 = dict(type="3", prompt="m = 2/3, (4, -3)", answer="y + 3 = 2/3 (x - 4); y = 2/3 x - 17/3")
assert B.check(p3) == "checked"
assert B.check(dict(p3, answer="y - 1 = 2/3 (x - 10); y = 2/3 x - 17/3")) == "failed", "Type 3: the given point"
p6 = dict(type="6", prompt="(-2, 5), (0, 4), (2, 3), (4, 2), (6, 1)", answer="y - 5 = -1/2 (x + 2); y = -1/2 x + 4")
assert B.check(p6) == "checked"
assert B.check(dict(p6, answer="y - 3 = -1/2 (x - 2); y = -1/2 x + 4")) == "checked", "any point of the table"
assert B.check(dict(p6, prompt="(-2, 5), (0, 4), (2, 3), (4, 2), (6, 0)")) == "failed", "not on one line"
assert B.check(dict(type="2", prompt="y - 3 = -(x - 1)", answer="y = -x + 4")) == "checked"
assert B.check(dict(type="2", prompt="y - 3 = -(x - 1)", answer="y = -1 x + 4")) == "failed"

# ---- showing: the key stacks the parts; Type 5's answer is the graph; Type 6 is a table, down the page
assert "#stack(" in B.answer_typst(p) and B.answer_typst(p).count("align(right)") == 3
assert B.answer_typst(dict(type="1", prompt="", answer="m = 4")) == "$display(m = 4)$"
g = dict(type="5", prompt="y + 3 = 2/3 (x - 4)", answer="y = 2/3 x - 17/3")
assert B.check(g) == "checked" and B.answer_typst(g) == ""
assert "circle(" not in B.typst(g) and B.key_typst(g).count("circle(") == len(B.si.lattice_points(F(2, 3), F(-17, 3)))
q, k = B.slide_typst(g), B.slide_typst(g, key=True)
assert q.startswith("#grid(columns: 2") and "circle(" not in q and "circle(" in k
assert B.slide_typst(p) is None
assert B.typst(p6).startswith("#table(columns: (2.2em, 2.2em)") and B.text(p6) == "x: -2  0  2  4  6   y: 5  4  3  2  1"
assert B.typst(p3) == "$display(m = display(2/3))$, through $display((4, -3))$"
assert B.text(p) == "(2, −3) and (5, 9)"

# ---- editing
new, status = B.from_edit("m = -1/2, (6, 2)", dict(type="3", prompt="", answer=""))
assert new["answer"] == "y - 2 = -1/2 (x - 6); y = -1/2 x + 5" and status == "checked" and new["source"] == "edited"
new, status = B.from_edit("(1,2),(3,8)", dict(type="4", prompt="", answer=""))
assert new["prompt"] == "(1, 2), (3, 8)" and new["answer"] == "m = 3; y - 2 = 3 (x - 1); y = 3 x - 1" and status == "checked"
new, status = B.from_edit("y − 2 = 3 (x + 1)", dict(type="5", prompt="", answer=""))
assert new["answer"] == "y = 3 x + 5" and status == "checked"
new, status = B.with_answer(dict(type="1", prompt="(2, -3), (5, 9)", answer=""), "m = 4")
assert status == "checked"

B.selftest(200, 2)
print("all point_slope_2_2 tests passed")
