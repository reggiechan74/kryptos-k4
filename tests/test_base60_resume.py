import itertools
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments'))
from resume_base60_beaufort import class_start_rank,rank_value,remaining_iterator,Peek,atomic_save

class Base60ResumeTests(unittest.TestCase):
    def test_binary_search_boundaries(self):
        for mask in ((0,1),(1,0),(1,1)):
            values=[rank_value(r,mask)[0] for r in range(900)]
            for start in (-1,0,values[0],values[1]-1,values[1],values[1]+1,values[-1],values[-1]+1,3600):
                expected=next((i for i,v in enumerate(values) if v>=start),900)
                self.assertEqual(class_start_rank(mask,start),expected)
    def test_merge_no_repeats(self):
        masks=[(0,1),(1,0),(1,1)];p={'parity_masks':[{'primer_parity':list(m),'compatible':True} for m in masks]}
        expected=sorted(rank_value(r,m) for m in masks for r in range(900))
        for start in (0,61,1000,3599,3600):self.assertEqual(list(remaining_iterator(p,start)),[x for x in expected if x[0]>=start])
    def test_peek_and_atomic_checkpoint(self):
        it=Peek(iter([1,2]));self.assertEqual(it.peek(),1);self.assertEqual(it.peek(),1);self.assertEqual(it.pop(),1);self.assertEqual(it.pop(),2);self.assertIsNone(it.peek())
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'checkpoint.json';atomic_save(p,{'n':1});atomic_save(p,{'n':2});self.assertEqual(json.loads(p.read_text()),{'n':2});self.assertEqual([x.name for x in Path(d).iterdir()],['checkpoint.json'])
