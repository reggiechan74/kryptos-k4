# Conditional face and lamp pilots — frozen before K4 evaluation

23 October 2026 UTC. Status: specified, awaiting parent protocol review before
actual K4 evaluation. The [completed source synthesis](evidence/2026-10-23-lodestone-compass/KRYPTOS-LODESTONE-COMPASS-EVIDENCE-2026-10-23.md)
and all three dossiers were read locally first. These are our finite models,
not claims about Sanborn's method. No surveyed bearing, date or missing city panel
is required or inferred. Main evidence remains insufficient for faithful magnetic,
shadow/time or dated celestial reconstruction. No Site change is involved.

## FACE-ROW-001

Start with the fixed 97 occupied cells: row 0 columns 27–30, then rows 1–3 columns
0–30. Indices are zero-based and natural order is increasing row then column.
Construct each of the four coordinate operations (r,c), (r,30−c), (3−r,c),
(3−r,30−c); sort the occupied transformed coordinates row-major, skipping holes.
Let T(x)[j]=x[pi(j)]. Also form every inverse permutation. No null padding,
repacking between coordinate operations, glyph substitution or shifted crib index.
A mirrored physical glyph is not automatically a different Latin letter.

Compare entire finite models against ROUTE-001, not just route names. Test only
uncovered models: alphabets AZ and KRYPTOS; C=T(V(P)) or C=V(T(P)); V uses
C=P+K or C=K−P modulo 26 and unrestricted periodic key lengths 1–12. C=P−K is
equivalent under key negation. Canonicalize phase partitions to deduplicate key
renamings and layer-order equivalence. Identity, vertical order, its inverse and
full reversal already match prior routes. Only horizontal reversal within each
actual carved row is new here. The old occupied-cell pilot read columns with
fixed words; it does not cover this unrestricted-key row operation.

There are 768 raw route aliases × alphabet/equation/period/order descriptions,
372 distinct model signatures, 280 already covered and 92 new models. The new
horizontal route has 96 raw descriptions; the two orders coincide at period 1,
removing four. Record every alias and exact prior-result coverage; do not count
skips as new K4 trials. No matrix/heading survey is claimed.

Fit only plaintext positions 22–34. For a plaintext crib at i, let j=pi inverse(i).
Required key is idx(C[j])−idx(P[i]) for addition or idx(C[j])+idx(P[i]) for true
Beaufort, at phase i mod m before T or j mod m after T. Contradictory repeated
phase assignments reject. Under this route those 13 positions visit consecutive
phases in either order, so any compatible training key has every entry fixed
for m≤12. Prove that in controls instead of filling free slots. Then decrypt all
97 positions and check the eleven public Berlin letters without refitting.
Require all 24 letters and exact full regeneration. A compatible crib fit alone
is not a solution; no language score is used.

Controls before evaluation: independent cell-matrix route/inverse; all 97 index
roundtrips; direct coordinate encoder versus route implementation; planted literal
English-crib messages for every new model through the complete new-model selector;
retain aliases/multiple compatible models rather than demanding unique keys.
Use mutation negatives to detect wrong row boundaries or key timing. Budget:
92 actual models, at most 92×92 planted selector decodes; 120 seconds per stage,
64 MiB result output. No new route, period, alphabet, equation or layer afterward.

## LAMP-STREAM-001

This explicitly tests the alternative Mengenlehreuhr, not the artist-confirmed
World Clock. Its support is the user's lamp-pattern hypothesis and a real
pre-1990 display format, not a creator-use attestation. The modern supplier's
[functional description](https://www.berlin-uhr.com/) was read on 23 October
2026: four five-hour fields, four one-hour fields, eleven five-minute fields and
four one-minute fields, plus a blinking round indicator. It describes a modern
table model with additional alarm LEDs; those alarm LEDs are excluded. No modern
firmware convention is asserted for the historical street installation.

For hour H=0..23 and minute M=0..59 define row counts
(a,b,c,d)=(floor(H/5),H mod5,floor(M/5),M mod5). Fields light consecutively from
the left in each row. Thus H=5a+b and M=5c+d, with c as large as 11: this is not
ordinary positional base 5. Binary field order is fixed once: top seconds field
index 0, then the four rows top-to-bottom and left-to-right, indices 1..23.
Let B(H,M,p) be the exact integer sum of on-field weights 2^index, where p∈{0,1}
is the seconds indicator's initial state. Color is not an extra symbol. The
24-bit pattern retains H,M,p uniquely; it does not recover an exact second.
No exact even/odd polarity is needed because both indicator phases are included.

For character index i=0..96, t_i=(t_0+i) mod1440, H_i=floor(t_i/60),
M_i=t_i mod60, and K_i=B(H_i,M_i,p) mod26. One minute per character is our declared
sampling hypothesis. The indicator state is constant under this minute sampling;
it is not reset at a crib. Search all t_0=0..1439 and p=0,1, alphabets AZ/KRYPTOS
and equations C=P+K or C=K−P: exactly 11,520 raw descriptions. No extra scalar
weights, bit order, colors, sampling rate, initial additive offset, word or route.
The binary positional readout is a design assumption, not a geometric fact.

This is a key-generation role. The modulo-26 reduction need not invert the clock
state; encryption/decryption must be exact given a model. Deduplicate identical
97-symbol key streams and full outputs while retaining raw aliases. Audit exact
full-stream overlap with earlier fixed/progressive/periodic domains before any
claim of new coverage; algebraically covered cases may be skipped with receipts.
No inference that previous geometric affine/base-5 proofs cover all lamp models.

Validate all 2,880 valid display states, exact pattern inverse and invalid row
rejection. Explicitly test midnight/hour/five-minute carries and indicator phase;
verify fixed-model message roundtrips. Use 32 literal-crib plants chosen before
actual evaluation: four start minutes {0,58,719,1438}, both indicator states,
both alphabets, both equations. Run the same complete 11,520-model selector per
plant (truth inclusion and compatible-set accounting, not assumed uniqueness),
with an independently coded clock/count oracle and framing/step mutation controls.

Decode every actual model from position 1 through all 97 symbols. Filter the first
13 crib letters, then evaluate the public second eleven without refitting.
No unknown-state gap is guessed: each fixed start phase specifies the whole
stream. Require exact 24-letter agreement and 97-character regeneration. All
compatible models/plaintext classes must be retained. Budget: 11,520 actual
model descriptions, 368,640 complete selector control descriptions, 120 seconds
per stage, 128 MiB results. If a budget is exceeded report unresolved, not zero.

## Shared stopping and evidence rules

Zero exact survivors means only the specified family is rejected; no null
significance claim is made from a partial score. Any survivors trigger a pause
for matched full-selector null calibration before evidential interpretation.
Report fitted versus predicted positions, raw/canonical counts and full-plaintext
multiplicity. Berlin is publicly known and historically used, not untouched data.
No adaptive variants or additional parameters after negatives. Physical frame,
shadow, celestial, historical city extraction, lamp/Greek and Greek phonetic
models remain distinct entries and are not eliminated by these pilots.
