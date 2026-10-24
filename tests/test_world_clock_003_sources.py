import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class WorldClockSourceTests(unittest.TestCase):
    def test_dated_band_counterexample_is_not_a_phase_change(self):
        d=json.loads((ROOT/'sources/world-clock-003/LOCAL-SOURCE-REVIEW.json').read_text())
        a,b=d['band_observations']
        self.assertEqual(a['raw_label'],b['raw_label'])
        self.assertNotEqual(a['physical_band'],b['physical_band'])
        old=json.loads((ROOT/'independent/2026-10-22/historical-clock/historical_clock_evidence.json').read_text())
        known=next(x for x in old['observations'] if x['id']==a['retained_observation_id'])
        self.assertEqual((known['raw_label'],known['physical_band']),(a['raw_label'],a['physical_band']))
        for rotation in range(24):
            for phase in range(24):
                translated=((rotation+phase)%24,a['physical_band'])
                self.assertNotEqual(translated[1],b['physical_band'])
    def test_removed_plate_spelling_and_unknown_dates_are_preserved(self):
        d=json.loads((ROOT/'sources/world-clock-003/LOCAL-SOURCE-REVIEW.json').read_text())
        plate=next(s for s in d['new_sources'] if s['id']=='STRAUSS-REMOVED')
        self.assertEqual(plate['raw_labels'],['HANOI','BANGKOK','PNOM PENH','SINGAPUR+','JAKARTA'])
        self.assertIsNone(plate['installation_date']);self.assertIsNone(plate['removal_date'])
        self.assertFalse(plate['verified_for_1989']);self.assertFalse(plate['image_copied_to_repository'])

    def test_date_separation_unknowns_and_five_target_year_labels(self):
        base=ROOT/'independent/2026-10-24/world-clock-item3'
        d=json.loads((base/'K4-ITEM3-WORLD-CLOCK-INVENTORY.json').read_text())
        segs={s['id']:s for s in d['segments']}
        self.assertTrue(all(not s['globally_registered'] for s in segs.values()))
        self.assertTrue(all(not p['complete_inventory_claim'] for s in segs.values() for p in s['panels']))
        for s in segs.values():
            self.assertEqual(s['adjacencies'],[[a['id'],b['id']] for a,b in zip(s['panels'],s['panels'][1:])])
        may=segs['M89'];known=[label for p in may['panels'] for label in (p['lower'] or [])]
        self.assertEqual(known,['PERTH','SYDNEY','CANBERRA','MELBOURNE','WELLINGTON'])
        self.assertIsNone(may['panels'][3]['lower'])
        pos={label:i for i,p in enumerate(may['panels']) for label in (p['lower'] or [])}
        self.assertEqual((pos['SYDNEY']-pos['PERTH'])%24,2)
        self.assertEqual((pos['WELLINGTON']-pos['SYDNEY'])%24,2)
        self.assertIsNone(may['noncity_annotation']['panel_assignment'])
        self.assertEqual(may['panels'][1]['partial_lines'],['[...]NGJANG','[T?]OKIO'])
        self.assertEqual(d['sources']['M89']['date'],'1989-05')
        self.assertTrue(segs['W90']['not1989']);self.assertIsNone(d['sources']['R_UNDATED']['date'])
        self.assertFalse(d['constraints']['complete_1989']);self.assertFalse(d['constraints']['source_grounded_AZ_bridge'])
        self.assertEqual(d['constraints']['K4_trials'],0)
        import hashlib
        receipt=json.loads((base/'LOCAL-TRANSFER-RECEIPT.json').read_text())
        for name,expected in receipt['files'].items():self.assertEqual(hashlib.sha256((base/name).read_bytes()).hexdigest(),expected)

    def test_changed_city_grouping_is_not_a_global_phase(self):
        old=json.loads((ROOT/'independent/2026-10-22/historical-clock/historical_clock_evidence.json').read_text())
        oldpos={o['raw_label']:o['local_sector'] for o in old['observations'] if o['segment']=='AM1970'}
        new=json.loads((ROOT/'independent/2026-10-24/world-clock-item3/K4-ITEM3-WORLD-CLOCK-INVENTORY.json').read_text())
        segment=next(s for s in new['segments'] if s['id']=='J74')
        newpos={name:i for i,p in enumerate(segment['panels']) for name in (p['upper'] or [])}
        self.assertEqual((oldpos['NEW YORK']-oldpos['MONTREAL'])%24,1)
        self.assertEqual((newpos['NEW YORK']-newpos['MONTREAL'])%24,0)
        for phase in range(24):
            self.assertNotEqual(((oldpos['NEW YORK']+phase)-(oldpos['MONTREAL']+phase))%24,0)
