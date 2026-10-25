"""sympy -> Typst (sheets/typmath.py): every expression reads back as itself,
and the key's form checks (sheets/check.py) see what was written.
Run from the project folder:  python3 tests/test_typmath.py"""
import random, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import sympy as sp
from sheets.typmath import tx, single, fr, text
from sheets.check import to_sympy, same_value, simplest_form, denominators

x, y, z, m, n = sp.symbols("x y z m n")
r = random.Random(4)

def nz(lo=1, hi=9):
    return r.choice((-1, 1)) * r.randint(lo, hi)

def monomial():
    return nz() * x ** nz(1, 5) * y ** r.randint(0, 4)

def shapes():
    """One random expression of each shape the banks write."""
    yield monomial()
    yield monomial() / (r.randint(1, 9) * x ** r.randint(1, 4) * z ** r.randint(0, 3))
    yield sum(nz() * x ** k for k in range(r.randint(1, 4))) + sp.Rational(nz(), r.randint(1, 5))
    yield nz() * x ** 2 + nz() * x + nz() + sp.Integer(nz()) / (r.randint(1, 4) * x + nz())
    yield (r.randint(1, 9) + nz() * sp.sqrt(r.choice((2, 3, 5, 7)))) / r.randint(2, 9)
    yield nz() * sp.sqrt(r.choice((2, 3, 5, 6))) / r.randint(2, 9)
    yield sp.Rational(nz(), r.randint(1, 9)) + sp.Rational(nz(), r.randint(1, 9)) * sp.I
    yield x ** (r.randint(1, 5) * m) + nz() * y ** (r.randint(1, 5) * n)
    yield x ** (m + r.randint(1, 5)) * y ** (m - r.randint(1, 5))
    yield nz() * x * (x + nz())
    yield r.randint(1, 9) * sp.pi * x ** r.randint(1, 3)
    yield (x * y + nz()) / (x ** 2 - nz() * y)

def same(a, b):
    return a == b or sp.simplify(a - b) == 0

for _ in range(120):
    for e in shapes():
        for t in (tx(e, "xyz"), single(e, "xyz")):
            assert same(to_sympy(t, imaginary=True), e), (e, t)
            assert simplest_form(t, imaginary=True) or not e.has(sp.I, sp.sqrt(2)), (e, t)
            assert "^(-" not in t and "xy" not in t.replace("sqrt", ""), t

# the key's order: descending degree, letters in order, then i; one fraction
assert tx(2 * x ** 2 - 3 * x + 5) == "2 x^2 - 3 x + 5"
assert tx(y ** 3 / (4 * x ** 2)) == "y^3/(4 x^2)"
assert tx(-3 * x / (4 * y)) == "-(3 x)/(4 y)"
assert tx(3 * sp.sqrt(2) * x * y ** 2) == "3 sqrt(2) x y^2"
assert tx(x ** (2 * m) - y ** (2 * n)) == "x^(2 m) - y^(2 n)"
assert tx(4 * sp.pi * x ** 2) == "4 pi x^2" and tx(x ** m) == "x^m"
assert tx(y * x, "yx") == "y x" and tx(x - 1) == "x - 1"
assert single((3 + 2 * sp.sqrt(2)) / 7) == "(3 + 2 sqrt(2))/7"
assert single(-(x + 1) / (2 * x)) == "-(x + 1)/(2 x)"
assert fr("x + 1", "2") == "(x + 1)/2" and fr("x^2", "y") == "x^2/y"
assert text("-x - 1 <= 2") == "−x − 1 ≤ 2"

# form checks read the text as written
assert not simplest_form("x^(-2) y") and not simplest_form("3/sqrt(2)")
assert simplest_form("(3 sqrt(2))/2") and simplest_form("y/x^2")
assert not simplest_form("2/(3 + i)", imaginary=True) and simplest_form("(6 - 2 i)/10", imaginary=True)
assert [str(d) for d in denominators("(x + 1)/(2 y)")] == ["2*y"]

# same_value: equal where it should be, and not where it shouldn't
assert same_value("(x^2 - 1)/(x - 1)", "x + 1") and not same_value("(x^2 - 1)/(x - 1)", "x - 1")
assert same_value("x^(2 m)/x^m", "x^m") and same_value("1/(1 + i)", "(1 - i)/2", imaginary=True)
assert same_value("cos(60 degree)", "1/2") and same_value("m(x + 2)", "m x + 2 m")

# Typst reads every form: compile them all, if typst is installed
if shutil.which("typst"):
    lines = [f"$display({tx(e, 'xyz')})$ #h(1em) $display({single(e, 'xyz')})$ \\" for _ in range(5) for e in shapes()]
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "forms.typ"
        src.write_text("\n".join(lines) + "\n")
        out = subprocess.run(["typst", "compile", str(src)], capture_output=True, text=True)
        assert out.returncode == 0, out.stderr
print("all typmath tests passed")
