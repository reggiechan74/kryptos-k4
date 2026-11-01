"""Independent, whole-string exhaustive oracle for the synthetic M21 pilot.

Written solely from PROTOCOL.md, without production implementation access.
No source imports from the production encoder, DP, comparator or caches.
This module does not execute a benchmark on import. Counts are input strings,
not distinct transported integers. Empty bitstring has integer value zero.
"""
from collections import Counter
from functools import lru_cache
from itertools import groupby, product


def alphabet(codec: int) -> str:
    if codec in (1, 7, 8, 9, 11, 12):
        return "AB"
    if codec in (2, 6, 10):
        return "ABC"
    if codec in (3, 4, 5):
        return "ABCD"
    raise ValueError("codec must be an integer in 1..12")


def encode(codec: int, text: str) -> str | None:
    """Direct whole-message reference encoder; None means incomplete phrase."""
    symbols = alphabet(codec)
    if any(letter not in symbols for letter in text):
        raise ValueError("input symbol outside fixture alphabet")
    if codec == 1:
        return text.translate(str.maketrans({"A": "0", "B": "1"}))
    if codec in (2, 3, 4, 5):
        words = {
            2: ("0", "10", "11"),
            3: ("1", "010", "011", "00100"),
            4: ("00", "01", "100", "101"),
            5: ("11", "011", "0011", "1011"),
        }[codec]
        return "".join(words[symbols.index(letter)] for letter in text)
    if codec == 6:
        words = (("0", "10", "11"), ("11", "0", "10"))
        # Previous B count determines the table; current B changes the next one.
        return "".join(words[text[:i].count("B") % 2][symbols.index(letter)]
                       for i, letter in enumerate(text))
    if codec == 7:
        # Split into maximal runs. Each pair of B contributes 110, and an odd
        # trailing B contributes 1. A runs map directly to zero runs.
        chunks = []
        for letter, run in groupby(text):
            size = sum(1 for _ in run)
            chunks.append("0" * size if letter == "A"
                          else "110" * (size // 2) + "1" * (size % 2))
        return "".join(chunks)
    if codec == 8:
        words = {"AA": "0", "AB": "10", "BA": "110", "BB": "111"}
        even_end = len(text) - len(text) % 2
        result = "".join(words[text[i:i+2]] for i in range(0, even_end, 2))
        if len(text) % 2:
            result += "0" if text[-1] == "A" else "1"
        return result
    if codec == 9:
        # Decompose whole maximal runs into canonical 3-symbol chunks, followed
        # by a 1- or 2-symbol remainder. This does not simulate encoder states.
        chunks = []
        for letter, run in groupby(text):
            size = sum(1 for _ in run)
            bit = "0" if letter == "A" else "1"
            triples, remainder = divmod(size, 3)
            chunks.extend([bit + "110"] * triples)
            if remainder:
                chunks.append(bit + "1" * (remainder - 1) + "0")
        return "".join(chunks)
    if codec == 10:
        ordering = list("ABC")
        chunks = []
        for letter in text:
            rank = ordering.index(letter)
            chunks.append(("0", "10", "11")[rank])
            ordering = [letter] + [other for other in ordering if other != letter]
        return "".join(chunks)
    if codec == 11:
        bits = "".join("0" if letter == "A" else "1" for letter in text)
        return bits + str(text.count("B") % 2)
    if codec == 12:
        dictionary = {"A": "00", "BA": "01", "BBA": "10", "BBB": "11"}
        chunks = []
        offset = 0
        while offset < len(text):
            for size in (1, 2, 3):
                phrase = text[offset:offset+size]
                # Prevent a short slice near the end pretending to consume size.
                if len(phrase) == size and phrase in dictionary:
                    chunks.append(dictionary[phrase])
                    offset += size
                    break
            else:
                return None
        return "".join(chunks)
    raise AssertionError("validated codec not handled")


def inputs(codec: int, n: int, mode: str = "all"):
    """Enumerate the protocol's domains, preserving empty-input semantics."""
    if n < 0:
        raise ValueError("negative input length")
    symbols = alphabet(codec)
    if mode not in ("all", "first_min", "first_max"):
        raise ValueError("unknown domain mode")
    domains = [symbols] * n
    if n and mode != "all":
        domains[0] = symbols[0] if mode == "first_min" else symbols[-1]
    for letters in product(*domains):
        yield "".join(letters)


@lru_cache(maxsize=None)
def _payloads(codec: int, n: int):
    """Encode each raw input once across domain/header/base/width variants."""
    return tuple((text, encode(codec, text)) for text in inputs(codec, n))


@lru_cache(maxsize=None)
def records(codec: int, n: int, mode: str = "all", header: str = ""):
    """Tuple of (input, complete framed bits, integer) for accepted inputs."""
    if mode not in ("all", "first_min", "first_max"):
        raise ValueError("unknown domain mode")
    if any(bit not in "01" for bit in header):
        raise ValueError("header must be binary")
    wanted = None
    if n and mode != "all":
        wanted = alphabet(codec)[0 if mode == "first_min" else -1]
    result = []
    for text, payload in _payloads(codec, n):
        if payload is None or (wanted is not None and text[0] != wanted):
            continue
        bits = header + payload
        result.append((text, bits, int(bits, 2) if bits else 0))
    return tuple(result)


def digit_count(value: int, base: int) -> int:
    """Actual repeated radix division, independent of threshold comparisons."""
    if value < 0 or base < 2:
        raise ValueError("unsigned integer and base >= 2 required")
    digits = 1
    while value >= base:
        value //= base
        digits += 1
    return digits


@lru_cache(maxsize=None)
def _digit_histogram(codec: int, n: int, mode: str, header: str, base: int):
    return tuple(sorted(Counter(digit_count(value, base)
                                for _, _, value in records(codec, n, mode, header)).items()))


def count(codec: int, n: int, mode: str, header: str,
          base: int, width: int, transport: str) -> int:
    """Count original inputs admitted by actual digit width, not numeric DP."""
    if width < 1 or base < 2:
        raise ValueError("width >= 1 and base >= 2 required")
    if transport not in ("canonical", "fixed"):
        raise NotImplementedError("only canonical and fixed-width positional transport")
    histogram = _digit_histogram(codec, n, mode, header, base)
    if transport == "canonical":
        return sum(multiplicity for digits, multiplicity in histogram if digits == width)
    return sum(multiplicity for digits, multiplicity in histogram if digits <= width)


def attainable_lengths(codec: int, n: int, mode: str, header: str):
    """Independent exhaustive length set to verify production length-only DP."""
    return frozenset(len(bits) for _, bits, _ in records(codec, n, mode, header))


def records_domains(codec: int, domains, header: str = ""):
    """Independent Cartesian oracle for position-specific control domains."""
    symbols = alphabet(codec)
    if any(bit not in "01" for bit in header):
        raise ValueError("header must be binary")
    frozen = tuple(tuple(domain) for domain in domains)
    if any(len(domain) != len(set(domain)) for domain in frozen):
        raise ValueError("domain symbols must not be duplicated")
    if any(letter not in symbols for domain in frozen for letter in domain):
        raise ValueError("domain outside fixture alphabet")
    result = []
    for letters in product(*frozen):
        text = "".join(letters)
        payload = encode(codec, text)
        if payload is not None:
            bits = header + payload
            result.append((text, bits, int(bits, 2) if bits else 0))
    return tuple(result)
