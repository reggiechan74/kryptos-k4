# Finite 71-hit K4 discovery-set closeout — 31 October 2026

## Decision

**All 71 original discovery hits now have one explicit disposition. No newly eligible, precisely specified unrun cipher was found; no hypothesis or experiment is admitted.** This is a finite discovery-set review, not a survey of all worldwide prior work. No third-party program, cipher search or solver was run; no author was contacted and no remote state changed.

The current local/external registers were read first. Prior reviewed sources were carried forward rather than redundantly audited. New work used pinned primary documentation, implementation and named outputs, plus metadata/tree reads needed for deduplication. Source caches are local audit aids: publication should use source links and original analysis, not wholesale redistribution of unlicensed code.

## Exact accounting

| Disposition | Hits |
|---|---:|
| Implemented K4 work, including tools/diagnostics rather than necessarily completed searches | 33 |
| Documentation-only / K4 placeholders | 8 |
| Unsupported or retracted solution claims | 13 |
| Forks, identical-code copies or same-project companion | 11 |
| Irrelevant to external K4 survey | 4 |
| Empty/unavailable repositories | 2 |
| **Total** | **71** |

The four irrelevant entries are Swedish tax-form software, two learning-only projects, and **our own repository** (not independent external work). Empty joquist and polancan repositories have no commit to pin; their metadata/empty responses are evidence, not cryptanalytic negatives.

After the eleven duplicates are grouped, the set has **60 distinct repository/project groups**. Removing four irrelevant groups and two empty groups leaves **54 relevant nonempty unique groups**, including claims, placeholders, utilities and actual research. This is NOT 54 independent completed research programs. Treating mproffitt's explicitly related PyKryptos and successor notebook as one declared lineage gives **53 lineages**, not a further code-identity deduplication.

Across the original set, **59 repositories had documentation or source text read**, **39 had some source file inspected**, and **six had separately named result artifacts inspected**. The source count includes source used to establish placeholders, invalid implementations and irrelevant learning code; it must **not** be presented as39 substantive completed-model audits. Of these39,31 are new source-file inspections in this pass. Named receipts newly read are Keith Adler, claudlos and Aciderix; earlier in-set receipts are Sovi11, ActiveTK and Barneyjm. No independent reproduction occurred.

### Correction to earlier coverage wording

The earlier report's14 reviewed repositories remain a true historical total, but only **13** belonged to `discovery.json`; **jcolinpatrick/kryptos was outside the71**. Conversely, **akaalias/k4 is discovery hit 23**, although reviewed later alongside its website. Thus the previously reviewed combined cohort was **15 repositories =14 in-set +jcolinpatrick outside**, not “14 in-set plus akaalias outside.” This dated correction should not rewrite frozen historical reports.

Including carried-forward jcolinpatrick evidence gives60 documentation/source-read repositories,40 source-file-read repositories and seven named-result repositories across this broader reviewed cohort. These totals still include nonresearch/invalid cases as qualified above. The only newly followed repository outside the71 is **isaaclyman/kryptos-typescript**, read solely as upstream metadata/commit comparison for an in-set fork; do not count it as an additional source/model-reviewed project. Additional previously reviewed web sources remain separate.

## Deduplication and aliases

- Five patrickkellogg forks share its exact pinned HEAD. Four other forks' pinned commits are present in the declared parent (RichardBean, speakeasy, and the two mproffitt projects). They are not independent trials.
- PrabhaharanNM/kryptos and kavinbharathii/kryptos share actual README, notebook, main and UI blobs despite `fork=false`. Count one code project.
- Esteban's two repositories explicitly describe the same anchor-displacement project; one is a documentation companion. Count one unsupported claim, not independent corroboration.
- instancer-kirik is a **substantive fork extension**, three commits ahead of upstream `f8b3848ee589c2566fbf76734d5ca36fbfa7d977`,27 changed paths. Retain its new finite implementations; do not discard it merely because GitHub says fork.
- Cross-batch code-blob comparison found **261 identical Aciderix implementation blobs vendored in ActiveTK under `refs/aciderix/`**, including T36. Both are distinct research projects, but this imported campaign is one experiment, not two independent replications. ActiveTK also imports a TTFH utility. Shared dictionary/data/common files were not used as whole-project duplication proof.
- “Symmetry transposition” in old-zet is a reflected **symbol substitution**, not message-position transposition. LazaUK's two additive-decryption stage orders commute. Aciderix Z26 is relabelled cyclic arithmetic; Z5×Z6 aliases Z30 rather than another independent group.

## Highest-value additions

1. **Aciderix finite-group plaintext autokey:** actual lag 7, shared injective 26-letter embedding into 23 specified finite abelian groups of orders26–36, free offset and 67 sign/group cases. Named output records optimal minima1 or2 violated equations for all 67. Derived17-equation supermodel relaxes intermediate values outside the alphabet image; no mod26 projection. A first-letter-zero gauge is valid **because the offset is free**, not by an automatic translation assumption: σ→σ+g requires d→d−g in Vigenère and d→d+g for Beaufort/variant; actual derived coefficient sums cancel. Larger-group English-plant generation can fail because the 26-letter image is not closed. These control and encoding limits must remain attached. No all-lag/all-group exclusion or independent solver replay. [Pinned implementation](https://github.com/aciderix/kryptos-research-handoff/blob/6b82bd5364b6fea78b6ef3cfd73fafaf85ac3462/audits/autocle_groupes_2026_09_25/t36_autocle_groupes.py).
2. **Keith Adler two-period sum keys:** same-axis AZ/KR, periods1≤a≤b≤26, Vigenère/Beaufort, linear consistency mod2/mod13, zero-redundancy cells skipped. Named receipt932 testable combinations has **two survivors**, KR Beaufort 12+15 and 9+19. Not a universal exclusion. [Receipt](https://github.com/keithadler/kryptos/blob/714e7c252165e106b2b827eacab156c4005f2b90/results/17_layer_two.txt).
3. **ZeroDay physical projection/overlay and key chains:** finite affine projection numerical sweeps, not measured geometry; level-two/three chain filters impose minimum6/8 equalities, and broader columnar reports impose larger-width thresholds. Zero retained hits is not full feasibility exclusion. [Projection code](https://github.com/ZeroDay-Labz/kryptos-k4/blob/854534543a93ddf2534758b620ae05cb36dd0a04/k4/projection.py), [chain code](https://github.com/ZeroDay-Labz/kryptos-k4/blob/854534543a93ddf2534758b620ae05cb36dd0a04/k4/chain.py).
4. **Tyler one-free-alphabet Gromark/running-key predicate:** in-place equality-pattern check across24 crib letters; finite base 10 primers5–7, base 26primer5, seven fixed cipher alphabets, two signs and finite text sources. Reported337,634,136settings and12plants are documentation evidence here, not a separately read completion receipt. Word-level moves are a stronger solver for an attempted model, not a new cipher. [Source](https://github.com/tylerj-spec/kryptos-k4/blob/c0e2a6847d0f7a505ccfa3bea2b0c58a5ccf2f3c/r40/sealed/whole_family.cpp).
5. **markmnl report-only hand-cipher portfolio:** Nicodemus through19, shifted AMSCO through 17, Ragbaby, Slidefair, Portax, wheel and grille variants. Rich public ledger but underlying source/log archive not bundled. Prevent generic-family duplication; do not inherit exact negatives from a manifest alone. [Ledger](https://github.com/markmnl/kryptos/blob/090347cbd3fd9329d59df3edcf999964edc9b873/WHAT_WE_TRIED.md).
6. **Other implemented prior art:** mproffitt clock lamp sums and table rules; mfascia dictionary+97cyclic shifts; old-zet progressive-table/reflected substitution; Elodine earlier-text crib sliding; LazaUK sampled weighted clock masks; Flavia elementary contradiction scripts; claudlos SAT/forced-crib interpolation; browser and TypeScript finite variation tools. Exact source bounds, aliases and skips are in the three batch reports.

## Invalid and weak evidence stays visible

GrafSpiel's inspected Gromark code uses wrong crib positions and a nonstandard last-two-digit recurrence; malak's fragment diagnostic is adjacent-triplet testing, not complete Gromark. Sofia's validation literally simulates success. Esteban's anchor script uses a noncanonical ciphertext literal. Several solved/closure/resonance repositories supply no executable forward cipher; one has only an uninspected ZIP beyond README, another links a4.91GiB external archive. These are unsupported, not authenticated solutions and not grounds for treating unknown models as excluded. No speculative target is derived from their claims.

## Deliverables and next decision

- `coverage-disposition-20261031.json`: all 71 unique discovery indexes, pins, project grouping, evidence, sources, findings and two separately identified out-of-set sources.
- `triage-{early,middle,late}.md`: proposed **additive external-register records** with exact models/bounds/caveats; publisher assigns stable IDs and integrates into existing readable structure.
- The normalized disposition file preserves the public batch evidence fields; raw source caches are not redistributed.
- `triage-shared-code-blobs.json` and `triage-late-instancer-compare.json`: exact deduplication evidence.

**Selection consequence:** consult these bounded external-register additions and the dated count correction, especially finite-group, key-chain, projection and free-alphabet coverage, before proposing work in those domains. Keep the execution queue empty. Future proposals must name a genuinely different operation, subtract these newly documented domains and retained local exclusions, and independently establish identifiability/control gates. Completing an attempted search, repairing a broken implementation or strengthening a solver is not an eligible new hypothesis. This finite task is complete; no open-ended linked-repository crawl is implied.
