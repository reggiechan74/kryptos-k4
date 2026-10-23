"""Exact split-path full cipher-state inference for frozen CSP-889 schedules."""
import argparse,hashlib,itertools,json,time
from collections import defaultdict,Counter
from pathlib import Path
import sigaba_csp889 as sig
ROOT=sig.ROOT;SPEC=ROOT/'research/SIGABA-CSP889-STATE-SPEC.md'


def join_states(plain,cipher,group,t,n=26,deadline=float('inf')):
    """Every compatible five-start tuple occurs exactly once in this Cartesian join."""
    delta=group['states'];order=sig.LAYOUTS[group['layout']][0]
    fw=[t['large'][w-1][0][0] for w in order];bw=[t['large'][w-1][0][1] for w in order]
    locations=list(plain)[:3];left=defaultdict(list);right_halves=0
    for a,b in itertools.product(range(n),repeat=2):
        values=[fw[1][(b+delta[i][1])%n][fw[0][(a+delta[i][0])%n][plain[i]]] for i in locations]
        left[tuple(values)].append((a,b))
    for e,d in itertools.product(range(n),repeat=2):
        if time.monotonic()>deadline:raise TimeoutError('state selector budget-unresolved')
        values=[bw[3][(d+delta[i][3])%n][bw[4][(e+delta[i][4])%n][cipher[i]]] for i in locations]
        for c in range(n):
            target=tuple(bw[2][(c+delta[i][2])%n][x] for i,x in zip(locations,values))
            for a,b in left.get(target,()):yield (a,b,c,d,e)


def enc_letter(x,i,seed,group,t,n=26):
    for j,w in enumerate(sig.LAYOUTS[group['layout']][0]):x=t['large'][w-1][0][0][(seed[j]+group['states'][i][j])%n][x]
    return x


def selector(cipher,prepared,groups=None,budget=180):
    d,t,all_groups=prepared;groups=all_groups if groups is None else groups;cv=[sig.AZ.index(x) for x in cipher]
    first={i:sig.AZ.index(x) for i,x in enumerate('EASTNORTHEAST',21)};second={i:sig.AZ.index(x) for i,x in enumerate('BERLINCLOCK',63)}
    deadline=time.monotonic()+budget;records=[];survivors=[];first_survivors=[];dig=hashlib.sha256();joined=0;complete=True;reason=None
    for group_id,group in enumerate(groups):
        hist=Counter();hits=0;firsts=0;after=0
        try:
            for seed in join_states(first,cv,group,t,deadline=deadline):
                hits+=1;joined+=1;bad=None
                for i,x in list(first.items())[3:]:
                    expected=enc_letter(x,i,seed,group,t)
                    if expected!=cv[i]:bad=(i+1,expected,cv[i]);hist[str(i+1)]+=1;break
                dig.update(json.dumps([group_id,list(seed),bad],separators=(',',':')).encode()+b'\n')
                if bad:continue
                firsts+=1;first_survivors.append(dict(group=group_id,layout=group['layout'],aliases=group['aliases'],cipher_starts=list(seed)))
                for i,x in second.items():
                    expected=enc_letter(x,i,seed,group,t)
                    if expected!=cv[i]:bad=(i+1,expected,cv[i]);break
                if bad:continue
                after+=1;q,r=group['aliases'][0];key=sig.key(group['layout'],0,q,r);key['cipherposition']=''.join(sig.AZ[x] for x in seed)
                p=sig.Machine(key,d,t).crypt(cipher,True);assert sig.Machine(key,d,t).crypt(p)==cipher
                survivors.append(dict(key=key,aliases=group['aliases'],plaintext=p))
        except TimeoutError as error:
            complete=False;reason=str(error)
        records.append(dict(group=group_id,layout=group['layout'],aliases=group['aliases'],covered_cipher_starts=26**5 if complete else None,three_letter_joined_starts=hits,first_conflict_histogram=dict(hist),first_crib_survivors=firsts,all_crib_survivors=after,completed=complete))
        if not complete:break
    return dict(completed=complete,reason=reason,schedules_completed=sum(r['completed'] for r in records),schedules_requested=len(groups),raw_state_descriptions_covered=sum(26**5*len(r['aliases']) for r in records if r['completed']),left_pairs_evaluated=sum(r['completed'] for r in records)*26**2,right_triples_evaluated=sum(r['completed'] for r in records)*26**3,three_letter_joined_starts=joined,first_stage_survivors=first_survivors,full_survivors=survivors,distinct_surviving_plaintexts=len({r['plaintext'] for r in survivors}),conflict_stream_sha256=dig.hexdigest(),records=records)


def direct_fixed(plain,cipher,group,t,n=26,deadline=float('inf')):
    found=[]
    for seed in itertools.product(range(n),repeat=5):
        if time.monotonic()>deadline:raise TimeoutError('direct control comparison budget-unresolved')
        if all(enc_letter(x,i,seed,group,t,n)==cipher[i] for i,x in plain.items()):found.append(seed)
    return set(found)


def toy_tables(n):
    # Declared toy permutations; not historical machines. Preserve ambiguous solutions.
    tables=[]
    for j in range(5):
        w=[((1 if j%2==0 else -1)*x+j+1)%n for x in range(n)]
        f=[[(w[(x+p)%n]-p)%n for x in range(n)] for p in range(n)]
        tables.append([(f,[[row.index(x) for x in range(n)] for row in f])])
    return {'large':tables}


def controls(prepared):
    d,t,groups=prepared;small=[]
    # Layout1 uses physical wheels1..5, so it is compatible with these five toy tables.
    for n,v in itertools.product((2,3,4,6),range(4)):
        tt=toy_tables(n);g=dict(layout=1,states=[tuple(((j+1)*i+i*i+v*j)%n for j in range(5)) for i in range(7)])
        p={i:(i*i+v)%n for i in range(7)};seed=tuple((j+v)%n for j in range(5));c=[enc_letter(x,i,seed,g,tt,n) for i,x in p.items()]
        a={s for s in join_states(p,c,g,tt,n) if all(enc_letter(x,i,s,g,tt,n)==c[i] for i,x in p.items())};b=direct_fixed(p,c,g,tt,n)
        assert a==b and seed in a
        z=dict(layout=1,states=[(0,0,0,0,0)]*7);pp={i:(i%2)%n for i in range(7)};bad=[enc_letter(x,i,seed,z,tt,n) for i,x in pp.items()];bad[2]=(bad[0]+1)%n
        assert not {s for s in join_states(pp,bad,z,tt,n) if all(enc_letter(x,i,s,z,tt,n)==bad[i] for i,x in pp.items())}
        small.append(dict(modulus=n,case=v,complete_set_size=len(a),true_state_included=True,mutation_rejected=True))
    p=list((sig.AZ*4)[:97]);p[21:34]='EASTNORTHEAST';p[63:74]='BERLINCLOCK';p=''.join(p);plants=[]
    for i,(layout,q,r,seed) in enumerate(((0,0,0,(0,25,1,24,2)),(1,25,9,(25,0,24,1,23)),(0,14,3,(7,11,13,17,19)),(1,2,4,(2,3,5,7,11)))):
        key=sig.key(layout,0,q,r);key['cipherposition']=''.join(sig.AZ[x] for x in seed);c=sig.Machine(key,d,t).crypt(p)
        chosen=groups if i<2 else [g for g in groups if g['layout']==layout and [q,r] in g['aliases']]
        result=selector(c,prepared,chosen);assert result['completed'];assert any(row['key']==key and row['plaintext']==p for row in result['full_survivors'])
        plants.append(dict(key=key,selector_schedules=len(chosen),truth_included=True,compatible_keys=len(result['full_survivors']),distinct_plaintexts=result['distinct_surviving_plaintexts']))
    # Exact 26^5 direct control, one schedule only, limited to its first three constraints.
    g=groups[0];seed=(3,5,7,11,13);pp={21:4,22:0,23:18};cv=[0]*97
    for i,x in pp.items():cv[i]=enc_letter(x,i,seed,g,t)
    joined=set(join_states(pp,cv,g,t));started=time.monotonic();brute=direct_fixed(pp,cv,g,t,deadline=started+180);assert joined==brute and seed in joined
    return dict(complete_toy_comparisons=small,literal_crib_plants=plants,direct_26_power_5_comparison=dict(schedules=1,raw_starts=26**5,compatible_states=len(brute),sets_equal=True),known_external_reference_vectors=12)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--controls',action='store_true');ap.add_argument('--actual',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args();prepared=sig.prepare();out={}
    if a.controls:out['controls']=controls(prepared)
    if a.actual:out['actual']=selector(json.loads((ROOT/'data/k4.json').read_text())['ciphertext'],prepared)
    out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),SPEC,ROOT/'experiments/sigaba_csp889.py',ROOT/'data/sigaba-csp889-v1.json',ROOT/'data/k4.json')}
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
