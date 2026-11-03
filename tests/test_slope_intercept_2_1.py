"""Lesson 2-1: Slope-Intercept Form: every step draws, checks, and edits;
every line keeps the lesson's rules; the key's graph draws the line checked.

    python3 tests/test_slope_intercept_2_1.py
"""
import random
import re
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import slope_intercept_2_1 as B

lib = library.current()
assert "slope_intercept_2_1" in dict(lib.view("Algebra 1"))["Lessons"]
assert B.label(B.TYPE["1"]) == "Step 1" and B.heading("1") == "Step 1: Solve for y"

# ---- Step 1: six forms, spread evenly, every line in the rules
rng, seen = random.Random(5), set()
ps = [B.generate("1", rng, seen) for _ in range(60)]
assert Counter(p["form"] for p in ps) == {f: 10 for f in B.FORMS}, "a sheet's forms are spread evenly"
for p in ps:
    m, b = B.solved(p["prompt"])
    assert B.check(p) == "checked" and p["answer"] == B.slope_intercept(m, b)
    assert m != 0 and b.denominator == 1 and -9 <= b <= 9
    assert B.written_form(p["prompt"]) is None, "never already solved for y"
    pts = B.lattice_points(m, b)
    assert (0, b) in pts and any(x != 0 for x, _ in pts)
    assert all(-10 <= x <= 10 and -10 <= y <= 10 for x, y in pts)

# ---- each form, as written
assert [B.FORM[f](-2, 3, -4) for f in B.FORMS] == [
    "3 y = -2 x - 12", "3 y + 2 x = -12", "-2 x = 3 y + 12",
    "x = -3/2 y - 6", "-3/2 y = x + 6", "6 = -3/2 y - x"]
assert all(B.solved(B.FORM[f](-2, 3, -4)) == (F(-2, 3), -4) for f in B.FORMS)

# ---- the check reads the key's form
p = dict(prompt="x = 3/2 y + 6", answer="y = 2/3 x - 4")
assert B.check(p) == "checked"
for wrong in ("y = 4/6 x - 4", "y = -4 + 2/3 x", "y = 2/3 x + 0", "y = 2/3 x + 4", "y = 3/2 x - 4", "x = 3/2 y + 6"):
    assert B.check(dict(p, answer=wrong)) == "failed", wrong
assert B.check(dict(prompt="y - 2 x = 1", answer="y = 2 x + 1")) == "checked", "a whole-number slope is fine"
assert B.check(dict(prompt="y - x = 1", answer="y = x + 1")) == "checked"
assert B.check(dict(prompt="y - x = 1", answer="y = 1 x + 1")) == "failed", "x, not 1 x"
ws = [B.generate("1", random.Random(i), set()) for i in range(300)]
assert any(B.written_form(p["answer"])[0].denominator == 1 for p in ws), "whole-number slopes are drawn"
assert all(abs(m) <= 5 for m, _ in map(B.written_form, (p["answer"] for p in ws)) if m.denominator == 1)

# ---- Steps 1 and 3 each spread their own forms
rng, seen = random.Random(9), set()
ps = [B.generate(e, rng, seen) for e in "1" * 6 + "3" * 6]
assert sorted(p["form"] for p in ps[:6]) == sorted(p["form"] for p in ps[6:]) == list(B.FORMS)
assert B.check(dict(prompt="3 y = x + 30", answer="y = 1/3 x + 10")) == "failed", "the intercept is past 9"
assert B.check(dict(prompt="11 y = x + 22", answer="y = 1/11 x + 2")) == "failed", "no other lattice point on the graph"

# ---- editing
new, status = B.from_edit("2 x − 5 y = 10", dict(prompt="", answer="", form="B"))
assert new["answer"] == "y = 2/5 x - 2" and status == "checked" and new["source"] == "edited"
new, status = B.with_answer(dict(prompt="2 x - 5 y = 10"), "y = 2/5 x + 2")
assert status == "failed"
try:
    B.from_edit("2 x - 5 y", {})
    raise AssertionError("an expression isn't an equation")
except ValueError:
    pass

# ---- Step 2: graph a line given in slope-intercept form
rng, seen = random.Random(6), set()
for _ in range(40):
    p = B.generate("2", rng, seen)
    assert p["prompt"] == p["answer"] and B.written_form(p["prompt"]) and B.check(p) == "checked"
    assert B.answer_typst(p) == "" and "rect(" in B.typst(p) and "circle(" not in B.typst(p) and "circle(" in B.key_typst(p)
assert B.check(dict(type="2", prompt="3 y = 2 x - 12", answer="y = 2/3 x - 4")) == "failed", "Step 2 starts solved"

# ---- Step 3: a Step 1 form and a graph; the key solves and draws
rng, seen = random.Random(7), set()
ps = [B.generate("3", rng, seen) for _ in range(30)]
assert Counter(p["form"] for p in ps) == {f: 5 for f in B.FORMS}
for p in ps:
    assert B.check(p) == "checked" and B.answer_typst(p).startswith("$display(y =")
    m, b = B.written_form(p["answer"])
    assert all(f"({x}, {y})" in B.answer_text(p) for x, y in B.lattice_points(m, b))
    assert B.key_typst(p).count("circle(") == len(B.lattice_points(m, b))

# ---- slides: a larger graph beside the equation; the sheet's graph keeps its size
p = ps[0]
assert "#grid(columns: 2" in B.slide_typst(p) and "circle(" not in B.slide_typst(p)
assert B.slide_typst(p, key=True).count("circle(") == len(B.lattice_points(*B.written_form(p["answer"])))
q, k = B.slide_typst(p), B.slide_typst(p, key=True)
assert f"#hide[#text(fill: red)[{B.answer_typst(p)}]]" in q and f"#text(fill: red)[{B.answer_typst(p)}]" in k
assert "#hide" not in k, "the question's slide holds the answer hidden, so the graph never moves when it shows"
assert B.slide_typst(dict(type="1", prompt="3 y = x + 3", answer="y = 1/3 x + 1")) is None, "Step 1 slides as usual"
assert B.graph(p) != B.graph(p, width=B.SLIDE_WIDTH) and "#grid" not in B.typst(p)
assert "text(size: 6pt)[" in B.graph(p) and "text(size: 14pt)[" in B.slide_typst(p), "larger numbers on slides only"

# ---- Step 4: the line drawn, no equation; the key writes y = m x + b
rng, seen = random.Random(8), set()
for _ in range(40):
    p = B.generate("4", rng, seen)
    m, b = B.written_form(p["answer"])
    assert p["prompt"] == p["answer"] and p["form"] is None and B.check(p) == "checked" and B.fits(m, b)
    sheet, key = B.typst(p), B.key_typst(p)
    assert sheet == key, "the same graph on the sheet and the key"
    assert "line(" in sheet and "rgb" in sheet and "circle(" not in sheet and "$display" not in sheet, "the line, no points, no equation"
    assert B.answer_typst(p).startswith("$display(y =") and B.answer_text(p) == B.text(p)[len("[graph of "):-1]
    q, k = B.slide_typst(p), B.slide_typst(p, key=True)
    assert f"#hide[#text(fill: red)[{B.answer_typst(p)}]]" in q and "#hide" not in k
    assert q.replace(f"#hide[#text(fill: red)[{B.answer_typst(p)}]]", "") == k.replace(f"#text(fill: red)[{B.answer_typst(p)}]", ""), \
        "the slides differ only in showing the answer"
p = dict(type="4", form=None, prompt="y = 2/3 x - 4", answer="y = 2/3 x - 4")
assert B.check(B.with_answer(p, "y = 2/3 x + 4")[0]) == "failed"
assert B.check(dict(p, prompt="3 y = 2 x - 12")) == "failed", "Step 4's prompt is written y = m x + b"
new, status = B.from_edit("y = -1/2 x + 3", p)
assert status == "checked" and new["answer"] == "y = -1/2 x + 3" and new["prompt"] == "y = -1/2 x + 3"
assert "rgb(" not in B.graph(dict(p, prompt="y = x^2")), "an edited prompt that isn't a line: a blank graph"

# ---- Steps 2 and 3 say "Graph:" before the equation, on the sheet, the key, the slides, and the terminal
for t, prompt in (("2", "y = 2/3 x - 4"), ("3", "3 y = 2 x - 12")):
    p = dict(type=t, form=None, prompt=prompt, answer="y = 2/3 x - 4")
    eq = B.display(B.dfrac(prompt))
    assert B.typst(p).startswith("Graph: " + eq) and B.key_typst(p).startswith("Graph: " + eq)
    assert f"[Graph: {eq}" in B.slide_typst(p) and B.text(p).startswith("Graph: ")
    assert B.edit_text(p) == prompt, "the prompt itself stays the equation"
assert not B.typst(dict(type="1", prompt="3 y = x + 3", answer="y = 1/3 x + 1")).startswith("Graph")

# ---- each step's own instructions; the sheet's come from the step when there's one
assert [B.type_instructions(k) for k in B.KEYS] == [
    "Solve each equation for y. Write it in the form y = mx + b.", "Graph each line.", "Solve each equation for y, then graph it.",
    "Write the equation of each line in the form y = mx + b."] + [
    "Write the equation of the line through each pair of points in the form y = mx + b."] * 3 + [
    B.TYPE[k]["instructions"] for k in B.ESTIMATE]
assert all(B.type_instructions(k).startswith("Sketch the line through each pair of points.") for k in B.ESTIMATE)
assert [B.TYPE[k]["title"] for k in B.ESTIMATE] == ["Estimation Graphs 1", "Estimation Graphs 2", "Estimation Graphs 3"]

# ---- Steps 5 to 7: two points, neither on an axis; the key is the line through them
for step in B.POINTS:
    rng, seen = random.Random(10 + int(step)), set()
    for _ in range(80):
        p = B.generate(step, rng, seen)
        pts = B.points_of(p["prompt"])
        m, b = B.through(pts)
        assert p["form"] is None and B.check(p) == "checked" and p["answer"] == B.slope_intercept(m, b)
        assert B.written_form(p["answer"]) == (m, b) and m != 0
        assert pts[0][0] != pts[1][0] and pts[0][1] != pts[1][1]
        for x, y in pts:
            assert all(v != 0 and abs(v) <= 10 for v in (x, y)), "on the graph, and not an intercept"
            assert all(v.denominator in ((1,) if step != "7" else (1, 2, 4)) for v in (x, y)), "no thirds in Step 7"
        assert "/1)" not in p["prompt"] and "/1," not in p["prompt"], "an integer is written as an integer"
        if step == "5":
            assert b.denominator == 1 and b != 0 and abs(b) <= 10, "the intercept on the graph"
        if step == "7":
            assert m.denominator <= 12 and b.denominator <= 12 and abs(b) <= 10, "the intercept on the graph"
        assert B.typst(p).startswith("Through $display(") and " and $display(" in B.typst(p)
        assert B.text(p).startswith("Through (") and ") and (" in B.text(p)
        assert B.slide_typst(p) is None
ws = [B.generate("6", random.Random(i), set()) for i in range(200)]
assert any(B.written_form(p["answer"])[1].denominator > 1 for p in ws), "Step 6 draws fractional intercepts"

# ---- a fractional intercept in the key: lowest terms, read back exactly
assert B.written_form("y = 1/2 x + 7/2") == (F(1, 2), F(7, 2))
assert B.written_form("y = 1/2 x + 14/4") is None and B.written_form("y = 1/2 x + 4/2") is None
assert B.check(dict(type="6", prompt="(1, 4), (3, 5)", answer="y = 1/2 x + 7/2")) == "checked"
assert B.check(dict(type="6", prompt="(1, 4), (3, 5)", answer="y = 1/2 x - 7/2")) == "failed"
assert B.check(dict(type="5", prompt="(1, 4), (3, 5)", answer="y = 1/2 x + 7/2")) == "failed", "Step 5's b is an integer"
assert B.check(dict(type="5", prompt="(1, 2), (2, 4)", answer="y = 2 x")) == "failed", "Step 5's b isn't 0"
assert B.check(dict(type="6", prompt="(0, 4), (3, 5)", answer="y = 1/3 x + 4")) == "failed", "a point on an axis"
assert B.check(dict(type="6", prompt="(1, 4), (3, 12)", answer="y = 4 x")) == "failed", "past the graph"
assert B.check(dict(type="7", prompt="(1/2, 3), (5/2, -1)", answer="y = -2 x + 4")) == "checked"
assert B.check(dict(type="7", prompt="(1, 3), (5/2, -1)", answer="y = -8/3 x + 17/3")) == "checked", "an integer point is fine"
assert B.check(dict(type="7", prompt="(-3/4, 3), (-5, -23/3)", answer="y = 128/51 x + 83/17")) == "failed", "past twelfths"
assert B.check(dict(type="7", prompt="(-23/4, -8), (-6, -13/4)", answer="y = -19 x - 469/4")) == "failed", "Step 7's b is off the graph"
assert B.check(dict(type="5", prompt="(-6, -9), (-8, -1)", answer="y = -4 x - 33")) == "failed", "Step 5's b is off the graph"
ps = [B.generate("7", random.Random(i), set()) for i in range(300)]
assert any(any(x.denominator == y.denominator == 1 for x, y in B.points_of(p["prompt"])) for p in ps), \
    "an integer point now and then"
assert B.check(dict(type="7", prompt="(1/5, 3), (5/2, -1)", answer="y = -40/23 x + 77/23")) == "failed", "fifths"
assert B.check(dict(type="7", prompt="(2/4, 3), (5/2, -1)", answer="y = -2 x + 4")) == "unchecked", "not in lowest terms"

# ---- Step 7 shows a coordinate past 1 as a mixed number, and reads it back
assert [B.mixed(F(v)) for v in ("13/3", "-11/4", "1/2", "-3/4", "5", "-7")] == ["4 1/3", "-2 3/4", "1/2", "-3/4", "5", "-7"]
assert B.points_of("(4 1/3, -2 3/4), (13/3, 1/2)") == [(F(13, 3), F(-11, 4)), (F(13, 3), F(1, 2))]
for bad in ("(4 2/6, 1), (2, 3)", "(4 4/3, 1), (2, 3)", "(4 -1/3, 1), (2, 3)"):
    try:
        B.points_of(bad)
        raise AssertionError(bad)
    except ValueError:
        pass
rng, seen = random.Random(17), set()
for _ in range(80):
    p = B.generate("7", rng, seen)
    assert p["prompt"] == B.point_prompt(B.points_of(p["prompt"]))
    for x, y in B.points_of(p["prompt"]):
        for v in (x, y):
            assert (B.mixed(v) in p["prompt"]) and (abs(v) < 1 or v.denominator == 1 or " " in B.mixed(v))
old = dict(type="7", form=None, prompt="(9/2, 1), (-1/2, -11/4)", answer="")
assert B.text(old) == "Through (4 1/2, 1) and (−1/2, −2 3/4)", "a saved improper fraction shows mixed"
assert "4 display(1/2)" in B.typst(old) and "-2 display(3/4)" in B.typst(old)
new, status = B.from_edit("(9/2, 1), (1/2, -3)", old)
assert new["prompt"] == "(4 1/2, 1), (1/2, -3)" and new["answer"] == "y = x - 7/2" and status == "checked"
assert B.check(dict(type="7", prompt="(4 1/3, 1), (1/3, -3)", answer="y = x - 10/3")) == "failed", "no thirds in Step 7"

# ---- editing the points: the key is solved again
p = dict(type="6", form=None, prompt="(1, 4), (3, 5)", answer="y = 1/2 x + 7/2")
new, status = B.from_edit("(2, 3) and (5, 9)", p)
assert new["prompt"] == "(2, 3), (5, 9)" and new["answer"] == "y = 2 x - 1" and status == "checked"
new, status = B.from_edit("(2, 3), (2, 9)", p)
assert new["answer"] == p["answer"] and status == "failed", "a vertical line keeps the old key, marked"
try:
    B.from_edit("y = 2 x - 1", p)
    raise AssertionError("Steps 5 to 7 take two points")
except ValueError:
    pass

# ---- Steps 8 to 10: estimation graphs, two points and bare axes; the key sketches
GRAINS = {1: F(1, 10), 10: F(1, 2), 100: 1, 1000: 10, 10000: 100}
seen_scales = {k: set() for k in B.ESTIMATE}
for step in B.ESTIMATE:
    rng, seen = random.Random(20 + int(step)), set()
    for _ in range(150):
        p = B.generate(step, rng, seen)
        pts = B.points_of(p["prompt"])
        sx, sy = B.scales(step, pts)
        seen_scales[step].add((sx, sy))
        assert p["form"] is None and B.check(p) == "checked" and B.written_form(p["answer"]) == B.through(pts)
        assert p["prompt"] == B.point_prompt(pts, step) and "/" not in p["prompt"], "decimals, never fractions"
        for i, s in ((0, sx), (1, sy)):
            grain = 1 if step == "8" else GRAINS[s]
            vs = [pt[i] for pt in pts]
            assert all(v != 0 and abs(v) <= s and v % grain == 0 for v in vs)
            assert abs(vs[0] - vs[1]) >= F(s, 5) and (step == "8" or s == 1 or max(map(abs, vs)) > F(s, 10))
        assert abs(B.through(pts)[1]) <= sy, "the y-intercept on the graph"
        assert (step != "8" or (sx, sy) == (10, 10)) and (step != "9" or sx == sy) and (step != "10" or sx != sy)
        sheet, key = B.typst(p), B.key_typst(p)
        assert sheet.startswith("Sketch: $display(") and " and $display(" in sheet
        assert sheet.count("line(") == 2 and "content(" in sheet and "circle(" not in sheet, "bare axes: no ticks, no numbers"
        assert "luma(200)" not in sheet, "no grid"
        assert key.count("circle(") == 3 and "run " in key and "rise " in key and "b " in key
        assert key.count("stroke: 0.7pt)") == 2 + 8, "the axes, and four ticks on each"
        assert B.answer_typst(p) == "" and B.text(p).startswith("Sketch: (") and B.text(p).endswith("[axes]")
        assert B.answer_text(p).startswith("run ") and "y-intercept" in B.answer_text(p)
        q, k = B.slide_typst(p), B.slide_typst(p, key=True)
        assert q.startswith("#grid(columns: 2") and "run " in k and "run " not in q
        frame = lambda t: [l.strip() for l in t.splitlines() if l.strip().startswith("rect(")]
        assert len(frame(sheet)) == 1 and frame(sheet) == frame(key) and frame(q) == frame(k), \
            "the same frame on the question and the answer, so the graph never moves"
        (fx0, fy0), (fx1, fy1) = (tuple(map(float, c.split(", "))) for c in re.findall(r"\(([-\d.]+, [-\d.]+)\)", frame(k)[0]))
        for c in re.findall(r"content\(\(([-\d.]+), ([-\d.]+)\)", k):
            assert fx0 - 1e-6 <= float(c[0]) <= fx1 + 1e-6 and fy0 - 1e-6 <= float(c[1]) <= fy1 + 1e-6
assert seen_scales["8"] == {(10, 10)} and seen_scales["9"] == {(s, s) for s in GRAINS}
assert len(seen_scales["10"]) >= 12, "Step 10 mixes the scales"
assert B.decimal(F(9, 2)) == "4.5" and B.decimal(F(4500)) == "4500" and B.decimal(F(-3, 10)) == "-0.3"

p = dict(type="9", form=None, prompt="(0.3, -0.7), (-0.8, 0.4)", answer="y = -x - 2/5")
assert B.check(p) == "checked" and B.scales("9", B.points_of(p["prompt"])) == (1, 1)
assert B.check(dict(p, prompt="(0.35, -0.7), (-0.8, 0.4)", answer="y = -22/23 x - 91/230")) == "failed", "a multiple of 0.1"
assert B.check(dict(p, prompt="(3, -7), (-8, 4)", answer="y = -x - 4")) == "checked", "an axis to 10, by halves"
assert B.check(dict(p, prompt="(3, -70), (-8, 40)", answer="y = -10 x - 40")) == "failed", "Step 9's axes match"
assert B.check(dict(p, type="10", prompt="(3, -70), (-8, 40)", answer="y = -10 x - 40")) == "checked"
assert B.check(dict(p, type="10", prompt="(0.3, -0.7), (-0.8, 0.4)", answer="y = -x - 2/5")) == "failed", "Step 10's axes differ"
assert B.check(dict(p, prompt="(0.3, -0.7), (0.2, 0.4)", answer="y = -11 x + 13/5")) == "failed", "too close to draw a triangle"
assert B.check(dict(p, type="8", prompt="(9, 1), (8, 3)", answer="y = -2 x + 19")) == "failed", "b off the graph"
assert B.check(dict(p, type="8", prompt="(2.5, 1), (8, 3)", answer="y = 4/11 x + 1/11")) == "failed", "Step 8 is integers"
new, status = B.from_edit("(2.50, -7) and (-4, 3.5)", dict(p, type="9"))
assert new["prompt"] == "(2.5, -7), (-4, 3.5)" and new["answer"] == "y = -21/13 x - 77/26" and status == "checked"

B.selftest(300, 1)
print("all slope_intercept_2_1 tests passed")
