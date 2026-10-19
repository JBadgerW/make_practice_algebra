#set page(paper: "us-letter", margin: (x: 0.75in, y: 0.7in))
#set text(size: 11pt)
#set par(justify: false)
#set text(top-edge: "bounds", bottom-edge: "bounds")

#align(center)[
  #text(size: 16pt, weight: "bold")[Lesson 1-4: Literal Equations and Formulas]
  #v(-0.4em)
  #text(size: 12pt)[Every Equation Solved for Every Variable]
]
#v(0.6em)

#let eq(n, prompt, sols) = block(spacing: 1.3em, breakable: false)[
  #strong[#n] #h(0.6em) #prompt \
  #pad(left: 1.2em, sols)
]

#text(size: 9.5pt, style: "italic")[Square-root solutions give the positive root, since these variables stand for lengths and other positive quantities. A variable the equation is already solved for is not listed again. "(book)" marks the variable the textbook asks for; "(target)" marks the one asked on the worksheet.]

== Part 1: Equations from the Textbook
#v(0.4em)
#columns(2, gutter: 2em)[
  #eq([Try It 1a.], [$display(y = x + 12)$], [#box[$x = display(y - 12)$ #text(size: 9pt)[(book)]]])
  #eq([Try It 1b.], [$display(n = 4/5 (m + 7))$], [#box[$m = display(5/4 n - 7)$ #text(size: 9pt)[(book)]]])
  #eq([Ex. 2.], [$display(d = r t)$], [#box[$r = display(d/t)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$t = display(d/r)$]])
  #eq([Ex. 3.], [$display(P = 2 ell + 2 w)$], [#box[$w = display((P - 2 ell)/2)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$ell = display((P - 2 w)/2)$]])
  #eq([Try It 3.], [$display(A = 1/2 b h)$], [#box[$h = display((2A)/b)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$b = display((2A)/h)$]])
  #eq([Ex. 4.], [$display(C = 5/9 (F - 32))$], [#box[$F = display(9/5 C + 32)$ #text(size: 9pt)[(book)]]])
  #eq([Try It 4.], [$display(K = C + 273.15)$], [#box[$C = display(K - 273.15)$ #text(size: 9pt)[(book)]]])
  #eq([Example.], [$display(V = ell w h)$], [#box[$h = display(V/(ell w))$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$ell = display(V/(w h))$] #h(1.4em) #box[$w = display(V/(ell h))$]])
  #eq([Check 2.], [$display(2x + c = d)$], [#box[$x = display((d - c)/2)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$c = display(d - 2x)$]])
  #eq([Check 4.], [$display(g = (x - 1)/k)$], [#box[$x = display(g k + 1)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$k = display((x - 1)/g)$]])
  #eq([Check 5.], [$display(I = p r t)$], [#box[$p = display(I/(r t))$] #h(1.4em) #box[$r = display(I/(p t))$] #h(1.4em) #box[$t = display(I/(p r))$]])
  #eq([13.], [$display(b/c = a)$], [#box[$c = display(b/a)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$b = display(a c)$]])
  #eq([14.], [$display(2y + k = 6y - k y)$], [#box[$y = display(k/(4 - k))$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$k = display((4y)/(1 + y))$]])
  #eq([15.], [$display(F = 9/5 C + 32)$], [#box[$C = display(5/9 (F - 32))$ #text(size: 9pt)[(book)]]])
  #eq([16.], [$display(w = x/(a - b))$], [#box[$x = display(w(a - b))$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$a = display(x/w + b)$] #h(1.4em) #box[$b = display(a - x/w)$]])
  #eq([17.], [$display(A = ((b_1 + b_2) h)/2)$], [#box[$h = display((2A)/(b_1 + b_2))$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$b_1 = display((2A)/h - b_2)$] #h(1.4em) #box[$b_2 = display((2A)/h - b_1)$]])
  #eq([18.], [$display(y = m x + b)$], [#box[$m = display((y - b)/x)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$x = display((y - b)/m)$] #h(1.4em) #box[$b = display(y - m x)$]])
  #eq([19.], [$display(P V = n R T)$], [#box[$R = display((P V)/(n T))$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$P = display((n R T)/V)$] #h(1.4em) #box[$V = display((n R T)/P)$] #h(1.4em) #box[$n = display((P V)/(R T))$] #h(1.4em) #box[$T = display((P V)/(n R))$]])
  #eq([20.], [$display(A x + B y = C)$], [#box[$y = display((C - A x)/B)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$x = display((C - B y)/A)$] #h(1.4em) #box[$A = display((C - B y)/x)$] #h(1.4em) #box[$B = display((C - A x)/y)$] #h(1.4em) #box[$C = display(A x + B y)$]])
  #eq([21.], [$display(y - y_1 = m(x - x_1))$], [#box[$m = display((y - y_1)/(x - x_1))$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$y = display(m(x - x_1) + y_1)$] #h(1.4em) #box[$y_1 = display(y - m(x - x_1))$] #h(1.4em) #box[$x = display((y - y_1)/m + x_1)$] #h(1.4em) #box[$x_1 = display(x - (y - y_1)/m)$]])
  #eq([22.], [$display(12(m + 3x) = 18(x - 3m))$], [#box[$m = display(-(3x)/11)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$x = display(-(11m)/3)$]])
  #eq([23.], [$display(V = 1/3 pi r^2 h)$], [#box[$h = display((3V)/(pi r^2))$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$r = display(sqrt((3V)/(pi h)))$]])
  #eq([24.], [$display(V = 1/3 pi r^2 (h - 1))$], [#box[$h = display((3V)/(pi r^2) + 1)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$r = display(sqrt((3V)/(pi (h - 1))))$]])
  #eq([25.], [$display(y a - y b = c y + c a)$], [#box[$y = display((a c)/(a - b - c))$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$a = display((y(b + c))/(y - c))$] #h(1.4em) #box[$b = display((a y - c y - a c)/y)$] #h(1.4em) #box[$c = display((y(a - b))/(a + y))$]])
  #eq([26.], [$display(x = (3(y - b))/m)$], [#box[$y = display((m x)/3 + b)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$b = display(y - (m x)/3)$] #h(1.4em) #box[$m = display((3(y - b))/x)$]])
  #eq([27.], [$display(F = -(G m)/r^2)$], [#box[$G = display(-(F r^2)/m)$ #text(size: 9pt)[(book)]] #h(1.4em) #box[$m = display(-(F r^2)/G)$] #h(1.4em) #box[$r = display(sqrt(-(G m)/F))$]])
]

#pagebreak()
== Part 2: Worksheet Equations by Type
#v(0.4em)
#columns(2, gutter: 2em)[
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 1: One Step]]
  #eq([1.], [$display(a = b + 9)$], [#box[$b = display(a - 9)$ #text(size: 9pt)[(target)]]])
  #eq([2.], [$display(y = x - 7)$], [#box[$x = display(y + 7)$ #text(size: 9pt)[(target)]]])
  #eq([3.], [$display(m/n = p)$], [#box[$m = display(n p)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$n = display(m/p)$]])
  #eq([4.], [$display(C = pi d)$], [#box[$d = display(C/pi)$ #text(size: 9pt)[(target)]]])
  #eq([5.], [$display(F = m a)$], [#box[$a = display(F/m)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$m = display(F/a)$]])
  #eq([6.], [$display(P = I^2 R)$], [#box[$R = display(P/I^2)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$I = display(sqrt(P/R))$]])
  #eq([7.], [$display(E = m c^2)$], [#box[$m = display(E/c^2)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$c = display(sqrt(E/m))$]])
  #eq([8.], [$display(C = 2 pi r)$], [#box[$r = display(C/(2 pi))$ #text(size: 9pt)[(target)]]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 2: Add or Subtract, Then Divide]]
  #eq([9.], [$display(y = 3x + 5)$], [#box[$x = display((y - 5)/3)$ #text(size: 9pt)[(target)]]])
  #eq([10.], [$display(P = 2a + b)$], [#box[$a = display((P - b)/2)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$b = display(P - 2a)$]])
  #eq([11.], [$display(3x + c = d)$], [#box[$x = display((d - c)/3)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$c = display(d - 3x)$]])
  #eq([12.], [$display(v = u + a t)$], [#box[$a = display((v - u)/t)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$t = display((v - u)/a)$] #h(1.4em) #box[$u = display(v - a t)$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 3: Clear One Denominator]]
  #eq([13.], [$display(V = 1/3 B h)$], [#box[$B = display((3V)/h)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$h = display((3V)/B)$]])
  #eq([14.], [$display(A = 1/2 d_1 d_2)$], [#box[$d_1 = display((2A)/d_2)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$d_2 = display((2A)/d_1)$]])
  #eq([15.], [$display(y = (x - 4)/k)$], [#box[$x = display(k y + 4)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$k = display((x - 4)/y)$]])
  #eq([16.], [$display(M = (a b)/c)$], [#box[$c = display((a b)/M)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((M c)/b)$] #h(1.4em) #box[$b = display((M c)/a)$]])
  #eq([17.], [$display(y = 2/3 x + 4)$], [#box[$x = display(3/2 (y - 4))$ #text(size: 9pt)[(target)]]])
  #eq([18.], [$display(y = (a x + b)/c)$], [#box[$x = display((c y - b)/a)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((c y - b)/x)$] #h(1.4em) #box[$b = display(c y - a x)$] #h(1.4em) #box[$c = display((a x + b)/y)$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 4: Distribute First]]
  #eq([19.], [$display(P = 2(ell + w))$], [#box[$w = display(P/2 - ell)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$ell = display(P/2 - w)$]])
  #eq([20.], [$display(y - 5 = m(x + 2))$], [#box[$x = display((y - 5)/m - 2)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$m = display((y - 5)/(x + 2))$] #h(1.4em) #box[$y = display(m(x + 2) + 5)$]])
  #eq([21.], [$display(a_n = a_1 + (n - 1) d)$], [#box[$n = display((a_n - a_1)/d + 1)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$d = display((a_n - a_1)/(n - 1))$] #h(1.4em) #box[$a_1 = display(a_n - (n - 1) d)$]])
  #eq([22.], [$display(5(a - 2b) = 3c)$], [#box[$b = display((5a - 3c)/10)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((3c)/5 + 2b)$] #h(1.4em) #box[$c = display((5(a - 2b))/3)$]])
  #eq([23.], [$display(4(p + 2q) = 10(q - p))$], [#box[$p = display(q/7)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$q = display(7p)$]])
  #eq([24.], [$display(6(x - 2y) = 9(x + y))$], [#box[$y = display(-x/7)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$x = display(-7y)$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 5: Clear a Denominator, Then Distribute]]
  #eq([25.], [$display(p = 3/4 (q - 8))$], [#box[$q = display(4/3 p + 8)$ #text(size: 9pt)[(target)]]])
  #eq([26.], [$display(A = 1/2 h(a + b))$], [#box[$a = display((2A)/h - b)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$b = display((2A)/h - a)$] #h(1.4em) #box[$h = display((2A)/(a + b))$]])
  #eq([27.], [$display(S = (n(a + ell))/2)$], [#box[$ell = display((2S)/n - a)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((2S)/n - ell)$] #h(1.4em) #box[$n = display((2S)/(a + ell))$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 6: Clear Two Denominators]]
  #eq([28.], [$display(a/b = c/d)$], [#box[$b = display((a d)/c)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((b c)/d)$] #h(1.4em) #box[$c = display((a d)/b)$] #h(1.4em) #box[$d = display((b c)/a)$]])
  #eq([29.], [$display(x/a + y/b = 1)$], [#box[$y = display(b - (b x)/a)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$x = display(a - (a y)/b)$] #h(1.4em) #box[$a = display((b x)/(b - y))$] #h(1.4em) #box[$b = display((a y)/(a - x))$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 7: Factor Out, Then Divide]]
  #eq([30.], [$display(a y - b y = c)$], [#box[$y = display(c/(a - b))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display(c/y + b)$] #h(1.4em) #box[$b = display(a - c/y)$] #h(1.4em) #box[$c = display(a y - b y)$]])
  #eq([31.], [$display(A = P + P r t)$], [#box[$P = display(A/(1 + r t))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$r = display((A - P)/(P t))$] #h(1.4em) #box[$t = display((A - P)/(P r))$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 8: Gather, Factor Out, Divide]]
  #eq([32.], [$display(k x = 2x + 5)$], [#box[$x = display(5/(k - 2))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$k = display((2x + 5)/x)$]])
  #eq([33.], [$display(a x + b = c x + d)$], [#box[$x = display((d - b)/(a - c))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((c x + d - b)/x)$] #h(1.4em) #box[$b = display(c x + d - a x)$] #h(1.4em) #box[$c = display((a x + b - d)/x)$] #h(1.4em) #box[$d = display(a x + b - c x)$]])
  #eq([34.], [$display(5y + 2k = 9y - k y)$], [#box[$y = display((2k)/(4 - k))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$k = display((4y)/(2 + y))$]])
  #eq([35.], [$display(3x - 2a = a x + 7)$], [#box[$x = display((2a + 7)/(3 - a))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((3x - 7)/(x + 2))$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 9: Distribute, Gather, Factor Out, Divide]]
  #eq([36.], [$display(m(x + 2) = 5x - n)$], [#box[$x = display((2m + n)/(5 - m))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$m = display((5x - n)/(x + 2))$] #h(1.4em) #box[$n = display(5x - m(x + 2))$]])
  #eq([37.], [$display(2(a x - 3) = b x + 4)$], [#box[$x = display(10/(2a - b))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((b x + 10)/(2x))$] #h(1.4em) #box[$b = display((2a x - 10)/x)$]])
  #eq([38.], [$display(T = 2(ell w + w h + ell h))$], [#box[$h = display((T - 2 ell w)/(2(ell + w)))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$ell = display((T - 2 w h)/(2(w + h)))$] #h(1.4em) #box[$w = display((T - 2 ell h)/(2(ell + h)))$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 10: Clear Single-Term Denominators, Then Solve]]
  #eq([39.], [$display((x - a)/b = (x + c)/d)$], [#box[$x = display((a d + b c)/(d - b))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display(x - (b(x + c))/d)$] #h(1.4em) #box[$b = display((d(x - a))/(x + c))$] #h(1.4em) #box[$c = display((d(x - a))/b - x)$] #h(1.4em) #box[$d = display((b(x + c))/(x - a))$]])
  #eq([40.], [$display(1/a + 1/b = 1/c)$], [#box[$c = display((a b)/(a + b))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((b c)/(b - c))$] #h(1.4em) #box[$b = display((a c)/(a - c))$]])
  #eq([41.], [$display(E = 1/2 m v^2 + m g h)$], [#box[$m = display((2E)/(v^2 + 2 g h))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$h = display((2E - m v^2)/(2 m g))$] #h(1.4em) #box[$g = display((2E - m v^2)/(2 m h))$] #h(1.4em) #box[$v = display(sqrt((2(E - m g h))/m))$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Type 11: Clear a Multi-Term Denominator]]
  #eq([42.], [$display(t = d/(r + s))$], [#box[$r = display(d/t - s)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$s = display(d/t - r)$] #h(1.4em) #box[$d = display(t(r + s))$]])
  #eq([43.], [$display(y = (2x + 3)/(x - 1))$], [#box[$x = display((y + 3)/(y - 2))$ #text(size: 9pt)[(target)]]])
  #eq([44.], [$display(a = (b + c)/(b - c))$], [#box[$b = display((c(a + 1))/(a - 1))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$c = display((b(a - 1))/(a + 1))$]])
  #eq([45.], [$display(y = (a x)/(x + b))$], [#box[$x = display((b y)/(a - y))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display((y(x + b))/x)$] #h(1.4em) #box[$b = display((x(a - y))/y)$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Special Case A: Watch the Sign]]
  #eq([46.], [$display(a - b = c)$], [#box[$b = display(a - c)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$a = display(b + c)$]])
  #eq([47.], [$display(4x - 3y = 12)$], [#box[$y = display((4x - 12)/3)$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$x = display((3y + 12)/4)$]])
  #block(sticky: true, above: 1.2em)[#text(weight: "bold")[Special Case B: Finish with a Square Root]]
  #eq([48.], [$display(A = 4 pi r^2)$], [#box[$r = display(sqrt(A/(4 pi)))$ #text(size: 9pt)[(target)]]])
  #eq([49.], [$display(V = pi r^2 h)$], [#box[$r = display(sqrt(V/(pi h)))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$h = display(V/(pi r^2))$]])
  #eq([50.], [$display(F = (k q_1 q_2)/r^2)$], [#box[$r = display(sqrt((k q_1 q_2)/F))$ #text(size: 9pt)[(target)]] #h(1.4em) #box[$q_1 = display((F r^2)/(k q_2))$] #h(1.4em) #box[$q_2 = display((F r^2)/(k q_1))$] #h(1.4em) #box[$k = display((F r^2)/(q_1 q_2))$]])
]
