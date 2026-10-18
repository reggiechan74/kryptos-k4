"""Offline replay runner; new run snapshots never overwrite audited artifacts."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import platform
import time
from bounded_models import ROOT, synthetic_controls, route_scan, running_scan, trifid_scan, deadline_check
from check_baseline import validate
from check_controls import run as check_controls
from run_io import RunSnapshot, specification, json_bytes

BASELINE_SHA='eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab'


def validated_baseline(path):
    data=json.loads(Path(path).read_text());text=validate(data)
    if hashlib.sha256(text.encode('ascii')).hexdigest()!=BASELINE_SHA:
        raise ValueError('ciphertext differs from verified baseline')
    return data


def arguments(description):
    parser=argparse.ArgumentParser(description=description)
    parser.add_argument('--spec-commit',required=True,help='Full SHA committed before execution; history verification is external')
    parser.add_argument('--spec-file',default='research/BOUNDED-SPEC.md')
    parser.add_argument('--output-dir',default='results/runs')
    parser.add_argument('--write-results',action='store_true',help='Compatibility flag; snapshots are always written')
    return parser.parse_args()


def payload(snapshot,name,result,hashes,started,command):
    result['run_metadata']={'run_id':snapshot.run_id,'status':'completed','python':platform.python_version(),
        'command':command,'elapsed_seconds':round(time.monotonic()-started,3),'file_sha256':hashes,
        'specification':snapshot.manifest['specification']}
    encoded=(json.dumps(result,separators=(',',':'))+'\n').encode()
    if name in ['ROUTE-001','STAT-001']:
        snapshot.write(name+'.json.gz',gzip.compress(encoded,mtime=0))
        hidden=['route_catalogue','survivors'] if name=='ROUTE-001' else ['raw_draws','evaluation_maxima_z']
        summary={k:v for k,v in result.items() if k not in hidden}
        if name=='ROUTE-001':
            summary['compatible_periods']=sorted({r['period'] for r in result['survivors']})
            summary['vacuous_fits']=sum(r['vacuous_fit'] for r in result['survivors'])
            summary['repeated_phase_comparisons_among_survivors']=sum(r['repeated_phase_comparisons'] for r in result['survivors'])
        summary.update({'detail_artifact':name+'.json.gz','detail_uncompressed_sha256':hashlib.sha256(encoded).hexdigest()})
        snapshot.write(name+'-summary.json',json_bytes(summary))
    else:snapshot.write(name+'.json',encoded)


def execute(root,label,spec,tasks,hashes,command,validate_inputs):
    with RunSnapshot(root,label,spec) as snapshot:
        validate_inputs()
        for name,action,limit in tasks:
            job={'experiment':name,'status':'running','deadline_seconds':limit};snapshot.manifest['jobs'].append(job)
            started=time.monotonic()
            try:
                deadline_check(started,limit)
                result=action(limit)
                deadline_check(started,limit)
                payload(snapshot,name,result,hashes,started,command)
                deadline_check(started,limit)  # includes serialization and staged writes
                job['status']='completed'
                snapshot.final_check=lambda started=started,limit=limit:deadline_check(started,limit)
            except BaseException:
                job['status']='incomplete'
                raise
        return snapshot.run_id


def inputs_hashes(names):return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}


def main():
    args=arguments('Replay fixed bounded cases into a new atomic run snapshot')
    spec=specification(args.spec_commit,args.spec_file)
    data_holder={}
    def validate_inputs():
        data_holder['data']=validated_baseline(ROOT/'data/k4.json')
        check_controls()
        data_holder['controls']=json.loads((ROOT/'data/controls.json').read_text())
        data_holder['synthetic']=synthetic_controls()
    names=['data/k4.json','data/controls.json','experiments/run_bounded.py','experiments/run_io.py','experiments/bounded_models.py','experiments/ciphers.py','experiments/structural_checks.py','experiments/check_baseline.py']
    tasks=[('ROUTE-001',lambda limit:route_scan(data_holder['data'],limit),30),
           ('RUNKEY-001',lambda limit:running_scan(data_holder['data'],data_holder['controls'],limit),30),
           ('TRIFID-001',lambda limit:trifid_scan(data_holder['data'],limit),5)]
    run_id=execute(args.output_dir,'bounded-replay',spec,tasks,inputs_hashes(names),'python3 experiments/run_bounded.py --spec-commit '+args.spec_commit,validate_inputs)
    print('completed run',run_id)


def statistics_main():
    from statistical_diagnostics import run
    args=arguments('Replay fixed diagnostic into a new atomic run snapshot')
    spec=specification(args.spec_commit,args.spec_file)
    names=['data/k4.json','experiments/statistical_diagnostics.py','experiments/run_bounded.py','experiments/run_io.py']
    run_id=execute(args.output_dir,'statistics-replay',spec,[('STAT-001',lambda limit:run(limit=limit),60)],inputs_hashes(names),'python3 experiments/statistical_diagnostics.py --write-results --spec-commit '+args.spec_commit,lambda:validated_baseline(ROOT/'data/k4.json'))
    print('completed run',run_id)


if __name__=='__main__':main()
