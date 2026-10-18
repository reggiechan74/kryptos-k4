"""24 frozen endpoint/multiset checks; no word/permutation/key search."""
import argparse
from collections import Counter
import json
import random
import time

from bounded_models import deadline_check
from masking_pilots import autokey,autokey_scan,read_spec,AUTO_SPEC
from run_bounded import ROOT,execute,inputs_hashes,validated_baseline
from run_io import specification

SPEC='research/specifications/WORD-SCRAMBLE-001.json'


def word_invariants(observed,target):
    length=len(observed)==len(target)
    first=length and observed[:1]==target[:1]
    last=length and observed[-1:]==target[-1:]
    actual=Counter(observed[1:-1]);expected=Counter(target[1:-1])
    counts=length and actual==expected
    reason=None if length and first and last and counts else 'word_length' if not length else 'endpoint_mismatch' if not(first and last) else 'interior_multiset_mismatch'
    return {'target':target,'observed_intermediate':observed,'length_matches':length,
            'first_matches':first,'last_matches':last,'interior_counts_match':counts,
            'target_interior_counts':dict(sorted(expected.items())),
            'observed_interior_counts':dict(sorted(actual.items())),
            'compatible':reason is None,'first_rejecting_condition':reason}


def apply_schedule(text,words,schedules,inverse=False):
    """Explicit synthetic-control permutations only; never infer a schedule."""
    if len(words)!=len(schedules):raise ValueError('one explicit schedule per word required')
    out=list(text);occupied=set()
    for word,permutation in zip(words,schedules):
        begin,end=word['start']-1,word['end']
        if not 0<=begin<end<=len(text):raise ValueError('invalid fixed span')
        span=set(range(begin,end))
        if occupied&span:raise ValueError('overlapping spans')
        occupied|=span
        interior=out[begin+1:end-1];n=len(interior)
        if sorted(permutation)!=list(range(n)):raise ValueError('invalid interior permutation')
        if inverse:
            restored=['']*n
            for j,source in enumerate(permutation):restored[source]=interior[j]
            out[begin+1:end-1]=restored
        else:out[begin+1:end-1]=[interior[i] for i in permutation]
    return ''.join(out)


def validate_intermediates(data,intermediates):
    spec=read_spec(AUTO_SPEC)
    expected={(a,p,f) for a in spec['alphabets'] for p in spec['primers'] for f in spec['feedback_sources']}
    actual=[(r['alphabet'],r['primer'],r['feedback']) for r in intermediates]
    if len(actual)!=12 or len(set(actual))!=12 or set(actual)!=expected:raise ValueError('must reuse exactly the frozen12models')
    for record in intermediates:
        q=record['plaintext']
        if len(q)!=97 or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in q):raise ValueError('complete97letter intermediate required')
        if autokey(q,record['alphabet'],record['primer'],record['feedback'])!=data['ciphertext']:
            raise ValueError('intermediate does not regenerate ciphertext')


def word_scan(data,intermediates,limit=10):
    started=time.monotonic();deadline_check(started,limit);validate_intermediates(data,intermediates)
    branches=read_spec(SPEC)['segmentation_branches'];records=[]
    for intermediate in intermediates:
        q=intermediate['plaintext']
        for branch in branches:
            deadline_check(started,limit);words=[]
            for word in branch['words']:
                check=word_invariants(q[word['start']-1:word['end']],word['text'])
                check.update({'start':word['start'],'end':word['end']});words.append(check)
            compatible=all(w['compatible'] for w in words)
            records.append({'alphabet':intermediate['alphabet'],'primer':intermediate['primer'],'feedback':intermediate['feedback'],
                'branch':branch['id'],'segmentation_is_assumption':True,'intermediate_Q':q,'word_checks':words,
                'compatible':compatible,'cipher_E_forward_regeneration':True,
                'complete_English_P_and_schedule_available':False,
                'first_rejecting_condition':next((w['first_rejecting_condition'] for w in words if not w['compatible']),None)})
            if len(records)>24:raise RuntimeError('24check cap exceeded')
    assert len(records)==24;deadline_check(started,limit)
    return {'experiment':'WORD-SCRAMBLE-001','tested_checks':24,'compatible_checks':sum(r['compatible'] for r in records),
            'records':records,'key_fits':0,'factorial_permutation_searches':0,'scoring':'none',
            'scope':'Only12frozen complete autokey intermediates x2fixed segmentation assumptions. Compatibility would not reconstruct full P or a permutation schedule, or establish a masking method.'}


def target_record(result,alphabet,primer,feedback,branch):
    return next(r for r in result['records'] if (r['alphabet'],r['primer'],r['feedback'],r['branch'])==(alphabet,primer,feedback,branch))


def controls():
    rng=random.Random(20261018);spec=read_spec(AUTO_SPEC);branches=read_spec(SPEC)['segmentation_branches']
    accepted=endpoint_rejects=count_rejects=roundtrips=0
    for branch in branches:
        words=branch['words'];schedule=[list(reversed(range(w['end']-w['start']-1))) for w in words]
        for alphabet in spec['alphabets']:
            for primer in spec['primers']:
                for feedback in spec['feedback_sources']:
                    plain=''.join(rng.choice(alphabet) for _ in range(97));plain=plain[:21]+'EASTNORTHEAST'+plain[34:63]+'BERLINCLOCK'+plain[74:]
                    q=apply_schedule(plain,words,schedule)
                    assert apply_schedule(q,words,schedule,True)==plain;roundtrips+=1
                    cipher=autokey(q,alphabet,primer,feedback)
                    data={'ciphertext':cipher,'cribs':[{'start':22,'end':34,'plaintext':'EASTNORTHEAST'},{'start':64,'end':74,'plaintext':'BERLINCLOCK'}]}
                    intermediates=autokey_scan(data)['records'];result=word_scan(data,intermediates)
                    true=target_record(result,alphabet,primer,feedback,branch['id']);assert true['compatible'];accepted+=1
                    first=words[0]['start']-1
                    for kind,index in [('endpoint',first),('count',first+1)]:
                        changed=q[:index]+'Z'+q[index+1:];data_bad=dict(data);data_bad['ciphertext']=autokey(changed,alphabet,primer,feedback)
                        tested=word_scan(data_bad,autokey_scan(data_bad)['records'])
                        true=target_record(tested,alphabet,primer,feedback,branch['id']);assert not true['compatible']
                        assert true['word_checks'][0]['first_rejecting_condition']==('endpoint_mismatch' if kind=='endpoint' else 'interior_multiset_mismatch')
                        if kind=='endpoint':endpoint_rejects+=1
                        else:count_rejects+=1
    assert word_invariants('SLAT','SALT')['compatible'] and word_invariants('SALT','SLAT')['compatible']
    assert apply_schedule('SALT',[{'start':1,'end':4}],[[1,0]])=='SLAT'
    assert apply_schedule('SLAT',[{'start':1,'end':4}],[[1,0]],True)=='SALT'
    return {'seed':20261018,'generator':'Python random.Random/MT19937','synthetic_schedule':'reverse interiors, known and retained; not fitted to actual K4',
            'actual_scanner_planted_acceptances':accepted,'endpoint_rejections':endpoint_rejects,'interior_multiset_rejections':count_rejects,
            'full_control_schedule_roundtrips':roundtrips,'SALT_SLAT_ambiguity_verified':True}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--spec-commit',required=True);parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output-dir',default='results/word-runs');args=parser.parse_args()
    frozen=read_spec(SPEC);artifact=frozen['fixed_intermediate_artifact'];spec=specification(args.spec_commit,SPEC)
    if len(args.code_commit)!=40 or any(c not in '0123456789abcdef' for c in args.code_commit):raise ValueError('full implementation commit required')
    spec['implementation_commit']=args.code_commit;holder={}
    def preflight():
        holder['data']=validated_baseline(ROOT/'data/k4.json')
        holder['intermediates']=json.loads((ROOT/artifact).read_text())['records']
    def action(limit):
        started=time.monotonic();deadline_check(started,limit);checks=controls();deadline_check(started,limit)
        result=word_scan(holder['data'],holder['intermediates'],limit);result['controls']=checks;deadline_check(started,limit);return result
    files=[SPEC,AUTO_SPEC,artifact,'data/k4.json','experiments/word_scramble.py','experiments/masking_pilots.py','experiments/run_io.py','experiments/run_bounded.py','experiments/check_baseline.py']
    run_id=execute(args.output_dir,'word-interior-compatibility',spec,[('WORD-SCRAMBLE-001',action,10)],inputs_hashes(files),'python3 experiments/word_scramble.py --spec-commit '+args.spec_commit+' --code-commit '+args.code_commit,preflight)
    print('completed word run',run_id)


if __name__=='__main__':main()
