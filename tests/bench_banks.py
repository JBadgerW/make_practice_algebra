"""How long each generator bank takes to draw a problem, slowest first.

    python3 tests/bench_banks.py                  # every generator bank
    python3 tests/bench_banks.py slope_intercept_2_1 ka1_06_04   # just these
    python3 tests/bench_banks.py -n 5 --strict    # 5 per type; exit 1 if any bank is over budget

A draw includes the bank's own answer check, as on a sheet. A new bank
should average under BUDGET_MS a problem: :mix and :versions draw dozens at
once, and a slow bank is felt in every one of them. The usual causes are
sympy simplify() inside a retry loop, and templates that reject most draws;
draw with integers, and keep sympy for the check."""
import argparse, random, statistics, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sheets import banks, sheet as sh

BUDGET_MS = 100

def bench(name, n):
    """(mean ms a problem, slowest type and its mean, failures) for one bank."""
    b = banks.get(name)
    per_type, failed = {}, 0
    for e in b.ENTRIES:
        seen = {}
        for k in range(n):
            t = time.perf_counter()
            try:
                sh._draw(name, e["key"], 1000 * k + 7, seen)
            except RuntimeError:               # a small pool can run dry: not a speed problem
                failed += 1
                continue
            per_type.setdefault(e["key"], []).append((time.perf_counter() - t) * 1000)
    if not per_type:
        return None
    every = [ms for v in per_type.values() for ms in v]
    worst = max(per_type, key=lambda k: statistics.mean(per_type[k]))
    return statistics.mean(every), worst, statistics.mean(per_type[worst]), failed

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("banks", nargs="*", help="bank names (default: every generator bank)")
    ap.add_argument("-n", type=int, default=3, help="problems drawn per type (default 3)")
    ap.add_argument("--strict", action="store_true", help=f"exit 1 if a bank averages over {BUDGET_MS} ms")
    a = ap.parse_args()
    names = a.banks or [n for n in banks.names() if not getattr(banks.get(n), "FIXED", False)]
    rows = []
    for name in names:
        if not banks.has(name):
            sys.exit(f"no bank named {name!r}")
        r = bench(name, a.n)
        if r:
            rows.append((name, *r))
            print(f"\r{len(rows)}/{len(names)} {name:<40}", end="", file=sys.stderr, flush=True)
    print("\r" + " " * 50 + "\r", end="", file=sys.stderr)
    rows.sort(key=lambda r: -r[1])
    print(f"{'bank':<28} {'ms/problem':>10}   slowest type")
    for name, mean, worst, wms, failed in rows:
        flag = "  << over budget" if mean > BUDGET_MS else ""
        dry = f"  ({failed} ran dry)" if failed else ""
        print(f"{name:<28} {mean:>10.1f}   {worst} ({wms:.0f} ms){dry}{flag}")
    over = [r for r in rows if r[1] > BUDGET_MS]
    print(f"\n{len(rows)} banks; median {statistics.median(r[1] for r in rows):.1f} ms a problem; "
          f"{len(over)} over the {BUDGET_MS} ms budget")
    if a.strict and over:
        sys.exit(1)

if __name__ == "__main__":
    main()
