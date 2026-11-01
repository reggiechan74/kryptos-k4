# E01 exact local 208-operator gate

1 November 2026. PASS: E01 is a different global encryption function from every exact local study060 description. This is a static initial-emission table comparison, not a cipher-message batch or target test.

Source archive `research/candidate-first-060/study-060-evolving-alphabets.zip` SHA256 `23ac5164362cc0b43a97ad82f3125ea9596e7a223321ac1509528f282a0fb9e9` was read without executing/importing it. Members inspected:
- `study-060/freeze/production.py`: `e46882f7fc47dfb7ccf396df171af9f45502e346d9ef3592015ab410d1d0d4f4`
- `study-060/freeze/reference.py`: `77b6d22d23725e4edb15e0982843cc83b8de428d384aaf9e58240d14844013fe`

Both emit from old S before applying the update. Arm A first emission is S[index_R(p)] and is independent of q0; only afterward swap j/q and advance q by index_R(c)+1. Arm B first emission is S[(index_R(p)+k) mod26]; only afterward reverse prefix length1+index_R(c). R,S each independently AZ or KA=`KRYPTOSABCDEFGHIJLMNQUVWXZ`; each arm has104 descriptions.

E01 starts at Q and L_Q=`LABCDEFGHIJKMNOPQRSTUVWXYZ`, so A→B and L→A. For the four (R,S) choices (AZ,AZ), (AZ,KA), (KA,AZ), (KA,KA):

| R,S | Arm A output on A | Arm B k required by A→B | Arm B output on L at that k |
|---|---|---|---|
| AZ,AZ | A | 1 | M |
| AZ,KA | K | 8 | N |
| KA,AZ | H | 20 | L |
| KA,KA | A | 1 | M |

Thus A alone separates all104 Arm A descriptions. Each Arm B description either differs on A, or its uniquely forced k differs on L. A first-emission mismatch proves global function inequality regardless of later state updates. This is stronger than merely finding a differently named update rule; it does not assert that every finite target trace differs or that all208 descriptions are mutually distinct.

`local208_static_gate.py` independently instantiates only these table equations (no cipher/message routine), yielding208 certificates, zero initial-map matches,103 distinct local initial maps, and minimum common separating input set {A,L}. `LOCAL208-CERTIFICATE.json` records every description, full initial map and first mismatch. The bound is208×26 direct table cells plus a finite minimum-witness search; no target text is an input.

No concrete known-repeat gate remains within these exact208 descriptions. External arbitrary/piecewise selectors and unavailable adaptive implementation details remain bounded source omissions, not disproved coverage or a worldwide novelty claim. E01 survives this available local gate, with no corpus/parameter change. Pilot source review and explicit grant remain required.
