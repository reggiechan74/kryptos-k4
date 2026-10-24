"""Exact necessary-root memoization only; physical owner recurrence remains024."""
import collections,copy,json,sys,time
import sigaba_unknown_anchor_collector as prior
from sigaba_unknown_anchor_collector import toy,Domain,ReservedPredicates,prefix_delta,root_support

class SupportCache:
 def __init__(self,cap=64<<20):
  self.cap=cap;self.model=None;self.cache=collections.OrderedDict();self.bytes=0;self.peak=0;self.hits=0;self.misses=0;self.evictions=0;self.signature_calls=0
 def signature(self,model,observations,digits,budget):
  if self.model is None:self.model=model
  if self.model is not model:raise ValueError('Support cache cannot cross immutable model instances')
  budget.check(force=True);start,block=prior.first_block(observations);classes={};names=[];sequence=[];domains=[]
  for t,_ in block[:-1]:
   B=tuple(sorted(set(digits[t])))
   if B not in classes:
    budget.check(force=True);classes[B]=len(names);names.append(B);domains.append(tuple(sorted(mask for mask,owners in model.mask_groups(B) if owners)))
   sequence.append(classes[B])
  self.signature_calls+=1
  return (start,tuple((t,tuple(map(tuple,pairs))) for t,pairs in block),tuple(sequence),tuple(domains),8),names
 def evaluate(self,model,observations,digits,budget,predicate,progress=None):
  key,names=self.signature(model,observations,digits,budget)
  if key in self.cache:
   self.hits+=1;self.cache.move_to_end(key);roots,canonical,cost=self.cache[key];receipt=copy.deepcopy(canonical);receipt['support_cache_hit']=True;receipt['reused_original_edge_support_calls']=receipt.get('implicit_edge_support_calls',0);receipt['implicit_edge_support_calls']=0
   if progress is not None:progress.update(stage='cached_necessary_support',layers_built=receipt['layers'],sweep=None,layer=None)
  else:
   self.misses+=1;roots,receipt=prior.root_support(model,observations,digits,budget,predicate,progress=progress);receipt=copy.deepcopy(receipt);receipt['support_cache_hit']=False
   canonical=copy.deepcopy(receipt);byname={x:i for i,x in enumerate(names)}
   for row in canonical.get('allowed_masks',[]):row['collector_class']=byname[tuple(row.pop('collector'))]
   # Conservative payload envelope; whole-process measured RSS remains authoritative.
   cost=sys.getsizeof(roots)+4*len(repr(key))+4*len(json.dumps(canonical))+4096
   if cost<=self.cap:
    while self.cache and self.bytes+cost>self.cap:
     _,(_,_,oldcost)=self.cache.popitem(last=False);self.bytes-=oldcost;self.evictions+=1
    self.cache[key]=(roots,canonical,cost);self.bytes+=cost;self.peak=max(self.peak,self.bytes)
   return roots,receipt
  for row in receipt.get('allowed_masks',[]):row['collector']=list(names[row.pop('collector_class')])
  return roots,receipt
 def metrics(self):return dict(signature_calls=self.signature_calls,hits=self.hits,misses=self.misses,evictions=self.evictions,live_bytes=self.bytes,peak_bytes=self.peak,cap_bytes=self.cap,cached_roots_only=True,physical_keys_cached=False)

def solve(model,observations,budget,cache_cap=64<<20,domain_cap=256<<20,full_initial_domain=True,storage_policy='auto',filter_enabled=True,support_cache_cap=64<<20):
 if full_initial_domain is not True:raise ValueError('Restricted starts require map-dependent translated restrictions')
 support_cache=SupportCache(support_cache_cap)
 q,r=model.q,model.r
 if q**r>2**32:raise ValueError('state universe exceeds u32 encoding')
 fullc=Domain((1<<(q**r))-1,storage_policy);obs=collections.defaultdict(list)
 for t,p,c in observations:
  if not(0<=p<q and 0<=c<q and t>=0):raise ValueError('invalid observation')
  obs[t].append((p,c))
 pred=ReservedPredicates(model,budget,cache_cap);length=max(obs,default=-1)+1;anchor=min(obs,default=0);direct_state_checks=0;output_bytes=0;reconstructed_classes=0;records=[];done=0;covered=0;branches=0;owner_transitions=0;peaknodes=0;peakowners=0;current_time=None;lastcontrol=None;reason=None
 filters=[];filter_started=0;filter_seconds=0.0;filter_progress={}
 def merge(target,delta,cs,owners):
  if cs and owners:
   key=(delta,cs)
   if key in target:target[key].extend(owners)
   else:target[key]=list(owners)
 def admit(nodes):
  nonlocal peaknodes,peakowners
  peaknodes=max(peaknodes,len(nodes));peakowners=max(peakowners,sum(map(len,nodes.values())));budget.check(force=True);objects={}
  for (_,cs),owners in nodes.items():objects[id(cs)]=cs;objects[id(cs.payload)]=cs.payload;objects[id(owners)]=owners
  envelope=sum(sys.getsizeof(x) for x in objects.values())+512*len(nodes)+28*sum(map(len,nodes.values()))
  if envelope>domain_cap:raise toy.Limit('conservative_branch_domain_envelope_unresolved')
  if budget.receipt()['peak_RSS_bytes']>budget.memory-(128<<20):raise toy.Limit('allocation_headroom_unresolved')
 try:
  import itertools
  for control in itertools.product(range(q),repeat=r):
   budget.check(force=True);lastcontrol=control;digits=model.digits(control,length);initial=fullc
   if filter_enabled:
    filter_started+=1;clock=time.monotonic()
    roots,receipt=support_cache.evaluate(model,observations,digits,budget,pred,progress=filter_progress)
    filter_seconds+=time.monotonic()-clock;filters.append(receipt);initial=Domain(roots,storage_policy)
   nodes={((0,)*r,initial):list(range(len(model.maps)))} if initial else {}
   for t in range(anchor,length):
    current_time=t;filtered={}
    for (delta,cs),owners in nodes.items():
     budget.check();branches+=1
     for p,c in obs[t]:
      cs,checked=cs.intersect(delta,p,c,model,pred,budget);direct_state_checks+=checked
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
   original_nodes={}
   for (delta,cs),owners in nodes.items():
    for h in owners:
     budget.check();prefix=prefix_delta(model,digits,h,anchor,budget)
     original=cs.preimage(prefix,model,pred,budget)
     original_delta=tuple((prefix[j]+delta[j])%q for j in range(r))
     merge(original_nodes,original_delta,original,[h]);reconstructed_classes+=1
     if len(original_nodes)%16==0:admit(original_nodes)
   admit(original_nodes);compact=[];seen=set();local_covered=0;local_output_bytes=0
   for (delta,cs),owners in original_nodes.items():
    if seen.intersection(owners):raise AssertionError('duplicate reconstructed owner')
    seen.update(owners);hs=0
    for h in owners:hs|=1<<h
    local_covered+=cs.count*sum(len(model.aliases[h]) for h in owners)
    encoded=cs.encode();local_output_bytes+=len(encoded['data'])+len(hex(hs))+256
    if output_bytes+local_output_bytes>256<<20:raise toy.Limit('compact_output_budget_unresolved')
    compact.append(dict(index_classes=hex(hs),cipher_domain=encoded,final_offsets=list(delta)))
   if compact:records.append(dict(control=list(control),relations=compact))
   covered+=local_covered;output_bytes+=local_output_bytes
   done+=1
 except toy.Limit as e:reason=str(e)
 return dict(support_cache=support_cache.metrics(),filter_progress=filter_progress,unfinished_filter_seconds=(time.monotonic()-clock) if filter_started>len(filters) else None,filter_enabled=filter_enabled,filters_started=filter_started,filters_completed=len(filters),filter_seconds_completed=filter_seconds,filter_receipts=filters,storage_policy=storage_policy,direct_state_evaluations=direct_state_checks,compact_output_accounted_bytes=output_bytes,first_observed_time=anchor,map_dependent_classes_reconstructed=reconstructed_classes,completed=reason is None,reason=reason,exact_raw_key_count=str(covered) if reason is None else None,found_raw_keys_lower_bound=str(covered),control_starts_completed=done,control_starts_requested=q**r,relations=records,current_unfinished_control=list(lastcontrol) if reason and lastcontrol is not None else None,current_time_zero_based=current_time,peak_live_nodes=peaknodes,peak_index_owners=peakowners,owner_transitions=owner_transitions,branches=branches,index_classes=len(model.maps),index_raw_states=sum(map(len,model.aliases)),backend_metrics=pred.metrics(),budget=budget.receipt(),domain_envelope_cap_bytes=domain_cap,K4_evaluations=0)
