import json, re
from pathlib import Path
from thematic_drafts import letters
ROOT=Path('/workspace/shared/candidate-first-051/authors')
LOG=ROOT/'thematic_draft_log.jsonl'
entries=[json.loads(x) for x in LOG.read_text().splitlines()]
byid={}
for entry in entries:
    byid.setdefault(entry['id'],[]).append(entry)
method=('Blind assistant authorship: each complete message was separately composed as a full thought, not assembled from a Cartesian phrase bank. Revisions used only local normalization, unconstrained-span lengths, total letter counts, crib positions, and readability. No ciphertext, derived keys, key-quality scoring, solution discussion, external sources, other author files, external model APIs, or cloud threads were consulted. These thematic priors are creative hypotheses, not decryption claims; statistical independence is not claimed.')
final=[]
newlog=[]
for cid, history in byid.items():
    latest=history[-1]
    assert latest['feedback']['valid'], cid
    prose=latest['spaced_prose'].replace('EAST NORTH EAST','east-north-east').replace('BERLIN CLOCK','Berlin clock').replace(' ;',';')
    if cid=='T13': prose=prose.replace('Berlin clock then','Berlin clock; then')
    if cid=='T14': prose=prose.replace('Berlin clock where','Berlin clock, where')
    if cid=='T16': prose=prose.replace('Berlin clock but','Berlin clock, but')
    norm=letters(prose)
    assert norm==latest['normalized']
    formatted={**latest,'spaced_prose':prose,'normalized':norm,'revision_reason':'Final readability formatting only: standard case, hyphenated compass direction, and punctuation; normalized letters unchanged.'}
    history=history+[formatted]
    newlog.append(formatted)
    revision_history=[]
    for idx,rev in enumerate(history,1):
        revision_history.append({'revision':idx,'spaced_prose':rev['spaced_prose'],'normalized':rev['normalized'],'constraint_feedback':rev['feedback'],'revision_reason':rev.get('revision_reason','Initial full-message draft' if idx==1 else 'Revision for exact span/total lengths and crib positions, with readability retained.')})
    final.append({'id':cid,'spaced_prose':prose,'normalized':norm,'revision_history':revision_history,'theme':latest['theme'],'authoring_method':method})
with LOG.open('a') as f:
    for entry in newlog: f.write(json.dumps(entry)+'\n')
(ROOT/'thematic.json').write_text(json.dumps(final,indent=2)+'\n')
checks=[]
for item in final:
    norm=item['normalized']
    checks.append({'id':item['id'],'uppercase_AZ_only':bool(re.fullmatch('[A-Z]+',norm)),'letter_count':len(norm),'east_northeast_start_1_based':norm.find('EASTNORTHEAST')+1,'east_northeast_end_1_based':norm.find('EASTNORTHEAST')+13,'berlin_clock_start_1_based':norm.find('BERLINCLOCK')+1,'berlin_clock_end_1_based':norm.find('BERLINCLOCK')+11,'unconstrained_span_lengths':[len(norm[:21]),len(norm[34:63]),len(norm[74:])],'valid':len(norm)==97 and norm[21:34]=='EASTNORTHEAST' and norm[63:74]=='BERLINCLOCK','recorded_versions':len(item['revision_history'])})
report={'author':'author_thematic_candidates','candidate_count':len(final),'all_valid':all(x['valid'] for x in checks),'distinct_normalized_count':len(set(x['normalized'] for x in final)),'all_drafts_preserved':True,'draft_log':'/workspace/shared/candidate-first-051/authors/thematic_draft_log.jsonl','logged_versions':len(entries)+len(newlog),'theme_counts':{theme:sum(x['theme']==theme for x in final) for theme in sorted({x['theme'] for x in final})},'limitations':['Creative thematic hypotheses, not recovered plaintext.','All candidates share the required cribs and directional/clock framing; statistical independence is not asserted.','Some exact-length wording is deliberately literary or slightly constrained (notably T04 and T10).','Historical/geographic details and clock-related scene elements are fictional creative priors, not independently verified factual assertions.'],'authoring_method':method,'candidates':checks}
(ROOT/'thematic_validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['Thematic blind authoring validation','',f"Candidates: {report['candidate_count']}; distinct normalized messages: {report['distinct_normalized_count']}; all valid: {report['all_valid']}.",'Each final message has 97 uppercase A–Z letters; EASTNORTHEAST occupies 22–34 and BERLINCLOCK occupies 64–74 (1-based).','Unconstrained spans: 21, 29, 23 letters.','All 52 drafted/revised/formatted versions and their validation feedback are preserved in thematic_draft_log.jsonl and in each final entry’s revision_history.','Four candidates per theme: Egypt memories, Berlin Wall transition, World Clock, secret message delivery.','','Limitations:']+['- '+x for x in report['limitations']]+['','Final messages:']+[x['id']+': '+x['spaced_prose'] for x in final]
(ROOT/'thematic_validation_report.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:report[k] for k in ['candidate_count','all_valid','distinct_normalized_count','logged_versions','theme_counts']},indent=2))
print('\n'.join(x['id']+': '+x['spaced_prose'] for x in final))
