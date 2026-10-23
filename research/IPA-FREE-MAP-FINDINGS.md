# Free IPA glyph values with periodic additive keys

23 October 2026 UTC.

All 24 frozen structures are incompatible with the two disclosed windows. Removing
the previous ordinary-letter identities does not rescue this bounded IPA model.
Ten structures fit the first block, with substantial ambiguity, but none survives
the second block and global injectivity. No full plaintext or alphabet was chosen.

## Scope and chronology

The [protocol](IPA-FREE-MAP-SPEC.md) was committed at bbe781b before local K4
comparison; implementation and controls at 633bb94 preceded the actual run.
The same source-fixed R2 IPA strings and unchanged offsets are used. Every one
of the fourteen observed glyphs now has a free, globally shared injective value
in 0–25. No Latin identity remains fixed. The first stage contains only its eight
observed glyphs; six more enter with the second block.

The equation is C=f(g)+k_phase modulo 26, periods 1–12, in AZ or KRYPTOS
ciphertext coordinates: 24 canonical structures. Negating the entirely free f
makes true Beaufort equivalent, so it is not counted again. Key phase is
redundant. Fixing f(i)=0 removes one common translation gauge; it does not assert
that IPA i historically encoded A. Every gauge-fixed description represents
26 numeric map/key descriptions with the same cipher behavior.

This is a necessary model for the observed glyph subset, not a universal IPA
alphabet. Global 97-character phonetic alignment and exact English spelling
reconstruction remain unproved. Current Cambridge notation is an operational
input, not evidence of the creator's method. Prior period restrictions and the
independent audit were known; no blind or global novelty claim is made.

Eighteen of these structures were already excluded by the prior two-window
mapping-independent periodic injectivity checks. All 24 were evaluated here to
preserve exact staging and counting. The six cases at periods 8,11,12 add the
stronger shared additive-map constraints to those earlier vacuous survivors.
The 24 raw structures are not 24 new independent statistical tests.

## Exact representation of every solution

Set q_phase=−k_phase. Every observation gives a graph edge f(g)−q_phase=C.
Exact modular potentials determine only within-component differences. Cycles
must close; equal relative values for distinct glyphs in a component violate
injectivity. Across components, translated glyph-value sets must be disjoint.
Phase values themselves need not be distinct.

The counter fixes one global gauge, enumerates multi-glyph component translations
with memoized bit masks, and multiplies by the falling factorial for the labeled
remaining singleton components. Translations yielding the same occupied mask
retain their multiplicity because they can assign different values to labeled
glyphs. Complete component templates and translation rules describe all solutions;
zero offsets in separate components are never treated as a completed alphabet.

## First-stage ambiguity

Periods 1–6 and 9 fail within the first block in each alphabet. The remaining
counts below are exact injective map/key descriptions after fixing the gauge:

| Period | Training components | AZ descriptions | KRYPTOS descriptions | Free component offsets before injectivity |
| ---: | ---: | ---: | ---: | ---: |
| 7 | 2 | 14 | 13 | 1 |
| 8 | 3 | 380 | 380 | 2 |
| 10 | 5 | 175,560 | 175,560 | 4 |
| 11 | 6 | 3,862,320 | 3,862,320 | 5 |
| 12 | 7 | 96,909,120 | 96,909,120 | 6 |

All five surviving training graphs are forests: their thirteen observations fit
independent combinations of mapping and key values with zero redundant algebraic
cycle checks. Injectivity restricts the remaining offsets but does not turn the
thirteen fitted letters into thirteen predictions. Ungauged counts are 26 times
the table entries. A training description has 18P6 possible injective assignments
to the six unseen glyphs before Berlin constraints; those variables are not
included prematurely in the first-stage counts.

## Second-stage constraints and exact failures

Every training-compatible structure fails when the second block is included.
Seven fail modular cycle closure; three have consistent linear potentials but
force two distinct IPA glyphs to the same value. Exact cycle paths and collision
certificates are retained in the complete results.

| Period | Full components | Training-component joins | New glyph values | Additional joint cycle checks |
| ---: | ---: | ---: | ---: | ---: |
| 7 | 1 | 1 | 6 | 4 |
| 8 | 1 | 2 | 6 | 3 |
| 10 | 1 | 4 | 6 | 1 |
| 11 | 1 | 5 | 6 | 0 |
| 12 | 3 | 4 | 6 | 1 |

The six first observations of new glyphs fit parameters. Component joins spend
relative offsets; later closures can involve those newly fitted values. This is
not eleven independent Berlin predictions. For the three positions using glyphs
already seen in training (66,69,73), all 26 possible ciphertext values are counted
under the entire injective training solution set. Each marginal sums to the
training count; no different favorable witness is selected per position.

Examples make the failures inspectable:

- AZ period 8 forces I at position 66 and L at 73 from the first block; actual
  ciphertext is P at both positions. These predictions are invariant over all
  380 injective training descriptions.
- Period 10 must repeat ciphertext L for the same length marker at positions
  23 and 73 in the same phase; actual position 73 is P.
- Period 11, in either alphabet, forces IPA i and ɑ to have equal values, violating
  injectivity. This is an injectivity failure despite zero additional cycle checks.
- KRYPTOS period 12 forces i and n equal. AZ period 12 instead fails a cycle.

Berlin remains public, historically used evidence rather than an untouched
holdout. Zero complete compatible descriptions remain in every tested structure;
there are no budget-unresolved cases. No empty-set prediction or full-message
multiplicity is claimed. No null significance simulation is needed for an exact
family rejection, and these description counts are not probabilities.

## Controls and reproduction

The controls include 45 complete small-ring comparisons against independently
enumerated gauge-fixed glyph maps, including disconnected components, collisions,
impossible packing and translation-symmetric occupied sets. Twenty-four literal
IPA-window plants retain their true descriptions and pass fixed-model full
round trips. Every plant also checks all 26 common translation gauges. Exact
prediction marginals and the new-variable/closure accounting are tested.

```sh
python3 experiments/ipa_free_map.py controls
python3 experiments/ipa_free_map.py actual
python3 -m unittest discover -s tests -v
```

The [full local result](../results/IPA-FREE-MAP-001.json) preserves every structure,
source hashes, raw edges, components, counts, exact prediction marginals and
certificates. [Controls](../results/IPA-FREE-MAP-001-controls.json) are separate.
An independent native replay is being supplied and will be recorded separately;
it is not yet claimed in this local report. No codec, period, route, notation or
mapping rule was added after the failures. The bounded family stops here.

At the local pre-native milestone, all 285 repository tests pass in 11.782 seconds.
