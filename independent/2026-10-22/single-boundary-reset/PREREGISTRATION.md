# K4 independent bounded reset audit preregistration

Recorded before evaluation, 2026-10-22 UTC. Scope is fixed as follows.

Ciphertext: OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
Known plaintext, one-based: positions 22–34 EASTNORTHEAST; positions 64–74 BERLINCLOCK.
Alphabets: AZ=ABCDEFGHIJKLMNOPQRSTUVWXYZ; K=KRYPTOSABCDEFGHIJLMNQUVWXZ.
A boundary b denotes a reset immediately before position b+1, with b in 1..96; b=0 denotes no reset (not a reset at position 1).

1. Move-to-front model. Four fixed (reference alphabet R, initial mutable alphabet S0) pairs in {AZ,K} squared. Encryption emits S[index_R(P)] and moves the emitted symbol to front; decryption applies its inverse and the same update. At the boundary reset to the SAME S0. Test all 97 baseline/boundary settings for each pair.
2. Ciphertext-feedback affine-key recurrence. For each AZ or K coordinate alphabet, enumerate all (a,b,d,k) in {0,...,25}^4. C_i=P_i+K_i modulo 26, K_1=k; away from reset, K_i=a*K_(i-1)+b+d*C_(i-1) modulo 26. At boundary before b+1 reset K_(b+1)=the SAME k, skipping that transition. One shared tuple on both blocks. Test all 97 settings. Linear contradictions internal to known plaintext islands may certify all keys excluded; no use of division modulo 26 without checking invertibility.
3. Periodic additive control/exclusion. AZ and K coordinate alphabets, shared arbitrary key of period exactly dividing p for p in {8,10}, no reset or one restart of the same base key at b. No independent block keys. Test equality constraints on known derived-key coordinates, with boundary in 1..96. Derive per-island contradictions without assuming relative phase between islands.

No extra resets, extra alphabets, independently chosen reset states/keys, plaintext edits, ciphertext edits, anagramming or new models after results. Distinguish parameter counts, distinct plaintext classes, forced positions, and untested alternatives. If internal constraints make a full tuple enumeration redundant, retain an independent brute-force oracle on reduced modulus projections plus a complete exact enumeration of remaining candidate (a,b,d) and k. Include generated positive controls with the same encrypt/decrypt convention and multiple boundary placements, and mutation/negative controls.

Outputs: a reproducible Python script, machine-readable results, and concise report in /workspace/shared. This audit makes no positive decipherment or novelty claim.
