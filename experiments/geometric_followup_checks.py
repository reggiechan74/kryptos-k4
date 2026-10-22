"""Replay comparisons of frozen artifacts; no new roots, offsets or cipher family."""
from collections import defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
from alphabet_geometry import load_schema, codebook, encode_array

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'independent/2026-10-22'


def verify_imports():
    receipt=json.loads((ROOT/'results/GEOMETRIC-FOLLOWUP-LOCAL-REPLAY.json').read_text())
    checked=0
    for item in receipt['bundles']:
        for name,record in item['members'].items():
            raw=(BASE/item['name']/name).read_bytes()
            assert len(raw)==record['bytes'] and hashlib.sha256(raw).hexdigest()==record['sha256'],name
            checked+=1
    return checked


def compare():
    members=verify_imports()
    directory=BASE/'geometric-pilot-oracle'
    raw=(directory/'oracle.py').read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='9ee330efcd2d93b633ae61264a334484a645bde793157f430c9f8b8a2c8edd88'
    spec=importlib.util.spec_from_file_location('independent_geometric_oracle',directory/'oracle.py')
    oracle=importlib.util.module_from_spec(spec);spec.loader.exec_module(oracle)
    codes,rank=oracle.read_geometry(directory/'geometry-core.json',directory/'geometry-full.json')
    vectors=codebook(load_schema())
    assert codes=={c:encode_array(v) for c,v in vectors.items()}
    local=json.loads((ROOT/'results/GEOMETRIC-PILOT-001.json').read_text())
    external=json.loads((directory/'result.json').read_text())
    fixture=json.loads((ROOT/'data/k4.json').read_text())
    assert fixture==json.loads((directory/'k4.json').read_text())
    cipher=fixture['ciphertext']
    exact_outputs=0
    for row in local['pilot_b']['rows']:
        name,source,r,seed=row['model']
        alpha=oracle.AZ if name=='AZ' else oracle.KRYPTOS
        out=oracle.rotor_crypt(cipher,alpha,codes,seed,r,'plaintext' if source=='P' else 'ciphertext',True)
        assert out==row['plaintext']
        assert sum(out[i]==p for i,p in enumerate('EASTNORTHEAST',21))==row['training_matches']
        exact_outputs+=1
    periodic={(r['family'],r['period']):r for r in external['pilot1']}
    for row in local['pilot_a']['rows']:
        family='add' if row['equation']=='plus' else 'beaufort'
        independent=periodic[family,row['period']]
        assert independent['first_crib_pass']==(not row['training_contradictions'])
        actual=[(c['key_residue'],[c['first_position_one_based'],c['second_position_one_based']],[c['first_value'],c['second_value']]) for c in row['training_contradictions']]
        expected=[(c['residue_zero_based'],c['positions_one_based'],c['required_key_values']) for c in independent['first_crib_conflicts']]
        assert actual==expected
        if independent['first_crib_pass']:
            assert independent['key']==row['key'] and independent['plaintext']==row['plaintext']
            assert independent['minimal_period']==row['primitive_key_period']
    lookup_results=[]
    raw_audit=json.loads((BASE/'geometric-base-security/geometric-base-schedule-audit.json').read_text())
    for case in raw_audit['cases']:
        radix=case['root_digit_radix'];lookup=defaultdict(list)
        for base in range(2,radix+2):
            for letter,v in vectors.items():
                lookup[encode_array(v,base)].append({'letter':letter,'base':base})
        generated=[{'code':str(code),'candidates':candidates} for code,candidates in sorted(lookup.items())]
        assert generated==case['lookup']
        collisions=[row for row in generated if len(row['candidates'])>1]
        assert collisions==case['collision_classes']
        lookup_results.append({'root_digit_radix':radix,'pairs':26*radix,'distinct_codes':len(lookup),'collision_classes':collisions,'full_lookup_equal':True})
    return {'verified_original_members':members,'pilot_a_conflict_and_fit_records_equal':24,
            'pilot_b_full_plaintext_outputs_equal':exact_outputs,'source_fixture_equal':True,
            'independent_pilot_result_sha256':hashlib.sha256((directory/'result.json').read_bytes()).hexdigest(),
            'independent_all_family_roundtrips':external['controls']['rotor_all_family_roundtrips'],
            'independent_ambiguous_planted_cases':sum(r['exact_survivor_count']>1 for r in external['controls']['rotor_full_selection_controls']),
            'raw_number_security_lookup_comparisons':lookup_results,
            'new_K4_models_or_root_searches':0}

if __name__=='__main__':print(json.dumps(compare(),indent=2))
