"""Connected legal cipher DAGs and necessary static-collector consistency.
Supplied-anchor synthetic panels only; not full-domain inference or K4 search.
"""
import collections,copy,hashlib,json,time
import sigaba_joint_toy as toy
import sigaba_real_adapter as real
import sigaba_csp889 as sig
from sigaba_first_observation import prefix_delta

def enc(model,state,p):
 for j,s in enumerate(state):p=model.cf[j][s][p]
 return p

def moved(model,state,mask):return tuple((s+(1 if getattr(model,'rev',[[0]*model.r])[0][j] else -1)*((mask>>j)&1))%model.q for j,s in enumerate(state))
def mask_for(mapping,digits):
 mask=0
 for d in digits:mask|=1<<mapping[d]
 return mask

def prune(layers,edges,allowed=None):
 good=[set() for _ in layers];good[-1]=set(layers[-1]);back=[[] for _ in edges]
 for i in range(len(edges)-1,-1,-1):
  back[i]=[(u,m,v) for u,m,v in edges[i] if v in good[i+1] and (allowed is None or m in allowed[i])];good[i]={u for u,m,v in back[i]}
 reach=[set() for _ in layers];reach[0]=set(layers[0])&good[0];out=[[] for _ in edges]
 for i,row in enumerate(back):out[i]=sorted((u,m,v) for u,m,v in row if u in reach[i]);reach[i+1]={v for u,m,v in out[i]}
 return dict(layers=reach,edges=out,nonempty=bool(reach[-1]))

def build(model,anchor,observations,budget,legal_masks=None):
 if not observations:raise ValueError('nonempty consecutive known block required')
 start=observations[0][0]
 if [x[0] for x in observations]!=list(range(start,start+len(observations))):raise ValueError('DAG block must be consecutive')
 masks=range(1,(1<<model.r)-1) if legal_masks is None else tuple(legal_masks)
 layers=[{tuple(anchor)} if enc(model,anchor,observations[0][1])==observations[0][2] else set()];edges=[];points=1;states=len(layers[0]);edge_count=0
 for i,(_,p,c) in enumerate(observations[1:]):
  row=[];following=set()
  for state in sorted(layers[-1]):
   for mask in masks:
    budget.check();child=moved(model,state,mask);points+=1
    if enc(model,child,p)==c:row.append((state,mask,child));following.add(child)
  edges.append(row);layers.append(following);states+=len(following);edge_count+=len(row)
  budget.check(force=True)
  if budget.receipt()['peak_RSS_bytes']>budget.memory-(128<<20):raise toy.Limit('allocation_headroom_unresolved')
  if states>100000 or edge_count>1000000:raise toy.Limit('DAG_size_budget_unresolved')
 result=prune(layers,edges);result.update(cipher_points=points,states_constructed=states,edges_constructed=edge_count);return result

def necessary_filter(graph,collector_sets):
 if len(collector_sets)!=len(graph['edges']):raise ValueError('collector/transition alignment')
 sets=[tuple(sorted(set(x))) for x in collector_sets];counts=collections.Counter(sets);common={}
 for B,row in zip(sets,graph['edges']):
  allowed={m for u,m,v in row};common[B]=allowed if B not in common else common[B]&allowed
 empty=[list(B) for B,allowed in common.items() if not allowed];allowed=[common[B] for B in sets]
 constrained=prune(graph['layers'],graph['edges'],allowed)
 return dict(passes=not empty and constrained['nonempty'],empty_repeat_intersections=empty,input_sets=[list(B) for B in sets],distinct_inputs=len(counts),repeat_occurrences=sum(n-1 for n in counts.values()),repeated_input_classes=sum(n>1 for n in counts.values()),common_masks=[dict(input=list(B),masks=sorted(common[B]),occurrences=counts[B]) for B in sorted(common)],connected_filtered_states=sum(map(len,constrained['layers'])),connected_filtered_edges=sum(map(len,constrained['edges'])),not_claimed='A pass is necessary only, not one consistent physical index map or one globally repeat-consistent path.')

def physical_first(model,anchor,observations,digits,h,budget):
 state=tuple(anchor);path=[];checks=0
 for i,(time,p,c) in enumerate(observations):
  budget.check();checks+=1
  if enc(model,state,p)!=c:return False,checks,path
  if i+1<len(observations):
   mask=mask_for(model.maps[h],digits[time]);child=moved(model,state,mask);path.append((state,mask,child));state=child
 return True,checks,path

def encode_graph(graph):return dict(layers=[[list(s) for s in sorted(layer)] for layer in graph['layers']],edges=[[[list(u),m,list(v)] for u,m,v in row] for row in graph['edges']],nonempty=graph['nonempty'],states_constructed=graph.get('states_constructed'),edges_constructed=graph.get('edges_constructed'),cipher_points=graph.get('cipher_points'))

def finish_candidate(model,f,controller,anchor,h,first,digits,budget):
 a=first[0][0];last=first[-1][0];state=tuple(anchor)
 for time in range(a,last):state=moved(model,state,mask_for(model.maps[h],digits[time]))
 rest=[x for x in f['observations'] if x[0]>last];targets={time:(p,c) for time,p,c in rest};last_check=max(targets,default=last);second_pass=True;gap_steps=0
 for time in range(last,last_check):
  budget.check();state=moved(model,state,mask_for(model.maps[h],digits[time]));next_time=time+1
  if next_time in targets:
   p,c=targets[next_time]
   if enc(model,state,p)!=c:second_pass=False;break
  else:gap_steps+=1
 if not second_pass:return dict(index_class=h,raw_aliases=len(model.aliases[h]),second_block_passes=False,gap_steps_executed=gap_steps)
 prefix=prefix_delta(model,digits,h,a,budget);start=tuple((anchor[j]-prefix[j])%26 for j in range(5));key=copy.deepcopy(f['key']);key.update(cipherposition=''.join(sig.AZ[x] for x in start),controlposition=''.join(sig.AZ[x] for x in controller),indexposition=''.join(map(str,model.aliases[h][0])))
 plain=sig.Machine(key,model.d,model.t).crypt(f['ciphertext'],True);regenerated=sig.Machine(key,model.d,model.t).crypt(plain);assert regenerated==f['ciphertext'];assert all(sig.AZ.index(plain[t])==p for t,p,c in f['observations'])
 return dict(index_class=h,raw_aliases=len(model.aliases[h]),second_block_passes=True,second_block_exists=bool(rest),gap_steps_executed=gap_steps,original_cipher_start=list(start),representative_key=key,plaintext=plain,plaintext_sha256=hashlib.sha256(plain.encode()).hexdigest(),equals_generated_plaintext=plain==f['plaintext'],exact_full_ciphertext_regeneration=True)

def run_panel(number):
 budget=toy.Budget(60);f=real.fixture(number);model=real.RealModel(budget=budget);first=f['observations'][:13];a=first[0][0];plant_control=tuple(sig.AZ.index(x) for x in f['key']['controlposition']);plant_index=tuple(map(int,f['key']['indexposition']));plant_h=next(h for h,rows in enumerate(model.aliases) if plant_index in rows);direct=sig.Machine(f['key'],model.d,model.t);direct.crypt(f['plaintext'][:a]);true_anchor=tuple(direct.pos[0]);plant_digits=model.digits(plant_control,97);prefix=prefix_delta(model,plant_digits,plant_h,a,budget);seed=tuple(sig.AZ.index(x) for x in f['key']['cipherposition']);assert true_anchor==tuple((s+d)%26 for s,d in zip(seed,prefix));assert model.stream(f['plaintext'],f['key'])==f['ciphertext']
 anchors=[];attempts=[];pairs=[];graphs=[];reason=None;graph_bytes=0;total_false_negatives=0
 try:
  g=build(model,true_anchor,first,budget);assert g['nonempty'];anchors.append(('plant',true_anchor,g))
  matching=0
  for state_id in range(4096):
   budget.check();state=toy.unpack(state_id,26,5)
   if state==true_anchor or enc(model,state,first[0][1])!=first[0][2]:continue
   matching+=1;g=build(model,state,first,budget);attempts.append(dict(state_id=state_id,state=list(state),nonempty=g['nonempty'],states=g['states_constructed'],edges=g['edges_constructed']))
   if g['nonempty']:anchors.append((f'wrong-{len(anchors)}',state,g))
   if len(anchors)==3 or matching==16:break
  controls=[plant_control,(0,)*5,tuple((v+(j==2))%26 for j,v in enumerate(plant_control)),tuple((v+(j==0))%26 for j,v in enumerate(plant_control))];controls=list(dict.fromkeys(controls));digit_traces={q:model.digits(q,97) for q in controls}
  for label,anchor,g in anchors:
   encoded=encode_graph(g);raw=json.dumps(encoded,separators=(',',':')).encode();graph_bytes+=len(raw)
   if graph_bytes>64<<20:raise toy.Limit('DAG_output_budget_unresolved')
   graphs.append(dict(label=label,anchor=list(anchor),graph=encoded,sha256=hashlib.sha256(raw).hexdigest()))
   edge_sets=[set(row) for row in g['edges']]
   for q in controls:
    budget.check(force=True)
    if budget.receipt()['peak_RSS_bytes']>budget.memory-(128<<20):raise toy.Limit('allocation_headroom_unresolved')
    digits=digit_traces[q];started=time.monotonic();decision=necessary_filter(g,digits[a:a+12]);filter_time=time.monotonic()-started;started=time.monotonic();feasible=[];points=0;tested=0
    for h in range(len(model.maps)):
     ok,checks,path=physical_first(model,anchor,first,digits,h,budget);points+=checks;tested+=1
     if ok:
      assert all(edge in edge_sets[i] for i,edge in enumerate(path));feasible.append(h)
    physical_time=time.monotonic()-started;false_negative=bool(feasible) and not decision['passes'];total_false_negatives+=false_negative;assert not false_negative
    finals=[finish_candidate(model,f,q,anchor,h,first,digits,budget) for h in feasible]
    pairs.append(dict(anchor_label=label,anchor=list(anchor),controller=list(q),filter=decision,filter_seconds=filter_time,physical_seconds=physical_time,reachable_map_trials=tested,cipher_point_checks=points,first_window_feasible_classes=feasible,first_window_raw_index_aliases=sum(len(model.aliases[h]) for h in feasible),false_negative=false_negative,false_positive=decision['passes'] and not feasible,candidate_checks=finals,counterfactual_map_trials_skippable=0 if decision['passes'] else len(model.maps),counterfactual_cipher_checks_skippable=0 if decision['passes'] else points,physical_audit_was_actually_executed=True))
  plant_pair=next(p for p in pairs if p['anchor_label']=='plant' and tuple(p['controller'])==plant_control);assert plant_h in plant_pair['first_window_feasible_classes'];assert any(c.get('equals_generated_plaintext') for c in plant_pair['candidate_checks'])
 except toy.Limit as e:reason=str(e)
 return dict(id='CSP889-FILTER-019',fixture=f,completed=reason is None,reason=reason,anchor_attempts=attempts,selected_anchor_count=len(anchors),graphs=graphs,serialized_graph_bytes=graph_bytes,controller_panel=[list(q) for q in controls] if 'controls' in locals() else None,pairs=pairs,false_negatives=total_false_negatives,summary=dict(completed_pairs=len(pairs),filter_rejects=sum(not p['filter']['passes'] for p in pairs),filter_passes=sum(p['filter']['passes'] for p in pairs),false_positive_pairs=sum(p['false_positive'] for p in pairs),physical_feasible_pairs=sum(bool(p['first_window_feasible_classes']) for p in pairs),repeated_input_pair_count=sum(p['filter']['repeat_occurrences']>0 for p in pairs),actual_map_trials=sum(p['reachable_map_trials'] for p in pairs),counterfactual_map_trials_skippable=sum(p['counterfactual_map_trials_skippable'] for p in pairs),counterfactual_is_not_measured_savings=True),budget=budget.receipt(),K4_evaluations=0,full_domain_gate_passed=False,scope='Supplied local anchors and four declared controllers, exact reachable-map panel audit; not blind key recovery or unrestricted search.')
