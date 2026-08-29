# Worked example: VDC BIO 04 — ADA (Peroxidase method)

Companion to the BIO 02 (ACE) and BIO 03 (ACP) worked audits. Dumped **53/53 chunks** from `vdc` (doc_id `VDC BIO 04 -  ADA by AU Series  Version No. 1.0`). Use as a third template for the AU-series audit pattern.

## Document

- VDC BIO 04 — Adenosine Deaminase (ADA), Beckman Coulter AU 680, Peroxidase method
- Version 1.0, Issue 07.08.2023, Copy 02, 11 pp; Biochem; SOP
- Chunks retrieved: 53/53 (full dump, not top-k)

## Strengths (what it does right)

| Item | Detail | § |
|---|---|---|
| Calibration Frequency | Defined §4.7 (lot change / shift in controls / PM / critical-part replacement) | §4.7 |
| EQA | Half-yearly ILC with NABL lab, VDC/MSP/19 | §4.8.2 |
| Interferences | Hb ≤800 mg/dL, intralipid ≤1000 mg/dL, ascorbic acid ≤50 mg/dL — no interference | §4.10 |
| Reference intervals | Serum/plasma 4–20; body fluids 0–40; CSF 0–5 U/L | §4.12 |
| Sample types | serum, plasma, body fluids, CSF | §1.0 |

## Findings (7)

1. **TAT missing (High)** — 0/53 chunks; all 9 "tat" hits are footer/word-substring ("format", "statement", "acceptance"); 0 contain "turnaround".
2. **LOQ = 0–200 U/L invalid (High)** — LOQ > AMR (0–20), contradicts LOD 4, overlaps reportable 0–2000. Same error class as BIO 02. Fix: verify vs G-cell ADA kit insert (expect ≈4 U/L, = LOD).
3. **Accuracy: NA / Specificity: Refer (Med-High)** — §4.10 already lists interference thresholds; the SOP should *convert* those into the specificity statement instead of deferring. Cite CLSI EP05/06 + method-verification SOP.
4. **No periodic-review clause (Medium)** — all 17 "review" hits are footer or QC/ILC-handling.
5. **MSP 29 / validation SOP not cited (Low)** — only MSP 18/19 (QC/EQA) cited in §5.0.
6. **Critical/decision values "NA" (Low)** — §4.14–4.15; replace with explicit "none established" statement.
7. **"Potential Sources of Variations: NA" (§4.18) (Low)** — understates real sample-type/dilution variation already described in §4.9.2/§4.10/§4.12.

## Contrast with siblings

| SOP | LOQ | Calibration Freq | "Potential Variab…: NA" | EQA |
|---|---|---|---|---|
| BIO 02 ACE | **0–150 (ERROR)** | defined | — | RIQAS monthly |
| BIO 03 ACP | **1.0 IU/L (correct =LOD)** | **"NA" (self-contradicts §4.8.1)** | Potential Variability: NA | RIQAS monthly |
| BIO 04 ADA | **0–200 (ERROR)** | defined | Potential Sources of Variations: NA | Half-yearly ILC |

## Verification gotcha observed this run

A `COMPOSIO_MULTI_EXECUTE_TOOL` call was rejected with `Expected object, received string at "tools[0]"` because `tool_slug` was placed as a *sibling* of the `tools` array. Correct shape: `tools: [{ arguments: {...}, tool_slug: "GOOGLEDOCS_..." }]`. Also: the doc was built + verified but the `display_url` was not pasted in the reply — the user had to ask "Share the link". Always surface `display_url` at the end.
