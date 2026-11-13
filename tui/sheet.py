"""The sheet pane: the cursor, selecting, and every change made on the sheet."""
import copy, re
from sheets import draft
from sheets import sheet as sh, edit as E, banks
from .common import SHEET

class SheetEdits:
    def clear(self):
        self.change(lambda: self.sheet.__setitem__("sections", []))
        self.say("sheet cleared (u to undo)")

    # -- the sheet cursor -------------------------------------------------
    def targets(self):
        """Every place the sheet cursor can stop, in reading order."""
        out = [SHEET]
        for si, sec in enumerate(self.sheet["sections"]):
            out.append((si, -1))
            if not self.folded:
                out += [(si, ii) for ii in range(len(sec["items"]))]
        return out

    def clamp(self):
        secs = self.sheet["sections"]
        si, ii = self.cur
        if si >= len(secs):
            si, ii = len(secs) - 1, (len(secs[-1]["items"]) - 1 if secs else -1)
        if si >= 0:
            ii = min(ii, len(secs[si]["items"]) - 1)
            if self.folded:
                ii = -1
        self.cur = (si, ii) if si >= 0 else SHEET
        if self.cur == SHEET and not self.folded and sh.items(self.sheet) and self.focus == "left":
            self.cur = next(t for t in self.targets() if t[1] >= 0)        # start on the first problem

    def item(self, pos=None):
        si, ii = pos or self.cur
        return self.sheet["sections"][si]["items"][ii] if si >= 0 and ii >= 0 else None

    def go(self, n):
        ts = self.targets()
        i = ts.index(self.cur) if self.cur in ts else 0
        self.cur = ts[min(max(0, i + n), len(ts) - 1)]

    def go_problem(self, n):
        """The sheet cursor to problem n (1-based, print order)."""
        ps = E.positions(self.sheet)
        if ps:
            self.folded = False
            self.cur = ps[min(max(1, n), len(ps)) - 1]

    def column(self, d):
        """h/l: the other problem in the same row, if there is one."""
        it = self.item()
        if not it:
            return
        si, ii = self.cur
        for row in sh.rows(self.sheet["sections"][si]["items"]):
            if any(x is it for x in row) and len(row) == 2:
                j = 0 if row[0] is it else 1
                if 0 <= j + d < 2:
                    self.go(d)
                return

    def section_jump(self, d):
        heads = [t for t in self.targets() if t[1] == -1 and t != SHEET]
        if not heads:
            return
        si = self.cur[0]
        if d > 0:
            nxt = [t for t in heads if t[0] > si]
            self.cur = nxt[0] if nxt else heads[-1]
        else:
            prv = [t for t in heads if t[0] < si or (t[0] == si and self.cur[1] >= 0)]
            self.cur = prv[-1] if prv else SHEET

    # -- selecting (v) ---------------------------------------------------
    def span(self):
        """The stops from the anchor to the cursor, in reading order."""
        ts = self.targets()
        a, b = sorted((ts.index(self.anchor), ts.index(self.cur)))
        return ts[a:b + 1]

    def selection(self):
        """The problems selected, in reading order: those between the anchor and the
        cursor, and every problem of a section whose title ends the selection."""
        span = self.span()
        si, ii = span[-1]
        ps = {t for t in span if t[1] >= 0}
        if ii < 0:
            ps |= set(E.positions(self.sheet, None if si < 0 else si))
        return sorted(ps)

    def selected(self):
        """What the sheet pane highlights: the selection and the titles inside it."""
        if self.anchor is None:
            return set()
        return set(self.span()) | set(self.selection())

    def start_visual(self):
        if self.folded:
            return self.say("v selects problems: zR to unfold first", True)
        self.anchor = self.cur
        self.say("-- VISUAL --  + - W r :space :width change them; gs shuffles; d y cut or copy; :group TITLE; Esc ends")

    def end_visual(self):
        if self.anchor is not None:
            self.last_sel = (self.anchor, self.cur)
        self.anchor = None

    def reselect(self):
        """gv: the last selection again."""
        ts = self.targets()
        if not self.last_sel or self.folded or not all(t in ts for t in self.last_sel):
            return self.say("no selection to bring back", True)
        self.anchor, self.cur = self.last_sel

    def cut_selection(self, keep=False):
        """d / y on a selection: cut or copy every problem in it (across sections)."""
        ps = self.selection()
        self.end_visual()
        self.cur = min(ps + [self.cur]) if ps else self.cur
        if not ps:
            return self.say("no problems selected", True)
        secs = self.sheet["sections"]
        self.reg = dict(kind="items", what=copy.deepcopy([self.item(p) for p in ps]), cut=not keep)
        if not keep:
            def go():
                for si, ii in reversed(ps):
                    del secs[si]["items"][ii]
            self.change(go)
        what = f"{len(ps)} problem{'s' * (len(ps) > 1)}"
        self.say(f"{what} copied: p pastes new ones like them" if keep else f"{what} cut: p pastes them")

    def group(self, title):
        """:group TITLE: the selection (or what the cursor is on) into a new section."""
        ps = self.scope()
        self.end_visual()
        def go():
            self.cur = (E.group(self.sheet, ps, title), -1)
        if self.change(go):
            self.say(f"{len(ps)} problem{'s' * (len(ps) > 1)} grouped" + (f" under {title}" if title else ""))

    # -- changes on the sheet ---------------------------------------------
    def scope(self):
        """The items a change applies to: the selection, the problem under the
        cursor, every problem of a section on its header, or every problem on the
        sheet header."""
        if self.anchor is not None:
            return self.selection()
        si, ii = self.cur
        if ii >= 0:
            return [self.cur]
        return E.positions(self.sheet, None if si < 0 else si)

    def reroll(self, n=1, section=False, everything=False):
        si, ii = self.cur
        if everything:
            ps = E.positions(self.sheet)
        elif self.anchor is not None and not section:
            ps = self.selection()
        elif section or ii < 0:
            ps = E.positions(self.sheet, None if si < 0 else si)
        else:
            ps = E.positions(self.sheet)
            k = ps.index(self.cur)
            ps = ps[k:k + n]
        if not ps:
            return self.say("nothing to reroll here", True)
        if self.change(lambda: E.reroll(self.sheet, ps, self.seeds())):
            self.say(f"{len(ps)} rerolled" if len(ps) > 1 else "rerolled")
        self.last_change = lambda: self.reroll(n, section, everything)

    def shuffle(self):
        """gs: the selection, or the section the cursor is in (each section on the
        sheet header), in a new order in the same places."""
        if self.anchor is not None:
            groups = [self.selection()]
        else:
            si = self.cur[0]
            groups = [E.positions(self.sheet, i) for i in (range(len(self.sheet["sections"])) if si < 0 else [si])]
        n = sum(len(g) for g in groups)
        if n < 2:
            return self.say("nothing to shuffle here", True)
        anchor, cur = self.anchor, self.cur
        if self.change(lambda: [E.shuffle(self.sheet, g, self.rng) for g in groups]):
            self.anchor, self.cur = anchor, cur        # the same places, so gs again reshuffles them
            self.say(f"{n} problems shuffled")
        self.last_change = self.shuffle

    def toggle_width(self):
        ps = self.scope()
        if not ps:
            return
        to = "full" if self.item(ps[0])["width"] == "half" else "half"
        self.change(lambda: [E.set_width(self.item(p), to) for p in ps])
        self.say(f"{'all ' + str(len(ps)) + ' ' if len(ps) > 1 else ''}{to} width")
        self.last_change = self.toggle_width

    def space(self, steps):
        ps = self.scope()
        if ps:
            self.change(lambda: [E.bump_space(self.item(p), steps) for p in ps])
            self.say(f"work space {self.item(ps[0])['space']}" + (f" (and {len(ps) - 1} more)" if len(ps) > 1 else ""))
        self.last_change = lambda: self.space(steps)

    def set_space(self, text):
        x = E.inches(text)
        ps = self.scope()
        self.change(lambda: [self.item(p).__setitem__("space", E.length(x)) for p in ps])

    def set_scope(self, text):
        """:scope bank|type: rerolls of the selected problems (or the one under the
        cursor, or a section's) draw from their whole bank, or from their type only."""
        if text not in ("bank", "type"):
            return self.say("usage: :scope bank|type", True)
        ps = self.scope()
        if not ps:
            return self.say("no problems here", True)
        self.change(lambda: [E.set_scope(self.item(p), text) for p in ps])
        n = len(ps)
        self.say(f"{'all ' + str(n) + ' ' if n > 1 else ''}reroll{'s' * (n == 1)} from "
                 + ("the whole bank" if text == "bank" else "the type only"))

    def set_width(self, text):
        w = text.strip().lower()
        if w not in sh.WIDTHS:
            return self.say("usage: :width half|full", True)
        ps = self.scope()
        self.change(lambda: [E.set_width(self.item(p), w) for p in ps])

    def move(self, n):
        si, ii = self.cur
        if si < 0:
            return
        def go():
            if ii >= 0:
                self.cur = E.move_item(self.sheet, self.cur, n)
            else:
                self.cur = (E.move_section(self.sheet, si, n), -1)
        self.change(go)
        self.last_change = lambda: self.move(n)

    def cut(self, n=1, keep=False):
        """dd / yy: cut (or copy) n problems, or the section on its header."""
        si, ii = self.cur
        if si < 0:
            return self.say("dd and yy work on a problem or a section header", True)
        secs = self.sheet["sections"]
        if ii < 0:
            self.reg = dict(kind="section", what=copy.deepcopy(secs[si]), cut=not keep)
            if not keep:
                self.change(lambda: secs.pop(si))
            return self.say("section " + ("copied: p pastes it with new problems" if keep else "cut: p pastes it"))
        its = secs[si]["items"][ii:ii + n]
        self.reg = dict(kind="items", what=copy.deepcopy(its), cut=not keep)
        if not keep:
            self.change(lambda: secs[si]["items"].__delitem__(slice(ii, ii + n)))
        what = f"{len(its)} problem{'s' * (len(its) > 1)}"
        self.say(f"{what} copied: p pastes new ones like {'them' if len(its) > 1 else 'it'}" if keep
                 else f"{what} cut: p pastes {'them' if len(its) > 1 else 'it'}")

    def paste(self, below=True, n=1):
        """p / P. A cut pastes exactly what was cut (once); a copy pastes newly drawn problems."""
        if not self.reg:
            return self.say("nothing to paste: dd or yy first", True)
        reg = self.reg
        si, ii = self.cur
        secs = self.sheet["sections"]
        def fresh(it):
            return E.fresh_copy(self.sheet, it, next(self.seeds())) if it["seed"] is not None and not it["edited"] \
                else copy.deepcopy(it)
        def go():
            for _ in range(n):
                if reg["kind"] == "section":
                    sec = copy.deepcopy(reg["what"])
                    if not reg["cut"]:
                        sec["auto"] = ""
                        sec["items"] = []
                    at = 0 if si < 0 else si + (1 if below else 0)
                    secs.insert(at, sec)
                    if not reg["cut"]:
                        for it in reg["what"]["items"]:
                            sec["items"].append(fresh(it))
                    self.cur = (at, -1)
                else:
                    if not secs:
                        secs.append(sh.new_section())
                    tsi = max(si, 0)
                    at = (ii + 1 if below else ii) if ii >= 0 else 0
                    for k, it in enumerate(reg["what"]):
                        secs[tsi]["items"].insert(at + k, copy.deepcopy(it) if reg["cut"] else fresh(it))
                    self.cur = (tsi, at)
                sh.fill_versions(self.sheet)
                reg["cut"] = False                     # pasting again makes new ones, never duplicates
        self.change(go)
        self.last_change = lambda: self.paste(below, n)

    def new_section(self, below=True):
        si = self.cur[0]
        at = 0 if si < 0 else si + (1 if below else 0)
        def go():
            self.sheet["sections"].insert(at, sh.new_section())
            self.cur = (at, -1)
        self.change(go)
        self.start_edit(("title", at), "")

    def join(self, every=False):
        """:join / :j: the section below into the cursor's; :ja, every one below."""
        si = self.cur[0]
        if si < 0:
            return self.say("move to a section first", True)
        n = len(self.sheet["sections"]) - si - 1 if every else 1
        if self.change(lambda: E.join(self.sheet, si, every)):
            self.say(f"{n} section{'s' * (n != 1)} joined (u to undo)")

    def rename(self, text, si=None):
        si = self.cur[0] if si is None else si
        text = text.strip()
        if si < 0:
            if not text:
                return self.say("the title can't be empty", True)
            return self.change(lambda: self.sheet.__setitem__("title", text))
        self.change(lambda: self.sheet["sections"][si].__setitem__("title", text))

    def set_instructions(self, text, si=None):
        si = self.cur[0] if si is None else si
        target = self.sheet if si < 0 else self.sheet["sections"][si]
        self.change(lambda: target.__setitem__("instructions", text.strip()))

    def edit_problem(self, text, pos):
        status = None
        def go():
            nonlocal status
            status = E.edit_problem(self.sheet, pos, text)
        if self.change(go):
            self.say({"checked": "edited; the answer was solved again and checks",
                      "failed": "edited, but the answer FAILS its check: A edits the answer",
                      "unchecked": "edited; the answer can't be checked"}[status], status == "failed")

    def edit_answer(self, text, pos):
        status = None
        def go():
            nonlocal status
            status = E.edit_answer(self.sheet, pos, text)
        if self.change(go):
            self.say({"checked": "answer checks", "failed": "that answer FAILS its check",
                      "unchecked": "answer kept; it can't be checked"}[status], status == "failed")

    def draft_steps(self, tokens):
        """:draft SEQ STEPS [xN] [review STEPS|none] [pinned]: a new sheet from a sequence."""
        try:
            plan = draft.parse_draft(tokens)
        except ValueError as e:
            return self.say(f"E: {e}", True)
        def go():
            new = draft.draft_sequence(plan, self.sheet["versions"], self.rng.randrange(2**31))
            self.sheet["sections"] = new["sections"]
            defaults = [banks.get(n) for n in banks.names()]
            if self.sheet["instructions"] in ["", *[b.INSTRUCTIONS for b in defaults]]:   # empty, or a bank's default
                self.sheet["instructions"] = new["instructions"]
            if self.sheet["title"] in [draft.DEFAULTS["title"]] + [f"{b.TITLE} Practice" for b in defaults] \
                    or re.search(r": Steps? [\d–,]+$", self.sheet["title"]):           # still a drafted title
                self.sheet["title"] = new["title"]
        if self.change(go):
            self.cur = SHEET
            self.clamp()
            r = plan["review"]
            self.say(f"drafted {self.total()} problems: step{'s' * (len(plan['new']) > 1)} {draft.steps_text(plan['new'])}"
                     + (f", review of {draft.steps_text(r)}" if r else ", no review") + " (u to undo)")

    def regroup(self, tokens):
        try:
            groups = draft.parse_groups(tokens)
        except ValueError as e:
            return self.say(f"E: {e}", True)
        self.change(lambda: draft.regroup(self.sheet, groups, self.rng))
        self.cur = SHEET
        self.go(1)

    def redraft(self, tokens):
        try:
            mix = draft.parse_mix(tokens)
        except ValueError as e:
            return self.say(f"E: {e}", True)
        def go():
            new = draft.draft(mix, self.sheet["versions"], self.rng.randrange(2**31))
            self.sheet["sections"] = new["sections"]
            defaults = [banks.get(n) for n in banks.names()]
            if self.sheet["instructions"] in ["", *[b.INSTRUCTIONS for b in defaults]]:   # empty, or a bank's default
                self.sheet["instructions"] = new["instructions"]
            if self.sheet["title"] in [draft.DEFAULTS["title"]] + [f"{b.TITLE} Practice" for b in defaults]:
                self.sheet["title"] = new["title"]
        if self.change(go):
            self.cur = SHEET
            self.clamp()
            self.say(f"new sheet: {self.total()} problems (u to undo)")
