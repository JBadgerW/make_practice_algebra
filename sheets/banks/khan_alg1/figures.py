"""Figures for the Khan Algebra 1 banks, drawn in Typst. (Not a bank.)

    PREAMBLE                     the Typst definitions; a bank that draws sets its
                                 PREAMBLE to this (the writer prints it once)
    area_model(top, left)        the area model of a product: a column per term on
                                 top, a row per term on the left, each box as wide (or
                                 tall) as its term's coefficient, labels outside
    labeled_box(top, left, center)  a rectangle with its area inside and its sides labeled
"""
PREAMBLE = r"""// Area models (Khan Algebra 1, Unit 13): boxes sized by their terms, labeled outside.
#let areamodel(top, left, widths, heights) = {
  let shades = (luma(205), luma(175), luma(150), luma(190))
  let cells = ([],)
  for t in top { cells.push(pad(bottom: 3pt, t)) }
  for (i, l) in left.enumerate() {
    cells.push(pad(right: 4pt, l))
    for j in range(top.len()) {
      cells.push(rect(width: widths.at(j), height: heights.at(i), stroke: 0.6pt + white,
                      fill: shades.at(calc.rem(i + j, 4))))
    }
  }
  grid(columns: (auto,) + widths, align: center + horizon, ..cells)
}

// A rectangle with its area inside and its sides labeled: top over it, left beside it.
#let labeledbox(top, left, inside, w: 4.2cm, h: 2.2cm) = grid(
  columns: (auto, w), align: center + horizon, row-gutter: 3pt, column-gutter: 4pt,
  [], top,
  left, rect(width: w, height: h, fill: luma(225), stroke: 0.8pt, align(center + horizon, inside)))
"""

def sizes(coefficients, most, unit=1.0, least=0.6):
    """Box lengths in cm, in proportion to |coefficient|, the total at most `most`."""
    raw = [max(abs(c), 1) * unit for c in coefficients]
    k = min(1.0, most / sum(raw))
    return [f"{max(x * k, least):.2f}cm" for x in raw]

def area_model(top, left):
    """top, left: lists of (term in Typst math, coefficient)."""
    cols = ", ".join(f"[${t}$]" for t, _ in top)
    rows = ", ".join(f"[${t}$]" for t, _ in left)
    w = ", ".join(sizes([c for _, c in top], 6.0))
    h = ", ".join(sizes([c for _, c in left], 3.2, 0.8))
    return f"#areamodel(({cols},), ({rows},), ({w},), ({h},))"

def labeled_box(top, left, center):
    return f"#labeledbox([{top}], [{left}], [{center}])"
