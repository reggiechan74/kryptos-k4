"""Exact declared-reset witnesses; no keyword/key/phase search."""
from ciphers import KRYPTOS
from structural_checks import known_pairs


def analyze(data):
    pairs = {index + 1: (cipher, plain) for index, cipher, plain in known_pairs(data)}
    # Explicit one-based starts, not searched or fitted.
    starts = (22, 64)
    first = (25, 67)
    offset = (first[0] - starts[0], first[1] - starts[1])
    c1, p1 = pairs[first[0]]
    c2, p2 = pairs[first[1]]
    fixed = {
        'positions_one_based': list(first), 'reset_starts_one_based': list(starts),
        'zero_based_offsets_after_resets': list(offset),
        'ciphertext': [c1, c2], 'plaintext': [p1, p2],
        'contradiction': offset[0] == offset[1] and c1 == c2 and p1 != p2,
        'reason': 'same restarted bijection cannot map distinct plaintext letters to the same ciphertext letter',
    }
    arithmetic = []
    # Direct formulae deliberately do not call bounded_models.required_key.
    for alphabet in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', KRYPTOS):
        for equation in ('plus', 'minus', 'beaufort'):
            for positions, purpose in [((22, 64), 'same_reset_offset_zero'),
                                       ((22, 33), 'within_segment_period_11')]:
                keys = []
                for position in positions:
                    cipher, plain = pairs[position]
                    p, c = alphabet.index(plain), alphabet.index(cipher)
                    key = c - p if equation == 'plus' else p - c if equation == 'minus' else c + p
                    keys.append(key % 26)
                arithmetic.append({'alphabet': alphabet, 'equation': equation,
                                   'purpose': purpose, 'positions_one_based': list(positions),
                                   'required_key_values': keys,
                                   'contradiction': keys[0] != keys[1]})
    return {'identical_reset_bijection_witness': fixed, 'arithmetic_witnesses': arithmetic,
            'candidate_keys_tested': 0, 'parameter_search': False}
