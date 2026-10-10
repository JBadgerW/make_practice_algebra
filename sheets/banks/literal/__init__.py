"""Literal equations: solve a formula for a given variable.

Each type has a set of templates that build a fresh equation from random
letters and numbers, plus a pool of real formulas sorted by type. Templates
only write the *equation*: the answer is solved by sympy, written out in
classroom form by answers.fmt(), and checked numerically before it is used.

As a bank, every type has two entries: KEY draws made-up equations from the
templates ("letters"), and KEYf draws from the real formulas ("formulas").
"""
import functools, json, random, re
from ... import ROOT
from .types import TYPES, TYPE, KEYS, label
from .templates import D, Redraw, need, TEMPLATES
from .formulas import FORMULAS
from .answers import solve, fmt, make

@functools.lru_cache(maxsize=None)
def _lesson_prompts():
    try:
        bank = json.loads((ROOT / "banks" / "lesson_1-4.json").read_text())   # written by gen_sequence.py
        return frozenset((p["prompt"], p["target"]) for p in bank["problems"])
    except (OSError, ValueError, KeyError):
        return frozenset()

def original_prompts():
    return set(_lesson_prompts())

def draw(typ, rng, style, seen, tries=400):
    pool = [f for f in FORMULAS if f[2] == typ and (f[0], f[1]) not in seen]
    use_formula = pool and (style == "formulas" or (style == "mixed" and rng.random() < 0.3))
    if use_formula:
        p, t, _ = rng.choice(pool)
        prob = make(p, t, typ)
    else:
        for _ in range(tries):
            d = D(rng)
            try:
                p, t = rng.choice(TEMPLATES[typ])(d)
                if rng.random() < 0.35:              # write the sides the other way round
                    l, r = p.split(" = ")
                    p = f"{r} = {l}"
                if (p, t) in seen:
                    continue
                prob = make(p, t, typ)
                break
            except Redraw:
                continue
        else:
            raise RuntimeError(f"could not draw a Type {typ} problem; check its templates")
    seen.add((prob["prompt"], prob["target"]))
    prob["source"] = "formula" if use_formula else "template"
    return prob

def selftest(n, seed):
    random.seed(seed)
    rng, bad = random.Random(seed), 0
    for typ in KEYS:
        seen = set()
        for _ in range(n):
            draw(typ, rng, "letters", seen)
        print(f"{label(TYPE[typ]):16} {n} drawn, all verified")
    for p, t, typ in FORMULAS:
        try:
            make(p, t, typ)
        except Redraw:
            bad += 1
            print("formula failed:", p, t, typ)
    print(f"{len(FORMULAS) - bad}/{len(FORMULAS)} formulas verified")
    return bad == 0


# ------------------------------------------------------------------
# The bank interface (see sheets/banks/__init__.py)
# ------------------------------------------------------------------
NAME = FAMILY = "literal"
FIXED = False
TITLE = "Literal Equations"
INSTRUCTIONS = "Solve each equation for the indicated variable."
COURSES = {"Algebra 1": "Equations"}

ENTRIES = []
_lesson = original_prompts()
for _t in TYPES:
    ENTRIES.append(dict(key=_t["key"], type=_t["key"], kind="letters", title=_t["title"],
                        width="half", space=_t["work"]))
    if any(f[2] == _t["key"] and (f[0], f[1]) not in _lesson for f in FORMULAS):   # a formulas entry needs one to draw
        ENTRIES.append(dict(key=_t["key"] + "f", type=_t["key"], kind="formulas",
                            title=f'{_t["title"]} (formulas)', width="half", space=_t["work"]))
ENTRY = {e["key"]: e for e in ENTRIES}

def entry_key(text):
    """User spelling -> entry key: "3" "3f" "a" "BF" -> "3" "3f" "A" "Bf"; None if unknown."""
    t = text.strip()
    f = t[-1:].lower() == "f" and len(t) > 1
    base = t[:-1] if f else t
    base = base.upper() if base.lower() in ("a", "b") else base
    k = base + ("f" if f else "")
    return k if k in ENTRY else None

def type_of(entry):
    return ENTRY[entry]["type"]

def hint(typ):
    """(label, title, look, move) for a type, used on slides and in the TUI."""
    t = TYPE[typ]
    return label(t), t["title"], t["look"], t["move"]

def heading(typ):
    t = TYPE[typ]
    return f'{label(t)}: {t["title"]}'

def special(typ):
    return bool(TYPE[typ].get("special"))

def initial_seen():
    """Problems that must never be drawn: the lesson's own fifty."""
    return original_prompts()

def seen_key(problem):
    return (problem["prompt"], problem["target"])

def generate(entry, rng, seen):
    """A new checked problem for this entry; adds it to seen. Raises RuntimeError."""
    e = ENTRY[entry]
    if e["kind"] == "formulas":
        if not any(f[2] == e["type"] and (f[0], f[1]) not in seen for f in FORMULAS):
            raise RuntimeError(f"no unused real formulas left for {label(TYPE[e['type']])}")
    return draw(e["type"], rng, e["kind"], seen)

def check(problem):
    """checked | failed | unchecked: is the answer right for the prompt?"""
    from ...check import holds, to_sympy, syms_of
    ans = problem["answer"]
    lhs, sep, rhs = ans.partition("=")
    if not sep or lhs.strip() != problem["target"]:
        return "unchecked"
    try:
        sol = rhs.strip()
        if syms_of(problem["prompt"])[problem["target"]] in to_sympy(sol).free_symbols:
            return "failed"                         # still has the unknown in it
        holds(problem["prompt"], problem["prompt"], problem["target"], sol)
        return "checked"
    except AssertionError:
        return "failed"
    except Exception:
        return "unchecked"

def typst(problem, gap="0.3em"):
    return f"$display({problem['prompt']})$; #h({gap}) ${problem['target']}$"

def answer_typst(problem):
    return f"$display({problem['answer']})$"

def pretty(s):
    """Typst math -> readable terminal text: a y - b y -> ay − by, pi -> π."""
    s = re.sub(r"\b(\d+)/(\d+) ", r"(\1/\2)", s)                     # 1/3 B h -> (1/3)B h
    s = re.sub(r"\bsqrt\(", "√(", s)
    s = re.sub(r"\bell\b", "ℓ", s)
    s = re.sub(r"\bpi\b", "π", s)
    s = re.sub(r"\^(\d)", lambda m: "⁰¹²³⁴⁵⁶⁷⁸⁹"[int(m.group(1))], s)
    s = re.sub(r"_(\d)", lambda m: "₀₁₂₃₄₅₆₇₈₉"[int(m.group(1))], s)
    s = re.sub(r"_([aehiklmnoprstuvx])\b",
               lambda m: dict(zip("aehiklmnoprstuvx", "ₐₑₕᵢₖₗₘₙₒₚᵣₛₜᵤᵥₓ"))[m.group(1)], s)
    s = re.sub(r"(?<=[\w)²³ℓπ₀-₉ₐ-ₜ]) (?=[\w(ℓπ√])", "", s)           # juxtaposition
    return s.replace(" - ", " − ").replace("-", "−")

def text(problem):
    """As the worksheet shows it: the equation, then the unknown."""
    return f"{pretty(problem['prompt'])};  {pretty(problem['target'])}"

def answer_text(problem):
    return pretty(problem["answer"])

# ------------------------------------------------------------------
# Hand editing. The text is Typst math, as stored: "R = s - 6 ; s".
# ------------------------------------------------------------------
def edit_text(problem):
    return f"{problem['prompt']} ; {problem['target']}"

def from_edit(text, old):
    """A problem from edited text "equation ; unknown" (the unknown may be left
    off to keep the old one). The answer is solved again when it can be; if
    not, the old answer is kept. Returns (problem, status); raises ValueError."""
    from ...check import side_diff, syms_of
    eq, _, target = text.partition(";")
    eq, target = " ".join(eq.split()), target.strip() or old["target"]
    if eq.count("=") != 1:
        raise ValueError("write one equation with a single =, then ; and the unknown")
    try:
        syms = syms_of(eq)
    except Exception as e:
        raise ValueError(f"can't read that equation: {e}") from None
    if target not in syms:
        raise ValueError(f"{target} isn't in the equation")
    new = dict(old, prompt=eq, target=target, source="edited")
    for root in (False, True):
        try:
            new["answer"] = f"{target} = {solve(eq, target, root=root)}"
            break
        except Exception:
            continue
    else:
        new["answer"] = old["answer"] if old["target"] == target else f"{target} = ?"
    return new, check(new)

def answer_edit_text(problem):
    return problem["answer"]

def with_answer(problem, text):
    """The problem with a hand-written answer; returns (problem, status)."""
    text = " ".join(text.split())
    if not text:
        raise ValueError("the answer can't be empty")
    if "=" not in text:
        text = f"{problem['target']} = {text}"
    elif text.partition("=")[0].strip() != problem["target"]:
        raise ValueError(f"the answer is for {problem['target']}: write {problem['target']} = ..., or just the right side")
    new = dict(problem, answer=text)
    return new, check(new)
