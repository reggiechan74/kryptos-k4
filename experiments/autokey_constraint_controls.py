"""Independent sequential reference and tiny exhaustive primer oracle, synthetic only."""
import itertools
import random
import time

from autokey_constraints import analyze, transform
from bounded_models import deadline_check

POSITIONS = tuple(range(21, 34)) + tuple(range(63, 74))
EQUATIONS = ('plus', 'minus', 'beaufort')
FEEDBACK = ('plaintext', 'ciphertext')


def reference(text, primer, alphabet, equation, feedback, decrypt):
    # Independent direct formulae, not the affine solver or its coefficients.
    out = []
    L, m = len(primer), len(alphabet)
    for i, letter in enumerate(text):
        if i < L:
            key = primer[i]
        elif feedback == 'plaintext':
            key = out[i - L] if decrypt else text[i - L]
        else:
            key = text[i - L] if decrypt else out[i - L]
        value, k = alphabet.index(letter), alphabet.index(key)
        if decrypt:
            if equation == 'plus': value -= k
            elif equation == 'minus': value += k
            else: value = k - value
        else:
            if equation == 'plus': value += k
            elif equation == 'minus': value -= k
            else: value = k - value
        out.append(alphabet[value % m])
    return ''.join(out)


def controls(alphabets, limit=10):
    started = time.monotonic()
    check = lambda: deadline_check(started, limit)
    check()
    rng = random.Random(20261018)
    positive = negative = vacuous_mutations = 0
    for alphabet in alphabets:
        for equation, feedback, lag in itertools.product(EQUATIONS, FEEDBACK, range(1, 97)):
            check()
            plain = ''.join(rng.choice(alphabet) for _ in range(97))
            primer = ''.join(rng.choice(alphabet) for _ in range(lag))
            cipher = reference(plain, primer, alphabet, equation, feedback, False)
            assert transform(plain, primer, alphabet, equation, feedback) == cipher
            recovered = transform(cipher, primer, alphabet, equation, feedback, True)
            assert recovered == plain
            assert transform(recovered, primer, alphabet, equation, feedback) == cipher
            known = {i: plain[i] for i in POSITIONS}
            result = analyze(cipher, known, alphabet, equation, feedback, lag)
            assert result['classification'].startswith('compatible')
            positive += 1
            if result['independent_consistency_checks']:
                if feedback == 'ciphertext':
                    target = next(i for i in POSITIONS if i >= lag)
                else:
                    seen = set()
                    for i in POSITIONS:
                        if i % lag in seen:
                            target = i
                            break
                        seen.add(i % lag)
                known[target] = alphabet[(alphabet.index(known[target]) + 1) % len(alphabet)]
                assert analyze(cipher, known, alphabet, equation, feedback, lag)['classification'] == 'contradicted'
                negative += 1
            else:
                target = POSITIONS[0]
                known[target] = alphabet[(alphabet.index(known[target]) + 1) % len(alphabet)]
                assert analyze(cipher, known, alphabet, equation, feedback, lag)['classification'].startswith('compatible')
                vacuous_mutations += 1
    assert (positive, negative, vacuous_mutations) == (1152, 732, 420)
    oracle_cases = decryptions = 0
    for alphabet, n in [('ABC', 4), ('ABCD', 3)]:
        masks = ({}, {0: 'A', n - 1: 'B'}, {i: alphabet[i % len(alphabet)] for i in range(n)})
        for symbols in itertools.product(alphabet, repeat=n):
            cipher = ''.join(symbols)
            for equation, feedback, lag, known in itertools.product(EQUATIONS, FEEDBACK, (1, 2), masks):
                check()
                solutions = 0
                for seed in itertools.product(alphabet, repeat=lag):
                    plain = reference(cipher, ''.join(seed), alphabet, equation, feedback, True)
                    solutions += all(plain[i] == p for i, p in known.items())
                    decryptions += 1
                result = analyze(cipher, known, alphabet, equation, feedback, lag)
                expected = result['exact_solution_count']
                predicted = 0 if expected == 0 else expected['base'] ** expected['exponent']
                assert predicted == solutions
                oracle_cases += 1
    assert (oracle_cases, decryptions) == (5220, 40536)
    check()
    return {'synthetic_roundtrips_and_planted_positives': positive,
            'planted_negative_rejections': negative, 'vacuous_mutations_still_compatible': vacuous_mutations,
            'oracle_cases': oracle_cases, 'toy_primer_decryptions': decryptions,
            'oracle_maximum_primers_per_case': 16, 'toy_alphabets': ['ABC', 'ABCD'],
            'seed': 20261018, 'generator': 'Python random.Random MT19937',
            'third_party_code_execution': False, 'K4_primer_enumerations': 0}
