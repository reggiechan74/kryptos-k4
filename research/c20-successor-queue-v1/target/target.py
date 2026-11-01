"""Exactly seven C20 decoders. Execute only after a separately pinned one-shot grant."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parent
INPUT_SHA = '08a1a84bd0dddf2449a2c7f67ee770d093ed47f6ad9a795630b77a2c8062f241'
CRIBS = [{'start': 22, 'end': 34, 'plaintext': 'EASTNORTHEAST'},
         {'start': 64, 'end': 74, 'plaintext': 'BERLINCLOCK'}]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def module(name, expected):
    path = ROOT / (name + '.py')
    b = path.read_bytes()
    require(sha(b) == expected, 'module source mismatch')
    m = types.ModuleType(name)
    exec(compile(b, str(path), 'exec', dont_inherit=True, optimize=0), m.__dict__)
    return m


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze-sha256', required=True)
    args = parser.parse_args()
    fb = (ROOT / 'FREEZE.json').read_bytes()
    require(sha(fb) == args.freeze_sha256, 'freeze mismatch')
    f = json.loads(fb)
    for name, pin in f['files'].items():
        require(sha((ROOT / name).read_bytes()) == pin, 'source mismatch')
    require(sha(Path(sys.executable).resolve().read_bytes()) == f['interpreter_sha256'], 'interpreter mismatch')
    ib = Path(f['input_path']).read_bytes()
    require(len(ib) == 308 and sha(ib) == INPUT_SHA == f['input_sha256'], 'input identity')
    data = json.loads(ib)
    require(set(data) == {'ciphertext', 'length', 'indexing', 'cribs'}, 'input schema')
    require(type(data['length']) is int and data['length'] == 97
            and data['indexing'] == 'one-based inclusive' and data['cribs'] == CRIBS, 'input metadata')
    text = data['ciphertext']
    require(type(text) is str and len(text) == 97 and all('A' <= ch <= 'Z' for ch in text), 'ciphertext framing')
    cipher = tuple(ord(ch)-65 for ch in text)
    c20 = module('c20', f['files']['c20.py'])
    ref = module('reference', f['files']['reference.py'])
    records = []
    for phase in range(7):
        plain = c20.decrypt(cipher, phase)
        shifted = tuple((x - (10,17,24,15,19,14,18)[(i+phase) % 7]) % 26 for i,x in enumerate(cipher))
        require(plain == ref.full_reference(shifted), 'independent traversal disagreement')
        require(len(plain) == 97 and c20.encrypt(plain, phase) == cipher, 'full re-encryption mismatch')
        decoded = ''.join(chr(x+65) for x in plain)
        mask = [decoded[c['start']-1+j] == ch for c in CRIBS for j,ch in enumerate(c['plaintext'])]
        require(len(mask) == 24, 'clue mask length')
        records.append({'phase': phase, 'plaintext': decoded, 'clue_mask': mask,
                        'clue_matches': sum(mask), 'compatible': all(mask),
                        'reference_agreement': True, 'full_reencryption': True})
    require(Path(f['input_path']).read_bytes() == ib, 'input changed')
    for name, pin in f['files'].items():
        require(sha((ROOT/name).read_bytes()) == pin, 'source changed')
    hits = [r['phase'] for r in records if r['compatible']]
    print(json.dumps({'schema': 'c20-target-result-v1', 'status': 'COMPLETE_SEVEN_DECODERS',
                      'freeze_sha256': args.freeze_sha256, 'input_sha256': INPUT_SHA,
                      'candidate_count': 7, 'clue_positions': 24, 'records': records,
                      'compatible_phases': hits,
                      'conclusion': 'COMPATIBLE_CANDIDATE_NOT_SOLUTION' if hits else 'EXACT_SEVEN_PHASE_MODEL_NEGATIVE'}, sort_keys=True))


if __name__ == '__main__':
    main()
