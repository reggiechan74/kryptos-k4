"""Source QA only: Friedman Legacy printed example, not a K4 experiment.

The question-mark slot is obscured by the physical long hand in figure 112.
It is not used in either direction of this example; no key fitting is done.
"""
import hashlib, json
from pathlib import Path
base=Path('/workspace/shared/item7-historical-sources')
outer='_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
inner='AGMUCIP?EJQXFBKSYNHOVRDLTZ'
plain='REFERENCE'
expected='XZAABGQAM'
assert len(outer)==27 and len(inner)==26
# Printed setup is plaintext G = ciphertext A.
o=outer.index('G'); q=inner.index('A')
trace=[]
for pos,p in enumerate(plain,1):
    nxt=outer.index(p)
    steps=(nxt-o)%len(outer)
    assert steps>0, 'Repeated-plaintext convention not tested here'
    q=(q+steps)%len(inner)
    c=inner[q]
    assert c!='?', 'Vector must not depend on occluded letter'
    trace.append(dict(position=pos,plain=p,steps=steps,inner_index=q,cipher=c))
    o=nxt
cipher=''.join(r['cipher'] for r in trace)
assert cipher==expected
# Decipher by strictly positive next occurrence (same letter requires 26 steps).
o=outer.index('G'); q=inner.index('A'); recovered=''; inv=[]
for pos,c in enumerate(expected,1):
    nq=inner.index(c)
    steps=(nq-q)%26 or 26
    o=(o+steps)%27; q=nq
    recovered+=outer[o]
    inv.append(dict(position=pos,cipher=c,steps=steps,plain=outer[o]))
assert recovered==plain
receipt=dict(
    purpose='Historical source QA; no K4 search',
    source_url='https://www.nsa.gov/portals/75/documents/resources/everyone/digital-media-center/video-audio/historical-audio/friedman-legacy/friedman-legacy-transcript.pdf',
    source_pdf_bytes=(base/'friedman-legacy-2006.pdf').stat().st_size,
    source_pdf_sha256=hashlib.sha256((base/'friedman-legacy-2006.pdf').read_bytes()).hexdigest(),
    printed_pages=dict(encipherment=141,decipherment_and_figure=144),
    physical_pdf_pages_one_based=dict(encipherment=152,decipherment_and_figure=155),
    initial_plaintext_pointer='G',initial_ciphertext_pointer='A',
    outer_clockwise=outer,inner_clockwise_from_A_with_occlusion=inner,
    occluded_index=7,occluded_letter_if_full_permutation='W',
    occluded_letter_used_by_vector=False,
    plaintext=plain,printed_encipherment_string='XZZZBGQAM',
    printed_decipherment_string=expected,computed_ciphertext=cipher,
    source_conflict='Both differing strings visually confirmed in original PDF; p141 is inconsistent with figure112 and procedure; p144 reproduces.',
    forward_trace=trace,inverse_trace=inv,recovered_plaintext=recovered,
    classification='Independent historical worked vector for the fixed-ring Wheatstone model; not Pletts KAT and not a materially different operation')
(base/'friedman-reference-source-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
