"""Exact necessary constraints under explicitly stated K4 models; no search."""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def known_pairs(data):
    return [(i, data['ciphertext'][i], p)
            for crib in data['cribs']
            for i, p in enumerate(crib['plaintext'], crib['start'] - 1)]


def periodic_conflicts(pairs, period):
    """All same-phase equality violations in either direction of a bijection."""
    if period < 1: raise ValueError('period must be positive')
    conflicts = []
    for j, (i, c, p) in enumerate(pairs):
        for k, d, q in pairs[j + 1:]:
            if (i - k) % period == 0 and ((c == d) != (p == q)):
                conflicts.append({'positions_one_based': [i + 1, k + 1],
                                  'cipher': c + d, 'plain': p + q,
                                  'reason': 'same cipher, different plain' if c == d else 'same plain, different cipher'})
    return conflicts


def encode_pairs(symbols, inventory=48):
    """SYNTHETIC codec control, not a Shavian historical encoding hypothesis."""
    if not 1 <= inventory <= 676: raise ValueError('invalid inventory')
    if any(not isinstance(n, int) or not 0 <= n < inventory for n in symbols):
        raise ValueError('unknown symbol')
    return ''.join(chr(65 + n // 26) + chr(65 + n % 26) for n in symbols)


def decode_pairs(text, inventory=48):
    if not 1 <= inventory <= 676: raise ValueError('invalid inventory')
    if len(text) % 2 or any(c < 'A' or c > 'Z' for c in text):
        raise ValueError('incomplete or non-ASCII codeword')
    values = [(ord(text[i]) - 65) * 26 + ord(text[i + 1]) - 65 for i in range(0, len(text), 2)]
    if any(n >= inventory for n in values): raise ValueError('unknown codeword')
    return values


def run():
    data = json.loads((ROOT / 'data/k4.json').read_text())
    text = data['ciphertext']; pairs = known_pairs(data)
    counts = Counter(text); required = Counter(p for _, _, p in pairs)
    deficits = {p: {'required_by_disjoint_cribs': n, 'available_ciphertext': counts[p]}
                for p, n in sorted(required.items()) if n > counts[p]}
    conflicts = {str(period): periodic_conflicts(pairs, period) for period in range(1, 97)}
    rejected = [int(period) for period, witnesses in conflicts.items() if witnesses]
    return {'experiment': 'STRUCT-001',
            'ciphertext_counts': dict(sorted(counts.items())),
            'crib_required_counts': dict(sorted(required.items())),
            'permutation_only': {'compatible': not bool(deficits), 'deficits': deficits,
                'scope': 'Fixed literal A-Z symbols, disjoint final cribs, length 97, no insertion/deletion/substitution; any composition of permutations.'},
            'periodic_bijective': {'tested_periods_inclusive': [1, 96],
                'contradicted': rejected,
                'not_contradicted': [p for p in range(1, 97) if p not in rejected],
                'witnesses': {p: w for p, w in conflicts.items() if w},
                'scope': 'Untransposed plaintext/ciphertext alignment; one fixed bijective substitution per position phase. Necessary constraints only; no positive support from survival.'},
            'language_feasibility': {
                '48_symbols_to_26_single_symbols_globally_injective': False,
                'exactly_two_AZ_per_intermediate_symbol_then_length_preserving_can_yield_97': False,
                'synthetic_48_symbol_pair_codec_roundtrip': decode_pairs(encode_pairs(list(range(48)))) == list(range(48)),
                'synthetic_all_48_encoded_length': len(encode_pairs(list(range(48)))),
                'scope': 'Cardinality/parity deductions only. Synthetic numerical labels have no historical significance. No translation or actual Shavian/Greek/Cyrillic converter is implemented.'}}


if __name__ == '__main__': print(json.dumps(run(), indent=2))
