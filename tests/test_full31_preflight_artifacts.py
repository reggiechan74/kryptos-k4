"""Static streamed archive checks only; no extraction or proof/source execution."""
import hashlib,json,re,tarfile,unittest
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'research/method-pilots/full31-preflight-v1'
class Full31PreflightArtifacts(unittest.TestCase):
 def test_streamed_archive_identity(self):
  r=json.loads((D/'ARCHIVE-RECEIPT.json').read_text());a=D/'full31-preflight-pilot.tar.gz';self.assertEqual(a.stat().st_size,r['archive_bytes']);self.assertEqual(hashlib.sha256(a.read_bytes()).hexdigest(),r['archive_sha256']);p=json.loads((D/'PACKAGE-PROVENANCE.json').read_text());wanted={x['member']:x for x in p['members']};seen=set();count=0;cert_bytes=0
  with tarfile.open(a,mode='r|gz') as t:
   for m in t:
    if not m.isfile():continue
    name=m.name.removeprefix('full31-preflight-pilot/');count+=1;seen.add(name);stream=t.extractfile(m);digest=hashlib.sha256();tail=b''
    while True:
     b=stream.read(65536)
     if not b:break
     digest.update(b);self.assertFalse(re.search(rb'page_[a-f0-9]{20,}|Responsibilities Page|/root/[A-Za-z_]|https://chatgpt.com/space/',tail+b),name);tail=b[-128:]
    if name in wanted:
     row=wanted[name];self.assertEqual(digest.hexdigest(),row['public_sha256']);self.assertEqual(m.size,row['bytes'])
    else:self.assertEqual(name,'PACKAGE-PROVENANCE.json');self.assertEqual(digest.hexdigest(),hashlib.sha256((D/name).read_bytes()).hexdigest())
    if name.endswith('.cert.jsonl'):cert_bytes+=m.size;self.assertEqual(wanted[name]['original_sha256'],wanted[name]['public_sha256'])
  self.assertEqual(count,73);self.assertTrue(set(wanted)<=seen);self.assertEqual(sum(x.endswith('.cert.jsonl') for x in seen),8);self.assertEqual(cert_bytes,40360596)
 def test_resource_deduplication(self):
  x=json.loads((D/'RESOURCE-ACCOUNTING.json').read_text());tot=x['totals'];self.assertEqual(len(x['jobs']),4);self.assertTrue(all(r['status']=='PASS' for r in x['jobs']));self.assertAlmostEqual(sum(r['worker_cpu_seconds_reported'] for r in x['jobs']),41.862310);self.assertAlmostEqual(sum(r['supervisor_exclusive_cpu_sample_seconds'] for r in x['jobs']),0.653631);self.assertEqual(tot['full_supervisor_policy_charge_seconds'],20);self.assertEqual(x['terminal_state']['outstanding_cpu_reservations'],0)
 def test_summary_gates(self):
  s=(D/'README.md').read_text()
  for text in ('89 supports','1,006,226','4,495-support','W = 1','not EMPTY','35,264','846,336','before execution','not original byte-identical','proposal only','No fresh draw'):self.assertIn(text,s)
 def test_original_source_maps_preserved(self):
  p=json.loads((D/'PACKAGE-PROVENANCE.json').read_text())
  self.assertEqual(p['original_freeze_sha256'],'eb9da11b8ee9de669294fc94c2dad98642d74bedc4a5e21399b663ba680f61ac')
  for e in p['members']:
   if e['member'].endswith(('.py','.cert.jsonl')):self.assertEqual(e['original_sha256'],e['public_sha256'])
