# Bounded experiment specification

Specification recorded 18 October 2026. Its text and original results entered
the same Git commit, so repository history does not independently establish
preregistration. The original account of declaration before execution is not
a separate timestamped registration. Future new specifications must be committed
before execution, and each result must reference that prior commit. Motivation: validated K1/K2
periodic substitution and K3 spatial procedures; published K4 width-7/21
observations; K2's corrected endpoint and K3 as literal potential running-key
sources. These motivations select finite tests, not asserted design intentions.
No scoring model or corpus download is used. All 24 crib characters must match.

## ROUTE-001

Identity route: periods 1–96. Ragged-grid widths 7,14,21,24,31,42: eight
row/column-major corner/direction readings per width, plus every inverse and
identity, deduplicated by complete position permutation. Empty cells skipped;
no padding or inserted/deleted characters. For nonidentity routes test periods
1–16, A–Z and KRYPTOS alphabets, C=P+K / C=P−K / C=K−P modulo 26, and
substitution before/after the route. Derive each key-phase constraint from the
cribs; do not enumerate missing phase values. Save compatible partial assignments
and unobserved phases; materialize plaintext only when every phase is known,
then require exact complete re-encryption. Plus/minus models overlap by key
negation; compatible cases are not independent evidence. Maximum 20,000 models,
30 seconds, one process. Twenty seeded synthetic true-model controls.

## RUNKEY-001

Use one declared version: restored-S K2, K3 without external separator, and
concatenated K1 + restored-S K2 + K3; plaintext and ciphertext streams separately.
Remove literal question marks to obtain letter streams. Every contiguous
97-letter window, forward and reversed, no wraparound, no arbitrary extraction.
A–Z and KRYPTOS alphabets; the same three modular equations. At most 30,000
model cases and 30 seconds. Twenty seeded synthetic running-key round trips.
If any actual candidate satisfies all 24 crib letters, run 199 histogram-
preserving shuffled-ciphertext controls and compare the whole-search maximum
crib-match count, not an isolated fitted candidate. No null run is needed if
all candidates fail the hard acceptance criterion. Partial matches are descriptive
only. Reused windows across source streams are recorded as duplicate model cases.

## TRIFID-001

Two fixed 27-symbol cube orders: A–Z + `?` and KRYPTOS + `?`. Standard
three-coordinate fractionation; periods 1–32,42,49,63,97; both transform
directions. Exactly 144 cases, under five seconds. No arbitrary cube ordering,
key search, altered ciphertext, added separator, or padding. Round-trip all
27 symbols and seeded samples containing the 27th symbol. No claim that Sanborn
was taught Trifid or used it in K4.

## STAT-001 (diagnostic calibration only)

Read Bean's paper and define collision statistic as duplicate excess among
ordered ciphertext pairs at a chosen positive lag. Check width 21 independently.
Scan widths 1–48; use 9,999 histogram-preserving shuffles, fixed seed 20261018,
first 4,999 for per-width calibration and remaining 5,000 for evaluation.
Calculate a standardized maximum over all 48 widths using calibration means and
standard deviations and compare with evaluation maxima. Also report a plus-one
empirical tail probability for the fixed width-21 statistic. Approximate Monte
Carlo uncertainty and postselection limits must accompany any numerical result.
Cap 60 seconds and one process; no broad Gromark primer/alphabet search. A
statistical anomaly does not identify its cause or validate a cipher family.

All code uses the standard library; no paid resources, external submissions,
third-party contact, or executable third-party code. Stop on any deadline or
candidate cap and mark the run incomplete. Record code/input hashes, environment,
command, parameters, actual work count, outputs, and exact negative-result scope.
