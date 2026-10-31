# Prior-art review: experiment coverage, proofs and statistical proposals

**Current navigation:** consult the [external hypothesis register](../research/EXTERNAL-PRIOR-ART.md) for the consolidated 31 October 2026 review and selection gate. This dated review and its original source pins remain unchanged evidence.

Revision date: **2026-10-18**. This is a bounded source/code review, not a new
cipher search or execution of either third-party project. Existing local proof
and experiment scopes remain unchanged. No K4 solution is claimed.

## Source pins and verification boundary

- [Barney's experiment map](https://barneyjm.github.io/kryptos-k4/), reviewed via
  its [pinned HTML source](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/docs/index.html)
  and [README](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/README.md)
  at commit `2db2722cc3f18c52d4d8369d7adc5a1db7e859d7`.
- [Scott Dunphy's repository](https://github.com/scott-dunphy/kryptos-k4),
  [pinned README](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/README.md)
  at commit `3ce19e3ae164a54af8743222ad3de5f6a93f6faf`.

Relevant source files and committed logs were read through the authenticated
GitHub connector. The live Barney page could not be retrieved by the web reader;
the pinned HTML supplies the reviewed map. No third-party imports, dependencies,
compiled kernels, scripts or downloaded code were executed. The only new local
calculations were direct bookkeeping over our unchanged 24 known positions:
eligible lag ranges and fingerprint counts/distances. These do not reproduce the
projects' searches, stochastic tests or claimed validation workloads.

Treat both projects as experiment inventories. A map tile or README heading
saying a family is ruled out cannot substitute for a declared model, exact
bounds, implementation, full artifacts and independently reproduced controls.

## Barney: effective coverage and unresolved survivors

### Forward autokey dictionary checks

[scripts/autokey_dict.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/autokey_dict.py)
nominally loops over lags 1–96, but skips a lag entirely when fewer than 12
known positions have an available preceding ciphertext position. Plaintext
feedback additionally requires at least eight known predecessor pairs. Direct
bookkeeping using our canonical crib positions confirms effective forward
ciphertext-autokey lags **1–33** and plaintext-autokey lags **1–8** for this file.
The second check is nested after the first skip. This is not coverage of every
lag through 96, and it does not describe separate backward/near-miss scripts.

The file compares implied key values on checkable cribs using its supplied
dictionary alphabets/role choices. It is not an independent full-message
recovery/regeneration audit. Its reported zero fits remain third-party results
for the actual checked domain; they cannot close general autokey or masking.

### Gromark/chain addition

[scripts/gromark_sweep.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/gromark_sweep.py)
uses bases 3–26 and primer lengths 2–8 but includes a configuration only when
`base ** primer_length <= 20,000,000`. Therefore the rectangular range label
does not mean every base/length pair was searched. Its
[committed log](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/results/gromark_sweep.out)
reports **804,684** two-term survivors. These counts are read from the source,
not locally rerun.

[scripts/chain3.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/chain3.py)
uses its own **12,000,000** cap on base-to-primer-length combinations. Its
[log](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/results/chain3.out)
reports **790,052** three-term survivors. A source-code comment about a planted
check is not evidence that an independent complete recovery audit was performed.

The imported [scripts/gromark2.py](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/gromark2.py)
constructs crib-graph cycle checks and within-component same-side distinctness
checks. The sweep logs count recurrence/primer streams passing those filters.
They do not present independently verified complete pairs of permutation
alphabets, a full plaintext or exact full-message reconstruction for each survivor.
Cross-component alphabet assignments and completion must be checked explicitly
before upgrading a survivor to a complete model.

The width-21 ranking asks how many observed repeated ciphertext pairs also have
identical key pairs. Both logs report a best explanation count of three. That
heuristic is not a necessary condition for a valid cipher: repeated ciphertext
can arise from different plaintext/key combinations. It cannot conclusively
reject the retained streams. Conversely, passing the crib filter is not evidence
of English plaintext or success. A fully constrained, bounded Gromark completion
check remains a possible lead, not a newly executed experiment or solved alphabet.

### The disputed 2019 premise and local algebraic overlap

The [2019 meeting article/comment thread](https://scienceblogs.de/klausis-krypto-kolumne/2019/03/15/cnn-documentary-about-kryptos-a-making-of-report-with-many-photographs/)
is relevant testimony, not a mathematical premise established by the experiment
map. The supplied prior-art review identifies a conflict between **Bob B's comment 4** and **Elonka's account**
about the one-to-one/no-transposition inference. Both accounts must remain
attached to that disputed premise; do not promote one recollection to a settled
Sanborn constraint. Direct article retrieval repeatedly failed with HTTP
502 in this coding review, so the conflict is retained as supplied testimony,
not newly checked wording or a quotation. No transcript or recording was verified.

Literal confirmed crib alignment constrains those positions. It does not alone
establish that every other position lacks nulls or that an unspecified layered
pipeline cannot include reordering or length changes. Such models would need
explicit framing and alignment; our fixed 97-letter baseline is unchanged.

The useful repeated-phase bijection collision observation is already subsumed
by [STRUCT-001](../research/STRUCTURAL-FINDINGS.md): equality must hold in both
directions at equal phases. In particular one-based positions 25/67 are V/V from
T/L, with separation 42. Their selected periodic collision exclusions are not a
new local result. This does not subsume every other model in their inventory.
The [shared-reset proof](../research/CLOCK-RESET-PROOF.md) also remains narrowly
scoped to identical restarted content-independent positionwise bijections.

### Leads that require an exact model

- [Interrupted/event-driven keys](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_interrupt.py):
  distinguish reset-at/reset-after, advance/pause, trigger sets, key periods,
  unknown offsets and word/line boundaries. Their finite source model is useful
  prior art, not proof about every interruption rule. Our identical-boundary
  contradiction must not be extended to content-dependent stateful feedback.
- Fully constrained Gromark: specify recurrence/base/primer domain, complete
  bijective alphabet assignments, exact inverse and full regeneration before
  interpreting retained crib-filter streams.
- [Wheatstone 27/26](https://github.com/barneyjm/kryptos-k4/blob/2db2722cc3f18c52d4d8369d7adc5a1db7e859d7/scripts/fe_wheatstone.py):
  the code models a 27-cell outer ring with a blank, a 26-letter inner ring,
  forward steps 1–27 and an offset between crib blocks. The tested outer-ring
  inventory and motion convention define its scope. No local search or blanket
  rejection of every Wheatstone-like mechanism follows from this review.

Shuffle-baseline language scores are diagnostics under their chosen corpora,
scorers, budgets and shuffles. Similar scores neither prove cryptographic
impossibility nor show that an unsearched full model cannot work.

## Scott: fingerprint observation versus hard constraint

The pinned README's blanket historical-family elimination and unrecoverable
personal-mask theory are author claims, not adopted conclusions here. Finite
search bounds and null calibration do not justify those universal assertions.

Direct local counting of the 24 confirmed pairs verifies the observation:
**9 of 10** positions whose plaintext belongs to `KRYPTOS` have A–Z circular
distance at most two from their ciphertext. The distinct represented plaintext
letters are **K, O, R, S, T**; there are no P or Y observations. The forward
exception is one-based position **72: O→F**, circular distance 9.

The ten member positions are 24, 25, 27, 28, 29, 33, 34, 66, 72 and 74. This is
a small, post-hoc selected pattern with repeated letters, not seven independently
validated letter-specific rules. The chosen letter set, distance threshold and
other explored features require their own selection-aware evaluation before a
significance claim can be transferred. We did not repeat a stochastic null test.

[run_fingerprint_decode.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_fingerprint_decode.py)
describes a biconditional: plaintext membership in KRYPTOS iff circular distance
is at most two. Direct counting shows **three known-crib exceptions**:

| One-based position | Plain → cipher | Membership | Circular distance |
| --- | --- | --- | --- |
| 22 | E → F | outside KRYPTOS | 1 |
| 31 | E → G | outside KRYPTOS | 2 |
| 72 | O → F | inside KRYPTOS | 9 |

Its `allowed` routine fixes supplied crib letters before applying the restriction
at other positions. Therefore it exempts these known counterexamples while
restricting unknown letters; it does not validate a universal biconditional.
Annealed text under that imposed rule and its finite shuffled baselines cannot
turn it into a hard admissibility condition for a real K4 candidate.

[candidate_check.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/candidate_check.py)
skips known crib positions when scoring the fingerprint on a candidate. Its
suggestion that the remaining text should fit at approximately 90% or higher is
an unproved extrapolation. Its binomial-like calculation uses a fixed chance
model; it does not correct for choosing the pattern, a candidate-dependent
membership denominator or fitting candidates with the same rule. Keep such
scores descriptive and optional; do not reject candidates on this fingerprint.

### The reported corrected p-value is for a different family

[run_signal.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_signal.py)
defines **15 statistics**: eight modular-window counts, six optimized two-offset
partitions and one three-bin statistic. It uses 20,000 full-ciphertext
permutations and calibrates a minimum p-value within that family. The
[committed signal log](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/results/signal.log)
reports corrected **p = 0.0029**. This is a third-party reported calibration for
that particular family, not a locally reproduced probability for the 9/10
KRYPTOS-membership/±2 fingerprint. It is neither the probability a cipher theory
is true nor a complete correction for every analysis explored in the repository.

## Scott exact-overlap matrix

The supplied independent review covered **41 grouped branches**; only selected
scripts were statically audited in that review and in this coding pass. This is
not an execution audit of all 41 branches. The following classifications retire
exact duplicate configurations, not entire cipher families. All Scott links in
this section refer to commit `3ce19e3ae164a54af8743222ad3de5f6a93f6faf`.

| Local scope | Pinned Scott evidence | Exact overlap and limit |
| --- | --- | --- |
| ROUTE-001 nonidentity routes, periods 1–16 | [run_e1.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_e1.py), [perms.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/perms.py), [cribfilter.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/cribfilter.py) | E1 covers the corresponding sufficiently constrained configurations at model-definition level. Its script passes minimum constraint count 5, while NOTES reports 4. Low-constraint configurations filtered out by that threshold are not exclusions. Preserve our complete identity-period 1–96 ledger and vacuous-fit classification. |
| Dictionary keywords with row restarts | [run_keyrow_all_mp.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_keyrow_all_mp.py), [run_keyrow_t3.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_keyrow_t3.py), [run_alphapairs.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_alphapairs.py) | Uses keyword phase zero, continuously or restarted at copper rows; there is no all-phase loop in the parallel script. Wordlist comes from unbundled, unhashed `/usr/share/dict/words`; the exact dictionary cannot be reconstructed from that path alone. No all-keyword/all-phase exclusion. |
| RUNKEY-001 complete literal-window ledger | [run_e4.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_e4.py) | Its loop scans `range(len(S)-97)`, omitting the final valid 97-letter window (and every window of an exactly 97-letter source). This run omits standalone K3 ciphertext and our full K1+K2+K3 ciphertext concatenation. It does include K1+K2 ciphertext, so do not describe all concatenated CT as absent. Our complete nonwrapping source/window ledger remains distinct. |
| TRIFID-001, 144 cases | [run_trifid.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_trifid.py), [run_trifid2.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_trifid2.py) | Source covers our 72 standard-decrypt configurations at model-definition level, allowing the equivalent label for the 27th filler symbol. It does not replace the opposite transform direction. No retained named Trifid completion log was found in the pinned tree; NOTES' reported outcome is not independently rerun evidence. |
| MASK-AUTO-001, 12 cases | [run_p2.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/run_p2.py) | P2's recurrence constraints cover our six ciphertext-autokey cases and two KRYPTOS-primer plaintext-autokey cases. Its plaintext lag limit is 7, so it does not cover plaintext primers ABSCISSA (lag 8) or PALIMPSEST (lag 10). This is overlap of necessary constraints; our full outputs, regeneration and immutable receipts remain separately retained. |
| MASK-FM-001, two fixed maps | [historic-method survey](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/data/historic_methods_survey.md) | Survey remarks about Fractionated Morse and length/alignment do not reproduce or subsume our two exact full-stream parses, separator failures or controls. No general Morse-family rejection follows. |
| WORD-SCRAMBLE-001 | [local findings](../research/WORD-SCRAMBLING-FINDINGS.md) compared with the supplied Scott inventory review | Our 24 endpoint/count checks remain distinct. No source-level evidence supplied for an exact duplicate of these frozen combinations. |
| CLOCK-BOUNDARY-REG-001 | [local proof](../research/CLOCK-RESET-PROOF.md), compared with fixed-alphabet reset models | The identical-reset injectivity proof applies to arbitrary shared positionwise bijections, hence is stronger than a finite fixed-alphabet reset scan. Preserve its assumptions: unchanged alignment, identical restarted sequence, no content-dependent feedback. |
| LANG-001 and dated clock evidence | [alternate-alphabet inventory in NOTES](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/NOTES.md), [local language findings](../research/LANGUAGE-FINDINGS.md), [dated photographs](historical-clock-inscriptions.md) | Alphabet relabelings do not implement our sourced language codecs, exact inverses or historical inscription review. They do not resolve the clock's true-ENE orientation or the full 1989 panel. |

### Power, missing runs and incomplete artifacts

The [pinned NOTES](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/NOTES.md)
reports that free-alphabet annealing loses useful recovery power at period 6 and
above. It explicitly treats those larger periods as untestable by that method,
not eliminated; it also says free-alphabet autokey was not run on K4 after poor
synthetic power. [synth.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/synth.py)
and [synth2.py](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/synth2.py)
provide the selected power-test definitions reviewed here. We did not run them
or independently reproduce their reported accuracies.

The supplied 41-branch review retains full M-209, M-138, real SOE tables and
width-at-most-5 row-strip permutations as **untested in the relevant survey**,
not proposed successes. The
[historical-method survey](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/data/historic_methods_survey.md)
and NOTES distinguish restricted machine subspaces and random unknown-table
proxies from actual complete machines/tables. The row-strip classification is
attributed to the supplied overlap review, not a claim that every permutation
script in the repository was audited here.

Some exact-DFS claims lack retained completion evidence. In the pinned tree,
[results/anneal/q4dfs_real.log](https://github.com/scott-dunphy/kryptos-k4/blob/3ce19e3ae164a54af8743222ad3de5f6a93f6faf/results/anneal/q4dfs_real.log)
is **zero bytes**. A code file, empty log or short startup log is not evidence of
a completed exhaustive run. This observation does not assert that every DFS log
is empty or that no work was performed; it limits what can be independently
verified from retained artifacts.

## Retained boundaries

No mass experiment, code execution from either repository, new corpus, paid
submission, arbitrary keyword expansion or hard fingerprint filter was added.
The Mac lock blocked this executor's earlier visibility action. Final GitHub
metadata verification during this review subsequently reported the repository
public; this documentation update did not change sharing settings. The supplied overlap review
is preserved above with static-review versus third-party-report distinctions.

## Reproduce the local bookkeeping only

From this repository's root, using Python standard library and the unchanged
baseline. This does not import either external project or reproduce its searches:

```sh
python3 - <<'PY'
import json
from pathlib import Path
d = json.loads(Path('data/k4.json').read_text())
pairs = [(i, p, d['ciphertext'][i]) for c in d['cribs']
         for i, p in enumerate(c['plaintext'], c['start'] - 1)]
positions = {i for i, _, _ in pairs}
ct = [lag for lag in range(1, 97)
      if sum(i - lag >= 0 for i in positions) >= 12]
pt = [lag for lag in ct if sum(i - lag in positions for i in positions) >= 8]
records = [(i + 1, p, c, min((ord(c)-ord(p)) % 26,
                           (ord(p)-ord(c)) % 26)) for i, p, c in pairs]
members = [r for r in records if r[1] in 'KRYPTOS']
exceptions = [r for r in records if (r[1] in 'KRYPTOS') != (r[3] <= 2)]
print('effective forward lags:', ct, pt)
print('member fits/total:', sum(r[3] <= 2 for r in members), len(members))
print('represented letters:', sorted({r[1] for r in members}))
print('biconditional exceptions:', exceptions)
PY
```

## Local follow-up: direct autokey constraint gap

[The exact local audit](../research/AUTOKEY-CONSTRAINT-FINDINGS.md) subsequently
classifies all forward same-alphabet PT/CT-feedback lags 1–96 under three equations
with arbitrary independent primers, including zero-check cases. Its full affine
PT chains connect cribs across unknown intervening positions; it therefore does
not inherit the selected prior scripts' immediate-predecessor thresholds. It
finds 732 contradictions and 420 vacuous underdetermined cases, not a general
autokey exclusion. Third-party source was not executed; the fixed primer
experiments and their earlier provenance remain preserved.
