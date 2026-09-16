# Common SOP gaps — pre-flight checklist

Scan every SOP against these dimensions before writing findings. These omissions
recur across the VDC BIO AU-series and are usually the real findings, not contradictions.

## Checklist

Clause numbers verified against `iso-15189-certification` (ISO 15189:2022, 192/192 clauses).

| # | Dimension | What to check | ISO 15189:2022 basis |
|---|---|---|---|
| 1 | **TAT** | Does the SOP define a turnaround time for routine and urgent samples? | 7.2.6.1 f) + 3.30 + 7.4.1.7 |
| 2 | **Calibration frequency** | Is there a stated cadence (daily/per-shift/per-lot) or only event-triggered? | 6.5.2 |
| 3 | **Method verification / validation** | Does the SOP cite CLSI EP05 (precision), EP06 (linearity), or a validation SOP? Is Accuracy / Specificity stated (not "NA")? | 7.3.2 (verify) / 7.3.3 (validate) |
| 4 | **Periodic review** | Is there a review clause (e.g. "every 2 years or on change") with a responsible owner? | 8.3.2 c) |
| 5 | **Risk-SOP citation** | Does the SOP reference the organisational risk-assessment SOP (e.g. MSP 29)? | 5.6 + 8.5 |
| 6 | **Known limitations in reporting** | If the method has a known limitation (e.g. dye-binding in cirrhosis), is there a reporting caveat or comment flag? | 5.3.3 a) + 6.6.5 |
| 7 | **Critical results** | Are critical/panic values defined with notification protocol? | 7.4.1.3 |
| 8 | **Reagent / sample stability** | Are stability conditions stated (unopened, on-board, after reconstitution)? | 6.6.2 + 7.2.7.3 |
| 9 | **Traceability of calibrator** | Is the calibrator traceable to a reference material / higher-order method? | 6.5.3 (+ ISO 17511) |
| 10 | **Interference limits** | Are haemolysis/icterus/lipaemia thresholds given, with numeric values? | 5.3.3 a) + 6.6.5 |
| 11 | **Document control compliance** | Unique ID, approval before issue, revision status tracked, obsolete docs identified | 8.3.2 a)–i) |
| 12 | **Rejection criteria matrix-appropriate** | DBS SOP must NOT list serum-plasma rejects (haemolysed/lipaemic/icteric) | 7.2.6.1 b) + 7.2.4.2 f) |
| 13 | **Personnel / authorisation** | Who is authorised to perform, review and release; competency recorded | 6.2.2 + 6.2.3 |
| 14 | **Safety — reagent-specific hazards** | GLP + H-codes for reagents (e.g. TCA H315, sodium azide plumbing warning) | 6.6.5 |
| 15 | **References completeness** | Kit insert + internal SOPs (MSP/14, MSP/20) + standards cited; no orphan citations | 7.3.6 + 8.3.1 |

## Multi-matrix note

A single analyte SOP claiming several matrices must state the validation basis for each.
Stability and rejection criteria differ per matrix — one blanket clause is a finding.

## Verification rule

Never hand-type a clause number into an audit. Look it up in
`iso-15189-certification/INDEX.tsv` (or grep its `chapters/`) and quote the verified
number. Hand-typed numbers drift into the superseded 2012 numbering, which is exactly
what this checklist previously carried (5.3.1.4, 5.3.1.5, 10.1 — none exist in 2022).