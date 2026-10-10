"""Make practice worksheets, answer keys, and slide decks of literal equations,
drawn by type (the same Types 1-11 and Special Cases A-B as the lesson).

Each type has two entries: 3 draws made-up equations from templates, and 3f
draws real formulas of that type. Every answer is solved by sympy, written
in classroom form, and checked numerically before it is used.

A run first drafts a *sheet* (sheets/sheet.py): sections of problems, each
problem with its own seed, width, and work space. The sheet is saved as
NAME.sheet.json beside the PDFs, and the worksheet, key, and slides of every
version are printed from it.

Examples (run from this folder):
    python3 make_practice.py --mix 3:6 8:4 A:2 --versions 3 --seed 12
    python3 make_practice.py --mix all:2 --shuffle
    python3 make_practice.py --mix 1f:6 3f:4         # real formulas
    python3 make_practice.py --draft by_move 5-6 review 1-4   # a sheet from a sequence's steps
    python3 make_practice.py --sheet practice/literal_practice.sheet.json   # print a saved sheet again
    python3 make_practice.py --selftest 200        # stress-test every type
    python3 mathsheet.py                        # the same, interactively (vim keys)

--mix ENTRY:COUNT ... entries are 1-11, A, B (made-up equations), 1f-11f, Af, Bf
                      (real formulas), all (every made-up entry), allf (every
                      formulas entry). Default all:2. Another bank's entries
                      take its name: systems/4:3, systems/all:1.
--versions N          N parallel versions: every drawn problem is redrawn in its slot
--seed S              same seed -> same sheet (default: random, printed)
--shuffle             one section with every problem shuffled, no headings
--groups G ...        section order and mixed sections: 9 8 3+4=Warm-up 1
--draft SEQ STEPS [xN] [review STEPS|none] [pinned]
                      a sheet from a sequence (sheets/sequences.py): N problems
                      (default 6) of each new step in its own section, then a
                      shuffled review of about one problem per two new ones,
                      spread over the review steps (default: every earlier
                      step). pinned starts each step with its pinned examples.
--sheet FILE          print a saved .sheet.json (or an older practice .json) again
--out DIR, --name N   output folder (default ./practice) and file prefix
--no-compile          write .typ files only
"""
import argparse, json, random, re, shlex, shutil, subprocess, sys
from pathlib import Path
from sheets import sheet as sh, writer, banks, library
from sheets.typst import esc
from sheets.banks import literal as L
from sheets.banks.literal import TYPE, label, selftest

BANK = L.NAME
ENTRY = L.ENTRY
KEYS = [e["key"] for e in L.ENTRIES]                   # what --mix counts: 1, 1f, 2, 2f, ...
TYPE_KEYS = L.KEYS                                     # what --groups orders: 1, 2, ..., A, B

def has_types(mix):
    """The literal types with at least one problem in mix (whose keys are entries or types)."""
    return {L.type_of(k) for k, n in mix.items() if n and "/" not in k}

def split_key(k):
    """A mix key -> (bank, entry): "3f" is the literal bank's; "systems/4" names its bank."""
    bank, _, entry = k.rpartition("/")
    return bank or BANK, entry

# ------------------------------------------------------------------
# Groups: the headed sections of a worksheet, in the order they print.
# A group is dict(types=["3", "4"], name="").  One type is a plain section;
# several types make a mixed section.  An empty name means "use the default".
# ------------------------------------------------------------------
def default_layout(mix):
    have = has_types(mix)
    return [dict(types=[k], name="") for k in TYPE_KEYS if k in have]

def layout(groups, mix):
    """The groups actually printed: those of `groups` that still have problems,
    then every other type with problems as its own group, in sequence order."""
    out, seen, have = [], set(), has_types(mix)
    for g in groups or []:
        ts = [k for k in g["types"] if k in have and k not in seen]
        seen.update(ts)
        if ts:
            out.append(dict(types=ts, name=g.get("name", "")))
    return out + [dict(types=[k], name="") for k in TYPE_KEYS if k in have and k not in seen]

def default_heading(g):
    if len(g["types"]) == 1:
        return L.heading(g["types"][0])
    return f'Mixed Practice ({", ".join(g["types"])})'

def heading(g):
    return g.get("name") or default_heading(g)

def parse_groups(tokens):
    """["9", "3+4=Warm up", "1"] -> [dict(types=["9"], name=""), ...]; raises ValueError."""
    out, seen = [], set()
    for tok in tokens:
        spec, _, name = tok.partition("=")
        ks = []
        for k in spec.split("+"):
            e = L.entry_key(k)
            if e is None:
                raise ValueError(f"bad group {tok!r}: use types {', '.join(TYPE_KEYS)} joined by +, e.g. 3+4 or 3+4=Name")
            k = L.type_of(e)
            if k in seen:
                raise ValueError(f"type {k} is in more than one group")
            seen.add(k)
            ks.append(k)
        out.append(dict(types=ks, name=name.strip()))
    return out

def group_token(g):
    return "+".join(g["types"]) + (f"={g['name']}" if g.get("name") else "")


# ------------------------------------------------------------------
# Drafting a sheet from a recipe
# ------------------------------------------------------------------
DEFAULTS = dict(versions=1, shuffle=False, title="Literal Equations Practice",
                class_name="Algebra 1", out="practice", name="literal_practice")

def parse_mix(tokens):
    """["3:6", "3f:2", "all:1", "systems/4:2"] -> {"3": 7, "3f": 2, ..., "systems/4": 2};
    raises ValueError. BANK/ENTRY names another bank's entry; BANK/all is all of them."""
    mix = {}
    for tok in tokens:
        k, _, c = tok.partition(":")
        if "/" in k:
            bank, _, e = k.partition("/")
            if not banks.has(bank):
                raise ValueError(f"bad mix entry {tok!r}: no bank {bank!r} (banks: {', '.join(banks.names())})")
            b = banks.get(bank)
            es = [x["key"] for x in b.ENTRIES] if e.lower() == "all" else [b.entry_key(e)] if b.entry_key(e) else None
            if not c.isdigit() or not es:
                raise ValueError(f"bad mix entry {tok!r}: use {bank}/ENTRY:COUNT with ENTRY in "
                                 f"{', '.join(x['key'] for x in b.ENTRIES)}, or all")
            for e in es:
                mix[f"{bank}/{e}"] = mix.get(f"{bank}/{e}", 0) + int(c)
            continue
        keys = ([e for e in KEYS if not e.endswith("f")] if k.lower() == "all" else
                [e for e in KEYS if e.endswith("f")] if k.lower() == "allf" else
                [L.entry_key(k)] if L.entry_key(k) else None)
        if not c.isdigit() or not keys:
            raise ValueError(f"bad mix entry {tok!r}: use ENTRY:COUNT with ENTRY in "
                             f"{', '.join(KEYS)}, all, or allf")
        for key in keys:
            mix[key] = mix.get(key, 0) + int(c)
    return mix

def apply_style(mix, style):
    """Old --style: formulas moved counts to the formulas entries; mixed and letters keep made-up ones."""
    if style != "formulas":
        return mix
    out = {}
    for k, n in mix.items():
        f = k + "f" if not k.endswith("f") and k + "f" in ENTRY else k
        out[f] = out.get(f, 0) + n
    return out

def ordered(mix):
    """mix in entry order (the literal bank's, then the others as given), without zero counts."""
    return {**{k: mix[k] for k in KEYS if mix.get(k)}, **{k: n for k, n in mix.items() if "/" in k and n}}

def command_for(mix, versions, seed, shuffle=False, title=DEFAULTS["title"], out=DEFAULTS["out"],
                name=DEFAULTS["name"], class_name=DEFAULTS["class_name"], groups=None):
    """The make_practice.py command line that drafts and writes a sheet exactly."""
    mix = ordered(mix)
    c = ["python3 make_practice.py", "--mix", *[f"{k}:{n}" for k, n in mix.items()],
         "--versions", str(versions), "--seed", str(seed)]
    if shuffle:
        c.append("--shuffle")
    lay = layout(groups, mix)
    if not shuffle and lay != default_layout(mix):
        c += ["--groups", *[shlex.quote(group_token(g)) for g in lay]]
    for opt, val in (("title", title), ("out", out), ("name", name), ("class_name", class_name)):
        if val != DEFAULTS[opt]:
            c += [f"--{'class' if opt == 'class_name' else opt}", shlex.quote(val)]
    return " ".join(c)

def draft_command(plan, versions, seed, title=DEFAULTS["title"], out=DEFAULTS["out"],
                  name=DEFAULTS["name"], class_name=DEFAULTS["class_name"]):
    """The make_practice.py command line that drafts and writes a sequence's sheet exactly."""
    c = ["python3 make_practice.py", "--draft", *map(shlex.quote, draft_tokens(plan)),
         "--versions", str(versions), "--seed", str(seed)]
    for opt, val in (("title", title), ("out", out), ("name", name), ("class_name", class_name)):
        if val != DEFAULTS[opt]:
            c += [f"--{'class' if opt == 'class_name' else opt}", shlex.quote(val)]
    return " ".join(c)

def draft(mix, versions=1, seed=0, shuffle=False, groups=None, title=DEFAULTS["title"],
          class_name=DEFAULTS["class_name"]):
    """A new sheet from a recipe. Depends only on these arguments.
    Each problem gets its own seed from the run's seed; sections follow
    layout(groups, mix), and a mixed section's problems are shuffled."""
    mix = ordered(mix)
    rng = random.Random(seed)
    seen = {}                                  # (the literal bank never draws the lesson's own 50)
    drawn = [sh.new_item(*split_key(k), rng.randrange(2**31), seen) for k, n in mix.items() for _ in range(n)]
    fams = {banks.get(it["bank"]).FAMILY for it in drawn}
    first = banks.get(fams.pop()) if len(fams) == 1 else L       # one family: its instructions for the sheet
    if title == DEFAULTS["title"] and first is not L:
        title = f"{first.TITLE} Practice"
    sheet = sh.new_sheet(title, class_name, first.INSTRUCTIONS, versions)
    sheet["sections"] = [dict(sh.new_section(), items=drawn)]
    (shuffle_all(sheet, rng) if shuffle else regroup(sheet, groups, rng))
    return sh.fill_versions(sheet, seen)

# ------------------------------------------------------------------
# Drafting from a sequence
# ------------------------------------------------------------------
PER_STEP, REVIEW_RATIO = 6, 0.5          # new problems per step; review problems per new one

def parse_steps(text, q):
    """"5", "5-6", "1-3,5" -> step numbers of sequence q, in order; raises ValueError."""
    nums = []
    for part in text.split(","):
        a, _, b = part.strip().partition("-")
        if not a.isdigit() or (b and not b.isdigit()):
            raise ValueError(f"bad steps {text!r}: use 5, 5-6, or 1-3,5")
        lo, hi = sorted((int(a), int(b or a)))
        nums += range(lo, hi + 1)
    if any(not 1 <= n <= len(q.steps) for n in nums):
        raise ValueError(f"{q.NAME} has steps 1-{len(q.steps)}")
    return list(dict.fromkeys(nums))

def steps_text(nums):
    """[1, 2, 3, 5] -> "1-3,5"."""
    out, run = [], []
    for n in sorted(nums) + [None]:
        if run and n == run[-1] + 1:
            run.append(n)
            continue
        if run:
            out.append(f"{run[0]}-{run[-1]}" if len(run) > 1 else str(run[0]))
        run = [n]
    return ",".join(out)

def parse_draft(tokens):
    """["by_move", "5-6", "x8", "review", "1-4", "pinned"] -> dict(seq, new, per,
    review, pinned); raises ValueError. Without review, every earlier step that
    can draw is reviewed; review none reviews nothing."""
    usage = "use SEQUENCE STEPS [xN] [review STEPS|none] [pinned], e.g. by_move 5-6 x6 review 1-4"
    if len(tokens) < 2:
        raise ValueError(usage)
    lib = library.current()
    name = tokens[0]
    if name not in lib.sequences:
        near = library.suggest(name, list(lib.sequences))
        raise ValueError(f"no sequence {name!r}" + (f" (did you mean {near}?)" if near else
                         f"; sequences: {', '.join(sorted(lib.sequences)) or 'none'}"))
    q = lib.sequences[name]
    new = parse_steps(tokens[1], q)
    per, review, pinned, rest = PER_STEP, None, False, list(tokens[2:])
    while rest:
        t = rest.pop(0)
        if re.fullmatch(r"x\d+", t) and 1 <= int(t[1:]) <= 40:
            per = int(t[1:])
        elif t == "review" and rest:
            r = rest.pop(0)
            review = [] if r in ("none", "0") else parse_steps(r, q)
        elif t == "pinned":
            pinned = True
        else:
            raise ValueError(f"bad draft option {t!r}: {usage}")
    if review is None:
        review = [n for n in range(1, min(new)) if not q.steps[n - 1]["missing"]]
    review = [n for n in review if n not in new]
    bad = [n for n in new + review if q.steps[n - 1]["missing"]]
    if bad:
        raise ValueError(f"step {bad[0]} of {name} can't draw: {q.steps[bad[0] - 1]['missing']}")
    return dict(seq=name, new=new, per=per, review=review, pinned=pinned)

def draft_tokens(plan):
    """The tokens that parse_draft turns back into this plan."""
    return [plan["seq"], steps_text(plan["new"]), f"x{plan['per']}",
            "review", steps_text(plan["review"]) or "none"] + (["pinned"] if plan["pinned"] else [])

def spread(steps, k):
    """How many of k review problems each review step gets: as even as possible,
    any extra going to the most recent steps; with fewer problems than steps,
    evenly spaced steps ending with the most recent."""
    m = len(steps)
    if not m or k <= 0:
        return {}
    if k >= m:
        base, extra = divmod(k, m)
        return {n: base + (i >= m - extra) for i, n in enumerate(steps)}
    picks = [round(m - 1 - i * (m - 1) / (k - 1)) for i in range(k)] if k > 1 else [m - 1]
    return {steps[i]: 1 for i in sorted(set(picks))}

def draft_sequence(plan, versions=1, seed=0, title=DEFAULTS["title"], class_name=DEFAULTS["class_name"]):
    """A new sheet from a sequence: the new steps in their own sections, in order,
    then one shuffled review section. Depends only on these arguments (and the
    library's contents)."""
    q = library.current().sequence(plan["seq"])
    rng, seen = random.Random(seed), {}
    step = lambda n: q.steps[n - 1]
    def drawn(st, n):
        return [sh.new_item(st["bank"], st["entry"], rng.randrange(2**31), seen) for _ in range(n)]
    secs = []
    for n in plan["new"]:
        st, its = step(n), []
        if plan["pinned"]:
            for b, pid in st["examples"][:plan["per"]]:
                x = banks.get(b)
                if banks.has(b) and pid in getattr(x, "PROBLEM", {}):
                    its.append(sh.fixed_item(b, pid))
                    seen.setdefault(x.FAMILY, set()).add(x.seen_key(its[-1]["problem"]))
        its += drawn(st, plan["per"] - len(its))
        b = banks.get(st["bank"])
        secs.append(dict(sh.new_section(st["title"], b.INSTRUCTIONS), items=its))
    review = []
    for n, k in spread(plan["review"], round(len(plan["new"]) * plan["per"] * REVIEW_RATIO)).items():
        review += drawn(step(n), k)
    rng.shuffle(review)
    if review:
        secs.append(dict(sh.new_section("Review"), items=review))
    first = banks.get(step(plan["new"][0])["bank"])
    if title == DEFAULTS["title"]:
        title = f"{q.TITLE}: Step{'s' * (len(plan['new']) > 1)} {steps_text(plan['new']).replace('-', '–')}"
    sheet = sh.new_sheet(title, class_name, first.INSTRUCTIONS, versions)
    for sec in secs:                       # a section repeats the sheet's instructions only when they differ
        if sec["instructions"] == first.INSTRUCTIONS:
            sec["instructions"] = ""
    sheet["sections"] = secs
    return sh.fill_versions(sheet, seen)

def regroup(sheet, groups, rng):
    """Put every problem on the sheet into sections by type, following
    layout(groups, ...): a type's own section, or a mixed one (shuffled).
    Problems keep their order within a type. Nothing is redrawn."""
    its = sh.items(sheet)
    typ = lambda it: banks.get(it["bank"]).type_of(it["entry"])
    mine = [it for it in its if banks.get(it["bank"]).FAMILY == BANK and typ(it) in TYPE_KEYS]
    mix = {}
    for it in mine:
        mix[typ(it)] = mix.get(typ(it), 0) + 1
    secs = []
    for g in layout(groups, mix):
        sec = sh.new_section(heading(g), auto=f"{BANK}:{g['types'][0]}" if len(g["types"]) == 1 else "")
        sec["items"] = sorted((it for it in mine if typ(it) in g["types"]),     # stable: lesson, letters, formulas
                              key=lambda it: (it["bank"] == BANK, KEYS.index(it["entry"]) if it["entry"] in KEYS else 0))
        if len(g["types"]) > 1:
            rng.shuffle(sec["items"])
        secs.append(sec)
    others = [it for it in its if not any(it is m for m in mine)]
    names = banks.names()
    def where(it):
        b = banks.get(it["bank"])
        return names.index(it["bank"]), [e["key"] for e in b.ENTRIES].index(it["entry"])
    for it in sorted(others, key=where):                 # other banks: a section per type, in bank order
        b = banks.get(it["bank"])
        typ = b.type_of(it["entry"])
        tag = f"{b.FAMILY}:{typ}"
        sec = next((x for x in secs if x["auto"] == tag), None)
        if sec is None:
            ins = b.INSTRUCTIONS if b.INSTRUCTIONS != sheet["instructions"] else ""
            sec = sh.new_section(b.heading(typ), ins, auto=tag)
            secs.append(sec)
        sec["items"].append(it)
    sheet["sections"] = secs

def shuffle_all(sheet, rng):
    """One untitled section with every problem, shuffled."""
    its = sh.items(sheet)
    rng.shuffle(its)
    sheet["sections"] = [dict(sh.new_section(), items=its)]

# ------------------------------------------------------------------
# Reading an older practice .json (written before sheets existed)
# ------------------------------------------------------------------
def from_practice_json(path):
    """A sheet holding exactly the problems of an older NAME_vN.json and its sibling versions."""
    path = Path(path)
    d = json.loads(path.read_text())
    a = parser().parse_args(shlex.split(d["command"])[2:])
    m = re.fullmatch(r"(.*)_v\d+\.json", path.name)
    if not m:
        raise ValueError(f"{path.name}: expected a name like NAME_v1.json")
    vs, v = [], 1
    while (f := path.with_name(f"{m.group(1)}_v{v}.json")).exists():
        vs.append(json.loads(f.read_text())["problems"])
        v += 1
    if not vs:
        raise ValueError(f"{path.name}: no NAME_v1.json beside it")
    probs = vs[0]
    sheet = sh.new_sheet(a.title, a.class_name, L.INSTRUCTIONS, len(vs))
    sheet["command"] = d["command"]
    lay = layout(parse_groups(a.groups), {p["type"]: 1 for p in probs})
    secs = [sh.new_section()] if a.shuffle else \
        [sh.new_section(heading(g), auto=f"{BANK}:{g['types'][0]}" if len(g["types"]) == 1 else "") for g in lay]
    for i, p in enumerate(probs):
        e = ENTRY[p["type"] + ("f" if p.get("source") == "formula" else "")]
        clean = lambda q: {k: q[k] for k in ("type", "prompt", "target", "answer", "source") if k in q}
        it = dict(bank=BANK, entry=e["key"], seed=None, width=e["width"], space=e["space"],
                  problem=clean(p), alts=[clean(other[i]) for other in vs[1:]], edited=False,
                  status=L.check(p))
        secs[0 if a.shuffle else p["group"]]["items"].append(it)
    sheet["sections"] = secs
    return sheet

def read_sheet(path):
    """A .sheet.json, or an older practice .json converted; raises ValueError or OSError."""
    try:
        return sh.load(path)
    except ValueError:
        return from_practice_json(path)

# ------------------------------------------------------------------
# Writing
# ------------------------------------------------------------------
def build(sheet, out=DEFAULTS["out"], name=DEFAULTS["name"], compile=True):
    """Write NAME.sheet.json and, for every version, the worksheet, key, and
    slides (compiled when typst is found).
    Returns dict(out, files, compiled, sheet); raises RuntimeError."""
    if not sh.items(sheet):
        raise RuntimeError("no problems: the sheet is empty")
    outp = Path(out).expanduser().resolve()   # ~ is home; a relative out starts in the current folder
    outp.mkdir(parents=True, exist_ok=True)
    typst = shutil.which("typst") if compile else None
    sh.save(sheet, outp / f"{name}.sheet.json")
    written = [f"{name}.sheet.json"]
    for v in range(sheet["versions"]):
        base = f"{name}_v{v + 1}"
        files = {f"{base}.typ": writer.worksheet(sheet, v),
                 f"{base}_key.typ": writer.worksheet(sheet, v, key=True),
                 f"{base}_slides.typ": writer.slides(sheet, v)}
        for fname, text in files.items():
            (outp / fname).write_text(text)
            if typst:
                r = subprocess.run([typst, "compile", fname], cwd=outp, capture_output=True, text=True)
                if r.returncode:
                    raise RuntimeError(f"typst failed on {fname}:\n{r.stderr}")
            written.append(fname)
    return dict(out=outp, files=written, compiled=bool(typst), sheet=sheet)

# ------------------------------------------------------------------
# Command line
# ------------------------------------------------------------------
def parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mix", nargs="+", default=["all:2"], metavar="ENTRY:COUNT")
    ap.add_argument("--versions", type=int, default=DEFAULTS["versions"])
    ap.add_argument("--seed", type=int)
    ap.add_argument("--style", choices=("mixed", "letters", "formulas"), default="mixed",
                    help=argparse.SUPPRESS)           # old commands: formulas means the 3f entries
    ap.add_argument("--shuffle", action="store_true")
    ap.add_argument("--groups", nargs="+", default=[], metavar="GROUP",
                    help="print sections in this order; join types with +, rename with =: 9 8 3+4=Warm-up 1")
    ap.add_argument("--title", default=DEFAULTS["title"])
    ap.add_argument("--out", default=DEFAULTS["out"])
    ap.add_argument("--name", default=DEFAULTS["name"])
    ap.add_argument("--class", dest="class_name", default=DEFAULTS["class_name"], metavar="NAME")
    ap.add_argument("--draft", nargs="+", metavar="TOKEN",
                    help="a sheet from a sequence: SEQ STEPS [xN] [review STEPS|none] [pinned]")
    ap.add_argument("--sheet", metavar="FILE", help="print a saved .sheet.json (or older practice .json) again")
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--selftest", type=int, metavar="N")
    return ap

def main():
    a = parser().parse_args()
    seed = a.seed if a.seed is not None else random.randrange(10**6)
    if a.selftest:
        from sheets.banks import systems
        sys.exit(0 if selftest(a.selftest, seed) and systems.selftest(a.selftest, seed) else 1)
    try:
        if a.sheet:
            sheet = read_sheet(a.sheet)
        elif a.draft:
            plan = parse_draft(a.draft)
            sheet = draft_sequence(plan, a.versions, seed, a.title, a.class_name)
            sheet["command"] = draft_command(plan, a.versions, seed, a.title, a.out, a.name, a.class_name)
        else:
            mix, groups = apply_style(parse_mix(a.mix), a.style), parse_groups(a.groups)
            sheet = draft(mix, a.versions, seed, a.shuffle, groups, a.title, a.class_name)
            sheet["command"] = command_for(mix, a.versions, seed, a.shuffle, a.title, a.out, a.name,
                                           a.class_name, groups)
        r = build(sheet, a.out, a.name, compile=not a.no_compile)
    except (ValueError, RuntimeError, OSError) as e:
        sys.exit(str(e))
    n = len(sh.items(sheet))
    print(("" if a.sheet else f"seed {seed}: ") + f"{n} problems x {sheet['versions']} version(s) -> {r['out']}")
    print("  " + "\n  ".join(r["files"]) + ("" if r["compiled"] else "\n  (not compiled)"))

if __name__ == "__main__":
    main()
