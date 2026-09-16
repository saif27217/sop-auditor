# Worked example: VDC BIO 08 — Amylase (AU Series, chromogenic)

Full audit delivered as Google Doc `17Wtbf5z4P1fMHF3fDXwt3vox3AQ0PTUx1NO5Zx7v-10`. This is the **strongest SOP in the AU-series** — use as a reference for the "minimal-gap" pattern when an SOP has only recurring gaps and shows proper documentation of dilution ranges.

## Document

- VDC BIO 08 — Amylase (including fluids), Beckman Coulter AU Series
- Version 1.0, Issue 07.08.2023, 11 pp
- Chunks: 61/61 (full dump, not top-k)
- IFU Code: BLOSR6x06.01

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
| **Calibration Frequency** | Defined §4.7 (every 30 days) | §4.7 ✅ |
| **Interferences** | Icterus <10% up to 20 mg/dL; Haemolysis <10% up to 2.5 g/L; Lipemia <5% up to 1000 mg/dL | §4.10 ✅ All 3 quantified |
| **EQA** | RIQAS monthly + Fluids Amylase ILC | §4.8.2 |
| **Reference intervals** | Serum 28–100 U/L; Fluids NA | §4.12 |
| **§4.18** | Populated — macroamylasemia | ✅ Not NA |
| **IQC** | Per VDC/MSP/18 | §5.0 |

## Findings (9 total)

### High Severity
1. **TAT missing** — 0 "turnaround" hits in 61 chunks. ISO 15189:2022 §7.2.6.1 f) + §7.4.1.7 require defined TAT for routine and STAT samples. Amylase is often STAT in acute abdominal pain.
   - **Exact Suggested Change:** Add section 4.xx: "Routine amylase results shall be reported within 4 hours of sample receipt. STAT (urgent) amylase results shall be reported within 1 hour of sample receipt."

2. **Periodic review clause absent** — grep for "review every", "shall be reviewed", "next review" returns 0 hits. Footer artifact "Reviewed & Issued by" is not a periodic-review clause (Pitfall #8).
   - **Exact Suggested Change:** Add to §5.0: "This SOP shall be reviewed every 2 years or upon significant method/equipment change, whichever comes first. Review responsibility: HOD Biochemistry."

### Medium Severity
3. **Accuracy marked "NA"** — ISO 15189:2022 §7.3.2 requires documented accuracy or explicit "not established" with justification.
   - **Exact Suggested Change:** "Accuracy: Not established by laboratory — manufacturer validation per IFU BLOSR6x06.01. Method comparison data available upon request."

4. **Specificity marked "NA"** — Interference thresholds exist in §4.10 but specificity field is NA.
   - **Exact Suggested Change:** "Specificity: Haemolysis (>0.5 g/L Hb), lipemia, icterus may interfere — see IFU BLOSR6x06.01 for thresholds. Macroamylasemia may cause discrepant results."

5. **Reference interval not stated** — Clinical Decision Values (50, 120, 200 U/L) defined but no reference range. Beckman IFU states 22-80 U/L for serum/plasma.
   - **Exact Suggested Change:** "Reference Interval (Serum/Plasma): 22 – 80 U/L (0.36 – 1.33 µkat/L). Source: Beckman Coulter IFU BLOSR6x06.01; laboratory verification pending."

6. **Risk-SOP citation absent** — References list NABL 112, Wallach's, RICOS, Beckman IFU, Tietz — but no MSP 29 (Risk Assessment SOP).
   - **Exact Suggested Change:** Add to §5.0: "• VDC/MSP/29 - Risk Assessment and Risk Management SOP"

### Low Severity
7. **Critical Results vs. Clinical Decision Values — clarification needed** — §4.14 states "Critical Results: NA" while §4.15 defines CDVs (50, 120, 200 U/L). These are distinct concepts; CDVs support diagnosis but don't require immediate notification.
   - **Exact Suggested Change:** "Critical Results: Not defined for amylase. Clinical Decision Values (50, 120, 200 U/L) support diagnostic interpretation but do not constitute critical results requiring immediate notification per VDC/MSP/20."

8. **Interference thresholds not explicitly stated in rejection criteria** — §4.3.7 lists "Grossly haemolysed specimens", "Highly lipemic specimens", "Highly icteric specimens" but no numeric thresholds.
   - **Exact Suggested Change:** Add to §4.3.7: "Interference Limits (per IFU BLOSR6x06.01): Haemolysis: >0.5 g/L Hb may interfere — reject or flag. Lipemia/Icterus: Check IFU for specific thresholds."

9. **LOD discrepancy vs. IFU** — SOP states "LOD / Sensitivity: 1 U/L" but Beckman IFU BLOSR6x06.01 states "Lowest detectable level (serum, AU600) = 2 U/L". May be lab-verified improvement or transcription error.
   - **Exact Suggested Change:** "Verify LOD claim against current IFU BLOSR6x06.01 revision. If laboratory-verified at 1 U/L, add: 'Laboratory-verified LOD: 1 U/L (per internal validation, date: ___).' If error, correct to '2 U/L' per IFU."

## Cross-SOP Contrast (AU-Series Context)

| Dimension | VDC BIO 08 (Amylase) | Series Average | Notes |
|---|---|---|---|
| TAT | **Absent** | Absent | Recurring gap across all BIO SOPs |
| Calibration Frequency | **Every 30 days** | Mixed (some "NA") | BIO 08 correctly states cadence |
| Precision (%CV) | **6.7%** | Variable | Strong performance data |
| MU | **13.2%** | Variable | Stated (rare in series) |
| Accuracy | **NA** | Mostly NA | Recurring gap |
| Specificity | **NA** | Mostly NA | Recurring gap |
| LOQ | **10 U/L** | Variable | Correctly ≥ LOD (1 U/L) |
| AMR | **10-2000 U/L** | Variable | Matches IFU linearity |
| CRR | **10-20000 U/L** | Variable | Proper dilution handling (CRR > AMR) |
| Critical Results | **NA** | Mixed | CDVs defined (50, 120, 200) |
| Reference Interval | **Absent** | Mostly absent | Recurring gap |
| Periodic Review | **Absent** | Absent | Recurring gap |
| Risk-SOP Citation | **Absent** | Mostly absent | Recurring gap |

## Priority Action Plan

### Immediate (Before Next Audit)
1. Add TAT clause (§4.xx) — ISO 15189 compliance
2. Add periodic review clause (§5.0 or new section) — ISO 15189 compliance
3. Clarify Critical Results vs. CDVs (§4.14) — eliminates confusion

### 30 Days
4. State reference interval (§4.13) — ISO 15189 §7.3.5
5. Add Accuracy/Specificity statements (§4.13) — replace "NA" with explicit policy
6. Add risk-SOP citation (§5.0) — ISO 15189 §5.6 / §8.5

### Long Term
7. Verify LOD claim (1 U/L vs. IFU 2 U/L) — document source
8. Add interference thresholds (§4.3.7) — NABL-112 compliance
9. Consider locally validating reference interval — strengthens ISO 15189 position

## Verification Gotcha (this session)

When calling `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT` via direct MCP JSON-RPC, the response key is **`plain_text`** (underscore), not `plaintext`. Using `plaintext` returns empty string. The display URL was at `response.data.display_url`.

## Document URL

https://docs.google.com/document/d/17Wtbf5z4P1fMHF3fDXwt3vox3AQ0PTUx1NO5Zx7v-10/edit
