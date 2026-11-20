"""Lesson 26 (Advanced Math): the logarithmic form of the exponential,
logarithmic equations. Every source is reachable from in-range parameters and
checks with the deck's answer; wrong answers fail; every type draws, checks,
and keeps its shape; edits solve again.

    python3 tests/test_adv_lesson_26.py
"""
import random, re
import sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import library
from sheets.banks import adv_lesson_26 as B

lib = library.current()
assert "adv_lesson_26" in dict(lib.view("Advanced Math"))["Lessons"]
assert B.TITLE == "Lesson 26: The Logarithmic Form of the Exponential, Logarithmic Equations"
assert B.type_instructions("1") == "Write each equation in logarithmic form."
assert B.type_instructions("2") == "Write each equation in exponential form."
assert all(B.type_instructions(k) == "Solve." for k in "34567")

# ---- every source: the deck's answer, and checked
SOURCES = [   # (id, type, prompt, deck answer)
    ("ex 26.1", "1", "4 = 3^y", "log_3 4 = y"),
    ("ex 26.2", "2", "log_x 4 = m", "x^m = 4"),
    ("ex 26.3", "3", "log_b 8 = 3", "b = 2"),
    ("ex 26.4", "4", "log_b 9 = -1/2", "b = 1/81"),
    ("ex 26.5", "5", "log_3 (1/27) = M", "M = -3"),
    ("ex 26.6", "7", "log_(1/3) P = -2", "P = 9"),
    ("ex 26.7", "6", "log_4 8 = x", "x = 3/2"),
    ("PS 6a", "1", "k^p = 7", "log_k 7 = p"),
    ("PS 6b", "2", "log_k 7 = p", "k^p = 7"),
    ("PS 7a", "2", "log_b 12 = a", "b^a = 12"),
    ("PS 7b", "1", "b^a = 12", "log_b 12 = a"),
    ("PS 8", "3", "log_b 27 = 3", "b = 3"),
    ("PS 9", "5", "log_2 (1/8) = m", "m = -3"),
    ("PS 10", "7", "log_(1/2) c = -4", "c = 16"),
]
prompt_of = {s[0]: s[2] for s in SOURCES}
for sid, typ, prompt, answer in SOURCES:
    assert B.answer_of(prompt, typ) == answer, (sid, B.answer_of(prompt, typ), answer)
    assert B.check(dict(type=typ, prompt=prompt, answer=answer)) == "checked", sid

# ---- every source is reachable: its template builds it from in-range parameters
REACH = {
    "ex 26.1": (B.t1, dict(b=F(3), L="y", N=F(4), power_first=False)),
    "ex 26.2": (B.t2, dict(b="x", N=F(4), L="m")),
    "ex 26.3": (B.t3, dict(x="b", b=2, L=3)),
    "ex 26.4": (B.t4, dict(x="b", root=3, n=2, m=-4)),
    "ex 26.5": (B.t5, dict(x="M", b=F(3), k=-3)),
    "ex 26.6": (B.t7, dict(x="P", b=F(1, 3), L=F(-2))),
    "ex 26.7": (B.t6, dict(x="x", root=2, m=2, n=3)),
    "PS 6a": (B.t1, dict(b="k", L="p", N=F(7), power_first=True)),
    "PS 6b": (B.t2, dict(b="k", N=F(7), L="p")),
    "PS 7a": (B.t2, dict(b="b", N=F(12), L="a")),
    "PS 7b": (B.t1, dict(b="b", L="a", N=F(12), power_first=True)),
    "PS 8": (B.t3, dict(x="b", b=3, L=3)),
    "PS 9": (B.t5, dict(x="m", b=F(2), k=-3)),
    "PS 10": (B.t7, dict(x="c", b=F(1, 2), L=F(-4))),
}
assert set(REACH) == set(prompt_of)                                    # nothing left out
TYPE_OF = {s[0]: s[1] for s in SOURCES}
for sid, (build, params) in REACH.items():
    assert build(**params) == prompt_of[sid], (sid, build(**params))
    assert B.in_range(build, params), sid
    assert any(b is build for _, b in B.TEMPLATES[TYPE_OF[sid]]), sid  # the type's own template
assert sorted(set(TYPE_OF.values())) == B.KEYS                          # every type has a source
# out of range, or another type's problem
assert not B.in_range(B.t4, dict(x="b", root=2, n=3, m=1))             # log 3: a Type 3 problem
assert not B.in_range(B.t6, dict(x="x", root=2, m=2, n=4))             # log 2: a Type 5 problem
assert not B.in_range(B.t3, dict(x="b", b=2, L=1))                     # log_b 2 = 1
assert not B.in_range(B.t5, dict(x="x", b=F(3), k=0))                  # log_3 1 = 0
assert not B.in_range(B.t1, dict(b="k", L="k", N=F(7), power_first=True))   # one letter twice
assert not B.in_range(B.t1, dict(b=F(2), L=F(3), N=F(9), power_first=True)) # 2^3 = 9 is false
assert not B.in_range(B.t7, dict(x="x", b=F(6), L=F(1, 2)))            # sqrt(6) isn't rational
assert not B.in_range(B.t2, dict(b=F(2), N=F(16), L="j"))              # log_2 16 = j: Type 5's

# ---- wrong answers fail
WRONG = [
    ("1", "4 = 3^y", "log_y 4 = 3"),                    # base and log swapped
    ("1", "4 = 3^y", "log_4 3 = y"),                    # base and number swapped
    ("1", "4 = 3^y", "3^y = 4"),                        # still exponential
    ("2", "log_x 4 = m", "m^x = 4"),
    ("2", "log_x 4 = m", "4 = x^m"),                    # the power goes first, as the deck writes it
    ("2", "log_x 4 = m", "log_x 4 = m"),
    ("1", "2^5 = 32", "log_2 32 = 6"),
    ("3", "log_b 8 = 3", "b = 8/3"),
    ("3", "log_b 8 = 3", "x = 2"),                      # the wrong letter
    ("3", "log_b 8 = 3", "2"),                          # the letter not named
    ("4", "log_b 9 = -1/2", "b = 81"),                  # sign of the power lost
    ("4", "log_b 9 = -1/2", "b = -3"),
    ("4", "log_b 9 = -1/2", "b = 2/162"),               # not in lowest terms
    ("5", "log_3 (1/27) = M", "M = 3"),
    ("5", "log_3 (1/27) = M", "M = 1/27"),
    ("6", "log_4 8 = x", "x = 2/3"),                    # upside down
    ("6", "log_4 8 = x", "x = 6/4"),
    ("7", "log_(1/3) P = -2", "P = 1/9"),
    ("7", "log_(1/3) P = -2", "P = -9"),
    ("7", "log_(1/2) c = -4", "c = 8"),
]
for typ, prompt, answer in WRONG:
    got = B.check(dict(type=typ, prompt=prompt, answer=answer))
    assert got != "checked", (prompt, answer, got)

# ---- every type: drawn, checked, and in its shape
def unknown(p):
    _, b, L, N = B.read(p["prompt"])
    return "b" if isinstance(b, str) else "L" if isinstance(L, str) else "N"

rng = random.Random(26)
for k in B.KEYS:
    seen = set()
    for i in range(300):
        if i % 60 == 0:
            seen = set()
        p = B.generate(k, rng, seen)
        assert B.check(p) == "checked", p
        assert B.answer_of(p["prompt"], k) == p["answer"], p
        form, b, L, N = B.read(p["prompt"])
        ls = B.letters_in(b, L, N)
        if k == "1":
            assert form != "log" and B.read(p["answer"])[0] == "log", p
        elif k == "2":
            assert form == "log" and B.read(p["answer"])[0] == "exp", p
        else:
            assert form == "log" and len(ls) == 1, p
            v = F(p["answer"].split(" = ")[1])
            assert v > 0 or k in "56", p
            if k == "3":
                assert unknown(p) == "b" and L.denominator == 1 and L > 1 and v.denominator == 1, p
            if k == "4":
                assert unknown(p) == "b" and (L < 0 or L.denominator > 1), p
            if k == "5":
                assert unknown(p) == "L" and v.denominator == 1 and v not in (0, 1), p
            if k == "6":
                assert unknown(p) == "L" and v.denominator > 1, p
            if k == "7":
                assert unknown(p) == "N", p
        assert all(abs(x.numerator) <= 1000 and x.denominator <= 1000 for x in (b, L, N) if isinstance(x, F)), p

# ---- showing: each problem in its own sentence, set as the deck sets it
s = dict(type="7", prompt="log_(1/3) P = -2", answer="P = 9")
assert B.typst(s) == "Solve: #h(0.5em) $log_(1\\/3) P = -2$", B.typst(s)
assert B.text(s) == "Solve: log_(1/3) P = -2"
s = dict(type="5", prompt="log_3 (1/27) = M", answer="M = -3")
assert B.typst(s) == "Solve: #h(0.5em) $log_3 display(1/27) = M$", B.typst(s)
s = dict(type="4", prompt="log_b 9 = -1/2", answer="b = 1/81")
assert B.typst(s) == "Solve: #h(0.5em) $log_b 9 = -display(1/2)$", B.typst(s)
assert B.answer_typst(s) == "$b = display(1/81)$"
s = dict(type="1", prompt="4 = 3^y", answer="log_3 4 = y")
assert B.typst(s) == "Write $4 = 3^y$ in logarithmic form." and B.text(s) == "Write 4 = 3^y in logarithmic form."
s = dict(type="2", prompt="3^(-2) = 1/9", answer="")
assert B.typst(dict(s, type="1")) == "Write $3^(-2) = display(1/9)$ in logarithmic form."

# ---- editing: a new prompt is solved again; a typed answer is checked
p, status = B.from_edit("log_b 16 = -1/2", dict(type="4", prompt="", answer="", source="template"))
assert status == "checked" and p["answer"] == "b = 1/256", p
p, status = B.from_edit("5 = 2^t", dict(type="1", prompt="", answer=""))
assert status == "checked" and p["answer"] == "log_2 5 = t", p
p, status = B.with_answer(dict(type="6", prompt="log_8 4 = x", answer=""), "x = 2/3")
assert status == "checked", p
p, status = B.with_answer(p, "x = 3/2")
assert status == "failed", p
try:
    B.from_edit("log b 8 3", dict(type="3", prompt="", answer="")); raise AssertionError("unreadable")
except ValueError:
    pass

print("adv_lesson_26: ok")
