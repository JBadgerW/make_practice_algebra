"""Lesson 17 (Advanced Math): proofs of similarity, and similar or not. Every source is
reachable and its key is the deck's; the proof checkers and the similarity check reject
wrong answers; every type draws, checks, and keeps its rules; edits solve again.

    python3 tests/test_adv_lesson_17.py
"""
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fractions import Fraction as F
from sheets import library
from sheets.banks import adv_lesson_17 as B

lib = library.current()
assert "adv_lesson_17" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 17: Proofs of the Pythagorean Theorem, Proofs of Similarity"
assert B.type_instructions("1") == "Write a two-column proof."

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, the deck's answer)
    ("ex 17.1", "1", "bowtie A B C D E; angle A = angle E; show triangle A B C ~ triangle E D C",
     "angle A = angle E | given; angle A C B = angle E C D | vertical; angle B = angle D | third; "
     "triangle A B C ~ triangle E D C | AAA"),
    ("ex 17.2", "2", "bowtie A B C D E; A B par E D; show triangle A B C ~ triangle D E C",
     "A B par E D | given; angle A C B = angle D C E | vertical; angle A = angle D | parallel; "
     "angle B = angle E | third; triangle A B C ~ triangle D E C | AAA"),
    ("ex 17.3", "3", "sas G H I 30 12 15; J K L 30 8 10; pose 1",
     "angle G = angle J | measure 30; G H/J K = 12/8 | given; G I/J L = 15/10 | given; "
     "G H/J K = G I/J L | 12/8 = 3/2 = 15/10; triangle G H I ~ triangle J K L | SAS"),
    ("PS 4", "4", "sas B C A 6 4; Y Z X 3 2; pose 0", "similar; SAS; triangle A B C ~ triangle X Y Z; 2 : 1"),
    ("PS 5", "4", "sss G H I 2 2 2; J K L 3 3 3; pose 0", "similar; SSS; triangle G H I ~ triangle J K L; 2 : 3"),
    ("PS 6", "5", "marks P Q R S T U; Q T, R U; pose 0", "similar; AA; triangle P Q R ~ triangle S T U"),
    ("PS 7", "5", "angles A B C D E F; A 27, C 115; E 38, D 27; pose 0",
     "angle B = 38, angle F = 115; similar; AAA; triangle A B C ~ triangle D E F"),
    ("PS 8", "2", "bowtie A E D C B; B C par A E; show triangle A D E ~ triangle C D B",
     "B C par A E | given; angle A D E = angle C D B | vertical; angle E = angle B | parallel; "
     "angle A = angle C | third; triangle A D E ~ triangle C D B | AAA"),
]
for sid, typ, prompt, answer in SOURCES:
    assert B.kind_of(prompt) == typ, sid
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt))
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid
p = dict(type="4", prompt=SOURCES[3][2], answer=SOURCES[3][3])
assert B.answer_text(p) == "Similar by SAS: △ABC ~ △XYZ, ratio 2 : 1", B.answer_text(p)
p = dict(type="5", prompt=SOURCES[5][2], answer=SOURCES[5][3])
assert B.answer_text(p).startswith("Similar by AA → AAA: △PQR ~ △STU"), B.answer_text(p)
p = dict(type="3", prompt=SOURCES[2][2], answer=SOURCES[2][3])
assert B.answer_text(p).splitlines()[0] == "1. ∠G ≅ ∠J   Both angles measure 30°", B.answer_text(p)

# ---- every source is reachable: its template builds it from in-range parameters
G, J, A, X, P, S, Dd = (B.ALPHA3.index(c) for c in "GJAXPSD")
REACH = {
    "ex 17.1": (B.bow_build, dict(kind="1", start=0, lettering="run", given=0, goal=0)),
    "ex 17.2": (B.bow_build, dict(kind="2", start=0, lettering="run", given=0, goal=0)),
    "ex 17.3": (B.t3, dict(n1=G, n2=J, deg=30, p2=8, q2=10, r=F(3, 2), pose=1)),
    "PS 4": (B.t4_sas, dict(n1=A, n2=X, k1=1, k2=1, p2=3, q2=2, r=F(2), similar=1, pose=0)),
    "PS 5": (B.t4_sss, dict(n1=G, n2=J, s=(3, 3, 3), r=F(2, 3), similar=1, pose=0)),
    "PS 6": (B.t5_marks, dict(n1=P, n2=S, i=1, j=2, pose=0)),
    "PS 7": (B.t5_angles, dict(n1=A, n2=Dd, A=27, B=38, i1=0, j1=2, i2=1, j2=0, shift=0, pose=0)),
    "PS 8": (B.bow_build, dict(kind="2", start=0, lettering="problem 8", given=1, goal=1)),
}
prompt_of = {s[0]: s[2] for s in SOURCES}
type_of = {s[0]: s[1] for s in SOURCES}
assert set(REACH) == set(prompt_of)
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[type_of[sid]]), sid
assert set(type_of.values()) == set(B.KEYS)
assert not B.in_range(B.t3, dict(n1=G, n2=J, deg=30, p2=3, q2=12, r=F(3, 2), pose=1))    # a sliver
assert not B.in_range(B.t5_angles, dict(n1=A, n2=Dd, A=10, B=38, i1=0, j1=2, i2=1, j2=0, shift=0, pose=0))   # no room for 10°
assert not B.in_range(B.bow_build, dict(kind="3", start=0, lettering="run", given=0, goal=0))

# ---- wrong answers fail
A1, A2, A3 = SOURCES[0][3], SOURCES[1][3], SOURCES[2][3]
P1, P2, P3 = SOURCES[0][2], SOURCES[1][2], SOURCES[2][2]
WRONG = [
    ("1", P1, A1.replace("angle A C B = angle E C D | vertical; ", "")),               # one pair of angles: AA -> AAA fails
    ("1", P1, A1.replace("triangle A B C ~ triangle E D C", "triangle A B C ~ triangle D E C")),   # the wrong order
    ("1", P1, A1.replace("angle A C B = angle E C D", "angle A C B = angle B C D")),   # beside it, not vertical
    ("2", P2, A2.replace("angle A = angle D | parallel", "angle A = angle E | parallel")),   # not alternate interior
    ("2", P2, A2.replace("A B par E D | given; ", "")),                                 # parallels never stated
    ("2", P2, A2.replace("; triangle A B C ~ triangle D E C | AAA", "")),               # the goal never reached
    ("3", P3, A3.replace("= 12/8 | given", "= 12/10 | given")),                         # not the data
    ("3", P3, A3.replace("12/8 = 3/2 = 15/10", "12/8 = 4/3 = 15/10")),                 # the ratio not reduced right
    ("3", P3, A3.replace("triangle G H I ~ triangle J K L", "triangle G H I ~ triangle J L K")),
    ("4", SOURCES[3][2], "similar; SAS; triangle A B C ~ triangle X Y Z; 1 : 2"),       # the ratio upside down
    ("4", SOURCES[3][2], "similar; SAS; triangle A B C ~ triangle Z Y X; 2 : 1"),       # the sides don't match so
    ("4", SOURCES[3][2], "similar; SSS; triangle A B C ~ triangle X Y Z; 2 : 1"),       # not the data's postulate
    ("4", SOURCES[3][2], "not similar"),
    ("4", "sas B C A 6 5; Y Z X 3 2; pose 0", "similar; SAS; triangle A B C ~ triangle X Y Z; 2 : 1"),   # 5/2 isn't 2
    ("5", SOURCES[5][2], "similar; AA; triangle P Q R ~ triangle S U T"),
    ("5", SOURCES[6][2], "similar; AAA; triangle A B C ~ triangle D E F"),              # the missing angles left out
    ("5", "angles A B C D E F; A 27, C 115; E 43, D 27; pose 0",
     "angle B = 38, angle F = 110; similar; AAA; triangle A B C ~ triangle D E F"),   # 115 isn't 110
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)
assert B.check(dict(type="4", prompt="sas B C A 6 5; Y Z X 3 2; pose 0", answer="not similar")) == "checked"
assert B.check(dict(type="5", prompt="angles A B C D E F; A 27, C 115; E 43, D 27; pose 0",
                    answer="angle B = 38, angle F = 110; not similar")) == "checked"

# ---- every type: drawn, checked, and in its rules
rng = random.Random(17)
seen_not = {"4": 0, "5": 0}
for k in B.KEYS:
    for i in range(60):
        if i % 10 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert B.kind_of(p["prompt"]) == k, p
        assert "cetz.canvas" in B.typst(p) and B.slide_typst(p) is not None, p
        if k in ("1", "2"):
            codes = [r.split(" | ")[1] for r in p["answer"].split("; ")]
            assert codes[0] == "given" and codes[1] == "vertical" and codes[-2:] == ["third", "AAA"], p
            assert ("parallel" in codes) == (k == "2"), p
        if k in ("4", "5") and "not similar" in p["answer"]:
            seen_not[k] += 1
assert all(n >= 5 for n in seen_not.values()), seen_not                          # "not similar" comes up

# ---- showing
s = dict(type="2", prompt=SOURCES[1][2], answer=SOURCES[1][3])
assert B.typst(s).startswith("Given: $overline(A B) parallel overline(E D)$. Write a two-column proof to prove: "
                             "$triangle A B C tilde triangle D E C$."), B.typst(s)
assert B.text(dict(type="5", prompt=SOURCES[6][2])).startswith("Determine if △ABC ~ △DEF and justify your answer.")
assert "#hide[" in B.slide_typst(s) and "#hide[" not in B.slide_typst(s, key=True)

# ---- editing
p, status = B.from_edit("sss A B C 4 6 8; D E F 2 3 4", dict(type="4", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"] == "similar; SSS; triangle A B C ~ triangle D E F; 2 : 1", p
p, status = B.with_answer(p, "not similar")
assert status != "checked", p
p, status = B.from_edit("bowtie P Q R S T; angle Q = angle S; show triangle P Q R ~ triangle T S R",
                        dict(type="1", prompt="", answer=""))
assert status == "checked", p
for typ, bad in (("4", "sss A B C 1 2 9; D E F 2 3 4"), ("1", "bowtie A B C D E; show triangle A B C ~ triangle E D C"),
                 ("5", "angles A B C D E F; A 100, C 115; E 38, D 27")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_17: ok")
