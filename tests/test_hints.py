"""Every bank's hints (a type's "Look for" and "The move") as the slides set them:
Typst markup, so their math must be in $...$ (see EXTENDING.md).

  - Each look and move has its $ paired, keeps Typst's markup characters
    (* _ # @ < \\ `) inside $...$, and writes no math in Unicode (x², −, ≤, 30°)
    outside $...$: the slides would set it as text.
  - Every hint and type title compiles as slide content (when typst is on the PATH).
  - prose(), the terminal's view of a hint, reads the math back without the $ signs.

NOT_YET is the families whose hints are still being converted: each one must
still break a rule (take it off the list once its hints are fixed), and no
other family may.
"""
import re, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import banks
from tui.common import hint_search_text, prose

NOT_YET = {
    "absolute", "absolute_words", "adv_radical_equations", "adv_rational_add",
    "adv_spheres", "adv_trig", "adv_word", "alg1_units_1_2_cumulative", "inequalities",
    "ka1_02_10", "ka1_11_01", "ka1_11_02", "ka1_15_02", "ka2_02_09", "ka2_03_01",
    "ka2_03_05", "ka2_03_07", "ka2_03_09", "ka2_03_10", "kpa_01_01", "kpa_01_02",
    "kpa_01_03", "kpa_08_02", "modeling", "modeling_1_2", "point_slope_2_2",
    "slope_intercept_2_1", "systems",
}

MARKUP = re.compile(r"[*_#@`\\]|<[A-Za-z]")              # strong, emphasis, code, ref, escape, label
UNICODE_MATH = re.compile(r"[⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ₀₁₂₃₄₅₆₇₈₉−·×÷√π≤≥≠±θ∞≈°]")

def hints():
    """[(family, type, label, title, look, move)], each family's type once."""
    out, seen = [], set()
    for name in banks.names():
        b = banks.get(name)
        for e in b.ENTRIES:
            typ = b.type_of(e["key"])
            h = b.hint(typ)
            if h and (b.FAMILY, typ) not in seen:
                seen.add((b.FAMILY, typ))
                out.append((b.FAMILY, typ, *h))
    return out

def problems(t):
    """What's wrong with one hint string, as the slides would set it."""
    if t.count("$") % 2:
        return ["an unpaired $"]
    rest = re.sub(r"\$[^$]*\$", " ", t)
    out = [f"{m.group(0)!r} outside $...$ is Typst markup" for m in MARKUP.finditer(rest)]
    out += [f"{m.group(0)!r} outside $...$: write it as Typst math" for m in UNICODE_MATH.finditer(rest)]
    return out

H = hints()
assert len(H) > 400, len(H)
bad = {}
for fam, typ, lbl, title, look, move in H:
    for field, t in (("look", look), ("move", move)):
        for p in problems(t):
            bad.setdefault(fam, []).append(f"{fam} type {typ} {field}: {p}: {t}")
new = sorted(set(bad) - NOT_YET)
assert not new, "hints that break the $...$ rule:\n" + "\n".join(x for f in new for x in bad[f])
done = sorted(NOT_YET - set(bad))
assert not done, f"these families' hints are fixed now: take them off NOT_YET: {done}"

# the rule's own checks
assert problems("Pair the $i$'s: $i^2 = -1$.") == []
assert problems("Then $S_n = a (1 - r^n)/(1 - r)$, and $a * b$.") == []
assert problems("S_n = a (1 - r^n)/(1 - r)") and problems("x² − 1") and problems("an $x odd")
assert problems("sin 30°") and not problems("$sin 30 degree$")

# every hint and title compiles as the slides' content blocks; a failing line is named, then left out
if shutil.which("typst"):
    d = Path(tempfile.mkdtemp())
    lines = []
    for fam, typ, lbl, title, look, move in H:
        for field, t in (("label", lbl), ("title", title), ("look", look), ("move", move)):
            lines.append((f"{fam} type {typ} {field}: {t}", f"#box[{t}]"))
    failed, live = [], dict(enumerate(lines, 1))
    for _ in range(50):
        (d / "h.typ").write_text("\n".join(live[i][1] if i in live else "" for i in range(1, len(lines) + 1)) + "\n")
        r = subprocess.run(["typst", "compile", str(d / "h.typ")], capture_output=True, text=True)
        if r.returncode == 0:
            break
        at = {}                                     # line -> its first error
        for msg, n in re.findall(r"^error: (.*)\n.*?h\.typ:(\d+):\d+", r.stderr, re.M | re.S):
            at.setdefault(int(n), msg)
        at = {n: m for n, m in at.items() if n in live}
        assert at, r.stderr
        for n, msg in sorted(at.items()):
            failed.append(f"{live.pop(n)[0]}\n    error: {msg}")
    assert r.returncode == 0, r.stderr
    assert not failed, "hints that don't compile as Typst:\n" + "\n".join(failed)

# the terminal shows a hint's math readable, without the $ signs
assert prose("Pair the $i$'s: each $i i$ is $-1$, so $i^2 = -1$ and $a + b i$.") \
    == "Pair the i's: each i·i is −1, so i² = −1 and a + bi."
assert prose("Write $sqrt(3/2)$ as $sqrt(3)/sqrt(2)$; $root(4, t)$ is $t^(1/4)$.") \
    == "Write √(3/2) as √(3)/√(2); ⁴√(t) is t^(1/4)."
assert prose('$|"amount" - "target"| <= "tolerance"$') == "|amount − target| ≤ tolerance"
assert prose('$"LCD" = 6 x$, $2 "cm"$') == "LCD = 6x, 2 cm"
assert prose("$S_n = a (1 - r^n)/(1 - r)$") == "Sₙ = a(1 − rⁿ)/(1 − r)"
assert prose("$+$, $-$, $times$, or $div$; $6 sqrt(2) cos 30 degree$") == "+, −, ×, or ÷; 6√(2) cos 30°"
assert prose("$a sin x$, $log x + ln(y)$, $f(theta) = tan theta$") == "a sin x, log x + ln(y), f(θ) = tan θ"
assert prose("$x >= 2$, $x != 3$, $b^m dot b^n$") == "x ≥ 2, x ≠ 3, bᵐ · bⁿ"
assert all("$" not in prose(t) for *_, look, move in H for t in (look, move))
# the finder matches a hint as written and as shown
s = hint_search_text("A sum of terms with powers of $i$: $i^2 = -1$.")
assert "powers of i" in s and "i^2 = -1" in s and "i² = −1" in s and "$" not in s

print(f"all hint tests passed ({len(H)} types; {len(NOT_YET)} families still to convert)")
