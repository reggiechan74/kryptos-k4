# DYNAMIC-KEY-001: bounded stateful-key tests

22 October 2026. **Zero compatible models in 1,344 configurations. No plaintext
candidate or solution.** A controlled local progressive-key replication and a
specific ciphertext-dependent cursor rule both contradict the fixed public cribs.
These conclusions cover only the frozen alphabets, equations, periods and rules.

The active Mac mini checkout was clean at `6af8caadff18`, on `main`, with its
recorded remote one commit ahead and one behind. No fetch, push, merge, history
rewrite or unrelated edit was performed. Work is on local branch
`research/dynamic-key-20261022`. No applicable AGENTS.md or software-engineering
skill was available. The research policy, ledgers, prior-art review and landmark
findings were inspected before changes. No geographic counts were retested.

## Design and chronology

[Specification](specifications/DYNAMIC-KEY-001.json) committed first:
`4f0c056ee633828e88af89f9f6e066cf250a3606`.
Implementation and six synthetic/control tests committed next:
`11bc39f705ed24d1d591f0746f8217d78d39bb6f`.
One actual run then completed in **4.228 seconds** against a 60-second limit.
268,800 configuration evaluations include the actual ciphertext and 199 complete
shuffled reruns. Standard library, one process, no key-word enumeration.
The specification is preserved unchanged, including its original ranking.

A transport disconnect occurred before the first attempted code commit/run.
Read-only Git and result-directory checks established that neither had started;
the command was retried with the full specification SHA. Exactly one actual run
exists. A progress-message tool later returned `Transport closed`; its delivery
is uncertain, without effect on the saved local work.

The verified 97-letter fixture and 24 known plaintext positions are unchanged.
The existing K1–K3 controls ran before the experiment. Both models use A–Z or
KRYPTOS alphabets; C = sigma*P + K mod26 with sigma +1 or -1. C=P-K is redundant
under arbitrary key negation. Global cursor origin is absorbed by phase keys.
No routes, keyword lists, added symbols or shifted cribs were introduced.

- Progressive cycle: K_i = base[i mod p] + d*floor(i/p), periods 1–12,
  steps 0–25, both signs and alphabets: **1,248 configurations**.
- Ciphertext extra step: cursor starts0, advances by 1 plus 1 after a ciphertext
  vowel (AEIOU), or after a consonant (the other 21 letters); periods 1–12,
  both signs and alphabets: **96 configurations**. Updating after the ciphertext
  symbol makes encryption and decryption deterministic. No plaintext triggers,
  pause rules or resets were tested.

Each crib pair implies one required base-key value. Two different values at the
same phase are an exact contradiction. Every rejected configuration retains its
first conflicting positions and required values; independent artifact tests
recompute all 1,344 certificates. Occupied/free phases and equality checks are
recorded. Free parameters are never filled arbitrarily.

## Results and controls

| Family | Cases | Fits to first 13 letters | Compatible with all 24 | Best fitted agreements/24 |
| --- | ---: | ---: | ---: | ---: |
| Progressive | 1,248 | 4 | 0 | 14 |
| Ciphertext extra step | 96 | 0 | 0 | 14 |

All four first-crib fits have period 12. Their Berlin predictions are fully
checkable, with **1,0,1,0 matches out of 11**, respectively:

| Alphabet | sigma | step | Berlin matches | First contradiction positions |
| --- | ---: | ---: | ---: | --- |
| AZ | +1 | 24 | 1/11 | 28,64: required keys 2,22 |
| AZ | -1 | 2 | 0/11 | 28,64: required keys 2,4 |
| KRYPTOS | +1 | 1 | 1/11 | 28,64: required keys 0,6 |
| KRYPTOS | -1 | 13 | 0/11 | 28,64: required keys 4,14 |

For each shuffled ciphertext, both entire parameter families were rescanned.
The statistic is the largest possible same-data crib agreement after selecting
the modal required key in each phase. It deliberately accounts for fitting the
key and choosing the best configuration; 14 partial matches are not evidence.
Seed 20261022, Python random.Random/MT19937; fresh original histogram each draw.

| Statistic | Observed | Null draws equal/higher | Plus-one conditional tail |
| --- | ---: | ---: | ---: |
| Progressive family maximum | 14 | 199/199 | 1.00 |
| Extra-step family maximum | 14 | 111/199 | 0.56 |
| Maximum across both families | 14 | 199/199 | 1.00 |

Progressive null maxima:14(58),15(118),16(22),17(1).
Extra-step null maxima:12(6),13(82),14(96),15(15).
These are exploratory, histogram-conditioned shuffle diagnostics, not discovery
p-values or probabilities that a historical mechanism is true. The resolution
is 1/200; the models overlap and are correlated. The calibration covers both
families searched here, not all prior research. Both crib blocks were public
before model design: withholding Berlin during key fitting creates a useful
prediction check, not independently obtained plaintext evidence.

288 synthetic cases cover both families, both signs/alphabets, all 12 periods and
multiple steps. All round-trip through a separate sequential transform, satisfy
the planted constraints, and reject an altered known-letter constraint. Manually
computed stepping/progression examples and exhaustive toy key-score comparison
pass. The full existing suite plus initial new tests passes **147 tests, 8.705s**.
Three additional saved-artifact tests pass **3 tests, 0.097s**, verifying hashes,
commit chronology, every conflict and null/holdout accounting without rerunning
the experiment. No test failures occurred.

## Prior-art correction and currently ranked hypotheses

The original specification ranked progressive cycles first. After execution,
the parent's independent researcher identified additional pinned prior art.
Direct static reads confirm [cokernel.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/cokernel.py)
constructs progressive design matrices for periods 1–26 and filters by at least
8 independent checks by default. Our periods 1–12 have at least 11 checks when
the unknown progression step is included, so they do **not** close that
check-threshold gap. [gap1.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/gap1.py)
uses those matrices in a mixed-alphabet scan; its literal AZ/AZ and KRYPTOS/KRYPTOS
coverage depends on the imported alphabet catalog, not fully inspected here.
No third-party executable was run, and no claim of exhaustive published-output
replication is made. Progressive cycles are **known prior art and local controlled
replication**, not a genuinely new mechanism or cryptanalytic discovery. This
correction does not alter the frozen test or results. Avoid further progressive
sweeps without independent motivation.

The three distinct hypotheses retained for the next research decision are:

1. **H-ASYMMETRIC-FEEDBACK (unrun, highest next priority).** Independently choose
   plaintext, ciphertext and feedback symbol orders from AZ/KRYPTOS. With
   C_index=sigma*P_index+tau*K_index mod26, interpret output through the ciphertext
   order; a feedback character is reindexed through the key order, never silently
   reused as its plaintext/ciphertext ordinal. Test PT or CT feedback at lags 1–12,
   three conventional equations, six alphabet triples excluding the two fully
   identical triples: 432 configurations. This changes the same-alphabet assumption
   of AUTOKEY-CONSTRAINT-001 and is not a consequence of Berlin wordplay. For PT
   feedback, enumerate 26 primer values per independent lag lane and propagate
   deterministically, intersecting every known-letter constraint; CT feedback is
   directly determined beyond the primer. Report allowed lane seeds and product
   of surviving counts, free lanes and predictions; compatibility remains
   underdetermination. Require a new committed specification, independently
   implemented symbol conversion, synthetic planted/mutated controls and full
   same-budget shuffle calibration before any actual run. Reject the precise
   model if any lane has no seed satisfying all its constraints. The earlier
   affine same-alphabet proof cannot simply be reused across reindexing.
2. **H-CIPHERTEXT-EXTRA-STEP (new local rule, tested negative).** The exact two
   class-triggered after-letter extra-step rules above. The earlier inspected
   interrupted-key source uses single/pair triggers and advance/pause; our
   separate rule is not claimed absent from all literature. This experiment
   rejects all 96 declared cases. Unknown triggers, variable increments and new
   alphabets require independent motivation, not rescue tuning.
3. **H-AFFINE-DIGRAPH (originally unrun; analytically excluded, 23 October 2026).** Fixed invertible 2x2 affine
   substitution modulo26, AZ or KRYPTOS, pair origins 0 or 1, one edge symbol copied.
   Solve rows on complete EASTNORTHEAST pairs, require determinant coprime26,
   predict Berlin then require all 24 letters and full 97-character inverse. Contradiction of
   all admissible matrices rejects this precise model. Test known matrices,
   boundary behavior and altered heldout letters, with full-family null controls.
   No K4-specific pair signal or attested teaching supports ranking it higher.
   **Current status:** the four same-alphabet/origin cases are excluded by
   [exact parity certificates](AFFINE-DIGRAPH-PARITY-BOUNDARY.md), without key
   enumeration and even without requiring invertibility. The test design above
   is preserved as the historical proposal, not a remaining unrun candidate.

These are speculative mechanisms, not claims of invention. The new directions
are exact assumptions that can fail. None is supported just because older
models failed. Historical clock-face orientation, asymmetric feedback and
plaintext-triggered interruption must remain separate mechanisms. Plain
Wheatstone is already prior art and is not offered as a new test.

## Reproduce

From the active repository:

```sh
python3 -m unittest discover -s tests -p 'test_dynamic_key*.py' -v
python3 experiments/dynamic_key.py --spec-commit 4f0c056ee633828e88af89f9f6e066cf250a3606
```

The runner uses existing atomic RunSnapshot infrastructure and verifies that
all consulted files match its recorded code commit. It writes a new immutable
run directory, preserves the earlier one and marks timed-out attempts incomplete.
The recorded code version is 11bc39f705ed24d1d591f0746f8217d78d39bb6f.
The three certificate tests were added afterward; original consulted files were
unchanged. A new run is unnecessary to audit these results.

[Full result and per-model certificates](../results/dynamic-key-runs/20261022T120128Z-c15ba5ffeb55479490d2be553daf60f0/DYNAMIC-KEY-001.json),
[atomic manifest](../results/dynamic-key-runs/20261022T120128Z-c15ba5ffeb55479490d2be553daf60f0/manifest.json).
The next recommended experiment is the narrowly defined asymmetric-feedback
constraint audit, after checking the parent's forthcoming exact prior-art scope.

## Subsequent fixed pilots — 22 October 2026

The asymmetric-feedback recommendation above was subsequently tested in a
separate six-case PALIMPSEST/lag-10/addition pilot; all six cases fail. A final
12-case plaintext-driven extra-step pilot also fails. The separate
[fixed-pilot findings](FIXED-PILOT-FINDINGS.md) record complete outputs, controls,
prior-art gaps, shuffle diagnostics and the updated ranking. The broader
72-case arbitrary-primer specification remains deferred and unrun.
