"""Drive mathsheet.App with scripted keys (no terminal needed).
Run from the project folder:  python3 tests/test_mathsheet.py"""
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
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
def text(app, width=80):
    lines, _ = app.render(width)
    return "\n".join("".join(t for _, t, _, _ in l) for l in lines)

# ---- the types pane: counts make sections in sequence order
a = T.App(seed=12); keys = driver(a)
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
keys("ggj"); keys("l"); assert titles(a)[0] == mp.L.heading("1"), "type 1's section goes first"
keys("\x01\x01"); assert counts(a)["1"] == 3, "ctrl-a"
keys("G"); assert a.row == len(a.rows()) - 1
keys("/square\n"); assert a.rid() == ("count", ("literal", "B")), a.rid()
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
keys("ggj"); keys("2L"); assert len(a.sheet["sections"][0]["items"]) == n0 + 2
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
from sheets.banks.fixed import FixedBank
f = Path(OUT) / "words.json"
f.write_text(json.dumps({"format": 1, "name": "words", "title": "Word Problems",
    "types": [{"key": "rate", "title": "Rate Problems", "width": "full", "space": "2in"}],
    "problems": [{"id": "w1", "type": "rate", "prompt": "A train goes $60$ miles in $1.5$ hours. How fast?",
                  "answer": "$40$ mph", "text": "A train goes 60 miles in 1.5 hours. How fast?"},
                 {"id": "w2", "type": "rate", "prompt": "Pat walks $3$ miles in $1$ hour. How far in $4$?",
                  "answer": "$12$ miles"}]}))
banks._fixed["words"] = FixedBank(f)
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
wk("/Clear One\n"); assert w.rid() == ("count", ("literal", "3")), w.rid()
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
del banks._fixed["words"]

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
print("all key tests passed")
