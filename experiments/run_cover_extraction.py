import datetime,hashlib,json,platform,random,resource,subprocess,sys,time
from pathlib import Path
import cover_extraction as c
import cover_extraction_reference as ref
ROOT=Path(__file__).resolve().parents[1];AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def encrypt(plain,key):return plain.translate(str.maketrans(AZ,AZ[key:]+AZ[:key]))
def infer_caesar(cipher,vocab,known):
 out=[]
 for key in range(26):
  plain=''.join(chr((ord(x)-65-key)%26+65) for x in cipher)
  if all(plain[i]==v for i,v in known.items()):
   for words in c.decode_cover(plain,vocab):out.append(dict(key=key,cover=plain,words=list(words)))
 return out

def run():
 start=utc();clock=time.monotonic();known=c.source_known(json.loads((ROOT/'data/k4.json').read_text()));models=c.models();records=[];plants=[];rng=random.Random(330024);checks=0
 for m in models:
  distribution=m.distributions();edges=c.word_lattice(m.vocab,97,known,c.fixed_spans(m));independent=c.lattice_counts(edges,97);assert independent==distribution['counts']
  for stratum in ('all','15'):
   words=m.sample(rng,None if stratum=='all' else 15)
   if words is None:continue
   cover=''.join(words);assert len(cover)==97
   for key in (0,7,19):
    cipher=encrypt(cover,key);found=infer_caesar(cipher,m.vocab,known);assert len(found)==1 and found[0]['key']==key and found[0]['cover']==cover
    assert encrypt(found[0]['cover'],found[0]['key'])==cipher
    outputs=[]
    for N,phase in [(1,0),(2,0),(2,1)]:
     for k in range(1,5):
      y=c.extract(words,k,N,phase);lane=c.Lane(m,k,N,phase,stratum);native=lane.count(y);reference=ref.count_message(m,y,k,N,phase,None if stratum=='all' else 15);assert native==reference and native>0;checks+=1;outputs.append(dict(k=k,N=N,phase=phase,text=y,compatible_covers=native))
    plants.append(dict(purpose='Synthetic public-Caesar control only, not actual K4',model=m.name,stratum=stratum,key_hidden_from_solver=key,cover=cover,words=words,ciphertext=cipher,recovered=found,outputs=outputs))
  initials=collections_for_initials(m.vocab);supports={str(k):''.join(sorted({w[k-1] for w in m.vocab if len(w)>=k})) for k in range(1,5)}
  records.append(dict(id=m.name,vocabulary=list(m.vocab),boundary_hypothesis='|'.join(m.a)+' / '+'|'.join(m.b),source_fixed_spans=c.fixed_spans(m),unknown_runs=list(m.runs),prefix_free=c.prefix_free(m.vocab),initial_aliases=initials,extraction_supports=supports,distribution=distribution,source_lattice=edges,known_output_kN1={str(k):[c.extract(m.a,k),c.extract(m.b,k)] for k in range(1,5)}))
 strict_edges=c.word_lattice(c.NATO,97,known);strict=c.lattice_counts(strict_edges,97)
 for r in records:
  if r['id'].startswith('A30'):
   sub=next(x for x in records if x['id']=='R26'+r['id'][3:]);r['distinct_initials_N1_bounds']=dict(lower=sub['distribution']['total'],upper=r['distribution']['total'],basis='R26 subcode gives distinct initial strings; added synonyms create cover aliases')
  else:r['distinct_initials_N1_exact']=r['distribution']['total']
 elapsed=time.monotonic()-clock;peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert elapsed<60 and peak<256*1024**2
 paths=['research/COVER-EXTRACTION-033-SPEC.md','experiments/cover_extraction.py','experiments/cover_extraction_reference.py','experiments/run_cover_extraction.py','data/k4.json'];return dict(id='COVER-EXTRACTION-033',kind='Conditional post-decryption source-grammar feasibility; no actual K4 decryption',started_at_utc=start,finished_at_utc=utc(),elapsed_seconds=elapsed,peak_rss_bytes=peak,python=platform.python_version(),implementation_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},models=records,strict_NATO_unanchored_counts=strict,strict_NATO_aligned_cases=[dict(tokens='ENE/BC',compatible_covers=0,reason='required custom tokens absent'),dict(tokens='EN/BC',compatible_covers=0,reason='required custom tokens absent')],synthetic_plants=plants,independent_real_size_fixed_message_checks=checks,actual_K4_cipher_trials=0,Site_changed=False,push_attempted=False)

def collections_for_initials(vocab):
 out={}
 for w in vocab:out.setdefault(w[0],[]).append(w)
 return {k:v for k,v in out.items() if len(v)>1}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['started_at_utc','finished_at_utc','elapsed_seconds','peak_rss_bytes','independent_real_size_fixed_message_checks']}));print(json.dumps({x['id']:x['distribution'] for x in r['models']}))
