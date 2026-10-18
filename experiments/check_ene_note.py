"""Verify arithmetic and two-cell evidence in the ENE note; no key/search sweep."""
from fractions import Fraction
from math import gcd
from pathlib import Path
import gzip
import hashlib
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bounded_models import ALPHABETS, EQUATIONS, required_key
ROOT = Path(__file__).resolve().parents[1]

def check():
    turn = Fraction(3, 16)
    assert turn * 360 == Fraction(135, 2)
    assert turn * 12 == Fraction(9, 4) and turn * 24 == Fraction(9, 2)
    assert turn * 43200 == 8100 and turn * 86400 == 16200
    assert 24 * 16 // gcd(24, 16) == 48
    assert turn * 48 == 9 and 48 // gcd(48, 9) == 16
    assert 86400 // gcd(86400, 8100) == 32
    assert Fraction(13, 2) / 3600 == Fraction(13, 7200)
    data = json.loads((ROOT / 'data/k4.json').read_text())
    pairs = []
    for pos, p, c in [(22, 'E', 'F'), (70, 'C', 'M')]:
        assert data['ciphertext'][pos-1] == c
        assert any(x['start'] <= pos <= x['end'] and x['plaintext'][pos-x['start']] == p for x in data['cribs'])
        pairs.append((p,c))
    assert (70-22) % 16 == 0
    ledger_path = ROOT / 'results/ROUTE-001.json.gz'
    ledger = json.loads(gzip.decompress(ledger_path.read_bytes()))
    identity = next(x['id'] for x in ledger['route_catalogue'] if 'identity' in x['aliases'])
    assert not any(x['route'] == identity and x['period'] == 16 for x in ledger['survivors'])
    witnesses = []
    for name, alphabet in ALPHABETS:
        for equation in EQUATIONS:
            keys = [required_key(p,c,alphabet,equation) for p,c in pairs]
            assert keys[0] != keys[1]
            witnesses.append({'alphabet':name,'equation':equation,'positions_one_based':[22,70],'required_keys_zero_based':keys})
    return {'check':'ENE-NOTE-001','new_sweep':False,'clockwise_north_degrees':'135/2','radians_coefficient_of_pi':'3/8','ccw_east_degrees':'45/2','ccw_east_radians_coefficient_of_pi':'1/8','turn':'3/16','grid_slots':48,'increment_slots':9,'wrapped_state_period':16,'twelve_hour_increment_seconds':8100,'twentyfour_hour_increment_seconds':16200,'8100_second_day_state_period':32,'witnesses':witnesses,'retained_ledger_sha256':hashlib.sha256(ledger_path.read_bytes()).hexdigest(),'retained_identity_period16_survivors':0,'scope':'Fixed AZ/KRYPTOS plus/minus/true-Beaufort at unchanged alignment only; arbitrary phase bijections not excluded.'}

if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
