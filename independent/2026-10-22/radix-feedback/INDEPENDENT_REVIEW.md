# Independent review: frozen-glyph affine feedback audit

Independent result: all eight specified feedback families are impossible on the training crib, even allowing unrelated integer bases ≥2 at every position. No heldout evaluation was performed.

## Verified inputs

- Specification SHA256: `caa60d80cf41e7b0a498eeaff62a14b84ef250c44756762fcf84878cfb2c6e5f`
- Geometry SHA256: `6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010`
- Schema amendment SHA256: `01982c71b729ec5673c9ba52a63a6e699e3955a05af3c8ee25ead8265795683d`
- Ciphertext positions 22–34: `FLRVQQPRNGKSS`
- Plaintext: `EASTNORTHEAST`

## Parity theorem

For `code_b(T) = Σ v_j b^j`, even b gives v_0 modulo 2; odd b gives Σv_j modulo 2. Thus every modular-26 recurrence must satisfy the corresponding modulo-2 recurrence.

All certificate glyphs have even codes for every integer base:

- E: b³¹+b²⁸+b²⁶+b²⁴
- S: b⁸+b²
- L: b³¹+b²⁴
- Q: b¹³+b
- T: b²⁹+b²⁸

Consequently, their transitions reduce to `k_(i+1) = a·k_i+c` modulo 2, independently of d and base.

## Exact minimum contradiction certificates

Lexicographic tie-breaking is by transition start position. Positions are 1-based, and updates occur after the source letter.

1. **AZ, plaintext source:** 22→23 and 24→25. E requires a+c=1; S requires a+c=0.
2. **AZ, ciphertext source:** 23→24 and 26→27. L requires a+c=1; Q requires a+c=0.
3. **KRYPTOS, plaintext source:** 22→23 and 29→30. E requires a+c=0; T requires a+c=1.
4. **KRYPTOS, ciphertext source:** 23→24 and 33→34. L requires c=1; S requires c=0.

Each applies to both additive and true Beaufort. All eight parity triples were explicitly checked against each certificate. Two transitions are minimum because any single transition admits a=d=0 and c equal to the required next-key parity. Exhaustive subset enumeration confirmed the stated lexicographic choices; numbers of minimum two-transition cores are respectively 5, 7, 4, and 5.

## Full keys

Keys at positions 22–34, using zero-based indices in the designated alphabet:

- AZ additive: `[1,11,25,2,3,2,24,24,6,2,10,0,25]`
- AZ Beaufort: `[9,11,9,14,3,4,6,10,20,10,10,10,11]`
- KRYPTOS additive: `[1,10,21,18,1,15,2,23,5,2,19,0,2]`
- KRYPTOS Beaufort: `[23,24,7,0,13,25,4,5,7,24,7,12,10]`

The equations genuinely produce different full keys: additive requires K=C−P, whereas true Beaufort requires K=C+P. Their parity sequences coincide because `(C+P)−(C−P)=2P`:

- AZ: `1110100000001`
- KRYPTOS: `1010110110100`

## Independent cross-checks

- Enumerated all 17,576 coefficient triples for each family, independently allowing every code residue obtained from bases 2–27 at each transition. All eight families have zero survivors. These bases represent all residues modulo 26, so they cover every integer base ≥2 for an integer-coefficient polynomial modulo 26.
- Reconstructed vectors from frozen sparse components and feature order; verified 35 unique ordered primitives and binary counts.
- For all 26 glyphs, compared exact polynomial, Horner, modular evaluation, and parity at bases 2–61 and 10⁵⁰+2,+3. All agreed.
- Generated positive synthetic cases for all eight families with after-letter updates, varied bases including huge bases, and planted coefficients (17,9,23). Both solvers retained the planted coefficients, and reconstructed full keys matched exactly.

The missing stored-vectors field is the only specification issue found; the supplied amendment correctly repairs that validation control without changing the mathematical family. The independent reviewer did not inspect the primary audit script. Calculations initially ran read-only; only this report and its companion replay script were subsequently written for packaging.

## Scope

The conclusion is restricted to this frozen-glyph first-order affine feedback family. It does not exclude other geometric ciphers or establish anything about their historical intent. Neither the auxiliary direct-map claim nor the heldout crib was evaluated by this independent reviewer.

The companion `independent_verify.py` reproduces the independent calculations from the pinned inputs, reads no primary audit code, and writes no files.
