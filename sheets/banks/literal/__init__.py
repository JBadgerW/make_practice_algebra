"""Literal equations: solve a formula for a given variable.

Each type has a set of templates that build a fresh equation from random
letters and numbers, plus a pool of real formulas sorted by type. Templates
only write the *equation*: the answer is solved by sympy, written out in
classroom form by answers.fmt(), and checked numerically before it is used.
"""
import json, random
from ... import ROOT
from .types import TYPES, TYPE, KEYS, label
from .templates import D, Redraw, need, TEMPLATES
from .formulas import FORMULAS
from .answers import solve, fmt, make

def original_prompts():
    try:
        bank = json.loads((ROOT / "lesson_1-4" / "lesson_1-4_literal_seq_bank.json").read_text())
        return {(p["prompt"], p["target"]) for p in bank["problems"]}
    except (OSError, ValueError, KeyError):
        return set()

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
