"""Exact source-rule constraints; no K4 evaluation or invented context trigger."""
import collections,itertools,math
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';KRYPTOS='KRYPTOSABCDEFGHIJLMNQUVWXZ';ALPHABETS={'AZ':AZ,'KRYPTOS':KRYPTOS}
WORDS=[('K1','ILLUSION','IQLUSION','intent attributed by Dunin'),('K2','UNDERGROUND','UNDERGRUUND','intent attributed by Dunin'),('K3','DESPERATELY','DESPARATLY','intent not established'),('USER','MISTAKE','MISTSKE','illustration only')]

def alignments(source,target):
 n,m=len(source),len(target);d=[[0]*(m+1) for _ in range(n+1)]
 for i in range(n+1):d[i][0]=i
 for j in range(m+1):d[0][j]=j
 for i in range(1,n+1):
  for j in range(1,m+1):d[i][j]=min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(source[i-1]!=target[j-1]))
 def walk(i,j):
  if i==0 and j==0:return [[]]
  out=[]
  if i and j and d[i][j]==d[i-1][j-1]+(source[i-1]!=target[j-1]):
   c=dict(op='M' if source[i-1]==target[j-1] else 'S',source_index=i-1,target_index=j-1,source=source[i-1],target=target[j-1])
   out += [x+[c] for x in walk(i-1,j-1)]
  if i and d[i][j]==d[i-1][j]+1:
   c=dict(op='D',source_index=i-1,target_index=None,source=source[i-1],target='');out += [x+[c] for x in walk(i-1,j)]
  if j and d[i][j]==d[i][j-1]+1:
   c=dict(op='I',source_index=None,target_index=j-1,source='',target=target[j-1]);out += [x+[c] for x in walk(i,j-1)]
  return out
 return dict(distance=d[n][m],alignments=walk(n,m))

def apply_script(source,columns):
 i=0;out=[]
 for c in columns:
  if c['op']!='I':
   if i>=len(source) or source[i]!=c['source']:raise ValueError('source/script mismatch')
   i+=1
  if c['op']!='D':out.append(c['target'])
 if i!=len(source):raise ValueError('unconsumed source')
 return ''.join(out)
def inverse(columns):return [dict(op={'M':'M','S':'S','I':'D','D':'I'}[c['op']],source_index=c['target_index'],target_index=c['source_index'],source=c['target'],target=c['source']) for c in columns]

def infer_function(pairs,alphabet=AZ,injective=False):
 mapping={};witness={};targets={}
 for ident,source,target in pairs:
  if len(source)!=len(target):return dict(compatible=False,completion_count=0,reason='length changes',witness=dict(pair=ident,source_length=len(source),target_length=len(target)))
  for i,(a,b) in enumerate(zip(source,target)):
   if a not in alphabet or b not in alphabet:raise ValueError('outside alphabet')
   here=dict(pair=ident,index=i,source=a,target=b)
   if a in mapping and mapping[a]!=b:return dict(compatible=False,completion_count=0,reason='one input requires different outputs',witness=[witness[a],here])
   if injective and b in targets and targets[b]['source']!=a:return dict(compatible=False,completion_count=0,reason='different inputs require same output',witness=[targets[b],here])
   mapping[a]=b;witness[a]=here;targets[b]=here
 free=len(alphabet)-len(mapping)
 return dict(compatible=True,completion_count=math.factorial(free) if injective else len(alphabet)**free,free_input_symbols=free,mapping=mapping)

def affine_candidates(pairs,alphabet,invertible=True):
 out=[]
 for a in range(len(alphabet)):
  if invertible and math.gcd(a,len(alphabet))!=1:continue
  for b in range(len(alphabet)):
   if all(alphabet[(a*alphabet.index(x)+b)%len(alphabet)]==y for x,y in pairs):out.append(dict(a=a,b=b,invertible=math.gcd(a,len(alphabet))==1))
 return out

def keyboard_coordinates():return {c:(4*i+shift,row) for row,(letters,shift) in enumerate([('QWERTYUIOP',0),('ASDFGHJKL',1),('ZXCVBNM',3)]) for i,c in enumerate(letters)}
def keyboard_apply(text,delta):
 k=keyboard_coordinates();inv={v:c for c,v in k.items()};out=[]
 for c in text:
  x,y=k[c];q=(x+delta[0],y+delta[1])
  if q not in inv:raise ValueError('outside fixed keyboard domain')
  out.append(inv[q])
 return ''.join(out)

def masks(alphabet):
 words='IQLUSIONUNDERGRUUND';correct='ILLUSIONUNDERGROUND'
 full=[(alphabet.index(b)-alphabet.index(a))%26 for a,b in zip(words,correct)]
 sparse=[v for v in full if v]
 return {'changed_only':sparse,'neutral_padded_word_pair':full}
def translate(text,key,alphabet,phase=0,inverse=False):
 direction=-1 if inverse else 1
 return ''.join(alphabet[(alphabet.index(c)+direction*key[(i+phase)%len(key)])%len(alphabet)] for i,c in enumerate(text))

def full_sources(controls):
 out=[]
 for ident,key,wrong,right in [('K1','k1','IQLUSION','ILLUSION'),('K2','k2_as_inscribed','UNDERGRUUND','UNDERGROUND'),('K3','k3','DESPARATLY','DESPERATELY')]:
  literal=controls[key]['plaintext'];assert literal.count(wrong)==1;normal=literal.replace(wrong,right)
  keep=lambda s:''.join(c for c in s if c in AZ)
  out.append(dict(id=ident,literal=literal,comparison=normal,normalized_literal=keep(literal),normalized_comparison=keep(normal),word_literal_start_zero_based=literal.index(wrong),word_normalized_start_zero_based=keep(literal).index(wrong)))
 return out

def investigate(controls):
 inventory=[]
 for ident,normal,literal,intent in WORDS:
  f=alignments(normal,literal);r=alignments(literal,normal)
  for x in f['alignments']:assert apply_script(normal,x)==literal and apply_script(literal,inverse(x))==normal
  inventory.append(dict(id=ident,normal=normal,literal=literal,intent=intent,forward=f,correction=r))
 primary=[x for x in inventory if x['id'] in ('K1','K2')]
 extraction=[dict(source=c['source'],target=c['target'],word=x['id'],source_word_index=None if c['source_index'] is None else c['source_index']+1,target_word_index=None if c['target_index'] is None else c['target_index']+1) for x in inventory[:3] for c in x['correction']['alignments'][0] if c['op']!='M']
 texts=full_sources(controls);pairs=[(t['id'],t['normalized_comparison'],t['normalized_literal']) for t in texts[:2]];functions={}
 for direction in ('forward','correction'):
  selected=pairs if direction=='forward' else [(i,b,a) for i,a,b in pairs]
  for injective in (False,True):functions[direction+('_bijection' if injective else '_function')]=infer_function(selected,injective=injective)
 changed=[('Q','L'),('U','O')];affine={name:dict(invertible=affine_candidates(changed,abc),unrestricted_diagnostic=affine_candidates(changed,abc,False)) for name,abc in ALPHABETS.items()}
 k=keyboard_coordinates();vectors=[dict(source=a,target=b,quarter_key_dx=k[b][0]-k[a][0],row_dy=k[b][1]-k[a][1]) for a,b in changed]
 inv=[]
 for t in primary:
  a,b=t['normal'],t['literal'];inv.append(dict(word=t['id'],transposition_possible=collections.Counter(a)==collections.Counter(b),copy_delete_can_introduce_all_target_symbols=set(b)<=set(a),new_target_symbols=sorted(set(b)-set(a)),vowel_only_possible=all(x==y or x in 'AEIOU' for x,y in zip(a,b))))
 phase_records=[]
 for name,abc in ALPHABETS.items():
  for mode,key in masks(abc).items():
   for phase in range(len(key)):
    checks=[]
    for t in texts[:2]:
     got=translate(t['normalized_literal'],key,abc,phase);want=t['normalized_comparison'];bad=[i for i,(x,y) in enumerate(zip(got,want)) if x!=y]
     checks.append(dict(source=t['id'],length=len(got),exact_match=not bad,mismatch_count=len(bad),first_mismatch_zero_based=bad[0] if bad else None,output=got))
    phase_records.append(dict(alphabet=name,role=mode,period=len(key),phase=phase,key_values=key,source_checks=checks))
 feasible=dict(trigger_free_forward=functions['forward_function']['compatible'],trigger_free_correction=functions['correction_function']['compatible'],invertible_affine_any=any(x['invertible'] for x in affine.values()),keyboard_single_translation=len({(x['quarter_key_dx'],x['row_dy']) for x in vectors})==1,transposition=all(x['transposition_possible'] for x in inv),copy_delete=all(x['copy_delete_can_introduce_all_target_symbols'] for x in inv),vowel_only=all(x['vowel_only_possible'] for x in inv),positional_masks=any(all(y['exact_match'] for y in x['source_checks']) for x in phase_records))
 return dict(source_rule_feasibility=feasible,inventory=inventory,ordered_correction_extraction=extraction,full_source_texts=texts,trigger_free_function_constraints=functions,affine_changed_site_oracle=affine,invertible_affine_descriptions=624,noninvertible_included_diagnostic_descriptions=1352,keyboard_displacements=vectors,keyboard_single_translation_possible=len({(x['quarter_key_dx'],x['row_dy']) for x in vectors})==1,overlapping_symbol_invariants=inv,source_mask_phase_records=phase_records,source_mask_descriptions=len(phase_records),full_source_mask_tests=2*len(phase_records),supported_source_rule_survivors=sum(bool(x) for x in feasible.values()),K4_trials=0,canonical_ciphertext_changed=False,not_claimed=['all contextual spelling systems excluded','intent established for DESPARATLY','correction extraction locates its own trigger sites','a key/cipher selected from the correction pairs'])
