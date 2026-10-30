// Half-page warm-ups: added after refined_template.typ's definitions
// (answer-blank, question, instructions-block, qnum), so it doesn't compile
// on its own. A US Letter page turned sideways holds two identical halves;
// the back holds the answers, lettered and shuffled, twice.

#set page(flipped: true, margin: 0.5in)

#let half-gutter = 0.8in

#let warmup-header(class-name, title) = grid(
  columns: (1fr, auto),
  column-gutter: 0.5em,
  row-gutter: 1.2em,

  [#class-name],
  align(right)[Name #answer-blank(5cm)],

  text(size: 14pt, weight: "bold", title),
  align(right)[Date #answer-blank(2.5cm)],
)

// One half: the header, the instructions, then the problems. The body puts
// #v(1fr) after each row of problems, so the work space is shared evenly.
#let warmup-half(class-name, title, instructions: none, body) = block(
  height: 100%,
  breakable: false,
  {
    qnum.update(0)
    warmup-header(class-name, title)
    if instructions != none {
      v(0.6em)
      instructions-block(instructions)
    }
    v(1em)
    body
  },
)

// The back of one half: the answers in shuffled order, lettered A, B, ...
#let answer-half(title, answers) = block(
  height: 100%,
  breakable: false,
  {
    text(size: 14pt, weight: "bold")[#title — Answers]
    v(1em)
    grid(
      columns: (1fr, 1fr),
      column-gutter: 1em,
      row-gutter: 1.6em,
      ..answers.enumerate().map(((i, a)) => [*#numbering("A.", i + 1)* #h(0.4em) #a]),
    )
  },
)

// The teacher's look at the back, never printed for students: each entry is
// (answer, note, decoy?), the note naming its problem or the one it imitates.
#let answer-key(title, entries) = {
  text(size: 14pt, weight: "bold")[#title — Answers, with decoys marked]
  v(1em)
  grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 1em,
    row-gutter: 1.6em,
    ..entries.enumerate().map(((i, e)) => {
      let col = if e.at(2) { luma(130) } else { blue }
      [*#numbering("A.", i + 1)* #h(0.4em) #text(fill: if e.at(2) { luma(130) } else { black }, e.at(0)) #h(0.5em) #text(size: 9pt, fill: col, e.at(1))]
    }),
  )
}

// The same half on both sides of the page.
#let two-up(half) = columns(2, gutter: half-gutter)[#half #colbreak() #half]
