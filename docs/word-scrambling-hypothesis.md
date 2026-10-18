# User-proposed word-interior scrambling

The user proposed keeping each word's first/last letters and scrambling its
interior. This is H-WORD-SCRAMBLE, a hypothesis rather than an established
Sanborn/Scheidt method. It follows the completed language and masking pilots.

[Matt Davis's Cambridge/MRC discussion](https://www.mrc-cbu.cam.ac.uk/people/matt-davis/cmabridge/),
read directly during this milestone, explains that readability depends on the
word/context and type of scrambling; endpoint preservation alone is insufficient.
SALT/SLAT illustrates ambiguity. A permutation is exactly invertible when its
schedule is retained; discarding the schedule does not identify an original word.

Pure scrambling preserves letter counts and remains subject to the existing
E-count contradiction. Pre-scrambling followed by a letter-changing cipher is a
different model. The [fixed24case specification](../research/specifications/WORD-SCRAMBLE-001.json)
uses only the12already tested autokey settings, with two explicit crib-word
segmentation assumptions. Neither segmentation is claimed as a known fact.
No key, boundary, alphabet, or permutation is fitted to make a candidate work.

K1 IQLUSION and K2 UNDERGRUUND are substitutions relative to conventional
spellings. DESPARATLY versus DESPERATELY changes counts/length. These are not
simple interior permutations. The [NSA summary reference](https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cia-kryptos-sculpture/KRYPTOS_Summary.pdf)
was supplied for historical context; its web fetch failed in this pass. This
classification is independently checkable from the preserved known-plaintext
fixtures; no claim is made to have newly read that inaccessible PDF. None of
these spelling anomalies proves a masking layer.

Endpoint/interior-count compatibility is only a necessary condition on the
known spans. A survivor would still require the full English message, exact
word boundaries and a reproducible inverse schedule, then complete regeneration
of all ciphertext. The test does not enumerate factorial permutations or infer
word boundaries in the unknown part of K4.
