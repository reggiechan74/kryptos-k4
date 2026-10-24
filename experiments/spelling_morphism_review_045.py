"""A memoryless globally reversible letter morphism cannot rescue equal-length anomalies."""
import datetime,hashlib,itertools,json
from pathlib import Path
import spelling_correction as s
ROOT=Path(__file__).resolve().parents[1]
def run():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();words=[''.join(x) for n in (1,2,3) for x in itertools.product('AB',repeat=n)];cases=equal=0
 for a,b in itertools.product(words,repeat=2):
  code={'A':a,'B':b}
  for n in range(1,5):
   for source in map(''.join,itertools.product('AB',repeat=n)):
    target=''.join(code[ch] for ch in source);cases+=1
    if len(target)==len(source):assert all(len(code[ch])==1 for ch in set(source));equal+=1
 f={'A':'','B':'B'};one='AB'+'A'*95;two='BA'+'A'*95;assert len(one)==len(two)==97 and one!=two and ''.join(f[x] for x in one)==''.join(f[x] for x in two)
 texts=s.full_sources(json.loads((ROOT/'data/controls.json').read_text()));rows=[]
 for role in ('normal_to_literal','literal_to_normal'):
  pairs=[(t['id'],t['normalized_comparison'],t['normalized_literal']) for t in texts[:2]]
  if role=='literal_to_normal':pairs=[(i,b,a) for i,a,b in pairs]
  assert all(len(a)==len(b) for _,a,b in pairs);value=s.infer_function(pairs,injective=True);assert not value['compatible'];rows.append(dict(role=role,equal_complete_stream_lengths=True,reduces_to_uniform_single_letter_on_observed_inputs=True,uniform_permutation_fit=value))
 return dict(id='SPELLING-MORPHISM-REVIEW-045',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),complete_binary_length_cases=cases,equal_length_cases=equal,full_fixed97_erasing_collision=dict(first=one,second=two,common_output='B'),source_constraints=rows,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('research/SPELLING-MORPHISM-REVIEW-045-SPEC.md','experiments/spelling_morphism_review_045.py','data/controls.json')},not_excluded=['context or word-boundary dependent codes','restricted vocabulary/framed side information','stateful invertible transducers','K3intent not independently established'],K4_trials=0)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(r['complete_binary_length_cases'],r['equal_length_cases'])
