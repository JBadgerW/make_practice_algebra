"""The screen stays quick as the library grows: a frame is drawn headless (no
terminal) and timed, with the real banks and with a made-up library of a
thousand. Run from the project folder:  python3 tests/test_perf.py

The budget is per frame, the time between a key and the screen showing it.
A frame that recomputes the course view, or rebuilds the bank tree for
each row, blows it at once, which is what this guards against."""
import os, statistics, sys, tempfile, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="config_")    # never the teacher's own config
(Path(os.environ["XDG_CONFIG_HOME"]) / "mathsheet").mkdir()
(Path(os.environ["XDG_CONFIG_HOME"]) / "mathsheet" / "config.json").write_text(
    '{"library": "%s"}' % tempfile.mkdtemp(prefix="emptylib_"))
import mathsheet as T
from sheets import library

BUDGET_MS = 15          # a frame, cursor moving, every bank open
BUDGET_OPEN_MS = 150    # the one frame that rebuilds the tree after zR, with 1000 banks

class Scr:
    """Enough of a curses window to draw into."""
    def __init__(self, h=50, w=180): self.h, self.w = h, w
    def getmaxyx(self): return self.h, self.w
    def erase(self): pass
    def addstr(self, *a): pass
    def move(self, *a): pass
    def refresh(self): pass

T.cursor = lambda visible: None
def screen():
    s = T.Screen.__new__(T.Screen)
    s.scr = Scr()
    s.st = {k: 0 for k in "plain head ans special dim count err title ital page normal insert "
                          "command search visual sel".split()}
    return s

views = [0]
_view = library.Library._view
def counted(self, *a):
    views[0] += 1
    return _view(self, *a)
library.Library._view = counted

def frame_ms(app, scr, keys="j", n=30):
    """The median time of n frames, each after one of keys (cycled)."""
    out = []
    for i in range(n):
        app.key(keys[i % len(keys)])
        t = time.perf_counter()
        scr.draw(app)
        out.append((time.perf_counter() - t) * 1000)
    return statistics.median(out)

def check(app, label):
    scr = screen()
    scr.draw(app)                                     # warm: the first frame builds the tree
    views[0] = 0
    ms = frame_ms(app, scr, "jjjk")
    assert views[0] == 0, f"{label}: moving the cursor recomputed the course view {views[0]} times"
    assert ms < BUDGET_MS, f"{label}: {ms:.1f} ms a frame (budget {BUDGET_MS})"
    t = time.perf_counter()
    app.key("z"); app.key("R")                        # open every bank: one rebuild
    scr.draw(app)
    opening = (time.perf_counter() - t) * 1000
    assert opening < BUDGET_OPEN_MS, f"{label}: zR took {opening:.0f} ms (budget {BUDGET_OPEN_MS})"
    views[0] = 0
    open_ms = frame_ms(app, scr, "jjjjk")
    assert views[0] == 0, f"{label}, all open: the course view was recomputed {views[0]} times"
    assert open_ms < BUDGET_MS, f"{label}, all open: {open_ms:.1f} ms a frame (budget {BUDGET_MS})"
    print(f"  {label}: {ms:.2f} ms a frame; zR {opening:.0f} ms; all open {open_ms:.2f} ms a frame "
          f"({len(app.rows())} rows)")

# ---- the real library, every course
print("frame times:")
for course in [c["title"] for c in library.current().courses] + ["all"]:
    a = T.App(seed=1)
    a.ex(f"course {course}")
    check(a, course)

# ---- with a sheet of problems: a frame doesn't redo the sheet's counts or layout
a = T.App(seed=2)
a.ex("course Algebra 1")
a.ex("mix all:2")
a.key("\t")
check(a, f"Algebra 1, {a.total()} problems, sheet focus")

# ---- a made-up library of 1000 banks, 5 types each, in Algebra 1's units
class FakeBank:
    FIXED = False
    INSTRUCTIONS = "Solve."
    def __init__(self, i, units):
        self.NAME = self.FAMILY = f"zz_fake_{i:04d}"
        self.TITLE = f"Fake Lesson {i // 10}-{i % 10}"
        self.COURSES = {"Algebra 1": units[i % len(units)]}
        self.ENTRIES = [dict(key=str(t), type=str(t), title=f"Type {t}", width="half", space="1in")
                        for t in range(1, 6)]
        self.ENTRY = {e["key"]: e for e in self.ENTRIES}
        self.TYPE = {str(t): ({"courses": {"Algebra 2": None}} if t == 5 else {}) for t in range(1, 6)}
    def type_of(self, entry): return entry
    def special(self, typ): return False
    def hint(self, typ): return None
    def heading(self, typ): return f"Type {typ}"

lib = library.current()
units = lib.course("Algebra 1")["units"]
for i in range(1000):
    b = FakeBank(i, units)
    lib.generators[b.NAME] = b
lib._memo.clear()
a = T.App(seed=3)
a.ex("course Algebra 1")
check(a, f"{len(lib.names())} banks, Algebra 1")
a.ex("course all")
check(a, f"{len(lib.names())} banks, all")

print("all perf tests passed")
