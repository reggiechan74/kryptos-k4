# Kryptos K4: experiments, evidence and open questions

This repository records an attempt to understand **K4, the final 97-letter section of Jim Sanborn’s Kryptos sculpture at CIA headquarters**. It contains reproducible experiments, source research and exact constraints, including failed ideas. **We do not have a verified solution or a recovered encryption method.**

K1–K3 serve as known-answer controls. Public reports of archival plaintext recovery are distinct from a published, reproducible cryptanalytic solution; see the [source verification](docs/source-verification-2026-10-18.md). This workspace does not claim independently to know all of K4’s plaintext.

**[Open the live Kryptos Light Laboratory on ChatGPT](https://kryptos-light-laboratory-rc2026.milky-lion-6014.chatgpt.site)** for interactive monument, light and cipher visualizations. Its geometry is illustrative, not a surveyed physical reconstruction. The downloadable fold-and-slide HTML below is a separate offline research artifact; the live Site includes the manual row/column overlay (version 15). The predefined integer row/column scan is now calibrated in the research report below; other manual exploration remains descriptive.

## Start here

| If you want to… | Read |
| --- | --- |
| Understand what has and has not been tested | [Hypothesis tracker](docs/tracking/HYPOTHESES.md) — 60 stable family IDs, linked to exact coverage |
| Find an experiment, its date, result, code and receipts | [Experiment tracker](docs/tracking/EXPERIMENTS.md) and [recorded run receipts](docs/tracking/RECEIPTS.md) |
| See the current obstacles and next discriminating work | [Research frontier](research/RESEARCH-FRONTIER-2026-10-23.md) and [machine-readable readiness assessment](results/FRONTIER-020.json) |
| Explore item 1’s systematic row-plus-column scan | [Findings](research/FOLD-SLIDE-2D-FINDINGS.md), [every 2D shift](results/FOLD-SLIDE-2D-001-frames.csv), [count maps](research/figures/fold-slide-2d-001.svg); the [earlier offline slider](research/figures/fold-slide-020.html) is column-only |
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
