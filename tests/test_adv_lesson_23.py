"""Lesson 23 (Advanced Math): the exponential function, sketching
exponentials. Every source problem is reachable from in-range parameters and
checks with the deck's answer; wrong answers fail; every type draws, checks,
and keeps its shape; the figures are drawn from the data; edits solve again.

    python3 tests/test_adv_lesson_23.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_23 as B

lib = library.current()
assert "adv_lesson_23" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 23: The Exponential Function, Sketching Exponentials"
assert B.type_instructions("1") == B.type_instructions("2") == "Sketch the graph of each function."

# ---- every source: the deck's answer, and checked
TWO = "(0, 1), (1, 2), (2, 4), (3, 8)"
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 23.1", "1", "y = 2^x", TWO),                       # the deck's table is -3, -2, 0, 2, 3; see the docstring
    ("ex 23.2", "1", "f(x) = 5^x", "(0, 1), (1, 5)"),
    ("ex 23.3", "2", "y = 0.25^x", "(-1, 4), (0, 1)"),
    ("PS 7", "1", "f(x) = 2^x", TWO),
    ("PS 8", "2", "g(x) = (1/2)^x", "(-3, 8), (-2, 4), (-1, 2), (0, 1)"),
]
TYPE_OF = {"ex 23.1": "1", "ex 23.2": "1", "ex 23.3": "2", "PS 7": "1", "PS 8": "2"}   # every source in one type
assert {s[0]: s[1] for s in SOURCES} == TYPE_OF and len(SOURCES) == len(TYPE_OF)
assert set(TYPE_OF.values()) == set(B.KEYS)                       # every type has a source
prompt_of = {sid: prompt for sid, _, prompt, _ in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 23.1": (B.t1_build, dict(name="y", b=2)),
    "ex 23.2": (B.t1_build, dict(name="f", b=5)),
    "ex 23.3": (B.t2_build, dict(name="y", k=4, decimal=True)),
    "PS 7": (B.t1_build, dict(name="f", b=2)),
    "PS 8": (B.t2_build, dict(name="g", k=2, decimal=False)),
}
assert set(REACH) == {s[0] for s in SOURCES}                     # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid                         # every parameter inside its named range
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert {2, 5} <= set(B.SMALL) and 4 in B.DECIMALS                 # the weighted picks hold the book's
assert not B.in_range(B.t1_build, dict(name="y", b=1))            # 1^x never changes
assert not B.in_range(B.t2_build, dict(name="y", k=3, decimal=True))   # 0.333...

# ---- wrong or unfinished answers fail
WRONG = [
    ("1", "y = 2^x", "(1, 2), (2, 4), (3, 8)"),                     # (0, 1) left out
    ("1", "y = 2^x", "(0, 1), (1, 2), (2, 4)"),                     # (3, 8) left out
    ("1", "y = 2^x", "(0, 1), (1, 2), (2, 4), (3, 8), (4, 16)"),    # off the graph
    ("1", "y = 2^x", "(0, 1), (2, 4), (3, 8)"),                     # a point skipped
    ("1", "y = 2^x", "(-3, 8), (-2, 4), (-1, 2), (0, 1)"),          # (1/2)^x's: the wrong way
    ("1", "y = 2^x", "(0, 0), (1, 2), (2, 4), (3, 8)"),             # 2^0 taken as 0
    ("1", "y = 2^x", "(3, 8), (2, 4), (1, 2), (0, 1)"),             # right to left
    ("1", "y = 2^x", "(0, 1), (1, 2), (2, 4), (3, 6)"),             # 2 times 3
    ("1", "f(x) = 5^x", "(0, 1), (1, 5), (2, 25)"),                 # off the graph
    ("1", "f(x) = 5^x", "(0, 1)"),                                  # no point on the steep side
    ("1", "f(x) = 5^x", "(-1, 0), (0, 1), (1, 5)"),                 # the tail isn't 0
    ("2", "y = 0.25^x", "(0, 1), (1, 4)"),                          # 0.25 read as 4
    ("2", "y = 0.25^x", "(-2, 16), (-1, 4), (0, 1)"),               # off the graph
    ("2", "y = 0.25^x", "(-1, 0.25), (0, 1)"),                      # 0.25^1, not 0.25^-1
    ("2", "g(x) = (1/2)^x", "(-2, 4), (-1, 2), (0, 1)"),            # (-3, 8) left out
    ("2", "g(x) = (1/2)^x", "(-3, -8), (-2, -4), (-1, -2), (0, 1)"),   # the sign of y
    ("2", "y = 2^x", TWO),                                          # a Type 1 prompt under Type 2
    ("1", "g(x) = (1/2)^x", "(-3, 8), (-2, 4), (-1, 2), (0, 1)"),   # a Type 2 prompt under Type 1
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^(y|[fgh]\(x\)) = ([2-9]|10)\^x$",
    "2": r"^(y|[fgh]\(x\)) = (0\.(5|25|2|1)|\(1/([2-9]|10)\))\^x$",
}
POINT = r"\(-?\d+, \d+\)"
ANSWER = {
    "1": rf"^\(0, 1\)(, \([1-3], \d+\))+$",
    "2": rf"^(\(-[1-3], \d+\), )+\(0, 1\)$",
}
rng = random.Random(23)
for k in B.KEYS:
    seen, prompts = set(), set()
    for i in range(90):
        if i % 9 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.match(SHAPE[k], p["prompt"]), p
        assert re.match(ANSWER[k], p["answer"]), p
        assert all(int(y) <= B.CAP for y in re.findall(r", (\d+)\)", p["answer"])), p
        prompts.add(p["prompt"].split(" = ")[1])
    if k == "2":                                                  # decimals and fractions, both
        assert any("." in q for q in prompts) and any("/" in q for q in prompts), prompts
seen = set()
drawn = {B.base_of(B.generate("2", rng, seen)["prompt"]) for _ in range(9)}
assert len(drawn) == 9, drawn                                     # 0.5^x and (1/2)^x are one problem
seen = set()
assert len({B.generate("1", rng, seen)["prompt"].split(" = ")[1] for _ in range(9)}) == 9   # the whole type

# ---- showing: the figures drawn from the data, the same axes on sheet and key
p = dict(type="2", prompt=prompt_of["PS 8"], answer="(-3, 8), (-2, 4), (-1, 2), (0, 1)")
t, key = B.typst(p), B.key_typst(p)
assert "$g(x) = (display(1/2))^x$" in t and "cetz.canvas" in t and "circle(" not in t   # blank axes
assert key.count("circle(") == 4 and "1f5fbf" in key                          # the curve and its four points
assert t.split("import cetz.draw: *")[1].count("content(") == key.split("import cetz.draw: *")[1].count("content(")
assert "$g(x)$" in t                                                          # the axis named as the book does
assert B.typst(dict(type="1", prompt=prompt_of["ex 23.2"], answer="")).split("cetz.canvas")[1] == \
       B.typst(dict(type="1", prompt="h(x) = 3^x", answer="")).split("cetz.canvas")[1].replace("$h(x)$", "$f(x)$")
q, a = B.slide_typst(p), B.slide_typst(p, key=True)
assert "#hide[" in q and "#text(fill: red)" in a
assert B.answer_typst(p) == "$(-3, 8), (-2, 4), (-1, 2), (0, 1)$"
assert B.text(p) == "g(x) = (1/2)^x" and B.answer_text(p) == "(−3, 8), (−2, 4), (−1, 2), (0, 1)", B.answer_text(p)

# ---- editing: a new prompt is solved again; a typed answer is checked
old = lambda typ: dict(type=typ, prompt="", answer="", source="template")
p, status = B.from_edit("h(x) = 3 ^ x", old("1"))
assert status == "checked" and p["answer"] == "(0, 1), (1, 3), (2, 9)", p
p, status = B.with_answer(p, "(0, 1), (1, 3), (2, 9)")
assert status == "checked", p
p, status = B.with_answer(p, "(0, 1), (1, 3)")
assert status == "failed", p
p, status = B.from_edit("0.1^x", old("2"))
assert status == "checked" and p["prompt"] == "y = 0.1^x" and p["answer"] == "(-1, 10), (0, 1)", p
p, status = B.from_edit("f(x) = (1/4)^x", old("2"))
assert status == "checked" and p["answer"] == "(-1, 4), (0, 1)", p
for typ, bad in (("1", "y = (1/2)^x"), ("2", "y = 2^x"), ("1", "y = 1^x"), ("1", "y = x^2"), ("1", "y = (3/2)^x"),
                 ("2", "y = 0.4^x"), ("1", "y = 2^(x + 1)"), ("1", "y = (-2)^x"), ("1", "y = 2^x +")):
    try:
        B.from_edit(bad, old(typ)); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_23: ok")
