"""mixed-types: find CSV columns whose values mix types (int, float, date, bool, text)."""
import argparse, csv, json, re, sys
from collections import Counter, defaultdict

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?)?$")
NULLS = {"", "null", "none", "na", "n/a", "nan"}

def kind(v):
    s = v.strip()
    if s.lower() in NULLS: return None
    if s.lower() in {"true", "false"}: return "bool"
    try:
        int(s); return "int"
    except ValueError: pass
    try:
        float(s); return "float"
    except ValueError: pass
    if DATE.match(s): return "date"
    return "text"

def scan(path, samples=3):
    kinds = defaultdict(Counter); ex = defaultdict(dict)
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            for c, v in row.items():
                k = kind(v or "")
                if k:
                    kinds[c][k] += 1
                    ex[c].setdefault(k, []) if len(ex[c].get(k, [])) < samples else None
                    if len(ex[c][k]) < samples: ex[c][k].append(v)
    out = {}
    for c, k in kinds.items():
        ks = set(k) - ({"int"} if set(k) == {"int", "float"} else set())
        if len(ks) > 1:
            out[c] = {"counts": dict(k), "examples": ex[c]}
    return out

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv")
    a = p.parse_args(argv)
    rep = scan(a.csv)
    print(json.dumps(rep, indent=2))
    return 1 if rep else 0

if __name__ == "__main__":
    sys.exit(main())
