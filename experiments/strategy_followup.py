"""STRATEGY-FOLLOWUP-001: fixed state models and small independent audits."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random
import subprocess
import time

from ciphers import vigenere
from check_controls import run as check_controls
from run_bounded import validated_baseline, inputs_hashes
from run_io import RunSnapshot, specification, json_bytes

ROOT = Path(__file__).resolve().parents[1]
SPEC = 'research/specifications/STRATEGY-FOLLOWUP-001.json'
AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KR = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
ALPHABETS = (AZ, KR)
TOY_KEY = (0, 1, 3, 2, 1, 0, 2, 3, 0, 3, 1, 2)
TRAIN = (0, 1, 4, 7)
CONSULTED = [SPEC, 'sources/strategy-followup-observations.json',
             'data/k4.json', 'data/controls.json', 'experiments/strategy_followup.py',
             'tests/test_strategy_followup.py', 'experiments/run_io.py',
             'experiments/run_bounded.py', 'experiments/check_baseline.py',
             'experiments/check_controls.py', 'experiments/ciphers.py',
             'experiments/dynamic_key.py', 'experiments/plaintext_step.py',
             'research/specifications/DYNAMIC-KEY-001.json',
             'research/specifications/PLAINTEXT-STEP-001.json']


def configurations():
    return [(r, s) for r in ALPHABETS for s in ALPHABETS]


def model_id(cfg):
    return '/'.join('AZ' if a == AZ else 'KRYPTOS' for a in cfg)


def transform(text, cfg, inverse=False, rotate=False, trace=False):
    """Candidate is move-to-front. rotate=True is a negative control ONLY."""
    r, state = cfg
    if any(c not in AZ for c in text):
        raise ValueError('only literal ASCII A-Z accepted')
    result, states = [], []
    for i, symbol in enumerate(text):
        before = state
        if inverse:
            c = symbol
            out = r[state.index(c)]
        else:
            out = c = state[r.index(symbol)]
        j = state.index(c)
        state = state[j:] + state[:j] if rotate else c + state[:j] + state[j+1:]
        assert len(state) == 26 and set(state) == set(AZ)
        result.append(out)
        if trace:
            states.append(dict(position_one_based=i+1, before=before, input=symbol,
                               output=out, ciphertext=c, after=state))
    return ''.join(result), states


def rank_oracle(text, cfg, inverse):
    """Independent rank-dictionary update; no slicing or transform calls."""
    r, s = cfg
    ranks = {letter: i for i, letter in enumerate(s)}
    result = []
    for symbol in text:
        if inverse:
            c = symbol
            result.append(r[ranks[c]])
        else:
            rank = r.index(symbol)
            c = next(letter for letter in AZ if ranks[letter] == rank)
            result.append(c)
        old = ranks[c]
        for letter in AZ:
            if ranks[letter] < old:
                ranks[letter] += 1
        ranks[c] = 0
        assert sorted(ranks.values()) == list(range(26))
    return ''.join(result)


def crib_map(data):
    return {c['start']-1+j: p for c in data['cribs'] for j, p in enumerate(c['plaintext'])}


def assess(cipher, known, cfg, full=False):
    plain, trace = transform(cipher, cfg, inverse=True, trace=full)
    if transform(plain, cfg)[0] != cipher:
        raise AssertionError('full inverse failed')
    matches = [i+1 for i in sorted(known) if known[i] == plain[i]]
    bad = next((dict(position_one_based=i+1, expected=p, observed=plain[i])
                for i, p in sorted(known.items()) if plain[i] != p), None)
    record = dict(model=model_id(cfg), matches=len(matches), all24=len(matches)==24,
                  east_matches=sum(22 <= i <= 34 for i in matches),
                  berlin_matches=sum(64 <= i <= 74 for i in matches),
                  matched_positions_one_based=matches, first_contradiction=bad,
                  fitted_symbols=0, predicted_crib_positions=24,
                  full_regeneration=True)
    if full:
        record.update(plaintext=plain, states=trace,
                      evidence_class='crib_fit_only' if len(matches)==24 else 'rejected_fixed_output')
    return record


def select(cipher, known):
    records = [assess(cipher, known, cfg) for cfg in configurations()]
    return dict(models=records, compatible=[x['model'] for x in records if x['all24']],
                maximum_matches=max(x['matches'] for x in records))


def equivalence_audit():
    # Superset of prior fixed-tableau arithmetic, including mixed-role alphabets.
    maps = {tuple(ca[(sign*pa.index(p)+k) % 26] for p in AZ)
            for pa, ca, sign, k in itertools.product(ALPHABETS, ALPHABETS, (1, -1), range(26))}
    records = []
    for r, s in configurations():
        j = s.index('D')
        moved = 'D' + s[:j] + s[j+1:]
        function = tuple(moved[r.index(p)] for p in AZ)
        records.append(dict(model=model_id((r, s)), reachable_cipher_prefix='D',
                            state=moved, next_letter_function=''.join(function),
                            outside_prior_affine_superset=function not in maps))
    assert all(x['outside_prior_affine_superset'] for x in records)
    return dict(raw_prior_role_sign_shift_cases=208, distinct_maps=len(maps),
                records=records, conclusion='Not prior fixed-tableau cursor stepping; no global novelty claim.')


def state_controls(known):
    rng = random.Random(2026102220)
    fixtures, nearby, checks = [], [], Counter()
    for cfg in configurations():
        for symbol in AZ:
            cipher = transform(symbol, cfg)[0]
            assert cipher == cfg[1][cfg[0].index(symbol)]
            assert rank_oracle(cipher, cfg, True) == symbol
            checks['one_step_symbols'] += 1
        for _ in range(8):
            plain = list(''.join(rng.choice(AZ) for _ in range(97)))
            for i, p in known.items():
                plain[i] = p
            plain = ''.join(plain)
            cipher = transform(plain, cfg)[0]
            assert transform(cipher, cfg, inverse=True)[0] == plain
            assert rank_oracle(cipher, cfg, True) == plain
            assert rank_oracle(plain, cfg, False) == cipher
            checks['independent_full_roundtrips'] += 1
            changed = dict(known)
            changed[21] = AZ[(AZ.index(known[21])+1) % 26]
            assert not assess(cipher, changed, cfg)['all24']
            checks['mutated_crib_rejections'] += 1
            fixtures.append(dict(ciphertext=cipher, plaintext=plain, true_model=model_id(cfg)))
            nearby.append(dict(ciphertext=transform(plain, cfg, rotate=True)[0],
                               true_model='cyclic_rotate_control:' + model_id(cfg)))
    # Selector receives only ciphertext and the identical fixed crib constraints.
    rng.shuffle(fixtures)
    for f in fixtures:
        f['selection'] = select(f['ciphertext'], known)
        assert f['true_model'] in f['selection']['compatible']
    rng.shuffle(nearby)
    for f in nearby:
        f['selection'] = select(f['ciphertext'], known)
    decoys = []
    for i in range(199):
        parent = fixtures[i % len(fixtures)]['ciphertext']
        shuffled = list(parent)
        rng.shuffle(shuffled)
        cipher = ''.join(shuffled)
        assert Counter(cipher) == Counter(parent)
        decoys.append(dict(ciphertext=cipher, source_fixture_index=i % len(fixtures),
                           selection=select(cipher, known)))
    unique = sum(f['selection']['compatible'] == [f['true_model']] for f in fixtures)
    ambiguous = sum(len(f['selection']['compatible']) > 1 for f in fixtures)
    nearby_false = sum(bool(f['selection']['compatible']) for f in nearby)
    decoy_false = sum(bool(f['selection']['compatible']) for f in decoys)
    return dict(seed=2026102220, checks=dict(checks), plants=fixtures,
                nearby_negative_controls=nearby, histogram_decoys=decoys,
                summary=dict(planted=32, correct_unique=unique, ambiguous=ambiguous,
                             nearby_compatible=nearby_false, decoy_compatible=decoy_false,
                             gate_passed=unique >= 30 and nearby_false <= 1 and decoy_false <= 1),
                limitation='Programmatically label-blind selection, not an external human blind; fixed synthetic crib structure, no English scoring or architecture posterior.')


def construction_audit():
    controls = json.loads((ROOT / 'data/controls.json').read_text())
    k1 = controls['k1']
    assert k1['plaintext'][56] == 'Q' and k1['key'][56 % 10] == 'S'
    intended = k1['plaintext'][:56] + 'L' + k1['plaintext'][57:]
    stream = (k1['key'] * 7)[:63]
    entered = stream[:56] + 'C' + stream[57:]
    with_entry = vigenere(intended, entered)
    ordinary = vigenere(intended, k1['key'])
    assert with_entry == k1['ciphertext']
    assert vigenere(with_entry, entered, decrypt=True) == intended
    assert ordinary != k1['ciphertext']
    restored, inscribed = controls['k2_restored_s'], controls['k2_as_inscribed']
    pos = restored['correction']['insert_before_one_based_character'] - 1
    assert pos == 364 and restored['ciphertext'][pos] == 'S'
    deleted = restored['ciphertext'][:pos] + restored['ciphertext'][pos+1:]
    assert deleted == inscribed['ciphertext']
    assert vigenere(deleted, inscribed['key'], decrypt=True) == inscribed['plaintext']
    assert vigenere(restored['ciphertext'], restored['key'], decrypt=True) == restored['plaintext']
    assert sum(c != '?' for c in restored['ciphertext'][:pos]) == 361
    return dict(status='completed_known_pair_controls',
                K1=dict(plaintext_position_one_based=57, observed_plaintext='L',
                        canonical_decoded_plaintext='Q', repeated_key='S', entered_key='C',
                        cipher_letter=k1['ciphertext'][56], entered_key_stream=entered,
                        intended_plaintext=intended, exact63_cipher_match=True,
                        normal_key_cipher=ordinary,
                        normal_key_differences_one_based=[i+1 for i in range(63) if ordinary[i] != k1['ciphertext'][i]],
                        intention='Not determined; neither accidental nor deliberate established.'),
                K2=dict(restored_character_one_based=365, restored_letter_one_based=362,
                        ciphertext_insertion='S', preceding_question_marks=3,
                        restored_suffix=restored['plaintext'][pos:],
                        deleted_suffix=inscribed['plaintext'][pos:], exact_deletion_reproduction=True),
                transfer_to_K4='None; canonical inputs unchanged; no independent K4 discrepancy.',
                related_artwork='Prerequisite pending: no complete independently sourced aligned pair supplied in this run.')


def clock_audit():
    source = json.loads((ROOT / 'sources/strategy-followup-observations.json').read_text())['clock']
    observed = source['observed_hours_left_to_right']
    assert observed == list(range(10, 17))
    def h(q, phi):
        return 1 + ((q + phi - 1) % 24)
    fits = [phi for phi in range(1, 25) if all(h(q, phi) == observed[q] for q in range(3))]
    assert fits == [10]
    predicted = [h(q, fits[0]) for q in range(3, 7)]
    assert predicted == observed[3:]
    return dict(status='observable_operator_control_only', local_visible_ordinals=list(range(7)),
                observations=observed, fitted_phase=fits[0], fitted_letters=0,
                training_labels=3, free_phase_parameters=1, redundant_training_checks=2,
                heldout_labels=observed[3:], predicted=predicted, exact_holdout=True,
                correlated_observations=True, partial_lower_band_labels=source['partial_lower_band_labels'],
                K4_application_status='underidentified_no_letter_operator',
                blockers=['No complete1989city/zone/order inventory',
                          'No independently specified city/time-to-K4-letter operator',
                          'No photograph time or absolute geographical phase calibration'],
                conclusion='One shared daily phase suffices for these visible consecutive hour labels; no inferred rotor per city or hemisphere bit. This is not cryptanalytic evidence.')


def toy_encode(plain, r, s):
    return ''.join(s[(r.index(p)+k) % 4] for p, k in zip(plain, TOY_KEY))


def toy_decode(cipher, r, s):
    return ''.join(r[(s.index(c)-k) % 4] for c, k in zip(cipher, TOY_KEY))


def toy_forward_oracle(cipher, r, s):
    result = []
    for c, k in zip(cipher, TOY_KEY):
        table = {p: s[(r.index(p)+k) % 4] for p in 'ABCD'}
        result.append(next(p for p, out in table.items() if out == c))
    return ''.join(result)


def gauge_id(r, s):
    return min((r[i:]+r[:i], s[i:]+s[:i]) for i in range(4))


def summarize_toy(cipher, plain, pairs):
    direct, oracle = [], []
    for r, s in pairs:
        decoded = toy_decode(cipher, r, s)
        checked = toy_forward_oracle(cipher, r, s)
        assert checked == decoded
        if all(decoded[i] == plain[i] for i in TRAIN):
            direct.append((r, s, decoded))
        if all(checked[i] == plain[i] for i in TRAIN):
            oracle.append((r, s, checked))
    assert direct == oracle
    assert len(direct) % 4 == 0
    quotient = {gauge_id(r, s) for r, s, _ in direct}
    assert len(quotient) * 4 == len(direct)
    functions_by_gauge = {}
    for r, s, decoded in direct:
        functions_by_gauge.setdefault(gauge_id(r, s), set()).add(decoded)
    assert all(len(x) == 1 for x in functions_by_gauge.values())
    all_plain = sorted({x[2] for x in direct})
    nonfit = [i for i in range(12) if i not in TRAIN]
    forced = {str(i): all_plain[0][i] for i in nonfit
              if all_plain and len({p[i] for p in all_plain}) == 1}
    small = [x for x in direct if x[0] in ('ABCD', 'ACBD') and x[1] in ('ABCD', 'ACBD')]
    predictions = {}
    for name, survivors, denominator in [('uniform576', direct, 576), ('fixed_list4', small, 4)]:
        predictions[name] = dict(compatible_assignments=len(survivors), prior_mass=len(survivors)/denominator,
                                heldout_counts={str(i): dict(Counter(p[i] for _, _, p in survivors)) for i in nonfit})
    return dict(raw_compatible=len(direct), gauge_classes=len(quotient),
                distinct_plaintexts=len(all_plain), compatible_plaintexts=all_plain,
                forced_nonfit=forced,
                forced_correct=sum(plain[int(i)] == letter for i, letter in forced.items()),
                priors=predictions)


def toy_calibration():
    rng = random.Random(2026102221)
    alphabets = [''.join(p) for p in itertools.permutations('ABCD')]
    pairs = list(itertools.product(alphabets, repeat=2))
    assert len(pairs) == 576
    assert len({gauge_id(r, s) for r, s in pairs}) == 144
    records = []
    for i in range(20):
        r, s = rng.choice(pairs)
        plain = ''.join(rng.choice('ABCD') for _ in range(12))
        cipher = toy_encode(plain, r, s)
        plant = summarize_toy(cipher, plain, pairs)
        assert plain in plant['compatible_plaintexts']
        assert plant['forced_correct'] == len(plant['forced_nonfit'])
        shuffled = list(cipher)
        rng.shuffle(shuffled)
        null_cipher = ''.join(shuffled)
        null = summarize_toy(null_cipher, plain, pairs)
        records.append(dict(index=i, true_r=r, true_s=s, plaintext=plain,
                            ciphertext=cipher, planted=plant, null_ciphertext=null_cipher, null=null))
    return dict(status='completed_exact_toy_calibration', seed=2026102221,
                raw_models=576, global_gauge_classes=144, gauge_orbit_size=4,
                cases=records, exhaustive_model_instance_checks=40*576,
                planted_unique_plaintexts=sum(x['planted']['distinct_plaintexts']==1 for x in records),
                planted_ambiguous=sum(x['planted']['distinct_plaintexts']>1 for x in records),
                null_impossible=sum(x['null']['raw_compatible']==0 for x in records),
                null_compatible=sum(x['null']['raw_compatible']>0 for x in records),
                interpretation='Oracle/gauge/prediction gates passed; toy capacity only. No K4 model or historical prior inferred; null compatibility can remain ambiguous.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec-commit', required=True)
    args = parser.parse_args()
    spec = specification(args.spec_commit, SPEC)
    code_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    subprocess.run(['git', 'merge-base', '--is-ancestor', args.spec_commit, code_commit], check=True)
    assert subprocess.check_output(['git', 'show', args.spec_commit+':'+SPEC]) == (ROOT/SPEC).read_bytes()
    for name in CONSULTED:
        if subprocess.check_output(['git', 'show', code_commit+':'+name]) != (ROOT/name).read_bytes():
            raise ValueError('consulted file uncommitted: '+name)
    with RunSnapshot('results/strategy-followup-runs', 'STRATEGY-FOLLOWUP-001', spec) as snapshot:
        start = time.monotonic()
        snapshot.manifest['jobs'].append(dict(experiment='STRATEGY-FOLLOWUP-001', status='running', deadline_seconds=120))
        data = validated_baseline(ROOT/'data/k4.json')
        baseline = check_controls()
        equivalent = equivalence_audit()
        known = crib_map(data)
        harness = state_controls(known)
        construction = construction_audit()
        clock = clock_audit()
        calibration = toy_calibration()
        if not harness['summary']['gate_passed']:
            raise AssertionError('blind control discrimination gate failed; no K4 evaluation')
        actual = [assess(data['ciphertext'], known, cfg, full=True) for cfg in configurations()]
        if any(x['all24'] for x in actual):
            raise RuntimeError('Survivor requires a separately audited null analysis; do not promote automatically')
        result = dict(id='STRATEGY-FOLLOWUP-001', status='completed', spec_commit=args.spec_commit,
                      code_commit=code_commit,
                      command='python3 experiments/strategy_followup.py --spec-commit '+args.spec_commit,
                      python=platform.python_version(), platform=platform.platform(),
                      file_sha256=inputs_hashes(CONSULTED), baseline=baseline,
                      equivalence_audit=equivalent, blind_harness=harness,
                      construction=construction, clock=clock, calibration=calibration,
                      actual_K4=actual, actual_free_parameters_per_model=0,
                      actual_model_selection_domain=4,
                      elapsed_seconds=time.monotonic()-start,
                      interpretation='Four fixed K4 models rejected, no parameter expansion. Model choice was public-clue-informed. Other tracks are known controls or toy calibration, not additional K4 search counts.')
        snapshot.write('STRATEGY-FOLLOWUP-001.json', json_bytes(result))
        snapshot.manifest['jobs'][-1]['status'] = 'completed'
        def check_deadline():
            if time.monotonic()-start > 120:
                raise TimeoutError('120-second total budget exceeded')
        snapshot.final_check = check_deadline
    print(json.dumps(dict(run_id=snapshot.run_id, state_matches=[x['matches'] for x in actual],
                          harness=harness['summary'], construction=construction['status'],
                          clock=clock['K4_application_status'],
                          toy={k: calibration[k] for k in ('raw_models','planted_unique_plaintexts','planted_ambiguous','null_impossible','null_compatible')},
                          elapsed_seconds=result['elapsed_seconds']), indent=2))


if __name__ == '__main__':
    main()
