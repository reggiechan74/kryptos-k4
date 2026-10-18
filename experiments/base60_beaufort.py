"""Exact sum-graph solver and parity-first base60 pilot. No third-party code."""
from itertools import product
from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parents[1]

def stream(primer, rule, base=60, length=97):
    d = list(primer); lag = len(d)
    if lag < 2 or rule not in (0,1): raise ValueError('bad recurrence')
    while len(d) < length:
        i = len(d); d.append((d[i-lag] + d[i-lag+1 if rule == 0 else i-1]) % base)
    return d[:length]

def graph_model(vertices, pairs):
    adj = {v:[] for v in vertices}
    for i,(a,b) in enumerate(pairs):
        adj[a].append((b,i));adj[b].append((a,i))
    components=[]; seen=set()
    for root in vertices:
        if root in seen or not adj[root]: continue
        todo=[root]; signs={root:1}; paths={root:[]}; nodes=[]; seen.add(root)
        while todo:
            a=todo.pop(0);nodes.append(a)
            for b,i in adj[a]:
                if b in seen: continue
                seen.add(b); signs[b]=-signs[a]
                # offset(b) = edge_i - offset(a)
                paths[b]=[(i,1)]+[(j,-s) for j,s in paths[a]];todo.append(b)
        edges=[(a,b,i) for i,(a,b) in enumerate(pairs) if a in signs]
        components.append({'root':root,'nodes':nodes,'signs':signs,'paths':paths,'edges':edges})
    return components

def component_options(component, labels, modulus, parity_only=False):
    offsets={v:sum(s*labels[i] for i,s in component['paths'][v]) % modulus for v in component['nodes']}
    roots=set(range(modulus))
    for a,b,i in component['edges']:
        coefficient=component['signs'][a]+component['signs'][b]
        residual=(labels[i]-offsets[a]-offsets[b]) % modulus
        if coefficient == 0:
            if residual: return [],'sum_cycle_contradiction'
        else:
            roots.intersection_update(t for t in range(modulus) if (coefficient*t-residual)%modulus == 0)
        if not roots: return [],'sum_cycle_contradiction'
    roots=sorted(roots)
    if not roots:return [],'sum_cycle_contradiction'
    options=[]
    for t in roots:
        values={v:(component['signs'][v]*t+offsets[v]) % modulus for v in component['nodes']}
        if parity_only or len(set(values.values()))==len(values):options.append(values)
    return options, None if options else 'internal_injectivity_contradiction'

def solve(vertices,pairs,labels,modulus=26,max_states=10000,seconds=.02,model=None):
    started=time.monotonic(); components=graph_model(vertices,pairs) if model is None else model; choices=[]
    for c in components:
        opts,reason=component_options(c,labels,modulus)
        if not opts:return {'status':'local_sum_or_injectivity_contradiction','reason':reason,'states':0}
        choices.append(opts)
    choices.sort(key=lambda x:(len(x),-len(x[0])))
    states=0; capped=False
    def visit(i,used,assignment):
        nonlocal states,capped
        if states >= max_states or time.monotonic()-started > seconds:capped=True;return None
        states+=1
        if i==len(choices):return assignment
        for values in choices[i]:
            residues=set(values.values())
            if residues.isdisjoint(used):
                answer=visit(i+1,used|residues,dict(assignment,**values))
                if answer is not None:return answer
            if capped:return None
        return None
    assignment=visit(0,set(),{})
    if capped:return {'status':'unresolved_resource_cap','states':states}
    if assignment is None:return {'status':'local_compatible_global_contradiction','states':states}
    remaining=iter(sorted(set(range(modulus))-set(assignment.values())))
    for v in vertices:
        if v not in assignment:assignment[v]=next(remaining)
    assert len(assignment)==modulus and len(set(assignment.values()))==modulus
    assert all((assignment[a]+assignment[b]-d)%modulus==0 for (a,b),d in zip(pairs,labels))
    return {'status':'complete_global_alphabet_feasible','alphabet_positions':assignment,'states':states}

def parity_proof(vertices,pairs,labels):
    comps=graph_model(vertices,pairs); choices=[]
    for c in comps:
        opts,reason=component_options(c,labels,2,True)
        if not opts:return {'compatible':False,'reason':reason,'component_root':c['root']}
        choices.append(opts)
    possible={0}; observed=sum(len(c['nodes']) for c in comps)
    for opts in choices:
        possible={n+sum(v==0 for v in x.values()) for n in possible for x in opts}
    balanced=sorted(n for n in possible if n<=13 and observed-n<=13)
    return {'compatible':bool(balanced),'reason':'parity_balance_possible' if balanced else 'too_many_same_parity_for_bijection','possible_observed_even_counts':sorted(possible),'permitted_observed_even_counts':balanced,'observed_letters':observed}

def baseline():
    data=json.loads((ROOT/'data/k4.json').read_text()); positions=[];pairs=[]
    for c in data['cribs']:
        for j,p in enumerate(c['plaintext']):
            i=c['start']-1+j;positions.append(i);pairs.append((p,data['ciphertext'][i]))
    return list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),positions,pairs

def analytical():
    vertices,positions,pairs=baseline(); records=[]
    for lag,rule in [(2,0),(3,0),(3,1),(4,0),(4,1)]:
        masks=[]
        for bits in product(range(2),repeat=lag):
            d=stream(bits,rule,2);result=parity_proof(vertices,pairs,[d[i] for i in positions]);masks.append({'primer_parity':list(bits),'primers_represented':30**lag,**result})
        records.append({'lag':lag,'rule':rule,'nominal_rule_multiplicity':2 if lag==2 else 1,'total_primers':60**lag,'parity_masks':masks,'parity_eliminated_primers':sum(x['primers_represented'] for x in masks if not x['compatible'])})
    return records

def eligible_primers(record):
    """Merge mask classes in ascending original base60 integer-code order."""
    import heapq
    def one(mask):
        for digits in product(range(30),repeat=record['lag']):
            primer=tuple(2*d+b for d,b in zip(digits,mask));code=0
            for d in primer:code=60*code+d
            yield code,primer
    return heapq.merge(*(one(m['primer_parity']) for m in record['parity_masks'] if m['compatible']))

def run_bounded(spec_commit,code_commit):
    import collections,datetime,hashlib,platform
    started=time.monotonic(); vertices,positions,pairs=baseline();model=graph_model(vertices,pairs)
    assert len(model)==1 and len(model[0]['nodes'])==21
    proofs=analytical(); records=[];iterators=[]
    for x in proofs:
        n=x['total_primers']-x['parity_eliminated_primers']
        records.append({'lag':x['lag'],'rule':x['rule'],'nominal_rule_multiplicity':x['nominal_rule_multiplicity'],'parity_rejected':x['parity_eliminated_primers'],'remaining_after_parity':n,'evaluated':0,'next_original_code':None,'last_original_code':None,'classifications':{},'complete':n==0})
        iterators.append(iter(eligible_primers(x)))
    counts=[collections.Counter() for x in proofs];witnesses=[];unresolved=[];total=0;pilot=None
    while total<100000 and time.monotonic()-started<30:
        progress=False
        for j,it in enumerate(iterators):
            if records[j]['complete']:continue
            if total>=100000 or time.monotonic()-started>=30:break
            try:code,primer=next(it)
            except StopIteration:records[j]['complete']=True;continue
            progress=True;d=stream(primer,proofs[j]['rule']);labels=[d[i]%26 for i in positions]
            # Trivial necessary sum-graph constraints; do not classify survivors as feasible.
            if d[32]%2 or d[73]%2 or (d[27]-d[65])%26:
                result={'status':'local_sum_or_injectivity_contradiction','reason':'self_loop_parity_or_duplicate_edge'}
            else:result=solve(vertices,pairs,labels,model=model)
            status=result['status'];counts[j][status]+=1;records[j]['evaluated']+=1;records[j]['last_original_code']=code;total+=1
            if status=='complete_global_alphabet_feasible':witnesses.append({'lag':proofs[j]['lag'],'rule':proofs[j]['rule'],'code':code,'primer':list(primer),**result})
            if status=='unresolved_resource_cap':unresolved.append({'lag':proofs[j]['lag'],'rule':proofs[j]['rule'],'code':code})
            if total==4096:
                pilot={'evaluated':total,'elapsed_seconds':round(time.monotonic()-started,6),'max_pilot_seconds':5}
                if pilot['elapsed_seconds']>=5:break
        if pilot and pilot['elapsed_seconds']>=5:break
        if not progress:break
    for j,it in enumerate(iterators):
        records[j]['classifications']=dict(counts[j])
        if not records[j]['complete']:
            try:records[j]['next_original_code']=next(it)[0]
            except StopIteration:records[j]['complete']=True
    elapsed=time.monotonic()-started
    files=['experiments/base60_beaufort.py','tests/test_base60_beaufort.py','data/k4.json','research/specifications/BASE60-BEAUFORT-001.json']
    return {'experiment':'BASE60-BEAUFORT-001','spec_commit':spec_commit,'code_commit':code_commit,'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'file_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files},'nominal_labeled_tuples':2*sum(60**n for n in (2,3,4)),'unique_tuples':60**2+2*60**3+2*60**4,'parity_proofs':proofs,'configurations':records,'pilot':pilot,'evaluated_after_parity':total,'elapsed_seconds':round(elapsed,6),'status':'complete' if all(x['complete'] for x in records) and not unresolved else 'verified_partial','complete_alphabet_witnesses':witnesses,'unresolved':unresolved,'full_plaintexts_emitted':False,'independent_math_audit':'Received/reconciled: one21-letter component, five unused letters, all parity survivor masks independently matched; noninvertible2x constraints enumerated. Four specialized modular equations not used for pruning beyond self-loop parity and duplicated R-P edge.'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--spec-commit',required=True);p.add_argument('--code-commit',required=True);args=p.parse_args()
    print(json.dumps(run_bounded(args.spec_commit,args.code_commit),indent=2))
