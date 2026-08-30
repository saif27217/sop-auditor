# SOP Audit Results — Kit-Insert Cross-Audits & Full-Lifecycle Series

These audits compare VDC SOPs (Qdrant `vdc` collection) against the manufacturer
**kit insert** for the test, and apply the **Full-Lifecycle Section Audit** framework
(18 sections, see `references/full-lifecycle-scorecard-template.md`).

## Deliverables (verified Google Docs)

| SOP | Title | Kit insert | Audit Doc | Key findings |
|---|---|---|---|---|
| BIO 169 | Troponin T (qualitative, POC) | Roche TROPT Sensitive | https://docs.google.com/document/d/1sVeG1ykfO5yxZmdfqQbT4zDKiBDOL4iorIjFWp-tuEU/edit | F1 Critical: SOP EDTA-only vs kit heparin/EDTA; F3 storage 15–25°C vs kit 2–8°C; F2 volume 4mL vs 150µL; F4 omits Roche control |
| BIO 156 | Newborn Screening G-6-PD (14pg) | ZENTECH Neonatal G-6PD | https://docs.google.com/document/d/1mQfkMC-qWmmIupLFgxLFRueYty8UqH0dBqjbzPPGr4s/edit | F1 High: Precision 29.35 / MU 57.526 no units; F2 ref interval "U/bHb" should be U/g Hb; controls fields blank |
| BIO 147 | Newborn Screening Galactose | ZENTECH Total Galactose | https://docs.google.com/document/d/1vlJmENywiFdaTqYM2CZMCgIbfzdpZNHFVH_0T8Gh3aU/edit | **Full-lifecycle** — F1 precision 19.4% vs kit 4.3–8.8%; F2 unsourced 5–27 ref range; F6 "timing NA" contradicts Day 3–5; F7 serum-plasma rejection boilerplate on DBS; F10 limitations omit 4 kit cautions; F11 missing TCA H315 hazard |
| BIO 146 | Newborn Screening G-6-PD (DBS) | ZENTECH E-IX-MZ-005 | https://docs.google.com/document/d/1VXx3YktNnQI6aEhScNRj89_cj7gUhZ7sFJUagtSLRZE/edit | **Best SOP in series** — 0 High, 4 Med, 2 Low. Matches kit perfectly (15µl+75µl+75µL transfer, 550nm kinetic + 405nm endpoint, 3 controls N/I/D). Gaps: Critical Values NA (F1), NaN3 plumbing warning missing (F2), TAT missing (F3) |
| BIO 166 | Troponin-T (qualitative, POC) v2 | Roche TROPT Sensitive | https://docs.google.com/document/d/168cT6_bK4UwUlKcmbzjHJY4HzEZcOwAqj5ZOOqaPCJI/edit | **Cleanest SOP in series** — 0 High, 2 Med, 3 Low. Fixes all BIO 169 errors (EDTA+heparin ✓, 150µL ✓, RT storage ✓, Critical Values defined). Reference section STRONG (Roche insert + MSP/14 + MSP/20 well-traced). Grammar: 1 spelling inconsistency (hemolysis vs haemolysed); clinical accuracy verified ✓ |

## Methodology notes

- BIO 169 / BIO 156 / BIO 147 use the **kit-insert cross-check pattern**: pull the
  manufacturer insert (native Google Doc) + dump the SOP chunks from Qdrant, then diff
  every parameter (sample type, volumes, wavelength, controls, storage, limitations,
  performance) line-by-line.
- BIO 147 was re-run through the **Full-Lifecycle Section Audit** after the user noted
  the default 6–7 analytical sections were too narrow. The re-audit added F6–F12
  (Purpose/Sample/Procedure/Limitations/Rejection/Safety/Clinical-Interpretation gaps).
- Legacy `.doc` SOPs (e.g. BIO 147) are Drive file IDs, not native Docs — extract via
  `GOOGLEDRIVE_DOWNLOAD_FILE` → local OLE2 text recovery (CP1252 WordDocument stream at
  `fcMin`, see `scripts/extract_doc_text.py` logic), then audit.

## Skill updates shipped with this batch

- `SKILL.md`: added **Full-Lifecycle Section Audit** mandatory 18-section walk + DBS
  rejection-boilerplate trap + "NA vs text" contradiction trap.
- `references/full-lifecycle-scorecard-template.md`: new scorecard table.
- Copied `au-series-*`, `deep-audit-checklist`, `example-bio02/03/04/08` references into
  the repo for completeness.
