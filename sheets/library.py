"""The library: every problem bank, and the courses they belong to.

Banks come from three places, all read when the app starts and again on
:rescan (it takes milliseconds):

    sheets/banks/*      generator banks (Python modules), found automatically
    banks/              the built-in fixed banks and the starter courses.json
    the library folder  your own fixed banks (any *.json, in any subfolder)
                        and your courses.json. It is set in
                        ~/.config/mathsheet/config.json ("library"), and is
                        ~/Documents/mathsheet-library by default.

A library bank with the same name as a built-in one replaces it.

courses.json lists the courses in order, each with its units in order:

    {"format": 1, "courses": [{"title": "Algebra 1", "units": ["Equations", ...]}, ...]}

The library's courses.json adds courses to the built-in list, or replaces
the one with the same title.

A bank's courses (COURSES in a generator, "courses" in a bank file) map each
course to a unit, or to null for none; a plain list means no units:

    {"Algebra 1": "Equations", "Algebra 2": null}    or    ["Algebra 1", "Algebra 2"]

A type may carry its own "courses", which replace the bank's for that type;
in a course, a bank shows only the types in it. Courses only decide what the
banks pane shows: a sheet keeps its problems whatever the tags say. A tag
that names a course or unit courses.json lacks is reported, not fatal.
"""
import difflib, importlib, json, os, pkgutil, re
from pathlib import Path
from . import ROOT

FORMAT = 1
BUILTIN = ROOT / "banks"
COURSES_FILE = "courses.json"
DEFAULT_LIBRARY = "~/Documents/mathsheet-library"

# ------------------------------------------------------------------
# The config file
# ------------------------------------------------------------------
def config_path():
    return Path(os.environ.get("XDG_CONFIG_HOME") or "~/.config").expanduser() / "mathsheet" / "config.json"

def config():
    """The saved settings (library, course), or {} if there are none yet."""
    try:
        d = json.loads(config_path().read_text())
    except (OSError, ValueError):
        return {}
    return d if isinstance(d, dict) else {}

def save_config(**changes):
    """Merge changes into the config file. Raises OSError."""
    p = config_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(dict(config(), **changes), indent=1) + "\n")

def library_dir():
    return Path(config().get("library") or DEFAULT_LIBRARY).expanduser()

# ------------------------------------------------------------------
# Tags
# ------------------------------------------------------------------
def tags(value):
    """A courses tag as {course: unit or None}. Raises ValueError if malformed."""
    if value is None:
        return {}
    if isinstance(value, list) and all(isinstance(c, str) for c in value):
        return dict.fromkeys(value)
    if isinstance(value, dict) and all(isinstance(c, str) and (u is None or isinstance(u, str))
                                       for c, u in value.items()):
        return dict(value)
    raise ValueError('"courses" must be a list of course titles, or map each course to a unit (or null)')

def _tags(value):
    try:
        return tags(value)
    except ValueError:
        return {}

def type_table(b):
    """A bank's types by key, as declared (where a type's own "courses" live)."""
    for attr in ("types", "TYPE"):                  # a bank file's, or a generator's
        t = getattr(b, attr, None)
        if isinstance(t, dict):
            return t
    return {}

def types(b):
    """A bank's types, in order."""
    out = []
    for e in b.ENTRIES:
        if e["type"] not in out:
            out.append(e["type"])
    return out

def bank_tags(b, typ=None):
    """{course: unit} for a bank, or for one of its types (its own tag, else the bank's)."""
    if typ is not None:
        own = type_table(b).get(typ, {}).get("courses")
        if own is not None:
            return _tags(own)
    return _tags(getattr(b, "COURSES", None))

def suggest(name, choices):
    """The choice a mistyped name most likely means, or None. Case and Roman
    numerals don't count (Algebra I is Algebra 1)."""
    roman = {"i": "1", "ii": "2", "iii": "3", "iv": "4"}
    def key(x):
        return " ".join(roman.get(w, w) for w in x.lower().split())
    same = [c for c in choices if key(c) == key(name)]
    if same:
        return same[0]
    near = difflib.get_close_matches(key(name), [key(c) for c in choices], 1)
    return next((c for c in choices if key(c) == near[0]), None) if near else None

# ------------------------------------------------------------------
# The library
# ------------------------------------------------------------------
class Library:
    def __init__(self, folder=None):
        self.folder = Path(folder).expanduser() if folder else library_dir()
        self.warnings = []
        self.generators, self.fixed, self.courses = {}, {}, []
        self._find_generators()
        self._read_courses(BUILTIN / COURSES_FILE, "banks/")
        if self._own_folder():
            self._read_courses(self.folder / COURSES_FILE, "")
        self._read_banks()
        self._check_tags()

    def _own_folder(self):
        """Is there a library folder, apart from the built-in one?"""
        return self.folder.is_dir() and self.folder.resolve() != BUILTIN.resolve()

    def warn(self, msg):
        self.warnings.append(msg)

    def _find_generators(self):
        from . import banks as pkg
        for m in pkgutil.iter_modules(pkg.__path__):
            if m.name == "fixed":
                continue
            try:
                mod = importlib.import_module(f"{pkg.__name__}.{m.name}")
            except Exception as e:                      # a broken generator mustn't stop the app
                self.warn(f"sheets/banks/{m.name}: {type(e).__name__}: {e}")
                continue
            if hasattr(mod, "NAME") and hasattr(mod, "generate"):
                self.generators[mod.NAME] = mod

    def _read_courses(self, path, where):
        if not path.is_file():
            return
        try:
            d = json.loads(path.read_text())
            if not isinstance(d, dict) or d.get("format") != FORMAT:
                raise ValueError(f'not a courses file (it needs "format": {FORMAT})')
            new = []
            for i, c in enumerate(d.get("courses", []), 1):
                if not isinstance(c, dict) or not isinstance(c.get("title"), str) or not c["title"].strip():
                    raise ValueError(f'course {i} needs a "title"')
                units = c.get("units", [])
                if not isinstance(units, list) or not all(isinstance(u, str) for u in units):
                    raise ValueError(f'{c["title"]}: "units" must be a list of names')
                new.append(dict(title=c["title"].strip(), units=units))
        except (OSError, ValueError) as e:
            return self.warn(f"{where}{COURSES_FILE}: {e}")
        for c in new:
            old = self.course(c["title"])
            if old:
                old["units"] = c["units"]
            else:
                self.courses.append(c)

    def _bank_files(self):
        """(path, label, built-in?) for every bank file, the built-in ones first."""
        out = [(f, f"banks/{f.name}", True) for f in sorted(BUILTIN.glob("*.json")) if f.name != COURSES_FILE]
        if self._own_folder():
            for f in sorted(self.folder.rglob("*.json")):
                rel = f.relative_to(self.folder)
                if f.name == COURSES_FILE or f.name.endswith(".sheet.json") or \
                        any(part.startswith(".") for part in rel.parts):
                    continue
                out.append((f, str(rel), False))
        return out

    def _read_banks(self):
        from .banks.fixed import FixedBank
        builtin = set()
        for f, label, is_builtin in self._bank_files():
            try:
                b = FixedBank(f, self.generators)
            except (ValueError, KeyError, TypeError, OSError) as e:
                self.warn(f"{label}: {e}")
                continue
            b.SOURCE = label
            if b.NAME in self.generators:
                self.warn(f"{label}: a generator is named {b.NAME!r}; rename this bank")
                continue
            if b.NAME in self.fixed and not (b.NAME in builtin and not is_builtin):
                self.warn(f"{label}: a bank named {b.NAME!r} already exists ({self.fixed[b.NAME].SOURCE})")
                continue
            builtin.discard(b.NAME)                     # a library bank replaces a built-in one
            if is_builtin:
                builtin.add(b.NAME)
            self.fixed[b.NAME] = b

    def _check_tags(self):
        titles = [c["title"] for c in self.courses]
        def check(value, where):
            try:
                t = tags(value)
            except ValueError as e:
                return self.warn(f"{where}: {e}")
            for course, unit in t.items():
                c = self.course(course)
                if not c:
                    near = suggest(course, titles)
                    self.warn(f"{where}: no course {course!r} in {COURSES_FILE}"
                              + (f" (did you mean {near!r}?)" if near else ""))
                elif unit is not None and unit not in c["units"]:
                    near = suggest(unit, c["units"])
                    self.warn(f"{where}: {c['title']} has no unit {unit!r}"
                              + (f" (did you mean {near!r}?)" if near else ""))
        for name in self.names():
            b = self.get(name)
            where = getattr(b, "SOURCE", f"the {name} generator")
            check(getattr(b, "COURSES", None), where)
            for typ, t in type_table(b).items():
                if isinstance(t, dict) and t.get("courses") is not None:
                    check(t["courses"], f"{where}, type {typ}")

    # -- looking things up ------------------------------------------------
    def names(self):
        """Every bank: the generators, then the fixed banks by name."""
        return list(self.generators) + sorted(self.fixed)

    def get(self, name):
        b = self.generators.get(name) or self.fixed.get(name)
        if b is None:
            raise KeyError(f"no bank named {name!r}")
        return b

    def course(self, title):
        """A course by title (ignoring case), or None."""
        return next((c for c in self.courses if c["title"].lower() == (title or "").lower()), None)

    def types_in(self, name, course=None):
        """A bank's types in a course (every type, for no course)."""
        b = self.get(name)
        if course is None:
            return types(b)
        course = course.lower()
        return [t for t in types(b) if course in (c.lower() for c in bank_tags(b, t))]

    def unit_of(self, name, course):
        """The unit a bank is filed under in a course: the bank's own, else its
        first type's there; None for none."""
        b, course = self.get(name), course.lower()
        for t in [None] + self.types_in(name, course):
            for c, u in bank_tags(b, t).items():
                if c.lower() == course and u:
                    return u
        return None

    def view(self, course=None):
        """The banks to show: [(unit or None, [bank names])], in the course's unit
        order, banks without a unit last; every bank under None for no course."""
        if course is None:
            return [(None, self.names())]
        c = self.course(course)
        units = c["units"] if c else []
        groups = {u: [] for u in units + [None]}
        for name in self.names():
            if self.types_in(name, course):
                u = self.unit_of(name, course)
                groups[u if u in groups else None].append(name)
        return [(u, ns) for u, ns in groups.items() if ns]

    def summary(self):
        n = len(self.warnings)
        return (f"{len(self.names())} banks, {len(self.courses)} courses"
                + (f", {n} warning{'s' * (n != 1)}" if n else ""))

_current = None

def current():
    """The library, read the first time it's needed."""
    global _current
    if _current is None:
        _current = Library()
    return _current

def rescan(folder=None):
    """Read the library again (from folder, or the configured one)."""
    global _current
    _current = Library(folder)
    return _current
