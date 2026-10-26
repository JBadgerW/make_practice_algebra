"""sheets/graphs.py: clipping a curve to the window, and the Typst it writes
(compiled with cetz when typst is on the PATH)."""
import shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets.graphs import Graph, PREAMBLE, clip, runs

# a segment inside, crossing, and outside the box
assert clip((0, 0), (1, 1), (-2, 2, -2, 2)) == ((0, 0), (1, 1), False, False)
(a, b, ca, cb) = clip((0, 0), (4, 0), (-2, 2, -2, 2))
assert b == (2, 0) and cb and not ca
assert clip((3, 3), (4, 4), (-2, 2, -2, 2)) is None
# a curve that leaves and comes back is two runs, each cut where it leaves
rs = runs([(-1, 0), (0, 5), (1, 0)], (-2, 2, -2, 2))
assert len(rs) == 2 and rs[0][2] and rs[1][1], rs

g = Graph(x=(-8, 8), y=(-8, 8))
g.line(2, -3).point(1, -1, label="A").segment((-5, 2), (-2, 4), ends=("open", "closed"))
g.smooth([(-6, 0), (-3, 4), (0, 1)], ends="closed").function(lambda x: 1 / (x - 1), color="red")
src = g.typst()
assert src.startswith("#cetz.canvas(") and src.count("circle(") == 5, src.count("circle(")   # the point, two ends each
q = Graph(x=(0, 90), y=(0, 70), step=10, xlabel="Time (minutes)")
assert 'start: ">"' not in q.typst().split("\n")[4], "a first-quadrant axis has no arrow back past 0"

if shutil.which("typst"):
    d = Path(tempfile.mkdtemp())
    (d / "g.typ").write_text(PREAMBLE + "\n".join(f"#box[{x.typst()}]" for x in (g, q)))
    r = subprocess.run(["typst", "compile", str(d / "g.typ")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
print("all graph tests passed")
