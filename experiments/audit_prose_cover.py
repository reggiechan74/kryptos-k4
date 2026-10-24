"""Post-outcome independent backward-chain/full actual-domain replay."""
import argparse,datetime,hashlib,itertools,json,time
from pathlib import Path
import prose_cover as p

def reference_plaintexts(cipher,known,alphabet,equation,lag):
 sigma,tau=p.ak.COEFFICIENTS[equation];m=len(alphabet);c=[alphabet.index(ch) for ch in cipher];fixed={}
 for i,ch in known.items():
  value=alphabet.index(ch)
  while i>=lag:value=tau*(c[i]-sigma*value)%m;i-=lag
  if i in fixed and fixed[i]!=value:return
  fixed[i]=value
 free=[i for i in range(lag) if i not in fixed]
 for values in itertools.product(range(m),repeat=len(free)):
  starts=fixed.copy();starts.update(zip(free,values));out=[starts[i] for i in range(lag)]
  for i in range(lag,len(cipher)):out.append(sigma*(c[i]-tau*out[i-lag])%m)
  yield ''.join(alphabet[x] for x in out)

def wordbreak(text,vocab,lengths=None):
 lengths=sorted({len(w) for w in vocab}) if lengths is None else lengths;reachable={0}
 for i in range(len(text)):
  if i not in reachable:continue
  for n in lengths:
   if i+n<=len(text) and text[i:i+n] in vocab:reachable.add(i+n)
 return len(text) in reachable,max(reachable)

def run(source,brown,output):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();r=json.loads(Path(source).read_text());known={int(i)-1:v for i,v in r['known_one_based'].items()};vocab,_=p.vocabularies(brown);rows=[];lengths=sorted({len(w) for w in vocab['O']})
 for name,alphabet in p.ALPHABETS.items():
  for equation in p.ak.COEFFICIENTS:
   reference=sorted(reference_plaintexts(r['canonical_ciphertext'],known,alphabet,equation,27));native=sorted(p.plaintexts(r['canonical_ciphertext'],known,alphabet,equation,27));assert reference==native and len(reference)==17576
   passes=[plain for plain in reference if wordbreak(plain,vocab['O'],lengths)[0]];assert not passes
   assert time.monotonic()-t<120,'independent replay resource cap'
   rows.append(dict(alphabet=name,equation=equation,complete_plaintext_set_equal=True,count=len(reference),sorted_plaintexts_sha256=hashlib.sha256(('\n'.join(reference)+'\n').encode()).hexdigest(),independent_wordbreak_survivors=len(passes)))
 calibration={}
 controls=json.loads((Path(__file__).resolve().parents[1]/'data/controls.json').read_text())
 for key in ('k1','k2_restored_s','k3'):
  text=''.join(x for x in controls[key]['plaintext'] if 'A'<=x<='Z');calibration[key]={name:dict(accepted=wordbreak(text,v)[0],furthest_reachable_prefix=wordbreak(text,v)[1],full_length=len(text)) for name,v in vocab.items()}
 out=dict(kind='Independent post-outcome complete actual-domain set and lexical-negative replay',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,source_receipt_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),model_rows=rows,model_key_descriptions=sum(x['count'] for x in rows),calibration=calibration,complete=True,new_search_domain=False)
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--brown-zip',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();run(a.source,a.brown_zip,a.output)
