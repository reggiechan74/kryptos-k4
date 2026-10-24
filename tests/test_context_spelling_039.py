import hashlib,json,math,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import context_spelling_039 as c
class ContextSpelling039Tests(unittest.TestCase):
 def test_complete_small_system_oracle(self):
  self.assertEqual(c.controls(),dict(complete_binary_table_relations=341,all_binary_table_roundtrips=248,enumerated_reachable_tables=8))
 def test_witnesses_and_four_unidentified_second_order_fits(self):
  r=json.loads((ROOT/'results/CONTEXT-SPELLING-039-ORIGINAL.json').read_text());self.assertEqual(r['compatible_descriptions'],4)
  for path,sha in r['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
  for row in r['rows']:
   f=row['fit'];self.assertEqual(f['compatible'],row['source_memory']==2)
   if f['compatible']:self.assertEqual(f['reachable_contexts'],703);self.assertEqual(f['unfixed_context_input_entries'],17942);self.assertGreater(f['log10_completion_count'],18000)
   else:
    a,b=f['witness'];self.assertEqual(a['context'],b['context']);self.assertTrue(a['source']==b['source'] and a['target']!=b['target'] or a['source']!=b['source'] and a['target']==b['target'])
 def test_completed_table_roundtrip_does_not_make_heldout_anomaly_predictive(self):
  r=json.loads((ROOT/'results/CONTEXT-SPELLING-039-ORIGINAL.json').read_text());texts=c.s.full_sources(json.loads((ROOT/'data/controls.json').read_text()))
  for row in r['rows']:
   if not row['fit']['compatible']:continue
   reverse=row['scan_direction']=='right_to_left';pairs=[(x['id'],x['normalized_comparison'],x['normalized_literal']) for x in texts[:2]]
   if row['role']=='literal_to_normal':pairs=[(i,b,a) for i,a,b in pairs]
   tables={}
   for context in c.contexts(c.s.AZ,2):
    f=dict(row['fit']['tables'].get(context,{}));unused=iter(v for v in c.s.AZ if v not in f.values())
    for x in c.s.AZ:
     if x not in f:f[x]=next(unused)
    tables[context]=f
   for ident,a,b in pairs:self.assertEqual(c.apply(a,tables,2,reverse),b);self.assertEqual(c.apply(b,tables,2,reverse,inverse=True),a)
   for j in (0,1):
    fit=c.infer([pairs[j]],c.s.AZ,2,reverse)
    for x in c.sites(*pairs[1-j],2,reverse):
     if x['source']!=x['target']:self.assertNotIn(x['source'],fit['tables'].get(x['context'],{}))
