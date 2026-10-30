"""Decoys for a warm-up's back: look-alike wrong answers, so an answer can't be
matched to its problem by its look alone (its variable, its form) without solving.

An answer's shape is its Typst with the numbers blanked: k = 5 and k = -12 share
one, k = 5 and h = 5 don't. An answer whose shape is the only one of its kind
gets a decoy: the same answer with some of its numbers changed. A changed number
keeps its sign (the minus is outside it), its digits, and its size (within a
factor of three), and is never what a
common slip gives (one or two off, double or half, ten times, its digits
reversed, 0). Numbers in exponents, subscripts, and under a root stay, so the
decoy looks as simplified as the answer. An answer with no number to change
("no solution", V = m/D) can't have a decoy: it is stuck.
"""
import random, re

NUM = re.compile(r"\d+(?:\.\d+)?")
GUARDED = re.compile(r"(?:sqrt|root|\^|_)\(")

def shape(ans):
    return NUM.sub("#", ans)

def _guarded(ans):
    """The spans of ans whose numbers stay: inside sqrt( root( ^( _( to the matching paren."""
    spans = []
    for m in GUARDED.finditer(ans):
        depth, i = 1, m.end()
        while i < len(ans) and depth:
            depth += {"(": 1, ")": -1}.get(ans[i], 0)
            i += 1
        spans.append((m.start(), i))
    return spans

def numbers(ans):
    """The numbers of ans that a decoy may change, as regex matches."""
    spans = _guarded(ans)
    return [m for m in NUM.finditer(ans)
            if not (m.start() and ans[m.start() - 1] in "^_")
            and not any(a <= m.start() < b for a, b in spans)]

def slips(n):
    """What common mistakes make of the whole number n (the digits, sign aside)."""
    out = {0, n, n - 1, n + 1, n - 2, n + 2, 2 * n, 10 * n, int(str(n)[::-1])}
    out |= {n // 2} if n % 2 == 0 else set()
    out |= {n // 10} if n % 10 == 0 else set()
    return out

def _new_number(text, rng):
    """Another number like text: as many digits (a whole number of one digit: 1-12)
    and decimal places, within a factor of three, and no slip."""
    whole, _, frac = text.partition(".")
    n = int(whole + frac)
    d = len(str(n))
    one = (1, 9 if frac else 12)
    lo, hi = one if d == 1 else (max(10 ** (d - 1), n // 3), min(10 ** d - 1, 3 * n))
    bad = slips(n)
    fits = lambda m: m not in bad and not (frac and m % 10 == 0 and n % 10)     # no 2.0 for 2.5
    ok = [m for m in range(lo, hi + 1) if fits(m)] or None if hi - lo < 1000 else None
    if ok is None and hi - lo < 1000:       # nothing near: any number of its digits
        lo, hi = one if d == 1 else (10 ** (d - 1), 10 ** d - 1)
    while ok is None:                       # a big number: draw until one fits
        m = rng.randint(lo, hi)
        ok = [m] if fits(m) else None
    m = rng.choice(ok)
    s = str(m).rjust(len(frac) + 1, "0") if frac else str(m)
    return f"{s[:-len(frac)]}.{s[-len(frac):]}" if frac else s

def decoy(ans, rng, avoid=()):
    """A look-alike of ans with at least one of its numbers changed, not in avoid;
    None if it has no number to change (or every try lands in avoid)."""
    nums = numbers(ans)
    if not nums:
        return None
    for _ in range(50):
        pick = [m for m in nums if rng.random() < 0.5] or [rng.choice(nums)]
        out, last = "", 0
        for m in pick:
            out += ans[last:m.start()] + _new_number(m.group(), rng)
            last = m.end()
        out += ans[last:]
        if out != ans and out not in avoid:
            return out
    return None

def plan(answers, seed=0):
    """Decoys for a back holding answers (Typst strings): [(i, decoy)] for each
    answer whose shape no other answer has, and the indexes of those that can't
    have one (stuck). The same answers and seed always give the same decoys."""
    rng = random.Random(f"{seed}|" + "|".join(answers))
    count = {}
    for a in answers:
        count[shape(a)] = count.get(shape(a), 0) + 1
    out, stuck, taken = [], [], set(answers)
    for i, a in enumerate(answers):
        if count[shape(a)] > 1:
            continue
        d = decoy(a, rng, taken)
        if d is None:
            stuck.append(i)
        else:
            out.append((i, d))
            taken.add(d)
    return out, stuck
