"""Lesson 12 (Advanced Math): polygons, angles and diagonals. Every source is reachable and
checks with the deck's answer; wrong answers fail; every type draws and checks; the figure is
drawn on the sheet and triangulated on the key; edits solve again.

    python3 tests/test_adv_lesson_12.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_12 as B

lib = library.current()
assert "adv_lesson_12" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 12: Polygons, Angles and Diagonals in Polygons, Proof of the Chord-Tangent Theorem"
assert B.type_instructions("2") == "Find the number of diagonals."
assert "$" not in "".join(B.type_instructions(k) for k in B.KEYS)   # instructions are plain text

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 12.1", "1", "7", "900 degree; 360 degree"),
    ("PS 4", "1", "6", "720 degree; 360 degree"),
    ("PS 5", "2", "9", "27"),
]
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt, typ) == answer, (sid, B.answer_of(prompt, typ), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable
REACH = {"ex 12.1": (B.t1, dict(n=7)), "PS 4": (B.t1, dict(n=6)), "PS 5": (B.t2, dict(n=9))}
prompt_of = {s[0]: s[2] for s in SOURCES}
type_of = {s[0]: s[1] for s in SOURCES}
assert set(REACH) == set(prompt_of)
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], sid
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[type_of[sid]]), sid
assert set(type_of.values()) == set(B.KEYS)
assert not B.in_range(B.t1, dict(n=11)) and not B.in_range(B.t2, dict(n=3))

# ---- wrong answers fail
WRONG = [
    ("1", "7", "1260 degree; 360 degree"),      # N times 180
    ("1", "7", "900 degree; 900 degree"),       # the exterior sum taken as the interior
    ("1", "7", "900 degree"),                   # one sum
    ("1", "7", "360 degree; 900 degree"),       # crossed
    ("2", "9", "54"),                           # not halved
    ("2", "9", "36"),                           # every pair, sides too
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn and checked, each number of sides
rng = random.Random(12)
for k in B.KEYS:
    seen, got = set(), set()
    for _ in range(len(B.SIDES[k])):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        got.add(int(p["prompt"]))
    assert got == set(B.SIDES[k]), (k, got)                            # the whole range is drawn

# ---- showing
s = dict(type="1", prompt="7", answer="900 degree; 360 degree")
assert B.text(s).startswith("Find the sum of the measures of (a) the interior angles and (b) the exterior angles of a seven-sided convex polygon.")
assert "cetz.canvas" in B.typst(s) and "[5]" not in B.typst(s) and "[5]" in B.key_typst(s)   # numbered triangles on the key only
assert B.answer_text(s) == "(a) 900°   (b) 360°"
assert "#hide[" in B.slide_typst(s) and "#hide[" not in B.slide_typst(s, key=True)
d = dict(type="2", prompt="13", answer="65")
assert B.text(d) == "How many diagonals can be drawn in a 13-sided convex polygon?"
assert B.answer_text(d) == "65 diagonals" and B.slide_typst(d) is None

# ---- editing
p, status = B.from_edit("10", dict(type="1", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"] == "1440 degree; 360 degree", p
p, status = B.with_answer(p, "1440°, 360°")
assert status == "checked", p
p, status = B.from_edit("20", dict(type="2", prompt="", answer=""))
assert status == "checked" and p["answer"] == "170", p
for bad in ("seven", "2"):
    try:
        B.from_edit(bad, dict(type="1", prompt="", answer="")); raise AssertionError(bad)
    except ValueError:
        pass

print("adv_lesson_12: ok")
