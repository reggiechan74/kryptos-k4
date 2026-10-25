import json,re
from pathlib import Path
ROOT=Path('/workspace/shared/candidate-first-052/authors')
LOG=ROOT/'a_themes_drafts.jsonl'
def norm(s): return re.sub('[^A-Z]','',s.upper())
def save(i,theme,a,b,c,note='Whole-message composition or constraint/readability revision; no phrase-bank combination.'):
    ident=f'A{i:03d}'
    prose=a+' east-north-east '+b+' Berlin clock '+c
    prose=prose.replace(' ;',';').replace(' ,',',').replace(' .','.').replace(' :',':').replace(' ?','?').replace(' !','!')
    n=norm(prose); spans=[len(norm(x)) for x in (a,b,c)]
    feedback={'span_lengths':spans,'letter_count':len(n),'first_crib_start':n.find('EASTNORTHEAST')+1,'second_crib_start':n.find('BERLINCLOCK')+1,'valid':len(n)==97 and n[21:34]=='EASTNORTHEAST' and n[63:74]=='BERLINCLOCK'}
    row={'id':ident,'theme':theme,'spaced_prose':prose,'normalized':n,'parts':[a,b,c],'feedback':feedback,'note':note}
    with LOG.open('a') as f:f.write(json.dumps(row)+'\n')
    print(ident,spans,'OK' if feedback['valid'] else 'NEEDS REVISION')
def revise(i,a=None,b=None,c=None,note='Full-message revision for exact letter spans and readability.'):
    ident=f'A{i:03d}'; rows=[json.loads(x) for x in LOG.read_text().splitlines()]; old=[r for r in rows if r['id']==ident][-1]
    vals=old['parts']; save(i,old['theme'],a if a is not None else vals[0],b if b is not None else vals[1],c if c is not None else vals[2],note)
def export():
    histories={}
    for line in LOG.read_text().splitlines():
        r=json.loads(line); histories.setdefault(r['id'],[]).append(r)
    finals=[]; invalid=[]
    method='Blind assistant-authored complete messages, composed one at a time in batches. Python used for normalization, length/crib-position feedback, revision recording, and artifact packaging only. No ciphertext, keys, scores, pilot results, other authors, solution discussions, external models, or external sources were consulted. Occasional grammatical scaffolding is reused; no Cartesian phrase-bank generation or statistical-independence claim.'
    for ident,rs in histories.items():
        r=rs[-1]
        if not r['feedback']['valid']: invalid.append(ident); continue
        finals.append({k:r[k] for k in ['id','spaced_prose','normalized','theme']}|{'revision_history':[{'revision':j+1,'spaced_prose':v['spaced_prose'],'normalized':v['normalized'],'feedback':v['feedback'],'note':v['note']} for j,v in enumerate(rs)],'authoring_method':method})
    (ROOT/'a_themes.json').write_text(json.dumps(finals,indent=2)+'\n')
    report={'accepted_count':len(finals),'drafted_messages':len(histories),'logged_versions':sum(map(len,histories.values())),'pending_invalid':invalid,'distinct_normalized_count':len(set(x['normalized'] for x in finals)),'validation':'97 uppercase A–Z letters; EASTNORTHEAST22–34; BERLINCLOCK64–74; unconstrained spans21/29/23.','authoring_method':method,'quality_limitations':['Creative priors, not decryption claims or verified historical/geographical facts.','Exact crib and length constraints favor explicit direction/name references, time imagery, and occasional unusual wording.','Grammatical scaffolding sometimes recurs; statistical independence is not claimed.'],'candidates':[{'id':x['id'],'letter_count':len(x['normalized']),'first_crib_start':x['normalized'].find('EASTNORTHEAST')+1,'second_crib_start':x['normalized'].find('BERLINCLOCK')+1} for x in finals]}
    (ROOT/'a_themes_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('ACCEPTED',len(finals),'DRAFTED',len(histories),'INVALID',invalid)
