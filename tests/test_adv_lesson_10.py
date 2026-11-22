"""Lesson 10 (Advanced Math): equation of a line, rational denominators, completing
the square. Every source is reachable and checks with the deck's answer; wrong and
unfinished answers fail; every type draws and checks in its rules; edits solve again.

    python3 tests/test_adv_lesson_10.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_10 as B

lib = library.current()
assert "adv_lesson_10" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 10: Equation of a Line, Rational Denominators, Completing the Square"
assert B.type_instructions("1") == "Write each equation in slope-intercept form."
assert B.type_instructions("7") == "Solve by completing the square."
assert not B.PREAMBLE == ""                                       # the graphs' cetz import

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 10.1", "1", "(-3, 2), (4, -3)", "y = -5/7 x - 1/7"),
    ("ex 10.2", "3", "3 y + 4 x = 2; (-2, 5)", "y = 3/4 x + 13/2"),
    ("ex 10.3", "4", "y = -2; (-6, -5), (-1, 6)", "y = -2; y = 11/5 x + 41/5"),
    ("ex 10.4", "5", "(4 + sqrt(3))/(2 - 3 sqrt(3))", "(-17 - 14 sqrt(3))/23"),
    ("ex 10.5", "6", "(2 - i^3 + 2 i^5)/(-2 i + 4)", "1/10 + 4/5 i"),
    ("ex 10.6", "7", "-x + 3 x^2 = -5", "x = 1/6 plus.minus sqrt(59)/6 i"),
    ("PS 5", "1", "(1, 0), (0, 1)", "y = -x + 1"),
    ("PS 6", "2", "y = 2 x - 1; (4, 1)", "y = 2 x - 7"),
    ("PS 9", "6", "(2 + i)/(3 - 2 i)", "4/13 + 7/13 i"),
    ("PS 10", "6", "(2 + i - 2 i^3)/(2 i^3 + 4)", "1/10 + 4/5 i"),
    ("PS 11", "5", "(2 + 2 sqrt(3))/(1 - sqrt(3))", "-4 - 2 sqrt(3)"),
    ("PS 12", "7", "x^2 - 4 x - 12 = 0", "x = 6 or x = -2"),
    ("PS 13", "7", "x + 3 x^2 = -5", "x = -1/6 plus.minus sqrt(59)/6 i"),
]
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt, typ) == answer, (sid, B.answer_of(prompt, typ), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 10.1": (B.t1, dict(x1=-3, y1=2, x2=4, y2=-3)),
    "ex 10.2": (B.t3, dict(form="y first", a=4, c=3, k=2, px=-2, py=5)),
    "ex 10.3": (B.t4, dict(kind="y", k=-2, x1=-6, y1=-5, x2=-1, y2=6)),
    "ex 10.4": (B.t5, dict(a=4, b=1, d=2, e=-3, c=3)),
    "ex 10.5": (B.t6, dict(top=((2, 0), (-1, 3), (2, 5)), bottom=((-2, 1), (4, 0)))),
    "ex 10.6": (B.t7_scrambled, dict(v="x", a=3, b=-1, c=5)),
    "PS 5": (B.t1, dict(x1=1, y1=0, x2=0, y2=1)),
    "PS 6": (B.t2, dict(form="si", a=2, c=1, k=-1, px=4, py=1)),
    "PS 9": (B.t6, dict(top=((2, 0), (1, 1)), bottom=((3, 0), (-2, 1)))),
    "PS 10": (B.t6, dict(top=((2, 0), (1, 1), (-2, 3)), bottom=((2, 3), (4, 0)))),
    "PS 11": (B.t5, dict(a=2, b=2, d=1, e=-1, c=3)),
    "PS 12": (B.t7_monic, dict(v="x", b=-4, c=-12)),
    "PS 13": (B.t7_scrambled, dict(v="x", a=3, b=1, c=5)),
}
prompt_of = {s[0]: s[2] for s in SOURCES}
type_of = {s[0]: s[1] for s in SOURCES}
assert set(REACH) == set(prompt_of)                                  # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[type_of[sid]]), sid  # a template of the source's own type
assert set(type_of.values()) == set(B.KEYS)                          # every type has a source
assert not B.in_range(B.t2, dict(form="si", a=2, c=1, k=-1, px=1, py=1))    # parallel through a point on the line
assert not B.in_range(B.t4, dict(kind="y", k=-5, x1=-6, y1=-5, x2=-1, y2=6))  # an endpoint on line (a)
assert not B.in_range(B.t5, dict(a=2, b=2, d=1, e=1, c=3))                  # top a multiple of the bottom
assert not B.in_range(B.t6, dict(top=((2, 0), (1, 3), (-1, 3)), bottom=((3, 0), (-2, 1))))  # like powers twice
assert not B.in_range(B.t7_monic, dict(v="x", b=-4, c=4))                    # a double root

# ---- wrong or unfinished answers fail
WRONG = [
    ("1", "(-3, 2), (4, -3)", "y = 5/7 x - 1/7"),                   # a sign error in the slope
    ("1", "(-3, 2), (4, -3)", "y + 1/7 = -5/7 x"),                  # not slope-intercept form
    ("1", "(1, 0), (0, 1)", "y = -1 x + 1"),                        # 1 x
    ("2", "y = 2 x - 1; (4, 1)", "y = -1/2 x + 3"),                 # perpendicular, not parallel
    ("3", "3 y + 4 x = 2; (-2, 5)", "y = -4/3 x + 7/3"),            # parallel, not perpendicular
    ("3", "3 y + 4 x = 2; (-2, 5)", "y = 6/8 x + 13/2"),            # not in lowest terms
    ("4", "y = -2; (-6, -5), (-1, 6)", "x = -2; y = 11/5 x + 41/5"),  # (a) vertical
    ("4", "y = -2; (-6, -5), (-1, 6)", "y = -2; y = 11/5 x + 8"),   # (b) misses a point
    ("5", "(4 + sqrt(3))/(2 - 3 sqrt(3))", "(17 + 14 sqrt(3))/23"), # a sign error below
    ("5", "(4 + sqrt(3))/(2 - 3 sqrt(3))", "(17 + 14 sqrt(3))/(-23)"),  # the minus left below
    ("5", "(2 + 2 sqrt(3))/(1 - sqrt(3))", "(8 + 4 sqrt(3))/(-2)"), # not reduced
    ("5", "(2 + 2 sqrt(3))/(1 - sqrt(3))", "(2 + 2 sqrt(3))/(1 - sqrt(3))"),  # not rationalized
    ("6", "(2 + i)/(3 - 2 i)", "(4 + 7 i)/13"),                     # not split into a + b i
    ("6", "(2 + i)/(3 - 2 i)", "4/13 - 7/13 i"),                    # a sign error
    ("6", "(2 - i^3 + 2 i^5)/(-2 i + 4)", "2/20 + 16/20 i"),        # not reduced
    ("7", "x^2 - 4 x - 12 = 0", "x = 6"),                           # a missing root
    ("7", "x^2 - 4 x - 12 = 0", "x = 2 plus.minus 4"),              # rational roots, not split
    ("7", "x^2 - 4 x - 12 = 0", "y = 6 or y = -2"),                 # the wrong letter
    ("7", "-x + 3 x^2 = -5", "x = 1/6 plus.minus sqrt(-59)/6"),     # a square root of a negative
    ("7", "-x + 3 x^2 = -5", "x = 1/6 plus.minus sqrt(59/36) i"),   # not simplified
    ("7", "-x + 3 x^2 = -5", "x = -1/6 plus.minus sqrt(59)/6 i"),   # the wrong sign
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)
# the minus-in-front form is accepted too
assert B.check(dict(type="5", prompt="(4 + sqrt(3))/(2 - 3 sqrt(3))", answer="-(17 + 14 sqrt(3))/23")) == "checked"

# ---- every type: drawn, checked, and in its rules
SHAPE = {
    "1": re.compile(r"\(-?\d+, -?\d+\), \(-?\d+, -?\d+\)"),
    "2": re.compile(r"(y = [^;]*x[^;]*|-?\d* ?[xy] [+-] \d* ?[xy] = -?\d+); \(-?\d+, -?\d+\)"),
    "4": re.compile(r"[xy] = -?[1-5]; \(-?\d, -?\d\), \(-?\d, -?\d\)"),
    "5": re.compile(r"\(\d+ [+-] (\d+ )?sqrt\((\d+)\)\)/\(\d+ [+-] (\d+ )?sqrt\(\2\)\)"),
    "6": re.compile(r"\(.*i.*\)/\(.*i.*\)"),
    "7": re.compile(r".*[a-z]\^2.* = -?\d+"),
}
SHAPE["3"] = SHAPE["2"]
LINE_ANSWER = re.compile(r"y = -?(\d+(/\d+)? )?x( [+-] \d+(/\d+)?)?")
rng = random.Random(10)
for k in B.KEYS:
    seen = set()
    for _ in range(80):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert SHAPE[k].fullmatch(p["prompt"]), (k, p)
        if k in "123":
            assert LINE_ANSWER.fullmatch(p["answer"]), p
        if k in "23":
            head, pts = B.split_line(p["prompt"])
            assert B.slope_of_given(head) != 0 and len(pts) == 1, p     # a line with a slope, one point
            if k == "2":                                                # the point is off the given line
                lhs, _, rhs = head.partition("=")
                at = {B.X: pts[0][0], B.Y: pts[0][1]}
                assert B.to_sympy(lhs).subs(at) != B.to_sympy(rhs).subs(at), p
        if k == "4":
            assert B.labels(*B.split_line(p["prompt"])) is not None, p
        if k == "6":
            assert re.fullmatch(r"-?\d+(/\d+)? [+-] (\d+(/\d+)? )?i", p["answer"]), p
        if k == "7":
            assert " or " in p["answer"] or "plus.minus" in p["answer"], p
        assert not re.search(r"(^|[ (])1 [a-z(]", p["prompt"]), p       # no 1 x, 1 sqrt, 1 i

# ---- showing: each problem says what to do
s = dict(type="3", prompt="3 y + 4 x = 2; (-2, 5)", answer="y = 3/4 x + 13/2")
assert B.text(s) == "Find the equation of the line that passes through (−2, 5) and is perpendicular to the line 3 y + 4 x = 2.", B.text(s)
assert B.typst(s).startswith("Find the equation of the line that passes through #box["), B.typst(s)
g = dict(type="4", prompt="y = -2; (-6, -5), (-1, 6)", answer="y = -2; y = 11/5 x + 41/5")
assert B.typst(g).startswith("Find the equations of lines (a) and (b).") and "cetz.canvas" in B.typst(g)
assert B.answer_text(g) == "(a) y = −2   (b) y = 11/5 x + 41/5", B.answer_text(g)
assert B.slide_typst(g) is not None and B.slide_typst(s) is None
assert "#hide[" in B.slide_typst(g) and "#hide[" not in B.slide_typst(g, key=True)
q = dict(type="7", prompt="-x + 3 x^2 = -5", answer="x = 1/6 plus.minus sqrt(59)/6 i")
assert B.text(q) == "Solve by completing the square: −x + 3 x^2 = −5", B.text(q)
assert B.answer_text(q) == "x = 1/6 ± sqrt(59)/6 i", B.answer_text(q)

# ---- editing: a new prompt is solved again; a typed answer is checked
p, status = B.from_edit("(2 + i)/(1 - i)", dict(type="6", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"] == "1/2 + 3/2 i", p
p, status = B.with_answer(p, "(1 + 3 i)/2")
assert status != "checked", p
p, status = B.from_edit("y = 3 x + 2; (1, 1)", dict(type="3", prompt="", answer=""))
assert status == "checked" and p["answer"] == "y = -1/3 x + 4/3", p
p, status = B.from_edit("x^2 + 2 x - 4 = 0", dict(type="7", prompt="", answer=""))
assert status == "checked" and p["answer"] == "x = -1 plus.minus sqrt(5)", p
for typ, bad in (("1", "(1, 2)"), ("5", "(4 + sqrt(3)/("), ("7", "x + 2 = 0")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_10: ok")
