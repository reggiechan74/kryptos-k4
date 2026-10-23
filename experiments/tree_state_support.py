"""Arbitrary crib-start permutation support; necessary-condition relaxation only."""
import argparse,hashlib,itertools,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments import tree_path_cipher as primitive
AZ=primitive.AZ

def support(word,cipher,tree,direction,start=1):
    if len(word)!=len(cipher):raise ValueError('window lengths differ')
    alphabet=set(tree['slots']);state=list(range(len(alphabet)));assigned={};inverse={};reasons={};trace=[];conflict=None
    for j,(p,c) in enumerate(zip(word,cipher)):
        if p not in alphabet or c not in alphabet:raise ValueError('outside model alphabet')
        slot=state[tree['index'][p]];row=dict(position=start+j,plaintext=p,ciphertext=c,initial_slot=slot)
        if slot in assigned and assigned[slot]!=c:
            if conflict is None:conflict=dict(kind='same initial slot requires different letters',first=reasons[slot],second=row)
        elif c in inverse and inverse[c]!=slot:
            if conflict is None:conflict=dict(kind='different initial slots require same letter',first=reasons[inverse[c]],second=row)
        else:assigned[slot]=c;inverse[c]=slot;reasons[slot]=row
        trace.append(row);primitive.update(state,tree,p,direction)
    return dict(compatible=conflict is None,local_start_state_count=str(math.factorial(len(alphabet)-len(assigned))) if conflict is None else '0',assigned_initial_slots=assigned,trace=trace,contradiction=conflict,scope='All local start permutations granted as a necessary-condition relaxation, not a reset or proof of reachable global states.')

def encrypt(text,tree,direction,initial):
    state=list(initial);out=[];states=[]
    for p in text:
        states.append(state.copy());out.append(state[tree['index'][p]]);primitive.update(state,tree,p,direction)
    return ''.join(out),states

def dictionary_oracle(text,tree,direction,initial):
    labels=dict(zip(tree['slots'],initial));out=[]
    for p in text:
        out.append(labels[p]);path=tree['paths'][p]
        for depth in range(1,len(path)+1):
            letters=[c for c in tree['slots'] if tree['paths'][c].startswith(path[:depth])];old=labels.copy()
            for j,c in enumerate(letters):labels[c]=old[letters[(j-direction)%len(letters)]]
    return ''.join(out)

def toy(n,shape):
    alphabet=AZ[:n];paths={}
    def split(chars,path):
        if len(chars)==1:paths[chars[0]]=path;return
        m=len(chars)//2;split(chars[:m],path+'0');split(chars[m:],path+'1')
    if shape=='balanced':split(alphabet,'')
    else:paths={c:'0'*i for i,c in enumerate(alphabet)}
    prefixes={path[:i] for path in paths.values() for i in range(len(path)+1)}
    return dict(slots=list(alphabet),index={c:i for i,c in enumerate(alphabet)},paths=paths,groups={pre:tuple(i for i,c in enumerate(alphabet) if paths[c].startswith(pre)) for pre in prefixes})

def controls():
    comparisons=[];mutations=0
    for n,shape,d,v in itertools.product(range(2,7),('balanced','internal-chain'),(1,-1),range(2)):
        t=toy(n,shape);a=AZ[:n];p=((a if v==0 else a[::-1])*4)[:2*n+3];initial=a[::-1];c,_=encrypt(p,t,d,initial);r=support(p,c,t,d)
        brute={tuple(s) for s in itertools.permutations(a) if encrypt(p,t,d,s)[0]==c};represented={tuple(s) for s in itertools.permutations(a) if all(s[i]==letter for i,letter in r['assigned_initial_slots'].items())} if r['compatible'] else set()
        assert brute==represented and len(brute)==int(r['local_start_state_count'])
        assert dictionary_oracle(p,t,d,initial)==c
        first=r['trace'][0];second=next(row for row in r['trace'] if row['initial_slot']!=first['initial_slot']);bad=list(c);bad[second['position']-1]=c[0];assert not support(p,''.join(bad),t,d)['compatible'];mutations+=1
        comparisons.append(dict(n=n,shape=shape,direction=d,case=v,compatible_states=len(brute),sets_equal=True))
    p=list((AZ*4)[:97]);p[21:34]='EASTNORTHEAST';p[63:74]='BERLINCLOCK';p=''.join(p);plants=[]
    initials=(AZ[::-1],''.join(AZ[(5*i+3)%26] for i in range(26)),'KRYPTOSABCDEFGHIJLMNQUVWXZ')
    for name,t in primitive.trees().items():
        for d,initial in itertools.product((1,-1),initials):
            c,states=encrypt(p,t,d,initial);assert dictionary_oracle(p,t,d,initial)==c
            windows=[]
            for start,word in ((21,'EASTNORTHEAST'),(63,'BERLINCLOCK')):
                r=support(word,c[start:start+len(word)],t,d,start+1);assert r['compatible'];assert all(states[start][i]==letter for i,letter in r['assigned_initial_slots'].items());windows.append(r['local_start_state_count'])
            plants.append(dict(tree=name,direction=d,initial=initial,true_states_included=True,local_counts=windows))
    return dict(complete_toy_systems=comparisons,injectivity_mutation_rejections=mutations,continuous_literal_crib_plants=plants,independent_path_prefix_oracle_agrees=True)

def actual():
    data=json.loads((ROOT/'data/k4.json').read_text());out=[]
    for name,t in primitive.trees().items():
        for d in (1,-1):
            rows=[]
            for crib in data['cribs']:
                start=crib['start'];rows.append(support(crib['plaintext'],data['ciphertext'][start-1:crib['end']],t,d,start))
            out.append(dict(tree=name,direction=d,local_windows=rows,continuous_model_excluded=any(not r['compatible'] for r in rows),global_key_count_not_computed=True,local_counts_not_multiplied=True))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--controls',action='store_true');ap.add_argument('--actual',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args();out={}
    if a.controls:out['controls']=controls()
    if a.actual:out['actual']=actual()
    out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'research/TREE-STATE-SUPPORT-SPEC.md',ROOT/'experiments/tree_path_cipher.py',primitive.SCHEMA,ROOT/'data/k4.json')}
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
