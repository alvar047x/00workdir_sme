#!/usr/bin/env python3
"""Pseudonymise AWS account ids in named files. Prints COUNTS ONLY, never an id.

  python3 ~/.sme/scrub-paths.py <file|dir> [...]           # dry run
  python3 ~/.sme/scrub-paths.py --write <file|dir> [...]   # apply

Stable pseudonyms: each distinct account maps to a consistent <aws-account-N>,
so "the same account" still reads as the same account after the scrub. D-0031.
"""
import re, sys, pathlib

PAT = re.compile(r'(?<!\d)(?<!-)\b\d{12}\b(?!\d)')
args = [a for a in sys.argv[1:] if a != "--write"]
WRITE = "--write" in sys.argv

targets = []
for a in args:
    p = pathlib.Path(a).expanduser()
    if p.is_dir():
        targets += [f for f in sorted(p.rglob("*"))
                    if f.is_file() and f.suffix in (".md", ".json") and ".git" not in f.parts]
    elif p.is_file():
        targets.append(p)

mapping, order = {}, []
def sub(m):
    v = m.group(0)
    if v not in mapping:
        order.append(v); mapping[v] = f"<aws-account-{len(order)}>"
    return mapping[v]

changed, total = [], 0
for p in targets:
    try: t = p.read_text()
    except Exception: continue
    new, n = PAT.subn(sub, t)
    if n:
        if WRITE: p.write_text(new)
        changed.append((p, n)); total += n

print("APPLIED" if WRITE else "DRY RUN")
print(f"distinct accounts : {len(order)}")
print(f"occurrences       : {total}")
for p, n in changed:
    print(f"  {n:>3}  {p}")
if not WRITE and total:
    print("\nnothing written. add --write to apply.")
