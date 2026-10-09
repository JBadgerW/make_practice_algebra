"""Terminal front end for make_practice.py, driven with vim keys.

    python3 practice_tui.py                       # start empty
    python3 practice_tui.py --mix 3:6 8:4 --seed 12
    python3 practice_tui.py practice/literal_practice.sheet.json   # reopen a set

The left pane holds a count for every entry (each type's made-up equations,
and its real formulas: 3 and 3f) plus the settings; the right pane previews
exactly the sheet :w will write (same seed, same draw). Press ? inside for
the full key list.
"""
import copy, curses, json, os, random, re, shlex, subprocess, sys, textwrap
from pathlib import Path
import make_practice as mp
from sheets import sheet as sh, banks
from sheets.banks.literal import pretty

# ------------------------------------------------------------------
# Rows in the left pane
# ------------------------------------------------------------------
SETTINGS = ["versions", "seed", "order", "title", "class", "name", "out"]
ROWS = [("count", k) for k in mp.KEYS] + [("set", s) for s in SETTINGS]
ORDERS = ("grouped", "shuffled")
SETTING_HINTS = {
    "versions": "How many parallel versions to write (h/l, or i to type one): each problem is redrawn in its slot. Each version gets its own worksheet, key, and slides.",
    "seed": "The same seed always draws the same problems. r picks a new one; i types one in.",
    "order": "grouped: problems sit under type headings.  shuffled: types interleaved, no headings. (h/l)",
    "title": "The worksheet and slide title. i to edit.",
    "class": "The class name in the worksheet and slide header (default Algebra 1). i to edit.",
    "name": "File prefix: NAME_v1.pdf, NAME_v1_key.pdf, NAME_v1_slides.pdf. i to edit.",
    "out": "Folder to write into, relative to this script's folder. i to edit.",
}

HELP = """\
MOVE                                  CHANGE THE ROW UNDER THE CURSOR
j k  ↓ ↑   down / up (5j)             l + →  ^A  add one (3l adds 3)
gg  G      first / last row (7G)      h - ←  ^X  take one away
/text n N  search, next / previous    x  dd      set to zero
^D  ^U     half page down / up        i a Enter  type a new value
Tab  ^W w  types > groups > preview   D          zero every type
                                      cc  s      erase, then type a value
                                      u  ^R      undo / redo
PREVIEW                               .          repeat last change
za         answers on / off           r          new random seed
gt  gT     next / prev version (3gt)
                                      FILES
COMMANDS                              :w         write sheets, keys, decks
:mix 3:6 8:4 A:2  set the counts      :wq :x ZZ  write, then quit
:mix all:2        two of every type   :q :q! ZQ  quit (:q! discards)
:seed [N]  :versions N  :clear        :e FILE.sheet.json  reopen
:mix 3f:4 allf:1  real formulas       :open [sheet|key|slides] [N]
:set [no]shuffle [no]answers key=value    :title  :class  :name  :out  :N  :help

GROUPS PANE (Tab once from types): the sections of the worksheet, in print order
> <  move the group down / up (3> )   J  join with the group below (mixed)
dd then p / P  pick up, drop below / above   S  split a mixed group apart
i a Enter  rename the heading (empty = default)   s cc  erase, then type
:groups 9 8 3+4=Warm-up 1  set it all at once    :groups  back to sequence order
:rename TEXT  rename the group under the cursor

Types 1-11 are the lesson's sequence; A and B are the special cases.
A row ending in f (3f) draws real formulas of that type.
Any key closes this help."""

# ------------------------------------------------------------------
# State and editing (no curses here, so it can be driven by tests)
# ------------------------------------------------------------------
class App:
    def __init__(self, mix=None, seed=None, **settings):
        self.s = dict(counts={k: 0 for k in mp.KEYS}, seed=seed if seed is not None else random.randrange(10**6),
                      versions=mp.DEFAULTS["versions"],
                      shuffle=mp.DEFAULTS["shuffle"], title=mp.DEFAULTS["title"], **{"class": mp.DEFAULTS["class_name"]},
                      out=mp.DEFAULTS["out"], name=mp.DEFAULTS["name"], groups=[])
        self.s["counts"].update(mix or {})
        self.s.update({k: v for k, v in settings.items() if v is not None})
        self.undo, self.redo = [], []
        self.row, self.focus, self.version = 0, "left", 0
        self.pane = "left"              # which view the left column shows: left (types) or groups
        self.grow = 0                   # cursor row in the groups view
        self.held = None                # first type of a group picked up with dd
        self.answers = False
        self.pv_top = 0
        self.mode = "normal"            # normal, insert, command, search, help
        self.buf, self.edit_clear = "", False
        self.count, self.pending = "", ""
        self.msg, self.err = "Press ? for help.  l adds a problem to the type under the cursor.", False
        self.last_change = None
        self.search_q = ""
        self.cmd_hist, self.hist_i = [], 0
        self.written = None             # snapshot at the last :w
        self.last_build = None
        self.sheet, self.sheet_key = None, None
        self.quit = False

    # -- values --------------------------------------------------------
    def total(self):
        return sum(self.s["counts"].values())

    def mix(self):
        return {k: n for k, n in self.s["counts"].items() if n}

    def value(self, row):
        kind, key = ROWS[row]
        if kind == "count":
            return self.s["counts"][key]
        if key == "order":
            return "shuffled" if self.s["shuffle"] else "grouped"
        return self.s[key]

    def dirty(self):
        return self.total() > 0 and self.written != self.snapshot()

    def snapshot(self):
        return copy.deepcopy(self.s)

    def change(self, fn):
        before = self.snapshot()
        fn()
        if self.s != before:
            self.undo.append(before)
            self.redo.clear()

    def say(self, msg, err=False):
        self.msg, self.err = msg, err

    # -- edits on the current row --------------------------------------
    def bump(self, n, row=None):
        row = self.row if row is None else row
        kind, key = ROWS[row]
        def go():
            if kind == "count":
                self.s["counts"][key] = max(0, self.s["counts"][key] + n)
            elif key == "versions":
                self.s["versions"] = min(26, max(1, self.s["versions"] + n))
            elif key == "seed":
                self.s["seed"] = max(0, self.s["seed"] + n)
            elif key == "order":
                if n % 2:
                    self.s["shuffle"] = not self.s["shuffle"]
            else:
                self.say(f"{key} is text: press i to edit it", True)
        self.change(go)
        self.last_change = ("bump", n)

    def zero(self, row=None):
        row = self.row if row is None else row
        kind, key = ROWS[row]
        def go():
            if kind == "count":
                self.s["counts"][key] = 0
            elif key == "versions":
                self.s["versions"] = 1
            else:
                self.say(f"x and dd only zero counts and versions", True)
        self.change(go)
        self.last_change = ("zero",)

    def set_value(self, text, row=None):
        """Apply typed text to a row; returns an error string or None."""
        row = self.row if row is None else row
        kind, key = ROWS[row]
        text = text.strip()
        if kind == "count" or key in ("versions", "seed"):
            if not text.isdigit():
                return f"{key if kind == 'set' else 'count'} must be a whole number"
            n = int(text)
            if key == "versions" and not 1 <= n <= 26:
                return "versions must be 1-26"
            if kind == "count":
                self.change(lambda: self.s["counts"].__setitem__(key, n))
            else:
                self.change(lambda: self.s.__setitem__(key, n))
        elif key == "order":
            hit = [x for x in ORDERS if x.startswith(text.lower())] if text else []
            if len(hit) != 1:
                return "order is grouped or shuffled"
            self.change(lambda: self.s.__setitem__("shuffle", hit[0] == "shuffled"))
        else:
            if not text:
                return f"{key} can't be empty"
            if key == "name" and not re.fullmatch(r"[\w.-]+", text):
                return "name may use letters, digits, _ . - only"
            self.change(lambda: self.s.__setitem__(key, text))
        self.last_change = ("set", text)
        return None

    def do_undo(self, n=1):
        for _ in range(n):
            if not self.undo:
                return self.say("Already at oldest change")
            self.redo.append(self.snapshot())
            self.s = self.undo.pop()
        self.say(f"{n} change{'s' * (n > 1)} undone")

    def do_redo(self, n=1):
        for _ in range(n):
            if not self.redo:
                return self.say("Already at newest change")
            self.undo.append(self.snapshot())
            self.s = self.redo.pop()
        self.say(f"{n} change{'s' * (n > 1)} redone")

    def repeat(self, n=1):
        if not self.last_change:
            return
        what = self.last_change
        for _ in range(n):
            if what[0] == "bump":
                self.bump(what[1])
            elif what[0] == "zero":
                self.zero()
            elif what[0] == "set":
                err = self.set_value(what[1])
                if err:
                    return self.say(err, True)

    # -- preview -------------------------------------------------------
    def preview_key(self):
        return (tuple(sorted(self.mix().items())), self.s["versions"], self.s["seed"],
                self.s["shuffle"], tuple((tuple(g["types"]), g["name"]) for g in self.layout()))

    def stale(self):
        return self.sheet_key != self.preview_key()

    def refresh_preview(self):
        key = self.preview_key()
        if not self.total():
            self.sheet, self.sheet_key = None, key
            return
        try:
            self.sheet = mp.draft(self.mix(), self.s["versions"], self.s["seed"],
                                  self.s["shuffle"], self.s["groups"])
        except RuntimeError as e:
            self.sheet = None
            self.say(str(e), True)
        self.sheet_key = key
        self.version = min(self.version, self.s["versions"] - 1)

    def preview_lines(self):
        """[(text, style)] for the preview pane; style in plain/head/dim/ans/special."""
        if not self.total():
            return [("No problems yet.", "head"), ("", "plain"),
                    ("Move to a type with j/k and press l to add one,", "dim"),
                    ("or type  :mix all:2  for two of every type.", "dim")]
        if self.sheet is None or self.stale():
            return [("drawing…", "dim")]
        order = "shuffled" if self.s["shuffle"] else "grouped"
        out = [(f"Version {self.version + 1}/{self.s['versions']} · {order} · "
                f"answers {'on' if self.answers else 'off'} (za)"
                + (" · gt next" if self.s["versions"] > 1 else ""), "dim"), ("", "plain")]
        i, lay = 0, self.layout()
        for j, sec in enumerate(self.sheet["sections"]):
            if sec["title"]:
                if i:
                    out.append(("", "plain"))
                g = lay[j] if j < len(lay) else dict(types=[])
                special = len(g["types"]) == 1 and mp.L.special(g["types"][0])
                out.append((sec["title"], "special" if special else "head"))
            if sec["instructions"]:
                out.append((sec["instructions"], "dim"))
            for it in sec["items"]:
                i += 1
                b, p = banks.get(it["bank"]), sh.problem(it, self.version)
                tag = f"   [{it['entry']}]" if self.s["shuffle"] else ""
                src = "  (formula)" if p.get("source") == "formula" else ""
                out.append((f"{i:>3}. {b.text(p)}{tag}{src}", "plain"))
                if self.answers:
                    out.append((f"       {b.answer_text(p)}", "ans"))
        return out

    # -- files ---------------------------------------------------------
    def write(self):
        if not self.total():
            return self.say("E: nothing to write: every count is 0", True) or False
        if self.stale():
            self.refresh_preview()
        if self.sheet is None:
            return self.say(self.msg if self.err else "E: nothing to write", True) or False
        sheet = copy.deepcopy(self.sheet)
        sheet.update(title=self.s["title"], class_name=self.s["class"],
                     command=mp.command_for(self.mix(), self.s["versions"], self.s["seed"], self.s["shuffle"],
                                            self.s["title"], self.s["out"], self.s["name"], self.s["class"],
                                            self.s["groups"]))
        try:
            r = mp.build(sheet, self.s["out"], self.s["name"])
        except (RuntimeError, OSError) as e:
            self.say(f"E: {e}".splitlines()[0], True)
            return False
        self.written, self.last_build = self.snapshot(), r
        n = len(r["files"])
        try:
            where = r["out"].relative_to(Path.cwd())
        except ValueError:
            where = r["out"]
        self.say(f'"{where}/" {n} files written ({"PDFs compiled" if r["compiled"] else "typst not found: .typ only"})')
        return True

    def open_file(self, args):
        if not self.last_build:
            return self.say("E: nothing written yet (:w first)", True)
        what, v = "sheet", 1
        for a in args:
            if a.isdigit():
                v = int(a)
            elif a in ("sheet", "key", "slides"):
                what = a
            else:
                return self.say("usage: :open [sheet|key|slides] [version]", True)
        b = self.last_build
        if not 1 <= v <= b["sheet"]["versions"]:
            return self.say(f"E: there are {b['sheet']['versions']} versions", True)
        suffix = {"sheet": "", "key": "_key", "slides": "_slides"}[what]
        f = b["out"] / f"{self.s['name']}_v{v}{suffix}.{'pdf' if b['compiled'] else 'typ'}"
        try:
            subprocess.Popen(["xdg-open", str(f)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
            self.say(f"opening {f.name}")
        except OSError as e:
            self.say(f"E: {e}", True)

    def load(self, path):
        """Reopen the settings a .sheet.json (or an older practice .json) was made with."""
        try:
            d = json.loads(Path(path).read_text())
            cmd = d["command"]
            a = parse_args(shlex.split(cmd)[2:])
            mix = mp.apply_style(mp.parse_mix(a.mix), a.style)
            groups = mp.parse_groups(a.groups)
        except (OSError, ValueError, KeyError, TypeError, SystemExit) as e:
            return self.say(f"E: can't read settings from {path}: {e}", True)
        def go():
            self.s["counts"] = {k: mix.get(k, 0) for k in mp.KEYS}
            self.s.update(seed=a.seed, versions=a.versions, shuffle=a.shuffle,
                          title=a.title, out=a.out, name=a.name, groups=groups, **{"class": a.class_name})
        self.change(go)
        self.written = self.snapshot()
        if d.get("format") == sh.FORMAT:
            self.say(f'"{path}" loaded: {self.total()} problems, seed {a.seed}')
        else:
            self.say(f'"{path}" is an older file: its settings are loaded, but the problems are drawn anew '
                     f'(make_practice.py --sheet FILE reprints the old ones)')

    # -- ex commands -----------------------------------------------------
    def ex(self, line):
        line = line.strip()
        if not line:
            return
        if line.isdigit():
            self.row = min(len(ROWS), max(1, int(line))) - 1
            return
        cmd, _, rest = line.partition(" ")
        rest = rest.strip()
        bang = cmd.endswith("!")
        cmd = cmd.rstrip("!")
        if cmd in ("w", "write"):
            self.write()
        elif cmd in ("wq", "x", "xit"):
            if self.write():
                self.quit = True
        elif cmd in ("q", "quit", "qa", "qall"):
            if self.dirty() and not bang:
                self.say("E37: No write since last change (add ! to override)", True)
            else:
                self.quit = True
        elif cmd == "mix":
            try:
                mix = mp.parse_mix(rest.split())
            except ValueError as e:
                return self.say(f"E: {e}", True)
            self.change(lambda: self.s.__setitem__("counts", {k: mix.get(k, 0) for k in mp.KEYS}))
        elif cmd == "groups":
            try:
                self.set_groups(shlex.split(rest))
            except ValueError as e:
                self.say(f"E: {e}", True)
        elif cmd == "rename":
            if rest and self.layout():
                self.rename(rest)
            else:
                self.say("usage: :rename NEW HEADING   (for the group under the groups cursor)", True)
        elif cmd == "clear":
            self.change(lambda: self.s.__setitem__("counts", {k: 0 for k in mp.KEYS}))
        elif cmd == "seed" and not rest:
            self.reroll()
        elif cmd in ("seed", "versions", "title", "class", "name", "out", "order"):
            err = self.set_value(rest, ROWS.index(("set", cmd)))
            if err:
                self.say(f"E: {err}", True)
        elif cmd in ("set", "se"):
            self.ex_set(rest)
        elif cmd in ("e", "edit"):
            self.load(rest) if rest else self.say("usage: :e FILE.json", True)
        elif cmd == "open":
            self.open_file(rest.split())
        elif cmd in ("h", "help"):
            self.mode = "help"
        else:
            self.say(f"E492: Not an editor command: {line}", True)

    def ex_set(self, rest):
        opts = rest.split()
        for i, o in enumerate(opts):            # title=/class= keep their spaces
            if o.startswith(("title=", "class=")):
                opts = opts[:i] + [" ".join(opts[i:])]
                break
        for opt in opts:
            if opt in ("shuffle", "noshuffle", "shuffle!"):
                new = (not self.s["shuffle"]) if opt.endswith("!") else opt == "shuffle"
                self.change(lambda: self.s.__setitem__("shuffle", new))
            elif opt in ("answers", "noanswers", "answers!"):
                self.answers = (not self.answers) if opt.endswith("!") else opt == "answers"
            elif "=" in opt:
                k, _, v = opt.partition("=")
                k = k.strip()
                if ("set", k) not in ROWS:
                    return self.say(f"E518: Unknown option: {k}", True)
                err = self.set_value(v, ROWS.index(("set", k)))
                if err:
                    return self.say(f"E: {err}", True)
            else:
                return self.say(f"E518: Unknown option: {opt}", True)

    # -- groups ------------------------------------------------------------
    def layout(self):
        return mp.layout(self.s["groups"], self.mix())

    def grow_at(self):
        return min(self.grow, max(0, len(self.layout()) - 1))

    def edit_layout(self, fn):
        """fn edits a copy of the layout in place; stored (and undoable) only if it changed."""
        new = copy.deepcopy(self.layout())
        fn(new)
        if new != self.layout():
            self.change(lambda: self.s.__setitem__("groups", new))
            return True
        return False

    def move_group(self, n):
        i = self.grow_at()
        j = min(max(0, i + n), len(self.layout()) - 1)
        if i == j:
            return
        def go(lay):
            lay.insert(j, lay.pop(i))
        self.edit_layout(go)
        self.grow = j

    def pick_up(self):
        lay = self.layout()
        if not lay:
            return
        self.held = lay[self.grow_at()]["types"][0]
        self.say("group picked up: p drops it below the cursor, P above, Esc cancels")

    def drop(self, below):
        if self.held is None:
            return self.say("nothing picked up: dd picks up the group under the cursor", True)
        lay = self.layout()
        src = next((i for i, g in enumerate(lay) if self.held in g["types"]), None)
        dst = self.grow_at()
        self.held = None
        if src is None or src == dst:
            return
        target = lay[dst]
        def go(new):
            g = new.pop(src)
            at = next(i for i, x in enumerate(new) if x["types"] == target["types"])
            new.insert(at + (1 if below else 0), g)
            self.grow = new.index(g)
        self.edit_layout(go)

    def join(self):
        i = self.grow_at()
        if i + 1 >= len(self.layout()):
            return self.say("no group below to join", True)
        def go(lay):
            lay[i] = dict(types=lay[i]["types"] + lay.pop(i + 1)["types"], name="")
        self.edit_layout(go)
        self.say("joined (u to undo): its problems are shuffled together")

    def split(self):
        i = self.grow_at()
        if len(self.layout()[i]["types"]) < 2:
            return self.say("that group is already a single type", True)
        def go(lay):
            lay[i:i + 1] = [dict(types=[k], name="") for k in lay[i]["types"]]
        self.edit_layout(go)

    def rename(self, text):
        text = text.strip()
        i = self.grow_at()
        def go(lay):
            lay[i]["name"] = "" if text == mp.default_heading(lay[i]) else text
        self.edit_layout(go)
        self.say("heading reset to the default" if not text else f"renamed: {mp.heading(self.layout()[i])}")

    def set_groups(self, tokens):
        try:
            groups = mp.parse_groups(tokens)
        except ValueError as e:
            return self.say(f"E: {e}", True)
        self.change(lambda: self.s.__setitem__("groups", groups))
        self.grow = 0

    def key_groups(self, c, ch, n):
        """Keys specific to the groups view. True if handled here."""
        if c == "\x1b":
            self.held = None
            return False
        if c == ">":
            self.move_group(n)
        elif c == "<":
            self.move_group(-n)
        elif c == "p":
            self.drop(True)
        elif c == "P":
            self.drop(False)
        elif c == "J":
            self.join()
        elif c == "S":
            self.split()
        elif c in ("i", "a", "s", "\n", "\r") or ch == curses.KEY_ENTER:
            self.start_insert(clear=(c == "s"))
        elif c in ("l", "h", "+", "-", "x", "D", ".", "\x01", "\x18") or ch in (curses.KEY_LEFT, curses.KEY_RIGHT):
            self.say("groups: > < move, dd then p/P moves far, J joins, S splits, i renames", True)
        else:
            return False
        return True

    def reroll(self):
        self.change(lambda: self.s.__setitem__("seed", random.randrange(10**6)))
        self.say(f"seed {self.s['seed']}")

    def search(self, q, step=1):
        if not q:
            return
        n = len(ROWS)
        for i in range(1, n + 1):
            r = (self.row + step * i) % n
            kind, key = ROWS[r]
            text = (f"{key} {mp.label(mp.TYPE[mp.L.type_of(key)])} {mp.ENTRY[key]['title']}"
                    if kind == "count" else key).lower()
            if q.lower() in text:
                self.row = r
                return self.say(f"/{q}")
        self.say(f"E486: Pattern not found: {q}", True)

    # -- keys ------------------------------------------------------------
    def key(self, ch, page=10):
        """Handle one key (an int as from curses getch, or a 1-char str)."""
        if isinstance(ch, str):
            ch = ord(ch)
        if self.mode == "help":
            self.mode = "normal"
            return
        if self.mode in ("insert", "command", "search"):
            return self.key_line(ch)
        c = chr(ch) if 0 <= ch < 0x110000 else ""
        self.msg, self.err = "", False

        if self.pending:
            p, self.pending = self.pending, ""
            n = int(self.count) if self.count else None
            self.count = ""
            combo = p + c
            if combo == "gg":
                if self.focus == "groups":
                    self.grow = min((n or 1) - 1, max(0, len(self.layout()) - 1))
                elif self.focus == "left":
                    self.row = (n or 1) - 1 if n else 0
                    self.row = min(self.row, len(ROWS) - 1)
                else:
                    self.pv_top = 0
            elif combo == "gt":
                if n:
                    self.version = min(n, self.s["versions"]) - 1
                else:
                    self.version = (self.version + 1) % self.s["versions"]
                self.pv_top = 0
            elif combo == "gT":
                self.version = (self.version - (n or 1)) % self.s["versions"]
                self.pv_top = 0
            elif combo == "dd":
                self.pick_up() if self.focus == "groups" else self.zero()
            elif combo == "cc":
                self.start_insert(clear=True)
            elif combo == "ZZ":
                self.ex("x")
            elif combo == "ZQ":
                self.quit = True
            elif combo == "za":
                self.answers = not self.answers
            elif p == "\x17" and c in ("w", "\x17", "h", "l"):
                self.set_focus({"h": self.pane, "l": "preview"}.get(c) or self.next_focus())
            return

        if c.isdigit() and (c != "0" or self.count):
            self.count += c
            return
        n = int(self.count) if self.count else 1
        had_count = bool(self.count)
        self.count = ""

        if self.focus == "groups" and c and self.key_groups(c, ch, n):
            return
        if c in "gdcZz\x17" and c:
            self.pending = c
            if had_count:
                self.count = str(n)
        elif c == "j" or ch == curses.KEY_DOWN:
            self.move(n)
        elif c == "k" or ch == curses.KEY_UP:
            self.move(-n)
        elif c == "G":
            if self.focus == "groups":
                last = max(0, len(self.layout()) - 1)
                self.grow = min(n - 1, last) if had_count else last
            elif self.focus == "left":
                self.row = min(n, len(ROWS)) - 1 if had_count else len(ROWS) - 1
            else:
                self.pv_top = 10**6
        elif c == "\x04":
            self.scroll(page // 2 * n) if self.focus == "preview" else self.move(5 * n)
        elif c == "\x15":
            self.scroll(-page // 2 * n) if self.focus == "preview" else self.move(-5 * n)
        elif c in ("\x06",) or ch == curses.KEY_NPAGE:
            self.scroll(page * n)
        elif c in ("\x02",) or ch == curses.KEY_PPAGE:
            self.scroll(-page * n)
        elif c in ("l", "+", "\x01") or ch == curses.KEY_RIGHT:
            self.bump(n)
        elif c in ("h", "-", "\x18") or ch == curses.KEY_LEFT:
            self.bump(-n)
        elif c == "x":
            self.zero()
        elif c == "D":
            self.change(lambda: self.s.__setitem__("counts", {k: 0 for k in mp.KEYS}))
            self.say("all counts zeroed (u to undo)")
        elif c in ("i", "a", "\n", "\r") or ch == curses.KEY_ENTER:
            self.start_insert()
        elif c == "s":
            self.start_insert(clear=True)
        elif c == "u":
            self.do_undo(n)
        elif c == "\x12":
            self.do_redo(n)
        elif c == ".":
            self.repeat(n)
        elif c == "r":
            self.reroll()
        elif c == ":":
            self.mode, self.buf = "command", ""
            self.hist_i = len(self.cmd_hist)
        elif c == "/":
            self.mode, self.buf = "search", ""
        elif c == "n":
            self.search(self.search_q, 1)
        elif c == "N":
            self.search(self.search_q, -1)
        elif c == "?":
            self.mode = "help"
        elif c == "\t":
            self.set_focus(self.next_focus())
        elif c == "\x1b":
            pass
        elif c == "\x03":
            self.say("Type  :q!  and press Enter to quit")

    def next_focus(self):
        return {"left": "groups", "groups": "preview", "preview": "left"}[self.focus]

    def set_focus(self, f):
        self.focus = f
        if f != "preview":
            self.pane = f

    def move(self, n):
        if self.focus == "groups":
            self.grow = min(max(0, len(self.layout()) - 1), max(0, self.grow + n))
        elif self.focus == "left":
            self.row = min(len(ROWS) - 1, max(0, self.row + n))
        else:
            self.scroll(n)

    def scroll(self, n):
        self.pv_top = max(0, self.pv_top + n)

    def start_insert(self, clear=False):
        if self.focus == "groups":
            lay = self.layout()
            if not lay:
                return self.say("no groups yet: add some problems first", True)
            self.mode, self.buf = "insert", "" if clear else mp.heading(lay[self.grow_at()])
            return
        kind, key = ROWS[self.row]
        self.mode, self.buf = "insert", "" if clear else str(self.value(self.row))

    def key_line(self, ch):
        c = chr(ch) if 0 <= ch < 0x110000 else ""
        if c == "\x1b" or (c == "\x03"):
            self.mode, self.buf = "normal", ""
        elif c in ("\n", "\r") or ch == curses.KEY_ENTER:
            mode, buf = self.mode, self.buf
            self.mode, self.buf = "normal", ""
            if mode == "insert" and self.focus == "groups":
                self.rename(buf)
            elif mode == "insert":
                err = self.set_value(buf)
                if err:
                    self.say(f"E: {err}", True)
            elif mode == "command":
                if buf.strip():
                    self.cmd_hist.append(buf)
                self.ex(buf)
            else:
                self.search_q = buf or self.search_q
                self.search(self.search_q)
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if not self.buf and self.mode != "insert":
                self.mode = "normal"
            self.buf = self.buf[:-1]
        elif c == "\x15":
            self.buf = ""
        elif c == "\x17":
            self.buf = re.sub(r"\S*\s*$", "", self.buf.rstrip()) if self.buf.strip() else ""
        elif self.mode == "command" and ch in (curses.KEY_UP, curses.KEY_DOWN) and self.cmd_hist:
            self.hist_i = max(0, min(len(self.cmd_hist), self.hist_i + (-1 if ch == curses.KEY_UP else 1)))
            self.buf = self.cmd_hist[self.hist_i] if self.hist_i < len(self.cmd_hist) else ""
        elif c.isprintable() and c:
            self.buf += c

# ------------------------------------------------------------------
# Drawing
# ------------------------------------------------------------------

def cursor(visible):
    try:                                # some terminals can't hide the cursor
        curses.curs_set(visible)
    except curses.error:
        pass

class Screen:
    def __init__(self, scr):
        self.scr = scr
        cursor(0)
        P = lambda i: 0                                # monochrome fallback
        if curses.has_colors():
            curses.start_color()
            try:
                curses.use_default_colors()
                bg = -1
            except curses.error:
                bg = curses.COLOR_BLACK
            for i, (fg, b) in enumerate([(curses.COLOR_CYAN, bg), (curses.COLOR_RED, bg),
                                         (curses.COLOR_YELLOW, bg), (curses.COLOR_GREEN, bg),
                                         (curses.COLOR_BLACK, curses.COLOR_BLUE),
                                         (curses.COLOR_BLACK, curses.COLOR_GREEN),
                                         (curses.COLOR_BLACK, curses.COLOR_YELLOW)], 1):
                curses.init_pair(i, fg, b)
            P = curses.color_pair
        self.st = dict(plain=0, head=P(1) | curses.A_BOLD, ans=P(2), special=P(3) | curses.A_BOLD,
                       dim=curses.A_DIM, count=P(4) | curses.A_BOLD, err=P(2) | curses.A_BOLD,
                       normal=P(5) | curses.A_BOLD, insert=P(6) | curses.A_BOLD,
                       command=P(7) | curses.A_BOLD, search=P(7) | curses.A_BOLD)

    def put(self, y, x, text, attr=0, width=None):
        h, w = self.scr.getmaxyx()
        if y < 0 or y >= h or x >= w:
            return
        width = min(width if width is not None else w - x, w - x)
        if len(text) > width:
            text = text[:max(0, width - 1)] + "…"
        try:
            self.scr.addstr(y, x, text, attr)
        except curses.error:            # writing the bottom-right cell
            pass

    def draw(self, app):
        scr, st = self.scr, self.st
        scr.erase()
        h, w = scr.getmaxyx()
        if h < 14 or w < 72:
            self.put(0, 0, f"Make the terminal at least 72x14 (now {w}x{h}).  :q! quits.")
            return self.cmdline(app, h, w)
        body = h - 3                                   # title, status, command lines
        LEFT_W = max(40, min(55, w - 50))
        self.put(0, 0, " Literal Equations Practice", st["head"])
        self.put(0, w - 12, "? for help", st["dim"])

        (self.groups_view if app.pane == "groups" else self.types_view)(app, body, LEFT_W)
        for y in range(1, body + 1):
            self.put(y, LEFT_W, "│", st["dim"])

        # right pane
        px, pw = LEFT_W + 2, w - LEFT_W - 3
        pv = app.preview_lines()
        app.pv_top = max(0, min(app.pv_top, len(pv) - body))
        for y, (text, s) in enumerate(pv[app.pv_top:app.pv_top + body], 1):
            self.put(y, px, text, st[s], pw)
        where = ""
        if len(pv) > body:
            where = "Top" if app.pv_top == 0 else "Bot" if app.pv_top >= len(pv) - body else \
                f"{100 * app.pv_top // (len(pv) - body)}%"
        self.status(app, h, w, where)

    def groups_view(self, app, body, LEFT_W):
        st = self.st
        lay = app.layout()
        self.put(1, 1, "GROUPS  (printed top to bottom)", st["dim"] | curses.A_BOLD)
        if app.s["shuffle"]:
            self.put(2, 1, "order is shuffled: groups are ignored", st["err"])
        elif not lay:
            self.put(2, 1, "no problems yet: add some on the types pane", st["dim"])
        cur = app.grow_at()
        top = max(0, min(cur - (body - 3) // 2, len(lay) - (body - 3)))
        counts = {i: sum(n for k, n in app.s["counts"].items() if mp.L.type_of(k) in g["types"])
                  for i, g in enumerate(lay)}
        for y, (i, g) in enumerate(list(enumerate(lay))[top:top + body - 3], 3):
            held = app.held is not None and app.held in g["types"]
            text = f" {i + 1:>2}{'▸' if held else ' '} {mp.heading(g)}"
            if g["name"]:
                text += f"  [{'+'.join(g['types'])}]"
            val = str(counts[i])
            room = LEFT_W - 3
            space = room - len(val) - 1
            text = text if len(text) <= space else text[:space - 1] + "…"
            row = text.ljust(space + 1) + val + " "
            if i == cur:
                self.put(y, 1, row, curses.A_REVERSE | (curses.A_BOLD if app.focus == "groups" else 0))
            else:
                mixed = len(g["types"]) > 1
                self.put(y, 1, text, st["special"] if mixed else 0)
                self.put(y, 1 + space + 1, val, st["count"])
        if body >= 12:
            hint = ("> < move  dd then p/P pick up and drop  J join with next  S split  "
                    "i rename (empty = default)  Tab: preview")
            for y, line in enumerate(textwrap.wrap(hint, LEFT_W - 3)[:body - 3 - min(len(lay), body - 3) - 1],
                                     min(len(lay), body - 3) + 4):
                self.put(y, 1, line, st["dim"])

    def types_view(self, app, body, LEFT_W):
        scr, st = self.scr, self.st
        lines = [("TYPES", None)] + [(None, i) for i in range(len(mp.KEYS))] + \
                [("", None), ("SETTINGS", None)] + [(None, i) for i in range(len(mp.KEYS), len(ROWS))]
        cur = next(j for j, (_, i) in enumerate(lines) if i == app.row)
        top = max(0, min(cur - body // 2, len(lines) - body))
        for y, (hdr, i) in enumerate(lines[top:top + body], 1):
            if hdr is not None:
                self.put(y, 1, hdr, st["dim"] | curses.A_BOLD)
                continue
            kind, key = ROWS[i]
            if kind == "count":
                ty = mp.TYPE[mp.L.type_of(key)]
                n = app.s["counts"][key]
                text = (f" {key:>3}    real formulas" if mp.ENTRY[key]["kind"] == "formulas"
                        else f" {key:>3}  {ty['title']}")
                val = str(n) if n else "·"
                attr_v = st["count"] if n else st["dim"]
                attr_t = st["special"] if ty.get("special") else 0
            else:
                text, val = f" {key}", str(app.value(i))
                attr_v, attr_t = st["count"], 0
            room = LEFT_W - 3
            val = val if len(val) <= room - 12 else val[:room - 13] + "…"
            space = room - len(val) - 1                # always a gap before the value
            text = text if len(text) <= space else text[:space - 1] + "…"
            row = text.ljust(space + 1) + val + " "
            if i == app.row:
                self.put(y, 1, row, curses.A_REVERSE | (curses.A_BOLD if app.focus == "left" else 0))
            else:
                self.put(y, 1, text, attr_t)
                self.put(y, 1 + space + 1, val, attr_v)
        # under the list, if there's room: what the current row is for
        free = body - min(len(lines), body) - 1
        if free >= 3:
            kind, key = ROWS[app.row]
            if kind == "count":
                ty = mp.TYPE[mp.L.type_of(key)]
                hint = f"Look for: {ty['look']}  The move: {ty['move']}"
            else:
                hint = SETTING_HINTS[key]
            hint = re.sub(r"\$([^$]*)\$", lambda m: pretty(m.group(1)), hint)
            for y, line in enumerate(textwrap.wrap(hint, LEFT_W - 3)[:free], len(lines) + 2):
                self.put(y, 1, line, st["dim"])

    def status(self, app, h, w, where):
        st = self.st
        mode = {"normal": "NORMAL", "insert": "INSERT", "command": "COMMAND",
                "search": "SEARCH", "help": "HELP"}[app.mode]
        self.put(h - 2, 0, " " * (w - 1), curses.A_REVERSE)
        self.put(h - 2, 0, f" {mode} ", st[app.mode if app.mode in st else "normal"])
        info = (f" {app.total()} problem{'s' * (app.total() != 1)} × {app.s['versions']} "
                f"version{'s' * (app.s['versions'] != 1)}  ·  seed {app.s['seed']}"
                f"{'  ·  [+]' if app.dirty() else ''}")
        self.put(h - 2, len(mode) + 2, info, curses.A_REVERSE)
        right = (f"{app.count}{app.pending.replace(chr(23), '^W')}  "
                 f"{'preview ' + where if app.focus == 'preview' else app.focus.replace('left', 'types')} ")
        self.put(h - 2, w - len(right) - 1, right, curses.A_REVERSE)
        if app.mode == "help":
            self.help(h, w)
        self.cmdline(app, h, w)

    def help(self, h, w):
        lines = HELP.splitlines()
        bw = min(w - 2, max(map(len, lines)) + 4)
        bh = min(h - 2, len(lines) + 2)
        y0, x0 = max(0, (h - bh) // 2), max(0, (w - bw) // 2)
        for y in range(bh):
            self.put(y0 + y, x0, " " * bw, curses.A_REVERSE)
        for y, line in enumerate(lines[:bh - 2], 1):
            self.put(y0 + y, x0 + 2, line, curses.A_REVERSE, bw - 4)

    def cmdline(self, app, h, w):
        st = self.st
        if app.mode in ("command", "search", "insert"):
            if app.mode == "insert":
                kind, key = ROWS[app.row]
                prompt = f"{'Type ' + key if kind == 'count' else key}: "
            else:
                prompt = ":" if app.mode == "command" else "/"
            text = prompt + app.buf
            self.put(h - 1, 0, text[-(w - 1):])
            cursor(1)
            try:
                self.scr.move(h - 1, min(len(text), w - 1))
            except curses.error:
                pass
        else:
            cursor(0)
            self.put(h - 1, 0, app.msg, st["err"] if app.err else 0)

def writes(app, ch):
    """Will this key run :w (which compiles, and takes a moment)?"""
    return ((app.mode == "command" and ch in ("\n", "\r") and re.match(r"\s*(w|write|wq|x|xit)!?\s*$", app.buf))
            or (app.mode == "normal" and app.pending == "Z" and ch == "Z"))

def run(scr, app):
    screen = Screen(scr)
    scr.timeout(250)
    while not app.quit:
        h, _ = scr.getmaxyx()
        screen.draw(app)
        scr.refresh()
        try:
            ch = scr.get_wch()
        except curses.error:                 # timeout: idle, so draw the preview
            if app.stale() and app.mode == "normal":
                app.refresh_preview()
            continue
        except KeyboardInterrupt:
            ch = "\x03"
        if ch == curses.KEY_RESIZE:
            continue
        if writes(app, ch):                  # show "writing…" before the wait
            saved = app.mode, app.msg, app.err
            app.mode, app.msg, app.err = "normal", "writing…", False
            screen.draw(app)
            scr.refresh()
            app.mode, app.msg, app.err = saved
        app.key(ch, page=max(2, h - 3))

def parse_args(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="a .sheet.json written by make_practice.py to reopen")
    ap.add_argument("--mix", nargs="+", default=[], metavar="TYPE:COUNT")
    ap.add_argument("--versions", type=int, default=mp.DEFAULTS["versions"])
    ap.add_argument("--seed", type=int)
    ap.add_argument("--style", choices=("mixed", "letters", "formulas"), default="mixed",
                    help=argparse.SUPPRESS)           # old files: formulas means the 3f entries
    ap.add_argument("--shuffle", action="store_true")
    ap.add_argument("--groups", nargs="+", default=[], metavar="GROUP")
    ap.add_argument("--title", default=mp.DEFAULTS["title"])
    ap.add_argument("--out", default=mp.DEFAULTS["out"])
    ap.add_argument("--name", default=mp.DEFAULTS["name"])
    ap.add_argument("--class", dest="class_name", default=mp.DEFAULTS["class_name"], metavar="NAME")
    return ap.parse_args(argv)

def main():
    a = parse_args(sys.argv[1:])
    try:
        mix = mp.apply_style(mp.parse_mix(a.mix), a.style)
        groups = mp.parse_groups(a.groups)
    except ValueError as e:
        sys.exit(str(e))
    app = App(mix, a.seed, versions=a.versions, shuffle=a.shuffle, groups=groups,
              title=a.title, out=a.out, name=a.name, **{"class": a.class_name})
    if a.file:
        app.load(a.file)
        app.undo.clear()
    os.environ.setdefault("ESCDELAY", "25")      # Esc should feel instant
    curses.wrapper(run, app)
    if app.last_build:
        print(f"last written: {app.last_build['out']}  (seed {app.s['seed']})")
        print(f"reproduce with: {app.last_build['sheet']['command']}")

if __name__ == "__main__":
    main()
