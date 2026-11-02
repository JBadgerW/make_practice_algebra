"""App: the state, the caches keyed by revision, change() and undo; the rest of its
methods come from one mixin per part (see tui/__init__.py)."""
import copy, random
import make_practice as mp
from sheets import sheet as sh, banks, library
from .common import SHEET, start_out
from .tree import Tree
from .sheet import SheetEdits
from .render import Render
from .files import Files
from .commands import Commands
from .keys import Keys
from .info import Info

# ------------------------------------------------------------------
# State and editing (no curses here, so it can be driven by tests)
# ------------------------------------------------------------------
class App(Tree, SheetEdits, Render, Files, Commands, Keys, Info):
    def __init__(self, seed=None, sheet=None, out=None, name=None):
        self.rng = random.Random(seed)
        self.s = dict(sheet=sheet or sh.new_sheet(mp.DEFAULTS["title"], None),
                      out=out or start_out(),
                      name=name or mp.DEFAULTS["name"])
        self.sheet.setdefault("course", library.config().get("course"))     # the course used last
        if not self.sheet.get("class_name"):                                # no --class: the course's
            self.sheet["class_name"] = self.course or mp.DEFAULTS["class_name"]
        self.undo, self.redo = [], []
        self.rev = 0                    # bumped whenever self.s may have changed: what the caches key on
        self._memo = (None, {})         # (rev, library) -> values derived from the sheet (see memo)
        self.drawn, self.cancel = 0, False  # problems drawn by the key being handled; Esc asked it to stop
        self._changing = 0              # how deep in change() we are: only a change can be cancelled
        self.row, self.focus, self.version = 2, "left", 0
        self.open = set()               # banks and sequences open in the tree: all closed at start
        self.open_types = set()         # (bank, type) showing its problems; (sequence, step) its examples
        self.cur = SHEET
        self.anchor = None              # where v was pressed: a selection runs from here to the cursor
        self.last_sel = None            # (anchor, cursor) of the last selection, for gv
        self.answers = self.compact = self.folded = False
        self.wide = False               # the sheet fills the screen while it has focus
        self.pv_top = 0
        self.mode = "normal"            # normal, insert, command, search, help, info
        self.resume_info = False        # back to the info box when an edit started from it ends
        self.buf, self.editing = "", None
        self.count, self.pending = "", ""
        self.msg, self.err = "Press ? for help.  l adds a problem; Tab moves to the sheet.", False
        self.last_change = None         # a function that repeats the last change (for .)
        self.search_q = ""
        self.cmd_hist, self.hist_i = [], 0
        self.comp = None                # Tab completion in progress: dict(start, options, i, buf)
        self.written = None             # the state at the last :w (or when a file was opened)
        self.reg = None                 # dict(kind="items"|"section", what=..., cut=bool)
        self.last_build = None
        self.preview_dir = None         # the temp folder :pre compiles into, made on the first :pre
        self.quit = False
        self.row = next((i for i, r in enumerate(self.rows()) if r[0] in ("seq", "bank")), 0)   # the first to open
        self.clamp()
        if banks.errors():
            self.say("E: " + "; ".join(banks.errors()), True)

    @property
    def sheet(self):
        return self.s["sheet"]

    @property
    def course(self):
        """The course whose banks the left pane shows (its title), or None for all."""
        c = library.current().course(self.sheet.get("course"))
        return c["title"] if c else None

    def seeds(self):
        return iter(lambda: self.rng.randrange(2**31), None)

    # -- values --------------------------------------------------------
    def total(self):
        return self.memo("total", lambda: len(sh.items(self.sheet)))

    def memo(self, key, make):
        """make(), computed once until the sheet or the library changes."""
        stamp = (self.rev, library.current())
        if self._memo[0] != stamp:
            self._memo = (stamp, {})
        d = self._memo[1]
        if key not in d:
            d[key] = make()
        return d[key]

    def dirty(self):
        return self.memo("dirty", lambda: self.written != self.s)

    def snapshot(self):
        return copy.deepcopy(self.s)

    def change(self, fn):
        """Run fn, which edits self.s; undoable. A ValueError or RuntimeError
        undoes it and becomes the message. Returns True if it worked."""
        before, layout = self.snapshot(), self.layout()
        self.rev += 1
        self._changing += 1
        try:
            fn()
        except (ValueError, RuntimeError) as e:
            self.s = before
            self.say(f"E: {e}".splitlines()[0], True)
            return False
        except sh.Cancelled:
            self.s = before
            if self._changing > 1:              # a change inside a change: undo the outer one too
                raise
            self.say("cancelled: nothing changed")
            return False
        finally:
            self._changing -= 1
        if self.anchor is not None and self.layout() != layout:
            self.end_visual()                  # its positions no longer mean the same problems
        if self.s != before:
            self.undo.append(before)
            self.redo.clear()
        self.clamp()
        return True

    def progress(self):
        """Called before each problem is drawn (sheet.progress): counts them for the
        status line, and stops the change in progress once Esc has asked."""
        self.drawn += 1
        if self.cancel and self._changing:
            raise sh.Cancelled()

    def layout(self):
        """Which problem is where (by identity), to tell a change that moves them."""
        return [[id(it) for it in sec["items"]] for sec in self.sheet["sections"]]

    def say(self, msg, err=False):
        self.msg, self.err = msg, err

    def statuses(self):
        return self.memo("statuses", self._statuses)

    def _statuses(self):
        its = sh.items(self.sheet)
        return (sum(it["status"] == "unchecked" for it in its), sum(it["status"] == "failed" for it in its))

    def missing(self):
        """The banks this sheet uses that the library doesn't have."""
        return list(self.memo("missing", self._missing))

    def _missing(self):
        return sorted({it["bank"] for it in sh.items(self.sheet) if not banks.has(it["bank"])})

    # -- undo ----------------------------------------------------------
    def do_undo(self, n=1):
        for _ in range(n):
            if not self.undo:
                return self.say("Already at oldest change")
            self.redo.append(self.snapshot())
            self.s = self.undo.pop()
            self.rev += 1
            self.end_visual()
        self.clamp()
        self.say(f"{n} change{'s' * (n > 1)} undone")

    def do_redo(self, n=1):
        for _ in range(n):
            if not self.redo:
                return self.say("Already at newest change")
            self.undo.append(self.snapshot())
            self.s = self.redo.pop()
            self.rev += 1
            self.end_visual()
        self.clamp()
        self.say(f"{n} change{'s' * (n > 1)} redone")

    def repeat(self, n=1):
        if self.last_change:
            for _ in range(n):
                self.last_change()
