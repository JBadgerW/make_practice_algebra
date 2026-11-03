"""Lesson 2-1: Slope-Intercept Form: every step draws, checks, and edits;
every line keeps the lesson's rules; the key's graph draws the line checked.

    python3 tests/test_slope_intercept_2_1.py
"""
import random
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
    "Write the equation of each line in the form y = mx + b."]

B.selftest(300, 1)
print("all slope_intercept_2_1 tests passed")
