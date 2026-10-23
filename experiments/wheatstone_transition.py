"""Source-grounded reversible processed-stream cryptograph and key-free invariant."""
import argparse,hashlib,itertools,json,math,random,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';SPEC='research/WHEATSTONE-TRANSITION-SPEC.md'

def validate(outer,inner):
    if len(outer)!=len(set(outer)) or len(inner)!=len(set(inner)) or len(outer)!=len(inner)+1:raise ValueError('Unequal rings must have distinct labels and sizes n+1/n')

def crypt(text,outer,inner,o=0,q=0,decrypt=False):
    validate(outer,inner);m,n=len(outer),len(inner);out=[];trace=[]
    for c in text:
        if decrypt:
            target=inner.index(c);d=(target-q)%n or n;o=(o+d)%m;q=target;value=outer[o]
        else:
            target=outer.index(c);d=(target-o)%m
            if not d:raise ValueError('Unprepared repeated plaintext symbol or repeated initial pointer symbol')
            o=target;q=(q+d)%n;value=inner[q]
        out.append(value);trace.append(dict(input=c,output=value,outer=o,inner=q,steps=d))
    return ''.join(out),trace

def tooth_oracle(text,outer,inner,o=0,q=0,decrypt=False):
    out=[]
    for c in text:
        ring=inner if decrypt else outer;position=q if decrypt else o
        if not decrypt and ring[position]==c:raise ValueError('unprepared repeat')
        for _ in range(len(outer)):
            o=(o+1)%len(outer);q=(q+1)%len(inner)
            if (inner[q] if decrypt else outer[o])==c:break
        else:raise AssertionError('unreachable symbol')
        out.append(outer[o] if decrypt else inner[q])
    return ''.join(out)

def constraints(plaintext,ciphertext,start=1):
    if len(plaintext)!=len(ciphertext):raise ValueError('Processed/cipher spans must align')
    groups={};cert=[]
    for i in range(len(plaintext)-1):
        pair=plaintext[i:i+2];equal=ciphertext[i]==ciphertext[i+1];item=dict(positions=[start+i,start+i+1],plaintext_pair=pair,ciphertext_pair=ciphertext[i:i+2],equal_cipher=equal)
        if pair in groups and groups[pair]['equal_cipher']!=equal:cert.append(dict(kind='same_processed_plaintext_pair_opposed_cipher_equality',first=groups[pair],second=item))
        groups.setdefault(pair,item)
    return dict(compatible_necessary_condition=not cert,certificates=cert,ordered_pair_classes=groups)

def toy_controls():
    start=time.monotonic();comparisons=0;rows=[]
    for m in range(3,7):
        n=m-1;alphabet=tuple(range(m));outer_orders=0;inner_orders=math.factorial(n-1)
        for tail in itertools.permutations(range(1,m)):
            outer=(0,)+tail;outer_orders+=1
            for tail2 in itertools.permutations(range(1,n)):
                inner=(0,)+tail2
                for u,v in itertools.permutations(alphabet,2):
                    d=(outer.index(v)-outer.index(u))%m;flags=[]
                    for q in range(n):
                        if comparisons>=2000000 or time.monotonic()-start>120:raise TimeoutError('toy control budget unresolved')
                        equal=inner[q]==inner[(q+d)%n];assert equal==(d%n==0);flags.append(equal);comparisons+=1
                    assert len(set(flags))==1
        rows.append(dict(outer_size=m,inner_size=n,outer_rotation_representatives=outer_orders,inner_rotation_representatives=inner_orders,represented_outer_permutations=math.factorial(m),represented_inner_permutations=math.factorial(n),all_inner_states=True))
    naive=[]
    for m in (3,4):
        n=m-1;count=0;positive=0
        for outer,inner in itertools.product(itertools.permutations(range(m)),itertools.permutations(range(n))):
            for u,v in itertools.permutations(range(m),2):
                d=(outer.index(v)-outer.index(u))%m
                for q in range(n):
                    flag=inner[q]==inner[(q+d)%n];assert flag==(d%n==0);count+=1;positive+=flag
        # Each ring has exactly m ordered distinct pairs at distance n.
        expected=math.factorial(m)*math.factorial(n)*m*n;assert positive==expected
        naive.append(dict(outer_size=m,comparisons=count,equality_events=positive))
    return dict(rotation_quotient_rows=rows,state_transition_comparisons=comparisons,naive_complete_size3_size4=naive,rotation_is_coordinate_gauge=True)

def controls():
    refs=json.loads((ROOT/'data/wheatstone-reference-vectors.json').read_text());vectors=[]
    for v in refs['vectors']:
        args=(v['outer'],v['inner'],v['initial_outer'],v['initial_inner']);c,t=crypt(v['processed_message'],*args);p,dt=crypt(v['ciphertext'],*args,decrypt=True)
        assert c==v['ciphertext'] and p==v['processed_message'];assert tooth_oracle(p,*args)==c and tooth_oracle(c,*args,decrypt=True)==p
        vectors.append(dict(source=v['source'],ciphertext=c,processed_plaintext=p,trace=t,external_known_answer_pass=True))
    repeated,tr=crypt('BA','_'+AZ,AZ);assert repeated[0]==repeated[1] and tr[1]['steps']==26;assert crypt(repeated,'_'+AZ,AZ,decrypt=True)[0]=='BA'
    rejected=False
    try:crypt('AA','_'+AZ,AZ)
    except ValueError:rejected=True
    assert rejected
    rng=random.Random(80023);plants=[]
    for k in range(24):
        def segment(n,previous,last_forbidden=None):
            text=''
            for i in range(n):text+=rng.choice([c for c in AZ if c!=(text[-1] if text else previous) and (i<n-1 or c!=last_forbidden)])
            return text
        p=segment(21,'_',last_forbidden='E')+'EASTNORTHEAST'+segment(29,'T',last_forbidden='B')+'BERLINCLOCK'+segment(23,'K');outer=list('_'+AZ);inner=list(AZ);rng.shuffle(outer);rng.shuffle(inner);outer=''.join(outer);inner=''.join(inner);o=rng.choice([i for i,c in enumerate(outer) if c!=p[0]]);q=rng.randrange(26)
        c,trace=crypt(p,outer,inner,o,q);assert len(p)==97 and crypt(c,outer,inner,o,q,True)[0]==p;assert tooth_oracle(p,outer,inner,o,q)==c and tooth_oracle(c,outer,inner,o,q,True)==p
        r=constraints(p[21:34],c[21:34],22);assert r['compatible_necessary_condition']
        mutated=list(c);mutated[33]=c[32] if c[32]!=c[33] else next(x for x in AZ if x!=c[32]);assert not constraints(p[21:34],''.join(mutated)[21:34],22)['compatible_necessary_condition']
        plants.append(dict(outer=outer,inner=inner,initial_outer=o,initial_inner=q,continuous_plaintext=p,ciphertext=c,full_roundtrip=True,invariant_accepts=True,opposed_equality_mutation_rejects=True))
    return dict(external_vectors=vectors,repeated_cipher_requires_26_steps=True,unprepared_plaintext_repeat_rejects=True,toy=toy_controls(),continuous_literal_crib_plants=plants)

def actual():
    data=json.loads((ROOT/'data/k4.json').read_text());first=data['cribs'][0];r=constraints(first['plaintext'],data['ciphertext'][first['start']-1:first['end']],first['start']);second=None
    if r['compatible_necessary_condition']:
        c=data['cribs'][1];second=constraints(c['plaintext'],data['ciphertext'][c['start']-1:c['end']],c['start'])
    return dict(first=r,second=second,second_stage_evaluated=second is not None,K4_keys_enumerated=0,scope='Arbitrary fixed permutation rings with displacement depending only on adjacent processed plaintext symbols; disclosed processed positions aligned, no hidden moves',historically_untouched_checks=0,discovery_chronology='Invariant/witness identified from public cribs during source review, then frozen and mechanically verified; not a blind discovery')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--controls',action='store_true');ap.add_argument('--actual',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args();out={}
    if a.controls:out['controls']=controls()
    if a.actual:out['actual']=actual()
    out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/SPEC,ROOT/'data/wheatstone-reference-vectors.json',ROOT/'data/k4.json')};Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
