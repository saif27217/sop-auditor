# Worked example: VDC BIO 02 — ACE (FAPGG method)

Full audit with Exact Suggested Changes. Use as a second template (the first is
`example-bio01-albumin.md`). Key difference from Albumin: ACE **does** define a
Calibration Frequency (§4.7) — but it has a unique LOQ transcription error.

## Document

**VDC BIO 02** — Angiotensin Converting Enzyme (ACE) by Beckman Coulter AU Series
- Version 1.0, Issue Date 07.08.2023, Copy 02, 11 pp
- Instrument: AU 5800 / 680 / 5811
- Method: FAPGG spectrophotometric, 340 nm
- Department: Biochemistry | Category: SOP
- Source PDF: `zoho_pdfs/.../Biochemistry SOPs/AU Series/VDC BIO 02 - ACE by AU Series Version No. 1.0.pdf`
- Chunks retrieved: 48 of 48 (full dump, not top-k)

## What's already present (strengths)

| Item | Detail | Chunk ID |
|---|---|---|
| Principle / method | FAPGG →(ACE)→ FAP + GG, decrease in A340nm ∝ activity | cid 13 |
| Sample | Serum; stable 2–8°C 1 mo, −20°C 6 mo | cid 13, 16 |
| Reference interval | 12–68 U/L | cid 40 |
| Performance | %CV 7.1; MU 13.9; AMR 0–150; LOD 5; Sensitivity 5 | cid 40-41 |
| **Calibration Frequency** | Defined §4.7: on lot change / shift in controls / PM / critical-part replacement | cid 27 |
| Interferences | Hb ≤12.5 mg/dL, intralipid ≤150 mg/dL, bilirubin ≤50 µmol/L, H-Val-Trp ≤5 µmol/L, EDTA ≤300 µmol/L | cid 38, 40 |
| QC | 2 levels; MSP 18 (IQC), MSP 19 (EQA/PT); RIQAS monthly | cid 30, 33 |
| Sample rejection | 9 criteria + compromised-sample workflow + rejection log | cid 16-18, 20-21 |

## Findings with Exact Suggested Changes

### Finding 1 — TAT missing (High)
**Evidence:** 0/48 chunks define TAT; all 11 "tat" hits were the footer "Reviewed & Issued by" artifact.
**Exact Suggested Change:** Insert §4.9.5: "**Turnaround Time (TAT).** Routine serum ACE: X hours from sample receipt. Urgent (STAT): Y hours from sample receipt. TAT exceptions recorded in monthly TAT log per VDC/MSP/XX. Quarterly review by Section Head."

### Finding 2 — LOQ = 0–150 U/L is invalid (High)
**Evidence:** cid 40: "Limit of Quantitation (LOQ): 0 - 150 U/L" — identical to AMR and CRR; LOD is 5 U/L.
**Exact Suggested Change:** Replace "Limit of Quantitation (LOQ): 0 - 150 U/L" with the verified kit-insert LOQ (e.g. "LOQ: 5 U/L" if lower AMR bound is the quantifiable limit). Cross-check against Beckman Coulter AU ACE kit insert before publishing. A LOQ of 0 is analytically meaningless and contradicts LOD=5.

### Finding 3 — Accuracy: NA, no validation SOP (Medium-High)
**Evidence:** cid 40-41: "Accuracy: NA"; "Specificity: Refer Cl. 4.10". No CLSI EP05/EP06 cited.
**Exact Suggested Change:** Replace "Accuracy: NA" with "Accuracy (bias): within ±X% of target (verified via CRM trueness check per Method Verification SOP)". Replace "Specificity: Refer Cl. 4.10" with a quantitative statement (e.g. "No significant cross-reactivity ≤X% with haemoglobin ≤12.5 mg/dL, bilirubin ≤50 µmol/L — see §4.10"). Add: "Method verification per CLSI EP05/EP06, doc ref: Lab-ACE-VER-001."

### Finding 4 — No periodic-review clause (Medium)
**Exact Suggested Change:** Add §7.0: "**Document Review and Validity.** Reviewed ≤2 years from issue or on significant change. Responsible: Biochemistry Section Head. Changes approved per Document Control SOP. Next review: [Issue Date + 2 years]."

### Finding 5 — MSP 29 / validation SOP not cited (Low)
**Exact Suggested Change:** Add to §5.0: "VDC/MSP/29 — Risk Assessment and Risk Management" and "VDC/MSP/XX — Method Verification and Validation".

### Finding 6 — Critical/decision values blank (Low)
**Evidence:** cid 41: "Critical Results: NA", "Clinical decision values: NA".
**Exact Suggested Change:** Replace "NA" with an explicit note: "No critical/panic value established for serum ACE at this laboratory. Results are interpreted in clinical context per §4.17."

## Priority Action Plan

| Horizon | Actions |
|---|---|
| Immediate | 1. Define TAT (F1). 2. Correct LOQ value (F2) — verify vs kit insert. |
| Within 30 days | 3. Replace Accuracy/Specificity NA with validation evidence (F3). 4. Add review clause (F4). |
| Long term | 5. Update references (F5). 6. Document the no-critical-value decision (F6). |

## Confidence Note

Full payload-filtered dump of all 48 chunks of VDC BIO 02 (doc_id `VDC BIO 02 - ACE by AU Series Version No. 1.0-b93750ca73eb`) from `vdc`. Chunk IDs cited. Single-doc audit; no cross-SOP contradiction. Unlike Albumin, this SOP defines a calibration frequency (§4.7).
