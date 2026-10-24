"""Unknown-anchor implicit connected support, then exact persistent-map inference.
Synthetic engineering only. Necessary filter success is not a physical key.
"""
import sys,time
import sigaba_joint_toy as toy
import sigaba_compressed_ownership as compact
from sigaba_sparse_ownership import ReservedPredicates


def step(model,mask):
    return tuple((1 if getattr(model,'rev',[[0]*model.r])[0][j] else -1)*((mask>>j)&1) for j in range(model.r))


def first_block(observations):
    bytime={}
    for t,p,c in observations:bytime.setdefault(t,[]).append((p,c))
    start=min(bytime,default=0);block=[];t=start
    while t in bytime:block.append((t,bytime[t]));t+=1
    return start,block


def root_support(model,observations,digits,budget,predicate,max_passes=8,layer_cap=128<<20,progress=None):
    """Monotone necessary relaxation with every initial cipher state admitted."""
    progress={} if progress is None else progress;progress.update(stage='build_layers',layers_built=0,sweep=None,layer=None)
    start,block=first_block(observations);full=(1<<(model.q**model.r))-1
    if not block:return full,dict(first_time=start,layers=0,passes=0,fixed_point=True,repeats=0,initial_roots=model.q**model.r,retained_roots=model.q**model.r)
    layers=[];previous=()
    def guard():
        budget.check(force=True)
        if sum(sys.getsizeof(v) for v in {id(x):x for x in list(layers)+list(previous)}.values())+4*sys.getsizeof(full)+4096*len(layers)>layer_cap:raise toy.Limit('implicit_layer_envelope_unresolved')
        if budget.receipt()['peak_RSS_bytes']>budget.memory-(128<<20):raise toy.Limit('allocation_headroom_unresolved')
    for time,pairs in block:
        value=full
        for p,c in pairs:
            budget.check();value&=predicate.get((0,)*model.r,p,c)
        layers.append(value);progress['layers_built']=len(layers);guard()
    inputs=[tuple(sorted(set(digits[t]))) for t,_ in block[:-1]]
    allowed={}
    progress['stage']='reachable_masks'
    for B in inputs:
        if B not in allowed:
            budget.check(force=True);allowed[B]={mask for mask,owners in model.mask_groups(B) if owners};guard()
    initial=toy.pop(layers[0]);passes=0;fixed=False;edge_calls=0
    for sweep in range(max_passes):
        progress.update(stage='connected_support',sweep=sweep);previous=tuple(layers);old_masks={B:frozenset(v) for B,v in allowed.items()}
        for backward in (True,False):
            supported={B:set(v) for B,v in allowed.items()}
            positions=range(len(inputs)-1,-1,-1) if backward else range(len(inputs))
            for i in positions:
                progress.update(direction='backward' if backward else 'forward',layer=i);budget.check();B=inputs[i];union=0;local=set()
                for mask in sorted(allowed[B]):
                    budget.check();delta=step(model,mask)
                    source=layers[i]&predicate.translate(layers[i+1],delta);edge_calls+=1
                    if source:
                        local.add(mask)
                        union|=source if backward else predicate.translate(source,tuple(-x for x in delta))
                supported[B]&=local
                target=i if backward else i+1;layers[target]&=union;guard()
            for B in allowed:allowed[B]&=supported[B]
            if any(not v for v in allowed.values()):layers[0]=0;break
        passes+=1
        if not layers[0]:break
        if tuple(layers)==previous and all(allowed[B]==old_masks[B] for B in allowed):fixed=True;break
    return layers[0],dict(first_time=start,layers=len(layers),passes=passes,fixed_point=fixed,repeats=len(inputs)-len(set(inputs)),initial_roots=initial,retained_roots=toy.pop(layers[0]),implicit_edge_support_calls=edge_calls,allowed_masks=[dict(collector=list(B),masks=sorted(allowed[B])) for B in sorted(allowed)],not_a_physical_key=True)

# Exact recurrence retained from COMPACT-018; only controller-specific initial
# necessary root restriction is inserted. Baseline module is not modified.
import collections
from sigaba_compact_domain import Domain
from sigaba_compressed_ownership import prefix_delta
def solve(model,observations,budget,cache_cap=64<<20,domain_cap=256<<20,full_initial_domain=True,storage_policy='auto',filter_enabled=True):
 if full_initial_domain is not True:raise ValueError('Restricted starts require map-dependent translated restrictions')
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
    roots,receipt=root_support(model,observations,digits,budget,pred,progress=filter_progress)
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
 return dict(filter_progress=filter_progress,unfinished_filter_seconds=(time.monotonic()-clock) if filter_started>len(filters) else None,filter_enabled=filter_enabled,filters_started=filter_started,filters_completed=len(filters),filter_seconds_completed=filter_seconds,filter_receipts=filters,storage_policy=storage_policy,direct_state_evaluations=direct_state_checks,compact_output_accounted_bytes=output_bytes,first_observed_time=anchor,map_dependent_classes_reconstructed=reconstructed_classes,completed=reason is None,reason=reason,exact_raw_key_count=str(covered) if reason is None else None,found_raw_keys_lower_bound=str(covered),control_starts_completed=done,control_starts_requested=q**r,relations=records,current_unfinished_control=list(lastcontrol) if reason and lastcontrol is not None else None,current_time_zero_based=current_time,peak_live_nodes=peaknodes,peak_index_owners=peakowners,owner_transitions=owner_transitions,branches=branches,index_classes=len(model.maps),index_raw_states=sum(map(len,model.aliases)),backend_metrics=pred.metrics(),budget=budget.receipt(),domain_envelope_cap_bytes=domain_cap,K4_evaluations=0)
