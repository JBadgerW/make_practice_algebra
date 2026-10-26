"""What the Khan Prealgebra factor lessons share (Unit 1): factors,
multiples, factor pairs, and the hundred chart, drawn in Typst. (Not a bank.)

    factors(n), multiples(k)   as sets (multiples up to 100, the chart)
    pairs(n)                   the factor pairs (a, b), a <= b
    PREAMBLE, hundred_chart(shaded)
"""
def factors(n):
    return {d for d in range(1, n + 1) if n % d == 0}

def multiples(k, top=100):
    return set(range(k, top + 1, k))

def pairs(n):
    return [(a, n // a) for a in range(1, int(n ** 0.5) + 1) if n % a == 0]

PREAMBLE = r"""// The hundred chart (Khan Prealgebra, Unit 1): 1 to 100, the shaded numbers gray.
#let hundredchart(shaded) = table(
  columns: (0.62cm,) * 10, rows: 0.5cm, inset: 0pt, align: center + horizon, stroke: 0.5pt + luma(120),
  fill: (x, y) => if shaded.contains(y * 10 + x + 1) { luma(190) },
  ..range(1, 101).map(n => text(size: 8pt)[#n]))
"""

def hundred_chart(shaded):
    return f"#hundredchart(({', '.join(str(n) for n in sorted(shaded))},))"
