"""What generator banks share: random helpers, letters and names, the
standard type functions, and the draw-and-check loop.

The banks before the Advanced Math ones each carry their own copies of
these; new banks use this module.

    Redraw, need(ok)              reject a draw that drifted, and try again
    signed, signed_except, except_, proper_divisor, reduced, sig_figs, decimal
    LETTERS, NAMES                letters for variables, first names for stories
    Types(TYPES, ...)             the type table and the bank functions built from it
    generator(...)                generate(entry, rng, seen): draw, check, no repeats
    shown(), edits(...)           display, terminal text, and hand editing for Typst-math banks

Every random choice takes the bank's rng (random.Random(seed)) first, so a
draw is reproducible; checks use the global random, so checking never
changes what gets drawn.
"""
import math
from decimal import Decimal
from fractions import Fraction as F

class Redraw(Exception):
    pass

def need(ok):
    if not ok:
        raise Redraw

# ------------------------------------------------------------------
# Numbers
# ------------------------------------------------------------------
def signed(r, lo, hi):
    """±(lo..hi): signed(r, 1, 5) is one of -5..-1, 1..5."""
    return r.choice((-1, 1)) * r.randint(lo, hi)

def except_(r, lo, hi, *out):
    """lo..hi, leaving out the numbers in out."""
    choices = [n for n in range(lo, hi + 1) if n not in out]
    need(choices)
    return r.choice(choices)

def signed_except(r, lo, hi, *out):
    """±(lo..hi), leaving out the signed numbers in out: signed_except(r, 1, 3, 1) is -3..-1, 2, 3."""
    choices = [n for n in range(-hi, hi + 1) if lo <= abs(n) and n not in out]
    need(choices)
    return r.choice(choices)

def prime_factors(n):
    out, p = [], 2
    while p * p <= n:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out + ([n] if n > 1 else [])

def proper_divisor(r, n):
    """A divisor of |n| other than 1 and |n|, made from some of its prime factors; Redraw if n is prime or ±1."""
    fs = prime_factors(abs(n))
    need(len(fs) >= 2)
    return math.prod(r.sample(fs, r.randint(1, len(fs) - 1)))

def reduced(*ns):
    """Integers divided by their greatest common factor: reduced(4, 6) = (2, 3)."""
    g = math.gcd(*ns)
    return tuple(n // g for n in ns) if g else tuple(ns)

def sig_figs(x, digits):
    """x rounded to that many significant figures, as a Fraction (exact, for checks)."""
    if x == 0:
        return F(0)
    d = Decimal(str(float(x)))
    return F(round(d, digits - 1 - d.adjusted()))

def decimal(q, places=2):
    """A Fraction as a decimal with at most `places` places and no trailing zeros: 2.5, 12, 0.75."""
    d = round(Decimal(q.numerator) / Decimal(q.denominator), places)
    s = format(d, "f")
    return s.rstrip("0").rstrip(".") if "." in s else s

# ------------------------------------------------------------------
# Letters and names
# ------------------------------------------------------------------
# No e (Euler's number), i (the imaginary unit), l (looks like 1), or o (looks like 0).
LETTERS = tuple("abcdfghjkmnpqrstuvwxyz")

NAMES = ("Enrique", "Maya", "Darnell", "Priya", "Tomás", "Grace", "Kenji", "Amara", "Luis", "Hannah",
         "Mateo", "Aaliyah", "Owen", "Sofia", "Isaiah", "Mei", "Caleb", "Fatima", "Noah", "Lucia")

def letters(r, n):
    """n different letters, in alphabetical order."""
    return sorted(r.sample(LETTERS, n))

# ------------------------------------------------------------------
# The type table
# ------------------------------------------------------------------
class Types:
    """A bank's types: TYPES is a list of dict(key, title, look, move, and optional
    instructions, special, courses, space, width). space and width default to the
    arguments here. The bank functions come from functions():

        label, entry_key, type_of, heading, hint, special, type_instructions = T.functions()
    """
    def __init__(self, types, instructions="", space="1in", width="half", kind="numbers"):
        self.TYPES = types
        self.TYPE = {t["key"]: t for t in types}
        self.KEYS = [t["key"] for t in types]
        self.instructions = instructions
        self.ENTRIES = [dict(key=t["key"], type=t["key"], kind=kind, title=t["title"],
                             width=t.get("width", width), space=t.get("space", space)) for t in types]
        self.ENTRY = {e["key"]: e for e in self.ENTRIES}

    def label(self, t):
        return ("Special Case " if t.get("special") else "Type ") + t["key"]

    def entry_key(self, text):
        t = text.strip()
        return t if t in self.ENTRY else t.upper() if t.upper() in self.ENTRY else None

    def type_of(self, entry):
        return entry

    def heading(self, typ):
        return f"{self.label(self.TYPE[typ])}: {self.TYPE[typ]['title']}"

    def hint(self, typ):
        t = self.TYPE[typ]
        return self.label(t), t["title"], t["look"], t["move"]

    def special(self, typ):
        return bool(self.TYPE[typ].get("special"))

    def type_instructions(self, typ):
        return self.TYPE[typ].get("instructions", self.instructions)

    def functions(self):
        return (self.label, self.entry_key, self.type_of, self.heading, self.hint,
                self.special, self.type_instructions)

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------
def generator(family, draw, check, seen_key, templates, tries=400):
    """generate(entry, rng, seen) for a bank. draw(entry, rng, tpl) returns the
    problem's fields (prompt, answer, ...) or raises Redraw; templates(entry) is
    how many templates the entry has. The template is chosen once, so one that
    redraws often isn't rarer than the rest. Every problem must pass check()."""
    def generate(entry, rng, seen):
        tpl = rng.randrange(templates(entry))
        for _ in range(tries):
            try:
                p = dict(type=entry, **draw(entry, rng, tpl), source="template")
            except Redraw:
                continue
            if seen_key(p) in seen:
                continue
            if check(p) != "checked":                    # the independent check must agree with the build
                raise AssertionError(f"{family} type {entry}: {p}")
            seen.add(seen_key(p))
            return p
        raise RuntimeError(f"could not draw a {family} Type {entry} problem; check its template")
    return generate

def selftest(name, generate, keys, label, n, seed, reset=25):
    """Draw n problems of every type (seen resets every `reset` draws, for small types)."""
    import random
    rng = random.Random(seed)
    for k in keys:
        seen = set()
        for i in range(n):
            if i % reset == 0:
                seen = set()
            generate(k, rng, seen)
        print(f"{name} {label(k):8} {n} drawn, all verified")
    return True

# ------------------------------------------------------------------
# Showing and editing a problem whose prompt and answer are Typst math
# ------------------------------------------------------------------
def shown():
    """typst, answer_typst, text, answer_text, height for a bank whose prompt
    and answer are both Typst math, shown in display style: every fraction
    full size, nested ones too (but not in exponents)."""
    from .typmath import display, dfrac, text as plain
    return (lambda p, gap="0.3em": display(dfrac(p["prompt"])),
            lambda p: display(dfrac(p["answer"])),
            lambda p: plain(p["prompt"]),
            lambda p: plain(p["answer"]),
            lambda p: 0.55 if "/" in p["prompt"] else 0.3)

def edits(answer_of, check, example, example_answer, imaginary=False):
    """edit_text, from_edit, answer_edit_text, with_answer for such a bank.
    An edited prompt is solved again with answer_of(prompt) (a ValueError
    there keeps the old answer, which check() then marks); an edited answer
    is checked against the prompt."""
    from .check import to_sympy
    def clean(t):
        return " ".join(t.replace("−", "-").split())
    def from_edit(t, old):
        t = clean(t)
        try:
            to_sympy(t, imaginary)
        except Exception:
            raise ValueError(f"write it in Typst math, like {example}") from None
        try:
            answer = answer_of(t)
        except (ValueError, Redraw):
            answer = old["answer"]
        new = dict(old, prompt=t, answer=answer, source="edited")
        return new, check(new)
    def with_answer(p, t):
        t = clean(t)
        try:
            to_sympy(t, imaginary)
        except Exception:
            raise ValueError(f"write the answer in Typst math, like {example_answer}") from None
        new = dict(p, answer=t)
        return new, check(new)
    return (lambda p: p["prompt"]), from_edit, (lambda p: p["answer"]), with_answer
