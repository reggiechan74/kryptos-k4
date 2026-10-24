# Item 8: frozen one-edit counterfactual robustness study

24 October 2026 UTC, before modified-K4 evaluation. User explicitly requests testing without an observed K4 discrepancy. This is not a claim of engraving/transcription error, a proposed canonical correction, or transfer of K1/K2/Projector algorithms to K4. Keep data/k4.json byte-for-byte unchanged.

## Existing proposal and exact channel

Source: independent/2026-10-22/construction/REPORT.md §4. For observed O of length97: baseline1; substitute one observed cell by another A–Z letter97*25=2425; insert one intended latent ciphertext letter at any gap98*26=2548; delete one extra observed cell97. Total5071 raw descriptions. At most one event, no transposition, key-entry error, reset, combined edits or guessed phrase.

Repair produces latent L of length97/98/96. The tested ciphers are length-preserving between latent plaintext P and L, so P's length is len(L). These latent lengths are counterfactual, not changes to observed K4. Record raw descriptions and unique L strings separately. Deduplicate computation only by (L, complete known-position mask), retaining every edit/alignment alias.

- baseline/substitution: observed and latent indices identical. Forward channel changes the latent cell back to the original observed symbol for substitution.
- insert_latent at gap g=0..97: L=O[:g]+b+O[g:]. Observed i maps to latent i+[i>=g]; latent g has no observed partner. Forward channel removes latent g.
- delete_observed at i=0..96: L omits O[i]. That observed cell has no latent partner; later indices shift down one. Forward channel reinserts the original observed symbol at i.

P_j always encrypts to L_j before this channel. Store explicit bidirectional index maps; never discard a contradictory known letter or infer an edit stage/intent from a fit.

## Two predeclared coordinate interpretations

A ENGLISH_FIXED is primary: the complete English phrases remain at zero-based21..33 and63..73 in latent P. No phrase is moved. This models the published numbers as intended-English coordinates, even if an observed ciphertext channel shifts their corresponding cells.

B OBSERVED_CELL_TRANSPORT is a separate conditional interpretation: the same24 letter labels initially attach to observed cells21..33/63..73, and all are transported by the one monotone edit map. Both phrases must remain complete and contiguous. A deleted labelled observed cell or an insertion splitting a phrase makes B alignment-inadmissible, not a cipher rejection. No independent per-island shift, phase reset or missing known letter is permitted. B is not evidence that the published numbers actually mean observed-cell coordinates; B-only fits must not be called fits at the primary English positions. Substitution/baseline A/B may alias exactly. Test boundaries explicitly.

Gross5071*2 alignment descriptions. Expect B to reject24 labelled deletions and22 internal gaps*26 insertion letters=596 descriptions. Record actual admission counts before cipher scoring. No after-outcome alignment variant.

## Complete tested cipher families

P PERMUTATION_ONLY: every permutation of latent positions, no substitution. Exact symbol-budget feasibility is sufficient for arbitrary unknown position permutations. Known plaintext counts must be contained in L. Represent all compatible plaintexts by (length, letter multiset, complete known mask), with exact multinomial plaintext count and exact position-permutation-key count. Keep all classes/aliases, not a guessed route. Emit two deterministic different non-language witnesses where possible, with actual bijective position keys, full latent encryption and forward-channel verification. Do not claim their union count by summing overlapping classes; report compact union and per-class counts/bounds. This tests the old count-deficit exclusion, not optical/clock routes or language plausibility.

V PERIODIC: AZ or KRYPTOS coordinates, C=P+K or C=K−P modulo26, unrestricted periodic keys of periods1..12. Exactly48 structures. C=P−K is an alias under key negation, and free phase is redundant. No mixed input/output alphabets, routes or other state models. Fit all13 first-phrase letters, retain every first fit and key. They cover every phase, so no free entries. Normalize key phase to absolute latent position0 and keep that same key across prefix/gap/second phrase. Apply all11 Berlin constraints without refitting and fully decrypt/re-encrypt any full survivor. Public clues are not untouched evidence. Record smaller-period keys and full-output/edit aliases; descriptions are not independent keys/hypotheses.

Also replay two earlier necessary certificates as DIAGNOSTICS ONLY: nonzero-strip fixed points and the Wheatstone same-adjacent-pair/opposed-cipher-equality contradiction. Losing a certificate does not mean that a physical key exists; no compatible diagnostic is a cipher candidate, and no new historical strip/ring search is counted.

The old E symbol deficit and period12 single-closure weakness were known during design. For period12, changing one first-window endpoint can always satisfy its only redundant equation; baseline handles an already-consistent input. Thus first-stage fit under this edit freedom is guaranteed for arbitrary input, not positive evidence or a blind discovery.

## Controls before K4 scoring

Recheck K1/K2 full construction fixtures and seven retained offline convention controls. Explicitly retain Projector restart/phase-jump equivalence rather than invent a unique physical omission. No new full1133-character source retrieval claim.

Independently generate tagged-token edit maps and compare every5071 description, both directions and forward channel. Complete tiny alphabets/strings verify variant sets, duplicate accounting and index-map distinctions. Exhaustive tiny permutation truth sets/counts and tiny periodic-key enumeration verify complete represented sets, not just planted inclusion. Fixed-model forward/inverse checks across all48 structures and lengths96/97/98.

24 full-selector plants: operations substitution/insert_latent/delete_observed, positions [0,21,22,33,34,63,74,97] (clamp97 to96 for observed-cell operations); global index j=0..23 selects periodic structure floor(j*47/23). Alternate A/B where B is admissible, otherwise A with B rejection recorded. Fixed key k_i=(7*i+3) mod26, fixed pangram filler and complete crib masks at the declared coordinates. Whole combined selector must retain the true edit/key/interpretation; keep all alternate fits and any smaller-period/key aliases. Include endpoints and crib boundaries/internal positions, independent fixed decoder and channel mutations.

## Actual, matched controls and reporting

Evaluate the full5071-description arm including unchanged baseline. Count admissible and inadmissible coordinate cases, unique latent strings, unique (L,mask) instances, all first/full V fits and complete compact P classes. Candidate success requires all24 letters in its declared interpretation and exact full forward-channel regeneration of canonical97 O. No partial-letter score, attractive fragment, post-hoc crib relocation or language ranking.

99 histogram-preserving shuffles, seed280024: rerun the ENTIRE edit/alignment/family selector, including baseline, all variants and discarded cases. Report P compatibility/volume capacity separately from V first/all-fit events. P is deliberately unrestricted; a generic compatibility event is not a cryptanalytic lead. With no partial-score promotion, no partial-score p-value; if a finite V full fit appears, report empirical whole-family exact-fit calibration and ambiguity, not a solution or error claim. Do not call zero null events probability zero. No broad all-prior-hypothesis significance claim.

Budgets: controls180seconds, actual120seconds, null panel300seconds, each512MiB RSS and64MiB saved result payload per stage. Check between instances/draws, preserve budget-unresolved states rather than negatives. Exact integers only. Save source hashes and original/replay UTC times. Final regressions on Python3.9/3.12; eight-item summary must distinguish finite negatives, underidentification, solver-resource limits and evidence gaps. Publish validated main and verify remote/checks. No Site change or ninth investigation; stop after item8.
