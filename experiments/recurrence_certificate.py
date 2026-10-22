"""Verify supplied exact contradictions, not a parameter search or synthesis run."""
import json
from math import gcd
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ALPHABETS=('ABCDEFGHIJKLMNOPQRSTUVWXYZ','KRYPTOSABCDEFGHIJLMNQUVWXZ')


def determinant(m):
    a,b,c=m[0];d,e,f=m[1];g,h,i=m[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def run():
    data=json.loads((ROOT/'data/k4.json').read_text())
    crib=data['cribs'][0]
    assert (crib['start'],crib['plaintext'])==(22,'EASTNORTHEAST')
    records=[]
    for alphabet in ALPHABETS:
        cipher=[alphabet.index(c) for c in data['ciphertext']]
        key={21+j:(cipher[21+j]-alphabet.index(p))%26 for j,p in enumerate(crib['plaintext'])}
        if alphabet==ALPHABETS[0]:
            # Internal transitions P23->P24 and P24->P25 (one-based).
            rows=[dict(from_position_one_based=i+1,key=key[i],cipher=cipher[i],
                       target_position_one_based=i+2,target_key=key[i+1]) for i in (22,23)]
            assert [(x['key'],x['cipher'],x['target_key']) for x in rows]==[(11,11,25),(25,17,2)]
            assert [(x['key']%2,x['cipher']%2) for x in rows]==[(1,1),(1,1)]
            assert rows[0]['target_key']%2 != rows[1]['target_key']%2
            records.append(dict(alphabet='AZ',certificate='identical predictor parity, different target parity',
                                rows=rows,contradicted=True))
        else:
            matrix=[[key[i],1,cipher[i]] for i in (21,22,23)]
            rhs=[key[i+1] for i in (21,22,23)]
            coeff=(11,23,24) # independently supplied certificate, not searched
            det=determinant(matrix)
            assert gcd(det,26)==1
            assert [sum(x*y for x,y in zip(row,coeff))%26 for row in matrix]==rhs
            i=24
            predicted=(coeff[0]*key[i]+coeff[1]+coeff[2]*cipher[i])%26
            assert (predicted,key[i+1])==(21,1)
            records.append(dict(alphabet='KRYPTOS',matrix=matrix,rhs=rhs,determinant=det,
                                determinant_is_unit=True,unique_coefficients_a_b_d=list(coeff),
                                next_from_position_one_based=25,target_position_one_based=26,
                                predicted_key=predicted,required_key=key[i+1],contradicted=True))
    return dict(id='RECURRENCE-CERTIFICATE-REVIEW-001',status='verified_contradictions',
                origin='Independent supplied certificates, locally recalculated from canonical fixtures',
                grammar='C_i=P_i+K_i;K0=k;K_i=a*K_(i-1)+b+d*C_(i-1) mod26, no reset, AZ or KRYPTOS',
                parameter_descriptions=2*26**4,parameter_search_executed=False,
                proofs=records,training_compatible=0,
                interpretation='All descriptions impossible already within first crib, regardless of seed/history. This is a symbolic certificate audit, not913952new local trials; known overlap remains documented.')


if __name__=='__main__':print(json.dumps(run(),indent=2))
