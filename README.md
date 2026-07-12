# sop-auditor

Hermes skill + scripts for auditing SOPs / work instructions stored as chunks in a
Qdrant RAG collection — detecting contradictions, missing steps, and compliance gaps,
then delivering an audit-ready report as a Google Doc via Composio MCP.

## Why this exists

A normal semantic top-k search **misses critical data**. In the founding audit
(Risk Assessment SOPs), top-k surfaced ~15 of 100 chunks for the master SOP and
~15 of 290 for the work instructions — the risk matrices and RPN formulas were
never retrieved (they live in dense tables that don't match natural-language
queries). That produced a wrong audit which had to be corrected.

The fix is a **full payload-filtered dump** of every chunk for the target documents
before any analysis. This repo packages that workflow as a reusable Hermes skill.

## What it does

1. Identify target docs from the user request (`doc_id` substrings).
2. **Full dump** (not top-k) every chunk for those docs via `client.scroll()`.
3. Scan for the terms that matter (RPN, severity, occurrence, bands, acceptance).
4. Extract verbatim scales/matrices from each doc.
5. Cross-document comparison → conflict table.
6. Findings with severity × category, each grounded in a source chunk.
7. Deliver as a Google Doc (create + staged table appends via Composio MCP).

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The full skill: workflow, evidence rules, pitfalls, output format |
| `scripts/full_dump.py` | Scroll ALL chunks for given `doc_id` substrings; print totals / dump JSON |
| `scripts/scan_terms.py` | Term-hit scanner across dumped chunks |
| `scripts/extract_section.py` | Verbatim extraction for specific terms/sections |

## Requirements

- Python 3.11+, `qdrant-client`
- Env: `QDRANT_URL`, `QDRANT_API_KEY` (source `~/.hermes/.env`)
- Collection name: `vdc` (default; override with `--collection`)
- Composio MCP with an active Google Docs connection for the delivery step

## Install as a Hermes skill

```bash
# copy into your Hermes skills dir
cp -r . ~/.hermes/skills/automation/sop-auditor/
```

## Quick start

```bash
source ~/.hermes/.env
python scripts/full_dump.py "MSP 29" "Risk Work Instructions" --json dump.json
python scripts/scan_terms.py dump.json
python scripts/extract_section.py dump.json --any "RPN" "60-1000" "VDC/MSP/29"
```

## The founding finding (example)

The Risk Assessment master SOP (VDC MSP 29) defines `RPN = Severity × Occurrence`
(2-factor, no detection axis), while its own work instructions define
`RPN = Severity × Occurrence × Detection` (3-factor). Acceptance bands also conflict
(MSP 29 `AC 6–25 / UAC 30–100` vs WI `AC 1–60 / UAC 60–1000`). Same failure mode,
opposite risk verdict. Only visible via full dump.

## License

MIT
