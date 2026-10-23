# Arbitrary-key Fractionated Morse: exact local rejection

23 October 2026. MASK-FM-ARBITRARY-007 closes the arbitrary-alphabet gap in the earlier two-key pilot. Every first-crib word-break/stream-offset context rejects. This is a conditional exclusion of a direct standard Fractionated Morse model, not a general rejection of Morse, fractionation, preprocessing or layered ciphers. No plaintext candidate was generated.

## Why this test

The 60-entry register contains two nominally untested families, lamp-to-Greek and Wheatstone. The former lacks a justified ordering, framing and reversible bridge; the latter has substantial pinned prior-art coverage, including outer-alphabet reversals. Neither is improved by another arbitrary sample. Physical models still lack measured inputs; unknown SIGABA controller inference remains resource-unresolved; arbitrary three-round functions were proved non-identifiable. The construction-error sensitivity arm lacks an independently observed K4 discrepancy.

H-MASK-FM had a different, tractable gap: only AZ and KRYPTOS trigraph maps were previously tried. An arbitrary permutation contains every keyword alphabet. Repeated cipher symbols impose exact constraints, so no keyword selection or 26!-key enumeration is needed. The [ACA procedure](https://www.cryptogram.org/downloads/aca.info/ciphers/FractionatedMorse.pdf) was freshly read before freezing the [protocol](FRACTIONATED-MORSE-ARBITRARY-SPEC.md). Its historical availability and the sculpture's separate Morse material are context, not evidence that Sanborn chose this particular cipher.

## Exact coverage and result

The standard A–Z Morse dictionary, x letter separators, xx word separators, fixed three-symbol groups and one shared cipher-symbol-to-trigram mapping are unchanged. All 4,096 internal word-break masks for EASTNORTHEAST are tested. Its first Morse symbol can start at each zero-based stream offset 42 through 126: 21 preceding decoded letters plus their separators require between 42 and 126 symbols. This is not an assumption that decoded-letter indices equal ciphertext indices. No particular prefix, gap, word segmentation or total plaintext length was invented.

All **348,160 raw mask/offset contexts reject**, with zero compatible local domain records, zero budget-unresolved contexts and zero Berlin evaluations. These contexts are not 348,160 independent keys or statistical trials. One map would have to satisfy at least one context; every context instead assigns conflicting ternary symbols to the same coordinate of the same cipher letter's trigraph. Thus even a non-injective fixed cipher-to-trigram assignment could not repair these local conflicts; bijectivity and global Morse parsing are not needed for the actual negative proof.

For example, no internal word breaks and offset 42 put relative pattern positions 12 and 15 at coordinate zero of ciphertext B's trigraph. They require dot and dash respectively. The [native receipt](../results/MASK-FM-ARBITRARY-007.json) retains the complete rejection tally and input hashes. The independent oracle's canonical certificate stream covers every context; its reproducible digest is `b649b0ef2c4007360dc6fbcf836f988b511b93a23bb1bcb4a53d68a2097326ad`.

The [independent coordinate-slot oracle](../experiments/fractionated_morse_oracle.mjs) uses explicit coordinate equalities rather than production bitmask intersections and permutation counting. It independently rejects all contexts: 225,152 first conflicts at coordinate zero, 77,568 at coordinate one and 45,440 at coordinate two. [Receipt and example certificates](../results/MASK-FM-ARBITRARY-007-independent.json). This is verification of the same domain, not another search count.

## Validation and staging

The protocol was committed at `ceeae63` before implementation. The controlled implementation was committed at `c3d75fa` before K4 evaluation. The JavaScript verification was written after the actual result and is labeled accordingly.

[Controls](../results/MASK-FM-ARBITRARY-007-controls.json) reproduce the published COME AT ONCE example and its inverse, compare exact feasibility/counts/witnesses against 100 complete small permutation domains, and retain six planted keys under complete 348,160-context first-stage selectors. Plants have literal disclosed crib strings at their true decoded-letter positions, unrelated surrounding text, varied spaces and arbitrary nontrivial alphabets. Their ciphertext lengths need not be 97. Full encoding/decoding roundtrips pass. A direct substring oracle checks 102 windows, including all three boundary phases. Mutated empty-domain and injectivity cases reject; an intentionally exhausted completion cap reports unresolved rather than zero.

These controls demonstrate truth inclusion, not unique key recovery. Partial-context key completion counts can overlap across contexts and are never summed into a distinct-key or plaintext count. No actual second-stage join ran, because the first stage already rejects; no claim that it recovered a complete prefix/gap parse is made. No null simulation or significance estimate is required for an exact contradiction, and Berlin is public rather than historically untouched data.

## Limits and frontier

The proof assumes the disclosed English strings occur at the declared decoded-letter indices, standard A–Z Morse, separators of length one or two, a fixed grouping from the start and a memoryless cipher-letter/trigram assignment. Digits, punctuation, nonstandard codes, altered separators, state-dependent trigrams, routes or an outer cipher are outside coverage. An actual different historical specification could justify a new protocol; changing these choices solely to rescue the failed model would not supply evidence.

The strongest remaining frontiers need a concrete missing ingredient: independently constrained SIGABA control/index states or a scalable joint solver; source-grounded Wheatstone conventions outside reviewed coverage; a justified lamp/Greek bridge; or measured physical geometry/historical clock registration. The existing Gromark and three-round fits need independent key restrictions or non-fit plaintext evidence. More arbitrary function entries, roots, glyph orders or cipher layers would increase flexibility without solving identifiability. No claim of globally exhausting K4 follows from this bounded result.
