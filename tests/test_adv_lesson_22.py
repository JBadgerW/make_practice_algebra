"""Lesson 22 (Advanced Math): absolute value, reciprocal functions. Every
source problem is reachable from in-range parameters and checks with the
deck's answer; wrong answers fail; every type draws, checks, and keeps its
shape; the figures are drawn from the data; edits solve again.

    python3 tests/test_adv_lesson_22.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_22 as B

lib = library.current()
assert "adv_lesson_22" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 22: Absolute Value, Reciprocal Functions"
assert B.type_instructions("1") == B.type_instructions("2") == "Graph each set on the real number line."
assert B.type_instructions("3") == "Graph each inequality on the real number line."
assert B.type_instructions("4") == B.type_instructions("5") == "Sketch the graph of each function."
assert B.type_instructions("6").endswith("Sketch the graph of the reciprocal function g.")

# ---- every source: the deck's answer, and checked
TABLE = "(-2, 0.25), (-1, 1), (-0.5, 4), (0.5, 4), (1, 1), (2, 0.25)"
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 22.1", "3", "abs(x) - 2 < 0", "-2 < x < 2"),
    ("ex 22.2", "1", "abs(x - 5) < 2", "3 < x < 7"),
    ("ex 22.3", "2", "abs(x + 2) >= 3", 'x <= -5 "or" x >= 1'),
    ("PS 6a", "1", "abs(x - 3) < 4", "-1 < x < 7"),
    ("PS 6b", "2", "abs(x - 3) >= 4", 'x <= -1 "or" x >= 7'),
    ("ex 22.4", "4", "y = abs(x)", "(-2, 2), (0, 0), (2, 2)"),
    ("PS 7", "4", "f(x) = abs(x)", "(-2, 2), (0, 0), (2, 2)"),
    ("ex 22.5", "5", "y = 1/x^2", "x = 0; " + TABLE),
    ("PS 8", "6", "f(x) = x + 3; g(x) = 1/(x + 3)", "x = -3; (-2, 1), (-4, -1)"),
]
TYPE_OF = {"ex 22.1": "3", "ex 22.2": "1", "ex 22.3": "2", "PS 6a": "1", "PS 6b": "2", "ex 22.4": "4",
           "PS 7": "4", "ex 22.5": "5", "PS 8": "6"}                # every source in exactly one type
assert {s[0]: s[1] for s in SOURCES} == TYPE_OF and len(SOURCES) == len(TYPE_OF)
assert set(TYPE_OF.values()) == set(B.KEYS)                       # every type has a source
prompt_of = {sid: prompt for sid, _, prompt, _ in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 22.1": (B.t3_build, dict(a=0, c=-2, op="<", d=0)),
    "ex 22.2": (B.t1_build, dict(a=5, k=2, op="<")),
    "ex 22.3": (B.t2_build, dict(a=-2, k=3, op=">=")),
    "PS 6a": (B.t1_build, dict(a=3, k=4, op="<")),
    "PS 6b": (B.t2_build, dict(a=3, k=4, op=">=")),
    "ex 22.4": (B.t4_build, dict(name="y", a=0, c=0)),
    "PS 7": (B.t4_build, dict(name="f", a=0, c=0)),
    "ex 22.5": (B.t5_build, dict(name="y", a=0)),
    "PS 8": (B.t6_build, dict(b=3, down=False)),
}
assert set(REACH) == {s[0] for s in SOURCES}                     # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid                         # every parameter inside its named range
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert not B.in_range(B.t1_build, dict(a=5, k=2, op=">"))         # Type 2's sign
assert not B.in_range(B.t3_build, dict(a=0, c=-2, op="<", d=-2))  # |x| < 0: no distance
assert not B.in_range(B.t6_build, dict(b=0, down=True))           # f(x) = 0 - x

# ---- wrong or unfinished answers fail
WRONG = [
    ("1", "abs(x - 5) < 2", "3 <= x <= 7"),                         # solid circles for <
    ("1", "abs(x - 5) < 2", "-7 < x < -3"),                         # the center's sign
    ("1", "abs(x - 5) < 2", 'x < 3 "or" x > 7'),                    # rays for "within"
    ("1", "abs(x - 5) < 2", "-2 < x < 2"),                          # the center forgotten
    ("1", "abs(x - 5) < 2", "7 > x > 3"),                           # not the key's form
    ("2", "abs(x + 2) >= 3", "-5 <= x <= 1"),                       # one piece for "farther"
    ("2", "abs(x + 2) >= 3", 'x <= -1 "or" x >= 5'),                # the center as +2
    ("2", "abs(x + 2) >= 3", 'x < -5 "or" x > 1'),                  # open circles for >=
    ("2", "abs(x + 2) >= 3", 'x >= 1 "or" x <= -5'),                # the right ray first
    ("2", "abs(x - 3) >= 4", 'x <= -1 "or" x >= 1'),
    ("3", "abs(x) - 2 < 0", "0 < x < 2"),                           # half of it
    ("3", "abs(x) - 2 < 0", "-2 <= x <= 2"),
    ("3", "abs(x - 1) + 3 > 7", 'x < -9 "or" x > 11'),              # 3 added, not subtracted
    ("1", "abs(x) - 2 < 0", "-2 < x < 2"),                          # a Type 3 prompt under Type 1
    ("1", "abs(x + 2) >= 3", 'x <= -5 "or" x >= 1'),                # a Type 2 prompt under Type 1
    ("4", "y = abs(x)", "(-2, -2), (0, 0), (2, 2)"),                # the line y = x
    ("4", "f(x) = abs(x - 3)", "(-5, 2), (-3, 0), (-1, 2)"),        # shifted the wrong way
    ("4", "y = abs(x) + 2", "(-2, 2), (0, 0), (2, 2)"),             # the shift forgotten
    ("4", "y = abs(x)", "(-1, 1), (0, 0), (1, 1)"),                 # not the deck's table
    ("4", "y = abs(x)", "(0, 0), (2, 2), (4, 4)"),                  # the vertex isn't in the middle
    ("5", "y = 1/x^2", "x = 0; (-2, -0.25), (-1, -1), (-0.5, -4), (0.5, 4), (1, 1), (2, 0.25)"),   # below the axis
    ("5", "y = 1/x^2", "x = 1; " + TABLE),                          # the asymptote
    ("5", "y = 1/x^2", "x = 0; (-2, 0.5), (-1, 1), (-0.5, 2), (0.5, 2), (1, 1), (2, 0.5)"),         # 1/x's values
    ("5", "y = 1/x^2", "x = 0; (-2, 1/4), (-1, 1), (-1/2, 4), (1/2, 4), (1, 1), (2, 1/4)"),         # not in decimals
    ("5", "y = 1/(x - 2)^2", "x = -2; (-4, 0.25), (-3, 1), (-2.5, 4), (-1.5, 4), (-1, 1), (0, 0.25)"),
    ("6", prompt_of["PS 8"], "x = 3; (-2, 1), (-4, -1)"),           # the asymptote's sign
    ("6", prompt_of["PS 8"], "x = -3; (-2, 1), (-4, 1)"),
    ("6", prompt_of["PS 8"], "x = -3; (-2, 1), (-3, 0)"),           # the x intercept isn't on g
    ("6", "f(x) = x + 3; g(x) = 1/(x - 3)", "x = -3; (-2, 1), (-4, -1)"),   # g isn't f's reciprocal
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)
p = dict(type="1", prompt="abs(x - 5) < 2", answer="3 < x < 7", line=[3, 9])
assert B.check(p) == "failed"                                     # the graph's end is at the line's end
assert B.check(dict(p, line=[2, 8])) == "checked"

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^abs\(x( [+-] \d)?\) <=? [1-6]$",
    "2": r"^abs\(x( [+-] \d)?\) >=? [1-6]$",
    "3": r"^abs\(x( [+-] \d)?\) [+-] \d (<|<=|>|>=) -?\d+$",
    "4": r"^(y|[fgh]\(x\)) = abs\(x( [+-] \d)?\)( [+-] \d)?$",
    "5": r"^(y|[fgh]\(x\)) = 1/(x\^2|\(x [+-] \d\)\^2)$",
    "6": r"^f\(x\) = (x|x [+-] \d|\d - x); g\(x\) = 1/(x|\(x [+-] \d\)|\(\d - x\))$",
}
POINT = r"\(-?\d+(\.\d+)?, -?\d+(\.\d+)?\)"
ANSWER = {
    "1": r"^-?\d+ (<|<=) x \1 -?\d+$", "2": r'^x (<|<=) -?\d+ "or" x (>|>=) -?\d+$',
    "3": r'^(-?\d+ (<|<=) x \2 -?\d+|x (<|<=) -?\d+ "or" x (>|>=) -?\d+)$',
    "4": rf"^{POINT}, {POINT}, {POINT}$", "5": rf"^x = -?\d; {POINT}(, {POINT}){{5}}$",
    "6": r"^x = -?\d; \(-?\d, 1\), \(-?\d, -1\)$",
}
rng = random.Random(22)
for k in B.KEYS:
    seen, answers = set(), set()
    for i in range(80):
        if i % 10 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.match(SHAPE[k], p["prompt"]), p
        assert re.match(ANSWER[k], p["answer"]), p
        assert not re.search(r"\b1 (x|abs)|\+ -|- -|[+-] 0\b", p["prompt"]), p
        assert ("line" in p) == (k in "123"), p
        if "line" in p:
            lo, hi = p["line"]
            ends = [int(n) for n in re.findall(r"-?\d+", p["answer"])]
            assert all(1 <= e - lo <= 3 or 1 <= hi - e <= 3 for e in ends) and lo < min(ends) < max(ends) < hi, p
            assert hi - lo <= 18, p                                # the numbers fit under the line
        answers.add(p["answer"])
    if k == "3":                                                  # one piece and two rays, both
        assert any('"or"' in a for a in answers) and any('"or"' not in a for a in answers)
seen = set()
drawn = [B.generate("4", rng, seen)["prompt"].split(" = ")[1] for _ in range(15)]
assert len(set(drawn)) == 15, drawn                               # y = |x| and f(x) = |x| are one problem

# ---- showing: the deck's words, the figures drawn from the data
p = dict(type="1", prompt=prompt_of["ex 22.2"], answer="3 < x < 7", line=[1, 9])
t, key = B.typst(p), B.key_typst(p)
assert t.startswith("${x in RR | abs(x - 5) < 2}$") and "cetz.canvas" in t and "circle(" not in t   # a blank line
assert key.count("circle(") == 2 and key.count("fill: white") == 2, key        # two open circles
assert t.count("content(") == key.count("content(") == 9                        # the integers 1 to 9
assert B.answer_typst(p) == "$3 < x < 7$" and B.slide_typst(p) is None
assert B.text(p) == "{x ∈ ℝ | |x − 5| < 2}" and B.answer_text(p) == "3 < x < 7", (B.text(p), B.answer_text(p))
p = dict(type="2", prompt=prompt_of["ex 22.3"], answer='x <= -5 "or" x >= 1', line=[-7, 3])
key = B.key_typst(p)
assert key.count("circle(") == 2 and "fill: white" not in key and key.count('mark: (end: ">"') == 2   # solid; two rays
assert B.answer_text(p) == "x ≤ −5 or x ≥ 1", B.answer_text(p)
p = dict(type="3", prompt=prompt_of["ex 22.1"], answer="-2 < x < 2")
assert B.typst(p).startswith("$abs(x) - 2 < 0$") and "cetz.canvas" in B.typst(p)   # no line given: one is made
p = dict(type="4", prompt=prompt_of["PS 7"], answer="(-2, 2), (0, 0), (2, 2)")
assert "$f(x) = abs(x)$" in B.typst(p) and "circle(" not in B.typst(p)       # blank axes to sketch on
assert B.key_typst(p).count("circle(") == 3                                  # the key: the deck's three points
q, a = B.slide_typst(p), B.slide_typst(p, key=True)
assert "#hide[" in q and "#text(fill: red)" in a
assert B.text(p) == "f(x) = |x|", B.text(p)
p = dict(type="5", prompt=prompt_of["ex 22.5"], answer="x = 0; " + TABLE)
assert "dash" not in B.typst(p) and "dash" in B.key_typst(p) and B.key_typst(p).count("circle(") == 6
assert "Asymptote: $x = 0$" in B.answer_typst(p) and "[$0.25$]" in B.answer_typst(p)
p = dict(type="6", prompt=prompt_of["PS 8"], answer="x = -3; (-2, 1), (-4, -1)")
t, key = B.typst(p), B.key_typst(p)
assert "dash" in t and t.count("circle(") == 2 and "$(-2, 1)$" in t and "$(-4, -1)$" in t   # the book's figure
assert "$(-2, 1)$" not in key and key.count("circle(") == 2 and key.count("line(") > t.count("line(")   # g drawn
assert B.answer_typst(p) == "Asymptote: $x = -3$ \\\nThrough $(-2, 1)$ and $(-4, -1)$", B.answer_typst(p)
assert B.text(p) == "f(x) = x + 3; g(x) = 1/(x + 3)   [graph of f]", B.text(p)

# ---- editing: a new prompt is solved again; a typed answer is checked
old = lambda typ: dict(type=typ, prompt="", answer="", source="template")
p, status = B.from_edit("|x − 7| ≤ 3", dict(old("1"), line=[-3, 3]))
assert status == "checked" and p["answer"] == "4 <= x <= 10" and p["line"] == [2, 12], p
p, status = B.with_answer(p, "4 ≤ x ≤ 10")
assert status == "checked", p
p, status = B.from_edit("abs(x + 4)>1", old("2"))
assert status == "checked" and p["answer"] == 'x < -5 "or" x > -3', p
p, status = B.with_answer(p, "x < -5 or x > -3")
assert status == "checked" and p["answer"] == 'x < -5 "or" x > -3', p
p, status = B.with_answer(p, "x < -5 or x >= -3")
assert status == "failed", p
p, status = B.from_edit("abs(x - 1) + 3 > 7", old("3"))
assert status == "checked" and p["answer"] == 'x < -3 "or" x > 5', p
p, status = B.from_edit("g(x) = abs(x + 1) - 2", old("4"))
assert status == "checked" and p["answer"] == "(-3, 0), (-1, -2), (1, 0)", p
p, status = B.from_edit("y = 1/(x + 4)^2", old("5"))
assert status == "checked" and p["answer"].startswith("x = -4; (-6, 0.25), (-5, 1), (-4.5, 4)"), p
p, status = B.from_edit("f(x) = 2 - x; g(x) = 1/(2 - x)", old("6"))
assert status == "checked" and p["answer"] == "x = 2; (1, 1), (3, -1)", p
for typ, bad in (("1", "abs(x - 5) > 2"), ("1", "abs(x - 5) < 0"), ("2", "abs(x - 5 >= 2"), ("3", "abs(x) < 2"),
                 ("4", "y = x^2"), ("4", "y = abs(x^2 - 1)"), ("5", "y = 1/x"), ("5", "y = 1/(x^2 - 1)"),
                 ("6", "f(x) = x + 3; g(x) = 1/(x - 3)"), ("6", "f(x) = 2 x + 4; g(x) = 1/(2 x + 4)")):
    try:
        B.from_edit(bad, old(typ)); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_22: ok")
