"""Run complete K1-K3 known-answer controls and emit a reproducible summary."""
import hashlib
import json
from pathlib import Path
from ciphers import vigenere, k3_permutation, permute

ROOT = Path(__file__).resolve().parents[1]


def run():
    data = json.loads((ROOT / 'data/controls.json').read_text())
    checks = []
    for name in ['k1', 'k2_as_inscribed', 'k2_restored_s']:
        f = data[name]
        assert vigenere(f['plaintext'], f['key']) == f['ciphertext'], name
        assert vigenere(f['ciphertext'], f['key'], decrypt=True) == f['plaintext'], name
        checks.append({'id': name, 'symbols': len(f['ciphertext']),
                       'letters': len(f['ciphertext'].replace('?', '')),
                       'question_marks': f['ciphertext'].count('?'),
                       'ciphertext_sha256': hashlib.sha256(f['ciphertext'].encode()).hexdigest(),
                       'plaintext_sha256': hashlib.sha256(f['plaintext'].encode()).hexdigest(),
                       'full_known_answer_and_inverse': 'PASS'})
    f = data['k3']; permutation = k3_permutation()
    assert permute(f['plaintext'], permutation) == f['ciphertext']
    assert permute(f['ciphertext'], permutation, inverse=True) == f['plaintext']
    checks.append({'id': 'k3', 'letters': 336, 'displayed_separator_excluded': '?',
                   'ciphertext_sha256': hashlib.sha256(f['ciphertext'].encode()).hexdigest(),
                   'plaintext_sha256': hashlib.sha256(f['plaintext'].encode()).hexdigest(),
                   'permutation_sha256': hashlib.sha256(json.dumps(permutation).encode()).hexdigest(),
                   'full_known_answer_and_inverse': 'PASS'})
    return {'experiment': 'CTRL-001', 'checks': checks,
            'scope': 'Full fixed K1, both K2 variants, and 336-letter K3 controls only; no K4 method inference.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
