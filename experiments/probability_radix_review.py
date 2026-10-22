"""Replay preserved geometric probability/radix audits without changing inputs."""
import hashlib
import itertools
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from alphabet_geometry import load_schema,codebook,encode_array

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'independent/2026-10-22'
CAL=BASE/'periodic-crib-calibration'
RAD=BASE/'radix-feedback'


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_members():
    t=json.loads((ROOT/'results/GEOMETRIC-PROBABILITY-RADIX-TRANSFER.json').read_text())
    count=0
    for package in t['bundles']:
        for name,record in package['members'].items():
            p=BASE/package['name']/name
            assert len(p.read_bytes())==record['bytes'] and digest(p)==record['sha256'],name
            count+=1
    assert digest(CAL/'calibrate.py')=='3b41f37b3f7d911cb55eb61a8f5ab9188f6b3bf311992ea876d86b91f634a1a7'
    return count


def exact_checks():
    members=verify_members()
    vectors=codebook(load_schema())
    codes={c:encode_array(v) for c,v in vectors.items()}
    alphabet=''.join(sorted(codes,key=codes.get));index={c:i for i,c in enumerate(alphabet)}
    fixture=json.loads((ROOT/'data/k4.json').read_text())
    assert fixture==json.loads((CAL/'k4.json').read_text())
    cipher=fixture['ciphertext'];plain='EASTNORTHEAST'
    calibration=json.loads((CAL/'result.json').read_text())
    plan=json.loads((CAL/'preregistration.json').read_text())
    assert plan['N']==19999 and calibration['N']==19999 and plan['recorded_before_simulation']
    assert calibration['rank_alphabet']==alphabet
    counts={}
    for family,delta in [('add',17),('beaufort',9)]:
        favorable=sum((index[cipher[j]]-index[cipher[i]])%26==delta for i in range(97) for j in range(97) if i!=j)
        assert favorable==382
        fraction=Fraction(favorable,97*96)
        recorded=calibration['exact_period12_histogram_null'][family]
        assert str(fraction)==recorded['probability_fraction'] and float(fraction)==recorded['probability']
        counts[family]={'favorable':favorable,'denominator':97*96,'fraction':str(fraction)}
    assert 9!=17 and calibration['exact_union_of_both_period12_models']==float(Fraction(764,97*96))
    fit=calibration['observed_survivors'];assert len(fit)==1
    assert (fit[0]['family'],fit[0]['period'],fit[0]['second_window'])==('beaufort',12,'ZBVJDFKRUCA')
    assert (index['F']+index['E'])%26==(index['S']+index['T'])%26==13
    distribution=calibration['family_null_count_distribution']
    assert distribution=={'0':18268,'1':1728,'2':3}
    assert sum(distribution.values())==19999
    assert calibration['family_exceedances']==1731
    assert calibration['family_plus_one_monte_carlo_p']==float(Fraction(1732,20000))
    controls=calibration['controls']
    assert controls['pairwise_comparisons']==479976 and controls['original_oracle_model_comparisons']==5256
    assert len(controls['synthetic_plants'])==24 and all(x['status']=='pass' for x in controls['synthetic_plants'])
    # Independently verify Wilson endpoints by their binomial score equation.
    n=19999;k=1731;phat=k/n;z=1.959963984540054
    lo,hi=calibration['family_tail_95pct_wilson_interval']
    assert lo<phat<hi
    for p in (lo,hi):assert math.isclose(n*(phat-p)**2,z*z*p*(1-p),rel_tol=1e-11,abs_tol=1e-14)

    result=json.loads((RAD/'results.json').read_text())
    independent=json.loads((RAD/'independent-results.json').read_text())
    spec=json.loads((RAD/'SPECIFICATION.json').read_text())
    assert spec['ciphertext']==cipher
    assert result['training']=={'positions':[22,34],'plaintext':plain,'ciphertext':cipher[21:34]}
    assert not result['heldout_evaluated'] and not result['root_or_digit_search_performed']
    assert not independent['heldout_evaluated']
    certificates=[]
    for family in result['families']:
        name=family['alphabet'];a=spec['alphabets'][name]
        keys=[(a.index(c)+(-1 if family['equation']=='additive' else 1)*a.index(p))%26 for c,p in zip(cipher[21:34],plain)]
        assert keys==family['key_sequence']
        assert family['parity_survivors']==[] and family['mod26_survivor_count']==0
        glyphs=plain if family['source']=='plaintext' else cipher[21:34]
        for row in family['all_training_transitions']:
            i=row['position']-22;v=vectors[glyphs[i]]
            assert row['source_glyph']==glyphs[i] and row['key']==keys[i] and row['next_key']==keys[i+1]
            assert row['code_parities']==sorted({v[0]%2,sum(v)%2})
            assert row['code_residues_mod26']==sorted({encode_array(v,b)%26 for b in range(2,28)})
        cert=family['minimum_certificate'];assert len(cert)==2
        for row in cert:
            v=vectors[row['source_glyph']]
            assert v[0]==0 and sum(v)%2==0 and row['code_parities']==[0]
        assert cert[0]['key']%2==cert[1]['key']%2 and cert[0]['next_key']%2!=cert[1]['next_key']%2
        for aa,cc,dd in itertools.product(range(2),repeat=3):
            assert any((aa*r['key']+cc-r['next_key'])%2 for r in cert)
        other=next(x for x in independent['families'] if x['alphabet']==name and x['equation'].lower()==family['equation'] and x['source']==family['source'][0].upper())
        assert other['keys']==keys and other['mod26_survivors']==0
        assert [x['position'] for x in other['minimum_core']]==[x['position'] for x in cert]
        certificates.append({'alphabet':name,'equation':family['equation'],'source':family['source'],
                             'positions':[r['position'] for r in cert],
                             'glyphs':[r['source_glyph'] for r in cert],
                             'key_parity':cert[0]['key']%2,
                             'opposed_output_parities':[r['next_key']%2 for r in cert]})
    assert len(certificates)==8
    assert result['controls']['roundtrip_cases']==3264
    assert result['controls']['parity_solver_plants_retained']==3264 and result['controls']['mod26_plants_retained']==3264
    assert result['controls']['alignment_mutation']['mutation_detected']
    e={encode_array(vectors['E'],b)%26 for b in range(2,28)}
    assert e=={0,2,4,6,10,14,16,22}
    return {'original_members_verified':members,'calibration_exact_closure':counts,
            'calibration_distribution':distribution,'plus_one_monte_carlo_p':0.0866,
            'calibration_pairwise_comparisons':479976,'calibration_original_oracle_checks':5256,
            'first_crib_only_certificates':certificates,'radix_families_excluded':8,
            'radix_roundtrips':3264,'auxiliary_direct_E_residues':sorted(e),
            'root_searches_added':0,'scope':'Calibration: frozen 24 periodic models only. Radix audit: frozen eight first-order affine feature-feedback families only.'}


def replay():
    checks=exact_checks()
    with tempfile.TemporaryDirectory(prefix='k4-geometric-audit-replay-') as tmp:
        tmp=Path(tmp);cal=tmp/'calibration';shutil.copytree(CAL,cal)
        subprocess.run([sys.executable,str(cal/'calibrate.py')],check=True,stdout=subprocess.DEVNULL,timeout=60)
        original=json.loads((CAL/'result.json').read_text());local=json.loads((cal/'result.json').read_text())
        changed=[k for k in original if original[k]!=local[k]]
        assert not set(changed)-{'python_version'}
        primary=tmp/'radix-primary.json';secondary=tmp/'radix-secondary.json'
        subprocess.run([sys.executable,str(RAD/'audit.py'),'--output',str(primary)],check=True,stdout=subprocess.DEVNULL,timeout=60)
        with secondary.open('w') as out:
            subprocess.run([sys.executable,str(RAD/'independent_verify.py')],check=True,stdout=out,timeout=60)
        assert primary.read_bytes()==(RAD/'results.json').read_bytes()
        assert secondary.read_bytes()==(RAD/'independent-results.json').read_bytes()
        return {'checks':checks,'calibration':{'numeric_and_trace_fields_exactly_equal':True,
                'differing_metadata_fields':changed,'original_python_version':original['python_version'],
                'local_python_version':local['python_version'],'original_result_sha256':digest(CAL/'result.json'),
                'local_result_sha256':digest(cal/'result.json'),'null_trace_sha256':local['null_draw_and_count_trace_sha256']},
                'radix_primary_byte_equal':True,'radix_primary_sha256':digest(primary),
                'radix_independent_byte_equal':True,'radix_independent_sha256':digest(secondary),
                'original_files_modified':False}

if __name__=='__main__':print(json.dumps(replay(),indent=2))
