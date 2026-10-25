"""All benchmarks/tests use synthetic messages, never the actual052author bank."""
import random
import unittest
import concurrent.futures
import reference as p
import native


def synthetic_bank(n=1024,seed=52052,tie_heavy=False):
    assert n%4==0
    rng=random.Random(seed)
    records=[]
    for j in range(n):
        values=[rng.choice(p.AZ) for _ in range(97)] if not tie_heavy else ['A']*97
        # Preserve uniqueness in the tie-heavy fixture without using crib positions.
        if tie_heavy:
            value=j
            for i in range(6):values[i]=p.AZ[value%26];value//=26
        for start,word in p.CRIBS:values[start:start+len(word)]=word
        records.append({'id':f'S{j:04}','group':p.GROUPS_BANK[j%4],'text':''.join(values)})
    return records


def random_cipher(seed):return ''.join(random.Random(seed).choices(p.AZ,k=97))


class NativeTests(unittest.TestCase):
    def test_dimensions_and_penalty(self):
        self.assertEqual(len(native.DESCRIPTIONS),1152)
        self.assertEqual(len(native.PERIOD_TABLE),32*74)
        self.assertAlmostEqual(p.CHOICE_BITS,p.math.log2(1024)+p.math.log2(1152))
        self.assertEqual(p.UNKNOWN,tuple(i for i in range(97) if not(21<=i<34 or 63<=i<74)))

    def test_every_description_score_against_independent_reference(self):
        for fixture in range(3):
            bank=synthetic_bank(4,seed=100+fixture,tie_heavy=fixture==2)
            cipher=random_cipher(200+fixture)
            scorer=native.NativeScorer(bank,4)
            best,desc,ties,all_scores=scorer.raw(cipher,all_scores=True,with_ties=True)
            for j,rec in enumerate(scorer.bank):
                expected=[]
                for t,structure,r in native.DESCRIPTIONS:
                    plain=p.encode(rec['text'],t.plain_alphabet);c=p.encode(cipher,t.cipher_alphabet)
                    q=p.induced(plain,c,t.operation)
                    expected.append(p.reference_description(q,plain,c,structure,r)['score_bits'])
                self.assertEqual(list(all_scores[j*1152:(j+1)*1152]),expected)
                maximum=max(expected)
                chosen=min((i for i,v in enumerate(expected) if v==maximum),key=lambda i:native.KEYS[i])
                self.assertEqual(best[j],maximum);self.assertEqual(desc[j],chosen)
                actual_ties={i for i in range(1152) if ties[j*18+i//64] & (1<<(i%64))}
                self.assertEqual(actual_ties,{i for i,v in enumerate(expected) if v==maximum})

    def test_full_1024_bank_exact_python_agreement(self):
        bank=synthetic_bank();cipher=random_cipher(333)
        actual=native.NativeScorer(bank).score(cipher,details=True)
        expected=p.Scorer(bank).score(cipher,details=True)
        self.assertEqual(actual,expected)

    def test_tie_heavy_bank_model_and_candidate_ties(self):
        bank=synthetic_bank(32,tie_heavy=True)
        for cipher in ['A'*97,random_cipher(555)]:
            self.assertEqual(native.NativeScorer(bank,32).score(cipher,True),p.Scorer(bank,32).score(cipher,True))

    def test_all_tableau_structure_boundary_plants(self):
        bank=synthetic_bank(4)
        scorer=native.NativeScorer(bank,4);rng=random.Random(99052)
        for ti,t in enumerate(p.TABLEAUX):
            for si,structure in enumerate(p.STRUCTURES):
                r=(1,29,32)[(ti+si)%3]
                record=scorer.bank[(ti+si)%4]
                seed=tuple(rng.randrange(26) for _ in range(r))
                cipher,key=p.encrypt_structured(record['text'],seed,t,structure)
                self.assertEqual(p.decrypt_structured(cipher,seed,t,structure),record['text'])
                self.assertEqual(p.decrypt_key(cipher,key,t),record['text'])
                actual=scorer.score(cipher,True)
                self.assertEqual(actual,p.Scorer(bank,4).score(cipher,True))
                self.assertEqual(actual['tied_top_candidate_ids'],[record['id']])
                self.assertTrue(actual['ranked_candidates'][0]['exact_full_fit'])
                self.assertGreater(actual['maximum_score_bits'],16)

    def test_conditional_nulls_full_bank_parallel_identity(self):
        bank=synthetic_bank(32);scorer=native.NativeScorer(bank,32)
        cipher=random_cipher(1234);rng=p.rng_for('synthetic-independent-null-test')
        nulls=[p.conditioned_null(cipher,rng) for _ in range(12)]
        for value in nulls:
            self.assertEqual([value[i] for i in p.KNOWN],[cipher[i] for i in p.KNOWN])
            self.assertEqual(sorted(value[i] for i in p.UNKNOWN),sorted(cipher[i] for i in p.UNKNOWN))
        sequential=[scorer.score(value) for value in nulls]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            parallel=list(executor.map(scorer.score,nulls))
        self.assertEqual(sequential,parallel)
        self.assertEqual(sequential,[p.Scorer(bank,32).score(value) for value in nulls])

    def test_all_exact_diagnostics_match_uncached_reference(self):
        bank=synthetic_bank(8)
        for cipher in (random_cipher(53535),p.encrypt_structured(bank[3]['text'],p.encode('KRYPTOS','AZ'),p.TABLEAUX[4],'periodic')[0]):
            self.assertEqual(native.exact_diagnostics(bank,cipher,8),p.exact_diagnostics(bank,cipher,8))

    def test_independent_hand_vector_and_crib_score_exclusion(self):
        plain='ATTACKATDAWN';seed=p.encode('LEMON','AZ')
        vectors={'vigenere':'LXFOPVEFRNHR','beaufort':'LLTOLBETLNPR','variant_beaufort':'PPHMPZWHPNLJ'}
        for op,expected in vectors.items():
            self.assertEqual(p.encrypt_structured(plain,seed,p.Tableau('AZ','AZ',op),'periodic')[0],expected)
        q=tuple(random.Random(556).choices(range(26),k=97))
        changed=tuple((v+1)%26 if i in p.KNOWN else v for i,v in enumerate(q))
        for r in p.PERIODS:self.assertEqual(p.periodic_errors(q,r),p.periodic_errors(changed,r))


if __name__=='__main__':unittest.main(verbosity=2)
