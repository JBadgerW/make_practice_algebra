#set page(paper: "us-letter", margin: (x: 0.75in, y: 0.7in), numbering: "1")
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: false)

// Worked steps: rows of (left side, =, right side, note).
#let steps(note-size: 0.85em, last: 1fr, ..rows) = grid(
  columns: (auto, auto, auto, last),
  column-gutter: 0.45em,
  row-gutter: 1.15em,
  align: (right + horizon, center + horizon, left + horizon, left + horizon),
  ..rows.pos().map(((l, r, n)) => (l, $=$, r,
    text(size: note-size, fill: luma(90), style: "italic", n))).flatten()
)

#let type-sec(lbl, title, look, move, probs) = block(sticky: true, below: 0.9em)[
  #text(size: 14pt, weight: "bold")[#lbl: #title]
  #v(-0.3em)
  #line(length: 100%, stroke: 0.5pt)
  #v(-0.2em)
  *Look for:* #look \
  *The move:* #move \
  *Worksheet problems:* #probs
]

#let example(n, prob, body) = block(breakable: false, inset: (left: 1.2em), below: 1.4em)[
  *Problem #n.* #h(0.4em) #prob
  #v(0.2em)
  #pad(left: 1em, body)
]

#let callout(title, body) = block(breakable: false, width: 100%, inset: 0.6em,
  stroke: (left: 2pt + luma(120)), fill: luma(245), below: 1.2em)[*#title* #h(0.3em) #body]

#align(center)[
  #text(size: 17pt, weight: "bold")[Literal Equations: A Strategy for Each Type]
  #v(-0.4em)
  #text(size: 12pt)[Lesson 1-4 #h(0.6em) Worked Examples]
]
#v(0.5em)

Every literal equation is solved the same way an ordinary equation is: undo what has been done to the unknown, in reverse order, doing the same thing to both sides. The types below are ordered so each one adds one new move to the moves before it. Work out what the *first* move is, and the rest follows. Problem numbers refer to the Literal Equations by Type worksheet. An answer in a different but equivalent form (for example, $(P - 2 ell)/2$ instead of $P/2 - ell$) is still correct.
#v(0.6em)

#type-sec([Type 1], [One Step], [The unknown is tied to the rest by a single operation: $+$, $-$, $times$, or $div$.], [Undo that one operation on both sides.], [1, 2, 3, 4, 5, 6, 7, 8])
#example(1, [$display(a = b + 9)$; #h(0.3em) solve for $b$], [
  #steps(
    ([$display(a)$], [$display(b + 9)$], []),
    ([$display(a - 9)$], [$display(b)$], [subtract 9 from both sides]),
    ([$display(b)$], [$display(a - 9)$], [rewrite with $b$ on the left]),
  )
])

#type-sec([Type 2], [Add or Subtract, Then Divide], [No fractions. The unknown's term has other terms added to it or subtracted from it.], [Undo the adding or subtracting first, then divide by the unknown's coefficient.], [9, 10, 11, 12])
#example(9, [$display(y = 3x + 5)$; #h(0.3em) solve for $x$], [
  #steps(
    ([$display(y)$], [$display(3x + 5)$], []),
    ([$display(y - 5)$], [$display(3x)$], [subtract 5]),
    ([$display((y - 5)/3)$], [$display(x)$], [divide by 3]),
    ([$display(x)$], [$display((y - 5)/3)$], [rewrite with $x$ on the left]),
  )
])

#type-sec([Type 3], [Clear One Denominator], [One fraction bar (or a fraction coefficient like $1/3$), and no parentheses to distribute.], [Multiply both sides by the denominator; then add or subtract and divide as usual.], [13, 14, 15, 16, 17, 18])
#example(13, [$display(V = 1/3 B h)$; #h(0.3em) solve for $B$], [
  #steps(
    ([$display(V)$], [$display(1/3 B h)$], []),
    ([$display(3V)$], [$display(B h)$], [multiply both sides by 3]),
    ([$display((3V)/h)$], [$display(B)$], [divide by $h$]),
    ([$display(B)$], [$display((3V)/h)$], [rewrite with $B$ on the left]),
  )
])

#type-sec([Type 4], [Distribute First], [The unknown is inside parentheses, with a number or letter multiplying the group.], [Distribute; then add or subtract like terms and divide.], [19, 20, 21, 22, 23, 24])
#example(19, [$display(P = 2(ell + w))$; #h(0.3em) solve for $w$], [
  #steps(
    ([$display(P)$], [$display(2(ell + w))$], []),
    ([$display(P)$], [$display(2 ell + 2w)$], [distribute the 2]),
    ([$display(P - 2 ell)$], [$display(2w)$], [subtract $2 ell$]),
    ([$display((P - 2 ell)/2)$], [$display(w)$], [divide by 2]),
    ([$display(w)$], [$display((P - 2 ell)/2)$], [same as $P/2 - ell$]),
  )
])

#type-sec([Type 5], [Clear a Denominator, Then Distribute], [A fraction and a set of parentheses.], [Multiply both sides by the denominator first, then distribute and solve.], [25, 26, 27])
#example(25, [$display(p = 3/4 (q - 8))$; #h(0.3em) solve for $q$], [
  #steps(
    ([$display(p)$], [$display(3/4 (q - 8))$], []),
    ([$display(4p)$], [$display(3(q - 8))$], [multiply both sides by 4]),
    ([$display(4p)$], [$display(3q - 24)$], [distribute the 3]),
    ([$display(4p + 24)$], [$display(3q)$], [add 24]),
    ([$display((4p + 24)/3)$], [$display(q)$], [divide by 3]),
    ([$display(q)$], [$display((4p + 24)/3)$], [same as $4/3 p + 8$]),
  )
])

#type-sec([Type 6], [Clear Two Denominators], [Two different fractions in the equation.], [Multiply every term on both sides by both denominators, which clears both fractions at once.], [28, 29])
#example(28, [$display(a/b = c/d)$; #h(0.3em) solve for $b$], [
  #steps(
    ([$display(a/b)$], [$display(c/d)$], []),
    ([$display(a d)$], [$display(c b)$], [multiply both sides by $b d$]),
    ([$display((a d)/c)$], [$display(b)$], [divide by $c$]),
    ([$display(b)$], [$display((a d)/c)$], [rewrite with $b$ on the left]),
  )
])

#type-sec([Type 7], [Factor Out, Then Divide], [The unknown appears in two terms that are already together on one side.], [Factor the unknown out of those terms, then divide by what is left in the parentheses.], [30, 31])
#example(30, [$display(a y - b y = c)$; #h(0.3em) solve for $y$], [
  #steps(
    ([$display(a y - b y)$], [$display(c)$], []),
    ([$display(y(a - b))$], [$display(c)$], [factor out $y$]),
    ([$display(y)$], [$display(c/(a - b))$], [divide by $(a - b)$]),
  )
])

#type-sec([Type 8], [Gather, Factor Out, Divide], [The unknown appears on both sides of the equation.], [Add or subtract to get every term with the unknown on one side and everything else on the other; then factor out and divide.], [32, 33, 34, 35])
#example(32, [$display(k x = 2x + 5)$; #h(0.3em) solve for $x$], [
  #steps(
    ([$display(k x)$], [$display(2x + 5)$], []),
    ([$display(k x - 2x)$], [$display(5)$], [subtract $2x$]),
    ([$display(x(k - 2))$], [$display(5)$], [factor out $x$]),
    ([$display(x)$], [$display(5/(k - 2))$], [divide by $(k - 2)$]),
  )
])

#type-sec([Type 9], [Distribute, Gather, Factor Out, Divide], [Parentheses, and the unknown shows up in more than one term.], [Distribute first; then gather, factor out, and divide as in Type 8.], [36, 37, 38])
#example(36, [$display(m(x + 2) = 5x - n)$; #h(0.3em) solve for $x$], [
  #steps(
    ([$display(m(x + 2))$], [$display(5x - n)$], []),
    ([$display(m x + 2m)$], [$display(5x - n)$], [distribute the $m$]),
    ([$display(m x + 2m + n)$], [$display(5x)$], [add $n$]),
    ([$display(2m + n)$], [$display(5x - m x)$], [subtract $m x$ (gather the $x$-terms on the right)]),
    ([$display(2m + n)$], [$display(x(5 - m))$], [factor out $x$]),
    ([$display(x)$], [$display((2m + n)/(5 - m))$], [divide by $(5 - m)$]),
  )
])

#type-sec([Type 10], [Clear Single-Term Denominators, Then Solve], [Fractions whose denominators are single numbers or letters.], [Multiply both sides by every denominator to clear the fractions; what is left is a Type 9 (or easier) equation.], [39, 40, 41])
#example(39, [$display((x - a)/b = (x + c)/d)$; #h(0.3em) solve for $x$], [
  #steps(
    ([$display((x - a)/b)$], [$display((x + c)/d)$], []),
    ([$display(d(x - a))$], [$display(b(x + c))$], [multiply both sides by $b d$]),
    ([$display(d x - a d)$], [$display(b x + b c)$], [distribute]),
    ([$display(d x - b x)$], [$display(a d + b c)$], [subtract $b x$, add $a d$]),
    ([$display(x(d - b))$], [$display(a d + b c)$], [factor out $x$]),
    ([$display(x)$], [$display((a d + b c)/(d - b))$], [divide by $(d - b)$]),
  )
])

#type-sec([Type 11], [Clear a Multi-Term Denominator], [A denominator that is a sum or difference, such as $(x - 1)$.], [Multiply both sides by the whole denominator, keeping its parentheses; then distribute and solve as in Type 9.], [42, 43, 44, 45])
#example(42, [$display(t = d/(r + s))$; #h(0.3em) solve for $r$], [
  #steps(
    ([$display(t)$], [$display(d/(r + s))$], []),
    ([$display(t(r + s))$], [$display(d)$], [multiply both sides by $(r + s)$]),
    ([$display(t r + t s)$], [$display(d)$], [distribute the $t$]),
    ([$display(t r)$], [$display(d - t s)$], [subtract $t s$]),
    ([$display(r)$], [$display((d - t s)/t)$], [divide by $t$; same as $d/t - s$]),
  )
])

#pagebreak()
#align(center, text(size: 16pt, weight: "bold")[Special Cases])
#v(0.3em)
#type-sec([Special Case A], [Watch the Sign], [The term with the unknown has a minus sign in front of it.], [Add that term to both sides so it is positive on the other side, then solve. (If you leave it where it is, divide by the negative coefficient, not the positive one.)], [46, 47])
#example(46, [$display(a - b = c)$; #h(0.3em) solve for $b$], [
  #callout([Notice:], [Before moving anything, look at the sign *in front of* the unknown: here it is $-b$, not $b$.])
  #steps(
    ([$display(a - b)$], [$display(c)$], []),
    ([$display(a)$], [$display(c + b)$], [add $b$ to both sides: now $b$ is positive]),
    ([$display(a - c)$], [$display(b)$], [subtract $c$]),
    ([$display(b)$], [$display(a - c)$], [rewrite with $b$ on the left]),
  )
  #v(0.6em)
  _Or, leaving the negative term where it is:_
  #v(0.3em)
  #steps(
    ([$display(a - b)$], [$display(c)$], []),
    ([$display(-b)$], [$display(c - a)$], [subtract $a$]),
    ([$display(b)$], [$display(a - c)$], [multiply (or divide) both sides by $-1$]),
  )
  #v(0.6em)
  #callout([Watch out:], [Writing $b = c - a$. Check with numbers: if $a = 10$ and $c = 3$, then $10 - b = 3$ gives $b = 7$, but $c - a = -7$.])
])
#example(47, [$display(4x - 3y = 12)$; #h(0.3em) solve for $y$], [
  #callout([Notice:], [The $y$ term is $-3y$. The coefficient of $y$ is $-3$, not 3.])
  #steps(
    ([$display(4x - 3y)$], [$display(12)$], []),
    ([$display(4x)$], [$display(12 + 3y)$], [add $3y$ to both sides: now $3y$ is positive]),
    ([$display(4x - 12)$], [$display(3y)$], [subtract 12]),
    ([$display((4x - 12)/3)$], [$display(y)$], [divide by 3]),
    ([$display(y)$], [$display((4x - 12)/3)$], [rewrite with $y$ on the left]),
  )
  #v(0.6em)
  _Or, leaving the negative term where it is:_
  #v(0.3em)
  #steps(
    ([$display(4x - 3y)$], [$display(12)$], []),
    ([$display(-3y)$], [$display(12 - 4x)$], [subtract $4x$]),
    ([$display(y)$], [$display((12 - 4x)/(-3))$], [divide by $-3$, not by 3]),
    ([$display(y)$], [$display((4x - 12)/3)$], [the negative flips both signs on top]),
  )
  #v(0.6em)
  #callout([Watch out:], [From $-3y = 12 - 4x$, dividing by 3 instead of $-3$ gives $y = (12 - 4x)/3$, which has every sign wrong.])
])

#type-sec([Special Case B], [Finish with a Square Root], [The unknown is squared.], [Solve for the squared term as usual, then take the square root of both sides. These unknowns are lengths, so use the positive root.], [48, 49, 50])
#example(48, [$display(A = 4 pi r^2)$; #h(0.3em) solve for $r$], [
  #steps(
    ([$display(A)$], [$display(4 pi r^2)$], []),
    ([$display(A/(4 pi))$], [$display(r^2)$], [divide by $4 pi$]),
    ([$display(sqrt(A/(4 pi)))$], [$display(r)$], [take the positive square root]),
    ([$display(r)$], [$display(sqrt(A/(4 pi)))$], [rewrite with $r$ on the left]),
  )
])
#example(49, [$display(V = pi r^2 h)$; #h(0.3em) solve for $r$], [
  #steps(
    ([$display(V)$], [$display(pi r^2 h)$], []),
    ([$display(V/(pi h))$], [$display(r^2)$], [divide by $pi h$]),
    ([$display(sqrt(V/(pi h)))$], [$display(r)$], [take the positive square root]),
    ([$display(r)$], [$display(sqrt(V/(pi h)))$], [rewrite with $r$ on the left]),
  )
])
#example(50, [$display(F = (k q_1 q_2)/r^2)$; #h(0.3em) solve for $r$], [
  #steps(
    ([$display(F)$], [$display((k q_1 q_2)/r^2)$], []),
    ([$display(F r^2)$], [$display(k q_1 q_2)$], [multiply both sides by $r^2$]),
    ([$display(r^2)$], [$display((k q_1 q_2)/F)$], [divide by $F$]),
    ([$display(r)$], [$display(sqrt((k q_1 q_2)/F))$], [take the positive square root]),
  )
])

