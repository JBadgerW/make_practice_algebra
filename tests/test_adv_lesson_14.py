"""Lesson 14 (Advanced Math): sine, cosine, tangent; elevation and depression; polar
coordinates. Every source is reachable and checks with the deck's answer; wrong answers
fail; every type draws, checks, and keeps its rules; edits solve again.

    python3 tests/test_adv_lesson_14.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_14 as B

I, J = B.I, B.J
lib = library.current()
assert "adv_lesson_14" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == ("Lesson 14: Sine, Cosine, and Tangent, Angles of Elevation and Depression, "
                   "Rectangular and Polar Coordinates, Coordinate Conversion")
assert B.type_instructions("5") == "Convert to polar coordinates. Write four forms."
assert B.type_instructions("6") == "Convert to rectangular coordinates."
assert "$" not in "".join(B.type_instructions(k) for k in B.KEYS)

ELEV = ("A man 6 feet tall is 200 feet from a tree and measures the angle of elevation to the top of the tree "
        "as 11°. How tall is the tree?")
DEP = ("An airplane is flying at an altitude of {} feet above the ground. The pilot sights an object on the ground "
       "at an angle of depression of {}°. What is the slant range from the airplane to the object?")

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 14.1", "1", "6, 36; A, B; pose 0", "A = 4.85, B = 3.53"),
    ("ex 14.2", "2", "7, 3 opposite; M, x; pose 0", "M = 25.38 degree, x = 6.32"),
    ("ex 14.3", "3", ELEV, "44.88 ft"),
    ("ex 14.4", "4", DEP.format(3000, 26), "6843.52 ft"),
    ("ex 14.5", "5", f"-3 {I} + 2 {J}",
     "sqrt(13)/146.31 degree, sqrt(13)/-213.69 degree, -sqrt(13)/-33.69 degree, -sqrt(13)/326.31 degree"),
    ("ex 14.6", "6", "-13/-253 degree", f"(3.80, -12.43) or 3.80 {I} - 12.43 {J}"),
    ("PS 4", "4", DEP.format(5000, 28), "10650.27 ft"),
    ("PS 5", "5", f"3.06 {I} - 2.75 {J}",
     "4.11/-41.95 degree, 4.11/318.05 degree, -4.11/138.05 degree, -4.11/-221.95 degree"),
    ("PS 6", "5", f"-2.41 {I} + 7.3 {J}",
     "7.69/108.27 degree, 7.69/-251.73 degree, -7.69/-71.73 degree, -7.69/288.27 degree"),
    ("PS 7", "6", "-8.6/265 degree", f"(0.75, 8.57) or 0.75 {I} + 8.57 {J}"),
    ("PS 8", "6", "7.42/-143 degree", f"(-5.93, -4.47) or -5.93 {I} - 4.47 {J}"),
]
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt, typ) == answer, (sid, B.answer_of(prompt, typ), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 14.1": (B.t1, dict(h=6, a=36, legs=("A", "B"), swap=0, pose=0)),
    "ex 14.2": (B.t2, dict(h=7, leg=3, where="opposite", angle="M", side="x", pose=0)),
    "ex 14.3": (B.t3, dict(person="man", h=6, d=200, thing="tree", a=11)),
    "ex 14.4": (B.t4, dict(vehicle="airplane", alt=3000, a=26)),
    "ex 14.5": (B.t5_whole, dict(x=-3, y=2)),
    "ex 14.6": (B.t6, dict(r=-1300, theta=-253)),
    "PS 4": (B.t4, dict(vehicle="airplane", alt=5000, a=28)),
    "PS 5": (B.t5_decimal, dict(x=306, y=-275)),
    "PS 6": (B.t5_decimal, dict(x=-241, y=730)),
    "PS 7": (B.t6, dict(r=-860, theta=265)),
    "PS 8": (B.t6, dict(r=742, theta=-143)),
}
prompt_of = {s[0]: s[2] for s in SOURCES}
type_of = {s[0]: s[1] for s in SOURCES}
assert set(REACH) == set(prompt_of)                                  # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[type_of[sid]]), sid
assert set(type_of.values()) == set(B.KEYS)                          # every type has a source
assert not B.in_range(B.t1, dict(h=6, a=85, legs=("A", "B"), swap=0, pose=0))   # a sliver of a triangle
assert not B.in_range(B.t2, dict(h=7, leg=7, where="opposite", angle="M", side="x", pose=0))
assert not B.in_range(B.t5_decimal, dict(x=300, y=-200))             # both whole: Type 5's other template
assert not B.in_range(B.t6, dict(r=-1300, theta=-270))               # on an axis

# ---- wrong answers fail
WRONG = [
    ("1", "6, 36; A, B; pose 0", "A = 3.53, B = 4.85"),               # sine and cosine crossed
    ("1", "6, 36; A, B; pose 0", "B = 3.53, A = 4.85"),               # not in order
    ("1", "6, 36; A, B; pose 0", "A = 4.854, B = 3.527"),             # not to two places
    ("2", "7, 3 opposite; M, x; pose 0", "M = 64.62 degree, x = 6.32"),   # the cosine used
    ("2", "7, 3 opposite; M, x; pose 0", "M = 25.38, x = 6.32"),      # no degrees
    ("3", ELEV, "38.88 ft"),                                           # eye height left off
    ("3", ELEV, "44.88"),                                              # no unit
    ("4", DEP.format(3000, 26), "3337.94 ft"),                         # cos 26: the angle not moved
    ("4", DEP.format(3000, 26), "6843.51 ft"),                         # rounded wrong
    ("5", f"-3 {I} + 2 {J}",
     "sqrt(13)/33.69 degree, sqrt(13)/-326.31 degree, -sqrt(13)/-146.31 degree, -sqrt(13)/213.69 degree"),  # quadrant
    ("5", f"-3 {I} + 2 {J}",
     "3.61/146.31 degree, 3.61/-213.69 degree, -3.61/-33.69 degree, -3.61/326.31 degree"),   # r not exact
    ("5", f"-3 {I} + 2 {J}",
     "sqrt(13)/-213.69 degree, sqrt(13)/146.31 degree, -sqrt(13)/-33.69 degree, -sqrt(13)/326.31 degree"),  # order
    ("5", f"-3 {I} + 2 {J}", "sqrt(13)/146.31 degree"),               # one form
    ("6", "-13/-253 degree", f"(-3.80, 12.43) or -3.80 {I} + 12.43 {J}"),   # the negative r ignored
    ("6", "-13/-253 degree", f"(3.80, -12.43) or 3.80 {I} + 12.43 {J}"),    # the two forms disagree
    ("6", "-13/-253 degree", "(3.8, -12.43)"),                         # one form, one place
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its rules
SHAPE = {
    "1": re.compile(r"\d+, \d+; [A-Za-z], [A-Za-z]; pose [01]"),
    "2": re.compile(r"\d+, \d+ (opposite|adjacent); [A-Z], [xy]; pose [01]"),
    "3": re.compile(r"A (man|woman|surveyor|student) \d feet tall is \d+ feet from a \w+ and measures .*"),
    "4": re.compile(r"(An airplane|A helicopter) is flying at an altitude of \d+ feet .*"),
    "5": re.compile(rf"-?\d+(\.\d+)? {re.escape(I)} [+-] \d+(\.\d+)? {re.escape(J)}"),
    "6": re.compile(r"-?\d+(\.\d\d?)?/-?\d+ degree"),
}
rng = random.Random(14)
for k in B.KEYS:
    for i in range(60):
        if i % 20 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert SHAPE[k].fullmatch(p["prompt"]), (k, p)
        assert not re.search(r"(?<![\d.])-?0\.00\b", p["answer"]), p           # no point on an axis
        if k in B.FIGURES:
            assert "cetz.canvas" in B.typst(p) and B.slide_typst(p) is not None, p
        else:
            assert B.slide_typst(p) is None
        if k == "5":
            assert len(p["answer"].split(", ")) == 4, p

# ---- showing
s = dict(type="2", prompt="7, 3 opposite; M, x; pose 0", answer="M = 25.38 degree, x = 6.32")
assert B.typst(s).startswith("Find angle $M$ and side $x$.")
assert B.text(s) == "Find angle M and side x.   [figure: 7, 3 opposite; M, x; pose 0]", B.text(s)
assert B.answer_text(s) == "M = 25.38°, x = 6.32", B.answer_text(s)
assert "#hide[" in B.slide_typst(s) and "#hide[" not in B.slide_typst(s, key=True)
q = dict(type="6", prompt="-13/-253 degree", answer=f"(3.80, -12.43) or 3.80 {I} - 12.43 {J}")
assert 'underline(\\/ class("unary", -) 253 degree)' in B.typst(q), B.typst(q)
assert B.text(q) == "Convert to rectangular coordinates: -13/-253°", B.text(q)
assert B.answer_text(q) == "(3.80, -12.43) or 3.80î - 12.43ĵ", B.answer_text(q)
assert B.text(dict(type="3", prompt=ELEV)) == ELEV

# ---- editing: a new prompt is solved again; a typed answer is checked
p, status = B.from_edit("10, 30; A, B; pose 1", dict(type="1", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"] == "A = 8.66, B = 5.00", p
p, status = B.with_answer(p, "A = 5.00, B = 8.66")
assert status != "checked", p
p, status = B.from_edit(ELEV.replace("200", "100"), dict(type="3", prompt="", answer=""))
assert status == "checked" and p["answer"] == "25.44 ft", p
p, status = B.from_edit(f"3 {I} - 4 {J}", dict(type="5", prompt="", answer=""))
assert status == "checked" and p["answer"].startswith("5/-53.13 degree, 5/306.87 degree, -5/126.87 degree"), p
p, status = B.from_edit("5/30 degree", dict(type="6", prompt="", answer=""))
assert status == "checked" and p["answer"] == f"(4.33, 2.50) or 4.33 {I} + 2.50 {J}", p
for typ, bad in (("1", "6, 36"), ("2", "7, 9 opposite; M, x"), ("3", "How tall is the tree?"),
                 ("5", "3 + 4 i"), ("6", "-13 at 253")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_14: ok")
