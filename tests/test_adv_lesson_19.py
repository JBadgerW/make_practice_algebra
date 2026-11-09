"""Lesson 19 (Advanced Math): nonlinear systems, factoring exponentials, sums and
differences of cubes. Every type draws and checks; the deck's own problems check
with the deck's answers; wrong and unfinished answers fail; edits solve again.

    python3 tests/test_adv_lesson_19.py
"""
import random, re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_19 as B

lib = library.current()
assert "adv_lesson_19" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE.startswith("Lesson 19: ")
assert B.type_instructions("1") == "Solve." and B.type_instructions("5") == "Simplify."

# ---- numbers as the deck writes them
import sympy as sp
assert B.number(sp.Rational(-1, 2) + sp.sqrt(17) / 2) == "-1/2 + sqrt(17)/2"
assert B.number(-1 - sp.sqrt(5)) == "-1 - sqrt(5)"
assert B.number(-2 * sp.sqrt(2)) == "-2 sqrt(2)"
assert B.number(sp.Rational(2, 5) - 3 * sp.sqrt(51) / 5) == "2/5 - (3 sqrt(51))/5"
assert B.number(sp.Integer(4)) == "4"

# ---- the deck's problems, with the deck's answers
DECK = [
    ("1", "x^2 + y^2 = 9; y - x = 1",
     '(-1/2 + sqrt(17)/2, 1/2 + sqrt(17)/2) "and" (-1/2 - sqrt(17)/2, 1/2 - sqrt(17)/2)'),
    ("2", "x^2 + y^2 = 9; 2 x^2 - y^2 = -6",
     "(1, 2 sqrt(2)), (1, -2 sqrt(2)), (-1, 2 sqrt(2)), (-1, -2 sqrt(2))"),
    ("3", "x y = -4; y = -x - 2", '(-1 + sqrt(5), -1 - sqrt(5)) "and" (-1 - sqrt(5), -1 + sqrt(5))'),
    ("4", "3 x^(2 n + 2) + 12 x^(3 n + 3)", "3 x^(2 n + 2) (1 + 4 x^(n + 1))"),
    ("4", "4 x^(3 n + 2) - 6 x^(4 n + 1)", "2 x^(3 n + 1) (2 x - 3 x^n)"),
    ("5", "(x^(2 a) - y^(2 b))/(x^a + y^b)", "x^a - y^b"),
    ("5", "(x^(4 a) - y^(4 b))/(x^(2 a) + y^(2 b))", "x^(2 a) - y^(2 b)"),
    ("6", "x^3 y^3 - p^3", "(x y - p) (x^2 y^2 + x y p + p^2)"),
    ("6", "8 m^3 y^6 + x^3", "(2 m y^2 + x) (4 m^2 y^4 - 2 m y^2 x + x^2)"),
    ("6", "27 x^12 y^6 - z^9", "(3 x^4 y^2 - z^3) (9 x^8 y^4 + 3 x^4 y^2 z^3 + z^6)"),
]
for typ, prompt, answer in DECK:
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", (prompt, answer)
    if typ in B.SYSTEMS:
        assert B.answer_of(prompt) == answer, (B.answer_of(prompt), answer)

# ---- wrong, missing, or unsimplified answers fail
WRONG = [
    ("1", "x^2 + y^2 = 9; y - x = 1", "(-1/2 + sqrt(17)/2, 1/2 + sqrt(17)/2)"),                 # one point missing
    ("1", "x^2 + y^2 = 9; y - x = 1",
     '(-1/2 + sqrt(17)/2, 1/2 - sqrt(17)/2) "and" (-1/2 - sqrt(17)/2, 1/2 + sqrt(17)/2)'),          # y's swapped
    ("1", "x^2 + y^2 = 9; y - x = 1",
     '((-1 + sqrt(17))/2, (1 + sqrt(17))/2) "and" ((-1 - sqrt(17))/2, (1 - sqrt(17))/2)'),         # right, but not the key's form... still exact
    ("2", "x^2 + y^2 = 9; 2 x^2 - y^2 = -6", "(1, sqrt(8)), (1, -sqrt(8)), (-1, sqrt(8)), (-1, -sqrt(8))"),
    ("2", "x^2 + y^2 = 9; 2 x^2 - y^2 = -6", '(1, 2 sqrt(2)) "and" (-1, -2 sqrt(2))'),
    ("3", "x y = -4; y = -x - 2", '(-2/2 + sqrt(5), -1 - sqrt(5)) "and" (-1 - sqrt(5), -1 + sqrt(5))'),
    ("3", "x y = -4; y = -x - 2", '(-1 + sqrt(5), -1 - sqrt(5)), (-1 + sqrt(5), -1 - sqrt(5))'),
    ("4", "3 x^(2 n + 2) + 12 x^(3 n + 3)", "3 x^(2 n + 1) (x + 4 x^(n + 2))"),                      # x is still common
    ("4", "3 x^(2 n + 2) + 12 x^(3 n + 3)", "x^(2 n + 2) (3 + 12 x^(n + 1))"),                        # 3 is still common
    ("4", "3 x^(2 n + 2) + 12 x^(3 n + 3)", "3 x^(2 n + 2) (1 + 4 x^(n + 2))"),                       # wrong value
    ("5", "(x^(2 a) - y^(2 b))/(x^a + y^b)", "x^a + y^b"),
    ("6", "x^3 y^3 - p^3", "(x y - p) (x^2 y^2 - x y p + p^2)"),
    ("6", "8 m^3 y^6 + x^3", "(2 m y^2 + x) (4 m^2 y^4 - 2 m y^2 x + x^2) + 0"),
]
for i, (typ, prompt, answer) in enumerate(WRONG):
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    if i == 2:
        assert got == "checked", "the same exact values written as one fraction are fine"
    else:
        assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its rules
rng = random.Random(19)
for k in B.KEYS:
    seen = set()
    for _ in range(60):
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        if k in B.SYSTEMS:
            pts = B.read_points(p["answer"])
            assert len(pts) == (4 if k == "2" else 2), p
            xs = [float(sp.sympify(B.to_sympy(a))) for a, _ in pts]
            assert xs == sorted(xs, reverse=True), "largest x first"
            assert ('"and"' in p["answer"]) == (len(pts) == 2)
            assert len(B.equations(p["prompt"])) == 2 and B.equations(p["prompt"])[0].startswith(("x^2 + y^2 =", "x y ="))
            assert "-x + y" not in p["prompt"] and "- -" not in p["prompt"] and "+ -" not in p["prompt"], p
        else:
            assert ";" not in p["prompt"]
        if k == "5":
            pairs = re.findall(r"([a-z])\^\(?(?:\d+ )?([a-z])", p["prompt"])
            assert pairs and all(base != e for base, e in pairs), ("a letter its own exponent", p)
        assert "1 x" not in p["prompt"] and "1 x" not in p["answer"]

# ---- showing
s = dict(type="2", prompt="x^2 + y^2 = 9; 2 x^2 - y^2 = -6", answer=DECK[1][2])
assert B.typst(s) == "$display(cases(x^2 + y^2 = 9, 2 x^2 - y^2 = -6))$"
assert B.text(s) == "{ x^2 + y^2 = 9\n{ 2 x^2 − y^2 = −6"
assert B.answer_text(dict(s, answer=DECK[2][2])).count(" and ") == 1
assert B.typst(dict(type="5", prompt=DECK[5][1], answer="")).startswith("$display(")

# ---- editing: a system is solved again; an answer typed with "and" is read
p, status = B.from_edit("x^2 + y^2 = 25 ; x + y = 7", dict(type="1", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"] == '(4, 3) "and" (3, 4)' and p["prompt"] == "x^2 + y^2 = 25; x + y = 7", p
p, status = B.with_answer(dict(type="3", prompt="x y = -4; y = -x - 2", answer=""),
                          "(-1 + sqrt(5), -1 - sqrt(5)) and (-1 - sqrt(5), -1 + sqrt(5))")
assert status == "checked", p
try:
    B.with_answer(p, "x = 4"); raise AssertionError("not points")
except ValueError:
    pass
p, status = B.from_edit("3 x^(2 n + 2) + 12 x^(3 n + 3)", dict(type="4", prompt="", answer="3 x^(2 n + 2) (1 + 4 x^(n + 1))"))
assert status == "checked" and p["source"] == "edited", "letters in the exponents: the old answer stays"
p, status = B.from_edit("x^3 - 8", dict(type="6", prompt="", answer=""))
assert status == "checked", p

print("adv_lesson_19: ok")
