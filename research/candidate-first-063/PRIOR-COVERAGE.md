# Study 063 external operator-equivalence review

31 October 2026. Read-only source review and algebra, no K4 constraints or external-program execution. The source files below were fetched at exact public commits and their bytes verified against Git blob IDs. Copies stay private; public delivery uses URLs, hashes and this original analysis.

## Admission decision and limits

The proposed persistent 26/24 carry state with OLD-high-digit output is not the operation tested by the inspected prior campaigns. No known whole fixed-parameter subdomain alias was identified. This is bounded prior-work clearance, not a proof that every ciphertext/plaintext pair is disjoint from every old model, a global novelty claim, or evidence of Sanborn's method. The local radix family is nonlinear and needs the separate stronger witness audit; it must NOT be dismissed merely as linear feedback.

The zero key does not make the proposed cipher a pure transposition or identity: the state still accumulates plaintext and carries. No zero-key exclusion is imported from061/062. Individual messages can avoid a carry for a time, but that conditional trace is not an entire fixed-key cipher domain; removing all such keys would be unsound.

## Exact inspected sources

Scott source pin `a75178587efe9401ebf2a4edf3828472dd6fb2a2`:

- [novel/carry.py](https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/carry.py): direct inferred key values in each residue class must lie in one adjacent pair modulo26, periods1–30 and fixed alphabet pairs. This is a set-valued adjacent-noise constraint, not a retained quotient accumulating modulo24. Do not misdescribe this as an ordinary deterministic linear recurrence. The proposed effective shift a+h+K can vary across26 values as prior inputs vary; it is not constrained to one fixed adjacent pair by the proposed equations. This distinguishes operations, but is not a universal disjointness theorem for coincidental finite-message fits.
- [novel/run_chain.py](https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py): fixed affine mod26 combinations of lagged plaintext/ciphertext ranks plus position drift/constant; lag sets(1),(2),(3),(4),(5),(7),(1,2),(1,3),(2,3). Current-symbol tableau arithmetic and fixed alphabets. No persistent nonlinear quotient state.
- [run_digitcode.py](https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/run_digitcode.py): per-symbol mixed-radix digit-wise keyed shifts WITHOUT carry, radices(2,13),(13,2),(3,9),(9,3),(4,7),(7,4),(5,6),(6,5),(3,3,3), periods1–26/31. All positions are independent conditional on key phase; invalid alphabet cells rejected. Not a message-driven cross-letter state.
- [run_clock16.py](https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/run_clock16.py): fixed World-Clock city/ring-derived alphabets with periodic direct additive/Beaufort/variant arithmetic, periods1–30. An artifact-themed alphabet does not implement coupled carry. An initial attempted `novel/run_clock16.py` URL returned404; tree inspection located the correct root file. No source substitution was hidden.

Zeyeteam source pin `00696f393c861db2dcfaf3adfef29823c601cf7a`:

- [scripts/odometer.py](https://github.com/zeyeteam-debug/kryptos-k4-eliminations/blob/00696f393c861db2dcfaf3adfef29823c601cf7a/scripts/odometer.py): odometer shift a[i mod p]+b[floor(i/p) mod q], p,q2–24 with p+q<=20; Alberti shift a[i mod p]+d floor(i/N), p1–18,N2–48. Both position-driven. Its M3 24-hour-clock comment has no corresponding yielded model in this file; do not count a comment as executed coverage.

## Normal form and separation from all fixed-alphabet linear recurrences

Let T=26h+a modulo624. Then T'=T+x+K modulo624, while output is y=(low(T')+high(T)) modulo26. The nonlinear readout and old-high timing matter; the machine is a scalar modular accumulator, not an invented physical gear system.

For EVERY fixed initial state and key, select x0 so that a1=(1-k1) modulo26. Then a1+k1 is1 or27. Holding x2 fixed, outputs at the third position for x1=0,1 have difference1 modulo26; x1=25 causes one extra high-digit carry, changing that affine prediction by1 or−23 (equal3 modulo26). Thus the plaintext-to-ciphertext function is non-affine even for zero key. No whole initial-state/key member equals a native-coordinate affine mod26 recurrence.

Fixed nonlinear alphabet relabelings do not silently evade this argument for the inspected direct cyclic-tableau linear class. After two input letters, T spans51 consecutive states modulo624 and therefore contains a complete aligned26-state block. The next conditional shift a+h+k spans all26 values. If an equivalent fixed input/output alphabet pair represents these same cyclic translations, its relabelings f,g satisfy f(x+s)=alpha*g(x)+b_s for every x,s. The conditional26-symbol bijection forces alpha to be a unit; subtracting s=0 forces f and g to be affine unit relabelings of the cyclic group. Those cannot remove the non-affinity above. This proof applies to the stated fixed-alphabet causal affine class, not arbitrary nonlinear state machines or set-valued noise constraints.

For arbitrary position-only per-symbol substitutions (including digitcode and autonomous odometers), two different prefixes can reach different shifts at the same position while the current input is held fixed. A position-only map cannot reproduce both. This is an operator distinction, not another target search.

## Local and control gate still required

The local radix model uses nonlinear fixed glyph codes; implementation owner supplies synthetic parity-separation witnesses covering both input/cipher source modes, alphabets and key digits, with a reachability proof. An independent reviewer must verify those witnesses and this algebra before freeze. Complete tiny truth sets and fresh whole97-character benchmark remain mandatory. No target result or probable solution follows from prior-work admission.

## Reproducibility and resources

`SOURCE-INVENTORY.json` records source URLs, exact Git blobs and SHA256. A local file-writing helper initially introduced one extra terminal newline; removal restored each fetched source's exact published Git blob, verified before review closeout. Neither variant was executed. Source inspection is read-only; no cryptanalytic computation was performed in this external review. Conservatively charge30CPU seconds for source reconstruction/hash administration (reserve, not a measured cryptanalytic runtime); the implementation owner's independently measured algebra controls are separate.
