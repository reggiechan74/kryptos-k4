"""Exact C20 queue involution. No I/O, target data or randomness."""

KEY = (10, 17, 24, 15, 19, 14, 18)  # A=0, literal KRYPTOS


def checked(word, q):
    if type(q) is not int or not 2 <= q <= 26:
        raise ValueError('q must be an integer in 2..26')
    if type(word) not in (tuple, list):
        raise ValueError('word must be a tuple or list')
    if any(type(x) is not int or x < 0 or x >= q for x in word):
        raise ValueError('symbols must be integer alphabet ranks')
    return tuple(word)


def transform(word, q=26):
    x = checked(word, q)
    if len(x) < 2:
        return x
    lists = [[] for _ in range(q)]
    for a, b in zip(x, x[1:]):
        lists[a].append(b)
    terminal = x[-1]
    for v in range(q):
        if v == terminal:
            lists[v].reverse()
        elif lists[v]:
            lists[v][:-1] = reversed(lists[v][:-1])
    cursor = [0] * q
    out = [x[0]]
    for _ in range(len(x)-1):
        u = out[-1]
        if cursor[u] >= len(lists[u]):
            raise ValueError('premature trail termination')
        v = lists[u][cursor[u]]
        cursor[u] += 1
        out.append(v)
    if out[-1] != terminal or any(cursor[v] != len(lists[v]) for v in range(q)):
        raise ValueError('incomplete trail or incorrect endpoint')
    return tuple(out)


def phase_checked(phase):
    if type(phase) is not int or not 0 <= phase < 7:
        raise ValueError('phase must be an integer in 0..6')
    return phase


def encrypt(word, phase):
    phase_checked(phase)
    z = transform(word, 26)
    return tuple((v + KEY[(i+phase) % 7]) % 26 for i, v in enumerate(z))


def decrypt(word, phase):
    phase_checked(phase)
    c = checked(word, 26)
    z = tuple((v - KEY[(i+phase) % 7]) % 26 for i, v in enumerate(c))
    return transform(z, 26)
