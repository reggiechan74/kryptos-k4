"""Post-outcome exact reference and period/bit-operation validation."""
import hashlib,json,time
from datetime import datetime,timezone
from pathlib import Path
from tree_geometry_ipa import ROOT,MODELS,KEYS,CODES,select,crypt,rotl35,MASK
from tree_geometry_ipa_reference import step

def audit():
 started=datetime.now(timezone.utc).isoformat();clock=time.monotonic();cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];native=select(cipher);reference=select(cipher,True);assert native==reference
 bits=0
 for value in CODES.values():
  for state in (0,1,26,MASK,MASK-1)+tuple(1<<j for j in range(35)):
   assert step(state,value)==(rotl35(state,1)+(state^value))&MASK;bits+=1
 periods=[]
 for key,bytes_ in KEYS.items():
  residue=tuple(v%26 for v in bytes_);period=next(p for p in range(1,len(residue)+1) if len(residue)%p==0 and all(x==residue[i%p] for i,x in enumerate(residue)))
  assert period>12
  periods.append(dict(key=key,utf8_bytes=list(bytes_),mod26_values=list(residue),primitive_period=period,within_prior_unrestricted_period1to12=False))
 return dict(kind='post_outcome_independent_implementation_validation_not_new_model_search',started_at_utc=started,finished_at_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,actual_complete_record_set_equal=True,raw_descriptions=len(MODELS),geometry_bit_carry_boundary_checks=bits,ipa_periods=periods,actual_first_survivors=0,actual_all_survivors=0,independence_limit='Same author, independently structured reference; not external blinded verification.',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'experiments/tree_geometry_ipa_reference.py')})
if __name__=='__main__':print(json.dumps(audit(),indent=2))
