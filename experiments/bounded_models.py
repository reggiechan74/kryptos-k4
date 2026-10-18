"""Finite exact-crib experiments. All key/route conventions explicit."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
from string import ascii_uppercase
import time

from ciphers import KRYPTOS, alphabet_check, permute
from structural_checks import known_pairs

ROOT = Path(__file__).resolve().parents[1]
ALPHABETS = [('AZ', ascii_uppercase), ('KRYPTOS', KRYPTOS)]
EQUATIONS = ['plus', 'minus', 'beaufort']
WIDTHS = [7, 14, 21, 24, 31, 42]
TRIFID_PERIODS = list(range(1, 33)) + [42, 49, 63, 97]
SEED = 20261018


def deadline_check(started, limit):
    if time.monotonic() - started > limit:
        raise TimeoutError('declared deadline reached; no complete result')


def crypt(text, key_values, alphabet, equation, decrypt=False):
    alphabet_check(alphabet)
    if not key_values or any(not 0 <= x < 26 for x in key_values):
        raise ValueError('nonempty modular key required')
    if any(c not in alphabet for c in text): raise ValueError('A-Z input only')
    out = []
    for i, c in enumerate(text):
        value, key = alphabet.index(c), key_values[i % len(key_values)]
        if equation == 'plus': value += -key if decrypt else key
        elif equation == 'minus': value += key if decrypt else -key
        elif equation == 'beaufort': value = key - value
        else: raise ValueError('unknown equation')
        out.append(alphabet[value % 26])
    return ''.join(out)


def required_key(plain, cipher, alphabet, equation):
    p, c = alphabet.index(plain), alphabet.index(cipher)
    if equation == 'plus': return (c - p) % 26
    if equation == 'minus': return (p - c) % 26
    if equation == 'beaufort': return (c + p) % 26
    raise ValueError('unknown equation')


def inverse_permutation(route):
    if sorted(route) != list(range(len(route))): raise ValueError('bad permutation')
    out = [0] * len(route)
    for j, i in enumerate(route): out[i] = j
    return out


def routes(length=97):
    """Return every unique route plus all source aliases for audit."""
    found = {tuple(range(length)): ['identity']}
    for width in WIDTHS:
        height = (length + width - 1) // width
        for major in ['rows', 'columns']:
            for reverse_rows in [False, True]:
                for reverse_columns in [False, True]:
                    rows = list(range(height))[::(-1 if reverse_rows else 1)]
                    cols = list(range(width))[::(-1 if reverse_columns else 1)]
                    cells = [(r,c) for r in rows for c in cols] if major == 'rows' else [(r,c) for c in cols for r in rows]
                    route = tuple(r * width + c for r,c in cells if r * width + c < length)
                    label = '{}:{}:rows{}:cols{}'.format(width, major, '-' if reverse_rows else '+', '-' if reverse_columns else '+')
                    found.setdefault(route, []).append(label)
                    found.setdefault(tuple(inverse_permutation(route)), []).append(label + ':inverse')
    return [{'id': 'R{:03}'.format(i), 'permutation': list(p), 'aliases': names}
            for i, (p, names) in enumerate(found.items())]


def model_encrypt(plain, key, alphabet, equation, route, order):
    if order in ['identity', 'sub_then_route']:
        return permute(crypt(plain, key, alphabet, equation), route)
    if order == 'route_then_sub': return crypt(permute(plain, route), key, alphabet, equation)
    raise ValueError('unknown order')


def model_decrypt(cipher, key, alphabet, equation, route, order):
    if order in ['identity', 'sub_then_route']:
        return crypt(permute(cipher, route, inverse=True), key, alphabet, equation, decrypt=True)
    if order == 'route_then_sub':
        return permute(crypt(cipher, key, alphabet, equation, decrypt=True), route, inverse=True)
    raise ValueError('unknown order')


def constrain(cipher, pairs, route, period, alphabet, equation, order):
    inverse = inverse_permutation(route)
    assigned = {}
    for i, _, plain in pairs:
        j = inverse[i]
        phase = (j if order == 'route_then_sub' else i) % period
        key = required_key(plain, cipher[j], alphabet, equation)
        if phase in assigned and assigned[phase] != key: return None
        assigned[phase] = key
    return [assigned.get(i) for i in range(period)]


def crib_matches(plain, pairs):
    return sum(plain[i] == p for i, _, p in pairs)


def route_scan(data):
    started = time.monotonic(); text = data['ciphertext']; pairs = known_pairs(data)
    catalogue = routes(); survivors = []; tested = 0
    for route in catalogue:
        identity = route['permutation'] == list(range(len(text)))
        periods = range(1, 97) if identity else range(1, 17)
        orders = ['identity'] if identity else ['sub_then_route', 'route_then_sub']
        for period in periods:
            for alphabet_name, alphabet in ALPHABETS:
                for equation in EQUATIONS:
                    for order in orders:
                        tested += 1
                        if tested > 20000: raise RuntimeError('model cap exceeded')
                        if tested % 100 == 0: deadline_check(started, 30)
                        key = constrain(text, pairs, route['permutation'], period, alphabet, equation, order)
                        if key is None: continue
                        unknown = [i for i, value in enumerate(key) if value is None]
                        record = {'route': route['id'], 'period': period, 'alphabet': alphabet_name,
                                  'equation': equation, 'order': order, 'key_values': key,
                                  'unobserved_phases_zero_based': unknown}
                        if not unknown:
                            plain = model_decrypt(text, key, alphabet, equation, route['permutation'], order)
                            assert crib_matches(plain, pairs) == 24
                            assert model_encrypt(plain, key, alphabet, equation, route['permutation'], order) == text
                            record.update({'plaintext': plain, 'exact_reencryption': True})
                        survivors.append(record)
    return {'experiment': 'ROUTE-001', 'tested_models': tested, 'unique_routes': len(catalogue),
            'compatible_models': len(survivors), 'fully_observed_keys': sum(not x['unobserved_phases_zero_based'] for x in survivors),
            'route_catalogue': catalogue, 'survivors': survivors,
            'scope': 'Necessary crib compatibility only; high periods can have unconstrained phases. Complete roundtrip is necessary, not evidence of a solve. Plus/minus overlap by key negation.'}


def running_streams(controls):
    names = ['k1', 'k2_restored_s', 'k3']
    result = []
    for field in ['plaintext', 'ciphertext']:
        clean = {name: controls[name][field].replace('?', '') for name in names}
        for name in ['k2_restored_s', 'k3']:
            result.append((name + ':' + field, clean[name]))
        result.append(('k1+k2_restored_s+k3:' + field, ''.join(clean[name] for name in names)))
    return result


def running_scan(data, controls):
    started = time.monotonic(); cipher = data['ciphertext']; pairs = known_pairs(data)
    tested = 0; survivors = []; windows = []; unique_windows = set(); histogram = Counter()
    # Index tables avoid full decryptions for candidates failing crib checks.
    for source, stream in running_streams(controls):
        for begin in range(len(stream) - 96):
            window = stream[begin:begin + 97]
            for reverse in [False, True]:
                key_text = window[::-1] if reverse else window
                windows.append((source, begin, reverse, key_text)); unique_windows.add(key_text)
                for name, alphabet in ALPHABETS:
                    key_values = [alphabet.index(c) for c in key_text]
                    for equation in EQUATIONS:
                        tested += 1
                        if tested > 30000: raise RuntimeError('candidate cap exceeded')
                        if tested % 1000 == 0: deadline_check(started, 30)
                        matches = 0
                        for i, c, p in pairs:
                            matches += crypt(c, [key_values[i]], alphabet, equation, decrypt=True) == p
                        histogram[matches] += 1
                        if matches == 24:
                            plain = crypt(cipher, key_values, alphabet, equation, decrypt=True)
                            assert crypt(plain, key_values, alphabet, equation) == cipher
                            survivors.append({'source':source, 'start_one_based':begin+1, 'reverse':reverse,
                                              'alphabet':name, 'equation':equation, 'plaintext':plain,
                                              'exact_reencryption':True})
    return {'experiment':'RUNKEY-001', 'tested_models':tested,
            'window_cases_including_direction':len(windows), 'unique_key_strings':len(unique_windows),
            'source_lengths':{name:len(stream) for name,stream in running_streams(controls)},
            'crib_match_histogram':dict(sorted(histogram.items())), 'survivors':survivors,
            'null_calibration':'required if survivors exist; skipped because none' if not survivors else 'PENDING: must run 199 whole-search null controls before interpretation',
            'scope':'Only these restored-S, letter-only streams, contiguous nonwrapping windows, two directions, alphabets and equations. Partial match counts are descriptive, not scored evidence.'}


def trifid(text, cube, period, decrypt=False):
    if len(cube) != 27 or len(set(cube)) != 27: raise ValueError('27 distinct cube symbols required')
    if period < 1 or any(c not in cube for c in text): raise ValueError('invalid period or symbol')
    out = ''
    for begin in range(0, len(text), period):
        block = text[begin:begin+period]; n = len(block)
        coords = [(cube.index(c)//9, (cube.index(c)//3)%3, cube.index(c)%3) for c in block]
        if decrypt:
            flat = [digit for point in coords for digit in point]
            triplets = zip(flat[:n], flat[n:2*n], flat[2*n:])
        else:
            flat = [coords[i][axis] for axis in range(3) for i in range(n)]
            triplets = zip(flat[::3], flat[1::3], flat[2::3])
        out += ''.join(cube[9*a+3*b+c] for a,b,c in triplets)
    return out


def trifid_scan(data):
    pairs = known_pairs(data); tested=0; survivors=[]; maximum=0
    for name, alphabet in ALPHABETS:
        cube=alphabet+'?'
        for period in TRIFID_PERIODS:
            for decrypt in [False,True]:
                tested+=1
                plain=trifid(data['ciphertext'],cube,period,decrypt)
                assert trifid(plain,cube,period,not decrypt)==data['ciphertext']
                matches=crib_matches(plain,pairs);maximum=max(maximum,matches)
                if matches==24:
                    survivors.append({'cube':name+'?', 'period':period, 'operation':'decrypt' if decrypt else 'encrypt', 'plaintext':plain, 'contains_question_mark':'?' in plain, 'exact_reencryption':True})
    return {'experiment':'TRIFID-001','tested_models':tested, 'periods':TRIFID_PERIODS, 'survivors':survivors,
            'maximum_crib_matches_descriptive_only':maximum,
            'scope':'Two literal fixed cube orders, 36 block periods, both directions; no cube/key search, altered input, framing, or added separator.'}


def synthetic_controls():
    rng=random.Random(SEED); catalogue=routes(); running_cases=0; route_cases=0
    for case in range(20):
        plain=''.join(rng.choice(ascii_uppercase) for _ in range(97))
        alphabet=ALPHABETS[case%2][1];equation=EQUATIONS[case%3]
        key=[rng.randrange(26) for _ in range(4)]
        route=catalogue[case%len(catalogue)]['permutation']
        order=['sub_then_route','route_then_sub'][(case//2)%2]
        cipher=model_encrypt(plain,key,alphabet,equation,route,order)
        pairs=[(i,cipher[i],plain[i]) for i in list(range(21,34))+list(range(63,74))]
        recovered=constrain(cipher,pairs,route,4,alphabet,equation,order)
        assert recovered==key
        assert model_decrypt(cipher,key,alphabet,equation,route,order)==plain
        route_cases+=1
        running=[rng.randrange(26) for _ in range(97)]
        cipher=crypt(plain,running,alphabet,equation)
        assert crypt(cipher,running,alphabet,equation,decrypt=True)==plain
        assert all(required_key(p,c,alphabet,equation)==running[i] for i,(p,c) in enumerate(zip(plain,cipher)))
        # Recover an actual planted key window through the same scanner used on K4.
        key_text=''.join(alphabet[i] for i in running)
        stream='ABCDE'+key_text+'ZYXWVUT'
        synthetic_data={'ciphertext':cipher,'cribs':[
            {'start':22,'end':34,'plaintext':plain[21:34]},
            {'start':64,'end':74,'plaintext':plain[63:74]}]}
        synthetic_sources={
            'k1':{'plaintext':'','ciphertext':''},
            'k2_restored_s':{'plaintext':stream,'ciphertext':stream[::-1]},
            'k3':{'plaintext':'','ciphertext':''}}
        recovered_windows=running_scan(synthetic_data,synthetic_sources)['survivors']
        assert any(x['source']=='k2_restored_s:plaintext' and x['start_one_based']==6
                   and not x['reverse'] and x['alphabet']==ALPHABETS[case%2][0]
                   and x['equation']==equation and x['plaintext']==plain
                   for x in recovered_windows)
        running_cases+=1
    return {'seed':SEED,'generator':'Python random.Random/MT19937','route_true_model_recoveries':route_cases,'running_key_roundtrips':running_cases,'running_key_planted_window_recoveries':running_cases}


def main():
    data=json.loads((ROOT/'data/k4.json').read_text());controls=json.loads((ROOT/'data/controls.json').read_text())
    print(json.dumps({'synthetic':synthetic_controls(),'route':route_scan(data),'running':running_scan(data,controls),'trifid':trifid_scan(data)},indent=2))


if __name__=='__main__':main()
