# Study 058 independent target audit

**PASS — exact bounded exclusion.** Both unchanged engines returned `UNSAT_COMPLETE` with zero compatible key cylinders, zero operators and zero plaintexts.

- Verified all 34 frozen files and the additive target freeze `074213b711fc5737ffff49ed268e8aa39b215a6a3f2b720bce3531a16e8d24a0`.
- Independently retrieved the pinned repository `data/k4.json`; the 97-letter canonical ciphertext and all 24 fixed plaintext clues match exactly. Ciphertext SHA256: `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.
- The exhaustive reference completed 408,960 routes and 22,901,760 route/period/convention trials. Production reports complete prefix enumeration with an empty compatible-family set.
- Inclusive target CPU: production 0.015615 seconds; reference 1.588733 seconds. Maximum conservative worker-plus-child peak memory: 19,374,080 bytes. Resource receipts and shared budget are valid.
- No target rerun was performed by this audit. Audit CPU was 0.0046 seconds; charge one second conservatively.

This excludes only the frozen eight AZ/KRYPTOS alphabet-role/sign conventions, widths 6–9, arbitrary output-index key periods 2–8, fixed literal clues, and unpadded ragged columnar transposition followed by arithmetic. It does not exclude feedback, other alphabets, other bounds or arbitrary compositions. The earlier synthetic ambiguities are retained and do not become target solutions.

Canonical source: https://github.com/reggiechan74/kryptos-k4/blob/e589286feedd6c3b52959418acd848f0a54a62b5/data/k4.json
