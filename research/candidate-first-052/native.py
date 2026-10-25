"""Exact C acceleration with Python reference descriptions. No network or model APIs."""
from __future__ import annotations
import ctypes as ct
import hashlib
import json
from pathlib import Path
import subprocess
import reference as p

ROOT=Path(__file__).resolve().parent
LIB=ROOT/'scorer.so'
DESCRIPTIONS=tuple((t,s,r) for t in p.TABLEAUX for s in p.STRUCTURES for r in p.PERIODS)
KEYS=tuple((t.id,s,r) for t,s,r in DESCRIPTIONS)
RANK_MAP={key:i for i,key in enumerate(sorted(KEYS))}
RANKS=(ct.c_int*1152)(*(RANK_MAP[k] for k in KEYS))
PERIOD_TABLE=(ct.c_double*(32*74))(*(value for r in p.PERIODS for value in p.PERIOD_SCORES[r]))
AUTO_TABLE=(ct.c_double*(32*74))(*(value for r in p.PERIODS for value in p.AUTO_SCORES[r]+(0.0,)*(74-len(p.AUTO_SCORES[r]))))


def build():
    command=['cc','-O3','-std=c99','-Wall','-Wextra','-Werror','-fPIC','-shared',str(ROOT/'scorer.c'),'-o',str(LIB)]
    result=subprocess.run(command,text=True,capture_output=True)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    compiler=subprocess.run(['cc','--version'],text=True,capture_output=True,check=True).stdout
    receipt={'command':command,'compiler':compiler,'source_sha256':p.sha256_file(ROOT/'scorer.c'),
             'binary_sha256':p.sha256_file(LIB),'no_fast_math':True}
    p.write_json(ROOT/'build.json',receipt)
    return receipt


def library():
    lib=ct.CDLL(str(LIB))
    lib.score_bank.argtypes=[ct.c_size_t,ct.POINTER(ct.c_uint8),ct.POINTER(ct.c_uint8),ct.POINTER(ct.c_double),
        ct.POINTER(ct.c_double),ct.POINTER(ct.c_int),ct.POINTER(ct.c_double),ct.POINTER(ct.c_int),
        ct.POINTER(ct.c_uint64),ct.POINTER(ct.c_double)]
    lib.score_bank.restype=ct.c_int
    return lib


class NativeScorer:
    def __init__(self,bank,expected_count=1024):
        self.bank=p.validate_bank(bank,expected_count)
        self.n=len(self.bank)
        self.plain=[{a:p.encode(rec['text'],a) for a in p.ALPHABETS} for rec in self.bank]
        raw=bytes(v for row in self.plain for a in p.ALPHABETS for v in row[a])
        self.input=(ct.c_uint8*len(raw)).from_buffer_copy(raw)
        self.lib=library()

    def raw(self,ciphertext,all_scores=False,with_ties=False):
        p.validate_ciphertext(ciphertext)
        raw=bytes(v for a in p.ALPHABETS for v in p.encode(ciphertext,a))
        cipher=(ct.c_uint8*len(raw)).from_buffer_copy(raw)
        best=(ct.c_double*self.n)();desc=(ct.c_int*self.n)()
        ties=(ct.c_uint64*(self.n*18))() if with_ties else None
        scores=(ct.c_double*(self.n*1152))() if all_scores else None
        status=self.lib.score_bank(self.n,self.input,cipher,PERIOD_TABLE,AUTO_TABLE,RANKS,best,desc,ties,scores)
        if status:raise RuntimeError(f'native scorer status{status}')
        return best,desc,ties,scores

    def score(self,ciphertext,details=False):
        best,desc,ties,_=self.raw(ciphertext,with_ties=details)
        maximum=max(best)
        if not details:return maximum
        ranked=[]
        cipher={a:p.encode(ciphertext,a) for a in p.ALPHABETS}
        for j,record in enumerate(self.bank):
            t,structure,r=DESCRIPTIONS[desc[j]]
            plain,c=self.plain[j][t.plain_alphabet],cipher[t.cipher_alphabet]
            q=p.induced(plain,c,t.operation)
            d=p.reference_description(q,plain,c,structure,r)
            if d['score_bits']!=best[j]:raise AssertionError('C/reference score disagreement')
            tied=[]
            for index,(tt,ss,rr) in enumerate(DESCRIPTIONS):
                if ties[j*18+index//64] & (1 << (index%64)):
                    tied.append({'tableau_id':tt.id,'structure':ss,'r':rr})
            tied.sort(key=lambda x:(x['tableau_id'],x['structure'],x['r']))
            entry={'candidate_id':record['id'],'group':record['group'],'score_bits':best[j],
                   'tableau_id':t.id,'structure':structure,'r':r,'equal_score_top_descriptions':tied,
                   'plaintext':record['text'],**d}
            for key in ('original_id','source_file','source_sha256','spaced_prose','theme'):
                if key in record:entry[key]=record[key]
            ranked.append(entry)
        ranked.sort(key=lambda x:(-x['score_bits'],x['candidate_id'],x['tableau_id'],x['structure'],x['r']))
        return {'maximum_score_bits':maximum,'ranked_candidates':ranked,
                'tied_top_candidate_ids':[r['candidate_id'] for r in ranked if abs(r['score_bits']-maximum)<1e-10],
                'different_plaintext_margin_bits':ranked[0]['score_bits']-ranked[1]['score_bits']}


if __name__=='__main__':print(json.dumps(build(),indent=2))


def exact_diagnostics(bank,ciphertext,expected_count=1024):
    """Same full97-letter diagnostics; cache only candidate-invariant crib equations."""
    records=p.validate_bank(bank,expected_count)
    cipher={a:p.encode(ciphertext,a) for a in p.ALPHABETS}
    first={a:p.encode(records[0]['text'],a) for a in p.ALPHABETS}
    known_constraints={}
    for t in p.TABLEAUX:
        plain,c=first[t.plain_alphabet],cipher[t.cipher_alphabet]
        q=p.induced(plain,c,t.operation)
        known_constraints[t.id]={
            'crib_excluded_periods':[r for r in p.PERIODS if any(q[i]!=q[j] for i in p.KNOWN for j in p.KNOWN if i%r==j%r)],
            'crib_excluded_plaintext_autokey_lengths':[r for r in p.PERIODS if any(q[i]!=plain[i-r] for i in p.KNOWN if i>=r and i-r in p.KNOWN)],
            'crib_excluded_ciphertext_autokey_lengths':[r for r in p.PERIODS if any(q[i]!=c[i-r] for i in p.KNOWN if i>=r)]}
    results=[]
    for rec in records:
        encoded={a:p.encode(rec['text'],a) for a in p.ALPHABETS}
        for t in p.TABLEAUX:
            plain,c=encoded[t.plain_alphabet],cipher[t.cipher_alphabet]
            q=p.induced(plain,c,t.operation)
            if tuple(p.forward(a,k,t.operation) for a,k in zip(plain,q))!=c:
                raise AssertionError('Full re-encryption failed')
            if tuple(p.backward(b,k,t.operation) for b,k in zip(c,q))!=plain:
                raise AssertionError('Full inverse failed')
            periods=[r for r in range(1,98) if all(q[i]==q[i-r] for i in range(r,97))]
            pa=[r for r in p.PERIODS if all(q[i]==plain[i-r] for i in range(r,97))]
            ca=[r for r in p.PERIODS if all(q[i]==c[i-r] for i in range(r,97))]
            results.append({'candidate_id':rec['id'],'tableau_id':t.id,'minimum_exact_period':min(periods),
                            'registered_exact_periods':[r for r in periods if r<=32],
                            'exact_plaintext_autokey_lengths':pa,'exact_ciphertext_autokey_lengths':ca,
                            **known_constraints[t.id],'full_reencryption':True,'full_inverse':True})
    return results
