"""Four supplied adjacent affine-digraph parity certificates; no key search."""
import json
from pathlib import Path
from ipa_preprocessing import AZ,KR
ROOT=Path(__file__).resolve().parents[1]
WITNESSES=[('AZ',1,[25,29],['TN','TH'],['VQ','RN']),
           ('AZ',2,[22,32],['EA','AS'],['FL','KS']),
           ('KRYPTOS',1,[27,31],['OR','EA'],['QP','GK']),
           ('KRYPTOS',2,[22,26],['EA','NO'],['FL','QQ'])]


def parity_obstruction(pairs,alphabet):
    seen={}
    for plain,cipher in pairs:
        ip=tuple(alphabet.index(c)%2 for c in plain)
        op=tuple(alphabet.index(c)%2 for c in cipher)
        if ip in seen and seen[ip]!=op:return {'input_parity':list(ip),'opposed_output_parities':[list(seen[ip]),list(op)]}
        seen[ip]=op
    return None


def verify():
    data=json.loads((ROOT/'data/k4.json').read_text())
    known={i:c for crib in data['cribs'] for i,c in enumerate(crib['plaintext'],crib['start'])}
    certificates=[]
    for name,origin,positions,plain,cipher in WITNESSES:
        a=AZ if name=='AZ' else KR
        actual_plain=[''.join(known[p+j] for j in range(2)) for p in positions]
        actual_cipher=[data['ciphertext'][p-1:p+1] for p in positions]
        assert actual_plain==plain and actual_cipher==cipher
        assert all((p-origin)%2==0 for p in positions)
        obstruction=parity_obstruction(list(zip(plain,cipher)),a);assert obstruction
        certificates.append({'alphabet':name,'pair_origin_one_based':origin,'positions':positions,
                             'plaintext_pairs':plain,'ciphertext_pairs':cipher,**obstruction})
    positives=mutations=0
    for a in (AZ,KR):
        for matrix in ([[1,0],[0,1]],[[1,2],[3,5]],[[0,0],[0,0]],[[2,0],[0,2]]):
            for offset in ([0,0],[5,7]):
                vectors=[[1,3],[5,7]]
                output=[[(sum(row[j]*v[j] for j in range(2))+offset[i])%26 for i,row in enumerate(matrix)] for v in vectors]
                pairs=[(''.join(a[x] for x in v),''.join(a[x] for x in out)) for v,out in zip(vectors,output)]
                assert parity_obstruction(pairs,a) is None;positives+=1
                bad=[list(out) for out in output];bad[1][0]=(bad[1][0]+1)%26
                changed=[(''.join(a[x] for x in v),''.join(a[x] for x in out)) for v,out in zip(vectors,bad)]
                assert parity_obstruction(changed,a) is not None;mutations+=1
    return {'model':'C_pair=M*P_pair+b mod26, same AZ/AZ or KRYPTOS/KRYPTOS coordinates, adjacent pair origins 1 or 2 one-based',
            'certificates':certificates,'analytic_exclusions':4,'matrices_or_keys_searched':0,
            'invertibility_not_required_for_exclusion':True,
            'controls':{'fixed_affine_positive_cases':positives,'parity_mutation_negatives':mutations},
            'source':'Exact witnesses supplied by parent; independently checked against unchanged canonical English cribs/ciphertext.',
            'scope':'Not all polygraphic ciphers, mixed alphabets, variable matrices, reordered pairs or other preprocessing.'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
