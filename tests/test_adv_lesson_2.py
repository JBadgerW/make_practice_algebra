"""Lesson 2 (Advanced Math): more on area, cylinders and prisms, cones and
pyramids. Every source problem is reachable from in-range parameters and
checks with the deck's answer; wrong answers fail; every type draws, checks,
and keeps its shape; the figures show; edits solve again.

    python3 tests/test_adv_lesson_2.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_2 as B

lib = library.current()
assert "adv_lesson_2" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 2: More on Area, Cylinders and Prisms, Cones and Pyramids, Spheres"
assert B.type_instructions("1").startswith("Round each area and volume to two decimal places")
assert B.type_instructions("5") == "Solve each problem. Include units."

# ---- every source: the deck's answer (problems 25-28: worked here, in the deck's way), and checked
SOURCES = [   # (id, type, prompt, answer)
    ("ex 2.1", "1", "cylinder area: base 5 x 6, right semicircle; height 10 cm", '342.53 "cm"^2'),
    ("ex 2.2", "2", "prism area: plus, side 2, length 6 units", '184 "square units"'),
    ("ex 2.3", "4", "cone volume: base 3 x 2, right semicircle; height 6 m", '15.14 "m"^3'),
    ("ex 2.4", "5", "cone area: radius 8, slant 10 cm", '144 pi "cm"^2'),
    ("ex 2.5", "6", "cone radius: volume 6 pi, height 2 cm", '3 "cm"'),
    ("ex 2.6", "7", "pyramid area: side 4, slant 5 cm", '56 "cm"^2'),
    ("PS 25", "6", "cylinder height: radius 7, volume 588 pi cm", '12 "cm"'),
    ("PS 26", "6", "wedge height: legs 2 pi and 3, sector 60, volume 9 pi cm", '2 "cm"'),
    ("PS 27", "4", "cone volume: base 5 x 6, left semicircle; height 8 m", '117.71 "m"^3'),
    ("PS 28a", "3", "cylinder volume: base 11 x 10, right semicircle, left semicircle 20; height 9 cm", '2757.15 "cm"^3'),
    ("PS 28b", "1", "cylinder area: base 11 x 10, right semicircle, left semicircle 20; height 9 cm", '1324.82 "cm"^2'),
    ("PS 28c", "4", "cone volume: base 11 x 10, right semicircle, left semicircle 20; height 9 cm", '919.05 "cm"^3'),
]
TYPE_OF = {"ex 2.1": "1", "ex 2.2": "2", "ex 2.3": "4", "ex 2.4": "5", "ex 2.5": "6", "ex 2.6": "7",
           "PS 25": "6", "PS 26": "6", "PS 27": "4", "PS 28a": "3", "PS 28b": "1", "PS 28c": "4"}
assert {s[0]: s[1] for s in SOURCES} == TYPE_OF and len(SOURCES) == len(TYPE_OF)
assert set(TYPE_OF.values()) == set(B.KEYS)
prompt_of = {sid: prompt for sid, _, prompt, _ in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 2.1": (B.t1_build, dict(w=5, h=6, caps="right", d=0, height=10, unit="cm")),
    "ex 2.2": (B.t2_build, dict(shape="plus", side=2, length=6, unit="units")),
    "ex 2.3": (B.t4_build, dict(w=3, h=2, caps="right", d=0, height=6, unit="m")),
    "ex 2.4": (B.t5_build, dict(r=8, l=10, unit="cm")),
    "ex 2.5": (B.t6_cone_build, dict(r=3, h=2, unit="cm")),
    "ex 2.6": (B.t7_build, dict(s=4, l=5, unit="cm")),
    "PS 25": (B.t6_cyl_build, dict(r=7, H=12, unit="cm")),
    "PS 26": (B.t6_wedge_build, dict(k=2, b=3, angle=60, H=2, unit="cm")),
    "PS 27": (B.t4_build, dict(w=5, h=6, caps="left", d=0, height=8, unit="m")),
    "PS 28a": (B.t3_build, dict(w=11, h=10, caps="tall", d=20, height=9, unit="cm")),
    "PS 28b": (B.t1_build, dict(w=11, h=10, caps="tall", d=20, height=9, unit="cm")),
    "PS 28c": (B.t4_build, dict(w=11, h=10, caps="tall", d=20, height=9, unit="cm")),
}
assert set(REACH) == {s[0] for s in SOURCES}
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert not B.in_range(B.t6_cone_build, dict(r=2, h=2, unit="cm"))      # 8/3 pi: not a whole volume
assert not B.in_range(B.t1_build, dict(w=5, h=5, caps="right", d=0, height=10, unit="cm"))   # radius 2.5

# ---- wrong or unfinished answers fail
WRONG = [
    ("1", prompt_of["ex 2.1"], '342.5 "cm"^2'),                 # one place
    ("1", prompt_of["ex 2.1"], '298.39 "cm"^2'),                # one base only
    ("1", prompt_of["ex 2.1"], '342.53 "cm"^3'),                # cubed
    ("1", prompt_of["ex 2.1"], '342.53 "m"^2'),                 # the wrong unit
    ("1", prompt_of["ex 2.1"], "342.53"),                       # no unit
    ("1", prompt_of["ex 2.1"], '220 + 39 pi "cm"^2'),           # exact: the key is decimal
    ("4", prompt_of["ex 2.3"], '45.42 "m"^3'),                  # the cylinder's volume
    ("4", prompt_of["PS 27"], '117.85 "m"^3'),
    ("3", prompt_of["PS 28a"], '2133.15 "cm"^3'),               # the tall semicircle as an ordinary one
    ("2", prompt_of["ex 2.2"], '164 "square units"'),           # 10 lateral faces, not 12
    ("2", prompt_of["ex 2.2"], '184 "cubic units"'),
    ("5", prompt_of["ex 2.4"], '80 pi "cm"^2'),                 # the lateral area alone
    ("5", prompt_of["ex 2.4"], '452.39 "cm"^2'),                # a decimal: the key keeps pi
    ("6", prompt_of["ex 2.5"], '9 "cm"'),                       # r^2, not r
    ("6", prompt_of["PS 25"], '84 "cm"'),                       # divided by r, not r^2
    ("6", prompt_of["PS 26"], '3 "cm"'),
    ("7", prompt_of["ex 2.6"], '36 "cm"^2'),                    # two faces, not four
    ("7", prompt_of["ex 2.6"], '56 "cm"^3'),
    ("1", prompt_of["ex 2.3"], '15.14 "m"^3'),                  # a Type 4 prompt under Type 1
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
CAP = r"base \d+ x \d+(, right semicircle)?(, left semicircle( \d+)?)?; height \d+ (cm|m|ft|in)$"
SHAPE = {"1": "^cylinder area: " + CAP, "3": "^cylinder volume: " + CAP, "4": "^cone volume: " + CAP,
         "2": r"^prism area: (plus|T|L|S|U|step), side \d, length \d+ (units|cm|m|ft|in)$",
         "5": r"^cone area: radius \d+, slant \d+ (cm|m|ft|in)$",
         "6": r"^(cone radius|cylinder height|wedge height): ",
         "7": r"^pyramid area: side \d+, slant \d+ (cm|m|ft|in)$"}
ANSWER = {"1": r'^\d+\.\d\d "(cm|m|ft|in)"\^2$', "3": r'^\d+\.\d\d "(cm|m|ft|in)"\^3$',
          "4": r'^\d+\.\d\d "(cm|m|ft|in)"\^3$', "2": r'^\d+ ("square units"|"(cm|m|ft|in)"\^2)$',
          "5": r'^\d+ pi "(cm|m|ft|in)"\^2$', "6": r'^\d+ "(cm|m|ft|in)"$', "7": r'^\d+ "(cm|m|ft|in)"\^2$'}
rng = random.Random(2)
for k in B.KEYS:
    seen, kinds = set(), set()
    for _ in range(80):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.match(SHAPE[k], p["prompt"]), p
        assert re.match(ANSWER[k], p["answer"]), p
        assert int(re.match(r"\d+", p["answer"]).group()) > 0, p
        kinds.add(B.kind(p["prompt"]))
        if k in ("1", "3", "4"):
            _, w, h, right, left, height, unit = B.read_cap(p["prompt"])
            assert h % 2 == 0 and (right or left) and (left == 0 or left >= h), p
    if k == "6":
        assert kinds == {"cone radius", "cylinder height", "wedge height"}, kinds

# ---- showing: the deck's words, the figure drawn from the data
p = dict(type="1", prompt=prompt_of["ex 2.1"], answer='342.53 "cm"^2')
t = B.typst(p)
assert t.startswith("The base of a right cylinder 10 centimeters high is shown. Find the surface area of the "
                    "right cylinder. Dimensions are in centimeters."), t
assert "cetz.canvas" in t and "[$3$]" in t and "[$6$]" in t, t
assert B.answer_typst(p) == '$342.53 thin "cm"^2$'
assert B.answer_text(p) == "342.53 cm²", B.answer_text(p)
p = dict(type="3", prompt=prompt_of["PS 28a"], answer='2757.15 "cm"^3')
assert "[$10$]" in B.typst(p) and "[$11$]" in B.typst(p) and "[$5$]" in B.typst(p)   # as the book labels it
p = dict(type="6", prompt=prompt_of["ex 2.5"], answer='3 "cm"')
assert B.typst(p) == ("The volume of a right circular cone is $6 pi$ cm#super[3]. The height of this right "
                      "circular cone is 2 cm. Find the radius of the base of the cone.")
assert B.slide_typst(p) is None
p = dict(type="6", prompt=prompt_of["PS 26"], answer='2 "cm"')
assert "[$2 pi$]" in B.typst(p) and "[$60°$]" in B.typst(p)
q, a = B.slide_typst(p), B.slide_typst(p, key=True)
assert q.replace('#hide[$2 thin "cm"$]', "") == a.replace('#text(fill: red)[$2 thin "cm"$]', "")
p = dict(type="2", prompt=prompt_of["ex 2.2"], answer='184 "square units"')
assert B.typst(p).startswith("Find the surface area of this right prism. #v")
assert B.answer_text(p) == "184 square units"

# ---- editing: a new prompt is solved again; a typed answer is checked
old = dict(type="5", prompt="", answer="", source="template")
p, status = B.from_edit("cone area: radius 3, slant 5 cm", old)
assert status == "checked" and p["answer"] == '24 pi "cm"^2', p
p, status = B.with_answer(p, '24 pi "cm"^2')
assert status == "checked", p
p, status = B.with_answer(p, '24π "cm"^2')
assert status == "checked", p
p, status = B.with_answer(p, '15 pi "cm"^2')
assert status != "checked", p
p, status = B.from_edit("cylinder area: base 4 x 2, right semicircle, left semicircle; height 5 ft",
                        dict(type="1", prompt="", answer=""))
assert status == "checked" and p["answer"] == '93.70 "ft"^2', p          # 2(8 + pi) + 5(8 + 2 pi): 22.28 + 71.42
p, status = B.from_edit("cylinder height: radius 3, volume 45 pi m", dict(type="6", prompt="", answer=""))
assert status == "checked" and p["answer"] == '5 "m"', p
for typ, bad in (("1", "cylinder area: base 5 x 6; height 10 cm"),        # no semicircle
                 ("1", "cone area: radius 3, slant 5 cm"),                  # another type's problem
                 ("6", "cylinder height: radius 3, volume 40 pi m"),        # 40/9: not whole
                 ("2", "prism area: star, side 2, length 6 units"),
                 ("7", "pyramid area: side 10, slant 4 cm")):               # the slant too short
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_2: ok")
