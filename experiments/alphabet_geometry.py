"""Frozen geometric codebook, with exact integers and no ciphertext access."""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'data/alphabet-skeleton-v1.json'
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def integer(value, name):
    if type(value) is not int:
        raise ValueError(name + ' must be an exact integer')
    return value


def geometry_key(p):
    """Exact declared geometry; straight segments are undirected."""
    if p.get('kind') == 'line':
        if set(p) != {'kind', 'p0', 'p1'}:
            raise ValueError('unexpected line fields')
        points = []
        for name in ('p0', 'p1'):
            xy = p[name]
            if len(xy) != 2 or any(type(x) not in (int, float) or not math.isfinite(x) or not 0 <= x <= 1 for x in xy):
                raise ValueError('invalid line endpoint')
            points.append(tuple(xy))
        if points[0] == points[1]:
            raise ValueError('zero-length line')
        return ('line',) + tuple(sorted(points))
    if p.get('kind') != 'elliptic_arc' or set(p) != {'kind', 'center', 'radii', 'start_degrees', 'sweep_degrees', 'closed'}:
        raise ValueError('unknown primitive or fields')
    for name in ('center', 'radii'):
        if len(p[name]) != 2 or any(type(x) not in (int, float) or not math.isfinite(x) for x in p[name]):
            raise ValueError('invalid arc geometry')
    if any(x <= 0 for x in p['radii']):
        raise ValueError('arc radii must be positive')
    for name in ('start_degrees', 'sweep_degrees'):
        if type(p[name]) not in (int, float) or not math.isfinite(p[name]):
            raise ValueError('invalid arc angle')
    if not 0 < abs(p['sweep_degrees']) <= 360 or type(p['closed']) is not bool or p['closed'] != (abs(p['sweep_degrees']) == 360):
        raise ValueError('invalid arc closure')
    return ('elliptic_arc', tuple(p['center']), tuple(p['radii']), p['start_degrees'], p['sweep_degrees'], p['closed'])


def load_schema(path=SCHEMA):
    s = json.loads(Path(path).read_text())
    order = s['feature_order']
    if order != sorted(s['primitives']) or len(set(order)) != 35 or s['vectorization']['dimensions'] != 35:
        raise ValueError('changed frozen dictionary')
    if list(s['glyphs']) != list(AZ):
        raise ValueError('expected ordered A-Z codebook')
    keys = [geometry_key(s['primitives'][key]) for key in order]
    if len(set(keys)) != len(keys):
        raise ValueError('duplicate primitive geometry')
    for ids in s['glyphs'].values():
        if len(ids) != len(set(ids)) or not set(ids) <= set(order):
            raise ValueError('unknown or repeated primitive')
    if len({vector_from_ids(ids, s) for ids in s['glyphs'].values()}) != 26:
        raise ValueError('codebook collision')
    return s


def vector_from_ids(ids, schema):
    counts = Counter(ids)
    if not set(counts) <= set(schema['feature_order']):
        raise ValueError('unknown primitive')
    return validate_vector([counts[key] for key in schema['feature_order']], len(schema['feature_order']))


def vector_from_geometry(primitives, schema):
    reverse = {geometry_key(p): key for key, p in schema['primitives'].items()}
    try:
        ids = [reverse[geometry_key(p)] for p in primitives]
    except KeyError as exc:
        raise ValueError('geometry absent from frozen dictionary') from exc
    return vector_from_ids(ids, schema)


def validate_vector(vector, length=35):
    v = tuple(vector)
    if len(v) != length or any(type(x) is not int or x not in (0, 1) for x in v):
        raise ValueError('expected fixed-length binary vector')
    return v


def encode_array(vector, radix=2):
    integer(radix, 'radix')
    if radix < 2:
        raise ValueError('radix must be at least two')
    code = 0
    for i, digit in enumerate(vector):
        integer(digit, 'digit')
        if not 0 <= digit < radix:
            raise ValueError('digit outside radix')
        code += digit * radix ** i
    return code


def decode_array(code, length=35, radix=2):
    integer(code, 'code'); integer(length, 'length'); integer(radix, 'radix')
    if code < 0 or length < 0 or radix < 2:
        raise ValueError('invalid code, length, or radix')
    out = []
    for _ in range(length):
        code, digit = divmod(code, radix)
        out.append(digit)
    if code:
        raise ValueError('code outside declared length')
    return tuple(out)


def codebook(schema):
    return {letter: vector_from_ids(ids, schema) for letter, ids in schema['glyphs'].items()}


def lookup_vector(vector, schema):
    v = validate_vector(vector, len(schema['feature_order']))
    reverse = {v: c for c, v in codebook(schema).items()}
    if v not in reverse:
        raise ValueError('vector is not a member of this glyph codebook')
    return reverse[v]


def lookup_code(code, schema):
    return lookup_vector(decode_array(code, len(schema['feature_order'])), schema)


def decision_tree(vectors, order):
    def build(letters):
        if len(letters) == 1:
            return {'letter': letters[0]}
        i = next(i for i in range(len(order)) if len({vectors[c][i] for c in letters}) > 1)
        return {'feature_index': i, 'feature_id': order[i], 'branches': {
            str(value): build([c for c in letters if vectors[c][i] == value])
            for value in sorted({vectors[c][i] for c in letters})}}
    return build(list(vectors))


def lookup_tree(vector, schema, tree):
    v = validate_vector(vector, len(schema['feature_order']))
    node = tree
    while 'letter' not in node:
        branch = str(v[node['feature_index']])
        if branch not in node['branches']:
            raise ValueError('unknown vector branch')
        node = node['branches'][branch]
    # Reaching a leaf alone is insufficient: many unknown vectors take that path.
    letter = node['letter']
    if v != vector_from_ids(schema['glyphs'][letter], schema):
        raise ValueError('leaf reached by a nonmember vector')
    return letter


def collision_groups(values):
    groups = defaultdict(list)
    for c, value in values.items():
        groups[value].append(c)
    return [{'value': value, 'letters': letters} for value, letters in sorted(groups.items())]


def artifacts(schema, source_sha):
    vectors = codebook(schema)
    codes = {c: encode_array(v) for c, v in vectors.items()}
    tree = decision_tree(vectors, schema['feature_order'])
    pairs = []
    for a, b in itertools.combinations(AZ, 2):
        different = [i for i in range(35) if vectors[a][i] != vectors[b][i]]
        assert different
        pairs.append({'letters': a+b, 'first_different_index': different[0], 'feature_id': schema['feature_order'][different[0]]})
    known, rejected = 0, 0
    for c, vector in vectors.items():
        assert lookup_vector(vector, schema) == lookup_code(codes[c], schema) == lookup_tree(vector, schema, tree) == c
        assert decode_array(codes[c]) == vector
        for i in range(35):
            mutant = list(vector); mutant[i] ^= 1
            if tuple(mutant) in vectors.values():
                assert lookup_tree(mutant, schema, tree) == lookup_vector(mutant, schema)
                known += 1
            else:
                try:
                    lookup_tree(mutant, schema, tree)
                except ValueError:
                    rejected += 1
                else:
                    raise AssertionError('unknown mutation accepted')
    data = {'schema_id': schema['schema_id'], 'source_sha256': source_sha, 'dimensions': 35,
            'radix': 2, 'feature_order': schema['feature_order'],
            'vectors': {c: list(v) for c, v in vectors.items()},
            'codes_decimal_strings': {c: str(n) for c, n in codes.items()},
            'decision_tree': tree}
    report = {'schema_id': schema['schema_id'], 'source_sha256': source_sha,
              'dimensions': 35, 'line_features': sum(p['kind']=='line' for p in schema['primitives'].values()),
              'curve_features': sum(p['kind']=='elliptic_arc' for p in schema['primitives'].values()),
              'letters': 26, 'pair_comparisons': 325, 'pair_certificates': pairs,
              'unique_vectors': len(set(vectors.values())), 'unique_full_codes': len(set(codes.values())),
              'roundtrips': {'array': 26, 'integer': 26, 'tree_with_membership': 26},
              'single_bit_mutations': {'total': 910, 'valid_other_glyphs': known, 'unknown_rejected': rejected},
              'ordinary_sum_groups': collision_groups({c: sum(v) for c, v in vectors.items()}),
              'modulo_26_groups': collision_groups({c: n%26 for c, n in codes.items()}),
              'code_sorted_alphabet': ''.join(sorted(AZ, key=codes.get)),
              'pen_stroke_anchors_only': {'A': 3, 'B': 2, 'C': 1, 'D': 2, 'E': 4},
              'scope': 'Representation only; no ciphertext read or cryptanalysis executed.'}
    return data, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    s = load_schema()
    digest = hashlib.sha256(SCHEMA.read_bytes()).hexdigest()
    data, report = artifacts(s, digest)
    if args.write:
        for path, value in [(ROOT/'data/alphabet-features-v1.json', data), (ROOT/'results/ALPHABET-GEOMETRY-001.json', report)]:
            path.write_text(json.dumps(value, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('pair_certificates',)}, indent=2))

if __name__ == '__main__':
    main()
