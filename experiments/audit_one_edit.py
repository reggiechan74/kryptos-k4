"""Independent post-outcome complete periodic sets and permutation union audit."""
from collections import Counter
from datetime import datetime,timezone
import gzip,hashlib,itertools,json,math,time
from pathlib import Path
from one_edit_models import select,MODELS,ALPHABETS
from one_edit_channel import mask,forward,WINDOWS
from one_edit_reference import audit_periodic_instances
ROOT=Path(__file__).resolve().parents[1]

def multinomial_by_choices(total,counts):
 result=1
 for count in counts:
  result*=math.comb(total,count);total-=count
 assert total==0
 return result


def permutation_union(actual):
 catalog=actual['catalog'];unique={}
 for record in actual['permutation_classes']:
  instance=catalog['instances'][record['instance_id']];latent=catalog['strings'][instance['latent_id']];known=mask(instance['starts']);counts=Counter(latent);required=Counter(known.values());remaining=counts-required
  volume=multinomial_by_choices(len(latent)-len(known),[remaining[c] for c in sorted(remaining)])
  assert volume==int(record['distinct_plaintexts'])
  assert int(record['position_permutation_keys'])==volume*math.prod(math.factorial(n) for n in counts.values())
  key=(len(latent),tuple(sorted(counts.items())),tuple(sorted(known.items())))
  if key not in unique:unique[key]=dict(class_id=len(unique),length=len(latent),counts=dict(sorted(counts.items())),known_positions_one_based={str(i+1):p for i,p in known.items()},known_starts_zero_based=instance['starts'],distinct_plaintexts=str(volume),source_instance_ids=[],alignments=set())
  row=unique[key];row['source_instance_ids'].append(record['instance_id']);row['alignments'].update(a['alignment'] for a in instance['aliases'])
  for witness in record['witnesses']:
   text=witness['plaintext'];route=witness['latent_position_at_each_plaintext_position_zero_based'];assert sorted(route)==list(range(len(latent)));regenerated=['']*len(latent)
   for i,j in enumerate(route):regenerated[j]=text[i]
   assert ''.join(regenerated)==latent and all(text[i]==p for i,p in known.items())
   assert all(forward(latent,catalog['descriptions'][a['edit_id']])==json.loads((ROOT/'data/k4.json').read_text())['ciphertext'] for a in instance['aliases'])
 rows=list(unique.values());pairs=[]
 for a,b in itertools.combinations(rows,2):
  if a['length']!=b['length']:reason='different_lengths';witness=None
  elif a['counts']!=b['counts']:reason='different_letter_multisets';witness=None
  else:
   left=a['known_positions_one_based'];right=b['known_positions_one_based'];position=next((i for i in left if i in right and left[i]!=right[i]),None)
   if position is None:raise AssertionError('Cannot sum overlapping classes; exact union unresolved')
   reason='conflicting_known_position';witness=dict(position_one_based=int(position),letters=[left[position],right[position]])
  pairs.append(dict(classes=[a['class_id'],b['class_id']],disjoint_reason=reason,witness=witness))
 for row in rows:row['alignments']=sorted(row['alignments'])
 primary=[r for r in rows if 'ENGLISH_FIXED' in r['alignments']]
 return dict(unique_plaintext_constraint_classes=len(rows),primary_plaintext_constraint_classes=len(primary),pairwise_disjointness_checks=len(pairs),all_pairs_disjoint=True,exact_distinct_plaintexts_across_both_interpretations=str(sum(int(r['distinct_plaintexts']) for r in rows)),exact_distinct_plaintexts_primary_english_fixed=str(sum(int(r['distinct_plaintexts']) for r in primary)),original_bounds_are_preserved=True,post_outcome_reporting_refinement_not_new_search=True,classes=rows,disjointness_certificates=pairs)


def audit(folder=None):
 started=datetime.now(timezone.utc).isoformat();clock=time.monotonic();root=ROOT/'results/one-edit-028';folder=root/json.loads((root/'latest.json').read_text())['run_id'] if folder is None else Path(folder)
 with gzip.open(folder/'actual.json.gz','rt') as stream:actual=json.load(stream)
 result=audit_periodic_instances(actual);result['permutation_union']=permutation_union(actual);cat=actual['catalog'];fixed_witnesses=[];wheatstone_unrejected=[]
 for instance,row in zip(cat['instances'],actual['instance_results']):
  latent=cat['strings'][instance['latent_id']];known=mask(instance['starts']);fixed=[i for i,p in known.items() if latent[i]==p];groups={}
  for i,p in known.items():
   if i+1 in known:groups.setdefault((p,known[i+1]),set()).add(latent[i]==latent[i+1])
  wheat=any(len(values)>1 for values in groups.values())
  assert bool(fixed)==row['nonzero_strip_certificate_reject'] and wheat==row['wheatstone_relaxed_pair_certificate_reject']
  if fixed:fixed_witnesses.append([instance['instance_id'],fixed[0]+1,known[fixed[0]]])
  if not wheat:wheatstone_unrejected.append(instance['instance_id'])
 result['independent_certificate_replay']=dict(all_instances_checked=len(cat['instances']),strip_rejected_instances=len(fixed_witnesses),strip_first_fixed_witnesses=fixed_witnesses,wheatstone_certificate_unrejected_instance_ids=wheatstone_unrejected,necessary_conditions_only=True)
 positiveids={x['instance_id'] for x in actual['permutation_classes']};counts=Counter();letters=Counter()
 for instance in cat['instances']:
  if instance['instance_id'] not in positiveids:continue
  for alias in instance['aliases']:
   e=cat['descriptions'][alias['edit_id']];counts[(alias['alignment'],e['kind'])]+=1;letters[(e['kind'],e['latent_char'])]+=1
 result.update(permutation_compatible_by_alignment_and_operation=[dict(alignment=a,operation=k,count=n) for (a,k),n in sorted(counts.items())],permutation_compatible_inserted_or_replacement_letters=[dict(operation=k,letter=c,raw_alignment_cases=n) for (k,c),n in sorted(letters.items())],actual_complete_periodic_fits=len(actual['complete_periodic_fits']),unique_first_fit_records=len(actual['first_periodic_fits']),kind='independent_post_outcome_actual_set_and_exact_disjoint_union_validation',started_at_utc=started,finished_at_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'experiments/one_edit_reference.py')})
 return result
if __name__=='__main__':print(json.dumps(audit(),indent=2))
