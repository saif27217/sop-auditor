#!/usr/bin/env python3
"""Dump an ENTIRE Qdrant collection to JSONL (one record per chunk).

WHY: The skill's Pitfall #10 says "don't enumerate, it times out" — true for a
synchronous unfiltered scroll() (exceeds the 60s client timeout on large
collections like `vdc`, ~135k chunks). But a database-wide audit ("is validation
data for accuracy/specificity present ANYWHERE in the DB?") REQUIRES enumerating
every doc. This script does it safely:

  - run it in the BACKGROUND (terminal background=true, notify_on_complete=true)
  - uses limit=1000 pages + a client timeout of 600s
  - writes incrementally and flushes, so a crash loses little
  - prints progress every 5000 chunks

USAGE:
  source ~/.hermes/.env            # QDRANT_URL, QDRANT_API_KEY
  source .venv-sop/bin/activate     # qdrant_client installed here
  python dump_all_collection.py --collection vdc --out /home/sak/all_vdc_chunks.jsonl

Then group by doc_id in your analyzer (see scan_validation_deficiencies.py).
"""
import os, json, argparse
from qdrant_client import QdrantClient

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", default="vdc")
    ap.add_argument("--out", default="/home/sak/all_chunks.jsonl")
    ap.add_argument("--limit", type=int, default=1000)
    args = ap.parse_args()

    url = os.environ.get("QDRANT_URL"); key = os.environ.get("QDRANT_API_KEY")
    if not url or not key:
        raise SystemExit("Set QDRANT_URL / QDRANT_API_KEY (source ~/.hermes/.env)")
    c = QdrantClient(url=url, api_key=key, timeout=600)

    total = 0
    with open(args.out, "w") as f:
        offset = None
        while True:
            pts, offset = c.scroll(collection_name=args.collection,
                                   limit=args.limit, offset=offset,
                                   with_payload=True, with_vectors=False)
            if not pts:
                break
            for p in pts:
                pl = p.payload or {}
                rec = {
                    "doc_id": pl.get("doc_id") or pl.get("document_id") or "",
                    "source_pdf": pl.get("source_pdf") or pl.get("source") or "",
                    "location": pl.get("location") or "",
                    "chunk_text": pl.get("chunk_text") or "",
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                total += 1
            f.flush()
            if total % 5000 == 0:
                print(f"  ...{total} chunks dumped", flush=True)
            if offset is None:
                break
    print(f"DONE total={total} -> {args.out}", flush=True)

if __name__ == "__main__":
    main()
