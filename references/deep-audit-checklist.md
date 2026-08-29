# Deep Audit Checklist — Beyond the Recurring Gaps

Use after the standard recurring-gap scan (Accuracy/Specificity/TAT/review/CLSI/
calibration/LOQ/MSP29). This checklist targets **structural, operational, quality,
and workflow** issues that the standard scan misses.

## 1. Section Map — are all required sections present?

Extract every numbered section from the full text. Compare against ISO 15189:2022
requirements:

| § | Required section |
|---|---|
| 4.1 | Introduction / Scope |
| 4.2 | Principle / Method |
| 4.3 | Sample Collection & Handling |
| 4.3.x | Fasting prep, tube type, stability, transport, rejection |
| 4.4 | Equipment |
| 4.5 | Reagents / Calibrators |
| 4.6 | Additional requirements |
| 4.7 | Calibration |
| 4.8 | Quality Control |
| 4.9 | Procedure |
| 4.10 | Interferences |
| 4.11 | Troubleshooting / Limitations |
| 4.12 | Reference Intervals |
| 4.13 | Performance Characteristics |
| 4.14 | Critical Results |
| 4.15 | Clinical Decision Values |
| 4.16 | Calculations |
| 4.17 | Clinical Interpretation |
| 4.18 | Potential Sources of Variation |
| 4.19 | Safety Precautions |
| 5.0 | References |
| 6.0 | Appendices / Forms |
| 7.0 | Review / Validity (often MISSING) |

**Method:** regex `^((?:\d\.)+\d+)\s+(.*)` over concatenated chunk_text.

## 2. Internal Cross-Reference Validation

Scan the full text for references to other sections:
```
(?:§|Cl\.|clause|section|per|as per|refer)\s*(\d+\.\d+)
```

Zero cross-references = sections exist in isolation — poor navigation.

**Common missing links (found in VDC BIO 01):**
- §4.13 Specificity → §4.10 Interferences
- §4.18 (limitation) → §4.17 Clinical Interpretation
- §4.16 Calculations → Total Protein SOP (for globulin/A:G)
- §4.9 Procedure → §4.4 Equipment

## 3. Vague / Ambiguous Language Scan

Search for these phrases. Each represents a commitment without a trigger:

| Phrase | Problem | Fix |
|---|---|---|
| "as required" | Unspecified condition | Replace with specific trigger |
| "as applicable" | Unspecified applicability | Define the condition |
| "if needed" / "if necessary" | No triggering condition | State what constitutes need |
| "appropriate" / "sufficient" / "adequate" | No defined criteria | Add acceptance criteria |
| "soon as possible" | No time bound | Replace with X h / Y min |
| "periodically" | No frequency | State the interval |
| "etc." | Incomplete list | Complete or use "including but not limited to" |

## 4. Pre-Analytical Checklist

| Item | Severity if missing |
|---|---|
| Fasting requirement stated (even if "not required") | Medium |
| Tube type — specific brand/code, not just colour | Medium |
| Anticoagulant specified | High |
| Centrifugation — speed (g/RCF), time, temperature | Medium |
| Stability — ambient, refrigerated, frozen, per matrix | High |
| Transport — temperature, time, packaging | Medium |
| Rejection criteria — ≥5 specific criteria + workflow | High |
| Body fluid protocol — separate handling if applicable | Medium |

## 5. Post-Analytical Checklist

| Item | Severity if missing |
|---|---|
| TAT defined — X h routine / Y h STAT | High |
| Auto-commenting rules | Medium |
| Delta check criteria | Medium |
| Panic value notification workflow | High |
| Dilution protocol for >AMR results | Medium |
| Result recall procedure | Medium |
| Repeat criteria — when to repeat vs accept | Medium |

## 6. QC Detail Checklist

| Item | Severity if missing |
|---|---|
| LJ charts required or referenced | Medium |
| Target values (mean/SD) per control level | Medium |
| Westgard rules — which rules applied | Medium |
| OOS procedure — structured investigation | Medium |
| QC frequency — per shift / per day / per run | Medium |
| EQA program — named program, frequency | Medium |

## 7. Calibration Detail Checklist

| Item | Severity if missing |
|---|---|
| Frequency — time-based + event-triggered (not just event) | High |
| Traceability — CRM or reference method stated | Medium |
| Acceptance criteria — what constitutes a pass | Medium |
| Cal failure procedure — follow-up actions | Medium |

## 8. Safety Checklist

| Item | Severity if missing |
|---|---|
| Biosafety level explicitly stated | Medium |
| PPE requirements — gloves, lab coat, eye protection | Medium |
| Spill procedure — clean-up protocol | Medium |
| Waste disposal — BMW category, method | Medium |

## 9. Document Control Checklist

| Item | Severity if missing |
|---|---|
| Amendment log — records of changes with dates | Medium |
| Version number — current and consistent | Medium |
| Review/expiry clause (§7.0 or equivalent) | Medium |
| Author/approver signatures present | Low |

## 10. Numerical Consistency Checks

- LOQ ≥ LOD? (CLSI EP17)
- AMR interval logical? Lower ≤ upper bound
- LOQ ≤ AMR lower bound? (should be equal or lower)
- CRR ≥ AMR? (CRR should include or exceed AMR)
- Reference interval within AMR?
- Critical result threshold within AMR?
- Units consistent across §4.3, §4.12, §4.13, §4.14–15?

## 11. Operational Workflow Gaps

For SOPs with derived calculations (ratios, gradients, indices, clearances):

| Example: BIO 01 SAAG | Status |
|---|---|
| Formula explicitly stated? | ✅ |
| Input tests referenced? | ❌ No link to Total Protein SOP |
| Single-sample requirement? | ❌ Not stated |
| Reporting format? | ❌ Not described |
| QC on derived value? | ❌ Not addressed |
| TAT for paired samples? | ❌ Not defined |

## 12. Second-Pass Deep Items

- **Duplicate sections** — same section number in multiple chunks
- **Contradictory statements** — same concept described differently
- **Empty fields** — fields set to "NA" that should have content
- **Placeholder language** — "Refer to manual" without specifying which
- **Orphan references** — SOPs/forms referenced but not in doc tree

---

## Usage

After running the standard recurring-gap scan, execute each section above
against the full concatenated dump. Each item produces either a finding
or a confirmation. Items that fail should get severity per the table.

For VDC BIO 01 (2026-07-16), this checklist produced 9 additional findings
beyond the 6 standard recurring gaps: zero cross-references, QC detail gaps,
empty amendment log, missing SAAG workflow, pre-analytical gaps, vague
language, safety gaps, and CRR formalisation.
