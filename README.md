# Kryptos K4: experiments, evidence and open questions

This repository records an attempt to understand **K4, the final 97-letter section of Jim Sanborn’s Kryptos sculpture at CIA headquarters**. It contains reproducible experiments, source research and exact constraints, including failed ideas. **We do not have a verified solution or a recovered encryption method.**

**Start with the [current hypothesis status and working to-do list](research/HYPOTHESES.md).** Completed tests and remaining gaps are tracked there. **Also check the [external hypothesis and prior-art register](research/EXTERNAL-PRIOR-ART.md)** for what other researchers have tried. [AGENTS.md](AGENTS.md) requires checking both before selection and reconciling them after every experiment. The [fresh four-family program](research/fresh-program-20261031/README.md) follows the public survey. Studies 060–062 ruled out their precisely bounded alphabet-update, sum-locked rotation and ciphertext-steered Josephus rules. Next is coupled 26/24 carry, subject to separate equivalence and validation gates. Q-04/Q-05 remain unrun.

**The [eight requested investigations are complete to their stated scopes](research/EIGHT-ITEM-INVESTIGATION-SUMMARY.md).** Results include finite negatives, unresolved computation and evidence-blocked models. The final one-edit study supplies no correction or decryption.

**New physical diagnostic:** [projection-ray concurrence](research/PROJECTION-CONCURRENCE-029-FINDINGS.md) is now synthetic-validated and preregistered for independent photo correspondences. Real-data fitting remains evidence-blocked; no measured monument result is claimed.

**Published through study 062:** [051–062 results and current selection status](research/HYPOTHESES.md) are reconciled with the canonical experiment log. Historical validation counts belong to their recorded snapshots, not this documentation update.

**Published coverage review:** the [seven-family coverage matrix](research/SEVEN-FAMILY-REVIEW-046.md) tracks 34 subbranches across studies 038–046, with the [047 native-photo follow-through](research/PHOTO-NATIVE-047-FINDINGS.md) and [048–050 fixed-source, ENE-route and hand-grammar tests](research/048-050-PRIOR-COVERAGE.md). Narrow exclusions, non-identifiable fits, unresolved computation and evidence gaps remain separate. No K4 plaintext is identified. These scoped results are published; publication does not change the live Site.

K1–K3 serve as known-answer controls. Public reports of archival plaintext recovery are distinct from a published, reproducible cryptanalytic solution; see the [source verification](docs/source-verification-2026-10-18.md). This workspace does not claim independently to know all of K4’s plaintext.

**[Open the live Kryptos Light Laboratory on ChatGPT](https://kryptos-light-laboratory-rc2026.milky-lion-6014.chatgpt.site)** for interactive monument, light and cipher visualizations. Its geometry is illustrative, not a surveyed physical reconstruction. The downloadable fold-and-slide HTML below is a separate offline research artifact; the live Site includes the manual row/column overlay and synthetic projection diagnostic ([complete version 19 source archive and restore instructions](docs/site-source/light-laboratory-v19-20261031/README.md)). The reviewed photographic record has zero certified pairs or real fits; this does not show that accessible photos cannot yield them. The predefined integer row/column scan is now calibrated in the research report below; other manual exploration remains descriptive.

## Start here

| If you want to… | Read |
| --- | --- |
| Review the seven requested families and remaining gaps | [Coverage matrix](research/SEVEN-FAMILY-REVIEW-046.md) and [structured branches](research/specifications/SEVEN-FAMILY-REVIEW-046.json) |
| Understand what has and has not been tested | [Hypothesis tracker](docs/tracking/HYPOTHESES.md) — 67 stable family IDs, linked to exact coverage |
| Find an experiment, its date, result, code and receipts | [Experiment tracker](docs/tracking/EXPERIMENTS.md) and [recorded run receipts](docs/tracking/RECEIPTS.md) |
| Avoid repeating other researchers’ hypotheses | [External prior-art register](research/EXTERNAL-PRIOR-ART.md) — exact scopes, source pins, evidence quality and overlap with our tests |
| Decide what to test next | [Canonical working to-do list](research/HYPOTHESES.md); [historical frontier and source gates](research/RESEARCH-FRONTIER-2026-10-23.md) remain reference snapshots |
| Explore item 1’s systematic row-plus-column scan | [Findings](research/FOLD-SLIDE-2D-FINDINGS.md), [every 2D shift](results/FOLD-SLIDE-2D-001-frames.csv), [count maps](research/figures/fold-slide-2d-001.svg); the [earlier offline slider](research/figures/fold-slide-020.html) is column-only |
| Compare all eight scopes and outcomes | [Eight-item summary](research/EIGHT-ITEM-INVESTIGATION-SUMMARY.md) — complete investigation does not mean a solved or exhausted family |
| Inspect the final one-edit robustness study | [Exact counts, ambiguity and controls](research/ONE-EDIT-028-FINDINGS.md); canonical ciphertext is unchanged |
| Inspect the published geographic maps and their limits | [Berlin WSW map archive](docs/maps/berlin-wsw-2026-10-24/README.md) —four maps, supporting data, attribution and read-only validators |
| Review the completed candidate-first pilot 051 | [32-message pilot and reproducible package](research/candidate-first-051/README.md) — negative result; all three target gates failed |
| Review the 1,024-message structural-key test 052 | [Frozen bank and compact reproduction package](research/candidate-first-052/REPOSITORY.md) — all three target gates failed |
| Review the ordinary-language running-key test 053 | [Frozen model, corpus and compact reproduction package](research/candidate-first-053/REPOSITORY.md) — all four target criteria failed |
| Review exact source lookup 054 | [Corpus, complete results and reproduction package](research/candidate-first-054/README.md) — zero matches within the frozen 89-document corpus |
| Compare new cryptanalysis strategies and proposed next experiments | [31 October 2026 research study](research/strategy-review-20261031/README.md) — literature comparison, exact scope limits and benchmark-first roadmap |
| Review calibrated English-key fragment screen 055 | [Report, audits and reproduction archive](research/candidate-first-055/README.md) — 0/12 target pairs survive; a bounded heuristic screen, not an impossibility proof |
| Review joint periodic-key and column-route study 056 | [Exact scope, benchmark, target and audits](research/candidate-first-056/README.md) — complete independent exclusion of the frozen A–Z Vigenère → ragged-columnar family |
| Study 057: alphabet-role and Beaufort extensions | [Exact bounded exclusion, benchmark and audits](research/candidate-first-057/README.md) |
| Study 058: reverse-stage columnar and periodic arithmetic | [Exact key-cylinder exclusion, ambiguity controls and audits](research/candidate-first-058/README.md) |
| Review short-primer feedback study 059 | [Bounded exclusion, ambiguity controls and audits](research/candidate-first-059/README.md) — subtractive feedback remains untested; conditional Q-04/Q-05 prerequisites not established |
| Reproduce the work | [Running experiments](experiments/README.md) and [test guide](tests/README.md) |

**Overlay scope:** the earlier column-only study used `dy = 0`. [Item 1’s newer predefined two-dimensional study](research/FOLD-SLIDE-2D-FINDINGS.md) covers all integer rows −28…+28 and columns −33…+33 under two fixed registrations. Its own whole-search controls show no unusual excess; the older column-only p-values are not repurposed for rows.

The detailed [hypothesis ledger](research/HYPOTHESES.md) and [experiment log](research/EXPERIMENTS.md) remain the canonical sources. Generated trackers improve navigation without replacing those records.

## What is actually known

Confirmed English plaintext clues occupy these **one-based inclusive** positions:

| Positions | Plaintext | Ciphertext | Python slice |
| --- | --- | --- | --- |
| 22–34 | EASTNORTHEAST | FLRVQQPRNGKSS | `[21:34]` |
| 64–74 | BERLINCLOCK | NYPVTTMZFPK | `[63:74]` |

[Exact ciphertext and anchors](data/k4.json) are fixed inputs. The clues refer to the final English plaintext. A phonetic, transposed or variable-length intermediate stream does **not** automatically retain those positions. A model using unchanged alignment states that assumption explicitly. Public clues used in earlier research are not historically untouched validation data.

## Findings worth understanding

- **Structural constraints are stronger than attractive text.** [Count, repeated-phase and support checks](research/STRUCTURAL-FINDINGS.md) exclude specific direct-alignment models independently of guessed keywords. They do not exclude combinations with unspecified preprocessing or routes.
- **Flexible models can fit without identifying a message.** The tracker distinguishes exact contradictions, compatible but ambiguous models, and mere parameter fits. Unknown keys or glyph mappings are retained as unknowns.
- **SIGABA is an engineering frontier, not a solved K4 lead.** The [authentic adapter](research/SIGABA-REAL-ADAPTER-FINDINGS.md) has historical-convention and simulator-wiring limits. Exact synthetic inference still fails the full-domain resource gate. The [supplied-anchor filter diagnostic](research/SIGABA-COLLECTOR-FILTER-FINDINGS.md) is not blind recovery and added no full-domain controller coverage.
- **The fold idea has now been implemented.** Double reflection reproduces MYVGT opposite AABCD without a row shift. The new 7,638-frame integer row/column study extends the earlier column-only comparison. Label coincidences and approximate shared apertures show no unusual excess under the whole-search controls; measured monument optics remain untested.
- **Physical evidence has useful limits.** [Archival research](research/evidence/README.md) distinguishes the static compass needle, true north, stone alignments and pool lighting. [Geometry provenance](docs/scott-sun-geometry-audit-2026-10-22.md) is insufficient for a calibrated optical key search.

A finite negative is never a rejection of every cipher in its family. A timeout is unresolved. A source quotation, a synthetic round trip, an analytical exclusion and an actual K4 search provide different kinds of evidence.

## Repository map

| Folder | Contents |
| --- | --- |
| [research/](research/README.md) | Protocols, findings, canonical ledgers and evidence |
| [experiments/](experiments/README.md) | Reproducible implementations and navigation generator |
| [data/](data/README.md) | Pinned ciphertext, controls, alphabets and modeled representations |
| [results/](results/README.md) | Original run receipts, full outputs and later replay records |
| [tests/](tests/README.md) | Regression, planted recovery, mutation and independent comparisons |
| [independent/](independent/README.md) | Original separately supplied audits; provenance and limitations preserved |
| [sources/](sources/README.md) | Source identities, verification and derived evidence |
| [docs/](docs/README.md) | Reader guides, generated trackers and retained Site source handoffs |

## Reproduce a small check

From the repository root, using Python 3.9 or 3.12:

```sh
python3 experiments/check_baseline.py
python3 experiments/check_controls.py
python3 experiments/run_regressions.py
```

Most code uses the standard library. Particular independent audits declare their own dependencies; Node.js is required for the fold’s independent JavaScript checks. Follow each frozen specification rather than treating every Python file as an interchangeable command. Tests use tracked filenames so unrelated local duplicate files are not silently executed.

## Dates, status and provenance

The [receipt index](docs/tracking/RECEIPTS.md) labels explicit run start/end, receipt-recording and artifact-creation timestamps separately in ISO 8601 UTC. Historical times missing from the records stay **unknown**; commit times and filenames are not substituted. Date-only log statements remain date-only. Toronto local time is not silently assumed.

Research artifacts are preserved even when later audits narrow their claims. Historical “unrun” labels may be superseded by the current canonical ledger; consult its precise tested and untested scopes. No live Site deployment is performed by these documentation or research commands.

The [previous root README](docs/history/README-before-navigation.txt) is retained as an archival snapshot; its historical wording does not override the current ledger.


