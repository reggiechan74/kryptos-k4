"""End-to-end planted controls, independent vectors, archived-result replay."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from bounded_models import ALPHABETS,EQUATIONS,SEED,routes,model_encrypt,model_decrypt,route_scan,running_scan,trifid_scan
from structural_checks import known_pairs
from statistical_diagnostics import run as statistical_run
from run_bounded import execute,validated_baseline
from run_io import RunSnapshot,specification
from ciphers import k3_permutation,rotate_clockwise


def planted_data(plain,cipher):
    return {'ciphertext':cipher,'cribs':[{'start':22,'end':34,'plaintext':plain[21:34]}, {'start':64,'end':74,'plaintext':plain[63:74]}]}


def archived(name):
    path=ROOT/'results'/name
    return json.loads(gzip.decompress(path.read_bytes()) if name.endswith('.gz') else path.read_text())


class AuditHardeningTests(unittest.TestCase):
    def test_independent_k3_coordinate_formula_every_position(self):
        permutation=k3_permutation()
        for i in range(336):
            r,c=divmod(i,42);j=8*c+7-r;k=24*(j%14)+23-j//14
            self.assertEqual(permutation[k],i)
            v,u=k//24,23-k%24;j_inverse=14*u+v
            self.assertEqual(42*(7-j_inverse%8)+j_inverse//8,i)
        for i,k in [(0,191),(294,23),(335,144)]:self.assertEqual(permutation[k],i)
        controls=json.loads((ROOT/'data/controls.json').read_text())
        intermediate=rotate_clockwise(controls['k3']['plaintext'],8,42)
        self.assertEqual(intermediate[:14],'ILNTAYESTATHCW')
        self.assertEqual(intermediate[-14:],'EDNRWEQWFIGEAD')
        self.assertEqual(controls['k3']['ciphertext'][144],'Q')

    def test_independent_operation_order_vectors(self):
        # Hand arithmetic: P=ABCDE, alternating shifts 1,2; output->input route.
        route=[2,0,4,1,3]
        vectors={'plus':('DBFDF','DCFDE'),'minus':('BZDZB','BYDZC'),'beaufort':('ZBXBZ','ZCXBY')}
        for equation,(sub_first,route_first) in vectors.items():
            for order,cipher in [('sub_then_route',sub_first),('route_then_sub',route_first)]:
                self.assertEqual(model_encrypt('ABCDE',[1,2],ALPHABETS[0][1],equation,route,order),cipher)
                self.assertEqual(model_decrypt(cipher,[1,2],ALPHABETS[0][1],equation,route,order),'ABCDE')

    def test_end_to_end_route_scan_periods_1_16_both_orders(self):
        rng=random.Random(SEED);route=routes()[-1]  # Exercise a route beyond the old first-20 control set.
        for period in [1,16]:
            for case,order in enumerate(['sub_then_route','route_then_sub']):
                name,alphabet=ALPHABETS[case]
                equation=EQUATIONS[(period+case)%3]
                plain=''.join(rng.choice(alphabet) for _ in range(97))
                key=[rng.randrange(26) for _ in range(period)]
                cipher=model_encrypt(plain,key,alphabet,equation,route['permutation'],order)
                result=route_scan(planted_data(plain,cipher))
                candidates=[r for r in result['survivors'] if (r['route'],r['period'],r['alphabet'],r['equation'],r['order'])==(route['id'],period,name,equation,order)]
                self.assertEqual(len(candidates),1)
                record=candidates[0]
                self.assertTrue(all(v is None or v==key[i] for i,v in enumerate(record['key_values'])))
                if not record['unobserved_phases_zero_based']:
                    self.assertEqual(record['plaintext'],plain)
                    self.assertTrue(record['exact_reencryption'])

    def test_end_to_end_route_scan_incomplete_phase_fit(self):
        rng=random.Random(SEED);name,alphabet=ALPHABETS[0]
        plain=''.join(rng.choice(alphabet) for _ in range(97));key=[rng.randrange(26) for _ in range(96)]
        cipher=model_encrypt(plain,key,alphabet,'plus',list(range(97)),'identity')
        result=route_scan(planted_data(plain,cipher))
        candidate=next(r for r in result['survivors'] if (r['route'],r['period'],r['alphabet'],r['equation'])==('R000',96,name,'plus'))
        self.assertEqual(len(candidate['unobserved_phases_zero_based']),72)
        self.assertTrue(candidate['vacuous_fit']);self.assertEqual(candidate['repeated_phase_comparisons'],0)
        self.assertNotIn('plaintext',candidate)
        self.assertTrue(all(v is None or v==key[i] for i,v in enumerate(candidate['key_values'])))

    def test_reversed_running_key_window_recovered_end_to_end(self):
        rng=random.Random(SEED)
        for name,alphabet in ALPHABETS:
            for equation in EQUATIONS:
                plain=''.join(rng.choice(alphabet) for _ in range(97))
                key=[rng.randrange(26) for _ in range(97)]
                cipher=model_encrypt(plain,key,alphabet,equation,list(range(97)),'identity')
                key_text=''.join(alphabet[i] for i in key)
                sources={'k1':{'plaintext':'','ciphertext':''},'k2_restored_s':{'plaintext':'ABCDE'+key_text[::-1]+'ZYXWVUT','ciphertext':''},'k3':{'plaintext':'','ciphertext':''}}
                result=running_scan(planted_data(plain,cipher),sources)
                self.assertTrue(any((r['source'],r['start_one_based'],r['reverse'],r['alphabet'],r['equation'],r['plaintext'])==('k2_restored_s:plaintext',6,True,name,equation,plain) for r in result['survivors']))

    def test_all_282_archived_fits_are_vacuous(self):
        old=archived('ROUTE-001.json.gz');pairs=known_pairs(archived_baseline())
        self.assertEqual(len(old['survivors']),47*2*3)
        periods=Counter()
        for record in old['survivors']:
            self.assertEqual(record['route'],'R000')
            self.assertEqual(len({i%record['period'] for i,_,_ in pairs}),24)
            periods[record['period']]+=1
        self.assertEqual(len(periods),47);self.assertEqual(set(periods.values()),{6})

    def test_archived_route_running_trifid_replay(self):
        data=archived_baseline();controls=json.loads((ROOT/'data/controls.json').read_text())
        new=route_scan(data);old=archived('ROUTE-001.json.gz')
        self.assertEqual(new['route_catalogue'],old['route_catalogue'])
        stripped=[{k:v for k,v in r.items() if k not in ['vacuous_fit','repeated_phase_comparisons']} for r in new['survivors']]
        self.assertEqual(stripped,old['survivors'])
        for actual,filename in [(running_scan(data,controls),'RUNKEY-001.json'),(trifid_scan(data),'TRIFID-001.json')]:
            expected=archived(filename)
            for key,value in json.loads(json.dumps(actual)).items():self.assertEqual(value,expected[key])

    def test_all_archived_statistical_draws_and_tails_replay(self):
        actual=statistical_run();expected=archived('STAT-001.json.gz')
        from statistical_receipt_compare import compare
        report=compare(actual,expected)
        self.assertTrue(report['exact_integer_draws_and_tail_decisions'])

    def test_audited_artifact_bytes_unchanged(self):
        manifest=json.loads((ROOT/'data/audited-results-b83.json').read_text())
        for name,sha in manifest['files'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),sha,name)

    def test_all_scanners_initial_and_final_deadlines(self):
        data=archived_baseline();controls=json.loads((ROOT/'data/controls.json').read_text())
        for action in [lambda limit:route_scan(data,limit),lambda limit:running_scan(data,controls,limit),lambda limit:trifid_scan(data,limit)]:
            with self.assertRaises(TimeoutError):action(-1)
            with patch('bounded_models.deadline_check') as check:
                action(30);calls=check.call_count
            self.assertGreater(calls,1)
            with patch('bounded_models.deadline_check',side_effect=[None]*(calls-1)+[TimeoutError('final check')]):
                with self.assertRaises(TimeoutError):action(30)
        with self.assertRaises(TimeoutError):statistical_run(limit=-1)
        with patch('statistical_diagnostics.deadline_check') as check:
            statistical_run(100,50);calls=check.call_count
        with patch('statistical_diagnostics.deadline_check',side_effect=[None]*(calls-1)+[TimeoutError('final check')]):
            with self.assertRaises(TimeoutError):statistical_run(100,50)

    def test_atomic_success_then_failure_has_no_stale_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with RunSnapshot(root,'test',{'commit':'0'*40},'success') as snapshot:snapshot.write('answer.json',b'{}\n')
            self.assertEqual(json.loads((root/'latest.json').read_text())['status'],'completed')
            before=(root/'success/answer.json').read_bytes()
            with self.assertRaises(TimeoutError):
                with RunSnapshot(root,'test',{'commit':'0'*40},'failure') as snapshot:
                    snapshot.write('answer.json',b'{"not_publishable":true}')
                    raise TimeoutError('injected')
            pointer=json.loads((root/'latest.json').read_text());self.assertEqual(pointer['status'],'incomplete');self.assertEqual(pointer['run_id'],'failure')
            manifest=json.loads((root/'failure/manifest.json').read_text())
            self.assertEqual(manifest['outcome'],'timed_out');self.assertEqual(manifest['artifacts'],{})
            self.assertFalse((root/'failure/answer.json').exists());self.assertEqual((root/'success/answer.json').read_bytes(),before)
            self.assertFalse(any(root.glob('*.pending')))

    def test_executor_final_deadline_after_output_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch('run_bounded.deadline_check',side_effect=[None,None,TimeoutError('after staged output')]):
                with self.assertRaises(TimeoutError):execute(tmp,'test',{},[('TEST',lambda limit:{'value':1},5)],{},'test',lambda:None)
            pointer=json.loads((Path(tmp)/'latest.json').read_text())
            manifest=json.loads((Path(tmp)/pointer['manifest']).read_text())
            self.assertEqual(manifest['status'],'incomplete');self.assertEqual(manifest['jobs'][0]['status'],'incomplete');self.assertEqual(manifest['artifacts'],{})

    def test_final_publish_gate_cannot_publish_completed_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(TimeoutError):
                with RunSnapshot(tmp,'test',{},'publish-timeout') as snapshot:
                    snapshot.write('answer.json',b'{}')
                    snapshot.final_check=lambda:(_ for _ in ()).throw(TimeoutError('publish gate'))
            manifest=json.loads((Path(tmp)/'publish-timeout/manifest.json').read_text())
            self.assertEqual(manifest['status'],'incomplete');self.assertEqual(manifest['artifacts'],{})
            self.assertFalse((Path(tmp)/'publish-timeout/answer.json').exists())

    def test_baseline_validation_and_failed_preflight_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.json';data=archived_baseline();data['ciphertext']='A'+data['ciphertext'][1:];path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):execute(Path(tmp)/'runs','test',{},[],{},'test',lambda:validated_baseline(path))
            pointer=json.loads((Path(tmp)/'runs/latest.json').read_text());self.assertEqual(pointer['status'],'incomplete')
        with self.assertRaises(ValueError):specification(None,ROOT/'research/BOUNDED-SPEC.md')


def archived_baseline():return json.loads((ROOT/'data/k4.json').read_text())

if __name__=='__main__':unittest.main()
