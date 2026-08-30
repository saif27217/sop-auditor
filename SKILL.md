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

If you ALREADY know the `doc_id` substring for the target SOP (e.g. from a prior
audit or from the user's request such as "VDC BIO 02 ACE"), **skip straight to
Step 2** — call `full_dump.py` with that substring. Do NOT enumerate the whole
collection first; an unfiltered `client.scroll()` over a large collection
(`vdc` has hundreds of docs) **times out at the 60s client default** (see
Pitfall #10).

If you genuinely do not know the target's `doc_id`, the supported (but slow)
pattern is a `MatchText`/`category` filtered `scroll()` — never a bare
`scroll_filter=None` over the full collection.

Typical `doc_id` substrings: `"MSP 29"`, `"Risk Work Instructions"`, `"VDC BIO 02"`.
The `category` and `department` payload fields also help scope.

## Step 2 — FULL DUMP (the critical step)

Use `scripts/full_dump.py` (copy into the working dir or run from the skill dir).
It scrolls every chunk for a list of `doc_id` substrings and prints totals +
chunk counts. Always confirm you got ALL chunks (e.g. 100 for MSP 29, 290 for
Risk WI), not a top-k subset.

### Step 2b — Database-wide / family-wide audits (new in v1.1)

When the question is scope-wide ("is validation data present in ANY SOP?",
"what common deficiencies exist across the whole series?"), a per-`doc_id`
`full_dump.py` loop is insufficient — you must enumerate the entire collection.
Pitfall #10 warns a synchronous unfiltered `scroll()` times out, but you CAN do
it safely:

1. `python scripts/dump_all_collection.py --collection vdc --out /home/sak/all_vdc_chunks.jsonl`
   — **run in the BACKGROUND** (`terminal(background=true, notify_on_complete=true)`),
   with `limit=1000` and `client timeout=600`. A `~135k`-chunk collection takes a
   few minutes; wait for the `DONE total=…` line, don't poll the 60s foreground cap.
2. `python scripts/scan_validation_deficiencies.py /home/sak/all_vdc_chunks.jsonl --family "au series" --out matrix.json`
   — classifies every matching `doc_id` against the recurring-gap checklist and
   emits a per-SOP matrix + aggregate (see `references/au-series-validation-findings.md`
   for the worked result). Omit `--family` to scan all docs.
3. Build the consolidated Google Doc from the matrix (one table per
   `UPDATE_DOCUMENT_SECTION_MARKDOWN` call — Pitfall #3).

This is the supported way to defeat Pitfall #10 *and* answer scope-wide questions.

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

### Cumulative series table (batch sequential audit)

When auditing a **family of SOPs** sequentially (user says "continue" → next SOP), maintain a **cumulative contrast table** that grows one row per SOP:

1. **Initialize** the table with the first SOP's row. Columns: LOQ, Calibration, Critical Results, Clinical Decision Values, §4.18 "Variab", TAT, plus analyte-specific fields (Precision/MU, EQA program, Specificity data).
2. **Append a row** for each subsequent SOP before writing its findings. This gives context for which gaps are recurring vs per-SOP.
3. **Highlight outliers** in **bold** — LOQ errors, unique calibration patterns, real validation data (e.g. Specificity 99.5%), or rare fields that are populated when most are NA.
4. **Reference** the cumulative table in the "Cross-SOP Contrast" section of every audit doc.

This pattern was refined during the VDC BIO AU-series (BIO 02–10, 2026-07-16). The result bank lives in `references/au-series-gap-matrix.md`.

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

**Use the native `mcp__composio__*` session tools** — do NOT rely solely on the
JSON-RPC endpoint (the OAuth token file at `~/.hermes/mcp-tokens/composio.json`
can rotate and break direct calls). If `mcp__composio__*` tools are loaded, use
them directly via `mcp__composio__COMPOSIO_MULTI_EXECUTE_TOOL` (pass a valid
`session_id` — see Pitfall #9 for the expiry signal).

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
   footer hits when scanning for commitments. A SECOND false positive this session:
   the footer artifact also appears truncated as **"Prepared by: Reviewe[…]"** (the
   "Reviewed by:" line wraps). When a `review` scan returns exactly one hit that is
   just "Prepared by: Reviewe", that is NOT a periodic-review clause — treat the SOP
   as having no review clause (confirmed on VDC BIO 04 ADA). Always require an
   explicit "review every N years / shall be reviewed / next review due" phrase.
9. **Google Doc delivery can fail via a session-expiry fault (not a content error).**
   When `COMPOSIO_MULTI_EXECUTE_TOOL` returns `Required at "tools"` (bare key, NOT
   `tools[0]`) on EVERY call regardless of arguments, the `session_id` you used earlier
   has expired. **Fix:** call `COMPOSIO_SEARCH_TOOLS(queries=[...], session={generate_id:true})`
   to get a fresh `session.id`, then pass that new `session_id` to all subsequent calls.
   If it STILL fails after regeneration, it is a transient gateway fault — do NOT loop:
   write the full audit to a local Markdown file (`/home/sak/sop_audit_<doc>.md`),
   report the blocker honestly with the local path, and retry the Doc creation on a
   fresh turn. Never fabricate a Google Doc URL when the creation call did not return a
   real `documentId`. (Full write-up of the `Required at "tools"` signal: composio-mcp
   skill, Common Errors section.)

10. **Unfiltered `scroll()` times out on large collections.** Enumerating distinct
   `doc_id`s with a no-filter `client.scroll()` over the whole `vdc` collection
   exceeds the 60s client timeout (hundreds of docs × many chunks). **Fix:** skip
   enumeration — call `full_dump.py "VDC BIO 02 - ACE"` directly (a `MatchText`
   filter on the known `doc_id` substring returns all matching chunks fast, ~seconds).
   Only enumerate distinct doc_ids when you genuinely don't know the target's
   substring, and then use a tight `MatchText`/`category` filter with a raised
   `timeout=`, never `scroll_filter=None` over the full collection.

review every N years'.

12. **`COMPOSIO_MULTI_EXECUTE_TOOL` shape: `tool_slug` goes INSIDE each `tools[]` entry.** A call shaped as `{ tool_slug: "...", tools: [{ arguments: {...} }] }` (slug as a *sibling* of `tools`) is rejected with `Validation error: Expected object, received string at "tools[0]"`. The correct shape is `tools: [{ arguments: {...}, tool_slug: "GOOGLEDOCS_..." }]`. Keep `tool_slug` adjacent to its `arguments` inside the array entry when building the call.

13. **Always paste the `display_url` in your final reply.** Building + verifying the Doc is not the end of the turn. A run that created and verified the doc but omitted the link forced the user to ask "Share the link". Both `CREATE_DOCUMENT_MARKDOWN` and `GET_DOCUMENT_PLAINTEXT` return `display_url`/`documentId` — surface it explicitly in your closing message.

14. **Whole-collection enumeration IS possible — just run it in the background.** Pitfall #10's
   "unfiltered scroll times out" applies to a *synchronous* `scroll()` inside a 60s
   foreground/terminal cap. A database-wide or family-wide audit needs every chunk, and
   you CAN get it: `python scripts/dump_all_collection.py --collection vdc --out all.jsonl`
   launched with `terminal(background=true, notify_on_complete=true)`, `limit=1000`,
   `client timeout=600`. A ~135k-chunk collection finishes in a few minutes; the
   background process is not bound by the foreground 60s timeout. Do NOT call an unfiltered
   `scroll()` in the FOREGROUND and then conclude "enumeration is impossible" — that blocks
   the real scope-wide answer. After it completes, `scripts/scan_validation_deficiencies.py`
   classifies every `doc_id` against the gap checklist (see `references/au-series-validation-findings.md`).

15. **Doc_id substrings may have non-standard spacing, casing, or naming.** A `MatchText`
   search for `"BIO 07"` (single space) returned zero hits because the actual doc_id was
   `"VDC BIO  07 - AMMONIA BY AU 5800"` (double space, all-caps, "BY AU 5800" instead of
   "by AU Series"). Similarly, `"BIO 10"` matched BIO 101, 107, 103.1 (numeral prefix
   collision) before the intended AU Series AST doc. **Fix:** when a direct substring
   search fails, try multiple patterns: the analyte name alone, the full instrument suffix,
   or a broader substring. Scope via `category` or `department` payload fields first.

## Pre-flight: the recurring gap checklist

Before writing findings, scan against `references/common-sop-gaps.md` — the common
*omissions* (TAT, calibration frequency, method validation, periodic review, risk-SOP
citation). These recur across the VDC BIO AU-series and are usually the real findings,
not contradictions. A worked example lives in `references/example-bio01-albumin.md`.

## Deep Audit Mode — going beyond the recurring gaps

After the standard recurring-gap scan returns its findings, execute the **deep audit
checklist** (`references/deep-audit-checklist.md`) to uncover structural, operational,
quality, and workflow issues that the standard scan misses.

The deep audit covers 12 dimensions:
1. **Section Map** — are all ISO 15189-required sections present?
2. **Internal Cross-Reference Validation** — does the SOP link its own sections?
3. **Vague Language Scan** — "as required", "appropriate", "etc." without criteria
4. **Pre-Analytical Checklist** — fasting, tube type, centrifugation, stability
5. **Post-Analytical Checklist** — auto-commenting, delta check, dilution protocol
6. **QC Detail Checklist** — LJ charts, Westgard rules, OOS procedure
7. **Calibration Detail Checklist** — beyond frequency (traceability, acceptance criteria)
8. **Safety Checklist** — BSL, PPE, spill, waste disposal
9. **Document Control Checklist** — amendment log, version, review clause
10. **Numerical Consistency Checks** — LOQ≥LOD? AMR logical? Units consistent?
11. **Operational Workflow Gaps** — derived calculations (ratios, gradients, clearances)
12. **Second-Pass Deep Items** — duplicates, contradictions, empty fields, orphan refs

Each dimension has a structured checklist with severity assignments per missing item.
The VDC BIO 01 deep audit (2026-07-16) using this checklist produced **9 additional
findings** beyond the standard 6 recurring gaps, including: zero cross-references, QC
detail gaps, empty amendment log, and missing operational SAAG workflow.

Run the deep audit after the standard scan when the user asks to "go deeper" or
when the standard findings cover only the obvious gaps.

## Full-Lifecycle Section Audit — auditing EVERY section, not just analytical performance

A recurring weakness: audits default to 6–7 analytical sections (TAT, calibration,
precision/MU, accuracy/specificity, reference interval, review clause, critical results)
and SKIP the sections that carry the most operational risk — Purpose/Scope, Sample Type,
Collection Timing, Handling/Stability, **Rejection Criteria**, **Test Procedure step-wise**,
**Limitations**, Safety (reagent-specific hazards), Clinical Interpretation, Reporting
format. This was corrected during the VDC BIO 147 Galactose audit (2026-08-29), where the
first pass missed that the SOP's Rejection Criteria copied serum-plasma boilerplate
("grossly haemolysed") that is irrelevant to dried blood spots, and that "Special timing
of collection: NA" contradicted the Day 3–5 collection text two lines below.

**Mandatory:** for every SOP audit, walk ALL of these 18 lifecycle sections and record a
status (GOOD / OK / PARTIAL / GAP / CONTRADICTION) per section in a scorecard table:

1. **Purpose & Scope** — does it state the test's intent AND its limits (screening-only?
   not for confirmatory use — match the kit insert's intended-use caveat)?
2. **Definitions / Abbreviations** — are all abbreviations used in the body defined?
   (e.g. GALT/GALK/GALE/DBS/NBS if referenced)
3. **Responsibility / Competency** — who is authorised; any training prerequisite?
4. **Sample Type** — matrix + container (e.g. Whatman 903 DBS); verify vs kit insert.
5. **Collection Timing** — window (e.g. Day 3–5 / 48–120 h); flag "NA" fields that
   contradict a stated window elsewhere in the same SOP.
6. **Handling / Transport / Stability** — temp, duration; verify vs kit storage clause.
7. **Rejection Criteria** — MUST be matrix-appropriate. A DBS SOP must NOT list
   "grossly haemolysed / highly lipemic / highly icteric" (those are serum-plasma criteria;
   a filter card does not haemolyse). Keep only DBS-relevant rejects (incomplete saturation,
   insufficient volume, wrong card, transport delay, ID error).
8. **Test Procedure (step-wise)** — reproduce each step (volumes, incubation, read
   wavelength/mode) and compare line-by-line vs the kit insert. Flag over-specification
   (e.g. "405–550 nm, kinetic" when the assay is 550 nm endpoint only) and wording drift
   ("part of Color Booster" missing the "1" in a 1:10 ratio).
9. **Calculation** — formula vs kit; units consistent.
10. **IQC / EQC** — levels, frequency, rules, post-maintenance/repair re-qualification,
    reference to internal QC SOP (e.g. MSP/18). Check for contradiction with a "Control: NA"
    field elsewhere.
11. **Calibration Frequency** — beyond "when kit opened"; traceability.
12. **Performance** — Precision (%CV) & MU vs kit's validated CV; Accuracy; Specificity
    (numeric or cross-ref); flag magnitudes ~2× the kit as CAPA-level.
13. **AMR / LOD / LOQ** — internal consistency (LOD ≤ LOQ ≤ AMR) and vs kit sensitivity.
14. **Reference Interval** — is it sourced/locally validated, or a fixed number with no
    basis? Kit inserts often say "each lab must establish its own cut-off" — a fixed range
    cited without derivation is a finding.
15. **Limitations / Potential Sources of Variation** — list ALL kit-cited cautions
    (transfusion, premature, low-birth-weight, sick newborns, <48 h). An SOP that lists
    only one while the kit lists five is a PARTIAL finding.
16. **Safety** — generic GLP PLUS reagent-specific hazards (e.g. TCA elution buffer is
    corrosive H315; sodium azide plumbing warning). Flag if only generic rules present.
17. **Clinical Interpretation** — mechanism/deficiency text vs kit; watch substrate-name
    drift (e.g. "galactose-6 phosphate" vs kit's "galactose-1-phosphate").
18. **Reporting / TAT / Critical Results / Review clause** — turnaround time, urgent-report
    path, critical-value threshold, and a real periodic-review record (not just a footer).

Deliver the scorecard as its own section in the audit Doc (see
`references/full-lifecycle-scorecard-template.md`). The BIO 147 comprehensive audit
(2026-08-29, Google Doc `1vlJmENywiFdaTqYM2CZMCgIbfzdpZNHFVH_0T8Gh3aU`) is the worked
example of this full-lifecycle approach.

## Reference Section Audit (SOP §4.19 or equivalent)

After the 18-section lifecycle walk, audit the **References** section as a standalone
section in the audit Doc. This was formalized during the BIO 166 v2 audit (2026-08-30).

**Mandatory checklist:**
1. **Primary method reference** — is the kit insert / manufacturer manual cited? (e.g. "Roche Cobas Trop T sensitive kit insert")
2. **Internal SOP references** — are supporting procedures cited? (e.g. "VDC/MSP/14 - Primary Sample Collection Manual", "VDC/MSP/20 - Reporting of Results")
3. **Traceability** — do Critical Values / Sample Collection clauses point to these references? (e.g. "report immediately per VDC/MSP/20")
4. **Appendices / Forms** — are any forms, logs, or work instructions referenced? (e.g. "Appendices/Forms/WIs/Logs: None" or list them)
5. **Completeness** — no missing references; no orphan citations (a reference cited in the body but not listed in §4.19 is a finding)

**Assessment:** GOOD (complete, well-traced) / PARTIAL (missing one internal reference) / GAP (no references cited).

The BIO 166 v2 audit (Google Doc `168cT6_bK4UwUlKcmbzjHJY4HzEZcOwAqj5ZOOqaPCJI`) is the worked example — its reference section was rated STRONG (Roche insert + MSP/14 + MSP/20, all well-traced).

## Grammar, Spelling & Clinical-Accuracy Scan

After the lifecycle walk and reference audit, run a **Grammar/Spelling/Clinical-Accuracy scan** as a standalone section. This was formalized during the BIO 166 v2 audit (2026-08-30).

**Mandatory checklist:**
1. **Spelling consistency** — flag mixed British/US spelling (e.g. "hemolysis" vs "haemolysed"). Recommend standardizing to one convention (British preferred in Indian lab SOPs).
2. **Clinical terminology** — verify key terms match the kit insert (e.g. "chromatographic immunoassay", "myocardial infarction", "lateral flow"). No clinical errors detected in BIO 166.
3. **Clinical accuracy** — verify clinical statements match the kit insert AND standard references (e.g. "cTnT rises 2-10 h after AMI onset, detectable up to 14 days" — clinically correct per Roche literature).
4. **Interference thresholds** — verify numeric limits match the kit insert exactly (e.g. bilirubin ≤20, Hb ≤200, TG ≤500, biotin ≤100).
5. **No clinical errors** — flag any statement that contradicts standard cardiology / biochemistry references.

**Assessment:** GOOD (no errors) / PARTIAL (1–2 spelling inconsistencies, no clinical errors) / GAP (clinical error detected).

The BIO 166 v2 audit rated this section GOOD — one spelling inconsistency (hemolysis vs haemolysed), no clinical errors, all statements verified against the kit insert and standard references.

## 3-Source Clinical Data Verification (NEW — 2026-08-31)

After the lifecycle walk, reference audit, and grammar/clinical scan, run a **3-source verification** against Qdrant collections. This catches errors the kit-insert-only audit misses: textbook reference ranges, clinical interpretations from Harrison's, and test catalog cross-checks.

**Mandatory verification sources:**
1. **`biochem-v1`** (26,303 points) — Biochemistry textbook. Query for:
   - Reference ranges (verify SOP's range matches textbook)
   - Analyte info (mechanism, pathophysiology context)
   - Interference data (cross-check SOP's interference list against textbook)
2. **`harrison-22nd`** (39,460 points) — Harrison's Principles of Internal Medicine. Query for:
   - Clinical interpretations (verify SOP's interpretation text matches Harrison's)
   - Disease context (e.g. "cTnT rises 2-10h after AMI" — verify against Harrison's cardiology chapter)
   - Critical value thresholds (verify SOP's critical values match Harrison's clinical guidance)
3. **`lab-tests-galore`** (4,014 points) — Lab test catalog. Query for:
   - Service code (verify SOP's service code matches catalog)
   - Department (verify SOP's department matches catalog)
   - Processing type (Local/OutSource — verify SOP's processing matches catalog)
   - Reference ranges (verify SOP's range matches catalog's range)
   - TAT (verify SOP's TAT matches catalog's schedule mode)

**Verification method:**
- Use `qdrant_client` to query each collection with a keyword search (e.g. `"albumin reference range"`, `"troponin T critical value Harrison's"`).
- Compare retrieved context against SOP text. Flag discrepancies as findings (severity: High if critical value mismatch, Medium if range differs by >10%, Low if minor wording difference).
- Cite source collection and point ID in findings (e.g. `[biochem-v1: point_12345]`).

**Assessment:** VERIFIED (all 3 sources agree) / PARTIAL (1–2 sources disagree, minor) / GAP (critical value mismatch or textbook contradicts SOP).

The BIO 166 v2 audit rated this VERIFIED — all 3 sources agreed on troponin T critical values, reference ranges, and clinical interpretations.

## Scripts

> **Runtime setup (this host):** the system `python3` does NOT have `qdrant_client`.
> Create a venv once, then run scripts inside it:
> ```bash
> uv venv .venv-sop && source .venv-sop/bin/activate && uv pip install qdrant-client
> source ~/.hermes/.env   # exports QDRANT_URL, QDRANT_API_KEY
> python scripts/full_dump.py --collection vdc "VDC BIO 02 - ACE" --json /home/sak/dump.json
> ```
> Do NOT run an unfiltered `client.scroll()` to "discover" doc_ids on a large
> collection — it times out (see Pitfall #10). Go straight to the targeted dump.

- `scripts/full_dump.py` — scroll all chunks for given `doc_id` substrings, print totals.
- `scripts/scan_terms.py` — term-hit scanner across dumped chunks.
- `scripts/extract_section.py` — verbatim extraction for specific terms/sections.
- `scripts/dump_all_collection.py` — **background-safe** full-collection dump to JSONL
  (defeats Pitfall #10 for database-wide audits). Run with `terminal(background=true,
  notify_on_complete=true)`.
- `scripts/scan_validation_deficiencies.py` — classifies every `doc_id` in a dumped
  JSONL against the recurring-gap checklist (Accuracy/Specificity/TAT/review/CLSI/
  calibration/critical/LOQ/MSP29); emits a per-SOP matrix + aggregate JSON.

## References (support files)

- `references/common-sop-gaps.md` — reusable checklist of dimensions to scan every SOP
  against (TAT, calibration frequency, method validation, periodic review, risk-SOP
  citation). Start here before drafting findings.
- `references/au-series-validation-findings.md` — condensed result bank from the
  2026-07-15 database-wide audit: the "is validation data anywhere?" answer, the AU-series
  45-SOP deficiency profile, and the reusable scan pipeline. Read BEFORE a scope-wide or
  new-BIO audit.
- `references/example-bio01-albumin.md` — full worked audit (VDC BIO 01, BCG method)
  with verbatim evidence and findin'gs; use as a template.
- `references/example-bio02-ace.md` — full worked audit (VDC BIO 02, ACE / FAPGG method),
  including the LOQ=0–150 U/L transcription-error finding; use as a second template.
- `references/example-bio03-acp.md` — full worked audit (VDC BIO 03, ACP / Alpha Naphthyl
  phosphate kinetic method); shows a *correct* LOQ plus a unique Calibration-Frequency
  "NA" self-contradiction (§4.7 vs §4.8.1) and a "Potential Variability: NA" field.
- `references/example-bio04-ada.md` — full worked audit (VDC BIO 04, ADA / Peroxidase
  method); shows a LOQ=0–200 U/L inconsistency (LOQ > AMR 0–20, contradicts LOD 4) and a
  "Potential Sources of Variations: NA" field (§4.18). Pair with BIO 02/03 audits.
- `references/example-bio08-amylase.md` — full worked audit (VDC BIO 08, Amylase /
  AU Series chromogenic); strongest-in-series pattern — CRR properly > AMR with validated
  dilution, Clinical Decision Values defined (50, 120, 200), Precision/MU stated, §4.18
  populated. Use as the "minimal-gap" SOP reference.
- `references/au-series-gap-matrix.md` — consolidated cross-SOP gap matrix for the VDC BIO
  AU-series (BIO 01–08): the always-present recurring gaps plus per-SOP outliers (LOQ
  errors in BIO 02/04, Calibration-Frequency "NA" unique to BIO 03, Critical Results vs
  Clinical Decision Values divergence pattern). Read BEFORE a new
  BIO audit to confirm known gaps quickly.
- `references/deep-audit-checklist.md` — 12-dimension structured checklist for the
  **second-pass deep audit**: section map, cross-reference validation, vague language
  scan, pre/post-analytical checklists, QC detail, calibration detail, safety, document
  control, numerical consistency, operational workflow gaps, and orphan references.
  Produced 9 additional findings when applied to VDC BIO 01.

