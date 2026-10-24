"""Frozen Brown window study and conditional capacity controls, local only."""
import argparse,gzip,hashlib,json,platform,random,subprocess,time
from pathlib import Path
import cover_extraction as c
import cover_phrase as p
from run_cover_extraction import encrypt,infer_caesar
ROOT=Path(__file__).resolve().parents[1]
def run(zip_path,output_prefix):
 models=c.models();lanes=[lane for m in models for lane in m.lanes()];start=p.utc();clock=time.monotonic();summary,bank,vocab,first=p.census(zip_path,lanes,str(output_prefix)+'-windows.jsonl.gz');output=dict(id='COVER-PHRASE-034',kind='Conditional corpus/cover capacity, not decryption or K4 significance',started_at_utc=start,corpus=summary,lanes=[dict(id=l.id,model=l.model.name,k=l.k,N=l.N,phase=l.phase,stratum=l.stratum,output_lengths=l.lengths) for l in lanes],vocabulary_sha256=hashlib.sha256('\n'.join(sorted(vocab)).encode()).hexdigest(),cipher_trials_on_actual_K4=0,Site_changed=False,push_attempted=False)
 if summary['complete']:
  nullstart=p.utc();nc=time.monotonic();rng=random.Random(340024);known=c.source_known(json.loads((ROOT/'data/k4.json').read_text()));draws=[];maxima=[]
  for draw in range(31):
   rows=[];event=False
   for m in models:
    for stratum in ('all','15'):
     words=m.sample(rng,None if stratum=='all' else 15)
     if words is None:continue
     for N,phase in [(1,0),(2,0),(2,1)]:
      for k in range(1,5):
       text=c.extract(words,k,N,phase);splits=p.split_message(text,vocab);in_corpus=text in bank;positive=in_corpus or splits['total']>0;event|=positive
       rows.append(dict(model=m.name,stratum=stratum,k=k,N=N,phase=phase,cover=''.join(words),coverwords=words,output=text,branch_A_member=in_corpus,branch_B=splits))
   draws.append(dict(draw=draw,any_family_match=event,records=rows));maxima.append(event)
   if time.monotonic()-nc>120 or p.rss_bytes()>512*1024**2:raise RuntimeError('frozen null-control budget exceeded; preserve corpus output')
  nullfile=str(output_prefix)+'-controls.json.gz'
  with gzip.open(nullfile,'wt') as f:json.dump(dict(seed=340024,draws=draws),f,separators=(',',':'))
  output['capacity_controls']=dict(started_at_utc=nullstart,finished_at_utc=p.utc(),elapsed_seconds=time.monotonic()-nc,draws=31,whole_family_max_positive=sum(maxima),saved_file=Path(nullfile).name,sha256=hashlib.sha256(Path(nullfile).read_bytes()).hexdigest(),bytes=Path(nullfile).stat().st_size,interpretation='Conditional capacity, not a K4 p-value; no observed independently decrypted cover exists')
  plants=[]
  for (model_id,stratum),(idx,source,text) in sorted(first.items()):
   lane=lanes[idx];words=p.construct_cover(lane,text);assert words is not None;cover=''.join(words);key=(17+len(plants))%26;cipher=encrypt(cover,key);found=infer_caesar(cipher,lane.model.vocab,known);assert len(found)==1 and found[0]['key']==key and found[0]['cover']==cover;recovered=c.extract(found[0]['words'],lane.k,lane.N,lane.phase);assert recovered==text and encrypt(found[0]['cover'],found[0]['key'])==cipher
   plants.append(dict(purpose='Conditional synthetic corpus-eligible plant, not recovered K4',source_reference=source,lane=lane.id,key_hidden_from_solver=key,cover=cover,coverwords=words,ciphertext=cipher,recovered_output=recovered,output_sha256=hashlib.sha256(text.encode()).hexdigest(),full97_reencryption=True,known_dictionary_and_extractor_supplied=True))
  output['eligible_phrase_plants']=plants;output['no_eligible_plant_groups']=[dict(model=m.name,stratum=s) for m in models for s in ('all','15') if (m.name,s) not in first]
  output['backward_bank_null_invariance']='With fixed length/cribs/vocabulary and no outer cipher, the entire backward corpus query is identical under ciphertext nulls; no significance claim is possible.'
 else:output['capacity_controls']=dict(status='not run: corpus incomplete, no use of partial vocabulary as full Brown')
 paths=['research/COVER-PHRASE-034-SPEC.md','experiments/cover_extraction.py','experiments/cover_phrase.py','experiments/run_cover_phrase.py','data/k4.json'];output.update(finished_at_utc=p.utc(),elapsed_seconds=time.monotonic()-clock,peak_rss_bytes=p.rss_bytes(),python=platform.python_version(),implementation_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),source_sha256={x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in paths});Path(str(output_prefix)+'-summary.json').write_text(json.dumps(output,indent=2)+'\n');return output
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--brown-zip',required=True);a.add_argument('--output-prefix',required=True);args=a.parse_args();r=run(args.brown_zip,args.output_prefix);print(json.dumps({k:r[k] for k in ['started_at_utc','finished_at_utc','elapsed_seconds','peak_rss_bytes']}));print(json.dumps(r['corpus']['counts']));print(json.dumps({k:r.get(k) for k in ['capacity_controls','no_eligible_plant_groups']}))
