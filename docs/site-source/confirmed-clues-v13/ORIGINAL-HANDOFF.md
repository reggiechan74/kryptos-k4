# Confirmed K4 clue display · focused Site update

Base/source integration point:5b266eb0fc6744c5eda45e30ad089731be97cb35 (public Siteversion12).

Only confirmed positions:22–25 EAST,26–34 NORTHEAST,64–69 BERLIN,70–74 CLOCK. Mask length97,known24,unknown73. All unknowns are neutral middle dots. No experimental candidate/IPA text is included. First O is position1. A shared31-column grid places each clue character directly below its ciphertext character, retaining the existing first27paddingcells and97indexedcipherbuttons.

Changed runtime files (both candidate source and deployed dist):app.mjs,index.html,style.css,newk4-clues.mjs. Also dist/RELEASE_MANIFEST.json; tests/k4-clues.test.mjs; qa/k4-clue-alignment.html; this handoff file. Frozen dist/validation snapshots are unchanged. No changes to /work/kryptos-k4 or the separate researchbranch.

Verification:76tests passed via node --test tests/*.test.mjs. New tests cover exactmask/all24knownone-basedletters/all73unknowns/canonicalciphersegments/first27padding/sharedgridcoordinates/accessiblelabels/selection. Actual nativeArc browser on thisMac executor loaded the complete Site in390px and1280px same-originframes:97pairs,24known,73unknown; maximum horizontal/widthdifference0CSSpx;0cluesaboveitsciphercell;no pagewideoverflow;K4#22selectionworks atbothwidths. A representative grid screenshot was inspected. The final full-Site screenshot action reported noWindowsAvailable after these render checks completed; no further browser actions or lock bypass attempted. These checks do not claim realphone/touchtesting.

Run tests with the installed Node runtime. Serve repository root and open /qa/k4-clue-alignment.html for browser alignment checks. Runtime has no new dependencies.
