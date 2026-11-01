#!/usr/bin/env python3
"""Apply dated proposal-status overrides; metadata only, never cipher execution."""
import copy,hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent
original=(D/'catalog.json').read_bytes();catalog=json.loads(original);overrides=json.loads((D/'CURRENT-STATUS.json').read_text());effective=copy.deepcopy(catalog)
by={r['id']:r for r in effective['records']}
assert len(by)==len(effective['records'])==100
for update in overrides['overrides']:
 assert update['id'] in by
 record=by[update['id']];record['original_draft_status']=record['status'];record['status']=update['status'];record['status_override_evidence']=update['evidence'];record['synthetic_ready']=update['synthetic_ready'];record['target_admission']=update['target_admission'];record['recorded_runs']=update['runs'];record['run_scope']=update.get('run_scope','No recorded execution')
effective['current_status_source']='CURRENT-STATUS.json';effective['original_catalog_sha256']=hashlib.sha256(original).hexdigest();effective['effective_status_date']=overrides['date'];effective['status_note']='Use this current derivative for scheduling metadata; catalog.json is the immutable original draft. All proposals remain K4-target-unrun and unadmitted; C20 has completed synthetic-only correctness validation.'
(D/'CURRENT-CATALOG.json').write_text(json.dumps(effective,indent=2,ensure_ascii=False)+'\n')
lines=['# Current proposal index','','Generated from immutable draft plus CURRENT-STATUS.json; status overrides take precedence. Historical ranks are triage, not execution authority. All 100 remain K4-target-unrun/unadmitted; C20 has one synthetic-only correctness pilot.','','| Original review rank | ID | Draft | Effective status | Title |','| --- | --- | --- | --- | --- |']
for r in sorted(effective['records'],key=lambda x:x['review_rank']):lines.append(f"| {r['review_rank']} | [{r['id']}]({r['group']}.md#{r['id'].lower()}) | {r['draft_id']} | {r['status']} | {r['specification']['title'].replace('|','/')} |")
(D/'CURRENT-INDEX.md').write_text('\n'.join(lines)+'\n')
print('100 effective proposals; status overrides applied. No execution authority.')
