"""Drive mathsheet.App with scripted keys (no terminal needed).
Run from the project folder:  python3 tests/test_mathsheet.py"""
import os, shlex, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="config_")    # never the teacher's own config
(Path(os.environ["XDG_CONFIG_HOME"]) / "mathsheet").mkdir()
EMPTY_LIB = tempfile.mkdtemp(prefix="emptylib_")
(Path(os.environ["XDG_CONFIG_HOME"]) / "mathsheet" / "config.json").write_text(
    '{"library": "%s"}' % EMPTY_LIB)                                        # nor their library
import mathsheet as T, make_practice as mp
from sheets import sheet as sh, edit as E
OUT = tempfile.mkdtemp(prefix="mathsheet_test_")

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
    """Fold the built-in sequence and start on the literal bank's first type,
    for the tests of the banks themselves."""
    app.open.discard("literal_by_type")
    app.row = app.rows().index(("count", ("literal", "1")))
    return app
def text(app, width=80):
    lines, _ = app.render(width)
    return "\n".join("".join(t for _, t, _, _ in l) for l in lines)

# ---- the types pane: counts make sections in sequence order
a = T.App(seed=12)
assert a.rows()[1:3] == [("seq", "literal_by_type"), ("step", ("literal_by_type", 1))] and a.row == 2, \
    "the built-in sequence comes first, open, and the cursor starts on its first step"
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
keys("ggjjj"); keys("l"); assert titles(a)[0] == mp.L.heading("1"), "type 1's section goes first"
keys("\x01\x01"); assert counts(a)["1"] == 3, "ctrl-a"
keys("G"); assert a.row == len(a.rows()) - 1
keys("/square\n"); assert a.rid() == ("step", ("literal_by_type", 13)), "the sequence's step, by its note"
assert "literal_by_type" in a.open, "/ opens what it finds"
keys("n"); assert a.rid() == ("count", ("literal", "B")), a.rid()
keys("n"); assert a.rid() == ("count", ("literal", "Bf")), a.rid()
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
written = sh.load(a.last_build["out"] / "literal_practice.sheet.json")
assert written["sections"] == a.sheet["sections"], ":w writes exactly what the sheet pane shows"
assert written["command"].endswith("literal_practice.sheet.json")
b = T.App(); b.load(str(a.last_build["out"] / "literal_practice.sheet.json"))
assert b.sheet["sections"] == a.sheet["sections"] and b.s["name"] == "literal_practice" and not b.dirty()
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
assert [r for r in w.rows() if r[0] == "bank"] == [("bank", "literal"), ("bank", "systems"), ("bank", "lesson_1-4"), ("bank", "words")]
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
key = (Path(OUT) / "words_v1_key.typ").read_text()
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
key = (Path(OUT) / "systems_v1_key.typ").read_text()
assert "mat(delim:" in key and "$(1, 3, 2)$" not in key and "infinitely many solutions" in key
mixed = mp.draft(mp.parse_mix(["3:1", "systems/2:1"]), 1, 4)
assert [s["instructions"] for s in mixed["sections"]] == ["", "Solve each system of equations."], \
    "a second family's section carries its own instructions"
try:
    mp.parse_mix(["systems/9:1"]); raise AssertionError("bad entry accepted")
except ValueError as e:
    assert "1, 2, 3, 4, 5, A, B" in str(e)

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
    {"title": "Algebra 1", "units": ["Foundations", "Equations"]}]}))
(lib / "ints.json").write_text(_json.dumps({"format": 1, "name": "ints", "title": "Integers",
    "courses": {"Prealgebra": None, "Algebra 1": "Foundations"},
    "types": [{"key": "add", "title": "Adding"}, {"key": "mul", "title": "Multiplying", "courses": ["Prealgebra"]}],
    "problems": [{"id": "1", "type": "add", "prompt": "$-3 + 5$", "answer": "$2$"},
                 {"id": "2", "type": "mul", "prompt": "$-3 dot 5$", "answer": "$-15$"}]}))
library.save_config(library=str(lib))
c = T.App(seed=6); ck = driver(c)
assert c.course is None and c.rows()[0] == ("course", None) and c.value(0) == "All banks"
ck(":rescan\n"); assert "4 banks, 1 sequence, 6 courses" in c.msg and not c.err, c.msg
ck("gg"); assert c.rid() == ("course", None)
ck("l"); assert c.course == "Prealgebra" and c.sheet["class_name"] == "Prealgebra", "the class follows"
assert [r for r in c.rows() if r[0] == "bank"] == [("bank", "ints")]
ck("o"); assert c.rid() == ("course", None)
c.open.add("ints"); assert [r for r in c.rows() if r[0] == "count"] == [("count", ("ints", "add")), ("count", ("ints", "mul"))]
ck("l"); assert c.course == "Algebra 1" and c.sheet["class_name"] == "Algebra 1"
assert [r for r in c.rows() if r[0] == "count" and r[1][0] == "ints"] == [("count", ("ints", "add"))], "mul is Prealgebra only"
assert library.current().view("Algebra 1") == [("Foundations", ["ints"]), ("Equations", ["literal", "lesson_1-4"])]
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

# the sheet keeps its course; a bank that goes missing still shows and prints
ck(":course Algebra 1\n"); c.open.add("ints")
ck("gg/Adding\n"); ck("l"); assert E.count(c.sheet, "ints", "add") == 1
ck(f":out {OUT}\n:name course\n:w\n"); assert not c.err, c.msg
saved = sh.load(Path(OUT) / "course.sheet.json"); assert saved["course"] == "Algebra 1"
library.save_config(library=str(Path(tempfile.mkdtemp()))); library.rescan()
d = T.App(); dk = driver(d); d.load(str(Path(OUT) / "course.sheet.json"))
assert d.course == "Algebra 1" and d.missing() == ["ints"] and d.err and "not in the library: ints" in d.msg, d.msg
assert "!1." in text(d) and "-3 + 5" in text(d), "marked, and still shown"
dk("\tG"); assert "ints (missing)" not in d.msg
dk("r"); assert d.err and "isn't in the library" in d.msg, d.msg
dk(f":out {OUT}\n:w\n"); assert not d.err and "-3 + 5" in (Path(OUT) / "course_v1.typ").read_text(), "still prints"
dk(f":library {lib}\n"); assert not d.missing() and not d.err and "4 banks" in d.msg, d.msg
assert library.config()["library"] == str(lib)
dk(":library ~/nowhere\n"); assert "no such folder" in d.msg and d.missing() == ["ints"]
dk(":warnings\n"); assert d.msg == "no warnings"
library.save_config(library=EMPTY_LIB, course=None)
library.rescan()

# ---- sequences in the banks pane: steps act as their entries, examples as their problems
sl = Path(tempfile.mkdtemp(prefix="seqlib_"))
(sl / "by_move.json").write_text(_json.dumps({"format": 1, "kind": "sequence", "title": "By First Move",
    "courses": {"Algebra 1": "Equations"}, "steps": [
        {"entry": "literal/1", "note": "one operation to undo"},
        {"entry": "literal/3", "note": "a fraction bar appears", "examples": ["lesson_1-4#13", "lesson_1-4#14"]},
        {"entry": "literal/44"},
        {"entry": "systems/1", "title": "Back-Substitute (systems)"}]}))
(sl / "other.json").write_text(_json.dumps({"format": 1, "kind": "sequence", "title": "Untagged",
    "steps": [{"entry": "literal/2"}]}))
library.save_config(library=str(sl), course="Algebra 1"); library.rescan()
q = T.App(seed=9); qk = driver(q)
assert q.rows()[:6] == [("course", None), ("seq", "by_move"), ("step", ("by_move", 1)), ("step", ("by_move", 2)),
                        ("step", ("by_move", 3)), ("step", ("by_move", 4))], q.rows()[:6]
assert ("seq", "other") not in q.rows() and ("bank", "literal") in q.rows(), "a sequence shows in its own course"
qk(":course all\n"); tops = [r for r in q.rows() if r[0] in ("seq", "bank")]
assert tops[:4] == [("seq", "by_move"), ("seq", "literal_by_type"), ("seq", "other"), ("bank", "literal")], \
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
gk(":title Literal Equations Practice\n:draft long 3\n"); assert g.sheet["title"] == "Long: Step 3"
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
    ck(":e ~/Doc\t"); assert c.buf == "e ~/Doc notes.txt", c.buf
    ck("\x1b:title Doc\t"); assert c.buf == "title Doc", "Tab completes paths only"
    ck("\x1b")

    ck(":mix 1:2\n:out ~/Desktop\n:w\n"); assert not c.err, c.msg
    assert (home / "Desktop" / "literal_practice.sheet.json").exists() and '"~/Desktop/"' in c.msg, c.msg
    assert str(home / "Desktop" / "literal_practice.sheet.json") in c.last_build["sheet"]["command"]
    ck(":out sets\n:w\n"); assert (here / "sets" / "literal_practice.sheet.json").exists(), "relative: the current folder"
    d = T.App(); d.load("~/Desktop/literal_practice.sheet.json"); assert d.s["out"] == "~/Desktop", d.s["out"]
finally:
    os.environ["HOME"] = saved_home; os.chdir(saved_cwd)

print("all key tests passed")
