# Worked example: VDC BIO 03 — ACP (Alpha Naphthyl phosphate Kinetic Method)

Third worked audit in the series (after BIO 01 Albumin, BIO 02 ACE). Use as a
template for **labile-enzyme / kinetic-method SOPs**. Key contrasts with BIO 02:
LOQ is correct here, but it has a unique **Calibration-Frequency "NA" self-contradiction**
and a unique **"Potential Variability: NA"** field.

## Document

**VDC BIO 03** — Acid Phosphatase (ACP) by Beckman Coulter AU Series
- Version 1.0, Issue Date 07.08.2023, Copy 02, 11 pp
- Method: Alpha Naphthyl phosphate Kinetic, 405 nm
- Department: Biochemistry | Category: SOP
- Chunks retrieved: 52 of 52 (full dump, not top-k)

## Strengths (better than BIO 02)

| Item | Detail | Evidence |
|---|---|---|
| LOQ | 1.0 IU/L — equals LOD/Sensitivity (1.0 IU/L), = lower AMR bound. Internally consistent. | §4.13 |
| Sample stabilisation | Serum separated within 2 h, acetate buffer 20 µL/mL, stable 7 days 2-8°C; plasma rejected | §4.3.4-4.3.5 |
| Reference intervals | Total ACP ≤4.7 IU/L; Prostatic ACP ≤1.6 IU/L | §4.12 |
| Interferences | Reagent rejected if absorbance >0.500 at 405 nm | §4.10 |
| QC | 2 levels; controls run "as calibration verification"; RIQAS monthly; cites VDC/MSP/18 | §4.8 |

## Findings with Exact Suggested Changes

### Finding 1 — TAT missing (High)
**Evidence:** 0/52 chunks; all 18 "tat" hits are footer-word fragments or the "Reviewed & Issued by" footer; 0 "turnaround".
**Exact Suggested Change:** Add §4.9.6: *"Turnaround Time (TAT). Routine serum ACP within X hours of receipt. STAT within Y hours. Given ACP lability, STAT samples stabilised on receipt per §4.3.5. TAT exceptions in monthly TAT log (VDC/MSP/XX). Section Head reviews quarterly."*

### Finding 2 — Calibration Frequency "NA" self-contradicts §4.8.1 (High)
**Evidence:** §4.7 "Calibration Frequency: NA" vs §4.8.1 controls run "As calibration verification … new kit/lot; after PM; after major repairs." Analyzer needs a calibration factor (§4.16).
**Exact Suggested Change:** Replace *"4.7 Calibration Frequency: NA"* with *"4.7 Calibration Frequency. Calibrate per Accurex Biomedical kit insert: on each new reagent lot, after PM, and after critical-part/hardware/software change. Controls run as calibration verification per §4.8.1 and VDC/MSP/18."*

### Finding 3 — Accuracy "NA" / Specificity "Refer" (Medium-High)
**Exact Suggested Change:** Replace *"Accuracy: NA"* → *"Accuracy (bias): within ±X% of target, CRM trueness check per Method Verification SOP (VDC/MSP/XX; CLSI EP15/EP06)."* Replace *"Specificity: Refer Cl. 4.10"* → *"Specificity: No significant interference (≤X% bias); oxalate/fluoride anticoagulants inhibit ACP and cause turbidity (§4.3.4); reagent rejected if absorbance >0.500 at 405 nm (§4.10)."* Add *"Method verification per CLSI EP05/EP06; ref Lab-ACP-VER-001."*

### Finding 4 — No periodic-review clause (Medium)
**Exact Suggested Change:** Add §7.0 — *"Document Review and Validity. Reviewed at least every 2 years from issue or on significant change. Responsible: Biochemistry Section Head. Next review: [Issue Date + 2 years]."*

### Finding 5 — MSP 29 / validation SOP not cited (Low)
**Exact Suggested Change:** In §5.0 add *"VDC/MSP/29 — Risk Assessment"* and *"VDC/MSP/XX — Method Verification and Validation."*

### Finding 6 — Critical / decision values "NA" without rationale (Low)
**Exact Suggested Change:** Replace with *"No critical/panic value established for serum ACP. Results interpreted per §4.17."*

### Finding 7 — "Potential Variability: NA" (§4.18) (Low, unique to BIO 03)
**Evidence:** §4.18 bare "NA" despite ACP being highly labile (2 h separation, mandatory stabiliser, anticoagulant inhibition).
**Exact Suggested Change:** Replace *"4.18 Potential Variability: NA"* with *"4.18 Potential Variability. ACP highly labile: separate within 2 h and stabilise with acetate buffer (20 µL/mL, §4.3.5); unstabilised unreliable. Oxalate/fluoride inhibit and turbidify — plasma not acceptable (§4.3.4). Invalid if reagent absorbance >0.500 at 405 nm (§4.10)."*

## Priority Action Plan

| Horizon | Actions |
|---|---|
| Immediate | 1. Fix Calibration Frequency + §4.7/§4.8.1 contradiction (F2). 2. Define TAT (F1). |
| 30 days | 3. Accuracy/Specificity evidence (F3). 4. Review clause (F4). 5. Potential Variability (F7). |
| Long term | 6. MSP 29 cite (F5). 7. No-critical-value note (F6). |

## Confidence Note
Full payload-filtered dump of all 52 chunks of VDC BIO 03 (doc_id `VDC BIO 03 - ACP BY AU Series  Version No. 1.0`) from `vdc`. Single-doc audit; no cross-SOP contradiction. Unlike BIO 02, LOQ is correct.
