# sop-auditor-bulk

Hermes skill for **database-wide / family-wide** SOP audits over a Qdrant RAG
collection. Dumps the *entire* collection (full payload, not top-k), classifies
every SOP against the recurring-gap checklist (Accuracy/Specificity validation,
TAT, periodic review, CLSI/EP method validation, calibration, critical values,
LOQ, MSP29), and delivers a consolidated audit as a Google Doc via Composio MCP.

This is the scaled companion to [`sop-auditor`](../sop-auditor/) (single/few-doc
deep audit). Use it when the question is scope-wide: "is validation data present
in ANY SOP?", "what common deficiencies exist across the whole AU-series?".

## Quick start

```bash
source ~/.hermes/.env
source .venv-sop/bin/activate

# 1. Dump the whole collection (run in background — ~135k chunks)
python scripts/dump_all_collection.py --collection vdc --out /home/sak/all_vdc_chunks.jsonl

# 2. Classify every SOP in a family (omit --family to scan all docs)
python scripts/scan_validation_deficiencies.py /home/sak/all_vdc_chunks.jsonl \
       --family "au series" --out /home/sak/au_series_deficiency_matrix.json

# 3. Build the consolidated Google Doc from the matrix
#    (create + staged one-table-per-call appends via Composio MCP)
```

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Full workflow, classification rules, pitfalls, worked example |
| `scripts/dump_all_collection.py` | Background-safe full-collection dump to JSONL (defeats the 60s scroll timeout) |
| `scripts/scan_validation_deficiencies.py` | Classifies every `doc_id` against the gap checklist; emits per-SOP matrix + aggregate JSON |
| `references/common-sop-gaps.md` | The recurring-gap checklist (TAT, calibration, method validation, periodic review, risk-SOP citation, …) |
| `references/au-series-validation-findings.md` | Result bank from the 2026-07-15 database-wide audit (the "is validation data anywhere?" answer + AU-series 45-SOP profile) |

## Requirements

- Python 3.11+, `qdrant-client` (`.venv-sop` venv)
- Env `QDRANT_URL`, `QDRANT_API_KEY` (source `~/.hermes/.env`)
- Collection `vdc` (default)
- Composio MCP with an active Google Docs connection

## License

MIT
