# Historical CSP-889 mechanism: bounded result

23 October 2026. None of the 13,520 preregistered starting-key descriptions matches EASTNORTHEAST. No key reaches the public Berlin check and no candidate plaintext is retained. This is **not an exhaustive SIGABA exclusion**.

The implemented variant is CSP-889 / ECM Mark II, with the real three-bank electrical/control mechanism and the published simulator wiring set. CSP-2900, other wheel orders/orientations, independent unrestricted starts, and unknown wartime wiring permutations are outside coverage. The older SIGABA-inspired experiment used custom collectors and wheels; its result is not counted again here.

## Validation and provenance

All twelve external known-answer vectors reproduce exactly in both directions, covering 100–130 characters, nonzero positions, reversed cipher/control/index wheels and scrambled wheel orders. The fixtures were published in CrypTool's test suite, attributed to Geoff Sullivan's simulator. This establishes agreement with independently published simulator outputs, not a hardware transcript or proof of Sanborn use. Sources and normalized/original fixture settings are retained in [the data](../data/sigaba-csp889-v1.json), with source hashes and the [frozen protocol](SIGABA-CSP889-SPEC.md).

An initial control run failed before K4 evaluation. The original experimental plugin numbers one wheel as 10 where the modern table calls it 1, and uses opposite control-wheel and position-string orders. Reading that source supplied an explicit translation. All twelve input/output strings are unchanged; both original and translated settings are saved. No K4-driven convention fitting occurred. The specification's convention correction precedes actual evaluation.

The old source explicitly describes the large-wheel permutations as simulator choices, not recovered secret historical wheel wirings. The index wirings and machine architecture have a different evidential status. Therefore the result concerns a historical mechanism using that reproducible public wiring set, not all original machines.

Additional controls: 14,520 per-position/per-symbol inverse and physical-contact-set checks, including reversed insertions; three 805-step schedule checks against independently expressed counter/contact calculations; unrelated-message roundtrips; four complete-selector literal-crib plants; constant-ciphertext and mutated-vector negatives. All four plants retain their planted key and one compatible plaintext in this fixture; that is not a general uniqueness theorem.

## Search accounting

Two fixed layouts × 26 common cipher starts × 26 fast-control starts × 10 common index starts = 13,520 raw descriptions. There are 520 distinct 97-position stepping schedules, and 13,520 schedule/start descriptions. All 13,520 actual full-decryption SHA-256 values are distinct; this is a fingerprint-based count, not a formal collision-free theorem about all inputs. No global equivalence of encryption functions is asserted.

Every setting fails the first crib: 13,010 first fail at position 22, 489 at 23, 20 at 24 and one at 25. State propagates continuously from position 1; no state is invented at a crib boundary. Every mismatch is retained in [the result](../results/SIGABA-CSP889-001.json). The [control receipt](../results/SIGABA-CSP889-001-controls.json) is separate. No significance simulation was needed and no score-based partial lead is claimed.

Reproduce:

```sh
python3 experiments/sigaba_csp889.py --controls --output /tmp/csp889-controls.json
python3 experiments/sigaba_csp889.py --actual --output /tmp/csp889-actual.json
```

The domain is deliberately modest and historically unmotivated at the key level. A useful next step needs independent key/wheel restrictions, rather than treating more random starting settings as evidence. Exact mechanism validation is progress in tooling; this search produced no K4 lead.
