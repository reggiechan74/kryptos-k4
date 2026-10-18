"""73 fixed-tuple difference queries; no alphabet or primer sweep."""
import argparse
from collections import Counter
import hashlib
import json
import time

from bounded_models import deadline_check
from gromark_alphabet import expand, decrypt, encrypt
from gromark_identifiability import checked_maps, check_counterexample, difference
from gromark_identifiability_controls import controls
from run_bounded import ROOT, execute, inputs_hashes, validated_baseline
from run_io import specification
from structural_checks import known_pairs

SPEC = 'research/specifications/GROMARK-IDENTIFIABILITY-001.json'
PRIOR_SPEC = 'research/specifications/GROMARK-ALPHABET-001.json'
POOL = 'data/gromark-identifiability-counterexamples.json'


def context(data, spec, pool):
    raw = (ROOT / spec['reference']['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != spec['reference']['sha256']:
        raise ValueError('immutable reference artifact hash mismatch')
    old = json.loads(raw)
    reference = {k: old['witness'][k] for k in ('plain_alphabet', 'cipher_alphabet')}
    if any(reference[k] != spec['reference'][k] for k in reference):
        raise ValueError('frozen reference alphabet mismatch')
    model = spec['model_frozen']
    stream = expand(model['base'], model['primer'], model['lags'], 97)
    if stream != old['stream']:
        raise ValueError('fixed stream changed')
    known = known_pairs(data)
    edges = [(p, c, stream[i]) for i, c, p in known]
    for witness in [reference] + pool:
        checked_maps(model['alphabet'], edges, witness)
        plain = decrypt(data['ciphertext'], stream, witness['plain_alphabet'], witness['cipher_alphabet'])
        if not all(plain[i] == p for i, _, p in known):
            raise ValueError('reference/pool does not satisfy canonical cribs')
        if encrypt(plain, stream, witness['plain_alphabet'], witness['cipher_alphabet']) != data['ciphertext']:
            raise ValueError('reference/pool does not regenerate ciphertext')
    return reference, stream, known, edges


def audit(data, spec, pool, limit=20):
    started = time.monotonic()
    reference, stream, known, edges = context(data, spec, pool)
    protected = {i for i, _, _ in known}
    positions = [i for i in range(97) if i not in protected]
    assert len(positions) == 73
    alphabet = spec['model_frozen']['alphabet']
    records = []
    for i in positions:
        remaining = limit - (time.monotonic() - started)
        if remaining <= 0:
            records.append({'position_one_based': i + 1, 'classification': 'unresolved',
                            'query_attempted': False, 'reason': 'aggregate_audit_time_cap'})
            continue
        query_started = time.monotonic()
        query_limit = min(spec['resources']['per_query_seconds'], remaining)
        r = difference(alphabet, edges, reference, data['ciphertext'][i], stream[i], pool,
                       max_states=spec['resources']['per_query_search_states'], limit=query_limit)
        if r['classification'] == 'variable':
            witness = r['counterexample']
            assert check_counterexample(alphabet, edges, reference, witness, data['ciphertext'][i], stream[i])
            plain = decrypt(data['ciphertext'], stream, witness['plain_alphabet'], witness['cipher_alphabet'])
            assert all(plain[j] == p for j, _, p in known)
            assert encrypt(plain, stream, witness['plain_alphabet'], witness['cipher_alphabet']) == data['ciphertext']
            r['acceptance'] = {'full_bijections': True, 'all24cribs': True,
                               'target_differs_from_reference': True, 'full97regeneration': True}
        elapsed = time.monotonic() - query_started
        if elapsed > query_limit:
            r = {'classification': 'unresolved', 'reason': 'per_query_verification_time_cap',
                 'search_states': r['search_states'], 'exact_search_invoked': r['exact_search_invoked']}
        records.append({'position_one_based': i + 1, 'query_attempted': True,
                        'query_seconds_limit': query_limit, 'elapsed_seconds': round(elapsed, 6), **r})
    counts = Counter(r['classification'] for r in records)
    return {'experiment': 'GROMARK-IDENTIFIABILITY-001', 'model': spec['model_frozen'],
            'reference_artifact': spec['reference'], 'record_count': 73,
            'queries_attempted': sum(r['query_attempted'] for r in records),
            'classification_counts': {k: counts[k] for k in ('forced', 'variable', 'unresolved')},
            'method_counts': dict(Counter(r.get('method', 'unresolved') for r in records)),
            'exact_CSP_queries_invoked': sum(r.get('exact_search_invoked', False) for r in records),
            'forced_model_conditional_letters': [{'position_one_based': r['position_one_based'],
                'letter': r['model_conditional_letter']} for r in records if r['classification'] == 'forced'],
            'records': records, 'new_K4_primers': 0, 'full_K4_messages_emitted': False,
            'marginal_map_does_not_describe_joint_freedom': True,
            'scope': 'One fixed tuple/full-alphabet model only; forced letters are conditional deductions, not confirmed K4 plaintext.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec-commit', required=True)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--output-dir', default='results/gromark-identifiability-runs')
    args = parser.parse_args()
    if len(args.code_commit) != 40 or any(c not in '0123456789abcdef' for c in args.code_commit):
        raise ValueError('full implementation commit required')
    spec = json.loads((ROOT / SPEC).read_text())
    prior = json.loads((ROOT / PRIOR_SPEC).read_text())
    pool = json.loads((ROOT / POOL).read_text())['witnesses']
    provenance = specification(args.spec_commit, SPEC)
    provenance['implementation_commit'] = args.code_commit
    holder = {}
    def preflight():
        holder['data'] = validated_baseline(ROOT / 'data/k4.json')
    def action(limit):
        started = time.monotonic()
        checked = controls(prior, min(spec['resources']['controls_deadline_seconds'], limit))
        deadline_check(started, limit)
        result = audit(holder['data'], spec, pool,
                       min(spec['resources']['audit_deadline_seconds'], limit - (time.monotonic() - started)))
        result['controls'] = checked
        deadline_check(started, limit)
        return result
    files = [SPEC, PRIOR_SPEC, POOL, spec['reference']['path'], 'data/k4.json',
             'data/gromark-one-survivor.json', 'experiments/gromark_identifiability.py',
             'experiments/gromark_identifiability_controls.py', 'experiments/run_gromark_identifiability.py',
             'experiments/gromark_alphabet.py', 'experiments/run_io.py', 'experiments/run_bounded.py',
             'experiments/bounded_models.py', 'experiments/check_baseline.py', 'experiments/structural_checks.py']
    command = 'python3 experiments/run_gromark_identifiability.py --spec-commit ' + args.spec_commit + ' --code-commit ' + args.code_commit
    run_id = execute(args.output_dir, 'GROMARK-IDENTIFIABILITY-001', provenance,
                     [('GROMARK-IDENTIFIABILITY-001', action, 25)], inputs_hashes(files), command, preflight)
    print('completed GROMARK-IDENTIFIABILITY-001', run_id)


if __name__ == '__main__':
    main()
