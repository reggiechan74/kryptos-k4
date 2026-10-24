# tests

<!-- FOLDER-GUIDE: navigation only; original inputs and results are preserved. -->

Regression tests include baseline fixtures, planted cases, exact tiny-system comparisons, mutation rejection and retained artifact validation. A round trip alone does not establish historical authenticity.

## Run the supported suite

`python3 experiments/run_regressions.py` selects only Git-tracked test basenames, avoiding unrelated local duplicate files. Validate under Python 3.9 and 3.12 when changing shared numerical code. JavaScript-dependent checks also need Node.js. No test success implies that K4 is solved.

[Project overview](../README.md) · [Trackers](../docs/tracking/README.md)

## Contents

<details><summary>Local files and subdirectories</summary>

- [reset_control_reference.py](reset_control_reference.py)
- [test_affine_digraph_boundary.py](test_affine_digraph_boundary.py)
- [test_alphabet_geometry.py](test_alphabet_geometry.py)
- [test_asymmetric_feedback.py](test_asymmetric_feedback.py)
- [test_asymmetric_primer.py](test_asymmetric_primer.py)
- [test_audit_hardening.py](test_audit_hardening.py)
- [test_autokey_constraints.py](test_autokey_constraints.py)
- [test_autonomous_recurrence.py](test_autonomous_recurrence.py)
- [test_autonomous_recurrence_artifacts.py](test_autonomous_recurrence_artifacts.py)
- [test_base60_beaufort.py](test_base60_beaufort.py)
- [test_base60_resume.py](test_base60_resume.py)
- [test_baseline.py](test_baseline.py)
- [test_bounded.py](test_bounded.py)
- [test_clock_boundary_regression.py](test_clock_boundary_regression.py)
- [test_conditional_face_lamp.py](test_conditional_face_lamp.py)
- [test_conditional_face_lamp_preflight.py](test_conditional_face_lamp_preflight.py)
- [test_continuation_artifacts.py](test_continuation_artifacts.py)
- [test_controls.py](test_controls.py)
- [test_cp_convention_replay.py](test_cp_convention_replay.py)
- [test_direct_enigma.py](test_direct_enigma.py)
- [test_dynamic_key.py](test_dynamic_key.py)
- [test_dynamic_key_artifacts.py](test_dynamic_key_artifacts.py)
- [test_feistel_tree_extensions.py](test_feistel_tree_extensions.py)
- [test_fixed_pilot_artifacts.py](test_fixed_pilot_artifacts.py)
- [test_fractionated_morse_constraints.py](test_fractionated_morse_constraints.py)
- [test_frontier_assessment.py](test_frontier_assessment.py)
- [test_geometric_independent_audits.py](test_geometric_independent_audits.py)
- [test_geometric_pilots.py](test_geometric_pilots.py)
- [test_greek_sigaba_candidates.py](test_greek_sigaba_candidates.py)
- [test_gromark_alphabet.py](test_gromark_alphabet.py)
- [test_gromark_identifiability.py](test_gromark_identifiability.py)
- [test_historical_declination_receipts.py](test_historical_declination_receipts.py)
- [test_historical_language.py](test_historical_language.py)
- [test_hypothesis_register.py](test_hypothesis_register.py)
- [test_independent_construction_artifacts.py](test_independent_construction_artifacts.py)
- [test_independent_followup_artifacts.py](test_independent_followup_artifacts.py)
- [test_ipa_free_map.py](test_ipa_free_map.py)
- [test_ipa_independent_integration.py](test_ipa_independent_integration.py)
- [test_ipa_preprocessing.py](test_ipa_preprocessing.py)
- [test_ipa_source_review.py](test_ipa_source_review.py)
- [test_joint_nonrotor.py](test_joint_nonrotor.py)
- [test_k3_clock_artifacts.py](test_k3_clock_artifacts.py)
- [test_k3_clock_routes.py](test_k3_clock_routes.py)
- [test_landmark_axis.py](test_landmark_axis.py)
- [test_language_interfaces.py](test_language_interfaces.py)
- [test_language_masking_artifacts.py](test_language_masking_artifacts.py)
- [test_masking_pilots.py](test_masking_pilots.py)
- [test_monument_slide.py](test_monument_slide.py)
- [test_monument_slide_artifacts.py](test_monument_slide_artifacts.py)
- [test_occupied_cell_artifacts.py](test_occupied_cell_artifacts.py)
- [test_occupied_cell_routes.py](test_occupied_cell_routes.py)
- [test_phonetic_cl.py](test_phonetic_cl.py)
- [test_phonetic_subset.py](test_phonetic_subset.py)
- [test_plaintext_step.py](test_plaintext_step.py)
- [test_probability_radix_review.py](test_probability_radix_review.py)
- [test_recurrence_certificate.py](test_recurrence_certificate.py)
- [test_reset_boundary_proof.py](test_reset_boundary_proof.py)
- [test_reset_controls.py](test_reset_controls.py)
- [test_route_key_graph.py](test_route_key_graph.py)
- [test_sigaba_anchor_artifacts.py](test_sigaba_anchor_artifacts.py)
- [test_sigaba_collector_artifacts.py](test_sigaba_collector_artifacts.py)
- [test_sigaba_collector_filter.py](test_sigaba_collector_filter.py)
- [test_sigaba_compact_artifacts.py](test_sigaba_compact_artifacts.py)
- [test_sigaba_compressed_ownership.py](test_sigaba_compressed_ownership.py)
- [test_sigaba_domain_artifacts.py](test_sigaba_domain_artifacts.py)
- [test_sigaba_domain_identity.py](test_sigaba_domain_identity.py)
- [test_sigaba_first_observation.py](test_sigaba_first_observation.py)
- [test_sigaba_full_state.py](test_sigaba_full_state.py)
- [test_sigaba_historical_scope.py](test_sigaba_historical_scope.py)
- [test_sigaba_joint_toy.py](test_sigaba_joint_toy.py)
- [test_sigaba_joint_toy_artifacts.py](test_sigaba_joint_toy_artifacts.py)
- [test_sigaba_real_adapter.py](test_sigaba_real_adapter.py)
- [test_sigaba_real_artifacts.py](test_sigaba_real_artifacts.py)
- [test_sigaba_sparse_artifacts.py](test_sigaba_sparse_artifacts.py)
- [test_sigaba_sparse_ownership.py](test_sigaba_sparse_ownership.py)
- [test_sigaba_torus.py](test_sigaba_torus.py)
- [test_sigaba_torus_artifacts.py](test_sigaba_torus_artifacts.py)
- [test_silk_periodic.py](test_silk_periodic.py)
- [test_single_boundary_reset.py](test_single_boundary_reset.py)
- [test_single_boundary_reset_artifacts.py](test_single_boundary_reset_artifacts.py)
- [test_site_entrance_handoff.py](test_site_entrance_handoff.py)
- [test_site_source_handoff.py](test_site_source_handoff.py)
- [test_split_coordinate.py](test_split_coordinate.py)
- [test_statistical_receipt_compare.py](test_statistical_receipt_compare.py)
- [test_statistics.py](test_statistics.py)
- [test_strategy_followup.py](test_strategy_followup.py)
- [test_strategy_followup_artifacts.py](test_strategy_followup_artifacts.py)
- [test_structural.py](test_structural.py)
- [test_tree_path_cipher.py](test_tree_path_cipher.py)
- [test_wheatstone_transition.py](test_wheatstone_transition.py)
- [test_word_scramble.py](test_word_scramble.py)

</details>

## Evolved runner provenance

Historical artifact checks validate the shared `run_io.py` / `run_bounded.py` bytes at each receipt’s recorded implementation commit after those helpers evolve. Other unchanged input/model files retain their working-tree hash checks. Original receipt hashes are never rewritten to match new code. Dedicated temporary-fixture timing tests validate the current runner, including failure completion and explicit replay labels.

## Item 5 controls

[test_lamp_greek.py](test_lamp_greek.py) checks the complete display, Greek framing/ranks, local-key constraint equivalence, preserved original receipt hashes, support exclusion and complete independent-selector results. Full expensive original selectors are retained as receipts and separately runnable; regression checks do not silently rerun model searches.

## Item 6 checkpoint

[Item 6 tests](test_tree_geometry_ipa.py) check dynamic topology, causal inverse, independent reference, exact original artifact hashes, failed-control staging, full candidate sets and historical period scope.

## Item 7 checkpoint

[Conditional strip controls](test_strip_source_gates.py) and [historical source QA/admission tests](test_item7_historical_source_qa.py) preserve raw ambiguities, source conflicts and unavailable binary metadata. No network retrieval is required for regression.

## Final item 8 checkpoint

[One-edit core tests](test_one_edit_core.py) cover all tagged maps, complete tiny truth sets and table-based inverses. [Artifact tests](test_one_edit_artifacts.py) verify immutable hashes, full-selector accounting, lossless storage and independent exact union/certificate replay. Large control JSON is streamed rather than fully loaded during regression.
