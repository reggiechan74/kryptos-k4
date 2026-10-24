"""Exact non-veto trigram scoring; not an English decision rule or hidden-message decoder."""
import collections,datetime,hashlib,json,random,resource,time,zipfile
from fractions import Fraction
from pathlib import Path
import prose_cover as p
ROOT=Path(__file__).resolve().parents[1];AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def table_from_counts(counts,q):
 totals=[sum(counts[i*q:(i+1)*q]) for i in range(q*q)];return dict(q=q,counts=counts,numerators=[x+1 for x in counts],denominators=[v+q for v in totals])
def train(path):
 names=p.cp.validate_brown(path);counts=[0]*(26**3);reference=collections.Counter();letters=0;lines=0
 with zipfile.ZipFile(path) as z:
  for name in names:
   for line in z.read(name).decode('ascii').splitlines():
    text=''.join(ch for token in line.split() for ch in token.rsplit('/',1)[0].upper() if ch in AZ);v=[ord(x)-65 for x in text];lines+=1;letters+=len(text)
    for i in range(2,len(v)):counts[v[i-2]*676+v[i-1]*26+v[i]]+=1
    reference.update(text[i-2:i+1] for i in range(2,len(text)))
 for a in range(26):
  for b in range(26):
   for c in range(26):assert counts[a*676+b*26+c]==reference[AZ[a]+AZ[b]+AZ[c]]
 return dict(kind='Aggregated Brown sentence-internal unspaced A-Z trigrams; no corpus sentences',brown_zip_sha256=p.cp.BROWN_SHA,sentence_lines=lines,normalized_letters=letters,counts=counts,q=26,normalization='Every token spelling before finalPOS slash; uppercase retainA-Z, no cross-line joining',smoothing='Add one per26letter continuation')
def indices(n,known):return [i for i in range(2,n) if not any(j in known for j in (i-2,i-1,i))]
def score(text,terms,table,alphabet=AZ):
 q=table['q'];v=[alphabet.index(ch) for ch in text];N=D=1;nums=table['numerators'];dens=table['denominators']
 for i in terms:context=v[i-2]*q+v[i-1];N*=nums[context*q+v[i]];D*=dens[context]
 return N,D
def reference_score(text,terms,table,alphabet=AZ):
 q=len(alphabet);result=Fraction(1)
 for i in terms:
  a,b,c=(alphabet.index(x) for x in text[i-2:i+1]);row=table['counts'][(a*q+b)*q:(a*q+b+1)*q];result*=Fraction(row[c]+1,sum(row)+q)
 return result

def controls():
 count=0;table=table_from_counts([1,2,0,4,3,0,2,1],2)
 for n in range(7):
  import itertools
  for text in map(''.join,itertools.product('AB',repeat=n)):
   for known in ({},{i for i in range(n) if i%2==0}):
    terms=indices(n,known);N,D=score(text,terms,table,'AB');assert Fraction(N,D)==reference_score(text,terms,table,'AB');count+=1
 return dict(complete_small_string_mask_fraction_checks=count,all_continuations_positive=True)

def fraction_record(N,D):
 f=Fraction(N,D);return dict(numerator=str(f.numerator),denominator=str(f.denominator))
def search(cipher,known,table,truth=None,audit=False):
 begin=utc();clock=time.monotonic();terms=indices(97,known);assert len(terms)==67;bestN,bestD=0,1;maxima=[];rows=[];allcount=0;better=equal=0;truth_found=False
 if truth:truthN,truthD=score(truth['truth'],terms,table)
 old=json.loads((ROOT/'results/PROSE-COVER-035-INDEPENDENT-AUDIT.json').read_text()) if audit else None
 for name,alphabet in p.ALPHABETS.items():
  for eq in p.ak.COEFFICIENTS:
   alltexts=list(p.plaintexts(cipher,known,alphabet,eq,27));assert len(alltexts)==17576;count=0
   if audit:
    digest=hashlib.sha256(('\n'.join(sorted(alltexts))+'\n').encode()).hexdigest();prior=next(x for x in old['model_rows'] if x['alphabet']==name and x['equation']==eq);assert digest==prior['sorted_plaintexts_sha256']
   for plain in alltexts:
    assert all(plain[i]==x for i,x in known.items());N,D=score(plain,terms,table);comparison=N*bestD-bestN*D
    if comparison>=0:
     key=p.primer_for(cipher,plain,alphabet,eq,27);assert p.ak.transform(plain,key,alphabet,eq,'plaintext')==cipher
     record=dict(alphabet=name,equation=eq,plaintext=plain,primer=key,plaintext_sha256=hashlib.sha256(plain.encode()).hexdigest(),full97_ciphertext_regeneration=True)
     if comparison>0:bestN,bestD=N,D;maxima=[record]
     else:maxima.append(record)
    if truth:
     comparison=N*truthD-truthN*D;better+=comparison>0;equal+=comparison==0
     if plain==truth['truth'] and name==truth['alphabet'] and eq==truth['equation']:assert p.primer_for(cipher,plain,alphabet,eq,27)==truth['primer'];truth_found=True
    count+=1
    if count%512==0 and time.monotonic()-clock>120:raise RuntimeError('Selector time budget unresolved')
   rows.append(dict(alphabet=name,equation=eq,descriptions=count,original035_complete_plaintext_hash_equal=True if audit else None));allcount+=count
 result=dict(started_at_utc=begin,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,complete=True,model_key_descriptions=allcount,score_terms=len(terms),max_score=fraction_record(bestN,bestD),maxima=maxima,model_rows=rows,all_strings_have_positive_support=True,not_a_language_acceptance_or_decryption=True)
 if truth:result['plant']=dict(true_pair_enumerated=truth_found,descriptions_strictly_above_truth=better,descriptions_tied_with_truth=equal,truth_among_global_maxima=better==0,truth_score=fraction_record(truthN,truthD));assert truth_found
 return result

def run(brown,output):
 start=utc();clock=time.monotonic();checks=controls();data=train(brown);raw=json.dumps(data,sort_keys=True,separators=(',',':')).encode()+b'\n';tablepath=ROOT/'data/cover-trigrams-045.json'
 if tablepath.exists():assert tablepath.read_bytes()==raw
 else:tablepath.write_bytes(raw)
 table=table_from_counts(data['counts'],26);out=dict(id='COVER-LANGUAGE-045',started_at_utc=start,controls=checks,counts_sha256=hashlib.sha256(raw).hexdigest(),source_sha256={q:hashlib.sha256((ROOT/q).read_bytes()).hexdigest() for q in ('research/COVER-LANGUAGE-045-SPEC.md','experiments/cover_language_045.py','data/k4.json','data/controls.json','results/PROSE-COVER-035-ORIGINAL.json','results/PROSE-COVER-035-INDEPENDENT-AUDIT.json')},new_outer_cipher_domain=False,new_hidden_extraction_trials=0,stages={},complete=False)
 def save():Path(output).write_text(json.dumps(out,indent=2)+'\n')
 save();rng=random.Random(450024);calibration=[];controlsdata=json.loads((ROOT/'data/controls.json').read_text())
 for name in ('k1','k2_restored_s','k3'):
  text=''.join(x for x in controlsdata[name]['plaintext'] if x in AZ);terms=indices(len(text),set());N,D=score(text,terms,table);nulls=[]
  for i in range(31):
   chars=list(text);rng.shuffle(chars);a,b=score(''.join(chars),terms,table);nulls.append(dict(draw=i,score=fraction_record(a,b),at_least_as_large=a*D>=N*b))
  exceed=sum(x['at_least_as_large'] for x in nulls);assert Fraction(N,D)==reference_score(text,terms,table);calibration.append(dict(stream=name,length=len(text),score_terms=len(terms),score=fraction_record(N,D),positive_support=True,nulls=nulls,at_least_as_large=exceed,descriptive_competence_gate=exceed<=1))
 out['stages']['calibration']=calibration;out['calibration_gate_passed']=all(x['descriptive_competence_gate'] for x in calibration);save();prior=json.loads((ROOT/'results/PROSE-COVER-035-ORIGINAL.json').read_text());known={int(i)-1:v for i,v in prior['known_one_based'].items()};actual=search(prior['canonical_ciphertext'],known,table,audit=True);out['stages']['actual']=actual;save();print('actual',actual['model_key_descriptions'],'maxima',len(actual['maxima']),flush=True);actualscore=Fraction(int(actual['max_score']['numerator']),int(actual['max_score']['denominator']));nullrows=[]
 for row in prior['stages']['nulls']['records'][:7]:
  value=search(row['ciphertext'],known,table);f=value['max_score'];nullrows.append(dict(prior_draw=row['draw'],ciphertext=row['ciphertext'],search=value,whole_family_max_at_least_actual=Fraction(int(f['numerator']),int(f['denominator']))>=actualscore));print('null',len(nullrows),flush=True)
  if time.monotonic()-clock>600:raise RuntimeError('Batch time unresolved')
 out['stages']['nulls']=dict(reused_prior_inputs=True,not_pristine_holdout=True,records=nullrows,exceedances=sum(x['whole_family_max_at_least_actual'] for x in nullrows),resolution='1/8 descriptive conditional permutation count; no positive significance claim');save();plants=[]
 for oldplant in prior['stages']['plants']['records']:
  plantknown={i:oldplant['truth'][i] for i in known};value=search(oldplant['ciphertext'],plantknown,table,truth=oldplant);plants.append(dict(original_model=dict(alphabet=oldplant['alphabet'],equation=oldplant['equation']),search=value));print('plant',len(plants),value['plant'],flush=True)
  if time.monotonic()-clock>600:raise RuntimeError('Batch time unresolved')
 out['stages']['plants']=plants;out.update(complete=True,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,positive_K4_identification=False,puzzle_solved=False,Site_changed=False,pushed=False);assert out['peak_RSS_bytes']<512*1024**2;assert len(json.dumps(out).encode())<64*1024**2;save();print('complete',out['elapsed_seconds'],'null_exceedances',out['stages']['nulls']['exceedances'],flush=True)
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--brown-zip',required=True);a.add_argument('--output',required=True);args=a.parse_args();run(args.brown_zip,args.output)
