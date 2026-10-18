"""Replay only the newly registered finite scopes; preserve older audit files."""
import hashlib,json
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
from historical_language import run_language
from masking_pilots import autokey_scan,fractionated_morse_scan
from word_scramble import word_scan


REGISTERED_RUNS={
    'language-runs':['20261018T111712Z-27a5aec4af474b789d386fcb5e4e67c0'],
    'masking-runs':['20261018T112316Z-4302f65c58784dc79d801f8a44609fff','20261018T112317Z-3a585d17cef148e0a80c158a43e841dc'],
    'word-runs':['20261018T112641Z-6df780ad6f254787ad9f539f7a60b740']}


def runs(group):
    paths=[ROOT/'results'/group/run_id/'manifest.json' for run_id in REGISTERED_RUNS[group]]
    return [(p.parent,json.loads(p.read_text())) for p in paths]


def artifact(group,experiment):
    for directory,manifest in runs(group):
        name=experiment+'.json'
        if name in manifest['artifacts']:return json.loads((directory/name).read_text())
    raise AssertionError('missing result '+experiment)


class NewMilestoneArtifactTests(unittest.TestCase):
    def test_new_manifests_specifications_code_and_output_hashes(self):
        count=0
        for group in ['language-runs','masking-runs','word-runs']:
            for directory,manifest in runs(group):
                self.assertEqual(manifest['status'],'completed')
                for name,metadata in manifest['artifacts'].items():
                    raw=(directory/name).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),metadata['sha256'])
                    result=json.loads(raw);self.assertEqual(result['run_metadata']['run_id'],manifest['run_id'])
                    for name,sha in result['run_metadata']['file_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),sha,name)
                    count+=1
                spec=manifest['specification'];self.assertEqual(hashlib.sha256((ROOT/spec['file']).read_bytes()).hexdigest(),spec['sha256'])
                self.assertEqual(len(spec['commit']),40);self.assertEqual(len(spec['implementation_commit']),40)
        self.assertEqual(count,4)
    def test_GOST_exhaustive_37060_and_Shavian_gates_replay(self):
        actual=run_language(json.loads((ROOT/'data/k4.json').read_text()));expected=artifact('language-runs','LANG-001')
        self.assertEqual(actual['GOST'],expected['GOST']);self.assertEqual(actual['Shavian'],expected['Shavian'])
        self.assertEqual(actual['GOST']['source_strings_tested'],37060)
    def test_both_fixed_masking_pilots_replay(self):
        data=json.loads((ROOT/'data/k4.json').read_text())
        for result,name in [(autokey_scan(data),'MASK-AUTO-001'),(fractionated_morse_scan(data),'MASK-FM-001')]:
            expected=artifact('masking-runs',name);self.assertEqual(result['records'],expected['records']);self.assertEqual(result['accepted_models'],0)
    def test_24_word_invariant_checks_replay(self):
        data=json.loads((ROOT/'data/k4.json').read_text());intermediates=artifact('masking-runs','MASK-AUTO-001')['records']
        actual=word_scan(data,intermediates);expected=artifact('word-runs','WORD-SCRAMBLE-001')
        self.assertEqual(actual['records'],expected['records']);self.assertEqual(actual['compatible_checks'],0)

if __name__=='__main__':unittest.main()
