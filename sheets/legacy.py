"""Reading an older practice .json (written before sheets existed): one
NAME_vN.json per version, each holding the command that made it and its
problems. They were all literal equations.

    read_sheet(path)    a .sheet.json, or an older practice .json converted
"""
import json, re, shlex
from pathlib import Path
from . import sheet as sh
from .draft import BANK, DEFAULTS, ENTRY, L, heading, layout, parse_groups

def from_practice_json(path):
    """A sheet holding exactly the problems of an older NAME_vN.json and its sibling versions."""
    path = Path(path)
    d = json.loads(path.read_text())
    from .cli import parser                    # the old file's command, read as it was typed
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
    title = f"{L.TITLE} Practice" if a.title == DEFAULTS["title"] else a.title    # older files were all literal
    sheet = sh.new_sheet(title, a.class_name, L.INSTRUCTIONS, len(vs))
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
