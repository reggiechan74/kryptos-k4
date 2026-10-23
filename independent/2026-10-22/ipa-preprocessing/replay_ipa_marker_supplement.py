#!/usr/bin/env python3
"""Post-audit check only; does not alter the frozen main protocol or results."""
import json
from pathlib import Path
root = Path(__file__).resolve().parent
proof = json.loads((root / "ipa-first-crib-marker-supplement.json").read_text())
ipa, cipher, alphabet = "iːstnɔːrθiːst", "FLRVQQPRNGKSS", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
required = []
for ordinary, marker in [(22, 32), (33, 23)]:
    oi, mi = ordinary - 22, marker - 22
    assert (ordinary - marker) % 10 == 0
    assert ipa[mi] == "ː"
    key = (alphabet.index(cipher[oi]) - alphabet.index(ipa[oi].upper())) % 26
    required.append((alphabet.index(cipher[mi]) - key) % 26)
assert required == [13, 11]
assert required == [r["required_marker_alias_index"] for r in proof["proof"]]
assert len(set(required)) == 2
print(json.dumps({"status": "pass", "supplementary_post_audit_check": True,
                  "required_marker_alias_indices": required,
                  "single_global_marker_encoding_contradicted": True}, indent=2))

