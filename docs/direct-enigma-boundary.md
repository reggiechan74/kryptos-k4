# Direct aligned standard Enigma boundary

DIRECT-ENIGMA-001 is an exact structural check, not a key search. At one-based
position 74, the confirmed BERLINCLOCK crib ends in K and K4 ciphertext is K.
Thus the direct aligned plaintext-to-ciphertext mapping has a fixed point.

Standard wartime reflector Enigma cannot encrypt a letter to itself. At each
keypress its mapping is a conjugate `P^-1 U P`, where the outward path P is a
bijection and the reflector U has no fixed points. If `P^-1 U P(x) = x`, applying
P would give `U(P(x)) = P(x)`, contradicting that reflector property. Stepping
does not change this per-keypress argument. Historical background links supplied
with this research request: [Bletchley Park](https://www.bletchleypark.org.uk/our-story/enigma/)
and [Imperial War Museums](https://www.iwm.org.uk/history/second-world-war/intelligence/how-alan-turing-cracked-the-enigma-code).
These pages were not independently retrieved during this coding update.

This rejects only direct, aligned standard wartime reflector Enigma for these
exact cribs and transcription. Extra substitutions, transpositions, encodings,
or other transformations can change the alignment or fixed-point constraint and
are outside the conclusion. No broader Enigma/composite family is eliminated.

The regression pins position 74 independently from the crib interval and uses
26 seeded toy bijections to illustrate conjugation. The toy reflector is paired
adjacent integers, not historical Enigma wiring. The proof, not a sampled rotor
scan, establishes the model boundary. Command:
`python3 -m unittest discover -s tests -p 'test_direct_enigma.py' -v`.
