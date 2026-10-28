"""The Lesson 1-2: Modeling bank: every entry draws and checks, a wrong key
fails, editing writes the key again, and (when the teacher's bank file is
there) every one of its 100 problems is one a story draws, word for word,
with the bank's own answer. Run from the project folder:
    python3 tests/test_modeling_1_2.py
"""
import json, os, random, sys, tempfile
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="config_")
from sheets import library as L
from sheets.banks import modeling_1_2 as B

SOURCE = Path("~/Documents/alg1/unit_1/lesson_1-2/lesson_1-2_modeling_bank.json").expanduser()

# ---- tagged, and every entry belongs to a level
lib = L.Library(Path(tempfile.mkdtemp()) / "missing")
assert "modeling_1_2" in dict(lib.view("Algebra 1"))["Lessons"] and lib.warnings == []
assert {e["type"] for e in B.ENTRIES} == set(B.KEYS) == {"1", "2", "3", "4", "5"}
assert B.heading("3") == "Level 3: One Inference"

# ---- every entry draws; a key off by a sign or a term fails
r = random.Random(4)
for e in B.ENTRY:
    seen = set()
    for _ in range(20):
        p = B.generate(e, r, seen)
        assert B.check(p) == "checked" and B.text(p).count("$") == p["prompt"].count("\\$"), "only money keeps a $"
        a = p["answer"]
        for wrong in (a.replace("+", "-", 1) if "+" in a else a.replace("-", "+", 1),
                      a.replace("=", "= 1 +") if "=" in a else a + " + 1"):
            assert wrong == a or B.check(dict(p, answer=wrong)) == "failed", (e, a, wrong)

# ---- editing: new numbers write a new key; other words are refused; an answer is checked
p = B.generate("5e", random.Random(5), set())
q, status = B.from_edit(p["prompt"].replace("for \\$", "for \\$1", 1), p)
assert status == "checked" and q["answer"] != p["answer"] and q["source"] == "edited"
try:
    B.from_edit("Write an expression.", p); raise AssertionError("the story's words must stay")
except ValueError:
    pass
left, right = p["answer"].split(" = ")
assert B.with_answer(p, f"{right} = {left}")[1] == "checked", "the sides may be swapped"
assert B.with_answer(p, f"{left} = {right} + 1")[1] == "failed"

def allowed(st, d):
    """The story's need, where the prompt shows what it needs (a hidden draw, like a ticket's price, can't be read)."""
    try:
        return st.need is None or st.need(SimpleNamespace(**d))
    except AttributeError:
        return True

# ---- the teacher's bank: each problem is drawn by a story of its level and category, with its answer
if SOURCE.exists():
    problems = json.loads(SOURCE.read_text())["problems"]
    missing = []
    for src in problems:
        found = False
        for e in (x["key"] for x in B.ENTRIES if x["type"] == str(src["difficulty"]) and x["category"] == src["category"]):
            for i, st in enumerate(B.STORIES[e]):
                try:
                    d = B.read_back(st, src["prompt"])
                    answer, alt = B.keyed(st, d)
                except (ValueError, KeyError, AttributeError, TypeError):
                    continue
                drawable = all(callable(how) or (any(all(d[k] == v for k, v in c.items() if k in d) for c in how)
                                                 if isinstance(how, list) else name not in d or d[name] in how)
                               for name, how in st.draws.items())
                p = dict(type=e, story=f"{e}.{i}", prompt=src["prompt"], answer=answer, alt=alt)
                if (drawable and allowed(st, d) and answer == src["answer"]
                        and alt == src.get("answer_alt", []) and B.check(p) == "checked"):
                    found = True
        if not found:
            missing.append(src["id"])
    assert not missing, missing
    print(f"all {len(problems)} problems of the teacher's bank are drawn")
print("all modeling_1_2 tests passed")
