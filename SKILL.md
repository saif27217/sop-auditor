---
name: sop-auditor
description: "Audit SOPs and controlled documents retrieved from a Qdrant RAG collection for discrepancies, contradictions, missing steps, and compliance gaps. Use when asked to audit, review, or reconcile SOPs / work instructions / procedures against standards (ISO 15189, NABL, ISO 13485, CLIA, etc.). Covers the full workflow: broad retrieval (with a full payload dump to defeat semantic top-k blindness), discrepancy analysis, and delivery as a Google Doc via Composio MCP."
version: 1.0.0
author: Sak / Lazer
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [sop, audit, qdrant, rag, compliance, iso15189, nabl, discrepancy, composio, google-docs]
    related_skills: [composio-mcp, deep-rag, literature-review, peer-review, scientific-critical-thinking]
---

# SOP Auditor

Audit Standard Operating Procedures (SOPs), work instructions, and controlled
documents stored as chunks in a Qdrant RAG collection. Detect contradictions,
missing steps, duplicated/conflicting instructions, ambiguous wording, and
regulatory/documentation gaps — then deliver an audit-ready report as a Google Doc.

## The one hard lesson this skill encodes

**Semantic top-k retrieval misses critical data.** In the founding audit
(Risk Assessment SOPs), a normal top-k vector search surfaced ~15 of 100 chunks
for the master SOP and ~15 of 290 for the work instructions. The **risk
matrices and RPN formulas were never retrieved** — they sit in dense tables
that don't match natural-language queries well. This produced a wrong audit
("matrices are missing") which had to be corrected.

**Fix:** Always do a *full payload-filtered dump* of the target document(s)
before analyzing. Use `client.scroll()` with a `MatchText` filter on `doc_id`,
paginate to exhaustion, and load every chunk. Then grep the full text for the
terms you care about. This is non-negotiable for tables, matrices, scales, and
banding values.

## When to Use This Skill

- "Audit the SOPs for <topic>"
- "Check these procedures for contradictions / compliance gaps"
- "Reconcile the master SOP with its work instructions"
- "Review our SOPs against ISO 15189 / NABL-112-A / ISO 13485"
- Any request to find discrepancies among controlled documents in the RAG store

## Architecture of the Workflow

```
1. Identify target docs        → from the user request, find doc_id substrings
2. FULL DUMP (not top-k)       → scripts/full_dump.py — scroll all chunks per doc
3. Scan for key terms          → RPN, severity, occurrence, bands, acceptance, etc.
4. Extract exact scales/tables → pull verbatim text for scoring + banding
5. Cross-document comparison   → table of conflicts
6. Findings + severity         → Critical/High/Medium/Low, by category
7. Deliver Google Doc          → Composio MCP GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN
                                 + staged UPDATE_DOCUMENT_SECTION_MARKDOWN appends
```

## Step 1 — Identify target documents

Query the collection broadly first to learn what `doc_id` values exist:

```python
from qdrant_client import QdrantClient
# credentials from env: QDRANT_URL, QDRANT_API_KEY
client = QdrantClient(url=URL, api_key=KEY, timeout=120)
# List distinct doc_ids (paginate scroll with no filter, or filter by category)
```

Typical `doc_id` substrings: `"MSP 29"`, `"Risk Work Instructions"`, `"SOP"`.
The `category` and `department` payload fields also help scope.

## Step 2 — FULL DUMP (the critical step)

Use `scripts/full_dump.py` (copy into the working dir or run from the skill dir).
It scrolls every chunk for a list of `doc_id` substrings and prints totals +
chunk counts. Always confirm you got ALL chunks (e.g. 100 for MSP 29, 290 for
Risk WI), not a top-k subset.

Key payload fields available per chunk:
`doc_id, track, source_pdf, chunk_id, chunk_text, section_path,
extraction_mode, quality_score, run_id, department, category, location,
prev_chunk_id, next_chunk_id, parent_chunk_id, chunk_hash`

Filter example:
```python
from qdrant_client.models import Filter, FieldCondition, MatchText
f = Filter(must=[FieldCondition(key="doc_id", match=MatchText(text="MSP 29"))])
offset=None; out=[]
while True:
    pts, offset = client.scroll(collection_name="vdc", scroll_filter=f,
                                limit=200, offset=offset,
                                with_payload=True, with_vectors=False)
    if not pts: break
    for p in pts: out.append(p.payload or {})
    if offset is None: break
```

## Step 3 — Scan for the terms that matter

Dense tables (RPN formulas, severity/occurrence scales, acceptance bands) only
appear when you grep the full text. See `scripts/scan_terms.py` for a term-list
scanner that reports hit counts per term across all dumped chunks.

## Step 4 — Extract verbatim scales / matrices

When two documents discuss the same workflow (e.g. master SOP vs department
work instruction), extract BOTH documents' exact wording for the same concept
(severity scale, RPN formula, acceptance band) and put them side by side. The
founding audit found a direct contradiction this way:

- Master SOP (MSP 29): `RPN = Severity × Occurrence` (2-factor, **no detection**)
- Work Instruction: `RPN = Severity × Occurrence × Detection` (3-factor)
- Bands conflict: MSP 29 `AC 6–25 / UAC 30–100` vs WI `AC 1–60 / UAC 60–1000`

That contradiction is invisible to top-k search but obvious in a full dump.

## Step 5 — Cross-document comparison

Build a conflict table:

| Dimension | Doc A | Doc B | Conflict |
|---|---|---|---|
| RPN factors | S × O (2) | S × O × D (3) | Direct contradiction |
| Severity scale | {3,4,5,8,10} | 1–10 | Divergent anchors |
| Acceptance bands | AC 6–25 / UAC 30–100 | AC 1–60 / UAC 60–1000 | Opposite verdicts |

## Step 6 — Findings with severity & category

For each issue: Severity (Critical/High/Medium/Low) × Category
(Compliance/Documentation/Workflow/Safety/Quality/Operational/Training/
Traceability/Record Keeping/Regulatory/Efficiency). Include:

- Current SOP text (short verbatim quote)
- Problem
- Why it matters
- Recommended improvement
- **Exact Suggested Change** — draft SOP text that could be inserted or
  modified directly (e.g. *"Add a new section 4.xx: 'TAT: Routine serum
  albumin results shall be reported within X hours of sample receipt.
  Urgent (STAT) albumin shall be reported within Y hours.'"*)
- Expected benefit
- Confidence (High/Medium/Low) + the chunk it came from

The **Exact Suggested Change** column is not optional. A finding that only
says "add TAT" is half-finished. The value is in providing language the SOP
owner can copy-paste with minimal edits. Default to placeholder variables
(e.g. X hours, Y days) where the exact number needs local calibration.

## Step 7 — Deliver as Google Doc (Composio MCP)

**Use the native `mcp_composio_*` session tools** — do NOT rely solely on the
JSON-RPC endpoint (the OAuth token file at `~/.hermes/mcp-tokens/composio.json`
can rotate and break direct calls). If `mcp_composio_*` tools are loaded, use
them directly via `COMPOSIO_MULTI_EXECUTE_TOOL`.

1. **Create** the doc (title + intro only — Composio rejects multiple Markdown
   tables in a single call):
   `COMPOSIO_MULTI_EXECUTE_TOOL` →
   `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN` with `title` + `markdown_text`.
   Returns `documentId` + `display_url` (double-nested:
   `result["data"]["results"][0]["response"]["data"]["documentId"]`).

2. **Append** the rest in stages — one Markdown table per
   `GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN` call (prose is fine in bulk,
   but split each table into its own call to avoid the multi-table rejection).
   Pass `document_id` + `markdown_text`. Omit `start_index` to append at end.

3. **Verify** the doc URL is reachable before reporting done.

> If `mcp_composio_*` tools are NOT in the session, fall back to the
> `composio-mcp` skill's direct JSON-RPC helper (requires a live
> `~/.hermes/mcp-tokens/composio.json` Bearer token + `initialize` handshake).

## Output format (audit-ready)

```
# Executive Summary
  Overall assessment / documentation quality / major risks / highest-priority fixes
# SOPs Reviewed  (table: SOP | Version | Chunks | Relevance)
# What the full dump contains  (verbatim scales, formulas, bands)
# Findings  (1..N: Severity | Category | Doc | Section | Evidence | Problem |
            Recommendation | **Exact Suggested Change** | Benefit | Confidence)
# Cross-SOP Conflict Table
# Worked Example  (same input → divergent verdict under each doc)
# Priority Action Plan  (Immediate / 30 days / Long term)
# Confidence Note  (state that findings are grounded in full-chunk retrieval)
```

## Evidence rules

- Every finding cites the source chunk (`source_pdf`, `location`, `chunk_id`).
- Never invent missing content. If a scale/band is absent, say so explicitly:
  "Insufficient evidence found in retrieved documents."
- State uncertainty. Distinguish "missing from docs" from "failed to retrieve".

## Pitfalls (learned the hard way)

1. **Top-k blindness** — semantic search hides tables/matrices. Always full-dump.
2. **Token rotation** — the Composio JSON-RPC token file can disappear mid-session
   when other accounts re-auth. Prefer native `mcp_composio_*` tools.
3. **Multi-table rejection** — `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN` / update calls
   reject more than one Markdown table per call. Split tables across calls.
4. **Double-nested JSON** — Composio responses wrap twice:
   `result.content[0].text` (string) → `json.loads` → `data.results[i].response.data`.
5. **Contradiction over absence** — when a child doc cites a parent but diverges,
   that's a Critical compliance finding, not a documentation gap.
6. **Verify deliverables end-to-end** — a tool returning `successful:true` does NOT
   mean the content is correct. After any file/doc write, re-read the actual result
   (clone the repo / open the doc / `read_file` the saved file) and check it is NOT
   base64/garbage and matches the source. A corrupted README slipped through because
   the success message was trusted without inspection.
7. **Composio `...FILE_CONTENTS` with `encoding:base64` stores RAW base64** — the API
   does NOT decode it; the file ends up containing the base64 string, not the decoded
   text. Do NOT pass `encoding:base64` expecting auto-decode. For GitHub file writes,
   prefer the `gh` CLI (`gh repo clone` → copy files → `git commit` → `git push`) which
   is authenticated and avoids the envelope limits that break large `mcp_composio_*`
   JSON args. (Large base64 args also exceed the tool-call envelope ~19 KB.)
8. **Footer artifacts masquerade as content** — grepping `tat`/`review` catches the
   document footer "Reviewed & Issued by" line, not a real TAT/review clause. Exclude
   footer hits when scanning for commitments.

## Pre-flight: the recurring gap checklist

Before writing findings, scan against `references/common-sop-gaps.md` — the common
*omissions* (TAT, calibration frequency, method validation, periodic review, risk-SOP
citation). These recur across the VDC BIO AU-series and are usually the real findings,
not contradictions. A worked example lives in `references/example-bio01-albumin.md`.

## Scripts

- `scripts/full_dump.py` — scroll all chunks for given `doc_id` substrings, print totals.
- `scripts/scan_terms.py` — term-hit scanner across dumped chunks.
- `scripts/extract_section.py` — verbatim extraction for specific terms/sections.

## References (support files)

- `references/common-sop-gaps.md` — reusable checklist of dimensions to scan every SOP
  against (TAT, calibration frequency, method validation, periodic review, risk-SOP
  citation). Start here before drafting findings.
- `references/example-bio01-albumin.md` — full worked audit (VDC BIO 01, BCG method)
  with verbatim evidence and findings; use as a template.
