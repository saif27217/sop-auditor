# SOP Structure Template — canonical 21-section framework

Single source of truth for "what sections must an SOP have". Used both to write new
SOPs and to walk an existing one. Clause numbers verified against
`iso-15189-certification` (ISO 15189:2022).

## Template

| # | Section | What it must contain | ISO 15189:2022 basis |
|---|---|---|---|
| 1 | **Purpose & Scope** | Intent AND limits (screening-only? confirmatory caveat?). Must agree with the specimen section (serum vs serum/plasma) | 7.3.1 a) + 7.3.6 |
| 2 | **Definitions / Abbreviations** | ALL body abbreviations defined (LCLL/LCLH, PSC, SC, lyophilized, aliquot, on-board, MTC …) | 7.3.6 b) |
| 3 | **Responsibility / Competency** | Who is authorised + training prerequisite. Assign critical-path roles: who calibrates, reports criticals, coordinates EQA, investigates QC failures, handles rejection | 6.2.2 + 6.2.3 |
| 4 | **Sample Type** | Matrix + container; verify vs kit insert | 7.2.4.2 b) |
| 5 | **Collection Timing** | Window (fasting? special timing?); flag "NA" fields contradicting text elsewhere | 7.2.4.2 c) + 7.2.4.4 b) |
| 6 | **Handling / Transport / Stability** | Temp, duration, freeze-thaw; verify vs kit storage clause | 7.2.5 + 7.2.7.3 |
| 7 | **Rejection Criteria** | MUST be matrix-appropriate, with quantitative thresholds from the kit (Hb mg/dL, TG mg/dL, bilirubin) not qualitative "grossly haemolysed". Separate administrative (billing) from specimen rejections | 7.2.6.1 b) + 7.2.6.2 |
| 8 | **Test Procedure (step-wise)** | Reproduce each step (volumes, incubation, read mode); line-by-line vs kit | 7.3.6 a) |
| 9 | **Calculation** | Formula vs kit; units consistent | 7.3.6 a) |
| 10 | **IQC / EQC** | Levels, frequency, Westgard rules, post-repair re-qualification, internal QC SOP (MSP/18); check for contradiction with a "Control: NA" field | 7.3.7.2 + 7.3.7.3 |
| 11 | **Calibration Frequency** | Beyond "when kit opened"; traceability; define "significant shift" concretely | 6.5.2 + 6.5.3 |
| 12 | **Performance** | Precision (%CV) & MU vs kit claim; Accuracy; Specificity (numeric or cross-ref); magnitudes ~2× kit are CAPA-level | 7.3.2 / 7.3.3 + 7.3.4 |
| 13 | **AMR / LOD / LOQ** | Internal consistency (LOD ≤ LOQ ≤ AMR) and vs kit sensitivity | 7.3.2 b) |
| 14 | **Reference Interval** | Sourced/locally validated, or fixed with no basis | 7.3.5 |
| 15 | **Limitations / Potential Variation** | ALL kit-cited cautions, not just one. Heterophilic/HAMA interference belongs in Interferences, not here, unless the SOP addresses interferences separately — reconcile | 5.3.3 a) + 6.6.5 |
| 16 | **Safety** | Generic GLP PLUS reagent-specific hazards (eye protection, first aid, SDS location, TCA H315, azide) | 6.6.5 |
| 17 | **Clinical Interpretation** | Lead with the PRIMARY indication (MTC for calcitonin, AMI for troponin) — do not bury it under secondaries. Include syndrome surveillance (MEN2), post-treatment monitoring, physiological causes, obstetric/benign conditions. Watch substrate-name drift | 5.3.3 b) |
| 18 | **Reporting / TAT / Critical Results** | TAT, urgent-report path, critical threshold (set explicitly, or "not established" with rationale — "NA" is not a policy), notification protocol, real review record | 7.2.6.1 f) + 7.4.1.3 + 7.4.1.6 |
| 19 | **References** | Kit insert + internal SOPs (MSP/14, MSP/20, MSP/29) + standards; no orphan citations | 7.3.6 c) |
| 20 | **Appendices / Forms** | Any forms, logs, or work instructions referenced | 7.3.6 c) |
| 21 | **Document Control** | Unique ID, approval before issue, revision status, review clause + owner, amendment log | 8.3.2 a)–e) |

## Key rules

1. **No bare "NA" fields** — content, or "not applicable, because …".
2. **Matrix-appropriate rejection criteria** — DBS must not copy serum-plasma boilerplate.
3. **Numeric interference limits** — "Hb ≤200 mg/dL, bilirubin ≤66 mg/dL, TG ≤500 mg/dL".
4. **Review clause must be explicit** — a "Reviewed & Issued by" footer is NOT a review
   clause; require "reviewed every N years or on change of method/reagent" plus an owner.
5. **Quantify specificity** — "highly specific" is not evidence; a cross-reactivity table is.
6. **Distinguish manufacturer from local performance** — the kit's CV is a claim; the SOP's
   CV must be the lab's validated value, and a large divergence is a finding, not a copy-paste.

## Assessment scale

| Rating | Meaning |
|---|---|
| **GOOD** | All 21 sections present with complete content |
| **OK** | All sections present, minor gaps (1–2 items PARTIAL) |
| **PARTIAL** | Missing 1–3 sections, or major gaps in critical sections (7, 10, 11, 18) |
| **GAP** | Missing ≥4 sections, or critical sections (7, 10, 11) incomplete |
| **REWRITE** | Wrong platform / method / matrix throughout — amend is futile |

## Worked results

Per-SOP scores and outliers: `au-series-gap-matrix.md`. Narrative templates:
`example-bio01-albumin.md` (full audit), `example-bio08-amylase.md` (minimal-gap SOP).