#!/usr/bin/env python3
"""Independent prefix/last-occurrence decoder, with no generator import."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KRYPTOS = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
ALPHABETS = {'AZ': AZ, 'KRYPTOS': KRYPTOS}
CRIBS = {**dict(zip(range(22, 35), 'EASTNORTHEAST')), **dict(zip(range(64, 75), 'BERLINCLOCK'))}
assert len('EASTNORTHEAST') == 13 and len('BERLINCLOCK') == 11 and len(CRIBS) == 24

def ordered_prefix(prefix, initial):
    """MTF state theorem: seen symbols in most-recent-use order, then unseen."""
    seen = set(prefix)
    recent = sorted(seen, key=prefix.rindex, reverse=True)
    return ''.join(recent) + ''.join(ch for ch in initial if ch not in seen)

def recover(ciphertext, reference, initial, with_trace=False):
    plaintext, trace = [], []
    for i, observed in enumerate(ciphertext):
        state = ordered_prefix(ciphertext[:i], initial)
        # Explicit ordinal count is separate from the generator's list lookup/update.
        rank = sum(1 for ch in state[:state.find(observed)])
        predicted = reference[rank]
        plaintext.append(predicted)
        if with_trace:
            trace.append({'position_1based': i+1, 'ciphertext': observed, 'state_before': state,
                          'rank_0based': rank, 'plaintext': predicted,
                          'known_plaintext': CRIBS.get(i+1),
                          'known_match': predicted == CRIBS[i+1] if i+1 in CRIBS else None,
                          'state_after': ordered_prefix(ciphertext[:i+1], initial)})
    return ''.join(plaintext), trace

def predict(ciphertext):
    output = []
    for r_name, reference in ALPHABETS.items():
        for s_name, initial in ALPHABETS.items():
            plaintext, _ = recover(ciphertext, reference, initial)
            matches = [i for i, expected in CRIBS.items() if plaintext[i-1] == expected]
            output.append({'model': f'R={r_name},S0={s_name}', 'matched': len(matches),
                           'total_known': len(CRIBS), 'accepted': len(matches) == len(CRIBS),
                           'plaintext': plaintext})
    return output

if __name__ == '__main__':
    cases = json.loads((HERE / 'blind_cases.json').read_text())
    # Never read sealed_truth.json here. Write all predictions before grading.
    predictions = [{'id': case['id'], 'models': predict(case['ciphertext'])} for case in cases]
    (HERE / 'blind_predictions.json').write_text(json.dumps(predictions, indent=2) + '\n')
    print(f'Independent selector wrote predictions for {len(predictions)} unlabeled cases.')
