"""The finder (f, ^P, :find): type a few letters, see every bank and type that
fits, best first; go to one, or add from it without leaving the box.

A query is words, in any order, and each must fit. A word fits a row's text
(the bank's title and name, the type's label and title) if the text has it in
it; or, for a word of three letters or more, is the starts of some of the
text's words run together ("sysel" fits "Systems of equations with
elimination": sys + el), or has its letters in order and close together
("fctr" fits "Factor"); or, last, if the type's hints (look for, the move)
have it. Rows that fit better come first; of
equals, the banks the course shows.
"""
import curses, functools, re
from sheets import edit as E, banks, library

FIND_MAX = 300                          # rows kept for a query (the box shows a screenful)

def span(word, text):
    """The length of the shortest stretch of text that has word's letters in order, or None."""
    best = None
    start = text.find(word[0])
    while start >= 0:
        j = start
        for ch in word[1:]:
            j = text.find(ch, j + 1)
            if j < 0:
                break
        else:
            if best is None or j - start + 1 < best:
                best = j - start + 1
            start = text.find(word[0], start + 1)
            continue
        break                           # no later start can fit either
    return best

@functools.lru_cache(maxsize=None)
def words_of(text):
    return tuple(re.findall(r"[a-z0-9]+", text))

def starts(word, words, i=0):
    """Is word the starts of some of these words, run together in order? "sysel" is,
    of (systems, of, equations, with, elimination): sys + el."""
    if not word:
        return True
    for k in range(i, len(words)):
        w = words[k]
        if w[0] == word[0]:
            n = 1
            while n < len(word) and n < len(w) and w[n] == word[n]:
                n += 1
            if any(starts(word[m:], words, k + 1) for m in range(n, 0, -1)):
                return True
    return False

def fit(words, text, more=""):
    """How well a row fits the query's words (higher is better), or None if a word doesn't fit."""
    total = 0
    for w in words:
        i = text.find(w)
        if i >= 0:
            total += 130 if i == 0 or not text[i - 1].isalnum() else 100     # at the start of a word, or inside one
            continue
        if len(w) >= 3 and starts(w, words_of(text)):
            total += 90
            continue
        n = span(w, text) if len(w) >= 3 else None
        if n is not None and n <= 3 * len(w):
            total += 60 - (n - len(w))
        elif w in more:
            total += 20
        else:
            return None
    return total - len(text) / 1000     # of equals, the shorter (a bank before its types)

def find_items(lib):
    """Every row the finder can show, in the library's order: [(rid, shown, text, more)].
    Built once for each library."""
    try:
        return lib._find_items
    except AttributeError:
        pass
    out = []
    for name in sorted(lib.sequences, key=lambda n: lib.sequences[n].TITLE.lower()):
        q = lib.sequences[name]
        out.append((("seq", name), f"≡ {q.TITLE}", f"{q.TITLE} {name}".lower(), ""))
    for name in lib.names():
        b = lib.get(name)
        out.append((("bank", name), b.TITLE, f"{b.TITLE} {name}".lower(), ""))
        for e in b.ENTRIES:
            label = banks.label(b, e["key"])
            title = e["title"] + (" (real formulas)" if e.get("kind") == "formulas" else "")
            try:
                hint = b.hint(b.type_of(e["key"]))
            except Exception:           # a bank's bug mustn't keep the finder from opening
                hint = None
            more = f"{hint[2]} {hint[3]}".lower() if hint else ""
            out.append((("count", (name, e["key"])), f"{b.TITLE} › {label}  {title}",
                        f"{b.TITLE} {label} {title} {name}".lower(), more))
    lib._find_items = out
    return out

class Find:
    # -- the finder ----------------------------------------------------------
    def find_open(self, q=""):
        self.mode, self.find = "find", dict(q=q, i=0, key=None, rows=[])

    def find_rows(self):
        """The rows that fit the query, best first: [(rid, shown, in the course?)]."""
        f, lib = self.find, library.current()
        key = (f["q"], lib, self.course)
        if f["key"] != key:
            shown = {n for _, ns in lib.view(self.course, sequences=True) for n in ns} if self.course else None
            inside = lambda rid: shown is None or (rid[1] if rid[0] != "count" else rid[1][0]) in shown
            words = f["q"].lower().split()
            got = []
            for k, (rid, text, hay, more) in enumerate(find_items(lib)):
                s = fit(words, hay, more) if words else 0
                if s is not None:
                    got.append((-s, not inside(rid), k, rid, text))
            got.sort()
            f.update(key=key, rows=[(rid, text, not out) for _, out, _, rid, text in got[:FIND_MAX]])
            f["i"] = min(f["i"], max(0, len(f["rows"]) - 1))
        return f["rows"]

    def find_count(self, rid):
        """How many of a row's problems are on the sheet."""
        kind, key = rid
        if kind == "count":
            return E.count(self.sheet, *key)
        if kind == "bank":
            return sum(it["bank"] == key for sec in self.sheet["sections"] for it in sec["items"])
        return 0

    def key_find(self, ch, page=10):
        c = chr(ch) if 0 <= ch < 0x110000 else ""
        f = self.find
        rows = self.find_rows()
        self.msg, self.err = "", False
        if c in ("\x1b", "\x03"):
            self.mode = "normal"
        elif c in ("\n", "\r") or ch == curses.KEY_ENTER:
            self.find_go()
        elif c == "\x0e" or ch == curses.KEY_DOWN:                        # ^N
            f["i"] = min(f["i"] + 1, max(0, len(rows) - 1))
        elif c == "\x10" or ch == curses.KEY_UP:                        # ^P
            f["i"] = max(0, f["i"] - 1)
        elif ch in (curses.KEY_NPAGE, curses.KEY_PPAGE) or c in ("\x04", "\x15"):   # ^D ^U
            d = page if ch == curses.KEY_NPAGE or c == "\x04" else -page
            f["i"] = max(0, min(f["i"] + d, len(rows) - 1))
        elif c in ("\x01", "\t") or ch == curses.KEY_RIGHT:             # ^A, as on the banks pane
            self.find_bump(1)
        elif c == "\x18" or ch == curses.KEY_LEFT:                      # ^X
            self.find_bump(-1)
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if not f["q"]:
                self.mode = "normal"
            f["q"], f["i"] = f["q"][:-1], 0
        elif c == "\x17":                                               # ^W: the last word
            f["q"], f["i"] = re.sub(r"\S*\s*$", "", f["q"].rstrip()), 0
        elif c and c.isprintable():
            f["q"], f["i"] = f["q"] + c, 0

    def find_at(self):
        rows = self.find_rows()
        return rows[self.find["i"]] if rows else None

    def find_go(self):
        """Enter: to the row in the banks pane (opening its bank), and out of the box."""
        at = self.find_at()
        if not at:
            return self.say("nothing fits: Backspace, or Esc", True)
        rid, text, inside = at
        if not inside:
            return self.say(f"not in {self.course}: Tab adds one from here, or :course all shows it", True)
        parent = self.parent(rid)
        if parent:
            self.open.add(parent[1])
        self.mode = "normal"
        self.end_visual()
        self.focus, self.row = "left", self.rows().index(rid)
        self.say(text)

    def find_bump(self, n):
        """Tab / ^A adds one of the row's problems (a bank: one of any type); ^X takes the last away."""
        at = self.find_at()
        if not at:
            return
        (kind, key), text, _ = at
        if kind == "seq":
            return self.say("a sequence: Enter goes to it (then o opens its steps)", True)
        if kind == "count":
            ok = self.change(lambda: E.set_count(self.sheet, *key, E.count(self.sheet, *key) + 1, self.seeds())) if n > 0 \
                else self.change(lambda: E.remove_last(self.sheet, *key, 1))
        else:
            ok = self.change(lambda: E.add_from_bank(self.sheet, key, 1, self.seeds())) if n > 0 \
                else self.change(lambda: E.remove_last_from_bank(self.sheet, key, 1))
        if ok:
            self.say(f"{'added one' if n > 0 else 'removed one'}: {text}  ·  {self.total()} on the sheet")
