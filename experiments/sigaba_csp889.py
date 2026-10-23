"""CSP-889 convention implementation; validated by external published vectors.
Historical facts / vector provenance in data/sigaba-csp889-v1.json.
This implementation does not execute or import downloaded source.
"""
import argparse,hashlib,itertools,json,time
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DATA=ROOT/'data/sigaba-csp889-v1.json'
SPEC=ROOT/'research/SIGABA-CSP889-SPEC.md'
WINDOWS=((21,'EASTNORTHEAST'),(63,'BERLINCLOCK'))
LAYOUTS=(((10,1,2,3,4),(9,8,7,6,5)),((1,2,3,4,5),(6,7,8,9,10)))

def data():return json.loads(DATA.read_text())

def inverse(w):return [w.index(i) for i in range(len(w))]

def rotor(w,p,x,reverse=False,back=False):
    n=len(w)
    if reverse:return (p-(w if back else inverse(w))[(p-x)%n])%n
    return ((inverse(w) if back else w)[(x+p)%n]-p)%n

def contact_oracle(w,p,reverse=False):
    """Rotate the physical contact-pair set, reflect and exchange sides if reversed."""
    n=len(w)
    pairs=[((i-p)%n,(v-p)%n) for i,v in enumerate(w)] if not reverse else [((p-v)%n,(p-i)%n) for i,v in enumerate(w)]
    return dict(pairs)

def wheel_tables(d):
    out={}
    for kind,ws,n in (('large',d['large'],26),('index',d['index'],10)):
        out[kind]=[]
        for s in ws:
            w=[AZ.index(x) for x in s] if n==26 else list(map(int,s))
            both=[]
            for rev in (False,True):
                fs=[];bs=[]
                for p in range(n):
                    f=[rotor(w,p,x,rev) for x in range(n)];b=inverse(f)
                    fs.append(f);bs.append(b)
                both.append((fs,bs))
            out[kind].append(both)
    return out

class Machine:
    def __init__(self,key,d=None,tables=None):
        self.d=d or data();self.t=tables or wheel_tables(self.d)
        self.order=[key[x] for x in ('cipherrotors','controlrotors','indexrotors')]
        self.rev=[[x=='1' for x in key[name]] for name in ('cipherorientation','controlorientation','indexorientation')]
        self.pos=[[AZ.index(x) for x in key[name]] if j<2 else list(map(int,key[name])) for j,name in enumerate(('cipherposition','controlposition','indexposition'))]
    def path(self,bank,x,back=False):
        for j in (range(4,-1,-1) if back else range(5)):
            typ='index' if bank==2 else 'large'
            x=self.t[typ][self.order[bank][j]-1][self.rev[bank][j]][int(back)][self.pos[bank][j]][x]
        return x
    def advance(self,bank,j):self.pos[bank][j]=(self.pos[bank][j]+(1 if self.rev[bank][j] else -1))%26
    def step(self):
        selected={self.d['magnets'][self.path(2,self.d['collector'][self.path(1,x,True)])] for x in range(5,9)}
        for j in selected:self.advance(0,j)
        if self.pos[1][2]==14:
            if self.pos[1][3]==14:self.advance(1,1)
            self.advance(1,3)
        self.advance(1,2)
        return tuple(sorted(selected))
    def crypt(self,text,decrypt=False):
        if any(x not in AZ for x in text):raise ValueError('raw machine framing requires A-Z')
        out=[]
        for x in text:
            out.append(AZ[self.path(0,AZ.index(x),decrypt)]);self.step()
        return ''.join(out)

def key(layout=0,c=0,q=0,r=0):
    cr,co=LAYOUTS[layout]
    return dict(cipherrotors=list(cr),controlrotors=list(co),indexrotors=[1,2,3,4,5],cipherorientation='00000',controlorientation='00000',indexorientation='00000',cipherposition=AZ[c]*5,controlposition='AA'+AZ[q]+'AA',indexposition=str(r)*5)

def ticks(i,first):return 0 if i<=first else 1+(i-1-first)//26

def schedule(q,r,layout,t,d,length=97,oracle=False):
    m=Machine(key(layout,0,q,r),d,t);out=[];masks=[]
    for i in range(length):
        out.append(tuple(m.pos[0]))
        if oracle:
            medium=ticks(i,(q-14)%26);slow=ticks(medium,12)
            expected=[0,(-slow)%26,(q-i)%26,(-medium)%26,0]
            if m.pos[1]!=expected:raise AssertionError((i,m.pos[1],expected))
            # Contact-set evaluation, rather than precomputed electrical tables.
            hits=set()
            for x in range(5,9):
                for j in range(4,-1,-1):
                    w=[AZ.index(z) for z in d['large'][m.order[1][j]-1]]
                    mapping=contact_oracle(w,expected[j]);x={b:a for a,b in mapping.items()}[x]
                x=d['collector'][x]
                for j in range(5):x=contact_oracle(list(map(int,d['index'][j])),r)[x]
                hits.add(d['magnets'][x])
            got=m.step()
            if set(got)!=hits:raise AssertionError('independent contact-path mismatch')
        else:got=m.step()
        masks.append(got)
    return out,masks

def prepare():
    d=data();t=wheel_tables(d);groups=[]
    for layout in range(2):
        seen={}
        for q,r in itertools.product(range(26),range(10)):
            st,_=schedule(q,r,layout,t,d)
            seen.setdefault(tuple(st),[]).append([q,r])
        for st,aliases in seen.items():groups.append(dict(layout=layout,states=st,aliases=aliases))
    return d,t,groups

def evaluate(cipher,prepared,records=True):
    d,t,groups=prepared;start=time.monotonic();rows=[];fits=[];first=0;raw=0;hist=Counter();streams=set();all_outputs=set()
    for group in groups:
        layout=group['layout'];cr=LAYOUTS[layout][0]
        for c in range(26):
            if time.monotonic()-start>180:raise TimeoutError('budget-unresolved: selector not completed')
            raw+=len(group['aliases']);failure=None
            output=[]
            for i,ch in enumerate(cipher):
                x=AZ.index(ch)
                for j in range(4,-1,-1):x=t['large'][cr[j]-1][0][1][(group['states'][i][j]+c)%26][x]
                output.append(AZ[x])
            all_outputs.add(hashlib.sha256(''.join(output).encode()).hexdigest())
            # Encrypt the known first crib at continuously propagated states.
            for i,ch in enumerate(WINDOWS[0][1],21):
                x=AZ.index(ch)
                for j in range(5):x=t['large'][cr[j]-1][0][0][(group['states'][i][j]+c)%26][x]
                if AZ[x]!=cipher[i]:failure=dict(position=i+1,expected=AZ[x],observed=cipher[i]);break
            second=False
            if failure is None:
                first+=len(group['aliases']);second=True
                for i,ch in enumerate(WINDOWS[1][1],63):
                    x=AZ.index(ch)
                    for j in range(5):x=t['large'][cr[j]-1][0][0][(group['states'][i][j]+c)%26][x]
                    if AZ[x]!=cipher[i]:failure=dict(position=i+1,expected=AZ[x],observed=cipher[i]);break
            if failure:hist[failure['position']]+=len(group['aliases'])
            else:
                q,r=group['aliases'][0];k=key(layout,c,q,r);p=Machine(k,d,t).crypt(cipher,True)
                assert Machine(k,d,t).crypt(p)==cipher
                streams.add(p);fits.append(dict(layout=layout,c=c,aliases=group['aliases'],plaintext=p))
            if records:rows.append(dict(layout=layout,c=c,aliases=group['aliases'],berlin_evaluated=second,first_conflict=failure))
    return dict(raw_keys=raw,schedule_classes=len(groups),schedule_normalized_descriptions=len(groups)*26,first_stage_raw_survivors=first,full_compatible=fits,distinct_surviving_plaintexts=len(streams),distinct_full_decryption_sha256=len(all_outputs),mismatch_histogram={str(k):v for k,v in hist.items()},records=rows,completed=True)

def controls(prepared):
    d,t,groups=prepared;vectors=[]
    for v in d['vectors']:
        enc=Machine(v,d,t).crypt(v['input']);dec=Machine(v,d,t).crypt(v['output'],True)
        assert enc==v['output'],('vector',v['n'],enc[:30],v['output'][:30])
        assert dec==v['input'];vectors.append(v['n'])
    checks=0
    for typ,n in (('large',26),('index',10)):
        for s in d[typ]:
            w=[AZ.index(x) for x in s] if n==26 else list(map(int,s))
            for rev,p,x in itertools.product((False,True),range(n),range(n)):
                y=rotor(w,p,x,rev);assert rotor(w,p,y,rev,True)==x;assert contact_oracle(w,p,rev)[x]==y;checks+=1
    for q,r,layout in ((0,0,0),(25,9,1),(14,3,0)):
        assert schedule(q,r,layout,t,d,805)==schedule(q,r,layout,t,d,805,True)
    for p in ('',AZ,AZ[::-1],'CONTINUOUSSTATEPASSESACROSSUNKNOWNPLAINTEXTGAPS'):
        k=key(1,25,14,9);assert Machine(k,d,t).crypt(Machine(k,d,t).crypt(p),True)==p
    plants=[]
    p=list((AZ*4)[:97])
    for start,word in WINDOWS:p[start:start+len(word)]=word
    p=''.join(p)
    for layout,c,q,r in ((0,0,0,0),(1,25,25,9),(0,7,14,3),(1,13,2,4)):
        cipher=Machine(key(layout,c,q,r),d,t).crypt(p);sel=evaluate(cipher,prepared,False)
        assert any(f['layout']==layout and f['c']==c and [q,r] in f['aliases'] for f in sel['full_compatible'])
        plants.append(dict(key=[layout,c,q,r],raw_fits=sum(len(f['aliases']) for f in sel['full_compatible']),plaintexts=sel['distinct_surviving_plaintexts'],truth_included=True))
    assert evaluate('A'*97,prepared,False)['full_compatible']==[]
    changed=d['vectors'][0]['output'];changed=('A' if changed[0]!='A' else 'B')+changed[1:]
    assert Machine(d['vectors'][0],d,t).crypt(d['vectors'][0]['input'])!=changed
    return dict(external_vectors_both_directions=vectors,contact_and_inverse_checks=checks,independent_805_step_cases=3,plants=plants,constant_negative=True,mutated_vector_rejected=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--controls',action='store_true');ap.add_argument('--actual',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args()
    prepared=prepare();out={'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (DATA,SPEC,Path(__file__))}}
    if a.controls:out['controls']=controls(prepared)
    if a.actual:out['actual']=evaluate(json.loads((ROOT/'data/k4.json').read_text())['ciphertext'],prepared)
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
