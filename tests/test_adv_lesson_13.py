"""Lesson 13 (Advanced Math): secants and tangents. Every source is reachable and checks
with the deck's answer; wrong answers fail; every type draws, checks, and keeps its rules;
every figure places its labels clear; edits solve again.

    python3 tests/test_adv_lesson_13.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_13 as B

lib = library.current()
assert "adv_lesson_13" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == ("Lesson 13: Secants and Tangents, Intersecting Secants, Intersecting Secants and Tangents, "
                   "Products of Chord Segments, Products of Secant and Tangent Segments")
assert all(B.type_instructions(k) == "Find x." for k in B.KEYS)

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 13.5", "2", "secants; far 80, near 30; pose 0", "x = 25"),
    ("ex 13.6", "3", "tangent and secant; far 170, back 120; pose 1", "x = 50"),
    ("ex 13.8", "4", "30, x + 20; 40, x + 10; pose 0", "x = 20"),
    ("ex 13.10", "6", "3, x; x, 3; pose 0", "x = 3"),
    ("ex 13.12", "7", "x, 12; 8; pose 1", "x = 4"),
    ("PS 4", "1", "30, 70; pose 0", "x = 50"),
    ("PS 5", "2", "secants; far 80, near 50; pose 0", "x = 15"),
    ("PS 6", "4", "3, 9; 5, x; pose 0", "x = 27/5"),
    ("PS 7", "5", "5, 7; 6, x; pose 0", "x = 4"),
]
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt, typ) == answer, (sid, B.answer_of(prompt, typ), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid
    assert B.drawable(typ, prompt), sid                                # its labels placed clear

# ---- every source is reachable: its template builds it from in-range parameters
KF, LF = "known first", "letter first"
REACH = {
    "ex 13.5": (B.t2_secants, dict(far=80, near=30, pose=0)),
    "ex 13.6": (B.t3_tangent, dict(far=170, back=120, pose=1)),
    "ex 13.8": (B.t4_linear, dict(n1=30, k1=20, n2=40, k2=10, o1=KF, o2=KF, pose=0)),
    "ex 13.10": (B.t6_cross, dict(a=3, b=3, flip=0, pose=0)),
    "ex 13.12": (B.t7_external, dict(x=4, i=12, pose=1)),
    "PS 4": (B.t1, dict(a=30, b=70, pose=0)),
    "PS 5": (B.t2_secants, dict(far=80, near=50, pose=0)),
    "PS 6": (B.t4_plain, dict(a=3, b=9, c=5, o=KF, pose=0)),
    "PS 7": (B.t5, dict(e1=5, i1=7, e2=6, flip=0, pose=0)),
}
prompt_of = {s[0]: s[2] for s in SOURCES}
type_of = {s[0]: s[1] for s in SOURCES}
assert set(REACH) == set(prompt_of)                                  # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[type_of[sid]]), sid  # a template of the source's own type
assert set(type_of.values()) == set(B.KEYS)                          # every type has a source
assert not B.in_range(B.t1, dict(a=50, b=50, pose=0))                 # equal arcs
assert not B.in_range(B.t2_secants, dict(far=80, near=60, pose=0))    # x under 15
assert not B.in_range(B.t3_tangent, dict(far=170, back=180, pose=0))  # a near arc of 10
assert not B.in_range(B.t4_plain, dict(a=3, b=9, c=3, o=KF, pose=0))  # x is just the other part
assert not B.in_range(B.t5, dict(e1=5, i1=7, e2=5, flip=0, pose=0))   # the same secant twice
assert not B.in_range(B.t7_external, dict(x=4, i=11, pose=0))         # no whole tangent

# ---- wrong answers fail
WRONG = [
    ("1", "30, 70; pose 0", "x = 20"),                                 # half the difference
    ("1", "30, 70; pose 0", "x = 100"),                                # not halved
    ("2", "secants; far 80, near 30; pose 0", "x = 55"),               # half the sum
    ("2", "secants; far 80, near 30; pose 0", "x = 50/2"),             # not in lowest terms
    ("3", "tangent and secant; far 170, back 120; pose 1", "x = 25"),  # the back arc taken as near
    ("3", "tangents; far 240; pose 0", "x = 120"),                     # the near arc
    ("4", "30, x + 20; 40, x + 10; pose 0", "x = 10"),
    ("4", "3, 9; 5, x; pose 0", "x = 5.4"),                            # a decimal
    ("4", "3, 9; 5, x; pose 0", "x = 15"),                             # 3 times 5 over 9... upside down
    ("5", "5, 7; 6, x; pose 0", "x = 10"),                             # 5 times 12 over 6, the whole secant
    ("5", "5, 7; 6, x; pose 0", "x = 35/6"),                           # external times internal
    ("6", "3, x; x, 3; pose 0", "x = -3"),                             # the rejected root
    ("6", "3, x; x, 3; pose 0", "x = 3, x = -3"),                      # both roots
    ("7", "x, 12; 8; pose 1", "x = -16"),
    ("7", "x, 12; 8; pose 1", "x = 8"),
    ("7", "x, 12; 8; pose 1", "y = 4"),                                # the wrong letter
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its rules
SHAPE = {
    "1": re.compile(r"\d+, \d+; pose [0-3]"),
    "2": re.compile(r"(secants|tangent and secant); far \d+, near \d+; pose [0-3]"),
    "3": re.compile(r"tangent and secant; far \d+, back \d+; pose [0-3]|tangents; (far|near) \d+; pose [0-3]"),
    "4": re.compile(r"(\d+, x \+ \d+|x \+ \d+, \d+); (\d+, x \+ \d+|x \+ \d+, \d+); pose [0-7]"
                    r"|\d+, \d+; (\d+, x|x, \d+); pose [0-7]"),
    "5": re.compile(r"(\d+, \d+; \d+, x|\d+, x; \d+, \d+); pose [0-3]"),
    "6": re.compile(r"(\d+, x; x, \d+|x, \d+; \d+, x|x, \d+; \d+, \d+|\d+, \d+; x, \d+); pose [0-3]"),
    "7": re.compile(r"(x, \d+; \d+|\d+, \d+; x|\d+, x; \d+); pose [0-3]"),
}
rng = random.Random(13)
for k in B.KEYS:
    for i in range(60):
        if i % 20 == 0:
            seen = set()                                               # a sheet's worth at a time
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert SHAPE[k].fullmatch(p["prompt"]), (k, p)
        assert B.drawable(k, p["prompt"]), p
        assert re.fullmatch(r"x = \d+(/\d+)?", p["answer"]), p
        assert "cetz.canvas" in B.typst(p) and B.slide_typst(p) is not None, p
        if k in "1237":
            assert "/" not in p["answer"], p                          # whole degrees; whole lengths
        if k == "2":                                                   # the near arc is given: no drift into Type 3
            assert "near" in p["prompt"], p
        if k == "3":                                                   # one intercepted arc missing
            assert not ("far" in p["prompt"] and "near" in p["prompt"]), p

# ---- showing: each problem says what to do
s = dict(type="2", prompt="secants; far 80, near 30; pose 0", answer="x = 25")
assert B.typst(s).startswith("Find $x$.")
assert B.text(s) == "Find x.   [figure: secants; far 80, near 30; pose 0]", B.text(s)
assert "#hide[" in B.slide_typst(s) and "#hide[" not in B.slide_typst(s, key=True)
assert B.answer_text(dict(type="4", prompt="3, 9; 5, x; pose 0", answer="x = 27/5")) == "x = 27/5"

# ---- editing: a new prompt is solved again; a typed answer is checked
p, status = B.from_edit("40, 100; pose 1", dict(type="1", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"] == "x = 70", p
p, status = B.with_answer(p, "x = 30")
assert status != "checked", p
p, status = B.from_edit("tangent and secant; far 150, near 50", dict(type="2", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = 50", p
p, status = B.from_edit("4, 8; 6, x; pose 2", dict(type="5", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = 2", p
p, status = B.from_edit("4, 12; x; pose 0", dict(type="7", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = 8", p
for typ, bad in (("1", "30; pose 0"), ("2", "secants; far 30, near 80"), ("3", "chords; far 170, back 120"),
                 ("5", "5, 7; 6, 8"), ("7", "x, 12")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_13: ok")
