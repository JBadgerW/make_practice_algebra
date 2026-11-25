"""Lesson 27 (Advanced Math): related angles, signs of trigonometric functions.
Every source is reachable from in-range parameters and checks with the deck's
answer; wrong and unfinished answers fail; every type draws, checks, and keeps
its shape; edits solve again.

    python3 tests/test_adv_lesson_27.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_27 as B

lib = library.current()
assert "adv_lesson_27" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 27: Related Angles, Signs of Trigonometric Functions"
assert B.type_instructions("1") == B.type_instructions("2") == \
    "Draw the necessary reference triangles and evaluate. Do not use a calculator."
assert B.type_instructions("3") == "Do not use a calculator."

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 27.1", "1", "4 cos(135 degree)", "-2 sqrt(2)"),
    ("ex 27.2", "2", "-2 cos(-150 degree)", "sqrt(3)"),
    ("ex 27.3", "1", "5/3 cos(300 degree)", "5/6"),
    ("PS 16", "1", "3 cos(300 degree)", "3/2"),
    ("PS 18", "3", "f(x) = -2 cos(x); f(-300 degree)", "f(-300 degree) = -1"),     # the deck: -1
]
prompt_of = {s[0]: s[2] for s in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 27.1": (B.t1, dict(n=4, d=1, f="cos", a=135)),
    "ex 27.2": (B.t2, dict(n=-2, d=1, f="cos", a=-150)),
    "ex 27.3": (B.t1, dict(n=5, d=3, f="cos", a=300)),
    "PS 16": (B.t1, dict(n=3, d=1, f="cos", a=300)),
    "PS 18": (B.t3, dict(g="f", n=-2, d=1, f="cos", a=-300)),
}
assert set(REACH) == set(prompt_of)                                    # nothing left out
TYPE_OF = {s[0]: s[1] for s in SOURCES}
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert sorted(set(TYPE_OF.values())) == B.KEYS                          # every type has a source
assert B.POSITIVE == (120, 135, 150, 210, 225, 240, 300, 315, 330)
assert set(B.NEGATIVE) == {-a for a in B.POSITIVE} | {-30, -45, -60}
# out of range
assert not B.in_range(B.t1, dict(n=4, d=1, f="cos", a=45))              # first quadrant: Lesson 20's
assert not B.in_range(B.t1, dict(n=4, d=1, f="cos", a=-135))            # negative: Type 2's
assert not B.in_range(B.t2, dict(n=4, d=1, f="cos", a=135))
assert not B.in_range(B.t1, dict(n=6, d=3, f="cos", a=135))             # 6/3 is not in lowest terms
assert not B.in_range(B.t1, dict(n=0, d=1, f="cos", a=135))
assert not B.in_range(B.t3, dict(g="x", n=-2, d=1, f="cos", a=-300))

# ---- quadrants and related angles
assert [B.quadrant(a) for a in (135, -150, 300, -300)] == [2, 3, 4, 1]
assert [B.related(a) for a in (135, -150, 300, -300, 210)] == [45, 30, 60, 60, 30]

# ---- wrong or unfinished answers fail
WRONG = [
    ("4 cos(135 degree)", "2 sqrt(2)"),                         # the sign of the second quadrant
    ("4 cos(135 degree)", "-4/sqrt(2)"),                        # not rationalized
    ("4 cos(135 degree)", "-(4 sqrt(2))/2"),                    # not reduced
    ("4 cos(135 degree)", "-sqrt(8)"),                          # a square under the radical
    ("-2 cos(-150 degree)", "-sqrt(3)"),                        # -150° taken in the second quadrant
    ("-2 cos(-150 degree)", "1"),                               # sin 30° for cos 30°
    ("5/3 cos(300 degree)", "-5/6"),                            # cosine is positive in the fourth
    ("5/3 cos(300 degree)", "10/12"),
    ("3 cos(300 degree)", "3 cos(60 degree)"),                  # not evaluated
    ("f(x) = -2 cos(x); f(-300 degree)", "f(-300 degree) = 1"),
    ("f(x) = -2 cos(x); f(-300 degree)", "-1"),                 # doesn't name what it finds
    ("f(x) = -2 cos(x); f(-300 degree)", "f(300 degree) = -1"),
]
for prompt, answer in WRONG:
    typ = "3" if ";" in prompt else "1"
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^(-?\d+ |-?\d+/\d+ |-)?(sin|cos|tan)\((\d+) degree\)$",
    "2": r"^(-?\d+ |-?\d+/\d+ |-)?(sin|cos|tan)\((-\d+) degree\)$",
    "3": r"^([fgh])\(x\) = (-?\d+ |-?\d+/\d+ |-)?(sin|cos|tan)\(x\); \1\((-?\d+) degree\)$",
}
rng = random.Random(27)
for k in B.KEYS:
    seen = set()
    for i in range(200):
        if i % 50 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        m = re.match(SHAPE[k], p["prompt"])
        assert m, p
        a = int(m.groups()[-1])
        assert B.related(a) in (30, 45, 60) and a % 90, p
        if k == "1":
            assert B.quadrant(a) > 1, p
        if k == "2":
            assert a < 0, p
        assert not re.search(r"(?<![\d/])1 (sin|cos|tan)|\b0 ", p["prompt"]), p
        assert not re.search(r"(sin|cos|tan)", p["answer"]), p
        if k == "3":
            assert p["answer"].startswith(p["prompt"].split("; ")[1] + " = "), p

# ---- showing: a negative angle keeps its parentheses; the fraction in display style
p = dict(type="2", prompt=prompt_of["ex 27.2"], answer="sqrt(3)")
assert B.typst(p) == "Evaluate: #h(0.5em) $display(-2 cos(-150 degree))$", B.typst(p)
assert B.text(p) == "Evaluate: −2 cos(−150°)", B.text(p)
p = dict(type="1", prompt=prompt_of["ex 27.3"], answer="5/6")
assert "display(5/3) cos 300 degree" in B.typst(p), B.typst(p)
p = dict(type="3", prompt=prompt_of["PS 18"], answer="f(-300 degree) = -1")
assert B.typst(p) == "If $f(x) = -2 cos x$, find $f(-300 degree)$.", B.typst(p)
assert B.text(p) == "If f(x) = −2 cos x, find f(−300°).", B.text(p)
assert B.answer_text(p) == "f(−300°) = −1"

# ---- editing: new numbers are solved again
src = {s[0]: dict(type=s[1], prompt=s[2], answer=s[3], source="template") for s in SOURCES}
p, status = B.from_edit("6 cos(135°)", src["ex 27.1"])
assert status == "checked" and p["answer"] == "-3 sqrt(2)", p
p, status = B.from_edit("f(x) = -2 sin(x); f(-300 degree)", src["PS 18"])
assert status == "checked" and p["answer"] == "f(-300 degree) = -sqrt(3)", p
p, status = B.with_answer(src["ex 27.3"], "5/6")
assert status == "checked", p
p, status = B.with_answer(src["ex 27.3"], "-5/6")
assert status == "failed", p
try:
    B.from_edit("cos of 135", src["ex 27.1"]); raise AssertionError("unreadable")
except ValueError:
    pass

print("adv_lesson_27: ok")
