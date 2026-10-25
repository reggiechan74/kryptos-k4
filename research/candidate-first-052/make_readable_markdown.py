from pathlib import Path
import json,re,hashlib
root=Path(__file__).parent
sets=[('A','Memory, Egypt, art and time','a_themes.json'),('B','Neutral observations and everyday messages','b_neutral.json'),('C','Berlin, borders and changing times','c_berlin.json'),('D','Messages, concealment and interpretation','d_messages.json')]
lines=['# Kryptos K4: 1,024 candidate messages','', 'Candidate-first experiment 052 · 25 October 2026','', 'These are invented, AI-authored plaintext hypotheses, not recovered plaintext or verified historical/geographical statements. No expanded-batch key scoring was used to write or select them. Recurrent phrasing and themes mean the messages are not statistically independent.','', 'Every message contains exactly 97 letters after removing spaces and punctuation and converting to uppercase. EASTNORTHEAST occupies letter positions 22–34; BERLINCLOCK occupies positions 64–74. All 1,024 normalized messages are distinct.','', 'Four groups contain 256 messages each. IDs below combine the group label with the original author ID. Spaces and punctuation are retained for readability.','']
seen=set(); records=[]; hashes={}
for group,title,filename in sets:
 p=root/'authors'/filename; raw=p.read_bytes(); hashes[filename]=hashlib.sha256(raw).hexdigest(); rows=json.loads(raw)
 assert len(rows)==256
 lines += [f'## Group {group}: {title}', '']
 for row in rows:
  prose=row['spaced_prose']; normalized=re.sub('[^A-Z]','',prose.upper())
  assert normalized==row['normalized'] and len(normalized)==97
  assert normalized[21:34]=='EASTNORTHEAST' and normalized[63:74]=='BERLINCLOCK'
  assert normalized not in seen;seen.add(normalized)
  cid=group+':'+row['id'];lines += [f'### {cid}', '', prose, ''];records.append((cid,prose))
assert len(records)==1024
out=root/'Kryptos-K4-1024-Candidate-Messages.md';out.write_text('\n'.join(lines),encoding='utf-8')
s=out.read_text();assert len(re.findall(r'^### ',s,re.M))==1024
for cid,prose in records:assert f'### {cid}\n\n{prose}\n' in s
receipt={'count':1024,'unique_normalized':len(seen),'all_constraints_valid':True,'source_sha256':hashes,'markdown_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'size_bytes':out.stat().st_size}
(root/'message_markdown_validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt));print(out)
