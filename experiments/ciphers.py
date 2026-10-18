"""Small exact primitives. No search, network, or silent text normalization."""
from string import ascii_uppercase

KRYPTOS = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'


def alphabet_check(alphabet):
    if len(alphabet) != 26 or set(alphabet) != set(ascii_uppercase):
        raise ValueError('alphabet must be a permutation of ASCII A-Z')


def vigenere(text, key, alphabet=KRYPTOS, decrypt=False):
    """Mixed-alphabet addition, index K=0; ? passes through without key advance."""
    alphabet_check(alphabet)
    if not key or any(c not in alphabet for c in key):
        raise ValueError('key must be nonempty uppercase ASCII')
    if any(c not in alphabet + '?' for c in text):
        raise ValueError('normalize explicitly; only A-Z and literal ? accepted')
    indices = {c: i for i, c in enumerate(alphabet)}
    output, position = [], 0
    for c in text:
        if c == '?':
            output.append(c)
            continue
        shift = indices[key[position % len(key)]]
        output.append(alphabet[(indices[c] + (-shift if decrypt else shift)) % 26])
        position += 1
    return ''.join(output)


def rotate_clockwise(stream, rows, columns):
    """Row-major input/output. Accepts sequences for unique-index controls."""
    if rows < 1 or columns < 1 or rows * columns != len(stream):
        raise ValueError('rectangle must exactly fit the stream')
    output = [stream[r * columns + c]
              for c in range(columns) for r in range(rows - 1, -1, -1)]
    return ''.join(output) if isinstance(stream, str) else output


def k3_permutation():
    """Output position -> input position, two clockwise rotations and reshape."""
    return rotate_clockwise(rotate_clockwise(list(range(336)), 8, 42), 24, 14)


def permute(text, permutation, inverse=False):
    if len(text) != len(permutation) or sorted(permutation) != list(range(len(text))):
        raise ValueError('permutation must bijectively cover all input positions')
    if inverse:
        out = [''] * len(text)
        for i, source in enumerate(permutation):
            out[source] = text[i]
        return ''.join(out)
    return ''.join(text[i] for i in permutation)
