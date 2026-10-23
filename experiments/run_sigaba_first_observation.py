"""Frozen synthetic CSP-889 resource gate. Never reads data/k4.json."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path
import sigaba_real_adapter as real
import sigaba_first_observation as sparse
import sigaba_joint_toy as toy
ROOT=Path(__file__).resolve().parents[1]
PIN=['experiments/sigaba_first_observation.py','research/SIGABA-FIRST-OBSERVATION-SPEC.md','experiments/sigaba_domain_identity.py','research/SIGABA-DOMAIN-IDENTITY-SPEC.md','research/SIGABA-DOMAIN-IDENTITY-IMPLEMENTATION.md','experiments/sigaba_sparse_ownership.py','research/SIGABA-SPARSE-OWNERSHIP-SPEC.md','experiments/sigaba_real_adapter.py','experiments/run_sigaba_first_observation.py','experiments/sigaba_csp889.py','experiments/sigaba_torus.py','experiments/sigaba_joint_toy.py','data/sigaba-csp889-v1.json','research/SIGABA-REAL-ADAPTER-SPEC.md']
def run(n):
 b=toy.Budget(60);f=real.fixture(n);m=real.RealModel(budget=b);assert m.stream(f['plaintext'],f['key'])==f['ciphertext'];assert real.physical(f['plaintext'],f['key'])==f['ciphertext'];b.check(force=True)
 pre=dict(cipher_starts=26**5,control_starts=26**5,raw_index_starts=10**5,index_functions=len(m.maps),raw_full_start_descriptions=str(26**10*10**5),cipher_domain_payload_bytes=(26**5+7)//8,index_domain_payload_bytes=(len(m.maps)+7)//8,one_dense_cipher_domain_per_index_function_bytes=len(m.maps)*((26**5+7)//8),estimate_is_necessary_lower_bound=False,Cartesian_table_allocated=False)
 digest=hashlib.sha256()
 for mapping,aliases in zip(m.maps,m.aliases):digest.update(json.dumps([mapping,len(aliases)],separators=(',',':')).encode()+b'\n')
 previous=json.loads((ROOT/f'results/sigaba-real-adapter/case-{n}.json').read_text());assert f=={**previous['fixture'],'observations':[tuple(x) for x in previous['fixture']['observations']]}
 result=sparse.solve(m,f['observations'],b)
 return dict(id='CSP889-ANCHOR-017',fixture=f,preflight=pre,index_quotient_sha256=digest.hexdigest(),solver=result,plant_directly_validated=True,plant_selector_recovered=None if not result['completed'] else 'requires complete relation replay',independent_full_compatible_set_validation=False,real_sized_gate_passed=False,K4_evaluations=0,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in PIN})
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,choices=(0,1));ap.add_argument('--output',required=True);ap.add_argument('--all',action='store_true');a=ap.parse_args()
 if a.all:
  out=Path(a.output);out.mkdir(exist_ok=True,parents=True)
  for n in (0,1):
   p=out/f'case-{n}.json'
   try:subprocess.run([sys.executable,__file__,'--case',str(n),'--output',str(p)],check=True,timeout=65)
   except subprocess.TimeoutExpired:
    p.write_text(json.dumps(dict(id='CSP889-ANCHOR-017',case=n,status='watchdog_unresolved',completed=False,exact_raw_key_count=None,real_sized_gate_passed=False,K4_evaluations=0))+'\n')
   r=json.loads(p.read_text());print(n,r.get('solver',{}).get('reason'),r.get('solver',{}).get('budget'),flush=True)
 else:Path(a.output).write_text(json.dumps(run(a.case),indent=2)+'\n')
