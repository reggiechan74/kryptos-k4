"""Run preregistered PROSE-COVER-035; actual and synthetic stages are separate."""
import argparse,datetime,gzip,hashlib,json,random,re,time
from pathlib import Path
import prose_cover as p
import cover_phrase as cp
ROOT=Path(__file__).resolve().parents[1]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(path,out):Path(path).write_text(json.dumps(out,indent=2)+'\n')
def run(path,output):
 start=utc();clock=time.monotonic();data=json.loads((ROOT/'data/k4.json').read_text());known={x['start']-1+j:v for x in data['cribs'] for j,v in enumerate(x['plaintext'])};out=dict(id='PROSE-COVER-035',started_at_utc=start,canonical_ciphertext=data['ciphertext'],known_one_based={i+1:v for i,v in known.items()},source_zip_sha256=cp.BROWN_SHA,source_sha256={q:hashlib.sha256((ROOT/q).read_bytes()).hexdigest() for q in ('research/PROSE-COVER-035-SPEC.md','experiments/prose_cover.py','experiments/run_prose_cover.py','data/k4.json','data/controls.json')},stages={},pushed=False,Site_changed=False)
 vocab,plants=p.vocabularies(path);out['vocabularies']={name:p.vocab_receipt(v) for name,v in vocab.items()};out['artifact_additions']=p.ADDITIONS;out['plant_selection']=[{k:v for k,v in x.items() if k!='text'} for x in plants];lex={name:p.Lexicon(v) for name,v in vocab.items()};save(output,out)
 stage=dict(started_at_utc=utc(),models={});t=time.monotonic()
 for name,v in vocab.items():
  hist=p.mask_hist(97,known,v);stage['models'][name]=dict(mask_word_length_edges=hist,selectors=p.selectors(hist))
  if time.monotonic()-t>120 or cp.rss_bytes()>512*1024**2:stage['complete']=False;break
 else:stage['complete']=True
 stage.update(finished_at_utc=utc(),elapsed_seconds=time.monotonic()-t);out['stages']['mask_constraints']=stage
 controls=json.loads((ROOT/'data/controls.json').read_text());out['calibration']={}
 for key in ('k1','k2_restored_s','k3'):
  text=re.sub('[^A-Z]','',controls[key]['plaintext']);out['calibration'][key]=dict(length=len(text),source_stream_sha256=hashlib.sha256(text.encode()).hexdigest(),models={name:p.distribution(l.hist(text)) for name,l in lex.items()})
 save(output,out)
 actual_start=utc();actual=p.search(data['ciphertext'],known,lex,seconds=120);actual.update(started_at_utc=actual_start,finished_at_utc=utc());out['stages']['actual']=actual;save(output,out);print('actual',actual['complete'],actual['model_key_descriptions'],actual['distinct_lexical_plaintexts'],flush=True)
 prng=random.Random(350025);plantrows=[]
 for index,((name,equation),plant) in enumerate(zip([(a,e) for a in p.ALPHABETS for e in p.ak.COEFFICIENTS],plants)):
  alphabet=p.ALPHABETS[name];primer=''.join(prng.choice(alphabet) for _ in range(27));plain=plant['text'];cipher=p.ak.transform(plain,primer,alphabet,equation,'plaintext');mask={i:plain[i] for i in known};beg=utc();result=p.search(cipher,mask,lex,[(name,equation)],seconds=60)
  truth=[x for x in result['candidates'] if x['plaintext']==plain and x['primer']==primer];assert truth,'planted truth missing'
  plantrows.append(dict(started_at_utc=beg,finished_at_utc=utc(),alphabet=name,equation=equation,source={k:v for k,v in plant.items() if k!='text'},ciphertext=cipher,primer=primer,truth=plain,truth_recovered=True,search=result));print('plant',index+1,result['complete'],len(result['candidates']),flush=True)
 out['stages']['plants']=dict(complete=len(plantrows)==6 and all(x['search']['complete'] for x in plantrows),records=plantrows);save(output,out)
 rng=random.Random(350024);indices=sorted(set(range(97))-set(known));original=[data['ciphertext'][i] for i in indices];nulls=[];t=time.monotonic();nullstart=utc()
 for n in range(31):
  remaining=600-(time.monotonic()-t)
  if remaining<=0:break
  shuffled=original[:];rng.shuffle(shuffled);chars=list(data['ciphertext'])
  for i,v in zip(indices,shuffled):chars[i]=v
  cipher=''.join(chars);beg=utc();result=p.search(cipher,known,lex,seconds=min(120,remaining));nulls.append(dict(draw=n,started_at_utc=beg,finished_at_utc=utc(),ciphertext=cipher,search=result));print('null',n+1,result['complete'],result['distinct_lexical_plaintexts'],flush=True)
  if not result['complete']:break
 out['stages']['nulls']=dict(started_at_utc=nullstart,finished_at_utc=utc(),complete=len(nulls)==31 and all(x['search']['complete'] for x in nulls),seed=350024,shuffled_positions=indices,held_fixed_crib_cipher_positions=sorted(known),conditional_exchangeability_assumption=True,whole_family_statistic='Distinct complete lexical plaintexts in union of six cipher models and three nested lexicons',records=nulls,tail_resolution='1/32 only if31 complete; no positive significance claim from zero observed survivors')
 out.update(finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,peak_rss_bytes=cp.rss_bytes(),actual_K4_model_key_descriptions=actual['model_key_descriptions'],actual_K4_complete=actual['complete'],puzzle_solved=False);save(output,out);print('complete',out['elapsed_seconds'],out['peak_rss_bytes'],flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--brown-zip',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();run(args.brown_zip,args.output)
