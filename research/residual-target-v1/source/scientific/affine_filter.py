"""Exact prime-field affine-minus-union scalar marginals, development version 1.
No target-specific predicates. Malformed input raises ValueError; exhausted valid
requests return INCOMPLETE with no masks/witnesses. All checks survive python -O.
"""
from dataclasses import dataclass
import hashlib, json, time

VERSION='affine-filter-1'
class CertificateError(RuntimeError): pass
class Exhausted(Exception): pass
@dataclass(frozen=True)
class Budget:
    max_work:int=20_000_000
    max_solves:int=200_000
    max_terms:int=65536
    max_seconds:float=10.0

class Meter:
    def __init__(self,b):
        self.b=b; self.work=0; self.solves=0; self.terms=0; self.start=time.monotonic()
    def tick(self,w=1):
        if w>self.b.max_work-self.work: raise Exhausted('work budget')
        self.work+=w
        if time.monotonic()-self.start>=self.b.max_seconds: raise Exhausted('wall-time budget')
    def preflight_ie(self,r,q,k):
        # Avoid forming unbounded 2**r. Include all subset solves and q-entry counts.
        if r>=self.b.max_terms.bit_length(): raise Exhausted('subset preflight')
        terms=1<<r
        if terms>self.b.max_terms-self.terms: raise Exhausted('subset preflight')
        if terms>self.b.max_solves-self.solves: raise Exhausted('solve preflight')
        if terms*max(1,k*q)>self.b.max_work-self.work: raise Exhausted('count preflight')
        self.tick(); return terms
    def receipt(self):
        return dict(work=self.work,solves=self.solves,terms=self.terms,wall_seconds=time.monotonic()-self.start)

def require(ok,msg):
    if not ok: raise CertificateError(msg)
def dot(a,b,q):
    require(len(a)==len(b),'internal dot dimension')
    return sum(a[j]*b[j] for j in range(len(a)))%q

def validate(q,n,base,forbidden,scalars,budget):
    if type(q) is not int or not 2<=q<=65521 or any(q%d==0 for d in range(2,int(q**0.5)+1)):
        raise ValueError('q must be prime, 2 <= q <= 65521; prime powers unsupported')
    if type(n) is not int or not 0<=n<=64: raise ValueError('n must be integer in [0,64]')
    if type(budget) is not Budget: raise ValueError('Budget required')
    for x in (budget.max_work,budget.max_solves,budget.max_terms):
        if type(x) is not int or x<0 or x>10**12: raise ValueError('invalid integer budget')
    if type(budget.max_seconds) not in (int,float) or not 0<=budget.max_seconds<=3600:
        raise ValueError('invalid finite time budget')
    def seq(x):
        if type(x) not in (list,tuple): raise ValueError('only list/tuple sequences accepted')
    seq(base);seq(forbidden);seq(scalars)
    if len(forbidden)>256 or len(scalars)>256: raise ValueError('too many systems/scalars')
    systems=[base]+list(forbidden)
    for rows in systems: seq(rows)
    if sum(len(rows) for rows in systems)>256: raise ValueError('too many input equations')
    def row(x,size):
        seq(x)
        if len(x)!=size or any(type(v) is not int or not 0<=v<q for v in x):
            raise ValueError('wrong row dimension or noncanonical field integer')
        return tuple(x)
    return tuple(row(x,n+1) for x in base),tuple(tuple(row(x,n+1) for x in rows) for rows in forbidden),tuple(row(x,n) for x in scalars)

def solve(rows,n,q,m):
    m.tick()
    if m.solves>=m.b.max_solves: raise Exhausted('solve budget')
    m.solves+=1
    original=[list(row) for row in rows]; a=[row[:] for row in original]; ops=[]; piv=[]; k=0
    for j in range(n):
        m.tick(max(1,len(a)))
        h=next((h for h in range(k,len(a)) if a[h][j]),None)
        if h is None: continue
        a[k],a[h]=a[h],a[k];ops.append(('swap',k,h))
        inv=pow(a[k][j],-1,q);a[k]=[(v*inv)%q for v in a[k]];ops.append(('scale',k,inv));m.tick(n+1)
        for h in range(len(a)):
            if h!=k and a[h][j]:
                c=a[h][j];a[h]=[(a[h][v]-c*a[k][v])%q for v in range(n+1)]
                ops.append(('add',h,k,(-c)%q));m.tick(n+1)
        piv.append(j);k+=1
    # Nonoptional certificate verifier: replay reversible row operations.
    replay=[row[:] for row in original]
    for op in ops:
        m.tick(n+1)
        if op[0]=='swap': replay[op[1]],replay[op[2]]=replay[op[2]],replay[op[1]]
        elif op[0]=='scale':
            require(op[2]!=0,'zero row scaling');replay[op[1]]=[v*op[2]%q for v in replay[op[1]]]
        else:
            _,h,k,c=op;require(h!=k,'noninvertible row addition')
            replay[h]=[(replay[h][v]+c*replay[k][v])%q for v in range(n+1)]
    require(replay==a,'row operation certificate mismatch')
    require(all(a[h][p]==int(h==j) for j,p in enumerate(piv) for h in range(len(a))),'pivot certificate')
    require(all(not any(row[:n]) for row in a[len(piv):]),'rank certificate')
    receipt={'rref':a,'pivots':piv,'operations':ops}
    if any(not any(row[:n]) and row[n] for row in a): return None,receipt
    b=[0]*n
    for j,p in enumerate(piv):b[p]=a[j][n]
    N=[]
    for f in range(n):
        if f not in piv:
            v=[0]*n;v[f]=1
            for j,p in enumerate(piv):v[p]=-a[j][f]%q
            N.append(v)
    m.tick(max(1,len(rows)*(len(N)+1)*(n+1)))
    require(all(dot(row[:n],b,q)==row[n] for row in rows),'particular solution')
    require(all(dot(row[:n],v,q)==0 for row in rows for v in N),'nullspace solution')
    # Free-coordinate identity proves independence; pivot rank proves completeness.
    free=[f for f in range(n) if f not in piv]
    require(all(N[j][f]==int(j==h) for j in range(len(N)) for h,f in enumerate(free)),'nullspace rank')
    return (b,N),receipt

def restrict(rows,V,q,m):
    a,N=V;m.tick(max(1,len(rows)*(len(N)+1)*(len(a)+1)))
    return [tuple([dot(row[:-1],v,q) for v in N]+[(row[-1]-dot(row[:-1],a,q))%q]) for row in rows]
def contains(rows,V,q,m):return all(not any(row) for row in restrict(rows,V,q,m))
def check_witness(x,base,forbidden,c,t,q,m):
    m.tick(max(1,(len(base)+sum(map(len,forbidden))+1)*(len(x)+1)))
    sat=lambda rows:all(dot(row[:-1],x,q)==row[-1] for row in rows)
    require(sat(base) and all(not sat(w) for w in forbidden) and dot(c,x,q)==t,'witness certificate')

def greedy(base,forbidden,c,t,n,q,m):
    V,_=solve(list(base)+[tuple(c)+(t,)],n,q,m);require(V is not None,'claimed fiber absent')
    require(not any(contains(w,V,q,m) for w in forbidden),'claimed fiber excluded')
    a,N=V;d=len(N);cuts=[restrict(w,V,q,m) for w in forbidden];prefix=[]
    for j in range(d):
        found=False
        for u in range(q):
            p=prefix+[u]+[0]*(d-j-1);K=[[int(h==k) for k in range(d)] for h in range(j+1,d)]
            if not any(contains(w,(p,K),q,m) for w in cuts):prefix.append(u);found=True;break
        require(found,'greedy invariant failed')
    x=[(a[k]+sum(prefix[j]*N[j][k] for j in range(d)))%q for k in range(n)]
    check_witness(x,base,forbidden,c,t,q,m);return x

def ie(base,forbidden,scalars,n,q,m,record=False):
    terms=m.preflight_ie(len(forbidden),q,len(scalars));counts=[[0]*q for c in scalars];total=0;evidence=[]
    for mask in range(terms):
        m.tick(max(1,q*len(scalars)));m.terms+=1
        rows=list(base)+[row for j,w in enumerate(forbidden) if mask>>j&1 for row in w]
        V,cert=solve(rows,n,q,m);sign=(-1)**mask.bit_count()
        if V is None:
            if record:evidence.append({'subset':mask,'empty':True,'solve':cert})
            continue
        a,N=V;d=len(N);total+=sign*q**d;projections=[]
        for j,c in enumerate(scalars):
            m.tick(max(1,(len(N)+1)*(n+1)))
            if any(dot(c,v,q) for v in N):
                for t in range(q):counts[j][t]+=sign*q**(d-1)
                projections.append({'full':True,'dimension':d})
            else:
                t=dot(c,a,q);counts[j][t]+=sign*q**d;projections.append({'value':t,'dimension':d})
        if record:evidence.append({'subset':mask,'empty':False,'solve':cert,'projections':projections})
    require(total>=0 and all(v>=0 for row in counts for v in row),'negative IE count')
    require(all(sum(row)==total for row in counts),'IE total mismatch')
    return total,counts,evidence

def ie_witness(base,forbidden,c,t,n,q,m):
    rows=list(base)+[tuple(c)+(t,)];x=[]
    for j in range(n):
        found=False
        for u in range(q):
            row=tuple(int(j==h) for h in range(n))+(u,)
            count,_,_=ie(rows+[row],forbidden,[],n,q,m)
            if count>0:rows.append(row);x.append(u);found=True;break
        require(found,'IE witness invariant')
    check_witness(x,base,forbidden,c,t,q,m);return x

def project_filtered_affine(q,n,base,forbidden,scalars,budget=Budget()):
    """Each equation is [n coefficients, rhs]; scalar rows have n coefficients.
    All residues must be canonical built-in integers. A zero-scalar probe always
    supplies a feasibility witness, even when no projections are requested.
    Certificate errors raise rather than being relabeled as budget exhaustion.
    """
    base,forbidden,scalars=validate(q,n,base,forbidden,scalars,budget)
    identity=hashlib.sha256(json.dumps([VERSION,q,n,base,forbidden,scalars],separators=(',',':')).encode()).hexdigest()
    m=Meter(budget);route='small-union' if len(forbidden)<q else 'inclusion-exclusion'
    result={'version':VERSION,'instance_sha256':identity,'route':route}
    try:
        m.tick();V,cert=solve(base,n,q,m);evidence={'base':cert,'r':len(forbidden),'q':q}
        if V is None:return dict(result,status='EMPTY',masks=[[] for _ in scalars],witnesses=[{} for _ in scalars],evidence=evidence,resources=m.receipt())
        # Probe ensures nonempty relation is never inferred solely from zero masks.
        queries=scalars+(tuple(0 for _ in range(n)),)
        if route=='small-union':
            a,N=V;cuts=[];evidence['cuts']=[]
            for w in forbidden:
                reduced=restrict(w,V,q,m);D,cproof=solve(reduced,len(N),q,m)
                evidence['cuts'].append({'restricted':reduced,'solve':cproof})
                if D is not None and len(D[1])==len(N):
                    require(contains(w,V,q,m),'containment receipt')
                    return dict(result,status='EMPTY',masks=[[] for _ in scalars],witnesses=[{} for _ in scalars],evidence=evidence,resources=m.receipt())
                cuts.append(D)
            masks=[];evidence['projections']=[]
            for c in queries:
                m.tick(q+max(1,(len(N)+1)*(n+1)));h=[dot(c,v,q) for v in N];offset=dot(c,a,q);removed=[]
                if not any(h):mask=[offset]
                else:
                    for idx,D in enumerate(cuts):
                        if D is None:continue
                        p,K=D;m.tick(max(1,len(K)*len(h)))
                        if len(K)==len(N)-1 and all(dot(h,v,q)==0 for v in K):
                            t=(offset+dot(h,p,q))%q
                            # Independently verify direct rank-one fiber identity.
                            rows=evidence['cuts'][idx]['restricted'];pivot=next(j for j,v in enumerate(h) if v)
                            u=[row[pivot]*pow(h[pivot],-1,q)%q for row in rows]
                            require(any(u),'zero rank-one normal')
                            require(all(row[j]==u[k]*h[j]%q for k,row in enumerate(rows) for j in range(len(h))),'rank-one normal')
                            require(all(row[-1]==u[k]*(t-offset)%q for k,row in enumerate(rows)),'rank-one offset')
                            removed.append({'cut':idx,'value':t,'multipliers':u})
                    mask=[t for t in range(q) if t not in {x['value'] for x in removed}]
                masks.append(mask);evidence['projections'].append({'offset':offset,'h':h,'removed':removed})
            witnesses=[{t:greedy(base,forbidden,c,t,n,q,m) for t in mask} for c,mask in zip(queries,masks)]
        else:
            total,counts,terms=ie(base,forbidden,queries,n,q,m,True);evidence['terms']=terms;evidence['counts']=counts;evidence['total']=total
            if total==0:return dict(result,status='EMPTY',masks=[[] for _ in scalars],witnesses=[{} for _ in scalars],evidence=evidence,resources=m.receipt())
            masks=[[t for t,k in enumerate(row) if k] for row in counts]
            witnesses=[{t:ie_witness(base,forbidden,c,t,n,q,m) for t in mask} for c,mask in zip(queries,masks)]
        m.tick();require(masks[-1]==[0] and 0 in witnesses[-1],'feasibility witness absent')
        return dict(result,status='EXACT',masks=masks[:-1],witnesses=witnesses[:-1],feasibility_witness=witnesses[-1][0],evidence=evidence,resources=m.receipt())
    except Exhausted as exc:
        return dict(result,status='INCOMPLETE',reason=str(exc),masks=None,witnesses=None,evidence=None,resources=m.receipt())
