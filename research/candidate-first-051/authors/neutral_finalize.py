import json, re
from pathlib import Path
root=Path('/workspace/shared/candidate-first-051/authors')
normalize=lambda s: re.sub('[^A-Z]','',s.upper())
target=[21,29,23]
updates={
'N06':(['This old road runs almost','with a gentle curve just beyond the','and a tram stop on the corner.'],'Replace compressed map-report syntax with a direct road description.'),
'N09':(['Please take this path due','and meet us on the broad steps by the','at noon for a short city tour.'],'Remove the implication that a clock has an entrance; use a nearby meeting place.'),
'N12':(['Our local guide led us due','on a scenic walk that ended near the','avoiding the busy main road.'],'Replace choosing a compass direction with a natural guided walk and keep past tense consistent.'),
}
with (root/'neutral_drafts.jsonl').open('a') as f:
 for cid,(spans,note) in updates.items():
  lengths=list(map(lambda s:len(normalize(s)),spans))
  record={'id':cid,'revision':2,'spans':spans,'span_lengths':lengths,'feedback':{'target':target,'deltas':[a-b for a,b in zip(lengths,target)]},'revision_note':note}
  f.write(json.dumps(record)+'\n')
records=[json.loads(x) for x in (root/'neutral_drafts.jsonl').read_text().splitlines()]
history={}
for item in records:
 history.setdefault(item['id'],[]).append(item)
final_prose={
'N01':'From our station, walk due east-north-east until you see the square beside the Berlin Clock, then pause awhile for lunch.',
'N02':'The morning breeze blows east-north-east as we sit eating fresh bagels by the Berlin Clock before our early train ride.',
'N03':'Our tiny hotel rooms face east-north-east and offer a lovely view towards the Berlin Clock across the wide town square.',
'N04':'We chose a route going due east-north-east to avoid the noisy streets near the Berlin Clock and enjoy a peaceful stroll.',
'N05':'Walk from that church due east-north-east, then look for the little cafe by the Berlin Clock, where our friends drink tea.',
'N06':'This old road runs almost east-north-east, with a gentle curve just beyond the Berlin Clock and a tram stop on the corner.',
'N07':'I saw storm clouds moving east-north-east while we all waited on a bench by the Berlin Clock as the rain began to ease off.',
'N08':'The white kite sailed due east-north-east above the park as we walked past the Berlin Clock on our way back to the hostel.',
'N09':'Please take this path due east-north-east and meet us on the broad steps by the Berlin Clock at noon for a short city tour.',
'N10':'That narrow lane runs due east-north-east from the shops straight toward the Berlin Clock, with trees shading the road.',
'N11':'The tram took us straight east-north-east past the gardens and right up to the Berlin Clock in time to take a group photo.',
'N12':'Our local guide led us due east-north-east on a scenic walk that ended near the Berlin Clock, avoiding the busy main road.',
'N13':'Seven pigeons headed due east-north-east above the old square, while near the Berlin Clock a child counted every light.',
'N14':'A chilly breeze came from east-north-east while I drew all the houses near the Berlin Clock and waited for my sister Amy.',
'N15':'This river path leads due east-north-east and crosses a small bridge near the Berlin Clock before it ends beside a pond.',
'N16':'We steered both bikes due east-north-east at that cafe and soon arrived at the Berlin Clock, where I checked my new watch.',
}
themes={
'N01':'Walking directions and lunch', 'N02':'Breakfast, weather, and train travel', 'N03':'Hotel view', 'N04':'Quiet walking route', 'N05':'Meeting friends at a cafe', 'N06':'Road layout and tram stop', 'N07':'Rain and cloud movement', 'N08':'Kite observation during a walk', 'N09':'Meeting for a city tour', 'N10':'Shaded lane', 'N11':'Tram journey and group photo', 'N12':'Guided walk', 'N13':'Bird observation and a child counting lights', 'N14':'Sketching while awaiting a sister', 'N15':'Riverside walking path', 'N16':'Cycling and checking a watch'
}
# Complete intermediate prose variants considered during individual revision.
# These are retained even though none influenced any cryptographic score.
alternates={
'N02':[('The morning breeze blows east-north-east as we sit eating fresh loaves by the Berlin Clock before our early train ride.','Replaced fresh loaves with fresh bagels for a more natural individual breakfast.')],
'N08':[('The high wooded hills lie east-north-east of the old park as we walked past the Berlin Clock on our way back to that hotel.','Rejected awkward mixed temporal framing and hill geography; rewrote as a kite observation.'),('The high wooded hills lay east-north-east of the old park as we walked past the Berlin Clock on our way back to that hotel.','Retained grammatical past tense but replaced the whole hill observation for credibility.'),('The white kite sailed due east-north-east over that park as we walked past the Berlin Clock on our way back to that hotel.','Replaced repeated demonstratives with above the park and the hostel.')],
'N14':[('A chilly breeze came from east-north-east while I drew all the houses near the Berlin Clock as I waited for my sister Sue.','Replaced nested while/as framing with a coordinated verb and sister Amy.')],
}

def validation(prose):
 n=normalize(prose)
 return {'length':len(n),'length_is_97':len(n)==97,'crib_22_34':n[21:34], 'crib_64_74':n[63:74], 'crib_positions_correct':n[21:34]=='EASTNORTHEAST' and n[63:74]=='BERLINCLOCK'}

out=[]
for cid,prose in final_prose.items():
 h=[]
 for r in history[cid]:
  p=r['spans'][0]+' east-north-east '+r['spans'][1]+' Berlin Clock '+r['spans'][2]
  h.append({'stage':f"saved_draft_{r['revision']}",'spaced_prose':p,'normalized':normalize(p),'unconstrained_spans':r['spans'],'span_lengths':r['span_lengths'],'validation':validation(p),'feedback':r['feedback'],'revision_note':r.get('revision_note','Initial individually composed full-message draft, before length correction.')})
 for p,note in alternates.get(cid,[]):
  h.append({'stage':'intermediate_prose_alternative','spaced_prose':p,'normalized':normalize(p),'validation':validation(p),'feedback':note})
 h.append({'stage':'final_punctuation_and_prose_review','spaced_prose':prose,'normalized':normalize(prose),'validation':validation(prose),'feedback':'Accepted as a coherent ordinary message. Fictional setting details are not verified geography; no cryptographic information was used.'})
 n=normalize(prose)
 assert len(n)==97,(cid,len(n))
 assert n[21:34]=='EASTNORTHEAST',(cid,n[21:34])
 assert n[63:74]=='BERLINCLOCK',(cid,n[63:74])
 assert n==normalize(history[cid][-1]['spans'][0]+'EASTNORTHEAST'+history[cid][-1]['spans'][1]+'BERLINCLOCK'+history[cid][-1]['spans'][2]),cid
 out.append({'id':cid,'spaced_prose':prose,'normalized':n,'revision_history':h,'theme':themes[cid],'authoring_method':'Blind candidate-first individual full-message creative composition, followed only by A-Z normalization, length/position validation, and prose revision. No phrase-bank Cartesian product, ciphertext inspection, key derivation, score optimization, external model API, or other-author candidate inspection. Distinctness is not a claim of statistical independence.'})
assert len(out)==16
assert len({x['normalized'] for x in out})==16
(root/'neutral.json').write_text(json.dumps(out,indent=2)+'\n')
report={'file':'neutral.json','count':len(out),'distinct_normalized_count':len({x['normalized'] for x in out}),'all_exact_length_97':all(len(x['normalized'])==97 for x in out),'all_fixed_crib_positions_correct':all(x['normalized'][21:34]=='EASTNORTHEAST' and x['normalized'][63:74]=='BERLINCLOCK' for x in out),'target_unconstrained_span_lengths':[21,29,23],'validation_scope':'Plaintext normalization, exact letter counts, fixed crib positions, and duplicate detection only. No cryptographic quality tests.','prose_review':'All 16 are complete grammatical ordinary messages. The fixed compass phrase and clock landmark make directional travel framing recur. Deictic words such as that and invented local details are plausible narrative devices, not independently verified geography. No statistical independence claim.','provenance':'Initial drafts, length-feedback records, all saved revisions, and complete intermediate prose alternatives are retained in each revision_history and in the dedicated draft log where applicable. Internal word/phrase brainstorming is not a separate full-message candidate.','per_message':[{'id':x['id'],**validation(x['spaced_prose'])} for x in out]}
(root/'neutral_validation.json').write_text(json.dumps(report,indent=2)+'\n')
(root/'neutral_validation.txt').write_text('16 / 16 distinct complete neutral messages validated.\nEach has exactly 97 normalized uppercase A-Z letters.\nEASTNORTHEAST occupies 1-based positions 22-34.\nBERLINCLOCK occupies 1-based positions 64-74.\nUnconstrained spans are 21, 29, and 23 letters.\nValidation used no ciphertext, keys, or cryptographic scores.\nAll 16 received a prose review; local details are fictional and directional framing recurs.\nDistinct messages do not establish statistical independence.\n')
print(json.dumps(report,indent=2))
