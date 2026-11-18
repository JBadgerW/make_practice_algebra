"""Lesson 5 (Advanced Math): exponents and radicals, complex numbers, areas of
similar figures, diagonals of rectangular solids. Every source is reachable from
in-range parameters and checks with the deck's answer; wrong and unfinished
answers fail; every type draws and keeps its shape; edits solve again.

    python3 tests/test_adv_lesson_5.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_5 as B

lib = library.current()
assert "adv_lesson_5" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == ("Lesson 5: Exponents and Radicals, Complex Numbers, Areas of Similar Geometric Figures, "
                   "Diagonals of Rectangular Solids")
assert B.type_instructions("1") == "Simplify."
assert B.type_instructions("8") == "Answer each question."
assert B.type_instructions("9").startswith("Find the length of the diagonal")

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 5.1", "1", "sqrt(x^3 y) root(4, x y^3)", "x^(7/4) y^(5/4)"),
    ("PS 7", "1", "sqrt(x^3 y^2) root(4, x y^3)", "x^(7/4) y^(7/4)"),
    ("PS 8", "1", "x^(1/2) x^(3/4) sqrt(x y) root(3, x^4)", "x^(37/12) y^(1/2)"),
    ("ex 5.2", "2", "(a^(x/2) (y^(2 - x))^(1/2))/(a^(3 x) y^(-2 x))", "a^((-5 x)/2) y^((2 + 3 x)/2)"),
    ("PS 9", "2", "(a^(x/2) (y^(2 - x))^(1/2))/(a^(4 x) y^(-2 x))", "a^((-7 x)/2) y^((2 + 3 x)/2)"),
    ("PS 10", "2", "(y^(x + 3) y^(x/2 - 1) z^a)/(y^((x - a)/2) z^((x - a)/3))", "y^((2 x + a + 4)/2) z^((4 a - x)/3)"),
    ("ex 5.3", "3", "(x^(-2) + y^(-2))/(x y)^(-1)", "(x^2 + y^2)/(x y)"),
    ("PS 14", "3", "(x^(-2) + y^(-2))/(x y)^(-1)", "(x^2 + y^2)/(x y)"),
    ("ex 5.4", "4", "3 sqrt(3/2) - 4 sqrt(2/3) + 2 sqrt(24)", "(25 sqrt(6))/6"),
    ("PS 11", "4", "2 sqrt(3/2) - 3 sqrt(2/3) + 2 sqrt(24)", "4 sqrt(6)"),
    ("ex 5.5", "5", "(sqrt(2) + sqrt(x))(1 - sqrt(x))", "sqrt(2) + (1 - sqrt(2)) sqrt(x) - x"),
    ("PS 12", "5", "(sqrt(3) + sqrt(x))(sqrt(3) + sqrt(x))", "3 + 2 sqrt(3 x) + x"),
    ("PS 13", "5", "(sqrt(2) - sqrt(x))(1 - sqrt(x))", "sqrt(2) - (sqrt(2) + 1) sqrt(x) + x"),
    ("ex 5.6", "6", "3 i^3 + 2 i^5 - 3 i + 2 i^2", "-2 - 4 i"),
    ("PS 15", "6", "3 i^4 + 2 i^5 + 3 i^3 + 2 i^2", "1 - i"),
    ("ex 5.7", "7", "sqrt(-3) sqrt(4) + 3 sqrt(-2) sqrt(-9) + sqrt(-16) + sqrt(16)", "(4 - 9 sqrt(2)) + (2 sqrt(3) + 4) i"),
    ("PS 16", "7", "sqrt(-3) sqrt(4) + 3 sqrt(-2) sqrt(-9)", "-9 sqrt(2) + 2 sqrt(3) i"),
    ("PS 17", "7", "2 sqrt(-2) sqrt(2) + 3 i sqrt(2)", "(4 + 3 sqrt(2)) i"),
    ("ex 5.8", "8", "scale 4, rectangles", "16 to 1, or 1 to 16"),
    ("ex 5.9", "8", "one circle R, (3 R)/5; first", "25/9"),
    ("PS 6", "8", "big circle R, 2/5 R, meters; small", "4/25"),
    ("ex 5.10", "9", "BH; x, y, z", "sqrt(x^2 + y^2 + z^2)"),
    ("ex 5.11", "9", "CA; 2, 3, m", "sqrt(13 + m^2)"),
    ("PS 19", "9", "CA; 3, 2, n", "sqrt(13 + n^2)"),
]
prompt_of = {s[0]: s[2] for s in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt, typ) == answer, (sid, B.answer_of(prompt, typ), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source in exactly one type, and every type has a source
TYPE_OF = {s[0]: s[1] for s in SOURCES}
assert len(TYPE_OF) == len(SOURCES) == 24
assert set(TYPE_OF.values()) == set(B.KEYS)

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 5.1": (B.t1_two, dict(u="x", v="y", a=3, b=1, n=4, c=1, d=3)),
    "PS 7": (B.t1_two, dict(u="x", v="y", a=3, b=2, n=4, c=1, d=3)),
    "PS 8": (B.t1_mixed, dict(u="x", v="y", f1="1/2", f2="3/4", a=1, b=1, n=3, c=4)),
    "ex 5.2": (B.t2_quot, dict(a="a", y="y", x="x", p=1, q=2, m=2, sx="-", n=2, k=3, j=2, sj="-")),
    "PS 9": (B.t2_quot, dict(a="a", y="y", x="x", p=1, q=2, m=2, sx="-", n=2, k=4, j=2, sj="-")),
    "PS 10": (B.t2_three, dict(y="y", z="z", x="x", a="a", c1=3, c2=-1, h=2, d1=2, d2=3)),
    "ex 5.3": (B.t3_power, dict(x="x", y="y", a=1, m=2, s="+", b=1, n=2, k=1)),
    "PS 14": (B.t3_power, dict(x="x", y="y", a=1, m=2, s="+", b=1, n=2, k=1)),
    "ex 5.4": (B.t4, dict(a=3, p=3, q=2, s1="-", b=4, s2="+", c=2, k=2)),
    "PS 11": (B.t4, dict(a=2, p=3, q=2, s1="-", b=3, s2="+", c=2, k=2)),
    "ex 5.5": (B.t5_mixed, dict(p=2, s1="+", n=1, s2="-", x="x")),
    "PS 12": (B.t5_square, dict(p=3, s="+", x="x")),
    "PS 13": (B.t5_mixed, dict(p=2, s1="-", n=1, s2="-", x="x")),
    "ex 5.6": (B.t6, dict(terms=(("+", 3, 3), ("+", 2, 5), ("-", 3, 1), ("+", 2, 2)))),
    "PS 15": (B.t6, dict(terms=(("+", 3, 4), ("+", 2, 5), ("+", 3, 3), ("+", 2, 2)))),
    "ex 5.7": (B.t7, dict(terms=(("+", "K1", 1, 3, 2), ("+", "K2", 3, 2, 3), ("+", "K3", 1, 2, 4), ("+", "K4", 1, 2, 4)))),
    "PS 16": (B.t7, dict(terms=(("+", "K1", 1, 3, 2), ("+", "K2", 3, 2, 3)))),
    "PS 17": (B.t7, dict(terms=(("+", "K5", 2, 2, 2), ("+", "K6", 3, 2, 2)))),
    "ex 5.8": (B.t8_scale, dict(k=4, shapes="rectangles")),
    "ex 5.9": (B.t8_one, dict(shape="circle", L="R", a=3, b=5, first="first")),
    "PS 6": (B.t8_big, dict(shape="circle", L="R", a=2, b=5, unit="meters", small="small")),
    "ex 5.10": (B.t9, dict(diag="BH", w="x", d="y", h="z")),
    "ex 5.11": (B.t9, dict(diag="CA", w=2, d=3, h="m")),
    "PS 19": (B.t9, dict(diag="CA", w=3, d=2, h="n")),
}
assert set(REACH) == set(prompt_of)                                  # nothing left out
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid   # a template of the source's own type
# out of range is out
assert not B.in_range(B.t1_two, dict(u="x", v="y", a=2, b=4, n=4, c=1, d=3))     # sqrt(x^2 y^4): no radical left
assert not B.in_range(B.t4, dict(a=3, p=3, q=2, s1="-", b=4, s2="+", c=2, k=3) | dict(p=7, q=2))
assert not B.in_range(B.t8_one, dict(shape="circle", L="R", a=3, b=3, first="first"))
assert not B.in_range(B.t9, dict(diag="BH", w="x", d="x", h="z"))

# ---- wrong or unfinished answers fail
WRONG = [
    ("1", "sqrt(x^3 y) root(4, x y^3)", "x^(3/2) y^(1/2) x^(1/4) y^(3/4)"),   # bases not combined
    ("1", "sqrt(x^3 y) root(4, x y^3)", "x^(14/8) y^(5/4)"),                  # exponent not reduced
    ("1", "sqrt(x^3 y) root(4, x y^3)", "x^(3/4) y^(5/4)"),
    ("2", "(a^(x/2) (y^(2 - x))^(1/2))/(a^(3 x) y^(-2 x))", "a^((-5 x)/2) y^((2 - 3 x)/2)"),   # sign error
    ("2", "(a^(x/2) (y^(2 - x))^(1/2))/(a^(3 x) y^(-2 x))", "a^(x/2 - 3 x) y^((2 + 3 x)/2)"),   # not one fraction
    ("2", "(a^(x/2) (y^(2 - x))^(1/2))/(a^(3 x) y^(-2 x))", "y^((2 + 3 x)/2)/a^((5 x)/2)"),     # a power below
    ("2", "(a^(x/2) (y^(2 - x))^(1/2))/(a^(3 x) y^(-2 x))", "a^((-10 x)/4) y^((2 + 3 x)/2)"),   # not reduced
    ("3", "(x^(-2) + y^(-2))/(x y)^(-1)", "x y (x^(-2) + y^(-2))"),                            # negative exponents
    ("3", "(x^(-2) + y^(-2))/(x y)^(-1)", "(x^3 y + x y^3)/(x^2 y^2)"),                        # not lowest terms
    ("3", "(x^(-2) + y^(-2))/(x y)^(-1)", "(x^2 + y^2)/(x^2 y^2)"),
    ("4", "3 sqrt(3/2) - 4 sqrt(2/3) + 2 sqrt(24)", "25/sqrt(6)"),                             # not rationalized
    ("4", "3 sqrt(3/2) - 4 sqrt(2/3) + 2 sqrt(24)", "(50 sqrt(6))/12"),
    ("4", "2 sqrt(3/2) - 3 sqrt(2/3) + 2 sqrt(24)", "sqrt(96)"),                               # radicand not square-free
    ("5", "(sqrt(2) + sqrt(x))(1 - sqrt(x))", "sqrt(2) + sqrt(x) - sqrt(2 x) - x"),            # middle not combined
    ("5", "(sqrt(2) + sqrt(x))(1 - sqrt(x))", "sqrt(2) + (1 + sqrt(2)) sqrt(x) - x"),
    ("5", "(sqrt(3) + sqrt(x))(sqrt(3) + sqrt(x))", "3 + 2 sqrt(3) sqrt(x) + x"),             # radicals not multiplied
    ("5", "(sqrt(3) + sqrt(x))(sqrt(3) + sqrt(x))", "3 + x"),
    ("6", "3 i^3 + 2 i^5 - 3 i + 2 i^2", "-2 - 4 i^1"),
    ("6", "3 i^3 + 2 i^5 - 3 i + 2 i^2", "-4 i - 2"),                                         # not a + b i
    ("6", "3 i^4 + 2 i^5 + 3 i^3 + 2 i^2", "1 + i"),
    ("7", "sqrt(-3) sqrt(4) + 3 sqrt(-2) sqrt(-9)", "9 sqrt(2) + 2 sqrt(3) i"),                # sqrt(-2) sqrt(-9) taken as sqrt(18)
    ("7", "sqrt(-3) sqrt(4) + 3 sqrt(-2) sqrt(-9)", "2 sqrt(-3) - 9 sqrt(2)"),                 # sqrt of a negative left
    ("7", "2 sqrt(-2) sqrt(2) + 3 i sqrt(2)", "4 i + 3 sqrt(2) i"),                            # like terms not grouped
    ("7", "sqrt(-3) sqrt(4) + 3 sqrt(-2) sqrt(-9) + sqrt(-16) + sqrt(16)", "(4 - 9 sqrt(2)) + (2 sqrt(3) + sqrt(16)) i"),
    ("8", "one circle R, (3 R)/5; first", "9/25"),                                             # upside down
    ("8", "one circle R, (3 R)/5; first", "5/3"),                                              # not squared
    ("8", "big circle R, 2/5 R, meters; small", "8/50"),
    ("8", "scale 4, rectangles", "4 to 1, or 1 to 4"),
    ("9", "CA; 2, 3, m", "sqrt(4 + 9 + m^2)"),                                                 # numbers not combined
    ("9", "CA; 2, 3, m", "sqrt(5 + m^2)"),
    ("9", "BH; x, y, z", "sqrt(x^2 + y^2)"),                                                   # the base diagonal
    ("9", "CA; 2, 6, 9", "sqrt(121)"),
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (typ, prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
SHAPE = {
    "1": r"^(?:[a-z]\^\(\d/\d\) ){0,2}sqrt\([^()]*\) root\(\d, [^()]*\)$",
    "2": r"^\(.*\)/\(.*\)$",
    "3": r"^\(.*\^\(-\d\).*\)/.*\^\(-\d\)\)?$",
    "4": r"^(?:\d )?sqrt\(\d/\d\) [+-] (?:\d )?sqrt\(\d/\d\) [+-] (?:\d )?sqrt\(\d+\)$",
    "5": r"^\((?:sqrt\(\d+\)) [+-] sqrt\([a-z]\)\)\((?:sqrt\(\d+\)|\d) [+-] sqrt\([a-z]\)\)$",
    "6": r"^(?:\d )?i(?:\^\d)?(?: [+-] (?:\d )?i(?:\^\d)?){2,3}$",
    "7": r"sqrt\(-\d+\)",
    "8": r"^(scale|one|big) ",
    "9": r"^(BH|CE|CA); ",
}
ANSWER_SHAPE = {
    "1": r"^[a-z](\^\S+)?( [a-z](\^\S+)?)*$", "6": r"^-?\d+ [+-] (\d+ )?i$", "8": r"^\d+/\d+$|to 1, or 1 to",
    "9": r"^sqrt\(.*\)$|^\d+( sqrt\(\d+\))?$|^sqrt\(\d+\)$",
}
rng = random.Random(5)
for k in B.KEYS:
    for rep in range(4):
        seen = set()
        for _ in range(20):
            p = B.generate(k, rng, seen)
            assert B.check(p) == "checked", p
            assert re.search(SHAPE[k], p["prompt"]), (k, p)
            if k in ANSWER_SHAPE:
                assert re.search(ANSWER_SHAPE[k], p["answer"]), (k, p)
            if k not in "89":
                assert not re.search(r"(?<![\d.])1 [a-z(]", p["prompt"] + " " + p["answer"]), p   # no 1 x, 1 sqrt
            if k == "3":
                assert "/" in p["answer"] and not p["answer"].startswith("-"), p
            if k == "7":
                assert p["answer"].endswith("i") and "sqrt(-" not in p["answer"], p

# ---- showing
s = dict(type="1", prompt="sqrt(x^3 y) root(4, x y^3)", answer="x^(7/4) y^(5/4)")
assert B.typst(s) == "$display(sqrt(x^3 y) root(4, x y^3))$", B.typst(s)
assert B.text(s) == "√(x^3 y) ⁴√(x y^3)", B.text(s)
s8 = dict(type="8", prompt="one circle R, (3 R)/5; first", answer="25/9")
assert B.typst(s8).startswith("The radius of one circle is $R$, and the radius of a second circle is $(3 R)/5$."), B.typst(s8)
assert B.text(s8).endswith("to the area of the second circle?"), B.text(s8)
assert B.answer_typst(dict(type="8", prompt="scale 4, rectangles", answer="16 to 1, or 1 to 16")) == "16 to 1, or 1 to 16"
s9 = dict(type="9", prompt="CA; 2, 3, m", answer="sqrt(13 + m^2)")
q, key = B.typst(s9), B.key_typst(s9)
assert "cetz.canvas" in q and B.fig.KEY_INK not in q and B.fig.KEY_INK in key       # red on the key only
assert re.sub(r"\s+", "", q).count("rect(") == re.sub(r"\s+", "", key).count("rect(")
assert B.text(s9) == "Find the length of diagonal AC in the rectangular solid shown.   [figure]", B.text(s9)
hide, show = B.slide_typst(s9), B.slide_typst(s9, key=True)
assert "#hide[" in hide and "#text(fill: red)" in show and "sqrt(13 + m^2)" in show
assert B.slide_typst(s) is None
assert B.height(s9) > 1.5

# ---- editing: a new prompt is solved again; a typed answer is checked; unreadable edits raise
old = dict(type="1", prompt="", answer="", source="template")
p, status = B.from_edit("√(x^5 y) root(3, x y^2)", old)
assert status == "checked" and p["answer"] == "x^(17/6) y^(7/6)", p
p, status = B.with_answer(p, "x^(17/6) y^(7/6)")
assert status == "checked"
p, status = B.with_answer(p, "x^(5/2) x^(1/3) y^(7/6)")
assert status != "checked"
p, status = B.from_edit("4 i^3 − i^6", dict(old, type="6"))
assert status == "checked" and p["answer"] == "1 - 4 i", p
p, status = B.from_edit("CA; 4, 1, h; C left", dict(old, type="9"))
assert status == "checked" and p["answer"] == "sqrt(17 + h^2)", p
p, status = B.from_edit("big square s, 3/4 s, feet; large", dict(old, type="8"))
assert status == "checked" and p["answer"] == "16/9", p
for typ, bad in (("1", "sqrt(x^3"), ("5", "(sqrt(2) + x)(1 - x"), ("8", "the circles"), ("9", "AC; 2, 3")):
    try:
        B.from_edit(bad, dict(old, type=typ)); raise AssertionError(("unreadable", typ, bad))
    except ValueError:
        pass

print("adv_lesson_5: ok")
