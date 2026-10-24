# Late reviewer controls — 24 October 2026

[Separate timestamped receipt](../results/REVIEW-CONTROLS-046.json), [implementation](../experiments/review_controls_046.py). These supplement already completed numerical runs; no large experiment, original source or original receipt changed.

- **041 active interruption:** the real root calculation constructs four layers and enters connected-support pruning before a deliberate exception. No partial root is cached. A fresh complete evaluation equals the direct root result, then a genuine cache hit agrees. The original deadline-before-construction test alone did not demonstrate this stronger behavior.
- **042 wrong shared-DST reference:** a separately implemented model applies the same EU March–September schedule to both cities at every one of8,760hours. Direct comparison with the pinned actual timezone tables finds840difference disagreements. This now substantiates the negative control independently of the earlier `8760−maxcounts` summary identity.
- **043 flags:**48transported inputs retain valid.Zmagic but use invalid width/reserved flag bits. All fail the declared header validator; the valid short vector passes and a truncated header fails. Earlier mutations tested changed magic, not these flag failures.

The earlier [038changed-crib supplement](../results/REVIEW-CONTROLS-045.json) and [040off-site-data clarification](PHYSICAL-IDENTIFIABILITY-040-FINDINGS.md#review-clarification-an-off-site-evidence-gate) remain separate. These controls do not turn any broad family into a global exclusion.
