"""The library: finding banks, reading courses.json, and tags.
Run from the project folder:  python3 tests/test_library.py"""
import json, os, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="config_")
from sheets import library as L, banks

def bank(path, name, courses=None, types=(("1", None),), **extra):
    path.parent.mkdir(parents=True, exist_ok=True)
    d = dict(format=1, name=name, title=name.title(),
             types=[dict(key=k, title=f"Type {k}", **({"courses": c} if c is not None else {})) for k, c in types],
             problems=[dict(id=f"{k}a", type=k, prompt=f"$x = {k}$", answer=f"${k}$") for k, _ in types], **extra)
    if courses is not None:
        d["courses"] = courses
    path.write_text(json.dumps(d))

# ---- no config, no library folder: the built-in banks and courses
lib = L.Library(Path(tempfile.mkdtemp()) / "missing")
assert lib.names() == ["literal", "systems", "lesson_1-4"] and lib.warnings == [], lib.warnings
assert [c["title"] for c in lib.courses] == ["Prealgebra", "Algebra 1", "Geometry", "Algebra 2", "Precalculus", "Calculus"]
assert lib.view("Algebra 1") == [("Equations", ["literal", "lesson_1-4"])]
assert lib.view("algebra 2") == [(None, ["systems"])] and lib.view("Precalculus") == [(None, ["systems"])]
assert lib.view("Geometry") == [] and lib.view() == [(None, lib.names())]
assert lib.types_in("literal", "Algebra 1") == L.types(lib.get("literal")) and lib.types_in("literal", "Calculus") == []
assert L.library_dir() == Path("~/Documents/mathsheet-library").expanduser(), "the default library"

# ---- the config file
L.save_config(library="~/somewhere")
assert L.config()["library"] == "~/somewhere" and L.library_dir() == Path("~/somewhere").expanduser()
L.save_config(course="Algebra 2"); assert L.config() == dict(library="~/somewhere", course="Algebra 2"), "merged"
L.config_path().write_text("not json"); assert L.config() == {}, "a broken config is ignored"

# ---- a library folder: courses, banks in subfolders, tags, type overrides
root = Path(tempfile.mkdtemp(prefix="lib_"))
(root / "courses.json").write_text(json.dumps({"format": 1, "courses": [
    {"title": "Algebra 1", "units": ["Foundations", "Equations", "Factoring"]},
    {"title": "Statistics", "units": ["Data"]}]}))
bank(root / "alg" / "factoring.json", "factoring", {"Algebra 1": "Factoring", "Algebra 2": None},
     types=[("1", None), ("2", None), ("9", ["Precalculus"])])
bank(root / "alg" / "warmups.json", "warmups", ["Algebra 1"])
bank(root / "found.json", "found", {"Algebra 1": "Foundations"})
bank(root / "stats.json", "stats", {"Statistics": "Data"})
bank(root / "lesson.json", "lesson_1-4", {"Algebra 2": None})                # replaces the built-in one
bank(root / "typos.json", "typos", {"Algebra I": None, "Algebra 1": "Equatoins"})
bank(root / "fam.json", "fam", family="nope")
bank(root / ".hidden" / "x.json", "hidden", ["Algebra 1"])
(root / "mysheet.sheet.json").write_text("{}")                                 # sheets saved here are skipped
(root / "other.json").write_text("[1, 2]")
lib = L.Library(root)
assert lib.names() == ["literal", "systems", "factoring", "found", "lesson_1-4", "stats", "typos", "warmups"], lib.names()
assert lib.get("lesson_1-4").SOURCE == "lesson.json" and "hidden" not in lib.names()
assert [c["title"] for c in lib.courses][-1] == "Statistics", "a new course goes at the end"
assert lib.course("algebra 1")["units"] == ["Foundations", "Equations", "Factoring"], "the library's units replace the built-in"
w = "\n".join(lib.warnings)
assert "no course 'Algebra I'" in w and "did you mean 'Algebra 1'" in w, w
assert "has no unit 'Equatoins'" in w and "did you mean 'Equations'" in w, w
assert "fam.json" in w and "no generator bank 'nope'" in w, w
assert "other.json" in w and "sheet.json" not in w and len(lib.warnings) == 4, lib.warnings
assert lib.view("Algebra 1") == [("Foundations", ["found"]), ("Equations", ["literal"]),
                                 ("Factoring", ["factoring"]), (None, ["typos", "warmups"])], \
    "a unit courses.json lacks files the bank under Other"
assert lib.types_in("factoring", "Algebra 1") == ["1", "2"], "type 9 has its own courses"
assert lib.types_in("factoring", "Precalculus") == ["9"] and lib.view("Precalculus") == [(None, ["systems", "factoring"])]
assert lib.view("Algebra 2") == [(None, ["systems", "factoring", "lesson_1-4"])]
assert lib.summary() == "8 banks, 7 courses, 4 warnings", lib.summary()

# ---- a bank that names a generator, or a name used twice
bank(root / "more" / "found.json", "found")
bank(root / "lit.json", "literal")
lib = L.Library(root)
w = "\n".join(lib.warnings)
assert "more/found.json: a bank named 'found' already exists (found.json)" in w, w
assert "lit.json: a generator is named 'literal'" in w, w

# ---- the library the app uses, through banks
L.save_config(library=str(root))
L.rescan(); assert "factoring" in banks.names() and banks.get("factoring").TITLE == "Factoring"
assert any("Algebra I" in e for e in banks.errors())
L.rescan(Path(tempfile.mkdtemp())); assert "factoring" not in banks.names()
try:
    banks.get("factoring"); raise AssertionError("a bank that's gone")
except KeyError:
    pass
L.save_config(library=str(root / "alg"))
assert L.rescan().folder == root / "alg" and "warmups" in banks.names() and "found" not in banks.names()
print("all library tests passed")
