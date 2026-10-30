"""The warm-up's decoys: look-alike wrong answers, never a common slip.
Run from the project folder:  python3 tests/test_decoys.py"""
import random, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets.decoys import decoy, plan, shape, numbers

r = random.Random(1)
k6 = {decoy("$display(k = 6)$", r) for _ in range(300)}
assert k6 and all(d.startswith("$display(k = ") for d in k6)
assert not k6 & {f"$display(k = {n})$" for n in (6, -6, 4, 5, 7, 8, 12, 3, 60, 0)}, k6
k_neg = {decoy("$display(p = -14)$", r) for _ in range(300)}
assert all(d.startswith("$display(p = -") for d in k_neg), "the sign stays"
assert not k_neg & {f"$display(p = -{n})$" for n in (12, 13, 14, 15, 16, 28, 7, 41, 140)}, k_neg
assert all(5 <= int(d[14:-2]) <= 42 for d in k_neg), "within a factor of three"

for _ in range(100):
    d = decoy("$display(display((6 sqrt(5))/5))$", r)
    assert "sqrt(5)" in d, "nothing under a root changes"
    d = decoy("$x^2 + 3$", r)
    assert d.startswith("$x^2 + "), "nor an exponent"
    d = decoy("$x = 2.5$", r)
    assert len(d) == len("$x = 2.5$") and not d.endswith("0$"), d
assert decoy("$display(V_2 = (P_1 V_1)/P_2)$", r) is None, "subscripts only: nothing to change"
assert decoy("no solution", r) is None
assert [m.group() for m in numbers("$(-5, 2, 1)$")] == ["5", "2", "1"]
assert shape("$k = 5$") == shape("$k = 12$") != shape("$h = 5$")

answers = ["$k = 5$", "$h = -3$", "$x = 2$", "$x = 7$", "no solution", "$V = m/D$"]
fake, stuck = plan(answers, 0)
assert [i for i, _ in fake] == [0, 1] and stuck == [4, 5], (fake, stuck)
assert plan(answers, 0) == (fake, stuck), "the same answers and seed: the same decoys"
assert plan(answers, 1)[0] != fake, "another seed: new decoys"
shapes = Counter(shape(a) for a in answers[:4] + [d for _, d in fake])
assert min(shapes.values()) == 2, "every answer with a decoy now shares its shape"
assert not {d for _, d in fake} & set(answers)

print("all decoy tests passed")
