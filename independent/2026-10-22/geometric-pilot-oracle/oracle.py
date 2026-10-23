#!/usr/bin/env python3
"""Independent frozen geometric-code pilots. Standard-library Python 3 only.
All indexing internal zero-based; ciphertext positions are one-based in reports.
Never optimize the geometry or select features from a cryptanalytic result.
"""
import argparse, hashlib, itertools, json, random
from pathlib import Path
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KRYPTOS = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
CORE_SHA = '6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010'
FULL_SHA = 'e55edb5b19917dead65d8971b75693dcd5d18a0ceb995f25febcd6193af430dd'
CRIBS = ((21, 'EASTNORTHEAST'), (63, 'BERLINCLOCK'))
WIDTH = 35
MASK = (1 << WIDTH) - 1
PERIODS = tuple(range(1, 13))


def read_geometry(core_path, full_path=None):
    raw = Path(core_path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CORE_SHA, 'Frozen core SHA mismatch'
    schema = json.loads(raw)
    order = schema['feature_order']
    assert len(order) == WIDTH and order == sorted(schema['primitives'])
    assert sorted(schema['glyphs']) == list(AZ)
    code = {}
    for letter, primitive_ids in schema['glyphs'].items():
        assert len(primitive_ids) == len(set(primitive_ids))
        assert set(primitive_ids) <= set(order)
        # Independently derive codes from primitive IDs, not stored decimal values.
        code[letter] = sum(1 << order.index(p) for p in primitive_ids)
    assert len(set(code.values())) == 26
    assert all(0 <= x <= MASK for x in code.values())
    if full_path:
        full_raw = Path(full_path).read_bytes()
        assert hashlib.sha256(full_raw).hexdigest() == FULL_SHA
        full = json.loads(full_raw)
        assert code == {k:int(v) for k,v in full['integer_encoding']['binary_weighted_sum']['codes_decimal_strings'].items()}
        for letter in AZ:
            assert [(code[letter] >> i) & 1 for i in range(WIDTH)] == full['vectors'][letter]
    return code, ''.join(sorted(AZ, key=code.__getitem__))


def minimal_period(key):
    return next(d for d in range(1, len(key)+1) if len(key)%d == 0 and all(key[i] == key[i%d] for i in range(len(key))))


def periodic_crypt(text, alphabet, key, family, decrypt=False):
    index = {c:i for i,c in enumerate(alphabet)}
    assert sorted(alphabet) == list(AZ)
    assert family in ('add', 'beaufort')
    result = []
    for i, ch in enumerate(text):
        x, k = index[ch], key[i%len(key)]
        y = ((x-k) if decrypt else (x+k)) if family == 'add' else k-x
        result.append(alphabet[y%26])
    return ''.join(result)


def fit_periodic(ciphertext, alphabet, family, period, crib=CRIBS[0]):
    start, plaintext = crib
    index = {c:i for i,c in enumerate(alphabet)}
    key, origins = [None]*period, [None]*period
    conflicts = []
    for off, pchar in enumerate(plaintext):
        i = start + off
        c, p = index[ciphertext[i]], index[pchar]
        k = ((c-p) if family == 'add' else (c+p))%26
        residue = i%period
        if key[residue] is not None and key[residue] != k:
            conflicts.append({'residue_zero_based':residue, 'positions_one_based':[origins[residue]+1,i+1], 'required_key_values':[key[residue],k]})
        elif key[residue] is None:
            key[residue], origins[residue] = k, i
    return key, conflicts


def periodic_scan(ciphertext, alphabet, periods=PERIODS):
    rows = []
    for family, period in itertools.product(('add','beaufort'), periods):
        key, conflicts = fit_periodic(ciphertext, alphabet, family, period)
        row = {'family':family,'period':period,'previously_structurally_excluded':period not in (8,11,12),
               'first_crib_pass':not conflicts,'first_crib_conflicts':conflicts,'free_key_entries':[i for i,k in enumerate(key) if k is None]}
        if not conflicts:
            assert not row['free_key_entries'], 'Do not select arbitrary unseen key values'
            plain = periodic_crypt(ciphertext,alphabet,key,family,True)
            row.update(key=key,minimal_period=minimal_period(key),plaintext=plain,
                       second_crib_pass=plain[63:74] == CRIBS[1][1],
                       exact_cribs=all(plain[s:s+len(t)] == t for s,t in CRIBS))
        rows.append(row)
    return rows


def rotl35(state, r):
    assert 0 <= state <= MASK and 0 <= r < WIDTH
    return ((state << r) & MASK) | (state >> (WIDTH-r))


def rotor_crypt(text, alphabet, code, seed, r, source, decrypt=False):
    assert source in ('plaintext','ciphertext')
    assert sorted(alphabet) == list(AZ)
    index = {c:i for i,c in enumerate(alphabet)}
    state = code[seed]
    result = []
    for incoming in text:
        shift = state%26
        outgoing = alphabet[(index[incoming] + (-shift if decrypt else shift))%26]
        plain, cipher = (outgoing,incoming) if decrypt else (incoming,outgoing)
        state = rotl35(state,r) ^ code[plain if source == 'plaintext' else cipher]
        assert 0 <= state <= MASK
        result.append(outgoing)
    return ''.join(result)


def rotor_models():
    yield from itertools.product(('AZ','KRYPTOS'), ('plaintext','ciphertext'), range(WIDTH), AZ)


def rotor_scan(ciphertext, code):
    first_pass, exact = [], []
    count = 0
    for alpha_name, source, r, seed in rotor_models():
        count += 1
        alpha = AZ if alpha_name == 'AZ' else KRYPTOS
        plaintext = rotor_crypt(ciphertext,alpha,code,seed,r,source,True)
        if plaintext[21:34] != CRIBS[0][1]:
            continue
        row = {'alphabet':alpha_name,'source':source,'rotation':r,'seed':seed,'plaintext':plaintext,
               'second_crib_pass':plaintext[63:74] == CRIBS[1][1]}
        first_pass.append(row)
        if row['second_crib_pass']:
            exact.append(row)
    assert count == 3640
    return {'raw_models':count,'first_crib_survivors':first_pass,'exact_crib_survivors':exact,
            'distinct_exact_plaintexts':len({r['plaintext'] for r in exact})}


def synthetic_plaintext():
    rng = random.Random(20261022)
    chars = [rng.choice(AZ) for _ in range(97)]
    for start, crib in CRIBS:
        chars[start:start+len(crib)] = crib
    return ''.join(chars)


def bit_reference_rotation(x,r):
    # Deliberately independent of shifts spanning the boundary.
    return sum(1 << ((i+r)%WIDTH) for i in range(WIDTH) if (x>>i)&1)


def controls(code, rank):
    plain = synthetic_plaintext()
    assert len(plain)==97 and all(plain[s:s+len(t)]==t for s,t in CRIBS)
    count_rotation = 0
    for x in [0,MASK]+[1<<i for i in range(WIDTH)]+list(code.values()):
        for r in range(WIDTH):
            assert rotl35(x,r) == bit_reference_rotation(x,r)
            assert rotl35(rotl35(x,r),(WIDTH-r)%WIDTH)==x
            count_rotation += 1
    # Six positive controls are searched against all 24 periodic models.
    periodic_results = []
    for family, period in itertools.product(('add','beaufort'),(8,11,12)):
        key = [(7*i+3)%26 for i in range(period)]
        cipher = periodic_crypt(plain,rank,key,family)
        assert periodic_crypt(cipher,rank,key,family,True) == plain
        rows = periodic_scan(cipher,rank)
        matching = [x for x in rows if x['family']==family and x['period']==period]
        assert len(matching)==1 and matching[0]['exact_cribs'] and matching[0]['plaintext']==plain and matching[0]['key']==key
        periodic_results.append({'family':family,'period':period,'searched_models':len(rows),'planted_recovered':True})
    # Roundtrip every member of the finite 3,640-model family.
    roundtrips = 0
    for name,source,r,seed in rotor_models():
        alphabet = AZ if name=='AZ' else KRYPTOS
        cipher = rotor_crypt(plain,alphabet,code,seed,r,source)
        assert rotor_crypt(cipher,alphabet,code,seed,r,source,True)==plain
        roundtrips += 1
    # Twelve boundary/interior plants, each selected by full-family search.
    rotor_results = []
    for name,source,r in itertools.product(('AZ','KRYPTOS'),('plaintext','ciphertext'),(0,17,34)):
        alphabet = AZ if name=='AZ' else KRYPTOS
        seed = 'U' if r==34 else ('J' if r==17 else 'A')
        cipher = rotor_crypt(plain,alphabet,code,seed,r,source)
        result = rotor_scan(cipher,code)
        matching = [x for x in result['exact_crib_survivors'] if (x['alphabet'],x['source'],x['rotation'],x['seed'])==(name,source,r,seed)]
        assert len(matching)==1 and matching[0]['plaintext']==plain
        rotor_results.append({'alphabet':name,'source':source,'rotation':r,'seed':seed,'searched_models':3640,'planted_recovered':True,'exact_survivor_count':len(result['exact_crib_survivors'])})
    # Alphabet coordinate-origin rotations must leave physical cipher mappings unchanged.
    gauges = 0
    for alpha in (AZ,KRYPTOS,rank):
        for offset in range(26):
            rotated = alpha[offset:]+alpha[:offset]
            for source in ('plaintext','ciphertext'):
                assert rotor_crypt(plain,alpha,code,'U',34,source)==rotor_crypt(plain,rotated,code,'U',34,source)
                gauges += 1
            assert periodic_crypt(plain,alpha,[2,7,13],'add')==periodic_crypt(plain,rotated,[2,7,13],'add')
    # A feature-column permutation preserves codebook injectivity, not recurrence output.
    reversed_code = {c:sum(((x>>i)&1)<<(WIDTH-1-i) for i in range(WIDTH)) for c,x in code.items()}
    assert len(set(reversed_code.values()))==26
    assert any(rotor_crypt(plain,AZ,code,'U',34,s) != rotor_crypt(plain,AZ,reversed_code,'U',34,s) for s in ('plaintext','ciphertext'))
    return {'status':'all_passed','synthetic_plaintext':plain,'rotation_boundary_comparisons':count_rotation,
            'periodic_full_selection_controls':periodic_results,'rotor_all_family_roundtrips':roundtrips,
            'rotor_full_selection_controls':rotor_results,'alphabet_rotation_gauge_comparisons':gauges,
            'feature_permutation_test':'injectivity preserved; arithmetic cipher behavior changes, as expected'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--core',default='/workspace/shared/modeled-uppercase-geometry-001-core.json')
    parser.add_argument('--full',default='/workspace/shared/modeled-uppercase-geometry-001.json')
    parser.add_argument('--source',default='/workspace/shared/geometric_code_k4_oracle_source.json')
    parser.add_argument('--output',default='/workspace/shared/geometric_code_pilot_audit/result.json')
    parser.add_argument('--controls-only',action='store_true')
    args=parser.parse_args()
    code,rank=read_geometry(args.core,args.full)
    result={'schema_sha256':CORE_SHA,'full_schema_sha256':FULL_SHA,'rank_alphabet':rank,'integer_codes':code,'controls':controls(code,rank)}
    if not args.controls_only:
        raw=Path(args.source).read_bytes()
        source=json.loads(raw)
        ciphertext=source['ciphertext']
        assert len(ciphertext)==97 and source['length']==97 and set(ciphertext)<=set(AZ)
        assert [(c['start']-1,c['plaintext']) for c in source['cribs']]==list(CRIBS)
        assert all(c['end']-c['start']+1==len(c['plaintext']) for c in source['cribs'])
        result['k4_source']={'url':'https://github.com/reggiechan74/kryptos-k4/blob/0d138240fb248d0b74942efc86a51d895946921d/data/k4.json','local_sha256':hashlib.sha256(raw).hexdigest(),'github_blob_sha':'361714e4d9b19393bcc89df59e73d1c0522eeedb'}
        result['pilot1']=periodic_scan(ciphertext,rank)
        result['pilot2']=rotor_scan(ciphertext,code)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'rank_alphabet':rank,'control_status':result['controls']['status'],
        'pilot1_first_survivors':sum(x['first_crib_pass'] for x in result.get('pilot1',[])),
        'pilot1_exact_survivors':sum(x.get('exact_cribs',False) for x in result.get('pilot1',[])),
        'pilot2_first_survivors':len(result.get('pilot2',{}).get('first_crib_survivors',[])),
        'pilot2_exact_survivors':len(result.get('pilot2',{}).get('exact_crib_survivors',[])),
        'output':args.output},indent=2))


if __name__=='__main__':
    main()
