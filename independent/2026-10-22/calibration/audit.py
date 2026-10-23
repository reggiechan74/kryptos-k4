#!/usr/bin/env python3
"""Independent local-constraint audit, not used to select or fit classifier."""
import importlib.util,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('calibration',R/'run_calibration.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def independent_candidates(cipher):
    found=[];details=[]
    for alphabet in [m.AZ,m.KA]:
        c=m.encode(cipher,alphabet)
        # Adjacent known states eliminate recurrence coefficient triples first.
        desired=(c[21:34]-m.encode('EASTNORTHEAST',alphabet))%26
        a,b,d=np.indices((26,26,26),dtype=np.int64).reshape(3,-1)
        for j in range(1,13):
            ok=(a*desired[j-1]+b+d*c[21+j-1])%26==desired[j]
            a,b,d=a[ok],b[ok],d[ok]
        local_count=len(a);first_count=0;full_count=0
        for aa,bb,dd in zip(a,b,d):
            for seed in range(26):
                # Independently recompute keystream, then compare string slices.
                state=seed;pt=[]
                for y in c:
                    pt.append(alphabet[(int(y)-state)%26])
                    state=(int(aa)*state+int(bb)+int(dd)*int(y))%26
                pt=''.join(pt)
                if pt[21:34]=='EASTNORTHEAST':
                    first_count+=1
                    if pt[63:74]=='BERLINCLOCK':
                        full_count+=1;found.append((alphabet,int(aa),int(bb),int(dd),seed))
        details.append({'alphabet':alphabet,'adjacent_crib_coefficient_triples':local_count,'first_crib_seeded_fits':first_count,'full_crib_seeded_fits':full_count})
    return set(found),details

results=json.loads((R/'synthesis_results.json').read_text()); audit=[]
targets=[('K4',m.K4,results['K4'])]+[(f"positive_{r['case']}",r['ciphertext'],r) for r in results['synthetic_positives']]
for name,cipher,stored in targets:
    independent,details=independent_candidates(cipher)
    fresh,original=m.synthesize(cipher,[m.CRIB1],[m.CRIB2])
    assert independent==set(original)
    assert len(independent)==stored['parameter_candidates']
    assert all(row['first_crib_seeded_fits']==stored['counts_by_alphabet'][i]['after_first_crib'] for i,row in enumerate(details))
    audit.append({'target':name,'candidate_sets_equal':True,'details':details})
data=json.loads((R/'generated_examples.json').read_text())
train_plains={x['plaintext'] for x in data['windows']['train']};test_plains={x['plaintext'] for x in data['windows']['test']}
assert not train_plains&test_plains
for split in ['train','test']:
    for row in data['data'][split]:
        assert len(row['plaintext'])==len(row['ciphertext'])==97
        assert np.array_equal(m.decrypt(m.encode(row['ciphertext']),row['label'],row['key']),m.encode(row['plaintext']))
# Expected exact invariance under alphabet renaming for the chosen features.
for plain,mono in zip(data['controls']['PLAINTEXT'],data['controls']['MONOALPHABETIC']):
    assert np.allclose(plain['features'],mono['features'])
assert m.features(m.encode(m.K4))[0]==float(sum(m.K4.count(ch)*(m.K4.count(ch)-1) for ch in m.AZ)/(97*96))
out={'synthesis_independent_audit':audit,'all_288_encrypt_decrypt_roundtrips':True,'exact_length_97_every_ciphertext':True,'train_test_plaintext_overlap':0,'unique_train_windows':len(train_plains),'unique_test_windows':len(test_plains),'plaintext_mono_feature_invariance':True,'K4_IC_independent_match':True}
(R/'audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
