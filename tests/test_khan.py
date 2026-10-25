"""The Khan banks and what they share: banks found in packages, terms as
written, multiple choice, one-variable linear equations, and every Khan
lesson's tags, titles, and draws. Run from the project folder:
    python3 tests/test_khan.py
"""
import os, random, re, sys, tempfile
from decimal import Decimal as D
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="config_")
from sheets import library as L, gen, linear
from sheets.check import to_sympy

# ---- terms as written, and read back as the same expression
cases = {((-7, ""), (4, "m"), (10, "")): "-7 + 4 m + 10",
         ((1, "x"), (-1, "")): "x - 1",
         ((F(2, 3), "p"), (-5, "")): "2/3 p - 5",
         ((D("0.5"), "s"), (1, "")): "0.5 s + 1",
         ((-1, "(x + 3)"),): "-(x + 3)",
         ((3, "(x + 5)"), (0, "x")): "3 (x + 5)",
         ((0, "x"),): "0"}
for terms, want in cases.items():
    got = gen.written(*terms)
    assert got == want, (terms, got)
    at = lambda e: float(e.subs({s: 1.7 for s in e.free_symbols}))
    value = sum(float(c) * (at(to_sympy(v)) if v else 1) for c, v in terms)
    assert abs(at(to_sympy(got)) - value) < 1e-9, got

# ---- multiple choice
r = random.Random(4)
choices, answer = gen.lettered(r, "x = 4", ["x = -4", "x = 1/4", "x = 2"])
assert sorted(choices) == sorted(["x = 4", "x = -4", "x = 1/4", "x = 2"]) and gen.chosen(dict(choices=choices, answer=answer)) == ["x = 4"]
choices, answer = gen.lettered(r, ["a", "b"], ["c"], shuffle=False)
assert (choices, answer) == (["a", "b", "c"], "A, B")
assert gen.in_order(["No", "One", "All"], "All") == (["No", "One", "All"], "C")
try:
    gen.lettered(r, "a", ["a", "b"]); raise AssertionError("two choices alike")
except gen.Redraw:
    pass
p = dict(choices=["No", "One", "All"], answer="B")
assert gen.choice_answer_typst(p) == "B. One"
assert gen.with_letters(p, " c ", lambda q: "checked") == (dict(p, answer="C"), "checked")
try:
    gen.with_letters(p, "D", lambda q: "checked"); raise AssertionError("no choice D")
except ValueError:
    pass

# ---- linear equations
assert linear.answer_of("12 c - 4 = 14 c - 10") == "c = 3" and linear.answer_of("2 - 1/2 n = 3 n + 16") == "n = -4"
assert linear.count("4 (t + 5) = 20 + 4 t") == "all" and linear.count("-4 (x + 6) = 24 - 4 x") == "none"
assert linear.solves("12 c - 4 = 14 c - 10", "c = 3") and not linear.solves("12 c - 4 = 14 c - 10", "c = -3")
assert not linear.solves("4 (t + 5) = 20 + 4 t", "t = 1"), "an identity has no one solution"

# ---- the library: banks one level into a package, tagged with Khan courses and units
lib = L.Library(Path(tempfile.mkdtemp()) / "missing")
assert not lib.warnings, lib.warnings
khan = sorted(n for n in lib.names() if n.startswith(("ka1_", "ka2_", "kpa_")))
assert "ka1_02_01" in khan and "khan_alg1" not in lib.names(), "a package of lessons is not itself a bank"
assert "literal" in lib.names(), "a package that is a bank still is one"
for n in khan:
    b = lib.get(n)
    course = {"ka1": "Khan Algebra 1", "ka2": "Khan Algebra 2", "kpa": "Khan Prealgebra"}[n[:3]]
    unit, lesson = int(n[4:6]), int(n[7:9])
    assert list(b.COURSES) == [course] and lib.unit_of(n, course).startswith(f"Unit {max(unit, 1)}:"), n
    assert re.match(rf"Lesson {unit}-{lesson}[a-z]?: \S", b.TITLE), b.TITLE
    for k in b.KEYS:                        # every type draws, checks, and shows
        seen = set()
        for i in range(8):
            p = b.generate(k, random.Random(f"{n}{k}{i}"), seen)
            assert b.check(p) == "checked" and b.typst(p) and b.answer_typst(p) and b.text(p), (n, k, p)
units = dict(lib.view("Khan Algebra 1"))
unit2 = units["Unit 2: Solving equations & inequalities"]
assert unit2.index("ka1_02_01") < unit2.index("ka1_02_06"), "lessons in order"
print(f"all khan tests passed ({len(khan)} lessons)")
