"""The board presenter: the panels compile, two pages per problem, and the
page's queue behaves (clicks, the number strip, undo).
Run from the project folder:  python3 tests/test_present.py"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="config_")
from sheets import sheet as sh, present, writer

# A sheet with a graph (it lays out its own slide), a system, and a word problem.
s = sh.new_sheet("Presenter Test")
sec = sh.new_section()
s["sections"].append(sec)
seen = {}
for i, (bank, entry) in enumerate([("slope_intercept_2_1", "4"), ("systems", "1"), ("modeling_1_2", "1a"),
                                   ("slope_intercept_2_1", "2"), ("systems", "A")]):
    sec["items"].append(sh.new_item(bank, entry, f"present-{i}", seen))
N = len(sh.items(s))

# ---- the panels use the slides' own question and answer
t = present.panels_typst(s)
for it in sh.items(s):
    q, a = present.stacked(it, 0) or writer.slide_args(it, 0)
    fix = ", fixed: true" if writer.own_slide(it, 0) and not present.stacked(it, 0) else ""
    assert f"{q}{fix})\n#pagebreak()\n#slide(" in t and f"{a}{fix})\n" in t
assert t.count("#slide(") == 2 * N               # each problem's two pages

# ---- a graph sits under its equation: the same graph on both pages, the answer hidden on the question's
from sheets import banks
graphed = [it for it in sh.items(s) if present.stacked(it, 0)]
assert len(graphed) == 2
for it in graphed:
    (tq, gq), (ta, ga) = (banks.get(it["bank"]).slide_parts(it["problem"], key=k) for k in (False, True))
    q, a = present.stacked(it, 0)
    assert q.index(tq) < q.index(gq) and a.index(ta) < a.index(ga)    # text above the graph
    assert tq == ta or ("#hide[" in tq and "#hide[" not in ta)     # Step 2's answer is the graph alone
assert any("#hide[" in banks.get(it["bank"]).slide_parts(it["problem"])[0] for it in graphed)

# ---- the deck still gives each problem its question slide, then its answer slide
d = writer.slides(s)
for n, it in enumerate(sh.items(s), 1):
    q, a = writer.slide_args(it, 0)
    assert f"#slide({n}, {q})\n#pagebreak()\n#slide({n}, {a})\n" in d

if not shutil.which("typst"):
    print("typst not found: skipping the compile and page checks")
    sys.exit()

# ---- they compile, two SVG pages per problem
pairs = present.render(s)
assert len(pairs) == N and all(q.lstrip().startswith("<svg") and a.lstrip().startswith("<svg") for q, a in pairs)
out = Path(tempfile.mkdtemp()) / "t.present.html"
present.build(s, out)
page = out.read_text()
assert page.count("data:image/svg+xml;base64,") == 2 * N
assert "<title>Presenter Test</title>" in page

# ---- the command line writes NAME.present.html next to the sheet
tmp = Path(tempfile.mkdtemp())
sh.save(s, tmp / "lesson.sheet.json")
r = subprocess.run([sys.executable, str(Path(__file__).resolve().parent.parent / "present.py"),
                    str(tmp / "lesson.sheet.json"), "--no-open"], capture_output=True, text=True)
assert r.returncode == 0 and (tmp / "lesson.present.html").exists(), r.stderr
r = subprocess.run([sys.executable, str(Path(__file__).resolve().parent.parent / "present.py"),
                    str(tmp / "lesson.sheet.json"), "--version", "2", "--no-open"], capture_output=True, text=True)
assert r.returncode and "1 version" in r.stderr, r.stderr

# ---- the page's queue, run in node against a stand-in for the DOM
if not shutil.which("node"):
    print("node not found: skipping the queue checks")
    sys.exit()
script = re.search(r"<script>(.*)</script>", page, re.S).group(1)
probs = json.dumps([[f"q{k}", f"a{k}"] for k in range(1, N + 1)])
script = re.sub(r"^const PROBS = .*$", lambda m: f"const PROBS = {probs};", script, count=1, flags=re.M)
harness = r"""
const els = {}, keys = [];
function el(id) { return els[id] || (els[id] = {id, innerHTML: "", className: "", children: [],
  appendChild(c) { this.children.push(c); }, scrollIntoView() {}}); }
globalThis.document = {getElementById: el, createElement: () => el("b" + Object.keys(els).length),
                       addEventListener: (t, f) => keys.push(f)};
""" + script + r"""
const shown = i => { const h = el("p" + i).innerHTML;
  return h.includes("Done") ? "done" : h.match(/src="([^"]+)"/)[1]; };
const st = () => [shown(0), shown(1), next];
const log = [];
const step = (what, f) => { f(); log.push([what, ...st()]); };
log.push(["start", ...st()]);
step("click L", () => el("p0").onclick());
step("click L", () => el("p0").onclick());
step("click R", () => el("p1").onclick());
step("strip 1", () => buttons[0].onclick());
step("click R", () => el("p1").onclick());
step("undo", () => keys[0]({key: "u"}));
step("key l", () => keys[0]({key: "l"}));
step("strip N", () => buttons[N - 1].onclick());
step("click L", () => el("p0").onclick());
step("click L", () => el("p0").onclick());
step("click L", () => el("p0").onclick());
step("click L", () => el("p0").onclick());
step("strips", () => {});
log.push(["classes", ...buttons.map(b => b.className.trim())]);
console.log(JSON.stringify(log));
"""
r = subprocess.run(["node"], input=harness, capture_output=True, text=True)
assert r.returncode == 0, r.stderr
log = json.loads(r.stdout)
assert log[:12] == [
    ["start", "q1", "q2", 3],
    ["click L", "a1", "q2", 3],          # the answer
    ["click L", "q3", "q2", 4],          # then the next problem
    ["click R", "q3", "a2", 4],
    ["strip 1", "q3", "a2", 1],          # the queue moves back; nothing on screen changes
    ["click R", "q3", "q1", 2],          # problem 1 again, though it was done
    ["undo", "q3", "a2", 1],
    ["key l", "q3", "q1", 2],            # l clicks the right half
    ["strip N", "q3", "q1", N],
    ["click L", "a3", "q1", N],
    ["click L", f"q{N}", "q1", N + 1],
    ["click L", f"a{N}", "q1", N + 1],
], log
assert log[12] == ["click L", "done", "q1", N + 1], log[12]     # nothing left: Done
cls = log[14][1:]
assert cls[0] == "done on-1" and cls[1] == "done" and cls[2] == "done" and cls[N - 1] == "done", cls
print("present: ok")
