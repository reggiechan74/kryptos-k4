"""Audited, stage-gated053 runner. No network, target ciphertext or model selection."""
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import argparse,hashlib,json,math,platform,time,sys,statistics
import reference as p
import native
ROOT=Path(__file__).resolve().parent
CODE_FILES=('PROTOCOL.md','IMPLEMENTATION_SPEC.md','CONTROL_SOURCE_PLAN.json','prepare_source_plan.py','prepare_data.py','reference.py',
            'native.py','native053.c','native053.so','build.json','run_experiment.py','test_reference.py','test_native.py','test_runner.py',
            'config.json','bank.json','bank_import.json','prior051_bank.json','windows.json','controls.json')

def configuration():
    c=p.load_json(ROOT/'config.json')
    if c['candidate_count']!=1024 or c['tableau_count']!=12 or c['primary_letters']!=73 or c['minimum_score_bits']!=32:raise ValueError('Invalid fixed configuration')
    return c

def required_files(root=ROOT):
    names=set(CODE_FILES)
    for folder in ('data','controls','model','authors'):
        names.update(str(f.relative_to(root)) for f in (root/folder).rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix not in ('.pyc','.pyo'))
    return sorted(names)

def verify_audit_bindings(audit,root=ROOT,names=None):
    if audit.get('passed') is not True or not isinstance(audit.get('audited_sha256'),dict):raise ValueError('Independent passed hash-bound audit required')
    mapping=audit['audited_sha256']
    for name in names if names is not None else required_files(root):
        if name not in mapping or p.sha256_file(root/name)!=mapping[name]:raise ValueError('Missing or changed audited file: '+name)
    # Additional certificate-bound evidence must also be intact.
    for name,digest in mapping.items():
        if p.sha256_file(root/name)!=digest:raise ValueError('Changed audit evidence: '+name)

def freeze_sources():
    if (ROOT/'freeze.json').exists():raise ValueError('Freeze already exists; never overwrite')
    audit=p.load_json(ROOT/'implementation_audit.json');verify_audit_bindings(audit)
    if audit.get('target_scoring_authorized') is not False:raise ValueError('Implementation certificate must be control-stage only')
    bank=p.validate_bank(p.load_json(ROOT/'bank.json'))
    if p.sha256_file(ROOT/'bank.json')!='e929b4c5a93bab76195dd9d16556aa1def8db530a987f9bdf3dc6861c28b11e7':raise ValueError('Bank is not immutable052')
    build=p.load_json(ROOT/'build.json')
    if build['source_sha256']!=p.sha256_file(ROOT/'native053.c') or build['binary_sha256']!=p.sha256_file(ROOT/'native053.so'):raise ValueError('Build mismatch')
    names=required_files()+['implementation_audit.json']
    receipt={'version':configuration()['version'],'utc':datetime.now(timezone.utc).isoformat(),
             'status':'Frozen before all actual-bank controls and K4 scoring','files':{n:p.sha256_file(ROOT/n) for n in names},
             'python':sys.version,'platform':platform.platform(),'candidate_count':len(bank)}
    p.write_json(ROOT/'freeze.json',receipt);return receipt

def verify_freeze():
    f=p.load_json(ROOT/'freeze.json')
    for n,h in f['files'].items():
        if p.sha256_file(ROOT/n)!=h:raise ValueError('Frozen file changed: '+n)
    return p.sha256_file(ROOT/'freeze.json')

def enrich_observed(observed,bank):
    records={r['id']:r for r in bank};best={}
    for row in observed['ranking']:
        if row['candidate_id'] not in best:best[row['candidate_id']]={**records[row['candidate_id']],**row}
    ranked=list(best.values());observed['ranked_candidates']=ranked
    observed['selected_candidate']=records[observed['candidate_id']]
    observed['group_statistics']={}
    for group in sorted({r.get('group','unknown') for r in bank}):
        vals=[r['score_bits'] for r in ranked if r.get('group','unknown')==group]
        observed['group_statistics'][group]={'count':len(vals),'maximum':max(vals),'minimum':min(vals),'mean':statistics.mean(vals),'median':statistics.median(vals)}
    return observed

def tail_p(observed,maxima):return (1+sum(m>=observed for m in maxima))/(len(maxima)+1)
def detection(winner,pvalue,ceiling,alpha=.05):return winner['score_bits']>=32 and pvalue<=alpha and winner['full_key_cross_entropy']<=ceiling

def compact_null(cipher,scorer):
    w=scorer.score(cipher,details=False)
    return {'ciphertext':cipher,'ciphertext_sha256':hashlib.sha256(cipher.encode()).hexdigest(),**w}

def evaluate_control(spec,scorer,ceiling,executor,c):
    observed=enrich_observed(scorer.score(spec['ciphertext'],details=True),scorer.bank)
    cal_c=p.conditional_nulls(spec['ciphertext'],c['calibration_nulls_per_control'],spec['calibration_rng_label'])
    val_c=p.conditional_nulls(spec['ciphertext'],c['validation_nulls_per_control'],spec['validation_rng_label'])
    cal=list(executor.map(lambda x:compact_null(x,scorer),cal_c));val=list(executor.map(lambda x:compact_null(x,scorer),val_c))
    maxima=[r['score_bits'] for r in cal];pv=tail_p(observed['score_bits'],maxima);flag=detection(observed,pv,ceiling,c['control_alpha'])
    for r in val:
        r['conditional_p']=tail_p(r['score_bits'],maxima);r['flagged']=detection(r,r['conditional_p'],ceiling,c['control_alpha'])
    true_plain_top=observed['candidate_id']==spec['plaintext_id'];true_key=observed['key']==spec['key']
    recovered=bool(true_plain_top and observed['unique_top_plaintext'] and true_key and flag and observed['full_reencryption'] and observed['full_inverse'])
    summary={'id':spec['id'],'kind':spec['kind'],'planted_candidate_id':spec['plaintext_id'],'planted_tableau_id':spec['tableau_id'],
             'source_document':spec['source_document'],'observed_score_bits':observed['score_bits'],'conditional_p':pv,'flagged':flag,
             'top_candidate_id':observed['candidate_id'],'top_tableau_id':observed['tableau_id'],'top_key':observed['key'],
             'full_key_cross_entropy':observed['full_key_cross_entropy'],'margin_bits':observed['margin_bits'],
             'unique_top_plaintext':observed['unique_top_plaintext'],'true_plaintext_top':true_plain_top,'exact_key_recovered':true_key,
             'exact_tableau_label_match':observed['tableau_id']==spec['tableau_id'],'successful_recovery':recovered,
             'validation_flags':sum(r['flagged'] for r in val),'validation_count':len(val),
             'all_candidate_model_crypto_passed':all(r['full_reencryption'] and r['full_inverse'] for r in observed['ranking'])}
    return {'control':spec,'summary':summary,'observed':observed,'calibration_nulls':cal,'validation_nulls':val}

def control_gate(rows):
    c=configuration();bykind={k:[r for r in rows if r['kind']==k] for k in ('published_prose','hard_style','novel_prose','uniform_key','letter_permuted','plaintext_absent','word_order_stress')}
    expected={'published_prose':36,'hard_style':24,'novel_prose':12,'uniform_key':24,'letter_permuted':24,'plaintext_absent':12,'word_order_stress':12}
    recovered={k:sum(r['successful_recovery'] for r in v) for k,v in bykind.items()}
    flags={k:sum(r['flagged'] for r in v) for k,v in bykind.items()}
    bytableau={t.id:sum(r['successful_recovery'] for r in bykind['published_prose'] if r['planted_tableau_id']==t.id) for t in p.TABLEAUX}
    checks={'complete_counts':len(rows)==144 and all(len(bykind[k])==v for k,v in expected.items()) and sum(r['validation_count'] for r in rows)==1440,
            'all_crypto_checks':all(r['all_candidate_model_crypto_passed'] for r in rows),
            'published_recovery':recovered['published_prose']>=c['minimum_published_recovery'],
            'published_each_tableau':all(v>=c['minimum_published_per_tableau'] for v in bytableau.values()),
            'novel_recovery':recovered['novel_prose']>=c['minimum_novel_recovery'],
            'hard_recovery':recovered['hard_style']>=c['minimum_hard_recovery'],
            'negative_flags':flags['uniform_key']+flags['letter_permuted']<=c['maximum_negative_flags'],
            'absent_flags':flags['plaintext_absent']<=c['maximum_absent_flags'],
            'validation_flags':sum(r['validation_flags'] for r in rows)<=c['maximum_validation_flags']}
    return {'passed':all(checks.values()),'checks':checks,'counts':{k:len(v) for k,v in bykind.items()},'recoveries':recovered,'flags':flags,
            'published_recoveries_by_tableau':bytableau,'validation_flags':sum(r['validation_flags'] for r in rows),'validation_count':sum(r['validation_count'] for r in rows),
            'dependence_warning':'Fixed bank; related source windows, paired keys and shared matched calibration sets. Counts are not independent universal false-positive trials.',
            'word_order_stress_not_semantic_evidence':True}

def run_controls():
    freeze_hash=verify_freeze();c=configuration();out=ROOT/'results';out.mkdir(exist_ok=True);folder=out/'controls';folder.mkdir(exist_ok=True)
    if (out/'control_results.json').exists() or any(folder.glob('*.json')):raise ValueError('Control results already exist; no overwrite or unregistered retry')
    specs=p.load_json(ROOT/'controls.json');model=p.LanguageModel.load(ROOT/'model/log_tables.bin');scorer=native.NativeScorer(p.load_json(ROOT/'bank.json'),model)
    ceiling=p.load_json(ROOT/'model/training_receipt.json')['full_key_cross_entropy_ceiling'];rows=[];inventory={};start=time.time()
    with ThreadPoolExecutor(max_workers=c['workers']) as executor:
        for spec in specs:
            receipt=evaluate_control(spec,scorer,ceiling,executor,c);path=folder/(spec['id']+'.json');p.write_json(path,receipt)
            rows.append(receipt['summary']);inventory[str(path.relative_to(ROOT))]={'sha256':p.sha256_file(path),'bytes':path.stat().st_size}
            print(json.dumps({'completed':len(rows),'of':len(specs),'id':spec['id'],'kind':spec['kind'],'elapsed_seconds':time.time()-start}),flush=True)
    verify_freeze();summary={'freeze_sha256':freeze_hash,'elapsed_seconds':time.time()-start,'full_key_ceiling':ceiling,'controls':rows,'receipts':inventory,
                             'control_count':len(rows),'null_count':len(rows)*(c['calibration_nulls_per_control']+c['validation_nulls_per_control'])}
    p.write_json(out/'control_results.json',summary);gate=control_gate(rows);gate['control_results_sha256']=p.sha256_file(out/'control_results.json');gate['freeze_sha256']=freeze_hash
    p.write_json(out/'control_gate.json',gate);return gate

def require_target_gate():
    freeze_hash=verify_freeze();gate=p.load_json(ROOT/'results/control_gate.json');audit=p.load_json(ROOT/'results/pretarget_gate_audit.json')
    if gate.get('passed') is not True or gate.get('freeze_sha256')!=freeze_hash:raise ValueError('Pretarget controls failed or stale')
    verify_audit_bindings(audit,names=['freeze.json','results/control_gate.json','results/control_results.json'])
    if gate['control_results_sha256']!=p.sha256_file(ROOT/'results/control_results.json'):raise ValueError('Control summary changed')
    return freeze_hash

def run_target(ciphertext):
    freeze_hash=require_target_gate();c=configuration();p.validate_ciphertext(ciphertext)
    if hashlib.sha256(ciphertext.encode()).hexdigest()!=c['canonical_target_sha256']:raise ValueError('Canonical ciphertext hash mismatch')
    path=ROOT/'results/target_result.json'
    if path.exists():raise ValueError('Target already scored; no overwrite')
    scorer=native.NativeScorer(p.load_json(ROOT/'bank.json'),p.LanguageModel.load(ROOT/'model/log_tables.bin'))
    ceiling=p.load_json(ROOT/'model/training_receipt.json')['full_key_cross_entropy_ceiling'];start=time.time();observed=enrich_observed(scorer.score(ciphertext,details=True),scorer.bank)
    null_c=p.conditional_nulls(ciphertext,c['target_nulls'],'K4|conditional-null')
    with ThreadPoolExecutor(max_workers=c['workers']) as ex:nulls=list(ex.map(lambda x:compact_null(x,scorer),null_c))
    pv=tail_p(observed['score_bits'],[r['score_bits'] for r in nulls])
    checks={'primary_score':observed['score_bits']>=c['minimum_score_bits'],'global_p':pv<=c['target_alpha'],
            'different_plaintext_margin':observed['margin_bits']>=c['target_minimum_margin_bits'],'full_key_ceiling':observed['full_key_cross_entropy']<=ceiling}
    verify_freeze();result={'freeze_sha256':freeze_hash,'pretarget_gate_audit_sha256':p.sha256_file(ROOT/'results/pretarget_gate_audit.json'),
                           'ciphertext':ciphertext,'ciphertext_sha256':hashlib.sha256(ciphertext.encode()).hexdigest(),'elapsed_seconds':time.time()-start,
                           'observed':observed,'nulls':nulls,'global_p':pv,'nulls_greater_or_equal':sum(r['score_bits']>=observed['score_bits'] for r in nulls),
                           'nulls_equal':sum(r['score_bits']==observed['score_bits'] for r in nulls),'gates':checks,'evidence_gate_passed':all(checks.values()),
                           'full_key_ceiling':ceiling,'statistical_scope':'Standalone exploratory053 test; not cumulative051/052/053 error control. Re-encryption is tautological.'}
    p.write_json(path,result);return {k:v for k,v in result.items() if k not in ('observed','nulls')}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['freeze','verify-freeze','controls','target']);parser.add_argument('--ciphertext');args=parser.parse_args()
    if args.stage=='target' and args.ciphertext is None:parser.error('Provide canonical ciphertext explicitly after parent authorization')
    result={'freeze':freeze_sources,'verify-freeze':verify_freeze,'controls':run_controls,'target':lambda:run_target(args.ciphertext)}[args.stage]()
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
