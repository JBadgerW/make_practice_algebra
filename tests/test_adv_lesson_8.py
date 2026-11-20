"""Lesson 8 (Advanced Math): similarity statements, proportional segments,
angle bisectors. Every source is reachable from in-range parameters and checks
with the deck's answer; wrong answers fail; every type draws, checks, and keeps
its shape; figures compile from the data; edits solve again.

    python3 tests/test_adv_lesson_8.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_8 as B

lib = library.current()
assert "adv_lesson_8" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 8: Statements of Similarity, Proportional Segments, Angle Bisectors and Side Ratios"
assert B.type_instructions("1") == "Use similar triangles to show that the ratios are equal."
assert B.type_instructions("2") == B.type_instructions("3") == B.EXACT

# ---- every source, and its key
SOURCES = [   # (id, type, prompt, key)
    ("ex 8.1", "1", "altitude A B C D; (A D)/(A B) = (A B)/(A C)",
     "triangle A D B tilde triangle A B C; (A D)/(A B) = (D B)/(B C) = (A B)/(A C)"),            # the deck's
    ("PS 9", "1", "altitude X Y Z M; (X Y)/(X M) = (Y Z)/(M Y)",
     "triangle Y X Z tilde triangle M X Y; (Y X)/(M X) = (X Z)/(X Y) = (Y Z)/(M Y)"),            # directly
    ("ex 8.2", "2", "parallel x + 1, 13; x + 4, 19", "x = 11/2"),
    ("PS 10", "2", "parallel 3x - 1, 12; x + 11, 21", "x = 3"),
    ("ex 8.3", "3", "bisect A B C, B, D; 10, 15, x, 12", "x = 8"),
    ("ex 8.4", "3", "bisect A B C, A, D; x, 20, 6, 14", "x = 60/7"),
    ("PS 11", "3", "bisect A B C, B, D; 8, 12, x, 8", "x = 16/3"),
]
prompt_of = {s[0]: s[2] for s in SOURCES}
src = {s[0]: dict(type=s[1], prompt=s[2], answer=s[3]) for s in SOURCES}
for sid, typ, prompt, key in SOURCES:
    assert B.answer_of(prompt) == key, (sid, B.answer_of(prompt))
    assert B.check(src[sid]) == "checked", sid
# the deck's own route for problem 9 (△XMY ~ △YMZ, then rearranged) is not the key's,
# but its similarity is real: its ratios check against XM/YM = XY/YZ
assert B.check(dict(type="1", prompt="altitude X Y Z M; (X M)/(Y M) = (X Y)/(Y Z)",
                    answer="triangle X M Y tilde triangle Y M Z; (X M)/(Y M) = (M Y)/(M Z) = (X Y)/(Y Z)")) == "checked"

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 8.1": (B.t1_build, dict(names=("A", "B", "C", "D"), pair=("left", "big"), order=(0, 2, 1), swap=False,
                                spell=(False, False, False, False))),
    "PS 9": (B.t1_build, dict(names=("X", "Y", "Z", "M"), pair=("big", "left"), order=(2, 0, 1), swap=False,
                              spell=(True, True, False, False))),
    "ex 8.2": (B.t2_build, dict(a=1, b=1, n1=13, c=1, d=4, n2=19)),
    "PS 10": (B.t2_build, dict(a=3, b=-1, n1=12, c=1, d=11, n2=21)),
    "ex 8.3": (B.t3_build, dict(names=("A", "B", "C"), V="B", D="D", VP=10, VQ=15, PD="x", DQ=12)),
    "ex 8.4": (B.t3_build, dict(names=("A", "B", "C"), V="A", D="D", VP="x", VQ=20, PD=6, DQ=14)),
    "PS 11": (B.t3_build, dict(names=("A", "B", "C"), V="B", D="D", VP=8, VQ=12, PD="x", DQ=8)),
}
assert set(REACH) == set(prompt_of)                                    # nothing left out
TYPE_OF = {s[0]: s[1] for s in SOURCES}
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert sorted(set(TYPE_OF.values())) == B.KEYS
# out of range
assert not B.in_range(B.t2_build, dict(REACH["ex 8.2"][1], c=13))       # a coefficient too big
assert not B.in_range(B.t2_build, dict(REACH["ex 8.2"][1], d=1, n2=13)) # the same segments: no single x
assert not B.in_range(B.t3_build, dict(REACH["ex 8.3"][1], VQ=10))      # sides equal: x is just DC
assert not B.in_range(B.t3_build, dict(REACH["ex 8.3"][1], VP=30, VQ=40, DQ=3))   # a needle of a triangle
assert not B.in_range(B.t3_build, dict(REACH["ex 8.3"][1], D="B"))      # the foot is a vertex

# ---- wrong answers fail
WRONG = [
    ("ex 8.1", "triangle A B D tilde triangle A B C; (A B)/(A B) = (B D)/(B C) = (A D)/(A C)"),   # B and D swapped
    ("ex 8.1", "triangle A D B tilde triangle B D C; (A D)/(B D) = (D B)/(D C) = (A B)/(B C)"),   # true, not asked
    ("ex 8.1", "triangle A D B tilde triangle A B C; (A D)/(A B) = (A B)/(A C)"),                 # two ratios only
    ("ex 8.1", "triangle A D B tilde triangle A B C; (D B)/(B C) = (A D)/(A B) = (A B)/(A C)"),   # out of order
    ("PS 9", "triangle X M Y tilde triangle X Y Z; (X M)/(X Y) = (M Y)/(Y Z) = (X Y)/(X Z)"),     # true, not asked
    ("ex 8.2", "x = 33/6"),                                             # not in lowest terms
    ("ex 8.2", "x = 5"),
    ("PS 10", "x = 2"),
    ("ex 8.3", "x = 18"),                                               # 15/10 of 12: the ratio upside down
    ("ex 8.4", "x = 140/3"),                                            # 20 times 14/6
    ("PS 11", "x = 12"),
    ("PS 11", "x = 32/6"),
]
for sid, answer in WRONG:
    got = B.check(dict(src[sid], answer=answer))
    assert got == "failed", (sid, answer, got)
# a false equation to show: the check catches it
assert B.check(dict(type="1", prompt="altitude A B C D; (A D)/(A B) = (A C)/(A B)",
                    answer="triangle A D B tilde triangle A B C; (A D)/(A B) = (D B)/(B C) = (A B)/(A C)")) == "failed"
try:
    B.answer_of("altitude A B C D; (A D)/(A B) = (B C)/(D C)"); raise AssertionError("no triangle holds AD, BC")
except ValueError:
    pass

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^altitude (\w) (\w) (\w) (\w); \(\w \w\)/\(\w \w\) = \(\w \w\)/\(\w \w\)$",
    "2": r"^parallel [^,;]+, [^,;]+; [^,;]+, [^,;]+$",
    "3": r"^bisect \w \w \w, \w, \w; \S+, \S+, \S+, \S+$",
}
ANSWER = {"1": r"^triangle \w \w \w tilde triangle \w \w \w; (\(\w \w\)/\(\w \w\)( = )?){3}$",
          "2": r"^x = \d+(/\d+)?$", "3": r"^x = \d+(/\d+)?$"}
rng = random.Random(8)
seen_rows = set()
for k in B.KEYS:
    seen = set()
    for i in range(300):
        if i % 50 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.search(SHAPE[k], p["prompt"]), p
        assert re.search(ANSWER[k], p["answer"]), p
        assert B.answer_of(p["prompt"]) == p["answer"], p
        assert "cetz.canvas" in B.typst(p), p
        if k == "2":
            segs = B.read_parallel(p["prompt"])
            seen_rows.add("upper" if segs[0][0] else "lower")
            x = B.solve2(p["prompt"])
            assert 0 < x <= 20 and all(0 < a * x + b <= 60 for a, b in segs), p
        if k == "3":
            vals = B.read_bisect(p["prompt"])[3]
            assert vals.index("x") in (0, 1, 2, 3), p
assert seen_rows == {"upper", "lower"}

# ---- showing
p = src["ex 8.1"]
t = B.typst(p)
assert t.startswith("In $triangle A B C$, segment $B D$ is the altitude to the hypotenuse $A C$. Show the following:")
assert "$display((A D)/(A B)) = display((A B)/(A C))$" in t, t
assert B.answer_typst(p) == ("$triangle A D B tilde triangle A B C$ \\ "
                                 "$display((A D)/(A B)) = display((D B)/(B C)) = display((A B)/(A C))$")
assert B.answer_text(p) == "△ADB ~ △ABC\nAD/AB = DB/BC = AB/AC", B.answer_text(p)
assert B.typst(src["ex 8.2"]).startswith("Find $x$.")
assert B.statement(src["ex 8.4"]) == "In $triangle A B C$, segment $A D$ is the angle bisector of angle $A$. Find $x$."
assert B.answer_typst(src["ex 8.4"]) == "$x = display(60/7)$"
assert "#hide[" in B.slide_typst(src["PS 11"]) and "#text(fill: red)[" in B.slide_typst(src["PS 11"], key=True)
assert B.text(src["ex 8.3"]) == "In △ABC, segment BD is the angle bisector of angle B. Find x.   [figure]", \
    B.text(src["ex 8.3"])

# ---- editing: the data solved again
p, status = B.from_edit("parallel x + 1, 13; x + 5, 19", src["ex 8.2"])
assert status == "checked" and p["answer"] == "x = 23/3", p
p, status = B.from_edit("bisect A B C, B, D; 10, 15, x, 9", src["ex 8.3"])
assert status == "checked" and p["answer"] == "x = 6", p
p, status = B.from_edit("altitude A B C D; (C D)/(C B) = (C B)/(C A)", src["ex 8.1"])
assert status == "checked" and p["answer"].startswith("triangle C D B tilde triangle C B A"), p
for bad, sid in (("parallel x + 1, x; 4, 19", "ex 8.2"), ("bisect A B C, E, D; 10, 15, x, 12", "ex 8.3"),
                 ("Find x", "ex 8.3")):
    try:
        B.from_edit(bad, src[sid]); raise AssertionError(bad)
    except ValueError:
        pass
p, status = B.with_answer(src["ex 8.2"], "x = 11/2")
assert status == "checked"
p, status = B.with_answer(src["ex 8.2"], "x = 11")
assert status == "failed"

print("adv_lesson_8: ok")
