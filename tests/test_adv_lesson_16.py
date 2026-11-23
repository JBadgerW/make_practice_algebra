"""Lesson 16 (Advanced Math): complex fractions, abstract equations, division of
polynomials. Every source is reachable and checks, its key the deck's answer (or the
same value in the deck's form, where the deck groups it otherwise); wrong answers fail;
every type draws, checks, and keeps its shape; edits solve again.

    python3 tests/test_adv_lesson_16.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.check import same_value
from sheets.banks import adv_lesson_16 as B

lib = library.current()
assert "adv_lesson_16" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 16: Complex Fractions, Abstract Equations, Division of Polynomials"
assert B.type_instructions("3") == "Solve for the indicated variable."

# ---- every source: the key, the deck's answer (the same value), and checked
SOURCES = [   # (id, problem, the key, the deck's answer as the deck writes it)
    ("ex 16.1", dict(type="1", prompt="x/(a + m/(b + c/d))"),
     "(x (b d + c))/(a b d + a c + d m)", "(x (b d + c))/(a (b d + c) + m d)"),
    ("ex 16.2", dict(type="2", prompt="(a/x^2 + b/x)/(m/x^2 + k/(x c))"),
     "(c (a + b x))/(c m + k x)", "(c (a + b x))/(m c + k x)"),
    ("ex 16.3", dict(type="3", prompt="y = v (a/x + b/(m c))", target="c"),
     "c = (b v x)/(m x y - a m v)", "c = (x v b)/(x m y - m v a)"),
    ("ex 16.4", dict(type="4", prompt="x^3 - 2", divisor="x - 1"),
     "x^2 + x + 1 - 1/(x - 1)", "x^2 + x + 1 - 1/(x - 1)"),
    ("PS 5", dict(type="2", prompt="(x/a^2 + b/a)/(1/a^2 - k/(a c))"),
     "(c (a b + x))/(c - a k)", "(x c + a b c)/(c - a k)"),
    ("PS 6", dict(type="1", prompt="p/(m + m/(1 + b/c))"),
     "(p (b + c))/(m (b + 2 c))", "(p (b + c))/(m (b + 2 c))"),
    ("PS 7", dict(type="1", prompt="a/(x + y/(p + m/c))"),
     "(a (c p + m))/(c p x + c y + m x)", "(a (p c + m))/(x p c + x m + y c)"),
    ("PS 8", dict(type="3", prompt="x = p m (1/y + a/(b d))", target="d"),
     "d = (a m p y)/(b x y - b m p)", "d = (p m a y)/(x y b - p m b)"),
    ("PS 9", dict(type="3", prompt="y = m (a/x + b/(m c))", target="c"),
     "c = (b x)/(x y - a m)", "c = (x b)/(x y - m a)"),
    ("PS 10", dict(type="4", prompt="x^3 - 1", divisor="x - 2"),
     "x^2 + 2 x + 4 + 7/(x - 2)", "x^2 + 2 x + 4 + 7/(x - 2)"),
]
for sid, p, key, deck in SOURCES:
    assert B.answer_of(p) == key, (sid, B.answer_of(p))
    assert B.check(dict(p, answer=key)) == "checked", sid
    assert B.check(dict(p, answer=deck)) == "checked", (sid, "the deck's own form")
    lhs = lambda a: a.split("=")[-1]
    assert same_value(lhs(key), lhs(deck)), sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 16.1": (B.t1_letters, dict(n="x", a="a", m="m", b="b", c="c", d="d")),
    "ex 16.2": (B.t2, dict(p1="a", p2="b", q1="m", q2="k", v="x", c="c", s1="+", s2="+")),
    "ex 16.3": (B.t3, dict(L="y", K="v", n="a", x="x", q="b", m="m", c="c", s="+")),
    "ex 16.4": (B.t4, dict(n=3, k=-2, a=1)),
    "PS 5": (B.t2, dict(p1="x", p2="b", q1="1", q2="k", v="a", c="c", s1="+", s2="-")),
    "PS 6": (B.t1_repeat, dict(n="p", a="m", k=1, b="b", c="c")),
    "PS 7": (B.t1_letters, dict(n="a", a="x", m="y", b="p", c="m", d="c")),
    "PS 8": (B.t3, dict(L="x", K="p m", n="1", x="y", q="a", m="b", c="d", s="+")),
    "PS 9": (B.t3, dict(L="y", K="m", n="a", x="x", q="b", m="m", c="c", s="+")),
    "PS 10": (B.t4, dict(n=3, k=-1, a=2)),
}
source = {s[0]: s[1] for s in SOURCES}
assert set(REACH) == set(source)
for sid, (build, params) in REACH.items():
    p = dict(type=source[sid]["type"], **B.problem(source[sid]["type"], build(**params)))
    assert p == source[sid], (sid, p)
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[p["type"]]), sid
assert {s[1]["type"] for s in SOURCES} == set(B.KEYS)
assert not B.in_range(B.t1_letters, dict(n="x", a="a", m="m", b="b", c="c", d="x"))   # a letter twice
assert not B.in_range(B.t2, dict(p1="1", p2="b", q1="1", q2="k", v="a", c="c", s1="+", s2="-"))   # two 1's
assert not B.in_range(B.t4, dict(n=3, k=-8, a=2))                                      # no remainder
assert not B.in_range(B.t4, dict(n=4, k=-2, a=4))                                      # remainder 254: too big

# ---- wrong answers fail
WRONG = [
    (dict(type="1", prompt="x/(a + m/(b + c/d))"), "(x (b d + c))/(a (b d + c) + m)"),      # m d lost
    (dict(type="1", prompt="x/(a + m/(b + c/d))"), "x/(a + (m d)/(b d + c))"),              # not finished
    (dict(type="2", prompt="(a/x^2 + b/x)/(m/x^2 + k/(x c))"), "(a + b x)/(m + k x)"),      # c dropped
    (dict(type="2", prompt="(a/x^2 + b/x)/(m/x^2 + k/(x c))"), "(c x (a + b x))/(x (c m + k x))"),   # not lowest terms
    (dict(type="3", prompt="y = v (a/x + b/(m c))", target="c"), "c = (b v x)/(m x y + a m v)"),     # a sign
    (dict(type="3", prompt="y = v (a/x + b/(m c))", target="c"), "c = (b v)/(m c y - a m v/x)"),     # c on both sides
    (dict(type="4", prompt="x^3 - 2", divisor="x - 1"), "x^2 + x + 1 + 1/(x - 1)"),               # the remainder's sign
    (dict(type="4", prompt="x^3 - 1", divisor="x - 2"), "x^2 + 2 x + 4"),                         # the remainder dropped
]
for p, answer in WRONG:
    got = B.check(dict(p, answer=answer))
    assert got != "checked", (p, answer, got)

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": re.compile(r"[a-z]/\([a-z] \+ [a-z]/\(([a-z]|\d) \+ [a-z]/[a-z]\)\)"),
    "2": re.compile(r"\(([a-z]|1)/[a-z]\^2 [+-] [a-z]/[a-z]\)/\(([a-z]|1)/[a-z]\^2 [+-] [a-z]/\([a-z] [a-z]\)\)"),
    "3": re.compile(r"[a-z] = [a-z]( [a-z])? \(([a-z]|1)/[a-z] [+-] [a-z]/\([a-z] [a-z]\)\)"),
    "4": re.compile(r"x\^[234] [+-] \d"),
}
rng = random.Random(16)
for k in B.KEYS:
    seen = set()
    for _ in range(60):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert SHAPE[k].fullmatch(p["prompt"]), (k, p)
        assert p["answer"] == B.answer_of(p), p
        if k in "12":
            assert "(-" not in p["answer"] and not p["answer"].startswith("-"), p    # a positive term first
        if k == "3":
            assert p["answer"].startswith(p["target"] + " = "), p
        if k == "4":
            assert re.fullmatch(r"x [+-] \d", p["divisor"]) and "/(" in p["answer"], p   # always a remainder

# ---- showing
q = dict(type="4", prompt="x^3 - 2", divisor="x - 1", answer="x^2 + x + 1 - 1/(x - 1)")
assert B.text(q) == ("Divide x^3 − 2 by x − 1 and check the result by adding the quotient and the remainder "
                     "fraction."), B.text(q)
assert B.text(dict(type="3", prompt="y = v (a/x + b/(m c))", target="c")).startswith("Solve for c:")
assert B.typst(dict(type="1", prompt="x/(a + m/(b + c/d))")).startswith("Simplify:")

# ---- editing: a new prompt is solved again; a typed answer is checked
p, status = B.from_edit("a/(b + c/(1 + d/m))", dict(type="1", prompt="", answer="", source="template"))
assert status == "checked", p
p, status = B.from_edit("y = v (a/x - b/(m c)) ; c", dict(type="3", prompt="", answer="", target="c"))
assert status == "checked" and p["answer"] == "c = (b v x)/(a m v - m x y)", p
p, status = B.from_edit("x^3 + 5 ; x - 2", dict(type="4", prompt="", answer="", divisor=""))
assert status == "checked" and p["answer"] == "x^2 + 2 x + 4 + 13/(x - 2)", p
p, status = B.with_answer(p, "x^2 + 2 x + 4")
assert status != "checked", p
for typ, bad in (("1", "a/(b +"), ("4", "x^3 + 5 ; ")):
    try:
        B.from_edit(bad, dict(type=typ, prompt="", answer="", divisor="")); raise AssertionError(("unreadable", bad))
    except ValueError:
        pass

print("adv_lesson_16: ok")
