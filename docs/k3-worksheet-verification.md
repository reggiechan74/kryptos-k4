# K3 paper-route verification

Checked 18 October 2026. This report concerns K3 provenance and exact reproducibility; it establishes no new K4 key or mechanism.

Import note: this is the supplied independent worksheet-provenance review. Visual inspections and source-access outcomes below belong to that review. The local coding executor independently checks the coordinate formula and fixed fixture, without claiming to repeat the image/video inspection.

## Result

The two-clockwise-rotation reconstruction exactly regenerates all 336 K3 ciphertext letters and has an exact inverse. It is stronger evidence for a practical paper workflow than merely observing that some transposition gives English. However, the commonly linked first-sheet image is partly reconstructed, not a complete photograph of the original worksheet. Describe the procedure as a **worksheet-supported reconstruction**, not as fully observed historical execution.

## Provenance and limits

1. [The Kryptos Project’s K3 method page](https://www.thekryptosproject.com/tjp/observations/k3_method.php) describes an initial 42-wide × 8-high plaintext sheet, clockwise rotation, copying into 14-wide × 24-high, and another clockwise rotation. Its page modification label is April 2014. This is a commentator’s reconstruction, not Sanborn’s first-person procedural account.
2. The [first-sheet image](https://www.thekryptosproject.com/tjp/observations/images/two.jpg), visually inspected, explicitly labels the rightmost five columns “UNVERIFIED SECTION (NOT SHOWN IN FOOTAGE).” It also labels alternative tentative fold locations. Its typography and annotations are a reconstructed diagram. The [chart index](https://www.thekryptosproject.com/kryptos/charts/all.php) separately labels the relevant plaintext-sheet and combined-cipher-sheet images as recreations from HD NOVA footage.
3. The [second-sheet image](https://www.thekryptosproject.com/kryptos/charts/images/2_k3.jpg), visually inspected, is a low-resolution photographed handwritten chart marked with a circled 2. The archive index attributes it to Sanborn’s Big Techday 6 presentation. The [larger annotated version](https://www.thekryptosproject.com/tjp/observations/images/twoc.png) shows a 24-row × 14-column grid and original bottom-left arrow, plus editorial enlargement/arrows. Its readable rows agree with the computed intermediate, including the first row ILNTAYESTATHCW and bottom row EDNRWEQWFIGEAD. Resolution does not justify claiming a separate high-confidence transcription of every handwritten cell.
4. Original talk links at Techcast and the later media.techcast.cloud location currently return 404. The source chain therefore remains a third-party preserved presentation image. The talk/slide attribution was not independently reconfirmed from a functioning original video during this check.
5. [Preserved NOVA stills](https://www.thekryptosproject.com/media/nova/index.php), especially images 18–22, visibly show Sanborn handling/folding the sheets, but do not establish an exact operational fold coordinate or that folds encode anything. Image 22 contains a partly occluded view of the plaintext sheet.
6. [RR Auction’s primary catalogue](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/) explicitly withholds photographs of items 1–7, including item 4, the original K1–K3 coding charts. It also states that the auction house had not independently examined the archive. Public auction pictures therefore do not close the K3 original-sheet gap.
7. [Current archive owner Paradigm’s public gallery](https://www.paradigm.xyz/kryptos/archive) lists the coding charts among its holdings, but its displayed public gallery has no identified K3 chart. Page captions alone are not transcriptions. No private or restricted archive was accessed.

## Exact reproducible route

Use the accepted 336-letter plaintext, retaining DESPARATLY and the terminal Q. The sculpture separator ? is excluded from this permutation.

All dimensions below are **rows × columns**; all indices are zero-based.

- Write plaintext P row-major into A of shape 8 × 42: A[r,c] = P[42r+c].
- Rotate A clockwise and read row-major. Intermediate index j = 8c + 7 − r.
- Reshape the resulting stream row-major into B of shape 24 × 14: u = floor(j/14), v = j mod 14.
- Rotate B clockwise and read row-major. Output index k = 24v + 23 − u.
- Thus C[k] = P[i], where i = 42r+c and k = 24((8c+7−r) mod 14)+23−floor((8c+7−r)/14).

Inverse for ciphertext index k: v = floor(k/24); u = 23−(k mod 24); j = 14u+v; c = floor(j/8); r = 7−(j mod 8); i = 42r+c. Then P[i] = C[k].

Anchor mappings: P[0] → C[191]; P[294] → C[23]; P[335] → C[144]. Thus the terminal plaintext Q lands at ciphertext index 144, not at the ciphertext’s end. This is an indexing observation, not an interpretation of the neighboring separator.

The full ciphertext fixture was checked against [Elonka Dunin’s sculpture transcript](https://www.elonka.com/kryptos/transcript.html). Exact 336/336 match and exact inverse pass. The independent review names companion artifacts `verify_route.py` and `route_result.json`, containing its coordinate implementation, complete grids, permutations, inputs, and checksums. Those files were not included with the supplied receipt. Repository checks separately validate the complete fixture, coordinate formula, inverse, and anchors in [test_audit_hardening.py](../tests/test_audit_hardening.py) and [test_controls.py](../tests/test_controls.py).

Plaintext SHA-256: ea07f4ff5bc4ffcf6cd2a3e33263d25543ea81d1089ed9a413021d75db46aafc
Ciphertext SHA-256: db8807dfc8354a42dc2f52aed3f0b54ac938873372c6b504b4c8d69fdfc85c35

## Gillogly: algorithm versus historical procedure

Gillogly’s [16 June 1999 email, preserved in a mirrored mailing-list thread](https://www.elonka.com/kryptos/mirrors/cypherpunks/1999/0930.html), describes K3 with the short label “three columnar transpositions.” It does not specify the three keys, dimensions, or implementation in that message. Therefore this source cannot support a claim that we reproduced his precise three-stage algorithm.

His [2013 first-person response, published by Kryptos–Beyond K4](https://kryptosfan.wordpress.com/kryptos-foia/kryptos-fan-letter-to-solvers/jim-gilloglys-response/) explains that he recovered K3 without seeing the method used to encrypt it. This reconciles the apparent conflict: a working cryptanalytic decomposition and a reconstruction of the artist’s physical operations need not contain the same number of steps. Multiple compositions can realize the same permutation. Successful decryption alone does not identify the artist’s procedure.

## Recommendation for bounded K4 research

Keep the validated two-stage rotation/reshape route as a K3 control. Track two different claims: computational equivalence, which is fully verified here; and historical choreography, which remains partly reconstructed. Deduplicate future route candidates by their full permutation, rather than count equivalent descriptions as separate discoveries.

The supported transferable primitive is: copy a fixed sequence onto a rectangle, rotate it, reserialize, and reshape onto another rectangle. This gives a bounded operation grammar. It does not license transferring K3’s dimensions to the prime-length 97-character K4, inventing null positions, selecting fold coordinates from a blurry still, treating sleeve labels as a mask, or claiming K4 was created when it first appears in a displayed combined chart. Any new dimension, padding rule, route origin, or K4 mask needs a separately stated motivation and a full inverse.
