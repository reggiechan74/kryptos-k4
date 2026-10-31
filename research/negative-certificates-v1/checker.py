"""Read-only inherited-negative metadata checker; never computes target key values."""
import argparse
import hashlib
import json
from pathlib import Path

RECEIPT = 'results/MINIMUM-REPAIR-044-ORIGINAL.json'
RECEIPT_HASH = 'a270eea127fd1c11343034e390c6a25ff87c2ac21d24c9fc2648da98137840a2'
DEPENDENCIES = {
 'research/MINIMUM-REPAIR-044-SPEC.md': 'bd4b7619b4326b82bbc30218def671a6b5eff53bd5ece4318ab2e0c297a684a6',
 'experiments/minimum_repair_044.py': '741c29952b214553b8125843efaf918963d40a82eb639a28245e395818128e4f',
 'experiments/run_minimum_repair_044.py': 'aefe53e55cd997c7c8a129fd6f721ec0c21b5fa08fe98992ecb4dfdcf1caec0c',
 'data/k4.json': '08a1a84bd0dddf2449a2c7f67ee770d093ed47f6ad9a795630b77a2c8062f241',
}
CONTEXT = {
 'equation': 'C = sigma*P + tau*K (mod q)', 'sigma': 1, 'tau': 1, 'q': 26,
 'plaintext_alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
 'ciphertext_alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'key_alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
 'data_sha256': DEPENDENCIES['data/k4.json'],
 'normalization': 'identity uppercase A-Z; no edits, insertions, deletions, or reordering',
 'alignment': 'same plaintext/ciphertext position; zero-based', 'message_length': 97,
 'coordinates': list(range(21,34)) + list(range(63,74)),
}

def load_json(text):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out: raise ValueError('duplicate JSON key: '+k)
            out[k]=v
        return out
    return json.loads(text, object_pairs_hook=pairs, parse_constant=lambda s: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def canonical(labels):
    if not isinstance(labels,list) or not labels or any(type(x) is not int or x<0 for x in labels):
        raise ValueError('partition must be a nonempty integer-label list')
    names={}
    return [names.setdefault(x,len(names)) for x in labels]

def contains(old,new):
    """Old unrestricted equality model contains new iff E(old) subset E(new)."""
    a,b=canonical(old),canonical(new)
    if len(a)!=len(b): raise ValueError('partition lengths differ')
    return all(a[i]!=a[j] or b[i]==b[j] for i in range(len(a)) for j in range(i))

def checked_bytes(root,path,digest):
    blob=(Path(root)/path).read_bytes()
    if hashlib.sha256(blob).hexdigest()!=digest: raise ValueError('hash mismatch: '+path)
    return blob

def build_index(root):
    receipt=load_json(checked_bytes(root,RECEIPT,RECEIPT_HASH))
    for path,digest in DEPENDENCIES.items(): checked_bytes(root,path,digest)
    if receipt['source_sha256']!=DEPENDENCIES or receipt['id']!='MINIMUM-REPAIR-044' or not receipt['finished_at_utc']:
        raise ValueError('unsupported receipt provenance/completion')
    if len(receipt['rows'])!=1536 or receipt['descriptions']!=1536:
        raise ValueError('incomplete receipt')
    records=[]
    for period in range(1,97):
        matches=[(i,r) for i,r in enumerate(receipt['rows']) if all(r.get(k)==v for k,v in
            dict(mode='periodic',alphabet='AZ',q=26,sigma=1,tau=1,lag_or_period=period).items())]
        if len(matches)!=1: raise ValueError('missing/duplicate selected row')
        i,row=matches[0]; minimum=row['minimum_substitutions']
        if type(minimum) is not int or minimum<0: raise ValueError('invalid minimum')
        eligible=minimum>0
        records.append({'id':f'044-AZ-ADD-P{period:02}', 'period':period,
          'receipt_pointer':f'/rows/{i}', 'minimum_substitutions':minimum,
          'status':'completed_exact_negative' if eligible else 'ineligible',
          'reason':'retained exact minimum > 0' if eligible else 'zero minimum: compatible/underconstrained, not negative',
          'key_domain':'unrestricted_mod_q',
          'partition':canonical([x%period for x in CONTEXT['coordinates']])})
    return {'schema_version':1,'context':CONTEXT,'receipt':{'path':RECEIPT,'sha256':RECEIPT_HASH},
      'dependencies':DEPENDENCIES,'records':records,
      'not_indexed':[{'scope':'phase/reset and other equations/alphabets', 'status':'ineligible',
                     'reason':'not independently extracted/reviewed in this bounded initial index'},
                    {'scope':'external skipped/heuristic/unknown/incomplete results','status':'ineligible',
                     'reason':'no source-complete completed negative admitted'}]}

def check_request(index,request):
    # Strict wire shape avoids accepted extra claims, bool/int equivalence and altered context.
    if set(request)!={'context','partition','domain'}: raise ValueError('unsupported request fields')
    if json.dumps(request['context'],sort_keys=True)!=json.dumps(index['context'],sort_keys=True):
        raise ValueError('context mismatch: equation/alphabet/data/normalization/alignment/coordinates')
    part=canonical(request['partition'])
    if len(part)!=len(index['context']['coordinates']): raise ValueError('missing/extra partition rows')
    domain=request['domain']; q=index['context']['q']
    if domain=={'kind':'unrestricted_mod_q'}: pass
    elif isinstance(domain,dict) and set(domain)=={'kind','allowed_values'} and domain['kind']=='per_class_values':
        values=domain['allowed_values']
        if not isinstance(values,list) or len(values)!=len(set(part)): raise ValueError('domain class count mismatch')
        for group in values:
            if not isinstance(group,list) or not group or len(set(group))!=len(group) or any(type(v) is not int or not 0<=v<q for v in group):
                raise ValueError('invalid restricted domain')
    else: raise ValueError('unsupported key domain; no inferred subset claims')
    matches=[]
    for r in index['records']:
        if r['status']!='completed_exact_negative' or r['key_domain']!='unrestricted_mod_q': continue
        if contains(r['partition'],part):
            matches.append({'certificate':r['id'],'receipt_pointer':r['receipt_pointer'],
                'relation':'equal crib partition' if r['partition']==part else 'strict crib-only containment',
                'explanation':'Every equality required by the old unrestricted key model is required by the supplied partition. Any supplied zero-edit crib fit would fit the old model, contradicting its retained positive exact repair minimum.'})
    return {'decision':'inherited_negative' if matches else 'no_certificate',
            'scope':'crib-only negative implication; not full-message/operator equivalence',
            'conditional_on':'human verification that supplied partition is required by the proposed mechanism on every admissible key/plaintext',
            'matches':matches,'new_target_execution':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--index');p.add_argument('--request')
    a=p.parse_args()
    try:
        expected=build_index(a.repo)
        if a.index:
            supplied=load_json(Path(a.index).read_text())
            if json.dumps(supplied,sort_keys=True)!=json.dumps(expected,sort_keys=True): raise ValueError('index differs from pinned-source extraction')
        result=check_request(expected,load_json(Path(a.request).read_text())) if a.request else expected
        print(json.dumps(result,indent=2))
    except (ValueError,KeyError,TypeError,OSError) as e:
        print(json.dumps({'decision':'rejected','reason':str(e)}));return 2
    return 0
if __name__=='__main__': raise SystemExit(main())
