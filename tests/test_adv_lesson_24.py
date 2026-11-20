"""Lesson 24 (Advanced Math): sums of trigonometric functions, combining
functions. Every source is reachable from in-range parameters and checks with
the deck's answer; wrong and unfinished answers fail; every type draws and
keeps its shape; edits solve again.

    python3 tests/test_adv_lesson_24.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_24 as B

lib = library.current()
assert "adv_lesson_24" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 24: Sums of Trigonometric Functions, Combining Functions"
assert B.type_instructions("1").startswith("Draw the necessary reference triangles")
assert B.type_instructions("5") == "Solve each problem."
C = "circle.small"

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer, the key's answer when it differs)
    ("ex 24.1", "1", "cos(60 degree) + sin(45 degree)", "(sqrt(2) + 1)/2", "(1 + sqrt(2))/2"),
    ("ex 24.2", "1", "tan(30 degree) + cos(45 degree)", "(2 sqrt(3) + 3 sqrt(2))/6", None),
    ("ex 24.3", "1", "tan(45 degree) + 2 tan(30 degree)", "(3 + 2 sqrt(3))/3", None),
    ("ex 24.4", "2", "sqrt(6) sin(30 degree) + 1/sqrt(2) tan(60 degree)", "sqrt(6)", None),
    ("PS 13", "2", "sqrt(3)/2 tan(30 degree) + sqrt(2) cos(60 degree)", "(1 + sqrt(2))/2", None),
    ("PS 15", "3", "f(theta) = tan(theta); f(45 degree) + 2 f(30 degree)",
     "f(45 degree) + 2 f(30 degree) = (3 + 2 sqrt(3))/3", None),
    ("ex 24.5", "4", f"f(x) = log(x); g(x) = x^2 + 6; (g {C} f)(x)", f"(g {C} f)(x) = (log(x))^2 + 6", None),
    ("ex 24.6a", "5", "f(x) = x + 2; g(x) = x^2 + 3; (f + g)(6)", "(f + g)(6) = 47", None),
    ("ex 24.6b", "5", "f(x) = x + 2; g(x) = x^2 + 3; (f - g)(6)", "(f - g)(6) = -31", None),
    ("ex 24.6c", "5", "f(x) = x + 2; g(x) = x^2 + 3; (f g)(6)", "(f g)(6) = 312", None),
    ("ex 24.6d", "5", "f(x) = x + 2; g(x) = x^2 + 3; (f/g)(6)", "(f/g)(6) = 8/39", None),
    ("PS 14a", "5", "f(x) = x + 3; g(x) = x^2 + 1; (f + g)(3)", "(f + g)(3) = 16", None),
    ("PS 14b", "5", "f(x) = x + 3; g(x) = x^2 + 1; (f - g)(3)", "(f - g)(3) = -4", None),
    ("PS 14c", "6", f"f(x) = x + 3; g(x) = x^2 + 1; (f {C} g)(3)", f"(f {C} g)(3) = 13", None),
]
prompt_of = {s[0]: s[2] for s in SOURCES}
for sid, typ, prompt, deck, key in SOURCES:
    assert B.answer_of(prompt, typ) == (key or deck), (sid, B.answer_of(prompt, typ))
    assert B.check(dict(type=typ, prompt=prompt, answer=deck)) == "checked", sid
    assert B.check(dict(type=typ, prompt=prompt, answer=key or deck)) == "checked", sid

TYPE_OF = {s[0]: s[1] for s in SOURCES}
assert len(TYPE_OF) == len(SOURCES) == 14
assert set(TYPE_OF.values()) == set(B.KEYS)

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 24.1": (B.t1, dict(k1=1, f1="cos", a1=60, s="+", k2=1, f2="sin", a2=45)),
    "ex 24.2": (B.t1, dict(k1=1, f1="tan", a1=30, s="+", k2=1, f2="cos", a2=45)),
    "ex 24.3": (B.t1, dict(k1=1, f1="tan", a1=45, s="+", k2=2, f2="tan", a2=30)),
    "ex 24.4": (B.t2, dict(c1="sqrt(6)", f1="sin", a1=30, s="+", c2="1/sqrt(2)", f2="tan", a2=60)),
    "PS 13": (B.t2, dict(c1="sqrt(3)/2", f1="tan", a1=30, s="+", c2="sqrt(2)", f2="cos", a2=60)),
    "PS 15": (B.t3, dict(name="f", func="tan", k1=1, a1=45, s="+", k2=2, a2=30)),
    "ex 24.5": (B.t4, dict(f="log(x)", g="x^2 + 6", outer="g")),
    "ex 24.6a": (B.t5, dict(f="x + 2", g="x^2 + 3", op="+", n=6)),
    "ex 24.6b": (B.t5, dict(f="x + 2", g="x^2 + 3", op="-", n=6)),
    "ex 24.6c": (B.t5, dict(f="x + 2", g="x^2 + 3", op=" ", n=6)),
    "ex 24.6d": (B.t5, dict(f="x + 2", g="x^2 + 3", op="/", n=6)),
    "PS 14a": (B.t5, dict(f="x + 3", g="x^2 + 1", op="+", n=3)),
    "PS 14b": (B.t5, dict(f="x + 3", g="x^2 + 1", op="-", n=3)),
    "PS 14c": (B.t6, dict(f="x + 3", g="x^2 + 1", outer="f", n=3)),
}
assert set(REACH) == set(prompt_of)
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid
assert not B.in_range(B.t1, dict(k1=1, f1="cos", a1=60, s="+", k2=1, f2="sin", a2=30))   # 1/2 + 1/2: no radical
assert not B.in_range(B.t5, dict(f="x + 2", g="x^2 + 3", op="+", n=8))

# ---- wrong or unfinished answers fail
WRONG = [
    ("1", "cos(60 degree) + sin(45 degree)", "1/2 + 1/sqrt(2)"),                     # not one fraction, not rationalized
    ("1", "cos(60 degree) + sin(45 degree)", "(2 + sqrt(2))/(2 sqrt(2))"),           # a radical below
    ("1", "cos(60 degree) + sin(45 degree)", "(2 sqrt(2) + 2)/4"),                   # not reduced
    ("1", "tan(30 degree) + cos(45 degree)", "(sqrt(2) + sqrt(3))/sqrt(6)"),
    ("1", "tan(45 degree) + 2 tan(30 degree)", "(3 + sqrt(3))/3"),
    ("1", "tan(45 degree) + 2 tan(30 degree)", "1 + 2 tan(30 degree)"),              # not evaluated
    ("2", "sqrt(6) sin(30 degree) + 1/sqrt(2) tan(60 degree)", "(2 sqrt(3))/sqrt(2)"),
    ("2", "sqrt(6) sin(30 degree) + 1/sqrt(2) tan(60 degree)", "(sqrt(6) + sqrt(6))/2"),   # like terms not added
    ("2", "sqrt(6) sin(30 degree) + 1/sqrt(2) tan(60 degree)", "sqrt(24)/2"),
    ("3", "f(theta) = tan(theta); f(45 degree) + 2 f(30 degree)", "(3 + 2 sqrt(3))/3"),   # not named
    ("3", "f(theta) = tan(theta); f(45 degree) + 2 f(30 degree)", "f(45 degree) + 2 f(30 degree) = (3 + sqrt(3))/3"),
    ("4", f"f(x) = log(x); g(x) = x^2 + 6; (g {C} f)(x)", f"(g {C} f)(x) = log(x^2 + 6)"),   # the other way around
    ("4", f"f(x) = log(x); g(x) = x^2 + 6; (g {C} f)(x)", f"(f {C} g)(x) = (log(x))^2 + 6"),   # misnamed
    ("4", f"f(x) = x + 2; g(x) = x^2 + 3; (g {C} f)(x)", f"(g {C} f)(x) = (x + 2)^2 + 3"),     # not multiplied out
    ("4", f"f(x) = x + 2; g(x) = x^2 + 3; (g {C} f)(x)", f"(g {C} f)(x) = x^2 + 5"),
    ("5", "f(x) = x + 2; g(x) = x^2 + 3; (f - g)(6)", "(f - g)(6) = 31"),
    ("5", "f(x) = x + 2; g(x) = x^2 + 3; (f/g)(6)", "(f/g)(6) = 16/78"),             # not lowest terms
    ("5", "f(x) = x + 2; g(x) = x^2 + 3; (f/g)(6)", "(f/g)(6) = 39/8"),
    ("5", "f(x) = x + 2; g(x) = x^2 + 3; (f g)(6)", "312"),
    ("6", f"f(x) = x + 3; g(x) = x^2 + 1; (f {C} g)(3)", f"(f {C} g)(3) = 37"),        # g(f(3))
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (typ, prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
TRIG = r"(sin|cos|tan)\((30|45|60) degree\)"
SHAPE = {
    "1": rf"^(\d )?{TRIG} [+-] (\d )?{TRIG}$",
    "2": rf"^(\d )?\S*sqrt\(\d\)\S* {TRIG} [+-] (\d )?\S*sqrt\(\d\)\S* {TRIG}$",
    "3": r"^[fgh]\(theta\) = (sin|cos|tan)\(theta\); (\d )?[fgh]\(\d\d degree\) [+-] (\d )?[fgh]\(\d\d degree\)$",
    "4": rf"^f\(x\) = [^;]+; g\(x\) = [^;]+; \([fg] {re.escape(C)} [fg]\)\(x\)$",
    "5": r"^f\(x\) = [^;]+; g\(x\) = [^;]+; \(f( [+-] |/| )g\)\(-?\d\)$",
    "6": rf"^f\(x\) = [^;]+; g\(x\) = [^;]+; \([fg] {re.escape(C)} [fg]\)\(-?\d\)$",
}
rng = random.Random(24)
for k in B.KEYS:
    for rep in range(4):
        seen = set()
        for _ in range(20):
            p = B.generate(k, rng, seen)
            assert B.check(p) == "checked", p
            assert re.search(SHAPE[k], p["prompt"]), (k, p)
            value = p["answer"].split("=")[-1].strip()
            if k in "123":
                assert "sqrt" in value and "degree" not in value and value.count("/") <= 1, p
            if k in "56":
                assert re.fullmatch(r"-?\d+(/\d+)?", value), p
            if k in "3456":
                assert p["answer"].split(" = ")[0] == p["prompt"].split("; ")[-1], p
            assert not re.search(r"(?<![\d.])1 [a-z(]", p["prompt"] + " " + p["answer"]), p

# ---- showing
s = dict(type="2", prompt="sqrt(6) sin(30 degree) + 1/sqrt(2) tan(60 degree)", answer="sqrt(6)")
assert B.typst(s) == "Evaluate: #h(0.5em) $display(sqrt(6) sin 30 degree + display(1/sqrt(2)) tan 60 degree)$", B.typst(s)
assert B.text(s) == "Evaluate: √(6) sin 30° + 1/√(2) tan 60°", B.text(s)
s5 = dict(type="5", prompt="f(x) = x + 2; g(x) = x^2 + 3; (f/g)(6)", answer="(f/g)(6) = 8/39")
assert B.typst(s5) == "If $f(x) = x + 2$ and $g(x) = x^2 + 3$, find $(f\\/g)(6)$.", B.typst(s5)
assert B.answer_typst(s5) == "$display((f\\/g)(6) = display(8/39))$", B.answer_typst(s5)
s4 = dict(type="4", prompt=prompt_of["ex 24.5"], answer=f"(g {C} f)(x) = (log(x))^2 + 6")
assert B.text(s4) == "If f(x) = log x and g(x) = x^2 + 6, find (g ∘ f)(x).", B.text(s4)
assert B.answer_text(s4) == "(g ∘ f)(x) = (log x)^2 + 6", B.answer_text(s4)
s3 = dict(type="3", prompt=prompt_of["PS 15"], answer="")
assert B.typst(s3).startswith("If $f(theta) = tan theta$, evaluate $f(45 degree) + 2 f(30 degree)$"), B.typst(s3)

# ---- editing: a new prompt is solved again; a typed answer is checked; unreadable edits raise
old = dict(type="1", prompt="", answer="", source="template")
p, status = B.from_edit("sin 60° + cos 45°", old)
assert status == "checked" and p["prompt"] == "sin(60 degree) + cos(45 degree)" and p["answer"] == "(sqrt(3) + sqrt(2))/2", p
p, status = B.with_answer(p, "(sqrt(2) + sqrt(3))/2")
assert status == "checked"
p, status = B.with_answer(p, "sqrt(3)/2 + sqrt(2)/2")
assert status != "checked"
p, status = B.from_edit("f(x) = log x; g(x) = 3 x; (f ∘ g)(x)", dict(old, type="4"))
assert status == "checked" and p["answer"] == f"(f {C} g)(x) = log(3 x)", p
p, status = B.from_edit("f(x) = x - 1; g(x) = x^2 + 2; (f g)(4)", dict(old, type="5"))
assert status == "checked" and p["answer"] == "(f g)(4) = 54", p
p, status = B.from_edit("g(θ) = sin θ; 2 g(30°) + g(60°)", dict(old, type="3"))
assert status == "checked" and p["answer"] == "2 g(30 degree) + g(60 degree) = (2 + sqrt(3))/2", p
for typ, bad in (("1", "sin(30 degree"), ("5", "f(x) = x; (f + g)(2)"), ("3", "f(theta) = tan(theta); g(30 degree)"),
                 ("5", "f(x) = x + 1; g(x) = x - 2; (f/g)(2)")):
    try:
        B.from_edit(bad, dict(old, type=typ)); raise AssertionError(("unreadable", typ, bad))
    except ValueError:
        pass

print("adv_lesson_24: ok")
