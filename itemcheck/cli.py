"""Check one or more item files.

    python -m itemcheck examples/*.md
    python -m itemcheck examples/ --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .parser import parse_file
from .rules import check

ICON = {"error": "✖", "warning": "⚠", "info": "ℹ"}


def collect(paths):
    for p in paths:
        p = Path(p)
        if p.is_dir():
            yield from sorted(p.glob("*.md"))
        else:
            yield p


def main(argv=None):
    ap = argparse.ArgumentParser(description="Automated item-writing flaw checker.")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--fail-on", choices=["error", "warning", "never"], default="error")
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    results, worst = [], 0
    rank = {"info": 0, "warning": 1, "error": 2}
    for path in collect(a.paths):
        for item in parse_file(path):
            f = check(item)
            results.append({"file": str(path), "id": item.id,
                            "findings": [x.__dict__ for x in f]})
            worst = max([worst, *[rank[x.severity] for x in f]])

    if a.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(f"\n{r['id']}  ({r['file']})")
            if not r["findings"]:
                print("  ✔ no issues found")
            for x in r["findings"]:
                print(f"  {ICON[x['severity']]} {x['rule']:<22} {x['message']}")
        n = sum(len(r["findings"]) for r in results)
        print(f"\n{len(results)} item(s) checked, {n} finding(s).")

    threshold = {"error": 2, "warning": 1, "never": 99}[a.fail_on]
    return 1 if worst >= threshold else 0


if __name__ == "__main__":
    raise SystemExit(main())
