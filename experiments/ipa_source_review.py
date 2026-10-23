"""Independent IPA source/certificate checks; no new transcription or cipher scan."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unicodedata
from ipa_preprocessing import normalize,ORDINARY,WINDOWS,AZ,KR
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'independent/2026-10-22/ipa-preprocessing'
SPECIAL_X={'ː':':','ɔ':'O','θ':'T','ɝ':'3`','ɪ':'I','ɑ':'A'}
XMAP={**{c:c for c in ORDINARY},**SPECIAL_X}


def xsampa_subset(ipa):
    try:return ''.join(XMAP[c] for c in ipa)
    except KeyError as exc:raise ValueError('outside disclosed IPA subset') from exc


def inverse_subset(text):
    inverse={v:k for k,v in XMAP.items()};out=[];i=0
    while i<len(text):
        token=next((t for t in sorted(inverse,key=len,reverse=True) if text.startswith(t,i)),None)
        if token is None:raise ValueError('outside disclosed X-SAMPA subset')
        out.append(inverse[token]);i+=len(token)
    return ''.join(out)


def compare():
    receipt=json.loads((ROOT/'results/IPA-INDEPENDENT-LOCAL-REPLAY.json').read_text())
    for name,r in receipt['members'].items():
        raw=(BASE/name).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
    source=json.loads((BASE/'ipa-feasibility-001.json').read_text())
    native=json.loads((BASE/'ipa-feasibility-001b-results.json').read_text())
    data=json.loads((ROOT/'data/ipa-cambridge-us-v1.json').read_text())
    local=json.loads((ROOT/'results/IPA-PREPROCESSING-001.json').read_text())
    fixture=json.loads((ROOT/'data/k4.json').read_text())
    cipher=fixture['ciphertext'];assert source['baseline']['ciphertext']==cipher
    for word,raw in source['pronunciation'].items():
        assert normalize(raw)==normalize(data['entries'][word.lower()])
        assert unicodedata.normalize('NFC',raw)==raw and '-' not in raw
    assert source['representations'][1]['strings']==[w for _,w in WINDOWS]
    assert source['representations'][0]['tokens']==local['normalization']['R1_segments']
    for row in source['results']['periodic_constraints']:
        p=str(row['period']);w=local['mapping_independent_periods']['witnesses'][p]
        assert row['deterministic_contradictions']==sum(x['reason']=='same IPA, different ciphertext' for x in w)
        assert row['injectivity_contradictions']==sum(x['reason']=='different IPA, same ciphertext' for x in w)
        d=local['mapping_independent_periods']['pair_diagnostics'][p]
        assert (row['same_source_same_phase_pairs'],row['same_cipher_same_phase_pairs'])==(d['repeated_IPA_pairs'],d['repeated_ciphertext_pairs'])
    symbols={i:s for start,w in WINDOWS for i,s in enumerate(w,start)}
    cross=[]
    for row in native['certificates']:
        a=row['alphabet'];sign=1 if row['family']=='Vigenere addition' else -1
        cert=row['first_certificate'];left,right=cert['first'],cert['second']
        for anchor in (left,right):
            i=anchor['i'];s=symbols[i];p=a.index(ORDINARY[s]);c=a.index(cipher[i]);k=(c-sign*p)%26
            assert anchor=={'i':i,'position':i+1,'symbol':s,'cipher':cipher[i],'P':p,'C':c,'K':k}
        assert (left['i']-right['i'])%row['period']==0 and left['K']!=right['K']
        localrow=next(r for r in local['rows'] if (r['alphabet'],r['equation'],r['period'])==('AZ' if a==AZ else 'KRYPTOS','add' if sign==1 else 'beaufort',row['period']))
        if right['position']>34:
            assert not localrow['fixed_ordinary_anchor_conflicts'];cross.append({'alphabet':'AZ' if a==AZ else 'KRYPTOS','equation':'add' if sign==1 else 'beaufort','period':row['period'],'positions':[left['position'],right['position']],'key_values':[left['K'],right['K']]})
        else:assert localrow['fixed_ordinary_anchor_conflicts']
    assert cross==[{'alphabet':'AZ','equation':'add','period':10,'positions':[24,64],'key_values':[25,12]}]
    assert len(native['certificates'])==48 and local['ordinary_anchor_rejected_structures']==47
    supplement=json.loads((BASE/'ipa-first-crib-marker-supplement.json').read_text())
    marker=[]
    for proof in supplement['proof']:
        oi=proof['ordinary_position']-1;mi=proof['marker_position']-1
        assert (oi-mi)%10==0 and symbols[mi]=='ː'
        key=(AZ.index(cipher[oi])-AZ.index(ORDINARY[symbols[oi]]))%26
        value=(AZ.index(cipher[mi])-key)%26
        assert key==proof['implied_K'] and value==proof['required_marker_alias_index'];marker.append(value)
    assert marker==[13,11]
    serialized=[xsampa_subset(w) for _,w in WINDOWS]
    assert serialized==['i:stnO:rTi:st','b3`:lInklA:k']
    assert [inverse_subset(s) for s in serialized]==[w for _,w in WINDOWS]
    return {'verified_original_members':len(receipt['members']),'source_normalized_forms_match':True,
            'structural_period_records_match':12,'native_full_window_anchor_certificates_verified':48,
            'native_cross_window_certificate':cross,'local_first_window_ordinary_anchor_rejections':47,
            'supplementary_first_window_marker_indices':marker,'local_first_window_relaxed_rejections':48,
            'xsampa_subset_strings':serialized,'xsampa_lengths':list(map(len,serialized)),
            'native_normalization_extra_rules_change_fixed_inputs':False,
            'source_retrieval_claim':'Supplied source-worker evidence, not independently re-fetched pages.',
            'new_cipher_families_or_alias_trials_added':0}


def replay():
    checks=compare();outputs={}
    for key,name in [('main_replay','replay_ipa_pilot.py'),('supplement_replay','replay_ipa_marker_supplement.py')]:
        raw=subprocess.check_output([sys.executable,str(BASE/name)],timeout=30,text=True)
        outputs[key]=json.loads(raw)
    receipt=json.loads((ROOT/'results/IPA-INDEPENDENT-LOCAL-REPLAY.json').read_text())
    assert all(outputs[k]==receipt[k] for k in outputs)
    return {'checks':checks,'native_replays':outputs,'original_files_modified':False}

if __name__=='__main__':print(json.dumps(replay(),ensure_ascii=False,indent=2))
