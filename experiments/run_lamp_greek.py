"""Record original frozen item5 controls, complete selector and histogram nulls."""
import argparse
from datetime import datetime,timezone
import hashlib,json,random,time
from pathlib import Path
from lamp_greek import controls,select,representation_audit,ALPHABETS
from run_io import RunSnapshot,json_bytes,specification
ROOT=Path(__file__).resolve().parents[1]

def stamp():return datetime.now(timezone.utc).isoformat()
def main():
    p=argparse.ArgumentParser();p.add_argument('--spec-commit',required=True);args=p.parse_args()
    cipher=json.loads((ROOT/'data/k4.json').read_text())
    if isinstance(cipher,dict):
        cipher=cipher.get('ciphertext',cipher.get('text'))
    assert isinstance(cipher,str) and len(cipher)==97
    spec=ROOT/'research/LAMP-GREEK-025-SPEC.md'
    with RunSnapshot(ROOT/'results/lamp-greek-025','Item5 ordinal lamp Greek codecs',specification(args.spec_commit,spec),execution_kind='original') as run:
        run.write('README.md',b'# Original item 5 run\n\nThe manifest supplies UTC chronology and hashes. Controls, full actual selection and 199 whole-family nulls are separate receipts. No historical mechanism claim.\n')
        for label,fn in [('controls',controls),('representation',representation_audit),('actual',lambda:select(cipher,seconds=30))]:
            started=stamp();out=fn();out.update(started_at_utc=started,finished_at_utc=stamp());run.write(label+'.json',json_bytes(out));print(label, 'completed',flush=True)
        started=stamp();clock=time.monotonic();rng=random.Random(250024);rows=[]
        for i in range(199):
            xs=list(cipher);rng.shuffle(xs);result=select(''.join(xs),clock,120)
            rows.append(dict(index=i,first_survivors=result['first_survivors'],all_survivors=result['all_survivors'],accounting=result['accounting']))
        run.write('nulls.json',json_bytes(dict(seed=250024,shuffles=199,rows=rows,first_events=sum(r['first_survivors']>0 for r in rows),all_events=sum(r['all_survivors']>0 for r in rows),started_at_utc=started,finished_at_utc=stamp(),elapsed_seconds=time.monotonic()-clock,interpretation='Full-family histogram controls; no significance claim for a negative actual result.')))
        sources={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in (spec,Path(__file__),ROOT/'experiments/lamp_greek.py',ROOT/'experiments/conditional_face_lamp.py',ROOT/'data/k4.json')}
        run.write('inputs.json',json_bytes(sources));print(run.final,flush=True)
if __name__=='__main__':main()
