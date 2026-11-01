#!/usr/bin/env python3
"""Validate proposal metadata only. Does not implement or execute any cipher."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
catalog = json.loads((root / 'catalog.json').read_text())
rows = catalog['records']
assert len(rows) == catalog['record_count'] == 100
assert {r['id'] for r in rows} == {f'N100-{i:03d}' for i in range(1,101)}
assert len({r['specification']['title'].casefold() for r in rows}) == 100
assert len({r['draft_id'] for r in rows}) == 100
assert sorted(r['review_rank'] for r in rows) == list(range(1,101))
assert sum(r['type']=='mechanism' for r in rows) == catalog['mechanisms'] == 78
assert sum(r['type']=='method' for r in rows) == catalog['methods'] == 22
assert catalog['target_runs_executed'] == 0
assert catalog['baseline_commit'] == '3e128d9a617af377516a0b9878a942b29bf2e3b8'
for r in rows:
    assert r['status'] in {'proposed_unrun','specification_blocked'}
    assert r['novelty_status'] == 'exact_scope_review_pending'
    assert r['target_admission'] == 'not_admitted'
    s=r['specification']
    assert s.get('mechanism')
    assert s.get('bounded_test') or s.get('finite_falsifiable_test')
    assert s.get('identifiability_limit')
    assert s.get('controls') or s.get('positive_controls')
    assert s.get('sources') or s.get('prior_art')
    text=(root/(r['group']+'.md')).read_text()
    assert f'<a id="{r["id"].lower()}"></a>' in text
    assert r['id'] in (root/'INDEX.md').read_text()
    assert r['id'] in (root/'RANKED-INDEX.md').read_text()
print('PASS: 100 unique proposals, 78 mechanisms + 22 methods; required scientific metadata, anchors and ranks present.')
print('This does not certify novelty, mathematical correctness, controls, execution readiness or a K4 result.')
