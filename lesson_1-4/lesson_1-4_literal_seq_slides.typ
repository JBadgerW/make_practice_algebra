// The point of this is to incorporate in a single file the modular
// imports that I eventually will bundle in a package. Right now I
// don't want to bother with all that. So this file should work the
// way I want it to without any local package installs.

//#import "worksheet-headers.typ": first-page-header
//#import "question-env.typ": question, parts, choices

#set page(
  paper: "presentation-16-9",
  margin: 0.75in
)

#set text(
  font: "New Computer Modern",
  // font: "Linux Libertine O",
  size: 25pt,
)

#set par(
  justify: false,
  leading: 0.65em,
)

// Question Environment definitions
// Usage: #question(points: which is optional)[body of question]
//        #parts[] An inner environment for parts of a question
//        #choices(arrangement: stacked, linear, grid)[] for 
//          multiple choice questions

#let answer-blank(width) = box(
  width: width,
  inset: 0pt,
  stroke: (bottom: 0.7pt),
)

// Question counter
#let qnum = counter("question")

// Question environment
#let question(points: none, 
  space-below: 2em, 
  answer-line: none,
  renum: none,
  body
) = {
  if renum != none {
    qnum.update(renum - 1)
  }
  qnum.step()

  block(
    below: space-below,
    breakable: false,
  )[
    #grid(
      columns: (auto, 1fr, auto),
      column-gutter: 0.5em,

      [
        #context qnum.display("1.")
        #if answer-line != none [
          #answer-blank(answer-line)
        ]
     ],

      [
        #body
     ],

      [
        #if points != none [
          (#points pts)
       ]
     ],
    )
  ]
}

// Parts environment
#let parts(..items) = {
  stack(
    dir: ttb,
    spacing: 0.75em,

    ..items.pos().enumerate().map(((i, item)) => [
      #numbering("(a)", i + 1)
      #h(0.5em)
      #item
    ])
  )
}

// choices environment for multiple choice questions
#let choices(arrangement: "vertical", ..items) = {
  let labeled = items.pos().enumerate().map(((i, item)) => (
    numbering("A.", i + 1),
    item,
  ))

  if arrangement == "vertical" {
    // Original behavior: one choice per line
    stack(
      dir: ttb,
      spacing: 3em,
      ..labeled.map(((label, item)) => [
        #grid(
          columns: (auto, 1fr),
          [#label #h(0.25em)],
          [#item]
        )
      ])
    )

  } else if arrangement == "linear" {
    [
      #parbreak()
      // All choices on one line
      #labeled.map(((label, item)) => [
        #label #h(0.25em) #item #h(1fr)
      ]).join()
    ]

  } else if arrangement == "grid" {
    // chunk into pairs, padding with empty if odd
    let pairs = range(0, labeled.len(), step: 2).map(i => {
      let a = labeled.at(i)
      let b = if i + 1 < labeled.len() { labeled.at(i + 1) } else { none }
      (a, b)
    })

    stack(
      dir: ttb,
      spacing: 3em,
      ..pairs.map(((a, b)) =>
        grid(
          columns: (1fr, 1fr),
          gutter: 12pt,
          [
            #grid(
              columns: (auto, 1fr),
              [#a.at(0) #h(0.25em)],
              [#a.at(1)],
            ) 
          ],
          if b != none [
            #grid(
              columns: (auto, 1fr),
              [#b.at(0) #h(0.25em)],
              [#b.at(1)],
            ) 
          ] else [],
        )
      )
    )
  } else {
    panic("choices: unknown arrangement '" + arrangement + "'. Use vertical, linear, or grid.")
  }
}



#let first-page-header(class-name, worksheet-title, version: "1") = [
  #v(-0.25in)
  #grid(
    columns: (1fr, auto),
    column-gutter: 0pt,
    row-gutter: 1.4em,

    [#class-name],
    align(right)[Name #answer-blank(7cm)],

    [#set text(size: 15pt, weight: "bold"); #worksheet-title],
    align(right)[Date #answer-blank(3.5cm) Ver: #version],
  )
  #v(3em)
]

// ==================================================
// DOCUMENT VARIABLES
// ==================================================

#let class-name = "Algebra 1"
#let worksheet-title = "Literal Equations by Type"
#let version = "1"


// Worked steps: rows of (left side, =, right side, note).
#let steps(note-size: 0.85em, last: 1fr, ..rows) = grid(
  columns: (auto, auto, auto, last),
  column-gutter: 0.45em,
  row-gutter: 1.15em,
  align: (right + horizon, center + horizon, left + horizon, left + horizon),
  ..rows.pos().map(((l, r, n)) => (l, $=$, r,
    text(size: note-size, fill: luma(90), style: "italic", n))).flatten()
)

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

#align(center + horizon)[
  #text(size: 44pt, weight: "bold")[Literal Equations by Type]
  #v(0.4em)
  #text(size: 28pt)[Lesson 1-4]
  #v(0.2em)
  #text(size: 24pt)[Solve each equation for the indicated variable.]
]
#pagebreak()
#type-slide([Type 1], [One Step], [The unknown is tied to the rest by a single operation: $+$, $-$, $times$, or $div$.], [Undo that one operation on both sides.])
#pagebreak()
#slide(1, [$display(a = b + 9)$; #h(0.5em) $b$])
#pagebreak()
#worked-slide(1, [$display(a = b + 9)$; #h(0.5em) $b$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(a)$], [$display(b + 9)$], []),
    ([$display(a - 9)$], [$display(b)$], [subtract 9 from both sides]),
    ([$display(b)$], [$display(a - 9)$], [rewrite with $b$ on the left]),
  )
])
#pagebreak()
#slide(2, [$display(y = x - 7)$; #h(0.5em) $x$])
#pagebreak()
#slide(2, [$display(y = x - 7)$; #h(0.5em) $x$], answer: [$display(x = y + 7)$])
#pagebreak()
#slide(3, [$display(m/n = p)$; #h(0.5em) $m$])
#pagebreak()
#slide(3, [$display(m/n = p)$; #h(0.5em) $m$], answer: [$display(m = n p)$])
#pagebreak()
#slide(4, [$display(C = pi d)$; #h(0.5em) $d$])
#pagebreak()
#slide(4, [$display(C = pi d)$; #h(0.5em) $d$], answer: [$display(d = C/pi)$])
#pagebreak()
#slide(5, [$display(F = m a)$; #h(0.5em) $a$])
#pagebreak()
#slide(5, [$display(F = m a)$; #h(0.5em) $a$], answer: [$display(a = F/m)$])
#pagebreak()
#slide(6, [$display(P = I^2 R)$; #h(0.5em) $R$])
#pagebreak()
#slide(6, [$display(P = I^2 R)$; #h(0.5em) $R$], answer: [$display(R = P/I^2)$])
#pagebreak()
#slide(7, [$display(E = m c^2)$; #h(0.5em) $m$])
#pagebreak()
#slide(7, [$display(E = m c^2)$; #h(0.5em) $m$], answer: [$display(m = E/c^2)$])
#pagebreak()
#slide(8, [$display(C = 2 pi r)$; #h(0.5em) $r$])
#pagebreak()
#slide(8, [$display(C = 2 pi r)$; #h(0.5em) $r$], answer: [$display(r = C/(2 pi))$])

#pagebreak()
#type-slide([Type 2], [Add or Subtract, Then Divide], [No fractions. The unknown's term has other terms added to it or subtracted from it.], [Undo the adding or subtracting first, then divide by the unknown's coefficient.])
#pagebreak()
#slide(9, [$display(y = 3x + 5)$; #h(0.5em) $x$])
#pagebreak()
#worked-slide(9, [$display(y = 3x + 5)$; #h(0.5em) $x$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(y)$], [$display(3x + 5)$], []),
    ([$display(y - 5)$], [$display(3x)$], [subtract 5]),
    ([$display((y - 5)/3)$], [$display(x)$], [divide by 3]),
    ([$display(x)$], [$display((y - 5)/3)$], [rewrite with $x$ on the left]),
  )
])
#pagebreak()
#slide(10, [$display(P = 2a + b)$; #h(0.5em) $a$])
#pagebreak()
#slide(10, [$display(P = 2a + b)$; #h(0.5em) $a$], answer: [$display(a = (P - b)/2)$])
#pagebreak()
#slide(11, [$display(3x + c = d)$; #h(0.5em) $x$])
#pagebreak()
#slide(11, [$display(3x + c = d)$; #h(0.5em) $x$], answer: [$display(x = (d - c)/3)$])
#pagebreak()
#slide(12, [$display(v = u + a t)$; #h(0.5em) $a$])
#pagebreak()
#slide(12, [$display(v = u + a t)$; #h(0.5em) $a$], answer: [$display(a = (v - u)/t)$])

#pagebreak()
#type-slide([Type 3], [Clear One Denominator], [One fraction bar (or a fraction coefficient like $1/3$), and no parentheses to distribute.], [Multiply both sides by the denominator; then add or subtract and divide as usual.])
#pagebreak()
#slide(13, [$display(V = 1/3 B h)$; #h(0.5em) $B$])
#pagebreak()
#worked-slide(13, [$display(V = 1/3 B h)$; #h(0.5em) $B$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(V)$], [$display(1/3 B h)$], []),
    ([$display(3V)$], [$display(B h)$], [multiply both sides by 3]),
    ([$display((3V)/h)$], [$display(B)$], [divide by $h$]),
    ([$display(B)$], [$display((3V)/h)$], [rewrite with $B$ on the left]),
  )
])
#pagebreak()
#slide(14, [$display(A = 1/2 d_1 d_2)$; #h(0.5em) $d_1$])
#pagebreak()
#slide(14, [$display(A = 1/2 d_1 d_2)$; #h(0.5em) $d_1$], answer: [$display(d_1 = (2A)/d_2)$])
#pagebreak()
#slide(15, [$display(y = (x - 4)/k)$; #h(0.5em) $x$])
#pagebreak()
#slide(15, [$display(y = (x - 4)/k)$; #h(0.5em) $x$], answer: [$display(x = k y + 4)$])
#pagebreak()
#slide(16, [$display(M = (a b)/c)$; #h(0.5em) $c$])
#pagebreak()
#slide(16, [$display(M = (a b)/c)$; #h(0.5em) $c$], answer: [$display(c = (a b)/M)$])
#pagebreak()
#slide(17, [$display(y = 2/3 x + 4)$; #h(0.5em) $x$])
#pagebreak()
#slide(17, [$display(y = 2/3 x + 4)$; #h(0.5em) $x$], answer: [$display(x = 3/2 (y - 4))$])
#pagebreak()
#slide(18, [$display(y = (a x + b)/c)$; #h(0.5em) $x$])
#pagebreak()
#slide(18, [$display(y = (a x + b)/c)$; #h(0.5em) $x$], answer: [$display(x = (c y - b)/a)$])

#pagebreak()
#type-slide([Type 4], [Distribute First], [The unknown is inside parentheses, with a number or letter multiplying the group.], [Distribute; then add or subtract like terms and divide.])
#pagebreak()
#slide(19, [$display(P = 2(ell + w))$; #h(0.5em) $w$])
#pagebreak()
#worked-slide(19, [$display(P = 2(ell + w))$; #h(0.5em) $w$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(P)$], [$display(2(ell + w))$], []),
    ([$display(P)$], [$display(2 ell + 2w)$], [distribute the 2]),
    ([$display(P - 2 ell)$], [$display(2w)$], [subtract $2 ell$]),
    ([$display((P - 2 ell)/2)$], [$display(w)$], [divide by 2]),
    ([$display(w)$], [$display((P - 2 ell)/2)$], [same as $P/2 - ell$]),
  )
])
#pagebreak()
#slide(20, [$display(y - 5 = m(x + 2))$; #h(0.5em) $x$])
#pagebreak()
#slide(20, [$display(y - 5 = m(x + 2))$; #h(0.5em) $x$], answer: [$display(x = (y - 5)/m - 2)$])
#pagebreak()
#slide(21, [$display(a_n = a_1 + (n - 1) d)$; #h(0.5em) $n$])
#pagebreak()
#slide(21, [$display(a_n = a_1 + (n - 1) d)$; #h(0.5em) $n$], answer: [$display(n = (a_n - a_1)/d + 1)$])
#pagebreak()
#slide(22, [$display(5(a - 2b) = 3c)$; #h(0.5em) $b$])
#pagebreak()
#slide(22, [$display(5(a - 2b) = 3c)$; #h(0.5em) $b$], answer: [$display(b = (5a - 3c)/10)$])
#pagebreak()
#slide(23, [$display(4(p + 2q) = 10(q - p))$; #h(0.5em) $p$])
#pagebreak()
#slide(23, [$display(4(p + 2q) = 10(q - p))$; #h(0.5em) $p$], answer: [$display(p = q/7)$])
#pagebreak()
#slide(24, [$display(6(x - 2y) = 9(x + y))$; #h(0.5em) $y$])
#pagebreak()
#slide(24, [$display(6(x - 2y) = 9(x + y))$; #h(0.5em) $y$], answer: [$display(y = -x/7)$])

#pagebreak()
#type-slide([Type 5], [Clear a Denominator, Then Distribute], [A fraction and a set of parentheses.], [Multiply both sides by the denominator first, then distribute and solve.])
#pagebreak()
#slide(25, [$display(p = 3/4 (q - 8))$; #h(0.5em) $q$])
#pagebreak()
#worked-slide(25, [$display(p = 3/4 (q - 8))$; #h(0.5em) $q$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(p)$], [$display(3/4 (q - 8))$], []),
    ([$display(4p)$], [$display(3(q - 8))$], [multiply both sides by 4]),
    ([$display(4p)$], [$display(3q - 24)$], [distribute the 3]),
    ([$display(4p + 24)$], [$display(3q)$], [add 24]),
    ([$display((4p + 24)/3)$], [$display(q)$], [divide by 3]),
    ([$display(q)$], [$display((4p + 24)/3)$], [same as $4/3 p + 8$]),
  )
])
#pagebreak()
#slide(26, [$display(A = 1/2 h(a + b))$; #h(0.5em) $a$])
#pagebreak()
#slide(26, [$display(A = 1/2 h(a + b))$; #h(0.5em) $a$], answer: [$display(a = (2A)/h - b)$])
#pagebreak()
#slide(27, [$display(S = (n(a + ell))/2)$; #h(0.5em) $ell$])
#pagebreak()
#slide(27, [$display(S = (n(a + ell))/2)$; #h(0.5em) $ell$], answer: [$display(ell = (2S)/n - a)$])

#pagebreak()
#type-slide([Type 6], [Clear Two Denominators], [Two different fractions in the equation.], [Multiply every term on both sides by both denominators, which clears both fractions at once.])
#pagebreak()
#slide(28, [$display(a/b = c/d)$; #h(0.5em) $b$])
#pagebreak()
#worked-slide(28, [$display(a/b = c/d)$; #h(0.5em) $b$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(a/b)$], [$display(c/d)$], []),
    ([$display(a d)$], [$display(c b)$], [multiply both sides by $b d$]),
    ([$display((a d)/c)$], [$display(b)$], [divide by $c$]),
    ([$display(b)$], [$display((a d)/c)$], [rewrite with $b$ on the left]),
  )
])
#pagebreak()
#slide(29, [$display(x/a + y/b = 1)$; #h(0.5em) $y$])
#pagebreak()
#slide(29, [$display(x/a + y/b = 1)$; #h(0.5em) $y$], answer: [$display(y = b - (b x)/a)$])

#pagebreak()
#type-slide([Type 7], [Factor Out, Then Divide], [The unknown appears in two terms that are already together on one side.], [Factor the unknown out of those terms, then divide by what is left in the parentheses.])
#pagebreak()
#slide(30, [$display(a y - b y = c)$; #h(0.5em) $y$])
#pagebreak()
#worked-slide(30, [$display(a y - b y = c)$; #h(0.5em) $y$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(a y - b y)$], [$display(c)$], []),
    ([$display(y(a - b))$], [$display(c)$], [factor out $y$]),
    ([$display(y)$], [$display(c/(a - b))$], [divide by $(a - b)$]),
  )
])
#pagebreak()
#slide(31, [$display(A = P + P r t)$; #h(0.5em) $P$])
#pagebreak()
#slide(31, [$display(A = P + P r t)$; #h(0.5em) $P$], answer: [$display(P = A/(1 + r t))$])

#pagebreak()
#type-slide([Type 8], [Gather, Factor Out, Divide], [The unknown appears on both sides of the equation.], [Add or subtract to get every term with the unknown on one side and everything else on the other; then factor out and divide.])
#pagebreak()
#slide(32, [$display(k x = 2x + 5)$; #h(0.5em) $x$])
#pagebreak()
#worked-slide(32, [$display(k x = 2x + 5)$; #h(0.5em) $x$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(k x)$], [$display(2x + 5)$], []),
    ([$display(k x - 2x)$], [$display(5)$], [subtract $2x$]),
    ([$display(x(k - 2))$], [$display(5)$], [factor out $x$]),
    ([$display(x)$], [$display(5/(k - 2))$], [divide by $(k - 2)$]),
  )
])
#pagebreak()
#slide(33, [$display(a x + b = c x + d)$; #h(0.5em) $x$])
#pagebreak()
#slide(33, [$display(a x + b = c x + d)$; #h(0.5em) $x$], answer: [$display(x = (d - b)/(a - c))$])
#pagebreak()
#slide(34, [$display(5y + 2k = 9y - k y)$; #h(0.5em) $y$])
#pagebreak()
#slide(34, [$display(5y + 2k = 9y - k y)$; #h(0.5em) $y$], answer: [$display(y = (2k)/(4 - k))$])
#pagebreak()
#slide(35, [$display(3x - 2a = a x + 7)$; #h(0.5em) $x$])
#pagebreak()
#slide(35, [$display(3x - 2a = a x + 7)$; #h(0.5em) $x$], answer: [$display(x = (2a + 7)/(3 - a))$])

#pagebreak()
#type-slide([Type 9], [Distribute, Gather, Factor Out, Divide], [Parentheses, and the unknown shows up in more than one term.], [Distribute first; then gather, factor out, and divide as in Type 8.])
#pagebreak()
#slide(36, [$display(m(x + 2) = 5x - n)$; #h(0.5em) $x$])
#pagebreak()
#worked-slide(36, [$display(m(x + 2) = 5x - n)$; #h(0.5em) $x$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(m(x + 2))$], [$display(5x - n)$], []),
    ([$display(m x + 2m)$], [$display(5x - n)$], [distribute the $m$]),
    ([$display(m x + 2m + n)$], [$display(5x)$], [add $n$]),
    ([$display(2m + n)$], [$display(5x - m x)$], [subtract $m x$ (gather the $x$-terms on the right)]),
    ([$display(2m + n)$], [$display(x(5 - m))$], [factor out $x$]),
    ([$display(x)$], [$display((2m + n)/(5 - m))$], [divide by $(5 - m)$]),
  )
])
#pagebreak()
#slide(37, [$display(2(a x - 3) = b x + 4)$; #h(0.5em) $x$])
#pagebreak()
#slide(37, [$display(2(a x - 3) = b x + 4)$; #h(0.5em) $x$], answer: [$display(x = 10/(2a - b))$])
#pagebreak()
#slide(38, [$display(T = 2(ell w + w h + ell h))$; #h(0.5em) $h$])
#pagebreak()
#slide(38, [$display(T = 2(ell w + w h + ell h))$; #h(0.5em) $h$], answer: [$display(h = (T - 2 ell w)/(2(ell + w)))$])

#pagebreak()
#type-slide([Type 10], [Clear Single-Term Denominators, Then Solve], [Fractions whose denominators are single numbers or letters.], [Multiply both sides by every denominator to clear the fractions; what is left is a Type 9 (or easier) equation.])
#pagebreak()
#slide(39, [$display((x - a)/b = (x + c)/d)$; #h(0.5em) $x$])
#pagebreak()
#worked-slide(39, [$display((x - a)/b = (x + c)/d)$; #h(0.5em) $x$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display((x - a)/b)$], [$display((x + c)/d)$], []),
    ([$display(d(x - a))$], [$display(b(x + c))$], [multiply both sides by $b d$]),
    ([$display(d x - a d)$], [$display(b x + b c)$], [distribute]),
    ([$display(d x - b x)$], [$display(a d + b c)$], [subtract $b x$, add $a d$]),
    ([$display(x(d - b))$], [$display(a d + b c)$], [factor out $x$]),
    ([$display(x)$], [$display((a d + b c)/(d - b))$], [divide by $(d - b)$]),
  )
])
#pagebreak()
#slide(40, [$display(1/a + 1/b = 1/c)$; #h(0.5em) $c$])
#pagebreak()
#slide(40, [$display(1/a + 1/b = 1/c)$; #h(0.5em) $c$], answer: [$display(c = (a b)/(a + b))$])
#pagebreak()
#slide(41, [$display(E = 1/2 m v^2 + m g h)$; #h(0.5em) $m$])
#pagebreak()
#slide(41, [$display(E = 1/2 m v^2 + m g h)$; #h(0.5em) $m$], answer: [$display(m = (2E)/(v^2 + 2 g h))$])

#pagebreak()
#type-slide([Type 11], [Clear a Multi-Term Denominator], [A denominator that is a sum or difference, such as $(x - 1)$.], [Multiply both sides by the whole denominator, keeping its parentheses; then distribute and solve as in Type 9.])
#pagebreak()
#slide(42, [$display(t = d/(r + s))$; #h(0.5em) $r$])
#pagebreak()
#worked-slide(42, [$display(t = d/(r + s))$; #h(0.5em) $r$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(t)$], [$display(d/(r + s))$], []),
    ([$display(t(r + s))$], [$display(d)$], [multiply both sides by $(r + s)$]),
    ([$display(t r + t s)$], [$display(d)$], [distribute the $t$]),
    ([$display(t r)$], [$display(d - t s)$], [subtract $t s$]),
    ([$display(r)$], [$display((d - t s)/t)$], [divide by $t$; same as $d/t - s$]),
  )
])
#pagebreak()
#slide(43, [$display(y = (2x + 3)/(x - 1))$; #h(0.5em) $x$])
#pagebreak()
#slide(43, [$display(y = (2x + 3)/(x - 1))$; #h(0.5em) $x$], answer: [$display(x = (y + 3)/(y - 2))$])
#pagebreak()
#slide(44, [$display(a = (b + c)/(b - c))$; #h(0.5em) $b$])
#pagebreak()
#slide(44, [$display(a = (b + c)/(b - c))$; #h(0.5em) $b$], answer: [$display(b = (c(a + 1))/(a - 1))$])
#pagebreak()
#slide(45, [$display(y = (a x)/(x + b))$; #h(0.5em) $x$])
#pagebreak()
#slide(45, [$display(y = (a x)/(x + b))$; #h(0.5em) $x$], answer: [$display(x = (b y)/(a - y))$])

#pagebreak()
#type-slide([Special Case A], [Watch the Sign], [The term with the unknown has a minus sign in front of it.], [Add that term to both sides so it is positive on the other side, then solve. (If you leave it where it is, divide by the negative coefficient, not the positive one.)])
#pagebreak()
#slide(46, [$display(a - b = c)$; #h(0.5em) $b$])
#pagebreak()
#worked-slide(46, [$display(a - b = c)$; #h(0.5em) $b$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(a - b)$], [$display(c)$], []),
    ([$display(a)$], [$display(c + b)$], [add $b$ to both sides: now $b$ is positive]),
    ([$display(a - c)$], [$display(b)$], [subtract $c$]),
    ([$display(b)$], [$display(a - c)$], [rewrite with $b$ on the left]),
  )
])
#pagebreak()
#slide(47, [$display(4x - 3y = 12)$; #h(0.5em) $y$])
#pagebreak()
#worked-slide(47, [$display(4x - 3y = 12)$; #h(0.5em) $y$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(4x - 3y)$], [$display(12)$], []),
    ([$display(4x)$], [$display(12 + 3y)$], [add $3y$ to both sides: now $3y$ is positive]),
    ([$display(4x - 12)$], [$display(3y)$], [subtract 12]),
    ([$display((4x - 12)/3)$], [$display(y)$], [divide by 3]),
    ([$display(y)$], [$display((4x - 12)/3)$], [rewrite with $y$ on the left]),
  )
])

#pagebreak()
#type-slide([Special Case B], [Finish with a Square Root], [The unknown is squared.], [Solve for the squared term as usual, then take the square root of both sides. These unknowns are lengths, so use the positive root.])
#pagebreak()
#slide(48, [$display(A = 4 pi r^2)$; #h(0.5em) $r$])
#pagebreak()
#worked-slide(48, [$display(A = 4 pi r^2)$; #h(0.5em) $r$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(A)$], [$display(4 pi r^2)$], []),
    ([$display(A/(4 pi))$], [$display(r^2)$], [divide by $4 pi$]),
    ([$display(sqrt(A/(4 pi)))$], [$display(r)$], [take the positive square root]),
    ([$display(r)$], [$display(sqrt(A/(4 pi)))$], [rewrite with $r$ on the left]),
  )
])
#pagebreak()
#slide(49, [$display(V = pi r^2 h)$; #h(0.5em) $r$])
#pagebreak()
#worked-slide(49, [$display(V = pi r^2 h)$; #h(0.5em) $r$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(V)$], [$display(pi r^2 h)$], []),
    ([$display(V/(pi h))$], [$display(r^2)$], [divide by $pi h$]),
    ([$display(sqrt(V/(pi h)))$], [$display(r)$], [take the positive square root]),
    ([$display(r)$], [$display(sqrt(V/(pi h)))$], [rewrite with $r$ on the left]),
  )
])
#pagebreak()
#slide(50, [$display(F = (k q_1 q_2)/r^2)$; #h(0.5em) $r$])
#pagebreak()
#worked-slide(50, [$display(F = (k q_1 q_2)/r^2)$; #h(0.5em) $r$], [
  #steps(last: auto, note-size: 0.7em,
    ([$display(F)$], [$display((k q_1 q_2)/r^2)$], []),
    ([$display(F r^2)$], [$display(k q_1 q_2)$], [multiply both sides by $r^2$]),
    ([$display(r^2)$], [$display((k q_1 q_2)/F)$], [divide by $F$]),
    ([$display(r)$], [$display(sqrt((k q_1 q_2)/F))$], [take the positive square root]),
  )
])

