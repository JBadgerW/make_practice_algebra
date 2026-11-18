"""Lesson 4 (Advanced Math): construction. Every source construction is
reachable from in-range parameters and checks with its key; wrong keys and
broken constructions fail; every type draws, checks, keeps its shape, and
fits its column; the figures show the construction only on the key, at the
same size; edits solve again.

    python3 tests/test_adv_lesson_4.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_4 as B

lib = library.current()
assert "adv_lesson_4" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 4: Construction"
assert B.type_instructions("2").startswith("Use a compass and a straightedge.")
assert B.type_instructions("1") == "Find each angle's measure."

# ---- every source: its key, and checked
SOURCES = [   # (id, type, prompt, answer)
    ("con 1", "1", "O; A 0, B 45, C 180", "m angle B O A = 45 degree, m angle C O B = 135 degree"),   # the deck's
    ("con 2", "2", "AB = 4; ray XY", 'X P = A B = 4 "cm"'),
    ("PS 7", "2", "AB = 4", 'X P = A B = 4 "cm"'),
    ("con 3", "3", "BAC = 40, AC at 0", "m angle B' X Y = m angle B A C = 40 degree"),
    ("PS 8", "3", "PQR = 30, QR at -15", "m angle P' X Y = m angle P Q R = 30 degree"),          # the deck's P'XY
    ("con 4", "4", "BAC = 40, AC at 0", "m angle B A D = m angle D A C = 20 degree"),
    ("con 5", "5", "BK = 4.5", 'B D = D K = 2.25 "cm"'),
    ("PS 9", "5", "MN = 6", 'M D = D N = 3 "cm"'),
    ("con 6", "6", "line AC = 6, P at 2", "overline(P D) perp arrow.l.r(A C)"),
    ("PS 10", "6", "segment RS = 6.5, P at 2.5", "overline(P D) perp overline(R S)"),
    ("con 7", "7", "line EF = 7.2, P at 3.6, 2.2 above", 'overline(P D) perp arrow.l.r(E F), P D = 2.2 "cm"'),
    ("con 8", "8", "BC = 3, AX = 4, MN = 5", 'B C = 3 "cm", A X = 4 "cm", M N = 5 "cm"'),
    ("PS 11", "8", "a = 2, b = 3, c = 4", 'a = 2 "cm", b = 3 "cm", c = 4 "cm"'),
    ("con 9", "9", "line 7, P at 2.5, 2.5 above", 'arrow.l.r(P Q) parallel "the given line"'),
    ("con 10", "10", "AB = 6, 3 parts", 'A X = X Y = Y B = 2 "cm"'),                           # the deck's X, Y
]
TYPE_OF = {"con 1": "1", "con 2": "2", "PS 7": "2", "con 3": "3", "PS 8": "3", "con 4": "4", "con 5": "5",
           "PS 9": "5", "con 6": "6", "PS 10": "6", "con 7": "7", "con 8": "8", "PS 11": "8", "con 9": "9",
           "con 10": "10"}                                       # every source in exactly one type
assert {s[0]: s[1] for s in SOURCES} == TYPE_OF and len(SOURCES) == len(TYPE_OF)
assert set(TYPE_OF.values()) == set(B.KEYS)                       # every type has a source
prompt_of = {sid: prompt for sid, _, prompt, _ in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt, typ) == answer, (sid, B.answer_of(prompt, typ), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid
    if typ != "1":                                                # it fits its column, like a draw
        assert B.extent(typ, prompt)[0] <= B.MAX_WIDE[B.ENTRY[typ]["width"]], sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "con 1": (B.t1_build, dict(letters=("O", "A", "B", "C"), dirs=(0, 45, 180))),
    "con 2": (B.t2_build, dict(seg="AB", L=4.0, ray="XY")),
    "PS 7": (B.t2_build, dict(seg="AB", L=4.0)),
    "con 3": (B.t3_build, dict(name="BAC", meas=40, d=0)),
    "PS 8": (B.t3_build, dict(name="PQR", meas=30, d=-15)),
    "con 4": (B.t4_build, dict(name="BAC", meas=40, d=0)),
    "con 5": (B.t5_build, dict(seg="BK", L=4.5)),
    "PS 9": (B.t5_build, dict(seg="MN", L=6.0)),
    "con 6": (B.t6_build, dict(kind="line", seg="AC", L=6.0, p="P", x=2.0)),
    "PS 10": (B.t6_build, dict(kind="segment", seg="RS", L=6.5, p="P", x=2.5)),
    "con 7": (B.t7_build, dict(line="EF", L=7.2, p="P", x=3.6, h=2.2)),
    "con 8": (B.t8_build, dict(labels=("BC", "AX", "MN"), lengths=(3.0, 4.0, 5.0))),
    "PS 11": (B.t8_build, dict(labels=("a", "b", "c"), lengths=(2.0, 3.0, 4.0))),
    "con 9": (B.t9_build, dict(L=7.0, p="P", x=2.5, h=2.5)),
    "con 10": (B.t10_build, dict(seg="AB", L=6.0, n=3)),
}
assert set(REACH) == {s[0] for s in SOURCES}                     # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid                         # every parameter inside its named range
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
# the guards say no where they should
assert not B.in_range(B.t1_build, dict(letters=("O", "A", "B", "C"), dirs=(0, 5, 180)))     # rays too close
assert not B.in_range(B.t8_build, dict(labels=("a", "b", "c"), lengths=(2.0, 2.5, 4.5)))    # 2 + 2.5 = 4.5: no triangle
assert not B.in_range(B.t10_build, dict(seg="AB", L=5.0, n=3))                               # 5/3 cm pieces
assert not B.in_range(B.t6_build, dict(kind="segment", seg="RS", L=6.5, p="P", x=1.0))      # P too near R

# ---- wrong keys, and constructions that can't be made, fail
WRONG = [
    ("1", "O; A 0, B 45, C 180", "m angle B O A = 135 degree, m angle C O B = 45 degree"),   # the wrong scales
    ("1", "O; A 0, B 45, C 180", "m angle B O A = 45 degree, m angle C O A = 180 degree"),   # the wrong angle
    ("1", "O; X 0, Y 40, Z 110", "m angle Y O X = 40 degree, m angle Z O Y = 110 degree"),   # not subtracted
    ("2", "AB = 4", 'X P = A B = 4.5 "cm"'),
    ("2", "AB = 4", 'X Y = A B = 4 "cm"'),                       # Y is the ray's point, not the copy's end
    ("3", "PQR = 30, QR at -15", "m angle P' X Y = m angle P Q R = 60 degree"),
    ("3", "PQR = 30, QR at -15", "m angle P' X Y = m angle P Q R = 150 degree"),   # the supplement
    ("4", "BAC = 40, AC at 0", "m angle B A D = m angle D A C = 40 degree"),       # not halved
    ("4", "BAC = 40, AC at 0", "m angle B A D = m angle D A C = 20"),              # no degrees
    ("5", "MN = 6", 'M D = D N = 6 "cm"'),
    ("5", "MN = 6", 'M D = D N = 3'),                            # no unit
    ("6", "segment RS = 6.5, P at 2.5", "overline(P D) perp arrow.l.r(R S)"),      # it's a segment
    ("6", "segment RS = 6.5, P at 2.5", "overline(P D) parallel overline(R S)"),
    ("7", "line EF = 7.2, P at 3.6, 2.2 above", 'overline(P D) perp arrow.l.r(E F), P D = 3.6 "cm"'),
    ("8", "a = 2, b = 3, c = 4", 'a = 3 "cm", b = 2 "cm", c = 4 "cm"'),
    ("8", "a = 2, b = 3, c = 4", 'a = 2 "cm", b = 3 "cm"'),
    ("8", "a = 1, b = 2, c = 4", 'a = 1 "cm", b = 2 "cm", c = 4 "cm"'),           # no such triangle
    ("8", "a = 2, b = 2, c = 4", 'a = 2 "cm", b = 2 "cm", c = 4 "cm"'),           # flat: the arcs only touch
    ("9", "line 7, P at 2.5, 2.5 above", 'arrow.l.r(P X) parallel "the given line"'),
    ("10", "AB = 6, 3 parts", 'A X = X Y = Y B = 3 "cm"'),
    ("10", "AB = 6, 3 parts", 'A X = X B = 3 "cm"'),                               # two parts, not three
    ("2", "MN = 6", 'X P = M N = 6 "cm"'.replace("X P", "M D")),                   # another type's answer
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (typ, prompt, answer, got)

# ---- every type: drawn, checked, in its shape, and fitting its column
SHAPE = {
    "1": r"^[A-Z]; [A-Z] (0|180), [A-Z] \d+, [A-Z] \d+$",
    "2": r"^[A-Z]{2} = [\d.]+(, tilt -?\d+)?(; ray [A-Z]{2})?$",
    "3": r"^[A-Z]{3} = \d+, [A-Z]{2} at -?\d+$",
    "4": r"^[A-Z]{3} = \d+, [A-Z]{2} at -?\d+$",
    "5": r"^[A-Z]{2} = [\d.]+(, tilt -?\d+)?$",
    "6": r"^(segment|line) [A-Z]{2} = [\d.]+, [A-Z] at [\d.]+(, tilt -?\d+)?$",
    "7": r"^line [A-Z]{2} = [\d.]+, [A-Z] at [\d.]+, [\d.]+ (above|below)$",
    "8": r"^([a-z]|[A-Z]{2}) = [\d.]+, ([a-z]|[A-Z]{2}) = [\d.]+, ([a-z]|[A-Z]{2}) = [\d.]+$",
    "9": r"^line [\d.]+, [A-Z] at [\d.]+, [\d.]+ (above|below)$",
    "10": r"^[A-Z]{2} = [\d.]+, \d parts$",
}
rng = random.Random(4)
for k in B.KEYS:
    seen = set()
    for i in range(80):
        if i % 20 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.match(SHAPE[k], p["prompt"]), p
        if k != "1":
            assert B.extent(k, p["prompt"])[0] <= B.MAX_WIDE[B.ENTRY[k]["width"]], p
        if k == "1":
            (_, a), (_, b) = B.asked1(p["prompt"])
            assert min(a, b) >= B.GAP1, p
        if k == "8":
            x, y, z = sorted(v for _, v in B.read8(p["prompt"]))
            assert x + y - z >= B.MARGIN8 - 1e-9, p
        if k == "10":
            _, _, L, n = B.read10(p["prompt"])
            assert L / n >= 1 and round(L * 10) % n == 0, p

# ---- showing: the deck's words; the construction only on the key, the figure the same size
p = dict(type="2", prompt="AB = 4", answer='X P = A B = 4 "cm"')
assert B.typst(p).startswith("Construct a segment congruent to $overline(A B)$.")
q, k = B.typst(p), B.key_typst(p)
assert "c0392b" not in q and "c0392b" in k                       # red: the key's marks
box = lambda t: re.search(r"rect\([^)]*\)[^)]*\)", t).group(0)
assert box(q) == box(k)                                           # the same size: nothing moves
assert B.text(p) == "Construct a segment congruent to AB.   [figure]", B.text(p)
assert B.answer_text(p) == "XP = AB = 4 cm" and B.answer_typst(p) == '$X P = A B = 4 "cm"$'
p = dict(type="1", prompt="O; A 0, B 45, C 180", answer=SOURCES[0][3])
assert B.typst(p).startswith("Use the protractor to find the measures of $angle B O A$ and $angle C O B$.")
assert B.answer_text(p) == "m∠BOA = 45°, m∠COB = 135°", B.answer_text(p)
assert B.answer_typst(p) == "$m angle B O A = 45 degree, quad m angle C O B = 135 degree$"
p = dict(type="6", prompt="line AC = 6, P at 2", answer="overline(P D) perp arrow.l.r(A C)")
assert B.text(p) == "Construct a perpendicular to AC at P.   [figure]" and B.answer_text(p) == "PD ⊥ AC"
p = dict(type="9", prompt="line 7, P at 2.5, 2.5 above", answer=SOURCES[13][3])
assert B.answer_text(p) == "PQ ∥ the given line", B.answer_text(p)
p = dict(type="8", prompt="BC = 3, AX = 4, MN = 5", answer=SOURCES[11][3])
assert B.typst(p).startswith("Given segments $B C$, $A X$, and $M N$, construct a triangle")
# the slide: the steps and answer hidden on the question slide, the figure the same on both
for sid, typ, prompt, answer in SOURCES:
    p = dict(type=typ, prompt=prompt, answer=answer)
    q, a = B.slide_typst(p), B.slide_typst(p, key=True)
    assert "#hide[" in q and "#text(fill: red)[" in a, sid
    if typ != "1":
        assert box(q) == box(a), sid
    assert B.height(p) > 1, sid

# ---- editing: a new figure is solved again; a typed answer is checked
old = dict(type="10", prompt="AB = 6, 3 parts", answer=SOURCES[-1][3], source="template")
p, status = B.from_edit("CD = 8, 4 parts", old)
assert status == "checked" and p["answer"] == 'C X = X Y = Y Z = Z D = 2 "cm"', p
p, status = B.with_answer(p, 'C X = X Y = Y Z = Z D = 2  "cm"')
assert status == "checked", p
p, status = B.with_answer(p, 'C X = X Y = Y Z = Z D = 2.5 "cm"')
assert status != "checked", p
p, status = B.from_edit("∠PQR = 50°, QR at −25", dict(type="3", prompt="", answer=""))
assert status == "checked" and p["prompt"] == "PQR = 50, QR at -25", p
for typ, bad in (("8", "a = 1, b = 1, c = 5"), ("2", "AB 4"), ("1", "O; A 0, B 45")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(bad)
    except ValueError:
        pass

print("adv_lesson_4: ok")
