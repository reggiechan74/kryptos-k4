import itertools,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import sigaba_collector_filter as f
import sigaba_joint_toy as t
import sigaba_joint_toy_oracle as o

class CollectorFilterTests(unittest.TestCase):
 def test_complete_tiny_path_enumeration_matches_dag_edges(self):
  for q in (2,3):
   fixture=t.fixture(q,3);m=t.Model(fixture);plant=fixture['plant'];plain=fixture['plaintext'][:4];cipher=o.simulate(fixture,plain,plant['control'],plant['index'],plant['cipher']);obs=[(i,p,c) for i,(p,c) in enumerate(zip(plain,cipher))];root=tuple(plant['cipher']);g=f.build(m,root,obs,t.Budget(10),range(1,8));paths=[]
   def walk(state,i,edges):
    x=plain[i]
    for j,s in enumerate(state):x=o.wire(fixture['cipher'][j],s,x)
    if x!=cipher[i]:return
    if i==3:paths.append(edges);return
    for mask in range(1,8):
     child=tuple((s-((mask>>j)&1))%q for j,s in enumerate(state));walk(child,i+1,edges+[(state,mask,child)])
   walk(root,0,[]);self.assertTrue(paths)
   for layer in range(3):self.assertEqual(set(g['edges'][layer]),{p[layer] for p in paths})
 def test_disconnected_paths_are_not_pooled(self):
  g=f.prune([{(0,)},{(1,),(9,)},{(2,)}],[ [((0,),1,(1,))], [((9,),1,(2,))] ])
  self.assertFalse(g['nonempty']);self.assertFalse(f.necessary_filter(g,[(1,),(1,)])['passes'])
 def test_all_occurrences_intersect_and_rejection_is_active(self):
  layers=[{(i,)} for i in range(4)];rows=[[( (i,),mask,(i+1,) ) for mask in allowed] for i,allowed in enumerate(({1,2},{2,3},{1,3}))];g=f.prune(layers,rows);self.assertFalse(f.necessary_filter(g,[(1,),(1,),(1,)])['passes'])
  simple=f.prune(layers[:3],[[((0,),1,(1,))],[((1,),2,(2,))]]);self.assertFalse(f.necessary_filter(simple,[(1,),(1,)])['passes'])
 def test_connected_filter_pass_is_not_a_static_map_witness(self):
  g=f.prune([{(0,)},{(1,),(2,)},{(3,),(4,)},{(5,)}],[[((0,),1,(1,)),((0,),2,(2,))],[((1,),1,(3,)),((2,),1,(4,))],[((3,),2,(5,)),((4,),1,(5,))]])
  self.assertTrue(f.necessary_filter(g,[(1,),(2,),(1,)])['passes'])
  paths=[(1,1,2),(2,1,1)];self.assertFalse(any(masks[0]==masks[2] for masks in paths))
 def test_tiny_physical_panel_has_no_false_negatives(self):
  fixture=t.fixture(2,3);m=t.Model(fixture);plain=fixture['plaintext'][:4];seed=fixture['plant']['cipher']
  for control in itertools.product(range(2),repeat=3):
   digits=m.digits(control,4)
   for h,aliases in enumerate(m.aliases):
    cipher=o.simulate(fixture,plain,control,aliases[0],seed);obs=[(i,p,c) for i,(p,c) in enumerate(zip(plain,cipher))];g=f.build(m,seed,obs,t.Budget(10),range(1,8));ok,checks,path=f.physical_first(m,seed,obs,digits,h,t.Budget(10));self.assertTrue(ok);self.assertTrue(f.necessary_filter(g,digits[:3])['passes']);self.assertTrue(all(edge in g['edges'][i] for i,edge in enumerate(path)))
 def test_only_consecutive_known_blocks_define_this_dag(self):
  m=t.Model(t.fixture(2,3))
  with self.assertRaises(ValueError):f.build(m,[0]*3,[(0,0,0),(2,0,0)],t.Budget(10))
