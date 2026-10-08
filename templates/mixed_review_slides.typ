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
#let worksheet-title = "Mixed Equations Review"
#let version = "1"


#let slide(n, prob, answer: none) = {
  align(left)[#text(size: 30pt, weight: "bold")[Question #n]]
  v(1.5em)
  align(center)[
    #text(size: 34pt)[#prob]
    #if answer != none [
      #h(1.5em) #text(fill: red, size: 34pt)[#answer]
    ]
  ]
}

#slide(1, $display(0.45(y - 0.2) = 5 - 0.25(1 - y))$)
#pagebreak()
#slide(1, $display(0.45(y - 0.2) = 5 - 0.25(1 - y))$, answer: [$display(y = 24.2)$])
#pagebreak()

#slide(2, $display(0.25(y - 0.4) = 3 - 0.5(1 - y))$)
#pagebreak()
#slide(2, $display(0.25(y - 0.4) = 3 - 0.5(1 - y))$, answer: [$display(y = -10.4)$])
#pagebreak()

#slide(3, $display((0.40) (60) = 0.30x + 0.50 (60 - x))$)
#pagebreak()
#slide(3, $display((0.40) (60) = 0.30x + 0.50 (60 - x))$, answer: [$display(x = 30)$])
#pagebreak()

#slide(4, $display((0.35) (80) = 0.25x + 0.45 (80 - x))$)
#pagebreak()
#slide(4, $display((0.35) (80) = 0.25x + 0.45 (80 - x))$, answer: [$display(x = 40)$])
#pagebreak()

#slide(5, $display(5/36 = 7/18w + 11/12)$)
#pagebreak()
#slide(5, $display(5/36 = 7/18w + 11/12)$, answer: [$display(w = -2)$])
#pagebreak()

#slide(6, $display(0.2(y - 0.5) = 4 - 0.6(1 - y))$)
#pagebreak()
#slide(6, $display(0.2(y - 0.5) = 4 - 0.6(1 - y))$, answer: [$display(y = -8.75)$])
#pagebreak()

#slide(7, $display((7 m)/8 - m/4 = 5/6)$)
#pagebreak()
#slide(7, $display((7 m)/8 - m/4 = 5/6)$, answer: [$display(m = 4/3)$])
#pagebreak()

#slide(8, $display(0.05x + 0.25(60 - x) = 0.15(60))$)
#pagebreak()
#slide(8, $display(0.05x + 0.25(60 - x) = 0.15(60))$, answer: [$display(x = 30)$])
#pagebreak()

#slide(9, $display((5 m)/4 - m/12 = 7/6)$)
#pagebreak()
#slide(9, $display((5 m)/4 - m/12 = 7/6)$, answer: [$display(m = 1)$])
#pagebreak()

#slide(10, $display(3/20 = 3/10w + 3/4)$)
#pagebreak()
#slide(10, $display(3/20 = 3/10w + 3/4)$, answer: [$display(w = -2)$])
#pagebreak()

#slide(11, $display(0.25x + 0.55(40 - x) = 0.40(40))$)
#pagebreak()
#slide(11, $display(0.25x + 0.55(40 - x) = 0.40(40))$, answer: [$display(x = 20)$])
#pagebreak()

#slide(12, $display((0.25) (36) = 0.15x + 0.35 (36 - x))$)
#pagebreak()
#slide(12, $display((0.25) (36) = 0.15x + 0.35 (36 - x))$, answer: [$display(x = 18)$])
#pagebreak()

#slide(13, $display((5 m)/6 - m/3 = 5/4)$)
#pagebreak()
#slide(13, $display((5 m)/6 - m/3 = 5/4)$, answer: [$display(m = 5/2)$])
#pagebreak()

#slide(14, $display(0.6(y - 0.5) = 2 - 0.4(1 - y))$)
#pagebreak()
#slide(14, $display(0.6(y - 0.5) = 2 - 0.4(1 - y))$, answer: [$display(y = 9.5)$])
#pagebreak()

#slide(15, $display(0.10x + 0.40(50 - x) = 0.28(50))$)
#pagebreak()
#slide(15, $display(0.10x + 0.40(50 - x) = 0.28(50))$, answer: [$display(x = 20)$])
#pagebreak()

#slide(16, $display(7/45 = 4/15w + 5/9)$)
#pagebreak()
#slide(16, $display(7/45 = 4/15w + 5/9)$, answer: [$display(w = -3/2)$])
#pagebreak()

#slide(17, $display((8x + 12)/4 = (5x - 25)/5)$)
#pagebreak()
#slide(17, $display((8x + 12)/4 = (5x - 25)/5)$, answer: [$display(x = -8)$])
#pagebreak()

#slide(18, $display(2000 - 6(2x + 10) = 1100)$)
#pagebreak()
#slide(18, $display(2000 - 6(2x + 10) = 1100)$, answer: [$display(x = 70)$])
#pagebreak()

#slide(19, $display(2400 - 5(4x + 20) = 1500)$)
#pagebreak()
#slide(19, $display(2400 - 5(4x + 20) = 1500)$, answer: [$display(x = 40)$])
#pagebreak()

#slide(20, $display(1 / 3 (k - 4) = 5 / 6)$)
#pagebreak()
#slide(20, $display(1 / 3 (k - 4) = 5 / 6)$, answer: [$display(k = 13/2)$])
#pagebreak()

#slide(21, $display(20a + 22.5 = 12.5(a + 3))$)
#pagebreak()
#slide(21, $display(20a + 22.5 = 12.5(a + 3))$, answer: [$display(a = 2)$])
#pagebreak()

#slide(22, $display(((x - 7)) / 3 + 2x = 7)$)
#pagebreak()
#slide(22, $display(((x - 7)) / 3 + 2x = 7)$, answer: [$display(x = 4)$])
#pagebreak()

#slide(23, $display(360 = 18(4t - 6))$)
#pagebreak()
#slide(23, $display(360 = 18(4t - 6))$, answer: [$display(t = 6.5)$])
#pagebreak()

#slide(24, $display(8y = (24 - 32y)/4 + 6)$)
#pagebreak()
#slide(24, $display(8y = (24 - 32y)/4 + 6)$, answer: [$display(y = 0.75)$])
#pagebreak()

#slide(25, $display(1080 = h/6 + h/12)$)
#pagebreak()
#slide(25, $display(1080 = h/6 + h/12)$, answer: [$display(h = 4320)$])
#pagebreak()

#slide(26, $display(7 + (8x - 6) / 2 = 20)$)
#pagebreak()
#slide(26, $display(7 + (8x - 6) / 2 = 20)$, answer: [$display(x = 4)$])
#pagebreak()

#slide(27, $display(18(4 - m) = 36(-m/2 + 3))$)
#pagebreak()
#slide(27, $display(18(4 - m) = 36(-m/2 + 3))$, answer: [no solution])
#pagebreak()

#slide(28, $display(11 / 6x - 1 / 3x = 6)$)
#pagebreak()
#slide(28, $display(11 / 6x - 1 / 3x = 6)$, answer: [$display(x = 4)$])
#pagebreak()

#slide(29, $display((q + 4)/3 = (q - 3)/2)$)
#pagebreak()
#slide(29, $display((q + 4)/3 = (q - 3)/2)$, answer: [$display(q = 17)$])
#pagebreak()

#slide(30, $display((3 (x + 2)) / 4 - 5 = 10)$)
#pagebreak()
#slide(30, $display((3 (x + 2)) / 4 - 5 = 10)$, answer: [$display(x = 18)$])
#pagebreak()

#slide(31, $display((12x + 16)/4 = (6x - 42)/6)$)
#pagebreak()
#slide(31, $display((12x + 16)/4 = (6x - 42)/6)$, answer: [$display(x = -5.5)$])
#pagebreak()

#slide(32, $display(13 - 6(2 - x) = 43)$)
#pagebreak()
#slide(32, $display(13 - 6(2 - x) = 43)$, answer: [$display(x = 7)$])
#pagebreak()

#slide(33, $display(1/4 (n - 8) = -5n + 7)$)
#pagebreak()
#slide(33, $display(1/4 (n - 8) = -5n + 7)$, answer: [$display(n = 12/7)$])
#pagebreak()

#slide(34, $display(1.08x + 0.02x + 12 = 45)$)
#pagebreak()
#slide(34, $display(1.08x + 0.02x + 12 = 45)$, answer: [$display(x = 30)$])
#pagebreak()

#slide(35, $display(1/8(6(x - 2) + 28) = x)$)
#pagebreak()
#slide(35, $display(1/8(6(x - 2) + 28) = x)$, answer: [$display(x = 8)$])
#pagebreak()

#slide(36, $display(14(6 - 3m) = 84(-m/2 + 2))$)
#pagebreak()
#slide(36, $display(14(6 - 3m) = 84(-m/2 + 2))$, answer: [no solution])
#pagebreak()

#slide(37, $display(6x - 0.75 (x + 4) + 5 = 23)$)
#pagebreak()
#slide(37, $display(6x - 0.75 (x + 4) + 5 = 23)$, answer: [$display(x = 4)$])
#pagebreak()

#slide(38, $display(1800 - 8(3x + 10) = 1000)$)
#pagebreak()
#slide(38, $display(1800 - 8(3x + 10) = 1000)$, answer: [$display(x = 30)$])
#pagebreak()

#slide(39, $display(7/8 (8d + 16) = 6(d - 2) + 4)$)
#pagebreak()
#slide(39, $display(7/8 (8d + 16) = 6(d - 2) + 4)$, answer: [$display(d = -22)$])
#pagebreak()

#slide(40, $display(100(x - 0.6) = -30(2x + 0.8))$)
#pagebreak()
#slide(40, $display(100(x - 0.6) = -30(2x + 0.8))$, answer: [$display(x = 0.225)$])
#pagebreak()

#slide(41, $display(8x + 5 = 7.5x + 9)$)
#pagebreak()
#slide(41, $display(8x + 5 = 7.5x + 9)$, answer: [$display(x = 8)$])
#pagebreak()

#slide(42, $display(20 + 5.4n = 8 + 6n)$)
#pagebreak()
#slide(42, $display(20 + 5.4n = 8 + 6n)$, answer: [$display(n = 20)$])
#pagebreak()

#slide(43, $display(6(p - 12) = 90)$)
#pagebreak()
#slide(43, $display(6(p - 12) = 90)$, answer: [$display(p = 27)$])
#pagebreak()

#slide(44, $display(7(x - 8) = 189)$)
#pagebreak()
#slide(44, $display(7(x - 8) = 189)$, answer: [$display(x = 35)$])
#pagebreak()

#slide(45, $display(1 / 5 (4x + 3) = 11)$)
#pagebreak()
#slide(45, $display(1 / 5 (4x + 3) = 11)$, answer: [$display(x = 13)$])
#pagebreak()

#slide(46, $display(-0.55t - 0.55t - 3.4 = -7.8)$)
#pagebreak()
#slide(46, $display(-0.55t - 0.55t - 3.4 = -7.8)$, answer: [$display(t = 4)$])
#pagebreak()

#slide(47, $display(9(2x + 5) = 15x + 63)$)
#pagebreak()
#slide(47, $display(9(2x + 5) = 15x + 63)$, answer: [$display(x = 6)$])
#pagebreak()

#slide(48, $display(-5(4 + 3h) = 4h + 18)$)
#pagebreak()
#slide(48, $display(-5(4 + 3h) = 4h + 18)$, answer: [$display(h = -2)$])
#pagebreak()

#slide(49, $display(((x - 5)) / 7 - 2 = 3)$)
#pagebreak()
#slide(49, $display(((x - 5)) / 7 - 2 = 3)$, answer: [$display(x = 40)$])
#pagebreak()

#slide(50, $display(7(x + 2) = 8x + 5 + 2x)$)
#pagebreak()
#slide(50, $display(7(x + 2) = 8x + 5 + 2x)$, answer: [$display(x = 3)$])
#pagebreak()

#slide(51, $display(((x + 12)) / 6 + 5 = 9)$)
#pagebreak()
#slide(51, $display(((x + 12)) / 6 + 5 = 9)$, answer: [$display(x = 12)$])
#pagebreak()

#slide(52, $display((8x + 10)/2 - 5 = 4x)$)
#pagebreak()
#slide(52, $display((8x + 10)/2 - 5 = 4x)$, answer: [all real numbers])
#pagebreak()

#slide(53, $display(x + (x + 1) + (x + 2) = 96)$)
#pagebreak()
#slide(53, $display(x + (x + 1) + (x + 2) = 96)$, answer: [$display(x = 31)$])
#pagebreak()

#slide(54, $display(7(x - 3) = 14x)$)
#pagebreak()
#slide(54, $display(7(x - 3) = 14x)$, answer: [$display(x = -3)$])
#pagebreak()

#slide(55, $display(70 - 5p = 40 - 3.5p)$)
#pagebreak()
#slide(55, $display(70 - 5p = 40 - 3.5p)$, answer: [$display(p = 20)$])
#pagebreak()

#slide(56, $display(-10 = -11t + 14 + 5 t)$)
#pagebreak()
#slide(56, $display(-10 = -11t + 14 + 5 t)$, answer: [$display(t = 4)$])
#pagebreak()

#slide(57, $display(9(n - 6) = 7(n + 4))$)
#pagebreak()
#slide(57, $display(9(n - 6) = 7(n + 4))$, answer: [$display(n = 41)$])
#pagebreak()

#slide(58, $display(0.875(x + 4) - 7 = 0)$)
#pagebreak()
#slide(58, $display(0.875(x + 4) - 7 = 0)$, answer: [$display(x = 4)$])
#pagebreak()

#slide(59, $display(5(x + 6) = x + 6)$)
#pagebreak()
#slide(59, $display(5(x + 6) = x + 6)$, answer: [$display(x = -6)$])
#pagebreak()

#slide(60, $display(5w - 28 = 2(6w - 7))$)
#pagebreak()
#slide(60, $display(5w - 28 = 2(6w - 7))$, answer: [$display(w = -2)$])
#pagebreak()

#slide(61, $display(8(h - 0.25) = 7h)$)
#pagebreak()
#slide(61, $display(8(h - 0.25) = 7h)$, answer: [$display(h = 2)$])
#pagebreak()

#slide(62, $display(10(x + 3) = 4x)$)
#pagebreak()
#slide(62, $display(10(x + 3) = 4x)$, answer: [$display(x = -5)$])
#pagebreak()

#slide(63, $display(-7k + 2 = -10 - 9k)$)
#pagebreak()
#slide(63, $display(-7k + 2 = -10 - 9k)$, answer: [$display(k = -6)$])
#pagebreak()

#slide(64, $display(84 = -3(2r - 6))$)
#pagebreak()
#slide(64, $display(84 = -3(2r - 6))$, answer: [$display(r = -11)$])

