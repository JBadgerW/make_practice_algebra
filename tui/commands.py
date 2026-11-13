"""Ex commands (:w, :mix, :set, ...) and / search."""
import shlex
from sheets import draft
from sheets import sheet as sh, banks, library
from .common import SETTINGS, SHEET

class Commands:
    # -- ex commands -----------------------------------------------------
    def ex(self, line):
        line = line.strip()
        if not line:
            return
        if line.isdigit():
            if self.focus == "preview":
                return self.go_problem(int(line))
            self.row = min(len(self.rows()), max(1, int(line))) - 1
            return
        cmd, _, rest = line.partition(" ")
        rest = rest.strip()
        bang = cmd.endswith("!")
        cmd = cmd.rstrip("!")
        if cmd in ("w", "write", "wq", "x", "xit"):
            self.write_cmd(then=None if cmd in ("w", "write") else "quit", force=bang)
        elif cmd in ("q", "quit", "qa", "qall"):
            if self.dirty() and self.total() and not bang:
                self.say("E37: No write since last change (add ! to override)", True)
            else:
                self.quit = True
        elif cmd in ("new", "enew", "ene"):
            self.new_cmd(force=bang)
        elif cmd == "mix":
            self.redraft(rest.split())
        elif cmd == "draft":
            self.draft_steps(rest.split())
        elif cmd == "groups":
            try:
                self.regroup(shlex.split(rest))
            except ValueError as e:
                self.say(f"E: {e}", True)
        elif cmd == "shuffle" and self.anchor is not None:
            self.shuffle()
        elif cmd == "shuffle":
            self.change(lambda: draft.shuffle_all(self.sheet, self.rng))
            self.cur = SHEET
            self.go(1)
        elif cmd == "reroll":
            if rest in ("", "all"):
                self.reroll(everything=True)
            elif rest == "section":
                self.reroll(section=True)
            else:
                self.say("usage: :reroll [all|section]", True)
        elif cmd == "space":
            try:
                self.set_space(rest)
            except ValueError as e:
                self.say(f"E: {e}", True)
        elif cmd == "width":
            self.set_width(rest)
        elif cmd == "scope":
            self.set_scope(rest)
        elif cmd in ("j", "join"):
            self.join()
        elif cmd in ("ja", "joinall"):
            self.join(every=True)
        elif cmd in ("group", "gr"):
            self.group(rest)
        elif cmd == "course":
            if not rest:
                return self.say(f"course: {self.course or 'All banks'} (:course NAME, :course all)")
            err = self.set_course(rest)
            if err:
                self.say(f"E: {err}", True)
        elif cmd == "rescan":
            self.rescan()
        elif cmd in ("library", "lib"):
            self.set_library(rest)
        elif cmd == "warnings":
            ws = banks.errors()
            self.say("; ".join(ws) if ws else "no warnings", bool(ws))
        elif cmd == "rename":
            self.rename(rest) if rest else self.say("usage: :rename NEW TITLE (empty title: cS, then Enter)", True)
        elif cmd == "clear":
            self.clear()
        elif cmd in ("form", "versions", "title", "class", "instructions", "name", "out"):
            err = self.set_value(rest, self.rows().index(("set", cmd)))
            if err:
                self.say(f"E: {err}", True)
        elif cmd in ("set", "se"):
            self.ex_set(rest)
        elif cmd in ("e", "edit"):
            self.load(rest) if rest else self.say("usage: :e FILE.sheet.json", True)
        elif cmd == "open":
            self.open_file(rest.split())
        elif cmd in ("pre", "preview"):
            self.preview(rest.split())
        elif cmd in ("present", "pres"):
            self.present(rest.split())
        elif cmd == "decoys":
            self.redraw_decoys()
        elif cmd in ("h", "help"):
            self.mode = "help"
        else:
            self.say(f"E492: Not an editor command: {line}", True)

    def ex_set(self, rest):
        opts = rest.split()
        for i, o in enumerate(opts):            # text values keep their spaces
            if o.startswith(("title=", "class=", "instructions=")):
                opts = opts[:i] + [" ".join(opts[i:])]
                break
        for opt in opts:
            flag = opt.rstrip("!").removeprefix("no")
            if flag in ("answers", "compact", "wide"):
                val = (not getattr(self, flag)) if opt.endswith("!") else not opt.startswith("no")
                setattr(self, flag, val)
            elif "=" in opt:
                k, _, v = opt.partition("=")
                k = k.strip()
                if k not in SETTINGS:
                    return self.say(f"E518: Unknown option: {k}", True)
                err = self.set_value(v, self.rows().index(("set", k)))
                if err:
                    return self.say(f"E: {err}", True)
            else:
                return self.say(f"E518: Unknown option: {opt}", True)

    def search(self, q, step=1):
        if not q:
            return
        ql = q.lower()
        if self.focus == "preview":
            ts = self.targets()
            i = ts.index(self.cur) if self.cur in ts else 0
            for k in range(1, len(ts) + 1):
                t = ts[(i + step * k) % len(ts)]
                if ql in self.target_text(t).lower():
                    self.cur = t
                    return self.say(f"/{q}")
        else:                                   # every row of every bank, opening what it finds
            rows, here = self.rows(everything=True), self.rid()
            i = rows.index(here) if here in rows else 0
            for k in range(1, len(rows) + 1):
                rid = rows[(i + step * k) % len(rows)]
                if ql in self.row_text(rid).lower():
                    kind, key = rid
                    parent = self.parent(rid)
                    if parent:
                        self.open.add(parent[1])
                    if kind == "problem":
                        self.open_types.add((key[0], banks.get(key[0]).PROBLEM[key[1]]["type"]))
                    if kind == "example":
                        self.open_types.add(key[:2])
                    self.row = self.rows().index(rid)
                    return self.say(f"/{q}")
        self.say(f"E486: Pattern not found: {q}", True)

    def row_text(self, rid):
        """What / searches on a left-pane row."""
        kind, key = rid
        if kind == "course":
            return f"course {self.value(0)}"
        if kind == "seq":
            return f"{key} {library.current().sequence(key).TITLE}"
        if kind == "step":
            st = self.step(key)
            return f"{st['n']} {st['title']} {st['note']} {st['spec']}"
        if kind == "example":
            b = banks.get(key[2])
            return f"{key[2]}#{key[3]} {b.text(b.problem(key[3]))}"
        if kind == "bank":
            return f"{key} {banks.get(key).TITLE}"
        if kind == "count":
            b, e = banks.get(key[0]), banks.get(key[0]).ENTRY[key[1]]
            hint = b.hint(b.type_of(key[1]))
            return f"{banks.label(b, key[1])} {e['title']} {hint[0] if hint else ''}"
        if kind == "problem":
            b = banks.get(key[0])
            return f"{key[1]} {b.text(b.problem(key[1]))}"
        return key

    def target_text(self, t):
        si, ii = t
        if si < 0:
            return f"{self.sheet['title']} {self.sheet['instructions']}"
        sec = self.sheet["sections"][si]
        if ii < 0:
            return f"{sec['title']} {sec['instructions']}"
        it = sec["items"][ii]
        b, p = banks.get(it["bank"]), sh.problem(it, self.version)
        return f"{b.text(p)} {b.answer_text(p)} {p['prompt']} {it['entry']}"
