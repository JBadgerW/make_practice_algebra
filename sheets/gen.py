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
    coef, written(...)            terms as the prompt writes them, uncombined: "-7 + 4 m + 10"
    lettered, choices_typst, ...  multiple choice: choices A, B, C, ... and the key's letters

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
def generator(family, draw, check, seen_key, templates, tries=400, balance=None):
    """generate(entry, rng, seen) for a bank. draw(entry, rng, tpl) returns the
    problem's fields (prompt, answer, ...) or raises Redraw; templates(entry) is
    how many templates the entry has. The template is chosen once, so one that
    redraws often isn't rarer than the rest. Every problem must pass check().

    balance=(outcomes, outcome_of): spread a bank's answers over a sheet. seen
    holds the sheet's problems of the family; outcome_of(key) reads a seen key's
    outcome (or None). The draw is told to make one of the outcomes the sheet has
    fewest of: draw(entry, rng, tpl, want=outcome)."""
    def wanted(rng, seen):
        outcomes, outcome_of = balance
        count = {o: 0 for o in outcomes}
        for k in seen:
            o = outcome_of(k)
            if o in count:
                count[o] += 1
        least = min(count.values())
        return rng.choice([o for o in outcomes if count[o] == least])

    def generate(entry, rng, seen):
        tpl = rng.randrange(templates(entry))
        hint = {} if balance is None else dict(want=wanted(rng, seen))
        for _ in range(tries):
            try:
                p = dict(type=entry, **draw(entry, rng, tpl, **hint), source="template")
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

# ------------------------------------------------------------------
# Word problems: a story is text with {placeholders}; a problem fills
# them, and a check reads them back out of the words
# ------------------------------------------------------------------
def fill(template, **v):
    """The story with its numbers and words: fill("{n} {item}", n=3, item="apples")."""
    return template.format(**{k: (decimal(x) if isinstance(x, F) else x) for k, x in v.items()})

def pattern(template):
    """A regex for the story's text, with a named group per placeholder (a repeat must match the same)."""
    import re
    out, seen, i = "", set(), 0
    for m in re.finditer(r"\{(\w+)\}", template):
        out += re.escape(template[i:m.start()])
        name = m.group(1)
        out += f"(?P={name})" if name in seen else f"(?P<{name}>.+?)"
        seen.add(name)
        i = m.end()
    return "^" + out + re.escape(template[i:]) + "$"

def read(template, text):
    """The placeholders' values, as strings, read out of text written from the template; ValueError if it doesn't fit."""
    import re
    m = re.match(pattern(template), " ".join(text.split()))
    if not m:
        raise ValueError("keep the story's words; change only its numbers and names")
    return m.groupdict()

def number(s):
    """A number read out of words, as a Fraction: "12", "37.5", "$3.45", "1,200"."""
    return F(s.replace("$", "").replace(",", "").strip())

def text_shown(lines=90):
    """typst, answer_typst, text, answer_text, height for a bank whose prompt and answer are words."""
    from .typst import esc
    return (lambda p, gap="0.3em": esc(p["prompt"]),
            lambda p: esc(p["answer"]),
            lambda p: p["prompt"],
            lambda p: p["answer"],
            lambda p: 0.2 * (1 + len(p["prompt"]) // lines))

# ------------------------------------------------------------------
# Terms as the prompt writes them: in the order given, nothing combined
# ------------------------------------------------------------------
def coef(c):
    """A number as written: 3, 2.5 (a Decimal stays a decimal), 2/3 (a Fraction)."""
    if isinstance(c, F) and c.denominator != 1:
        return f"{c.numerator}/{c.denominator}"
    return str(int(c)) if c == int(c) else format(c, "f").rstrip("0")

def written(*terms):
    """Terms (coefficient, letters) in the order given: written((-7, ""), (4, "m"), (10, ""))
    is "-7 + 4 m + 10"; a coefficient of ±1 is left off a letter; zero terms are dropped.
    Letters may be a factor in parentheses: written((3, "(x + 5)")) is "3 (x + 5)"."""
    out = ""
    for c, v in terms:
        if c == 0:
            continue
        body = (coef(abs(c)) if abs(c) != 1 or not v else "") + (" " if abs(c) != 1 and v else "") + v
        out += ("-" if c < 0 else "") + body if not out else (" - " if c < 0 else " + ") + body
    return out or "0"

# ------------------------------------------------------------------
# Multiple choice: a problem stores its choices (Typst markup) and its
# answer as letters, "B" or, for choose-all, "A, C"
# ------------------------------------------------------------------
ABC = "ABCDEFGH"

def lettered(r, right, wrong, shuffle=True):
    """(choices, answer): the right choice (or a list of them) among the wrong ones,
    shuffled with r unless shuffle is False (then right, wrong, in the order given:
    for choices with a natural order, like no / one / infinitely many)."""
    right = list(right) if isinstance(right, (list, tuple)) else [right]
    allc = right + list(wrong)
    need(len(set(allc)) == len(allc))              # no two choices alike
    if shuffle:
        r.shuffle(allc)
    return allc, ", ".join(ABC[i] for i, c in enumerate(allc) if c in right)

def in_order(choices, right):
    """(choices, answer) for choices in a fixed order: right is the right one(s)."""
    right = right if isinstance(right, (list, tuple)) else [right]
    return list(choices), ", ".join(ABC[choices.index(c)] for c in right)

def letters_of(answer):
    """The answer's letters: "A, C" -> ["A", "C"]."""
    return [a.strip() for a in answer.split(",") if a.strip()]

def chosen(p):
    """The choices the answer names."""
    return [p["choices"][ABC.index(a)] for a in letters_of(p["answer"])]

def choices_typst(choices, arrangement="vertical"):
    return f'#choices(arrangement: "{arrangement}", ' + ", ".join(f"[{c}]" for c in choices) + ")"

def choice_answer_typst(p):
    """The key: each right letter with its choice, "B. $x = 4$"."""
    return "; ".join(f"{a}. {c}" for a, c in zip(letters_of(p["answer"]), chosen(p)))

def choices_text(choices, plain=lambda c: c):
    return "   ".join(f"{ABC[i]}. {plain(c)}" for i, c in enumerate(choices))

def with_letters(p, t, check):
    """with_answer for a multiple-choice bank: the answer edited as letters."""
    got = [a.upper() for a in letters_of(t.replace(" ", ",").replace(",,", ","))]
    if not got or any(a not in ABC[:len(p["choices"])] for a in got):
        raise ValueError(f"answer with letters, A to {ABC[len(p['choices']) - 1]}")
    new = dict(p, answer=", ".join(sorted(set(got))))
    return new, check(new)
