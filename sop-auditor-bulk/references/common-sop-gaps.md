# Common SOP gaps — pre-flight checklist

Scan every SOP against these dimensions before writing findings. These omissions
recur across the VDC BIO AU-series and are usually the real findings, not contradictions.

## Checklist

| # | Dimension | What to check | ISO 15189 / NABL basis |
|---|---|---|---|
| 1 | **TAT** | Does the SOP define a turnaround time for routine and urgent samples? | ISO 15189:2022 7.3.4; NABL-112 § |
| 2 | **Calibration frequency** | Is there a stated cadence (daily/per-shift/per-lot) or only event-triggered? | ISO 15189:2022 5.3.1.4; NABL-112 § Equipment |
| 3 | **Method validation / verification** | Does the SOP cite CLSI EP05 (precision), EP06 (linearity), or a validation SOP? Is Accuracy / Specificity stated (not "NA")? | ISO 15189:2022 7.3.1; NABL-112 § Method Validation |
| 4 | **Periodic review** | Is there a review clause (e.g. "every 2 years or on change") with a responsible owner? | ISO 15189:2022 7.2.2; NABL-112 § Document Control |
| 5 | **Risk-SOP citation** | Does the SOP reference the organisational risk-assessment SOP (e.g. MSP 29)? | ISO 15189:2022 10.1; NABL-112 § Risk Assessment |
| 6 | **Known limitations in reporting** | If the method has a known limitation (e.g. dye-binding in cirrhosis), is there a reporting caveat or comment flag? | ISO 15189:2022 7.3.6 |
| 7 | **Critical results** | Are critical/panic values defined with notification protocol? | ISO 15189:2022 7.4.2; NABL-112 § |
| 8 | **Reagent / sample stability** | Are stability conditions stated (unopened, on-board, after reconstitution)? | NABL-112 § Reagents |
| 9 | **Traceability of calibrator** | Is the calibrator traceable to a reference material / higher-order method? | ISO 15189:2022 5.3.1.5 |
| 10 | **Interference limits** | Are haemolysis/icterus/lipaemia thresholds given with the analysis method? | NABL-112 § |

## Recurring gotchas seen in live VDC BIO AU-series audits

These turned up repeatedly and are the real findings, not contradictions. Check each explicitly:

- **Calibration Frequency declared "NA" that self-contradicts the SOP.** VDC BIO 03 §4.7 says "Calibration Frequency: NA" yet §4.8.1 runs controls "As calibration verification … To qualify reagents on opening new kit/lot; After preventive maintenance; After major repairs." An accredited quantitative assay cannot have "no calibration" — this is a self-contradiction (High) and non-compliant with ISO 15189:2022 5.3.1.4. Fix: state the manufacturer cadence (kit insert) and reconcile with the verification clause.
- **Bare "NA" fields.** `Accuracy: NA`, `Specificity: Refer Cl. x`, `Potential Variability: NA`, `Critical Results: NA`, `Clinical decision values: NA`. "NA" with no rationale is not an explicit policy. Replace with a quantitative statement or an explicit "none established" note. (VDC BIO 02 and 03 both exhibit this.)
- **LOQ transcription error.** VDC BIO 02 lists `LOQ: 0 - 150 U/L` (identical to AMR/CRR) while `LOD: 5 U/L` — a LOQ of 0 is invalid. VDC BIO 03 correctly sets `LOQ: 1.0 IU/L` (= LOD). Always sanity-check LOQ ≥ LOD and LOQ = lower AMR bound.
- **TAT always absent — and the "tat" substring is a trap.** Every "tat" hit is either a footer-word fragment ("for**mat**", "state**ment**", "accep**t**ance criteria", "interpre**t**ation") or the document footer "Reviewed & Issued by" artifact. Grep for the word "turnaround" specifically; if it returns 0, TAT is genuinely missing (High).
- **Footer "review" artifact.** All "review" hits are either the footer or "review environmental conditions / review recent events" inside QC-failure handling — none are a document-review cadence. A periodic-review clause is therefore genuinely absent unless you find an explicit "review every N years" statement.
