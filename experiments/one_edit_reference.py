"""Independent tagged-token channel and global modular constraint oracle."""
from collections import Counter
import itertools,math
from one_edit_channel import AZ,WINDOWS
from one_edit_models import ALPHABETS,MODELS


def tagged(observed,e):
 tokens=[(c,i) for i,c in enumerate(observed)];p=e['position'];kind=e['kind']
 if kind=='substitute':tokens[p]=(e['latent_char'],p)
 elif kind=='insert_latent':tokens.insert(p,(e['latent_char'],None))
 elif kind=='delete_observed':tokens.pop(p)
 elif kind!='baseline':raise ValueError('bad channel')
 latent=''.join(c for c,_ in tokens);lt=[tag for _,tag in tokens];ot=[]
 for i in range(len(observed)):ot.append(next((j for j,(_,tag) in enumerate(tokens) if tag==i),None))
 return latent,tuple(ot),tuple(lt)


def reflected_forward(latent,e):
 # Recover observed by a list operation, not the production string slices.
 out=list(latent);p=e['position']
 if e['kind']=='substitute':out[p]=e['observed_char']
 elif e['kind']=='insert_latent':out.pop(p)
 elif e['kind']=='delete_observed':out.insert(p,e['observed_char'])
 return ''.join(out)


def raw_string_set(observed,alphabet):
 out={observed}
 for i in range(len(observed)):
  for c in alphabet:
   if c!=observed[i]:out.add(''.join(c if j==i else x for j,x in enumerate(observed)))
 for i in range(len(observed)+1):
  for c in alphabet:
   xs=list(observed);xs.insert(i,c);out.add(''.join(xs))
 for i in range(len(observed)):
  xs=list(observed);xs.pop(i);out.add(''.join(xs))
 return out


def periodic_global(latent,starts,m,words=WINDOWS,alphabet=None):
 a=ALPHABETS[m['alphabet']] if alphabet is None else alphabet;q=len(a);p=m['period'];sign=1 if m['equation']=='plus' else -1;key={};first_conflict=False
 for i,ch in enumerate(words[0][1],starts[0]):
  value=(a.index(latent[i])-sign*a.index(ch))%q;r=i%p
  if r in key and key[r]!=value:first_conflict=True
  key.setdefault(r,value)
 if first_conflict:return None,False
 assert len(key)==p
 complete=all((a.index(latent[i])-sign*a.index(ch))%q==key[i%p] for i,ch in enumerate(words[1][1],starts[1]))
 return tuple(key[j] for j in range(p)),complete


def audit_periodic_instances(result):
 cat=result['catalog'];rows=result['instance_results'];cache={};fits={(r['instance_id'],r['model_index']):r for r in result['first_periodic_fits']}
 for instance,row in zip(cat['instances'],rows):
  latent=cat['strings'][instance['latent_id']];s,t=instance['starts'];context=(latent[s:s+13],latent[t:t+11],s,t)
  if context not in cache:cache[context]=[periodic_global(latent,(s,t),m) for m in MODELS]
  first=0;all_=0
  for mi,(key,full) in enumerate(cache[context]):
   if key is not None:
    first|=1<<mi;all_|=int(full)<<mi;assert tuple(fits[(instance['instance_id'],mi)]['key_at_absolute_latent_position_zero'])==key
  assert first==int(row['first_fit_model_mask_hex'],16) and all_==int(row['all_fit_model_mask_hex'],16)
 return dict(complete_instance_model_sets_equal=True,unique_contexts=len(cache),instances=len(rows),structure_cases=len(rows)*48)


def tiny_controls():
 from one_edit_models import permutation_counts
 permutation_cases=0;periodic_cases=0
 for alphabet in ('AB','ABC'):
  q=len(alphabet)
  for n in (4,5,6):
   for j in range(4):
    latent=''.join(alphabet[(i*i+j*i+j)%q] for i in range(n));known={0:alphabet[j%q],n-2:alphabet[(j+1)%q]};possible=set();keys=0
    for route in itertools.permutations(range(n)):
     plain=''.join(latent[i] for i in route)
     if all(plain[i]==c for i,c in known.items()):possible.add(plain);keys+=1
    result=permutation_counts(latent,known);assert result['compatible']==bool(possible)
    if possible:assert int(result['distinct_plaintexts'])==len(possible) and int(result['position_permutation_keys'])==keys
    permutation_cases+=1
  for period,eq,j in itertools.product(range(1,4),('plus','beaufort'),range(8)):
   word1=''.join(alphabet[(i+j)%q] for i in range(4));word2=alphabet[(j+1)%q]*2;starts=(1,6);key=[(i+j)%q for i in range(period)];plain=list(alphabet[0]*9);plain[1:5]=word1;plain[6:8]=word2;sgn=1 if eq=='plus' else -1;cipher=''.join(alphabet[(sgn*alphabet.index(c)+key[i%period])%q] for i,c in enumerate(plain))
   if j%2:cipher=cipher[:7]+alphabet[(alphabet.index(cipher[7])+1)%q]+cipher[8:]
   m=dict(period=period,equation=eq,alphabet='toy');got,complete=periodic_global(cipher,starts,m,((1,word1),(6,word2)),alphabet)
   truth=[]
   for candidate in itertools.product(range(q),repeat=period):
    if all(alphabet[(sgn*alphabet.index(c)+candidate[i%period])%q]==cipher[i] for start,word in ((1,word1),(6,word2)) for i,c in enumerate(word,start)):truth.append(candidate)
   assert truth==([got] if complete and got is not None else []);periodic_cases+=1
 return dict(complete_permutation_truth_cases=permutation_cases,complete_periodic_key_truth_cases=periodic_cases)
