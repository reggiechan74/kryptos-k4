import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'experiments'))
from alphabet_geometry import (load_schema, codebook, geometry_key, vector_from_ids,
    vector_from_geometry, encode_array, decode_array, lookup_vector, lookup_code,
    decision_tree, lookup_tree, artifacts, SCHEMA)


class AlphabetGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = load_schema()
        cls.v = codebook(cls.s)
        cls.tree = decision_tree(cls.v, cls.s['feature_order'])

    def test_frozen_source_dictionary_and_model_choices(self):
        self.assertEqual(hashlib.sha256(SCHEMA.read_bytes()).hexdigest(), '6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010')
        kinds = [p['kind'] for p in self.s['primitives'].values()]
        self.assertEqual((kinds.count('line'), kinds.count('elliptic_arc')), (26,9))
        self.assertEqual(self.s['glyphs']['I'], ['V_CENTRE_FULL'])
        self.assertEqual(len(self.s['glyphs']['S']), 2)
        self.assertEqual(self.s['glyphs']['U'], ['V_LEFT_UPPER','V_RIGHT_UPPER','ARC_BOTTOM_HALF'])

    def test_all_325_pairs_and_three_lookup_roundtrips(self):
        pairs = list(itertools.combinations(self.v, 2))
        self.assertEqual(len(pairs), 325)
        for a,b in pairs:
            self.assertNotEqual(self.v[a],self.v[b])
            self.assertNotEqual(encode_array(self.v[a]),encode_array(self.v[b]))
        for c,v in self.v.items():
            self.assertEqual(lookup_vector(v,self.s),c)
            self.assertEqual(lookup_code(encode_array(v),self.s),c)
            self.assertEqual(lookup_tree(v,self.s,self.tree),c)

    def test_user_geometric_anchors_and_curves(self):
        for c,expected in {'A':(3,0),'B':(1,2),'C':(0,1),'D':(1,1),'E':(4,0)}.items():
            p=[self.s['primitives'][key] for key in self.s['glyphs'][c]]
            self.assertEqual((sum(x['kind']=='line' for x in p),sum(x['kind']=='elliptic_arc' for x in p)),expected)
        self.assertTrue(self.s['primitives']['ARC_CLOSED_OVAL']['closed'])
        self.assertFalse(self.s['primitives']['ARC_OPEN_RIGHT']['closed'])
        self.assertNotEqual(geometry_key(self.s['primitives']['ARC_OPEN_RIGHT']), geometry_key(self.s['primitives']['ARC_OPEN_UPPER_RIGHT']))

    def test_geometry_not_labels_and_primitive_order_or_direction(self):
        for c,ids in self.s['glyphs'].items():
            primitives = [copy.deepcopy(self.s['primitives'][key]) for key in reversed(ids)]
            for p in primitives:
                if p['kind']=='line':p['p0'],p['p1']=p['p1'],p['p0']
            self.assertEqual(vector_from_geometry(primitives,self.s),self.v[c])
        bad=copy.deepcopy(self.s['primitives']['V_CENTRE_FULL']);bad['p0'][0]=0.4
        with self.assertRaises(ValueError):vector_from_geometry([bad],self.s)
        with self.assertRaises(ValueError):vector_from_ids(['UNKNOWN'],self.s)
        with self.assertRaises(ValueError):vector_from_ids(['V_CENTRE_FULL']*2,self.s)

    def test_every_one_bit_mutation_requires_full_membership(self):
        reverse={v:c for c,v in self.v.items()}
        known=unknown=0
        for v in self.v.values():
            for i in range(35):
                m=list(v);m[i]^=1;m=tuple(m)
                if m in reverse:
                    self.assertEqual(lookup_tree(m,self.s,self.tree),reverse[m]);known+=1
                else:
                    with self.assertRaises(ValueError):lookup_tree(m,self.s,self.tree)
                    with self.assertRaises(ValueError):lookup_vector(m,self.s)
                    unknown+=1
        self.assertEqual(known+unknown,910)
        self.assertGreater(unknown,0)
        # Q tail removal is O; R diagonal removal is P, not an unknown letter.
        self.assertEqual(lookup_vector(vector_from_ids(['ARC_CLOSED_OVAL'],self.s),self.s),'O')
        self.assertEqual(lookup_vector(vector_from_ids(['V_LEFT_FULL','ARC_RIGHT_UPPER_HALF'],self.s),self.s),'P')
        with self.assertRaises(ValueError):lookup_tree([0]*35,self.s,self.tree)

    def test_integer_radices_exhaustive_and_no_machine_width_limit(self):
        for radix in (2,3,4):
            for v in itertools.product(range(radix),repeat=4):
                self.assertEqual(decode_array(encode_array(v,radix),4,radix),v)
        self.assertEqual(encode_array([1]*100),2**100-1)
        self.assertEqual(decode_array(2**100-1,100),(1,)*100)
        self.assertNotEqual(encode_array([0,1]),encode_array([1,0]))
        for args in [([2],2),([-1],2),([True],2),([1.0],2),([1],1)]:
            with self.assertRaises(ValueError):encode_array(*args)
        for args in [(-1,35,2),(2**35,35,2),(1.0,35,2),(True,35,2)]:
            with self.assertRaises(ValueError):decode_array(*args)
        for vector in [[0]*34,[0]*36,[2]+[0]*34,[False]+[0]*34]:
            with self.assertRaises(ValueError):lookup_vector(vector,self.s)

    def test_sums_and_modular_reduction_are_not_injective(self):
        self.assertEqual(sum(self.v['A']),sum(self.v['B']))
        self.assertNotEqual(encode_array(self.v['A']),encode_array(self.v['B']))
        residues=[encode_array(v)%26 for v in self.v.values()]
        self.assertLess(len(set(residues)),26)
        self.assertEqual(encode_array(self.v['O']),2)
        self.assertEqual(encode_array(self.v['I']),2**29)

    def test_base3_codebook_and_binary_order_invariant(self):
        for c,v in self.v.items():
            self.assertEqual(lookup_code(encode_array(v,3),self.s,3),c)
        for base in (2,3,4,5,10):
            self.assertEqual(sorted(self.v,key=lambda c:encode_array(self.v[c],base)),sorted(self.v,key=lambda c:encode_array(self.v[c])))
        # A ternary digit two is legal generic radix data, but not a binary glyph.
        with self.assertRaises(ValueError):lookup_code(2,self.s,3)
        self.assertTrue(any(encode_array(v,3)>2**53-1 for v in self.v.values()))
        # Exhaustive short binary vectors check the highest-difference proof.
        vectors=list(itertools.product((0,1),repeat=8))
        self.assertEqual(sorted(vectors,key=lambda v:encode_array(v,2)),sorted(vectors,key=lambda v:encode_array(v,3)))

    def test_derived_artifacts_rebuild_exactly(self):
        data,report=artifacts(self.s,hashlib.sha256(SCHEMA.read_bytes()).hexdigest())
        self.assertEqual(data,json.loads((ROOT/'data/alphabet-features-v1.json').read_text()))
        self.assertEqual(report,json.loads((ROOT/'results/ALPHABET-GEOMETRY-001.json').read_text()))

if __name__=='__main__':unittest.main()
