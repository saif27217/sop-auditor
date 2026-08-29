# AU-Series & Database-Wide Validation Finding (VDC BIO)

Condensed result bank from the 2026-07-15 database-wide audit of the `vdc`
collection (1,554 SOPs / 135,642 chunks). Use as quick context before a new
BIO audit, or to answer "does any SOP carry validation data?"

## The core question: is validation data for Accuracy/Specificity present ANYWHERE?

**Yes — but NOT in the AU-series clinical-chemistry family.**

- Of 1,554 SOPs, 343 mention Accuracy and 315 mention Specificity.
- **Accuracy real:** 29 SOPs (8.4% of those that state it). Concentrated in:
  serology/ELISA (CMV, Toxo, Rubella, HSV, HAV, HBsAg, HCV, H.Pylori,
  autoantibodies), molecular PCR (VDC MOL 18–38: ≥95%), FISH/cytogenetics
  (VDC CYT), flow cytometry (VDC FCM 02), HPLC HbA1c (BIO 139/175), troponin
  (BIO 84.1/169).
- **Specificity real:** 115 SOPs (36.5%). Same families — plus interference %
  (e.g. HBsAg 99.5%, Calprotectin 66.8%, CK-MB cross-reactivity CK-MM none /
  CK-BB 0.1%).
- **Both real:** only **17** SOPs.
- **CLSI protocol citations are rare even where data appears:** EP05 in 13
  docs, EP06 in 13, EP09 in 12, EP15 in only 2. So even "real" values often
  lack a documented validation *study* behind them.

## The AU-series (Beckman Coulter AU chemistry, 45 SOPs) — the family we audit

| Dimension | Finding across 45 SOPs |
|---|---|
| Accuracy | 0 real; 38 "NA"; 7 absent |
| Specificity | 2 real (BIO 36 RF 99%, BIO 49 Microalbumin 99%); 21 "Refer"; 19 "NA"; 3 absent |
| TAT | 0 present (100% missing) |
| Periodic-review clause | 0 present (100% missing) |
| CLSI/EP citation | 0 (100% missing) |
| MSP 29 / risk citation | 1 (BIO 15 only) |
| Critical/decision values | 8 stated, 37 "NA" |
| LOQ | 36 ok; 2 INVALID (BIO 02 ACE LOQ 0–150, BIO 04 ADA LOQ 0–200 — both LOQ<LOD); 7 absent |
| Calibration | 43 event-based (QC "calibration verification"); 1 defined (BIO 25); 1 "NA" (BIO 03, self-contradicts §4.8.1) |
| Reference intervals / interferences | 45 present (uniform strength) |

## Interpretation for future audits

- BIO 02/03/04 were NOT outliers — the whole AU-series shares the same gaps.
  One standardized TAT + periodic-review + Performance/Validation block,
  authored once and propagated to all 45, closes ~90 finding-instances.
- When a SINGLE BIO SOP is audited, expect: TAT absent, Accuracy "NA",
  Specificity "Refer Cl. 4.10" (an interference section, not a specificity
  statement), no review clause, no CLSI/EP citation. Confirm with a full dump
  (top-k hides the "Potential Variability/NA" and calibration clauses).
- LOQ transcription errors (LOQ < LOD, or LOQ > AMR) are the most common
  concrete numeric defect — always sanity-check LOQ ≥ LOD and LOQ ≈ lower AMR.
- Duplicate versioned copies exist for some analytes (e.g. BIO 32 Lipase,
  BIO 41 Total Bile Acid appear twice) — dedupe by clean name in reports.

## Reusable scan pipeline (see scripts/)

1. `scripts/dump_all_collection.py --collection vdc --out all_vdc_chunks.jsonl`
   → run in BACKGROUND (large; ~135k chunks).
2. `scripts/scan_validation_deficiencies.py all_vdc_chunks.jsonl --family "au series"`
   → emits per-SOP matrix + aggregate JSON.
3. Build the consolidated Google Doc from the matrix (one table per
   UPDATE_DOCUMENT_SECTION_MARKDOWN call — see Pitfall #3).
