"""Lesson 20 (Advanced Math): two special triangles. Every type draws and checks;
the deck's own problems check with the deck's answers; wrong and unsimplified
answers fail; edits solve again.

    python3 tests/test_adv_lesson_20.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_20 as B

lib = library.current()
assert "adv_lesson_20" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 20: Two Special Triangles"
assert B.type_instructions("1").startswith("Draw the necessary reference triangle")

# ---- the deck's problems, with the deck's answers
DECK = [
    ("1", "tan(30 degree)", "sqrt(3)/3"),                       # example 20.1
    ("1", "7 sin(45 degree)", "(7 sqrt(2))/2"),                 # example 20.2
    ("2", "4 sqrt(3) cos(60 degree)", "2 sqrt(3)"),             # example 20.3
    ("3", "10/sqrt(5) tan(45 degree)", "2 sqrt(5)"),            # example 20.4
    ("2", "6 sqrt(2) cos(30 degree)", "3 sqrt(6)"),             # problem 9
    ("2", "6 sqrt(3) sin(45 degree)", "3 sqrt(6)"),             # problem 10
    ("1", "4 tan(60 degree)", "4 sqrt(3)"),                     # problem 11
]
for typ, prompt, answer in DECK:
    assert B.answer_of(prompt) == answer, (prompt, B.answer_of(prompt), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", (prompt, answer)

# ---- wrong or unfinished answers fail
WRONG = [
    ("tan(30 degree)", "1/sqrt(3)"),                            # not rationalized
    ("tan(30 degree)", "sqrt(3)"),                              # the wrong ratio
    ("7 sin(45 degree)", "7/sqrt(2)"),
    ("6 sqrt(2) cos(30 degree)", "(6 sqrt(6))/2"),              # not reduced
    ("6 sqrt(2) cos(30 degree)", "sqrt(54)"),                   # a square under the radical
    ("6 sqrt(3) sin(45 degree)", "6 sqrt(3) sin(45 degree)"),   # not evaluated
    ("10/sqrt(5) tan(45 degree)", "(10 sqrt(5))/5"),
    ("4 tan(60 degree)", "2 sqrt(12)"),
]
for prompt, answer in WRONG:
    got = B.check(dict(type="1", prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its rules
rng = random.Random(20)
for k in B.KEYS:
    seen = set()
    for _ in range(60):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.search(r"(sin|cos|tan)\((30|45|60) degree\)$", p["prompt"]), p
        assert ("sqrt" in p["prompt"]) == (k != "1"), p
        assert ("/" in p["prompt"]) == (k == "3"), p
        assert not re.search(r"\b1 ", p["prompt"]) and not re.search(r"\b1 sqrt", p["answer"]), p

# ---- showing: sin 30°, the fraction in display style
s = dict(type="3", prompt="10/sqrt(5) tan(45 degree)", answer="2 sqrt(5)")
assert B.typst(s) == "$display(display(10/sqrt(5)) tan 45 degree)$", B.typst(s)
assert B.text(s) == "10/sqrt(5) tan 45°", B.text(s)
assert B.answer_typst(dict(s, answer="sqrt(3)/3")) == "$display(display(sqrt(3)/3))$"

# ---- editing: a new prompt is solved again; a typed answer is checked
p, status = B.from_edit("8 sin(60°)", dict(type="1", prompt="", answer="", source="template"))
assert status == "checked" and p["prompt"] == "8 sin(60 degree)" and p["answer"] == "4 sqrt(3)", p
p, status = B.with_answer(p, "4 sqrt(3)")
assert status == "checked", p
p, status = B.with_answer(p, "8 sqrt(3)/2")
assert status != "checked", p
try:
    B.from_edit("8 sin(", dict(type="1", prompt="", answer="")); raise AssertionError("unreadable")
except ValueError:
    pass

print("adv_lesson_20: ok")
