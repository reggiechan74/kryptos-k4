"""CSP-889 coupled adapter; synthetic observations only, no K4 reader."""
import collections,hashlib,itertools,json,sys,time
import sigaba_csp889 as sig
import sigaba_joint_toy as toy
from sigaba_torus import TorusPredicates

class RealModel:
 def __init__(self,key=None,budget=None,quotient=True):
  self.d=sig.data();self.t=sig.wheel_tables(self.d);self.key=key or sig.key(1);self.q=26;self.r=5;self.m=10;self.mask_cache={};self.b=budget or toy.Budget()
  self.orders=[self.key[x] for x in ('cipherrotors','controlrotors','indexrotors')]
  self.rev=[[int(x) for x in self.key[n]] for n in ('cipherorientation','controlorientation','indexorientation')]
  self.cf=[self.t['large'][w-1][self.rev[0][j]][0] for j,w in enumerate(self.orders[0])]
  self.cb=[self.t['large'][w-1][self.rev[0][j]][1] for j,w in enumerate(self.orders[0])]
  self.ctrl=[self.t['large'][w-1][self.rev[1][j]][1] for j,w in enumerate(self.orders[1])]
  self.ix=[self.t['index'][w-1][self.rev[2][j]][0] for j,w in enumerate(self.orders[2])]
  self.maps=[];self.aliases=[]
  if quotient:
   groups={}
   for positions in itertools.product(range(10),repeat=5):
    self.b.check();h=[]
    for x in range(10):
     for j in range(5):x=self.ix[j][positions[j]][x]
     h.append(self.d['magnets'][x])
    groups.setdefault(tuple(h),[]).append(positions)
   self.maps=sorted(groups);self.aliases=[groups[h] for h in self.maps]
 def digits(self,control,length):
  pos=list(control);out=[]
  for _ in range(length):
   hits=[]
   for x in range(5,9):
    for j in range(4,-1,-1):x=self.ctrl[j][pos[j]][x]
    hits.append(self.d['collector'][x])
   out.append(tuple(sorted(set(hits))))
   if pos[2]==14:
    if pos[3]==14:pos[1]=(pos[1]+(1 if self.rev[1][1] else -1))%26
    pos[3]=(pos[3]+(1 if self.rev[1][3] else -1))%26
   pos[2]=(pos[2]+(1 if self.rev[1][2] else -1))%26
  return out
 def mask_groups(self,digits):
  if digits not in self.mask_cache:
   groups={}
   # Byte arrays avoid quadratic growing-bigint allocation while grouping 66k maps.
   width=(len(self.maps)+7)//8;rows={}
   for h,mapping in enumerate(self.maps):
    self.b.check();mask=0
    for x in digits:mask|=1<<mapping[x]
    if mask not in rows:rows[mask]=bytearray(width)
    rows[mask][h//8]|=1<<(h%8)
   self.mask_cache[digits]=[(m,int.from_bytes(row,'little')) for m,row in sorted(rows.items())]
  return self.mask_cache[digits]
 def stream(self,text,key=None,decrypt=False):
  key=key or self.key;cp=[sig.AZ.index(x) for x in key['cipherposition']];control=[sig.AZ.index(x) for x in key['controlposition']];index=list(map(int,key['indexposition']));out=[]
  mapping=[]
  for x in range(10):
   for j in range(5):x=self.ix[j][index[j]][x]
   mapping.append(self.d['magnets'][x])
  for ch,digits in zip(text,self.digits(control,len(text))):
   x=sig.AZ.index(ch)
   for j in (range(4,-1,-1) if decrypt else range(5)):x=(self.cb if decrypt else self.cf)[j][cp[j]][x]
   out.append(sig.AZ[x]);selected={mapping[x] for x in digits}
   for j in selected:cp[j]=(cp[j]+(1 if self.rev[0][j] else -1))%26
  return ''.join(out)

def physical(text,key,decrypt=False):
 d=sig.data();orders=[key[n] for n in ('cipherrotors','controlrotors','indexrotors')];rev=[[int(x) for x in key[n]] for n in ('cipherorientation','controlorientation','indexorientation')];pos=[[sig.AZ.index(x) for x in key[n]] for n in ('cipherposition','controlposition')]+[list(map(int,key['indexposition']))];out=[]
 def path(bank,x,back=False):
  for j in (range(4,-1,-1) if back else range(5)):
   raw=d['index' if bank==2 else 'large'][orders[bank][j]-1];w=list(map(int,raw)) if bank==2 else [sig.AZ.index(c) for c in raw];pairs=sig.contact_oracle(w,pos[bank][j],rev[bank][j]);x=({v:k for k,v in pairs.items()} if back else pairs)[x]
  return x
 def advance(bank,j):pos[bank][j]=(pos[bank][j]+(1 if rev[bank][j] else -1))%26
 for ch in text:
  out.append(sig.AZ[path(0,sig.AZ.index(ch),decrypt)]);selected={d['magnets'][path(2,d['collector'][path(1,x,True)])] for x in range(5,9)}
  for j in selected:advance(0,j)
  if pos[1][2]==14:
   if pos[1][3]==14:advance(1,1)
   advance(1,3)
  advance(1,2)
 return ''.join(out)

def guarded_solve(model,observations,budget,cache_cap=64<<20,domain_cap=256<<20):
 """Same complete coupled recurrence, with conservative allocation admission."""
 q,r=model.q,model.r;N=q**r;fullc=(1<<N)-1;fullh=(1<<len(model.maps))-1;obs=collections.defaultdict(list)
 for t,p,c in observations:
  if not(0<=p<q and 0<=c<q and t>=0):raise ValueError('observation outside model')
  obs[t].append((p,c))
 length=max(obs,default=-1)+1;pred=TorusPredicates(model,budget,cache_cap);records=[];done=0;branches=0;covered=0;current_time=None;nodes={};peaknodes=0;reason=None;lastcontrol=None
 def admit(target):
  nonlocal peaknodes
  peaknodes=max(peaknodes,len(target));budget.check(force=True)
  # Count shared immutable integer objects once, plus a conservative per-node overhead.
  objects={}
  for (_,cs),hs in target.items():objects[id(cs)]=cs;objects[id(hs)]=hs
  envelope=sum(sys.getsizeof(v) for v in objects.values())+512*len(target)
  if envelope>domain_cap:raise toy.Limit('conservative_branch_domain_envelope_unresolved')
  if budget.receipt()['peak_RSS_bytes']>budget.memory-(128<<20):raise toy.Limit('allocation_headroom_unresolved')
 try:
  for control in itertools.product(range(q),repeat=r):
   budget.check(force=True);lastcontrol=control;nodes={((0,)*r,fullc):fullh};digits=model.digits(control,length)
   for t in range(length):
    current_time=t;filtered={}
    for (delta,cs),hs in nodes.items():
     budget.check();branches+=1
     for p,c in obs[t]:cs&=pred.get(delta,p,c)
     toy.merge(filtered,delta,cs,hs)
     if len(filtered)%16==0:admit(filtered)
    nodes=filtered;admit(nodes)
    if not nodes or t==length-1:break
    following={}
    for (delta,cs),hs in nodes.items():
     for mask,group in model.mask_groups(digits[t]):
      hh=hs&group
      if hh:
       new=tuple((v+(1 if getattr(model,'rev',[[0]*r])[0][j] else -1)*((mask>>j)&1))%q for j,v in enumerate(delta));toy.merge(following,new,cs,hh)
     if len(following)%16==0:admit(following)
    nodes=following;admit(nodes)
   compact=[];seenh=0
   for (delta,cs),hs in nodes.items():
    if seenh&hs:raise AssertionError('shared index class duplicated')
    seenh|=hs;covered+=toy.pop(cs)*sum(len(model.aliases[h]) for h in toy.bits(hs));compact.append(dict(index_classes=hex(hs),cipher_starts=hex(cs),final_offsets=list(delta)))
   if compact:records.append(dict(control=list(control),relations=compact))
   done+=1
 except toy.Limit as e:reason=str(e)
 return dict(completed=reason is None,reason=reason,exact_raw_key_count=str(covered) if reason is None else None,found_raw_keys_lower_bound=str(covered),control_starts_completed=done,control_starts_requested=q**r,relations=records,current_unfinished_control=list(lastcontrol) if reason else None,current_time_zero_based=current_time,peak_live_nodes=peaknodes,branches=branches,index_classes=len(model.maps),index_raw_states=sum(map(len,model.aliases)),backend_metrics=pred.metrics(),budget=budget.receipt(),domain_envelope_cap_bytes=domain_cap,K4_evaluations=0)

def fixture(number):
 plain=''.join(sig.AZ[(i*i+7*i+11)%26] for i in range(97));key=sig.key(1)
 c,q,x=(((3,5,7,11,13),(1,14,25,14,9),(1,3,5,7,9)),((25,0,14,2,19),(0,25,14,13,7),(9,7,5,3,1)))[number]
 key.update(cipherposition=''.join(sig.AZ[i] for i in c),controlposition=''.join(sig.AZ[i] for i in q),indexposition=''.join(map(str,x)))
 cipher=sig.Machine(key).crypt(plain);positions=list(range(13)) if number==0 else list(range(21,34))+list(range(63,74))
 return dict(number=number,plaintext=plain,ciphertext=cipher,key=key,observations=[(i,sig.AZ.index(plain[i]),sig.AZ.index(cipher[i])) for i in positions])
