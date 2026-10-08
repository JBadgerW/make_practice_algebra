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
print("all key tests passed")
