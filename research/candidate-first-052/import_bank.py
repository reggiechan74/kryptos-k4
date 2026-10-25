#!/usr/bin/env python3
"""Non-scoring import/validation; never edits author files or selects from cipher scores."""
import hashlib
import json
from pathlib import Path
import reference as p

ROOT=Path(__file__).resolve().parent
SOURCE_GROUPS=('a_themes','b_neutral','c_berlin','d_messages')


def import_records():
    prior=p.load_json(ROOT/'prior051_bank.json')
    heldout=p.load_json(ROOT/'heldout.json')
    excluded={r['text'] for r in prior}|{heldout['text']}
    bank=[];sources={};seen={}
    for group in SOURCE_GROUPS:
        path=ROOT/'authors'/f'{group}.json'
        raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
        records=json.loads(raw)
        if len(records)!=256:raise ValueError(f'{group}: require256records, got{len(records)}')
        original_ids=set()
        for r in records:
            if not isinstance(r.get('id'),str) or not r['id'] or r['id'] in original_ids:
                raise ValueError(f'{group}: duplicate/missing source ID')
            original_ids.add(r['id'])
            if not isinstance(r.get('spaced_prose'),str) or p.letters(r['spaced_prose'])!=r.get('normalized'):
                raise ValueError(f'{group}:{r["id"]}: prose/normalized mismatch')
            text=r['normalized'];p.validate_ciphertext(text)
            for start,word in p.CRIBS:
                if text[start:start+len(word)]!=word:raise ValueError(f'{group}:{r["id"]}: crib position mismatch')
            alias=f'{group}:{r["id"]}'
            if text in seen:raise ValueError(f'Duplicate normalized plaintext: {alias} and {seen[text]}')
            if text in excluded:raise ValueError(f'Prior051/heldout plaintext repeated: {alias}')
            if not isinstance(r.get('revision_history'),list):raise ValueError(f'{alias}: revision_history missing')
            seen[text]=alias
            bank.append({'id':alias,'original_id':r['id'],'group':group,'text':text,
                         'spaced_prose':r['spaced_prose'],'theme':r.get('theme',''),
                         'source_file':str(path.relative_to(ROOT)),'source_sha256':digest})
        sources[str(path.relative_to(ROOT))]={'sha256':digest,'records':len(records),'group':group}
    bank=p.validate_bank(bank)
    return bank,{'count':len(bank),'unique_plaintexts':len(seen),'prior051_exclusion_count':len(prior),
                 'heldout_excluded':True,'sources':sources,'alias_rule':'group:original_id',
                 'normalization':'uppercase A-Z only','scores_used':False}


def main():
    if (ROOT/'freeze.json').exists():raise ValueError('Cannot replace frozen bank')
    bank,manifest=import_records()
    p.write_json(ROOT/'bank.json',bank)
    p.write_json(ROOT/'bank_import.json',manifest)
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
