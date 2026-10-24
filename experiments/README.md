# experiments

<!-- FOLDER-GUIDE: navigation only; original inputs and results are preserved. -->

Executable research implementations. Each finite experiment has a specification and result receipt; running every file blindly is not a reproduction protocol.

## Small reproductions

Run from the repository root:

```sh
python3 experiments/check_baseline.py
python3 experiments/check_controls.py
python3 experiments/run_regressions.py
python3 experiments/build_research_navigation.py
```

Most implementations use Python’s standard library. Some independent audits declare additional dependencies. Fold oracle and interactive-artifact checks require Node.js; tests use `/opt/homebrew/bin/node` on the validated Mac. Inspect the linked frozen protocol before running searches or timed benchmarks. Navigation generation does not execute cryptanalysis.

[Project overview](../README.md) · [Trackers](../docs/tracking/README.md)

## Contents

<details><summary>Local files and subdirectories</summary>

- [affine_digraph_boundary.py](affine_digraph_boundary.py)
- [affine_digraph_crossed.py](affine_digraph_crossed.py)
- [alphabet_geometry.py](alphabet_geometry.py)
- [asymmetric_feedback.py](asymmetric_feedback.py)
- [asymmetric_primer.py](asymmetric_primer.py)
- [autokey_constraint_controls.py](autokey_constraint_controls.py)
- [autokey_constraints.py](autokey_constraints.py)
- [autonomous_recurrence.py](autonomous_recurrence.py)
- [base60_beaufort.py](base60_beaufort.py)
- [bounded_models.py](bounded_models.py)
- [build_research_navigation.py](build_research_navigation.py)
- [check_baseline.py](check_baseline.py)
- [check_controls.py](check_controls.py)
- [check_ene_note.py](check_ene_note.py)
- [check_landmark_receipts.py](check_landmark_receipts.py)
- [check_solar_bounds.py](check_solar_bounds.py)
- [check_westsouthwest.py](check_westsouthwest.py)
- [ciphers.py](ciphers.py)
- [clock_boundary_regression.py](clock_boundary_regression.py)
- [conditional_face_lamp.py](conditional_face_lamp.py)
- [conditional_face_lamp_oracle.mjs](conditional_face_lamp_oracle.mjs)
- [continuation_io.py](continuation_io.py)
- [cp_convention_replay.py](cp_convention_replay.py)
- [dynamic_key.py](dynamic_key.py)
- [exact_linear.py](exact_linear.py)
- [exclusion_scope_audit.py](exclusion_scope_audit.py)
- [export_monument_slide.py](export_monument_slide.py)
- [face_row_coverage.py](face_row_coverage.py)
- [feistel_symmetry.py](feistel_symmetry.py)
- [feistel_three.py](feistel_three.py)
- [feistel_three_oracle.mjs](feistel_three_oracle.mjs)
- [fractionated_morse_constraints.py](fractionated_morse_constraints.py)
- [fractionated_morse_oracle.mjs](fractionated_morse_oracle.mjs)
- [frontier_assessment.py](frontier_assessment.py)
- [geometric_followup_checks.py](geometric_followup_checks.py)
- [geometric_pilots.py](geometric_pilots.py)
- [greek_phonetic_candidate.py](greek_phonetic_candidate.py)
- [greek_sigaba_oracle.mjs](greek_sigaba_oracle.mjs)
- [gromark_alphabet.py](gromark_alphabet.py)
- [gromark_alphabet_controls.py](gromark_alphabet_controls.py)
- [gromark_identifiability.py](gromark_identifiability.py)
- [gromark_identifiability_controls.py](gromark_identifiability_controls.py)
- [historical_language.py](historical_language.py)
- [ipa_free_map.py](ipa_free_map.py)
- [ipa_preprocessing.py](ipa_preprocessing.py)
- [ipa_source_review.py](ipa_source_review.py)
- [k3_clock_routes.py](k3_clock_routes.py)
- [landmark_axis.py](landmark_axis.py)
- [landmark_geometry.py](landmark_geometry.py)
- [landmark_inventory.py](landmark_inventory.py)
- [language_interfaces.py](language_interfaces.py)
- [masking_pilots.py](masking_pilots.py)
- [monument_slide.py](monument_slide.py)
- [monument_slide_oracle.mjs](monument_slide_oracle.mjs)
- [monument_slide_visual_check.mjs](monument_slide_visual_check.mjs)
- [nonrotor_structural.py](nonrotor_structural.py)
- [nonrotor_structural_oracle.mjs](nonrotor_structural_oracle.mjs)
- [occupied_cell_routes.py](occupied_cell_routes.py)
- [phonetic_cl.py](phonetic_cl.py)
- [phonetic_subset.py](phonetic_subset.py)
- [plaintext_step.py](plaintext_step.py)
- [probability_radix_review.py](probability_radix_review.py)
- [profile_sigaba_payload.py](profile_sigaba_payload.py)
- [profile_sigaba_sparse.py](profile_sigaba_sparse.py)
- [recurrence_certificate.py](recurrence_certificate.py)
- [reference/](reference/README.md)
- [replay_independent_followup.py](replay_independent_followup.py)
- [reset_boundary_proof.py](reset_boundary_proof.py)
- [resume_base60_beaufort.py](resume_base60_beaufort.py)
- [review_supplied_synthesis.py](review_supplied_synthesis.py)
- [route_key_graph.py](route_key_graph.py)
- [run_autokey_constraints.py](run_autokey_constraints.py)
- [run_bounded.py](run_bounded.py)
- [run_gromark_alphabet.py](run_gromark_alphabet.py)
- [run_gromark_identifiability.py](run_gromark_identifiability.py)
- [run_io.py](run_io.py)
- [run_regressions.py](run_regressions.py)
- [run_sigaba_collector_filter.py](run_sigaba_collector_filter.py)
- [run_sigaba_compressed_ownership.py](run_sigaba_compressed_ownership.py)
- [run_sigaba_domain_identity.py](run_sigaba_domain_identity.py)
- [run_sigaba_first_observation.py](run_sigaba_first_observation.py)
- [run_sigaba_joint_toy.py](run_sigaba_joint_toy.py)
- [run_sigaba_payload_profile.py](run_sigaba_payload_profile.py)
- [run_sigaba_real_adapter.py](run_sigaba_real_adapter.py)
- [run_sigaba_sparse_ownership.py](run_sigaba_sparse_ownership.py)
- [run_sigaba_torus.py](run_sigaba_torus.py)
- [sigaba_collector_filter.py](sigaba_collector_filter.py)
- [sigaba_compact_domain.py](sigaba_compact_domain.py)
- [sigaba_compact_oracle.py](sigaba_compact_oracle.py)
- [sigaba_compressed_ownership.py](sigaba_compressed_ownership.py)
- [sigaba_csp889.py](sigaba_csp889.py)
- [sigaba_domain_identity.py](sigaba_domain_identity.py)
- [sigaba_first_observation.py](sigaba_first_observation.py)
- [sigaba_inspired.py](sigaba_inspired.py)
- [sigaba_joint_feasibility.py](sigaba_joint_feasibility.py)
- [sigaba_joint_toy.py](sigaba_joint_toy.py)
- [sigaba_joint_toy_oracle.py](sigaba_joint_toy_oracle.py)
- [sigaba_real_adapter.py](sigaba_real_adapter.py)
- [sigaba_sparse_ownership.py](sigaba_sparse_ownership.py)
- [sigaba_state_inference.py](sigaba_state_inference.py)
- [sigaba_torus.py](sigaba_torus.py)
- [sigaba_torus_controls.py](sigaba_torus_controls.py)
- [silk_periodic.py](silk_periodic.py)
- [single_boundary_reset.py](single_boundary_reset.py)
- [split_coordinate.py](split_coordinate.py)
- [statistical_diagnostics.py](statistical_diagnostics.py)
- [statistical_receipt_compare.py](statistical_receipt_compare.py)
- [strategy_followup.py](strategy_followup.py)
- [structural_checks.py](structural_checks.py)
- [summarize_sigaba_joint_toy.py](summarize_sigaba_joint_toy.py)
- [summarize_sigaba_torus.py](summarize_sigaba_torus.py)
- [tree_path_cipher.py](tree_path_cipher.py)
- [tree_state_support.py](tree_state_support.py)
- [wheatstone_transition.py](wheatstone_transition.py)
- [wheatstone_transition_oracle.mjs](wheatstone_transition_oracle.mjs)
- [word_scramble.py](word_scramble.py)

</details>

## Recording future run times

Use `RunSnapshot` for new immutable runs and declare `execution_kind` as `original`, `replay` or `validation`; the default `unspecified` deliberately makes no original-run claim. The common `run_bounded.execute` runner records timezone-bearing UTC start/end at run and job level, including failed jobs. Job timing includes action and artifact staging; snapshot end follows final publication checks. Its bounded/statistical command entrypoints are explicitly replays. Other standalone scripts retain their documented interfaces; this change does not invent historical times or imply all old scripts were migrated.

## Systematic two-dimensional overlay, item 1

[The frozen protocol](../research/FOLD-SLIDE-2D-SPEC.md) and [completed findings](../research/FOLD-SLIDE-2D-FINDINGS.md) distinguish label matches, surrogate apertures and conditional chance. `monument_slide_2d.py --controls` uses synthetic inputs only. To repeat the original fixed experiment, use `python3.12 experiments/monument_slide_2d.py --run --execution-kind replay --spec-commit f6aafc4735b8ff9e4f7e01975a97baf9991e1583`; a new immutable replay is created. The original source remains pinned at its recorded commit. `export_monument_slide_2d.py` formats retained results; `audit_monument_slide_2d_controls.py` records the separately labeled supplementary synthetic check. No Site deployment or subsequent numbered investigation is invoked.

`physical_solar_002.py` reproduces item 2 conditional solar/ray-plane constraints; [protocol](../research/PHYSICAL-SOLAR-002-SPEC.md) and [outputs](../results/physical-solar-002/README.md). It does not evaluate a cipher.

`world_clock_003.py` enumerates exact conditional partial-inventory registrations and phase invariants; [protocol](../research/WORLD-CLOCK-003-SPEC.md), [receipts](../results/world-clock-003/README.md). It assigns no historical UTC offsets or cipher symbols.

`run_sigaba_unknown_anchor.py` and `run_sigaba_unknown_anchor_byte_masks.py` are separately frozen synthetic resource comparisons; [protocol](../research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-SPEC.md) and [findings](../research/SIGABA-UNKNOWN-ANCHOR-COLLECTOR-FINDINGS.md). Neither reads K4 ciphertext.

## Item 5: ordinal lamp/Greek codecs

[Implementation](lamp_greek.py), [immutable original/replay runner](run_lamp_greek.py), [independent direct-selector validation](audit_lamp_greek.py), and [certificate replay](lamp_greek_certificates.py). Read the [frozen protocol](../research/LAMP-GREEK-025-SPEC.md) before running. These are exploratory constructions, not historical World Clock evidence.
