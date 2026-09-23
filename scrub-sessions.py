#!/usr/bin/env python3
"""One-shot: pseudonymise AWS account ids under ~/.sme/sessions before those
files move into a repo that pushes to GitHub (D-0031).

Stable pseudonyms, not blanket redaction: each distinct account maps to a
consistent <aws-account-N>, so "the same account as before" and "three distinct
accounts" still read correctly after the scrub.

Run:  python3 ~/.sme/scrub-sessions.py            # report only
      python3 ~/.sme/scrub-sessions.py --write    # apply

Prints COUNTS ONLY. It never prints an account id.
"""
import re, sys, pathlib

ROOT = pathlib.Path.home() / ".sme" / "sessions"
PAT = re.compile(r'(?<!\d)\b\d{12}\b(?!\d)')
WRITE = "--write" in sys.argv

mapping, order = {}, []
def sub(m):
    v = m.group(0)
    if v not in mapping:
        order.append(v); mapping[v] = f"<aws-account-{len(order)}>"
    return mapping[v]

changed, total = [], 0
for p in sorted(ROOT.rglob("*")):
    if ".git" in p.parts or not p.is_file() or p.suffix not in (".md", ".json"):
        continue
    try:
        t = p.read_text()
    except Exception:
        continue
    new, n = PAT.subn(sub, t)
    if n:
        if WRITE:
            p.write_text(new)
        changed.append((p.relative_to(ROOT), n)); total += n

print(f"{'APPLIED' if WRITE else 'DRY RUN'}")
print(f"distinct accounts : {len(order)}")
print(f"occurrences       : {total}")
print(f"files             : {len(changed)}")
for rel, n in changed:
    print(f"  {n:>3}  {rel}")
if not WRITE:
    print("\nnothing written. re-run with --write to apply.")
