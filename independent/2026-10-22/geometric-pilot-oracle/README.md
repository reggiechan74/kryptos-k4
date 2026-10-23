# Independent bounded geometric-code pilot audit

Geometry: MODELED-UPPERCASE-GEOMETRY-001. These canonical glyphs are invented declarations, not measured Kryptos glyphs. SHA-256 is verified before a run; no geometry is optimized against ciphertext.

## Result

Frozen ranked alphabet: OCSQVXWAGZITYDPBRKLFENMHJU.

- Pilot 1: 24 cases (addition and true Beaufort, periods 1–12). One first-crib survivor: true Beaufort, period 12. Its key is [15,24,3,4,1,18,2,24,4,13,25,18]. Its second-crib window is ZBVJDFKRUCA, not BERLINCLOCK. Zero exact survivors.
- Pilot 2: 3,640 cases (26 letter seeds × 35 left rotations × 2 alphabets × 2 feedback sources). Zero first-crib or exact survivors.
- This is only a bounded negative for these frozen hypotheses. It does not rule out all geometric encodings or indicate historical support for these particular constructions. No null experiment or significance claim is made because there are no actual survivors.

## Reproduction

Python 3, standard library only. From this directory:

    python oracle.py --core geometry-core.json --full geometry-full.json --source k4.json --output rerun.json

For only synthetic controls, append --controls-only. Controls run before K4. The oracle derives integer codes directly from primitive memberships, then checks the full schema's stored vectors and decimal encodings. It does not trust those precomputed code values as its calculation.

Pilot 1 uses rank-alphabet indices: C=P+K for addition and C=K-P for true Beaufort, modulo 26. Fit only EASTNORTHEAST at 22–34, then check BERLINCLOCK at 64–74 without refitting. The 13-character first crib fixes every key residue for every tested period, so passing keys have no free entries. Berlin is a public second-stage check, not a blind holdout. All periods are tested so previously known structural eliminations do not change the family.

Pilot 2 uses integer state S0=code(seed), C=P+(S mod 26), then S'=rotl35(S,r) XOR code(T), where T is plaintext or ciphertext. Rotation is applied before XOR, state is 35-bit, output indices use AZ or KRYPTOSABCDEFGHIJLMNQUVWXZ, and ciphertext is processed forward with no resets. Decryption is causal in both variants.

## Controls and equivalences

- 2,205 bit-rotation comparisons against an independently implemented bit-placement reference, including bit 34 and all one-hot states.
- 3,640 encrypt/decrypt roundtrips covering every member of the rotor family.
- Six positive periodic plants searched across the full 24-model family.
- Twelve rotor plants with literal cribs and r=0,17,34 searched across the full 3,640-model family.
- 156 alphabet-origin rotation comparisons. Rotating alphabet indices changes neither physical additive shifts nor rotor outputs. For true Beaufort, rotating alphabet indices is absorbed by changing unrestricted keys.
- Feature-column reversal preserves codebook uniqueness but changes arithmetic-cipher behavior, illustrating why primitive order must remain frozen.
- One synthetic rotor plant yields two distinct plaintexts that both satisfy all 24 crib letters; all candidates are retained. Exact cribs need not establish model or plaintext uniqueness.
- Plus/minus unrestricted additive keys and key starting phase are redundant choices. Keys with shorter fundamental periods should not be described as independent discoveries.

Never use JavaScript Number bitwise operators for the 35-bit state; use BigInt or arbitrary-precision integers. Raw model counts are not claims of independent statistical tests. Any future significance calibration must repeat the entire fit/select procedure for every null and retain all surviving models.

## Source

K4 and cribs independently read from https://github.com/reggiechan74/kryptos-k4/blob/0d138240fb248d0b74942efc86a51d895946921d/data/k4.json . Git blob SHA: 361714e4d9b19393bcc89df59e73d1c0522eeedb. Data-source and artifact hashes are recorded in manifest.json.
