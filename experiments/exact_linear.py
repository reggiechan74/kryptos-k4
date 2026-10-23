"""Exact prime-field affine spaces and square-free CRT; no numeric heuristics."""
import itertools
from math import prod

FACTORS={2:(2,),3:(3,),6:(2,3),26:(2,13)}


def solve_field(matrix,rhs,p,nvars=None):
    n=len(matrix[0]) if matrix else (nvars if nvars is not None else 0)
    if nvars is not None and n!=nvars:raise ValueError('variable count mismatch')
    if len(matrix)!=len(rhs) or any(len(row)!=n for row in matrix):raise ValueError('shape mismatch')
    m=len(matrix);rows=[[x%p for x in row]+[value%p] for row,value in zip(matrix,rhs)]
    combinations=[[int(i==j) for j in range(m)] for i in range(m)]
    rank=0;pivots=[]
    for col in range(n):
        pivot=next((i for i in range(rank,m) if rows[i][col]),None)
        if pivot is None:continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        combinations[rank],combinations[pivot]=combinations[pivot],combinations[rank]
        inv=pow(rows[rank][col],-1,p)
        rows[rank]=[(inv*x)%p for x in rows[rank]]
        combinations[rank]=[(inv*x)%p for x in combinations[rank]]
        for i in range(m):
            if i==rank:continue
            f=rows[i][col]
            if f:
                rows[i]=[(x-f*y)%p for x,y in zip(rows[i],rows[rank])]
                combinations[i]=[(x-f*y)%p for x,y in zip(combinations[i],combinations[rank])]
        pivots.append(col);rank+=1
    bad=next((i for i,row in enumerate(rows) if not any(row[:n]) and row[n]),None)
    result=dict(prime=p,variables=n,equations=m,rank=rank,augmented_rank=rank+(bad is not None),
                consistent=bad is None,pivots=pivots,consistency_checks=m-rank,rref=rows)
    if bad is not None:
        result.update(particular=None,basis=None,cardinality=0,
                      contradiction=dict(equation_weights=combinations[bad],rhs=rows[bad][n]))
        return result
    point=[0]*n
    for i,col in enumerate(pivots):point[col]=rows[i][n]
    free=[i for i in range(n) if i not in pivots];basis=[]
    for col in free:
        v=[0]*n;v[col]=1
        for i,pivot in enumerate(pivots):v[pivot]=-rows[i][col]%p
        basis.append(v)
    result.update(particular=point,basis=basis,free_columns=free,cardinality=p**len(free),contradiction=None)
    return result


def solve_ring(matrix,rhs,q,nvars=None):
    if q not in FACTORS:raise ValueError('only declared square-free moduli supported')
    fields=[solve_field(matrix,rhs,p,nvars) for p in FACTORS[q]]
    return dict(modulus=q,fields=fields,consistent=all(x['consistent'] for x in fields),
                cardinality=prod(x['cardinality'] for x in fields))


def field_contains(space,point):
    if not space['consistent']:return False
    p=space['prime'];x=[v%p for v in point];out=space['particular'][:]
    for col,basis in zip(space['free_columns'],space['basis']):
        for i,v in enumerate(basis):out[i]=(out[i]+x[col]*v)%p
    return out==x


def contains(space,point):return all(field_contains(f,point) for f in space['fields'])


def field_vectors(space):
    if not space['consistent']:return
    p=space['prime']
    for values in itertools.product(range(p),repeat=len(space['basis'])):
        yield tuple((v+sum(t*b[i] for t,b in zip(values,space['basis'])))%p
                    for i,v in enumerate(space['particular']))


def crt(values,primes):
    q=prod(primes)
    return sum(v*(q//p)*pow(q//p,-1,p) for v,p in zip(values,primes))%q


def ring_vectors(space):
    if not space['consistent']:return
    fields=space['fields'];primes=[f['prime'] for f in fields]
    for vectors in itertools.product(*(field_vectors(f) for f in fields)):
        yield tuple(crt([v[i] for v in vectors],primes) for i in range(fields[0]['variables']))


def canonical_affine(point,basis,p):
    n=len(point);r=solve_field(basis,[0]*len(basis),p,n)
    rows=[row[:n] for row in r['rref'][:r['rank']]];u=[v%p for v in point]
    for pivot,row in zip(r['pivots'],rows):
        f=u[pivot];u=[(x-f*y)%p for x,y in zip(u,row)]
    return dict(prime=p,point=u,basis=rows,dimension=len(rows),cardinality=p**len(rows))


def affine_key(space):return (space['prime'],tuple(space['point']),tuple(map(tuple,space['basis'])))


def affine_intersection(a,b):
    p=a['prime'];assert p==b['prime'];na=len(a['basis']);nb=len(b['basis']);n=len(a['point'])
    matrix=[[v[i] for v in a['basis']]+[-v[i] for v in b['basis']] for i in range(n)]
    rhs=[y-x for x,y in zip(a['point'],b['point'])]
    s=solve_field(matrix,rhs,p,na+nb)
    if not s['consistent']:return None
    point=[(x+sum(s['particular'][j]*v[i] for j,v in enumerate(a['basis'])))%p for i,x in enumerate(a['point'])]
    basis=[[(sum(t[j]*v[i] for j,v in enumerate(a['basis'])))%p for i in range(n)] for t in s['basis']]
    return canonical_affine(point,basis,p)


def product_key(space):return tuple(affine_key(s) for s in space)


def product_intersection(a,b):
    out=[affine_intersection(x,y) for x,y in zip(a,b)]
    return None if any(x is None for x in out) else out


def union_cardinality(spaces,term_limit=4096):
    """Exact signed intersections; never substitute a sum for a union."""
    terms={};seen=set()
    for space in spaces:
        key=product_key(space)
        if key in seen:continue
        seen.add(key);changes={key:[space,1]}
        for old,weight in list(terms.values()):
            intersect=product_intersection(old,space)
            if intersect is not None:
                k=product_key(intersect)
                changes.setdefault(k,[intersect,0])[1]-=weight
        for k,(value,weight) in changes.items():
            terms.setdefault(k,[value,0])[1]+=weight
            if not terms[k][1]:del terms[k]
        if len(terms)>term_limit:raise OverflowError('affine-union term budget')
    total=sum(weight*prod(s['cardinality'] for s in space) for space,weight in terms.values())
    assert total>=0
    return total,len(terms)
