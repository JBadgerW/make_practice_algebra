"""Functions (Advanced Math), from the 2025-26 midterm: evaluating,
substituting an expression, combining two functions, the domain, and which
relations are functions.

A problem's prompt is its parts in Typst math, separated by ";": the
functions it defines, then what to find.

    "f(x) = x^2 + 3 x - 4; f(-4), f(3)"
    "f(x) = x^2 + 3 x - 4; f(x + 2)"
    "f(x) = 3 x^2; g(x) = -x + 5; (f g)(2)"       (f/g)(2), (f circle.small g)(2)
    "f(x) = sqrt(x - 3)/(x^2 - 7 x + 10); domain"
    "{(1, 2), (3, 4), ...}; {...}; {...}; {...}"   Type 5: which relations are functions

The key's answer names each thing found: "f(-4) = 0, f(3) = 14",
"f(x + 2) = x^2 + 7 x + 6", "(f g)(2) = 36"; a domain is its conditions,
"x >= 3, x != 5"; Type 5's is the letters of the functions, "A, C".

Fixed from the midterm: f(x + n) was computed as f(x - 1); the domain of
sqrt(x - s) was written x >= -s, and a zero of the denominator outside the
domain was still listed.

check() works the prompt out again with sympy and compares: each answer's
value at random points (so its form doesn't matter, only that it is
multiplied out), a domain as a set of numbers, and Type 5 by reading the
ordered pairs back out of the prompt.
"""
import re
import sympy as sp
from sympy.calculus.util import continuous_domain
from .. import gen
from ..gen import need, signed
from ..check import to_sympy, same_value
from ..typmath import tx, single, fr, dfrac, text as plain

NAME = FAMILY = "adv_functions"
FIXED = False
TITLE = "Functions"
INSTRUCTIONS = ""
COURSES = {"Advanced Math": "Additional Practice"}

TYPES = [
    dict(key="1", title="Evaluating a Function", instructions="Evaluate.",
         look="f(x) is a formula, and you're asked for f of a number.",
         move="Replace every x with the number, in parentheses. Then follow the order of operations."),
    dict(key="2", title="Substituting an Expression", instructions="Find and simplify.",
         look="f of an expression, like f(x + 2) or f(3 x).",
         move="Replace every x with the whole expression, in parentheses. Multiply out and combine like terms."),
    dict(key="3", title="Combining Functions", instructions="Evaluate.",
         look="(f g)(2), (f/g)(2), or (f ∘ g)(2).",
         move="(f g)(2) = f(2) g(2) and (f/g)(2) = f(2)/g(2). For (f ∘ g)(2), find g(2) first, then f of that."),
    dict(key="4", title="The Domain", instructions="Find the domain of each function.",
         look="A square root, or a fraction with x in the denominator.",
         move="What's under a square root can't be negative: solve inside ≥ 0. A denominator can't be 0: "
              "solve denominator = 0 and leave those numbers out (if they're in the domain at all).",
         space="1.25in"),
    dict(key="5", title="Which Relations Are Functions?", instructions="Which of these relations are functions?",
         look="Sets of ordered pairs.",
         move="A relation is a function when no x is paired with two different y's. Look for a repeated first number.",
         width="full", space="0.5in"),
]
T = gen.Types(TYPES, INSTRUCTIONS, space="1in")
TYPE, KEYS, ENTRIES, ENTRY = T.TYPE, T.KEYS, T.ENTRIES, T.ENTRY
label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
X = sp.Symbol("x")
COMPOSE = "circle.small"

def initial_seen():
    return set()

def seen_key(p):
    return (NAME, p["type"], p["prompt"])

# ------------------------------------------------------------------
# Reading a prompt
# ------------------------------------------------------------------
DEF = re.compile(r"^([a-z])\(x\)\s*=\s*(.+)$")
APPLY = re.compile(r"^([a-z])\((.+)\)$")
COMBINE = re.compile(rf"^\(([a-z])\s*(/|{re.escape(COMPOSE)}|\s)\s*([a-z])\)\((.+)\)$")

def split_top(s, sep):
    """s split at sep where it's outside parentheses and braces."""
    out, depth, cur = [], 0, ""
    for ch in s:
        depth += {"(": 1, "{": 1, ")": -1, "}": -1}.get(ch, 0)
        if ch == sep and depth == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    return out + [cur.strip()]

def read(prompt):
    """({name: sympy expression in x}, [the things to find])."""
    parts = split_top(prompt, ";")
    defs = {}
    for part in parts[:-1]:
        m = DEF.match(part)
        if not m:
            raise ValueError(f"write each function like f(x) = x^2 + 3: not {part!r}")
        defs[m.group(1)] = to_sympy(m.group(2))
    return defs, split_top(parts[-1], ",")

def value(defs, ask):
    """What one request asks for, as a sympy expression."""
    m = COMBINE.match(ask)
    if m:
        f, op, g, arg = defs[m.group(1)], m.group(2), defs[m.group(3)], to_sympy(m.group(4))
        if op == COMPOSE:
            return f.subs(X, g.subs(X, arg))
        fv, gv = f.subs(X, arg), g.subs(X, arg)
        if op == "/":
            if gv == 0:
                raise ValueError("g is 0 there")
            return fv / gv
        return fv * gv
    m = APPLY.match(ask)
    if not m or m.group(1) not in defs:
        raise ValueError(f"can't read {ask!r}: write f(3), f(x + 2), (f g)(2), (f/g)(2), or (f {COMPOSE} g)(2)")
    v = defs[m.group(1)].subs(X, to_sympy(m.group(2)))
    if v.has(sp.zoo, sp.nan):
        raise ValueError(f"{ask} isn't defined")
    return sp.expand(v)

def domain_of(f):
    return continuous_domain(f, X, sp.S.Reals)

# ------------------------------------------------------------------
# Writing a domain: "x >= 3, x != 5"
# ------------------------------------------------------------------
def domain_text(s):
    """A domain as the key writes it: an interval from a, or all reals, less some points."""
    if s == sp.S.Reals:
        return "all real numbers"
    pieces = list(s.args) if isinstance(s, sp.Union) else [s]
    lo = pieces[0].start if isinstance(pieces[0], sp.Interval) else None
    conds = []
    if lo is not None and lo != -sp.oo:
        conds.append(f"x {'>' if pieces[0].left_open else '>='} {tx(lo)}")
    full = (sp.Interval(lo, sp.oo, pieces[0].left_open) if lo not in (None, -sp.oo) else sp.S.Reals)
    holes = full - s
    if not isinstance(holes, sp.FiniteSet) or any(isinstance(pc, sp.Interval) and pc.end != sp.oo and
                                                   not pc.right_open for pc in pieces):
        raise ValueError("a domain this bank doesn't write")
    conds += [f"x != {tx(h)}" for h in sorted(holes)]
    return ", ".join(conds)

COND = re.compile(r"^x\s*(>=|<=|>|<|!=)\s*(.+)$")

def domain_read(text):
    t = " ".join(text.replace("≥", ">=").replace("≠", "!=").replace("≤", "<=").split())
    if t in ("all real numbers", "all reals"):
        return sp.S.Reals
    s = sp.S.Reals
    for c in split_top(t, ","):
        m = COND.match(c)
        if not m:
            raise ValueError(f"write each condition like x >= 3 or x != 5: not {c!r}")
        op, v = m.group(1), to_sympy(m.group(2))
        s &= {">=": sp.Interval(v, sp.oo), ">": sp.Interval.open(v, sp.oo), "<=": sp.Interval(-sp.oo, v),
              "<": sp.Interval.open(-sp.oo, v), "!=": sp.S.Reals - sp.FiniteSet(v)}[op]
    return s

# ------------------------------------------------------------------
# Type 5: relations
# ------------------------------------------------------------------
PAIR = re.compile(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)")

def pairs(relation):
    return [(int(a), int(b)) for a, b in PAIR.findall(relation)]

def is_function(ps):
    seen = {}
    return all(seen.setdefault(a, b) == b for a, b in ps)

def relations_answer(prompt):
    rels = split_top(prompt, ";")
    if len(rels) < 2 or not all(r.startswith("{") and pairs(r) for r in rels):
        raise ValueError("write the relations like {(1, 2), (3, 4)}; {(1, 2), (1, 5)}")
    letters = [chr(65 + i) for i, rel in enumerate(rels) if is_function(pairs(rel))]
    return ", ".join(letters) if letters else "none"

# ------------------------------------------------------------------
# Solving a prompt (the key's answer)
# ------------------------------------------------------------------
def answer_of(prompt):
    if prompt.lstrip().startswith("{"):
        return relations_answer(prompt)
    defs, asks = read(prompt)
    if asks == ["domain"]:
        return domain_text(domain_of(defs["f"]))
    return ", ".join(f"{a} = {single(value(defs, a))}" for a in asks)

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def poly(*cs):
    """Coefficients, highest power first, as Typst: poly(1, 3, -4) = "x^2 + 3 x - 4"."""
    return tx(sum(c * X ** (len(cs) - 1 - i) for i, c in enumerate(cs)), "x")

def lin(r):
    """x + n or x - n, as an argument."""
    return tx(X + signed(r, 1, 9))

def t1_monic(r):                              # the midterm: f(x) = x^2 + b x + c; f(A), f(B)
    a1, a2 = r.sample([n for n in range(-12, 13) if n], 2)
    return f"f(x) = {poly(1, signed(r, 1, 12), signed(r, 1, 12))}; f({a1}), f({a2})"

def t1_quadratic(r):
    a1, a2 = r.sample([n for n in range(-6, 7) if n], 2)
    return f"f(x) = {poly(signed(r, 2, 5), signed(r, 1, 9), signed(r, 1, 9))}; f({a1}), f({a2})"

def t1_rational(r):
    b, c = signed(r, 1, 9), signed(r, 1, 9)
    a1, a2 = r.sample([n for n in range(-6, 7) if n != c], 2)
    return f"f(x) = {fr(poly(r.randint(1, 4), b), poly(1, -c))}; f({a1}), f({a2})"

def quad(r):
    return poly(r.choice((1, -1)), signed(r, 1, 9), signed(r, 1, 9))

def t2_plus(r):                               # the midterm: f(x + n)
    return f"f(x) = {quad(r)}; f({tx(X + r.randint(1, 9))})"

def t2_minus(r):
    return f"f(x) = {quad(r)}; f({tx(X - r.randint(1, 9))})"

def t2_times(r):
    return f"f(x) = {quad(r)}; f({r.randint(2, 5)} x)"

def two(r):
    """The midterm's f(x) = a x^2 and g(x) = ±x + b, and v, not g's zero."""
    a, b, c = r.randint(1, 6), signed(r, 1, 12), r.choice((1, -1))
    v = gen.except_(r, -10, 10, -c * b)
    return f"f(x) = {poly(a, 0, 0)}; g(x) = {poly(c, b)}", v

def t3_product(r):
    fg, v = two(r)
    return f"{fg}; (f g)({v})"

def t3_quotient(r):
    fg, v = two(r)
    return f"{fg}; (f/g)({v})"

def t3_composition(r):
    fg, v = two(r)
    return f"{fg}; (f {COMPOSE} g)({v})"

def t4_root_over_quadratic(r):                # the midterm: sqrt(x - s)/((x - n1)(x - n2))
    s, n1, n2 = signed(r, 1, 9), signed(r, 1, 9), signed(r, 1, 9)
    need(n1 != n2 and max(n1, n2) > s)                    # at least one zero to leave out
    return f"f(x) = {fr(f'sqrt({lin_text(s)})', poly(1, -(n1 + n2), n1 * n2))}; domain"

def lin_text(s):
    return tx(X - s)

def t4_over_quadratic(r):
    n1, n2 = r.sample([n for n in range(-9, 10) if n], 2)
    return f"f(x) = {fr(str(signed(r, 1, 9)), poly(1, -(n1 + n2), n1 * n2))}; domain"

def t4_root_over_linear(r):
    s, n = signed(r, 1, 9), signed(r, 1, 9)
    need(n > s)
    return f"f(x) = {fr(f'sqrt({lin_text(s)})', lin_text(n))}; domain"

def relation(r, function):
    xs = r.sample(range(-9, 10), 4) if function else None
    if function:
        ps = [(a, r.randint(-9, 9)) for a in xs]
    else:
        xs = r.sample(range(-9, 10), 3)
        ps = [(a, r.randint(-9, 9)) for a in xs]
        a, b = ps[r.randrange(3)]
        ps.append((a, gen.except_(r, -9, 9, b)))          # an x paired with a second y
        r.shuffle(ps)
    return "{" + ", ".join(f"({a}, {b})" for a, b in ps) + "}"

def t5_relations(r):                          # the midterm: which of four relations are functions
    kinds = [r.random() < 0.5 for _ in range(4)]
    need(any(kinds) and not all(kinds))
    return "; ".join(relation(r, k) for k in kinds)

TEMPLATES = {
    "1": [t1_monic, t1_quadratic, t1_rational],
    "2": [t2_plus, t2_minus, t2_times],
    "3": [t3_product, t3_quotient, t3_composition],
    "4": [t4_root_over_quadratic, t4_over_quadratic, t4_root_over_linear],
    "5": [t5_relations],
}

def draw(entry, r, tpl):
    prompt = TEMPLATES[entry][tpl](r)
    try:
        answer = answer_of(prompt)
    except ValueError:
        raise gen.Redraw from None
    return dict(prompt=prompt, answer=answer)

# ------------------------------------------------------------------
# Checking
# ------------------------------------------------------------------
def check(p):
    try:
        prompt, answer = p["prompt"], p["answer"]
        if p["type"] == "5":
            got = {a.strip() for a in answer.split(",")} - {"none"}
            want = {chr(65 + i) for i, rel in enumerate(split_top(prompt, ";")) if is_function(pairs(rel))}
            return "checked" if got == want else "failed"
        defs, asks = read(prompt)
        if asks == ["domain"]:
            same = domain_read(answer).symmetric_difference(domain_of(defs["f"])) == sp.S.EmptySet
            return "checked" if same else "failed"
        items = [a.partition("=") for a in split_top(answer, ",")]
        if [" ".join(lhs.split()) for lhs, _, _ in items] != [" ".join(a.split()) for a in asks]:
            return "failed"
        for (lhs, _, rhs), ask in zip(items, asks):
            if "(" in rhs.replace("sqrt(", "") or not same_value(rhs, tx(value(defs, ask))):
                return "failed"                       # wrong, or not multiplied out
        return "checked"
    except Exception:
        return "unchecked"

generate = gen.generator(NAME, draw, check, seen_key, lambda e: len(TEMPLATES[e]))

# ------------------------------------------------------------------
# Showing
# ------------------------------------------------------------------
def math(t):
    return f"${dfrac(t)}$"

def typst(p, gap="0.3em"):
    prompt = p["prompt"]
    if p["type"] == "5":
        items = ", ".join(f"[{math(rel)}]" for rel in split_top(prompt, ";"))
        return f"#choices(arrangement: \"grid\", {items})"
    parts = split_top(prompt, ";")
    defs = ", ".join(math(d) for d in parts[:-1])
    asks = parts[-1]
    if asks == "domain":
        return f"{defs}"
    return f"{defs}; #h({gap}) " + ", ".join(math(a) for a in split_top(asks, ","))

def answer_typst(p):
    if p["type"] == "5":
        return p["answer"]
    return ", ".join(math(a) for a in split_top(p["answer"], ","))

def text(p):
    if p["type"] == "5":
        return "   ".join(f"{chr(65 + i)}. {rel}" for i, rel in enumerate(split_top(p["prompt"], ";")))
    return plain(p["prompt"].replace(COMPOSE, "∘"))

def answer_text(p):
    return plain(p["answer"])

def height(p):
    return 0.6 if p["type"] == "5" else 0.4

# ------------------------------------------------------------------
# Editing: the prompt as stored, parts separated by ";"
# ------------------------------------------------------------------
def clean(t):
    return " ".join(t.replace("−", "-").replace("∘", COMPOSE).split())

def edit_text(p):
    return p["prompt"]

def from_edit(t, old):
    t = clean(t)
    try:
        answer = answer_of(t)
    except Exception as e:
        raise ValueError(f"{e}; write it like f(x) = x^2 + 3 x - 4; f(-4), f(3)") from None
    new = dict(old, prompt=t, answer=answer, source="edited")
    return new, check(new)

def answer_edit_text(p):
    return p["answer"]

def with_answer(p, t):
    new = dict(p, answer=clean(t))
    return new, check(new)

def selftest(n, seed):
    return gen.selftest(NAME, generate, KEYS, lambda k: label(TYPE[k]), n, seed)
