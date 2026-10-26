"""Drive mathsheet.App with scripted keys (no terminal needed).
Run from the project folder:  python3 tests/test_mathsheet.py"""
import os, re, shlex, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="config_")    # never the teacher's own config
(Path(os.environ["XDG_CONFIG_HOME"]) / "mathsheet").mkdir()
EMPTY_LIB = tempfile.mkdtemp(prefix="emptylib_")
(Path(os.environ["XDG_CONFIG_HOME"]) / "mathsheet" / "config.json").write_text(
    '{"library": "%s"}' % EMPTY_LIB)                                        # nor their library
import mathsheet as T, make_practice as mp
from sheets import sheet as sh, edit as E
PORTED = ("adv_", "ka1_", "ka2_", "kpa_")                  # the Advanced Math and Khan banks
NADV = sum(len(list((Path(__file__).resolve().parent.parent / "sheets/banks").glob(f"**/{p}*.py"))) for p in PORTED)
OUT = tempfile.mkdtemp(prefix="mathsheet_test_")

KEY_BREAK = "\n#pagebreak()\n#qnum.update(0)\n"

def parts(name):
    """A written NAME.typ's first version, split into its worksheet and the key after it."""
    ws, key = (Path(OUT) / f"{name}.typ").read_text().split(KEY_BREAK)[:2]
    return ws, key

def driver(app):
    def keys(s):
        for c in s:
            app.key(c)
    return keys
def counts(app):
    return {k: n for k in mp.KEYS if (n := E.count(app.sheet, "literal", k))}
def titles(app):
    return [s["title"] for s in app.sheet["sections"]]
def prompts(app):
    return [it["problem"]["prompt"] for it in sh.items(app.sheet)]
def banks_first(app):
    """Open the literal bank and start on its first type, for the tests of the banks themselves."""
    app.open.add("literal")
    app.row = app.rows().index(("count", ("literal", "1")))
    return app
def text(app, width=80):
    lines, _ = app.render(width)
    return "\n".join("".join(t for _, t, _, _ in l) for l in lines)

# ---- the types pane: counts make sections in sequence order
a = T.App(seed=12)
assert a.rows()[1] == ("seq", "literal_by_type") and a.row == 1 and not a.open, \
    "everything starts closed; the cursor starts on the built-in sequence, which comes first"
assert all(r[0] in ("course", "seq", "bank", "set") for r in a.rows()), "no steps or types showing"
banks_first(a); keys = driver(a)
keys("4j"); assert a.rid() == ("count", ("literal", "3")), a.rid()
keys("3l"); assert counts(a) == {"3": 3}, counts(a)
keys("2j6l"); assert counts(a) == {"3": 3, "4": 6}
keys("k2l"); assert counts(a) == {"3": 3, "3f": 2, "4": 6}
assert titles(a) == [mp.L.heading("3"), mp.L.heading("4")], titles(a)
keys("x"); assert "3f" not in counts(a); keys("j")
keys("h"); assert counts(a)["4"] == 5
keys("."); assert counts(a)["4"] == 4, "repeat"
keys("u"); assert counts(a)["4"] == 5, "undo"
keys("\x12"); assert counts(a)["4"] == 4, "redo"
keys("dd"); assert "4" not in counts(a) and titles(a) == [mp.L.heading("3")], "an emptied type section goes"
a.row = a.rows().index(("count", ("literal", "1"))); keys("l"); assert titles(a)[0] == mp.L.heading("1"), "type 1's section goes first"
keys("\x01\x01"); assert counts(a)["1"] == 3, "ctrl-a"
keys("G"); assert a.row == len(a.rows()) - 1
keys("/square\n"); assert a.rid() == ("step", ("literal_by_type", 13)), "the sequence's step, by its note"
assert "literal_by_type" in a.open, "/ opens what it finds"
def next_match():                     # the ported banks have squares too: pass over them
    keys("n")
    while (lambda k: k if isinstance(k, str) else str(k[0]))(a.rid()[1]).startswith(PORTED):   # a bank row, or a type row
        keys("n")
next_match(); assert a.rid() == ("count", ("literal", "B")), a.rid()
next_match(); assert a.rid() == ("count", ("literal", "Bf")), a.rid()
keys("i2\n"); assert counts(a)["Bf"] == 2, "typed count"
before = prompts(a)
keys("r"); assert prompts(a) != before and counts(a)["Bf"] == 2, "r rerolls the entry"
keys("/versions\n"); keys("l"); assert a.sheet["versions"] == 2
assert all(len(it["alts"]) == 1 for it in sh.items(a.sheet)), "versions are drawn for every problem"
keys("/title\n"); keys("cc\n"); assert a.err and "empty" in a.msg, a.msg
keys(":set title=Quiz 3 Review\n"); assert a.sheet["title"] == "Quiz 3 Review"
keys(":class Geometry\n"); assert a.sheet["class_name"] == "Geometry"
keys(":instructions Show your work.\n"); assert a.sheet["instructions"] == "Show your work."
keys(":set compact answers\n"); assert a.compact and a.answers
keys(":set nocompact noanswers\n"); assert not a.compact and not a.answers
keys(":set style=formulas\n"); assert a.err and "E518" in a.msg
keys(":bogus\n"); assert a.msg.startswith("E492")
keys(":mix 12:1\n"); assert a.err
keys(":q\n"); assert a.msg.startswith("E37") and not a.quit

# ---- :mix drafts a new sheet; the sheet pane moves, rerolls, and edits
keys(":mix 1:3 3:2 9:1\n"); assert counts(a) == {"1": 3, "3": 2, "9": 1}, counts(a)
keys("\t"); assert a.focus == "preview" and a.cur == (0, 0), a.cur
keys("l"); assert a.cur == (0, 1), "l: right column"
keys("l"); assert a.cur == (0, 1), "no third column"
keys("h"); assert a.cur == (0, 0)
keys("j"); assert a.cur == (0, 1)
keys("j"); assert a.cur == (0, 2)
keys("j"); assert a.cur == (1, -1), "j stops on a section header"
keys("[["); assert a.cur == (0, -1)
keys("]]"); assert a.cur == (1, -1)
keys("gg"); assert a.cur == T.SHEET
keys("5G"); assert a.cur == (1, 1), a.cur
keys(":1\n"); assert a.cur == (0, 0)

p0 = a.item()["problem"]["prompt"]; others = prompts(a)[1:]
keys("r"); assert a.item()["problem"]["prompt"] != p0 and prompts(a)[1:] == others, "r rerolls just this one"
assert len(a.item()["alts"]) == 1
keys("u"); assert a.item()["problem"]["prompt"] == p0
sec1 = [it["problem"]["prompt"] for it in a.sheet["sections"][1]["items"]]
sec0 = [it["problem"]["prompt"] for it in a.sheet["sections"][0]["items"]]
keys("R"); assert [it["problem"]["prompt"] for it in a.sheet["sections"][0]["items"]] != sec0 and \
    [it["problem"]["prompt"] for it in a.sheet["sections"][1]["items"]] == sec1, "R rerolls only its section"
keys("]]"); keys("R")
assert [it["problem"]["prompt"] for it in a.sheet["sections"][1]["items"]] != sec1, "R rerolls the section"
keys("gg"); old = prompts(a); keys(":reroll\n")
assert all(x != y for x, y in zip(old, prompts(a))), ":reroll rerolls everything"
assert len(set(prompts(a))) == len(prompts(a)), "no repeats"

keys(":1\n"); keys("W"); assert a.item()["width"] == "full"
keys("+"); assert a.item()["space"] == "1in", a.item()["space"]
keys("3-"); assert a.item()["space"] == "0.25in"
keys(":space 2in\n"); assert a.item()["space"] == "2in"
keys(":space wide\n"); assert a.err
keys("]]"); keys(":width full\n")
assert all(it["width"] == "full" for it in a.sheet["sections"][1]["items"]), ":width on a header sets the section"
keys("u")

# editing: the prompt is solved again; a hand-written answer is checked
keys(":1\n"); keys("cc"); assert a.mode == "insert" and a.buf == ""
keys("a x + b = c ; x\n"); assert a.item()["problem"]["answer"] == "x = (c - b)/a" and a.item()["status"] == "checked"
assert a.item()["edited"] and a.item()["alts"] == []
keys("A"); assert a.buf == "x = (c - b)/a"
keys("\x15x = (c + b)/a\n"); assert a.item()["status"] == "failed" and a.err, a.msg
assert "✗1." in text(a), "a failing answer is marked"
assert a.statuses() == (0, 1)
keys("A\x15(c - b)/a\n"); assert a.item()["status"] == "checked" and a.item()["problem"]["answer"] == "x = (c - b)/a"
keys("i\x15q = r\n"); assert a.err and "single =" not in a.msg and a.item()["problem"]["prompt"] == "a x + b = c"
keys("r"); assert not a.item()["edited"], "rerolling an edited problem draws it again"

# sections: new, rename, instructions, move, cut and paste, join
keys("gg"); keys("o"); assert a.mode == "insert" and a.cur == (0, -1)
keys("Warm-up\n"); assert titles(a)[0] == "Warm-up"
keys("cI"); keys("Do these first.\n"); assert a.sheet["sections"][0]["instructions"] == "Do these first."
assert "(empty" in text(a)
keys("j"); assert a.cur == (1, -1), "an empty section has no problems to stop on"
keys("j"); first = a.item()["problem"]["prompt"]
keys("dd"); assert first not in prompts(a) and a.reg["cut"]
keys("[["); keys("[["); keys("p"); assert a.sheet["sections"][0]["items"][0]["problem"]["prompt"] == first, "cut + paste moves it"
keys("p"); assert len(a.sheet["sections"][0]["items"]) == 2 and \
    a.sheet["sections"][0]["items"][1]["problem"]["prompt"] != first, "pasting again draws a new one"
keys("yy"); keys("P"); assert len(a.sheet["sections"][0]["items"]) == 3
assert len(set(prompts(a))) == len(prompts(a)), "copies are redrawn, never duplicated"
keys("gg"); keys("j"); keys("J"); assert titles(a)[1] == "Warm-up", "J moves a section down"
keys("K"); assert titles(a)[0] == "Warm-up"
keys("j"); p = a.item()["problem"]["prompt"]; keys("3J")
assert a.cur[0] == 1 and a.item()["problem"]["prompt"] == p, "J moves a problem, across sections"
keys(":1\n"); keys(":join\n"); assert titles(a)[0] == "Warm-up" and len(a.sheet["sections"][0]["items"]) >= 5
keys("u")
keys("zM"); assert a.folded and a.cur[1] == -1
assert all(t[1] == -1 for t in a.targets()), "folded: only headers"
assert "problems" in text(a)
keys("zR"); assert not a.folded
keys("/Warm\n"); assert a.cur == (0, -1)

# L adds the type under the types cursor where the sheet cursor is
keys(":1\n"); n0 = len(a.sheet["sections"][0]["items"])
keys("\t"); assert a.focus == "left"
keys("\x17o"); assert a.wide and a.focus == "preview", "^W o widens the sheet and moves to it"
keys("\t"); assert a.focus == "left" and a.wide, "Tab back shows the banks; the sheet stays wide for next time"
keys("\x17o"); assert not a.wide and a.focus == "left"
keys(":set wide\n"); assert a.wide
keys(":set nowide\n"); assert not a.wide
assert T.left_width(a, 80) == 40 and T.left_width(a, 125) == 55, "the banks pane, in focus"
keys("\t"); assert T.left_width(a, 80) == 30 and T.left_width(a, 125) == 55, "a narrow sheet takes room from the banks"
keys(":set wide\n"); assert T.left_width(a, 125) == 0
keys(":set nowide\n\t")
banks_first(a); keys("2L"); assert len(a.sheet["sections"][0]["items"]) == n0 + 2
assert [it["entry"] for it in a.sheet["sections"][0]["items"]][1:3] == ["1", "1"]

# groups and shuffle rearrange what is there, drawing nothing
keep = sorted(prompts(a))
keys(":groups 9 3+1=Mixed\n"); assert titles(a) == [mp.L.heading("9"), "Mixed"], titles(a)
assert sorted(prompts(a)) == keep
keys(":shuffle\n"); assert titles(a) == [""] and sorted(prompts(a)) == keep
keys(":groups\n"); assert titles(a) == [mp.L.heading("1"), mp.L.heading("3"), mp.L.heading("9")]

# the drawing: header, two columns, versions, answers
keys(":versions 2\n:title Quiz 3 Review\n")
t = text(a)
assert "Quiz 3 Review" in t and "Name ____" in t and "Ver: 1" in t and "Show your work." in t
lines, _ = a.render(80)
row = next(l for l in lines if l and l[0][1] == "1.")
assert any(x > 30 for x, *_ in row), "two half-width problems share a line"
keys("gt"); assert a.version == 1 and "Ver: 2" in text(a)
keys("gt"); assert a.version == 0
keys("za"); assert a.answers and " = " in text(a)

# write, then reopen exactly
keys(f":out {OUT}\n")
keys(":w\n"); assert not a.err and not a.dirty(), a.msg
written = sh.load(a.last_build["out"] / "untitled.sheet.json")
assert written["sections"] == a.sheet["sections"], ":w writes exactly what the sheet pane shows"
assert written["command"].endswith("untitled.sheet.json")
b = T.App(); b.load(str(a.last_build["out"] / "untitled.sheet.json"))
assert b.sheet["sections"] == a.sheet["sections"] and b.s["name"] == "untitled" and not b.dirty()
keys("D"); assert a.total() == 0; keys("u"); assert a.total() > 0
keys(":q\n"); assert a.quit

assert T.pretty("V = 1/3 pi r^2 h") == "V = (1/3)πr²h"
assert T.pretty("x = (2 m + n)/(5 - m)") == "x = (2m + n)/(5 − m)"

# ---- banks: the tree, a fixed bank, and a bank of plain Typst problems
import json
from sheets import banks
from sheets import library
LIB = Path(tempfile.mkdtemp(prefix="lib_"))
f = LIB / "words.json"
f.write_text(json.dumps({"format": 1, "name": "words", "title": "Word Problems",
    "types": [{"key": "rate", "title": "Rate Problems", "width": "full", "space": "2in"}],
    "problems": [{"id": "w1", "type": "rate", "prompt": "A train goes $60$ miles in $1.5$ hours. How fast?",
                  "answer": "$40$ mph", "text": "A train goes 60 miles in 1.5 hours. How fast?"},
                 {"id": "w2", "type": "rate", "prompt": "Pat walks $3$ miles in $1$ hour. How far in $4$?",
                  "answer": "$12$ miles"}]}))
library.rescan(LIB)
w = T.App(seed=3); wk = driver(w)
assert [r for r in w.rows() if r[0] == "bank" and not r[1].startswith(PORTED)] == [("bank", "absolute"), ("bank", "absolute_words"), ("bank", "inequalities"), ("bank", "literal"), ("bank", "modeling"), ("bank", "systems"), ("bank", "lesson_1-4"), ("bank", "words")]
lesson = w.rows().index(("bank", "lesson_1-4"))
wk(f":{lesson + 1}\n"); assert w.rid() == ("bank", "lesson_1-4")
wk("o"); assert ("count", ("lesson_1-4", "3")) in w.rows()
wk("3j"); assert w.rid() == ("count", ("lesson_1-4", "3")), w.rid()
wk("o"); assert ("problem", ("lesson_1-4", "13")) in w.rows()
wk("j"); assert w.rid() == ("problem", ("lesson_1-4", "13"))
wk("l"); assert E.where_problem(w.sheet, "lesson_1-4", "13") and w.value(w.row) is True
wk("l"); assert w.err and "already" in w.msg
wk("k2l"); assert E.count(w.sheet, "lesson_1-4", "3") == 3
wk("/Clear One\n"); assert w.rid() == ("step", ("literal_by_type", 3)) and w.act() == ("count", ("literal", "3")), w.rid()
wk("2l"); assert titles(w) == [mp.L.heading("3")], "the lesson and the generator share Type 3's section"
assert len(set(prompts(w))) == 5
wk(":versions 2\n")
lesson_items = [it for it in sh.items(w.sheet) if it["bank"] == "lesson_1-4"]
assert all(it["alts"] == [] for it in lesson_items) and all(it["status"] == "checked" for it in lesson_items)
assert all(len(it["alts"]) == 1 for it in sh.items(w.sheet) if it["bank"] == "literal")
wk("/A train\n"); assert w.rid() == ("problem", ("words", "w1")) and "words" in w.open
wk("l"); assert titles(w)[-1] == "Rate Problems"
it = w.sheet["sections"][-1]["items"][0]
assert it["width"] == "full" and it["space"] == "2in" and it["status"] == "unchecked"
wk("\t"); wk("G"); assert w.item() is it and "?" in text(w)
wk("r"); assert w.item()["problem"]["id"] == "w2", "rerolling a fixed problem swaps in another"
wk("r"); assert w.item()["problem"]["id"] == "w1", "and back: w1 is no longer on the sheet"
wk("yy"); wk("p"); assert w.item()["problem"]["id"] == "w2", "a copy draws the bank's other problem"
wk("p"); assert w.err and "no unused" in w.msg, "and then there are none left"
wk("u"); wk("G"); assert w.item()["problem"]["id"] == "w1"
wk("A\x15$13$ miles\n"); assert w.item()["problem"]["answer"] == "$13$ miles" and w.item()["status"] == "unchecked"
wk(f":out {OUT}\n:name words\n:w\n"); assert not w.err and "1 unchecked" in w.msg, w.msg
key = parts("words")[1]
assert "A train goes $60$ miles" in key and "$13$ miles" in key and "#section-head[Rate Problems]" in key
library.rescan()

# ---- systems of three equations: a second family
y = T.App(seed=8); yk = driver(y)
yk(":mix systems/1:2 systems/4:1 systems/A:1\n")
assert y.sheet["title"] == "Systems of Three Equations Practice", y.sheet["title"]
assert y.sheet["instructions"] == "Solve each system of equations."
assert titles(y) == ["Type 1: Back-Substitute", "Type 4: Eliminate", "Special Case A: No Solution"]
assert all(it["width"] == "half" and it["space"] == "2.5in" for it in sh.items(y.sheet))
assert "⎧" in text(y) and "⎩" in text(y)
yk("\t:3\n"); assert y.item()["entry"] == "4"
yk("cc"); yk("x + y + z = 6 ; y + z = 5 ; z = 2\n")
assert y.item()["problem"]["answer"] == "(1, 3, 2)" and y.item()["status"] == "checked", y.item()
yk("A\x15(1, 3, 3)\n"); assert y.item()["status"] == "failed" and y.err
yk("A\x15no solution\n"); assert y.item()["status"] == "failed"
yk("A\x15(1, 3, 2)\n"); assert y.item()["status"] == "checked"
yk("i\x15x + y = 1 ; 2x + 2y = 2 ; z = 4\n"); assert y.item()["problem"]["answer"] == "infinitely many solutions"
yk("A\x15banana\n"); assert y.err and "(x, y, z)" in y.msg
yk(":4\n"); assert y.item()["problem"]["answer"] == "no solution"
yk(":versions 2\n"); assert len(y.item()["alts"]) == 1 and y.item()["alts"][0]["answer"] == "no solution"
yk(":3\n"); assert y.item()["alts"] == [], "an edited system is the same in every version"
yk(f":out {OUT}\n:name systems\n:w\n"); assert not y.err, y.msg
key = parts("systems")[1]
assert "mat(delim:" in key and "$(1, 3, 2)$" not in key and "infinitely many solutions" in key
mixed = mp.draft(mp.parse_mix(["3:1", "systems/2:1"]), 1, 4)
assert mixed["instructions"] == "" and [s["instructions"] for s in mixed["sections"]] == [
    mp.L.INSTRUCTIONS, "Solve each system of equations."], "a mix: each family's section carries its own instructions"
assert mp.draft(mp.parse_mix(["modeling/1a:1", "3:1"]), 1, 4)["sections"][1]["items"][0]["entry"] == "1a", \
    "an entry that isn't a literal one, mixed with literal"
assert mixed["title"] == mp.DEFAULTS["title"] == "Untitled Worksheet", "no one bank's title for a mix"
assert mp.draft(mp.parse_mix(["3:1"]), 1, 4)["title"] == "Literal Equations Practice", "one bank: its title"
n = T.App()
assert (n.sheet["title"], n.sheet["instructions"], n.s["name"]) == ("Untitled Worksheet", "", "untitled"), "placeholders"
driver(n)(":mix modeling/1a:1\n")
assert n.sheet["title"] == "Lesson 1-6: Compound Inequalities Practice" and n.sheet["instructions"] == mp.banks.get("modeling").INSTRUCTIONS
try:
    mp.parse_mix(["systems/9:1"]); raise AssertionError("bad entry accepted")
except ValueError as e:
    assert "1, 2, 3, 4, 5, 6, A, B" in str(e)

# ---- inequalities: number lines, and an instruction line per type
q = T.App(seed=4); qk = driver(q)
qk(":mix inequalities/1:2 inequalities/3:1 inequalities/6:1\n")
assert q.sheet["instructions"] == "" and titles(q)[0] == "Type 1: Write the Inequality", titles(q)
assert [s["instructions"] for s in q.sheet["sections"]] == [
    "Write the inequality shown by each graph.", "Graph each inequality.",
    "Solve each compound inequality. Then graph its solution."]
assert "graph: " in text(q) and all(it["status"] == "checked" for it in sh.items(q.sheet))
qk("\t:1\n"); qk("cc"); qk("x <= 1\n")
assert q.item()["problem"]["graph"] == [None, [1, True]] and q.item()["status"] == "checked", q.item()
qk("cc"); qk("-4 < x <= 1\n"); assert q.err and "ray" in q.msg, "type 1 is a ray"
qk("A\x15x < 1\n"); assert q.item()["status"] == "failed"
qk("A\x151 >= x\n"); assert q.item()["status"] == "checked", "any equivalent answer checks"
qk(":4\n"); qk("cc"); qk("9 <= 2x + 7 <= 17\n")
p = q.item()["problem"]
assert p["answer"] == "1 <= x <= 5" and p["graph"] == [[1, True], [5, True]] and q.item()["status"] == "checked", p
qk("cc"); qk("2x - 1 > -5 and x + 3 <= 8\n")
assert q.item()["problem"]["answer"] == "-2 < x <= 5" and q.item()["status"] == "checked"
assert q.item()["problem"]["prompt"] == '2x - 1 > -5 quad "and" quad x + 3 <= 8'
qk("cc"); qk("2x <= 3 and x > -4\n"); assert q.err and "whole number" in q.msg
qk(f":out {OUT}\n:name ineq\n:w\n"); assert not q.err, q.msg
ws, key = parts("ineq")
assert ws.count("#let numline") == 1 and "#let numline" not in key, "the key shares the sheet's preamble"
assert not list(Path(OUT).glob("*_key.*")), "no separate key file"
assert "— Answer Key" in key and "— Answer Key" not in ws
assert "ink: red" in key and "ink: red" not in ws, "the key draws the graphs in red"
assert "$1 >= x$" in key, "the key prints the teacher's answer as written"
assert "#let numline" not in (Path(OUT) / "systems.typ").read_text(), "only sheets that need it"

# ---- modeling compound inequalities: word problems, a story per entry, parallel versions
m = T.App(seed=5); mk = driver(m)
mk(":mix modeling/1a:1 modeling/3D:1\n:versions 2\n")
assert titles(m) == ["Type 1: One Serving", "Type 3: Fractional Servings"], titles(m)
assert all(it["status"] == "checked" for it in sh.items(m.sheet))
it = sh.items(m.sheet)[1]
assert it["problem"]["story"] == it["alts"][0]["story"] == "d", "versions keep the story"
assert re.search(r"(1/2|1 1/2|2|2 1/2) bottles? of fruit juice", it["problem"]["prompt"]), it["problem"]["prompt"]
mk("\t:1\n"); mk("cc")
mk("\x15Nia is planning a diet for a dog named River. River should get between 510 and 540 Calories each day. "
   "River eats 1 1/2 servings of dog food each day, and the rest of the Calories come from treats. A serving "
   "of dog food has 320 Calories, and a treat has 15 Calories. How many treats can River have each day?\n")
assert m.item()["problem"]["answer"] == "510 <= 1.5(320) + 15t <= 540; 2 <= t <= 4" and m.item()["status"] == "checked"
mk("cc"); mk("\x15River eats a lot.\n"); assert m.err and "wording" in m.msg
mk("A\x15510 <= 480 + 15t <= 540; 2 <= t <= 5\n"); assert m.item()["status"] == "failed"
mk(f":out {OUT}\n:name model\n:w\n"); assert "1 failing answer" in m.msg, m.msg
key = parts("model")[1]
from sheets import library as _lib
assert T.App().s["out"] == T.home_path(Path.cwd()), "a session starts in the folder it was started from"
assert _lib.config()["out"] == T.home_path(OUT), "the folder written to last is remembered"
_cwd = os.getcwd(); os.chdir(Path.home())
try:
    assert T.App().s["out"] == T.home_path(OUT), "started from ~, it starts in the folder written to last"
finally:
    os.chdir(_cwd)
assert T.App(out="elsewhere").s["out"] == "elsewhere", "--out overrides it"
assert "$510 <= 480 + 15t <= 540$ \\ $2 <= t <= 5$ \\ 2 to 4 treats" in key and "$1 1/2$ servings" in key, "the teacher's answer as written; the count from the prompt"

# ---- Lesson 1-7 word problems: phrases, then stories that ask for more of the same model
a = T.App(seed=5); ak = driver(a)
ak(":mix absolute_words/1:4 absolute_words/4B:1\n:versions 2\n")
assert titles(a) == ["Type 1: Phrases for a Tolerance", "Type 4: Modeling and Solving"], titles(a)
assert all(it["status"] == "checked" for it in sh.items(a.sheet))
from sheets.banks import absolute_words as AW
assert len({AW.read_phrase(it["problem"]["prompt"])[0] for it in sh.items(a.sheet)[:4]}) == 4, "a new phrase each time"
it = sh.items(a.sheet)[4]
assert it["problem"]["story"] == it["alts"][0]["story"] == "b", "versions keep the story"
ak("\t:5\n"); ak("cc")
ak("\x15Members of the soccer team are traveling to a tournament, where they will stay in a hotel for 3 nights. "
   "The total cost for each member must be within $15 of $180. The hotels' rates are the following: A. $55/night; "
   "B. $60/night; C. $70/night. Let r be a hotel's rate, in dollars per night. Which hotels can the team stay in?\n")
assert a.item()["problem"]["answer"] == "abs(3r - 180) <= 15; 55 <= r <= 65; Hotels A and B" and a.item()["status"] == "checked"
ak("A\x15|3r - 180| <= 15; 55 <= r <= 65; Hotels A, B, and C\n"); assert a.item()["status"] == "failed"
ak("A\x15abs(3r - 180) <= 15; 55 <= r <= 65; Hotels A and B\n"); assert a.item()["status"] == "checked"
assert AW.check(dict(type="3", story="a", answer="abs(d - 80) <= 10", prompt=AW.fill(AW.template("3", AW.STORY["a"]),
    who="Ana", r="25", e="10", T="80"))) == "unchecked", "Type 3 is in terms of the unknown, not the amount"

# ---- an Advanced Math bank: simplifying with exponents
x = T.App(seed=3); xk = driver(x)
xk(":mix adv_exponents/1:2 adv_exponents/4:1\n:versions 2\n")
assert titles(x) == ["Type 1: Powers of Products and Quotients", "Type 4: Letters in the Exponents"], titles(x)
assert all(it["status"] == "checked" for it in sh.items(x.sheet))
xk("\t:1\n"); xk("cc"); xk("\x15(3 x^2 y^(-1))^(-2) ((2 x^3 y)/(x^(-1) y^4))^3\n")
assert x.item()["problem"]["answer"] == "(8 x^8)/(9 y^7)" and x.item()["status"] == "checked", x.item()
xk("A\x15(8 x^8 y^(-7))/9\n"); assert x.item()["status"] == "failed", "the right value, but a negative exponent"
xk("A\x15(8 x^8)/(9 y^6)\n"); assert x.item()["status"] == "failed"
xk("A\x15(8 x^8)/(9 y^7)\n"); assert x.item()["status"] == "checked"
x = T.App(seed=4); xk = driver(x)
xk(":mix adv_rationalize/all:1 adv_complex_fractions/all:1 adv_factoring/all:1\n")
assert len(sh.items(x.sheet)) == 11 and all(it["status"] == "checked" for it in sh.items(x.sheet))
where = [(it["bank"], it["entry"]) for it in sh.items(x.sheet)]
xk(f"\t:{where.index(('adv_rationalize', '3')) + 1}\n"); xk("cc"); xk("\x15(4 + sqrt(3))/(2 - sqrt(3))\n")
assert x.item()["problem"]["answer"] == "11 + 6 sqrt(3)" and x.item()["status"] == "checked", x.item()
xk(f":{where.index(('adv_factoring', '4')) + 1}\n"); xk("cc"); xk("\x153 y^(2 n + 1) + 12 y^(3 n + 2)\n")       # letter exponents: the old answer stays, and fails
assert x.item()["status"] == "failed"
xk("A\x153 y^(2 n + 1) (1 + 4 y^(n + 1))\n"); assert x.item()["status"] == "checked"
xk("A\x153 (y^(2 n + 1) + 4 y^(3 n + 2))\n"); assert x.item()["status"] == "failed", "not finished: y^(2 n + 1) is common"
x = T.App(seed=5); xk = driver(x)
xk(":mix adv_literal/all:1 adv_poly_division/all:1 adv_functions/all:1\n")
assert len(sh.items(x.sheet)) == 11 and all(it["status"] == "checked" for it in sh.items(x.sheet))
where = [(it["bank"], it["entry"]) for it in sh.items(x.sheet)]
xk(f"\t:{where.index(('adv_literal', '3')) + 1}\n"); xk("cc"); xk("\x15r = (d + 1)/(2 d - w) ; d\n")
assert x.item()["problem"]["answer"] == "d = (r w + 1)/(2 r - 1)" and x.item()["status"] == "checked", x.item()
xk(f":{where.index(('adv_poly_division', '2')) + 1}\n"); xk("cc"); xk("\x15x^3 - 5 x^2 + 9 ; x - 4\n")
assert x.item()["problem"]["answer"] == "x^2 - x - 4 - 7/(x - 4)" and x.item()["status"] == "checked", x.item()
xk(f":{where.index(('adv_functions', '4')) + 1}\n"); xk("cc"); xk("\x15f(x) = sqrt(x - 3)/(x^2 - 7 x + 10); domain\n")
assert x.item()["problem"]["answer"] == "x >= 3, x != 5" and x.item()["status"] == "checked", x.item()
xk("A\x15x >= 3, x != 2, x != 5\n"); assert x.item()["status"] == "checked", "2 is outside the domain anyway"
xk("A\x15x >= -3, x != 5\n"); assert x.item()["status"] == "failed"
x = T.App(seed=6); xk = driver(x)
xk(":mix adv_variation/all:1 adv_mixtures/all:1 adv_word/all:1\n")
assert len(sh.items(x.sheet)) == 10 and all(it["status"] == "checked" for it in sh.items(x.sheet))
where = [(it["bank"], it["entry"]) for it in sh.items(x.sheet)]
xk(f"\t:{where.index(('adv_mixtures', '4')) + 1}\n")
assert x.item()["problem"]["story"] == "c", "water boiled off"
xk("cc"); xk("\x15How many ounces of water must be boiled off from 60 ounces of a 10% salt solution to make a 15% salt solution?\n")
assert x.item()["problem"]["answer"] == "20 ounces of water" and x.item()["status"] == "checked", x.item()   # the answer follows the numbers
xk("A\x1525 ounces of water\n"); assert x.item()["status"] == "failed"
xk(f":{where.index(('adv_word', '1')) + 1}\n"); xk("A\x1599, 99\n"); assert x.item()["status"] == "failed"
x = T.App(seed=7); xk = driver(x)
xk(":mix adv_trig/all:1 adv_spheres/all:1\n")
assert len(sh.items(x.sheet)) == 6 and all(it["status"] == "checked" for it in sh.items(x.sheet))
where = [(it["bank"], it["entry"]) for it in sh.items(x.sheet)]
xk(f"\t:{where.index(('adv_trig', '4')) + 1}\n"); xk("cc"); xk("\x156 angle 200 degree\n")
assert x.item()["problem"]["answer"] == "-5.64 hat(dotless.i) - 2.05 hat(dotless.j)" and x.item()["status"] == "checked"
xk("A\x15-5.64 hat(dotless.i) + 2.05 hat(dotless.j)\n"); assert x.item()["status"] == "failed"
xk(f":{where.index(('adv_trig', '1')) + 1}\n"); xk("cc"); xk("\x152 sin(30 degree) + sqrt(2) cos(45 degree)\n")
assert x.item()["problem"]["answer"] == "2" and x.item()["status"] == "checked", x.item()
xk(f":{where.index(('adv_spheres', '2')) + 1}\n"); right = x.item()["problem"]["answer"]
xk("A\x15$5 pi$ cubic miles\n"); assert x.item()["status"] == "failed", "no radius 1 to 10 gives 5 pi"
xk(f"A\x15{right}\n"); assert x.item()["status"] == "checked"

# ---- selecting with v: changes apply to every selected problem
v = T.App(seed=3); vk = driver(v)
vk(":mix 1:3 3:2 9:1\n\t"); assert v.cur == (0, 0)
vk("jjv"); assert v.anchor == (0, 2) and v.selection() == [(0, 2)]
vk("jj"); assert v.cur == (1, 0) and v.selection() == [(0, 2), (1, 0)], "across a section title"
vk("k"); assert v.selection() == [(0, 2), (1, 0), (1, 1)], "a title at the end takes its whole section"
vk("j")
spaces = [v.item(q)["space"] for q in v.selection()]
vk("+"); assert [E.inches(v.item(q)["space"]) for q in v.selection()] == [E.inches(x) + 0.25 for x in spaces]
assert v.anchor is not None, "+ keeps the selection"
vk("2-"); assert [E.inches(v.item(q)["space"]) for q in v.selection()] == [max(0, E.inches(x) - 0.25) for x in spaces]
vk(":space 1.5in\n"); assert all(v.item(q)["space"] == "1.5in" for q in v.selection()) and v.anchor
assert v.item((0, 0))["space"] != "1.5in", "outside the selection, nothing changes"
vk("W"); ws = {v.item(q)["width"] for q in v.selection()}; assert len(ws) == 1, "W sets them all one way"
before = [v.item(q)["problem"]["prompt"] for q in v.selection()]
other = v.item((0, 0))["problem"]["prompt"]
vk("r"); assert [v.item(q)["problem"]["prompt"] for q in v.selection()] != before and v.anchor
assert v.item((0, 0))["problem"]["prompt"] == other
n_undo = len(v.undo)
vk("u"); assert v.anchor is None and len(v.undo) == n_undo - 1, "one u undoes the whole batch"
assert [v.item(q)["problem"]["prompt"] for q in [(0, 2), (1, 0)]] == before[:2]
vk("gv"); assert v.anchor == (0, 2) and v.cur == (1, 0), "gv brings the selection back"
vk("\x1b"); assert v.anchor is None
vk("gv")
cut = [v.item(q)["problem"]["prompt"] for q in v.selection()]
vk("d"); assert v.anchor is None and len(sh.items(v.sheet)) == 4 and v.reg["kind"] == "items"
assert v.cur == (0, 2) or v.cur[0] == 0, v.cur
vk("G"); vk("p"); assert prompts(v)[-2:] == cut, "p pastes the cut block"
vk("u"); vk("u"); assert len(sh.items(v.sheet)) == 6
vk(":1\n"); vk("v"); vk("j"); vk("y"); assert v.anchor is None and len(v.reg["what"]) == 2 and len(sh.items(v.sheet)) == 6
vk("v"); vk("v"); assert v.anchor is None, "v again ends it"
vk("vJ"); assert v.anchor is None, "moving a problem ends the selection"
vk("u")

# gs shuffles the selection in place (or the cursor's section), drawing nothing
secs0 = [[it["problem"]["prompt"] for it in sec["items"]] for sec in v.sheet["sections"]]
vk(":1\n"); vk("v"); vk("jj")
picked = [v.item(q)["problem"]["prompt"] for q in v.selection()]
vk("gs"); assert v.anchor == (0, 0) and v.cur == (0, 2), "gs keeps the selection"
now = [v.item(q)["problem"]["prompt"] for q in v.selection()]
assert sorted(now) == sorted(picked) and now != picked, now
assert prompts(v)[3:] == [q for sec in secs0 for q in sec][3:], "the rest stay put"
vk("\x1b"); vk("u"); assert [[it["problem"]["prompt"] for it in sec["items"]] for sec in v.sheet["sections"]] == secs0
vk(":1\n"); vk("gs")
assert [sorted(it["problem"]["prompt"] for it in sec["items"]) for sec in v.sheet["sections"]] == [sorted(x) for x in secs0], \
    "a section's problems stay in it"
vk("u")

# :group pulls the selection into a new section
vk(":1\n"); vk("jv"); vk("j"); vk("jj")
picked = [v.item(q)["problem"]["prompt"] for q in v.selection()]
vk(":group Challenge\n"); assert v.anchor is None and "Challenge" in titles(v)
gi = titles(v).index("Challenge"); assert v.cur == (gi, -1)
assert [it["problem"]["prompt"] for it in v.sheet["sections"][gi]["items"]] == picked
assert gi == 1 and len(v.sheet["sections"][0]["items"]) == 1, "it follows the first problem's section"
vk("u"); vk(":1\n"); vk("v"); vk("]]]]"); vk("k")
vk(":group\n"); assert titles(v)[0] == "" and len(v.sheet["sections"]) == 2, "emptied sections go"
vk("u")
vk("zM"); vk("v"); assert v.anchor is None and v.err, "no selecting while folded"
vk("zR\tv"); assert v.anchor is None and v.err, "v selects only on the sheet"

# ---- the empty sheet
e = T.App(seed=1); ek = driver(e)
assert "No problems yet" in text(e)
ek("\t"); assert e.cur == T.SHEET
ek("r"); assert e.err
ek("p"); assert e.err and "nothing to paste" in e.msg
ek(":w\n"); assert e.err

# ---- drafting from the command line keeps working
mixc = {"3": 2, "4": 2}
a1 = mp.draft(mixc, 1, 7); a2 = mp.draft(mixc, 1, 7, groups=[])
assert a1 == a2, "no groups means the default layout"
assert mp.draft(mixc, 2, 7)["sections"][0]["items"][0]["problem"] == a1["sections"][0]["items"][0]["problem"], \
    "adding versions doesn't change version 1"
assert mp.layout(mp.parse_groups(["3+4"]), {"3": 1}) == [dict(types=["3"], name="")]
# ---- courses: the banks pane shows one course's banks, by unit
import json as _json
lib = Path(tempfile.mkdtemp(prefix="courselib_"))
(lib / "courses.json").write_text(_json.dumps({"format": 1, "courses": [
    {"title": "Algebra 1", "units": ["Foundations", "Equations", "Lessons", "Additional Practice"]}]}))
(lib / "ints.json").write_text(_json.dumps({"format": 1, "name": "ints", "title": "Integers",
    "courses": {"Prealgebra": None, "Algebra 1": "Foundations"},
    "types": [{"key": "add", "title": "Adding"}, {"key": "mul", "title": "Multiplying", "courses": ["Prealgebra"]}],
    "problems": [{"id": "1", "type": "add", "prompt": "$-3 + 5$", "answer": "$2$"},
                 {"id": "2", "type": "mul", "prompt": "$-3 dot 5$", "answer": "$-15$"}]}))
library.save_config(library=str(lib))
c = T.App(seed=6); ck = driver(c)
assert c.course is None and c.rows()[0] == ("course", None) and c.value(0) == "All banks"
ck(":rescan\n"); assert f"{8 + NADV} banks, 1 sequence, 9 courses" in c.msg and not c.err, c.msg
ck("gg"); assert c.rid() == ("course", None)
ck("l"); assert c.course == "Prealgebra" and c.sheet["class_name"] == "Prealgebra", "the class follows"
assert [r for r in c.rows() if r[0] == "bank"] == [("bank", "ints")]
ck("o"); assert c.rid() == ("course", None)
c.open.add("ints"); assert [r for r in c.rows() if r[0] == "count"] == [("count", ("ints", "add")), ("count", ("ints", "mul"))]
ck("l"); assert c.course == "Algebra 1" and c.sheet["class_name"] == "Algebra 1"
assert [r for r in c.rows() if r[0] == "count" and r[1][0] == "ints"] == [("count", ("ints", "add"))], "mul is Prealgebra only"
assert library.current().view("Algebra 1") == [("Foundations", ["ints"]), ("Lessons", ["lesson_1-4", "inequalities", "modeling", "absolute", "absolute_words"]),
                                                ("Additional Practice", ["literal"])]
assert library.config()["course"] == "Algebra 1", "remembered for the next sheet"
ck("h"); assert c.course == "Prealgebra"
ck("h"); assert c.course is None and c.sheet["class_name"] == "Prealgebra", "All banks leaves the class alone"
ck(":class Period 3\n:course alg\t"); assert c.buf == "course Algebra 1", c.buf
ck("\n"); assert c.course == "Algebra 1" and c.sheet["class_name"] == "Period 3", "a typed class stays"
ck(":course Algebra I\n"); assert c.err and "did you mean Algebra 1" in c.msg, c.msg
ck(":course all\n"); assert c.course is None
ck("u"); assert c.course == "Algebra 1", "u undoes a course change"
ck(":course\n"); assert c.msg.startswith("course: Algebra 1")
ck("gg" + "i\x15Geo\t"); assert c.buf == "Geometry"
ck("\n"); assert c.course == "Geometry" and len(c.rows()) == 1 + len(T.SETTINGS)
ck("/Adding\n"); assert c.err, "/ searches the course"
ck(":course all\n/Adding\n"); assert c.rid() == ("count", ("ints", "add"))
assert T.App().course is None, "all banks, as last used"
library.save_config(course="Algebra 2"); assert T.App().course == "Algebra 2", "a new sheet starts in the last course"
assert T.App().sheet["class_name"] == "Algebra 2", "and its class is the course"
assert T.App(sheet=sh.new_sheet("Quiz", "Period 3")).sheet["class_name"] == "Period 3", "--class overrides it"

# the sheet keeps its course; a bank that goes missing still shows and prints
ck(":course Algebra 1\n"); c.open.add("ints")
ck("gg/Adding\n"); ck("l"); assert E.count(c.sheet, "ints", "add") == 1
ck(":class Algebra 1\n:course Prealgebra\n"); assert c.sheet["class_name"] == "Algebra 1", "a sheet with problems keeps its class"
ck(":course Algebra 1\n")
ck(f":out {OUT}\n:name course\n:w\n"); assert not c.err, c.msg
saved = sh.load(Path(OUT) / "course.sheet.json"); assert saved["course"] == "Algebra 1"
library.save_config(library=str(Path(tempfile.mkdtemp()))); library.rescan()
d = T.App(); dk = driver(d); d.load(str(Path(OUT) / "course.sheet.json"))
assert d.course == "Algebra 1" and d.missing() == ["ints"] and d.err and "not in the library: ints" in d.msg, d.msg
assert "!1." in text(d) and "-3 + 5" in text(d), "marked, and still shown"
dk("\tG"); assert "ints (missing)" not in d.msg
dk("r"); assert d.err and "isn't in the library" in d.msg, d.msg
dk(f":out {OUT}\n:w\n"); assert not d.err and "-3 + 5" in (Path(OUT) / "course.typ").read_text(), "still prints"
dk(f":library {lib}\n"); assert not d.missing() and not d.err and f"{8 + NADV} banks" in d.msg, d.msg
assert library.config()["library"] == str(lib)
dk(":library ~/nowhere\n"); assert "no such folder" in d.msg and d.missing() == ["ints"]
dk(":warnings\n"); assert d.msg == "no warnings"
library.save_config(library=EMPTY_LIB, course=None)
library.rescan()

# ---- sequences in the banks pane: steps act as their entries, examples as their problems
sl = Path(tempfile.mkdtemp(prefix="seqlib_"))
(sl / "by_move.json").write_text(_json.dumps({"format": 1, "kind": "sequence", "title": "By First Move",
    "courses": {"Algebra 1": "Lessons"}, "steps": [
        {"entry": "literal/1", "note": "one operation to undo"},
        {"entry": "literal/3", "note": "a fraction bar appears", "examples": ["lesson_1-4#13", "lesson_1-4#14"]},
        {"entry": "literal/44"},
        {"entry": "systems/1", "title": "Back-Substitute (systems)"}]}))
(sl / "other.json").write_text(_json.dumps({"format": 1, "kind": "sequence", "title": "Untagged",
    "steps": [{"entry": "literal/2"}]}))
library.save_config(library=str(sl), course="Algebra 1"); library.rescan()
q = T.App(seed=9); qk = driver(q)
assert q.rid() == ("seq", "by_move") and ("step", ("by_move", 1)) not in q.rows(), "closed, the cursor on it"
qk("o")
assert q.rows()[:6] == [("course", None), ("seq", "by_move"), ("step", ("by_move", 1)), ("step", ("by_move", 2)),
                        ("step", ("by_move", 3)), ("step", ("by_move", 4))], q.rows()[:6]
assert ("seq", "other") not in q.rows() and ("bank", "literal") in q.rows(), "a sequence shows in its own course"
qk(":course all\n"); tops = [r for r in q.rows() if r[0] in ("seq", "bank") and not r[1].startswith("adv_")]
assert tops[:4] == [("seq", "by_move"), ("seq", "literal_by_type"), ("seq", "other"), ("bank", "absolute")], \
    "sequences first"
qk(":course Algebra 1\n")
qk("ggjj"); assert q.rid() == ("step", ("by_move", 1))
qk("2l"); assert E.count(q.sheet, "literal", "1") == 2 and q.value(q.row) == 2, "l on a step adds its entry"
qk("h"); assert E.count(q.sheet, "literal", "1") == 1
qk("j"); qk("o"); assert ("example", ("by_move", 2, "lesson_1-4", "13")) in q.rows()
qk("j"); assert q.rid() == ("example", ("by_move", 2, "lesson_1-4", "13"))
qk("l"); assert E.where_problem(q.sheet, "lesson_1-4", "13") and q.value(q.row) is True
qk("l"); assert q.err and "already" in q.msg
qk("k"); assert q.value(q.row) == 1, "a pinned example counts for its step"
qk("l"); assert q.value(q.row) == 2 and E.count(q.sheet, "literal", "3") == 1
assert q.value(q.rows().index(("seq", "by_move"))) == 3
qk("o"); assert ("example", ("by_move", 2, "lesson_1-4", "13")) not in q.rows()
qk("j"); assert q.rid() == ("step", ("by_move", 3))
qk("l"); assert q.err and "step 3: literal has no entry '44'" in q.msg, q.msg
qk("i5\n"); assert q.err and "no entry" in q.msg
qk("o"); assert q.err and "no pinned examples" in q.msg
qk("j"); qk("l"); assert E.count(q.sheet, "systems", "1") == 1, "a step can come from any bank"
before = prompts(q)
qk("ggj"); assert q.rid() == ("seq", "by_move")
qk("l"); assert q.err and "o opens the sequence" in q.msg
qk("r"); assert prompts(q) != before and len(prompts(q)) == 4, "r rerolls the sequence's problems"
qk("x"); assert q.total() == 0, "x removes the sequence's problems"
qk("u"); assert q.total() == 4
qk("/fraction bar\n"); assert q.rid() == ("step", ("by_move", 2)), "/ finds a step by its note"
qk("zM"); assert ("step", ("by_move", 1)) not in q.rows() and q.rid() == ("seq", "by_move")
qk("gg"); qk("zR"); assert ("step", ("by_move", 1)) in q.rows() and q.rid() == ("course", None), "zR on COURSE"
qk("O"); assert not any(r[0] in ("step", "count") for r in q.rows()), "O closes all when any is open"
qk("O"); assert ("step", ("by_move", 1)) in q.rows() and "literal" in q.open, "O opens all when all are closed"
qk("O"); qk("ggj"); qk("o"); qk("O"); assert not q.open, "one open is enough to close all"
qk("/Algebra 1\n"); assert q.rid() == ("course", None) and not q.err, "/ can land on COURSE"
qk("/V = (1/3)\n"); assert q.rid() == ("example", ("by_move", 2, "lesson_1-4", "13")), q.rid()
assert ("by_move", 2) in q.open_types, "/ opens the step it finds an example in"

# ---- drafting from a sequence: new steps in sections, then a shuffled review
(sl / "long.json").write_text(_json.dumps({"format": 1, "kind": "sequence", "title": "Long",
    "courses": ["Algebra 1"], "steps": [{"entry": f"literal/{k}"} for k in ("1", "2", "3", "4", "5", "6", "7")]
                                       + [{"entry": "literal/3", "examples": ["lesson_1-4#13", "lesson_1-4#14"]}]}))
library.rescan()
assert mp.parse_steps("5", library.current().sequence("long")) == [5]
assert mp.parse_steps("1-3,5,3", library.current().sequence("long")) == [1, 2, 3, 5]
assert mp.steps_text([1, 2, 3, 5, 7, 8]) == "1-3,5,7-8"
assert mp.spread([1, 2, 3, 4], 6) == {1: 1, 2: 1, 3: 2, 4: 2}, "extras go to the most recent"
assert mp.spread([1, 2, 3, 4, 5, 6, 7], 3) == {1: 1, 4: 1, 7: 1}, "evenly spaced, ending at the latest"
assert mp.spread([1, 2], 1) == {2: 1} and mp.spread([], 4) == {}
plan = mp.parse_draft(["long", "5-6"])
assert plan == dict(seq="long", new=[5, 6], per=6, review=[1, 2, 3, 4], pinned=False), plan
assert mp.parse_draft(["long", "5", "x3", "review", "none"])["review"] == []
assert mp.parse_draft(["long", "4", "review", "1-5", "pinned"]) == dict(seq="long", new=[4], per=6, review=[1, 2, 3, 5], pinned=True)
for bad, why in ((["long"], "use SEQUENCE"), (["lng", "1"], "did you mean long"), (["long", "9"], "steps 1-8"),
                 (["long", "1", "x0"], "bad draft option"), (["by_move", "3"], "can't draw"),
                 (["long", "2", "review"], "bad draft option"), (["long", "a-b"], "bad steps")):
    try:
        mp.parse_draft(bad); raise AssertionError(bad)
    except ValueError as e:
        assert why in str(e), (bad, e)
assert mp.parse_draft(["by_move", "4"])["review"] == [1, 2], "a broken step is left out of the default review"
sheet = mp.draft_sequence(plan, 2, 11)
assert [x["title"] for x in sheet["sections"]] == ["Clear a Denominator, Then Distribute", "Clear Two Denominators", "Review"]
assert sheet["title"] == "Long: Steps 5–6" and sheet["instructions"] == mp.L.INSTRUCTIONS
assert [len(x["items"]) for x in sheet["sections"]] == [6, 6, 6], "one review problem per two new"
assert sorted(it["entry"] for it in sheet["sections"][2]["items"]) == ["1", "2", "3", "3", "4", "4"]
assert all(len(it["alts"]) == 1 for it in sh.items(sheet)), "versions"
assert len({it["problem"]["prompt"] for it in sh.items(sheet)}) == 18, "nothing repeats"
assert mp.draft_sequence(plan, 2, 11) == sheet, "same plan and seed, same sheet"
pin = mp.draft_sequence(mp.parse_draft(["long", "8", "x3", "review", "none", "pinned"]), 1, 2)
assert [it["problem"].get("id") for it in pin["sections"][0]["items"]][:2] == ["13", "14"] and len(pin["sections"]) == 1
assert pin["sections"][0]["items"][2]["bank"] == "literal", "then fresh draws"
cmd = mp.draft_command(plan, 2, 11, out="x y")
assert cmd == "python3 make_practice.py --draft long 5-6 x6 review 1-4 --versions 2 --seed 11 --out 'x y'", cmd
assert mp.draft_sequence(mp.parse_draft(shlex.split(cmd)[3:8]), 2, 11) == sheet, "the command redraws it"

g = T.App(seed=4); gk = driver(g)
gk(":title My Quiz\n:draft lo\t"); assert g.buf == "draft long", g.buf
gk(" 2-3 x4\n"); assert not g.err and g.total() == 4 + 4 + 4 and "review of 1" in g.msg, g.msg
assert g.sheet["title"] == "My Quiz", "a title you typed stays"
gk(":title Untitled Worksheet\n:draft long 3\n"); assert g.sheet["title"] == "Long: Step 3"
gk(":draft long 4\n"); assert g.sheet["title"] == "Long: Step 4", "a drafted title follows the next draft"
gk("u"); assert g.sheet["title"] == "Long: Step 3"
gk(":draft long 9\n"); assert g.err and "steps 1-8" in g.msg
gk(":draft\n"); assert g.err and "use SEQUENCE" in g.msg
gk(":draft literal_by_type 3-4 x4 pinned\n"); assert not g.err, g.msg
assert [it["problem"].get("id") for it in g.sheet["sections"][0]["items"]] == ["13", "14", "15", "16"], \
    "the lesson's own Type 3 problems, in order"
assert [x["title"] for x in g.sheet["sections"]] == ["Clear One Denominator", "Distribute First", "Review"]
assert {it["entry"] for it in g.sheet["sections"][2]["items"]} == {"1", "2"} and len(g.sheet["sections"][2]["items"]) == 4
library.save_config(library=EMPTY_LIB, course=None); library.rescan()

# ---- out: ~ is home, relative starts in the current folder, Tab completes
import os
home, here = Path(tempfile.mkdtemp(prefix="home_")), Path(tempfile.mkdtemp(prefix="cwd_"))
for d in ("Documents", "Downloads", "Desktop", ".config", "Documents/Algebra"):
    (home / d).mkdir()
(home / "Doc notes.txt").write_text("")
saved_home, saved_cwd = os.environ["HOME"], os.getcwd()
os.environ["HOME"] = str(home); os.chdir(here)
try:
    assert T.complete_path("~") == ["~/"]
    assert T.complete_path("~/Docu", True) == ["~/Documents/"]
    assert T.complete_path("~/Do", True) == ["~/Documents/", "~/Downloads/"]
    assert T.complete_path("~/Do") == ["~/Doc notes.txt", "~/Documents/", "~/Downloads/"], "files too, for :e"
    assert T.complete_path("~/", True) == ["~/Desktop/", "~/Documents/", "~/Downloads/"], "hidden ones stay hidden"
    assert T.complete_path("~/.c", True) == ["~/.config/"]
    assert T.complete_path("~/Nope/x") == [] and T.complete_path(str(home) + "/De", True) == [str(home) + "/Desktop/"]
    assert T.dir_label(home / "Desktop") == "~/Desktop" and T.dir_label(here / "practice") == "practice"
    assert T.dir_label(here) == "." and T.dir_label(home) == "~"

    c = T.App(seed=4); ck = driver(c)
    ck("G"); assert c.rid() == ("set", "out")
    ck("cc~/Docu\t"); assert c.buf == "~/Documents/", c.buf
    ck("\t"); assert c.buf == "~/Documents/Algebra/", "the next Tab looks inside"
    ck("\n"); assert c.s["out"] == "~/Documents/Algebra/"
    ck("cc~/D\t"); assert c.buf == "~/Desktop/" and c.comp
    ck("\t"); assert c.buf == "~/Documents/"
    ck(chr(T.curses.KEY_BTAB)); assert c.buf == "~/Desktop/", "Shift-Tab goes back"
    ck("\t\t\t"); assert c.buf == "~/D", "after the last match, what was typed"
    ck("\x1b"); assert c.comp is None and c.s["out"] == "~/Documents/Algebra/"
    ck(":out ~/Desk\t"); assert c.buf == "out ~/Desktop/", c.buf
    ck("\n"); assert c.s["out"] == "~/Desktop/"
    ck(":set out=~/Dow\t\n"); assert c.s["out"] == "~/Downloads/"
    ck(":e ~/Doc\t"); assert c.buf == "e ~/Documents/", "only what :e can open: not notes.txt"
    ck("\x1b:title Doc\t"); assert c.buf == "title Doc", "Tab completes paths only"
    ck("\x1b")

    ck(":mix 1:2\n:out ~/Desktop\n:w\n"); assert not c.err, c.msg
    assert (home / "Desktop" / "untitled.sheet.json").exists() and '"~/Desktop/"' in c.msg, c.msg
    assert str(home / "Desktop" / "untitled.sheet.json") in c.last_build["sheet"]["command"]
    ck(":out sets\n:w\n"); assert (here / "sets" / "untitled.sheet.json").exists(), "relative: the current folder"
    d = T.App(); d.load("~/Desktop/untitled.sheet.json"); assert d.s["out"] == "~/Desktop", d.s["out"]
    (home / "Desktop" / "old_v1.json").write_text("{}"); (home / "Desktop" / "old_v2.json").write_text("{}")
    (home / "Desktop" / "Unit 1").mkdir()
    assert any(f.suffix == ".pdf" for f in (home / "Desktop").iterdir()) or not c.last_build["compiled"]
    ck(":e ~/Desktop/\t"); assert c.buf == "e ~/Desktop/Unit 1/", c.buf
    assert c.comp["options"] == ["~/Desktop/Unit 1/", "~/Desktop/old_v1.json", "~/Desktop/untitled.sheet.json", "~/Desktop/"], \
        "folders and the sheets :e opens, not the PDFs and Typst beside them; then what was typed: " + repr(c.comp["options"])
    ck("\t"); assert c.buf == "e ~/Desktop/old_v1.json"
    ck("\t"); assert c.buf == "e ~/Desktop/untitled.sheet.json"
    ck("\x1b")
finally:
    os.environ["HOME"] = saved_home; os.chdir(saved_cwd)

# ---- adding from a whole bank: one section, any type; rerolls stay in the bank
library.rescan(EMPTY_LIB)
lesson, L4 = banks.get("lesson_1-4"), "lesson_1-4"
seeds = iter(range(10**6))
s = sh.new_sheet("Whole bank"); s["course"] = "Algebra 1"
E.add_from_bank(s, L4, 20, seeds)
assert [(x["title"], x["auto"]) for x in s["sections"]] == [(lesson.TITLE, "lesson_1-4:*")], s["sections"]
its = sh.items(s)
assert len(its) == 20 and all(sh.from_bank(it) and it["bank"] == L4 for it in its)
assert len({lesson.seen_key(it["problem"]) for it in its}) == 20, "no repeats"
assert len({it["entry"] for it in its}) >= 5, "spread over the types"
assert all(it["entry"] == it["problem"]["type"] and (it["width"], it["space"]) ==
           (lesson.ENTRY[it["entry"]]["width"], lesson.ENTRY[it["entry"]]["space"]) for it in its), "each its type's layout"
E.add_from_bank(s, L4, 5, seeds); assert len(s["sections"]) == 1 and E.count_from_bank(s, L4) == 25, "the same section again"
E.set_count(s, L4, "4", 2 + E.count(s, L4, "4"), seeds)
assert len(s["sections"]) == 2 and not any(sh.from_bank(it) for it in s["sections"][1]["items"]), \
    "a type's own problems: its own section, drawn from the type"
E.set_bank_count(s, L4, 3, seeds); assert E.count_from_bank(s, L4) == 3 and len(s["sections"]) == 2
E.remove_last_from_bank(s, L4, 10); assert [x["auto"] for x in s["sections"]] == ["literal:4"], "the emptied bank section goes"

# every unused problem equally likely: types turn up as often as they have problems
freq = {}
for k in range(3000):
    e, _ = sh.draw_any(L4, k, {})
    freq[e] = freq.get(e, 0) + 1
for t in lesson.types:
    want = sum(p["type"] == t for p in lesson.PROBLEMS) / len(lesson.PROBLEMS)
    assert abs(freq.get(t, 0) / 3000 - want) < 0.03, (t, freq.get(t, 0) / 3000, want)
assert sh.draw_any(L4, 7, {}) == sh.draw_any(L4, 7, {}), "a seed always gives the same problem"
assert all(sh.draw_any(L4, k, {}, keep=["1", "2"])[0] in ("1", "2") for k in range(50)), "only the types kept"
assert sh.bank_types(L4, "Calculus") == sh.bank_types(L4) == list(lesson.types), "a course that hides it: every type"

# rerolls: a whole-bank item may change type, and its layout follows unless set by hand
s = sh.new_sheet("Rerolls")
E.add_from_bank(s, L4, 2, seeds); E.set_count(s, L4, "4", 1 + E.count(s, L4, "4"), seeds)
a, b, t4 = sh.items(s)
b["space"] = "3in"
types_seen = set()
for _ in range(15):
    E.reroll(s, E.positions(s), seeds)
    types_seen.add(a["entry"])
    assert sh.from_bank(a) and (a["width"], a["space"]) == (lesson.ENTRY[a["entry"]]["width"], lesson.ENTRY[a["entry"]]["space"])
    assert b["space"] == "3in" and t4["entry"] == "4" and not sh.from_bank(t4)
assert len(types_seen) > 2, types_seen
E.set_scope(t4, "bank"); assert sh.from_bank(t4); E.set_scope(t4, "type"); assert "scope" not in t4
copy_ = E.fresh_copy(s, a, next(seeds)); assert sh.from_bank(copy_), "yy p keeps the scope"

# the pool runs out: nothing left raises, and a reroll that can't changes nothing
s = sh.new_sheet("All fifty")
E.add_from_bank(s, L4, 50, seeds); assert len({lesson.seen_key(it["problem"]) for it in sh.items(s)}) == 50
try:
    E.add_from_bank(s, L4, 1, seeds); raise AssertionError("none left")
except RuntimeError as e:
    assert "no unused problems" in str(e)
before = json.dumps(s)
try:
    E.reroll(s, E.positions(s)[:1], seeds); raise AssertionError("none left to reroll to")
except RuntimeError:
    assert json.dumps(s) == before

# a generator: an entry whose formula pool is used up is skipped
seen = {}
for k in range(500):
    try:
        sh._draw("literal", "3f", k, seen)
    except RuntimeError:
        break
else:
    raise AssertionError("the formula pool should run out")
assert all(sh.draw_any("literal", k, seen, keep=["3"])[0] == "3" for k in range(20))

# versions: parallel, so a whole-bank item keeps its type in every version
s = sh.new_sheet("Versions"); s["versions"] = 3
E.add_from_bank(s, "inequalities", 8, seeds)
assert all(len(it["alts"]) == 2 and all(p["type"] == it["entry"] for p in it["alts"]) for it in sh.items(s))
assert len({it["entry"] for it in sh.items(s)}) > 1

# a generator's bank section sits apart from its type sections, which keep their order
s = sh.new_sheet("Mixed")
E.add_from_bank(s, "literal", 2, seeds); E.set_count(s, "literal", "3", 1, seeds); E.set_count(s, "literal", "1", 1, seeds)
assert [x["auto"] for x in s["sections"]] == ["literal:*", "literal:1", "literal:3"], [x["auto"] for x in s["sections"]]
f = Path(OUT) / "whole.sheet.json"; sh.save(s, f)
assert sh.load(f) == s and [sh.from_bank(it) for it in sh.items(s)] == [True, True, False, False], "scope is saved"

# --mix BANK/any:N (or BANK/*:N): from every type of a bank, in the bank's own section
import random as _random, shlex as _shlex, subprocess as _sp
assert mp.parse_mix(["lesson_1-4/*:5", "lesson_1-4/any:2", "literal/3:2", "3:1"]) == {"lesson_1-4/*": 7, "literal/3": 2, "3": 1}
for bad in ("nope/any:2", "lesson_1-4/any:x"):
    try:
        mp.parse_mix([bad]); raise AssertionError(bad)
    except ValueError as e:
        assert "any (every type at once)" in str(e) or "no bank" in str(e), e
mixw = mp.parse_mix(["lesson_1-4/any:6", "3:2"])
d = mp.draft(mixw, 2, 11)
assert d == mp.draft(mixw, 2, 11), "a seed gives the same sheet"
assert [(x["title"], x["auto"]) for x in d["sections"]] == [(mp.L.heading("3"), "literal:3"), (lesson.TITLE, "lesson_1-4:*")]
assert all(sh.from_bank(it) for it in d["sections"][1]["items"]) and len(d["sections"][1]["items"]) == 6
assert not any(sh.from_bank(it) for it in d["sections"][0]["items"])
assert len({it["entry"] for it in d["sections"][1]["items"]}) > 1
order = [id(it) for it in d["sections"][1]["items"]]
mp.regroup(d, [], _random.Random(1))
assert [id(it) for it in d["sections"][-1]["items"]] == order and d["sections"][-1]["auto"] == "lesson_1-4:*", \
    ":groups keeps the bank's section, in its order"
cmd = mp.command_for(mixw, 1, 11)
assert "'lesson_1-4/*:6'" in cmd, cmd
toks = _shlex.split(cmd)
assert mp.parse_mix(toks[toks.index("--mix") + 1:toks.index("--versions")]) == mixw, "the saved command drafts it again"
r = _sp.run([sys.executable, "make_practice.py", "--mix", "lesson_1-4/any:4", "--seed", "3", "--no-compile",
             "--out", OUT, "--name", "cli"], capture_output=True, text=True, cwd=Path(__file__).resolve().parent.parent)
assert r.returncode == 0, r.stderr
cli = sh.load(Path(OUT) / "cli.sheet.json")
assert [x["title"] for x in cli["sections"]] == [lesson.TITLE] and all(sh.from_bank(it) for it in sh.items(cli))
m = T.App(seed=2); mk = driver(m)
mk(":mix lesson_1-4/any:3 1:1\n"); assert not m.err and titles(m) == [mp.L.heading("1"), lesson.TITLE], (m.msg, titles(m))

# the banks pane: l, h, a typed count, and L on a bank's row; the sheet marks and rescopes
g = T.App(seed=5); gk = driver(g)
g.set_course("Algebra 1")
g.row = g.rows().index(("bank", L4))
gk("20l"); assert titles(g) == [lesson.TITLE] and E.count_from_bank(g.sheet, L4) == 20 and g.value(g.row) == 20, g.msg
assert not g.err and "20 from all of" in g.msg, g.msg
gk("5h"); assert E.count_from_bank(g.sheet, L4) == 15
gk("cc8\n"); assert E.count_from_bank(g.sheet, L4) == 8, g.msg
gk("u"); assert E.count_from_bank(g.sheet, L4) == 15, "undo"
before = prompts(g)
gk("r"); assert prompts(g) != before and E.count_from_bank(g.sheet, L4) == 15, "r on the bank rerolls them all, from the bank"
gk("o"); g.row = g.rows().index(("count", (L4, "4"))); gk("2l")
assert titles(g) == [lesson.TITLE, mp.L.heading("4")] and not sh.from_bank(g.sheet["sections"][1]["items"][-1])
gk("\tgg]]j"); assert g.cur == (0, 0) and "rerolls from all of lesson_1-4" in g.where(), g.where()
gk(":scope type\n"); assert not sh.from_bank(g.item()) and "all of" not in g.where() and not g.err
gk(":scope bank\n"); assert sh.from_bank(g.item())
gk(":scope sideways\n"); assert g.err and "usage" in g.msg

# I: a box of what the cursor is on; the keys it lists still work while it's open
class FakeScr:
    def __init__(self, h, w):
        self.h, self.w, self.grid = h, w, [[" "] * w for _ in range(h)]
    def getmaxyx(self):
        return self.h, self.w
    def addstr(self, y, x, text, attr=0):
        for i, ch in enumerate(text[:self.w - x]):
            self.grid[y][x + i] = ch
    def text(self):
        return "\n".join("".join(r) for r in self.grid)
def box(app, h=24, w=80):
    scr = object.__new__(T.Screen); scr.scr = FakeScr(h, w)
    scr.info_box(app, h, w)
    return scr.scr.text()
def info(app):
    title, rows, foot = app.info()
    return title, {label: (value, keys) for label, value, keys in rows if label}
gk("I"); assert g.mode == "info"
title, rows = info(g)
assert title == "Problem 1" and rows["Rerolls"][0].startswith("from the whole bank, any type: ") and rows["Rerolls"][1] == "b"
assert rows["Bank"][0] == lesson.TITLE and rows["Type"][0].startswith(g.item()["entry"] + "  ")
assert rows["Width"] == (g.item()["width"] + " (the type's)", "W") and rows["Answer"][1] == "A"
assert "unused left" in rows["Rerolls"][0] and rows["Versions"][0] == "one"
drawn = box(g); assert "Problem 1" in drawn and "from the whole bank" in drawn and "Esc" in drawn, drawn
small = box(g, 12, 44); assert "…" in small and "Problem 1" in small, "a small screen: cut short"
gk("b"); assert g.mode == "info" and not sh.from_bank(g.item()) and info(g)[1]["Rerolls"][0].startswith("from its type only")
gk("b"); assert sh.from_bank(g.item())
w0 = g.item()["width"]
gk("W"); assert g.mode == "info" and g.item()["width"] != w0 and "by hand" in info(g)[1]["Width"][0]
gk("u"); assert g.item()["width"] == w0 and g.mode == "info", "undo, with the box open"
before = g.item()["problem"]
gk("r"); assert g.mode == "info" and g.item()["problem"] != before
gk("A"); assert g.mode == "insert"
gk("\x1b"); assert g.mode == "info", "an edit begun in the box comes back to it"
gk("x"); assert g.mode == "info" and g.err and E.count_from_bank(g.sheet, L4) == 15, "keys it doesn't list do nothing"
gk("j"); assert g.mode == "info" and info(g)[0] == "Problem 2", "the box follows the cursor"
gk("k[["); assert g.cur == (0, -1) and info(g)[0] == "Section 1"
rows = info(g)[1]
assert rows["Title"] == (lesson.TITLE, "cS") and "the bank's own" in rows["Kind"][0]
assert rows["Problems"][0].startswith(f"15  ({lesson.TITLE}: ") and rows["Rerolls"][0] == "all from their whole bank"
gk("\x1b"); assert g.mode == "normal"
gk("]]I"); assert "its type's own" in info(g)[1]["Kind"][0] and info(g)[1]["Rerolls"][0] == "all from their own type"
gk("b"); assert info(g)[1]["Rerolls"][0] == "all from their whole bank", "b on a section: all of it"
gk("b"); assert info(g)[1]["Rerolls"][0] == "all from their own type"
gk("q"); assert g.mode == "normal"
gk("gg"); assert g.cur[0] < 0
gk("I"); assert info(g)[0] == "The sheet" and "17" in info(g)[1]["Problems"][0]; gk("I"); assert g.mode == "normal"
gk("]]jvjI"); assert info(g)[0] == "2 selected", info(g)[0]; gk("\x1b\x1b")
# I on the banks pane: a bank, a type (or a step), a fixed bank's problem
gk("\t"); g.row = g.rows().index(("bank", L4)); assert g.focus == "left" and L4 in g.open
gk("o"); assert ("count", (L4, "1")) not in g.rows(), "closed, so oj below opens it"
gk("I"); assert g.mode == "info"
title, rows = info(g)
assert title == f"Bank: {lesson.TITLE}" and rows["Id"][0].startswith("lesson_1-4  (permanent")
assert rows["Kind"][0] == "50 written problems, checked as Literal Equations" and rows["File"][0] == "library/lesson_1-4.json"
assert rows["Courses"][0] == "Algebra 1 › Lessons" and rows["Types"][0] == "13"
on = E.count_from_bank(g.sheet, L4) + sum(1 for it in sh.items(g.sheet) if it["bank"] == L4 and not sh.from_bank(it))
assert rows["On sheet"][0].startswith(f"{on}") and rows["Unused"][0] == f"{50 - on} of the 50 that l here can draw", rows
assert "Bank: " in box(g)
gk("2l"); assert g.mode == "info" and info(g)[1]["On sheet"][0].startswith(f"{on + 2}"), "l works with the box open"
gk("2h"); assert info(g)[1]["On sheet"][0].startswith(f"{on}")
gk("W"); assert g.mode == "info" and g.err, "a sheet key does nothing here"
gk("oj"); assert g.rid() == ("count", (L4, "1")) and info(g)[0] == "Type 1: One Step", info(g)[0]
rows = info(g)[1]
assert rows["Look for"][0] == "The unknown is tied to the rest by a single operation: +, -, ×, or ÷.", rows["Look for"]
assert rows["Layout"][0] == "half width, 0.75in work space" and rows["Problems"][0].startswith("8 written, ")
n1 = E.count(g.sheet, L4, "1")
gk("l"); assert E.count(g.sheet, L4, "1") == n1 + 1 and info(g)[1]["On sheet"][0].startswith(f"{n1 + 1}")
gk("u"); assert E.count(g.sheet, L4, "1") == n1
gk("o"); gk("j"); assert g.rid()[0] == "problem" and info(g)[0] == f"Problem lesson_1-4#{g.rid()[1][1]}"
assert info(g)[1]["Answer"][0].endswith("(checked)")
gk("\x1b"); assert g.mode == "normal"
g.row = g.rows().index(("seq", "literal_by_type")); gk("I"); assert g.mode == "info"
title, rows = info(g)
assert title == "Sequence: Literal Equations by Type" and rows["File"][0] == "library/literal_by_type.json"
assert rows["Steps"][0] == "13; 50 pinned examples" and rows["Courses"][0] == "Algebra 1 › Additional Practice"
assert rows["  1"][0].startswith("One Step  (literal/1) · 8 pinned"), rows["  1"]
assert rows["Draft"][0].startswith(":draft literal_by_type STEPS")
assert box(g, 40, 80).count(" pinned") == 14, "every step shows (and the Steps row)"
had = int(rows["On sheet"][0])
gk("oj3lk"); assert g.rid() == ("seq", "literal_by_type") and g.mode == "info", "keys work with the box open"
assert info(g)[1]["On sheet"][0] == str(had + 3) and info(g)[1]["  1"][0].endswith(" on sheet")
gk("x"); assert info(g)[1]["On sheet"][0] == "0" and g.mode == "info", "x removes all the sequence's problems"
gk("u"); assert info(g)[1]["On sheet"][0] == str(had + 3)
gk("u"); assert info(g)[1]["On sheet"][0] == str(had), "and the sheet as it was"
gk("\x1b")
gk("j"); gk("I"); assert info(g)[1]["Step"][0].startswith("1 of literal_by_type: One Step") and info(g)[0] == "Type 1: One Step"
gk("q"); g.row = 0; gk("I"); assert g.mode == "normal" and g.err, "nor on COURSE"
gk("\t")
gk("gg]]]]"); assert g.cur[0] == 1
gk(":scope bank\n"); assert all(sh.from_bank(it) for it in g.sheet["sections"][1]["items"]), "a section's header: all of it"
gk("j\t"); g.row = g.rows().index(("bank", L4)); gk("3L")
assert len(g.sheet["sections"][1]["items"]) == 5 and all(sh.from_bank(it) for it in g.sheet["sections"][1]["items"]), \
    "L: where the sheet cursor is"
gk("zM"); assert lesson.TITLE in text(g); gk("zR")
gk("x"); assert not any(it["bank"] == L4 for it in sh.items(g.sheet)) and g.sheet["sections"] == []
g.row = g.rows().index(("bank", "inequalities")); gk("6l")
assert titles(g) == [banks.get("inequalities").TITLE] and len({it["entry"] for it in sh.items(g.sheet)}) > 1
gk(f":out {OUT}\n:name whole\n:w\n"); assert not g.err, g.msg
library.rescan()

# ---- :pre compiles the sheet as it stands to a temp PDF, writing and saving nothing
p = T.App(seed=7); pk = driver(p); opened = []
p.open_path = lambda f: opened.append(f) or True
pk(":pre\n"); assert p.err and not opened, "an empty sheet: nothing to preview"
pk(f":out {OUT}/preview_out\n:mix 1:2 3:2\n:versions 2\n")
if shutil.which("typst"):
    pk("gt:pre\n"); assert not p.err, p.msg
    assert opened[-1].name == "preview.pdf" and opened[-1].exists() and "version 2 worksheet" in p.msg, "the version showing"
    pk(":pre key 1\n"); assert opened[-1].name == "preview_key.pdf" and "version 1 key" in p.msg
    pk(":pre slides\n"); assert opened[-1].name == "preview_slides.pdf" and opened[-1].parent == p.preview_dir
    assert p.dirty() and p.last_build is None and not (Path(OUT) / "preview_out").exists(), "nothing written or saved"
pk(":pre 3\n"); assert p.err and "2 versions" in p.msg
pk(":pre bogus\n"); assert p.err and "usage" in p.msg

print("all key tests passed")
