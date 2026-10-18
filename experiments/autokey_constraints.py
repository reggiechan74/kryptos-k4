"""Exact existential-primer constraints; no primer search or plaintext filling."""
COEFFICIENTS = {'plus': (1, 1), 'minus': (1, -1), 'beaufort': (-1, 1)}


def validate(cipher, known, alphabet, equation, feedback, lag):
    if (not isinstance(alphabet, str) or len(alphabet) < 2
            or len(set(alphabet)) != len(alphabet)):
        raise ValueError('distinct alphabet symbols required')
    if not cipher or any(c not in alphabet for c in cipher):
        raise ValueError('nonempty literal ciphertext in alphabet required')
    if equation not in COEFFICIENTS or feedback not in ('plaintext', 'ciphertext'):
        raise ValueError('unknown equation or feedback')
    if type(lag) is not int or not 1 <= lag <= len(cipher):
        raise ValueError('integer lag within message required')
    if not isinstance(known, dict) or any(type(i) is not int or not 0 <= i < len(cipher)
            or not isinstance(p, str) or len(p) != 1 or p not in alphabet
            for i, p in known.items()):
        raise ValueError('explicit zero-based known-position map required')


def analyze(cipher, known, alphabet, equation, feedback, lag):
    validate(cipher, known, alphabet, equation, feedback, lag)
    m = len(alphabet)
    sigma, tau = COEFFICIENTS[equation]
    c = [alphabet.index(letter) for letter in cipher]
    first = None
    failures = 0
    if feedback == 'ciphertext':
        anchored = sum(i < lag for i in known)
        checks = len(known) - anchored
        for i, plain in sorted(known.items()):
            if i < lag:
                continue
            predicted = sigma * (c[i] - tau * c[i - lag]) % m
            if predicted != alphabet.index(plain):
                failures += 1
                if first is None:
                    first = {'position_one_based': i + 1,
                             'feedback_position_one_based': i - lag + 1,
                             'predicted_plaintext_at_known_position': alphabet[predicted],
                             'confirmed_plaintext': plain}
    else:
        alpha = [1] * len(cipher)
        beta = [0] * len(cipher)
        for i in range(lag, len(cipher)):
            alpha[i] = -sigma * tau * alpha[i - lag]
            beta[i] = (sigma * c[i] - sigma * tau * beta[i - lag]) % m
        roots = {}
        for i, plain in sorted(known.items()):
            residue = i % lag
            required = alpha[i] * (alphabet.index(plain) - beta[i]) % m
            if residue not in roots:
                roots[residue] = (required, i)
            elif roots[residue][0] != required:
                failures += 1
                if first is None:
                    root, earlier = roots[residue]
                    predicted = (alpha[i] * root + beta[i]) % m
                    first = {'known_positions_one_based': [earlier + 1, i + 1],
                             'root_position_one_based': residue + 1,
                             'required_root_values': [root, required],
                             'chain_positions_between_knowns_one_based': list(range(earlier + 1, i + 2, lag)),
                             'predicted_plaintext_at_known_position': alphabet[predicted],
                             'confirmed_plaintext': plain}
        anchored = len(roots)
        checks = len(known) - anchored
    free = lag - anchored
    classification = ('contradicted' if failures else
                      'compatible_but_underdetermined' if free else 'compatible_fully_constrained')
    return {'classification': classification, 'known_plaintext_constraints': len(known),
            'anchored_primer_parameters': anchored, 'independent_consistency_checks': checks,
            'failed_comparisons_to_first_anchor': failures, 'free_primer_symbols_if_compatible': free,
            'vacuous_consistency_test': checks == 0, 'first_conflict': first,
            'exact_solution_count': 0 if failures else {'base': m, 'exponent': free}}


def transform(text, primer, alphabet, equation, feedback, decrypt=False):
    validate(text, {}, alphabet, equation, feedback, len(primer))
    if any(c not in alphabet for c in primer):
        raise ValueError('literal primer symbols required')
    sigma, tau = COEFFICIENTS[equation]
    m = len(alphabet)
    given = [alphabet.index(c) for c in text]
    seed = [alphabet.index(c) for c in primer]
    out = []
    for i, value in enumerate(given):
        if i < len(seed):
            key = seed[i]
        elif feedback == 'plaintext':
            key = out[i - len(seed)] if decrypt else given[i - len(seed)]
        else:
            key = given[i - len(seed)] if decrypt else out[i - len(seed)]
        out.append((sigma * (value - tau * key) if decrypt else sigma * value + tau * key) % m)
    return ''.join(alphabet[v] for v in out)
