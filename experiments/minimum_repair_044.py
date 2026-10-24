"""Exact minimum ciphertext substitutions with arbitrary plaintext outside fixed cribs."""
import collections,itertools,math

def decrypt(C,key,L,q,sigma,tau,mode):
 P=[]
 for i,c in enumerate(C):
  k=key[i%L] if mode=='periodic' else key[i] if i<L else (P if mode=='plaintext' else C)[i-L]
  P.append(sigma*(c-tau*k)%q)
 return tuple(P)
def encrypt(P,key,L,q,sigma,tau,mode):
 C=[]
 for i,p in enumerate(P):
  k=key[i%L] if mode=='periodic' else key[i] if i<L else (P if mode=='plaintext' else C)[i-L]
  C.append((sigma*p+tau*k)%q)
 return tuple(C)
def first(values,q):return tuple(0 if x is None else x[0] for x in values)
def root_domains(C,known,L,q,sigma,tau):
 a=[1]*len(C);b=[0]*len(C);roots={}
 for i in range(L,len(C)):a[i]=-sigma*tau*a[i-L];b[i]=(sigma*C[i]-sigma*tau*b[i-L])%q
 for i,p in known.items():
  v=a[i]*(p-b[i])%q;r=i%L
  if r in roots and roots[r]!=v:raise AssertionError('Unrepaired plaintext chain')
  roots[r]=v
 return [[roots[i]] if i in roots else None for i in range(L)]
def primer_from_roots(C,roots,L,q,sigma,tau):return tuple(tau*(C[i]-sigma*roots[i])%q for i in range(L))

def profile(C,known,L,q,sigma,tau,mode):
 n=len(C);out=dict(mode=mode,lag_or_period=L,q=q,sigma=sigma,tau=tau);R=list(C)
 if mode=='periodic':
  domains=[];cost=0;free=0;strings=1
  for r in range(L):
   values=collections.Counter(tau*(C[i]-sigma*p)%q for i,p in known.items() if i%L==r)
   if not values:domains.append(None);free+=1;continue
   best=max(values.values());choices=sorted(x for x,count in values.items() if count==best);domains.append(choices);cost+=sum(values.values())-best;strings*=len(choices)
  key=first(domains,q)
  for i,p in known.items():R[i]=(sigma*p+tau*key[i%L])%q
  out.update(key_domains=domains,free_key_symbols=free,minimum_substitutions=cost,optimal_corrected_ciphertexts=str(strings),keys_per_corrected_ciphertext=str(q**free),optimal_cipher_key_pairs=str(strings*q**free))
 elif mode=='plaintext':
  intervals=[];cost=0;strings=1
  for r in range(L):
   indices=sorted(i for i in known if i%L==r)
   for a,b in zip(indices,indices[1:]):
    points=list(range(a+L,b+1,L));value=known[a]
    for i in points:value=sigma*(C[i]-tau*value)%q
    residual=(known[b]-value)%q;options=[]
    if residual:
     cost+=1
     for j,i in enumerate(points):
      delta=(sigma*(-sigma*tau)**(len(points)-1-j)*residual)%q;assert delta;options.append([i,delta])
     strings*=len(options);i,delta=options[0];R[i]=(R[i]+delta)%q
    intervals.append(dict(first_known=a,last_known=b,cipher_positions=points,residual=residual,one_edit_options=options))
  domains=root_domains(R,known,L,q,sigma,tau);free=sum(x is None for x in domains);key=primer_from_roots(R,first(domains,q),L,q,sigma,tau)
  out.update(intervals=intervals,free_key_symbols=free,minimum_substitutions=cost,optimal_corrected_ciphertexts=str(strings),keys_per_corrected_ciphertext=str(q**free),optimal_cipher_key_pairs=str(strings*q**free))
 elif mode=='ciphertext':
  adjacency=collections.defaultdict(list)
  for i,p in known.items():
   if i<L:continue
   j=i-L;adjacency[j].append((i,tau,sigma*p));adjacency[i].append((j,tau,-tau*sigma*p))
  seen=set();components=[];cost=0;strings=1
  for root in sorted(adjacency):
   if root in seen:continue
   affine={root:(1,0)};todo=[root];seen.add(root)
   for node in todo:
    a,b=affine[node]
    for following,mult,add in adjacency[node]:
     value=(mult*a,(mult*b+add)%q)
     if following in affine:assert (affine[following][0]-value[0])%q==0 and affine[following][1]==value[1]
     else:affine[following]=value;todo.append(following);seen.add(following)
   counts=collections.Counter(a*(C[i]-b)%q for i,(a,b) in affine.items());best=max(counts.values());choices=sorted(x for x,count in counts.items() if count==best);cost+=len(affine)-best;strings*=len(choices)
   nodes=[[i,a,b] for i,(a,b) in sorted(affine.items())]
   for i,a,b in nodes:R[i]=(a*choices[0]+b)%q
   components.append(dict(root=root,affine_nodes=nodes,optimal_root_values=choices,minimum_component_edits=len(affine)-best))
  domains=[[tau*(R[i]-sigma*known[i])%q] if i in known else None for i in range(L)];free=sum(x is None for x in domains);key=first(domains,q)
  out.update(components=components,free_key_symbols=free,minimum_substitutions=cost,optimal_corrected_ciphertexts=str(strings),keys_per_corrected_ciphertext=str(q**free),optimal_cipher_key_pairs=str(strings*q**free))
 else:raise ValueError('Unknown mode')
 P=decrypt(R,key,L,q,sigma,tau,mode);assert all(P[i]==v for i,v in known.items());assert encrypt(P,key,L,q,sigma,tau,mode)==tuple(R);edits=[[i,C[i],x] for i,x in enumerate(R) if x!=C[i]];assert len(edits)==out['minimum_substitutions'];undo=list(R)
 for i,before,after in edits:assert undo[i]==after;undo[i]=before
 assert tuple(undo)==tuple(C)
 out['witness']=dict(corrected_cipher=list(R),plaintext=list(P),key=list(key),edits=edits,full_reencryption=True,reverse_channel_recovers_observed=True,proposed_English_solution=False)
 return out

def expand(C,known,result):
 q=result['q'];L=result['lag_or_period'];sigma=result['sigma'];tau=result['tau'];mode=result['mode'];out=set()
 if mode=='periodic':
  for key in itertools.product(*(range(q) if v is None else v for v in result['key_domains'])):
   R=list(C)
   for i,p in known.items():R[i]=(sigma*p+tau*key[i%L])%q
   out.add((tuple(R),tuple(key)))
 elif mode=='plaintext':
  options=[row['one_edit_options'] for row in result['intervals'] if row['residual']]
  for edits in itertools.product(*options):
   R=list(C)
   for i,delta in edits:R[i]=(R[i]+delta)%q
   domains=root_domains(R,known,L,q,sigma,tau)
   for roots in itertools.product(*(range(q) if v is None else v for v in domains)):out.add((tuple(R),primer_from_roots(R,roots,L,q,sigma,tau)))
 else:
  comps=result['components']
  for values in itertools.product(*(x['optimal_root_values'] for x in comps)):
   R=list(C)
   for comp,value in zip(comps,values):
    for i,a,b in comp['affine_nodes']:R[i]=(a*value+b)%q
   domains=[[tau*(R[i]-sigma*known[i])%q] if i in known else range(q) for i in range(L)]
   for key in itertools.product(*domains):out.add((tuple(R),tuple(key)))
 return out

def oracle(C,known,L,q,sigma,tau,mode):
 best=len(C)+1;out=set()
 for R in itertools.product(range(q),repeat=len(C)):
  distance=sum(a!=b for a,b in zip(C,R))
  if distance>best:continue
  for key in itertools.product(range(q),repeat=L):
   # Independent sequential inverse, no root/phase/component solver.
   P=[]
   for i,c in enumerate(R):
    if mode=='periodic':k=key[i%L]
    elif i<L:k=key[i]
    elif mode=='plaintext':k=P[i-L]
    else:k=R[i-L]
    P.append((sigma*c-sigma*tau*k)%q)
   if not all(P[i]==v for i,v in known.items()):continue
   if distance<best:best=distance;out=set()
   out.add((R,key))
 return best,out

def controls():
 cases=0;relations=0
 for q,n in ((2,4),(3,3)):
  masks=({}, {0:0}, {n-1:1}, {0:1,n-1:0})
  for C in itertools.product(range(q),repeat=n):
   for known in masks:
    for L in (1,2):
     for mode in ('periodic','plaintext','ciphertext'):
      for sigma,tau in ((1,1),(-1,1)) if mode=='periodic' else ((1,1),(1,-1),(-1,1)):
       result=profile(C,known,L,q,sigma,tau,mode);cost,truth=oracle(C,known,L,q,sigma,tau,mode);actual=expand(C,known,result);assert result['minimum_substitutions']==cost and actual==truth;assert int(result['optimal_cipher_key_pairs'])==len(truth);cases+=1;relations+=len(truth)
 return dict(complete_tiny_optimal_relation_comparisons=cases,complete_optimal_cipher_key_pairs=relations,independent_brute_force_all_corrected_ciphertexts_and_keys=True)
