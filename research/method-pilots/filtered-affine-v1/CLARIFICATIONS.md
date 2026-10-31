> **Dated source/mathematics record.** Read DECISION-STATUS.md and INDEPENDENT-OPERATOR-AUDIT.md for later resolutions; earlier pending gates remain historical. Public prose sanitization is explicit in PUBLIC-PROVENANCE.json.

# Clarifications to immutable OPERATOR-MAP.md draft

31 October 2026. The draft with SHA256 `71ebdde4e31041d2e83aab4235e768445badc9a94d905e5edc4feb952b4305ea` remains unchanged.

1. Section 1's phrase "independently reviewed inherited parity-negative set" must be read as **the proposed inherited parity-negative set B, whose independent verification is a separate pending gate**. This source review has not itself validated the retained target certificate or recomputed target inputs. No acceptance of B is claimed here.
2. The equality-rank argument uses the **uncentered 26-by-26 equality-value matrix** e I_26, rank 26, against xy+f(z)+g(w), rank at most 3. It does not claim that a centered mixed-difference matrix has rank 26.
3. All comparator alphabets, coefficients, position offsets, primers and carry base keys must be fixed across all inputs. They must not be refitted per history or per finite trace. All feedback lags are positive. The operator argument is applied strictly beyond initialization, where all predecessor F expressions and all varied history symbols lie in the freely reachable tail. It does not invent or recover the first six plaintext symbols, or assert one full initialized cipher from the tail-only model.
4. The causal-chain separation theorem itself does not need the <=3 support bound. That bound remains part of the proposed residual and the already frozen method; this observation is not authority to enlarge it.
5. Repository checkout read during this review was clean at `abae4d2dd16b9950bbcc2446c8b004ac4c50bd26` when checked at approximately 19:43 UTC. This source review made no repository or Page changes.
