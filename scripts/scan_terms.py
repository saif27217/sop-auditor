#!/usr/bin/env python3
"""Term-hit scanner across dumped SOP chunks.

Reads payloads dumped by full_dump.py (--json out.json) and reports, per
document, how many chunks contain each search term. Use this to locate the
dense tables (RPN, severity, occurrence, bands) that top-k search hides.

USAGE:
  python scan_terms.py out.json
  python scan_terms.py out.json --terms "RPN" "severity" "occurrence" "UAC" "60-1000"
"""
import json
import argparse
from collections import defaultdict

DEFAULT_TERMS = [
    "RPN", "risk priority", "severity", "occurrence", "detect", "probability",
    "acceptab", "matrix", "1-60", "60-1000", "UAC", "unacceptable",
    "clinically acceptable", "ACP", "FMEA", "scale", "residual", "goal",
    "review", "timeline", "responsib", "change control",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file", help="payloads JSON from full_dump.py")
    ap.add_argument("--terms", nargs="*", default=DEFAULT_TERMS)
    args = ap.parse_args()

    data = json.load(open(args.json_file))
    for kw, chunks in data.items():
        print(f"\n################ {kw} ################", flush=True)
        # group by department/source for work instructions
        bydept = defaultdict(list)
        for pl in chunks:
            sp = pl.get("source_pdf", "")
            dept = sp.split("Work Instructions")[0].split("\\")[-1] if "Work Instructions" in sp else (pl.get("department") or "unknown")
            bydept[dept].append(pl.get("chunk_text", "") or "")
        print(f"TOTAL chunks: {len(chunks)} | distinct source groups: {len(bydept)}", flush=True)
        for t in args.terms:
            c = sum(1 for pl in chunks if t.lower() in (pl.get("chunk_text", "") or "").lower())
            if c:
                print(f"  term '{t}': {c} chunks")


if __name__ == "__main__":
    main()
