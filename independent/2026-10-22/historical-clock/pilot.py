"""Evidence integrity and reversible mechanical-coordinate tests, NOT K4 decoding."""
import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'historical_clock_evidence.json').read_text())
obs=D['observations']
forward={o['id']:o['raw_label'] for o in obs}
inverse={label:identity for identity,label in forward.items()}
assert len(forward)==len(obs)
assert len(inverse)==len(forward), 'Raw label is not globally unique; invert using observation identity instead.'
assert all(inverse[forward[o['id']]]==o['id'] for o in obs)
assert all(o['verified_for_1989'] is False and o['semantic_timezone_utc'] is None for o in obs)

def encode_slot(s,band,phase):
    assert 0 <= s < 24 and band in ('upper','lower')
    return ((s+phase)%24,band)
def decode_slot(h,band,phase):
    return ((h-phase)%24,band)
roundtrips=0
for phase in range(24):
 for sector in range(24):
  for band in ('upper','lower'):
   assert decode_slot(*encode_slot(sector,band,phase),phase)==(sector,band)
   roundtrips+=1
# These are integer-phase sanity tests only. Real photographs can have a fractional
# global phase, and imagery determines orientation/phase only to its own precision.
# One phase applies to the whole ring, never one phase per city/character.
cell_counts=Counter((o['segment'],o['local_sector'],o['physical_band']) for o in obs)
sector_counts=Counter((o['segment'],o['local_sector']) for o in obs)
# Test observed local adjacency on a source, without globally joining sources.
for seg in D['segments']:
 assert [x['s'] for x in seg['slots']]==list(range(len(seg['slots'])))
 if all('display_near' in x for x in seg['slots']):
  numerals=[x['display_near'] for x in seg['slots']]
  assert all((b-a)%24==1 for a,b in zip(numerals,numerals[1:]))
 else:
  numerals=[x['overlapping_display_numerals'] for x in seg['slots']]
  assert all(b==[v+1 for v in a] for a,b in zip(numerals,numerals[1:]))
result={
 'status':'PASS: evidence integrity and coordinate round trips only',
 'label_observations':len(obs),'disconnected_segments':len(D['segments']),
 'observed_sector_cells':len(sector_counts),'observed_sector_band_cells':len(cell_counts),
 'label_to_sector_band_loss':len(obs)-len(cell_counts),
 'label_to_sector_loss':len(obs)-len(sector_counts),
 'mechanical_integer_phase_roundtrips':roundtrips,
 'coordinate_label_roundtrips':len(obs),
 'k4_trials_executed':0,
 'k4_trial_blocker':'No observationally supported ciphertext-to-city/coordinate encoder; no 1989 inventory; segments have no observed global join.',
 'interpretation':'The algebra is reversible when phase and physical band are retained. Collapsing many city labels to a panel or panel+band is not invertible. Passing sanity checks is not evidence for a K4 cipher.'
}
(ROOT/'pilot_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
