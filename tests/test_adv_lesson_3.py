"""Lesson 3 (Advanced Math): the Pythagorean theorem, similar triangles. Every
source problem is reachable from in-range parameters and checks with the
deck's answer; wrong answers fail; every type draws, checks, and keeps its
shape; the figures show; edits solve again.

    python3 tests/test_adv_lesson_3.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_3 as B

lib = library.current()
assert "adv_lesson_3" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 3: Pythagorean Theorem, Similar Triangles"
assert B.type_instructions("1").startswith("Compare the square of the longest side")
for k in "2345":
    assert B.type_instructions(k).startswith("Find the unknown lengths."), k

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, answer)
    ("ex 3.1", "1", "7, 5, 4", "obtuse"),
    ("ex 3.2", "2", "bowtie 0; 5, 4, x; 7, y, 6", "x = 30/7, y = 28/5"),
    ("ex 3.3", "3", "right bowtie 0; 7, x, y; 10, z, 8", "x = 21/5, y = 28/5, z = 6"),   # deck: 4.2, 5.6
    ("ex 3.4", "4", "base 6 + 4, leg 4; A, B, C", "A = 2 sqrt(13), B = (4 sqrt(13))/3, C = 20/3"),
    ("ex 3.5", "5", "4 + 8; a, b, h", "a = 4 sqrt(3), b = 4 sqrt(6), h = 4 sqrt(2)"),
    ("PS 5", "1", "7 cm, 12 cm, 6 cm", "obtuse"),
    ("PS 6", "2", "apart 9 2, factors; 6, 7, x; 3, y, 4",
     '"right to left" = 2, "left to right" = 1/2, x = 8, y = 7/2'),
    ("PS 7", "2", "apart 1 6; 7, 15, y; 3, x, 5", "x = 45/7, y = 35/3"),
    ("PS 8", "3", "right bowtie 1; 15, x, 12; 21, y, z", "x = 9, y = 63/5, z = 84/5"),
    ("PS 9", "4", "hyp 13 + 26, leg 5; a, b, c", "a = 12, b = 24, c = 15"),
    ("PS 10", "5", "5 + 9; x, y, z", "x = sqrt(70), y = 3 sqrt(14), z = 3 sqrt(5)"),
]
TYPE_OF = {"ex 3.1": "1", "ex 3.2": "2", "ex 3.3": "3", "ex 3.4": "4", "ex 3.5": "5",
           "PS 5": "1", "PS 6": "2", "PS 7": "2", "PS 8": "3", "PS 9": "4", "PS 10": "5"}   # every source in one type
assert {s[0]: s[1] for s in SOURCES} == TYPE_OF and len(SOURCES) == len(TYPE_OF)
assert set(TYPE_OF.values()) == set(B.KEYS)                       # every type has a source
prompt_of = {sid: prompt for sid, _, prompt, _ in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 3.1": (B.t1_build, dict(a=7, b=5, c=4, unit="")),
    "PS 5": (B.t1_build, dict(a=7, b=12, c=6, unit="cm")),
    "ex 3.2": (B.t2_build, dict(layout="bowtie", pose=0, u=5, v=7, a=4, b=6, i=0, j=1, first="x", factors=False)),
    "PS 6": (B.t2_build, dict(layout="apart", pose=(9, 2), u=6, v=3, a=7, b=4, i=0, j=1, first="x", factors=True)),
    "PS 7": (B.t2_build, dict(layout="apart", pose=(1, 6), u=7, v=3, a=15, b=5, i=0, j=1, first="y", factors=False)),
    "ex 3.3": (B.t3_build, dict(flip=0, full_left=False, full=(10, 6, 8), gap=1, pos=0, w=7, letters="xyz")),
    "PS 8": (B.t3_build, dict(flip=1, full_left=True, full=(15, 9, 12), gap=1, pos=0, w=21, letters="xyz")),
    "ex 3.4": (B.t4_base_build, dict(p=6, q=4, h=4, letters="ABC")),
    "PS 9": (B.t4_hyp_build, dict(s=13, t=26, h=5, letters="abc")),
    "ex 3.5": (B.t5_build, dict(m=4, n=8, letters="abh")),
    "PS 10": (B.t5_build, dict(m=5, n=9, letters="xyz")),
}
assert set(REACH) == {s[0] for s in SOURCES}                     # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid                         # every parameter inside its named range
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert not B.in_range(B.t1_build, dict(a=2, b=3, c=9, unit=""))                     # not a triangle
assert not B.in_range(B.t2_build, dict(layout="apart", pose=(1, 1), u=7, v=3, a=15, b=5, i=0, j=1,
                                       first="y", factors=False))               # the same pose twice
assert not B.in_range(B.t5_build, dict(m=6, n=6, letters="abh"))                  # isosceles: no longer this type
assert not B.in_range(B.t3_build, dict(flip=0, full_left=False, full=(10, 6, 8), gap=1, pos=0, w=10,
                                       letters="xyz"))                          # congruent, not just similar

# ---- wrong or unfinished answers fail
WRONG = [
    ("1", "7, 5, 4", "acute"),
    ("1", "5, 12, 13", "acute"),                                   # right
    ("1", "6, 7, 9", "obtuse"),                                    # 81 < 85: acute
    ("2", "bowtie 0; 5, 4, x; 7, y, 6", "x = 28/5, y = 30/7"),     # the factor used the wrong way
    ("2", "bowtie 0; 5, 4, x; 7, y, 6", "x = 30/7"),               # y missing
    ("2", "bowtie 0; 5, 4, x; 7, y, 6", "x = 60/14, y = 28/5"),    # not reduced
    ("2", "bowtie 0; 5, 4, x; 7, y, 6", "x = 4.29, y = 5.6"),      # decimals
    ("2", "apart 9 2, factors; 6, 7, x; 3, y, 4", "x = 8, y = 7/2"),    # the scale factors not given
    ("2", "apart 9 2, factors; 6, 7, x; 3, y, 4",
     '"right to left" = 1/2, "left to right" = 2, x = 8, y = 7/2'),     # the factors swapped
    ("3", "right bowtie 0; 7, x, y; 10, z, 8", "x = 21/5, y = 28/5, z = 2"),   # 10 - 8, not the theorem
    ("3", "right bowtie 0; 7, x, y; 10, z, 8", "x = 4.2, y = 5.6, z = 6"),     # the deck's decimals: not the key's form
    ("3", "right bowtie 0; 7, x, y; 10, z, 8", "x = 28/5, y = 21/5, z = 6"),   # the legs swapped
    ("4", "base 6 + 4, leg 4; A, B, C", "A = sqrt(52), B = (4 sqrt(13))/3, C = 20/3"),   # not simplified
    ("4", "base 6 + 4, leg 4; A, B, C", "A = 2 sqrt(13), B = (10 sqrt(13))/3, C = 20/3"),  # A + B, not B
    ("4", "base 6 + 4, leg 4; A, B, C", "A = 2 sqrt(13), B = (8 sqrt(13))/6, C = 20/3"),   # not reduced
    ("4", "hyp 13 + 26, leg 5; a, b, c", "a = 12, b = 36, c = 15"),             # the whole base
    ("5", "4 + 8; a, b, h", "a = 4 sqrt(6), b = 4 sqrt(3), h = 4 sqrt(2)"),     # the legs swapped
    ("5", "4 + 8; a, b, h", "a = 4 sqrt(3), b = 4 sqrt(6), h = sqrt(32)"),     # not simplified
    ("5", "4 + 8; a, b, h", "a = 4 sqrt(3), b = 4 sqrt(6), h = 4 sqrt(2)/1"),
    ("2", "right bowtie 0; 7, x, y; 10, z, 8", "x = 21/5, y = 28/5, z = 6"),    # a Type 3 prompt under Type 2
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
SIDE = r"(\d+|[a-z])"
SHAPE = {
    "1": r"^\d+( (cm|m|in|ft))?, \d+( (cm|m|in|ft))?, \d+( (cm|m|in|ft))?$",
    "2": rf"^(apart \d+ \d+|bowtie [01])(, factors)?; {SIDE}, {SIDE}, {SIDE}; {SIDE}, {SIDE}, {SIDE}$",
    "3": rf"^right bowtie [01]; {SIDE}, {SIDE}, {SIDE}; {SIDE}, {SIDE}, {SIDE}$",
    "4": r"^(base|hyp) \d+ \+ \d+, leg \d+; ([ABC], [ABC], [ABC]|a, b, c|x, y, z)$",
    "5": r"^\d+ \+ \d+; (a, b, h|x, y, z)$",
}
VALUE = r"(\d+|\d+/\d+|(\d+ )?sqrt\(\d+\)|\(\d+ sqrt\(\d+\)\)/\d+|sqrt\(\d+\)/\d+)"
ANSWER = {
    "1": r"^(right|acute|obtuse)$",
    "2": rf'^("right to left" = {VALUE}, "left to right" = {VALUE}, )?x = {VALUE}, y = {VALUE}$',
    "3": rf"^[a-z] = {VALUE}, [a-z] = {VALUE}, [a-z] = {VALUE}$",
    "4": rf"^[A-Za-z] = {VALUE}, [A-Za-z] = {VALUE}, [A-Za-z] = {VALUE}$",
    "5": rf"^[a-z] = {VALUE}, [a-z] = {VALUE}, [a-z] = {VALUE}$",
}
rng = random.Random(1)
for k in B.KEYS:
    seen, answers, layouts = set(), set(), set()
    for i in range(80):
        if i % 20 == 0:
            seen = set()                                          # Type 5's whole-altitude pool is small
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.match(SHAPE[k], p["prompt"]), p
        assert re.match(ANSWER[k], p["answer"]), p
        answers.add(p["answer"].split(" = ")[0] if k != "1" else p["answer"])
        if k == "1":
            answers.add(p["answer"])
        if k in ("2", "3"):
            layout, poses, factors, L, R = B.read_pair(p["prompt"])
            layouts.add(layout)
            # Type 2: one pair known in both, one unknown in each (Type 3 may find its pair by Pythagoras)
            both = [i for i in range(3) if not isinstance(L[i], str) and not isinstance(R[i], str)]
            if k == "2":
                assert len(both) == 1, p
                assert sum(isinstance(s, str) for s in L) == 1 == sum(isinstance(s, str) for s in R), p
            _, _, Lv, Rv = B.pair_values(p["prompt"])
            assert B.drawable(*Lv), p
            for _, v in B.read_answer(p["answer"]).values():
                assert v.q <= B.MAX_DEN if v.is_Rational else True, p
        if k == "3":
            known = [sum(not isinstance(s, str) for s in T) for T in (L, R)]
            assert sorted(known) == [1, 2], p                       # Pythagoras first in one triangle
        if k == "4":
            kind, x, y, h, _ = B.read_nest(p["prompt"])
            assert 20 <= B.base_angle(kind, x, h) <= 55, p
        if k == "5":
            m, n, _ = B.read_alt(p["prompt"])
            assert m != n and m + n <= (B.SUM5_WHOLE if B.is_square(m * n) else B.SUM5), p
        assert B.figure(p) or k == "1"
    if k == "1":
        assert {"right", "acute", "obtuse"} <= answers, answers
    if k == "2":
        assert layouts == {"apart", "bowtie"}, layouts

# ---- showing: the deck's words, the figure drawn from the data
p = dict(type="1", prompt=prompt_of["ex 3.1"], answer="obtuse")
assert B.typst(p) == ("The lengths of the sides of a triangle are 7, 5, and 4, respectively. Is the triangle "
                      "a right triangle, an acute triangle, or an obtuse triangle?"), B.typst(p)
assert B.answer_typst(p) == "*obtuse triangle* #h(1em) $7^2 > 5^2 + 4^2$", B.answer_typst(p)
assert B.slide_typst(p) is None and B.answer_text(p) == "obtuse triangle"
p = dict(type="1", prompt=prompt_of["PS 5"], answer="obtuse")
assert "7 cm, 12 cm, and 6 cm, respectively" in B.typst(p)
assert B.answer_typst(p).endswith("$12^2 > 7^2 + 6^2$")
assert B.comparison("13, 5, 12") == "13^2 = 5^2 + 12^2" and B.comparison("6, 7, 9") == "9^2 < 6^2 + 7^2"
p = dict(type="2", prompt=prompt_of["ex 3.2"], answer="x = 30/7, y = 28/5")
t = B.typst(p)
assert t.startswith("Find $x$ and $y$. #v(0.4em) #align(center)[") and "cetz.canvas" in t, t
assert "[$5$]" in t and "[$x$]" in t and "[$y$]" in t
assert B.answer_typst(p) == "$x = display(30/7), quad y = display(28/5)$", B.answer_typst(p)
assert B.text(p) == "Find x and y.   [figure]" and B.answer_text(p) == "x = 30/7, y = 28/5"
p = dict(type="2", prompt=prompt_of["PS 6"], answer=SOURCES[6][3])
assert B.typst(p).startswith("In the two triangles shown, find the scale factor from right to left.")
assert " \\ x = 8" in B.answer_typst(p), B.answer_typst(p)
assert B.answer_text(p) == "right to left = 2, left to right = 1/2, x = 8, y = 7/2", B.answer_text(p)
p = dict(type="3", prompt=prompt_of["ex 3.3"], answer=SOURCES[2][3])
assert B.typst(p).startswith("Find $x$, $y$, and $z$.") and B.typst(p).count("close: true") == 2
p = dict(type="4", prompt=prompt_of["ex 3.4"], answer=SOURCES[3][3])
assert B.typst(p).startswith("Find $A$, $B$, and $C$.")
assert B.answer_text(p) == "A = 2√(13), B = (4√(13))/3, C = 20/3", B.answer_text(p)
p = dict(type="5", prompt=prompt_of["ex 3.5"], answer=SOURCES[4][3])
assert B.typst(p).startswith("Find $a$, $b$, and $h$.")
# the slide: the answer hidden on the question slide, so the figure never moves
q, a = B.slide_typst(p), B.slide_typst(p, key=True)
ans = B.answer_typst(p)
assert f"#hide[{ans}]" in q and f"#text(fill: red)[{ans}]" in a
assert q.replace(f"#hide[{ans}]", "") == a.replace(f"#text(fill: red)[{ans}]", "")
assert B.height(p) > B.height(dict(type="1", prompt="7, 5, 4", answer="obtuse"))
# the same triangles in another pose are the same problem
assert B.seen_key(dict(type="2", prompt="apart 1 6; 7, 15, y; 3, x, 5")) == \
       B.seen_key(dict(type="2", prompt="apart 3 0; 7, 15, y; 3, x, 5"))

# ---- editing: a new prompt is solved again; a typed answer is checked
old = dict(type="1", prompt="", answer="", source="template")
p, status = B.from_edit("6 in, 8 in, 10 in", old)
assert status == "checked" and p["answer"] == "right", p
p, status = B.with_answer(p, "Right triangle")
assert status == "checked" and p["answer"] == "right", p
p, status = B.with_answer(p, "acute")
assert status != "checked", p
p, status = B.from_edit("bowtie 1; 4, x, 6; 6, 9, y", dict(type="2", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = 6, y = 9", p
p, status = B.from_edit("apart 0 5, factors; 10, x, 8; 5, 6, y", dict(type="2", prompt="", answer=""))
assert status == "checked" and p["answer"] == '"right to left" = 2, "left to right" = 1/2, x = 12, y = 4', p
p, status = B.from_edit("right bowtie 0; 13, x, 12; 26, y, z", dict(type="3", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = 5, y = 10, z = 24", p
p, status = B.with_answer(p, "x = 5, y = 10, z = 24")
assert status == "checked", p
p, status = B.from_edit("base 3 + 6, leg 4; x, y, z", dict(type="4", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = 5, y = 10, z = 12", p
p, status = B.from_edit("9 + 16; a, b, h", dict(type="5", prompt="", answer=""))
assert status == "checked" and p["answer"] == "a = 15, b = 20, h = 12", p
for typ, bad in (("1", "2, 3, 9"), ("1", "7 cm, 5 m, 4 cm"), ("2", "bowtie 0; 5, 4, x"),
                 ("2", "bowtie 0; 5, x, y; 7, z, w"),                   # no pair known in both
                 ("2", "right bowtie 0; 7, x, y; 10, z, 8"),            # a Type 3 prompt under Type 2
                 ("3", "right bowtie 0; 7, x, y; 6, z, 8"),             # a hypotenuse shorter than a leg
                 ("4", "hyp 4 + 8, leg 5; a, b, c"), ("5", "4 + 8; a, a, h"), ("5", "4 and 8")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_3: ok")
