# Read-only pinned-source literal checker v1

**Independently validated for a deliberately narrow structural extraction task.** This repository-internal quality tool helps catch transcription mistakes; it is not a cryptanalysis algorithm, whole-program verifier or authenticated provenance service.

- Utility: `experiments/source_literal_check.py`
- [Frozen specification](FROZEN-SPEC.md)
- [Method improvement and decision](METHOD-REPORT.md)
- [Independent audit](INDEPENDENT-AUDIT.md)
- [Immutable development and independent evidence](source-literal-checker-v1-evidence.zip), [checksum](SHA256SUMS)

## Use

Python3.10+ and POSIX are required for the CLI resource guards. No external dependencies. Prepare a request JSON with exactly these fields:

```json
{"sha256":"<independently pinned 64-character lowercase SHA256>","provenance":"<source URL and commit pin>","assignment":"ERRnums","key":"shifts_ST","expected":["LQ","OU","EA","IE"]}
```

Run from the repository root:

```sh
python3 experiments/source_literal_check.py request.json pinned-source.py
python3 -m unittest discover -s tests -p 'test_source_literal_check.py' -v
```

The first command reads explicit request/source files and emits JSON. Exit0/PASS means **only the selected structural literal matches**. Exit2/FAIL means do not rely on the extraction. The source hash is checked exactly; the provenance string is recorded as supplied, not independently authenticated. Preserve the request and result with the source pin. Never replace a trusted pin/hash merely to accept an edited source.

## Exact support and limitations

The selector requires one direct module-level plain assignment, a dictionary, one selected literal string key, and a single unfiltered non-async list comprehension or exact `tuple(GeneratorExp)` wrapper. Its iterable must be a tuple/list of literal strings. **Every key in the selected dictionary must itself be a string literal**, including unrelated keys. Unsupported/dynamic keys and selected iterable expressions fail closed. Many lexical rebinding/direct-write forms are conservatively rejected.

The comprehension body is not interpreted. Tuple-name shadowing, aliases, `update()` calls, reflective mutation, imported alphabets and later runtime behavior are **not verified**. A PASS does not say a program computes those values, is harmless to execute, or has the claimed cipher semantics. Never execute external code on the strength of this receipt. These boundaries have explicit adversarial tests.

The CLI sets2CPU-second/256MiB process limits and bounds source bytes, AST nodes/depth and request size. In-process `verify()` does not establish OS limits. The audit observed these configured guards and tested bounded inputs; actual OS exhaustion was not forced. Supplemental injected exceptions are not evidence of real resource exhaustion behavior.

## Evidence and reproduction

The compact archive contains the original frozen utility/spec/development tests, the separately frozen independent fixtures, author/runner code, raw requests/results, actual-source hash-only supplement and error-path diagnostics. It does **not** contain the third-party motivating source file. Historical runners retain their original absolute paths to preserve provenance; the repository test provides a portable replay against the byte-identical utility and archived81synthetic fixtures plus3malformed-request cases. These replays are not newly blinded evidence. To replay the nonblind actual-source supplement, fetch the specified pinned source independently and verify its recorded checksum first.

Any syntax extension or stronger semantic claim needs a new specification/version/freeze and a fresh independently authored holdout. Keep this v1 and its original failure motivation unchanged.
