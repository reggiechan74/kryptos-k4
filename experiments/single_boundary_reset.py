"""SINGLE-BOUNDARY-RESET-001: one shared-state restart, exact bounded scope."""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random
import subprocess
import time

from check_controls import run as check_controls
from run_bounded import validated_baseline, inputs_hashes
from run_io import RunSnapshot, specification, json_bytes
from strategy_followup import ALPHABETS, AZ, configurations, model_id, transform, rank_oracle

ROOT=Path(__file__).resolve().parents[1]
SPEC='research/specifications/SINGLE-BOUNDARY-RESET-001.json'
BOUNDARIES=(None,)+tuple(range(1,97))
SEED=2026102222


def known(data):
    return {c['start']-1+j:p for c in data['cribs'] for j,p in enumerate(c['plaintext'])}


def deadline_check(deadline):
    if time.monotonic()>deadline:raise TimeoutError('120-second single-reset budget')


def split_transform(text,cfg,b,inverse=False,rotate=False):
    if b is None:return transform(text,cfg,inverse=inverse,rotate=rotate)[0]
    return (transform(text[:b],cfg,inverse=inverse,rotate=rotate)[0]
            +transform(text[b:],cfg,inverse=inverse,rotate=rotate)[0])


def generator(plain,cfg,b,rotate=False):
    reference,initial=cfg;state=list(initial);out=[]
    for i,p in enumerate(plain):
        if i==b:state=list(initial)
        c=state[reference.index(p)];out.append(c);j=state.index(c)
        if rotate:state=state[j:]+state[:j]
        else:state.pop(j);state.insert(0,c)
    return ''.join(out)


def recency_oracle(cipher,cfg,b):
    r,initial=cfg;out=[]
    for i,c in enumerate(cipher):
        start=b if b is not None and i>=b else 0
        prefix=cipher[start:i];seen=set(prefix)
        state=''.join(sorted(seen,key=prefix.rindex,reverse=True))+''.join(x for x in initial if x not in seen)
        out.append(r[state.index(c)])
    return ''.join(out)


def case_id(cfg,b):
    return model_id(cfg)+'/reset_before_'+('none' if b is None else str(b+1))


def forced_positions(plains,positions):
    if not plains:return {}
    return {str(i+1):next(iter(v)) for i in positions
            if len(v:={p[i] for p in plains})==1}


def mtf_select(cipher,k,deadline,full=False,oracle=False):
    rows=[];training=[];survivors=[];aliases=defaultdict(list)
    for cfg in configurations():
        for b in BOUNDARIES:
            deadline_check(deadline)
            plain=split_transform(cipher,cfg,b,inverse=True)
            if oracle:assert plain==recency_oracle(cipher,cfg,b)
            train=all(plain[i]==k[i] for i in range(21,34))
            all24=train and all(plain[i]==k[i] for i in range(63,74))
            row=dict(id=case_id(cfg,b),boundary_before_one_based=None if b is None else b+1,
                     model=model_id(cfg),training_compatible=train,
                     east_matches=sum(plain[i]==k[i] for i in range(21,34)),
                     berlin_matches=sum(plain[i]==k[i] for i in range(63,74)),all24=all24)
            if full:
                assert split_transform(plain,cfg,b)==cipher
                row.update(plaintext=plain,first_contradiction=next((dict(position_one_based=i+1,
                           expected=p,observed=plain[i]) for i,p in sorted(k.items()) if plain[i]!=p),None),
                           full_regeneration=True)
            if train:training.append((row['id'],plain))
            if all24:survivors.append((row['id'],plain))
            aliases[plain].append(row['id']);rows.append(row)
    train_plains={p for _,p in training};full_plains={p for _,p in survivors}
    result=dict(raw_cases=388,covered_no_reset_cases=4,new_boundary_cases=384,
                training_description_count=len(training),training_distinct_plaintexts=len(train_plains),
                compatible_description_count=len(survivors),compatible_distinct_plaintexts=len(full_plains),
                training_case_ids=[i for i,_ in training],compatible_case_ids=[i for i,_ in survivors],
                training_forced_Berlin=forced_positions(train_plains,range(63,74)),
                compatible_forced_noncrib=forced_positions(full_plains,[i for i in range(97) if i not in k]),
                unforced_noncrib_positions=[i+1 for i in range(97) if i not in k
                    and full_plains and len({p[i] for p in full_plains})>1],
                compatible_plaintext_sha256=sorted(hashlib.sha256(p.encode()).hexdigest() for p in full_plains),
                all_output_distinct_plaintexts=len(aliases),
                output_alias_groups=[dict(plaintext=p,case_ids=ids) for p,ids in aliases.items() if len(ids)>1],
                per_case=rows)
    return result


def doublet_certificates(cipher,k):
    rows=[]
    for i in (26,33):
        assert cipher[i-1]==cipher[i] and i in k
        required=k[i]
        assert all(required!=cfg[0][0] for cfg in configurations())
        rows.append(dict(repeated_cipher_positions_one_based=[i,i+1],cipher_doublet=cipher[i-1:i+1],
                         required_plaintext=required,required_reset_before_one_based=i+1,
                         no_reset_possible_plaintext=sorted({r[0] for r,_ in configurations()})))
    assert rows[0]['required_reset_before_one_based']!=rows[1]['required_reset_before_one_based']
    return dict(witnesses=rows,scope='At most one restart in the fixed four MTF models; supplied after spec before implementation/evaluation; verification of disclosed deduction, no multi-reset sweep.')


def recurrence_crypt(text,alphabet,params,b,inverse=False):
    a,c,d,seed=params;state=seed;out=[]
    for i,symbol in enumerate(text):
        if i==b:state=seed
        y=alphabet.index(symbol)
        if inverse:
            out.append(alphabet[(y-state)%26]);cipher_value=y
        else:
            cipher_value=(y+state)%26;out.append(alphabet[cipher_value])
        state=(a*state+c+d*cipher_value)%26
    return ''.join(out)


def internal_edges(cipher,k,alphabet,positions):
    values={i:(alphabet.index(cipher[i])-alphabet.index(k[i]))%26 for i in positions}
    return [dict(source=i,target=i+1,key=values[i],cipher=alphabet.index(cipher[i]),required=values[i+1])
            for i in positions if i+1 in values]


def parity_conflict(edges,b):
    remaining=[e for e in edges if e['target']!=b]
    for x,y in itertools.combinations(remaining,2):
        if (x['key']%2,x['cipher']%2)==(y['key']%2,y['cipher']%2) and x['required']%2!=y['required']%2:
            return [dict(from_position_one_based=e['source']+1,to_position_one_based=e['target']+1,
                         triple=[e['key'],e['cipher'],e['required']]) for e in (x,y)]
    return None


def fit_recurrence_seeds(cipher,train,alphabet,params,b):
    a,c,d=params;u,v=1,0;seeds=list(range(26))
    for i in range(max(train)+1):
        if i==b:u,v=1,0
        if i in train:
            required=(alphabet.index(cipher[i])-alphabet.index(train[i]))%26
            seeds=[seed for seed in seeds if (u*seed+v)%26==required]
        if not seeds:return []
        u,v=a*u%26,(a*v+c+d*alphabet.index(cipher[i]))%26
    return seeds


def recurrence_audit(cipher,k,deadline):
    results=[]
    train={i:k[i] for i in range(21,34)}
    for alphabet in ALPHABETS:
        all_edges=internal_edges(cipher,k,alphabet,range(21,34))+internal_edges(cipher,k,alphabet,range(63,74))
        train_edges=all_edges[:12]
        first=parity_conflict(train_edges,None);second=parity_conflict(all_edges[12:],None)
        assert first and second
        proofs=[]
        for b in BOUNDARIES:
            witness=parity_conflict(all_edges,b)
            assert witness,'supplied single-reset certificate failed; stop without widening domain'
            proofs.append(dict(boundary_before_one_based=None if b is None else b+1,parity_witness=witness,
                               compatible_parameters=0,compatible_distinct_plaintexts=0))
        buckets={b:[] for b in BOUNDARIES};triples=0;kept=0
        for a,c,d in itertools.product(range(26),repeat=3):
            triples+=1
            if triples%256==0:deadline_check(deadline)
            failures=[]
            for edge in train_edges:
                if (a*edge['key']+c+d*edge['cipher'])%26!=edge['required']:
                    failures.append(edge['target'])
                    if len(failures)>1:break
            if len(failures)>1:continue
            kept+=1
            schedules=BOUNDARIES if not failures else (failures[0],)
            for b in schedules:
                seeds=fit_recurrence_seeds(cipher,train,alphabet,(a,c,d),b)
                for seed in seeds:
                    params=(a,c,d,seed)
                    plain=recurrence_crypt(cipher,alphabet,params,b,inverse=True)
                    assert all(plain[i]==p for i,p in train.items())
                    assert recurrence_crypt(plain,alphabet,params,b)==cipher
                    buckets[b].append((params,plain))
        training_records=[]
        for b,candidates in buckets.items():
            plains={p for _,p in candidates}
            # Full inconsistency was proved independently, not fitted on Berlin.
            assert not any(all(p[i]==k[i] for i in range(63,74)) for p in plains)
            training_records.append(dict(boundary_before_one_based=None if b is None else b+1,
                parameter_count=len(candidates),distinct_plaintexts=len(plains),
                forced_Berlin=forced_positions(plains,range(63,74)),
                parameters=[list(p) for p,_ in candidates],
                plaintexts=sorted(plains)))
        results.append(dict(alphabet=alphabet,island_witnesses=[first,second],schedule_proofs=proofs,
                            coefficient_triples_checked=triples,triples_after_internal_training_filter=kept,
                            training=training_records,compatible_parameters=0,compatible_plaintexts=0))
    return dict(raw_description_upper_bound=88653344,full_parameter_enumeration=False,
                covered_no_reset_description_count=913952,raw_schedules=194,
                results=results,compatible_parameters=0,compatible_distinct_plaintexts=0)


def phases(period,b):
    return tuple((i if b is None or i<b else i-b)%period for i in range(97))


def canonical_phase(signature):
    labels={};result=[]
    for phase in signature:
        if phase not in labels:labels[phase]=len(labels)
        result.append(labels[phase])
    return tuple(result)


def phase_constraints(cipher,k,alphabet,sigma,schedule,period):
    def fit(positions):
        roots={};conflict=None
        for i in positions:
            phase=schedule[i];value=(alphabet.index(cipher[i])-sigma*alphabet.index(k[i]))%26
            if phase in roots and roots[phase][1]!=value and conflict is None:
                conflict=dict(positions_one_based=[roots[phase][0]+1,i+1],phase=phase,
                              required_effective_keys=[roots[phase][1],value])
            roots.setdefault(phase,(i,value))
        return roots,conflict
    t,tc=fit(range(21,34));full,fc=fit(sorted(k))
    predictions=[]
    if tc is None:
        for i in range(63,74):
            ph=schedule[i]
            predictions.append(dict(position_one_based=i+1,predicted=ph in t,
                matches=(alphabet[(alphabet.index(cipher[i])-t[ph][1])*sigma%26]==k[i]) if ph in t else None))
    return dict(training_compatible=tc is None,training_conflict=tc,full_compatible=fc is None,
                full_conflict=fc,training_occupied_phases=len(t),all_occupied_phases=len(full),
                training_parameter_assignments='0' if tc else str(26**(period-len(t))),
                free_all_crib_phases=period-len(full),
                compatible_parameter_assignments='0' if fc else str(26**(period-len(full))),
                compatible_distinct_plaintexts='0' if fc else str(26**(period-len(full))),
                Berlin_predictions=predictions,
                joint_Berlin_consistency_checks=11-(len(full)-len(t)),
                unconstrained_slots_not_completed=True)


def periodic_audit(cipher,k,deadline):
    cases={};raw=0
    for alphabet,period,equation,b in itertools.product(ALPHABETS,range(1,13),('plus','minus','beaufort'),BOUNDARIES):
        deadline_check(deadline);raw+=1
        sigma=-1 if equation=='beaufort' else 1
        schedule=canonical_phase(phases(period,b));key=(alphabet,period,sigma,schedule)
        alias=dict(equation=equation,boundary_before_one_based=None if b is None else b+1)
        if key not in cases:
            covered=schedule==canonical_phase(phases(period,None))
            cases[key]=dict(alphabet=alphabet,period=period,sigma=sigma,phase_signature=list(schedule),
                           covered_by_prior_no_reset_domain=covered,aliases=[],
                           **phase_constraints(cipher,k,alphabet,sigma,schedule,period))
        cases[key]['aliases'].append(alias)
    rows=list(cases.values());new=[x for x in rows if not x['covered_by_prior_no_reset_domain']]
    return dict(raw_shapes=raw,canonical_shapes=len(rows),covered_canonical_baselines=len(rows)-len(new),
                new_canonical_schedules=len(new),canonical_compatible=sum(x['full_compatible'] for x in rows),
                per_case=rows,key_negation_equivalence='plus/minus are the same unrestricted-key family',
                no_reset_coverage='ROUTE-001 identity arithmetic periods1..96, both alphabets, all3equations; no dictionary restriction')


def planted_plain(rng,k):
    p=[rng.choice(AZ) for _ in range(97)]
    for i,c in k.items():p[i]=c
    return ''.join(p)


def controls(k,deadline):
    rng=random.Random(SEED);plants=[];negatives=[];counts=Counter()
    for cfg in configurations():
        for p in AZ:
            cipher=generator(p,cfg,None)
            assert split_transform(cipher,cfg,None,inverse=True)==p
            counts['mtf_one_step']+=1
        for b in (None,21,63,74):
            for _ in range(2):
                plain=planted_plain(rng,k);cipher=generator(plain,cfg,b)
                assert recency_oracle(cipher,cfg,b)==plain
                assert split_transform(cipher,cfg,b,inverse=True)==plain
                plants.append(dict(ciphertext=cipher,plaintext=plain,true_case=case_id(cfg,b)))
    rng.shuffle(plants)
    for row in plants:
        result=mtf_select(row['ciphertext'],k,deadline)
        assert row['true_case'] in result['compatible_case_ids']
        assert hashlib.sha256(row['plaintext'].encode()).hexdigest() in result['compatible_plaintext_sha256']
        row['selection']=result
    for cfg in configurations():
        for _ in range(2):
            cipher=generator(planted_plain(rng,k),cfg,None,rotate=True)
            negatives.append(dict(kind='nearby_cyclic_rotation',ciphertext=cipher,selection=mtf_select(cipher,k,deadline)))
    for row in plants:
        shuffled=list(row['ciphertext']);rng.shuffle(shuffled);cipher=''.join(shuffled)
        assert Counter(cipher)==Counter(row['ciphertext'])
        negatives.append(dict(kind='histogram_shuffle',ciphertext=cipher,selection=mtf_select(cipher,k,deadline)))
    for alphabet,params,b in itertools.product(ALPHABETS,[(0,4,16,4),(2,17,7,16),(25,15,20,14),(1,0,0,5)],(None,21,63,74)):
        plain=planted_plain(rng,k);cipher=recurrence_crypt(plain,alphabet,params,b)
        assert recurrence_crypt(cipher,alphabet,params,b,True)==plain
        edges=internal_edges(cipher,k,alphabet,range(21,34))+internal_edges(cipher,k,alphabet,range(63,74))
        assert parity_conflict(edges,b) is None
        counts['recurrence_planted_roundtrips']+=1
        if params==(1,0,0,5):
            assert all(recurrence_crypt(plain,alphabet,params,other)==cipher for other in BOUNDARIES)
            counts['stationary_all_boundary_alias_checks']+=97
    recurrence_alias={}
    for a in (0,2):
        alphabet=AZ;params=(a,4,16,0);plain=planted_plain(rng,k);cipher=recurrence_crypt(plain,alphabet,params,None)
        outputs=[recurrence_crypt(cipher,alphabet,(a,4,16,seed),None,True) for seed in range(26)]
        same_tail=[p for p in outputs if p[1:]==plain[1:]]
        assert len(same_tail)==(26 if a==0 else 2)
        recurrence_alias[str(a)]=len(same_tail)
    for alphabet,eq,period,b in itertools.product(ALPHABETS,('plus','minus','beaufort'),range(1,13),(None,21,63)):
        sigma=-1 if eq=='beaufort' else 1;tau=-1 if eq=='minus' else 1
        key=[rng.randrange(26) for _ in range(period)];p=planted_plain(rng,k);schedule=phases(period,b)
        cipher=''.join(alphabet[(sigma*alphabet.index(x)+tau*key[schedule[i]])%26] for i,x in enumerate(p))
        restored=''.join(alphabet[(alphabet.index(x)-tau*key[schedule[i]])*sigma%26] for i,x in enumerate(cipher))
        assert restored==p
        result=phase_constraints(cipher,k,alphabet,sigma,schedule,period)
        assert result['full_compatible']
        collision=next((i,j) for i,j in itertools.combinations(sorted(k),2) if schedule[i]==schedule[j])
        changed=dict(k);j=collision[1];changed[j]=AZ[(AZ.index(changed[j])+1)%26]
        assert not phase_constraints(cipher,changed,alphabet,sigma,schedule,period)['full_compatible']
        counts['periodic_planted_roundtrips']+=1
        counts['periodic_mutated_rejections']+=1
    summary=dict(mtf_plants=32,truth_included=32,
        unique_correct_descriptions=sum(x['selection']['compatible_case_ids']==[x['true_case']] for x in plants),
        unique_plaintexts=sum(x['selection']['compatible_distinct_plaintexts']==1 for x in plants),
        ambiguous_plaintexts=sum(x['selection']['compatible_distinct_plaintexts']>1 for x in plants),
        nearby_compatible=sum(x['selection']['compatible_description_count']>0 for x in negatives if x['kind']=='nearby_cyclic_rotation'),
        histogram_compatible=sum(x['selection']['compatible_description_count']>0 for x in negatives if x['kind']=='histogram_shuffle'))
    return dict(seed=SEED,checks=dict(counts),recurrence_seed_alias_counts=recurrence_alias,
                mtf_plants=plants,mtf_negatives=negatives,summary=summary,
                blindness='Algorithmic label-blind selection only, not investigator blinding; report expected ambiguity and descriptive false acceptance without tuning.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--spec-commit',required=True);args=p.parse_args()
    spec=specification(args.spec_commit,SPEC)
    code=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    subprocess.run(['git','merge-base','--is-ancestor',args.spec_commit,code],check=True)
    assert subprocess.check_output(['git','show',args.spec_commit+':'+SPEC])==(ROOT/SPEC).read_bytes()
    names=[SPEC,'experiments/single_boundary_reset.py','tests/test_single_boundary_reset.py',
           'data/k4.json','data/controls.json','experiments/strategy_followup.py','experiments/run_io.py',
           'experiments/run_bounded.py','experiments/check_baseline.py','experiments/check_controls.py',
           'experiments/ciphers.py','experiments/bounded_models.py','research/CLOCK-RESET-PROOF.md']
    for name in names:
        assert subprocess.check_output(['git','show',code+':'+name])==(ROOT/name).read_bytes(),name
    with RunSnapshot('results/single-boundary-reset-runs','SINGLE-BOUNDARY-RESET-001',spec) as snap:
        start=time.monotonic();deadline=start+120
        snap.manifest['jobs'].append(dict(experiment='SINGLE-BOUNDARY-RESET-001',status='running',deadline_seconds=120))
        data=validated_baseline(ROOT/'data/k4.json');baseline=check_controls();k=known(data)
        passed=controls(k,deadline)
        mtf=mtf_select(data['ciphertext'],k,deadline,full=True,oracle=True)
        certificate=doublet_certificates(data['ciphertext'],k)
        recurrence=recurrence_audit(data['ciphertext'],k,deadline)
        periodic=periodic_audit(data['ciphertext'],k,deadline)
        result=dict(id='SINGLE-BOUNDARY-RESET-001',status='completed',spec_commit=args.spec_commit,
            code_commit=code,command='python3 experiments/single_boundary_reset.py --spec-commit '+args.spec_commit,
            python=platform.python_version(),platform=platform.platform(),file_sha256=inputs_hashes(names),
            baseline_controls=baseline,controls=passed,mtf=mtf,mtf_doublet_certificate=certificate,
            recurrence=recurrence,periodic=periodic,elapsed_seconds=time.monotonic()-start,
            interpretation='One shared-state reset only; no known sentence boundary or carved-row preference. Disclosed certificates verified, not blind discoveries. Compatible/free fits if any are not candidates; no automaticsecondreset.')
        snap.write('SINGLE-BOUNDARY-RESET-001.json',json_bytes(result));snap.manifest['jobs'][-1]['status']='completed'
        snap.final_check=lambda:deadline_check(deadline)
    print(json.dumps(dict(run_id=snap.run_id,controls=passed['summary'],
        mtf={x:mtf[x] for x in ['raw_cases','training_description_count','compatible_description_count','all_output_distinct_plaintexts']},
        recurrence_training_counts=[[x['parameter_count'] for x in r['training']] for r in recurrence['results']],
        periodic={x:periodic[x] for x in ['raw_shapes','canonical_shapes','covered_canonical_baselines','new_canonical_schedules','canonical_compatible']},
        elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__=='__main__':main()
