#!/usr/bin/env python3
"""One direct mutable-state generator; does not perform recovery or K4 scoring."""
import hashlib
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = json.loads((HERE / 'PROTOCOL.json').read_text())
ALPHABETS = {name: P[name] for name in ('AZ', 'KRYPTOS')}
SEED = P['seed']

def digest(text):
    return hashlib.sha256(text.encode('ascii')).hexdigest()

def encrypt(plaintext, reference, initial, move_to_back=False):
    state = list(initial)
    output = []
    for symbol in plaintext:
        cipher = state[reference.index(symbol)]
        output.append(cipher)
        state.remove(cipher)
        if move_to_back:
            state.append(cipher)
        else:
            state.insert(0, cipher)
    return ''.join(output)

def build():
    cases, truth = [], {}
    for r_name, reference in ALPHABETS.items():
        for s_name, initial in ALPHABETS.items():
            model = f'R={r_name},S0={s_name}'
            for rep in range(8):
                text = [P['AZ'][int(digest(f'{SEED}|{model}|{rep}|{i}'), 16) % 26] for i in range(97)]
                for start, crib in P['cribs_1based'].items():
                    k = int(start) - 1
                    text[k:k+len(crib)] = crib
                text = ''.join(text)
                for start, crib in P['cribs_1based'].items():
                    assert text[int(start)-1:int(start)-1+len(crib)] == crib
                ct = encrypt(text, reference, initial)
                def add(label, ciphertext, kind, expected=None, parent_id=None):
                    case_id = digest(f'{SEED}|opaque|{label}')[:24]
                    cases.append({'id': case_id, 'ciphertext': ciphertext})
                    truth[case_id] = {'kind': kind, 'model': expected, 'plaintext': text if kind != 'histogram_decoy' else None, 'parent_id': parent_id}
                    return case_id
                pos_id = add(f'positive|{model}|{rep}', ct, 'positive', model)
                add(f'move_to_back|{model}|{rep}', encrypt(text, reference, initial, True), 'move_to_back', model)
                for decoy in range(4):
                    chars = list(ct)
                    rng = random.Random(int(digest(f'{SEED}|shuffle|{model}|{rep}|{decoy}'), 16))
                    rng.shuffle(chars)
                    shuffled = ''.join(chars)
                    assert sorted(shuffled) == sorted(ct)
                    add(f'decoy|{model}|{rep}|{decoy}', shuffled, 'histogram_decoy', parent_id=pos_id)
    cases.sort(key=lambda row: row['id'])
    assert len(cases) == 192 and len(truth) == 192
    (HERE / 'blind_cases.json').write_text(json.dumps(cases, indent=2) + '\n')
    (HERE / 'sealed_truth.json').write_text(json.dumps(truth, indent=2, sort_keys=True) + '\n')
    print('Generated 192 opaque-ID controls: 32 positive, 32 move-to-back, 128 histogram decoys.')

if __name__ == '__main__':
    build()
