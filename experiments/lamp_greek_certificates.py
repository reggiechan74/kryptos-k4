"""Replay the finite first-crib elimination and 24-symbol support certificates."""
import itertools,json
from pathlib import Path
import lamp_greek as g
ROOT=Path(__file__).resolve().parents[1]
def certificates():
 cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];rows=[]
 for role,name,eq,rev in itertools.product(('L','B'),g.ALPHABETS,('plus','beaufort'),(False,True)):
  checks=g.first_constraints(cipher,role,g.ALPHABETS[name],eq);survivors=list(itertools.product(range(1440),(0,1)));stages=[]
  for i,allowed,n in checks:
   survivors=[(t,p) for t,p in survivors if g.VALUES[int(rev)][p][(t+i)%1440]%n in allowed]
   stages.append(dict(operation_index=i,allowed_keys=sorted(allowed),modulus=n,remaining_clock_descriptions=len(survivors)))
   if not survivors:break
  rows.append(dict(role=role,alphabet=name,equation=eq,order='reverse' if rev else 'row_major',initial_clock_descriptions=2880,stages=stages,final_remaining=len(survivors)))
 return dict(kind='post_outcome_explanatory_replay_not_new_model_search',support=[dict(alphabet=name,serialized_support=a[:24],absent_actual_symbols=sorted(set(cipher)-set(a[:24]))) for name,a in g.ALPHABETS.items()],first_stage_eliminations=rows,limits='Finite clock-domain certificates, not all Greek or lamp mechanisms.')
if __name__=='__main__':print(json.dumps(certificates(),indent=2))
