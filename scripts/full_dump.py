#!/usr/bin/env python3
"""Full payload-filtered dump of SOP chunks from a Qdrant collection.

WHY: Semantic top-k retrieval misses dense tables (RPN formulas, severity/
occurrence scales, acceptance bands). This scrolls EVERY chunk for the given
doc_id substrings so nothing is missed.

USAGE:
  source ~/.hermes/.env          # sets QDRANT_URL, QDRANT_API_KEY
  python full_dump.py "MSP 29" "Risk Work Instructions"
  python full_dump.py --collection vdc "SOP" --json out.json

Env: QDRANT_URL, QDRANT_API_KEY. Collection defaults to "vdc".
"""
import os
import sys
import json
import argparse

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchText


def client_from_env():
    url = os.environ.get("QDRANT_URL")
    key = os.environ.get("QDRANT_API_KEY")
    if not url or not key:
        raise SystemExit("Set QDRANT_URL and QDRANT_API_KEY (source ~/.hermes/.env)")
    return QdrantClient(url=url, api_key=key, timeout=120)


def dump_doc(client, collection, kw):
    f = Filter(must=[FieldCondition(key="doc_id", match=MatchText(text=kw))])
    offset = None
    out = []
    while True:
        pts, offset = client.scroll(
            collection_name=collection, scroll_filter=f,
            limit=200, offset=offset, with_payload=True, with_vectors=False,
        )
        if not pts:
            break
        for p in pts:
            out.append(p.payload or {})
        if offset is None:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords", nargs="+", help="doc_id substrings to dump")
    ap.add_argument("--collection", default="vdc")
    ap.add_argument("--json", help="optional path to write all payloads as JSON")
    args = ap.parse_args()

    client = client_from_env()
    all_payloads = {}
    for kw in args.keywords:
        chunks = dump_doc(client, args.collection, kw)
        all_payloads[kw] = chunks
        print(f"\n===== '{kw}' =====", flush=True)
        print(f"  TOTAL chunks: {len(chunks)}", flush=True)
        # quick sample of locations
        for pl in chunks[:3]:
            print(f"   loc={pl.get('location')}  len={len(pl.get('chunk_text','') or '')}  src={pl.get('source_pdf')}")

    if args.json:
        with open(args.json, "w") as f:
            json.dump(all_payloads, f, indent=2, default=str)
        print(f"\nWrote all payloads to {args.json}")


if __name__ == "__main__":
    main()
