"""Exact reachable-index ownership, dense cipher domains; synthetic gate only."""
import collections,sys
import sigaba_joint_toy as toy
from sigaba_torus import TorusPredicates

class ReservedPredicates(TorusPredicates):
 def __init__(self,model,budget,cap=64<<20):
  self.m=model;self.b=budget;self.total_cap=cap;self.mask_cap=cap//4;self.cap=cap-self.mask_cap;self.cache=collections.OrderedDict();self.cache_bytes=0;self.peak_bytes=0;self.hits=0;self.builds=0;self.evictions=0;self.translations=0;self.base_hits=0;self.calls=0;self.builder=toy.Predicates(model,budget,cap=0);self.N=model.q**model.r;self.full=(1<<self.N)-1;self.masks=collections.OrderedDict();self.mask_bytes=0;self.mask_peak=0;self.mask_evictions=0;self.mask_builds=0
 def translate(self,value,delta):
  if value<0 or value>>self.N or len(delta)!=self.m.r:raise ValueError('outside fixed torus')
  q,r=self.m.q,self.m.r
  for j,d in enumerate(delta):
   d%=q
   if not d:continue
   stride=q**(r-1-j);period=q*stride;shift=d*stride;key=(j,d)
   if key in self.masks:self.masks.move_to_end(key);low,high,size=self.masks[key]
   else:
    low=(self.full//((1<<period)-1))*((1<<shift)-1);high=self.full^low;size=sys.getsizeof(low)+sys.getsizeof(high)+256;self.mask_builds+=1
    if size<=self.mask_cap:
     while self.masks and self.mask_bytes+size>self.mask_cap:
      _,(_,_,old)=self.masks.popitem(last=False);self.mask_bytes-=old;self.mask_evictions+=1
     self.masks[key]=(low,high,size);self.mask_bytes+=size;self.mask_peak=max(self.mask_peak,self.mask_bytes)
   value=((value&low)<<(period-shift))|((value&high)>>shift)
  return value
 def metrics(self):
  r=super().metrics();r.update(value_cache_cap_bytes=self.cap,mask_cache_cap_bytes=self.mask_cap,total_cache_cap_bytes=self.total_cap,mask_builds=self.mask_builds,mask_evictions=self.mask_evictions,mask_cache_peak_bytes=self.mask_peak,total_cache_peak_accounting_upper_bound=self.peak_bytes+self.mask_peak);return r

def solve(model,observations,budget,cache_cap=64<<20,domain_cap=256<<20):
 q,r=model.q,model.r;fullc=(1<<(q**r))-1;obs=collections.defaultdict(list)
 for t,p,c in observations:
  if not(0<=p<q and 0<=c<q and t>=0):raise ValueError('invalid observation')
  obs[t].append((p,c))
 pred=ReservedPredicates(model,budget,cache_cap);length=max(obs,default=-1)+1;records=[];done=0;covered=0;branches=0;owner_transitions=0;peaknodes=0;peakowners=0;current_time=None;lastcontrol=None;reason=None
 def merge(target,delta,cs,owners):
  if cs and owners:
   key=(delta,cs)
   if key in target:target[key].extend(owners)
   else:target[key]=list(owners)
 def admit(nodes):
  nonlocal peaknodes,peakowners
  peaknodes=max(peaknodes,len(nodes));peakowners=max(peakowners,sum(map(len,nodes.values())));budget.check(force=True);objects={}
  for (_,cs),owners in nodes.items():objects[id(cs)]=cs;objects[id(owners)]=owners
  envelope=sum(sys.getsizeof(x) for x in objects.values())+512*len(nodes)+28*sum(map(len,nodes.values()))
  if envelope>domain_cap:raise toy.Limit('conservative_branch_domain_envelope_unresolved')
  if budget.receipt()['peak_RSS_bytes']>budget.memory-(128<<20):raise toy.Limit('allocation_headroom_unresolved')
 try:
  import itertools
  for control in itertools.product(range(q),repeat=r):
   budget.check(force=True);lastcontrol=control;nodes={((0,)*r,fullc):list(range(len(model.maps)))};digits=model.digits(control,length)
   for t in range(length):
    current_time=t;filtered={}
    for (delta,cs),owners in nodes.items():
     budget.check();branches+=1
     for p,c in obs[t]:cs&=pred.get(delta,p,c)
     merge(filtered,delta,cs,owners)
     if len(filtered)%16==0:admit(filtered)
    nodes=filtered
    for owners in nodes.values():owners.sort()
    admit(nodes)
    if not nodes or t==length-1:break
    following={}
    for (delta,cs),owners in nodes.items():
     partitions={}
     for h in owners:
      budget.check();mask=0
      for digit in digits[t]:mask|=1<<model.maps[h][digit]
      partitions.setdefault(mask,[]).append(h);owner_transitions+=1
     for mask,part in partitions.items():
      new=tuple((v+(1 if getattr(model,'rev',[[0]*r])[0][j] else -1)*((mask>>j)&1))%q for j,v in enumerate(delta));merge(following,new,cs,part)
     if len(following)%16==0:admit(following)
    nodes=following
    for owners in nodes.values():owners.sort()
    admit(nodes)
   compact=[];seen=set()
   for (delta,cs),owners in nodes.items():
    if seen.intersection(owners):raise AssertionError('duplicate owner');
    seen.update(owners);hs=0
    for h in owners:hs|=1<<h
    covered+=toy.pop(cs)*sum(len(model.aliases[h]) for h in owners);compact.append(dict(index_classes=hex(hs),cipher_starts=hex(cs),final_offsets=list(delta)))
   if compact:records.append(dict(control=list(control),relations=compact))
   done+=1
 except toy.Limit as e:reason=str(e)
 return dict(completed=reason is None,reason=reason,exact_raw_key_count=str(covered) if reason is None else None,found_raw_keys_lower_bound=str(covered),control_starts_completed=done,control_starts_requested=q**r,relations=records,current_unfinished_control=list(lastcontrol) if reason else None,current_time_zero_based=current_time,peak_live_nodes=peaknodes,peak_index_owners=peakowners,owner_transitions=owner_transitions,branches=branches,index_classes=len(model.maps),index_raw_states=sum(map(len,model.aliases)),backend_metrics=pred.metrics(),budget=budget.receipt(),domain_envelope_cap_bytes=domain_cap,K4_evaluations=0)
