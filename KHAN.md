# Khan Academy Courses

Three courses of banks, one bank per Khan Academy lesson, ported from the old
worksheet app's Khan-keyed sets (`PreAlg_*`, `Alg1_*`, `Alg2_*`):

| Course | Banks | Package |
|---|---|---|
| Khan Prealgebra | 7 (Units 1, 3, 6, 8) | `sheets/banks/khan_pre/` (`kpa_UU_LL`) |
| Khan Algebra 1 | 76 (Units 1, 2, 6, 8, 11, 13, 15) | `sheets/banks/khan_alg1/` (`ka1_UU_LL`) |
| Khan Algebra 2 | 30 (Units 1, 2, 3) | `sheets/banks/khan_alg2/` (`ka2_UU_LL`) |

Each bank's title is Khan's, `Lesson 2-6: Number of solutions to equations`,
so the lessons sort in order within a unit; its name, `ka1_02_06`, is
permanent. Its types are the lesson's distinct shapes, in Khan's order.

The old sets were the spec, not the code: their shapes, number ranges, and
the Khan items copied into them. Every problem is drawn new, and every
answer is checked by machine before anything is written. Most old items
had no answers; where they did, the errors found are listed in
`KHAN_PORT.md` (section 6), and none survives here.

## Using them

```sh
# Two of each type of Lesson 2-6 (Khan Algebra 1), for the course's header
python3 make_practice.py --mix ka1_02_06/all:2 --class "Khan Algebra 1"

# A unit review: six from anywhere in each of three lessons
python3 make_practice.py --mix 'ka2_02_06/any:6' 'ka2_02_07/any:6' 'ka2_02_08/any:6' --class "Khan Algebra 2" --title "Complex Numbers"
```

In `mathsheet.py`, choose the course on the COURSE row (`:course Khan
Algebra 1`); the banks are grouped under Khan's units. Two lessons reuse
another's bank under their own course: Prealgebra 6-2 is Algebra 1's 1-1,
and Algebra 2's 1-1 is Algebra 1's 13-1.

## How the keys write answers

- **Multiple choice stays** where Khan used it, with Khan's choices (or
  wrong ones made from real mistakes). The key gives the letter and the
  choice, `B. x = −4`; "choose all" gives every right one, `A, C`. Where
  the answers would bunch up (Yes/No, one/none/many), they're spread
  evenly over a sheet.
- **Exact numbers:** fractions, not decimals (`−9/4`), unless the problem
  says how to round.
- **Polynomials** in standard form; **factored completely**, the common
  factor first and a power of the letter before the binomials
  (`3x(x − 4)(x − 1)²`). A product that leads with its numbers is keyed in
  ascending order, as Khan does (`(5 + x)(5 − x) = 25 − x²`).
- **Systems:** `x = 2, y = −5`. Linear functions from points or tables in
  slope-intercept form.
- **Complex numbers** in `a + bi` form; `±` for a pair of roots. Khan's dot
  stays in products (`5i · (3 − 2i)`).
- **Word problems** use names, not pronouns, and give their units.
- **Graphs** (cetz, `sheets/graphs.py`): the key marks the answer on the
  graph in red, and writes it beside. Where Khan asks to mark points or
  draw a graph, the student writes the coordinates or draws on the grid,
  and the key draws the answer.

## How the answers are checked

Each bank's check works the answer out again without using how the
problem was made:

- **Expressions and equations:** the answer's value against the prompt's
  (substituted, or compared exactly with sympy), and its form read from its
  text: standard form, completely factored, simplest radical, `a + bi`.
- **Multiple choice:** every choice is tested; exactly the key's letters are right.
- **Word problems:** the numbers are read back out of the story and the
  problem solved forward.
- **Graphs:** the answer is read off the graph that's drawn: the points it
  goes through, or a smooth curve whose turns and crossings are known exactly
  (`khan_alg1/curves.py`). A function test runs the vertical line test,
  endpoints included.

A few types have only so many different problems, as Khan's do: the square
roots of the perfect squares to 400 (20), the cube roots of the perfect
cubes to 1728 (12), Algebra 2's square roots of negative perfect squares
(20). Asking for more of one of those than it has stops with *could not
draw*; mix in another type instead.

A few questions are interpretations (what a statement or a point means in a
story). Their checks confirm the key fits the story's numbers and the
graph, not the wording.

## The lessons

**Khan Prealgebra**

*Unit 1: Factors and multiples*

| Lesson | Bank | Types |
|---|---|---|
| 1-1: Factor pairs | `kpa_01_01` | 1 Which Are Factor Pairs? · 2 A Rectangle's Sides · 3 Complete the Table |
| 1-2: Identify factors | `kpa_01_02` | 1 List All the Factors · 2 Which Equation Shows a Factor? · 3 Which Number Is a Factor? |
| 1-3: Relate factors and multiples | `kpa_01_03` | 1 Factors and Multiples from a Product · 2 What Is Shaded? · 3 Find the Mistake |

*Unit 3: Ratios and rates*

| Lesson | Bank | Types |
|---|---|---|
| 3-9: Equivalent ratio word problems | `kpa_03_09` | 1 Find the Amount · 2 Complete the Ratio |

*Unit 6: Variables & expressions*

| Lesson | Bank | Types |
|---|---|---|
| 6-2: Evaluating expressions with one variable | `kpa_06_02` | 1 Add or Subtract · 2 Multiply or Divide · 3 Two Operations |

*Unit 8: Percent & rational number word problems*

| Lesson | Bank | Types |
|---|---|---|
| 8-1: Equivalent expressions with percent problems | `kpa_08_01` | 1 Percent Change Expressions |
| 8-2: Percent problems | `kpa_08_02` | 1 The New Amount or the Change · 2 The Original Amount · 3 The Percent Change · 4 Did They Meet the Goal? |

**Khan Algebra 1**

*Unit 1: Algebra foundations*

| Lesson | Bank | Types |
|---|---|---|
| 0-1: First introduction to algebra | `ka1_00_01` | 1 Add or Subtract · 2 Multiply or Divide |
| 1-1: Evaluating expressions with one variable | `ka1_01_01` | 1 Add or Subtract · 2 Multiply or Divide · 3 Two Operations |

*Unit 2: Solving equations & inequalities*

| Lesson | Bank | Types |
|---|---|---|
| 2-1: Equations with variables on both sides | `ka1_02_01` | 1 Variables on Both Sides · 2 Combine Like Terms First |
| 2-2: Equations with variables on both sides: decimals & fractions | `ka1_02_02` | 1 Decimals · 2 Fractions |
| 2-3: Equations with parentheses | `ka1_02_03` | 1 Distribute, Then Solve · 2 Distribute, Then Combine · 3 A Minus Sign Before Parentheses |
| 2-4: Equations with parentheses: decimals & fractions | `ka1_02_04` | 1 Decimals · 2 Fractions |
| 2-5: Reasoning with linear equations | `ka1_02_05` | 1 Which Move? |
| 2-6: Number of solutions to equations | `ka1_02_06` | 1 Distribute First · 2 Combine Like Terms First |
| 2-7a: Number of solutions to equations challenge | `ka1_02_07a` | 1 Which Equations? |
| 2-8: Linear equations with unknown coefficients | `ka1_02_08` | 1 Letters for Numbers · 2 Like Terms to Combine · 3 Distribute First |
| 2-9: Multi-step linear inequalities | `ka1_02_09` | 1 Variables on Both Sides |
| 2-10: Using inequalities to solve problems | `ka1_02_10` | 1 How Many? · 2 One More Step |
| 2-11: Compound inequalities | `ka1_02_11` | 1 AND · 2 OR |

*Unit 6: Systems of equations*

| Lesson | Bank | Types |
|---|---|---|
| 6-1: Solutions of systems of equations | `ka1_06_01` | 1 Check a Point |
| 6-2: Systems of equations with graphing | `ka1_06_02` | 1 Read the Solution · 2 Choose the Solution |
| 6-3: Creating systems in context | `ka1_06_03` | 1 Two Totals · 2 A Total and a Comparison · 3 Ages |
| 6-4: Interpret points relative to a system | `ka1_06_04` | 1 What Does the Point Mean? |
| 6-5: Systems of equations with substitution | `ka1_06_05` | 1 Solved for y · 2 Solved for x |
| 6-6: Combining equations | `ka1_06_06` | 1 Add the Equations · 2 Subtract the Equations |
| 6-7: Elimination strategies | `ka1_06_07` | 1 Which Strategies Work? |
| 6-8: Systems of equations with elimination | `ka1_06_08` | 1 Opposite Coefficients |
| 6-9: Systems of equations with elimination challenge | `ka1_06_09` | 1 Multiply One Equation · 2 Multiply Both Equations |
| 6-10: Reasoning with systems of equations | `ka1_06_10` | 1 Which Move? |
| 6-11: Number of solutions to a system of equations graphically | `ka1_06_11` | 1 How Many Solutions? |
| 6-12: Number of solutions to a system of equations algebraically | `ka1_06_12` | 1 Slope-Intercept Form · 2 A Multiple of an Equation |
| 6-13: Age word problems | `ka1_06_13` | 1 Older By, and Years Ago · 2 Times as Old, and Older By · 3 Times as Old, Now and Years Ago · 4 Into the Future |
| 6-14: Systems of equations word problems | `ka1_06_14` | 1 Two Totals · 2 A Total and a Comparison |
| 6-15: Systems of equations word problems (with zero and infinite solutions) | `ka1_06_15` | 1 Is There a Unique Answer? · 2 Enough Information? |

*Unit 8: Functions*

| Lesson | Bank | Types |
|---|---|---|
| 8-1: Evaluate functions | `ka1_08_01` | 1 Linear Functions · 2 With a Fraction or a Decimal |
| 8-2: Evaluate functions from their graph | `ka1_08_02` | 1 Read f(a) off the Graph |
| 8-3: Evaluate function expressions | `ka1_08_03` | 1 Combine Two Functions' Values |
| 8-4: Function inputs & outputs: equation | `ka1_08_04` | 1 Input from an Output |
| 8-5: Function inputs & outputs: graph | `ka1_08_05` | 1 The One Input · 2 The Other Input · 3 Select All the Inputs |
| 8-6: Function rules from equations | `ka1_08_06` | 1 Output and Input Terms · 2 Both Letters on Both Sides · 3 Distribute First · 4 A Number with Each Letter |
| 8-7: Function notation word problems | `ka1_08_07` | 1 An Input and Its Output · 2 Comparing Outputs |
| 8-8: Domain and range from graph | `ka1_08_08` | 1 The Domain · 2 The Range |
| 8-9: Identifying values in the domain | `ka1_08_09` | 1 In the Domain or Not? |
| 8-10: Determine the domain of functions | `ka1_08_10` | 1 Domains |
| 8-11: Function domain word problems | `ka1_08_11` | 1 Integers or Real Numbers? |
| 8-12: Recognize functions from graphs | `ka1_08_12` | 1 Function or Not? |
| 8-13: Recognize functions from tables | `ka1_08_13` | 1 Numbers · 2 Words |
| 8-14: Relative maxima and minima | `ka1_08_14` | 1 Relative Maxima · 2 Relative Minima |
| 8-15: Absolute maxima and minima | `ka1_08_15` | 1 Absolute Maximum · 2 Absolute Minimum |
| 8-16: Positive and negative intervals | `ka1_08_16` | 1 Where Is It Positive or Negative? |
| 8-17: Increasing and decreasing intervals | `ka1_08_17` | 1 Increasing or Decreasing? |
| 8-18: Graph interpretation word problems | `ka1_08_18` | 1 Match Statements to Features |
| 8-19: Average rate of change: graphs & tables | `ka1_08_19` | 1 Over an Interval · 2 Which Interval? |
| 8-20: Average rate of change word problems | `ka1_08_20` | 1 When Was It Faster? · 2 The Average Rate |
| 8-21: Evaluate inverse functions | `ka1_08_21` | 1 From a Table · 2 From a Graph · 3 Graph the Inverse |
| 8-22: Finding inverses of linear functions | `ka1_08_22` | 1 Whole-Number Coefficients · 2 A Fraction Coefficient · 3 A Number Times a Sum |

*Unit 11: Exponents & radicals*

| Lesson | Bank | Types |
|---|---|---|
| 11-1: Multiply & divide powers (integer exponents) | `ka1_11_01` | 1 Multiply Powers · 2 Divide Powers |
| 11-2: Powers of products & quotients (integer exponents) | `ka1_11_02` | 1 Power of a Product · 2 Power of a Quotient |
| 11-3: Properties of exponents challenge (integer exponents) | `ka1_11_03` | 1 Equivalent Expressions · 2 Find the Mistake |
| 11-4: Square roots | `ka1_11_04` | 1 Perfect Squares |
| 11-5: Roots of decimals & fractions | `ka1_11_05` | 1 Fractions · 2 Decimals |
| 11-6: Cube roots | `ka1_11_06` | 1 Perfect Cubes |
| 11-7: Simplify square roots | `ka1_11_07` | 1 Numbers |
| 11-8: Simplify square roots (variables) | `ka1_11_08` | 1 Numbers and a Variable |
| 11-9: Simplify square-root expressions | `ka1_11_09` | 1 One Root · 2 Multiply Roots |

*Unit 13: Quadratics: Multiplying & factoring*

| Lesson | Bank | Types |
|---|---|---|
| 13-1: Polynomials intro | `ka1_13_01` | 1 Describe a Polynomial · 2 Standard Form · 3 Degree |
| 13-2: Multiply monomials by polynomials (basic): area model | `ka1_13_02` | 1 A Number Times a Polynomial · 2 An x Term Times a Polynomial |
| 13-3: Multiply binomials: area model | `ka1_13_03` | 1 Two Binomials |
| 13-4: Multiply binomials intro | `ka1_13_04` | 1 Two Binomials |
| 13-5: Multiply binomials | `ka1_13_05` | 1 Two Binomials |
| 13-6: Multiply difference of squares | `ka1_13_06` | 1 Sum Times Difference |
| 13-7: Multiply perfect squares of binomials | `ka1_13_07` | 1 Square of a Binomial |
| 13-8: GCF factoring introduction | `ka1_13_08` | 1 The Width of an Area Model · 2 Factor Out the GCF |
| 13-9: Factoring quadratics intro | `ka1_13_09` | 1 Factor the Trinomial · 2 A Missing Side |
| 13-10: Factoring quadratics with a common factor | `ka1_13_10` | 1 Common Factor First |
| 13-11: Factor quadratics by grouping | `ka1_13_11` | 1 Leading Coefficient Not 1 |
| 13-12: Difference of squares intro | `ka1_13_12` | 1 Factor a Difference of Squares · 2 A Missing Side |
| 13-13: Difference of squares | `ka1_13_13` | 1 Difference of Squares · 2 A Common Factor First |
| 13-14: Perfect squares intro | `ka1_13_14` | 1 Factor a Perfect Square · 2 The Side of a Square |
| 13-15: Perfect squares | `ka1_13_15` | 1 Perfect Square Trinomials · 2 A Common Factor First |

*Unit 15: Irrational numbers*

| Lesson | Bank | Types |
|---|---|---|
| 15-1: Classify numbers: rational & irrational | `ka1_15_01` | 1 Rational or Irrational? |
| 15-2: Rational vs. irrational expressions | `ka1_15_02` | 1 Numbers · 2 Rational and Irrational Letters |

**Khan Algebra 2**

*Unit 1: Polynomial arithmetic*

| Lesson | Bank | Types |
|---|---|---|
| 1-1: Polynomials intro | `ka2_01_01` | 1 Describe a Polynomial · 2 Standard Form · 3 Degree |
| 1-2: Average rate of change of polynomials | `ka2_01_02` | 1 Over an Interval · 2 Which Interval? |
| 1-3: Add polynomials (intro) | `ka2_01_03` | 1 Add Polynomials |
| 1-4: Subtract polynomials (intro) | `ka2_01_04` | 1 Subtract Polynomials |
| 1-5: Add & subtract polynomials | `ka2_01_05` | 1 Named Polynomials · 2 Subtract One from Another |
| 1-6: Multiply monomials | `ka2_01_06` | 1 Multiply Monomials |
| 1-7: Multiply monomials by polynomials: area model | `ka2_01_07` | 1 Monomial Times Polynomial |
| 1-8: Multiply monomials by polynomials | `ka2_01_08` | 1 Monomial Times Polynomial |
| 1-9: Multiply binomials by polynomials: area model | `ka2_01_09` | 1 Binomial Times Polynomial |
| 1-10: Multiply binomials by polynomials | `ka2_01_10` | 1 Binomial Times Trinomial · 2 Two Binomials with Squared Terms |
| 1-11: Polynomial special products: difference of squares | `ka2_01_11` | 1 Sum Times Difference |
| 1-12: Polynomial special products: perfect square | `ka2_01_12` | 1 Square of a Binomial |

*Unit 2: Complex numbers*

| Lesson | Bank | Types |
|---|---|---|
| 2-1: Simplify roots of negative numbers | `ka2_02_01` | 1 Perfect Squares · 2 Not Perfect Squares |
| 2-2: Powers of the imaginary unit | `ka2_02_02` | 1 Powers of i |
| 2-3: Parts of complex numbers | `ka2_02_03` | 1 Name the Parts · 2 Which Parts? |
| 2-4: Classify complex numbers | `ka2_02_04` | 1 Real, Purely Imaginary, or Complex? |
| 2-5: Plot numbers on the complex plane | `ka2_02_05` | 1 Plot the Number · 2 Name the Point |
| 2-6: Add & subtract complex numbers | `ka2_02_06` | 1 Add · 2 Subtract |
| 2-7: Multiply complex numbers (basic) | `ka2_02_07` | 1 A Real Number Times · 2 An Imaginary Number Times |
| 2-8: Multiply complex numbers | `ka2_02_08` | 1 Two Complex Numbers |
| 2-9: Solve quadratic equations: complex solutions | `ka2_02_09` | 1 The Quadratic Formula |

*Unit 3: Polynomial factorization*

| Lesson | Bank | Types |
|---|---|---|
| 3-1: Factor monomials | `ka2_03_01` | 1 The Missing Factor · 2 A Missing Side · 3 Who Factored It Correctly? |
| 3-2: Greatest common factor of monomials | `ka2_03_02` | 1 GCF of Three Monomials |
| 3-4: Factor higher degree polynomials | `ka2_03_04` | 1 A Common Factor First · 2 A Product of Quadratics · 3 Grouping |
| 3-5: Identify quadratic patterns | `ka2_03_05` | 1 Which Pattern? |
| 3-6: Factorization with substitution | `ka2_03_06` | 1 Find U and V, Then Factor |
| 3-7: Factor polynomials using structure | `ka2_03_07` | 1 Difference of Squares · 2 Perfect Squares |
| 3-8: Polynomial identities | `ka2_03_08` | 1 Which Are Identities? · 2 Find the Mistake |
| 3-9: Geometric series formula | `ka2_03_09` | 1 The Sum from a and r · 2 The Sum of a Written Series · 3 The First Term |
| 3-10: Finite geometric series word problems | `ka2_03_10` | 1 The Total · 2 The First Amount · 3 Which Expression? |

