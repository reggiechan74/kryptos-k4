"""Independent-vector, property, null, and full-pipeline tests. No K4 data."""
import collections
import random
import unittest

import pilot as p


def synthetic_bank():
    rng = random.Random(510051)
    bank = []
    for j in range(32):
        text = [rng.choice(p.AZ) for _ in range(p.LENGTH)]
        for start, word in p.CRIBS:
            text[start:start+len(word)] = word
        bank.append({"id": f"S{j:02}", "group": "thematic" if j < 16 else "neutral", "text": "".join(text)})
    return bank


class ClassicalTests(unittest.TestCase):
    def test_alphabets_and_dimensions(self):
        self.assertEqual(p.KR, "KRYPTOSABCDEFGHIJLMNQUVWXZ")
        self.assertEqual(len(p.KR), 26)
        self.assertEqual(len(p.UNKNOWN), 73)
        self.assertEqual(len(p.KNOWN), 24)
        self.assertEqual(len(p.TABLEAUX), 12)
        self.assertEqual(len(p.TABLEAUX)*len(p.STRUCTURES)*len(p.PERIODS), 1152)
        self.assertEqual(p.PERIODS[-1], 32)

    def test_independent_hand_vectors(self):
        plain, seed = "ATTACKATDAWN", tuple(p.AZ.index(c) for c in "LEMON")
        expected = {"vigenere": "LXFOPVEFRNHR", "beaufort": "LLTOLBETLNPR", "variant_beaufort": "PPHMPZWHPNLJ"}
        for op, cipher in expected.items():
            t = p.Tableau("AZ", "AZ", op)
            actual, key = p.encrypt_structured(plain, seed, t, "periodic")
            self.assertEqual(actual, cipher)
            self.assertEqual(p.decrypt_structured(cipher, seed, t, "periodic"), plain)
            self.assertEqual(p.decrypt_key(cipher, key, t), plain)
        # Index zero in KR is K; index one is R. Mixed-axis test is literal, not a round-trip oracle.
        self.assertEqual(p.encrypt_key("ABZ", (0, 0, 0), p.Tableau("AZ", "KR", "vigenere")), "KRZ")
        self.assertEqual(p.encrypt_key("KRY", (0, 0, 0), p.Tableau("KR", "AZ", "vigenere")), "ABC")

    def test_random_roundtrips_all_tableaux_structures_and_boundary_lengths(self):
        rng = random.Random(75651)
        for t in p.TABLEAUX:
            for structure in p.STRUCTURES:
                for r in (1, 7, 24, 27, 29, 32):
                    plain = "".join(rng.choice(p.AZ) for _ in range(p.LENGTH))
                    seed = tuple(rng.randrange(26) for _ in range(r))
                    cipher, key = p.encrypt_structured(plain, seed, t, structure)
                    self.assertEqual(p.decrypt_structured(cipher, seed, t, structure), plain)
                    self.assertEqual(p.encrypt_key(plain, key, t), cipher)
                    self.assertEqual(p.decrypt_key(cipher, key, t), plain)
                    self.assertEqual(p.induced(p.encode(plain,t.plain_alphabet),p.encode(cipher,t.cipher_alphabet),t.operation),key)

    def test_residual_score_arithmetic(self):
        self.assertAlmostEqual(p.residual_bits(73, 0), p.math.log2(74))
        self.assertAlmostEqual(p.residual_bits(73, 73), p.math.log2(74)+73*p.LOG25)
        self.assertAlmostEqual(p.description_score(7,73,0), 73*p.LOG26-p.CHOICE_BITS-7*p.LOG26-p.math.log2(74))
        with self.assertRaises(ValueError):
            p.residual_bits(73,74)

    def test_periodic_errors_reference_and_crib_exclusion(self):
        rng = random.Random(451)
        q = tuple(rng.randrange(26) for _ in range(97))
        q2 = tuple((v+1)%26 if i in p.KNOWN else v for i,v in enumerate(q))
        for r in p.PERIODS:
            d = p.reference_description(q,q,q,"periodic",r)
            self.assertEqual(d["mismatch_count_scored"],p.periodic_errors(q,r))
            self.assertEqual(p.periodic_errors(q,r),p.periodic_errors(q2,r))
            self.assertEqual(d["n_scored"],73)

    def test_autokey_bitmask_matches_reference_all_lengths(self):
        rng = random.Random(55751)
        q = tuple(rng.randrange(26) for _ in range(97))
        source = tuple(rng.randrange(26) for _ in range(97))
        qm, sm = p.bitmasks(q,p.UNKNOWN), p.bitmasks(source)
        for r in p.PERIODS:
            matches = sum((a & (b << r)).bit_count() for a,b in zip(qm,sm))
            expected = sum(q[i] == source[i-r] for i in p.UNKNOWN if i >= r)
            self.assertEqual(matches,expected)
            d=p.reference_description(q,source,source,"plaintext_autokey",r)
            self.assertEqual(d["mismatch_count_scored"],p.TAIL_N[r]-matches)

    def test_conditioned_null_and_rng_independence(self):
        rng = random.Random(123)
        cipher = "".join(rng.choice(p.AZ) for _ in range(97))
        null = p.conditioned_null(cipher,p.rng_for("test-null"))
        self.assertEqual([cipher[i] for i in p.KNOWN],[null[i] for i in p.KNOWN])
        self.assertEqual(collections.Counter(cipher[i] for i in p.UNKNOWN),collections.Counter(null[i] for i in p.UNKNOWN))
        self.assertEqual(null,p.conditioned_null(cipher,p.rng_for("test-null")))
        self.assertNotEqual(null,p.conditioned_null(cipher,p.rng_for("other-null")))

    def test_pvalue_ties_and_thresholds(self):
        self.assertEqual(p.pvalue(1,[1]*99),1)
        self.assertEqual(p.pvalue(2,[1]*99),.01)
        self.assertFalse(p.flag(15.99,.01))
        self.assertFalse(p.flag(16,.051))
        self.assertTrue(p.flag(16,.05))

    def test_bank_validation(self):
        bank=synthetic_bank()
        self.assertEqual(len(p.validate_bank(bank)),32)
        bank[1]["text"]=bank[0]["text"]
        with self.assertRaises(ValueError):p.validate_bank(bank)

    def test_optimized_full_maximum_matches_exhaustive_reference(self):
        bank=synthetic_bank()
        cipher="".join(p.rng_for("test-full-reference").choices(p.AZ,k=97))
        scorer=p.Scorer(bank)
        result=scorer.score(cipher,details=True)
        all_scores=[]
        for record in bank:
            scores=[]
            for t in p.TABLEAUX:
                plain,c=p.encode(record["text"],t.plain_alphabet),p.encode(cipher,t.cipher_alphabet)
                key=p.induced(plain,c,t.operation)
                for structure in p.STRUCTURES:
                    for r in p.PERIODS:
                        scores.append(p.reference_description(key,plain,c,structure,r)["score_bits"])
            all_scores.append(max(scores))
            actual=next(x["score_bits"] for x in result["ranked_candidates"] if x["candidate_id"]==record["id"])
            self.assertAlmostEqual(actual,max(scores))
        self.assertAlmostEqual(max(all_scores),result["maximum_score_bits"])

    def test_end_to_end_planted_and_boundary_recovery(self):
        bank=synthetic_bank()
        scorer=p.Scorer(bank)
        plain=bank[0]["text"]
        rng=random.Random(56051)
        for t,structure,r in ((p.TABLEAUX[0],"periodic",7),(p.TABLEAUX[5],"plaintext_autokey",29),(p.TABLEAUX[10],"ciphertext_autokey",32)):
            seed=tuple(rng.randrange(26) for _ in range(r))
            cipher,_=p.encrypt_structured(plain,seed,t,structure)
            result=scorer.score(cipher,details=True)
            self.assertEqual(result["tied_top_candidate_ids"],[bank[0]["id"]])
            self.assertGreater(result["maximum_score_bits"],16)
            d=p.exact_diagnostics(bank,cipher)
            self.assertTrue(all(row["full_inverse"] and row["full_reencryption"] for row in d))
            intended=next(row for row in d if row["candidate_id"]==bank[0]["id"] and row["tableau_id"]==t.id)
            field={"periodic":"registered_exact_periods","plaintext_autokey":"exact_plaintext_autokey_lengths","ciphertext_autokey":"exact_ciphertext_autokey_lengths"}[structure]
            self.assertIn(r,intended[field])


class RunnerTests(unittest.TestCase):
    def test_frozen_control_definitions_reproduce_and_cover_bank(self):
        import run_experiment as runner
        runner.config()
        controls=runner.build_controls()
        self.assertEqual(controls,p.load_json(runner.ROOT/"controls.json"))
        inscope=[c for c in controls if c["kind"] in ("simple","structured_hard")]
        self.assertEqual(len(inscope),60)
        self.assertEqual(len({c["plaintext_id"] for c in inscope}),32)
        self.assertEqual({c["plaintext_group"] for c in inscope},{"thematic","neutral"})
        bank=p.validate_bank(p.load_json(runner.ROOT/"bank.json"))
        absent=[c for c in controls if c["kind"]=="bank_absent"]
        self.assertEqual(len(absent),12)
        self.assertNotIn(absent[0]["plaintext"],{r["text"] for r in bank})
        for c in controls:
            t=p.TABLEAU_BY_ID[c["tableau_id"]]
            key=p.encode(c["full_key_AZ"],"AZ")
            self.assertEqual(p.encrypt_key(c["plaintext"],key,t),c["ciphertext"])
            self.assertEqual(p.decrypt_key(c["ciphertext"],key,t),c["plaintext"])

    def test_freeze_binds_audit_to_current_sources(self):
        import run_experiment as runner
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            hashes={}
            for name in runner.AUDITED_SOURCE_NAMES:
                (root/name).write_text("audited synthetic content for "+name)
                hashes[name]=p.sha256_file(root/name)
            audit={"passed":True,"audited_sha256":hashes}
            runner.verify_audited_sources(audit,root)
            with self.assertRaises(ValueError):
                runner.verify_audited_sources({"passed":True},root)
            with self.assertRaises(ValueError):
                runner.verify_audited_sources({"passed":False,"audited_sha256":hashes},root)
            (root/"pilot.py").write_text("changed after audit")
            with self.assertRaises(ValueError):
                runner.verify_audited_sources(audit,root)

    def test_gate_requires_complete_denominators_and_all_thresholds(self):
        import run_experiment as runner
        controls=runner.build_controls()
        rows=[{"kind":c["kind"],"planted_structure":c["structure"],"successful_recovery":True,
               "validation_flags":0,"validation_count":10 if c["kind"]!="running_key" else 0,
               "flagged":c["kind"] in ("simple","structured_hard")} for c in controls]
        self.assertTrue(runner.control_gate(rows)["passed"])
        self.assertFalse(runner.control_gate(rows[:-1])["passed"])
        rows[0]["validation_flags"]=31
        self.assertFalse(runner.control_gate(rows)["passed"])
        rows[0]["validation_flags"]=0
        for row in rows[-2:]:row["flagged"]=True
        self.assertFalse(runner.control_gate(rows)["passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
