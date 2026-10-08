# Manual

1. [The lesson set](#1-the-lesson-set)
2. [Making practice sets from the command line](#2-making-practice-sets-from-the-command-line)
3. [The terminal app](#3-the-terminal-app)
4. [What gets written](#4-what-gets-written)
5. [Adding problems](#5-adding-problems)
6. [Checking your changes](#6-checking-your-changes)
7. [Troubleshooting](#7-troubleshooting)

## 1. The lesson set

`gen_sequence.py` holds the 50 lesson equations, the worked steps for the
guide, and the rules about which problems get worked out. Run it, then
compile:

```sh
python3 gen_sequence.py [--class NAME] && (cd lesson_1-4 && for f in *.typ; do typst compile "$f"; done)
```

| Output | Contents |
|---|---|
| `lesson_1-4_literal_seq_worksheet` | Problems 1–50 under type headings, each with a one-line hint |
| `lesson_1-4_literal_seq_key` | The same, with answers in red |
| `lesson_1-4_literal_seq_slides` | A title slide per type, then a problem slide and an answer slide; the worked examples get step-by-step answer slides |
| `lesson_1-4_literal_seq_guide` | For each type: Look for, The move, and a worked example; the special cases are worked in full, with a "Watch out" note |
| `lesson_1-4_literal_seq_all_solutions` | The textbook equations and the 50 lesson equations, each solved for every variable |
| `lesson_1-4_literal_seq_bank.json` | Everything above as data |

The script stops with an error if an answer or a worked step fails its
numeric check. It also stops if the types don't cover problems 1–50 exactly
once, in order.

**Editing the lesson.** The type names, hints, problem ranges, and worksheet
spacing are in `TYPES` in `literal_common.py`. The equations are in `EQ`,
and the worked steps are in `STEPS`, `ALT`, `NOTICE`, and `PITFALL`, all in
`gen_sequence.py`. A worked step is `("equation", "note")`. The first
equation must be the problem itself, and the last must be `target = answer`.

## 2. Making practice sets from the command line

```sh
python3 make_practice.py [options]
```

| Option | Meaning | Default |
|---|---|---|
| `--mix TYPE:COUNT ...` | How many problems of each type. Types are `1`–`11`, `A`, `B`, or `all`. Repeated entries add up: `all:1 3:2` gives three of Type 3 and one of everything else. | `all:2` |
| `--versions N` | Number of different versions | 1 |
| `--seed S` | Same seed → same problems | random (printed) |
| `--style` | `mixed`: about 30% real formulas. `letters`: made-up equations only. `formulas`: real formulas whenever the type has any left. | `mixed` |
| `--shuffle` | Interleave the types, with no headings | grouped |
| `--title TEXT` | Title on the worksheet and slides | Literal Equations Practice |
| `--class NAME` | Class name in the worksheet and slide header | Algebra 1 |
| `--out DIR` | Output folder, relative to the script's folder | `practice` |
| `--name NAME` | File prefix | `literal_practice` |
| `--no-compile` | Write `.typ` files only | compile |
| `--selftest N` | Draw N problems of every type, check them all, then check every formula | |

Examples:

```sh
# Three equal-difficulty quiz versions
python3 make_practice.py --mix 2:2 3:2 4:2 8:2 A:1 --versions 3 --title "Quiz 1-4" --name quiz_1-4

# Mixed review, interleaved
python3 make_practice.py --mix all:1 --shuffle

# Warm-up from real formulas
python3 make_practice.py --mix 1:4 3:4 B:2 --style formulas
```

**Guarantees:**
- Problems never repeat within a run, across versions, or with the 50 lesson
  problems.
- Every answer is solved by sympy, written out in classroom form, and checked
  numerically.
- **Answer forms:**
  - Answers come as a single fraction, with as few minus signs as possible.
  - Terms are listed in the order they appear in the problem.
  - Common letter factors are pulled out: `y(b + 8)`.
  - Numbers are pulled out only in denominators: `2(ℓ + w)`.
  - A student's correct answer may still be in a different but equivalent
    form.

## 3. The terminal app

```sh
python3 practice_tui.py                                    # start empty
python3 practice_tui.py --mix 3:6 8:4 --seed 12            # start from a mix
python3 practice_tui.py practice/literal_practice_v1.json  # reopen a set
```

It takes the same options as `make_practice.py`, apart from `--no-compile`
and `--selftest`.

**Screen.** The left pane lists the types with their counts (`·` means
zero), then the settings. Under the list is a hint for the row under the
cursor. The right pane previews the problems. The preview uses the same
code and seed as `:w`, so it shows exactly what will be written. The status
line shows the mode, the totals, the seed, and `[+]` when there are
unwritten changes.

### Keys

**Moving**

| Keys | Action |
|---|---|
| `j` `k` / arrows | Down / up. A count repeats: `5j`. |
| `gg` `G` | First / last row. `7G` or `7gg` goes to row 7. |
| `/text` `n` `N` | Search type names and settings; next / previous match |
| `Ctrl-D` `Ctrl-U` | Half a page down / up (scrolls the preview when it has focus) |
| `Ctrl-F` `Ctrl-B` | A full page down / up in the preview |
| `Tab`, `Ctrl-W w` | Switch between panes. `Ctrl-W h` and `Ctrl-W l` pick one. |

**Changing the row under the cursor.** These work whichever pane has focus.

| Keys | Action |
|---|---|
| `l` `+` `→` `Ctrl-A` | Add one; `3l` adds three. On *style* and *order*, cycles to the next choice. |
| `h` `-` `←` `Ctrl-X` | Take one away, or cycle back |
| `x` `dd` | Set the count to 0 (on *versions*, back to 1) |
| `i` `a` `Enter` | Type a new value, starting from the current one |
| `cc` `s` | Erase the value, then type a new one |
| `D` | Zero every type |
| `u` `Ctrl-R` | Undo / redo (counts work: `3u`) |
| `.` | Repeat the last change on the current row |
| `r` | New random seed |

While typing a value: `Enter` accepts, `Esc` cancels, `Ctrl-U` erases the
line, and `Ctrl-W` erases a word.

**Preview**

| Keys | Action |
|---|---|
| `za` | Show / hide answers |
| `gt` `gT` | Next / previous version; `3gt` goes to version 3 |

**Commands.** Type `:` and the command, then press Enter. `↑` and `↓` scroll
through earlier commands.

| Command | Action |
|---|---|
| `:w` | Write and compile every version |
| `:wq` `:x` `ZZ` | Write, then quit |
| `:q` | Quit. If there are unwritten changes, it refuses with *E37*. |
| `:q!` `ZQ` | Quit and discard |
| `:mix 3:6 8:4 A:2` | Replace all counts (`all:N` works) |
| `:clear` | Zero all counts |
| `:seed` / `:seed N` | Pick a random seed / set it |
| `:versions N` `:style X` `:order grouped` `:title TEXT` `:class NAME` `:name N` `:out DIR` | Set a setting |
| `:set shuffle` `noshuffle` `shuffle!` | Shuffle on / off / toggle |
| `:set answers` `noanswers` `answers!` | Answers in the preview |
| `:set key=value ...` | Set settings: `:set style=letters versions=3`. `title=` and `class=` take the rest of the line. |
| `:e FILE.json` | Load the settings and seed from a written set |
| `:open [sheet\|key\|slides] [N]` | Open version N's PDF (default: worksheet, version 1) |
| `:N` | Go to row N |
| `:help` or `?` | Show the keys |

`Ctrl-C` doesn't quit (same as vim); use `:q!` instead. The app needs a
terminal of at least 72×14. It works without color, and it shows more of
each type name when the terminal is wider than 100 columns.

## 4. What gets written

For each version N, in the output folder:

| File | Contents |
|---|---|
| `NAME_vN.typ` / `.pdf` | Worksheet with the Name/Date/Ver header and workspace sized by type |
| `NAME_vN_key.typ` / `.pdf` | The same, with answers in red |
| `NAME_vN_slides.typ` / `.pdf` | Title slide, a title slide per type (grouped only), then a problem slide and an answer slide for each problem |
| `NAME_vN.json` | The command, seed, version, and every problem (`type`, `prompt`, `target`, `answer`, `source`) |

Prompts and answers are stored as Typst math. Paste one into a Typst file
as `$display(...)$`.

## 5. Adding problems

**A real formula.** Add a line to `FORMULAS` in `make_practice.py`:

```python
("I = p r t", "p", "1"),        # equation, variable to solve for, type
```

You only give the equation; the script works out and checks the answer. Run
`--selftest 1` to confirm it passes. Before you assign a type, think through
the steps a student would take. The same formula can be a different type for
a different variable.

**A template.** A template is a function that takes a `D` (a source of random
letters and numbers that never repeats a letter within a problem). It
returns `(equation, unknown)`:

```python
def t8_f(d):
    x, a, b, k = d.x(), d.v(), d.coef(), d.const()
    need(lettered(a, b) and a != b)          # reject draws that change the type
    return f"{a} {x} + {k} = {b} {x}", x
```

Add it to that type's list in `TEMPLATES`. The helpers:

| Helper | Gives you |
|---|---|
| `d.x()`, `d.v()` | A fresh lowercase letter |
| `d.S()` | A fresh "subject" letter, upper- or lowercase |
| `d.n(lo, hi)` | An integer |
| `d.coef()` | A coefficient: a number from 2 to 9, or a letter |
| `d.const()` | A term on its own: a number from 2 to 15, or a letter |
| `d.prod()` | A richer coefficient: `2 pi`, `a b`, `3 a`, `a^2`, ... |
| `d.frac()` | `p, q` in lowest terms |
| `d.pm()`, `d.pick(...)`, `d.ch(p)` | Random sign, choice, or coin flip |
| `fr(n, d)` | A Typst fraction with the right parentheses |
| `co(n, v)` | `n v`, or just `v` when n is 1 |
| `need(cond)` | Throws the draw away and tries again |

Rules that keep templates honest:

- **Write Typst math with spaces between factors:** `a x`, `3 x`, `2 pi r`.
  Always use `fr()` for fractions; `a/b c` means (a/b)·c.
- **Build each type's move into the template's shape.** For example, Type 8
  needs the unknown on both sides, and at least one coefficient must be a
  letter (otherwise it's just Type 2). Use `need()` to throw out draws that
  turn into another type.
- **Keep the unknown's term positive,** except in Special Case A.
- After adding a template, **read a sample** as well as running the self-test.
  The self-test proves the answers are right; only reading proves the
  problems are the right type.

## 6. Checking your changes

```sh
python3 make_practice.py --selftest 100     # every type and every formula
python3 tests/test_tui_keys.py              # TUI key handling
python3 tests/screen_test.py 80 24 ":mix all:1\r" wait3 @    # the real screen (needs pyte)
python3 gen_sequence.py                     # lesson set: answers and worked steps
```

To confirm a refactor changed nothing, write a set with a fixed seed and
`--no-compile`, before and after, and compare the folders with `diff -r`.

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `could not draw a Type N problem` | Its templates reject almost every draw; loosen the `need()` conditions |
| `typst failed on ...` | Usually Typst syntax in a template or formula. Check the `.typ` file it names; the full error is in the message. |
| `FileNotFoundError: ... mixed_review` | The style preambles are missing; see Requirements in the README |
| The TUI shows `typst not found: .typ only` | Install Typst, or compile the `.typ` files somewhere else |
| `:open` does nothing | It uses `xdg-open`; open the PDF from the output folder instead |
