"""Frozen exact repair profiles, not proposed corrected English/canonical ciphertext."""
import collections,datetime,hashlib,itertools,json,time
from pathlib import Path
import minimum_repair_044 as m
ROOT=Path(__file__).resolve().parents[1];ALPHABETS={'AZ':'ABCDEFGHIJKLMNOPQRSTUVWXYZ','KRYPTOS':'KRYPTOSABCDEFGHIJLMNQUVWXZ'}
def run():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic();ctrl=m.controls();data=json.loads((ROOT/'data/k4.json').read_text());letters={x['start']-1+j:v for x in data['cribs'] for j,v in enumerate(x['plaintext'])};rows=[]
 for name,alphabet in ALPHABETS.items():
  C=tuple(map(alphabet.index,data['ciphertext']));known={i:alphabet.index(v) for i,v in letters.items()}
  for mode in ('periodic','plaintext','ciphertext'):
   for sigma,tau in ((1,1),(-1,1)) if mode=='periodic' else ((1,1),(1,-1),(-1,1)):
    for L in range(1,97):
     r=m.profile(C,known,L,26,sigma,tau,mode);r['alphabet']=name;w=r['witness'];r['witness']={k:''.join(alphabet[i] for i in v) if k in ('corrected_cipher','plaintext','key') else v for k,v in w.items()};rows.append(r)
     if time.monotonic()-clock>120:raise RuntimeError('Analytic batch unresolved')
 plants=[]
 for mode,lag in (('periodic',1),('periodic',7),('plaintext',1),('plaintext',26),('plaintext',27),('ciphertext',1),('ciphertext',73),('ciphertext',74)):
  P=[i%26 for i in range(97)]
  for i,ch in letters.items():P[i]=ALPHABETS['AZ'].index(ch)
  key=tuple((3*i+5)%26 for i in range(lag));C=m.encrypt(P,key,lag,26,1,1,mode);assert m.profile(C,{i:P[i] for i in letters},lag,26,1,1,mode)['minimum_substitutions']==0
  for sites in ((0,47),(21,73)):
   damaged=list(C)
   for i in sites:damaged[i]=(damaged[i]+1)%26
   result=m.profile(damaged,{i:P[i] for i in letters},lag,26,1,1,mode);assert result['minimum_substitutions']<=2;plants.append(dict(mode=mode,lag=lag,planted_edits=list(sites),minimum=result['minimum_substitutions'],true_cipher_key_still_a_valid_nonminimal_or_minimal_repair=True,minimal_truth_necessarily_unique=False,full_minimal_witness_replay=result['witness']['full_reencryption']))
 fixed=[dict(position_one_based=i+1,plaintext=p,ciphertext=data['ciphertext'][i]) for i,p in letters.items() if data['ciphertext'][i]==p];needs=collections.Counter(letters.values());have=collections.Counter(data['ciphertext']);deficits={ch:max(0,n-have[ch]) for ch,n in needs.items() if n>have[ch]};summary={}
 for mode in ('periodic','plaintext','ciphertext'):
  group=[r for r in rows if r['mode']==mode];summary[mode]=dict(descriptions=len(group),minimum_substitution_histogram=dict(sorted(collections.Counter(r['minimum_substitutions'] for r in group).items())),zero_repair_descriptions=sum(r['minimum_substitutions']==0 for r in group),short_1_to_12_minimum=min(r['minimum_substitutions'] for r in group if r['lag_or_period']<=12))
 return dict(id='MINIMUM-REPAIR-044',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('research/MINIMUM-REPAIR-044-SPEC.md','experiments/minimum_repair_044.py','experiments/run_minimum_repair_044.py','data/k4.json')},controls=ctrl,descriptions=len(rows),rows=rows,summary=summary,synthetic_two_error_plants=plants,direct_nonzero_strip_fixed_points=fixed,direct_nonzero_strip_substitution_lower_bound=len(fixed),arbitrary_permutation_required_letter_deficits=deficits,arbitrary_permutation_substitution_lower_bound=sum(deficits.values()),canonical_ciphertext_changed=False,puzzle_solved=False,worksheet_key_or_plaintext_errors_tested=False,Site_changed=False,pushed=False)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('started_at_utc','finished_at_utc','elapsed_seconds','controls','descriptions','summary','direct_nonzero_strip_fixed_points','arbitrary_permutation_required_letter_deficits')}))
