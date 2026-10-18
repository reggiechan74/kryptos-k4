"""Bounded literal-key confirmation and inherited period13 witness; no broad search."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from bounded_models import ALPHABETS,EQUATIONS,crypt,required_key
ROOT=Path(__file__).resolve().parents[1]
KEY='WESTSOUTHWEST'

def check():
    data=json.loads((ROOT/'data/k4.json').read_text());cipher=data['ciphertext'];known={i:p for x in data['cribs'] for i,p in enumerate(x['plaintext'],x['start']-1)}
    assert len(KEY)==13 and len(known)==24 and len(cipher)==97
    assert Fraction(3,16)+Fraction(1,2)==Fraction(11,16)
    assert Fraction(11,16)*360==Fraction(495,2)
    assert cipher[21]=='F' and known[21]=='E' and cipher[73]=='K' and known[73]=='K'
    assert (74-22)==4*13
    expected={('AZ','plus'):['B','A'],('AZ','minus'):['Z','A'],('AZ','beaufort'):['J','U'],('KRYPTOS','plus'):['R','K'],('KRYPTOS','minus'):['Z','K'],('KRYPTOS','beaufort'):['W','K']}
    witnesses=[];cases=[]
    for name,a in ALPHABETS:
        for eq in EQUATIONS:
            values=[required_key(known[i],cipher[i],a,eq) for i in (21,73)];letters=[a[v] for v in values]
            assert values[0]!=values[1] and letters==expected[(name,eq)]
            witnesses.append({'alphabet':name,'equation':eq,'one_based_positions':[22,74],'required_key_letters':letters,'required_key_values':values})
            for phase in range(13):
                rotated=KEY[phase:]+KEY[:phase];key=[a.index(c) for c in rotated]
                plain=crypt(cipher,key,a,eq,decrypt=True)
                matches=[i+1 for i,p in sorted(known.items()) if plain[i]==p]
                cases.append({'alphabet':name,'equation':eq,'cyclic_phase_zero_based':phase,'crib_matches':len(matches),'matching_one_based_positions':matches})
    assert len(cases)==78 and max(c['crib_matches'] for c in cases)==3 and not any(c['crib_matches']==24 for c in cases)
    return {'check':'WESTSOUTHWEST-NOTE-001','candidate':KEY,'reverse_bearing_clockwise_true_north_deg':'495/2','radians_coefficient_of_pi':'11/8','original_confirmed_crib_replaced':False,'literal_key_cases':cases,'case_count':78,'fully_matching_cases':0,'best_crib_matches':3,'total_confirmed_crib_letters':24,'period13_witnesses':witnesses,'phase_convention':'key[(zero_based_message_index+phase)%13], literal key valued in selected alphabet; direct alignment','classification':'Inherited period13 contradiction and exact literal-candidate confirmation; not new cipher-family exclusion','new_broad_search':False,'full_plaintexts_saved':False,'input_sha256':{'data/k4.json':hashlib.sha256((ROOT/'data/k4.json').read_bytes()).hexdigest(),'experiments/check_westsouthwest.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}

if __name__=='__main__':print(json.dumps(check(),indent=2))
