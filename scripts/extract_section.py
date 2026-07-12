#!/usr/bin/env python3
"""Verbatim extraction of specific terms/sections from dumped SOP chunks.

Prints the chunk text (truncated) for every chunk matching ANY of the given
predicates. Use to pull the exact RPN formula, severity/occurrence scales, and
acceptance bands from both documents for side-by-side comparison.

USAGE:
  python extract_section.py out.json --any "RPN" "60-1000" "VDC/MSP/29" "UAC"
  python extract_section.py out.json --all "rpn" "band"   # AND logic
"""
import json
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file")
    ap.add_argument("--any", nargs="*", default=[], help="match if ANY term present (OR)")
    ap.add_argument("--all", nargs="*", default=[], help="match only if ALL terms present (AND)")
    ap.add_argument("--max", type=int, default=900, help="char cap per chunk printed")
    ap.add_argument("--docs", nargs="*", default=None, help="restrict to these doc keys")
    args = ap.parse_args()

    data = json.load(open(args.json_file))
    keys = args.docs if args.docs else list(data.keys())

    for kw in keys:
        print(f"\n########## {kw} ##########", flush=True)
        for pl in data[kw]:
            t = pl.get("chunk_text", "") or ""
            low = t.lower()
            if args.any and not any(term.lower() in low for term in args.any):
                continue
            if args.all and not all(term.lower() in low for term in args.all):
                continue
            if len(t) < 40:
                continue
            src = pl.get("source_pdf", "").split("Work Instructions")[0].split("\\")[-1]
            print(f"\n===== src: {src} | len {len(t)} | loc {pl.get('location')} =====")
            print(t[:args.max])


if __name__ == "__main__":
    main()
