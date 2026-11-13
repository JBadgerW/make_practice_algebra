"""The board presenter: one web page that shows a sheet's problems two at a
time, one in each half of the screen, for two students at the board.

Each problem is drawn by Typst exactly as on its slides (writer.slide_args),
on a page half a slide wide: a question page and an answer page, compiled to
SVG and kept in the page as images, so the page needs nothing else to run.

Clicking a half shows its answer. A second click loads the next problem in
the queue, which both halves share. The thin strip of numbers on the left
moves the queue to any problem, back or forward, done before or not.
"""
import base64, html as _html, json, shutil, subprocess, tempfile
from pathlib import Path
from . import banks, graphs, writer
from .sheet import items, problem
from .typst import slhead, vars_

# Half a 16:9 slide (13.33in by 7.5in). A problem and its answer start at
# 20pt and wrap to the half's width, shrinking until they fit its height.
# A graphed problem whose bank gives its slide in parts (slide_parts) shows
# its equation centered above the graph, the graph always the same size (its
# text shrinks, never the graph). Another slide the bank lays out itself
# (fixed) keeps its own lines and is scaled down whole to fit. Either way the
# question page holds the answer hidden, so the graph never moves.
# A graph drawn bigger on a slide (Graph's slide_width) goes halfway from its
# sheet size to its slide size here: the panel is half a slide (graphs.PANEL).
PANEL = graphs.slide_at(graphs.PANEL) + """
#set page(width: 6.667in, height: 7.5in, margin: 0.4in)
#let slide(n, prob, answer: none, fixed: false) = {
  align(left)[#text(size: 22pt, weight: "bold")[Problem #n]]
  v(0.5em)
  block(width: 100%, height: 1fr, layout(room => {
    let body(s) = box(align(left, text(size: s, {
      prob
      if answer != none {
        v(0.8em)
        text(fill: red, answer)
      }
    })))
    let s = 20pt
    if fixed {
      let m = measure(body(s))
      let k = calc.min(1, 0.95 * room.width / m.width, room.height / m.height)
      align(center, scale(k * 100%, reflow: true, body(s)))
    } else {
      while s > 12pt and measure(body(s), width: room.width).height > room.height {
        s -= 1pt
      }
      align(center, body(s))
    }
  }))
}
"""

def stacked(it, v):
    """The question and answer bodies of a graphed problem whose bank gives its
    slide in parts: the text centered above the graph. None for any other."""
    b = banks.get(it["bank"])
    parts = b.slide_parts
    p = problem(it, v)
    if parts(p) is None:
        return None
    def body(text, g):
        return f"[{f'#align(center)[{text}] #v(0.6em) ' if text else ''}#align(center)[{g}]]"
    return body(*parts(p)), body(*parts(p, key=True))

def panels_typst(sheet, v=0):
    """Typst for version v's panels: problem n's question on page 2n - 1, its answer on page 2n."""
    s = slhead + vars_(sheet["title"], str(v + 1), sheet["class_name"]) + writer._preambles(sheet) + PANEL
    for n, it in enumerate(items(sheet), 1):
        q, a = stacked(it, v) or writer.slide_args(it, v)
        if writer.own_slide(it, v) and not stacked(it, v):
            q, a = q + ", fixed: true", a + ", fixed: true"
        s += ("" if n == 1 else "#pagebreak()\n") + f"#slide({n}, {q})\n#pagebreak()\n#slide({n}, {a})\n"
    return s

def render(sheet, v=0):
    """The panels as SVG text, [(question, answer)] per problem; raises RuntimeError."""
    n = len(items(sheet))
    if not n:
        raise RuntimeError("no problems: the sheet is empty")
    typst = shutil.which("typst")
    if not typst:
        raise RuntimeError("typst not found: can't draw the problems")
    with tempfile.TemporaryDirectory(prefix="mathsheet-present-") as d:
        (Path(d) / "panels.typ").write_text(panels_typst(sheet, v))
        r = subprocess.run([typst, "compile", "panels.typ", "p{0p}.svg"], cwd=d, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"typst failed on the panels:\n{r.stderr}")
        pages = [p.read_text() for p in sorted(Path(d).glob("p*.svg"))]
    if len(pages) != 2 * n:
        raise RuntimeError(f"expected {2 * n} panels, typst made {len(pages)}")
    return list(zip(pages[0::2], pages[1::2]))

def _uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

def html(sheet, v=0):
    """The presenter page for version v, self-contained."""
    probs = [[_uri(q), _uri(a)] for q, a in render(sheet, v)]
    title = sheet["title"] + (f" (Version {v + 1})" if sheet["versions"] > 1 else "")
    return (PAGE.replace("@TITLE@", _html.escape(title))
                .replace("@PROBS@", json.dumps(probs)))

def build(sheet, path, v=0):
    """Write the presenter page for version v to path; returns the path."""
    path = Path(path)
    path.write_text(html(sheet, v))
    return path

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@TITLE@</title>
<style>
  :root { --bg: #fff; --ink: #222; --dim: #bbb; --line: #ccc; --left: #2b6cb0; --right: #c05621; }
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; background: var(--bg); color: var(--ink);
               font-family: system-ui, sans-serif; overflow: hidden; user-select: none; }
  #app { display: flex; height: 100vh; }
  #strip { width: 2.6rem; flex: none; overflow-y: auto; border-right: 1px solid var(--line);
           padding: 0.3rem 0.2rem; scrollbar-width: thin; }
  #strip button { display: block; width: 100%; margin: 0 0 0.15rem; padding: 0.2rem 0;
                  font: inherit; font-size: 0.8rem; border: 2px solid transparent; border-radius: 4px;
                  background: none; color: var(--ink); cursor: pointer; }
  #strip button:hover { background: #eee; }
  #strip button.done { color: var(--dim); }
  #strip button.next { border-color: var(--ink); }
  #strip button.on-0 { background: var(--left); color: #fff; }
  #strip button.on-1 { background: var(--right); color: #fff; }
  .pane { flex: 1; min-width: 0; position: relative; cursor: pointer; display: flex;
          align-items: center; justify-content: center; }
  .pane + .pane { border-left: 2px solid var(--line); }
  .pane img { width: 100%; height: 100%; object-fit: contain; display: block; }
  .pane .done { font-size: 2rem; color: var(--dim); }
  .pane .tag { position: absolute; top: 0.4rem; right: 0.6rem; font-size: 0.75rem; color: var(--dim); }
</style>
</head>
<body>
<div id="app">
  <nav id="strip" aria-label="Problems"></nav>
  <div class="pane" id="p0"></div>
  <div class="pane" id="p1"></div>
</div>
<script>
const PROBS = @PROBS@;            // [question, answer] image per problem
const N = PROBS.length;
let next = Math.min(3, N + 1);    // the next problem a pane will load (1-based)
const panes = [{n: N >= 1 ? 1 : 0, ans: false}, {n: N >= 2 ? 2 : 0, ans: false}];
const done = new Set();           // problems whose answer has been shown
const history = [];               // states before each click, for undo

const strip = document.getElementById("strip");
const buttons = [];
for (let k = 1; k <= N; k++) {
  const b = document.createElement("button");
  b.textContent = k;
  b.title = "Problem " + k + " next";
  b.onclick = () => { save(); next = k; draw(true); };
  strip.appendChild(b);
  buttons.push(b);
}

function save() {
  history.push(JSON.stringify({next, panes, done: [...done]}));
  if (history.length > 200) history.shift();
}

function undo() {
  const s = history.pop();
  if (!s) return;
  const o = JSON.parse(s);
  next = o.next; panes[0] = o.panes[0]; panes[1] = o.panes[1];
  done.clear(); o.done.forEach(k => done.add(k));
  draw(true);
}

function click(i) {
  const p = panes[i];
  if (!p.n) return;
  save();
  if (!p.ans) { p.ans = true; done.add(p.n); }
  else if (next <= N) { p.n = next++; p.ans = false; }
  else { p.n = 0; p.ans = false; }
  draw(true);
}

function draw(scroll) {
  panes.forEach((p, i) => {
    const el = document.getElementById("p" + i);
    el.innerHTML = p.n
      ? '<img alt="Problem ' + p.n + (p.ans ? ' answer' : '') + '" src="' + PROBS[p.n - 1][p.ans ? 1 : 0] + '">'
        + '<span class="tag">' + (p.ans ? "answer" : "") + '</span>'
      : '<span class="done">Done</span>';
  });
  buttons.forEach((b, j) => {
    const k = j + 1;
    b.className = (done.has(k) ? "done " : "") + (k === next ? "next " : "")
                + (panes[0].n === k ? "on-0" : panes[1].n === k ? "on-1" : "");
  });
  if (scroll && next <= N) buttons[next - 1].scrollIntoView({block: "nearest"});
}

document.getElementById("p0").onclick = () => click(0);
document.getElementById("p1").onclick = () => click(1);
document.addEventListener("keydown", e => {
  if (e.key === "a" || e.key === "ArrowLeft") click(0);
  else if (e.key === "l" || e.key === "ArrowRight") click(1);
  else if (e.key === "u" || (e.key === "z" && (e.ctrlKey || e.metaKey))) undo();
});
draw(false);
</script>
</body>
</html>
"""
