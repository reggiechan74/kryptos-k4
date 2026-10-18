"""Deterministic baseline validation; no cryptanalytic search or network access."""
import hashlib
import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "k4.json"


def one_based_slice(text, start, end):
    """Return an inclusive, one-based range; reject invalid bounds."""
    if not 1 <= start <= end <= len(text):
        raise ValueError("range must satisfy 1 <= start <= end <= text length")
    return text[start - 1:end]


def validate(data):
    ciphertext = data["ciphertext"]
    if len(ciphertext) != 97 or data["length"] != 97:
        raise ValueError("K4 must contain exactly 97 letters")
    if not ciphertext.isascii() or any(c < "A" or c > "Z" for c in ciphertext):
        raise ValueError("ciphertext must contain only ASCII uppercase A-Z")
    if data["indexing"] != "one-based inclusive":
        raise ValueError("unexpected indexing convention")
    expected = [(22, 34, "EASTNORTHEAST"), (64, 74, "BERLINCLOCK")]
    actual = [(c["start"], c["end"], c["plaintext"]) for c in data["cribs"]]
    if actual != expected:
        raise ValueError("cribs differ from the supplied confirmed baseline")
    seen = set()
    for start, end, plaintext in actual:
        segment = one_based_slice(ciphertext, start, end)
        if len(segment) != len(plaintext):
            raise ValueError("crib length and interval disagree")
        positions = set(range(start, end + 1))
        if seen & positions:
            raise ValueError("overlapping crib intervals")
        seen |= positions
    return ciphertext


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    ciphertext = validate(data)
    print("PASS: 97 uppercase ASCII letters; 2 consistent one-based crib intervals")
    print("ciphertext SHA-256:", hashlib.sha256(ciphertext.encode("ascii")).hexdigest())
    for crib in data["cribs"]:
        start, end = crib["start"], crib["end"]
        print("{}-{}: {} -> {} (Python [{}:{}])".format(
            start, end, one_based_slice(ciphertext, start, end),
            crib["plaintext"], start - 1, end))


if __name__ == "__main__":
    main()
