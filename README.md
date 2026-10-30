# Literal Equations by Type

Algebra 1 materials for solving literal equations (formulas) for a given
variable. The equations are sorted into eleven **types** by the first move
each one needs, plus two **special cases**.

The practice generator makes new problems of whatever types you choose, as
many versions as you like. It writes a worksheet, an answer key, and a
slide deck for each version. You can run it from the command line or from
a terminal app with vim keys.

The terminal app draws from a **library** of problem banks: generators, the
lesson's fifty, and banks you write yourself, each tagged with the courses it
belongs to (Algebra 1, Algebra 2, Advanced Math, ...), so you see one course's
banks at a time. Three courses follow Khan Academy lesson by lesson: Khan
Prealgebra, Khan Algebra 1, and Khan Algebra 2 (113 lessons; see
[KHAN.md](KHAN.md)).

Every answer, and every line of every worked example, is checked
numerically with sympy before anything is written.

## Quick start

```sh
# Practice sets from the command line (3f = real formulas of Type 3)
python3 make_practice.py --mix 3:6 3f:2 8:4 A:2 --versions 3 --seed 12

# Systems of three equations (another bank: name it before the entry)
python3 make_practice.py --mix systems/1:2 systems/4:4 systems/A:1 --versions 2

# Prealgebra: Single-Step Equations: six of each kind of fact
python3 make_practice.py --mix single_step/all:6 --title "Single-Step Equations"

# Algebra 1, Units 1-2 Cumulative Test: one of each of the 30 questions, two parallel versions
python3 make_practice.py --mix alg1_units_1_2_cumulative/all:1 --versions 2 --title "Units 1-2 Cumulative Test"

# Lesson 1-2: Modeling: five Level 3 skills, one problem each
python3 make_practice.py --mix modeling_1_2/3a:1 modeling_1_2/3b:1 modeling_1_2/3d:1 modeling_1_2/3f:1 modeling_1_2/3m:1 --title "Lesson 1-2: Modeling"

# Lesson 1-2: Solving Linear Equations: two of each type
python3 make_practice.py --mix equations_1_2/all:2 --title "Lesson 1-2: Solving Linear Equations"

# Lesson 1-6: Compound Inequalities (modeling): every story at every type, two parallel versions
python3 make_practice.py --mix modeling/all:1 --versions 2 --title "Lesson 1-6: Compound Inequalities"

# Lesson 1-7: Absolute Value Equations and Inequalities: two of each type
python3 make_practice.py --mix absolute/all:2 --title "Lesson 1-7: Absolute Value Equations and Inequalities"

# Lesson 1-7: Word Problems: every story at every type
python3 make_practice.py --mix absolute_words/all:1 --title "Lesson 1-7: Word Problems"

# Advanced Math: two of each type of complex fractions and rationalizing
python3 make_practice.py --mix adv_complex_fractions/all:2 adv_rationalize/all:2 --class "Advanced Math" --title "Review"

# Khan Algebra 1, Lesson 2-6: two of each type
python3 make_practice.py --mix ka1_02_06/all:2 --class "Khan Algebra 1"

# A half-page warm-up: two copies side by side, the answers shuffled on the back
python3 make_practice.py --mix adv_rationalize/all:2 --warmup --class "Advanced Math" --title "Warm Up"

# Build and edit a sheet interactively: add by type, then Tab to the sheet to
# reroll, resize, edit, and move problems (press ? inside for keys)
python3 mathsheet.py
```

The practice files go into `practice/` in the folder you run from (`--out`, or
`:out ~/Desktop` in mathsheet, changes it). mathsheet itself writes to the
folder you start it from; started from your home folder, it uses the folder
you last wrote to. See [MANUAL.md](MANUAL.md) for the
details.

## The types

| Key | Type | Lesson problems |
|---|---|---|
| 1 | One Step | 1–8 |
| 2 | Add or Subtract, Then Divide | 9–12 |
| 3 | Clear One Denominator | 13–18 |
| 4 | Distribute First | 19–24 |
| 5 | Clear a Denominator, Then Distribute | 25–27 |
| 6 | Clear Two Denominators | 28–29 |
| 7 | Factor Out, Then Divide | 30–31 |
| 8 | Gather, Factor Out, Divide | 32–35 |
| 9 | Distribute, Gather, Factor Out, Divide | 36–38 |
| 10 | Clear Single-Term Denominators, Then Solve | 39–41 |
| 11 | Clear a Multi-Term Denominator | 42–45 |
| A | Special Case: Watch the Sign | 46–47 |
| B | Special Case: Finish with a Square Root | 48–50 |

### Systems of three equations

A second family, in the `systems` bank, sorted the same way: by the first move.

| Key | Type | Look for |
|---|---|---|
| 1 | Back-Substitute | One equation has a single variable, another just two |
| 2 | Substitute First | One equation is already solved for a variable |
| 3 | One Variable Missing | One equation has only two of the variables |
| 4 | Eliminate | Every variable everywhere; some coefficients are 1 or −1 |
| 5 | Eliminate and Scale | Every variable everywhere; no coefficient is 1 or −1 |
| 6 | Clear Fractions and Decimals (Advanced Math) | Fraction and decimal coefficients; each equation is missing a variable |
| A | Special Case: No Solution | Left sides combine; constants don't |
| B | Special Case: Infinitely Many Solutions | One equation is a combination of the other two |

Solutions are integers from −9 to 9, coefficients at most 7 (or 12 in a
combined equation), constants at most 60, and no equation has a common
factor. Type 6 mixes fraction equations (like 1/3 x − 1/4 y = 2, right
sides with denominators up to 6) and decimal ones (like 0.4y + 0.2z = 2, in
tenths); clearing them leaves an integer system. Answers are ordered triples, `(2, −1, 3)`, or the words *no solution*
or *infinitely many solutions*. Each system is half width with 2.5in of work
space, its terms lined up in columns.

### Prealgebra: Single-Step Equations

The `single_step` bank, after the Single-Step Equations game of Precision
Teaching: Algebra. Each equation comes from one basic fact on the numbers 1 to
15 (a + b = c or a × b = c), showing two of its numbers and hiding the third.

| Key | Type | Forms |
|---|---|---|
| 1 | Addition | `x + a = c`, `a + x = c` |
| 2 | Subtraction | `x − a = b`, `c − x = a` (`x − 14 = 8`) |
| 3 | Multiplication | `ax = c` (`13x = 169`) |
| 4 | Division | `x/a = b`, `c/x = a` |

Answers are whole numbers from 1 up, written `x = 22`. The number next to x
is never 1 in multiplication or division. The check solves the prompt again
with sympy.

### Lesson 1-2: Modeling

The `modeling_1_2` bank: word problems that take one modeling decision at a
time, from the teacher's Lesson 1-2 modeling bank (100 problems built on the
Savvas 1-2 word problems). Each asks for one expression or equation, never a
solved value. Every problem of that bank is one a story here draws, word for
word, with the bank's answer; the stories also draw new numbers, letters,
names, and items. `tests/test_modeling_1_2.py` confirms all 100 when the bank
file is in `~/Documents/alg1/unit_1/lesson_1-2/`.

The types are the bank's difficulty levels. Each entry is one of the bank's
categories at that level, so a sequence can step through one skill at a time:

| Level | Type | Entries | Example |
|---|---|---|---|
| 1 | Direct Translation | 1a cost at a rate, 1b distance, 1c consecutive integers, 1d rows and stacks, 1e equal shares, 1f converting units, 1g verbal phrases | `15h`, `n + 1`, `108 / 4` |
| 2 | Two Operations or a Reversed Order | 2a budget equations, 2b consecutive integers, 2c discounts, 2d round trips, 2e mixtures, 2f percent of a number, 2g rate plus a fee, 2h totals from an average, 2i what's left, 2j equal shares, 2k related prices, 2l converting units, 2m verbal phrases | `15h + 25`, `x − 8`, `0.20n` |
| 3 | One Inference | 3a budget equations with a fee, 3b consecutive integers, 3c all but the last, 3d time from distance and rate, 3e groups, 3f mixtures, 3g percent equations, 3h salary plus bonuses, 3i what's left, 3j averages, 3k times that add up, 3l mixed units, 3m verbal phrases | `25 − x`, `0.10x`, `d / 2`, `n − 1` |
| 4 | Build a Quantity, Then Group It | 4a earnings equations, 4b mortar layers, 4c discounts, 4d percent of a total, 4e related prices, 4f converting units | `4(p − 15) = 108`, `3/8 (n − 1)` |
| 5 | Two Inferences Combined | 5a brick walls, 5b groups, 5c mixture equations, 5d trip times, 5e two items, one total | `8t + 2(t + 6) = 37` |

Answers are written as the bank writes them: products unevaluated where the
words give them (`6(20000)`, `0.15(25)`, `4(12) − 1 1/8`), percents as
two-place decimals (`0.10x`), and the rate before the fee (`3m + 12`). Where
the bank accepts other forms, the key shows them: `n + (n + 1) + (n + 2) (or
3n + 3)`. Only the source story's person gets a pronoun (Terrence, he); any
other name is repeated. The check reads the numbers, words, and letters back
out of the prompt with the story's template, works the quantity out with
sympy, and compares it with the key and every alternate (an equation may be
any nonzero multiple of the right one).

### Lesson 1-2: Solving Linear Equations

The `equations_1_2` bank: the one- to three-step equations (rated 1 to 3) of
the teacher's Lesson 1-2 and 1-3 equation banks, redrawn from templates.
Integer, decimal, and fraction coefficients appear in every type where the
lesson had them.

| Key | Type | Example |
|---|---|---|
| 1 | Two Steps | `5x + 12 = 37`, `x/4 + 7 = 12`, `1/3 x + 5 = 3`, `0.2r − 3 = 0.5` |
| 2 | Combine Like Terms First | `0.25 + t + 0.4 = 2`, `6x + 3(2x) = 48`, `x + (x + 1) + (x + 2) = 96` |
| 3 | Distribute First | `6(p − 12) = 90`, `84 = −3(2r − 6)`, `1/3 (2x + 1) = 15`, `0.045(q + 3) = 2.34` |
| 4 | Distribute, Then Combine | `−5x + 4(3x + 2) = 50`, `−(9 − 3x) + 5 = −10`, `0.875(x + 4) − 7 = 0` |
| 5 | A Binomial over a Number | `(x − 7)/4 − 3 = 5`, `6 + (x + 18)/3 = 9` |
| 6 | Variable on Both Sides | `7n − 23 = 3n + 5`, `40 − 3x = 8x`, `0.79s + 15 = 0.85s` |
| 7 | Distribute, Then Variable on Both Sides | `4(n − 9) = 3(n + 4)`, `3(x + 4) = 4x + 2 + x`, `x − 5 = −(x − 5)` |
| A | No Solution or All Real Numbers | `9b + 4 = 9b + 7`, `t − 14 = −(14 − t)`, `(8x + 10)/2 − 5 = 4x` |

### Lesson 1-3: Equations with Fractions, Decimals, and Parentheses

The `equations_1_3` bank: the four- and five-step equations (rated 4 and 5)
of the same two lesson banks.

| Key | Type | Example |
|---|---|---|
| 1 | Distribute a Subtraction | `11 − 3(4 − 2x) = 41`, `1500 − 4(2x + 25) = 600`, `300 = 12(4t − 3)` |
| 2 | Decimal Coefficients | `4x − 0.5(x + 2) + 3 = 16`, `1.025x + 0.05x + 40 = 61.5`, `20a + 22.5 = 12.5(a + 3)` |
| 3 | Clear One Denominator | `(3(x + 2))/4 − 5 = 10`, `4y = (10 − 16y)/2 + 3`, `1/4 (n − 8) = −5n + 7` |
| 4 | Clear Several Denominators | `4/3 x − 1/2 x = 5`, `960 = h/8 + h/4`, `(q + 2)/3 = (q − 1)/4` |
| 5 | Distribute on Both Sides | `3/4 (8d + 16) = 5(d − 2) + 2`, `0.25(y − 0.4) = 3 − 0.5(1 − y)` |
| 6 | Mixtures | `0.25(20) = 0.15x + 0.35(20 − x)` |
| A | No Solution or All Real Numbers | `12(5 − 2m) = 72(−m/3 + 1)` |

In both banks the key writes `x = 18`; a decimal when the prompt has decimals
(`r = 17.5`), otherwise a fraction in lowest terms (`n = 12/7`); *no
solution*; or *all real numbers*. The check solves the prompt again with
sympy and substitutes the key.

### Lesson 1-6: Compound Inequalities

Word problems in the `modeling` bank. Each one is the same model, a total
between two numbers made of a fixed part plus some count of a smaller item:
`low ≤ (amount)(one unit) + (one item)·n ≤ high`. Only the story changes, so
students set up the inequality instead of recognizing a story. The types
change only the amount of the fixed part:

| Key | Type | The fixed part |
|---|---|---|
| 1 | One Serving | one unit: 1 serving, 1 hour, 1 mile, 1 bottle |
| 2 | Whole-Number Servings | 2, 3, or 4 units |
| 3 | Fractional Servings | ½, 1½, 2, or 2½ units |

An entry is a type plus a story: `a` a dog's Calories (food and treats), `b` a
party budget (pavilion hours and guests), `c` workout minutes (miles run and
circuits), `d` punch ounces (bottles of juice and cans). So `modeling/3b:2` is
two fractional-hours party problems, and `modeling/all:1` is all twelve.
Versions of an entry keep its story and change its names and numbers. Bounds
are inclusive and built so the solved inequality has whole-number ends. The
key gives the model, written with the amount as a decimal (`510 ≤ 1.5(320) + 15t ≤ 540`),
the solved inequality (`2 ≤ t ≤ 4`), and the answer (*2 to 4 treats*). Each
problem is full width with 1.75in of work space.

### Lesson 1-7: Absolute Value Equations and Inequalities

The `absolute` bank, in teaching order. Every number on a problem and every
number met while solving it is between −20 and 20, and every solution is an
integer.

| Key | Type | Example |
|---|---|---|
| 1 | Absolute Value of x | `\|x\| = 5` |
| 2 | One Step Outside | `\|x\| + 4 = 12`, `\|x\| − 4 = 2`, `3\|x\| = 12`, `\|x\|/3 = 4` |
| 3 | One Step Inside | `\|x + 2\| = 10`, `\|x − 2\| = 10`, `\|2x\| = 10`, `\|x/2\| = 3` |
| 4 | Two Steps Inside | `\|2x − 3\| = 5`, `\|x/2 + 4\| = 5`, `\|(x − 1)/3\| = 5`, `\|10 − x\| = 4` |
| 5 | Steps Inside and Outside | `3\|x + 4\| − 2 = 13`, `7 − \|6x\| = 1` |
| 6 | No Solution | any of the above that reduces to `\|u\| = −3` |
| 7 | Inequalities with \|x\| | `\|x\| < 5`, `\|x\| >= 5`, `8 >= \|x\|` |
| 8 | Solving Absolute Value Inequalities | type 5's forms with <, >, ≤, ≥ |

The key writes `x = −2 or x = 6`, `−2 < x < 6`, `x ≤ −2 or x ≥ 6`, or *no
solution*. A problem never divides twice (no fraction inside a fraction).
In type 8, `b − a|u|` turns the sign around when you undo it. Each problem
is half width.

### Lesson 1-7: Word Problems

The `absolute_words` bank: an amount that must stay within a tolerance of a
target, `|amount − target| ≤ tolerance`. Type 1 is the phrases alone; types
2-4 are stories, and each type asks for more of the same story.

| Key | Type | Example key |
|---|---|---|
| 1 | Phrases for a Tolerance | *x is 125, give or take 20*: `\|x − 125\| ≤ 20` |
| 2 | Modeling the Amount | the boat's distance: `\|d − 80\| ≤ 10` |
| 3 | Writing the Amount as an Expression | distance = rate · time: `\|25t − 80\| ≤ 10` |
| 4 | Modeling and Solving | `\|25t − 80\| ≤ 10`, `2.8 ≤ t ≤ 3.6`, *2.8 to 3.6 hours* |

Type 1 uses ten phrases (*give or take*, *plus or minus*, *with a tolerance
of*, *within*, *no more than ... off from*, ...), a different one for each
problem on a sheet until all ten are used. *Less than* is the one phrase
keyed with `<`; the rest are `≤`. An entry of types 2-4 is a type plus a
story: `a` boat trip, `b` team hotel (which hotels), `c` road trip on cruise
control, `d` rectangle perimeter (drawn below the prompt, length x along the bottom and the width up the side; `2x + 2(w)`), `e`
phone cases (which cases are removed), `f` party budget (how many guests),
`g` gas purchase (gallons), `h` running. Story `e` has nothing to substitute,
so it has no Type 3 (`3e` doesn't exist). So `absolute_words/4b:2` is two
hotel problems to solve, and `absolute_words/all:1` is one of each. Every
solved bound is a decimal with at most two places (three for gallons, as on a
pump). Type 1 is half width; the stories are full width.

### Algebra 1: Units 1-2 Cumulative Test

The `alg1_units_1_2_cumulative` bank (Algebra 1, *Tests*): thirty types, one per
question of the Units 1-2 cumulative test, every one drawn new. Each type keeps its
question's logic and form (multiple choice, select all, blanks, parts) and
draws its own numbers. Each word problem picks from its own stories, written
fresh with the same logic as the original question (house numbers, jersey
numbers, or right-hand pages for consecutive integers; nuts or cheese by the
pound; trail mix or a coffee blend for the mixture model; and so on). Wrong
choices come from real mistakes: a sign not flipped, a fraction distributed
to one term, a reciprocal slope without its sign change, a tick misread on
the number line. The check works each question again from its numbers with
sympy and confirms that the key's letters are exactly the right choices.

| Keys | Topic |
|---|---|
| 1-3 | Sets of integers, ordering real numbers, rational results |
| 4-10 | Equations: fractions, consecutive integers, price per pound, a mixture model, literal equations, the square pyramid |
| 11-15 | Inequalities: no solution / all reals, compound, from a number line; absolute value equations and graphs |
| 16-28 | Lines: graphing, perpendicular, two points, a linear model, horizontal lines, justifying steps, point-slope and standard form, intercepts and solutions in context, parallel and perpendicular |
| 29-30 | Equivalent profit equations, the cone |

### Advanced Math

Twelve banks, tagged *Advanced Math → Additional Practice*, ported from the
old worksheet app's `AdvMath_*` sets (the 2025-26 midterm, Tests 4 and 5,
and the lesson sets). Every problem draws its own letters, as the old sets
did, and every answer is checked by machine: its value against the prompt,
and its form from its text.

| Bank | Title | Types |
|---|---|---|
| `adv_exponents` | Simplifying with Exponents | 1 Powers of Products and Quotients · 2 A Sum over a Monomial · 3 A Sum over a Power of a Product · 4 Letters in the Exponents |
| `adv_rationalize` | Rationalizing Denominators | 1 A Square Root in the Denominator · 2 i in the Denominator · 3 A Binomial with a Square Root · 4 A Complex Denominator |
| `adv_complex_fractions` | Complex Fractions | 1 A Sum over a Sum · 2 Nested Fractions · 3 Fractions with Powers |
| `adv_factoring` | Special Products with Letter Exponents | 1 Simplify by the Difference of Two Squares · 2 A Difference of Two Squares · 3 A Sum or Difference of Cubes · 4 A Greatest Common Factor with Letter Exponents |
| `adv_literal` | Literal Equations with Fractions | 1 The Unknown in a Numerator · 2 The Unknown in a Denominator · 3 The Unknown in Two Places |
| `adv_poly_division` | Polynomial Division | 1 Dividing by x + a, No Remainder · 2 Dividing by x + a, with a Remainder · 3 Dividing by a x + b |
| `adv_functions` | Functions | 1 Evaluating a Function · 2 Substituting an Expression · 3 Combining Functions · 4 The Domain · 5 Which Relations Are Functions? |
| `adv_variation` | Direct and Inverse Variation | 1 Directly as a Square, Inversely as Another · 2 Directly as a Cube, Inversely as Another · 3 Directly as One, Inversely as a Square |
| `adv_mixtures` | Mixture Problems | 1 Both Amounts, Given the Total · 2 One Amount, Given the Total · 3 One Amount, Given the Other · 4 Water or a Pure Ingredient |
| `adv_word` | Number, Coin, and Average Problems | 1 Digit Problems · 2 Coin Problems · 3 Averages |
| `adv_trig` | Trig Values and Polar Form | 1 Exact Trig Values · 2 Angles Past 90° · 3 Rectangular to Polar · 4 Polar to Rectangular |
| `adv_spheres` | Spheres | 1 Volume to Surface Area · 2 Surface Area to Volume |

How the keys write answers:

- **One fraction, multiplied out**, in lowest terms: `(x^3 + x y^4)/y^3`,
  `(3 + 2√2)/7`, `(9 − 2i)/5`.
- **Positive exponents only**; no radical and no `i` in a denominator.
- **A minus sign** goes into a denominator that is a sum, `(csv)/(kvy − aks)`,
  and otherwise in front, `−(x + 1)/(2x)`.
- **Every fraction in display style**, nested ones too (but not in
  exponents), so a complex fraction's parts are full size.
- **Factoring is complete**: `x^(4n) − 16 = (x^(2n) + 4)(x^n + 2)(x^n − 2)`.
- **Division**: quotient + remainder/divisor, `x² − x − 5 + 11/(x − 5)`.
- **Functions** name what they find: `f(−10) = 171`, `(f ∘ g)(2) = 8`; a
  domain is its conditions, `x ≥ −3, x ≠ 9`; relations, the letters of the
  functions.
- **Word problems** have whole-number (or exact) answers with their units,
  and use names only, no pronouns.
- **Polar form**: r to 0.1 and θ to 0.01°, four forms; rectangular to 0.01.

### Khan Academy courses

113 banks, one per Khan Academy lesson, tagged with Khan's courses and units:
*Khan Prealgebra* (7), *Khan Algebra 1* (76), and *Khan Algebra 2* (30).
They were ported from the old app's Khan-keyed sets. Multiple choice stays
where Khan used it, and graphs are drawn with cetz, the key marking the
answer in red. [KHAN.md](KHAN.md) lists every lesson and its types, and how
the keys write and check answers. `KHAN_PORT.md` is the port's record: the
decisions, each unit's approval, and the errors found in the old sets.

## Files

**Where problems live.** Written problems, sequences, and courses are JSON
in a *library*: the built-in one, `library/`, and your own,
`~/Documents/mathsheet-library` (see `library/README.md`). Generators, which
draw new problems, are Python code in `sheets/banks/`, so no library folder
ever runs code.

| File | What it is |
|---|---|
| `sheets/` | The shared package: `sheet.py` (the worksheet document), `edit.py` (changes to a sheet), `writer.py` (worksheet, key, and slide Typst), `check.py` (Typst-to-sympy parsing and numeric checks), `typst.py` (the Typst preambles), `banks/` (the bank interface, the loader for JSON banks, and the generators) |
| `sheets/library.py` | The library: finds every bank (generators, `library/`, and your library folder), reads `courses.json`, and groups banks by course and unit |
| `sheets/sequences.py` | Sequences: ordered steps through banks' entries (with notes on what changes, and pinned examples), read into the library |
| `sheets/banks/systems.py` | The systems-of-three-equations bank: types, templates, the sympy check, and the aligned Typst layout |
| `sheets/banks/alg1_units_1_2_cumulative.py` | The Algebra 1 Units 1-2 Cumulative Test bank: thirty question types, each drawn new with its own stories and mistake-based choices, and a check per type |
| `sheets/banks/single_step.py` | The Prealgebra single-step equations bank: one basic fact on 1 to 15 per equation, by kind of fact, and a sympy check |
| `sheets/banks/modeling_1_2.py` | The Lesson 1-2: Modeling bank: five levels, an entry per category, a story per problem shape of the teacher's bank, and a check that reads the prompt back with its story |
| `sheets/banks/equations_1_2.py`, `equations_1_3.py` | The Lesson 1-2 and 1-3 linear-equation banks: the types, a template per equation shape of the lessons' banks, and a sympy check (`sheets/linear.py`: `key`, `keyed`) |
| `sheets/banks/modeling.py` | The Lesson 1-6: Compound Inequalities bank: the four stories, the three types, and a check that reads the numbers back out of the prompt |
| `sheets/banks/absolute.py` | The Lesson 1-7: Absolute Value Equations and Inequalities bank: the eight types, the inside and outside templates, and a sympy check that solves the prompt again |
| `sheets/banks/absolute_words.py` | The Lesson 1-7: Word Problems bank: the ten phrases, the eight stories, the four types, and a check that reads the numbers back out of the prompt |
| `sheets/banks/literal/` | The literal-equation bank: `types.py`, `templates.py`, `formulas.py`, `answers.py` (solver and answer formatter), and drawing in `__init__.py` |
| `sheets/typmath.py` | sympy → Typst math as the key writes it (one fraction, positive exponents, terms by degree), and display-style fractions (`dfrac`) |
| `sheets/gen.py` | What the Advanced Math and Khan banks share: random helpers, letters and names, the type table, the draw-and-check loop (with answers spread evenly over a sheet where a bank asks), multiple choice, display and editing, and story templates for word problems |
| `sheets/banks/adv_*.py` | The twelve Advanced Math banks (see *Advanced Math* above) |
| `sheets/banks/khan_pre/`, `khan_alg1/`, `khan_alg2/` | The Khan Academy banks, one module per lesson (`kpa_`, `ka1_`, `ka2_`), with what each course's lessons share (systems, polynomials, stories, figures, curves; see [KHAN.md](KHAN.md)) |
| `sheets/linear.py`, `ineq.py`, `poly.py`, `radicals.py` | Shared math for those banks: one-variable equations and inequalities read and solved from their text, polynomials in standard and factored form, square roots in simplest form |
| `sheets/graphs.py` | Coordinate-plane graphs drawn with cetz: grids, axes, lines, curves, points; every coordinate worked out in Python |
| `KHAN.md`, `KHAN_PORT.md` | The Khan courses' reference, and the record of their port |
| `make_practice.py` | Practice generator: drafts a sheet from `--mix`/`--groups`/`--seed`, writes it, and the command line |
| `mathsheet.py` | mathsheet: the terminal worksheet editor (vim keys) |
| `tests/` | `test_mathsheet.py`, `test_library.py`, `test_typmath.py`, `test_khan.py` (every Khan type draws, checks, and shows), `test_modeling_1_2.py` (the Lesson 1-2 modeling bank, and its 100 source problems), and `test_graphs.py` (no terminal needed), and `screen_test.py` (draws the real screen; needs `pyte`) |
| `library/` | The built-in library: fixed banks (written problems as JSON; `lesson_1-4.json` is the lesson's fifty), the built-in sequence `literal_by_type.json` (the lesson's order, built by `lesson_sequence()` in `sheets/banks/literal`), and the starter `courses.json`. Your own banks go in your library folder (`~/Documents/mathsheet-library` by default; see the MANUAL). |
| `templates/` | Typst style headers shared by every worksheet and slide deck |
| `practice/` | Default output folder for practice sets |
| `PLAN.md` | The agreed plan for turning this into a general worksheet editor |
| `EXTENDING.md` | A brief for an LLM (or a person) turning this into a general worksheet builder |

## Requirements

- Python 3.10+ with **sympy** (tested with 1.13).
- **Typst** 0.15 to compile PDFs. Without it, the `.typ` files are still written.
  Graphs use Typst's **cetz** package (0.5.2): Typst downloads it the first
  time a sheet with a graph is compiled, so that one time needs the internet.
- The styles live in `templates/` and are read at run time: practice
  worksheets use `refined_template.typ`, and slides use `mixed_review_slides.typ`.
- Optional: `pyte`, only for `tests/screen_test.py`.

## Reproducibility

Each practice set is saved as `NAME.sheet.json`, which holds every problem
of every version; `python3 make_practice.py --sheet NAME.sheet.json` prints
it again exactly. The same settings and seed also always draft the same
sheet: each file begins with the command that does it, for example
`// Generated by: python3 make_practice.py --mix 3:6 8:4 A:2 --versions 2 --seed 12`,
and `mathsheet.py` opens the sheet to edit it.
