"""The sheet as the pane shows it, laid out like the page (with the page-break estimate)."""
import textwrap
from sheets import draft
from sheets import sheet as sh, edit as E, banks
from .common import FRAC_IN, HEADER_IN, LINE_IN, PAGE_IN, PLAIN_IN, SHEET, TITLE_IN

class Render:
    # -- the sheet, drawn ----------------------------------------------------
    def render(self, width):
        """The sheet as the page shows it, for a pane `width` columns wide.
        Returns (lines, span): each line is [(x, text, style, target)], and
        span is the (first, last) line of the cursor's target. The lines are
        built once for each sheet and view; moving the cursor only looks up its span."""
        key = ("render", self.version, max(30, width), self.answers, self.compact, self.folded)
        lines, spans = self.memo(key, lambda: self._render(width))
        return lines, spans.get(self.cur, (None, None))

    def _render(self, width):
        """(lines, {target: (first, last) line}) for render."""
        sheet, v, width = self.sheet, self.version, max(30, width)
        lines, spans = [], {}
        def emit(*segs):
            segs = [sg for sg in segs if sg[1]]
            for t in {sg[3] for sg in segs if sg[3] is not None}:
                spans[t] = (spans.get(t, (len(lines),))[0], len(lines))
            lines.append(segs)
        un, bad = self.statuses()
        info = [f"Version {v + 1}/{sheet['versions']}", f"answers {'on' if self.answers else 'off'} (za)",
                f"{'compact' if self.compact else 'work space shown'} (zs)"]
        emit((0, " · ".join(info), "dim", None))
        emit()
        r1, r2 = "Name ______________", f"Date ________  Ver: {v + 1}"
        emit((0, sheet["class_name"], "plain", SHEET), (max(len(sheet["class_name"]) + 2, width - len(r1)), r1, "plain", SHEET))
        emit((0, sheet["title"], "title", SHEET), (max(len(sheet["title"]) + 2, width - len(r2)), r2, "plain", SHEET))
        for l in textwrap.wrap(sheet["instructions"], width):
            emit((0, l, "ital", SHEET))
        if not sheet["sections"]:
            emit()
            emit((0, "No problems yet. On the banks pane, o opens a bank and l adds", "dim", None))
            emit((0, "a problem; or :add BANK/TYPE:COUNT (Tab completes the names).", "dim", None))
            return lines, spans

        used, page, n = HEADER_IN + LINE_IN * len(textwrap.wrap(sheet["instructions"], 90)), 1, 0
        def page_break():
            nonlocal used, page
            page += 1
            used = 0.0
            emit((0, f"{'─' * 6} page {page} (about here) {'─' * max(0, width - 30)}", "page", None))
        def prompt_h(it):
            b, p = banks.get(it["bank"]), sh.problem(it, v)
            return b.height(p)
        def fits(h):                                  # the last gap may hang off the page
            return used + h - (FRAC_IN - PLAIN_IN) - 0.05 <= PAGE_IN

        for si, sec in enumerate(sheet["sections"]):
            H = (si, -1)
            rows = sh.rows(sec["items"])
            ins = textwrap.wrap(sec["instructions"], width) if sec["instructions"] else []
            head_h = (TITLE_IN if sec["title"] else 0) + LINE_IN * len(ins)
            first_h = (max(map(prompt_h, rows[0])) + max(E.inches(it["space"]) for it in rows[0])) if rows else 0
            if not self.folded and not fits(head_h + first_h) and used > HEADER_IN:
                page_break()
            used += head_h
            if not self.folded or si == 0:
                emit()
            bk, _, typ = sec.get("auto", "").partition(":")
            style = "special" if bk and typ and typ != "*" and banks.get(bk).special(typ) else "head"
            title = (0, sec["title"], style, H) if sec["title"] else (0, "(untitled section: no header)", "dim", H)
            extra = (len(title[1]) + 2, f"{len(sec['items'])} problem{'s' * (len(sec['items']) != 1)}", "dim", H) \
                if self.folded else (0, "", "dim", H)
            emit(title, extra)
            for l in ins:
                emit((0, l, "ital", H))
            if self.folded:
                continue
            if not rows:
                emit((2, "(empty: p pastes here, or L on the banks pane)", "dim", H))
            index = {id(it): ii for ii, it in enumerate(sec["items"])}
            for ri, row in enumerate(rows):
                row_h = max(map(prompt_h, row)) + max(E.inches(it["space"]) for it in row)
                if ri and not fits(row_h):
                    page_break()
                used += row_h
                colw = (width - 3) // 2 if row[0]["width"] == "half" else width
                cells = []
                for k, it in enumerate(row):
                    n += 1
                    x0, tgt = k * (colw + 3), (si, index[id(it)])
                    b, p = banks.get(it["bank"]), sh.problem(it, v)
                    mark = "!" if b.MISSING else {"failed": "✗", "unchecked": "?"}.get(it["status"], "")
                    num = f"{mark}{n}."
                    body = [w for part in b.text(p).split("\n")
                            for w in textwrap.wrap(part, max(8, colw - len(num) - 1)) or [""]]
                    nstyle = "err" if mark == "!" else {"failed": "err", "unchecked": "dim"}.get(it["status"], "plain")
                    cell = [[(x0, num, nstyle, tgt), (x0 + len(num) + 1, body[0], "plain", tgt)]]
                    cell += [[(x0 + len(num) + 1, l, "plain", tgt)] for l in body[1:]]
                    if self.answers:
                        a = b.answer_text(p)[:colw - 2]
                        cell.append([(x0 + max(len(num) + 1, colw - len(a)), a, "ans", tgt)])
                    cells.append(cell)
                tall = max(map(len, cells))
                for i in range(tall):
                    emit(*[sg for cell in cells if i < len(cell) for sg in cell[i]])
                if not self.compact:
                    blank = round(max(E.inches(it["space"]) for it in row) * 4) - (tall - 1)
                    for _ in range(max(0, blank)):
                        emit()
        if not self.folded:
            emit()
            emit((0, f"about {page} page{'s' * (page > 1)}" + (f" · {bad} failing" if bad else "")
                  + (f" · {un} unchecked" if un else ""), "dim", None))
        return lines, spans

    def where(self):
        """A short description of what the sheet cursor is on, for the status line."""
        si, ii = self.cur
        if si < 0:
            return "sheet header"
        it = self.item()
        if not it:
            return f"section {si + 1}"
        n = E.positions(self.sheet).index(self.cur) + 1
        src = it["entry"] if it["bank"] == draft.BANK else f"{it['bank']}:{it['entry']}"
        src += f" (rerolls from all of {it['bank']})" if sh.from_bank(it) else ""
        return f"#{n} {src} {it['width']} {it['space']}" + ("" if it["status"] == "checked" else f" {it['status']}")
