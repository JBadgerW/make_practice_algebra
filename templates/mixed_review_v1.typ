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
#let worksheet-title = "Mixed Equations Review"
#let version = "1"

#first-page-header(class-name, worksheet-title, version: version)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(0.45(y - 0.2) = 5 - 0.25(1 - y))$ 
  ],
  question(space-below: 3em)[
    $display(0.25(y - 0.4) = 3 - 0.5(1 - y))$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display((0.40) (60) = 0.30x + 0.50 (60 - x))$ 
  ],
  question(space-below: 3em)[
    $display((0.35) (80) = 0.25x + 0.45 (80 - x))$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(5/36 = 7/18w + 11/12)$ 
  ],
  question(space-below: 3em)[
    $display(0.2(y - 0.5) = 4 - 0.6(1 - y))$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display((7 m)/8 - m/4 = 5/6)$ 
  ],
  question(space-below: 3em)[
    $display(0.05x + 0.25(60 - x) = 0.15(60))$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display((5 m)/4 - m/12 = 7/6)$ 
  ],
  question(space-below: 3em)[
    $display(3/20 = 3/10w + 3/4)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(0.25x + 0.55(40 - x) = 0.40(40))$ 
  ],
  question(space-below: 3em)[
    $display((0.25) (36) = 0.15x + 0.35 (36 - x))$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display((5 m)/6 - m/3 = 5/4)$ 
  ],
  question(space-below: 3em)[
    $display(0.6(y - 0.5) = 2 - 0.4(1 - y))$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(0.10x + 0.40(50 - x) = 0.28(50))$ 
  ],
  question(space-below: 3em)[
    $display(7/45 = 4/15w + 5/9)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display((8x + 12)/4 = (5x - 25)/5)$ 
  ],
  question(space-below: 3em)[
    $display(2000 - 6(2x + 10) = 1100)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(2400 - 5(4x + 20) = 1500)$ 
  ],
  question(space-below: 3em)[
    $display(1 / 3 (k - 4) = 5 / 6)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(20a + 22.5 = 12.5(a + 3))$ 
  ],
  question(space-below: 3em)[
    $display(((x - 7)) / 3 + 2x = 7)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(360 = 18(4t - 6))$ 
  ],
  question(space-below: 3em)[
    $display(8y = (24 - 32y)/4 + 6)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(1080 = h/6 + h/12)$ 
  ],
  question(space-below: 3em)[
    $display(7 + (8x - 6) / 2 = 20)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(18(4 - m) = 36(-m/2 + 3))$ 
  ],
  question(space-below: 3em)[
    $display(11 / 6x - 1 / 3x = 6)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display((q + 4)/3 = (q - 3)/2)$ 
  ],
  question(space-below: 3em)[
    $display((3 (x + 2)) / 4 - 5 = 10)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display((12x + 16)/4 = (6x - 42)/6)$ 
  ],
  question(space-below: 3em)[
    $display(13 - 6(2 - x) = 43)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(1/4 (n - 8) = -5n + 7)$ 
  ],
  question(space-below: 3em)[
    $display(1.08x + 0.02x + 12 = 45)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(1/8(6(x - 2) + 28) = x)$ 
  ],
  question(space-below: 3em)[
    $display(14(6 - 3m) = 84(-m/2 + 2))$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(6x - 0.75 (x + 4) + 5 = 23)$ 
  ],
  question(space-below: 3em)[
    $display(1800 - 8(3x + 10) = 1000)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(7/8 (8d + 16) = 6(d - 2) + 4)$ 
  ],
  question(space-below: 3em)[
    $display(100(x - 0.6) = -30(2x + 0.8))$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(8x + 5 = 7.5x + 9)$ 
  ],
  question(space-below: 3em)[
    $display(20 + 5.4n = 8 + 6n)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(6(p - 12) = 90)$ 
  ],
  question(space-below: 3em)[
    $display(7(x - 8) = 189)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(1 / 5 (4x + 3) = 11)$ 
  ],
  question(space-below: 3em)[
    $display(-0.55t - 0.55t - 3.4 = -7.8)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(9(2x + 5) = 15x + 63)$ 
  ],
  question(space-below: 3em)[
    $display(-5(4 + 3h) = 4h + 18)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(((x - 5)) / 7 - 2 = 3)$ 
  ],
  question(space-below: 3em)[
    $display(7(x + 2) = 8x + 5 + 2x)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(((x + 12)) / 6 + 5 = 9)$ 
  ],
  question(space-below: 3em)[
    $display((8x + 10)/2 - 5 = 4x)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(x + (x + 1) + (x + 2) = 96)$ 
  ],
  question(space-below: 3em)[
    $display(7(x - 3) = 14x)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(70 - 5p = 40 - 3.5p)$ 
  ],
  question(space-below: 3em)[
    $display(-10 = -11t + 14 + 5 t)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(9(n - 6) = 7(n + 4))$ 
  ],
  question(space-below: 3em)[
    $display(0.875(x + 4) - 7 = 0)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(5(x + 6) = x + 6)$ 
  ],
  question(space-below: 3em)[
    $display(5w - 28 = 2(6w - 7))$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(8(h - 0.25) = 7h)$ 
  ],
  question(space-below: 3em)[
    $display(10(x + 3) = 4x)$ 
  ],
)

#v(5em)

#grid(
  columns: (1fr, 1fr),
  rows: 1,
  question(space-below: 3em)[
    $display(-7k + 2 = -10 - 9k)$ 
  ],
  question(space-below: 3em)[
    $display(84 = -3(2r - 6))$ 
  ],
)

#v(5em)

