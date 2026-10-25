"""054 audited stage gates. No network, target constant, language scorer or p-values."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,time,sys,platform
import search as s
ROOT=Path(__file__).resolve().parent
CODE_FILES=('PROTOCOL.md','CORPUS_PLAN.json','BASELINE_048.json','config.json','search.py','prepare_corpus.py','run_experiment.py',
            'test_search.py','test_runner.py','control_plaintext.json','corpus_manifest.json','controls.json')

def required_files(root=ROOT):
    names=set(CODE_FILES)
    names.update(str(f.relative_to(root)) for f in (root/'data').rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix not in ('.pyc','.pyo'))
    return sorted(names)

def verify_audit(audit,root=ROOT,names=None):
    if audit.get('passed') is not True or not isinstance(audit.get('audited_sha256'),dict):raise ValueError('Passed independent hash-bound audit required')
    mapping=audit['audited_sha256']
    for name in names if names is not None else required_files(root):
        if name not in mapping or s.sha_file(root/name)!=mapping[name]:raise ValueError('Missing/changed audited input: '+name)
    for name,digest in mapping.items():
        if s.sha_file(root/name)!=digest:raise ValueError('Changed audit evidence: '+name)

def freeze_sources():
    if (ROOT/'freeze.json').exists():raise ValueError('Freeze exists; no overwrite')
    audit=s.read_json(ROOT/'implementation_audit.json');verify_audit(audit)
    if audit.get('target_lookup_authorized') is not False:raise ValueError('Implementation audit must be control-stage only')
    manifest=s.read_json(ROOT/'corpus_manifest.json');docs=s.load_corpus()
    if len(docs)!=manifest['accepted_document_count']:raise ValueError('Corpus count disagreement')
    paths=required_files()+['implementation_audit.json']
    freeze={'version':'candidate-first-054-v1','utc':datetime.now(timezone.utc).isoformat(),'status':'Frozen before full-corpus controls and canonical target fragment derivation/lookup',
            'files':{p:s.sha_file(ROOT/p) for p in paths},'environment':{'python':sys.version,'platform':platform.platform()},
            'document_count':len(docs),'normalized_letters':manifest['normalized_letters'],'target_lookup_performed':False}
    s.write_json(ROOT/'freeze.json',freeze);return freeze

def verify_freeze():
    data=s.read_json(ROOT/'freeze.json')
    for name,digest in data['files'].items():
        if s.sha_file(ROOT/name)!=digest:raise ValueError('Frozen input changed: '+name)
    return s.sha_file(ROOT/'freeze.json')

def summarize_control(spec,result):
    coverage=result['coverage']
    integrity=(result['full_reference_hit_set_checked'] and len(coverage)==12*result['document_count'] and
               sum(r['valid_hit_count'] for r in coverage)==result['hit_count'] and
               all(all(h['checks'].values()) for h in result['hits']))
    planted=[]
    if spec['kind']=='planted_positive':
        planted=[h for h in result['hits'] if h['tableau_id']==spec['tableau_id'] and h['document_id']==spec['source_document_id'] and h['window_start']==spec['source_window_start']]
        success=len(planted)==1 and planted[0]['key']==spec['key'] and planted[0]['plaintext']==spec['plaintext'] and integrity
    else:success=result['hit_count']==0 and integrity
    return {'id':spec['id'],'kind':spec['kind'],'planted_tableau_id':spec['tableau_id'],'boundary_case':spec.get('boundary_case'),
            'source_collection':spec.get('source_collection'),'source_document_id':spec.get('source_document_id'),'source_window_start':spec.get('source_window_start'),
            'hit_count':result['hit_count'],'additional_hits_beyond_planted':result['hit_count']-len(planted),
            'planted_hit_recovered':len(planted)==1,'planted_full_key_plaintext_exact':len(planted)==1 and planted[0]['key']==spec['key'] and planted[0]['plaintext']==spec['plaintext'],
            'reference_and_crypto_integrity_passed':integrity,'passed':bool(success)}

def control_gate(rows):
    positive=[r for r in rows if r['kind']=='planted_positive'];negative=[r for r in rows if r['kind']=='random_absent']
    counts={t.id:sum(r['passed'] for r in positive if r['planted_tableau_id']==t.id) for t in s.TABLEAUX}
    checks={'complete48controls':len(rows)==48 and len(positive)==36 and len(negative)==12,
            'all36planted_hits_exact':len(positive)==36 and all(r['passed'] for r in positive),
            'three_per_tableau':all(n==3 for n in counts.values()),
            'all12absent_controls_zero':len(negative)==12 and all(r['passed'] for r in negative),
            'all_reference_and_crypto_checks':all(r['reference_and_crypto_integrity_passed'] for r in rows)}
    return {'passed':all(checks.values()),'checks':checks,'positive_passed':sum(r['passed'] for r in positive),'positive_total':len(positive),
            'negative_passed':sum(r['passed'] for r in negative),'negative_total':len(negative),'positive_passes_by_tableau':counts,
            'all_positive_hit_count':sum(r['hit_count'] for r in positive),'all_negative_hit_count':sum(r['hit_count'] for r in negative),
            'interpretation':'Implementation/data correctness controls, not a calibrated K4 chance probability or independent language sample.'}

def run_controls():
    freeze_hash=verify_freeze();out=ROOT/'results';out.mkdir(exist_ok=True);folder=out/'controls';folder.mkdir(exist_ok=True)
    if (out/'control_results.json').exists() or any(folder.glob('*.json')):raise ValueError('Existing control outputs; no overwrite')
    docs=s.load_corpus();specs=s.read_json(ROOT/'controls.json');rows=[];inventory={};start=time.time()
    for spec in specs:
        result=s.search_all(spec['ciphertext'],docs,verify_reference=True);summary=summarize_control(spec,result)
        receipt={'control':spec,'summary':summary,'result':result};path=folder/(spec['id']+'.json');s.write_json(path,receipt)
        rows.append(summary);inventory[str(path.relative_to(ROOT))]={'sha256':s.sha_file(path),'bytes':path.stat().st_size}
        print(json.dumps({'completed':len(rows),'of':len(specs),'id':spec['id'],'elapsed_seconds':time.time()-start}),flush=True)
    verify_freeze();data={'freeze_sha256':freeze_hash,'elapsed_seconds':time.time()-start,'controls':rows,'receipts':inventory,
                         'document_count':len(docs),'normalized_letters':sum(len(d.normalized) for d in docs)}
    s.write_json(out/'control_results.json',data);gate=control_gate(rows);gate.update({'freeze_sha256':freeze_hash,'control_results_sha256':s.sha_file(out/'control_results.json')})
    s.write_json(out/'control_gate.json',gate);return gate

def require_target_gate():
    freeze_hash=verify_freeze();gate=s.read_json(ROOT/'results/control_gate.json');audit=s.read_json(ROOT/'results/pretarget_gate_audit.json')
    if gate.get('passed') is not True or gate.get('freeze_sha256')!=freeze_hash:raise ValueError('Control gate failed/stale')
    verify_audit(audit,names=['freeze.json','results/control_results.json','results/control_gate.json'])
    if s.sha_file(ROOT/'results/control_results.json')!=gate['control_results_sha256']:raise ValueError('Control summary changed')
    return freeze_hash

def run_target(ciphertext):
    freeze_hash=require_target_gate();s.valid_text(ciphertext);config=s.read_json(ROOT/'config.json')
    digest=hashlib.sha256(ciphertext.encode()).hexdigest()
    if digest!=config['canonical_target_sha256']:raise ValueError('Wrong canonical97letter target hash')
    path=ROOT/'results/target_result.json'
    if path.exists():raise ValueError('Target already queried; no overwrite')
    start=time.time();docs=s.load_corpus();result=s.search_all(ciphertext,docs,verify_reference=True);verify_freeze()
    receipt={'freeze_sha256':freeze_hash,'pretarget_gate_audit_sha256':s.sha_file(ROOT/'results/pretarget_gate_audit.json'),
             'ciphertext':ciphertext,'ciphertext_sha256':digest,'elapsed_seconds':time.time()-start,'result':result,
             'corpus_manifest_sha256':s.sha_file(ROOT/'corpus_manifest.json'),'statistical_p_value':None,
             'stop_rule_reached':True,'interpretation':'Exact deterministic coverage only. Zero hits excludes these frozen normalized passages/conventions; a hit still needs independent historical wording/plaintext verification.'}
    s.write_json(path,receipt);return {'hit_count':result['hit_count'],'boundary_rejections':len(result['boundary_rejected_pairs']),'documents':len(docs),
                                    'model_document_searches':len(result['coverage']),'elapsed_seconds':receipt['elapsed_seconds'],'statistical_p_value':None,'stop_rule_reached':True}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['freeze','verify-freeze','controls','target']);parser.add_argument('--ciphertext');args=parser.parse_args()
    if args.stage=='target' and args.ciphertext is None:parser.error('Explicit authorized canonical target input required')
    result={'freeze':freeze_sources,'verify-freeze':verify_freeze,'controls':run_controls,'target':lambda:run_target(args.ciphertext)}[args.stage]()
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
