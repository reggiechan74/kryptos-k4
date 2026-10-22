"""Shared provenance/atomic publication for the two finite continuation pilots."""
import argparse
import hashlib
from pathlib import Path
import platform
import subprocess
import time

from check_controls import run as check_controls
from run_bounded import validated_baseline, inputs_hashes
from run_io import RunSnapshot, specification, json_bytes

ROOT = Path(__file__).resolve().parents[1]


def deadline_check(deadline):
    if time.monotonic() > deadline:
        raise TimeoutError('registered continuation budget exhausted')


def registered_run(label, spec_path, runner, paths, limit, action):
    parser = argparse.ArgumentParser(description=label)
    parser.add_argument('--spec-commit', required=True)
    args = parser.parse_args()
    spec = specification(args.spec_commit, spec_path)
    code_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    subprocess.run(['git', 'merge-base', '--is-ancestor', args.spec_commit, code_commit], cwd=ROOT, check=True)
    raw = subprocess.check_output(['git', 'show', args.spec_commit + ':' + spec_path], cwd=ROOT)
    if hashlib.sha256(raw).hexdigest() != spec['sha256']:
        raise ValueError('specification differs from declared commit')
    names = list(dict.fromkeys([spec_path, runner, 'experiments/continuation_io.py',
             'data/k4.json', 'data/controls.json', 'experiments/run_io.py',
             'experiments/run_bounded.py', 'experiments/bounded_models.py',
             'experiments/structural_checks.py', 'experiments/check_baseline.py',
             'experiments/check_controls.py', 'experiments/ciphers.py'] + paths))
    for name in names:
        if subprocess.check_output(['git', 'show', code_commit + ':' + name], cwd=ROOT) != (ROOT / name).read_bytes():
            raise ValueError('consulted file not committed: ' + name)
    with RunSnapshot('results/' + label.lower() + '-runs', label, spec) as snapshot:
        started = time.monotonic()
        deadline = started + limit
        snapshot.manifest['jobs'].append(dict(experiment=label, status='running', deadline_seconds=limit))
        data = validated_baseline(ROOT / 'data/k4.json')
        check_controls()
        result = action(data, deadline)
        deadline_check(deadline)
        result.update(id=label, status='completed', spec_commit=args.spec_commit,
                      code_commit=code_commit, command='python3 ' + runner + ' --spec-commit ' + args.spec_commit,
                      python=platform.python_version(), platform=platform.platform(),
                      file_sha256=inputs_hashes(names), elapsed_seconds=time.monotonic() - started,
                      normalization='97 literal uppercase letters; one-based inclusive reported positions; zero-based internal indices')
        snapshot.write(label + '.json', json_bytes(result))
        snapshot.manifest['jobs'][-1]['status'] = 'completed'
        snapshot.final_check = lambda: deadline_check(deadline)
    return snapshot.run_id, result
