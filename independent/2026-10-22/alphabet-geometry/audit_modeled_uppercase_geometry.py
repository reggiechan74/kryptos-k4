"""Reconstruct arrays and identifiers from the frozen modeled glyph dictionary.

Usage: python audit_modeled_uppercase_geometry.py [core.json] [report.json]
No external dependencies, ciphertext access, or cryptanalytic tests.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys

core_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('modeled-uppercase-geometry-001-core.json')
report_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name('modeled-uppercase-geometry-001-audit.json')
s = json.loads(core_path.read_text())
order = s['feature_order']
glyphs = s['glyphs']
assert list(glyphs) == list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
assert order == sorted(s['primitives'])
assert len(order) == len(set(order)) == 35
assert all(set(ids) <= set(order) for ids in glyphs.values())
assert all(len(ids) == len(set(ids)) for ids in glyphs.values())
vectors = {letter: [ids.count(key) for key in order] for letter, ids in glyphs.items()}
codes = {letter: sum(value * 2**i for i, value in enumerate(v)) for letter, v in vectors.items()}
assert all(all(value in (0, 1) for value in v) for v in vectors.values())
assert all([(codes[letter] >> i) & 1 for i in range(len(order))] == v for letter, v in vectors.items())
pairs = list(itertools.combinations(glyphs, 2))
collisions = [[a, b] for a, b in pairs if vectors[a] == vectors[b]]
assert len(pairs) == 325 and not collisions
assert len(set(codes.values())) == 26
groups = {}
for letter, vector in vectors.items():
    groups.setdefault(sum(vector), []).append(letter)

def tree(letters):
    if len(letters) == 1:
        return {'letter': letters[0]}
    i = next(i for i in range(len(order)) if len({vectors[letter][i] for letter in letters}) > 1)
    return {'feature_index': i, 'feature_id': order[i], 'branches': {
        str(value): tree([letter for letter in letters if vectors[letter][i] == value])
        for value in sorted({vectors[letter][i] for letter in letters})}}

def decode_tree(node, vector):
    while 'letter' not in node:
        node = node['branches'][str(vector[node['feature_index']])]
    return node['letter']

t = tree(list(glyphs))
assert all(decode_tree(t, v) == letter for letter, v in vectors.items())
report = {
    'schema_id': s['schema_id'], 'source_core_sha256': hashlib.sha256(core_path.read_bytes()).hexdigest(),
    'dimensions': len(order), 'letters': 26, 'pairs_checked': len(pairs), 'collisions': collisions,
    'unique_integer_codes': len(set(codes.values())), 'integer_roundtrips': 26, 'tree_roundtrips': 26,
    'ordinary_sum_groups': groups, 'vectors': vectors, 'codes_decimal_strings': {k: str(v) for k,v in codes.items()},
    'decision_tree': t,
    'scope': 'Representation checks only. No ciphertext, K4 fit, key search, historical-font claim, or encryption claim.'}
report_path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({key: report[key] for key in ['dimensions','letters','pairs_checked','collisions','unique_integer_codes','integer_roundtrips','tree_roundtrips']}))
