"""Exact arbitrary-function three-round inference via weighted component packing."""
import argparse,copy,hashlib,itertools,json,math,time
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
import nonrotor_structural as base
ROOT=base.ROOT

def enc(l,r,key,q=26):
    a=(l+key['F'][r])%q;x=(r+key['G'][a])%q;return x,(a+key['H'][x])%q

def dec(x,y,key,q=26):
    a=(y-key['H'][x])%q;r=(x-key['G'][a])%q;return (a-key['F'][r])%q,r

def crypt(text,key,ai=base.AZ,ao=base.AZ,decrypt=False):
    out=list(text)
    for i in range(0,len(text)-1,2):
        if decrypt:l,r=dec(ao.index(text[i]),ao.index(text[i+1]),key);out[i:i+2]=[ai[l],ai[r]]
        else:x,y=enc(ai.index(text[i]),ai.index(text[i+1]),key);out[i:i+2]=[ao[x],ao[y]]
    return ''.join(out)

def graph(rows,q):
    adj=defaultdict(list)
    for k,row in enumerate(rows):
        if row['R'] is None:raise ValueError('canonical audit requires every partial pair to have known right input; not an exclusion of other frames')
        h='Q:'+str(row['X']);adj[h]
        if row['L'] is not None:
            f='F:'+str(row['R']);delta=(row['Y']-row['L'])%q
            adj[h].append((f,delta,k));adj[f].append((h,-delta%q,k))
    pot={};which={};comps=[]
    for root in sorted(adj):
        if root in pot:continue
        pot[root]=0;todo=[root];nodes=[];ci=len(comps)
        while todo:
            node=todo.pop(0);nodes.append(node);which[node]=ci
            for target,delta,rowid in adj[node]:
                value=(pot[node]+delta)%q
                if target not in pot:pot[target]=value;todo.append(target)
                elif pot[target]!=value:return dict(consistent=False,contradiction=dict(kind='F/Q cycle',row=rowid,node=target,assigned=pot[target],required=value))
        comps.append(dict(root=root,potentials={n:pot[n] for n in sorted(nodes)},points=[]))
    for row in rows:
        node='Q:'+str(row['X']);comps[which[node]]['points'].append(dict(a=(row['Y']+pot[node])%q,b=(row['X']-row['R'])%q,positions=row['positions']))
    for component in comps:
        seen={};points=[]
        for point in component['points']:
            if point['a'] in seen and seen[point['a']]['b']!=point['b']:return dict(consistent=False,contradiction=dict(kind='within-component G input collision',first=seen[point['a']],second=point))
            if point['a'] not in seen:seen[point['a']]=point;points.append(point)
        component['points']=points
    return dict(consistent=True,components=comps,observed_F=sum(n.startswith('F:') for n in adj),observed_H=sum(n.startswith('Q:') for n in adj),equations=len([r for r in rows if r['L'] is not None]))

@lru_cache(None)
def stirling(n,k):
    if n==k==0:return 1
    if not n or not k or k>n:return 0
    return stirling(n-1,k-1)+k*stirling(n-1,k)

def singleton_weight(single_labels,occupied,q):
    poly=[1];used=Counter(occupied.values())
    for label,m in sorted(single_labels.items()):
        c=used[label]
        factor=[sum(math.comb(m,l)*c**(m-l)*stirling(l,k) for l in range(k,m+1)) for k in range(m+1)]
        out=[0]*(len(poly)+m)
        for i,x in enumerate(poly):
            for j,y in enumerate(factor):out[i+j]+=x*y
        poly=out
    free=q-len(occupied);weight=0
    for k,coef in enumerate(poly):
        if k<=free:weight+=coef*math.prod(range(free-k+1,free+1))*q**(free-k)
    return weight

def witness(g,offsets,singles,occupied,q):
    offsets=offsets.copy();gm=occupied.copy()
    for ci in singles:
        point=g['components'][ci]['points'][0];choices=[x for x,y in gm.items() if y==point['b']]
        x=min(choices) if choices else next(x for x in range(q) if x not in gm)
        gm[x]=point['b'];offsets[ci]=(x-point['a'])%q
    key={name:[0]*q for name in ('F','G','H')}
    for ci,component in enumerate(g['components']):
        for node,pot in component['potentials'].items():
            index=int(node[2:]);value=(pot+offsets[ci])%q
            key['F' if node[0]=='F' else 'H'][index]=value if node[0]=='F' else -value%q
    for x,y in gm.items():key['G'][x]=y
    return key

def count(rows,q=26,seconds=10,cap=1000000):
    start=time.monotonic();g=graph(rows,q)
    if not g['consistent']:return dict(completed=True,status='impossible',raw_key_count='0',gauge_fixed_key_count='0',graph=g,witness=None)
    if not rows:return dict(completed=True,status='compatible',raw_key_count=str(q**(3*q)),gauge_fixed_key_count=str(q**(3*q-1)),graph=g,witness={name:[0]*q for name in ('F','G','H')},anchor=None,core_assignments=0)
    comps=g['components'];anchor=max(range(len(comps)),key=lambda i:(len(comps[i]['points']),-i));core=[i for i,c in enumerate(comps) if i!=anchor and len(c['points'])>1];singles=[i for i,c in enumerate(comps) if i!=anchor and len(c['points'])==1]
    total_assignments=q**len(core)
    if total_assignments>cap:return dict(completed=False,status='budget_unresolved',raw_key_count=None,graph=g,anchor=anchor,required_core_assignments=total_assignments,witness=None)
    labels=Counter(comps[i]['points'][0]['b'] for i in singles);s=0;example=None;tested=0;freeFH=2*q-g['observed_F']-g['observed_H']
    for values in itertools.product(range(q),repeat=len(core)):
        if time.monotonic()-start>seconds:return dict(completed=False,status='budget_unresolved',raw_key_count=None,graph=g,anchor=anchor,core_assignments=tested,witness=None)
        tested+=1;offsets={anchor:0,**dict(zip(core,values))};gm={};bad=False
        for ci in [anchor]+core:
            for point in comps[ci]['points']:
                x=(point['a']+offsets[ci])%q
                if x in gm and gm[x]!=point['b']:bad=True;break
                gm[x]=point['b']
            if bad:break
        if bad:continue
        w=singleton_weight(labels,gm,q)
        s+=w*q**freeFH
        if w and example is None:example=witness(g,offsets,singles,gm,q)
    if example is not None:
        for row in rows:
            l,r=dec(row['X'],row['Y'],example,q);assert r==row['R'] and (row['L'] is None or l==row['L'])
    return dict(completed=True,status='compatible' if s else 'impossible',raw_key_count=str(q*s),gauge_fixed_key_count=str(s),graph=g,anchor=anchor,core_assignments=tested,singleton_components=len(singles),free_F_H_entries=freeFH,witness=example,count_semantics='Complete F/G/H parameter descriptions. One global translation gauge removed then restored. Not distinct cipher functions or 97-character plaintexts.')

def key_matches(rows,key,q):
    return all((r['L'] is None or dec(r['X'],r['Y'],key,q)[0]==r['L']) and dec(r['X'],r['Y'],key,q)[1]==r['R'] for r in rows)

def controls():
    cases=[]
    for q,v in itertools.product((2,3),range(4)):
        key=dict(F=[(x*x+v)%q for x in range(q)],G=[(x*x*x+x+v)%q for x in range(q)],H=[(2*x+v)%q for x in range(q)])
        rows=[]
        for i,(l,r) in enumerate(((0,1),(1,0),(1,1))):
            l%=q;r%=q;x,y=enc(l,r,key,q);rows.append(dict(L=None if i==1 else l,R=r,X=x,Y=y,positions=[2*i+1,2*i+2]))
        result=count(rows,q);brute=normalized=0;anchor=result.get('anchor');root=result['graph']['components'][anchor]['root'] if anchor is not None else None
        for f,g,h in itertools.product(itertools.product(range(q),repeat=q),repeat=3):
            k=dict(F=f,G=g,H=h)
            if key_matches(rows,k,q):
                brute+=1
                value=f[int(root[2:])] if root and root[0]=='F' else (-h[int(root[2:])]%q if root else f[0])
                normalized+=int(value==0)
        assert int(result['raw_key_count'])==brute and int(result['gauge_fixed_key_count'])==normalized
        cases.append(dict(q=q,case=v,raw_keys=brute,gauge_fixed_keys=normalized,complete_enumeration_equal=True))
    weighted=[]
    q=4
    for v in range(4):
        key=dict(F=[(x*x+v)%q for x in range(q)],G=[(x*x*x+v)%q for x in range(q)],H=[(x+v)%q for x in range(q)]);rows=[]
        for i,(l,r) in enumerate(((0,1),(1,2),(2,1))):
            x,y=enc(l,r,key,q);rows.append(dict(L=None if i==1 else l,R=r,X=x,Y=y,positions=[2*i+1,2*i+2]))
        result=count(rows,q);total=0
        for f,h in itertools.product(itertools.product(range(q),repeat=q),repeat=2):
            gm={};bad=False
            for row in rows:
                a=(row['Y']-h[row['X']])%q
                if row['L'] is not None and (a-f[row['R']])%q!=row['L']:bad=True;break
                value=(row['X']-row['R'])%q
                if a in gm and gm[a]!=value:bad=True;break
                gm[a]=value
            if not bad:total+=q**(q-len(gm))
        assert total==int(result['raw_key_count']);weighted.append(dict(case=v,raw_keys=total,independent_F_H_enumeration_equal=True))
    # Independent weighted enumeration with two multi-point components.
    rows=[dict(L=l,R=r,X=x,Y=y,positions=[2*i+1,2*i+2]) for i,(l,r,x,y) in enumerate(((0,0,0,0),(1,0,1,1),(1,1,2,2),(2,1,3,3)))]
    result=count(rows,4);total=0
    for f,h in itertools.product(itertools.product(range(4),repeat=4),repeat=2):
        gm={};bad=False
        for row in rows:
            a=(row['Y']-h[row['X']])%4
            if (a-f[row['R']])%4!=row['L']:bad=True;break
            value=(row['X']-row['R'])%4
            if a in gm and gm[a]!=value:bad=True;break
            gm[a]=value
        if not bad:total+=4**(4-len(gm))
    assert total==int(result['raw_key_count']) and result['core_assignments']==4
    weighted.append(dict(case='two-multi-point-components',raw_keys=total,independent_F_H_enumeration_equal=True))
    singleton_checks=[]
    for q,v in itertools.product((2,3,4,6),range(4)):
        occupied={i:(2*i+v)%q for i in range(v%q)};labels=Counter((v+j)%q for j in range(1+v));total=0
        for gg in itertools.product(range(q),repeat=q):
            if all(gg[i]==y for i,y in occupied.items()):
                frequencies=Counter(gg);total+=math.prod(frequencies[label]**m for label,m in labels.items())
        assert singleton_weight(labels,occupied,q)==total;singleton_checks.append(dict(q=q,case=v,exact_weight=total))
    assert count([],3)['raw_key_count']==str(3**9)
    bad=[dict(L=None,R=0,X=0,Y=0,positions=[1,2]),dict(L=None,R=1,X=0,Y=0,positions=[3,4])];assert count(bad,3)['raw_key_count']=='0'
    plants=[];pairchecks=0;p=list((base.AZ*4)[:97]);p[21:34]='EASTNORTHEAST';p[63:74]='BERLINCLOCK';p=''.join(p)
    for ai,ao in itertools.product((base.AZ,base.KR),repeat=2):
        key=dict(F=[(x*x+3*x+7)%26 for x in range(26)],G=[(x*x*x+13*x+2)%26 for x in range(26)],H=[(5*x*x+x+11)%26 for x in range(26)])
        for l,r in itertools.product(range(26),repeat=2):assert dec(*enc(l,r,key),key)==(l,r);pairchecks+=1
        c=crypt(p,key,ai,ao);assert crypt(c,key,ai,ao,True)==p;known={i:ai.index(p[i]) for i in list(range(21,34))+list(range(63,74))};rows=base.pairs([ao.index(x) for x in c],known,1);result=count(rows)
        assert result['completed'] and int(result['raw_key_count'])>0 and key_matches(rows,key,26) and key_matches(rows,result['witness'],26)
        plants.append(dict(input=ai,output=ao,truth_included=True,raw_key_count=result['raw_key_count']))
    return dict(full_small_function_enumerations=cases,weighted_mod4_full_F_H_enumerations=weighted,singleton_weight_independent_enumerations=singleton_checks,literal_crib_plants=plants,pair_roundtrips=pairchecks,zero_observation_count=True,incompatible_mutation_rejected=True)

def actual():
    d=json.loads((ROOT/'data/k4.json').read_text());c=d['ciphertext'];rawknown={i:p for crib in d['cribs'] for i,p in enumerate(crib['plaintext'],crib['start']-1)};out=[]
    for ai,ao in itertools.product((base.AZ,base.KR),repeat=2):
        cv=[ao.index(x) for x in c];known={i:ai.index(p) for i,p in rawknown.items()};train={i:p for i,p in known.items() if i<34};tr=count(base.pairs(cv,train,1));full=count(base.pairs(cv,known,1)) if tr['completed'] and tr['raw_key_count']!='0' else None;certificates=[]
        if full and full['completed'] and full['witness']:
            key=full['witness'];p=crypt(c,key,ai,ao,True);assert crypt(p,key,ai,ao)==c and all(p[i]==x for i,x in rawknown.items())
            certificates.append(dict(kind='arbitrary_crib_fit_not_solution',key=key,plaintext=p,regeneration_verified=True))
            usedH={int(n[2:]) for comp in full['graph']['components'] for n in comp['potentials'] if n.startswith('Q:')};usedF={int(n[2:]) for comp in full['graph']['components'] for n in comp['potentials'] if n.startswith('F:')}
            for i in range(0,96,2):
                alternate=copy.deepcopy(key);x,y=cv[i:i+2]
                if x not in usedH:alternate['H'][x]=(alternate['H'][x]+1)%26
                else:
                    _,r=dec(x,y,key)
                    if r in usedF:continue
                    alternate['F'][r]=(alternate['F'][r]+1)%26
                p2=crypt(c,alternate,ai,ao,True)
                if p2!=p and all(p2[j]==v for j,v in rawknown.items()):
                    assert crypt(p2,alternate,ai,ao)==c;certificates.append(dict(kind='distinct_compatible_plaintext_ambiguity_witness',key=alternate,plaintext=p2,regeneration_verified=True));break
        out.append(dict(input_alphabet=ai,output_alphabet=ao,origin=1,training=tr,all_cribs=full,plaintext_witnesses=certificates,independently_unseen_plaintext_checks=0,first_stage_marginal_predictions_not_computed=True))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--controls',action='store_true');ap.add_argument('--actual',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args();out={}
    if a.controls:out['controls']=controls()
    if a.actual:out['actual']=actual()
    out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'research/FEISTEL-EXTENSION-SPEC.md',ROOT/'experiments/nonrotor_structural.py')}
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
