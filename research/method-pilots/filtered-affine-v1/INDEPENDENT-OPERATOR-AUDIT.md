> **Dated source/mathematics record.** Read DECISION-STATUS.md and INDEPENDENT-OPERATOR-AUDIT.md for later resolutions; earlier pending gates remain historical. Public prose sanitization is explicit in PUBLIC-PROVENANCE.json.

# Independent audit: global sparse-law operator separation

31 October 2026. Scope: source equations and general mathematics only. No target fit, target feature matrix, holdout, external-source execution, remote edit, or target admission. This is an audit of the operator argument, not a prior-art completion certificate.

## Verdict and exact scope

**Valid with the explicit quantifiers below.** A ciphertext-history law

`P_i = C_i - F(C_(i-1), ..., C_(i-6)) (mod 26)`

whose quadratic-plus-full-equality canonical descriptor has a nonzero equality coefficient cannot equal any one fixed operator in the stated fixed-alphabet causal linear-feedback grammar. The proof does not use the at-most-three-term restriction; that restriction remains relevant to the proposed family, not to this separation theorem.

Separately, a law with at least three globally reachable F-values cannot be contained in one fixed two-value carry relation, under any fixed plaintext/ciphertext alphabet permutations.

Neither statement excludes coincidental finite-message matches, matches to the 24 retained observations, or overlap after fitting a different comparator to each input. Neither certifies global historical novelty or admits a target run.

## 1. Comparator grammar and quantifiers

Let A and B be fixed bijections of Z26; let epsilon_C and epsilon_P be signs. Define the arithmetic key rank by

`kappa_i = epsilon_C B(C_i) + epsilon_P A(P_i)`.

The comparator has strictly causal linear feedback

`kappa_i = d_i + sum_(j>0) [a_j kappa_(i-j) + b_j A(P_(i-j)) + c_j B(C_(i-j))]`.

The displayed sums can be any fixed finite lag set. Coefficients, alphabet maps, initialization, and offsets are chosen once, independently of the input. The offsets d_i can be arbitrary deterministic position functions, including drift and periodic offsets. Position-dependent feedback coefficients also cause no difficulty if still input-independent: the proof fixes one time. What is not covered is arbitrary nonlinear feedback, different unlinked alphabet maps inside individual terms, noncausal access to future symbols, arbitrary tableau quasigroups, or input-dependent parameter/seed selection.

Operator equality means equality for every input under these fixed choices, at all sufficiently long prefixes. For a law specified only after six initial symbols, either explicitly fix a causal initialization or compare sufficiently beyond the initial region; do not manufacture six initial plaintext symbols from a tail-only model. With finite maximum feedback lag L, a comparison position after both the six-symbol initial region and all L delayed law evaluations suffices.

Why arbitrary histories are legitimate: with any fixed initial ciphertext history, `C_i = P_i + F(C_(i-1), ..., C_(i-6))` is a triangular bijection on finite streams. Consequently every ciphertext prefix, including every independent six-symbol history, is reached by some plaintext prefix. No language restriction is allowed in this universal operator quantifier.

## 2. Fixed alphabets force an affine key on the image of F

Write S = im(F). Fix a history and vary only the current ciphertext symbol c. Strict causality keeps kappa fixed while the sparse law gives P = c-f. Thus

`epsilon_C B(c) + epsilon_P A(c-f) = r(f)` for every c in Z26 and f in S.

The right side depends only on f: the left side has exactly the same value for any two histories attaining the same f. Fixed A and B also make r independent of the position.

Fix f0 in S. Subtraction shows that `A(t+d)-A(t)` is independent of t for every d in S-S. Translation composition extends this to H = <S-S>, yielding a well-defined homomorphism D:H -> Z26 with

`A(t+d) = A(t) + D(d)`.

It is injective: D(d)=0 would give A(t+d)=A(t), and A is a permutation. Every injective homomorphism on a subgroup H of Z26 extends to multiplication by a unit u of Z26. Explicitly, |H| is 1, 2, 13, or 26. For order 13, choose the odd one of the two lifts of the nonzero multiplier modulo 13; for order 2, any unit has the necessary action; the trivial and full-group cases are immediate. Thus

`r(f) = v + w f` on S, with `w = -epsilon_P u` a unit modulo 26.

This does NOT assert that A and B are globally affine. They need only be affine along H-cosets. In particular, assuming S spans Z26 is unnecessary, and dividing by a possibly nonunit equality coefficient would be an error.

## 3. Eliminate plaintext and isolate the earliest equality pair

Use

`A(P_i) = epsilon_P kappa_i - epsilon_P epsilon_C B(C_i)`

and `kappa_i = v+wF_i` in the recurrence. Since w is a unit, a putative equality of operators implies

`F_i = q_0(i) + sum_(j>0) q_j F_(i-j) + sum_(j>0) t_j B(C_(i-j))`.

Choose ONE CRT field p in {2,13} in which an equality descriptor is nonzero. Within that field choose the smallest pair start m in {1,3,5} with nonzero coefficient e. Write z=C_(i-m), w=C_(i-m-1), and fix every other ciphertext symbol involved.

The current equality term becomes e*1[z=w], with equality evaluated on the full 26 symbols, not on residues modulo p. No delayed nonzero equality term can have this same pair: it would have to come from an earlier pair start m-j<m, whose coefficient is zero in the chosen field. Any delayed equality involving only one of z,w is univariate after the other symbols are fixed. Equalities involving neither variable are constant.

All ordinary degree-at-most-two terms, including delayed copies, reduce to a constant plus univariate terms plus one scalar multiple of `(z mod p)(w mod p)`. The alphabet terms B(C) are also univariate. The alleged identity therefore has the form

`e*1[z=w] + a*(z mod p)*(w mod p) + f(z) + g(w) = 0`

for all 26-by-26 choices of z,w.

The equality-value matrix is e*I_26 and has rank 26 over F_p, since e is nonzero. The other three matrices have total rank at most 3: one outer product for the bilinear term, one for f(z), and one for g(w). Contradiction.

**Terminology correction:** rank 26 applies to the uncentered equality-value matrix. A doubly differenced/centered equality interaction matrix has rank 25. Either gives a contradiction with the appropriate low-rank bound, but one must not call the centered interaction rank 26.

This argument respects the canonical CRT descriptor, including parity square/linear aliases. It never infers equality nonlinearity from a merely nonzero raw coefficient in an arbitrary representation.

## 4. Two-value carry relation

Scott's carry source tests a set-valued condition, not a deterministic linear recurrence. For fixed alphabet pair, fixed signs, fixed period, and fixed base value a_r at a position's residue r, it requires

`kappa_i in {a_r, a_r+1}`.

Fix a position with arbitrary reachable six-symbol history and fix the current C_i=c. The induced key is

`epsilon_C B(c) + epsilon_P A(c-f)`.

This is injective as a function of f in S. Therefore |S|>=3 is incompatible with the one fixed two-value set at that phase. Arbitrary fixed alphabets do not change this counting argument. No causal independence of the carry choice is assumed or needed.

The same proof works for any two-element allowed key set, not only an adjacent pair. It does not classify the binary-valued boundary. That boundary really can overlap: F=1[C_(i-1)=C_(i-2)] has S={0,1}, and under identity alphabets/Vigenere arithmetic is contained in Scott's period-one pair {0,1}. Thus E alone cannot be declared disjoint from carry.

## 5. Source grammar mapping

Read-only inspection of the retained pinned sources confirms:

- [Scott run_chain.py](https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/run_chain.py) uses fixed plaintext/ciphertext alphabet ranks, the three signed current-symbol arithmetic rules, and linear combinations of lagged plaintext/ciphertext ranks with position drift and a constant. Its lag sets are (1), (2), (3), (4), (5), (7), (1,2), (1,3), and (2,3). Set a_j=0 in the comparator above.
- [ActiveTK E220](https://github.com/ActiveTK/dekrypt/blob/992c9668b9f0783221cb570abbff969e59cbf27c/src/e220_linrec_chain_exact.cu) uses one arbitrary shared alphabet, three lags of key/plaintext/ciphertext ranks, coefficients in {-1,0,1}, and a free constant. Set A=B and restrict the recurrence coefficients accordingly.
- [Scott carry.py](https://github.com/scott-dunphy/kryptos-k4/blob/a75178587efe9401ebf2a4edf3828472dd6fb2a2/novel/carry.py) checks whether each periodic residue's observed derived-key values are at most two and, when there are two, adjacent modulo 26; periods 1 through 30. It permits a set of finite-trace fits; the global counting argument only excludes an entire fixed law from one fixed carry parameterization.

These are mathematical containments of the source grammars in the comparator classes, not a re-verification of reported external campaign completion or exact-negative certificates. More complex nonlinear stage grammars and unspecified third-party recurrence claims require separate inspection.

## Final boundary

The permitted conclusion is **global operator separation of E from the specified fixed-alphabet causal linear class, and of all >=3-valued laws from any fixed two-value carry relation**. It is not target exclusion, finite-observation separation, proof that all remaining laws are new, or permission to reopen old target work.

## Addendum: exact Scott carry intersection independently verified

The stronger section 5 claim in `OPERATOR-MAP.md` was subsequently checked. **It is valid:** within E and the pinned Scott alphabet/rule domain, the global intersection is exactly

`C = {b + E12, b - E12, b + E34, b - E34, b + E56, b - E56 : b in Z26}`,

containing 156 distinct functions. This strengthens the conservative cardinality result above; it still concerns containment of an entire fixed operator in a fixed set-valued relation, not finite-trace separation.

### Binary image under arbitrary fixed alphabets

Suppose im(F)={f0,f1}, with d=f1-f0 nonzero. For every current c the two distinct inferred keys must be exactly the same adjacent pair. After subtracting the B(c) contribution and accounting for signs, the unordered pair `{A(c-f0),A(c-f1)}` is one ordinary cycle edge. Because B is a bijection, these pairs, as c ranges through all symbols, are all 26 ordinary-cycle edges exactly once.

The source pairs `{t,t-d}` have the graph structure of translation by d. For d=13 there are 13 edges each repeated twice. For nonzero even d there are two disjoint 13-cycles. Only unit d yields one simple 26-cycle. A therefore is a cycle isomorphism from the step-d cycle to the ordinary cycle, so `A(t)=u*t+a0` with `u*d=+1` or `-1`. Fixedness of the key pair then forces `B(t)` affine with slope `-epsilon_C*epsilon_P*u`. This rules out nonlinear fixed-alphabet exceptions rather than assuming them away.

An independent literal-only reconstruction of the pinned alphabet generator tested every one of the 312 unit-affine rank maps against every retained alphabet. It found 53 retained forward alphabets and just one affine map: AZ, slope 1 and offset 0. Receipt: `INDEPENDENT-SCOTT-ALPHABET-CHECK.json`. No external source was imported or executed; no ciphertext or plaintext input was used. Thus the actual Scott domain can contain a nonconstant globally binary F exactly when its two values are adjacent, via AZ/AZ Vigenere. Larger periods do not add a stationary global law: the full possible inferred-key set is the same at every phase, and hence a period-one base pair already suffices.

### Adjacent-image functions in the dictionary

Write the mod-13 descriptor as `Q(x mod 13)+sum e_m E_m`, with degree(Q)<=2. Choose opposite parity inputs within every designated pair. This forces all full-symbol equality indicators to zero while leaving the six mod-13 inputs unrestricted. If Q were nonconstant, a suitable coordinate line would give a nonconstant univariate polynomial of degree at most two, whose image has at least seven values. This is incompatible with an adjacent two-value image. Hence Q is constant.

The equality indicators on the three disjoint pairs can be toggled independently. Any two nonzero coefficients over the odd field F13 produce at least three subset-sum values: `{0,a,b,a+b}` cannot have at most two values when a,b are both nonzero. Thus there is at most one nonzero e_m. There must be one, since two adjacent Z26 outputs have distinct mod-13 residues.

Those two mod-13 residues identify which of the two full adjacent outputs occurred. Their parities differ. Therefore the mod-2 function is a constant plus exactly the same full-symbol equality indicator. Canonical descriptor uniqueness removes all other coordinates. The resulting full Z26 equality coefficient is +1 or -1, giving exactly C above. Each law has support at most two, so the sparsity restriction does not remove any of the 156 laws. Distinctness follows from independence of the equality indicators and from 1 not equaling -1 modulo 26.

Implementation-facing membership: for one chosen equality coordinate q, alpha is zero outside {constant,q}, alpha_q is 1 or 12 in F13, beta is zero outside {constant,q}, and beta_q=1. Constants are unrestricted.

The inherited B exclusion has not been reviewed in this addendum; it is a separate receipt/semantic implication check.

## Addendum: inherited B implication verified from retained receipt

the existing `results/RECURRENCE-CERTIFICATE-REVIEW-001.json` alone was inspected. Its SHA256 is `03bbae7ed8950b72da8c132ad028ad714aa92126d77ce39bac33c816a0029f25`, matching the source admission report. No canonical target data was reloaded, and no target matrix, fit, key extraction, or experiment was recomputed.

The receipt records AZ/Vigenere grammar `C_i=P_i+K_i`, with recurrence `K_i=a*K_(i-1)+b+d*C_(i-1)`. Its retained AZ contradiction rows are:

- From position 23: ciphertext 11, required key at position 24 is 25.
- From position 24: ciphertext 17, required key at position 25 is 2.

Positions are one-based. Both previous ciphertext values are odd, while the required next-key parities differ. A sparse global descriptor whose beta is supported only on {constant,lag1} has exactly `F_i mod2 = beta_0 + beta_1*(C_(i-1) mod2)`. It therefore predicts the same parity at positions 24 and 25, contradicting the two retained requirements. This is the a=0 restriction of the already contradicted grammar; no choice of alpha/mod-13 coefficients can alter the mod-2 contradiction.

**Verdict: the B semantic transfer is valid.** Both involved law evaluations are strictly inside the modeled tail and the first known crib, so it requires no recovery of the first six plaintext symbols, no guessed seed, no invented premesssage history, and no inference across an initialization boundary. This is an independently checked implication from an existing verified receipt, not independent re-authentication of that receipt's canonical fixture extraction. The KRYPTOS portion of the receipt is not needed for this transfer.

## Limited additional R6 source check

The pinned `src/e167c_twokey.cu` functions/lines identified in `E167-R6-SUPPLEMENT.md` were independently read: `r6f` at lines 20-23 uses only current p,c,k2; lines 40-43 select fixed position residues; lines 109-114 construct fixed periodic key arrays and apply them positionwise. No history update appears in those reviewed equations. This supports the stated position-only grammar mapping. Separation from E applies to each fixed deterministic invertible per-symbol operator. It must not be silently restated as exclusion from an arbitrary set-valued/noninvertible per-symbol relation; not every operation/chart helper was independently audited here. Source campaign completion and solver correctness are outside this review.

The source owner supplied a cleaner forward-direction argument, which also checks independently: fix current plaintext p and choose reachable predecessor histories with different F. Then the sparse law gives different ciphertexts `C=p+F(history)`, whereas any one fixed deterministic positionwise forward map gives only one ciphertext for p. This needs no inverse assumption. Arbitrary set-valued/nonfunctional relations remain outside that argument. The source's `buildTabs` lines 603-605 also explicitly checks that each operation/parameter induces a permutation; this source assertion was read, not executed.
