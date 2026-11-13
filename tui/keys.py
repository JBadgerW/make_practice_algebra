"""Keys: normal mode on either pane, the info box, and typing a line (insert, :, /) with Tab completion."""
import curses, re
from sheets import draft
from sheets import sheet as sh, banks
from .common import complete_course, complete_entry, complete_path, complete_sequence, openable, SHEET

# After a prefix key, the message line lists what can follow it: (on the sheet, on the banks pane).
FOLLOWS = {
    "g": ("gg top (5gg: problem 5) · gt gT version · gs shuffle · gv reselect", "gg top · gt gT version"),
    "z": ("za answers · zs compact · zM fold to sections · zR unfold", "za answers · zs compact · zM close all banks · zR open all"),
    "d": ("dd cut the problem, or the section on its header (3dd: three)", "dd remove all of this type"),
    "y": ("yy copy: p pastes new problems like it", ""),
    "c": ("cc retype · cS section title · cI section instructions", "cc retype the count or setting"),
    "Z": ("ZZ write and quit · ZQ quit without writing",) * 2,
    "]": ("]] next section",) * 2,
    "[": ("[[ previous section",) * 2,
    "\x17": ("^W w other pane · h banks · l sheet · o sheet full width / split",) * 2,
}

class Keys:
    # -- keys ------------------------------------------------------------
    def key(self, ch, page=10):
        """Handle one key (an int as from curses getch, or a 1-char str)."""
        if isinstance(ch, str):
            ch = ord(ch)
        if self.mode == "help":
            self.mode = "normal"
            return
        if self.mode in ("insert", "command", "search"):
            self.key_line(ch)
            if self.mode == "normal" and self.resume_info:
                self.mode, self.resume_info = "info", False
            return
        if self.mode == "info":
            return self.key_info(ch)
        if self.mode == "find":
            return self.key_find(ch, page)
        c = chr(ch) if 0 <= ch < 0x110000 else ""
        self.msg, self.err = "", False
        sheet = self.focus == "preview"

        if self.pending:
            p, self.pending = self.pending, ""
            n = int(self.count) if self.count else None
            self.count = ""
            combo = p + c
            if combo == "gg":
                if sheet:
                    self.go_problem(n) if n else self.go(-10**6)
                else:
                    self.row = min((n or 1) - 1, len(self.rows()) - 1)
            elif combo == "gt":
                self.version = min(n, self.sheet["versions"]) - 1 if n else (self.version + 1) % self.sheet["versions"]
            elif combo == "gs":
                self.shuffle() if sheet else self.say("gs shuffles on the sheet (Tab to it)", True)
            elif combo == "gv":
                self.reselect() if sheet else self.say("gv selects on the sheet (Tab to it)", True)
            elif combo == "gT":
                self.version = (self.version - (n or 1)) % self.sheet["versions"]
            elif combo == "dd":
                self.cut(n or 1) if sheet else self.zero()
            elif combo == "yy":
                self.cut(n or 1, keep=True) if sheet else self.say("yy copies on the sheet (Tab to it)", True)
            elif combo == "cc":
                self.start_insert(clear=True)
            elif combo == "cS":
                self.start_edit(("title", self.cur[0]))
            elif combo == "cI":
                self.start_edit(("instructions", self.cur[0]))
            elif combo == "ZZ":
                self.ex("x")
            elif combo == "ZQ":
                self.quit = True
            elif combo == "za":
                self.answers = not self.answers
            elif combo == "zs":
                self.compact = not self.compact
            elif combo in ("zM", "zR") and not sheet:
                self.fold_banks(combo == "zM")
            elif combo in ("zM", "zR"):
                self.folded = combo == "zM"
                if self.folded:
                    self.end_visual()
                if self.folded and self.cur[1] >= 0:
                    self.cur = (self.cur[0], -1)
                self.clamp()
            elif combo in ("]]", "[["):
                for _ in range(n or 1):
                    self.section_jump(1 if c == "]" else -1)
            elif p == "\x17" and c in ("w", "\x17", "h", "l"):
                self.set_focus({"h": "left", "l": "preview"}.get(c) or self.other_focus())
            elif p == "\x17" and c == "o":
                self.wide = not self.wide
                if self.wide:
                    self.set_focus("preview")
                self.say("the sheet full width (^W o splits)" if self.wide else "the sheet beside the banks")
            return

        if c.isdigit() and (c != "0" or self.count):
            self.count += c
            return
        n = int(self.count) if self.count else 1
        had_count = bool(self.count)
        self.count = ""

        if sheet and self.anchor is not None and c in ("d", "x", "y"):
            self.cut_selection(keep=(c == "y"))
        elif c == "\x1b":
            self.end_visual()
        elif c == "v":
            self.end_visual() if self.anchor is not None else \
                self.start_visual() if sheet else self.say("v selects on the sheet (Tab to it)", True)
        elif c and c in "gdcZz\x17y][":
            if c == "y" and not sheet:
                return
            self.pending = c
            if had_count:
                self.count = str(n)
            self.say(FOLLOWS[c][0 if sheet else 1])
        elif c == "j" or ch == curses.KEY_DOWN:
            self.go(n) if sheet else self.move_row(n)
        elif c == "k" or ch == curses.KEY_UP:
            self.go(-n) if sheet else self.move_row(-n)
        elif c == "G":
            if sheet:
                self.go_problem(n) if had_count else self.go(10**6)
            else:
                self.row = min(n, len(self.rows())) - 1 if had_count else len(self.rows()) - 1
        elif c in ("\x04", "\x15", "\x06", "\x02") or ch in (curses.KEY_NPAGE, curses.KEY_PPAGE):
            big = c in ("\x06", "\x02") or ch in (curses.KEY_NPAGE, curses.KEY_PPAGE)
            d = (1 if c in ("\x04", "\x06") or ch == curses.KEY_NPAGE else -1) * n * (10 if big else 5)
            self.go(d) if sheet else self.move_row(d)
        elif sheet and self.key_sheet(c, ch, n):
            pass
        elif c in ("l", "+", "\x01") or ch == curses.KEY_RIGHT:
            self.bump(n)
        elif c in ("h", "-", "\x18") or ch == curses.KEY_LEFT:
            self.bump(-n)
        elif c == "L":
            self.add_here(n)
        elif c == "o":
            self.toggle_open()
        elif c == "O":
            self.fold_banks(any(r[0] in ("bank", "seq") and r[1] in self.open for r in self.rows()))
        elif c == "x":
            self.zero()
        elif c == "D":
            self.clear()
        elif c in ("i", "a", "\n", "\r") or ch == curses.KEY_ENTER:
            self.start_insert()
        elif c == "s":
            self.start_insert(clear=True)
        elif c == "r":
            self.reroll_entry()
        elif c == "u":
            self.do_undo(n)
        elif c == "\x12":
            self.do_redo(n)
        elif c == ".":
            self.repeat(n)
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
        elif c in ("f", "\x10"):
            self.find_open()
        elif c == "I":
            if sheet or self.act()[0] in ("bank", "count", "problem", "seq"):
                self.mode = "info"
            else:
                self.say("I shows a bank, a sequence, a type, or a problem: move to one", True)
        elif c == "\t":
            self.set_focus(self.other_focus())
        elif c == "\x03":
            self.say("Type  :q!  and press Enter to quit")

    # -- the info box ------------------------------------------------------
    INFO_KEYS = set("WrRAiajk+-\x01\x18u\x12.0123456789cgz][")    # what still works with the box open
    INFO_KEYS_LEFT = set("lhLrxoiajk+-\x01\x18u\x12.0123456789c")  # ... on the banks pane

    def key_info(self, ch):
        """I's box stays open while these keys change what it shows; Esc, q, or I close it."""
        c = chr(ch) if 0 <= ch < 0x110000 else ""
        if c in ("\x1b", "q", "I", "\x03") and not self.pending:
            self.mode = "normal"
            return
        sheet = self.focus == "preview"
        if c == "b" and not self.pending and sheet:
            ps = self.scope()
            to = "type" if ps and all(sh.from_bank(self.item(q)) for q in ps) else "bank"
            return self.set_scope(to)
        keys = self.INFO_KEYS if sheet else self.INFO_KEYS_LEFT
        if not (self.pending or c in keys or ch in (curses.KEY_UP, curses.KEY_DOWN)):
            return self.say("in the box: the keys it lists, j k to move, Esc to close", True)
        self.mode = "normal"
        self.key(ch)
        if self.mode == "normal":
            self.mode = "info"
        elif self.mode == "insert":
            self.resume_info = True         # editing from the box comes back to it

    def key_sheet(self, c, ch, n):
        """Keys that mean something else on the sheet. True if handled here."""
        if c == "l" or ch == curses.KEY_RIGHT:
            self.column(1)
        elif c == "h" or ch == curses.KEY_LEFT:
            self.column(-1)
        elif c == "r":
            self.reroll(n)
        elif c == "R":
            self.reroll(section=True)
        elif c == "W":
            self.toggle_width()
        elif c in ("+", "\x01"):
            self.space(n)
        elif c in ("-", "\x18"):
            self.space(-n)
        elif c in ("i", "a", "\n", "\r") or ch == curses.KEY_ENTER:
            self.start_insert()
        elif c in ("A", "s"):
            if c == "A" and not self.item():
                self.say("A edits a problem's answer: move to a problem", True)
            else:
                self.start_insert(clear=(c == "s"), answer=(c == "A"))
        elif c == "x":
            self.cut(n)
        elif c in ("p", "P"):
            self.paste(c == "p", n)
        elif c == "J":
            self.move(n)
        elif c == "K":
            self.move(-n)
        elif c in ("o", "O"):
            self.new_section(c == "o")
        elif c in ("L", "D"):
            self.say(f"{c} works on the banks pane (Tab back to it)", True)
        else:
            return False
        return True

    def other_focus(self):
        return "left" if self.focus == "preview" else "preview"

    def set_focus(self, f):
        if f != "preview":
            self.end_visual()
        self.focus = f
        if f == "preview" and self.cur == SHEET and sh.items(self.sheet) and not self.folded:
            self.cur = next(t for t in self.targets() if t[1] >= 0)

    def move_row(self, n):
        self.row = min(len(self.rows()) - 1, max(0, self.row + n))

    # -- typing a value ------------------------------------------------
    def start_edit(self, what, buf=None):
        """Type a new value for what: ("row", r), ("title", si), ("instructions", si),
        ("problem", pos), ("answer", pos). buf starts as the current text."""
        kind, ref = what
        if buf is None:
            if kind == "row":
                v = self.value(ref)
                buf = "" if isinstance(v, bool) else str(v)
            elif kind in ("title", "instructions"):
                obj = self.sheet if ref < 0 else self.sheet["sections"][ref]
                buf = obj[kind]
            else:
                it = self.item(ref)
                b = banks.get(it["bank"])
                buf = b.edit_text(it["problem"]) if kind == "problem" else b.answer_edit_text(it["problem"])
        self.mode, self.editing, self.buf = "insert", what, buf

    def start_insert(self, clear=False, answer=False):
        if self.focus != "preview":
            return self.start_edit(("row", self.row), "" if clear else None)
        si, ii = self.cur
        if ii >= 0:
            return self.start_edit(("answer" if answer else "problem", self.cur), "" if clear else None)
        self.start_edit(("title", si), "" if clear else None)

    def finish_edit(self, buf):
        kind, ref = self.editing
        self.editing = None
        if kind == "row":
            err = self.set_value(buf, ref)
            if err:
                self.say(f"E: {err}", True)
        elif kind == "title":
            self.rename(buf, ref)
        elif kind == "instructions":
            self.set_instructions(buf, ref)
        elif kind == "problem":
            self.edit_problem(buf, ref)
        elif kind == "answer":
            self.edit_answer(buf, ref)
        elif kind == "write":
            buf = buf.strip()
            if buf != self.s["name"]:
                err = self.set_value(buf, self.rows().index(("set", "name")))
                if err:
                    return self.say(f"E: {err}; nothing written", True)
            self.write_cmd(then=ref, force=True)
        elif kind == "new":
            a = buf.strip().lower()
            if a in ("w", "write", "s", "save", "y", "yes"):
                self.write_cmd(then="new")
            elif a in ("d", "discard", "n", "no"):
                self.new_sheet()
            else:
                self.say("kept this sheet: nothing changed")

    def edit_label(self):
        kind, ref = self.editing
        if kind == "row":
            k, key = self.rid(ref)
            return f"{'count of ' + key[1] if k == 'count' else 'course' if k == 'course' else key}: "
        if kind in ("title", "instructions"):
            return f"{'sheet' if ref < 0 else 'section'} {kind}: "
        if kind == "new":
            return "unsaved changes: w writes them first, d discards them (Enter; Esc cancels): "
        if kind == "write":
            return f"name is still {draft.DEFAULTS['name']} (Enter writes, or retype; Esc cancels): "
        if kind == "problem":
            it = self.item(ref)
            hint = banks.get(it["bank"]).edit_hint(it["problem"]) if it else ""
            return f"problem ({hint}): " if hint else "problem: "
        return "answer: "

    def completing(self):
        """What Tab completes in the line being typed: (start, what), or None, with
        what "dirs", "files", "courses", or "sequences". The out setting, :out, and
        :library complete folders; :e the sheets it can open too; the course row and :course,
        courses; :draft, a sequence's name."""
        if self.mode == "insert" and self.editing and self.editing[0] == "row":
            return {("set", "out"): (0, "dirs"), ("course", None): (0, "courses")}.get(self.rid(self.editing[1]))
        if self.mode == "command":
            m = re.match(r"\s*(?:(out|e|edit|library|lib|course|w|write|sav|saveas)!?\s+|set\s+out=)", self.buf)
            if m:
                return m.end(), {"e": "sheets", "edit": "sheets", "course": "courses", "w": "sheets", "write": "sheets",
                                 "sav": "sheets", "saveas": "sheets"}.get(m.group(1), "dirs")
            m = re.match(r"\s*(?:add|a|mix)\s+(?:.*\s)?(?=\S*$)", self.buf)     # the entry being typed, the last word
            if m:
                return m.end(), "entries"
            m = re.match(r"\s*draft\s+(?=\S*$)", self.buf)            # the sequence's name, the first word
            if m:
                return m.end(), "sequences"
        return None

    def complete(self, step):
        """Tab / Shift-Tab: the next or previous name the path could become, as in
        Neovim: the first match at once, then each in turn, then what was typed."""
        c = self.comp
        if not (c and c["buf"] == self.buf):
            where = self.completing()
            if not where:
                return
            start, what = where
            word = self.buf[start:]
            labels = None
            if what == "entries":               # a bank's name, then its entry: the menu shows what each is
                pairs = complete_entry(word, self.course)
                matches, labels = [m for m, _ in pairs], [l for _, l in pairs]
            else:
                matches = complete_course(word) if what == "courses" else complete_sequence(word) \
                    if what == "sequences" else complete_path(word, what == "dirs", openable if what == "sheets" else None)
            if not matches:
                self.comp = None
                return
            if len(matches) == 1:               # done: the next Tab looks inside it
                self.buf, self.comp = self.buf[:start] + matches[0], None
                return
            c = self.comp = dict(start=start, options=matches + [word], i=-1 if step > 0 else len(matches),
                                 labels=labels)
        c["i"] = (c["i"] + step) % len(c["options"])
        self.buf = c["buf"] = self.buf[:c["start"]] + c["options"][c["i"]]

    def key_line(self, ch):
        c = chr(ch) if 0 <= ch < 0x110000 else ""
        if c == "\t" or ch == curses.KEY_BTAB:
            return self.complete(-1 if ch == curses.KEY_BTAB else 1)
        self.comp = None
        if c == "\x1b" or (c == "\x03"):
            self.mode, self.buf, self.editing = "normal", "", None
        elif c in ("\n", "\r") or ch == curses.KEY_ENTER:
            mode, buf = self.mode, self.buf
            self.mode, self.buf = "normal", ""
            if mode == "insert":
                self.finish_edit(buf)
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
