"""Lesson 21 (Advanced Math): evaluating functions, domain and range, types of
functions, tests for functions. Every source problem is reachable from
in-range parameters and checks with the deck's answer; wrong answers fail;
every type draws, checks, and keeps its shape; the figures show; edits solve
again.

    python3 tests/test_adv_lesson_21.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_21 as B

lib = library.current()
assert "adv_lesson_21" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 21: Evaluating Functions, Domain and Range, Types of Functions, Tests for Functions"
assert B.type_instructions("3").startswith("Draw the necessary reference triangle")
assert B.type_instructions("4") == B.type_instructions("5") == "Find the domain of each function."
assert B.type_instructions("9") == "Which of the following sets of ordered pairs are functions?"

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 21.1", "1", "f(x) = x^2 + x - 10; f(5)", "f(5) = 20"),
    ("PS 10", "1", "f(x) = x^2 - x + 3; f(4)", "f(4) = 15"),
    ("ex 21.2", "2", "f(x) = x^2 + 1; f(x + 2)", "f(x + 2) = x^2 + 4 x + 5"),
    ("ex 21.3", "3", "h(theta) = sin(theta); 4 sqrt(3) h(30 degree)", "4 sqrt(3) h(30 degree) = 2 sqrt(3)"),
    ("PS 11", "3", "g(theta) = 4 sqrt(3) cos(theta); g(60 degree)", "g(60 degree) = 2 sqrt(3)"),
    ("PS 12", "3", "h(theta) = 8 tan(theta); h(45 degree)", "h(45 degree) = 8"),
    ("ex 21.4", "4", "f(x) = sqrt(10 - x); domain", "{x in RR | x <= 10}"),
    ("PS 9b", "4", "g(x) = sqrt(x + 5); domain", "{x in RR | x >= -5}"),
    ("PS 9c", "4", "h(x) = sqrt(6 - x); domain", "{x in RR | x <= 6}"),
    ("ex 21.5", "5", "g(x) = 1/(x - 2); domain", "{x in RR | x != 2}"),
    ("PS 9a", "5", "f(x) = x^2 - 3; domain", "{x in RR}"),
    ("ex 21.6", "6", "y = sqrt(x)", "{x in RR | x >= 0}; {y in RR | y >= 0}"),
    ("ex 21.7", "6", "y = sqrt(x + 4)", "{x in RR | x >= -4}; {y in RR | y >= 0}"),
    ("ex 21.8", "7", "f(x) = sqrt(x)/(x - 2)", "{x in RR | x >= 0, x != 2}; {y in RR}"),
    ("ex 21.9a", "8", "domain 4, 3; range 3; 4 -> 3, 3 -> 3", "function"),
    ("ex 21.9b", "8", "domain 7, 5; range 3, 4; 7 -> 3, 5 -> 3, 5 -> 4", "not a function: 5 has two images"),
    ("ex 21.9c", "8", "domain 4, 6, m; range 5, 7; 4 -> 5, 6 -> 7", "not a function: m has no image"),
    ("ex 21.9d", "8", "x in RR -> x + 2", "function"),
    ("PS 8a", "8", "domain a, b, c; range 2, 4, 6; a -> 2, a -> 4, b -> 4, c -> 6", "not a function: a has two images"),
    ("PS 8b", "8", "domain x, y, z; range 1, 3; x -> 1, y -> 1, z -> 3", "function"),
    ("ex 21.10", "9", "{(1, 2), (2, 3), (3, 4), (4, 5)}; {(1, 2), (2, 3), (1, 3), (4, 5)}; "
                      "{(4, 3), (2, 2), (4, 3), (3, 3)}; {(1, -1), (4, -1), (-1, -1), (3, -2)}", "a, c, d"),
    ("PS 7", "9", "{(4, 6), (5, 7), (3, -2), (1, 3)}; {(2, 3), (6, 1), (2, -3)}; "
                  "{(1, -1), (4, -1), (-1, -1), (3, -2), (1, 2)}; {(1, 2), (2, 3), (4, 4), (7, -2)}", "a, d"),
    ("ex 21.11a", "10", "x = 3 y - y^3, y in (-oo, oo)", "not a function"),
    ("ex 21.11b", "10", "y = 2 - 2^(-x), x in (-oo, oo)", "function, one-to-one"),
    ("ex 21.11c", "10", "y = 1, x in (-oo, 1]; y = -1, x in (1, oo)", "function, not one-to-one"),
    ("ex 21.11d", "10", "y = -x, x in (-oo, -1]; y = -1, x in [-1, oo)", "not a function"),
]
TYPE_OF = {"ex 21.1": "1", "PS 10": "1", "ex 21.2": "2", "ex 21.3": "3", "PS 11": "3", "PS 12": "3",
           "ex 21.4": "4", "PS 9b": "4", "PS 9c": "4", "ex 21.5": "5", "PS 9a": "5", "ex 21.6": "6",
           "ex 21.7": "6", "ex 21.8": "7", "ex 21.9a": "8", "ex 21.9b": "8", "ex 21.9c": "8", "ex 21.9d": "8",
           "PS 8a": "8", "PS 8b": "8", "ex 21.10": "9", "PS 7": "9", "ex 21.11a": "10", "ex 21.11b": "10",
           "ex 21.11c": "10", "ex 21.11d": "10"}                    # every source in exactly one type
assert {s[0]: s[1] for s in SOURCES} == TYPE_OF and len(SOURCES) == len(TYPE_OF)
assert set(TYPE_OF.values()) == set(B.KEYS)                       # every type has a source
prompt_of = {sid: prompt for sid, _, prompt, _ in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt) == answer, (sid, B.answer_of(prompt), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 21.1": (B.t1_build, dict(name="f", a=1, b=1, c=-10, n=5)),
    "PS 10": (B.t1_build, dict(name="f", a=1, b=-1, c=3, n=4)),
    "ex 21.2": (B.t2_build, dict(name="f", a=1, b=0, c=1, k=2)),
    "ex 21.3": (B.t3_build, dict(name="h", k=4, m=3, func="sin", angle=30, inside=False)),
    "PS 11": (B.t3_build, dict(name="g", k=4, m=3, func="cos", angle=60, inside=True)),
    "PS 12": (B.t3_build, dict(name="h", k=8, m=1, func="tan", angle=45, inside=True)),
    "ex 21.4": (B.t4_build, dict(name="f", k=1, a=10, flip=True)),
    "PS 9b": (B.t4_build, dict(name="g", k=1, a=5, flip=False)),
    "PS 9c": (B.t4_build, dict(name="h", k=1, a=6, flip=True)),
    "ex 21.5": (B.t5_build, dict(name="g", n=1, a=2)),
    "PS 9a": (B.t5_poly_build, dict(name="f", a=1, b=0, c=-3)),
    "ex 21.6": (B.t6_build, dict(a=0, flip=False)),
    "ex 21.7": (B.t6_build, dict(a=4, flip=False)),
    "ex 21.8": (B.t7_build, dict(name="f", b=0, gap=2)),
    "ex 21.9a": (B.t8_build, dict(domain=["4", "3"], range_=["3"], arrows=[("4", "3"), ("3", "3")])),
    "ex 21.9b": (B.t8_build, dict(domain=["7", "5"], range_=["3", "4"], arrows=[("7", "3"), ("5", "3"), ("5", "4")])),
    "ex 21.9c": (B.t8_build, dict(domain=["4", "6", "m"], range_=["5", "7"], arrows=[("4", "5"), ("6", "7")])),
    "ex 21.9d": (B.t8_rule_build, dict(rule="x + 2")),
    "PS 8a": (B.t8_build, dict(domain=["a", "b", "c"], range_=["2", "4", "6"],
                               arrows=[("a", "2"), ("a", "4"), ("b", "4"), ("c", "6")])),
    "PS 8b": (B.t8_build, dict(domain=["x", "y", "z"], range_=["1", "3"], arrows=[("x", "1"), ("y", "1"), ("z", "3")])),
    "ex 21.10": (B.t9_build, dict(rels=[[(1, 2), (2, 3), (3, 4), (4, 5)], [(1, 2), (2, 3), (1, 3), (4, 5)],
                                        [(4, 3), (2, 2), (4, 3), (3, 3)], [(1, -1), (4, -1), (-1, -1), (3, -2)]])),
    "PS 7": (B.t9_build, dict(rels=[[(4, 6), (5, 7), (3, -2), (1, 3)], [(2, 3), (6, 1), (2, -3)],
                                    [(1, -1), (4, -1), (-1, -1), (3, -2), (1, 2)], [(1, 2), (2, 3), (4, 4), (7, -2)]])),
    "ex 21.11a": (B.t10_curve_build, dict(expr="3 y - y^3", sideways=True)),
    "ex 21.11b": (B.t10_curve_build, dict(expr="2 - 2^(-x)", sideways=False)),
    "ex 21.11c": (B.t10_jump_build, dict(c=1, m1=0, y1=1, m2=0, y2=-1, dots=("]", "("))),
    "ex 21.11d": (B.t10_jump_build, dict(c=-1, m1=-1, y1=1, m2=0, y2=-1, dots=("]", "["))),
}
assert set(REACH) == {s[0] for s in SOURCES}                     # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid                         # every parameter inside its named range
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert not B.in_range(B.t4_build, dict(name="f", k=3, a=10, flip=True))         # 10/3: not a whole bound
assert not B.in_range(B.t8_build, dict(domain=["4", "3"], range_=["3", "5"], arrows=[("4", "3"), ("3", "3")]))  # 5 unused

# ---- wrong or unfinished answers fail
WRONG = [
    ("1", "f(x) = x^2 + x - 10; f(5)", "f(5) = 30"),
    ("1", "f(x) = x^2 + x - 10; f(5)", "20"),                                       # doesn't name what it finds
    ("2", "f(x) = x^2 + 1; f(x + 2)", "f(x + 2) = (x + 2)^2 + 1"),                  # not multiplied out
    ("2", "f(x) = x^2 + 1; f(x + 2)", "f(x + 2) = x^2 + 5"),                        # (x + 2)^2 as x^2 + 4
    ("3", "h(theta) = sin(theta); 4 sqrt(3) h(30 degree)", "4 sqrt(3) h(30 degree) = 6"),   # cos for sin
    ("3", "g(theta) = 4 sqrt(3) cos(theta); g(60 degree)", "g(60 degree) = (4 sqrt(3))/2"),  # not reduced
    ("3", "g(theta) = 4 sqrt(3) cos(theta); g(60 degree)", "g(60 degree) = sqrt(12)"),       # not simplified
    ("4", "f(x) = sqrt(10 - x); domain", "{x in RR | x >= 10}"),                    # the flip missed
    ("4", "f(x) = sqrt(10 - x); domain", "{x in RR | x < 10}"),                     # 10 itself is in
    ("4", "g(x) = sqrt(x + 5); domain", "{x in RR | x >= 5}"),                      # the sign
    ("5", "g(x) = 1/(x - 2); domain", "{x in RR | x != -2}"),
    ("5", "g(x) = 1/(x - 2); domain", "{x in RR}"),
    ("5", "f(x) = 1/((x - 2)(x + 3)); domain", "{x in RR | x != 2}"),               # one zero left out
    ("5", "f(x) = x^2 - 3; domain", "{x in RR | x >= -3}"),                         # the range, not the domain
    ("4", "g(x) = 1/(x - 2); domain", "{x in RR | x != 2}"),                        # a Type 5 prompt under Type 4
    ("6", "y = sqrt(x + 4)", "{x in RR | x >= -4}; {y in RR}"),
    ("6", "y = sqrt(x + 4)", "{x in RR | x >= -4}; {y in RR | y >= 2}"),
    ("6", "y = sqrt(x + 4)", "{x in RR | x >= 4}; {y in RR | y >= 0}"),
    ("7", "f(x) = sqrt(x)/(x - 2)", "{x in RR | x >= 0}; {y in RR}"),               # 2 not left out
    ("7", "f(x) = sqrt(x)/(x - 2)", "{x in RR | x >= 0, x != 2}; {y in RR | y >= 0}"),
    ("8", "domain 7, 5; range 3, 4; 7 -> 3, 5 -> 3, 5 -> 4", "function"),
    ("8", "domain 7, 5; range 3, 4; 7 -> 3, 5 -> 3, 5 -> 4", "not a function: 7 has two images"),
    ("8", "domain 4, 3; range 3; 4 -> 3, 3 -> 3", "not a function: 3 has two images"),   # sharing an image is fine
    ("8", "domain 4, 6, m; range 5, 7; 4 -> 5, 6 -> 7", "function"),
    ("9", prompt_of["ex 21.10"], "a, d"),                                           # the repeated pair (4, 3)
    ("9", prompt_of["PS 7"], "a, c, d"),
    ("10", prompt_of["ex 21.11a"], "function, not one-to-one"),
    ("10", prompt_of["ex 21.11b"], "function, not one-to-one"),
    ("10", prompt_of["ex 21.11c"], "not a function"),                               # the open point
    ("10", prompt_of["ex 21.11d"], "function, not one-to-one"),                     # both points solid
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^[fgh]\(x\) = [^;]+; [fgh]\(-?\d+\)$",
    "2": r"^[fgh]\(x\) = [^;]+; [fgh]\(x [+-] \d\)$",
    "3": r"^[fgh]\(theta\) = [^;]*(sin|cos|tan)\(theta\); [^;]*[fgh]\((30|45|60) degree\)$",
    "4": r"^[fgh]\(x\) = sqrt\([^)]*x[^)]*\); domain$",
    "5": r"^[fgh]\(x\) = [^;s]+; domain$",
    "6": r"^y = sqrt\([^)]*\)$",
    "7": r"^[fgh]\(x\) = sqrt\([^)]*\)/(x|\(x [+-] \d\))$",
    "8": r"^(domain [^;]+; range [^;]+; .+|x in RR -> .+)$",
    "9": r"^\{[^}]+\}(; \{[^}]+\}){3}$",
    "10": r"^(x = [^,]+, y in \(-oo, oo\)|y = [^,]+, x in \(-oo, oo\)|y = [^,]+, x in \(-oo, -?\d[\])]; y = [^,]+, x in [\[(]-?\d, oo\))$",
}
ANSWER = {
    "1": r"^[fgh]\(-?\d+\) = -?\d+$", "2": r"^[fgh]\(x [+-] \d\) = [^()]+$",
    "3": r"^.+ = [^=]+$", "4": r"^\{x in RR \| x (<=|>=) -?\d+\}$", "5": r"^\{x in RR( \| x != -?\d+(, x != -?\d+)?)?\}$",
    "6": r"^\{x in RR \| x (<=|>=) -?\d+\}; \{y in RR \| y >= 0\}$", "7": r"^\{x in RR \| x >= -?\d+, x != -?\d+\}; \{y in RR\}$",
    "8": r"^(function|not a function: \w has (no|two) images?)$", "9": r"^[a-d](, [a-d])*$",
    "10": r"^(not a function|function, (not )?one-to-one)$",
}
rng = random.Random(21)
for k in B.KEYS:
    seen, answers = set(), set()
    for i in range(80):
        if i % 10 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert re.match(SHAPE[k], p["prompt"]), p
        assert re.match(ANSWER[k], p["answer"]), p
        assert not re.search(r"\b1 (x|sqrt)|\+ -|- -|\+ 0\b", p["prompt"]), p
        answers.add(p["answer"] if k in ("8", "10") else p["answer"].split(":")[0])
        if k == "9":
            assert p["answer"] != "a, b, c, d", p                 # at least one isn't a function
    if k in ("8", "10"):
        assert len(answers) >= 3, (k, answers)                    # the answers aren't all one verdict

# ---- showing: the deck's words, the figures drawn from the data
p = dict(type="1", prompt=prompt_of["ex 21.1"], answer="f(5) = 20")
assert B.typst(p) == "If $f(x) = x^2 + x - 10$, find $f(5)$.", B.typst(p)
assert B.text(p) == "If f(x) = x^2 + x − 10, find f(5).", B.text(p)
p = dict(type="3", prompt=prompt_of["PS 11"], answer="g(60 degree) = 2 sqrt(3)")
assert B.typst(p) == "If $g(theta) = 4 sqrt(3) cos theta$, find $g(60 degree)$.", B.typst(p)
assert B.text(p) == "If g(θ) = 4 sqrt(3) cos θ, find g(60°).", B.text(p)
p = dict(type="4", prompt=prompt_of["ex 21.4"], answer="{x in RR | x <= 10}")
assert B.answer_typst(p) == "${x in RR | x <= 10}$" and B.answer_text(p) == "{x ∈ ℝ | x ≤ 10}"
p = dict(type="6", prompt=prompt_of["ex 21.7"], answer="{x in RR | x >= -4}; {y in RR | y >= 0}")
assert "cetz.canvas" in B.typst(p) and "circle(" not in B.typst(p)          # blank axes to graph on
assert B.key_typst(p).count("circle(") == 4                                  # the key: the end and 3 points
q, a = B.slide_typst(p), B.slide_typst(p, key=True)
assert "#hide[" in q and "#text(fill: red)" in a
p = dict(type="7", prompt=prompt_of["ex 21.8"], answer="{x in RR | x >= 0, x != 2}; {y in RR}")
assert "cetz" not in B.typst(p) and "dash" in B.key_typst(p)                # the key draws the asymptote
p = dict(type="8", prompt=prompt_of["ex 21.9b"], answer="not a function: 5 has two images")
assert "cetz.canvas" in B.typst(p) and "[$5$]" in B.typst(p) and "Domain" in B.typst(p)
assert B.answer_typst(p) == "*Not a function*: $5$ has two images", B.answer_typst(p)
q, a = B.slide_typst(p), B.slide_typst(p, key=True)
assert q.replace("#hide[", "#X[") .split("#X[")[0] == a.split("#text(fill: red)[")[0]   # the figure never moves
assert "y = x + 2" in B.typst(dict(type="8", prompt=prompt_of["ex 21.9d"], answer="function"))
p = dict(type="9", prompt=prompt_of["ex 21.10"], answer="a, c, d")
assert B.typst(p).startswith("#box[(a) #h(0.2em) ${(1, 2), (2, 3), (3, 4), (4, 5)}$]"), B.typst(p)
assert B.answer_typst(p) == "*(a), (c), and (d)*" and B.slide_typst(p) is None
p = dict(type="10", prompt=prompt_of["ex 21.11c"], answer="function, not one-to-one")
t = B.typst(p)
assert "fill: white" in t and "fill: black" in t, t                          # an open point and a solid one
assert B.answer_typst(p) == "*Function, not one-to-one*"

# ---- editing: a new prompt is solved again; a typed answer is checked
old = lambda typ: dict(type=typ, prompt="", answer="", source="template")
p, status = B.from_edit("g(x) = x^2 - 2 x; g(-3)", old("1"))
assert status == "checked" and p["answer"] == "g(-3) = 15", p
p, status = B.from_edit("h(θ) = 6 sin(θ); h(60°)", old("3"))
assert status == "checked" and p["answer"] == "h(60 degree) = 3 sqrt(3)", p
p, status = B.from_edit("f(x) = sqrt(2 x - 7); domain", old("4"))
assert status == "checked" and p["answer"] == "{x in RR | x >= 7/2}", p
p, status = B.with_answer(p, "{x ∈ ℝ | x ≥ 7/2}")
assert status == "checked", p
p, status = B.from_edit("f(x) = (x + 1)/(x^2 - 9); domain", old("5"))
assert status == "checked" and p["answer"] == "{x in RR | x != -3, x != 3}", p
p, status = B.from_edit("y = sqrt(3 - x)", old("6"))
assert status == "checked" and p["answer"] == "{x in RR | x <= 3}; {y in RR | y >= 0}", p
p, status = B.from_edit("g(x) = sqrt(x + 1)/(x - 4)", old("7"))
assert status == "checked" and p["answer"] == "{x in RR | x >= -1, x != 4}; {y in RR}", p
p, status = B.from_edit("domain 1, 2, 3; range 5; 1 -> 5, 2 -> 5", old("8"))
assert status == "checked" and p["answer"] == "not a function: 3 has no image", p
p, status = B.from_edit("{(1, 2), (1, 2)}; {(3, 4), (3, 5)}", old("9"))
assert status == "checked" and p["answer"] == "a", p
p, status = B.with_answer(p, "(A)")
assert status == "checked" and p["answer"] == "a", p
p, status = B.from_edit("y = x^2, x in [0, oo)", old("10"))
assert status == "checked" and p["answer"] == "function, one-to-one", p
p, status = B.with_answer(p, "function, not one-to-one")
assert status != "checked", p
for typ, bad in (("1", "f(x) = x^2 +; f(2)"), ("3", "g(theta) = cos(theta); h(60 degree)"),
                 ("4", "f(x) = sqrt(x^2 - 4); domain"), ("6", "y = x^2"),
                 ("7", "f(x) = sqrt(x)/(x + 2)"), ("8", "domain 1, 2; range 3; 1 -> 4"),
                 ("9", "{(1, 2)"), ("10", "x = y^3, y in (-oo, oo)"), ("1", "f(x) = sqrt(10 - x); domain")):
    try:
        B.from_edit(bad, old(typ)); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_21: ok")
