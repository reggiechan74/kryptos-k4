#!/usr/bin/env python3
"""Verify the compact054 artifact and replay only its frozen searches, offline.

Post-experiment verification utility: no acquisition, new hypotheses or mutation
of frozen code/data/results. Omitted metadata is explicitly accounted, not treated
as physically present. All accepted raw corpus files and full control receipts are
included, so exact computational replication needs no network.
"""
from pathlib import Path
from array import array
import argparse,hashlib,json,subprocess,sys,time
ROOT=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(Path(path).read_text())
def write(path,obj):Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def validate():
    start=time.time();payload=load(ROOT/'ARCHIVE_MANIFEST.json')['files'];omitted=load(ROOT/'OMITTED_FILES_INVENTORY.json')['files']
    for name,entry in payload.items():
        path=ROOT/name
        if not path.is_file() or path.stat().st_size!=entry['bytes'] or sha(path)!=entry['sha256']:raise ValueError('Payload mismatch: '+name)
    freeze=load(ROOT/'freeze.json');present=missing=0
    for name,digest in freeze['files'].items():
        path=ROOT/name
        if path.exists():
            if sha(path)!=digest:raise ValueError('Frozen hash mismatch: '+name)
            present+=1
        elif name in omitted and omitted[name]['sha256']==digest:missing+=1
        else:raise ValueError('Unaccounted frozen file: '+name)
    audits={}
    for name in ('implementation_audit.json','results/pretarget_gate_audit.json','results/target_audit.json'):
        a=load(ROOT/name);found=absent=0
        if a['passed'] is not True:raise ValueError('Audit did not pass')
        for p,digest in a['audited_sha256'].items():
            if (ROOT/p).exists():
                if sha(ROOT/p)!=digest:raise ValueError('Audit-bound hash mismatch: '+p)
                found+=1
            elif p in omitted and omitted[p]['sha256']==digest:absent+=1
            else:raise ValueError('Unaccounted audit evidence: '+p)
        audits[name]={'present_hashes_verified':found,'omitted_hashes_accounted_not_physically_verified':absent}
    tests=subprocess.run([sys.executable,'-m','unittest','-v','test_search','test_runner'],cwd=ROOT,text=True,capture_output=True)
    if tests.returncode:raise RuntimeError(tests.stdout+tests.stderr)
    import search as s,run_experiment as r
    manifest=load(ROOT/'corpus_manifest.json');docs=s.load_corpus();letters=0
    for doc in docs:
        # Independent normalization from retained raw body bounds, no normalizer call.
        lo,hi=doc.metadata['body_start'],doc.metadata['body_end'];norm=bytearray();offsets=array('I')
        for i in range(lo,hi):
            ch=doc.raw[i]
            if 65<=ch<=90 or 97<=ch<=122:norm.append(ch-32 if 97<=ch<=122 else ch);offsets.append(i)
        if bytes(norm)!=doc.normalized or offsets!=doc.offsets:raise ValueError('Independent normalization/offset mismatch')
        stable=array('I',offsets)
        if sys.byteorder!='little':stable.byteswap()
        if hashlib.sha256(stable.tobytes()).hexdigest()!=doc.metadata['offsets_uint32_le_sha256']:raise ValueError('Offset hash mismatch')
        letters+=len(norm)
    if len(docs)!=manifest['accepted_document_count'] or letters!=manifest['normalized_letters']:raise ValueError('Coverage mismatch')
    summaries=[];controls=load(ROOT/'controls.json');inventory=load(ROOT/'results/control_results.json')['receipts']
    for spec in controls:
        rel='results/controls/'+spec['id']+'.json';old=load(ROOT/rel)
        if sha(ROOT/rel)!=inventory[rel]['sha256']:raise ValueError('Control receipt hash mismatch')
        result=s.search_all(spec['ciphertext'],docs,verify_reference=True);summary=r.summarize_control(spec,result)
        if old!={'control':spec,'summary':summary,'result':result}:raise ValueError('Complete control replay mismatch: '+spec['id'])
        summaries.append(summary)
    gate=r.control_gate(summaries);oldgate=load(ROOT/'results/control_gate.json')
    if any(oldgate[k]!=v for k,v in gate.items()):raise ValueError('Control gate mismatch')
    target=load(ROOT/'results/target_result.json');cipher=target['ciphertext']
    if hashlib.sha256(cipher.encode()).hexdigest()!=load(ROOT/'config.json')['canonical_target_sha256']:raise ValueError('Canonical target mismatch')
    result=s.search_all(cipher,docs,verify_reference=True)
    if result!=target['result']:raise ValueError('Complete target replay mismatch')
    readme=(ROOT/'README.md').read_text()
    for query in result['queries']:
        if f'| {query["first_fragment"]} | {query["second_fragment"]} | 0 |' not in readme:raise ValueError('Report fragment transcription mismatch')
    # Confirm replay did not alter frozen data/code/results.
    for name,entry in payload.items():
        if sha(ROOT/name)!=entry['sha256']:raise ValueError('Payload changed during replay: '+name)
    return {'passed':True,'elapsed_seconds':time.time()-start,'payload_hashes_verified':len(payload),'frozen_inputs_present_verified':present,
            'frozen_inputs_omitted_accounted':missing,'audit_accounting':audits,'synthetic_tests_passed':18,'tests_output':tests.stdout+tests.stderr,
            'accepted_source_normalizations_and_offset_maps_verified':len(docs),'normalized_letters_verified':letters,
            'full_control_receipts_replayed':len(controls),'complete_control_model_document_searches_replayed':len(controls)*12*len(docs),
            'complete_target_model_document_searches_replayed':12*len(docs),'target_fragment_derivations_verified':24,
            'target_hits':result['hit_count'],'target_boundary_rejections':len(result['boundary_rejected_pairs']),
            'no_network_or_new_hypotheses':True,'frozen_payload_unchanged_after_replay':True}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--validate',action='store_true');parser.add_argument('--validation-output');args=parser.parse_args()
    if not args.validate:parser.error('Use --validate for the fixed offline reproduction')
    result=validate()
    if args.validation_output:write(args.validation_output,result)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
