# STAT-001 cross-version floating-point replay

23 October 2026. Original archived `results/STAT-001.json.gz` is preserved byte for byte, as is its exact integer sample stream. No statistical search family, shuffle seed, draws, tail threshold or reported probability was changed.

Python 3.12.2 and Python 3.9.6 reproduce every integer draw and collision count and exactly the same fixed-width and multiple-width tail decisions. The old strict test fails on derived floating values under 3.12: one sample is `2.015795136647091` versus archived `2.0157951366470908`. The changed SD rounding propagates through subtraction/division to the z maxima; it is not different random data or a different tail count.

The new comparison independently derives each mean and sample variance as rational numbers from integer sums and squares, then rounds variance for square root. Both current and archived derived arrays are checked against that reference. A declared envelope of 16 ULP at scale `max(1, abs(reference))` accommodates the SD/sqrt, subtraction, division and maximum chain; near zero it provides a small absolute bound rather than a meaningless relative error. Means, SDs and z arrays alone use this envelope. Raw draws, counts, seeds, draw partition and tail-result dictionaries retain exact equality. Nonfinite values, changed lengths, an altered integer draw/tail and 1e-9 derived mutations are rejected.

Measured maxima are much smaller than the envelope: Python 3.12 SD differs from the archive by at most one scaled ULP and z maxima by at most two; Python 3.9 matches archived arrays exactly. Both implementations agree with rational moments within two scaled ULP. These receipts concern this finite replay, not a universal error bound for every conceivable statistical calculation. The original production statistical calculation is unchanged.

[Python 3.9 receipt](../results/STAT-CROSSVERSION-014-python39.json), [Python 3.12 receipt](../results/STAT-CROSSVERSION-014-python312.json), [comparison implementation](../experiments/statistical_receipt_compare.py), [mutation controls](../tests/test_statistical_receipt_compare.py).
