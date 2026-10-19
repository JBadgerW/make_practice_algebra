// The point of this is to incorporate in a single file the modular
// imports that I eventually will bundle in a package. Right now I
// don't want to bother with all that. So this file should work the
// way I want it to without any local package installs.

//#import "worksheet-headers.typ": first-page-header
//#import "question-env.typ": question, parts, choices

#set page(
  paper: "us-letter",
  margin: 0.75in
)

#set text(
  font: "New Computer Modern",
  // font: "Linux Libertine O",
  size: 12pt,
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

#let type-head(heading, hint) = block(sticky: true, above: 1.1em, below: 0.7em)[
  #text(weight: "bold", size: 13pt)[#heading] \
  #text(size: 10.5pt, style: "italic")[#hint]
]

#first-page-header(class-name, worksheet-title, version: version)
#v(-2.2em)
Solve each equation for the indicated variable. The problems are grouped by the kind of first move they need, from simplest to most involved.
#v(0.2em)

#type-head([Type 1: One Step], [The unknown is tied to the rest by a single operation: $+$, $-$, $times$, or $div$. Undo that one operation on both sides.])
#grid(
  columns: (1fr, 1fr),
  rows: 0.95in,
  column-gutter: 1em,
  question(renum: 1, space-below: 0em)[
    $display(a = b + 9)$; #h(0.3em) $b$
  ],
  question(renum: 2, space-below: 0em)[
    $display(y = x - 7)$; #h(0.3em) $x$
  ],
  question(renum: 3, space-below: 0em)[
    $display(m/n = p)$; #h(0.3em) $m$
  ],
  question(renum: 4, space-below: 0em)[
    $display(C = pi d)$; #h(0.3em) $d$
  ],
  question(renum: 5, space-below: 0em)[
    $display(F = m a)$; #h(0.3em) $a$
  ],
  question(renum: 6, space-below: 0em)[
    $display(P = I^2 R)$; #h(0.3em) $R$
  ],
  question(renum: 7, space-below: 0em)[
    $display(E = m c^2)$; #h(0.3em) $m$
  ],
  question(renum: 8, space-below: 0em)[
    $display(C = 2 pi r)$; #h(0.3em) $r$
  ],
)

#type-head([Type 2: Add or Subtract, Then Divide], [No fractions. The unknown's term has other terms added to it or subtracted from it. Undo the adding or subtracting first, then divide by the unknown's coefficient.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.1in,
  column-gutter: 1em,
  question(renum: 9, space-below: 0em)[
    $display(y = 3x + 5)$; #h(0.3em) $x$
  ],
  question(renum: 10, space-below: 0em)[
    $display(P = 2a + b)$; #h(0.3em) $a$
  ],
  question(renum: 11, space-below: 0em)[
    $display(3x + c = d)$; #h(0.3em) $x$
  ],
  question(renum: 12, space-below: 0em)[
    $display(v = u + a t)$; #h(0.3em) $a$
  ],
)

#type-head([Type 3: Clear One Denominator], [One fraction bar (or a fraction coefficient like $1/3$), and no parentheses to distribute. Multiply both sides by the denominator; then add or subtract and divide as usual.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.25in,
  column-gutter: 1em,
  question(renum: 13, space-below: 0em)[
    $display(V = 1/3 B h)$; #h(0.3em) $B$
  ],
  question(renum: 14, space-below: 0em)[
    $display(A = 1/2 d_1 d_2)$; #h(0.3em) $d_1$
  ],
  question(renum: 15, space-below: 0em)[
    $display(y = (x - 4)/k)$; #h(0.3em) $x$
  ],
  question(renum: 16, space-below: 0em)[
    $display(M = (a b)/c)$; #h(0.3em) $c$
  ],
  question(renum: 17, space-below: 0em)[
    $display(y = 2/3 x + 4)$; #h(0.3em) $x$
  ],
  question(renum: 18, space-below: 0em)[
    $display(y = (a x + b)/c)$; #h(0.3em) $x$
  ],
)

#type-head([Type 4: Distribute First], [The unknown is inside parentheses, with a number or letter multiplying the group. Distribute; then add or subtract like terms and divide.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.5in,
  column-gutter: 1em,
  question(renum: 19, space-below: 0em)[
    $display(P = 2(ell + w))$; #h(0.3em) $w$
  ],
  question(renum: 20, space-below: 0em)[
    $display(y - 5 = m(x + 2))$; #h(0.3em) $x$
  ],
  question(renum: 21, space-below: 0em)[
    $display(a_n = a_1 + (n - 1) d)$; #h(0.3em) $n$
  ],
  question(renum: 22, space-below: 0em)[
    $display(5(a - 2b) = 3c)$; #h(0.3em) $b$
  ],
  question(renum: 23, space-below: 0em)[
    $display(4(p + 2q) = 10(q - p))$; #h(0.3em) $p$
  ],
  question(renum: 24, space-below: 0em)[
    $display(6(x - 2y) = 9(x + y))$; #h(0.3em) $y$
  ],
)

#type-head([Type 5: Clear a Denominator, Then Distribute], [A fraction and a set of parentheses. Multiply both sides by the denominator first, then distribute and solve.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.5in,
  column-gutter: 1em,
  question(renum: 25, space-below: 0em)[
    $display(p = 3/4 (q - 8))$; #h(0.3em) $q$
  ],
  question(renum: 26, space-below: 0em)[
    $display(A = 1/2 h(a + b))$; #h(0.3em) $a$
  ],
  question(renum: 27, space-below: 0em)[
    $display(S = (n(a + ell))/2)$; #h(0.3em) $ell$
  ],
)

#type-head([Type 6: Clear Two Denominators], [Two different fractions in the equation. Multiply every term on both sides by both denominators, which clears both fractions at once.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.5in,
  column-gutter: 1em,
  question(renum: 28, space-below: 0em)[
    $display(a/b = c/d)$; #h(0.3em) $b$
  ],
  question(renum: 29, space-below: 0em)[
    $display(x/a + y/b = 1)$; #h(0.3em) $y$
  ],
)

#type-head([Type 7: Factor Out, Then Divide], [The unknown appears in two terms that are already together on one side. Factor the unknown out of those terms, then divide by what is left in the parentheses.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.4in,
  column-gutter: 1em,
  question(renum: 30, space-below: 0em)[
    $display(a y - b y = c)$; #h(0.3em) $y$
  ],
  question(renum: 31, space-below: 0em)[
    $display(A = P + P r t)$; #h(0.3em) $P$
  ],
)

#type-head([Type 8: Gather, Factor Out, Divide], [The unknown appears on both sides of the equation. Add or subtract to get every term with the unknown on one side and everything else on the other; then factor out and divide.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.6in,
  column-gutter: 1em,
  question(renum: 32, space-below: 0em)[
    $display(k x = 2x + 5)$; #h(0.3em) $x$
  ],
  question(renum: 33, space-below: 0em)[
    $display(a x + b = c x + d)$; #h(0.3em) $x$
  ],
  question(renum: 34, space-below: 0em)[
    $display(5y + 2k = 9y - k y)$; #h(0.3em) $y$
  ],
  question(renum: 35, space-below: 0em)[
    $display(3x - 2a = a x + 7)$; #h(0.3em) $x$
  ],
)

#type-head([Type 9: Distribute, Gather, Factor Out, Divide], [Parentheses, and the unknown shows up in more than one term. Distribute first; then gather, factor out, and divide as in Type 8.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.75in,
  column-gutter: 1em,
  question(renum: 36, space-below: 0em)[
    $display(m(x + 2) = 5x - n)$; #h(0.3em) $x$
  ],
  question(renum: 37, space-below: 0em)[
    $display(2(a x - 3) = b x + 4)$; #h(0.3em) $x$
  ],
  question(renum: 38, space-below: 0em)[
    $display(T = 2(ell w + w h + ell h))$; #h(0.3em) $h$
  ],
)

#type-head([Type 10: Clear Single-Term Denominators, Then Solve], [Fractions whose denominators are single numbers or letters. Multiply both sides by every denominator to clear the fractions; what is left is a Type 9 (or easier) equation.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.85in,
  column-gutter: 1em,
  question(renum: 39, space-below: 0em)[
    $display((x - a)/b = (x + c)/d)$; #h(0.3em) $x$
  ],
  question(renum: 40, space-below: 0em)[
    $display(1/a + 1/b = 1/c)$; #h(0.3em) $c$
  ],
  question(renum: 41, space-below: 0em)[
    $display(E = 1/2 m v^2 + m g h)$; #h(0.3em) $m$
  ],
)

#type-head([Type 11: Clear a Multi-Term Denominator], [A denominator that is a sum or difference, such as $(x - 1)$. Multiply both sides by the whole denominator, keeping its parentheses; then distribute and solve as in Type 9.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.85in,
  column-gutter: 1em,
  question(renum: 42, space-below: 0em)[
    $display(t = d/(r + s))$; #h(0.3em) $r$
  ],
  question(renum: 43, space-below: 0em)[
    $display(y = (2x + 3)/(x - 1))$; #h(0.3em) $x$
  ],
  question(renum: 44, space-below: 0em)[
    $display(a = (b + c)/(b - c))$; #h(0.3em) $b$
  ],
  question(renum: 45, space-below: 0em)[
    $display(y = (a x)/(x + b))$; #h(0.3em) $x$
  ],
)

#v(0.6em)
#align(center, text(weight: "bold", size: 14pt)[Special Cases])
#type-head([Special Case A: Watch the Sign], [The term with the unknown has a minus sign in front of it. Add that term to both sides so it is positive on the other side, then solve. (If you leave it where it is, divide by the negative coefficient, not the positive one.)])
#grid(
  columns: (1fr, 1fr),
  rows: 1.2in,
  column-gutter: 1em,
  question(renum: 46, space-below: 0em)[
    $display(a - b = c)$; #h(0.3em) $b$
  ],
  question(renum: 47, space-below: 0em)[
    $display(4x - 3y = 12)$; #h(0.3em) $y$
  ],
)

#type-head([Special Case B: Finish with a Square Root], [The unknown is squared. Solve for the squared term as usual, then take the square root of both sides. These unknowns are lengths, so use the positive root.])
#grid(
  columns: (1fr, 1fr),
  rows: 1.5in,
  column-gutter: 1em,
  question(renum: 48, space-below: 0em)[
    $display(A = 4 pi r^2)$; #h(0.3em) $r$
  ],
  question(renum: 49, space-below: 0em)[
    $display(V = pi r^2 h)$; #h(0.3em) $r$
  ],
  question(renum: 50, space-below: 0em)[
    $display(F = (k q_1 q_2)/r^2)$; #h(0.3em) $r$
  ],
)

