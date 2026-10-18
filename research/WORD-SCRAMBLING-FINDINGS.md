# Word-interior scrambling outcome

WORD-SCRAMBLE-001 followed the completed language branch and both fixed masking
pilots. Its specification was committed at
`ef0b3c91e11159886930299878b8636a72252acf` before implementation or execution;
implementation commit was `30fc403b85998731414160fcd1c5cecb5ec42f73`.
The local executor checked the prior specification bytes through GitHub.

Exactly 24 checks were run: the12already frozen complete autokey intermediates Q,
under two fixed segmentation assumptions. Branch A uses EAST/NORTHEAST and
BERLIN/CLOCK; branch B uses compound EASTNORTHEAST and BERLIN/CLOCK. These are
assumptions, not newly established plaintext boundaries. No new key, phase,
alphabet, cipher, boundary, or permutation was fitted.

**Zero of24combinations is compatible. All 24first fail an endpoint check.**
An interior permutation cannot repair an endpoint mismatch. Exact interior
multisets are also recorded. The negative result applies only to the registered
12 autokey settings and two segmentation branches. It does not reject pre-scrambling
with a different cipher, word structure, or explicitly specified model.

The invariant check covers possible interior permutations algebraically; it does
not enumerate factorial alternatives. Even a compatible known span would not
recover the whole97-letter English P, full word boundaries, or a permutation
schedule. Cipher E regeneration of Q is separately verified and must not be
mistaken for complete P→M→E validation.

Controls pass24 planted actual-scanner acceptances,24 endpoint rejections,
24 interior-count rejections, and24full schedule inversions. Synthetic controls
use an explicitly retained reverse-interior schedule; none was fitted to actual
K4. SALT/SLAT demonstrates ambiguity when that schedule is discarded. The run,
including controls, completed in0.069 seconds with no scoring, null simulation,
or key/permutation search.

[Run manifest](../results/word-runs/20261018T112641Z-6df780ad6f254787ad9f539f7a60b740/manifest.json)
· [all 24records](../results/word-runs/20261018T112641Z-6df780ad6f254787ad9f539f7a60b740/WORD-SCRAMBLE-001.json)
· [source/interpretation notes](../docs/word-scrambling-hypothesis.md).
