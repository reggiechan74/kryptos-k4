# Fixed masking-pilot outcomes

The language feasibility branch completed first. The two masking specifications
were then committed at `9f546aa279ec065f2a4788fe4a1895efbcf87750` before
implementation and K4 execution; code commit was
`705f65f50e95f8265f7227a2f91336f39091780b`. The local executor checked the
frozen specification bytes through GitHub before running them.

## MASK-AUTO-001

Exactly12 cases: two fixed alphabets × KRYPTOS/PALIMPSEST/ABSCISSA primers ×
plaintext/ciphertext feedback, with the registered addition recurrence. All12
produce complete deterministic97letter outputs and exact ciphertext regeneration.
**All12 fail the24English crib letters**; descriptive matches range0–3/24.
That rejects only these fixed complete models, not autokey or masking generally.
No language scoring, phase fitting, route, alternate equation, or extra key was used.

Preflight passes both hand vectors,72 short/boundary/repeated97letter round trips,
12 actual-scanner planted recoveries, and12 altered-crib rejections. Synthetic
outputs are test fixtures, not candidate K4 plaintexts. The run, including those
controls, took0.014seconds.

[Run manifest](../results/masking-runs/20261018T112316Z-4302f65c58784dc79d801f8a44609fff/manifest.json)
· [all12 complete outputs and24bit masks](../results/masking-runs/20261018T112316Z-4302f65c58784dc79d801f8a44609fff/MASK-AUTO-001.json).

## MASK-FM-001

Exactly two Fractionated Morse maps: A–Z and KRYPTOS over the registered triple
order and fixed separator/padding rule. Each maps the97cipher letters to291
ternary symbols. **Both fail on an internal run of at least three x separators.**
No plaintext is accepted or repaired; no crib score or regeneration is claimed
for an invalid parse. The complete streams and first rejecting condition are saved.
This excludes only these two literal maps, not keyed permutations, other framing,
or a Fractionated Morse component in an unspecified composite pipeline.

Preflight reproduces the ACA COME AT ONCE example exactly, including its two
padding x symbols, all26Morse letters/triples, terminal residue classes, one-letter
words, rejection cases, and two full actual-scanner planted recoveries. The
planted controls have97cipher letters and97final letters, with explicit spaces;
they demonstrate that crib indexing occurs after decoding and space removal.
The entire run took0.005seconds.

One implementation-authored negative fixture was corrected before the run:
`.-xx..` means A I and belongs in positive controls. The ACA vector and both
supplied autokey vectors were correct. See [fixture review](../docs/masking-fixture-review.md).
No cipher rule, key, alphabet, or K4 case count changed.

[Run manifest](../results/masking-runs/20261018T112317Z-3a585d17cef148e0a80c158a43e841dc/manifest.json)
· [both complete ternary streams](../results/masking-runs/20261018T112317Z-3a585d17cef148e0a80c158a43e841dc/MASK-FM-001.json).

Neither pilot identifies Scheidt's unspecified mask. Source-based distinctions
between statistical masking, semantic interpretation, and physical selection
remain in [the receipt](../docs/masking-source-and-pilots.md). No paid verifier,
outreach, arbitrary per-position mask, or expanded search followed these failures.
The next authorized extension is the user's separately specified word-interior
scrambling model using these same12autokey settings and two fixed segmentations.
