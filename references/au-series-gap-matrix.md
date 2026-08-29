# VDC BIO AU-series — recurring gap matrix

Consolidated across VDC BIO 01 (Albumin), 02 (ACE), 03 (ACP), 04 (ADA), 05 (ALP), and 06 (ALT) audits. **Read this BEFORE a new BIO audit** so you can confirm each known gap is present/absent in the target rather than rediscovering it from scratch.

## Always-present recurring gaps (audit EVERY SOP)

| Gap | Why it's a finding | Exact-change pointer |
|---|---|---|
| **TAT undefined** | grep "tat" is a trap (matches for**mat**, state**ment**, accep**t**ance, footer). Prove absence by searching the word **"turnaround"** specifically. | Add §4.9.5 TAT clause (routine X h, STAT Y h, monthly log, quarterly review). |
| **Accuracy/Specificity: NA (or Refer)** | No validation evidence; "NA" or "Refer" is not acceptable for an accredited method (ISO 15189 7.3.1). Some SOPs (BIO 05/06) have **both** "NA"; others (BIO 02/03/04) have "Accuracy: NA, Specificity: Refer". | Quantify bias (±X%) via CRM; convert interference data into the specificity statement; cite CLSI EP05/06 + validation SOP. |
| **No periodic-review clause** | All "review" hits are the footer or QC-handling text; no "review every N years". | Add §7.0 review/validity (2-year cadence, owner = Biochem Section Head). |
| **MSP 29 / validation SOP not cited** | Only MSP 18/19 (QC/EQA) cited in §5.0. | Add VDC/MSP/29 (Risk) + VDC/MSP/XX (Method Verification) to §5.0. |
| **Critical Results: NA (partial)** | §4.14 is "NA" but §4.15 Clinical Decision Values may be defined (BIO 05: 50 & 400; BIO 06: 20, 60 & 300). The "NA" lacks rationale — if no panic value exists, say so explicitly rather than leave a bare "NA". This gap is **silent** in older series SOPs (BIO 01–04 had "NA" for both fields). | Replace §4.14 with "No critical/panic value established for [analyte] at this laboratory. Results exceeding clinical decision thresholds (§4.15) warrant clinical correlation per §4.17." |

## Per-SOP outliers (confirm individually — do NOT assume)

| SOP | LOQ | Calibration Frequency | "Potential Variab…: NA" | EQA cadence | Notable |
|---|---|---|---|---|---|
| BIO 01 Albumin (BCG) | (dye-binding) | defined | — | RIQAS monthly | dye-binding limitation caveat |
| BIO 02 ACE (FAPGG) | **0–150 U/L (ERROR)** | defined §4.7 | — | RIQAS monthly | LOQ = AMR, contradicts LOD 5 |
| BIO 03 ACP (α-Naphthyl) | **1.0 IU/L (CORRECT =LOD)** | **"NA" §4.7 (self-contradicts §4.8.1)** | Potential Variability: NA §4.18 | RIQAS monthly | labile-sample stabilisation well covered |
| BIO 04 ADA (Peroxidase) | **0–200 U/L (ERROR)** | defined §4.7 | Potential Sources of Variations: NA §4.18 | Half-yearly ILC | LOQ > AMR 0–20, contradicts LOD 4 |
| BIO 05 ALP (AMP Buffer) | **5 U/L (CORRECT)** = lower AMR | defined §4.7 (AB mode) | §4.18 populated (not NA) | RIQAS monthly | **Clinical Decision Values defined** (50 & 400); one of few SOPs with CDV |
| BIO 06 ALT (IFCC) | **3 U/L (CORRECT)** = lower AMR | defined §4.7 | §4.18 populated (diurnal variation data) | RIQAS monthly | **Clinical Decision Values defined** (20, 60 & 300); Precision %CV 13.8 & MU 27 stated |
| BIO 07 Ammonia (AU 5800) | **10–600 (=AMR, range format)** ⚠️ | defined §4.7 **+ every 1 week** (unique time-based) | §4.18: NA | EQC per MSP/19 (program not named) | **Critical Results defined** (>109 μmol/L — first in series); Precision %CV 5.1 & MU 9.9 stated; LOQ/AMR/CRR all identical (10–600) |
| BIO 08 Amylase (AU Series) | **10 U/L (CORRECT)** = lower AMR | defined §4.7 | §4.18 populated (macroamylasemia) | RIQAS monthly + Fluids Amylase ILC | **CRR 20000 >> AMR 2000** (first to properly distinguish dilution); Clinical Decision Values defined (50, 120 & 200); Precision %CV 6.7 & MU 13.2 stated |

## LOQ error pattern (BIO 02 & 04)

Both list LOQ equal to or wider than the reportable/AMR range and include a "0" lower bound — analytically meaningless. Likely root cause: transcription of the reportable-interval upper bound into the LOQ field. **Fix:** cross-check against the kit insert; expected LOQ ≈ LOD. BIO 03 (ACP), BIO 05 (ALP), and BIO 06 (ALT) prove the correct shape (LOQ = LOD = lower AMR bound).

## Calibration-Frequency "NA" pattern (BIO 03 only, so far)

BIO 03 declares "Calibration Frequency: NA" yet §4.8.1 runs controls "as calibration verification" and the kinetic method needs a calibration factor — an internal self-contradiction. BIO 02/04 define it correctly. When you hit "NA", check whether the body text already describes event-triggered calibration; if so, it's a contradiction, not just an omission.

## "Potential Variab…: NA" pattern (BIO 03 & 04; **BIO 05 & 06 break the pattern**)

BIO 03 (ACP) and BIO 04 (ADA) carry a stray "NA" field (Potential Variability / Potential Sources of Variations, §4.18) that understates real pre-/intra-analytical variation the SOP itself describes elsewhere. Replace with the actual sample-type/dilution/interference caveats already present in the document.

**BIO 05 (ALP) and BIO 06 (ALT) do NOT have this gap** — their §4.18 is genuinely populated (BIO 05 with procedural caveats; BIO 06 with diurnal-variation data showing ALT fluctuates 45% daily, peaking in afternoon). This confirms the "NA" is fixable: the template exists for the rest of the series.

## Clinical Decision Values vs Critical Results divergence

Earlier SOPs (BIO 01–04) had **both** §4.14 Critical Results and §4.15 Clinical Decision Values set to "NA". Beginning with BIO 05 (ALP), the two fields **diverge** in three distinct patterns:

| Pattern | Examples | §4.14 Critical Results | §4.15 Clinical Decision Values |
|---------|----------|------------------------|--------------------------------|
| Both NA | BIO 01–04 | NA | NA |
| CDV defined | BIO 05, 06, 08 | NA | **Populated** (e.g. 20/60/300, 50/120/200) |
| Crit Res defined | BIO 07 | **>109 μmol/L** (first in series!) | NA |

**BIO 07 (Ammonia) is unique** — it is the **only SOP so far** that defines a Critical Results threshold (>109 μmol/L) but leaves Clinical Decision Values as NA. This is the reverse of the BIO 05/06/08 pattern.

**BIO 08 (Amylase) is the best-documented** — Clinical Decision Values (50, 120, 200), Precision/MU stated, **and** CRR (20000) properly exceeds AMR (2000) with validated dilution. It is the first SOP in the series to clearly distinguish analytical range from clinical reportable range.

Future audits should:
1. Check BOTH fields — they may diverge independently.
2. If either is "NA" without rationale, replace with an explicit note (see Always-Present gaps table).
3. When both are missing, the fix is more substantive (build thresholds from literature or clinical team input).
4. When only one is populated, the fix is a prose clarification — not a full rebuild.

## Delivery checklist

Each audit → 7-section Google Doc + local copy at `/home/sak/sop_audit_vdc_bio_XX.md`:
1. Executive Summary
2. SOPs Reviewed (table)
3. What the full dump contains (verbatim evidence table)
4. Findings (with **Exact Suggested Change** each)
5. Cross-SOP Conflict Table
6. Priority Action Plan (Immediate / 30 days / Long term)
7. Confidence Note (state full-chunk grounding)

Then **call `GET_DOCUMENT_PLAINTEXT` to verify rendering** and **paste the `display_url`** in the reply. Build `COMPOSIO_MULTI_EXECUTE_TOOL` calls with `tool_slug` *inside* each `tools[]` entry.
