#!/usr/bin/env python3
"""Check current proposal metadata without executing any cipher or benchmark."""
import hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent
raw=(D/'catalog.json').read_bytes();original=json.loads(raw);current=json.loads((D/'CURRENT-CATALOG.json').read_text());updates=json.loads((D/'CURRENT-STATUS.json').read_text())
assert current['original_catalog_sha256']==hashlib.sha256(raw).hexdigest()
orig={r['id']:r for r in original['records']};now={r['id']:r for r in current['records']};assert set(orig)==set(now) and len(now)==100
by={u['id']:u for u in updates['overrides']}
for ident,r in now.items():
 assert r['specification']==orig[ident]['specification'] and r['target_admission']=='not_admitted'
 assert r['status']==(by[ident]['status'] if ident in by else orig[ident]['status'])
 if ident in by:assert r['synthetic_ready'] is False and r['status_override_evidence']==by[ident]['evidence']
assert now['N100-036']['status']=='blocked_prior_art_overlap_unresolved'
assert 'blocked_prior_art_overlap_unresolved' in (D/'CURRENT-INDEX.md').read_text()
print('PASS: current100 metadata reflects all overrides; A01 blocked, specifications unchanged.')
