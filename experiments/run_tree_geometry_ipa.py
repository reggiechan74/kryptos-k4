import argparse,hashlib,json,random,time
from datetime import datetime,timezone
from pathlib import Path
from tree_geometry_ipa import controls,select,budget
from run_io import RunSnapshot,specification,json_bytes
ROOT=Path(__file__).resolve().parents[1]
def stamp():return datetime.now(timezone.utc).isoformat()
def main():
 p=argparse.ArgumentParser();p.add_argument('--spec-commit',required=True);args=p.parse_args();cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];spec=ROOT/'research/TREE-GEOMETRY-IPA-026-SPEC.md'
 with RunSnapshot(ROOT/'results/tree-geometry-ipa-026','Item6 distinct tree geometry IPA mechanisms',specification(args.spec_commit,spec),execution_kind='original') as run:
  run.write('README.md',b'# Item 6 original run\n\nUTC chronology and source hashes are in the manifest and inputs. Controls precede actual and whole-family shuffled evaluations. These are exploratory rules, not historical evidence.\n')
  for label,fn,cap in [('controls',controls,180),('actual',lambda:select(cipher),30)]:
   started=stamp();clock=time.monotonic();out=fn();budget(clock,cap);out.update(started_at_utc=started,finished_at_utc=stamp());run.write(label+'.json',json_bytes(out));print(label,'completed',flush=True)
  clock=time.monotonic();started=stamp();rng=random.Random(260024);rows=[]
  for j in range(199):
   xs=list(cipher);rng.shuffle(xs);out=select(''.join(xs));rows.append(dict(index=j,first_survivors=len(out['first_survivors']),all_survivors=len(out['all_survivors'])));budget(clock,180)
  run.write('nulls.json',json_bytes(dict(started_at_utc=started,finished_at_utc=stamp(),seed=260024,draws=rows,first_events=sum(r['first_survivors']>0 for r in rows),all_events=sum(r['all_survivors']>0 for r in rows),no_negative_result_significance_claim=True)))
  paths=[Path(__file__),spec,ROOT/'experiments/tree_geometry_ipa.py',ROOT/'experiments/tree_geometry_ipa_reference.py',ROOT/'data/ipa-cambridge-us-v1.json',ROOT/'data/alphabet-features-v1.json',ROOT/'data/k4.json']
  run.write('inputs.json',json_bytes({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}));print(run.final,flush=True)
if __name__=='__main__':main()
