"""Lesson 6 (Advanced Math): fractional equations, radical equations, systems of
three linear equations. Every source is reachable from in-range parameters and
checks with the deck's answer; wrong answers fail; every type draws and keeps
its shape; edits solve again.

    python3 tests/test_adv_lesson_6.py
"""
import random, re
import sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_6 as B

lib = library.current()
assert "adv_lesson_6" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 6: Fractional Equations, Radical Equations, Systems of Three Linear Equations"
assert all(B.type_instructions(k) == "Solve." for k in B.KEYS)

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 6.1", "1", "4/7 + 3/(x + 2) = 5/3", "x = 17/23"),
    ("PS 5", "1", "4/7 + 3/(x + 3) = 5/3", "x = -6/23"),
    ("PS 6", "1", "5/3 - 2/(x - 4) = 1/2", "x = 40/7"),
    ("PS 7", "1", "1/(x - 7) + 1/4 = 1/3", "x = 19"),
    ("ex 6.2", "2", "3/7 x + 2/5 y = 11; 0.03x - 0.2y = -0.37", "(21, 5)"),
    ("PS 10", "2", "3/7 x + 2/5 y = 11; 0.03x - 0.2y = -0.37", "(21, 5)"),
    ("ex 6.3", "3", "root(3, x - 5) - 2 = 2", "x = 69"),
    ("ex 6.4", "4", "sqrt(s - 48) + sqrt(s) = 8", "s = 49"),
    ("PS 8", "4", "sqrt(s - 7) + sqrt(s) = 7", "s = 16"),
    ("PS 9", "4", "sqrt(s - 27) + sqrt(s) = 9", "s = 36"),
    ("ex 6.5", "5", "2x + 2y - z = 14; 3x + 3y + z = 16; x - 2y = 0", "(4, 2, -2)"),
    ("PS 11", "5", "2x + 3y = -1; x - 2z = -3; 2y - z = -4", "(1, -1, 2)"),
    ("ex 6.6", "6", "x + 2y + z = 4; 2x - y - z = 0; 2x - 2y + z = 1", "(1, 1, 1)"),
    ("PS 12", "6", "x - 2y + z = -2; 2x - 2y - z = -3; x + y - 2z = 1", "(1, 2, 1)"),
]
prompt_of = {s[0]: s[2] for s in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt, typ) == answer, (sid, B.answer_of(prompt, typ), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source in exactly one type, and every type has a source
TYPE_OF = {s[0]: s[1] for s in SOURCES}
assert len(TYPE_OF) == len(SOURCES) == 14
assert set(TYPE_OF.values()) == set(B.KEYS)

# ---- every source is reachable: its template builds it from in-range parameters
F = Fraction
REACH = {
    "ex 6.1": (B.t1, dict(x="x", order="number first", p=4, q=7, sign=1, k=3, c=2, s=5, t=3)),
    "PS 5": (B.t1, dict(x="x", order="number first", p=4, q=7, sign=1, k=3, c=3, s=5, t=3)),
    "PS 6": (B.t1, dict(x="x", order="number first", p=5, q=3, sign=-1, k=2, c=-4, s=1, t=2)),
    "PS 7": (B.t1, dict(x="x", order="unknown first", p=1, q=4, sign=1, k=1, c=-7, s=1, t=3)),
    "ex 6.2": (B.t2, dict(a=3, b=7, c=2, d=5, e=F(3, 100), f=F(-2, 10), x=21, y=5)),
    "PS 10": (B.t2, dict(a=3, b=7, c=2, d=5, e=F(3, 100), f=F(-2, 10), x=21, y=5)),
    "ex 6.3": (B.t3, dict(x="x", k=1, b=-5, sign=-1, c=2, v=4)),
    "ex 6.4": (B.t4, dict(x="s", m=7, j=1, order="bare last")),
    "PS 8": (B.t4, dict(x="s", m=4, j=3, order="bare last")),
    "PS 9": (B.t4, dict(x="s", m=6, j=3, order="bare last")),
    "ex 6.5": (B.t5, dict(rows=((2, 2, -1), (3, 3, 1), (1, -2, 0)), sol=(4, 2, -2))),
    "PS 11": (B.t5, dict(rows=((2, 3, 0), (1, 0, -2), (0, 2, -1)), sol=(1, -1, 2))),
    "ex 6.6": (B.t6, dict(rows=((1, 2, 1), (2, -1, -1), (2, -2, 1)), sol=(1, 1, 1))),
    "PS 12": (B.t6, dict(rows=((1, -2, 1), (2, -2, -1), (1, 1, -2)), sol=(1, 2, 1))),
}
assert set(REACH) == set(prompt_of)                                  # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid   # a template of the source's own type
    if build in B.KEY:                                               # the draw's key is the deck's
        assert B.KEY[build](**params) == dict((s[0], s[3]) for s in SOURCES)[sid], sid
# out of range is out
assert not B.in_range(B.t1, dict(x="x", order="number first", p=4, q=7, sign=1, k=3, c=0, s=5, t=3))
assert not B.in_range(B.t2, dict(a=3, b=7, c=2, d=5, e=F(3, 100), f=F(-2, 10), x=20, y=5))   # constant not whole
assert not B.in_range(B.t4, dict(x="s", m=4, j=4, order="bare last"))                      # sqrt(s) + sqrt(s)
assert not B.in_range(B.t5, dict(rows=((1, 2, 1), (2, -1, -1), (2, -2, 1)), sol=(1, 1, 1)))  # a Type 6 system
assert not B.in_range(B.t6, dict(rows=((2, 3, 0), (1, 0, -2), (0, 2, -1)), sol=(1, -1, 2)))  # a Type 5 system
assert not B.in_range(B.t6, dict(rows=((1, 2, 1), (2, 4, 2), (2, -2, 1)), sol=(1, 1, 1)))    # singular

# ---- wrong answers fail
WRONG = [
    ("1", "4/7 + 3/(x + 2) = 5/3", "x = 17/23 + 1"),
    ("1", "4/7 + 3/(x + 2) = 5/3", "x = 34/46"),              # not in lowest terms
    ("1", "4/7 + 3/(x + 3) = 5/3", "x = 6/23"),               # a sign error
    ("1", "1/(x - 7) + 1/4 = 1/3", "y = 19"),                 # the wrong letter
    ("2", "3/7 x + 2/5 y = 11; 0.03x - 0.2y = -0.37", "(5, 21)"),
    ("2", "3/7 x + 2/5 y = 11; 0.03x - 0.2y = -0.37", "(21, -5)"),
    ("3", "root(3, x - 5) - 2 = 2", "x = 59"),
    ("3", "root(3, x - 5) - 2 = 2", "x = 21"),                # squared instead of cubed
    ("4", "sqrt(s - 48) + sqrt(s) = 8", "s = 7"),             # sqrt(s), not s
    ("4", "sqrt(s - 7) + sqrt(s) = 7", "s = 9"),
    ("5", "2x + 2y - z = 14; 3x + 3y + z = 16; x - 2y = 0", "(4, 2, 2)"),
    ("5", "2x + 3y = -1; x - 2z = -3; 2y - z = -4", "(1, -1)"),
    ("6", "x + 2y + z = 4; 2x - y - z = 0; 2x - 2y + z = 1", "(1, 1, 2)"),
    ("6", "x - 2y + z = -2; 2x - 2y - z = -3; x + y - 2z = 1", "(2, 1, 1)"),
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"(-?\d+/\d+ [+-] \d/\([a-z] [+-] \d\)|\d/\([a-z] [+-] \d\) [+-] \d+/\d+) = \d+/\d+",
    "2": r"\d/\d x [+-] \d/\d y = -?\d+; \d\.\d+x [+-] \d\.\d+y = -?\d+(\.\d+)?",
    "3": r"root\(3, (\d )?[a-z] [+-] \d\) [+-] \d = -?\d+",
    "4": r"(sqrt\([a-z] [+-] \d+\) \+ sqrt\([a-z]\)|sqrt\([a-z]\) \+ sqrt\([a-z] [+-] \d+\)) = \d+",
}
ANSWER = {"1": r"[a-z] = -?\d+(/\d+)?", "3": r"[a-z] = -?\d+(/\d+)?", "4": r"[a-z] = \d+",
          "2": r"\(-?\d+, -?\d+\)", "5": r"\(-?\d+, -?\d+, -?\d+\)", "6": r"\(-?\d+, -?\d+, -?\d+\)"}
rng = random.Random(6)
for k in B.KEYS:
    seen = set()
    for _ in range(80):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.fullmatch(ANSWER[k], p["answer"]), p
        if k in SHAPE:
            assert re.fullmatch(SHAPE[k], p["prompt"]), p
        else:
            eqs = p["prompt"].split("; ")
            assert len(eqs) == 3 and not re.search(r"\b1[xyz]", p["prompt"]), p
            missing = [sum(v not in e.split("=")[0] for v in "xyz") for e in eqs]
            if k == "5":
                assert sorted(missing) in ([0, 0, 1], [1, 1, 1]), p
            else:
                assert missing == [0, 0, 0], p
        if k == "4":
            assert int(p["answer"].split("= ")[1]) ** 0.5 % 1 == 0, p   # sqrt(s) is whole

# ---- showing
s = dict(type="2", prompt="3/7 x + 2/5 y = 11; 0.03x - 0.2y = -0.37", answer="(21, 5)")
t = B.typst(s)
assert t == "$display(cases(gap: #0.8em, display(3/7) x + display(2/5) y = 11, 0.03x - 0.2y = -0.37))$", t
assert B.answer_typst(s) == "$(21, 5)$"
assert B.text(s) == "⎰ 3/7 x + 2/5 y = 11\n⎱ 0.03x − 0.2y = −0.37", B.text(s)
s = dict(type="5", prompt="2x + 3y = -1; x - 2z = -3; 2y - z = -4", answer="(1, -1, 2)")
assert B.typst(s).count(";") == 2 and B.text(s).startswith("⎧ 2x + 3y = −1"), B.text(s)
s = dict(type="1", prompt="4/7 + 3/(x + 2) = 5/3", answer="x = 17/23")
assert "display(4/7)" in B.typst(s), B.typst(s)
assert B.answer_text(s) == "x = 17/23"

# ---- editing: a new prompt is solved again; a typed answer is checked
p, status = B.from_edit("sqrt(s − 20) + sqrt(s) = 10", dict(type="4", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"] == "s = 36", p
p, status = B.with_answer(p, "s = 16")
assert status != "checked", p
p, status = B.from_edit("x + y + z = 6 ; x - y = 0 ; 2x - z = -2", dict(type="5", prompt="", answer=""))
assert status == "checked" and p["prompt"] == "x + y + z = 6; x - y = 0; 2x - z = -2" and p["answer"] == "(1, 1, 4)", p
assert B.edit_text(p) == "x + y + z = 6 ; x - y = 0 ; 2x - z = -2"
p, status = B.from_edit("1/2 x + 1/3 y = 5; 0.1x + 0.2y = 1.4", dict(type="2", prompt="", answer=""))
assert status == "checked" and p["answer"] == "(8, 3)", p
p, status = B.from_edit("root(3, 2x + 3) + 1 = 4", dict(type="3", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = 12", p
p, status = B.from_edit("5/3 - 2/(x - 4) = 1/2", dict(type="1", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = 40/7", p
for typ, bad in (("1", "4/7 + 3/(x + "), ("5", "x + y = ; y = 2")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError("unreadable")
    except ValueError:
        pass

print("adv_lesson_6: ok")
