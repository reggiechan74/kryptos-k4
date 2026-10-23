"""AUTONOMOUS-RECURRENCE-001: exact coefficient, prefix and forecast audit."""
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random
import subprocess
import time

from exact_linear import (solve_field,solve_ring,contains,ring_vectors,canonical_affine,union_cardinality)
from check_controls import run as check_controls
from run_bounded import validated_baseline,inputs_hashes
from run_io import RunSnapshot,specification,json_bytes

ROOT=Path(__file__).resolve().parents[1]
SPEC='research/specifications/AUTONOMOUS-RECURRENCE-001.json'
ALPHABETS=('ABCDEFGHIJKLMNOPQRSTUVWXYZ','KRYPTOSABCDEFGHIJLMNQUVWXZ')


def check_deadline(deadline):
    if time.monotonic()>deadline:raise TimeoutError('120-second autonomous recurrence budget')


def keys(seed,coeff,constant,length,q=26):
    out=list(seed);r=len(coeff)
    for i in range(len(out),length):out.append((constant+sum(coeff[j-1]*out[i-j] for j in range(1,r+1)))%q)
    return out[:length]


def companion_keys(seed,coeff,constant,length,q=26):
    out=list(seed);state=list(reversed(seed))
    while len(out)<length:
        next_value=(constant+sum(a*x for a,x in zip(coeff,state)))%q
        state=[next_value]+state[:-1];out.append(next_value)
    return out[:length]


def coefficient_system(values,r,fitted,q=26):
    matrix=[list(reversed(values[i-r:i]))+([1] if fitted else []) for i in range(r,len(values))]
    rhs=values[r:]
    return matrix,rhs,solve_ring(matrix,rhs,q,r+int(fitted))


def linear_map(coeff,constant,length,q=26):
    r=len(coeff);w=[[int(i==j) for j in range(r)] for i in range(r)];offset=[0]*r
    for i in range(r,length):
        w.append([sum(coeff[j-1]*w[i-j][k] for j in range(1,r+1))%q for k in range(r)])
        offset.append((constant+sum(coeff[j-1]*offset[i-j] for j in range(1,r+1)))%q)
    return w,offset


def reachable_prefix(values,coeff,constant,start=21,length=97,q=26):
    r=len(coeff);w,offset=linear_map(coeff,constant,length,q)
    matrix=w[start:start+r];rhs=[value-o for value,o in zip(values[:r],offset[start:start+r])]
    space=solve_ring(matrix,rhs,q,r)
    result=dict(seed_space=space,seed_cardinality=space['cardinality'],reachable=space['consistent'])
    if not space['consistent']:return result
    tail=keys(values,coeff,constant,length-start,q)
    images=[]
    for f in space['fields']:
        p=f['prime'];point=f['particular']
        stream=[(o+sum(a*b for a,b in zip(row,point)))%p for row,o in zip(w,offset)]
        assert stream[start:]==[x%p for x in tail]
        basis_images=[[sum(a*b for a,b in zip(row,v))%p for row in w] for v in f['basis']]
        assert all(not any(v[start:]) for v in basis_images)
        images.append(canonical_affine(stream[:start],[v[:start] for v in basis_images],p))
    result['prefix_product_space']=images
    # Removing trailing zeros does not remove the higher-order startup freedom.
    reduced=r
    while reduced and coeff[reduced-1]==0:reduced-=1
    result['nonzero_coefficient_lag']=reduced
    if reduced<r:
        extra=[];targets=[]
        for i in range(reduced,r):
            row=[0]*r;row[i]=1
            for lag in range(1,reduced+1):row[i-lag]-=coeff[lag-1]
            extra.append(row);targets.append(constant)
        lower=solve_ring(matrix+extra,rhs+targets,q,r)
        result['same_rule_reduced_startup_seed_count']=lower['cardinality']
        result['all_reachable_seeds_globally_reduce']=lower['cardinality']==space['cardinality']
    return result


def exact_counts(records,budget,deadline):
    groups=defaultdict(list);raw=0
    for record in records:
        if record['prefix']['reachable']:
            raw+=record['prefix']['seed_cardinality']
            groups[tuple(record['tail'])].append(record['prefix']['prefix_product_space'])
    total=0;terms=0
    try:
        for spaces in groups.values():
            check_deadline(deadline);count,n=union_cardinality(spaces,4096);total+=count;terms+=n
            if budget['union_terms']+terms>20000:raise OverflowError('total affine-union terms')
    except OverflowError as error:
        return dict(raw_parameter_seed_descriptions=str(raw),distinct_full_streams=None,status='budget_unresolved',reason=str(error))
    budget['union_terms']+=terms
    return dict(raw_parameter_seed_descriptions=str(raw),distinct_full_streams=str(total),status='exact',union_terms=terms)


def analyze(values,held,r,fitted,q=26,start=21,length=97,held_start=63,budget=None,deadline=float('inf')):
    if budget is None:budget=dict(coefficients=0,union_terms=0)
    matrix,rhs,space=coefficient_system(values,r,fitted,q)
    result=dict(order=r,constant_mode='fitted' if fitted else 'zero',training_matrix=matrix,training_rhs=rhs,
                coefficient_space=space,training_coefficient_count=str(space['cardinality']),records=[])
    if not space['consistent']:
        result.update(status='impossible',reason='inconsistent_training_coefficients',training_counts=dict(status='exact',raw_parameter_seed_descriptions='0',distinct_full_streams='0'),
                      heldout_counts=dict(status='exact',raw_parameter_seed_descriptions='0',distinct_full_streams='0'),training_prediction_sets=None,heldout_compatible_coefficients=0)
        return result
    if space['cardinality']>20000 or budget['coefficients']+space['cardinality']>50000:
        result.update(status='budget_unresolved',reason='coefficient_enumeration_cap',training_prediction_sets=None,heldout_compatible_coefficients=None)
        return result
    records=[]
    for vector in ring_vectors(space):
        check_deadline(deadline);budget['coefficients']+=1
        coeff=list(vector[:r]);constant=vector[-1] if fitted else 0
        prefix=reachable_prefix(values,coeff,constant,start,length,q)
        tail=keys(values,coeff,constant,length-start,q)
        forecast=tail[held_start-start:held_start-start+len(held)]
        records.append(dict(coefficients=coeff,constant=constant,prefix=prefix,tail=tail,
                            gap=tail[len(values):held_start-start],heldout_prediction=forecast,
                            heldout_compatible=prefix['reachable'] and forecast==held))
    valid=[x for x in records if x['prefix']['reachable']];survivors=[x for x in valid if x['heldout_compatible']]
    train_counts=exact_counts(valid,budget,deadline);held_counts=exact_counts(survivors,budget,deadline)
    if not survivors:status='impossible'
    elif held_counts['status']!='exact':status='budget_unresolved'
    elif int(held_counts['distinct_full_streams'])==1:status='unique_under_assumptions'
    else:status='compatible_but_ambiguous'
    result.update(records=records,status=status,reason='no_joint_heldout_forecast' if not survivors else 'all_crib_compatibility_only',
                  reachable_coefficient_count=len(valid),unreachable_coefficient_count=len(records)-len(valid),
                  heldout_compatible_coefficients=len(survivors),training_counts=train_counts,heldout_counts=held_counts,
                  training_prediction_sets=[sorted({row['heldout_prediction'][i] for row in valid}) for i in range(len(held))] if valid else None,
                  distinct_training_forecast_vectors=sorted({tuple(row['heldout_prediction']) for row in valid}))
    return result


def enumerate_streams(result,q,length):
    for row in result['records']:
        if not row['prefix']['reachable']:continue
        for seed in ring_vectors(row['prefix']['seed_space']):
            yield tuple(row['coefficients']+[row['constant']]),seed,tuple(keys(seed,row['coefficients'],row['constant'],length,q))


def controls():
    rng=random.Random(2026102223);plants=[];small=[]
    for alphabet,r,fitted,last in itertools.product(ALPHABETS,range(2,7),(False,True),(1,2,13,0)):
        coeff=[rng.randrange(26) for _ in range(r-1)]+[last];constant=rng.randrange(26) if fitted else 0
        seed=[rng.randrange(26) for _ in range(r)];plain=[rng.choice(ALPHABETS[0]) for _ in range(97)]
        plain[21:34]=list('EASTNORTHEAST');plain[63:74]=list('BERLINCLOCK');plain=''.join(plain)
        stream=companion_keys(seed,coeff,constant,97)
        assert keys(seed,coeff,constant,97)==stream
        cipher=''.join(alphabet[(alphabet.index(p)+k)%26] for p,k in zip(plain,stream))
        assert ''.join(alphabet[(alphabet.index(c)-k)%26] for c,k in zip(cipher,keys(seed,coeff,constant,97)))==plain
        values=[(alphabet.index(c)-alphabet.index(p))%26 for c,p in zip(cipher[21:34],plain[21:34])]
        _,_,space=coefficient_system(values,r,fitted)
        vector=coeff+([constant] if fitted else [])
        assert contains(space,vector)
        prefix=reachable_prefix(values,coeff,constant)
        assert contains(prefix['seed_space'],seed)
        tail=keys(values,coeff,constant,76)
        assert tail==stream[21:] and len(tail[13:42])==29 and len(tail[42:53])==11
        plants.append(dict(alphabet=alphabet,order=r,fitted=fitted,last_coefficient=last,
            coefficients=coeff,constant=constant,seed=seed,plaintext=plain,ciphertext=cipher,
            coefficient_set_contains_truth=True,prefix_set_contains_truth=True,
            reachable_seed_count=str(prefix['seed_cardinality']),forecast_entire_tail_equal=True))
    for q,fitted,rep in itertools.product((2,3,6),(False,True),range(2)):
        r=2;coeff=[rng.randrange(q) for _ in range(r)];constant=rng.randrange(q) if fitted else 0;seed=[rng.randrange(q) for _ in range(r)]
        target=companion_keys(seed,coeff,constant,12,q);values=target[3:8];held=target[9:12]
        solved=analyze(values,held,r,fitted,q,3,12,9)
        fast=set(enumerate_streams(solved,q,12));brute=set()
        for params in itertools.product(range(q),repeat=r+int(fitted)):
            cs=list(params[:r]);b=params[-1] if fitted else 0
            for initial in itertools.product(range(q),repeat=r):
                # Independent unrolled scalar simulation, no solver/map/decode call.
                k=list(initial)
                for i in range(r,12):k.append((b+cs[0]*k[i-1]+cs[1]*k[i-2])%q)
                if k[3:8]==values:brute.add((tuple(cs+[b]),initial,tuple(k)))
        assert fast==brute
        valid={x[2] for x in fast};after={x for x in valid if list(x[9:12])==held}
        assert int(solved['training_counts']['distinct_full_streams'])==len(valid)
        assert int(solved['heldout_counts']['distinct_full_streams'])==len(after)
        small.append(dict(modulus=q,fitted=fitted,replicate=rep,raw_parameter_seed_space=q**(r+int(fitted)+r),
                          train_parameter_count=len(fast),train_distinct_streams=len(valid),heldout_distinct_streams=len(after),exact_sets_equal=True))
    # Extra startup degree: last coefficient zero does not force global lower order.
    example=reachable_prefix([8]*13,[1,0],0)
    assert example['seed_cardinality']==26 and example['same_rule_reduced_startup_seed_count']==1
    # An internally consistent local window may not be reachable from any prefix.
    unreachable=reachable_prefix([1,0,0,0,0],[0,0],0,start=3,length=12)
    assert not unreachable['reachable']
    return dict(seed=2026102223,literal_plants=plants,literal_plant_count=len(plants),
                ambiguous_planted_prefixes=sum(int(x['reachable_seed_count'])>1 for x in plants),
                complete_small_ring_comparisons=small,small_ring_count=len(small),
                startup_alias_example=dict(reachable_seeds=26,globally_reduced_seeds=1),
                unreachable_internal_fit_rejected=True,
                interpretation='Truth inclusion and exact planted forecasts, not unique unknown-model recovery. No statistical claim.')


def parity_context(values,start=21):
    seen={}
    for i in range(6,len(values)):
        signature=tuple(x%2 for x in values[i-6:i]);target=values[i]%2
        if signature in seen and seen[signature][1]!=target:
            earlier,old=seen[signature]
            return dict(context_parities=list(signature),windows_one_based=[[start+earlier-6+1,start+earlier],[start+i-6+1,start+i]],
                        targets_one_based=[start+earlier+1,start+i+1],target_parities=[old,target],
                        scope='Same six predecessor parities require different next parity; excludes fixed affine autonomous orders2..6, not arbitrary lookup maps or other alphabets.',
                        provenance='Independent witness supplied after spec before implementation; locally verified, not blind discovery.')
        seen.setdefault(signature,(i,target))
    return None


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--spec-commit',required=True);args=p.parse_args()
    spec=specification(args.spec_commit,SPEC);code=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    subprocess.run(['git','merge-base','--is-ancestor',args.spec_commit,code],check=True)
    assert subprocess.check_output(['git','show',args.spec_commit+':'+SPEC])==(ROOT/SPEC).read_bytes()
    files=[SPEC,'experiments/autonomous_recurrence.py','experiments/exact_linear.py','tests/test_autonomous_recurrence.py',
           'data/k4.json','data/controls.json','experiments/run_io.py','experiments/run_bounded.py','experiments/check_baseline.py',
           'experiments/check_controls.py','experiments/ciphers.py']
    for name in files:assert subprocess.check_output(['git','show',code+':'+name])==(ROOT/name).read_bytes(),name
    with RunSnapshot('results/autonomous-recurrence-runs','AUTONOMOUS-RECURRENCE-001',spec) as snap:
        started=time.monotonic();deadline=started+120
        snap.manifest['jobs'].append(dict(experiment='AUTONOMOUS-RECURRENCE-001',status='running',deadline_seconds=120))
        data=validated_baseline(ROOT/'data/k4.json');baseline=check_controls();passed=controls();check_deadline(deadline)
        results=[];contexts=[];budget=dict(coefficients=0,union_terms=0)
        for alphabet in ALPHABETS:
            values=[(alphabet.index(c)-alphabet.index(p))%26 for c,p in zip(data['ciphertext'][21:34],'EASTNORTHEAST')]
            held=[(alphabet.index(c)-alphabet.index(p))%26 for c,p in zip(data['ciphertext'][63:74],'BERLINCLOCK')]
            contexts.append(dict(alphabet=alphabet,training_key_values=values,parity_witness=parity_context(values)))
            for r,fitted in itertools.product(range(2,7),(False,True)):
                check_deadline(deadline);row=analyze(values,held,r,fitted,budget=budget,deadline=deadline)
                row.update(alphabet=alphabet,required_Berlin_key=held)
                results.append(row)
        result=dict(id='AUTONOMOUS-RECURRENCE-001',status='completed',spec_commit=args.spec_commit,code_commit=code,
                    command='python3 experiments/autonomous_recurrence.py --spec-commit '+args.spec_commit,
                    python=platform.python_version(),platform=platform.platform(),file_sha256=inputs_hashes(files),
                    baseline_controls=baseline,controls=passed,structures=results,parity_contexts=contexts,budget_used=budget,
                    elapsed_seconds=time.monotonic()-started,
                    interpretation='Exact first-crib coefficient spaces and reachable-prefix logic; no resets, edits, feedback, tree walk, routes or expansion. Public clues not independent evidence.')
        snap.write('AUTONOMOUS-RECURRENCE-001.json',json_bytes(result));snap.manifest['jobs'][-1]['status']='completed'
        snap.final_check=lambda:check_deadline(deadline)
    print(json.dumps(dict(run_id=snap.run_id,statuses=[x['status'] for x in results],
                         coefficient_counts=[x['training_coefficient_count'] for x in results],
                         plants=passed['literal_plant_count'],small_ring_comparisons=passed['small_ring_count'],
                         ambiguous_planted_prefixes=passed['ambiguous_planted_prefixes'],elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__=='__main__':main()
