# Narrow respelling feasibility and translation boundary

PHONETIC-SUBSET-001 was registered at
`35477f6c045d4cd831f9c72e60790042e93f6ba4`, before implementation commit
`f3b9792ae11afc81a360de12d78c63777d261bc9` and execution. This is a small
synthetic-rule check, not a universal German-accent model or historical claim.

W→V, word-final D→T, and word-final G→K leave EAST, NORTHEAST, BERLIN and
CLOCK unchanged. The known spans contain none of the source letters affected
by this subset. The same length-preserving aligned English cribs therefore
remain necessary. Independently comparing the same 12 frozen autokey outputs
finds **zero rescued cases**, with identical 24-character match masks. No new
key, cipher output, word-boundary choice, or pronunciation variant was searched.

Positive controls WORD→VORT, WEDDING→VEDDINK and DOG→DOK pass. WET/VET shows
that the synthetic map itself may lose information. The code explicitly leaves
TH and I rules unimplemented. This limited result cannot exclude other
respelling/cipher compositions.

[Run manifest](../results/phonetic-subset-runs/20261018T113329Z-3d5c35d85cbb4e2a9b9864410c053c54/manifest.json)
· [complete 12-case comparison](../results/phonetic-subset-runs/20261018T113329Z-3d5c35d85cbb4e2a9b9864410c053c54/PHONETIC-SUBSET-001.json)
· [source-interpretation caveat](../docs/linguistic-feasibility-boundary.md).

TH contractions and short-I expansion require a fixed pronunciation dictionary,
word boundaries, and cumulative input/output alignment. Moving Sanborn's English
crib indices to a post-linguistic-reconstruction stage is an additional model
assumption, not a fact established by the directly enciphered-English disclosures.
A wholly German intermediate cannot simply stand in for those aligned English
spans. German translation is distinct from English accent respelling and lacks a
fixed rendering, grammar/codebook, English inverse, and alignment here. No flexible
mapper, translator fitting, German candidate generation, or crib shifting was run.
