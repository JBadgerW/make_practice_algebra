"""Lesson 1 (Advanced Math): geometry review. Every source problem is
reachable from in-range parameters and checks with the deck's answer; wrong
answers fail; every type draws, checks, and keeps its shape; the figures
show; edits solve again.

    python3 tests/test_adv_lesson_1.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_1 as B

lib = library.current()
assert "adv_lesson_1" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 1: Geometry Review"
assert B.type_instructions("1").startswith("Leave each area in terms of π")
assert B.type_instructions("3").startswith("Compare the quantities")
assert B.type_instructions("4") == "Find the unknowns."

# ---- every source: the deck's answer (problems 20, 26, 30: worked here), and checked
SOURCES = [   # (id, type, prompt, answer)
    ("ex 1.1", "2", "unshaded 126, r = 2 sqrt(5) m", '13 pi "m"^2'),
    ("ex 1.2", "3", "x > 0, y < 0; x + y; x - y", "B"),
    ("ex 1.3", "3", "1 < x < 6, 1 < y < 6; x - y; y - x", "D"),
    ("ex 1.4", "5", "left k, top l, right m, bottom n; k + l + m; 180 - n", "A"),
    ("ex 1.5", "6", "ZW || XY; WXY; ZXY", "C"),
    ("PS 20", "4", "top A, left 2B, bottom 3C, right 60", "A = 120, B = 30, C = 40"),
    ("PS 26", "1", "shaded 40, r = 3 sqrt(3) m", '3 pi "m"^2'),
    ("PS 30", "3", "x > 0, y > 0; y - x; y + x", "B"),
]
TYPE_OF = {"ex 1.1": "2", "ex 1.2": "3", "ex 1.3": "3", "ex 1.4": "5", "ex 1.5": "6",
           "PS 20": "4", "PS 26": "1", "PS 30": "3"}               # every source in exactly one type
assert {s[0]: s[1] for s in SOURCES} == TYPE_OF and len(SOURCES) == len(TYPE_OF)
assert set(TYPE_OF.values()) == set(B.KEYS)                       # every type has a source
prompt_of = {sid: prompt for sid, _, prompt, _ in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 1.1": (B.t2_build, dict(angle=126, a=2, b=5, unit="m")),
    "ex 1.2": (B.t3_sign_build, dict(sx=">", sy="<", A="x + y", B="x - y")),
    "ex 1.3": (B.t3_box_build, dict(x0=1, x1=6, y0=1, y1=6, A="x - y", B="y - x")),
    "ex 1.4": (B.t5_build, dict(names="klmn", start=0, A="{0} + {1} + {2}", B="180 - {3}")),
    "ex 1.5": (B.t6_shared_build, dict(names="ZWXY", first=1)),
    "PS 20": (B.t4_build, dict(where="right", k=60, ca=1, cb=2, cc=3)),
    "PS 26": (B.t1_build, dict(angle=40, a=3, b=3, unit="m")),
    "PS 30": (B.t3_sign_build, dict(sx=">", sy=">", A="y - x", B="y + x")),
}
assert set(REACH) == {s[0] for s in SOURCES}                     # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid                         # every parameter inside its named range
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert not B.in_range(B.t4_build, dict(where="right", k=60, ca=1, cb=7, cc=3))
assert not B.in_range(B.t1_build, dict(angle=41, a=3, b=3, unit="m"))   # 41 * 27 / 360: not a nice area

# ---- wrong or unfinished answers fail
WRONG = [
    ("2", "unshaded 126, r = 2 sqrt(5) m", '7 pi "m"^2'),           # the unshaded sector's area
    ("2", "unshaded 126, r = 2 sqrt(5) m", '13 pi "cm"^2'),          # the wrong unit
    ("2", "unshaded 126, r = 2 sqrt(5) m", "13 pi"),                 # no unit
    ("2", "unshaded 126, r = 2 sqrt(5) m", '(234 pi)/18 "m"^2'),     # not reduced
    ("2", "unshaded 126, r = 2 sqrt(5) m", '40.84 "m"^2'),           # a decimal, not in terms of pi
    ("1", "shaded 40, r = 3 sqrt(3) m", '(40/360) pi (3 sqrt(3))^2 "m"^2'),   # not worked out
    ("1", "shaded 40, r = 3 sqrt(3) m", '(sqrt(3) pi)/1 "m"^2'),
    ("3", "x > 0, y < 0; x + y; x - y", "A"),
    ("3", "x > 0, y < 0; x + y; x - y", "D"),
    ("3", "1 < x < 6, 1 < y < 6; x - y; y - x", "C"),
    ("3", "x > 0, y > 0; y - x; y + x", "x"),                        # not a letter
    ("5", "left k, top l, right m, bottom n; k + l + m; 180 - n", "D"),
    ("6", "ZW || XY; WXY; ZXY", "A"),
    ("4", "top A, left 2B, bottom 3C, right 60", "A = 120, B = 60, C = 40"),   # B is 2B's angle
    ("4", "top A, left 2B, bottom 3C, right 60", "A = 120, B = 30"),           # C missing
    ("4", "top A, left 2B, bottom 3C, right 60", "A = 60, B = 30, C = 20"),    # A taken as vertical to 60
    ("1", "unshaded 126, r = 2 sqrt(5) m", '13 pi "m"^2'),           # a Type 2 prompt under Type 1
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^shaded \d+, r = (\d+|(\d )?sqrt\(\d\)) (m|cm|ft|in)$",
    "2": r"^unshaded \d+, r = (\d+|(\d )?sqrt\(\d\)) (m|cm|ft|in)$",
    "3": r"^(x [<>] 0, y [<>] 0|-?\d+ < x < -?\d+, -?\d+ < y < -?\d+); [^;]+; [^;]+$",
    "4": r"^top \d*[A-C]?, left \d*[A-C]?, bottom \d*[A-C]?, right \d*[A-C]?$",
    "5": r"^left [a-z], top [a-z], right [a-z], bottom [a-z]; [^;]+; [^;]+$",
    "6": r"^[A-Z]{2} \|\| [A-Z]{2}(, [A-Z]{2} = \d, [A-Z]{2} = \d)?; [A-Z]{3}; [A-Z]{3}$",
}
ANSWER = {
    "1": r'^(\d* ?pi|\(\d+ pi\)/[234]|pi/[234]) "(m|cm|ft|in)"\^2$', "2": r'^(\d* ?pi|\(\d+ pi\)/[234]|pi/[234]) "(m|cm|ft|in)"\^2$',
    "3": r"^[ABD]$", "4": r"^A = \d+, B = \d+, C = \d+$", "5": r"^[ABCD]$", "6": r"^[ABC]$",
}
rng = random.Random(1)
for k in B.KEYS:
    seen, answers = set(), set()
    for _ in range(80):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.match(SHAPE[k], p["prompt"]), p
        assert re.match(ANSWER[k], p["answer"]), p
        answers.add(p["answer"])
        if k == "4":
            vals = B.read_values(p["answer"])
            assert all(v % 5 == 0 and v > 0 for v in vals.values()), p
            assert sum(1 for t in p["prompt"].split(", ") if re.search(r"\d[A-C]$", t)) >= 1, p
        if k in ("1", "2"):
            assert not re.search(r"\b1 sqrt|r = 1 ", p["prompt"]), p
        if k == "3":
            _, A, Bq = B.read_compare3(p["prompt"])
            assert B.coefs(A) != B.coefs(Bq), p
    if k in ("3", "5", "6"):
        assert len(answers) >= 3, (k, answers)                    # the answers aren't all one letter

# ---- showing: the deck's words, the figure drawn from the data
p = dict(type="2", prompt=prompt_of["ex 1.1"], answer='13 pi "m"^2')
t = B.typst(p)
assert t.startswith("The measure of the central angle of the unshaded sector is $126°$. "
                    "The radius of the circle is $2 sqrt(5)$ m. Find the area"), t
assert "cetz.canvas" in t and "[$126°$]" in t, t
assert B.answer_typst(p) == '$display(13 pi thin "m"^2)$'
assert B.text(p).endswith("[figure]")
assert B.answer_text(p) == "13π m^2", B.answer_text(p)
p = dict(type="4", prompt=prompt_of["PS 20"], answer="A = 120, B = 30, C = 40")
assert B.typst(p).startswith("Find $A$, $B$, and $C$."), B.typst(p)
assert "[$(2 B)°$]" in B.typst(p) and "[$60°$]" in B.typst(p)
p = dict(type="3", prompt=prompt_of["ex 1.2"], answer="B")
assert B.typst(p) == ("Let $x$ and $y$ be real numbers. If $x > 0$ and $y < 0$, compare: \\\n"
                      "#box[A. #h(0.3em) $x + y$] #h(1.5em) #box[B. #h(0.3em) $x - y$]"), B.typst(p)
assert B.slide_typst(p) is None and B.answer_typst(p) == "*B*"
p = dict(type="5", prompt=prompt_of["ex 1.4"], answer="A")
assert "$(k + l + m)°$" in B.typst(p) and "$(180 - n)°$" in B.typst(p)
p = dict(type="6", prompt=prompt_of["ex 1.5"], answer="C")
assert B.typst(p).startswith("Given $overline(Z W)$ and $overline(X Y)$ are parallel, as shown. Compare:")
assert "Area of $triangle W X Y$" in B.typst(p)
# the slide: the answer hidden on the question slide, so the figure never moves
q, a = B.slide_typst(p), B.slide_typst(p, key=True)
assert "#hide[*C*]" in q and "#text(fill: red)[*C*]" in a
assert q.replace("#hide[*C*]", "") == a.replace("#text(fill: red)[*C*]", "")

# ---- editing: a new prompt is solved again; a typed answer is checked
old = dict(type="1", prompt="", answer="", source="template")
p, status = B.from_edit("shaded 90°, r = 4 cm", old)
assert status == "checked" and p["answer"] == '4 pi "cm"^2', p
p, status = B.with_answer(p, '4 pi "cm"^2')
assert status == "checked", p
p, status = B.with_answer(p, '16 pi "cm"^2')
assert status != "checked", p
p, status = B.from_edit("x > 0, y < 0; x; y", dict(type="3", prompt="", answer=""))
assert status == "checked" and p["answer"] == "A", p
p, status = B.from_edit("2 < x < 5, 1 < y < 3; x + 2 y; 3 x", dict(type="3", prompt="", answer=""))
assert status == "checked" and p["answer"] == "D", p
p, status = B.with_answer(p, "d")
assert status == "checked" and p["answer"] == "D", p
p, status = B.from_edit("top 2A, left 4B, bottom 100, right C", dict(type="4", prompt="", answer=""))
assert status == "checked" and p["answer"] == "A = 50, B = 20, C = 80", p
p, status = B.from_edit("left k, top l, right m, bottom n; k; m", dict(type="5", prompt="", answer=""))
assert status == "checked" and p["answer"] == "C", p
p, status = B.from_edit("AB || CE, CD = 3, DE = 5; ACD; BDE", dict(type="6", prompt="", answer=""))
assert status == "checked" and p["answer"] == "B", p
for typ, bad in (("1", "shaded 40, r ="), ("3", "x > 0; x"), ("4", "top A, left B"),
                 ("6", "ZW || XY; WXZ; ZXY"), ("1", "x > 0, y < 0; x; y"),
                 ("4", "top 2A, left 3B, bottom 100, right C")):         # 3B = 80: B isn't whole
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_1: ok")
