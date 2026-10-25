import json,hashlib,re
from pathlib import Path
from a_themes_work import ROOT,LOG,norm,export
rows=[json.loads(x) for x in LOG.read_text().splitlines()]
latest={x['id']:x for x in rows}
literal={14,15,20,23,26,27,28,30,31,32,39,42,45,46,53,54,55,56,57,60,77,84,99,100,102,104,105,106,107,108,116,122,127,137,145,148,149,155,156,162,167,170,178,180,184,189,197,198,200,203,209,210,212,219,233,245,250,255}
apposition={128,138,139,152,159}
new=[]
for ident,r in latest.items():
    i=int(ident[1:]); a,b,c=r['parts']
    if i in literal:
        crib='east-north-east'
        if a.rstrip().endswith(('.', '?', '!')): crib='East-north-east'
    else:
        crib='“East North East”' if i in {6,211} else '“East-north-east”'
    if i in {128,138,139}: a=a.rstrip()+':'
    if i in {152,159}: a=a.rstrip()+','; b=','+b
    if i==36: b=','+b
    prose=a+' '+crib+' '+b+' Berlin clock '+c
    prose=re.sub(r'\s+([;,:.!?])',r'\1',prose)
    prose=re.sub(r'([,;:])(?=\S)',r'\1 ',prose)
    assert norm(prose)==r['normalized'],ident
    v=dict(r);v['spaced_prose']=prose
    v['note']='Final punctuation/capitalization audit; quoted title/inscription versus literal-direction rendering. No normalized letters changed.'
    v['crib_rendering']='literal_direction' if i in literal else 'quoted_name_or_inscription'
    new.append(v)
with LOG.open('a') as f:
    for x in new:f.write(json.dumps(x)+'\n')
export()
path=ROOT/'a_themes.json'; data=json.loads(path.read_text())
assert len(data)==256 and len({x['normalized'] for x in data})==256
for x in data:
    n=x['normalized'];assert re.fullmatch('[A-Z]{97}',n) and n[21:34]=='EASTNORTHEAST' and n[63:74]=='BERLINCLOCK'
sha=hashlib.sha256(path.read_bytes()).hexdigest()
rp=ROOT/'a_themes_validation.json';report=json.loads(rp.read_text())
report.update({'finalized':True,'final_file_sha256':sha,'requested_count':256,'shortage':0,'final_prose_audit':'All 256 own messages were read in full; 29 targeted semantic/readability revisions and final typography were logged. No ciphertext, scores, pilot results, or other author outputs were used.','quoted_name_or_inscription_count':256-len(literal),'literal_direction_rendering_count':len(literal),'own_pilot_exclusion':'No original pilot message was reused. All 256 were newly composed; original051 files were not read or modified during this expansion.','specific_quality_caveats':['Title, inscription, remembered-phrase, and two-sentence scaffolding are frequent. The set is not statistically independent.','The words old, my, and the recur in clock noun phrases because of exact letter constraints. No Cartesian phrase-bank crossproduct was used.','Some messages are deliberately literary or metaphorical, e.g. A014, A031, A123, A174; they should not be treated as verified literal descriptions.','Ancient artifacts, Nile routes, clocks, chimes, and miniature replicas are fictional thematic premises, not claims about actual geography, archaeology, clock mechanisms, or recovered plaintext.','No exact normalized duplicates within this author set. Cross-author duplicate checking is left to the parent to preserve author blindness.']})
rp.write_text(json.dumps(report,indent=2)+'\n')
notes='''FINAL: 256 new thematic candidates; no shortage.\nAll normalized messages contain exactly 97 uppercase A–Z letters.\nEASTNORTHEAST occupies 22–34; BERLINCLOCK occupies 64–74, 1-based.\nAll complete-message drafts, revisions, feedback, and final typography are append-only in a_themes_drafts.jsonl and embedded as revision_history.\nIndividual complete-message composition; occasional grammatical scaffolding reused, no Cartesian phrase-bank combinations.\nPython performed length/position validation, recordkeeping, and artifact packaging, not key or candidate-quality scoring.\nNo ciphertext, keys, scores, pilot results, other author outputs, solution discussions, external model APIs, or cloud threads were used.\nThe original051 files were not read or changed during this expansion.\nBiases: quoted titles/inscriptions and two-sentence recollections are common; exact lengths encourage repeated short grammatical words. Statistical independence is not claimed.\nSome scenes are poetic, and geography/archaeology/clock behavior are fictional priors, not factual or decryption assertions.\nNo exact normalized duplicates within these256; cross-author checks remain the parent's responsibility.\n'''
(ROOT/'a_themes_authoring_notes.txt').write_text(notes+'\nSHA256 a_themes.json: '+sha+'\n')
print(json.dumps({'accepted':len(data),'distinct':len({x['normalized'] for x in data}),'logged_versions':report['logged_versions'],'final_file':str(path),'sha256':sha,'quoted_count':report['quoted_name_or_inscription_count'],'literal_count':len(literal)},indent=2))
