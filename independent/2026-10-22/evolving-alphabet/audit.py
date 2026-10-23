#!/usr/bin/env python3
"""Grade already-written blinded predictions; verify primitive; finally score K4."""
import collections
import csv
import hashlib
import itertools
import json
import platform
from pathlib import Path
from generate_controls import encrypt
from blind_selector import ALPHABETS, AZ, CRIBS, ordered_prefix, recover

HERE = Path(__file__).resolve().parent

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def check_state(state):
    assert len(state) == 26 and sorted(state) == list(AZ)

def forward_trace(plaintext, reference, initial):
    state, ciphertext, trace = list(initial), [], []
    for i, symbol in enumerate(plaintext):
        check_state(state)
        before = ''.join(state)
        rank = reference.index(symbol)
        selected = state[rank]
        ciphertext.append(selected)
        state.pop(rank)
        state.insert(0, selected)
        after = ''.join(state)
        assert after[0] == selected
        assert after[1:] == ''.join(c for c in before if c != selected)
        check_state(state)
        trace.append({'position_1based': i+1, 'state_before': before, 'state_after': after,
                      'rank_0based': rank, 'ciphertext': selected, 'plaintext': symbol})
    return ''.join(ciphertext), trace

def independent_forward(plaintext, reference, initial):
    # Maintains no mutable permutation: derives every state from generated CT prefix.
    output = ''
    for symbol in plaintext:
        output += ordered_prefix(output, initial)[reference.index(symbol)]
    return output

def grade_controls():
    predictions_path = HERE / 'blind_predictions.json'
    # Run after selector completed, then unseal truth.
    predictions = json.loads(predictions_path.read_text())
    truth = json.loads((HERE / 'sealed_truth.json').read_text())
    public = {row['id']: row['ciphertext'] for row in json.loads((HERE / 'blind_cases.json').read_text())}
    summary = {'positive_count': 0, 'positive_true_model_included': 0,
               'positive_full_plaintext_recovered': 0, 'positive_unique_correct': 0,
               'positive_ambiguous': 0, 'positive_wrong_unique': 0, 'positive_truth_omitted': 0,
               'move_to_back_count': 0, 'move_to_back_any_acceptance': 0,
               'histogram_decoy_count': 0, 'histogram_decoy_any_acceptance': 0,
               'accepted_model_counts': {}, 'positive_details': [], 'negative_acceptances': []}
    for case in predictions:
        t = truth[case['id']]
        accepted = [p for p in case['models'] if p['accepted']]
        # Exact roundtrip is checked for every candidate, not just selected models.
        for p in case['models']:
            r_name, s_name = [value.split('=')[1] for value in p['model'].split(',')]
            reference, initial = ALPHABETS[r_name], ALPHABETS[s_name]
            assert encrypt(p['plaintext'], reference, initial) == public[case['id']]
            assert independent_forward(p['plaintext'], reference, initial) == public[case['id']]
        if t['kind'] == 'positive':
            summary['positive_count'] += 1
            included = any(p['model'] == t['model'] for p in accepted)
            recovered = any(p['model'] == t['model'] and p['plaintext'] == t['plaintext'] for p in accepted)
            summary['positive_true_model_included'] += included
            summary['positive_full_plaintext_recovered'] += recovered
            summary['positive_unique_correct'] += len(accepted) == 1 and included
            summary['positive_ambiguous'] += len(accepted) > 1
            summary['positive_wrong_unique'] += len(accepted) == 1 and not included
            summary['positive_truth_omitted'] += not included
            for start, crib in ((22, 'EASTNORTHEAST'), (64, 'BERLINCLOCK')):
                assert t['plaintext'][start-1:start-1+len(crib)] == crib
            summary['positive_details'].append({'id': case['id'], 'planted_model': t['model'],
                'accepted_models': [p['model'] for p in accepted], 'full_truth_recovered': recovered})
        else:
            summary[t['kind'] + '_count'] += 1
            summary[t['kind'] + '_any_acceptance'] += bool(accepted)
            if accepted:
                summary['negative_acceptances'].append({'id': case['id'], 'kind': t['kind'], 'accepted_models': [p['model'] for p in accepted]})
            if t['kind'] == 'histogram_decoy':
                assert collections.Counter(public[case['id']]) == collections.Counter(public[t['parent_id']])
    assert summary['positive_true_model_included'] == 32
    assert summary['positive_full_plaintext_recovered'] == 32
    assert summary['positive_wrong_unique'] == 0
    dump('controls_summary.json', summary)
    return summary

def primitive_checks():
    one_step, exhaustive, full_checks = [], 0, 0
    for r_name, reference in ALPHABETS.items():
        for s_name, initial in ALPHABETS.items():
            model = f'R={r_name},S0={s_name}'
            for p in AZ:
                c = encrypt(p, reference, initial)
                restored, trace = recover(c, reference, initial, True)
                assert restored == p and c == initial[reference.index(p)]
                after = c + ''.join(ch for ch in initial if ch != c)
                assert trace[0]['state_after'] == after
                check_state(after)
                one_step.append({'model': model, 'plaintext': p, 'ciphertext': c, 'state_after': after})
            for c in AZ:
                p, _ = recover(c, reference, initial)
                assert encrypt(p, reference, initial) == c
            for n in range(4):
                for chars in itertools.product(AZ, repeat=n):
                    text = ''.join(chars)
                    ct = encrypt(text, reference, initial)
                    pt, _ = recover(ct, reference, initial)
                    assert pt == text
                    # Check arbitrary ciphertext inversion too, not just generated input.
                    restored, _ = recover(text, reference, initial)
                    assert encrypt(restored, reference, initial) == text
                    exhaustive += 1
            for rep in range(8):
                text = ''.join(AZ[int(hashlib.sha256(f'full-inverse-independent|{rep}|{i}'.encode()).hexdigest(), 16) % 26] for i in range(97))
                ct, ftrace = forward_trace(text, reference, initial)
                restored, dtrace = recover(ct, reference, initial, True)
                assert restored == text and independent_forward(text, reference, initial) == ct
                for f, d in zip(ftrace, dtrace):
                    for field in ('position_1based', 'state_before', 'state_after', 'rank_0based', 'ciphertext', 'plaintext'):
                        assert f[field] == d[field]
                    check_state(d['state_before'])
                    check_state(d['state_after'])
                full_checks += 1
    dump('one_step_cases.json', one_step)
    # A fixed cyclic alphabet retains its oriented cyclic neighbor relation.
    original = AZ
    mtf = 'D' + ''.join(ch for ch in original if ch != 'D')
    rotation = original[3:] + original[:3]
    def edges(s):
        return {(s[i], s[(i+1) % len(s)]) for i in range(len(s))}
    assert mtf != rotation and edges(mtf) != edges(original)
    assert all(mtf != original[k:] + original[:k] for k in range(26))
    summary = {'one_step_plaintext_cases': len(one_step), 'one_step_ciphertext_cases': 104,
               'exhaustive_strings_lengths_0_through_3': exhaustive,
               'exhaustive_inverse_directions_per_string': 2,
               'full_length_97_independent_roundtrips': full_checks,
               'full_trace_comparison_states': full_checks * 97,
               'all_passed': True,
               'non_rotation_witness': {'before': original, 'move_to_front_D': mtf,
                   'rotation_starting_D': rotation, 'removed_cyclic_edges': sorted(edges(original) - edges(mtf)),
                   'added_cyclic_edges': sorted(edges(mtf) - edges(original)),
                   'claim_limit': 'Not mere cyclic stepping over a fixed alphabet. No global novelty or arbitrary state-machine inequivalence claim.'}}
    dump('primitive_summary.json', summary)
    return summary

def score_k4():
    # K4 is first opened/scored here, after control grading and primitive tests.
    ciphertext = 'OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR'
    assert len(ciphertext) == 97 and len(CRIBS) == 24
    assert ''.join(CRIBS[i] for i in range(22, 35)) == 'EASTNORTHEAST'
    assert ''.join(CRIBS[i] for i in range(64, 75)) == 'BERLINCLOCK'
    results, traces = [], []
    for r_name, reference in ALPHABETS.items():
        for s_name, initial in ALPHABETS.items():
            model = f'R={r_name},S0={s_name}'
            plaintext, trace = recover(ciphertext, reference, initial, True)
            regen, ftrace = forward_trace(plaintext, reference, initial)
            assert regen == ciphertext and encrypt(plaintext, reference, initial) == ciphertext
            assert independent_forward(plaintext, reference, initial) == ciphertext
            for f, d in zip(ftrace, trace):
                for field in ('position_1based', 'state_before', 'state_after', 'rank_0based', 'ciphertext', 'plaintext'):
                    assert f[field] == d[field]
                check_state(d['state_before'])
                check_state(d['state_after'])
                assert d['state_after'][0] == d['ciphertext']
                assert d['state_after'][1:] == ''.join(ch for ch in d['state_before'] if ch != d['ciphertext'])
                traces.append({'model': model, **d})
            known = [row for row in trace if row['known_plaintext'] is not None]
            first = next((row for row in known if not row['known_match']), None)
            matched = [row['position_1based'] for row in known if row['known_match']]
            results.append({'model': model, 'matched_known': len(matched), 'total_known': 24,
                'matched_positions_1based': matched, 'first_contradiction': first,
                'crib_window_22_34': plaintext[21:34], 'crib_window_64_74': plaintext[63:74],
                'full_plaintext': plaintext, 'regenerated_exactly_97': regen == ciphertext,
                'status': 'rejected_exact_crib_contradiction' if first else 'survivor_requires_null_audit'})
    dump('k4_results.json', {'ciphertext': ciphertext, 'ciphertext_sha256_ascii_no_newline': hashlib.sha256(ciphertext.encode()).hexdigest(), 'models': results})
    dump('k4_full_trace.json', traces)
    with (HERE / 'k4_full_trace.csv').open('w', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=list(traces[0]))
        writer.writeheader()
        writer.writerows(traces)
    return results

if __name__ == '__main__':
    controls = grade_controls()
    print('CONTROLS:', json.dumps({k:v for k,v in controls.items() if k not in ('positive_details', 'negative_acceptances')}, sort_keys=True))
    primitive = primitive_checks()
    print('PRIMITIVE:', json.dumps(primitive, sort_keys=True))
    k4 = score_k4()
    print('K4:', json.dumps(k4, sort_keys=True))
    dump('runtime.json', {'python': platform.python_version(), 'platform': platform.platform()})
