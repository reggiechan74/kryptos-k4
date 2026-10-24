"""Exact periodic keys and arbitrary-permutation classes under frozen edits."""
from collections import Counter,defaultdict,deque
import hashlib,itertools,math,resource,sys,time
from one_edit_channel import AZ,WINDOWS,catalog,mask,forward
ALPHABETS={'AZ':AZ,'KRYPTOS':'KRYPTOSABCDEFGHIJLMNQUVWXZ'}
MODELS=[dict(alphabet=name,equation=eq,period=p) for name,eq,p in itertools.product(ALPHABETS,('plus','beaufort'),range(1,13))]
FACT=[math.factorial(i) for i in range(99)]


def budget(start,seconds):
 if time.monotonic()-start>seconds:raise TimeoutError('frozen elapsed budget; unresolved')
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
 if rss>512*1024**2:raise MemoryError('frozen512MiB RSS budget; unresolved')


def periodic_crypt(text,key,model,decrypt=False):
 a=ALPHABETS[model['alphabet']];sign=1 if model['equation']=='plus' else -1
 return ''.join(a[((a.index(c)-key[i%len(key)]) if sign==1 and decrypt else (a.index(c)+key[i%len(key)]) if sign==1 else key[i%len(key)]-a.index(c))%26] for i,c in enumerate(text))


def training(fragment):
 if len(fragment)!=13:raise ValueError('complete first phrase ciphertext span required')
 out=[]
 for m in MODELS:
  a=ALPHABETS[m['alphabet']];p=m['period'];sgn=1 if m['equation']=='plus' else -1;key=[None]*p;ok=True
  for j,(c,plain) in enumerate(zip(fragment,WINDOWS[0][1])):
   v=(a.index(c)-sgn*a.index(plain))%26;r=j%p
   if key[r] is not None and key[r]!=v:ok=False;break
   key[r]=v
  if ok:assert None not in key
  out.append(key if ok else None)
 return out


def forecast(second,key,m,delta):
 if len(second)!=11:raise ValueError('complete second phrase ciphertext span required')
 a=ALPHABETS[m['alphabet']];p=m['period']
 return ''.join(a[((a.index(c)-key[(delta+j)%p]) if m['equation']=='plus' else key[(delta+j)%p]-a.index(c))%26] for j,c in enumerate(second))


def permutation_counts(latent,known):
 counts=Counter(latent);required=Counter(known.values());deficits={c:n-counts[c] for c,n in required.items() if n>counts[c]}
 if deficits:return dict(compatible=False,deficits=deficits)
 remain=counts-required;n=len(latent)-len(known)
 # Divide once: sequential integer floors would be wrong in general.
 plaintexts=math.factorial(n)//math.prod(math.factorial(v) for v in remain.values())
 keys=math.factorial(n)*math.prod(math.factorial(counts[c])//math.factorial(counts[c]-required[c]) for c in required)
 return dict(compatible=True,distinct_plaintexts=str(plaintexts),position_permutation_keys=str(keys),remaining_counts=dict(sorted(remain.items())))


def permutation_witnesses(latent,known):
 free=[i for i in range(len(latent)) if i not in known];remain=Counter(latent)-Counter(known.values());letters=sorted(remain.elements());plain=['']*len(latent)
 for i,c in known.items():plain[i]=c
 for i,c in zip(free,letters):plain[i]=c
 variants=[''.join(plain)]
 if len(set(letters))>1:
  a=free[0];b=next(i for i in free if plain[i]!=plain[a]);plain[a],plain[b]=plain[b],plain[a];variants.append(''.join(plain))
 out=[]
 for text in variants:
  bins=defaultdict(deque)
  for i,c in enumerate(latent):bins[c].append(i)
  route=[bins[c].popleft() for c in text];assert sorted(route)==list(range(len(latent)));regen=['']*len(latent)
  for i,j in enumerate(route):regen[j]=text[i]
  assert ''.join(regen)==latent
  out.append(dict(plaintext=text,plaintext_sha256=hashlib.sha256(text.encode()).hexdigest(),latent_position_at_each_plaintext_position_zero_based=route,latent_reencryption_verified=True,classification='arbitrary non-language ambiguity witness, not a K4 candidate'))
 return out


def diagnostics(latent,known):
 fixed=[i for i,p in known.items() if latent[i]==p];groups={};reject=False
 for i in sorted(known):
  if i+1 not in known:continue
  pair=known[i]+known[i+1];same=latent[i]==latent[i+1]
  if pair in groups and groups[pair]!=same:reject=True
  groups[pair]=same
 return dict(nonzero_strip_certificate_reject=bool(fixed),wheatstone_relaxed_pair_certificate_reject=reject,necessary_only_not_cipher_fit=True)


def select(observed,details=True,start=None,seconds=120):
 start=time.monotonic() if start is None else start;cat=catalog(observed);cache={};forecasts={};rows=[];first=[];full=[];perms=[];by_model=[dict(model=m,raw_first=0,raw_all=0,unique_first=0,unique_all=0) for m in MODELS];by_alignment={a:dict(admissible=0,permutation_compatible=0,periodic_first=0,periodic_all=0,strip_certificate_reject=0,wheatstone_certificate_reject=0) for a in ('ENGLISH_FIXED','OBSERVED_CELL_TRANSPORT')};perm_raw=0;perm_unique=0;lower={};upper={}
 for instance in cat['instances']:
  i=instance['instance_id'];latent=cat['strings'][instance['latent_id']];s,t=instance['starts'];known=mask((s,t));pc=permutation_counts(latent,known);diag=diagnostics(latent,known);frag=latent[s:s+13];second=latent[t:t+11];delta=t-s
  if frag not in cache:cache[frag]=training(frag)
  fk=(frag,second,delta)
  if fk not in forecasts:forecasts[fk]=[None if key is None else forecast(second,key,m,delta) for key,m in zip(cache[frag],MODELS)]
  firstmask=0;allmask=0
  for mi,(key,m,predicted) in enumerate(zip(cache[frag],MODELS,forecasts[fk])):
   if key is None:continue
   firstmask|=1<<mi;passed=predicted==WINDOWS[1][1]
   if passed:allmask|=1<<mi
   aliases=instance['aliases'];by_model[mi]['raw_first']+=len(aliases);by_model[mi]['unique_first']+=1;by_model[mi]['raw_all']+=len(aliases)*passed;by_model[mi]['unique_all']+=passed
   if details:
    absolute=[key[(r-s)%m['period']] for r in range(m['period'])];row=dict(instance_id=i,model_index=mi,key_at_absolute_latent_position_zero=absolute,predicted_berlin=predicted,all_pass=passed)
    if passed:
     plain=periodic_crypt(latent,absolute,m,True);assert all(plain[j]==p for j,p in known.items());assert periodic_crypt(plain,absolute,m)==latent
     assert all(forward(latent,cat['descriptions'][a['edit_id']])==observed for a in aliases)
     minimal=next(d for d in range(1,len(absolute)+1) if len(absolute)%d==0 and all(v==absolute[j%d] for j,v in enumerate(absolute)))
     row.update(plaintext=plain,plaintext_sha256=hashlib.sha256(plain.encode()).hexdigest(),latent_reencryption_verified=True,forward_channel_verified=True,primitive_key_period=minimal);full.append(row)
    first.append(row)
  if pc['compatible']:
   perm_raw+=len(instance['aliases']);perm_unique+=1;n=len(latent);volume=int(pc['distinct_plaintexts']);lower[n]=max(lower.get(n,0),volume);upper[n]=upper.get(n,0)+volume
   if details:
    witnesses=permutation_witnesses(latent,known)
    for w in witnesses:
     assert all(w['plaintext'][j]==p for j,p in known.items())
     assert all(forward(latent,cat['descriptions'][a['edit_id']])==observed for a in instance['aliases'])
    perms.append(dict(instance_id=i,**pc,witnesses=witnesses,all_alias_channels_verified=True))
  for alias in instance['aliases']:
   a=by_alignment[alias['alignment']];a['admissible']+=1;a['permutation_compatible']+=pc['compatible'];a['periodic_first']+=firstmask.bit_count() if hasattr(int,'bit_count') else bin(firstmask).count('1');a['periodic_all']+=allmask.bit_count() if hasattr(int,'bit_count') else bin(allmask).count('1');a['strip_certificate_reject']+=diag['nonzero_strip_certificate_reject'];a['wheatstone_certificate_reject']+=diag['wheatstone_relaxed_pair_certificate_reject']
  if details:rows.append(dict(instance_id=i,first_fit_model_mask_hex=hex(firstmask),all_fit_model_mask_hex=hex(allmask),permutation_compatible=pc['compatible'],**diag))
  if i%128==0:budget(start,seconds)
 summary=dict(raw_edits=cat['raw_edits'],raw_edit_kind_counts=cat['raw_edit_kind_counts'],unique_latent_strings=cat['unique_latent_strings'],unique_constraint_instances=cat['unique_constraint_instances'],gross_alignment_descriptions=cat['gross_alignment_descriptions'],admissible_alignment_descriptions=cat['admissible_alignment_descriptions'],inadmissible_alignment_descriptions=len(cat['alignment_inadmissible']),logical_periodic_checks=cat['admissible_alignment_descriptions']*48,logical_permutation_checks=cat['admissible_alignment_descriptions'],permutation_compatible_raw_alignment_cases=perm_raw,permutation_compatible_unique_instances=perm_unique,periodic_first_raw_cases=sum(r['raw_first'] for r in by_model),periodic_all_raw_cases=sum(r['raw_all'] for r in by_model),by_alignment=by_alignment,models=by_model,permutation_distinct_plaintext_union_lower_bound=sum(lower.values()),permutation_distinct_plaintext_union_upper_bound=sum(upper.values()),permutation_union_exact_count_not_computed=True,any_compatibility_is_not_evidence=True,cache_training_fragments=len(cache))
 for k in ('permutation_distinct_plaintext_union_lower_bound','permutation_distinct_plaintext_union_upper_bound'):summary[k]=str(summary[k])
 if not details:return summary
 return dict(summary=summary,catalog=cat,instance_results=rows,first_periodic_fits=first,complete_periodic_fits=full,permutation_classes=perms,distinct_periodic_full_plaintexts=len({r['plaintext'] for r in full}))
