#!/usr/bin/env python3
"""Consolidated common-deficiency scanner over a dumped JSONL collection.

Given a full collection dump (see dump_all_collection.py), this classifies EVERY
doc_id against the sop-auditor recurring-gap checklist and emits a per-doc matrix
+ aggregate, ready to paste into a consolidated audit Google Doc.

Checks (per SOP, on the concatenated chunk_text):
  - Accuracy / Specificity labeled values  -> REAL | NA | Refer | other | absent
  - TAT          -> present only if the WORD "turnaround" appears (the substring
                   "tat" is a footer/word-fragment trap; see Pitfall #8)
  - Periodic review -> only on explicit "review every N years / shall be reviewed /
                   next review due", EXCLUDING the "Reviewed & Issued by" footer and
                   QC-failure "review environmental conditions" text
  - CLSI / EP05/06/09/15 citation
  - Calibration frequency (defined / event-based via "calibration verification" /
                   NA / absent)
  - Critical / decision values (stated / NA / absent)
  - MSP 29 / risk-assessment citation
  - Reference intervals / interference limits (presence)
  - LOQ validity: LOQ >= LOD and LOQ ~= lower AMR bound; flags LOQ > 2x AMR (high)
                   or LOQ < 0.5x LOD (low)

USAGE:
  source .venv-sop/bin/activate
  python scan_validation_deficiencies.py /home/sak/all_vdc_chunks.jsonl \
         --family "au series" --out /home/sak/au_series_deficiency_matrix.json

The --family filter selects which doc_ids to classify (e.g. "au series" for the
Beckman Coulter AU-series; omit to scan all). Output JSON has keys:
  n, matrix[], aggregate{}, bio_context{} (if VDC BIO present).
"""
import json, re, argparse
from collections import defaultdict, Counter

acc_re = re.compile(r'accuracy\s*[:\-–]\s*([^\n|]{1,80})', re.I)
spe_re = re.compile(r'specificity\s*[:\-–]\s*([^\n|]{1,80})', re.I)
na_re = re.compile(r'^\s*(na|n/?a|not applicable|none|—|-|nil|\.?)\s*$', re.I)
refer_re = re.compile(r'refer|see cl|cl\.|clause|section|appendix', re.I)
real_re = re.compile(r'\d|%|±|recovery|bias|correlat|deming|passing|trueness', re.I)

def field_status(text, rx):
    seen = []
    for m in rx.finditer(text):
        v = m.group(1).strip()
        if v not in [s[1] for s in seen]:
            seen.append(v)
    if not seen:
        return ('absent', '')
    for v in seen:
        if na_re.match(v) or v.replace(' ', '').lower() in ('na', 'n/a', 'na.', 'n.a'):
            return ('NA', v)
    for v in seen:
        if refer_re.search(v):
            return ('Refer', v)
    for v in seen:
        if real_re.search(v):
            return ('REAL', v[:60])
    return ('other', seen[0][:60])

def has(text, pattern):
    return bool(re.search(pattern, text))

tat_re = re.compile(r'turnaround time|\btat\b', re.I)
review_re = re.compile(r'review', re.I)
def has_review_clause(text):
    for m in review_re.finditer(text):
        s = text[max(0, m.start()-40): m.end()+40]
        sl = s.lower().replace(' ', '')
        if 'reviewed&issued' in sl or 'preparedby:reviewe' in sl:
            continue
        if 'review environmental' in s.lower() or 'review recent events' in s.lower():
            continue
        if 'reviewed by' in s.lower():
            continue
        if re.search(r'shall be reviewed|reviewed (at least|every|annually|biannually|2 year)|review cycle|document (review|validity)|next review due', s, re.I):
            return True
    return False

clsi_re = re.compile(r'clsi', re.I)
ep_re = re.compile(r'ep\s?0?[569]|ep\s?15', re.I)
cal_re = re.compile(r'calibration frequency\s*[:\-–]\s*([^\n|]{1,80})', re.I)
def calib_status(text):
    for m in cal_re.finditer(text):
        v = m.group(1).strip()
        if na_re.match(v) or v.replace(' ', '').lower() in ('na', 'n/a'):
            return ('NA', v)
        return ('defined', v[:50])
    if has(text, r'calibration verification'):
        return ('event-based*', 'controls run as calibration verification')
    return ('absent', '')

crit_re = re.compile(r'critical (results|decision values|values)\s*[:\-–]\s*([^\n|]{1,60})', re.I)
def crit_status(text):
    seen = []
    for m in crit_re.finditer(text):
        v = m.group(2).strip()
        if v not in seen:
            seen.append(v)
    if not seen:
        return ('absent', '')
    for v in seen:
        if na_re.match(v) or v.replace(' ', '').lower() in ('na', 'n/a'):
            return ('NA', v)
    return ('stated', '; '.join(seen)[:50])

msp29_re = re.compile(r'msp\s?/?\s?29|risk assessment', re.I)
refint_re = re.compile(r'reference interval|reference range|biological reference', re.I)
interf_re = re.compile(r'interfer|cross.?react|limitation', re.I)
loq_re = re.compile(r'limit of quantitation\s*\(?loq\)?\s*[:\-–]\s*([^\n|]{1,40})', re.I)
amr_re = re.compile(r'analytical measurement range\s*\(?amr\)?\s*[:\-–]\s*([^\n|]{1,40})', re.I)
lod_re = re.compile(r'limit of detection\s*\(?lod\)?\s*[:\-–]\s*([^\n|]{1,40})', re.I)
num_re = re.compile(r'(\d+(?:\.\d+)?)')
def parse_loq(text):
    loq = amr = lod = None
    for m in loq_re.finditer(text):
        nums = num_re.findall(m.group(1))
        if nums: loq = float(nums[0])
    for m in amr_re.finditer(text):
        nums = num_re.findall(m.group(1))
        if nums: amr = float(nums[0])
    for m in lod_re.finditer(text):
        nums = num_re.findall(m.group(1))
        if nums: lod = float(nums[0])
    if loq is None:
        return ('absent', f'loq={loq},amr={amr},lod={lod}')
    if amr is not None and loq > amr * 2:
        return ('INVALID(high)', f'loq={loq},amr={amr},lod={lod}')
    if lod is not None and loq < lod * 0.5:
        return ('INVALID(low)', f'loq={loq},amr={amr},lod={lod}')
    return ('ok', f'loq={loq},amr={amr},lod={lod}')

def classify(did, text):
    a = field_status(text, acc_re)
    s = field_status(text, spe_re)
    return {
        'doc_id': did, 'accuracy': a[0], 'accuracy_ex': a[1],
        'specificity': s[0], 'specificity_ex': s[1],
        'tat': 'present' if has(text, tat_re) else 'ABSENT',
        'review_clause': 'present' if has_review_clause(text) else 'ABSENT',
        'clsi_ep': 'cited' if (has(text, clsi_re) or has(text, ep_re)) else 'absent',
        'calibration': calib_status(text)[0], 'calibration_ex': calib_status(text)[1],
        'critical_values': crit_status(text)[0], 'critical_ex': crit_status(text)[1],
        'msp29': 'cited' if has(text, msp29_re) else 'absent',
        'reference_intervals': 'present' if has(text, refint_re) else 'ABSENT',
        'interferences': 'present' if has(text, interf_re) else 'ABSENT',
        'loq': parse_loq(text)[0], 'loq_ex': parse_loq(text)[1],
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("--family", default=None, help="substring filter on doc_id")
    ap.add_argument("--out", default="/home/sak/deficiency_matrix.json")
    args = ap.parse_args()

    docs = defaultdict(list)
    with open(args.jsonl) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            docs[r["doc_id"]].append(r)

    if args.family:
        sel = sorted(d for d in docs if args.family.lower() in d.lower())
    else:
        sel = sorted(docs)

    matrix = []
    for did in sel:
        text = "\n".join(c["chunk_text"] for c in docs[did])
        matrix.append(classify(did, text))

    agg = {}
    for key in ['accuracy', 'specificity', 'tat', 'review_clause', 'clsi_ep',
                'calibration', 'critical_values', 'msp29', 'reference_intervals',
                'interferences', 'loq']:
        agg[key] = dict(Counter(m[key] for m in matrix))

    result = {'n': len(matrix), 'matrix': matrix, 'aggregate': agg}
    with open(args.out, 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Family='{args.family}' -> {len(matrix)} docs classified")
    print("Aggregate:")
    for k, v in agg.items():
        print(f"  {k:18s}: {v}")
    print(f"Wrote -> {args.out}")

if __name__ == "__main__":
    main()
