"""Independent synthetic encoder for future reset-scanner recovery controls.

No K4 fixture access, scanner, candidate key list, or actual-data execution.
Indices here are zero based; a reset applies BEFORE encoding that position.
"""


def reference_encrypt(plain, key, alphabet, equation, reset_indices):
    if len(alphabet) != 26 or set(alphabet) != set('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        raise ValueError('invalid alphabet')
    if not plain or not key or any(c not in alphabet for c in plain + key):
        raise ValueError('nonempty uppercase plaintext/key required')
    if (not isinstance(reset_indices, tuple) or not reset_indices
            or any(type(i) is not int for i in reset_indices)
            or reset_indices[0] != 0
            or list(reset_indices) != sorted(set(reset_indices))
            or reset_indices[-1] >= len(plain)):
        raise ValueError('sorted unique in-range reset tuple starting at zero required')
    if equation not in ('plus', 'minus', 'beaufort'):
        raise ValueError('unknown equation')
    values = {letter: value for value, letter in enumerate(alphabet)}
    output = []
    phase = 0
    for index, letter in enumerate(plain):
        if index in reset_indices:
            phase = 0
        p = values[letter]
        k = values[key[phase % len(key)]]
        if equation == 'plus':
            c = p + k
        elif equation == 'minus':
            c = p - k
        else:
            c = k - p
        output.append(alphabet[c % 26])
        phase += 1
    return ''.join(output)
