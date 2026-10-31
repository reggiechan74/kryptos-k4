"""Study064 production v1: exact recurrence-distance clock; no target inputs."""
import argparse, json

def divisors(p):
    return [d for d in range(1,p) if p%d==0]

def schedule(ciphertext,p):
    q=0; last={}; out=[]
    for i,c in enumerate(ciphertext):
        out.append(q)
        q=(q+(i-last[c] if c in last else 1))%p
        last[c]=i
    return out

def primitive(key):
    return not any(all(key[i]==key[i%d] for i in range(len(key))) for d in divisors(len(key)))

def encrypt(plaintext,key,m=26):
    q=0; last={}; out=[]
    for i,v in enumerate(plaintext):
        c=(v+key[q])%m; out.append(c)
        q=(q+(i-last[c] if c in last else 1))%len(key)
        last[c]=i
    return out

def decrypt(ciphertext,key,m=26):
    return [(c-key[q])%m for c,q in zip(ciphertext,schedule(ciphertext,len(key)))]

def seed_count(forced,m):
    """Count exact primitive-period seeds by divisor recursion, no enumeration."""
    p=len(forced); counts={}
    for d in divisors(p)+[p]:
        folded={}; contradiction=False
        for j,v in enumerate(forced):
            if v is None: continue
            if j%d in folded and folded[j%d]!=v: contradiction=True; break
            folded[j%d]=v
        total=0 if contradiction else m**(d-len(folded))
        counts[d]=total-sum(counts[e] for e in divisors(d))
    return counts[p]

def witness(forced,m):
    if seed_count(forced,m)==0: return None
    out=list(forced)
    for j in range(len(out)):
        if out[j] is not None: continue
        for v in range(m):
            out[j]=v
            if seed_count(out,m): break
        else: raise AssertionError('positive count without witness')
    assert primitive(out)
    return out

def solve_case(case):
    c=case['ciphertext']; m=case.get('modulus',26)
    if m<2 or any(not isinstance(x,int) or not 0<=x<m for x in c): raise ValueError('alphabet')
    known=case['known']; periods=case.get('periods',list(range(2,9)))
    if any(not 0<=i<len(c) or not 0<=v<m for i,v in known): raise ValueError('known')
    rows=[]; witnesses=[]; seen=set()
    for p in periods:
        if p<2 or p>8: raise ValueError('period')
        s=schedule(c,p); f=[None]*p; ok=True
        for i,v in known:
            value=(c[i]-v)%m; q=s[i]
            if f[q] is not None and f[q]!=value: ok=False
            f[q]=value
        used=sorted(set(s)); count=seed_count(f,m) if ok else 0
        # For small alphabets use exact used-assignment enumeration when the
        # unused-coordinate extension theorem's alphabet bound is unavailable.
        if count==0: projection=0
        elif len(used)==p: projection=count
        elif m>len(divisors(p)):
            projection=m**sum(f[q] is None for q in used)
        else:
            from itertools import product
            free=[q for q in used if f[q] is None]; projection=0
            for vals in product(range(m),repeat=len(free)):
                g=list(f)
                for q,v in zip(free,vals): g[q]=v
                projection+=bool(seed_count(g,m))
        row={'period':p,'schedule':s,'forced':f,'used':used,'proper_divisors':divisors(p),
             'forced_consistent':ok,'consistent':bool(count),'primitive_seed_count':count,'plaintext_count':projection}
        rows.append(row)
        if not count: continue
        key=witness(f,m); pt=decrypt(c,key,m)
        def retain(k):
            plain=decrypt(c,k,m); t=tuple(plain)
            assert encrypt(plain,k,m)==c
            assert all(plain[i]==v for i,v in known)
            if t not in seen and len(witnesses)<2:
                seen.add(t); witnesses.append({'period':p,'key':k,'plaintext':plain})
        retain(key)
        if projection>1 and len(witnesses)<2:
            for q in used:
                if f[q] is not None: continue
                for v in range(m):
                    if v==key[q]: continue
                    g=list(f); g[q]=v; alt=witness(g,m)
                    if alt is not None:
                        retain(alt); break
                if len(witnesses)==2: break
    status='empty' if not witnesses else ('unique' if len(witnesses)==1 else 'ambiguous')
    return {'id':case.get('id'),'relations':rows,'union_status':status,'witnesses':witnesses,
            'union_semantics':'union of forced primitive-seed cylinders, existentially projected to full plaintext; counts not summed'}

if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('input'); a.add_argument('output'); x=a.parse_args()
    cases=json.load(open(x.input)); result=[solve_case(c) for c in cases]
    with open(x.output,'w') as f: json.dump(result,f,sort_keys=True,indent=2); f.write('\n')
