"""Synthetic-only equivalence and benchmark tests; never load experiment inputs.

Run: python -m unittest -v test_native
Analytic tables are constructed directly, without training on any text/corpus.
"""
from array import array
from contextlib import ExitStack
import hashlib
import json
import math
from pathlib import Path
import random
import statistics
import time
import tempfile
import unittest
from unittest.mock import patch

import native as native_module

from native import NativeScorer, _crypto, build_native
from reference import (AZ, CRIBS, GROUPS_BANK, KNOWN, TABLEAUX, UNKNOWN,
                       LanguageModel, conditional_nulls, decrypt_key, derive_key,
                       encrypt_key, reference_scores)

ROOT = Path(__file__).resolve().parent
SYNTHETIC_SEED = 5301907


def synthetic_bank(n=1024):
    rng = random.Random(SYNTHETIC_SEED)
    records = []
    for i in range(n):
        letters = [rng.choice(AZ) for _ in range(97)]
        for start, word in CRIBS:
            letters[start:start + len(word)] = word
        records.append({"id": f"synthetic-{i:04d}", "text": "".join(letters),
                        "group": GROUPS_BANK[i % 4], "provenance": "synthetic random letters only"})
    return records[::-1]  # Sorting must be explicit, not inherited accidentally.


def synthetic_ciphertext():
    rng = random.Random(SYNTHETIC_SEED + 1)
    return "".join(rng.choice(AZ) for _ in range(97))


def analytic_model(uniform=False):
    if uniform:
        return LanguageModel([array("d", [-math.log2(26)]) * 26**order for order in range(1, 5)])
    tables = []
    for order in range(1, 5):
        table = array("d")
        for context in range(26**(order - 1)):
            weights = [1 + ((context * 31 + letter * 17 + order * 13) % 97) for letter in range(26)]
            total = sum(weights)
            table.extend(math.log2(w / total) for w in weights)
        tables.append(table)
    return LanguageModel(tables)


class NativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = analytic_model()
        cls.bank = synthetic_bank()
        cls.cipher = synthetic_ciphertext()
        cls.scorer = NativeScorer(cls.bank, cls.model)

    def test_all_1024_by_12_scores_and_full_h_against_reference(self):
        before = time.perf_counter()
        reference = reference_scores(self.bank, self.cipher, self.model)
        reference_seconds = time.perf_counter() - before
        scores, full_h = self.scorer.raw(self.cipher)
        self.assertEqual(len(scores), 1024 * 12)
        score_errors = [abs(a - b["score_bits"]) for a, b in zip(scores, reference)]
        h_errors = [abs(a - b["full_key_cross_entropy"]) for a, b in zip(full_h, reference)]
        self.assertLessEqual(max(score_errors), 1e-10)
        self.assertLessEqual(max(h_errors), 1e-10)
        # Verify every candidate/model native key and both independent crypto directions.
        for i, row in enumerate(reference):
            plain = self.scorer.bank[i // 12]["text"]
            actual = self.scorer.derive_key(plain, self.cipher, i % 12)
            self.assertEqual(actual, row["key"])
            self.assertEqual(_crypto(plain, self.cipher, actual, i % 12), (True, True))
            self.assertTrue(row["full_reencryption"] and row["full_inverse"])
        # Synthetic throughput only: no production bank, corpus, key or ciphertext opened.
        durations = []
        for _ in range(7):
            before = time.perf_counter()
            self.scorer.raw(self.cipher)
            durations.append(time.perf_counter() - before)
        benchmark = {"synthetic_only": True, "training_performed": False,
                     "synthetic_seed": SYNTHETIC_SEED, "candidate_count": 1024, "tableau_count": 12,
                     "ciphertext_length": 97, "primary_scored_letters": 73,
                     "model_tables": "Direct analytic normalized modular weights; no text training",
                     "synthetic_bank_sha256": hashlib.sha256(json.dumps(self.bank, sort_keys=True).encode()).hexdigest(),
                     "synthetic_ciphertext_sha256": hashlib.sha256(self.cipher.encode()).hexdigest(),
                     "native_source_sha256": hashlib.sha256((ROOT / "native053.c").read_bytes()).hexdigest(),
                     "native_wrapper_sha256": hashlib.sha256((ROOT / "native.py").read_bytes()).hexdigest(),
                     "test_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     "reference_seconds": reference_seconds, "native_raw_seconds": durations,
                     "native_raw_median_seconds": statistics.median(durations),
                     "max_absolute_primary_error": max(score_errors), "max_absolute_full_h_error": max(h_errors),
                     "primary_bit_exact_count": sum(e == 0 for e in score_errors),
                     "full_h_bit_exact_count": sum(e == 0 for e in h_errors),
                     "all_12288_keys_and_bidirectional_crypto_checked": True}
        (ROOT / "synthetic_benchmark.json").write_text(json.dumps(benchmark, indent=2, sort_keys=True) + "\n")

    def test_primary_ignores_all_crib_letters_and_context(self):
        perturbed = list(self.cipher)
        for i in KNOWN:
            perturbed[i] = AZ[(AZ.index(perturbed[i]) + 7) % 26]
        original_scores, original_h = self.scorer.raw(self.cipher)
        changed_scores, changed_h = self.scorer.raw("".join(perturbed))
        self.assertEqual(original_scores, changed_scores)
        self.assertNotEqual(original_h, changed_h)
        for model_index in range(12):
            plain = self.scorer.bank[0]["text"]
            k1 = self.scorer.derive_key(plain, self.cipher, model_index)
            k2 = self.scorer.derive_key(plain, "".join(perturbed), model_index)
            self.assertTrue(all(k1[i] == k2[i] for i in UNKNOWN))
            self.assertTrue(all(k1[i] != k2[i] for i in KNOWN))
            self.assertEqual(self.model.score_key(k1), self.model.score_key(k2))

    def test_conditional_nulls_fixed_cribs_and_equivalence(self):
        bank = synthetic_bank(9)
        scorer = NativeScorer(bank, self.model, expected_count=9)
        nulls = conditional_nulls(self.cipher, 3, "synthetic-native-equivalence-only")
        self.assertEqual(nulls, conditional_nulls(self.cipher, 3, "synthetic-native-equivalence-only"))
        for null in nulls:
            self.assertTrue(all(null[i] == self.cipher[i] for i in KNOWN))
            self.assertEqual(sorted(null[i] for i in UNKNOWN), sorted(self.cipher[i] for i in UNKNOWN))
            scores, h = scorer.raw(null)
            rows = reference_scores(bank, null, self.model)
            for i, row in enumerate(rows):
                self.assertAlmostEqual(scores[i], row["score_bits"], delta=1e-10)
                self.assertAlmostEqual(h[i], row["full_key_cross_entropy"], delta=1e-10)

    def test_uniform_model_null_ties_and_lexical_identity(self):
        bank = synthetic_bank(8)
        model = analytic_model(uniform=True)
        scorer = NativeScorer(bank, model, expected_count=8)
        result = scorer.score(self.cipher, details=True)
        self.assertEqual(result["candidate_id"], "synthetic-0000")
        self.assertEqual(result["tableau_id"], min(t.id for t in TABLEAUX))
        self.assertEqual(len(result["ties"]), 8 * 12)
        self.assertFalse(result["unique_top_plaintext"])
        self.assertEqual(result["margin_bits"], 0)
        self.assertAlmostEqual(result["score_bits"], -math.log2(8) - math.log2(12), delta=1e-10)
        self.assertAlmostEqual(result["full_key_cross_entropy"], math.log2(26), delta=1e-10)
        self.assertEqual(len(result["ranking"]), 96)
        self.assertTrue(all(r["full_reencryption"] and r["full_inverse"] for r in result["ranking"]))
        expected_order = sorted((r["id"], t.id) for r in bank for t in TABLEAUX)
        self.assertEqual([(r["candidate_id"], r["tableau_id"]) for r in result["ranking"]], expected_order)
        raw = scorer.raw(self.cipher)
        for null in conditional_nulls(self.cipher, 3, "synthetic-uniform-null-only"):
            self.assertEqual(scorer.raw(null), raw)
        singleton = NativeScorer(synthetic_bank(1), model, expected_count=1).score(self.cipher)
        self.assertTrue(singleton["unique_top_plaintext"])
        self.assertTrue(math.isinf(singleton["margin_bits"]))

    def test_all_alphabet_key_spelling_encryption_and_inverse(self):
        # Every letter occurs on every axis; key labels must use the plaintext axis.
        plain = (AZ * 4)[:97]
        key = ((AZ[11:] + AZ[:11]) * 4)[:97]
        for model_index, tableau in enumerate(TABLEAUX):
            cipher = encrypt_key(plain, key, tableau)
            self.assertEqual(self.scorer.derive_key(plain, cipher, model_index), key)
            self.assertEqual(derive_key(plain, cipher, tableau), key)
            self.assertEqual(decrypt_key(cipher, key, tableau), plain)
            self.assertEqual(_crypto(plain, cipher, key, model_index), (True, True))

    def test_details_ranking_matrices_and_margin(self):
        bank = synthetic_bank(7)
        scorer = NativeScorer(bank, self.model, expected_count=7)
        result = scorer.score(self.cipher, details=True)
        reference = reference_scores(bank, self.cipher, self.model)
        expected = sorted(reference, key=lambda r: (-r["score_bits"], r["candidate_id"], r["tableau_id"]))
        self.assertEqual(result["ranking"], expected)
        for field in expected[0]:
            self.assertEqual(result[field], expected[0][field])
        self.assertEqual(result["margin_bits"], expected[0]["score_bits"] - next(
            r["score_bits"] for r in expected if r["candidate_id"] != expected[0]["candidate_id"]))
        self.assertEqual(result["block_log_probabilities"], self.model.block_log_probabilities(result["key"]))
        scores, h = scorer.raw(self.cipher)
        self.assertEqual([x for row in result["score_matrix"] for x in row], list(scores))
        self.assertEqual([x for row in result["full_key_cross_entropy_matrix"] for x in row], list(h))

    def test_input_validation_and_snapshot(self):
        for invalid in ("A" * 96, "A" * 98, "a" * 97, "A" * 96 + "!", "A" * 96 + "É"):
            with self.assertRaises(ValueError):
                self.scorer.raw(invalid)
        with self.assertRaises(ValueError):
            NativeScorer(synthetic_bank(7), self.model)
        duplicate = synthetic_bank(2)
        duplicate[0]["text"] = duplicate[1]["text"]
        with self.assertRaises(ValueError):
            NativeScorer(duplicate, self.model, expected_count=2)
        with self.assertRaises(ValueError):
            self.scorer.derive_key("A" * 97, self.cipher, 12)
        model = analytic_model(uniform=True)
        bank = synthetic_bank(2)
        scorer = NativeScorer(bank, model, expected_count=2)
        before = scorer.raw(self.cipher)
        model.log_tables[0][0] = -999
        bank[0]["text"] = "Z" * 97
        self.assertEqual(scorer.raw(self.cipher), before)
        model.log_tables[0][0] = float("nan")
        with self.assertRaises(ValueError):
            NativeScorer(synthetic_bank(2), model, expected_count=2)

    def test_crypto_failure_prevents_compact_and_detailed_receipts(self):
        scorer = NativeScorer(synthetic_bank(2), self.model, expected_count=2)
        for details in (False, True):
            for flags in ((False, True), (True, False), (False, False)):
                with self.subTest(details=details, crypto_flags=flags):
                    with patch.object(native_module, "_crypto", return_value=flags):
                        with self.assertRaisesRegex(RuntimeError, "crypto integrity failure"):
                            scorer.score(self.cipher, details=details)
        # A later ranking-row failure also prevents a partial detailed receipt.
        real_crypto = native_module._crypto
        calls = 0
        def fail_later(*args):
            nonlocal calls
            calls += 1
            return (True, False) if calls == 3 else real_crypto(*args)
        with patch.object(native_module, "_crypto", side_effect=fail_later):
            with self.assertRaisesRegex(RuntimeError, "crypto integrity failure"):
                scorer.score(self.cipher, details=True)
        self.assertEqual(calls, 3)

    def test_frozen_loading_never_invokes_compiler_or_replaces_files(self):
        # Inert temp artifacts exercise integrity checks without any experiment data.
        def fixture(root):
            (root / "native053.c").write_bytes(b"synthetic source fixture")
            (root / "native053.so").write_bytes(b"synthetic inert binary fixture")
            compiler = native_module.shutil.which("cc")
            receipt = {"source_sha256": native_module._sha(root / "native053.c"),
                       "binary_sha256": native_module._sha(root / "native053.so"),
                       "flags": list(native_module.FLAGS), "compiler": compiler,
                       "compiler_sha256": native_module._sha(compiler),
                       "compiler_version": "Synthetic hash-bound version fixture",
                       "platform": native_module.platform.platform(),
                       "machine": native_module.platform.machine(), "abi": 1,
                       "source": str(root / "native053.c"), "binary": str(root / "native053.so"),
                       "fast_math": False, "fp_contract": "off",
                       "command_template": [compiler, *native_module.FLAGS,
                                            str(root / "native053.c"), "-o", str(root / "native053.so")]}
            (root / "build.json").write_text(json.dumps(receipt))
            freeze = {"files": {name: native_module._sha(root / name)
                                for name in ("native053.c", "native053.so", "build.json")}}
            (root / "freeze.json").write_text(json.dumps(freeze))
            return receipt, freeze

        def checked_load(root, fail=False, build_dir=None):
            before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            with ExitStack() as stack:
                stack.enter_context(patch.object(native_module, "ROOT", root))
                for target in ("native.subprocess.run", "native.tempfile.NamedTemporaryFile",
                               "pathlib.Path.replace", "pathlib.Path.mkdir", "pathlib.Path.write_text",
                               "pathlib.Path.write_bytes"):
                    stack.enter_context(patch(target, side_effect=AssertionError("Frozen path attempted mutation/compiler: " + target)))
                if fail:
                    with self.assertRaises(RuntimeError):
                        build_native(build_dir)
                else:
                    self.assertEqual(build_native(build_dir), root / "native053.so")
            after = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            checked_load(root)
            checked_load(root, fail=True, build_dir=root / "alternate")
            self.assertFalse((root / "alternate").exists())
            # Every source/binary/receipt hash binding is mandatory and checked.
            for filename in ("native053.c", "native053.so", "build.json"):
                with self.subTest(tampered=filename):
                    fixture(root)
                    (root / filename).write_bytes(b"changed after freeze")
                    checked_load(root, fail=True)
                with self.subTest(missing=filename):
                    fixture(root)
                    (root / filename).unlink()
                    checked_load(root, fail=True)
            # Even hash-consistent fixture receipts cannot bypass environment checks.
            for field, invalid in (("compiler", "/synthetic/missing/cc"), ("compiler_sha256", "0" * 64),
                                   ("platform", "different platform"), ("machine", "different machine"),
                                   ("flags", ["-ffast-math"]), ("abi", 999),
                                   ("compiler_version", "")):
                with self.subTest(environment_mismatch=field):
                    receipt, freeze = fixture(root)
                    receipt[field] = invalid
                    (root / "build.json").write_text(json.dumps(receipt))
                    freeze["files"]["build.json"] = native_module._sha(root / "build.json")
                    (root / "freeze.json").write_text(json.dumps(freeze))
                    checked_load(root, fail=True)
            fixture(root)
            (root / "freeze.json").write_text("malformed")
            checked_load(root, fail=True)
            _, freeze = fixture(root)
            del freeze["files"]["native053.so"]
            (root / "freeze.json").write_text(json.dumps(freeze))
            checked_load(root, fail=True)

    def test_build_receipt_no_fast_math(self):
        binary = build_native()
        receipt = json.loads((ROOT / "build.json").read_text())
        self.assertFalse(receipt["fast_math"])
        self.assertEqual(receipt["fp_contract"], "off")
        self.assertIn("-O3", receipt["flags"])
        self.assertIn("-fno-fast-math", receipt["flags"])
        self.assertNotIn("-ffast-math", receipt["flags"])
        self.assertEqual(receipt["binary_sha256"], hashlib.sha256(binary.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)
