"""Exact two-round family non-alias certificates and new-only K4 constraints."""
import argparse,hashlib,itertools,json,time
from pathlib import Path
import nonrotor_structural as base
ROOT=base.ROOT;ALPHABETS=(base.AZ,base.KR)

def probes(q=26):
    out=[]
    for k in range(12):
        if k==11:
            values=[];s=7140
            for _ in range(2*q):s=(1664525*s+1013904223)&0xffffffff;values.append(s%q)
            out.append((values[:q],values[q:]));continue
        fn=((lambda x:0,lambda x:0),(lambda x:x,lambda x:x),(lambda x:x*x+3*x+7,lambda x:x*x*x+5*x+11),(lambda x:int(x==0),lambda x:int(x==1)),(lambda x:7*x+3,lambda x:5*x+9),(lambda x:x*x*x+13*x,lambda x:x*x+17),(lambda x:x+1,lambda x:0),(lambda x:0,lambda x:x+1),(lambda x:1,lambda x:2),(lambda x:x*(x+1)//2+3,lambda x:x*x+2*x+1),(lambda x:x*x*x+7*x*x,lambda x:3*x*x+11*x))[k]
        out.append(([fn[0](x)%q for x in range(q)],[fn[1](x)%q for x in range(q)]))
    return out

def labels():return [dict(id=f'{a}-{b}-I{i}-O{o}',ai=ai,ao=ao,input_swap=bool(i),output_swap=bool(o)) for a,ai in zip(('AZ','KR'),ALPHABETS) for b,ao in zip(('AZ','KR'),ALPHABETS) for i,o in itertools.product(range(2),repeat=2)]

def pairmap(p,label,f,g,decrypt=False):
    ai,ao=label['ai'],label['ao'];q=len(ai)
    if not decrypt:
        l,r=[ai.index(x) for x in p]
        if label['input_swap']:l,r=r,l
        x,y=base.encrypt_pair(l,r,f,g,q)
        if label['output_swap']:x,y=y,x
        return ao[x]+ao[y]
    x,y=[ao.index(c) for c in p]
    if label['output_swap']:x,y=y,x
    l,r=base.decrypt_pair(x,y,f,g,q)
    if label['input_swap']:l,r=r,l
    return ai[l]+ai[r]

def crypt(text,label,f,g,origin,decrypt=False):
    out=list(text)
    for i in range(origin-1,len(text)-1,2):out[i:i+2]=pairmap(text[i:i+2],label,f,g,decrypt)
    return ''.join(out)

def rows(cipher,known,label,origin):
    out=[]
    for i in range(origin-1,len(cipher)-1,2):
        l,r=known.get(i),known.get(i+1)
        if l is None and r is None:continue
        l=None if l is None else label['ai'].index(l);r=None if r is None else label['ai'].index(r)
        if label['input_swap']:l,r=r,l
        x,y=[label['ao'].index(c) for c in cipher[i:i+2]]
        if label['output_swap']:x,y=y,x
        out.append(dict(positions=[i+1,i+2],L=l,R=r,X=x,Y=y))
    return out

def full_membership(outputs,label):
    inputs=[''.join(x) for x in itertools.product(base.AZ,repeat=2)]
    text=''.join(outputs);known={i:c for i,c in enumerate(''.join(inputs))}
    return base.infer(rows(text,known,label,1))

def alias_audit():
    started=time.monotonic();ls=labels();ps=probes();inputs=[''.join(x) for x in itertools.product(base.AZ,repeat=2)]
    maps={(l['id'],k):[pairmap(p,l,f,g) for p in inputs] for l in ls for k,(f,g) in enumerate(ps)}
    certs=[];unresolved=[]
    for i,j in itertools.combinations(range(16),2):
        cert=None
        for source,target in ((ls[i],ls[j]),(ls[j],ls[i])):
            for k,(f,g) in enumerate(ps):
                if time.monotonic()-started>30:raise TimeoutError('alias audit unresolved')
                outputs=maps[source['id'],k];check=full_membership(outputs,target)
                if check['key_count']=='0':
                    bad=check['contradictions'][0];witness=[]
                    for pos in (bad['first_source'],bad['second_source']):
                        n=(pos[0]-1)//2;witness.append(dict(physical_input=inputs[n],physical_output=outputs[n]))
                    cert=dict(source=source['id'],target=target['id'],probe=k,F=f,G=g,contradiction=bad,witness_pairs=witness);break
            if cert:break
        if cert:certs.append(cert)
        else:unresolved.append([ls[i]['id'],ls[j]['id']])
    endpoint=[]
    for label in ls:
        found=None
        for k in range(12):
            for p,out in zip(inputs,maps[label['id'],k]):
                if out[0]!=p[0]:found=dict(source_label=label['id'],probe=k,physical_input_pair=p,physical_output_pair=out,reason='Origin1 changes first raw character; every origin2 family copies it.');break
            if found:break
        assert found;endpoint.append(found)
    return dict(raw_labels=32,covered_no_swap_labels=8,new_swap_labels=24,same_origin_base_family_comparisons=120,nonalias_certificates=certs,unresolved_comparisons=unresolved,across_origin_endpoint_witnesses=endpoint,all_32_proved_distinct=not unresolved,proof_scope='Exact family inequality from a full-pair-map counterexample, not disjointness or worldwide novelty. No passing probe is called an alias.')

def actual(audit):
    d=json.loads((ROOT/'data/k4.json').read_text());c=d['ciphertext'];known={i:p for crib in d['cribs'] for i,p in enumerate(crib['plaintext'],crib['start']-1)};out=[]
    for label in labels():
        if not label['input_swap'] and not label['output_swap']:continue
        for origin in (1,2):
            train={i:p for i,p in known.items() if i<34};tr=base.infer(rows(c,train,label,origin));full=base.infer(rows(c,known,label,origin)) if tr['completed'] and tr['branches'] else None
            out.append(dict(label=label,origin=origin,training=tr,second_stage=full,second_stage_evaluated=full is not None,compatible_keys='0' if tr['completed'] and tr['key_count']=='0' else (full['key_count'] if full else None)))
    return dict(new_records=out,old_eight_skipped=True,old_result='results/NONROTOR-STRUCTURAL-004.json',all_32_distinct_proved=audit['all_32_proved_distinct'])

def controls():
    p=list((base.AZ*4)[:97]);p[21:34]='EASTNORTHEAST';p[63:74]='BERLINCLOCK';p=''.join(p);known={i:p[i] for i in list(range(21,34))+list(range(63,74))};plants=[];checks=0
    f,g=probes()[2]
    for label in labels():
        for x in itertools.product(base.AZ,repeat=2):
            pair=''.join(x);assert pairmap(pairmap(pair,label,f,g),label,f,g,True)==pair;checks+=1
        for origin in (1,2):
            c=crypt(p,label,f,g,origin);assert crypt(c,label,f,g,origin,True)==p
            result=base.infer(rows(c,known,label,origin));assert result['completed'] and base.contains(result['branches'],f,g)
            plants.append(dict(label=label['id'],origin=origin,truth_included=True,key_count=result['key_count']))
    return dict(plants=plants,pair_roundtrips=checks)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--audit',action='store_true');ap.add_argument('--controls',action='store_true');ap.add_argument('--actual',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args();out={}
    if a.audit:out['alias_audit']=alias_audit()
    if a.controls:out['controls']=controls()
    if a.actual:
        audited=json.loads((ROOT/'results/FEISTEL-SYMMETRY-005-controls.json').read_text())['alias_audit'];out['actual']=actual(audited)
    out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'research/FEISTEL-EXTENSION-SPEC.md',ROOT/'experiments/nonrotor_structural.py')}
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
