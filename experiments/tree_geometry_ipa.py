"""Frozen item6 mechanisms. No historical-use or security claim."""
import hashlib,itertools,json,time,resource,sys
from pathlib import Path
from conditional_face_lamp import ALPHABETS,WINDOWS,literal_plant
from geometric_pilots import frozen_codes,MASK,rotl35
ROOT=Path(__file__).resolve().parents[1];AZ=ALPHABETS['AZ'];CODES=frozen_codes()
GEO=''.join(sorted(AZ,key=lambda c:CODES[c]))


def pronunciation_keys():
 d=json.loads((ROOT/'data/ipa-cambridge-us-v1.json').read_text())['entries']
 norm=lambda s:''.join(c for c in s if c not in '/ˈˌ. ')
 return {'east-northeast':norm(d['east']+d['northeast']),'berlin-clock':norm(d['berlin']+d['clock'])}
IPA=pronunciation_keys();KEYS={k:tuple(s.encode('utf-8')) for k,s in IPA.items()}


def domain():
 out=[]
 for order,seed,name in itertools.product(('AZ','geometry'),range(26),ALPHABETS):out.append(dict(role='T',order=order,seed=seed,alphabet=name))
 for seed,source,name,eq in itertools.product(AZ,('P','C'),ALPHABETS,('plus','beaufort')):out.append(dict(role='G',seed=seed,source=source,alphabet=name,equation=eq))
 for key in KEYS:
  for phase,name,eq in itertools.product(range(len(KEYS[key])),ALPHABETS,('plus','beaufort')):out.append(dict(role='I',key=key,phase=phase,alphabet=name,equation=eq))
 return out
MODELS=domain()


def budget(start,seconds):
 if time.monotonic()-start>seconds:raise TimeoutError('frozen budget exhausted; unresolved')
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
 if rss>512*1024**2:raise MemoryError('512 MiB peak RSS cap; unresolved')


class Splay:
 def __init__(self,labels):
  self.labels=labels;self.lookup={c:i for i,c in enumerate(labels)};self.left=[-1]*26;self.right=[-1]*26;self.parent=[-1]*26
  def build(lo,hi,parent=-1):
   if lo>=hi:return -1
   mid=(lo+hi)//2;self.parent[mid]=parent;self.left[mid]=build(lo,mid,mid);self.right[mid]=build(mid+1,hi,mid);return mid
  self.root=build(0,26)
 def preorder(self):
  out=[];stack=[self.root]
  while stack:
   x=stack.pop();out.append(x)
   if self.right[x]!=-1:stack.append(self.right[x])
   if self.left[x]!=-1:stack.append(self.left[x])
  return out
 def rotate(self,x):
  p=self.parent[x];g=self.parent[p]
  if self.left[p]==x:
   b=self.right[x];self.left[p]=b;self.right[x]=p
  else:
   b=self.left[x];self.right[p]=b;self.left[x]=p
  if b!=-1:self.parent[b]=p
  self.parent[p]=x;self.parent[x]=g
  if g==-1:self.root=x
  elif self.left[g]==p:self.left[g]=x
  else:self.right[g]=x
 def access(self,x):
  while self.parent[x]!=-1:
   p=self.parent[x];g=self.parent[p]
   if g!=-1:self.rotate(p if (self.left[g]==p)==(self.left[p]==x) else x)
   self.rotate(x)
 def signature(self):return (self.root,tuple(self.left),tuple(self.right))


def crypt(text,m,decrypt=False,wrong_timing=False):
 if any(c not in AZ for c in text):raise ValueError('uppercase A-Z framing required')
 a=ALPHABETS[m['alphabet']];out=[]
 if m['role']=='T':
  labels=AZ if m['order']=='AZ' else GEO;s=m['seed'];labels=labels[s:]+labels[:s];tree=Splay(labels)
  for c in text:
   slots=tree.preorder();x=slots[a.index(c)] if decrypt else tree.lookup[c]
   if wrong_timing:tree.access(x);slots=tree.preorder()
   out.append(labels[x] if decrypt else a[slots.index(x)])
   if not wrong_timing:tree.access(x)
  return ''.join(out)
 state=CODES[m['seed']] if m['role']=='G' else None
 for i,c in enumerate(text):
  key=state%26 if state is not None else KEYS[m['key']][(m['phase']+i)%len(KEYS[m['key']])]%26
  v=a.index(c);v=((v-key if decrypt else v+key) if m['equation']=='plus' else key-v)%26
  value=a[v];out.append(value)
  if state is not None:
   p=value if decrypt else c;ct=c if decrypt else value;source=p if m['source']=='P' else ct
   state=(rotl35(state,1)+(state^CODES[source]))&MASK
 return ''.join(out)


def select(cipher,reference=False):
 if reference:
  from tree_geometry_ipa_reference import crypt as decode
 else:decode=crypt
 outputs={};rows=[];first=[]
 for i,m in enumerate(MODELS):
  plain=decode(cipher,m,True);digest=hashlib.sha256(plain.encode()).hexdigest();outputs.setdefault(digest,[]).append(i)
  passed=plain[21:34]==WINDOWS[0][1];all_pass=passed and plain[63:74]==WINDOWS[1][1]
  row=dict(model_index=i,model=m,plaintext_sha256=digest,first_pass=passed,all_pass=all_pass)
  if passed:
   assert decode(plain,m)==cipher
   row.update(plaintext=plain,predicted_berlin=plain[63:74],full_reencryption=True);first.append(row)
  rows.append(row)
 return dict(raw_descriptions=len(MODELS),role_counts={r:sum(m['role']==r for m in MODELS) for r in ('T','G','I')},distinct_full_outputs=len(outputs),output_aliases=[v for v in outputs.values() if len(v)>1],first_survivors=first,all_survivors=[r for r in first if r['all_pass']],records=rows)


def controls():
 from tree_geometry_ipa_reference import crypt as ref,utf8
 start=time.monotonic();messages=('',AZ,'THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG','XYZAB');checks=0
 for m in MODELS:
  for plain in messages:
   cipher=crypt(plain,m);assert crypt(cipher,m,True)==plain;assert ref(plain,m)==cipher;assert ref(cipher,m,True)==plain;checks+=1
  budget(start,180)
 assert all(utf8(s)==list(KEYS[k]) for k,s in IPA.items())
 topology=[];bijections=0;timing=0
 for m in (m for m in MODELS if m['role']=='T'):
  labels=AZ if m['order']=='AZ' else GEO;s=m['seed'];tree=Splay(labels[s:]+labels[:s]);initial=tree.signature()
  for c in 'QAZWSXEDC':
   slots=tree.preorder();assert len(set(slots))==26 and set(tree.labels[x] for x in slots)==set(AZ);bijections+=26
   tree.access(tree.lookup[c])
  assert tree.signature()!=initial;topology.append(m)
  timing+=crypt('THEQUICKBROWNFOX',m)!=crypt('THEQUICKBROWNFOX',m,wrong_timing=True)
 assert timing==104
 plants=[];plain=literal_plant()
 for role in ('T','G','I'):
  indices=[i for i,m in enumerate(MODELS) if m['role']==role]
  for j in range(8):
   idx=indices[j*(len(indices)-1)//7];m=MODELS[idx];cipher=crypt(plain,m);native=select(cipher);other=select(cipher,True)
   assert native==other
   assert any(r['model_index']==idx and r['plaintext']==plain for r in native['all_survivors'])
   plants.append(dict(planted_index=idx,planted_model=m,truth_retained=True,all_survivors=native['all_survivors'],distinct_plaintexts=len({r['plaintext_sha256'] for r in native['all_survivors']}),independent_complete_set_equal=True))
   budget(start,180)
 # Same modulo26 key does not determine next key: a precise boundary of old affine proofs.
 witness=None
 for letter in AZ:
  for s in range(26):
   x=(rotl35(s,1)+(s^CODES[letter]))&MASK;y=(rotl35(s+26,1)+((s+26)^CODES[letter]))&MASK
   if x%26!=y%26:witness=dict(letter=letter,states=[s,s+26],initial_key_residue=s,next_key_residues=[x%26,y%26]);break
  if witness:break
 assert witness
 return dict(status='passed',fixed_model_reference_roundtrips=checks,tree_letter_bijection_checks=bijections,tree_topology_changes=len(topology),tree_timing_mutations_detected=timing,ipa_byte_lengths={k:len(v) for k,v in KEYS.items()},geometry_no_mod26_first_order_reduction_witness=witness,plants=plants,elapsed_seconds=time.monotonic()-start)
