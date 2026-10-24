"""Exact fixed-source candidate-first preflight; arbitrary derived keys are inadmissible."""
import collections,hashlib,itertools,json,random,resource,sys,time,zipfile
from datetime import datetime,timezone
from pathlib import Path
import cover_phrase,autokey_constraints as old
ROOT=Path(__file__).resolve().parents[1];ALPHABETS={'AZ':'ABCDEFGHIJKLMNOPQRSTUVWXYZ','KRYPTOS':'KRYPTOSABCDEFGHIJLMNQUVWXZ'};EQUATIONS={'plus':(1,1),'minus':(1,-1),'beaufort':(-1,1)}
def utc():return datetime.now(timezone.utc).isoformat()
class Budget:
 def __init__(self,seconds):self.start=time.monotonic();self.seconds=seconds
 def check(self):
  rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
  if time.monotonic()-self.start>self.seconds or rss>1024**3:raise RuntimeError('declared time/RSS budget unresolved')
def models(n=97,q=26):
 for a,alphabet in ALPHABETS.items() if q==26 else [('toy','ABC'[:q])]:
  for eq,(s,t) in EQUATIONS.items():
   for mode in ('periodic','plaintext','ciphertext','running'):
    for L in ([n] if mode=='running' else range(1,33) if n==97 else range(1,min(2,n)+1)):
     yield dict(alphabet_name=a,alphabet=alphabet,equation=eq,s=s,t=t,mode=mode,L=L)
def inverse(C,key,m):
 a=m['alphabet'];q=len(a);c=[a.index(x) for x in C];k=[a.index(x) for x in key];P=[]
 for i,x in enumerate(c):
  v=k[i%len(k)] if m['mode']=='periodic' else k[i] if i<len(k) else P[i-len(k)] if m['mode']=='plaintext' else c[i-len(k)]
  P.append(m['s']*(x-m['t']*v)%q)
 return ''.join(a[x] for x in P)
def forward(P,key,m):
 a=m['alphabet'];q=len(a);p=[a.index(x) for x in P];k=[a.index(x) for x in key];C=[]
 for i,x in enumerate(p):
  v=k[i%len(k)] if m['mode']=='periodic' else k[i] if i<len(k) else p[i-len(k)] if m['mode']=='plaintext' else C[i-len(k)]
  C.append((m['s']*x+m['t']*v)%q)
 return ''.join(a[x] for x in C)
def constraints(C,known,m):
 a=m['alphabet'];q=len(a);c=[a.index(x) for x in C];s,t,L=m['s'],m['t'],m['L'];mask={};owners={}
 def put(j,v,i):
  if j in mask and mask[j]!=v:return dict(known_positions_one_based=[owners[j]+1,i+1],seed_index_zero_based=j,required_values=[mask[j],v])
  mask[j]=v;owners[j]=i
 if m['mode']=='plaintext':
  coeff=[1]*len(C);bias=[0]*len(C)
  for i in range(L,len(C)):coeff[i]=-s*t*coeff[i-L];bias[i]=(s*c[i]-s*t*bias[i-L])%q
  for i,p in sorted(known.items()):
   root=coeff[i]*(a.index(p)-bias[i])%q;value=t*(c[i%L]-s*root)%q;conflict=put(i%L,value,i)
   if conflict:return {},conflict
 else:
  for i,p in sorted(known.items()):
   if m['mode']=='ciphertext' and i>=L:
    pred=s*(c[i]-t*c[i-L])%q
    if pred!=a.index(p):return {},dict(known_position_one_based=i+1,feedback_position_one_based=i-L+1,predicted=a[pred],required=p)
   else:
    j=i%L if m['mode']=='periodic' else i;conflict=put(j,t*(c[i]-s*a.index(p))%q,i)
    if conflict:return {},conflict
 return mask,None
def anchor(mask,alphabet):
 runs=[]
 for j in sorted(mask):
  if runs and j==runs[-1][-1]+1:runs[-1].append(j)
  else:runs.append([j])
 if not runs:return 0,''
 run=min(runs,key=lambda r:(-len(r),r[0]));return run[0],''.join(alphabet[mask[i]] for i in run)
def occurrences(text,pattern):
 if not pattern:yield from range(len(text)+1);return
 i=text.find(pattern)
 while i>=0:yield i;i=text.find(pattern,i+1)
def compatible_source(C,known,m,documents,budget=None):
 mask,conflict=constraints(C,known,m);row=dict(model={k:v for k,v in m.items() if k!='alphabet'},structural_conflict=conflict,free_seed_symbols=m['L']-len(mask) if not conflict else None,fixed_seed_mask=[[i,m['alphabet'][v]] for i,v in sorted(mask.items())]);records={}
 if conflict:row.update(source_windows_examined=0,source_occurrences=0,distinct_source_keys=0);return row,records
 off,pat=anchor(mask,m['alphabet']);row['lossless_anchor']=dict(seed_offset=off,text=pat,length=len(pat));examined=0;hits=0
 for name,text in documents:
  if budget:budget.check()
  for pos in occurrences(text,pat):
   start=pos-off
   if start<0 or start+m['L']>len(text):continue
   examined+=1
   if budget and examined%512==0:budget.check()
   if any(text[start+j]!=m['alphabet'][v] for j,v in mask.items()):continue
   seed=text[start:start+m['L']];P=inverse(C,seed,m);assert all(P[i]==v for i,v in known.items());assert forward(P,seed,m)==C
   if seed not in records:records[seed]=dict(key=seed,plaintext=P,source_positions=[])
   records[seed]['source_positions'].append([name,start]);hits+=1
 row.update(source_windows_examined=examined,source_occurrences=hits,distinct_source_keys=len(records));return row,records
def search(C,known,documents,budget,full=False):
 rows=[];plain=set();pairs=0;source=0;cases=[]
 for m in models(len(C)):
  budget.check();row,keys=compatible_source(C,known,m,documents,budget);rows.append(row);pairs+=len(keys);source+=row['source_occurrences']
  for v in keys.values():plain.add(v['plaintext']);cases.append(dict(model=row['model'],**v))
 return dict(complete=True,model_descriptions=len(rows),structurally_compatible_models=sum(x['structural_conflict'] is None for x in rows),distinct_compatible_full_plaintexts=len(plain),model_key_alias_pairs=pairs,source_occurrence_aliases=source,rows=rows if full else None,accepted_cases=cases if full else None)
def source_documents(path):
 names=cover_phrase.validate_brown(path);out=[];digest=hashlib.sha256()
 with zipfile.ZipFile(path) as z:
  for name in names:
   text=''.join(ch for token in z.read(name).decode('ascii').split() for ch in token.rsplit('/',1)[0].upper() if 'A'<=ch<='Z');out.append((name,text));digest.update(name.encode()+b'\0'+text.encode()+b'\n')
 return out,dict(zip_sha256=cover_phrase.BROWN_SHA,documents=len(out),normalized_letters=sum(len(t) for _,t in out),ordered_document_stream_sha256=digest.hexdigest(),already_used_not_pristine_holdout=True)
def candidate_accept(C,P,m,documents):
 if len(P)!=len(C):return None
 a=m['alphabet'];q=len(a);stream=[m['t']*(a.index(c)-m['s']*a.index(p))%q for c,p in zip(C,P)];L=m['L'];seed=''.join(a[v] for v in stream[:L])
 if m['mode']=='periodic':valid=all(v==stream[i%L] for i,v in enumerate(stream))
 elif m['mode']=='plaintext':valid=all(stream[i]==a.index(P[i-L]) for i in range(L,len(P)))
 elif m['mode']=='ciphertext':valid=all(stream[i]==a.index(C[i-L]) for i in range(L,len(P)))
 else:valid=True
 if not valid or not any(seed in text for _,text in documents):return None
 assert inverse(C,seed,m)==P and forward(P,seed,m)==C;return seed
def controls():
 comparisons=0;relations=0
 for q,n,text in [(2,4,'AABABBBA'),(3,3,'ABCABBCACBA')]:
  alpha='ABC'[:q];docs=[('tiny',text)]
  for C in map(''.join,itertools.product(alpha,repeat=n)):
   for known in ({},{0:alpha[0]},{n-1:alpha[1]},{0:alpha[0],n-1:alpha[1]}):
    for m in models(n,q):
     row,got=compatible_source(C,known,m,docs);truth={}
     for key in {text[i:i+m['L']] for i in range(len(text)-m['L']+1)}:
      # Independent old sequential cipher implementation and direct letter tests.
      if m['mode']=='periodic':P=''.join(alpha[m['s']*(alpha.index(c)-m['t']*alpha.index(key[i%len(key)]))%q] for i,c in enumerate(C))
      elif m['mode']=='running':P=''.join(alpha[m['s']*(alpha.index(c)-m['t']*alpha.index(k))%q] for c,k in zip(C,key))
      else:P=old.transform(C,key,alpha,m['equation'],m['mode'],decrypt=True)
      if all(P[i]==v for i,v in known.items()):truth[key]=P
     assert {key:v['plaintext'] for key,v in got.items()}==truth;comparisons+=1;relations+=len(truth)
 return dict(complete_tiny_source_key_plaintext_relations=comparisons,complete_admitted_pairs=relations)
def run(path,output):
 start=utc();ingest=Budget(180);documents,source=source_documents(path);checks=controls();ingest.check();data=json.loads((ROOT/'data/k4.json').read_text());C=data['ciphertext'];known={c['start']-1+i:x for c in data['cribs'] for i,x in enumerate(c['plaintext'])};rng=random.Random(48000);P=[rng.choice(ALPHABETS['AZ']) for _ in range(97)]
 for i,v in known.items():P[i]=v
 P=''.join(P);plants=[]
 for name,a in ALPHABETS.items():
  for eq,(s,t) in EQUATIONS.items():
   for mode in ('periodic','plaintext','ciphertext','running'):
    m=dict(alphabet_name=name,alphabet=a,equation=eq,s=s,t=t,mode=mode,L=97 if mode=='running' else 5);key=documents[0][1][:m['L']];cipher=forward(P,key,m);assert candidate_accept(cipher,P,m,documents)==key
    if mode in ('plaintext','ciphertext'):assert old.transform(P,key,a,eq,mode)==cipher
    mask,conflict=constraints(cipher,known,m);assert conflict is None and all(key[i]==a[v] for i,v in mask.items());plants.append(dict(model={k:v for k,v in m.items() if k!='alphabet'},true_key_recovered=True,all97_ciphertext_regenerated=True,unanchored73_truth_equal=True))
 ingest.check();budget=Budget(180);actual=search(C,known,documents,budget,True);nulls=[];unanchored=[i for i in range(97) if i not in known];rng=random.Random(48001)
 for j in range(31):
  chars=[C[i] for i in unanchored];rng.shuffle(chars);v=list(C)
  for i,x in zip(unanchored,chars):v[i]=x
  text=''.join(v);res=search(text,known,documents,budget);res.pop('rows');res.pop('accepted_cases');nulls.append(dict(index=j,cipher_sha256=hashlib.sha256(text.encode()).hexdigest(),**res))
 out=dict(id='CANDIDATE-FIRST-048',started_at_utc=start,finished_at_utc=utc(),source=source,controls=checks,plants=plants,actual=actual,nulls=nulls,primary_statistic='distinct compatible full97letter plaintexts',null_count=31,seed=48001,candidate_bank_generated=0,candidate_bank_status='omitted because exact source-key compatible plaintext set is empty' if not actual['distinct_compatible_full_plaintexts'] else 'pending blinded clause-bank authorship; preflight already fixes cipher coverage',null_limitations=['Conditional73-position permutation, not universal p-value.','Periodic/running source constraints use only anchored cipher cells and therefore can be invariant under these nulls.','Brown already inspected and not creator-selected.'],unrestricted_candidate_first_exhausted=False,canonical_changed=False,pushed=False,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['research/CANDIDATE-FIRST-048-SPEC.md','experiments/candidate_first_048.py','data/k4.json']})
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(id=out['id'],models=actual['model_descriptions'],structural_survivors=actual['structurally_compatible_models'],distinct_plaintexts=actual['distinct_compatible_full_plaintexts'],null_counts=[r['distinct_compatible_full_plaintexts'] for r in nulls],tiny_relations=checks['complete_tiny_source_key_plaintext_relations'],plants=len(plants),candidate_bank_generated=0)))
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--brown',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();run(args.brown,args.output)
