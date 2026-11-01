"""Frozen synthetic-only C20 validation. Never imports any repository or target data."""
import argparse
import collections
import hashlib
import itertools
import json
import pathlib
import sys
import time
import types

ROOT = pathlib.Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authenticate(freeze_sha):
    require(digest(ROOT / 'FREEZE.json') == freeze_sha, 'freeze mismatch')
    f = json.loads((ROOT / 'FREEZE.json').read_text())
    for name, pin in f['files'].items():
        require(digest(ROOT / name) == pin, 'source mismatch: ' + name)
    require(digest(pathlib.Path(sys.executable).resolve()) == f['interpreter_sha256'], 'interpreter mismatch')
    return f


def source_module(name, path, expected):
    b = path.read_bytes()
    require(hashlib.sha256(b).hexdigest() == expected, 'module source mismatch')
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(b, str(path), 'exec', dont_inherit=True, optimize=0), m.__dict__)
    return m


# The oracle enumerates all possible words, independently encodes their queue
# signatures, and uses lookup. It never reconstructs tiny outputs by walking.
def signature(word, q):
    if not word:
        return (None, tuple(() for _ in range(q)))
    queues = tuple(tuple(word[j+1] for j in range(len(word)-1) if word[j] == v) for v in range(q))
    return (word[0], queues)


def reversed_signature(word, q):
    start, queues = signature(word, q)
    if not word:
        return start, queues
    end = word[-1]
    changed = []
    for v, queue in enumerate(queues):
        if v == end:
            changed.append(queue[::-1])
        elif queue:
            changed.append(queue[-2::-1] + queue[-1:])
        else:
            changed.append(())
    return start, tuple(changed)


def full_reference(word):
    # Independent tuple/dictionary walk for disclosed length97 plants only.
    # Its mathematical construction is shared; tiny exhaustive lookup above
    # is the independent reconstruction oracle.
    if not word:
        return ()
    start, queues = reversed_signature(word, 26)
    pending = {i: queue for i, queue in enumerate(queues) if queue}
    out = [start]
    while pending:
        require(out[-1] in pending, 'reference premature end')
        queue = pending[out[-1]]
        v = queue[0]
        if len(queue) == 1:
            del pending[out[-1]]
        else:
            pending[out[-1]] = queue[1:]
        out.append(v)
    require(len(out) == len(word) and out[-1] == word[-1], 'reference endpoint/length')
    return tuple(out)


def edges(word):
    return collections.Counter(zip(word, word[1:]))


def invariants(x, y, q):
    require(len(x) == len(y), 'length')
    require(not x or (x[0], x[-1]) == (y[0], y[-1]), 'endpoints')
    require(collections.Counter(x) == collections.Counter(y), 'unigrams')
    require(edges(x) == edges(y), 'directed bigrams')
    if x:
        qa = signature(x, q)[1]
        qb = signature(y, q)[1]
        for v in range(q):
            if v != x[-1] and qa[v]:
                require(qb[v] and qa[v][-1] == qb[v][-1], 'last exit')


def text(s):
    return tuple(ord(c)-65 for c in s)


def repeat(s):
    return text((s * ((97+len(s)-1)//len(s)))[:97])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze-sha256', required=True)
    args = parser.parse_args()
    began = time.process_time()
    f = authenticate(args.freeze_sha256)
    c = source_module('c20_frozen', ROOT / 'c20.py', f['files']['c20.py'])
    trace = hashlib.sha256()
    per_q = []
    total = 0
    fixed_total = 0
    for q, maximum in ((2, 10), (3, 8), (4, 6)):
        count = fixed = 0
        for n in range(maximum+1):
            oracle = {}
            for w in itertools.product(range(q), repeat=n):
                sig = signature(w, q)
                require(sig not in oracle, 'nonunique queue signature')
                oracle[sig] = w
            require(len(oracle) == q**n, 'oracle count')
            for w in itertools.product(range(q), repeat=n):
                key = reversed_signature(w, q)
                require(key in oracle, 'transformed signature not a valid word')
                expected = oracle[key]
                observed = c.transform(w, q)
                require(observed == expected, 'tiny oracle mismatch')
                require(c.transform(observed, q) == w, 'involution')
                invariants(w, observed, q)
                count += 1
                fixed += int(observed == w)
                trace.update(bytes((q, n)) + bytes(w) + b'/' + bytes(observed) + b'\n')
        per_q.append({'q': q, 'max_length': maximum, 'cases': count, 'fixed_points': fixed})
        total += count
        fixed_total += fixed
    require([r['cases'] for r in per_q] == [2047, 9841, 5461], 'per alphabet totals')
    require(total == 17349, 'tiny total')

    hand = [('ABACAD', 'ACABAD'), ('ACABAD', 'ABACAD'), ('ABACA', 'ACABA'), ('ACABA', 'ABACA')]
    for before, after in hand:
        require(c.transform(text(before)) == text(after), 'literal expected fixture')
    # Deliberately broken transformation, isolated from production.
    naive = {0: [2, 1], 1: [0]}  # all-reversed ABAC successors
    naive_out = [0]
    while naive_out[-1] in naive and naive[naive_out[-1]]:
        naive_out.append(naive[naive_out[-1]].pop(0))
    require(naive_out == [0, 2] and sum(map(len, naive.values())) == 2, 'broken-rule negative control')
    x = text('ABACAD' + 'D'*91)
    y = text('ABECAD' + 'D'*91)
    require(c.transform(x) == text('ACABAD' + 'D'*91), 'length97 witness x')
    require(c.transform(y) == y, 'length97 witness y')
    require(x[3] == y[3] == 2 and c.transform(x)[1] == 2 and c.transform(y)[1] == 1, 'fixed-route distinction')

    malformed = [((), q) for q in (None, True, 1, 0, 27, 2.0, '2')]
    malformed += [(w, 2) for w in (None, 'AB', {0, 1}, (True,), (False,), (-1,), (2,), (0.0,), ('A',))]
    for w, q in malformed:
        try:
            c.transform(w, q)
        except ValueError:
            pass
        else:
            raise RuntimeError('malformed accepted')
    bad_phase = (None, True, -1, 7, 0.0, '0')
    phase_rejections = 0
    for fn in (c.encrypt, c.decrypt):
        for p in bad_phase:
            try:
                fn((0,), p)
            except ValueError:
                phase_rejections += 1
            else:
                raise RuntimeError('bad phase accepted')

    literals = ('A', 'AB', 'ABC', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'ZYXWVUTSRQPONMLKJIHGFEDCBA',
                'ABACAD', 'ABECAD', 'AABBAACCAADD', 'ABACABA', 'AAAABBBBCCCCDDDD')
    plants = [repeat(s) for s in literals] + [x, y, repeat('ABCDDCBA')]
    require(len(plants) == 13 and all(len(p) == 97 for p in plants), 'plant count/framing')
    ref_key = tuple(ord(a)-ord('A') for a in 'KRYPTOS')
    require(c.KEY == ref_key == (10, 17, 24, 15, 19, 14, 18), 'literal key')
    require(c.encrypt((0,), 0) == (10,) and c.decrypt((10,), 0) == (0,), 'single-letter key answer')
    phase_counts = []
    phase_pairs = 0
    plant_trace = hashlib.sha256()
    for index, p in enumerate(plants):
        z = full_reference(p)
        require(c.transform(p) == z, 'full reference')
        invariants(p, z, 26)
        outputs = set()
        for phase in range(7):
            expected = tuple((z[i] + ref_key[(i+phase) % 7]) % 26 for i in range(97))
            encrypted = c.encrypt(p, phase)
            require(encrypted == expected, 'phase encoding')
            decoded = c.decrypt(encrypted, phase)
            require(decoded == p, 'full hidden plant recovery')
            recovered_z = tuple((encrypted[i] - ref_key[(i+phase) % 7]) % 26 for i in range(97))
            require(full_reference(recovered_z) == p, 'reference inverse')
            require(c.encrypt(decoded, phase) == encrypted, 'reencryption')
            outputs.add(encrypted)
            phase_pairs += 1
            plant_trace.update(bytes((index, phase)) + bytes(encrypted) + b'\n')
        phase_counts.append(len(outputs))
    require(phase_pairs == 91 and phase_counts == [7]*13, 'phase counts')
    authenticate(args.freeze_sha256)
    result = {'schema': 'c20-synthetic-result-v1', 'status': 'PASS_SYNTHETIC_ONLY',
              'freeze_sha256': args.freeze_sha256, 'tiny_cases': total, 'per_alphabet': per_q,
              'tiny_fixed_points': fixed_total, 'tiny_trace_sha256': trace.hexdigest(),
              'literal_fixture_pairs': len(hand), 'naive_negative_control_detected': True,
              'non_fixed_route_witness': True, 'malformed_rejections': len(malformed),
              'phase_rejections': phase_rejections, 'plants': 13, 'plant_phase_pairs': phase_pairs,
              'distinct_phases_per_plant': phase_counts, 'plant_trace_sha256': plant_trace.hexdigest(),
              'no_target_inputs': True, 'no_statistical_calibration_claim': True,
              'target_admission': 'NOT_ADMITTED', 'worker_process_cpu_seconds': time.process_time()-began}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
