# Native LOC photo inspection, 24 October 2026 — local research

[Findings](../../PHOTO-NATIVE-047-FINDINGS.md), [frozen criteria](../../PHOTO-NATIVE-047-SPEC.md), [coordinate/annotation manifest](annotations.json), [independent exact crop check](../../../results/PHOTO-NATIVE-047-CROP-CHECK.json).

These nine lossless PNG crops come from the same previously known Carol M. Highsmith exposure, not nine independent photographs. No full TIFF is copied into this directory. Native origin is top-left; rectangles are half-open; each crop pixel `(x,y)` maps to `(x+left,y+top)` with no resize. `ground.png` is the initial 800 × 800 ROI; `q1`–`q4` are its four 400 × 400 quadrants. Two screen crops and two additional ground-context crops complete the frozen eight-additional-crop budget. All were visually inspected. The whole-image overview was displayed at 1408 × 1782 from 3384 × 4283; native crops were inspected separately.

The ten `G` boxes identify rough bright-feature regions, not glyph classifications, material points, proposed matches or confidence intervals. No source-aperture identity was certified; there are no fitted rays, image source, residuals or decrypted letters.

Source: [LOC catalogue 2011631531](https://www.loc.gov/pictures/item/2011631531/) and [original TIFF](https://cdn.loc.gov/master/pnp/highsm/13300/13337u.tif). SHA-256 `302fb88dee8db7f484a85d9d7f9bbd39f69de37cbf7bb25ae5a2e35bf8b8cf52`; 43,502,976 bytes; 3384 × 4283 RGB. The existing catalogue advisory says no known publication restrictions; this is not a blanket grant for the depicted artwork. Credit: **Photographs in the Carol M. Highsmith Archive, Library of Congress, Prints and Photographs Division.** These derivatives remain local; no publication was performed. A catalogue refresh returned 403 and was not retried; the already available TIFF matched the independently recorded hash.

Reproduction uses the system `/usr/bin/sips`, not a new software install:

```sh
sips -s format png /tmp/k4-loc-13337u.tif --out /tmp/photo047-original.png
# Example: crop height 800, width 800, top 2800, left 1400.
sips -c 800 800 --cropOffset 2800 1400 /tmp/photo047-original.png --out /tmp/photo047-ground.png
python3 experiments/photo_native_047.py --original-png /tmp/photo047-original.png --output /tmp/photo047-check.json
```

Run the Python command from repository root; use each manifest rectangle's height/width/top/left for the other crops. Sips PNG ancillary bytes may differ across versions; the frozen crop hashes identify this run. The independent verifier compares decoded RGB scanlines with the exact rectangle, so it checks spatial registration without relying on PNG compressed-byte identity. Conversion is lossless PNG with no requested enhancement/resizing; this does not independently calibrate the film scan's radiometry. Original exposure date/time, scene scale and camera calibration remain unknown and were not fitted.
