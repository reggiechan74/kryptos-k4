"""Independent compact full-set truth for full-contact toy controllers.
Uses physical schedules/seed enumeration, not production index classes or predicates.
"""
import hashlib,itertools,json
from pathlib import Path
import sigaba_joint_toy_oracle as physical

def pop(x):return bin(x).count('1')
def compact_domains(f,observations,guard):
    q,r=f['q'],f['r']
    if set(f['pulses'])!=set(range(q)):raise ValueError('Full-contact symmetry is not established for this fixture')
    domains={};checks=0
    for index in itertools.product(range(2*r),repeat=2):
        # Control-bank inverse is a permutation, so the full input set remains full.
        chosen=physical.physical_mask(f,[0]*r,index);domain=0
        for number,seed in enumerate(itertools.product(range(q),repeat=r)):
            guard();ok=True;checks+=1
            for t,p,c in observations:
                x=p
                for j in range(r):x=physical.wire(f['cipher'][j],(seed[j]-(t if j in chosen else 0))%q,x)
                if x!=c:ok=False;break
            if ok:domain|=1<<number
        if domain:domains[index]=domain
    return domains,checks

def emit_rows(f,lookup,path,guard,limit_error,controller_prefix=None,rowcap=2000000,bytecap=256<<20):
    q,r=f['q'],f['r'];rows=0;count=0;size=0;dig=hashlib.sha256()
    with Path(path).open('wb') as out:
        for controller_number,control in enumerate(itertools.product(range(q),repeat=r)):
            if controller_prefix is not None and controller_number>=controller_prefix:break
            for index in itertools.product(range(2*r),repeat=2):
                guard();domain=lookup(control,index)
                if not domain:continue
                raw=json.dumps([list(control),list(index),hex(domain)],separators=(',',':')).encode()+b'\n';rows+=1;size+=len(raw)
                if rows>rowcap or size>bytecap:raise limit_error('canonical_output_budget_unresolved')
                count+=pop(domain);out.write(raw);dig.update(raw)
    return dict(rows=rows,raw_key_count=str(count),bytes=size,sha256=dig.hexdigest(),controller_prefix=controller_prefix)

def truth_rows(f,observations,path,guard,limit_error):
    domains,checks=compact_domains(f,observations,guard);r=emit_rows(f,lambda control,index:domains.get(index,0),path,guard,limit_error);r['direct_cipher_seed_checks']=checks;r['full_contact_symmetry']=True;return r
