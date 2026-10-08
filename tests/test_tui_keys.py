"""Drive practice_tui.App with scripted keys (no terminal needed).
Run from literal_sequence/:  python3 tests/test_tui_keys.py"""
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import practice_tui as T, make_practice as mp
OUT = tempfile.mkdtemp(prefix="practice_tui_test_")
a = T.App(seed=12)
def keys(s):
    for c in s: a.key(c)
def st(): return {k:v for k,v in a.s["counts"].items() if v}
keys("2j"); assert a.row == 2
keys("3l"); assert st() == {"3": 3}, st()
keys("j6l"); assert st() == {"3": 3, "4": 6}
keys("h"); assert a.s["counts"]["4"] == 5
keys("."); assert a.s["counts"]["4"] == 4, "repeat"
keys("u"); assert a.s["counts"]["4"] == 5, "undo"
keys("\x12"); assert a.s["counts"]["4"] == 4, "redo"
keys("dd"); assert a.s["counts"]["4"] == 0
keys("\x01\x01"); assert a.s["counts"]["4"] == 2, "ctrl-a"
keys("gg"); assert a.row == 0
keys("G"); assert a.row == len(T.ROWS)-1
keys("5G"); assert a.row == 4
keys("/square\n"); assert T.ROWS[a.row] == ("count","B"), a.row
keys("/seed\n"); assert T.ROWS[a.row] == ("set","seed")
keys("cc99\n"); assert a.s["seed"] == 99
keys("k"); keys("i\x153\n"); assert a.s["versions"] == 3, a.s["versions"]
keys("jjl"); assert a.s["style"] == "letters"
keys("jl"); assert a.s["shuffle"]
keys("j"); keys("cc\n"); assert a.err and "empty" in a.msg, a.msg
keys(":mix 1:2 A:1\n"); assert st() == {"1": 2, "A": 1}
keys(":set noshuffle style=formulas\n"); assert a.s["style"]=="formulas" and not a.s["shuffle"], a.msg
keys(":set title=Quiz 3 Review\n"); assert a.s["title"] == "Quiz 3 Review"
assert a.s["class"] == "Algebra 1"
keys(":class Geometry\n"); assert a.s["class"] == "Geometry"
keys(":set class=Pre Algebra\n"); assert a.s["class"] == "Pre Algebra"
keys(":versions 2\n"); assert a.s["versions"] == 2
keys(":bogus\n"); assert a.msg.startswith("E492")
keys(":mix 12:1\n"); assert a.err
keys(":q\n"); assert a.msg.startswith("E37") and not a.quit
a.refresh_preview(); assert len(a.sets) == 2 and len(a.sets[0]) == 3
keys("za"); assert a.answers
keys("gt"); assert a.version == 1
keys("gt"); assert a.version == 0
keys("2gt"); assert a.version == 1
keys(f":out {OUT}\n")
keys(":w\n"); assert not a.err and not a.dirty()
assert a.sets == a.last_build["sets"], "preview must equal what :w wrote"
b = T.App(); b.load(str(a.last_build["out"] / "literal_practice_v1.json")); assert b.s == a.s, (b.s, a.s)
keys("D"); assert a.total()==0; keys("u"); assert a.total()==3
keys(":q\n"); assert a.quit
assert T.pretty("V = 1/3 pi r^2 h") == "V = (1/3)πr²h"
assert T.pretty("x = (2 m + n)/(5 - m)") == "x = (2m + n)/(5 − m)"
# ---- groups: reorder, join, split, rename
g = T.App(seed=5)
def gk(s):
    for c in s: g.key(c)
def order(): return ["+".join(x["types"]) for x in g.layout()]
gk(":mix 3:2 4:2 8:2 9:2 A:1\n"); assert order() == ["3", "4", "8", "9", "A"] and g.s["groups"] == []
gk("\t"); assert g.focus == "groups" and g.pane == "groups"
gk(">"); assert order() == ["4", "3", "8", "9", "A"] and g.grow == 1, order()
gk("<"); assert order() == ["3", "4", "8", "9", "A"]
gk("2>"); assert order() == ["4", "8", "3", "9", "A"] and g.grow == 2
gk("G"); assert g.grow == 4
gk("dd"); assert g.held == "A"
gk("gg"); gk("P"); assert order() == ["A", "4", "8", "3", "9"] and g.grow == 0, order()
gk("u"); assert order() == ["4", "8", "3", "9", "A"], "undo a move"
gk("\x12"); assert order()[0] == "A", "redo"
gk("p"); assert g.err and "nothing picked up" in g.msg
gk("jJ"); assert order() == ["A", "4+8", "3", "9"], order()
gk("S"); assert order() == ["A", "4", "8", "3", "9"]
gk("J"); gk("i"); assert g.mode == "insert" and g.buf == "Mixed Practice (4, 8)", g.buf
gk("\x15Warm-up\n"); assert g.layout()[1]["name"] == "Warm-up"
gk("i\x15\n"); assert g.layout()[1]["name"] == "", "empty resets"
gk(":rename Hard ones\n"); assert mp.heading(g.layout()[1]) == "Hard ones"
gk("gg"); gk("l"); assert g.err, "l does nothing in groups"
gk("\t"); assert g.focus == "preview"; gk("\t"); assert g.focus == "left" and g.pane == "left"
gk("\t\t^Ww"); assert g.focus in ("groups", "preview")
g.set_focus("left")
# counts changing under a layout: zeroed types vanish, new types append
gk(":mix 3:1 4:1 8:1 9:1\n"); assert order() == ["4+8", "3", "9"], order()
gk(":groups 9 8 3+4=Easy\n"); assert order() == ["9", "8", "3+4"] and g.layout()[2]["name"] == "Easy"
gk(":groups 3 3\n"); assert g.err and "more than one" in g.msg
gk(":groups\n"); assert order() == ["3", "4", "8", "9"]
gk(":groups 9 8 3+4=Easy\n")
g.refresh_preview()
assert [p["group"] for p in g.sets[0]] == [0, 1, 2, 2], g.sets[0]
assert sorted({p["group"] for p in g.sets[0]}) == [0, 1, 2], g.sets[0]
assert [p["type"] for p in g.sets[0]][:2] == ["9", "8"]
gk(f":out {OUT}\n:w\n"); assert not g.err, g.msg
cmd = g.last_build["command"]; assert "--groups 9 8 3+4=Easy" in cmd, cmd
h = T.App(); h.load(str(g.last_build["out"] / "literal_practice_v1.json"))
assert h.s["groups"] == g.layout(), (h.s["groups"], g.layout())
mixc = {"3": 2, "4": 2}
a1 = mp.draw_versions(mixc, 1, 7)[0]; a2 = mp.draw_versions(mixc, 1, 7, groups=[])[0]
assert a1 == a2, "default layout draws the same as before groups existed"
assert mp.layout(mp.parse_groups(["3+4"]), {"3": 1}) == [dict(types=["3"], name="")]
print("group tests passed")
print("all key tests passed")
