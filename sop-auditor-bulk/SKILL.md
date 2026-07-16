---
name: sop-auditor-bulk
description: "Database-wide / family-wide SOP deficiency scanner for a Qdrant RAG collection. Dumps the ENTIRE collection (full payload, not top-k), classifies every SOP against the recurring-gap checklist (Accuracy/Specificity validation, TAT, periodic review, CLSI/EP method validation, calibration, critical values, LOQ, MSP29), and delivers a consolidated audit as a Google Doc. Use when asked 'does any SOP carry validation data?', 'what common deficiencies exist across the series?', or to audit a whole analyzer family at once. Companion to sop-auditor (single-doc)."
version: 1.0.0
author: Sak / Lazer
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [sop, audit, qdrant, rag, bulk, compliance, iso15189, nabl, validation, composio, google-docs]
    related_skills: [sop-auditor, composio-mcp, deep-rag]
---

# SOP Auditor — Bulk (database-wide / family-wide)

Scan an ENTIRE Qdrant SOP collection (or one analyzer family within it) for
common validation/compliance deficiencies, then deliver a consolidated
audit-ready Google Doc.

This is the *scaled* companion to `sop-auditor` (which audits one or a few
documents in depth). Use `sop-auditor-bulk` when the question is scope-wide:
"is validation data for accuracy/specificity present in ANY SOP?", "what
common deficiencies exist across the whole AU-series?", "audit all 45
chemistry SOPs at once".

## The method (3 steps)

```text
1. FULL DUMP  → scripts/dump_all_collection.py  (background; ~135k chunks)
2. CLASSIFY   → scripts/scan_validation_deficiencies.py --family "au series"
3. DELIVER    → consolidated Google Doc (create + staged table appends)
```

### Step 1 — Full collection dump (background-safe)

`scripts/dump_all_collection.py` scrolls EVERY chunk in the collection to JSONL.
A synchronous unfiltered `scroll()` times out at the 60s client default on a
large collection (the `vdc` collection is ~135,642 chunks / 1,554 docs) — so
RUN IT IN THE BACKGROUND:

```bash
source ~/.hermes/.env                 # exports QDRANT_URL, QDRANT_API_KEY
source .venv-sop/bin/activate         # qdrant_client installed here
python scripts/dump_all_collection.py --collection vdc --out /home/sak/all_vdc_chunks.jsonl
```

Launch with `terminal(background=true, notify_on_complete=true)`, `limit=1000`,
client `timeout=600`. Wait for the `DONE total=…` line. Do NOT conclude
"enumeration is impossible" from a foreground timeout (see Pitfall #14 in
`sop-auditor`).

### Step 2 — Classify every SOP

`scripts/scan_validation_deficiencies.py` groups the JSONL by `doc_id` and
classifies each against the recurring-gap checklist
(`references/common-sop-gaps.md`). With `--family` it filters to a substring
(e.g. `"au series"`); omit it to scan all 1,554 docs.

```bash
python scripts/scan_validation_deficiencies.py /home/sak/all_vdc_chunks.jsonl \
       --family "au series" --out /home/sak/au_series_deficiency_matrix.json
```

Per-SOP fields emitted (see `references/common-sop-gaps.md` for the full
checklist): `accuracy`, `specificity` (REAL | NA | Refer | other | absent),
`tat`, `review_clause`, `clsi_ep`, `calibration`, `critical_values`, `msp29`,
`reference_intervals`, `interferences`, `loq` (ok | INVALID(high/low) | absent).

**Critical classification rules (learned the hard way):**
- **TAT** counts only on the WORD `turnaround` / `\btat\b`. The bare substring
  `tat` is a footer/word-fragment trap (`format`, `statement`, `microscop**y**`).
- **Periodic-review** counts only on an explicit
  `review every N years / shall be reviewed / next review due` clause. EXCLUDE
  the `Reviewed & Issued by` footer and QC-failure `review environmental
  conditions` text. A lone `Prepared by: Reviewe[…]` hit is the footer, NOT a
  review clause.
- **LOQ validity** is numeric: flag `LOQ < 0.5×LOD` (low) or `LOQ > 2×AMR`
  (high). BIO 02 (ACE LOQ 0–150) and BIO 04 (ADA LOQ 0–200) trip the low check
  — transcription errors, not real specs.

### Step 3 — Deliver as a Google Doc (Composio MCP)

Use the native `mcp__composio__*` session tools. One table per
`GOOGLEDOCS_UPDATE_DOCUMENT_SECTION_MARKDOWN` call (Composio rejects >1
Markdown table per call). Sections to emit:

```text
# Executive Summary            (the scope-wide answer + aggregate table)
# Methodology                  (full dump + classification rules)
# Database-wide context       (where real validation data DOES live)
# <Family> Deficiency Matrix   (one row per SOP — the big table)
# Aggregate Deficiency Rates
# Cross-SOP / Systemic Observations
# Priority Action Plan         (Immediate / 30 days / Long term)
# Confidence Note
```

**Always paste `display_url` in the final reply** (Pitfall #13). Verify the doc
by reading it back (`GET_DOCUMENT_PLAINTEXT`) before declaring done.

## Worked example (2026-07-15, VDC BIO AU-series)

Full dump of `vdc` → classified the 45 AU-series SOPs. Headline result:

| Dimension | Across 45 AU-series SOPs |
|---|---|
| Accuracy real | 0 (38 "NA", 7 absent) |
| Specificity real | 2 (RF 99%, Microalbumin 99%); 21 "Refer", 19 "NA" |
| TAT defined | 0 / 45 |
| Periodic-review clause | 0 / 45 |
| CLSI/EP citation | 0 / 45 |
| MSP 29 citation | 1 (BIO 15) |
| LOQ invalid | 2 (BIO 02, BIO 04) + 7 absent |
| Reference intervals / interferences | 45 / 45 (uniform strength) |

**Database-wide context:** validation data DOES exist in `vdc` — 29/1,554 SOPs
state real Accuracy, 115/1,554 state real Specificity — but it is concentrated
in serology/ELISA, molecular PCR, FISH, flow cytometry, HPLC, and troponin, NOT
in the AU-series clinical chemistry. The AU-series gaps are systemic, not three
outliers (BIO 02/03/04).

Consolidated deliverable (verified on creation):
`https://docs.google.com/document/d/1irdY941xhKWvabTkgEp3OLUkqdQyYxiIzQ8ibHd-DrA/edit`

Full result bank: `references/au-series-validation-findings.md`.

## Requirements

- Python 3.11+, `qdrant-client` (use the `.venv-sop` venv), env
  `QDRANT_URL` / `QDRANT_API_KEY` (source `~/.hermes/.env`).
- Collection `vdc` (default; override `--collection`).
- Composio MCP with an active Google Docs connection for delivery.

## Pitfalls (see `sop-auditor` for the full list)

- **Top-k blindness** — semantic search hides the validation fields; always
  full-dump.
- **Foreground dump timeout** — run the dump in the background (Pitfall #14).
- **Multi-table rejection** — one Markdown table per update call.
- **Footer `tat`/`review` false positives** — require explicit phrases.
- **Session-expiry fault** — `Required at "tools"` means regenerate the
  `session_id`; never fabricate a doc URL.
- **Paste the link** — always surface `display_url`.
