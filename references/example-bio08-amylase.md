# Worked example: VDC BIO 08 — Amylase (AU Series, chromogenic)

Full audit delivered as Google Doc `1amFzPDcK-1nbhAnhhj4sn1JZTHQHb0KJbCW0QtzcrBo`. This is the **strongest SOP in the AU-series so far** — use as a reference for the "minimal-gap" pattern when an SOP has only the 5 recurring gaps and shows proper documentation of dilution ranges.

## Document

- VDC BIO 08 — Amylase (including fluids), Beckman Coulter AU Series
- Version 1.0, Issue 07.08.2023, 11 pp
- Chunks: 61/61 (full dump, not top-k)

## Strengths (best-in-series)

| Item | Detail | § |
|---|---|---|
| **LOQ** | 10 U/L (single value, CORRECT = lower AMR bound) | §4.13 |
| **LOD** | 1 U/L | §4.13 |
| **AMR** | 10 – 2000 U/L | §4.13 |
| **CRR** | **10 – 20000 U/L** — properly > AMR (dilution validated) | §4.13 ✅ **First in series** |
| **Precision (%CV)** | 6.7 | §4.13 |
| **Measurement of Uncertainty** | 13.2 | §4.13 |
| **Clinical Decision Values** | **50, 120 and 200 U/L** (defined) | §4.15 ✅ |
| **Calibration Frequency** | Defined §4.7 (event-triggered) | §4.7 |
| **Interferences** | Icterus <10% up to 20 mg/dL; Haemolysis <10% up to 2.5 g/L; Lipemia <5% up to 1000 mg/dL | §4.10 ✅ All 3 quantified |
| **EQA** | RIQAS monthly + Fluids Amylase ILC | §4.8.2 |
| **Reference intervals** | Serum 28–100 U/L; Fluids NA | §4.12 |
| **§4.18** | Populated — macroamylasemia | ✅ Not NA |
| **IQC** | Per VDC/MSP/18 | §5.0 |

## Findings (5 recurring, same as BIO 05/06)

1. **TAT missing (High)** — 0 "turnaround" in 61 chunks.
2. **Accuracy: NA / Specificity: NA (Med-High)** — both "NA" despite interference data in §4.10.
3. **No periodic-review clause (Medium)** — only QC-failure "review" hits.
4. **MSP 29 / validation SOP not cited (Low)** — only MSP 18/19.
5. **Critical Results: NA (Low, partial)** — §4.14 is "NA" but §4.15 has clinical decision values.

## Key contrast with siblings

- **CRR > AMR**: BIO 08 is the **first SOP in the series** to properly distinguish CRR (20000) from AMR (2000), proving dilutions are validated for fluid amylase.
- **LOQ format**: Single value (10 U/L), not a range — correct per CLSI EP17. Contrast with BIO 02/04/07 which express LOQ as a range equal to AMR.
- **All 8 performance fields populated**: LOQ, LOD, AMR, CRR, %CV, MU, Accuracy (flagged NA), Specificity (flagged NA). Same coverage as BIO 05/06 but with cleaner CRR documentation.
- **§4.18**: Populated with macroamylasemia content — not "NA" (unlike BIO 03/04/07).

## Verification gotcha (this session)

When calling `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT` via direct MCP JSON-RPC, the response key is **`plain_text`** (underscore), not `plaintext`. Using `plaintext` returns empty string. The display URL was at `response.data.display_url`.

## Document URL

https://docs.google.com/document/d/1amFzPDcK-1nbhAnhhj4sn1JZTHQHb0KJbCW0QtzcrBo/edit
