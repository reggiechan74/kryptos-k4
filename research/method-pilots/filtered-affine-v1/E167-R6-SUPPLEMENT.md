> **Dated source/mathematics record.** Read DECISION-STATUS.md and INDEPENDENT-OPERATOR-AUDIT.md for later resolutions; earlier pending gates remain historical. Public prose sanitization is explicit in PUBLIC-PROVENANCE.json.

# E167 R6 source supplement

31 October 2026. Additional read-only primary-source inspection closes the separately noted R6 source gap in OPERATOR-MAP section 3. No external program execution or target calculation.

[src/e167c_twokey.cu](https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/e167c_twokey.cu), exact commit `992c9668b9f0783221cb570abbff969e59cbf27c`, Git blob `20d098f2f94edc090bce19d978f56fb26dea2c43`, now retained and blob-verified in SOURCE-MANIFEST.json.

R6 is explicitly a position-only two-keyword composition. The second key k2[i mod L2] drives an E167 operation on the current plaintext or ciphertext symbol; the first k1[i mod L1] enters the additive chart. Source lines 20-23 define r6f solely on the current p,c,k2; lines 40-43 assign residue classes using pos mod L1/L2; the independent synthetic constructor at lines 109-114 indexes the fixed keyword arrays by i mod period. The same-key branch reads one periodic keyword symbol through two fixed numberings. Periods L1,L2 each range1..13 with configurable sum cap (default18); no unknown alphabet inference or ciphertext-history recurrence is added.

Thus R6 shares the same fixed-per-symbol/global-operator separation as the inspected E167 R1-R5/R7/R8 grammar. This is not an audit of its solver soundness, completion or claimed negative results. It does not exclude finite-trace coincidences.
