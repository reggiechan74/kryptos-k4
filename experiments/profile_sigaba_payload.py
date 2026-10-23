"""Exact first-observation reparameterization of full independent cipher starts."""
import collections,sys
import sigaba_joint_toy as toy
from sigaba_domain_identity import Domain
from sigaba_sparse_ownership import ReservedPredicates

def prefix_delta(model,digits,h,anchor,budget):
 delta=[0]*model.r
 for time in range(anchor):
  budget.check();mask=0
  for digit in digits[time]:mask|=1<<model.maps[h][digit]
  for j in range(model.r):
   if mask>>j&1:delta[j]=(delta[j]+(1 if getattr(model,'rev',[[0]*model.r])[0][j] else -1))%model.q
 return tuple(delta)

def solve(model,observations,budget,cache_cap=64<<20,domain_cap=256<<20,full_initial_domain=True):
 if full_initial_domain is not True:raise ValueError('Restricted starts require map-dependent translated restrictions')
 q,r=model.q,model.r;fullc=Domain((1<<(q**r))-1);obs=collections.defaultdict(list)
 for t,p,c in observations:
  if not(0<=p<q and 0<=c<q and t>=0):raise ValueError('invalid observation')
  obs[t].append((p,c))
 pred=ReservedPredicates(model,budget,cache_cap);length=max(obs,default=-1)+1;anchor=min(obs,default=0);payload_profile=None;reconstructed_classes=0;records=[];done=0;covered=0;branches=0;owner_transitions=0;peaknodes=0;peakowners=0;current_time=None;lastcontrol=None;reason=None
 def merge(target,delta,cs,owners):
  if cs and owners:
   key=(delta,cs)
   if key in target:target[key].extend(owners)
   else:target[key]=list(owners)
 def admit(nodes):
  nonlocal peaknodes,peakowners,payload_profile
  peaknodes=max(peaknodes,len(nodes));peakowners=max(peakowners,sum(map(len,nodes.values())));budget.check(force=True);objects={}
  for (_,cs),owners in nodes.items():objects[id(cs)]=cs;objects[id(cs.bits)]=cs.bits;objects[id(owners)]=owners
  envelope=sum(sys.getsizeof(x) for x in objects.values())+512*len(nodes)+28*sum(map(len,nodes.values()))
  if envelope>domain_cap:
   payloads={id(cs.bits):cs.bits for (_,cs),owners in nodes.items()};counts=[value.bit_count() if hasattr(int,'bit_count') else bin(value).count('1') for value in payloads.values()]
   payload_profile=dict(time_zero_based=current_time,nodes=len(nodes),distinct_payload_objects=len(payloads),distinct_exact_set_values=len({cs for (_,cs),owners in nodes.items()}),integer_payload_bytes=sum(sys.getsizeof(v) for v in payloads.values()),packed_u32_payload_estimated_bytes=sum(4*n+sys.getsizeof(b'') for n in counts),cardinality_histogram=dict(sorted(collections.Counter(counts).items())),minimum_density=min(counts)/(q**r),maximum_density=max(counts)/(q**r),domain_envelope_bytes=envelope,domain_envelope_cap_bytes=domain_cap,state_universe=q**r,accounting='Distinct live immutable payload objects; sum of represented state counts is not a count of distinct keys or plaintexts.')
   raise toy.Limit('conservative_branch_domain_envelope_unresolved')
  if budget.receipt()['peak_RSS_bytes']>budget.memory-(128<<20):raise toy.Limit('allocation_headroom_unresolved')
 try:
  import itertools
  for control in itertools.product(range(q),repeat=r):
   budget.check(force=True);lastcontrol=control;nodes={((0,)*r,fullc):list(range(len(model.maps)))};digits=model.digits(control,length)
   for t in range(anchor,length):
    current_time=t;filtered={}
    for (delta,cs),owners in nodes.items():
     budget.check();branches+=1
     for p,c in obs[t]:cs=cs.meet(pred.get(delta,p,c))
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
     original=cs if not any(prefix) else Domain(pred.translate(cs.bits,prefix))
     original_delta=tuple((prefix[j]+delta[j])%q for j in range(r))
     merge(original_nodes,original_delta,original,[h]);reconstructed_classes+=1
     if len(original_nodes)%16==0:admit(original_nodes)
   admit(original_nodes);compact=[];seen=set();local_covered=0
   for (delta,cs),owners in original_nodes.items():
    if seen.intersection(owners):raise AssertionError('duplicate reconstructed owner')
    seen.update(owners);hs=0
    for h in owners:hs|=1<<h
    local_covered+=toy.pop(cs.bits)*sum(len(model.aliases[h]) for h in owners)
    compact.append(dict(index_classes=hex(hs),cipher_starts=hex(cs.bits),final_offsets=list(delta)))
   if compact:records.append(dict(control=list(control),relations=compact))
   covered+=local_covered
   done+=1
 except toy.Limit as e:reason=str(e)
 return dict(payload_profile=payload_profile,first_observed_time=anchor,map_dependent_classes_reconstructed=reconstructed_classes,completed=reason is None,reason=reason,exact_raw_key_count=str(covered) if reason is None else None,found_raw_keys_lower_bound=str(covered),control_starts_completed=done,control_starts_requested=q**r,relations=records,current_unfinished_control=list(lastcontrol) if reason else None,current_time_zero_based=current_time,peak_live_nodes=peaknodes,peak_index_owners=peakowners,owner_transitions=owner_transitions,branches=branches,index_classes=len(model.maps),index_raw_states=sum(map(len,model.aliases)),backend_metrics=pred.metrics(),budget=budget.receipt(),domain_envelope_cap_bytes=domain_cap,K4_evaluations=0)
