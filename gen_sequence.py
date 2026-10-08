"""Lesson 1-4 literal equations, re-sequenced by solving strategy.

The 50 equations from the original lesson 1-4 literal-equations worksheet are sorted into eleven
types plus two special cases and renumbered 1-50 in that order. Every
solution and every worked step is written in Typst math and checked numerically with
sympy before any Typst is emitted. Run from this folder:
    python3 gen_sequence.py [--class NAME] [--groups 9 8 3+4=Warm-up ...] && cd lesson_1-4 && for f in *.typ; do typst compile $f; done
"""
import argparse, json, random
from pathlib import Path
import make_practice as mp
from literal_common import (TYPES, label, to_sympy, side_diff, syms_of, holds,
                            MARK, head, slhead, vars_)

ap = argparse.ArgumentParser(description="Write the lesson 1-4 set into lesson_1-4/.")
ap.add_argument("--class", dest="class_name", default="Algebra 1", metavar="NAME",
                help="class name in the worksheet and slide header (default: Algebra 1)")
ap.add_argument("--groups", nargs="+", default=[], metavar="GROUP",
                help="print the worksheet, key, and slides in this order; join types with +, "
                     "rename with =: 9 8 3+4=Warm-up 1  (the guide and all-solutions stay in lesson order)")
ap.add_argument("--seed", type=int, default=0, help="shuffles the problems inside mixed groups (default: 0)")
_a = ap.parse_args()
CLASS = _a.class_name
try:
    GROUPS = mp.parse_groups(_a.groups)
except ValueError as e:
    ap.error(str(e))

HERE = Path(__file__).resolve().parent
OUT = HERE / "lesson_1-4"; OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------------
# Equations (from the original gen_literal.py, renumbered in sequence order). Typst math syntax.
# A solution of None means "already solved for this variable (given)".
# ------------------------------------------------------------------

SOURCE = [  # (label, prompt, book target, {var: solution})
    ('Try It 1a', 'y = x + 12', 'x', {'x': 'y - 12', 'y': None}),
    ('Try It 1b', 'n = 4/5 (m + 7)', 'm', {'m': '5/4 n - 7', 'n': None}),
    ('Ex. 2', 'd = r t', 'r', {'r': 'd/t', 't': 'd/r', 'd': None}),
    ('Ex. 3', 'P = 2 ell + 2 w', 'w', {'w': '(P - 2 ell)/2', 'ell': '(P - 2 w)/2', 'P': None}),
    ('Try It 3', 'A = 1/2 b h', 'h', {'h': '(2A)/b', 'b': '(2A)/h', 'A': None}),
    ('Ex. 4', 'C = 5/9 (F - 32)', 'F', {'F': '9/5 C + 32', 'C': None}),
    ('Try It 4', 'K = C + 273.15', 'C', {'C': 'K - 273.15', 'K': None}),
    ('Example', 'V = ell w h', 'h', {'h': 'V/(ell w)', 'ell': 'V/(w h)', 'w': 'V/(ell h)', 'V': None}),
    ('Check 2', '2x + c = d', 'x', {'x': '(d - c)/2', 'c': 'd - 2x', 'd': None}),
    ('Check 4', 'g = (x - 1)/k', 'x', {'x': 'g k + 1', 'k': '(x - 1)/g', 'g': None}),
    ('Check 5', 'I = p r t', None, {'p': 'I/(r t)', 'r': 'I/(p t)', 't': 'I/(p r)', 'I': None}),
    ('13', 'b/c = a', 'c', {'c': 'b/a', 'b': 'a c', 'a': None}),
    ('14', '2y + k = 6y - k y', 'y', {'y': 'k/(4 - k)', 'k': '(4y)/(1 + y)'}),
    ('15', 'F = 9/5 C + 32', 'C', {'C': '5/9 (F - 32)', 'F': None}),
    ('16', 'w = x/(a - b)', 'x', {'x': 'w(a - b)', 'a': 'x/w + b', 'b': 'a - x/w', 'w': None}),
    ('17', 'A = ((b_1 + b_2) h)/2', 'h', {'h': '(2A)/(b_1 + b_2)', 'b_1': '(2A)/h - b_2', 'b_2': '(2A)/h - b_1', 'A': None}),
    ('18', 'y = m x + b', 'm', {'m': '(y - b)/x', 'x': '(y - b)/m', 'b': 'y - m x', 'y': None}),
    ('19', 'P V = n R T', 'R', {'R': '(P V)/(n T)', 'P': '(n R T)/V', 'V': '(n R T)/P', 'n': '(P V)/(R T)', 'T': '(P V)/(n R)'}),
    ('20', 'A x + B y = C', 'y', {'y': '(C - A x)/B', 'x': '(C - B y)/A', 'A': '(C - B y)/x', 'B': '(C - A x)/y', 'C': 'A x + B y'}),
    ('21', 'y - y_1 = m(x - x_1)', 'm', {'m': '(y - y_1)/(x - x_1)', 'y': 'm(x - x_1) + y_1', 'y_1': 'y - m(x - x_1)', 'x': '(y - y_1)/m + x_1', 'x_1': 'x - (y - y_1)/m'}),
    ('22', '12(m + 3x) = 18(x - 3m)', 'm', {'m': '-(3x)/11', 'x': '-(11m)/3'}),
    ('23', 'V = 1/3 pi r^2 h', 'h', {'h': '(3V)/(pi r^2)', 'r': 'sqrt((3V)/(pi h))', 'V': None}),
    ('24', 'V = 1/3 pi r^2 (h - 1)', 'h', {'h': '(3V)/(pi r^2) + 1', 'r': 'sqrt((3V)/(pi (h - 1)))', 'V': None}),
    ('25', 'y a - y b = c y + c a', 'y', {'y': '(a c)/(a - b - c)', 'a': '(y(b + c))/(y - c)', 'b': '(a y - c y - a c)/y', 'c': '(y(a - b))/(a + y)'}),
    ('26', 'x = (3(y - b))/m', 'y', {'y': '(m x)/3 + b', 'b': 'y - (m x)/3', 'm': '(3(y - b))/x', 'x': None}),
    ('27', 'F = -(G m)/r^2', 'G', {'G': '-(F r^2)/m', 'm': '-(F r^2)/G', 'r': 'sqrt(-(G m)/F)', 'F': None}),
]

EQ = {  # problem number: (prompt, target, {var: solution})
    1: ('a = b + 9', 'b', {'b': 'a - 9', 'a': None}),
    2: ('y = x - 7', 'x', {'x': 'y + 7', 'y': None}),
    3: ('m/n = p', 'm', {'m': 'n p', 'n': 'm/p', 'p': None}),
    4: ('C = pi d', 'd', {'d': 'C/pi', 'C': None}),
    5: ('F = m a', 'a', {'a': 'F/m', 'm': 'F/a', 'F': None}),
    6: ('P = I^2 R', 'R', {'R': 'P/I^2', 'I': 'sqrt(P/R)', 'P': None}),
    7: ('E = m c^2', 'm', {'m': 'E/c^2', 'c': 'sqrt(E/m)', 'E': None}),
    8: ('C = 2 pi r', 'r', {'r': 'C/(2 pi)', 'C': None}),
    9: ('y = 3x + 5', 'x', {'x': '(y - 5)/3', 'y': None}),
    10: ('P = 2a + b', 'a', {'a': '(P - b)/2', 'b': 'P - 2a', 'P': None}),
    11: ('3x + c = d', 'x', {'x': '(d - c)/3', 'c': 'd - 3x', 'd': None}),
    12: ('v = u + a t', 'a', {'a': '(v - u)/t', 't': '(v - u)/a', 'u': 'v - a t', 'v': None}),
    13: ('V = 1/3 B h', 'B', {'B': '(3V)/h', 'h': '(3V)/B', 'V': None}),
    14: ('A = 1/2 d_1 d_2', 'd_1', {'d_1': '(2A)/d_2', 'd_2': '(2A)/d_1', 'A': None}),
    15: ('y = (x - 4)/k', 'x', {'x': 'k y + 4', 'k': '(x - 4)/y', 'y': None}),
    16: ('M = (a b)/c', 'c', {'c': '(a b)/M', 'a': '(M c)/b', 'b': '(M c)/a', 'M': None}),
    17: ('y = 2/3 x + 4', 'x', {'x': '3/2 (y - 4)', 'y': None}),
    18: ('y = (a x + b)/c', 'x', {'x': '(c y - b)/a', 'a': '(c y - b)/x', 'b': 'c y - a x', 'c': '(a x + b)/y', 'y': None}),
    19: ('P = 2(ell + w)', 'w', {'w': 'P/2 - ell', 'ell': 'P/2 - w', 'P': None}),
    20: ('y - 5 = m(x + 2)', 'x', {'x': '(y - 5)/m - 2', 'm': '(y - 5)/(x + 2)', 'y': 'm(x + 2) + 5'}),
    21: ('a_n = a_1 + (n - 1) d', 'n', {'n': '(a_n - a_1)/d + 1', 'd': '(a_n - a_1)/(n - 1)', 'a_1': 'a_n - (n - 1) d', 'a_n': None}),
    22: ('5(a - 2b) = 3c', 'b', {'b': '(5a - 3c)/10', 'a': '(3c)/5 + 2b', 'c': '(5(a - 2b))/3'}),
    23: ('4(p + 2q) = 10(q - p)', 'p', {'p': 'q/7', 'q': '7p'}),
    24: ('6(x - 2y) = 9(x + y)', 'y', {'y': '-x/7', 'x': '-7y'}),
    25: ('p = 3/4 (q - 8)', 'q', {'q': '4/3 p + 8', 'p': None}),
    26: ('A = 1/2 h(a + b)', 'a', {'a': '(2A)/h - b', 'b': '(2A)/h - a', 'h': '(2A)/(a + b)', 'A': None}),
    27: ('S = (n(a + ell))/2', 'ell', {'ell': '(2S)/n - a', 'a': '(2S)/n - ell', 'n': '(2S)/(a + ell)', 'S': None}),
    28: ('a/b = c/d', 'b', {'b': '(a d)/c', 'a': '(b c)/d', 'c': '(a d)/b', 'd': '(b c)/a'}),
    29: ('x/a + y/b = 1', 'y', {'y': 'b - (b x)/a', 'x': 'a - (a y)/b', 'a': '(b x)/(b - y)', 'b': '(a y)/(a - x)'}),
    30: ('a y - b y = c', 'y', {'y': 'c/(a - b)', 'a': 'c/y + b', 'b': 'a - c/y', 'c': 'a y - b y'}),
    31: ('A = P + P r t', 'P', {'P': 'A/(1 + r t)', 'r': '(A - P)/(P t)', 't': '(A - P)/(P r)', 'A': None}),
    32: ('k x = 2x + 5', 'x', {'x': '5/(k - 2)', 'k': '(2x + 5)/x'}),
    33: ('a x + b = c x + d', 'x', {'x': '(d - b)/(a - c)', 'a': '(c x + d - b)/x', 'b': 'c x + d - a x', 'c': '(a x + b - d)/x', 'd': 'a x + b - c x'}),
    34: ('5y + 2k = 9y - k y', 'y', {'y': '(2k)/(4 - k)', 'k': '(4y)/(2 + y)'}),
    35: ('3x - 2a = a x + 7', 'x', {'x': '(2a + 7)/(3 - a)', 'a': '(3x - 7)/(x + 2)'}),
    36: ('m(x + 2) = 5x - n', 'x', {'x': '(2m + n)/(5 - m)', 'm': '(5x - n)/(x + 2)', 'n': '5x - m(x + 2)'}),
    37: ('2(a x - 3) = b x + 4', 'x', {'x': '10/(2a - b)', 'a': '(b x + 10)/(2x)', 'b': '(2a x - 10)/x'}),
    38: ('T = 2(ell w + w h + ell h)', 'h', {'h': '(T - 2 ell w)/(2(ell + w))', 'ell': '(T - 2 w h)/(2(w + h))', 'w': '(T - 2 ell h)/(2(ell + h))', 'T': None}),
    39: ('(x - a)/b = (x + c)/d', 'x', {'x': '(a d + b c)/(d - b)', 'a': 'x - (b(x + c))/d', 'b': '(d(x - a))/(x + c)', 'c': '(d(x - a))/b - x', 'd': '(b(x + c))/(x - a)'}),
    40: ('1/a + 1/b = 1/c', 'c', {'c': '(a b)/(a + b)', 'a': '(b c)/(b - c)', 'b': '(a c)/(a - c)'}),
    41: ('E = 1/2 m v^2 + m g h', 'm', {'m': '(2E)/(v^2 + 2 g h)', 'h': '(2E - m v^2)/(2 m g)', 'g': '(2E - m v^2)/(2 m h)', 'v': 'sqrt((2(E - m g h))/m)', 'E': None}),
    42: ('t = d/(r + s)', 'r', {'r': 'd/t - s', 's': 'd/t - r', 'd': 't(r + s)', 't': None}),
    43: ('y = (2x + 3)/(x - 1)', 'x', {'x': '(y + 3)/(y - 2)', 'y': None}),
    44: ('a = (b + c)/(b - c)', 'b', {'b': '(c(a + 1))/(a - 1)', 'c': '(b(a - 1))/(a + 1)', 'a': None}),
    45: ('y = (a x)/(x + b)', 'x', {'x': '(b y)/(a - y)', 'a': '(y(x + b))/x', 'b': '(x(a - y))/y', 'y': None}),
    46: ('a - b = c', 'b', {'b': 'a - c', 'a': 'b + c', 'c': None}),
    47: ('4x - 3y = 12', 'y', {'y': '(4x - 12)/3', 'x': '(3y + 12)/4'}),
    48: ('A = 4 pi r^2', 'r', {'r': 'sqrt(A/(4 pi))', 'A': None}),
    49: ('V = pi r^2 h', 'r', {'r': 'sqrt(V/(pi h))', 'h': 'V/(pi r^2)', 'V': None}),
    50: ('F = (k q_1 q_2)/r^2', 'r', {'r': 'sqrt((k q_1 q_2)/F)', 'q_1': '(F r^2)/(k q_2)', 'q_2': '(F r^2)/(k q_1)', 'k': '(F r^2)/(q_1 q_2)', 'F': None}),
}

# Worked steps are (equation, note); notes are Typst markup.
STEPS = {
    1: [("a = b + 9", ""), ("a - 9 = b", "subtract 9 from both sides"),
        ("b = a - 9", "rewrite with $b$ on the left")],
    9: [("y = 3x + 5", ""), ("y - 5 = 3x", "subtract 5"),
         ("(y - 5)/3 = x", "divide by 3"), ("x = (y - 5)/3", "rewrite with $x$ on the left")],
    13: [("V = 1/3 B h", ""), ("3V = B h", "multiply both sides by 3"),
         ("(3V)/h = B", "divide by $h$"), ("B = (3V)/h", "rewrite with $B$ on the left")],
    19: [("P = 2(ell + w)", ""), ("P = 2 ell + 2w", "distribute the 2"),
         ("P - 2 ell = 2w", "subtract $2 ell$"), ("(P - 2 ell)/2 = w", "divide by 2"),
         ("w = (P - 2 ell)/2", "same as $P/2 - ell$")],
    25: [("p = 3/4 (q - 8)", ""), ("4p = 3(q - 8)", "multiply both sides by 4"),
         ("4p = 3q - 24", "distribute the 3"), ("4p + 24 = 3q", "add 24"),
         ("(4p + 24)/3 = q", "divide by 3"), ("q = (4p + 24)/3", "same as $4/3 p + 8$")],
    28: [("a/b = c/d", ""), ("a d = c b", "multiply both sides by $b d$"),
         ("(a d)/c = b", "divide by $c$"), ("b = (a d)/c", "rewrite with $b$ on the left")],
    30: [("a y - b y = c", ""), ("y(a - b) = c", "factor out $y$"),
         ("y = c/(a - b)", "divide by $(a - b)$")],
    32: [("k x = 2x + 5", ""), ("k x - 2x = 5", "subtract $2x$"),
         ("x(k - 2) = 5", "factor out $x$"), ("x = 5/(k - 2)", "divide by $(k - 2)$")],
    36: [("m(x + 2) = 5x - n", ""), ("m x + 2m = 5x - n", "distribute the $m$"),
         ("m x + 2m + n = 5x", "add $n$"),
         ("2m + n = 5x - m x", "subtract $m x$ (gather the $x$-terms on the right)"),
         ("2m + n = x(5 - m)", "factor out $x$"),
         ("x = (2m + n)/(5 - m)", "divide by $(5 - m)$")],
    39: [("(x - a)/b = (x + c)/d", ""), ("d(x - a) = b(x + c)", "multiply both sides by $b d$"),
         ("d x - a d = b x + b c", "distribute"), ("d x - b x = a d + b c", "subtract $b x$, add $a d$"),
         ("x(d - b) = a d + b c", "factor out $x$"), ("x = (a d + b c)/(d - b)", "divide by $(d - b)$")],
    42: [("t = d/(r + s)", ""), ("t(r + s) = d", "multiply both sides by $(r + s)$"),
         ("t r + t s = d", "distribute the $t$"), ("t r = d - t s", "subtract $t s$"),
         ("r = (d - t s)/t", "divide by $t$; same as $d/t - s$")],
    46: [("a - b = c", ""), ("a = c + b", "add $b$ to both sides: now $b$ is positive"),
        ("a - c = b", "subtract $c$"), ("b = a - c", "rewrite with $b$ on the left")],
    47: [("4x - 3y = 12", ""), ("4x = 12 + 3y", "add $3y$ to both sides: now $3y$ is positive"),
         ("4x - 12 = 3y", "subtract 12"), ("(4x - 12)/3 = y", "divide by 3"),
         ("y = (4x - 12)/3", "rewrite with $y$ on the left")],
    48: [("A = 4 pi r^2", ""), ("A/(4 pi) = r^2", "divide by $4 pi$"),
         ("sqrt(A/(4 pi)) = r", "take the positive square root"),
         ("r = sqrt(A/(4 pi))", "rewrite with $r$ on the left")],
    49: [("V = pi r^2 h", ""), ("V/(pi h) = r^2", "divide by $pi h$"),
         ("sqrt(V/(pi h)) = r", "take the positive square root"),
         ("r = sqrt(V/(pi h))", "rewrite with $r$ on the left")],
    50: [("F = (k q_1 q_2)/r^2", ""), ("F r^2 = k q_1 q_2", "multiply both sides by $r^2$"),
         ("r^2 = (k q_1 q_2)/F", "divide by $F$"),
         ("r = sqrt((k q_1 q_2)/F)", "take the positive square root")],
}

# Special Case A: the other way through, and the mistake it invites.
ALT = {
    46: [("a - b = c", ""), ("-b = c - a", "subtract $a$"),
        ("b = a - c", "multiply (or divide) both sides by $-1$")],
    47: [("4x - 3y = 12", ""), ("-3y = 12 - 4x", "subtract $4x$"),
         ("y = (12 - 4x)/(-3)", "divide by $-3$, not by 3"),
         ("y = (4x - 12)/3", "the negative flips both signs on top")],
}
PITFALL = {
    46: "Writing $b = c - a$. Check with numbers: if $a = 10$ and $c = 3$, then $10 - b = 3$ gives $b = 7$, but $c - a = -7$.",
    47: "From $-3y = 12 - 4x$, dividing by 3 instead of $-3$ gives $y = (12 - 4x)/3$, which has every sign wrong.",
}
NOTICE = {
    46: "Before moving anything, look at the sign *in front of* the unknown: here it is $-b$, not $b$.",
    47: "The $y$ term is $-3y$. The coefficient of $y$ is $-3$, not 3.",
}

# ------------------------------------------------------------------
# Verification
# ------------------------------------------------------------------
def check(prompt, sols):
    syms = syms_of(prompt)
    assert set(syms) == set(sols), (prompt, set(syms), set(sols))
    for var, sol in sols.items():
        if sol is None:  # "given": prompt must already be  var = (expr without var)
            l, r = (to_sympy(x) for x in prompt.split("="))
            assert (l == syms[var] and syms[var] not in r.free_symbols) or \
                   (r == syms[var] and syms[var] not in l.free_symbols), (prompt, var)
            continue
        assert syms[var] not in to_sympy(sol).free_symbols, (prompt, var, sol)
        holds(prompt, prompt, var, sol)

def check_steps(n, steps):
    p, t, sols = EQ[n]
    assert steps[0][0] == p, n
    last = steps[-1][0]
    assert last.split("=")[0].strip() == t, (n, last)  # ends "target = ..."
    assert syms_of(p)[t] not in to_sympy(last.split("=")[1]).free_symbols, (n, last)
    for eq, _ in steps:
        holds(eq, p, t, sols[t])

random.seed(4)
for _, p, _, s in SOURCE:
    check(p, s)
for n, (p, t, s) in EQ.items():
    check(p, s)
    assert s[t] is not None
seq = [n for ty in TYPES for n in ty["probs"]]
assert seq == list(range(1, 51)), "every problem in exactly one type, numbered in order"
for ty in TYPES:
    assert set(ty["worked"]) <= set(ty["probs"]), ty["key"]
    for n in ty["worked"]:
        check_steps(n, STEPS[n])
for n, st in ALT.items():
    check_steps(n, st)
print("all", sum(len(s) for *_, s in SOURCE) + sum(len(s) for *_, s in EQ.values()),
      "solutions and", sum(map(len, STEPS.values())) + sum(map(len, ALT.values())),
      "worked steps verified")

# ------------------------------------------------------------------
# JSON bank
# ------------------------------------------------------------------
TYPE_OF = {n: ty for ty in TYPES for n in ty["probs"]}

def order(sols, target=None):
    ks = list(sols)
    if target in ks:
        ks.remove(target); ks.insert(0, target)
    return ks

bank = {
    "_meta": {
        "topic": "Lesson 1-4: Literal Equations and Formulas (sequenced by type)",
        "prompt_format": "Typst math markup, without delimiters. Drop into a worksheet as: $display(<prompt>)$",
        "solutions_format": "{variable: solution in Typst math}; null means the equation is already solved for that variable. Square-root solutions take the positive root (lengths, speeds, etc.).",
        "steps_format": "[[equation, note], ...]; the first equation is the prompt, the last is target = answer. Notes are Typst markup.",
        "generator": "gen_sequence.py (every solution and step checked numerically with sympy)",
    },
    "types": [{"key": t["key"], "label": label(t), "title": t["title"], "look_for": t["look"],
               "the_move": t["move"], "problems": t["probs"], "worked": t["worked"]} for t in TYPES],
    "source": [{"id": f"src-{i+1:02d}", "book_item": lbl, "prompt": p, "book_target": t,
                "solutions": s} for i, (lbl, p, t, s) in enumerate(SOURCE)],
    "problems": [dict({"number": n, "type": TYPE_OF[n]["key"], "prompt": EQ[n][0], "target": EQ[n][1],
                       "answer": f"{EQ[n][1]} = {EQ[n][2][EQ[n][1]]}", "solutions": EQ[n][2]},
                      **({"steps": STEPS[n]} if n in STEPS else {}),
                      **({"alternate_steps": ALT[n]} if n in ALT else {}))
                 for n in seq],
}
(OUT / "lesson_1-4_literal_seq_bank.json").write_text(json.dumps(bank, indent=1))

# ------------------------------------------------------------------
# Typst
# ------------------------------------------------------------------
def write(name, s):
    (OUT / name).write_text(s)

def prompt_tx(n):
    p, t, _ = EQ[n]
    return f"$display({p})$; #h(0.3em) ${t}$"

def answer_tx(n):
    p, t, s = EQ[n]
    return f"$display({t} = {s[t]})$"

STEPS_DEF = """
// Worked steps: rows of (left side, =, right side, note).
#let steps(note-size: 0.85em, last: 1fr, ..rows) = grid(
  columns: (auto, auto, auto, last),
  column-gutter: 0.45em,
  row-gutter: 1.15em,
  align: (right + horizon, center + horizon, left + horizon, left + horizon),
  ..rows.pos().map(((l, r, n)) => (l, $=$, r,
    text(size: note-size, fill: luma(90), style: "italic", n))).flatten()
)
"""

def steps_tx(st, indent="  ", args=""):
    rows = []
    for eq, note in st:
        l, r = (x.strip() for x in eq.split("="))
        rows.append(f"{indent}  ([$display({l})$], [$display({r})$], [{note}]),")
    return f"{indent}#steps({args}\n" + "\n".join(rows) + f"\n{indent})\n"

# ---- groups: the printed order of the worksheet, key, and slides ----
TYPE = {t["key"]: t for t in TYPES}
LAY = mp.layout(GROUPS, {t["key"]: len(t["probs"]) for t in TYPES})
PLAIN = LAY == mp.default_layout({t["key"]: 1 for t in TYPES})
_rng = random.Random(_a.seed)
PRINT = []                       # [(group, [lesson problem numbers in print order])]
for _g in LAY:
    _nums = [n for k in _g["types"] for n in TYPE[k]["probs"]]
    if len(_g["types"]) > 1:
        _rng.shuffle(_nums)
    PRINT.append((_g, _nums))

def group_hint(g):
    if len(g["types"]) == 1:
        ty = TYPE[g["types"][0]]
        return f'{ty["look"]} {ty["move"]}'
    return "Includes: " + "; ".join(f'{label(TYPE[k])}, {TYPE[k]["title"]}' for k in g["types"]) + "."

def special_only(g):
    return all(TYPE[k].get("special") for k in g["types"])

# ---- worksheet and key ----
def ws(key):
    title = "Literal Equations by Type" + (" — Answer Key" if key else "")
    s = head + vars_(title, class_name=CLASS) + """#let type-head(heading, hint) = block(sticky: true, above: 1.1em, below: 0.7em)[
  #text(weight: "bold", size: 13pt)[#heading] \\
  #text(size: 10.5pt, style: "italic")[#hint]
]

#first-page-header(class-name, worksheet-title, version: version)
#v(-2.2em)
Solve each equation for the indicated variable. The problems are grouped by the kind of first move they need""" + (", from simplest to most involved" if PLAIN else "") + """.
#v(0.2em)

"""
    i, prev_special = 0, False
    for g, nums in PRINT:
        if special_only(g) and not prev_special:
            s += "#v(0.6em)\n#align(center, text(weight: \"bold\", size: 14pt)[Special Cases])\n"
        prev_special = special_only(g)
        space = max(TYPE[k]["space"] for k in g["types"])
        s += f'#type-head([{mp.esc(mp.heading(g))}], [{group_hint(g)}])\n'
        s += f'#grid(\n  columns: (1fr, 1fr),\n  rows: {space}in,\n  column-gutter: 1em,\n'
        for n in nums:
            i += 1
            a = f"\n    #v(0.3em) #h(1fr) #text(fill: red)[{answer_tx(n)}] #h(0.4em)" if key else ""
            s += f"  question(renum: {i}, space-below: 0em)[\n    {prompt_tx(n)}{a}\n  ],\n"
        s += ")\n\n"
    return s

write("lesson_1-4_literal_seq_worksheet.typ", ws(False))
write("lesson_1-4_literal_seq_key.typ", ws(True))

# ---- slides ----
s = slhead + vars_("Literal Equations by Type", class_name=CLASS) + STEPS_DEF + """
#let slide(n, prob, answer: none) = {
  align(left)[#text(size: 30pt, weight: "bold")[Problem #n]]
  v(1.5em)
  align(center)[
    #text(size: 34pt)[#prob]
    #if answer != none [
      #v(0.8em)
      #text(fill: red, size: 34pt)[#answer]
    ]
  ]
}

#let worked-slide(n, prob, body) = {
  grid(columns: (1fr, auto),
    text(size: 30pt, weight: "bold")[Problem #n #h(0.4em) #text(size: 20pt, weight: "regular")[worked out]],
    text(size: 24pt)[#prob])
  v(0.6em)
  set text(size: 27pt)
  align(center + horizon, block(height: 1fr, body))
}

#let type-slide(lbl, title, look, move) = align(horizon)[
  #text(size: 24pt, fill: luma(90))[#lbl]
  #v(-0.3em)
  #text(size: 40pt, weight: "bold")[#title]
  #v(0.6em)
  #text(size: 24pt)[*Look for:* #look]
  #v(0.2em)
  #text(size: 24pt)[*The move:* #move]
]

#let group-slide(heading, items) = align(horizon)[
  #text(size: 40pt, weight: "bold")[#heading]
  #v(0.5em)
  #for it in items [
    #text(size: 20pt)[*#it.at(0): #it.at(1)* #h(0.4em) _Look for:_ #it.at(2) #h(0.4em) _The move:_ #it.at(3)]
    #v(0.35em)
  ]
]

#align(center + horizon)[
  #text(size: 44pt, weight: "bold")[Literal Equations by Type]
  #v(0.4em)
  #text(size: 28pt)[Lesson 1-4]
  #v(0.2em)
  #text(size: 24pt)[Solve each equation for the indicated variable.]
]
"""
i = 0
for g, nums in PRINT:
    if len(g["types"]) == 1:
        ty = TYPE[g["types"][0]]
        s += (f'#pagebreak()\n#type-slide([{label(ty)}], [{mp.esc(g["name"]) or ty["title"]}], '
              f'[{ty["look"]}], [{ty["move"]}])\n')
    else:
        items = ", ".join(f'([{label(TYPE[k])}], [{TYPE[k]["title"]}], [{TYPE[k]["look"]}], [{TYPE[k]["move"]}])'
                          for k in g["types"])
        s += f'#pagebreak()\n#group-slide([{mp.esc(mp.heading(g))}], ({items}))\n'
    for n in nums:
        i += 1
        pr = f"$display({EQ[n][0]})$; #h(0.5em) ${EQ[n][1]}$"
        s += f"#pagebreak()\n#slide({i}, [{pr}])\n#pagebreak()\n"
        if n in STEPS:
            s += f"#worked-slide({i}, [{pr}], [\n{steps_tx(STEPS[n], args='last: auto, note-size: 0.7em,')}])\n"
        else:
            s += f"#slide({i}, [{pr}], answer: [{answer_tx(n)}])\n"
    s += "\n"
write("lesson_1-4_literal_seq_slides.typ", s)

# ---- worked-steps guide ----
g = """#set page(paper: "us-letter", margin: (x: 0.75in, y: 0.7in), numbering: "1")
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: false)
""" + STEPS_DEF + """
#let type-sec(lbl, title, look, move, probs) = block(sticky: true, below: 0.9em)[
  #text(size: 14pt, weight: "bold")[#lbl: #title]
  #v(-0.3em)
  #line(length: 100%, stroke: 0.5pt)
  #v(-0.2em)
  *Look for:* #look \\
  *The move:* #move \\
  *Worksheet problems:* #probs
]

#let example(n, prob, body) = block(breakable: false, inset: (left: 1.2em), below: 1.4em)[
  *Problem #n.* #h(0.4em) #prob
  #v(0.2em)
  #pad(left: 1em, body)
]

#let callout(title, body) = block(breakable: false, width: 100%, inset: 0.6em,
  stroke: (left: 2pt + luma(120)), fill: luma(245), below: 1.2em)[*#title* #h(0.3em) #body]

#align(center)[
  #text(size: 17pt, weight: "bold")[Literal Equations: A Strategy for Each Type]
  #v(-0.4em)
  #text(size: 12pt)[Lesson 1-4 #h(0.6em) Worked Examples]
]
#v(0.5em)

Every literal equation is solved the same way an ordinary equation is: undo what has been done to the unknown, in reverse order, doing the same thing to both sides. The types below are ordered so each one adds one new move to the moves before it. Work out what the *first* move is, and the rest follows. Problem numbers refer to the Literal Equations by Type worksheet. An answer in a different but equivalent form (for example, $(P - 2 ell)/2$ instead of $P/2 - ell$) is still correct.
#v(0.6em)

"""
for ty in TYPES:
    if ty["key"] == "A":
        g += "#pagebreak()\n#align(center, text(size: 16pt, weight: \"bold\")[Special Cases])\n#v(0.3em)\n"
    probs = ", ".join(str(n) for n in ty["probs"])
    g += f'#type-sec([{label(ty)}], [{ty["title"]}], [{ty["look"]}], [{ty["move"]}], [{probs}])\n'
    for n in ty["worked"]:
        pr = f"$display({EQ[n][0]})$; #h(0.3em) solve for ${EQ[n][1]}$"
        g += f"#example({n}, [{pr}], [\n"
        if n in NOTICE:
            g += f"  #callout([Notice:], [{NOTICE[n]}])\n"
        g += steps_tx(STEPS[n])
        if n in ALT:
            g += f"  #v(0.6em)\n  _Or, leaving the negative term where it is:_\n  #v(0.3em)\n{steps_tx(ALT[n])}"
            g += f"  #v(0.6em)\n  #callout([Watch out:], [{PITFALL[n]}])\n"
        g += "])\n"
    g += "\n"
write("lesson_1-4_literal_seq_guide.typ", g)

# ---- all-solutions reference ----
def sol_lines(sols, target):
    out = []
    for v in order(sols, target):
        if sols[v] is None:
            continue
        out.append(f"#box[${v} = display({sols[v]})$" + (" #text(size: 9pt)[(target)]" if v == target else "") + "]")
    return " #h(1.4em) ".join(out)

r = """#set page(paper: "us-letter", margin: (x: 0.75in, y: 0.7in))
#set text(size: 11pt)
#set par(justify: false)
#set text(top-edge: "bounds", bottom-edge: "bounds")

#align(center)[
  #text(size: 16pt, weight: "bold")[Lesson 1-4: Literal Equations and Formulas]
  #v(-0.4em)
  #text(size: 12pt)[Every Equation Solved for Every Variable]
]
#v(0.6em)

#let eq(n, prompt, sols) = block(spacing: 1.3em, breakable: false)[
  #strong[#n] #h(0.6em) #prompt \\
  #pad(left: 1.2em, sols)
]

#text(size: 9.5pt, style: "italic")[Square-root solutions give the positive root, since these variables stand for lengths and other positive quantities. A variable the equation is already solved for is not listed again. "(book)" marks the variable the textbook asks for; "(target)" marks the one asked on the worksheet.]

== Part 1: Equations from the Textbook
#v(0.4em)
#columns(2, gutter: 2em)[
"""
for lbl, p, t, sols in SOURCE:
    r += f"  #eq([{lbl}.], [$display({p})$], [{sol_lines(sols, t).replace('(target)', '(book)')}])\n"
r += "]\n\n#pagebreak()\n== Part 2: Worksheet Equations by Type\n#v(0.4em)\n#columns(2, gutter: 2em)[\n"
for ty in TYPES:
    r += f'  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[{label(ty)}: {ty["title"]}]]\n'
    for n in ty["probs"]:
        p, t, sols = EQ[n]
        r += f"  #eq([{n}.], [$display({p})$], [{sol_lines(sols, t)}])\n"
r += "]\n"
write("lesson_1-4_literal_seq_all_solutions.typ", r)
