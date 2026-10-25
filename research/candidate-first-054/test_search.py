import unittest,hashlib,base64
import search as s
PLAIN='OURYOUNGCOURIERCYCLEDEASTNORTHEASTWITHNEWBOOKSFORTHESHOPNEARTHEBERLINCLOCKWHILETHESTREETSLAYQUIET'

def key_for(label):
    rng=s.rng_for('synthetic|'+label)
    return ''.join(rng.choice(s.AZ) for _ in range(97))

class SearchTests(unittest.TestCase):
    def test_all_twelve_crypto_and_fragments(self):
        for t in s.TABLEAUX:
            key=key_for(t.id);cipher=s.encrypt(PLAIN,key,t)
            self.assertEqual(s.decrypt(cipher,key,t),PLAIN)
            self.assertEqual(s.derive_fragments(cipher,t),(key[21:34],key[63:74]))
            self.assertEqual(s.independent_reconstruction(cipher,key,t),(PLAIN,cipher))
            doc=s.Document.from_bytes('fixture',key.encode());out=s.search_all(cipher,[doc])
            expected=[h for h in out['hits'] if h['tableau_id']==t.id]
            self.assertEqual(len(expected),1);self.assertEqual(expected[0]['key'],key);self.assertEqual(expected[0]['plaintext'],PLAIN)
    def test_exact_first_last_and_interior_boundaries(self):
        key=key_for('boundaries');a,b=key[21:34],key[63:74]
        for prefix,suffix in [(b'',b''),(b'',b'Z'*60),(b'Q'*60,b''),(b'Z'*60,b'Q'*60)]:
            doc=s.Document.from_bytes('fixture',prefix+key.encode()+suffix)
            self.assertEqual(s.locate_pairs(doc,a,b)['valid_starts'],[len(prefix)])
            self.assertEqual(s.independent_positions(doc,a,b),[len(prefix)])
    def test_short_prefix_suffix_pair_rejected(self):
        key=key_for('truncation');a,b=key[21:34],key[63:74]
        for raw,prefix,suffix in [(key[1:].encode(),True,False),(key[:-1].encode(),False,True),(key[1:-1].encode(),True,True)]:
            doc=s.Document.from_bytes('short',raw);out=s.locate_pairs(doc,a,b)
            self.assertEqual(out['valid_starts'],[]);self.assertEqual(len(out['boundary_rejected_pairs']),1)
            self.assertEqual(out['boundary_rejected_pairs'][0]['insufficient_prefix'],prefix);self.assertEqual(out['boundary_rejected_pairs'][0]['insufficient_suffix'],suffix)
            self.assertEqual(s.independent_positions(doc,a,b),[])
    def test_spacing_41_42_43(self):
        key=key_for('spacing');a,b=key[21:34],key[63:74]
        for spacing in (41,42,43):
            raw=b'Z'*21+a.encode()+b'Z'*(spacing-13)+b.encode()+b'Z'*30
            doc=s.Document.from_bytes('spacing',raw);out=s.locate_pairs(doc,a,b)
            self.assertEqual(out['valid_starts'],[0] if spacing==42 else [])
            self.assertEqual(s.independent_positions(doc,a,b),out['valid_starts'])
    def test_mutated_cribs_each_tableau(self):
        for t in s.TABLEAUX:
            key=key_for('mutations'+t.id);cipher=s.encrypt(PLAIN,key,t);doc=s.Document.from_bytes('key',key.encode())
            for index in (0,1):
                cribs=list(s.CRIBS);pos,word=cribs[index];cribs[index]=(pos,('A' if word[0]!='A' else 'B')+word[1:])
                parts=s.derive_fragments(cipher,t,tuple(cribs));self.assertEqual(s.locate_pairs(doc,*parts)['valid_starts'],[])
    def test_cross_document_never_joined(self):
        key=key_for('split');t=s.TABLEAUX[0];cipher=s.encrypt(PLAIN,key,t)
        out=s.search_all(cipher,[s.Document.from_bytes('left',key[:50].encode()),s.Document.from_bytes('right',key[50:].encode())])
        self.assertEqual(out['hit_count'],0)
    def test_overlapping_duplicates_all_retained(self):
        key='A'*97;t=s.TABLEAUX[0];cipher=s.encrypt(PLAIN,key,t)
        docs=[s.Document.from_bytes('first',b'A'*101),s.Document.from_bytes('duplicate',b'A'*101)]
        out=s.search_all(cipher,docs);mine=[h for h in out['hits'] if h['tableau_id']==t.id]
        self.assertEqual(len(mine),10);self.assertEqual(sorted(h['window_start'] for h in mine),[0,0,1,1,2,2,3,3,4,4])
        for doc in docs:self.assertEqual(s.locate_pairs(doc,'A'*13,'A'*11)['valid_starts'],list(range(5)))
    def test_pg_markers_exclude_metadata_and_reject_ambiguity(self):
        key=key_for('headers');t=s.TABLEAUX[0];cipher=s.encrypt(PLAIN,key,t)
        start=b'*** START OF THE PROJECT GUTENBERG EBOOK TEST ***\r\n';end=b'*** END OF THIS PROJECT GUTENBERG EBOOK TEST ***\r\n'
        raw=key.encode()+b'\n'+start+b'\n Body: '+key.encode()+b'\n'+end+key.encode()
        doc=s.Document.from_bytes('pg',raw,'project_gutenberg')
        self.assertEqual(doc.normalized,b'BODY'+key.encode());self.assertEqual(doc.metadata['body_start'],len(key)+1+len(start))
        out=s.search_all(cipher,[doc]);mine=[h for h in out['hits'] if h['tableau_id']==t.id]
        self.assertEqual(len(mine),1);self.assertEqual(mine[0]['window_start'],4)
        for bad in [key.encode(),start+key.encode(),end+key.encode()+start,start+start+key.encode()+end]:
            with self.assertRaises(ValueError):s.normalize_with_offsets(bad,'project_gutenberg')
    def test_raw_offset_roundtrip_and_nltk_header(self):
        key=key_for('offsets');t=s.TABLEAUX[-1];cipher=s.encrypt(PLAIN,key,t)
        raw=b'[Historical title 1800]\n'+b'\n'.join((ch.lower().encode()+b'! 8\xc3\xa9') for ch in key)
        doc=s.Document.from_bytes('offsets',raw,'nltk_gutenberg');self.assertEqual(doc.normalized,key.encode())
        out=s.search_all(cipher,[doc]);hit=next(h for h in out['hits'] if h['tableau_id']==t.id)
        snippet=base64.b64decode(hit['raw_excerpt_base64']);self.assertEqual(snippet,raw[hit['raw_start']:hit['raw_end']])
        self.assertTrue(all(hit['checks'].values()));self.assertEqual(hit['key'],key)
    def test_absent_fragments_no_hits(self):
        doc=s.Document.from_bytes('onlyA',b'A'*500)
        self.assertEqual(s.locate_pairs(doc,'B'*13,'C'*11)['valid_starts'],[])
        self.assertEqual(s.independent_positions(doc,'B'*13,'C'*11),[])
    def test_compilation_crossing_retained_and_qualified(self):
        key=key_for('compilation');t=s.TABLEAUX[0];cipher=s.encrypt(PLAIN,key,t)
        doc=s.Document.from_bytes('combined',key.encode(),metadata={'uncertified_compilation_boundaries':[{'normalized_offset':50,'historical_adjacency_verified':False}]})
        hit=next(h for h in s.search_all(cipher,[doc])['hits'] if h['tableau_id']==t.id)
        self.assertEqual(len(hit['crossed_uncertified_compilation_boundaries']),1)
        self.assertIn('historical cross-work adjacency unverified',hit['historical_source_status'])
    def test_conditional_noncrib_changes_invariant(self):
        key=key_for('invariance');known={i for start,w in s.CRIBS for i in range(start,start+len(w))}
        for t in s.TABLEAUX:
            cipher=s.encrypt(PLAIN,key,t);changed=''.join(c if i in known else 'Z' if c!='Z' else 'A' for i,c in enumerate(cipher))
            self.assertEqual(s.derive_fragments(cipher,t),s.derive_fragments(changed,t))

if __name__=='__main__':unittest.main()
