"""Drawing with curses, and run: the loop."""
import curses, re, textwrap, threading
from sheets import sheet as sh, banks, library
from sheets.typmath import pretty
from .common import COURSE_HINT, HELP, INFO_KEYS_W, INFO_LABEL, info_lines, prose, SETTING_HINTS, SETTINGS, SHEET_MIN

# Drawing
# ------------------------------------------------------------------

def cursor(visible):
    try:                                # some terminals can't hide the cursor
        curses.curs_set(visible)
    except curses.error:
        pass

def left_width(app, w):
    """How wide the banks pane is in a terminal `w` columns wide (0: hidden)."""
    full = max(40, min(55, w - 50))
    if app.focus != "preview":
        return full
    if app.wide:
        return 0
    return 30 if w - full - 3 < SHEET_MIN else full    # a narrow terminal: give the sheet room

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
                                         (curses.COLOR_BLACK, curses.COLOR_YELLOW),
                                         (curses.COLOR_BLACK, curses.COLOR_MAGENTA),
                                         (curses.COLOR_BLACK, curses.COLOR_CYAN)], 1):
                curses.init_pair(i, fg, b)
            P = curses.color_pair
        italic = getattr(curses, "A_ITALIC", curses.A_DIM)
        self.st = dict(plain=0, head=P(1) | curses.A_BOLD, ans=P(2), special=P(3) | curses.A_BOLD,
                       dim=curses.A_DIM, count=P(4) | curses.A_BOLD, err=P(2) | curses.A_BOLD,
                       title=curses.A_BOLD, ital=italic, page=P(3) | curses.A_DIM,
                       normal=P(5) | curses.A_BOLD, insert=P(6) | curses.A_BOLD,
                       command=P(7) | curses.A_BOLD, search=P(7) | curses.A_BOLD,
                       visual=P(8) | curses.A_BOLD,
                       sel=P(9) if curses.has_colors() else curses.A_UNDERLINE)   # the cursor is reversed

    def put(self, y, x, text, attr=0, width=None):
        h, w = self.scr.getmaxyx()
        if y < 0 or y >= h or x >= w or x < 0:
            return
        width = min(width if width is not None else w - x, w - x)
        if width <= 0:
            return
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
        on_sheet = app.focus == "preview"
        LEFT_W = left_width(app, w)
        tab = lambda on: st["normal"] if on else st["dim"]      # the focused pane's label stands out
        if LEFT_W:
            self.put(0, 1, f" BANKS · {app.course or 'all'} ", tab(not on_sheet), LEFT_W - 2)
        self.put(0, LEFT_W + 1, " SHEET · " + app.sheet["title"] + " ", tab(on_sheet), w - LEFT_W - 14)
        self.put(0, w - 12, "? for help", st["dim"])
        if LEFT_W:
            self.types_view(app, body, LEFT_W)
            for y in range(1, body + 1):
                self.put(y, LEFT_W, "│", st["dim"])

        px = LEFT_W + 2 if LEFT_W else 1
        pw = w - px - 1
        lines, (first, last) = app.render(pw)
        if first is not None:                         # keep the sheet cursor in view
            if first < app.pv_top:
                app.pv_top = max(0, first - 2)
            elif last >= app.pv_top + body:
                app.pv_top = min(first - 2, last - body + 1)
        app.pv_top = max(0, min(app.pv_top, len(lines) - body))
        sel = app.selected()
        for y, segs in enumerate(lines[app.pv_top:app.pv_top + body], 1):
            for x, text, style, tgt in segs:
                attr = st[style]
                if tgt is not None and tgt == app.cur:
                    attr |= curses.A_REVERSE if on_sheet else curses.A_UNDERLINE
                elif tgt in sel:
                    attr = st["sel"]
                self.put(y, px + x, text, attr, pw - x)
        where = ""
        if len(lines) > body:
            where = "Top" if app.pv_top == 0 else "Bot" if app.pv_top >= len(lines) - body else \
                f"{100 * app.pv_top // (len(lines) - body)}%"
        self.status(app, h, w, where)

    def types_view(self, app, body, LEFT_W):
        st = self.st
        rows = app.rows()
        nset = len(SETTINGS)
        view = library.current().view(app.course, sequences=True)
        units = app.course is not None and any(u for u, _ in view)
        lines, i = [(None, 0), ("", None)], 1                    # the course row, then the banks by unit
        for unit, names in view:
            if units:
                lines.append((unit or "Other", None))
            for _ in names:
                lines.append((None, i))
                i += 1
                while i < len(rows) - nset and rows[i][0] not in ("bank", "seq"):
                    lines.append((None, i))
                    i += 1
        if not view:
            lines.append(("(no banks in this course yet)", None))
        lines += [("", None), ("SETTINGS", None)] + [(None, i) for i in range(len(rows) - nset, len(rows))]
        app.row = min(app.row, len(rows) - 1)
        cur = next(j for j, (_, i) in enumerate(lines) if i == app.row)
        top = max(0, min(cur - body // 2, len(lines) - body))
        room = LEFT_W - 3
        for y, (hdr, i) in enumerate(lines[top:top + body], 1):
            if hdr is not None:
                self.put(y, 1, hdr, st["dim"] | curses.A_BOLD)
                continue
            kind, key = rows[i]
            attr_t = 0
            if kind == "course":
                text, val, attr_v, attr_t = "COURSE", app.value(rows[i]), st["count"], curses.A_BOLD
            elif kind == "seq":
                text = f"{'▾' if key in app.open else '▸'} ≡ {library.current().sequence(key).TITLE}"
                n = app.value(rows[i])
                val, attr_v, attr_t = (str(n) if n else "·"), (st["count"] if n else st["dim"]), curses.A_BOLD
            elif kind == "step":
                stp = app.step(key)
                arrow = ("▾" if key in app.open_types else "▸") if app.examples(stp) else " "
                text = f"  {arrow}{stp['n']:>3}  {stp['title']}" + (" (missing)" if stp["missing"] else "")
                n = app.value(rows[i])
                val, attr_v = (str(n) if n else "·"), (st["count"] if n else st["dim"])
                attr_t = st["err"] if stp["missing"] else 0
            elif kind == "example":
                b = banks.get(key[2])
                on = app.value(rows[i])
                text = f"       {key[3]:>3}. {b.text(b.problem(key[3]))}"
                val, attr_v = ("●" if on else "·"), (st["count"] if on else st["dim"])
            elif kind == "bank":
                b = banks.get(key)
                size = f" ({len(b.PROBLEMS)})" if b.FIXED else ""
                text = f"{'▾' if key in app.open else '▸'} {b.TITLE}{size}"
                n = app.value(rows[i])
                val, attr_v, attr_t = (str(n) if n else "·"), (st["count"] if n else st["dim"]), curses.A_BOLD
            elif kind == "count":
                b, e = banks.get(key[0]), banks.get(key[0]).ENTRY[key[1]]
                if b.FIXED:
                    arrow = "▾" if key in app.open_types else "▸"
                    text = f"  {arrow}{banks.label(b, key[1]):>3}  {e['title']} ({e['count']})"
                elif e.get("kind") == "formulas":
                    text = f"   {banks.label(b, key[1]):>3}    real formulas"
                else:
                    text = f"   {banks.label(b, key[1]):>3}  {e['title']}"
                n = app.value(rows[i])
                val, attr_v = (str(n) if n else "·"), (st["count"] if n else st["dim"])
                attr_t = st["special"] if b.special(b.type_of(key[1])) else 0
            elif kind == "problem":
                b = banks.get(key[0])
                on = app.value(rows[i])
                text = f"       {key[1]:>3}. {b.text(b.problem(key[1]))}"
                val, attr_v = ("●" if on else "·"), (st["count"] if on else st["dim"])
            else:
                text, val = f" {key}", str(app.value(rows[i])) or "(none)"
                attr_v = st["count"]
            val = val if len(val) <= room - 14 else val[:room - 15] + "…"
            space = room - len(val) - 1                # always a gap before the value
            text = text if len(text) <= space else text[:space - 1] + "…"
            row = text.ljust(space + 1) + val + " "
            if i == app.row:
                self.put(y, 1, row, curses.A_REVERSE | (curses.A_BOLD if app.focus == "left" else 0))
            else:
                self.put(y, 1, text, attr_t)
                self.put(y, 1 + space + 1, val, attr_v)
        free = body - min(len(lines), body) - 1
        if free >= 3:
            self.hint(app, rows[app.row], len(lines) + 2, free, LEFT_W)

    def hint(self, app, rid, y0, free, LEFT_W):
        """Under the tree, if there's room: what the row under the cursor is."""
        kind, key = rid
        if kind == "course":
            hint = COURSE_HINT
        elif kind == "seq":
            q = library.current().sequence(key)
            hint = (f"{q.TITLE}: a sequence of {len(q.steps)} steps, each changing one thing. o opens it; "
                    f"l on a step adds a problem of it; o on a step lists its pinned examples.")
        elif kind == "step":
            stp = app.step(key)
            if stp["missing"]:
                hint = f"Step {stp['n']} ({stp['spec']}): {stp['missing']}. Fix the sequence file, then :rescan."
            else:
                k = len(app.examples(stp))
                hint = (f"Step {stp['n']}: {stp['title']}." + (f" What changes: {stp['note'].rstrip('.')}." if stp["note"] else "")
                        + f" ({stp['spec']}) l adds one, h removes one"
                        + (f"; o lists its {k} pinned example{'s' * (k > 1)}." if k else "."))
        elif kind == "example":
            b = banks.get(key[2])
            hint = f"Answer: {b.answer_text(b.problem(key[3]))}.  l adds this example, h removes it, L puts it at the sheet cursor."
        elif kind == "bank":
            b = banks.get(key)
            hint = (f"{b.TITLE}: written problems. l here adds one from any type (20l: twenty), in a section of "
                    f"its own; o opens it; l on a type adds one of it; l on a problem adds that one."
                    if b.FIXED else
                    f"{b.TITLE}: draws new problems. l here adds one of any type (20l: twenty), in a section of "
                    f"its own; o opens it; l on a type adds one of it.")
        elif kind == "count":
            b = banks.get(key[0])
            h = b.hint(b.type_of(key[1]))
            hint = f"Look for: {prose(h[2])}  The move: {prose(h[3])}" if h else b.ENTRY[key[1]]["title"]
        elif kind == "problem":
            b = banks.get(key[0])
            p = b.problem(key[1])
            hint = f"Answer: {b.answer_text(p)}.  l adds it, h removes it, L puts it at the sheet cursor."
        else:
            hint = SETTING_HINTS[key]
        hint = re.sub(r"\$([^$]*)\$", lambda m: pretty(m.group(1)), hint)
        for y, line in enumerate(textwrap.wrap(hint, LEFT_W - 3)[:free], y0):
            self.put(y, 1, line, self.st["dim"])

    def status(self, app, h, w, where):
        st = self.st
        look = "visual" if app.mode == "normal" and app.anchor is not None else app.mode
        mode = {"normal": "NORMAL", "insert": "INSERT", "command": "COMMAND",
                "search": "SEARCH", "help": "HELP", "info": "INFO", "visual": "VISUAL"}[look]
        self.put(h - 2, 0, " " * (w - 1), curses.A_REVERSE)
        self.put(h - 2, 0, f" {mode} ", st[look if look in st else "normal"])
        un, bad = app.statuses()
        v = app.sheet["versions"]
        info = (f" {app.total()} problem{'s' * (app.total() != 1)} × {v} version{'s' * (v != 1)}"
                + (f"  ·  {bad} failing" if bad else "") + (f"  ·  {un} unchecked" if un else "")
                + (f"  ·  {len(app.missing())} bank{'s' * (len(app.missing()) > 1)} missing (!)" if app.missing() else "")
                + ("  ·  [+]" if app.dirty() else "")
                + (f"  ·  {len(app.selection())} selected" if app.anchor is not None else ""))
        self.put(h - 2, len(mode) + 2, info, curses.A_REVERSE)
        right = (f"{app.count}{app.pending.replace(chr(23), '^W')}  "
                 + (f"{app.where()}  sheet {where}" if app.focus == "preview" else "banks") + " ")
        self.put(h - 2, w - len(right) - 1, right, curses.A_REVERSE)
        if app.comp:
            self.wildmenu(app, h, w)
        if app.mode == "help":
            self.help(h, w)
        if app.mode == "info":
            self.info_box(app, h, w)
        self.cmdline(app, h, w)

    def info_box(self, app, h, w):
        """I: what the cursor is on, each line with the keys that change it."""
        title, rows, foot = app.info()
        lines = info_lines(rows, min(w - 2, 76))
        bw = min(w - 2, 76)
        room = max(1, h - 5)                              # the status lines stay visible
        if len(lines) > room:
            lines = lines[:room - 1] + [("", "…", "")]
        bh = len(lines) + 4
        y0, x0 = max(0, (h - 2 - bh) // 2), max(0, (w - bw) // 2)
        for y in range(bh):
            self.put(y0 + y, x0, " " * bw, curses.A_REVERSE)
        self.put(y0, x0 + 2, f" {title} ", curses.A_REVERSE | curses.A_BOLD, bw - 4)
        for y, (label, text, keys) in enumerate(lines, 1):
            self.put(y0 + y, x0 + 2, label, curses.A_REVERSE | curses.A_BOLD, INFO_LABEL)
            self.put(y0 + y, x0 + 2 + INFO_LABEL, text, curses.A_REVERSE, bw - 4 - INFO_LABEL - INFO_KEYS_W)
            if keys:
                self.put(y0 + y, x0 + bw - 2 - len(keys), keys, curses.A_REVERSE | curses.A_BOLD)
        self.put(y0 + bh - 2, x0 + bw - 2 - min(len(foot), bw - 4), foot, curses.A_REVERSE, bw - 4)

    def wildmenu(self, app, h, w):
        """Over the status line while Tab cycles: the matches, the current one lit."""
        names = app.comp.get("labels") or [m.rstrip("/").rsplit("/", 1)[-1] + ("/" if m.endswith("/") else "")
                                           for m in app.comp["options"][:-1]]
        i, x = app.comp["i"], 1
        first = 0                                        # scroll so the current one shows
        while i < len(names) and sum(len(n) + 2 for n in names[first:i + 1]) > w - 6:
            first += 1
        self.put(h - 2, 0, " " * (w - 1), curses.A_REVERSE)
        if first:
            self.put(h - 2, 0, "<", curses.A_REVERSE)
        for k, n in enumerate(names[first:], first):
            if x + len(n) > w - 3:
                self.put(h - 2, w - 3, ">", curses.A_REVERSE)
                break
            self.put(h - 2, x, n, self.st["search"] if k == i else curses.A_REVERSE)
            x += len(n) + 2

    def help(self, h, w):
        lines = HELP.splitlines()
        bw = min(w - 2, max(map(len, lines)) + 4)
        bh = min(h - 2, len(lines) + 2)
        y0, x0 = max(0, (h - bh) // 2), max(0, (w - bw) // 2)
        for y in range(bh):
            self.put(y0 + y, x0, " " * bw, curses.A_REVERSE)
        for y, line in enumerate(lines[:bh - 2], 1):
            self.put(y0 + y, x0 + 2, line, curses.A_REVERSE, bw - 4)

    def busy(self, text):
        """While a long key runs: only the message line changes (the rest of the
        screen stays as it was, since the sheet is being changed)."""
        h, w = self.scr.getmaxyx()
        cursor(0)
        self.put(h - 1, 0, " " * (w - 1))
        self.put(h - 1, 0, text, self.st["dim"])
        self.scr.refresh()

    def cmdline(self, app, h, w):
        st = self.st
        if app.mode in ("command", "search", "insert"):
            prompt = app.edit_label() if app.mode == "insert" else ":" if app.mode == "command" else "/"
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

BUSY_AFTER = 0.15                      # seconds a key may take before the status line says it's working

def handle(screen, app, ch, page, typeahead):
    """app.key(ch) in a worker thread, so a long one (drawing many problems,
    writing) never freezes the screen: after BUSY_AFTER the status line counts
    the problems drawn, Esc or ^C cancels the change (nothing is changed), and
    other keys wait in typeahead until it's done. Only this thread touches
    curses, and nothing reads the sheet while the worker has it."""
    app.drawn, app.cancel = 0, False
    failed = []
    def go():
        try:
            app.key(ch, page=page)
        except Exception as e:          # a bug outside a change: say so and carry on (the sheet stands)
            app.mode, app.pending, app.count = "normal", "", ""
            app.unexpected(e, ":w saves the sheet as it stands")
        except BaseException as e:      # re-raised here, as if the key ran in this thread
            failed.append(e)
    t = threading.Thread(target=go, daemon=True)
    t.start()
    try:
        t.join(BUSY_AFTER)
    except KeyboardInterrupt:
        app.cancel = True
    if t.is_alive():
        scr, spin = screen.scr, 0
        scr.timeout(100)
        try:
            while t.is_alive():
                spin += 1
                n = app.drawn
                try:
                    screen.busy("cancelling…" if app.cancel else
                                f"working {'⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'[spin % 10]} "
                                + (f"{n} problem{'s' * (n != 1)} drawn  ·  Esc cancels" if n else ""))
                    k = scr.get_wch()
                except curses.error:    # no key within the timeout
                    k = None
                except KeyboardInterrupt:
                    k = "\x03"
                if k in ("\x1b", "\x03"):
                    app.cancel = True
                    typeahead.clear()
                elif k is not None and k != curses.KEY_RESIZE:
                    typeahead.append(k)
        finally:
            scr.timeout(-1)
        t.join()
    if failed:
        raise failed[0]

def run(scr, app):
    screen = Screen(scr)
    sh.progress = app.progress
    typeahead = []                      # keys pressed while a long one ran, in order
    while not app.quit:
        h, _ = scr.getmaxyx()
        screen.draw(app)
        scr.refresh()
        if typeahead:
            ch = typeahead.pop(0)
        else:
            try:
                ch = scr.get_wch()
            except curses.error:
                continue
            except KeyboardInterrupt:
                ch = "\x03"
        if ch == curses.KEY_RESIZE:
            continue
        handle(screen, app, ch, max(2, h - 3), typeahead)
