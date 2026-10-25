"""ctypes wrapper for the independent, fixed-family 053 C scorer.

No data is loaded implicitly. ``raw`` returns two candidate-major flat arrays;
``score`` returns a compact winner, or auditable full matrices and ranking.
Candidate rows are sorted by alias, and exact score ties use alias/tableau ID.
"""
from __future__ import annotations

from array import array
import ctypes
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile

from reference import BASELINE, TABLEAUX, validate_bank, validate_ciphertext

ROOT = Path(__file__).resolve().parent
FLAGS = ("-std=c11", "-O3", "-fPIC", "-shared", "-fno-fast-math",
         "-ffp-contract=off", "-Wall", "-Wextra", "-Werror")
AXES = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KRYPTOSABCDEFGHIJLMNQUVWXZ")
TABLE_SIZES = (26, 676, 17576, 456976)
U8 = ctypes.c_uint8
D = ctypes.c_double
U8P = ctypes.POINTER(U8)
DP = ctypes.POINTER(D)


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _freeze_present():
    path = ROOT / "freeze.json"
    # A dangling symlink or unreadable/malformed receipt must not enable builds.
    return path.exists() or path.is_symlink()


def _frozen_native(directory):
    """Verify the frozen artifact without invoking cc or mutating any file."""
    if directory.resolve() != ROOT.resolve():
        raise RuntimeError("Frozen native scorer cannot use an alternate build directory")
    source, output, receipt = (ROOT / name for name in ("native053.c", "native053.so", "build.json"))
    try:
        frozen = json.loads((ROOT / "freeze.json").read_text())
        files = frozen["files"]
        for name in ("native053.c", "native053.so", "build.json"):
            if name not in files or files[name] != _sha(ROOT / name):
                raise ValueError("Missing or changed frozen native file: " + name)
        old = json.loads(receipt.read_text())
        compiler = shutil.which("cc")
        if compiler is None:
            raise ValueError("Frozen compiler is no longer available")
        expected = {"source_sha256": _sha(source), "binary_sha256": _sha(output),
                    "flags": list(FLAGS), "compiler": compiler, "compiler_sha256": _sha(compiler),
                    "platform": platform.platform(), "machine": platform.machine(), "abi": 1,
                    "source": str(source), "binary": str(output), "fast_math": False,
                    "fp_contract": "off",
                    "command_template": [compiler, *FLAGS, str(source), "-o", str(output)]}
        for key, value in expected.items():
            if old.get(key) != value:
                raise ValueError("Frozen native build metadata mismatch: " + key)
        # The recorded version is hash-bound to freeze.json; hashing the actual
        # compiler binary detects version drift without executing the compiler.
        if not isinstance(old.get("compiler_version"), str) or not old["compiler_version"]:
            raise ValueError("Missing frozen compiler version")
    except (OSError, KeyError, TypeError, ValueError) as error:
        raise RuntimeError("Frozen native scorer integrity check failed; rebuilding is forbidden") from error
    return output


def build_native(build_dir=None):
    """Build before freeze only; after freeze verify/load and fail closed."""
    source = ROOT / "native053.c"
    directory = Path(build_dir) if build_dir is not None else ROOT
    # This branch precedes mkdir, compiler execution, and temporary-file creation.
    if _freeze_present():
        return _frozen_native(directory)
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "native053.so"
    receipt = directory / "build.json"
    compiler = shutil.which("cc")
    if compiler is None:
        raise RuntimeError("Existing local C compiler 'cc' is required; none installed")
    compiler_version = subprocess.run([compiler, "--version"], check=True,
                                      capture_output=True, text=True).stdout.splitlines()[0]
    expected = {"source_sha256": _sha(source), "flags": list(FLAGS),
                "compiler": compiler, "compiler_sha256": _sha(compiler),
                "compiler_version": compiler_version,
                "platform": platform.platform(), "machine": platform.machine(), "abi": 1}
    if receipt.exists() and output.exists():
        old = json.loads(receipt.read_text())
        if all(old.get(k) == v for k, v in expected.items()) and old.get("binary_sha256") == _sha(output):
            return output
    with tempfile.NamedTemporaryFile(prefix="native053-", suffix=".so", dir=directory, delete=False) as f:
        temporary = Path(f.name)
    command = [compiler, *FLAGS, str(source), "-o", str(temporary)]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        if _freeze_present():
            raise RuntimeError("Freeze appeared during native build; refusing artifact replacement")
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    expected.update({"source": str(source), "binary": str(output), "binary_sha256": _sha(output),
                     "command_template": [compiler, *FLAGS, str(source), "-o", str(output)],
                     "built_at_utc": datetime.now(timezone.utc).isoformat(),
                     "fast_math": False, "fp_contract": "off"})
    receipt.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    return output


def _letters(text):
    validate_ciphertext(text)
    return (U8 * 97)(*(ord(c) - 65 for c in text))


def _crypto(plaintext, ciphertext, key, model_index):
    """Independent encryption/inverse checks; no reference arithmetic calls."""
    plain_axis = AXES[model_index // 6]
    cipher_axis = AXES[(model_index // 3) % 2]
    op = model_index % 3
    pi = {c: i for i, c in enumerate(plain_axis)}
    ci = {c: i for i, c in enumerate(cipher_axis)}
    encrypted = []
    recovered = []
    for p, c, k in zip(plaintext, ciphertext, key):
        pv, cv, kv = pi[p], ci[c], pi[k]
        if op == 0:
            ev, dv = pv + kv, cv - kv
        elif op == 1:
            ev, dv = kv - pv, kv - cv
        else:
            ev, dv = pv - kv, cv + kv
        encrypted.append(cipher_axis[ev % 26])
        recovered.append(plain_axis[dv % 26])
    return "".join(encrypted) == ciphertext, "".join(recovered) == plaintext


class NativeScorer:
    """Validated immutable snapshots of a bank and its binary64 log tables."""
    def __init__(self, bank, model, expected_count=1024):
        self.bank = tuple(dict(r) for r in validate_bank(bank, expected_count=expected_count))
        if not self.bank:
            raise ValueError("Empty bank")
        if any(not isinstance(r["id"], str) for r in self.bank):
            raise ValueError("Candidate aliases must be strings")
        # Own the arrays: caller mutation cannot silently alter a scorer.
        self._logs = tuple(array("d", row) for row in model.log_tables)
        if tuple(map(len, self._logs)) != TABLE_SIZES:
            raise ValueError("Wrong model table sizes")
        if any(not math.isfinite(x) or x > 0 for row in self._logs for x in row):
            raise ValueError("Log probabilities must be finite and nonpositive")
        self._log_buffers = tuple((D * len(row)).from_buffer(row) for row in self._logs)
        self._bank_buffer = (U8 * (len(self.bank) * 97))(
            *(ord(c) - 65 for row in self.bank for c in row["text"]))
        self._choice = math.log2(len(self.bank)) + math.log2(12)
        self._library = ctypes.CDLL(str(build_native()))
        self._library.cf053_abi_version.argtypes = []
        self._library.cf053_abi_version.restype = ctypes.c_int
        if self._library.cf053_abi_version() != 1:
            raise RuntimeError("Unsupported native scorer ABI")
        self._library.cf053_score_all.argtypes = [U8P, U8P, ctypes.c_size_t,
                                                  DP, DP, DP, DP, D, D, DP, DP]
        self._library.cf053_score_all.restype = ctypes.c_int
        self._library.cf053_derive_key.argtypes = [U8P, U8P, ctypes.c_int, U8P]
        self._library.cf053_derive_key.restype = ctypes.c_int

    def raw(self, ciphertext):
        """Return (scores, full_H), each flat bank-id-major then TABLEAUX order."""
        cipher = _letters(ciphertext)
        count = len(self.bank) * 12
        scores = array("d", [0.0]) * count
        full_h = array("d", [0.0]) * count
        score_buffer = (D * count).from_buffer(scores)
        h_buffer = (D * count).from_buffer(full_h)
        status = self._library.cf053_score_all(cipher, self._bank_buffer, len(self.bank),
                                               *self._log_buffers, BASELINE, self._choice,
                                               score_buffer, h_buffer)
        if status:
            raise RuntimeError(f"Native score failure: status {status}")
        return scores, full_h

    def derive_key(self, plaintext, ciphertext, model_index):
        """Native arithmetic, exposed for independent reference tests."""
        if not isinstance(model_index, int) or not 0 <= model_index < 12:
            raise ValueError("Tableau index must be in 0..11")
        output = (U8 * 97)()
        status = self._library.cf053_derive_key(_letters(ciphertext), _letters(plaintext), model_index, output)
        if status:
            raise RuntimeError(f"Native key derivation failure: status {status}")
        return "".join(chr(65 + x) for x in output)

    def _row(self, flat_index, ciphertext, scores, full_h):
        bank_index, model_index = divmod(flat_index, 12)
        candidate = self.bank[bank_index]
        key = self.derive_key(candidate["text"], ciphertext, model_index)
        reencryption, inverse = _crypto(candidate["text"], ciphertext, key, model_index)
        if not reencryption or not inverse:
            raise RuntimeError("Native scorer crypto integrity failure: "
                               f"candidate={candidate['id']} tableau={TABLEAUX[model_index].id} "
                               f"reencryption={reencryption} inverse={inverse}")
        return {"candidate_id": candidate["id"], "tableau_id": TABLEAUX[model_index].id,
                "score_bits": scores[flat_index], "key": key,
                "full_key_cross_entropy": full_h[flat_index],
                "full_reencryption": reencryption, "full_inverse": inverse}

    def _block_logs(self, key):
        values = [ord(c) - 65 for c in key]
        result = []
        for start, end in ((0, 21), (34, 63), (74, 97)):
            total, context = 0.0, 0
            for pos in range(start, end):
                depth = min(3, pos - start)
                index = context * 26 + values[pos]
                total += self._logs[depth][index]
                context = index % 17576
            result.append(total)
        return result

    def score(self, ciphertext, details=False):
        scores, full_h = self.raw(ciphertext)
        maximum = max(scores)
        def identity(index):
            bank_index, model_index = divmod(index, 12)
            return self.bank[bank_index]["id"], TABLEAUX[model_index].id
        tied = sorted((i for i, value in enumerate(scores) if value == maximum), key=identity)
        selected = tied[0]
        result = self._row(selected, ciphertext, scores, full_h)
        selected_bank = selected // 12
        alternatives = (s for i, s in enumerate(scores) if i // 12 != selected_bank)
        next_plaintext = max(alternatives, default=-math.inf)
        result["margin_bits"] = maximum - next_plaintext
        result["ties"] = [{"candidate_id": identity(i)[0], "tableau_id": identity(i)[1]} for i in tied]
        result["unique_top_plaintext"] = len({i // 12 for i in tied}) == 1
        if details:
            ranking = sorted(range(len(scores)), key=lambda i: (-scores[i], *identity(i)))
            result["score_matrix"] = [list(scores[i:i + 12]) for i in range(0, len(scores), 12)]
            result["full_key_cross_entropy_matrix"] = [list(full_h[i:i + 12]) for i in range(0, len(full_h), 12)]
            result["ranking"] = [self._row(i, ciphertext, scores, full_h) for i in ranking]
            result["block_log_probabilities"] = self._block_logs(result["key"])
        return result
