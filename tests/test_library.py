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

# ---- the built-in sequence: Lesson 1-4's order, over the generator, its fifty pinned
from sheets.banks.literal import TYPES, lesson_sequence
q = lib.sequence("literal_by_type")
assert json.loads((L.BUILTIN / "literal_by_type.json").read_text()) == lesson_sequence(), \
    "banks/literal_by_type.json is what gen_sequence.py writes from TYPES"
assert [st["entry"] for st in q.steps] == [t["key"] for t in TYPES] and all(st["bank"] == "literal" for st in q.steps)
assert [st["title"] for st in q.steps] == [t["title"] for t in TYPES]
pinned = [pid for st in q.steps for _, pid in st["examples"]]
assert pinned == [str(n) for n in range(1, 51)], "the fifty, in lesson order"
lesson = lib.get("lesson_1-4")
assert all(lesson.PROBLEM[pid]["type"] == st["type"] for st in q.steps for _, pid in st["examples"])
assert lib.view("Algebra 1", sequences=True) == [("Equations", ["literal_by_type", "literal", "lesson_1-4"])]

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
assert "banks/literal_by_type.json: 50 pinned examples are in no fixed bank: lesson_1-4#1, lesson_1-4#2, lesson_1-4#3, …" in w, \
    "the built-in sequence's examples, gone with the built-in Lesson 1-4: one warning"
assert "other.json" in w and "sheet.json" not in w and len(lib.warnings) == 5, lib.warnings
assert lib.view("Algebra 1") == [("Foundations", ["found"]), ("Equations", ["literal"]),
                                 ("Factoring", ["factoring"]), (None, ["typos", "warmups"])], \
    "a unit courses.json lacks files the bank under Other"
assert lib.types_in("factoring", "Algebra 1") == ["1", "2"], "type 9 has its own courses"
assert lib.types_in("factoring", "Precalculus") == ["9"] and lib.view("Precalculus") == [(None, ["systems", "factoring"])]
assert lib.view("Algebra 2") == [(None, ["systems", "factoring", "lesson_1-4"])]
assert lib.summary() == "8 banks, 1 sequence, 7 courses, 5 warnings", lib.summary()

# ---- a bank that names a generator, or a name used twice
bank(root / "more" / "found.json", "found")
bank(root / "lit.json", "literal")
lib = L.Library(root)
w = "\n".join(lib.warnings)
assert "more/found.json: the name 'found' is taken (found.json)" in w, w
assert "lit.json: a generator is named 'literal'" in w, w

# ---- the library the app uses, through banks
L.save_config(library=str(root))
L.rescan(); assert "factoring" in banks.names() and banks.get("factoring").TITLE == "Factoring"
assert any("Algebra I" in e for e in banks.errors())
L.rescan(Path(tempfile.mkdtemp())); assert "factoring" not in banks.names()
gone = banks.get("factoring"); assert gone.MISSING and not banks.has("factoring") and gone is banks.get("factoring")
fam = {"prompt": "y = m x + b", "target": "m", "answer": "m = (y - b)/x", "family": "literal"}
assert gone.text(fam) == banks.get("literal").text(fam), "a missing bank's problem shows through its family"
assert gone.text({"prompt": "$x^2$", "answer": "$4$"}) == "x^2" and gone.check({"prompt": "", "answer": ""}) == "unchecked"
try:
    gone.generate("1", None, set()); raise AssertionError("nothing new from a missing bank")
except RuntimeError as e:
    assert "isn't in the library" in str(e)
L.save_config(library=str(root / "alg"))
assert L.rescan().folder == root / "alg" and "warmups" in banks.names() and "found" not in banks.names()
# ---- sequences: ordered steps that point at banks' entries
from sheets.sequences import Sequence
sq = Path(tempfile.mkdtemp(prefix="seqlib_"))
(sq / "courses.json").write_text(json.dumps({"format": 1, "courses": [
    {"title": "Algebra 1", "units": ["Foundations", "Equations"]}]}))
bank(sq / "found.json", "found", {"Algebra 1": "Foundations"}, types=[("1", None), ("2", None)])
def seq(fname, steps, **extra):
    (sq / f"{fname}.json").write_text(json.dumps(dict(format=1, kind="sequence", title=fname.title(), steps=steps, **extra)))
seq("by_move", [
    {"entry": "literal/1", "note": "one operation to undo"},
    {"entry": "literal/2"},
    {"entry": "literal/3", "title": "A Fraction Bar", "note": "a fraction bar appears",
     "examples": ["lesson_1-4#13", "lesson_1-4#14"]},
    {"entry": "literal/a", "examples": ["lesson_1-4#19"]},       # spelled loosely; a Type 4 example
    {"entry": "literal/99"},
    {"entry": "nope/1", "examples": ["nope#1"]},
    {"entry": "systems/1", "examples": ["literal#1", "lesson_1-4#999"]},
    {"entry": "sytems/2"},
], courses={"Algebra 1": "Equations"})
seq("warmup", [{"entry": "found/1"}, {"entry": "found/2"}], courses=["Algebra 1"])
seq("untagged", [{"entry": "found/1"}])
(sq / "broken.json").write_text(json.dumps({"format": 1, "kind": "sequence", "steps": [{"note": "no entry"}]}))
(sq / "empty.json").write_text(json.dumps({"format": 1, "kind": "sequence", "steps": []}))
seq("same_name", [{"entry": "found/1"}], name="found")               # a bank has this name
seq("typo", [{"entry": "found/1"}], courses={"Algebra 1": "Equatoins"})
lib = L.Library(sq)
w = "\n".join(lib.warnings)
assert sorted(lib.sequences) == ["by_move", "literal_by_type", "typo", "untagged", "warmup"] and "found" in lib.names(), \
    sorted(lib.sequences)
assert "broken.json: step 1 needs an \"entry\" like \"literal/3\"" in w and "empty.json: \"steps\" must be a list" in w, w
assert "same_name.json: the name 'found' is taken (found.json)" in w, w
q = lib.sequence("by_move")
assert [st["n"] for st in q.steps] == [1, 2, 3, 4, 5, 6, 7, 8], "every step keeps its number"
assert [st["title"] for st in q.steps[:4]] == ["One Step", "Add or Subtract, Then Divide", "A Fraction Bar",
                                               "Watch the Sign"], [st["title"] for st in q.steps]
assert q.steps[3]["entry"] == "A" and q.steps[2]["type"] == "3" and q.steps[0]["note"] == "one operation to undo"
assert q.steps[2]["examples"] == [("lesson_1-4", "13"), ("lesson_1-4", "14")]
assert [st["n"] for st in q.usable()] == [1, 2, 3, 4, 7]
assert q.steps[4]["missing"] == "literal has no entry '99'" and q.steps[5]["missing"] == "no bank 'nope'"
assert "by_move.json, step 5 (literal/99): literal has no entry '99'" in w, w
assert "step 8 (sytems/2): no bank 'sytems' (did you mean 'systems'?)" in w, w
assert "step 4 (literal/a): example lesson_1-4#19 is" in w, w
assert "by_move.json: 2 pinned examples are in no fixed bank: literal#1, lesson_1-4#999" in w, w
assert "step 3" not in w, "matching examples are fine"
assert "typo.json: Algebra 1 has no unit 'Equatoins'" in w, w
assert lib.view("Algebra 1") == [("Foundations", ["found"]), ("Equations", ["literal", "lesson_1-4"])], "banks only, by default"
assert lib.view("Algebra 1", sequences=True) == [("Foundations", ["found"]), ("Equations", ["by_move", "literal_by_type", "literal", "lesson_1-4"]),
                                                 (None, ["typo", "warmup"])], lib.view("Algebra 1", sequences=True)
assert lib.view(None, sequences=True)[0][1][:5] == ["by_move", "literal_by_type", "typo", "untagged", "warmup"]
assert lib.summary().startswith("4 banks, 5 sequences, ") and "warnings" in lib.summary(), lib.summary()
try:
    lib.sequence("found"); raise AssertionError("a bank isn't a sequence")
except KeyError:
    pass
try:
    Sequence({"format": 1, "steps": [{"entry": "literal/1"}]}, "x.json"); raise AssertionError("kind is required")
except ValueError:
    pass
print("all library tests passed")
