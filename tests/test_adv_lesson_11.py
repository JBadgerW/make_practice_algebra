"""Lesson 11 (Advanced Math): circles, the quadratic formula. Every source is reachable
and checks with the deck's answer; wrong answers fail; every type draws, checks, and keeps
its rules; every figure places its labels clear; edits solve again.

    python3 tests/test_adv_lesson_11.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_11 as B

lib = library.current()
assert "adv_lesson_11" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 11: Circles, Properties of Circles, The Quadratic Formula"
assert B.type_instructions("2") == "Find x, y, and z."
assert B.type_instructions("6") == "Use the quadratic formula to solve."
assert "$" not in "".join(B.type_instructions(k) for k in B.KEYS)   # instructions are plain text

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 11.1", "1", "46, x + 10; 30, y + 20; pose 0", "x = 36, y = 10"),
    ("ex 11.2", "2", "75, 80; 50; pose 0", "x = 100, y = 105, z = 110"),
    ("ex 11.3", "3", "35, 75; pose 0", "x = 150, y = 70, z = 140"),
    ("ex 11.4", "4", "15, x + 10; 20, x + 5; pose 0", "x = 10"),
    ("ex 11.5", "5", "x + 4, 6; x + y, 10; x, x; pose 0", "x = 2, y = 8"),
    ("ex 11.6", "6", "3 x^2 - 2 x + 5 = 0", "x = 1/3 plus.minus sqrt(14)/3 i"),
    ("PS 5", "1", "y + 13, 38; x + 16, 54; pose 1", "x = 38, y = 25"),
    ("PS 6", "4", "24, x + 5; x + 15, 12; pose 0", "x = 5"),
    ("PS 7", "5", "x + 3, 7; x + y, 19; x, x; pose 0", "x = 4, y = 15"),
    ("PS 9", "6", "3 x^2 + 2 x + 5 = 0", "x = -1/3 plus.minus sqrt(14)/3 i"),
    ("PS 10", "6", "-x = -3 x^2 + 4", "x = 4/3 or x = -1"),
]
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt, typ) == answer, (sid, B.answer_of(prompt, typ), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid
    if typ in B.FIGURES:
        assert B.drawable(typ, prompt), sid                            # its labels placed clear

# ---- every source is reachable: its template builds it from in-range parameters
KF, LF = "known first", "letter first"
REACH = {
    "ex 11.1": (B.t1, dict(k1=46, c1=10, k2=30, c2=20, l1="x", o1=KF, o2=KF, pose=0)),
    "ex 11.2": (B.t2, dict(v1=75, v4=80, a2=50, pose=0)),
    "ex 11.3": (B.t3, dict(a=35, b=75, pose=0)),
    "ex 11.4": (B.t4, dict(n1=15, k1=10, n2=20, k2=5, o1=KF, o2=KF, pose=0)),
    "ex 11.5": (B.t5, dict(a=4, n1=6, n2=10, f1=0, f2=0, pose=0)),
    "ex 11.6": (B.t6, dict(v="x", a=3, b=-2, c=5)),
    "PS 5": (B.t1, dict(k1=38, c1=13, k2=54, c2=16, l1="y", o1=LF, o2=LF, pose=1)),
    "PS 6": (B.t4, dict(n1=24, k1=5, n2=12, k2=15, o1=KF, o2=LF, pose=0)),
    "PS 7": (B.t5, dict(a=3, n1=7, n2=19, f1=0, f2=0, pose=0)),
    "PS 9": (B.t6, dict(v="x", a=3, b=2, c=5)),
    "PS 10": (B.t6_moved, dict(v="x", a=3, b=-1, c=-4, s=-1)),
}
prompt_of = {s[0]: s[2] for s in SOURCES}
type_of = {s[0]: s[1] for s in SOURCES}
assert set(REACH) == set(prompt_of)                                  # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[type_of[sid]]), sid  # a template of the source's own type
assert set(type_of.values()) == set(B.KEYS)                          # every type has a source
assert not B.in_range(B.t1, dict(k1=70, c1=10, k2=60, c2=20, l1="x", o1=KF, o2=KF, pose=0))   # top arc too small
assert not B.in_range(B.t2, dict(v1=75, v4=80, a2=150, pose=0))                                 # an arc below 40°
assert not B.in_range(B.t3, dict(a=85, b=75, pose=0))                                           # a third angle under 30°
assert not B.in_range(B.t4, dict(n1=15, k1=10, n2=15, k2=10, o1=KF, o2=KF, pose=0))            # no x to find
assert not B.in_range(B.t5, dict(a=13, n1=15, n2=25, f1=0, f2=0, pose=0))                       # a sliver of a triangle

# ---- wrong answers fail
WRONG = [
    ("1", "46, x + 10; 30, y + 20; pose 0", "x = 10, y = 36"),        # the pairs crossed
    ("1", "46, x + 10; 30, y + 20; pose 0", "y = 10, x = 36"),        # not in order
    ("1", "46, x + 10; 30, y + 20; pose 0", "x = 36"),                # y missing
    ("2", "75, 80; 50; pose 0", "x = 105, y = 100, z = 110"),         # the opposite angles crossed
    ("2", "75, 80; 50; pose 0", "x = 100, y = 105, z = 160"),         # the arc not less the 50
    ("3", "35, 75; pose 0", "x = 70, y = 150, z = 140"),              # each arc beside its angle
    ("3", "35, 75; pose 0", "x = 75, y = 35, z = 250"),               # not doubled
    ("4", "15, x + 10; 20, x + 5; pose 0", "x = 5"),
    ("4", "15, x + 10; 20, x + 5; pose 0", "x = 20/2"),               # not in lowest terms
    ("5", "x + 4, 6; x + y, 10; x, x; pose 0", "x = 2, y = 10"),      # y = 10 - 0
    ("6", "3 x^2 - 2 x + 5 = 0", "x = 1/3 plus.minus sqrt(56)/6 i"),  # not simplified
    ("6", "3 x^2 - 2 x + 5 = 0", "x = -1/3 plus.minus sqrt(14)/3 i"), # -b taken as b
    ("6", "-x = -3 x^2 + 4", "x = 1/6 plus.minus 7/6"),               # rational roots, not split
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its rules
SHAPE = {
    "1": re.compile(r"(\d+, [xy] \+ \d+|[xy] \+ \d+, \d+); (\d+, [xy] \+ \d+|[xy] \+ \d+, \d+); pose [0-3]"),
    "2": re.compile(r"\d+, \d+; \d+; pose [0-3]"),
    "3": re.compile(r"\d+, \d+; pose [0-3]"),
    "4": re.compile(r"(\d+, x \+ \d+|x \+ \d+, \d+); (\d+, x \+ \d+|x \+ \d+, \d+); pose [0-7]"),
    "5": re.compile(r"(x \+ \d+, \d+|\d+, x \+ \d+); (x \+ y, \d+|\d+, x \+ y); x, x; pose [0-3]"),
    "6": re.compile(r"[^=]*[a-z]\^2[^=]*= .*|.* = [^=]*[a-z]\^2.*"),
}
rng = random.Random(11)
for k in B.KEYS:
    seen = set()
    for _ in range(60):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert SHAPE[k].fullmatch(p["prompt"]), (k, p)
        if k in B.FIGURES:
            assert B.drawable(k, p["prompt"]), p
            assert all(int(v) > 0 for v in re.findall(r"= (\d+)", p["answer"])), p
            assert "cetz.canvas" in B.typst(p) and B.slide_typst(p) is not None, p
        else:
            assert " or " in p["answer"] or "plus.minus" in p["answer"], p
        assert not re.search(r"(^|[ (])1 [a-z(]", p["prompt"]), p       # no 1 x

# ---- showing: each problem says what to do
s = dict(type="5", prompt="x + 4, 6; x + y, 10; x, x; pose 0", answer="x = 2, y = 8")
assert B.typst(s).startswith("The triangle and the circle are tangent at three points, as shown. Find $x$ and $y$.")
assert B.text(s) == "The triangle and the circle are tangent at three points, as shown. Find x and y.   [figure: x + 4, 6; x + y, 10; x, x; pose 0]", B.text(s)
assert "#hide[" in B.slide_typst(s) and "#hide[" not in B.slide_typst(s, key=True)
q = dict(type="6", prompt="3 x^2 - 2 x + 5 = 0", answer="x = 1/3 plus.minus sqrt(14)/3 i")
assert B.text(q) == "Use the quadratic formula to solve: 3 x^2 − 2 x + 5 = 0", B.text(q)
assert B.answer_text(q) == "x = 1/3 ± sqrt(14)/3 i", B.answer_text(q)
assert B.slide_typst(q) is None

# ---- editing: a new prompt is solved again; a typed answer is checked
p, status = B.from_edit("40, x + 5; y + 10, 35", dict(type="1", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"] == "x = 35, y = 25", p
p, status = B.with_answer(p, "x = 25, y = 35")
assert status != "checked", p
p, status = B.from_edit("12, x + 2; 8, x + 6; pose 2", dict(type="4", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = 6", p
p, status = B.from_edit("x^2 + 2 x - 4 = 0", dict(type="6", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = -1 plus.minus sqrt(5)", p
for typ, bad in (("1", "46, x + 10"), ("3", "120, 75; pose 0"), ("4", "15, x + 10; 15, x + 10"), ("6", "x + 2 = 0")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_11: ok")
