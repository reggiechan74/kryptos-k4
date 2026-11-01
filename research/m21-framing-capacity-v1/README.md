# M21: exact framing-capacity counting — synthetic method validated

**Result:**24,624 synthetic cases and132 controls passed, with zero exact-count mismatches or false pruning against an independent exhaustive oracle. This is a **method validation**, not a fourth K4 target experiment, a cipher-family exclusion, or a new mathematical primitive. K4 target coverage remains3tested/97unrun.

## What it does
A deterministic finite-state bit encoder is composed with exact integer-interval comparisons. The resulting dynamic program counts plaintext strings that fit a declared radix-width/framing contract. Zero count excludes only that specific model/domain. A positive count is not evidence of compatibility with actual ciphertext. See [method and proof](METHOD.md), [finite protocol](PROTOCOL.md), and [static applicability/gaps](NEXT-APPLICABILITY.md).

This instantiates established weighted-automaton/regular-constraint counting; primary sources and the distinction from local Compression043/EXT-024 are in METHOD.md. Twelve fixtures are classical coverage adapters, not twelve novel cryptanalytic mechanisms.

## Results and limitations
| Measurement | Result |
|---|---:|
| Complete matrix |24,624/24,624 |
| Mandatory controls |132/132 |
| Count mismatches / false pruning |0 /0 |
| Additional zero-count cases beyond strong exact-length baseline |1,930 |
| Additional zero-count cases beyond weak length baseline |8,453 |
| Cases where all methods agree |16,171 |
| Child CPU / wall seconds |4.11879517 /4.12233698 |
| Peak RSS |43,440KiB |
| DP states / transitions / bit work |375,129 /761,882 /1,301,302 |
| Aggregate DP case CPU / cached-oracle CPU |2.313976845 /0.507157471 |

**The DP was slower in aggregate than the cached oracle on this tiny matrix.** These timings do not compare uncached algorithms: the oracle reuses encodings and digit histograms. No general speedup,97-symbol scalability or adaptive-compression tractability follows. Cases are correlated; fixtures2/6/10 share aggregate feasibility counts. Strengthened baseline uses a nonzero leading-bit guarantee only where the declared header supplies it. Entropy is diagnostic, never a sound per-message rejector.

The one bounded execution completed with external exit0, supervisor status0 and empty stderr. Limits were180childCPU seconds,240wall seconds and1GiB address space. [Independent readback](results/INDEPENDENT-READBACK.md) checked every retained row/control, exact manifest, baseline decisions, aggregate totals and frozen hashes without rerunning the experiment.

## Evidence and provenance
- [Complete compressed case rows](results/cases.jsonl.gz): lossless gzip of all24,624 rows; uncompressed SHA256 `8a1810a8f6aa7cf4b7fab9bc8b94b4ba46548805dab19faba0833b2abdca9b0c`.
- [Controls](results/controls.json), [summary](results/summary.json), [per-codec aggregation](results/by-codec.json), stdout/stderr and supervisor status retain the full outcome.
- [Compressed input manifest](inputs/cases.json.gz) expands to the exact frozen24,624-case JSON.
- `code/` contains byte-identical production DP, independently authored oracle, runner and supervisor used for the run. The oracle was written without reading production and uses independent whole-string encoders and repeated radix division.
- [Publication map](provenance/PUBLICATION-MAP.json) maps source/result hashes and lossless compression, and identifies administrative omissions. [Original frozen hashes](provenance/original-frozen-input-hashes.json) retain historical provenance; some corresponding administrative documents/runtime paths are intentionally not published. Public explanatory documents are labeled derivatives, not silently substituted frozen originals.
- [Runtime metadata](provenance/runtime-public.json) retains interpreter version/binary hash/flags, with local interpreter path removed. This is not a complete standard-library/shared-library environment digest. Isolated mode ignores PYTHONHASHSEED; no fixed hash-seed claim.

The archived runtime-bound supervisor is evidence, **not an out-of-box portable rerun command**: its original machine binding and administrative freeze are intentionally not reproduced as an executable public setup. Any future reproduction requires a newly reviewed portable binding and an explicit new finite protocol, rather than silently editing old frozen receipts. Original files remain unchanged in the research archive. No third-party source bodies or private coordination records are included.
