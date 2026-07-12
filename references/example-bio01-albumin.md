# Worked example: VDC BIO 01 — Albumin (BCG method)

Full audit with Exact Suggested Changes. Use as a template for other SOP audits.

## Document

**VDC BIO 01** — *Albumin including Globulins, A/G Ratio and Serum Ascitic Albumin*
- Version 1.0, Issue Date 07.08.2023, Copy 02, 13 pages
- Instrument: Beckman Coulter AU 5800 / AU 680 / AU 5811
- Method: Bromocresol Green (BCG), bi-chromatic 600/800 nm
- Department: Biochemistry | Category: SOP
- Source PDF: `zoho_pdfs/.../Biochemistry SOPs/AU Series/VDC BIO 01 - Albumin.pdf`
- Chunks retrieved: 59 of 59 (full dump, not top-k)

## What's already present (strengths)

| Item | Detail | Chunk ID |
|---|---|---|
| Principle / method | BCG, 600/800 nm, pH 4.2 | cid 12-13 |
| Reference interval (adult) | 3.5–5.2 g/dL | cid 44-47 |
| Paediatric reference | Newborn 2.8–4.4 g/dL | cid 47 |
| Globulins / A:G ratio | 1.8–3.6 / 0.8–2.0 | cid 47 |
| Critical values | <1.7 / >6.8 g/dL | cid 47 |
| Clinical decision values | 2.0, 3.5, 5.2 g/dL | cid 47 |
| AMR | 1.5–6.0 g/dL | cid 47 |
| LOQ / LOD | 1.5 / 0.7 g/dL | cid 47 |
| %CV / MU | 5.7 / 11.2 | cid 47 |
| Calibrator traceability | IFCC CRM 470 | cid 22 |
| Sample stability | Ambient 7 d / 4°C 30 d / body fluid: process immediately | cid 16-17 |
| Reagent on-board stability | 90 days | cid 22 |
| Interference limits | Icterus ≤40 mg/dL, Hb ≤4.5 g/L, lipid ≤800 mg/dL | cid 44 |
| IQC / EQA | 2 levels; MSP 18 (IQC), MSP 19 (EQA/PT), RIQAS monthly | cid 33, 38 |
| Sample rejection criteria | 9 criteria listed with contact/clarification workflow | cid 17-18, 20-21 |
| Equipment | AU 5800 / AU 680 / AU 5811 | cid 21 |
| SAAG calculation | Serum Albumin − Ascitic Albumin | cid 49 |
| Clinical interpretations | High/low causes listed | cid 49 |

## Findings with Exact Suggested Changes

### Finding 1 — TAT missing (High / Operational-Compliance)

**Evidence:** 0 of 59 chunks define a turnaround time. All 15 "tat" hits were the footer "Reviewed & Issued by" artifact.

**Problem:** ISO 15189:2022 §7.3.4 / NABL-112 require a stated TAT for each examination procedure. None exists.

**Exact Suggested Change:**
> _Insert a new sub-section after 4.9:_
>
> **4.9.5 Turnaround Time (TAT)**
> | Sample Type | Routine TAT | Urgent (STAT) TAT |
> |---|---|---|
> | Serum Albumin | X hours from sample receipt | Y hours from sample receipt |
> | Body Fluid Albumin | X hours from sample receipt | Y hours from sample receipt |
>
> All TATs are calculated from the time of sample receipt in the laboratory to the time of verified result release. Record TAT exceptions in the monthly TAT log per VDC/MSP/XX. TAT performance is reviewed quarterly by the Section Head.

**Benefit:** Direct compliance with ISO 15189:2022 §7.3.4; measurable SLA for clinicians.
**Confidence:** High (confirmed absent in full 59-chunk dump).

---

### Finding 2 — No calibration frequency (High / Quality-Traceability)

**Evidence:** Chunks 26, 32-33 describe how to perform calibration and when to re-calibrate (after maintenance/repair/failure), but no routine frequency is stated.

**Problem:** Event-triggered re-calibration alone is insufficient for accreditation. A minimum cadence (daily/per-shift/per-lot) must be documented.

**Exact Suggested Change:**
> _Insert after the first paragraph of 4.7 (Calibration):_
>
> **Calibration Frequency:** Calibration shall be performed at minimum:
> - With each new reagent lot number
> - After each preventive maintenance or critical-part replacement
> - After any major hardware/software upgrade
> - When IQC results indicate a systematic shift (per Westgard rules)
>
> A calibration verification (2-level QC) shall be performed at the start of each analytical shift. Calibration status (pass/fail) shall be recorded in the equipment maintenance log at each occurrence.

**Benefit:** Defensible calibration protocol for NABL assessment.
**Confidence:** High.

---

### Finding 3 — No method-validation reference (Medium-High / Compliance)

**Evidence:** Section 4.13 (cid 47): "Accuracy: NA", "Specificity: NA". No citation of a method-validation SOP or CLSI EP05/EP06.

**Problem:** ISO 15189:2022 §7.3.1 requires verification of performance claims. "NA" for accuracy without evidence is not acceptable.

**Exact Suggested Change:**
> _Replace the "Accuracy: NA" and "Specificity: NA" lines in §4.13 with:_
>
> | Parameter | Value | Source |
> |---|---|---|
> | Accuracy (bias) | Within ±X% of target (verified via CRM 470 trueness check) | VDC/MSP/XX — Method Verification |
> | Specificity | No significant cross-reactivity (≤X%) with: haemoglobin ≤4.5 g/L, bilirubin ≤40 mg/dL, intralipid ≤800 mg/dL | §4.10 of this SOP |
>
> **Method verification status:** This assay was verified per VDC/MSP/XX (Method Verification SOP). The verification study (CLSI EP05 precision, EP06 linearity, EP07 interference, trueness against CRM 470) is documented in Appendix A or referenced by file Lab-Alb-VER-001.

**Benefit:** Converts a compliance finding ("NA") into documented evidence.
**Confidence:** High.

---

### Finding 4 — No periodic-review clause (Medium / Documentation)

**Evidence:** No review validity period or expiry clause found in 59 chunks.

**Problem:** ISO 15189:2022 §7.2.2 requires documented review/revision cycle for examination procedures.

**Exact Suggested Change:**
> _Insert at the end of §6.0 (Appendices/Forms/WI's/Logs) or add as §7.0:_
>
> **7.0 Document Review and Validity**
> This SOP shall be reviewed at intervals not exceeding **2 years** from the date of issue or whenever a significant change occurs in the method, equipment, or regulatory requirements. The responsible reviewer is the Biochemistry Section Head. All changes require approval per VDC/MSP/XX (Document Control). The next scheduled review date is **[Issue Date + 2 years]**.

**Benefit:** Prevents SOP expiry/de facto obsolescence.
**Confidence:** High.

---

### Finding 5 — Cirrhosis limitation not flagged in reporting (Medium / Workflow)

**Evidence:** §4.18 (cid 53) notes: "Dye binding assays have decreased accuracy for patients with cirrhosis, possibly related to oxidized or other modified forms of albumin."

**Problem:** This known limitation is documented in the SOP body but not translated into a report flag/caveat. Without a reporting note, clinicians may be unaware that the BCG method overestimates albumin in cirrhosis.

**Exact Suggested Change:**
> _Add to the final paragraph of §4.17 (Clinical Interpretations) or create §4.17a:_
>
> **4.17a Reporting Note for Cirrhosis / Liver Disease**
> The BCG dye-binding method used in this assay may overestimate albumin concentration in patients with cirrhosis or severe liver disease (see §4.18). For such patients, consider: (a) adding a comment: *"Albumin measured by BCG method — results may be falsely elevated in liver disease"*; or (b) referring to an alternative method (e.g. serum protein electrophoresis) if clinically indicated.

**Benefit:** Mitigates misdiagnosis risk; demonstrates quality awareness.
**Confidence:** Medium (impact depends on patient population frequency).

---

### Finding 6 — MSP 29 risk-SOP not cited (Low / Traceability)

**Evidence:** References list (cid 56) includes NABL-112, kit insert, Tietz, RICOS, Westgard, and instrument SOPs — but no MSP 29 (Risk Assessment) or any validation SOP.

**Exact Suggested Change:**
> _Add to §5.0 (References):_
> - VDC/MSP/29 — Risk Assessment and Risk Management (if applicable to examination procedure risk analysis)
> - VDC/MSP/XX — Method Verification and Validation

**Benefit:** Completes the document tree.
**Confidence:** High.

---

## Priority Action Plan

| Horizon | Action |
|---|---|
| Immediate | 1. Define TAT (Finding 1). 2. Add calibration frequency (Finding 2). |
| Within 30 days | 3. Add method-verification evidence (Finding 3). 4. Add periodic-review clause (Finding 4). |
| Long term | 5. Add reporting flag for cirrhosis (Finding 5). 6. Complete references list (Finding 6). |

## Confidence Note

All findings are grounded in verbatim chunks from a full payload-filtered dump of all 59 chunks of VDC BIO 01 (doc_id `VDC BIO 01 - Albumin-12b752ae1ab3`) retrieved from the `vdc` Qdrant collection. Chunk IDs (cid) are cited per finding. No top-k/semantic subset was used. This was a single-document audit; no cross-SOP contradiction was found.
