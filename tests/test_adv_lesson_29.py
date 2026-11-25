"""Lesson 29 (Advanced Math): the unit circle, very large and very small
fractions, quadrantal angles. Every source is reachable from in-range
parameters and checks with the deck's answer; wrong and unfinished answers
fail; every type draws, checks, and keeps its shape; edits solve again.

    python3 tests/test_adv_lesson_29.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_29 as B

lib = library.current()
assert "adv_lesson_29" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 29: The Unit Circle, Very Large and Very Small Fractions, Quadrantal Angles"
assert B.type_instructions("1") == "Draw the necessary reference triangles and evaluate. Do not use a calculator."
assert B.type_instructions("4") == "Do not use a calculator."

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 29.1", "1", "3 tan(180 degree)", "0"),
    ("ex 29.2a", "1", "4 sin(270 degree)", "-4"),
    ("ex 29.2b", "1", "3 tan(270 degree)", "undefined"),
    ("ex 29.3", "3", "sin(-135 degree) + 3 sqrt(2) cos(180 degree)", "-(7 sqrt(2))/2"),
    ("PS 17", "3", "2 sin(30 degree) cos(30 degree) - sin(60 degree) + cos(90 degree)", "0"),
    ("PS 18", "2", "2 sin(180 degree) - 3 cos(90 degree) + cos(270 degree)", "0"),
    ("PS 19", "4", "f(theta) = cos(theta); g(theta) = sin(theta); 3 f(60 degree) + g(180 degree)", "3/2"),
    ("PS 20", "4", "r(theta) = (sin(theta))/(cos(theta)); s(theta) = cos(theta) + sin(theta - 300 degree); "
                   "sqrt(3)/2 r(180 degree) + s(30 degree)", "(2 + sqrt(3))/2"),
]
prompt_of = {s[0]: s[2] for s in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 29.1": (B.t1, dict(n=3, f="tan", a=180)),
    "ex 29.2a": (B.t1, dict(n=4, f="sin", a=270)),
    "ex 29.2b": (B.t1, dict(n=3, f="tan", a=270)),
    "ex 29.3": (B.t23, dict(terms=[(1, 1, 1, (("sin", -135),)), (3, 2, 1, (("cos", 180),))])),
    "PS 17": (B.t23, dict(terms=[(2, 1, 1, (("sin", 30), ("cos", 30))), (-1, 1, 1, (("sin", 60),)),
                                 (1, 1, 1, (("cos", 90),))])),
    "PS 18": (B.t23, dict(terms=[(2, 1, 1, (("sin", 180),)), (-3, 1, 1, (("cos", 90),)), (1, 1, 1, (("cos", 270),))])),
    "PS 19": (B.t4, dict(names=("f", "g"), rules=[("one", "cos", None, None), ("one", "sin", None, None)],
                         asks=[((3, 1, 1), 60), ((1, 1, 1), 180)])),
    "PS 20": (B.t4, dict(names=("r", "s"), rules=[("ratio", "sin", "cos", None), ("shifted", "cos", "sin", 300)],
                         asks=[((1, 3, 2), 180), ((1, 1, 1), 30)])),
}
assert set(REACH) == set(prompt_of)                                    # nothing left out
TYPE_OF = {s[0]: s[1] for s in SOURCES}
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params, TYPE_OF[sid]), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert sorted(set(TYPE_OF.values())) == B.KEYS                          # every type has a source
# out of range
assert not B.in_range(B.t1, dict(n=3, f="tan", a=135))                  # not quadrantal: Lesson 27's
assert not B.in_range(B.t23, REACH["ex 29.3"][1], "2")                  # a triangle value in Type 2
assert not B.in_range(B.t23, REACH["PS 18"][1], "3")                    # no triangle value in Type 3
assert not B.in_range(B.t23, dict(terms=[(1, 1, 1, (("tan", 90),)), (1, 1, 1, (("sin", 30),))]), "3")  # undefined
assert not B.in_range(B.t4, dict(REACH["PS 19"][1], asks=[((3, 1, 1), 60), ((1, 1, 1), 30)]))   # no quadrantal

# ---- wrong or unfinished answers fail
WRONG = [
    ("3 tan(180 degree)", "undefined"),
    ("3 tan(180 degree)", "-3"),                                # cos for tan
    ("4 sin(270 degree)", "4"),                                 # the endpoint is (0, -1)
    ("3 tan(270 degree)", "0"),                                 # undefined, not 0
    ("3 tan(270 degree)", "-3"),
    ("sin(-135 degree) + 3 sqrt(2) cos(180 degree)", "-1/sqrt(2) - 3 sqrt(2)"),   # not one fraction
    ("sin(-135 degree) + 3 sqrt(2) cos(180 degree)", "-sqrt(2)/2 - 3 sqrt(2)"),
    ("sin(-135 degree) + 3 sqrt(2) cos(180 degree)", "-(5 sqrt(2))/2"),           # sin(-135°) taken positive
    ("sin(-135 degree) + 3 sqrt(2) cos(180 degree)", "-(14 sqrt(2))/4"),          # not reduced
    ("2 sin(30 degree) cos(30 degree) - sin(60 degree) + cos(90 degree)", "1"),   # cos 90° taken as 1
    ("2 sin(180 degree) - 3 cos(90 degree) + cos(270 degree)", "-3"),
    (prompt_of["PS 19"], "3/2 + 0"),
    (prompt_of["PS 19"], "3 sqrt(3)/2"),                        # sin for cos
    (prompt_of["PS 20"], "1 + sqrt(3)/2"),                      # not one fraction
    (prompt_of["PS 20"], "(sqrt(3) - 2)/2"),                    # sin(-270°) taken as -1
    (prompt_of["PS 20"], "undefined"),
]
for prompt, answer in WRONG:
    typ = "4" if ";" in prompt else "1"
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- one fraction: two radicals over one denominator
import sympy as sp
assert B.written(sp.sqrt(2) / 2 + sp.sqrt(3) / 2) == "(sqrt(2) + sqrt(3))/2"
assert B.written(-sp.sqrt(2) / 2 - sp.sqrt(3) / 3) == "-(2 sqrt(3) + 3 sqrt(2))/6"   # typmath.single's order
assert B.written(sp.Integer(0)) == "0"

# ---- every type: drawn, checked, and in its shape
TERM = r"(-?(\d+ )?(sqrt\(\d\) )?)?((sin|cos|tan)\(-?\d+ degree\) ?)+"
rng = random.Random(29)
counts = {k: dict(zero=0, undefined=0) for k in B.KEYS}
N = 240
for k in B.KEYS:
    seen = set()
    for i in range(N):
        if i % 30 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert B.answer_of(p["prompt"]) == p["answer"], p
        ans = p["answer"]
        counts[k]["zero"] += ans == "0"
        counts[k]["undefined"] += ans == "undefined"
        assert ans == "undefined" or ans.count("/") <= 1, p
        angles = [int(a) for a in re.findall(r"(-?\d+) degree\)", p["prompt"])]
        if k in "12":
            assert all(a % 90 == 0 for a in angles), p
            assert re.fullmatch(rf"{TERM}( [-+] {TERM})*", p["prompt"].replace(" - ", " + ")), p
        if k == "2":
            assert 2 <= len(angles) <= 3 and "sqrt" not in p["prompt"], p
        if k == "3":
            assert any(a % 90 == 0 for a in angles) and any(a % 90 for a in angles), p
        if k == "4":
            names = re.findall(r"(\w)\(theta\) =", p["prompt"])
            assert len(names) == 2 and tuple(names) in B.NAMES, p
        if k != "1":
            assert ans != "undefined", p
assert counts["1"]["undefined"] > N / 10 and counts["2"]["zero"] < N / 3, counts

# ---- showing
p = dict(type="3", prompt=prompt_of["ex 29.3"], answer="-(7 sqrt(2))/2")
assert B.typst(p) == "Evaluate: #h(0.5em) $display(sin(-135 degree) + 3 sqrt(2) cos 180 degree)$", B.typst(p)
assert B.text(p) == "Evaluate: sin(−135°) + 3 sqrt(2) cos 180°", B.text(p)
p = dict(type="4", prompt=prompt_of["PS 20"], answer="(2 + sqrt(3))/2")
assert B.typst(p) == ("If $r(theta) = display((sin theta)/(cos theta))$ and $s(theta) = cos theta + sin(theta - 300 "
                      "degree)$, find $display(sqrt(3)/2) r(180 degree) + s(30 degree)$."), B.typst(p)
assert B.text(p) == "If r(θ) = (sin θ)/(cos θ) and s(θ) = cos θ + sin(θ − 300°), find (sqrt(3)/2) r(180°) + s(30°).", \
    B.text(p)
assert B.answer_typst(dict(type="1", prompt=prompt_of["ex 29.2b"], answer="undefined")) == "undefined"

# ---- editing: new numbers are solved again
src = {s[0]: dict(type=s[1], prompt=s[2], answer=s[3], source="template") for s in SOURCES}
p, status = B.from_edit("5 sin(270°)", src["ex 29.2a"])
assert status == "checked" and p["answer"] == "-5", p
p, status = B.from_edit("3 tan(90°)", src["ex 29.1"])
assert status == "checked" and p["answer"] == "undefined", p
p, status = B.from_edit(prompt_of["PS 19"].replace("g(180 degree)", "g(270 degree)"), src["PS 19"])
assert status == "checked" and p["answer"] == "1/2", p
p, status = B.with_answer(src["PS 20"], "(2 + sqrt(3))/2")
assert status == "checked", p
p, status = B.with_answer(src["PS 20"], "(2 - sqrt(3))/2")
assert status == "failed", p
try:
    B.from_edit("tan of ninety", src["ex 29.1"]); raise AssertionError("unreadable")
except ValueError:
    pass

print("adv_lesson_29: ok")
