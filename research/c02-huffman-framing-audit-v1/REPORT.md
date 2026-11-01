# C02 / N100-047 static source, framing and eligibility audit

2026-11-01 UTC. No target ciphertext read/transform/fitting, message batch, M21 execution, or experimental allocation in this audit. Static table derivation only. Canonical repository instructions, current catalog and M21 applicability notes were reviewed. No repo edits or external mutations.

## Decision

**Do not launch a C02 M21 capacity-count experiment. C02 remains target-not-admitted.** M21 has genuine bit-level information on the forward boundary stratum, but cannot eliminate this family or distinguish its seven phases; inverse target candidates already satisfy the capacity inequality by construction. This is not a negative K4 result, no extra backlog completion, and no evidence that Huffman is novel.

C02 is a completely specifiable partial reversible codec distinct from the inspected local/external maps. Missing operational choices prevent even its catalog-mandated synthetic admission gate from running: blind English generator/corpus/version/normalization and seed, minimum useful-capacity threshold, finite controls, independent decoder implementation, failure rules, resource cap and review. Exact external K4 coverage remains bounded by this search, not universal. No target proposal is authorized by this document.

## Exact finite map

Frequency order ETAOINSHRDLCUMWFGYPBVKJXQZ, ranks0..25, weights26-r, total351. Use a binary Huffman priority queue ordered by (weight, smallest AZ leaf). Pop two least nodes, first left/0 and second right/1; parent weight sum and leaf minimum. Live nodes have disjoint leaves, hence distinct minimum letters; the declared tie rule is total without insertion-order ambiguity. Reset root after each decoded leaf. No codebook learning.

SOURCE-POLICY.json fixes this interpretation; CODEBOOK.json contains26codewords and25merges. Length counts:11of4bits,7of5,5of6,1of7,2of8; Kraft sum256/256=1. Weighted length1569/351=4.470085...bits under the artificial weights, **not measured English capacity**. No empirical language distribution or historically selected tree is established.

Exactly97uppercase AZ plaintext symbols; concatenate their binary codewords, no spaces/EOF/header other than sentinel, no byte or terminal padding. For payload b of lengthL use N=2^L+value(b). Require N<26^97; oversize rejects, never clips. Render positional AZ digits (A=0) big-endian width97, retaining leading A. This is fixed width, not minimal width. N=0 invalid. Inverse removes the single most-significant binary1, parses all remaining bits, requires exactly97complete leaves and no incomplete suffix or extra symbols, and canonical re-encoding. The only outer layer is AZ Vigenere KRYPTOS, C_i=(Z_i+AZ(KRYPTOS[(i+phase)%7]))mod26, i zero-based, phase0..6. No other key, alphabet, reversal, byte convention or additional layer.

Proof: binary-tree code is prefix-free, so complete concatenations have unique parses. Sentinel preserves bit length and leading zero bits. Fixed-width positional radix representation is injective over0<=N<26^97; seven fixed outer shifts are bijections. Therefore each phase defines an injective **partial**97letter codec and unique inverse on its image. Different phases are descriptions, not independently evidenced keys. Exact97count supplies external framing, not an encoded count header.

## Capacity proof and M21 utility

Static integer arithmetic gives 2^455 <26^97<2^456. Consequently payload lengthsL<=454alwaysfit, L>=456neverfit, and L=455fits iff value(b)<B=26^97-2^455. STATIC-CERTIFICATE.json records exact integers. B in455bit binary starts1110110000001100.

The fixed table gives C=11111 and L=0000. The symbolic multiset67C+30L has455bits. Ordering all30L first starts0000 and therefore fits; ordering67C first starts11111 and fails, regardless of remaining suffix. This is an analytic witness, **not an encoded message experiment**. Thus the boundary restriction is not vacuous and a bit-aware count would improve a mere exact-length feasibility test for specified subfamilies.

Nevertheless, all97shortest-codeword messages have388payload bits and fit. All97longest-codeword messages have776bits and fail. Every outer phase has nonempty capacity because outer Vigenere changes no radix validity. A whole-family capacity filter therefore returns feasible for allseven. In inverse testing, each97digit AZ intermediate already represents0<=N<26^97: capacity is automatic, except zero rejection. A direct tree parse determines the image-membership conditions. Running a large forward DP to count all97letter strings is unnecessary to evaluate seven deterministic inverses and cannot substitute for the blind-English utility gate. Do not treat the M21 pilot's nontrivial toy exclusions as proof of benefit here.

## Prior-art exact-scope comparison

- Local043, COMPRESS-TRANSPORT-043-SPEC/FINDINGS: native full .Z/LZW bytes, big-endian integer;8positional/bijective,AZ/keyed,orientation transports; tested without extra encryption. Necessary magic-header failure covers those transports only. C02 lacks .Zheader/dictionary and uses fixed binary letters, sentinel, fixed width and explicit outer Vigenere. Not a repeat or a stronger solver of043.
- Local carried/splay-tree work H-TREE-STATEFUL/TREE-PATH-CIPHER-SPEC: persistent walk/access-splay state and geometry, not reset-to-root variable-bit prefix decoding. C02 does not change topology or carry tree state.
- EXT024 primary README pinned commit5a2a598cde181444769ef4fbe48dfb1bea12b44c, blob15eb9802fbeecb411cf0e2dce719df3b0eadf97c: describes one/two plaintext letters per ciphertext letter, bounded reuse and English-word/clue pruning. No binary prefix tree, sentinel whole-integer transport or completed exhaustive receipt established from that README. This is documentation-level scope, not independent source/run reproduction. https://github.com/neuroretransmit/kryptos-k4/blob/5a2a598cde181444769ef4fbe48dfb1bea12b44c/README.md
- Newly located primary Colossus documentation and primitive: Compressocrat is fixed ternary prefix coding followed by padding to trigraphs and keyed26letter substitution. That is a block-fractionation/key-search map, unlike C02's whole-message binary integer and seven fixed phases. CLAUDE documentation blob6b43b765c6d2fe012851a185abea2a634e34bd7b and src/polygraphic/compressocrat.c blob475604ef593ebcb88d081ad3d2ffcce7c700c033, fetched2026-11-01. Main URLs are mutable; blob identities pin fetched content, not a commit chronology. Code lines1–110 inspected, not executed. Project states K1–K4 purpose; **a Compressocrat K4 run/result is not verified**. https://github.com/stblake/colossus/blob/main/CLAUDE.md and https://github.com/stblake/colossus/blob/main/src/polygraphic/compressocrat.c
- Huffman's1952 paper is foundational, not a new cryptanalytic invention. https://compression.ru/download/articles/huff/huffman_1952_minimum-redundancy-codes.pdf

Finite indexed queries included Kryptos/K4 plus Huffman, prefix and compression; an exact matching C02 map was not established. Generic rafael-santiago/kryptos cryptography library, Swisslite messaging application and general compression discussions are not evidence of a K4 hypothesis test. Absence from indexed results does not establish absence from public/private work. Proposed external-register addition should classify Colossus as implemented related codec with K4-specific run unverified, not an externally rejected K4 model.

## Minimum next step, if prioritized later

No further capacity experiment is warranted merely to use M21. Before any actual codec gate, freeze an independently reviewed finite synthetic-only protocol: exact generator/source and fixed unseen97letter samples, meaningful predeclared capacity threshold (not retrofitted), total test counts, independent tree/serializer decoder, all codeword depths and non-byte-aligned leading-zero vectors, zero/oversize/incomplete-prefix/excess-symbol failures, allseven outer phases, runtime/memory bound and explicit stop-on-failure. Test table construction against an independent sorting/merge implementation and tiny exhaustive alphabets. Preserve oversize failures; do not select only representable English.

Catalog wording 'codewords crossing base26digit boundaries' needs correction: whole-integer radix conversion has **no fixed local bit-to-digit boundary**. Replace prospectively with length/integer threshold and leading-zero roundtrip cases, not invented local alignment.

Only after that gate passes and its exact scope/receipts are reviewed would a separate target proposal consist of exactlyseven inverse decodes, no search/fitting/rescue. That proposal must separately freeze evidence verification/full roundtrip and matched full-pipeline controls if making any significance claim. This audit does not supply a runnable target protocol or authorization.

## Execution boundary and limitations

One initial static derivation command had a syntax error before any Python execution; corrected static script generated the fixed table/constants. No97symbol message encoder was implemented or invoked, no synthetic batch run. No globally novel tactic established. No useful-capacity rate measured. No public target plaintext or raw ciphertext is an input artifact. This package is source/proof bookkeeping, not a fourth target-tested mechanism or a new M21 experiment.
