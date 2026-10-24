"""Length-free selector support and exact key/cover non-identifiability; no new cipher search."""
import collections,datetime,hashlib,itertools,json,resource,time
from pathlib import Path
import prose_cover as p
ROOT=Path(__file__).resolve().parents[1]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def lanes():return [(k,N,r) for k in range(1,5) for N in range(1,5) for r in range(N)]
def oracle(total,known,vocab,k,N,phase):
 counts=collections.Counter();outputs=collections.Counter()
 def visit(words,text):
  if len(text)==total:
   picked=[w for j,w in enumerate(words) if j%N==phase]
   if any(len(w)<k for w in picked):return
   counts[len(words)]+=1;outputs[len(picked)]+=1;return
  for w in vocab:
   nxt=text+w
   if len(nxt)<=total and all(nxt[i]==c for i,c in known.items() if i<len(nxt)):visit(words+[w],nxt)
 visit([],"")
 return dict(total=sum(counts.values()),coverwords=dict(sorted(counts.items())),output_lengths=dict(sorted(outputs.items())))
def controls():
 cases=0;plants=0;vocab={'A','B','AA','AB','BA','BBB'}
 for n in range(8):
  for kind in range(3):
   known={} if kind==0 else {i:'AB'[i%2] for i in range(n) if i%2==kind-1};h=p.mask_hist(n,known,vocab)
   for k,N,r in lanes():
    got=p.distribution(h,k,N,r);expected=oracle(n,known,vocab,k,N,r);assert got==expected;(cases:=cases+1)
 for k,N,r in lanes():
  words=['ABAB']*(r+N+1);text=''.join(words);known=dict(enumerate(text));h=p.mask_hist(len(text),known,{'ABAB'});got=p.distribution(h,k,N,r);assert got['total']==1;plants+=1
 # Independent full key enumeration versus every plaintext satisfying its crib.
 keycases=0
 for q in (2,3):
  for n in range(1,5):
   cipher=tuple(i%q for i in range(n));known={0:0,n-1:(n-1)%q};expected={x for x in itertools.product(range(q),repeat=n) if all(x[i]==v for i,v in known.items())}
   actual=set()
   for key in itertools.product(range(q),repeat=n):
    plain=tuple((c-z)%q for c,z in zip(cipher,key))
    if all(plain[i]==v for i,v in known.items()):actual.add(plain)
   assert actual==expected and len(actual)==q**(n-len(known));keycases+=1
 return dict(complete_tiny_selector_distribution_comparisons=cases,selector_plants=plants,complete_full_key_relations=keycases)
def run(brown):
 start=utc();clock=time.monotonic();ctrl=controls();data=json.loads((ROOT/'data/k4.json').read_text());known={c['start']-1+j:v for c in data['cribs'] for j,v in enumerate(c['plaintext'])};vocab,_=p.vocabularies(brown);old=json.loads((ROOT/'results/PROSE-COVER-035-ORIGINAL.json').read_text());rows={};comparisons=0
 for name,v in vocab.items():
  h=p.mask_hist(97,known,v);rows[name]=dict(vocabulary=p.vocab_receipt(v),selectors={})
  for k,N,r in lanes():
   label=f'k{k}:N{N}:p{r}';value=p.distribution(h,k,N,r);rows[name]['selectors'][label]=value
   if N<=2:
    expected=old['stages']['mask_constraints']['models'][name]['selectors'][label];assert json.loads(json.dumps(value))==expected;comparisons+=1
   if time.monotonic()-clock>120 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>512*1024**2:raise RuntimeError('resource gate unresolved')
 out=dict(id='COVER-SELECTOR-038',started_at_utc=start,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,controls=ctrl,models=rows,selector_descriptions=120,previous_distribution_equalities=comparisons,added_N3_N4_descriptions=84,source_hashes={x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in ('research/COVER-SELECTOR-038-SPEC.md','experiments/cover_selector_038.py','data/k4.json','results/PROSE-COVER-035-ORIGINAL.json')},key_freedom=dict(alphabet_size=26,unfixed_positions=73,compatible_full_length_key_plaintext_pairs=26**73,claim='Every 97-letter plaintext satisfying24cribletters determines exactly one97-letter additive key for fixed ciphertext; not a candidate or evidence for this unconstrained model'),new_K4_outer_cipher_trials=0,puzzle_solved=False,Site_changed=False,pushed=False)
 return out
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--brown-zip',required=True);a.add_argument('--output',required=True);args=a.parse_args();out=run(args.brown_zip);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('started_at_utc','finished_at_utc','controls','selector_descriptions','previous_distribution_equalities')}))
