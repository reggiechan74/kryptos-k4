"""Frozen source-rule study: standard library, no K4 cipher scoring."""
import datetime,hashlib,itertools,json,math,platform,random,resource,subprocess,sys,time
from pathlib import Path
import spelling_correction as s
import spelling_correction_reference as ref
ROOT=Path(__file__).resolve().parents[1]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def strings(alphabet,length):return [''.join(x) for n in range(length+1) for x in itertools.product(alphabet,repeat=n)]
def controls():
 counts={};alignment_cases=0;alignment_roundtrips=0
 for alphabet,maxlen in [('AB',3),('ABC',2)]:
  for a in strings(alphabet,maxlen):
   for b in strings(alphabet,maxlen):
    native=s.alignments(a,b);distance,paths=ref.brute_alignments(a,b);assert native['distance']==distance;assert {''.join(c['op'] for c in x) for x in native['alignments']}==paths;alignment_cases+=1
    for columns in native['alignments']:assert s.apply_script(a,columns)==b and s.apply_script(b,s.inverse(columns))==a;alignment_roundtrips+=1
 counts.update(complete_tiny_alignment_sets=alignment_cases,all_retained_tiny_script_roundtrips=alignment_roundtrips)
 tiny_functions=0
 for alphabet in ('AB','ABC'):
  for a in strings(alphabet,2):
   for b in strings(alphabet,2):
    for injective in (False,True):
     got=s.infer_function([('tiny',a,b)],alphabet,injective)['completion_count'];assert got==ref.brute_function_count(a,b,alphabet,injective);tiny_functions+=1
 counts['complete_tiny_function_oracles']=tiny_functions
 for _,normal,literal,_ in s.WORDS:
  d=s.alignments(normal,literal)['distance'];assert ref.bfs_distance(normal,literal,2)==d;assert ref.bfs_distance(literal,normal,2)==d
 counts['independent_word_BFS_distances']=8
 plants=0;rng=random.Random(320024)
 for _ in range(24):
  perm=list(s.AZ);rng.shuffle(perm);table=dict(zip(s.AZ,perm));plain='SPHINXOFBLACKQUARTZJUDGEMYVOW'+s.AZ;cipher=''.join(table[c] for c in plain);got=s.infer_function([('plant',plain,cipher)],injective=True);assert got['compatible'] and got['completion_count']==1 and got['mapping']==table;plants+=1
 counts['planted_complete_substitutions']=plants
 affine=0
 for name,abc in s.ALPHABETS.items():
  for unit in range(26):
   if math.gcd(unit,26)!=1:continue
   inverse=next(x for x in range(26) if x*unit%26==1)
   for b in range(26):
    cipher=''.join(abc[(unit*i+b)%26] for i in range(26));plain=''.join(abc[(inverse*(abc.index(c)-b))%26] for c in cipher);assert plain==abc;affine+=1
  pairs=[('Q','L'),('U','O')]
  for invertible in (False,True):assert {(r['a'],r['b']) for r in s.affine_candidates(pairs,abc,invertible)}==set(ref.congruence_candidates(pairs,abc,invertible))
 counts['all_invertible_affine_roundtrips']=affine;counts['independent_affine_candidate_sets']=4
 for text in ('ASDF','QWERT','ZXCV'):
  got=s.keyboard_apply(text,(4,0));assert s.keyboard_apply(got,(-4,0))==text
 try:s.keyboard_apply('L',(4,0));raise AssertionError('keyboard boundary not rejected')
 except ValueError:pass
 counts['partial_keyboard_roundtrips']=3;counts['keyboard_boundary_rejections']=1
 masks=0
 for name,abc in s.ALPHABETS.items():
  for mode,key in s.masks(abc).items():
   for phase in range(len(key)):
    for text in ('PACKMYBOXWITHFIVEDOZENLIQUORJUGS',s.AZ,'ABRACADABRA'):
     coded=s.translate(text,key,abc,phase);assert s.translate(coded,key,abc,phase,True)==text;masks+=1
 counts['positional_mask_roundtrips']=masks
 assert s.apply_script('IQLUSION',s.alignments('IQLUSION','ILLUSION')['alignments'][0])=='ILLUSION'
 collapse=lambda t:t.replace('Q','L')
 assert collapse('IQLUSION')==collapse('ILLUSION')
 counts['metadata_free_correction_collision']=dict(inputs=['IQLUSION','ILLUSION'],same_output=collapse('ILLUSION'),label='toy Q-to-L correction only; not a complete source-fitting mechanism')
 return counts

def run():
 start=utc();clock=time.monotonic();checks=controls();control_end=utc();study=s.investigate(json.loads((ROOT/'data/controls.json').read_text()));end=utc();elapsed=time.monotonic()-clock;peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
 assert elapsed<=60 and peak<=256*1024**2
 source=['research/SPELLING-CORRECTION-032-SPEC.md','experiments/spelling_correction.py','experiments/spelling_correction_reference.py','experiments/run_spelling_correction.py','data/controls.json','data/k4.json']
 return dict(id='SPELLING-CORRECTION-032',kind='Original source-rule constraints and controls; no K4 model evaluation',started_at_utc=start,controls_finished_at_utc=control_end,finished_at_utc=end,elapsed_seconds=elapsed,peak_rss_bytes=peak,budget_seconds=60,budget_rss_bytes=256*1024**2,python=platform.python_version(),implementation_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source},controls=checks,study=study,canonical_ciphertext_changed=False,K4_trials=0,pushed=False,Site_changed=False)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=run();Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['started_at_utc','finished_at_utc','elapsed_seconds','peak_rss_bytes','K4_trials']}));print(json.dumps(out['controls']));print(json.dumps(out['study']['source_rule_feasibility']))
