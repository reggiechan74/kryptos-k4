# IPA preprocessing pre-fit implementation notes

22 October 2026 UTC. These notes supplement, without changing, the model domain
in `IPA-PREPROCESSING-SPEC.md` committed at 2c40fca.

The parent corrected an independent preliminary summary before this repository's
K4 evaluation: it expects 47 ordinary-anchor contradictions and one additional
shared-length-marker contradiction, rather than 48 ordinary-anchor failures.
The repository implementation does not inherit that classification; it derives
all first-window constraint matrices and independent fixed-anchor conflicts.
The preliminary results were disclosed, so no blind discovery is claimed.

If a fixed ordinary-letter subset is inconsistent, the complete relaxation is
inconsistent too. Such a certificate avoids evaluating every alias assignment.
The full modular solver still checks each structure. Actual trial accounting
will distinguish formal structures, symbolic constraints and actual enumerated
alias assignments; 26^3 possibilities per structure are not falsely reported as
executed trials. A non-anchor failure retains its full modular certificate.

Mapping-independent phase equality/injectivity checks combine both disclosed R2
windows as necessary conditions. They are not used to select periods for the
first-stage arithmetic test: that test evaluates all 48 structures using only
positions 22–34. This prevents accidental second-window information leakage.

The source normalization audit observed the R2 local 13/11 lengths before the
arithmetic protocol was frozen. English clue lengths were publicly known.
Cumulative alignment through unknown phonetic prefixes and the gap is unproved.

A separately supplied Unicode CLDR IPA-to-X-SAMPA serialization contrast will be
retained as a source-normalization control only: its same two normalized windows
have lengths 13 and 12. X-SAMPA retains case and punctuation, so no uppercasing,
A–Z substitution assumption or extra K4 model scan follows from this control.
