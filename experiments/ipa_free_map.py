"""Exact free injective IPA-glyph maps and periodic additive constraints."""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from math import prod
from pathlib import Path
import random
import time
from ipa_preprocessing import WINDOWS,AZ,KR
from route_key_graph import solve_graph
ROOT=Path(__file__).resolve().parents[1]


def falling(n,k):return 0 if n<k else prod(range(n-k+1,n+1))


def model(observations,period,modulus=26):
    glyphs=list(dict.fromkeys(g for _,g,_ in observations))
    if set(i%period for i,_,_ in observations)!=set(range(period)):
        raise ValueError('all modeled key phases must be observed')
    edges=[{'u':glyphs.index(g),'v':len(glyphs)+i%period,'delta':c%modulus,'position':i+1}
           for i,g,c in observations]
    graph=solve_graph(len(glyphs)+period,edges,modulus)
    graph['linear_vertex_assignments_without_injectivity']=graph.pop('exact_key_assignments')
    return {'modulus':modulus,'period':period,'glyphs':glyphs,
            'node_labels':['f:'+g for g in glyphs]+['q:'+str(r) for r in range(period)],
            'edges':edges,'graph':graph}


def count_injections(m,deadline=None,max_states=2000000):
    q=m['modulus'];g=m['graph'];ng=len(m['glyphs'])
    base={'gauge':'f(first observed glyph)=0','gauge_fixed_count':0,'ungauged_count':0,
          'offset_parameters_before_injectivity':g['component_count']-1,
          'linear_gauge_fixed_count':q**(g['component_count']-1) if g['compatible'] else 0,
          'states_evaluated':0}
    if not g['compatible']:
        return dict(base,status='impossible_cycle',certificate=g['first_conflict'])
    if ng>q:return dict(base,status='impossible_glyph_capacity',certificate={'glyphs':ng,'values':q})
    descriptions=[]
    for label,nodes in enumerate(g['components']):
        glyph_nodes=[v for v in nodes if v<ng]
        if not glyph_nodes:raise ValueError('phase-only component outside observed-phase domain')
        potentials=[g['representative_potentials'][v] for v in glyph_nodes]
        if len(set(potentials))!=len(potentials):
            x,y=next((a,b) for a,b in itertools.combinations(glyph_nodes,2)
                     if g['representative_potentials'][a]==g['representative_potentials'][b])
            return dict(base,status='impossible_within_component_injectivity',certificate={
                'component':label,'glyphs':[m['glyphs'][x],m['glyphs'][y]],
                'equal_relative_value':g['representative_potentials'][x]})
        descriptions.append({'component':label,'glyphs':{m['glyphs'][v]:g['representative_potentials'][v] for v in glyph_nodes},
            'phase_potentials':{str(v-ng):g['representative_potentials'][v] for v in nodes if v>=ng},
            'glyph_shape':sorted(potentials),'offset_rule':'one common component translation modulo '+str(q)})
    root=g['component_labels'][0];root_offset=-g['representative_potentials'][0]%q
    root_shape=descriptions[root]['glyph_shape']
    used=sum(1<<((v+root_offset)%q) for v in root_shape)
    multis=sorted([d for d in descriptions if d['component']!=root and len(d['glyph_shape'])>1],key=lambda d:(-len(d['glyph_shape']),d['component']))
    singles=[d['component'] for d in descriptions if d['component']!=root and len(d['glyph_shape'])==1]
    options=[]
    for d in multis:
        by_mask={}
        for t in range(q):
            mask=sum(1<<((v+t)%q) for v in d['glyph_shape'])
            by_mask.setdefault(mask,[]).append(t)
        options.append([(mask,len(shifts)) for mask,shifts in sorted(by_mask.items())])
        d['translations_grouped_by_occupied_set']=[{'mask_decimal':str(mask),'offsets':shifts,'multiplicity':len(shifts)} for mask,shifts in sorted(by_mask.items())]
    calls=0
    @lru_cache(None)
    def place(index,occupied):
        nonlocal calls
        calls+=1
        if calls>max_states:raise TimeoutError('packing memo-state budget')
        if deadline is not None and time.monotonic()>deadline:raise TimeoutError('packing time budget')
        if index==len(options):return 1
        return sum(weight*place(index+1,occupied|mask) for mask,weight in options[index] if not occupied&mask)
    ways=place(0,used)
    occupied_count=len(root_shape)+sum(len(d['glyph_shape']) for d in multis)
    singleton_factor=falling(q-occupied_count,len(singles))
    total=ways*singleton_factor
    return dict(base,status='compatible' if total else 'impossible_component_packing',
                gauge_fixed_count=total,ungauged_count=q*total,states_evaluated=calls,
                component_descriptions=descriptions,root_component=root,root_component_offset=root_offset,
                multi_component_order=[d['component'] for d in multis],singleton_components=singles,
                singleton_factor=singleton_factor,multi_translation_count=ways,
                packing_rule='Disjoint translated glyph sets only; phase values need not be injective. Translation multiplicities retained.',
                certificate=None if total else {'multi_translation_count':ways,'singleton_factor':singleton_factor})


def contains_description(m,values):
    g=m['graph'];q=m['modulus'];ng=len(m['glyphs'])
    if not g['compatible'] or len(set(values[:ng]))!=ng or values[0]%q!=0:return False
    return all((values[e['u']]-values[e['v']]-e['delta'])%q==0 for e in m['edges'])


def observations(cipher,alphabet,blocks=2):
    return [(i,s,alphabet.index(cipher[i])) for start,w in WINDOWS[:blocks] for i,s in enumerate(w,start)]


def stage_topology(train,full):
    ng=len(full['glyphs']);p=full['period'];parent=list(range(ng+p))
    def find(v):
        while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
        return v
    def join(u,v):parent[find(v)]=find(u)
    first_glyphs=set(train['glyphs']);seen=set(first_glyphs)
    for e in full['edges'][:13]:join(e['u'],e['v'])
    records=[]
    for e in full['edges'][13:]:
        s=full['glyphs'][e['u']]
        if s not in seen:
            kind='new_glyph_parameter';seen.add(s)
        elif find(e['u'])==find(e['v']):kind='closure_check'
        else:kind='component_offset_join'
        training_forced=False
        if s in first_glyphs:
            a=train['glyphs'].index(s);b=len(train['glyphs'])+(e['position']-1)%p
            training_forced=train['graph']['component_labels'][a]==train['graph']['component_labels'][b]
        records.append({'position':e['position'],'glyph':s,'classification':kind,'forced_by_training_graph':training_forced})
        join(e['u'],e['v'])
    counts=Counter(r['classification'] for r in records)
    assert counts['new_glyph_parameter']==6
    merges=train['graph']['component_count']-full['graph']['component_count']
    assert counts['component_offset_join']==merges and counts['closure_check']==5-merges
    assert full['graph']['independent_cycle_checks']-train['graph']['independent_cycle_checks']==5-merges
    return {'records':records,'counts':dict(counts),'training_component_merges':merges,
            'additional_joint_cycle_checks':5-merges,'new_glyphs':6}


def analyze(cipher,alphabet_name,period,deadline=None):
    alphabet=AZ if alphabet_name=='AZ' else KR
    first=observations(cipher,alphabet,1);train=model(first,period)
    tc=count_injections(train,deadline)
    row={'alphabet':alphabet_name,'period':period,'training':train,'training_count':tc,
         'second_block_evaluated':False,'full_count':None,'status':tc['status']}
    if not tc['gauge_fixed_count']:return row
    preds=[]
    for start,w in WINDOWS[1:]:
        for i,s in enumerate(w,start):
            if s not in train['glyphs']:continue
            dist=[]
            for value in range(26):
                extended=model(first+[(i,s,value)],period)
                dist.append(count_injections(extended,deadline)['gauge_fixed_count'])
            assert sum(dist)==tc['gauge_fixed_count']
            possible=[v for v,n in enumerate(dist) if n]
            phase=len(train['glyphs'])+i%period;glyph=train['glyphs'].index(s)
            preds.append({'position':i+1,'glyph':s,'counts_by_cipher_value':dist,'possible_cipher_values':possible,
                          'forced_by_training_graph':train['graph']['component_labels'][glyph]==train['graph']['component_labels'][phase],
                          'forced_under_all_training_injections':len(possible)==1,'actual_cipher_value':alphabet.index(cipher[i]),
                          'actual_in_prediction_set':alphabet.index(cipher[i]) in possible})
    full=model(observations(cipher,alphabet),period)
    fc=count_injections(full,deadline)
    row.update(second_block_evaluated=True,full=full,full_count=fc,status='compatible_observed_subset' if fc['gauge_fixed_count'] else 'impossible_second_block',
               first_stage_existing_glyph_predictions=preds,second_stage_topology=stage_topology(train,full),
               training_descriptions_with_unfitted_new_glyphs=tc['gauge_fixed_count']*falling(18,6),
               interpretation='Counts concern observed-subset map/key descriptions modulo one common translation; no full plaintext or universal IPA codec.')
    return row


def brute_gauge_count(m):
    q=m['modulus'];glyphs=m['glyphs'];ng=len(glyphs);p=m['period'];count=0
    for rest in itertools.permutations(range(1,q),ng-1):
        f=(0,)+rest;phases={};ok=True
        for edge in m['edges']:
            phase=edge['v']-ng;value=(f[edge['u']]-edge['delta'])%q
            if phase in phases and phases[phase]!=value:ok=False;break
            phases[phase]=value
        if ok:count+=1
    return count


def controls():
    deadline=time.monotonic()+300;rng=random.Random(20261023);toy=[]
    fixtures=[(4,[(0,'a',0),(2,'b',1),(1,'c',0),(3,'d',2)],2),
              (4,[(0,'a',0),(1,'b',0),(3,'c',2)],2),
              (7,[(i,chr(97+i),i) for i in range(4)],4),
              (5,[(0,'a',0),(1,'b',0)],1),
              (5,[(0,'a',0),(1,'a',1)],1)]
    for q in (3,4,5,6,7):
        for trial in range(8):
            p=1+trial%3;symbols=list('abc')+[rng.choice('abc') for _ in range(4)]
            f=dict(zip('abc',rng.sample(range(q),3)));key=[rng.randrange(q) for _ in range(p)]
            obs=[(i,s,(f[s]+key[i%p])%q) for i,s in enumerate(symbols)]
            if trial%2:obs[-1]=(obs[-1][0],obs[-1][1],(obs[-1][2]+1)%q)
            fixtures.append((q,obs,p))
    for q,obs,p in fixtures:
        m=model(obs,p,q);count=count_injections(m,deadline);brute=brute_gauge_count(m)
        assert count['gauge_fixed_count']==brute
        toy.append({'modulus':q,'period':p,'gauge_fixed_count':brute,'complete_enumeration_equal':True})
    assert toy[0]['gauge_fixed_count']==0 and toy[1]['gauge_fixed_count']==2 and toy[2]['gauge_fixed_count']==falling(6,3)
    symbols=list(dict.fromkeys(''.join(w for _,w in WINDOWS)))
    f=dict(zip(symbols,rng.sample(range(26),len(symbols))))
    tokens=[rng.choice(symbols) for _ in range(97)]
    for start,w in WINDOWS:tokens[start:start+len(w)]=w
    plants=[]
    for name,alphabet in [('AZ',AZ),('KRYPTOS',KR)]:
        for p in range(1,13):
            key=[(7*i+3)%26 for i in range(p)]
            cipher=''.join(alphabet[(f[s]+key[i%p])%26] for i,s in enumerate(tokens))
            inverse={v:s for s,v in f.items()}
            assert ''.join(inverse[(alphabet.index(c)-key[i%p])%26] for i,c in enumerate(cipher))==''.join(tokens)
            row=analyze(cipher,name,p,deadline)
            assert row['training_count']['gauge_fixed_count']>0 and row['full_count']['gauge_fixed_count']>0
            for stage in ('training','full'):
                m=row[stage];shift=f[m['glyphs'][0]]
                vals=[(f[s]-shift)%26 for s in m['glyphs']]+[(-key[i]-shift)%26 for i in range(p)]
                assert contains_description(m,vals)
            for shift in range(26):
                altered=''.join(alphabet[((f[s]+shift)+(key[i%p]-shift))%26] for i,s in enumerate(tokens))
                assert altered==cipher
            plants.append({'alphabet':name,'period':p,'true_description_retained':True,'fixed_model_full_roundtrip':True,
                           'global_translation_gauges_checked':26,'training_count':row['training_count']['gauge_fixed_count'],
                           'full_observed_subset_count':row['full_count']['gauge_fixed_count']})
    return {'complete_small_ring_comparisons':toy,'small_ring_count':len(toy),'translation_symmetry_count_is_two':True,
            'plants':plants,'plant_count':len(plants),'scope':'Counts and truth inclusion, not unique recovery or K4 evidence.'}


def actual():
    d=json.loads((ROOT/'data/k4.json').read_text());deadline=time.monotonic()+120;rows=[]
    for name in ('AZ','KRYPTOS'):
        for period in range(1,13):
            try:rows.append(analyze(d['ciphertext'],name,period,deadline))
            except TimeoutError as exc:rows.append({'alphabet':name,'period':period,'status':'budget_unresolved','reason':str(exc)})
    return {'experiment':'IPA-FREE-MAP-001','canonical_structures':24,'rows':rows,
            'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['data/k4.json','data/ipa-cambridge-us-v1.json','research/IPA-FREE-MAP-SPEC.md','experiments/ipa_free_map.py','experiments/route_key_graph.py']},
            'scope':'Fixed windows and offsets. Free injective values on observed IPA subset; no full codec, decoded message, null significance or new codec search.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('mode',choices=['controls','actual']);args=parser.parse_args()
    result=controls() if args.mode=='controls' else actual();serialized=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if len(serialized.encode())>256*1024*1024:raise MemoryError('retained-result budget')
    print(serialized,end='')
