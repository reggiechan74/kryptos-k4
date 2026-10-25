import json,re
from pathlib import Path
ROOT=Path('/workspace/shared/candidate-first-052/authors')
LOG=ROOT/'b_neutral_drafts.jsonl'
OUT=ROOT/'b_neutral.json'
def norm(s): return re.sub('[^A-Z]','',s.upper())
def prose(spans):
 a,b,c=spans
 result=a+' east-north-east '+b+' Berlin Clock '+c
 for mark in [',','.',';',':','?','!']:
  result=result.replace(' '+mark,mark)
 return result

def record(batch, note='Individually composed whole-message draft; length and position feedback only.'):
 old=[json.loads(x) for x in LOG.read_text().splitlines()] if LOG.exists() else []
 revisions={}
 for x in old: revisions[x['id']]=revisions.get(x['id'],0)+1
 with LOG.open('a') as f:
  for cid,spans in batch.items():
   p=prose(spans); n=norm(p); lens=[len(norm(s)) for s in spans]
   item={'id':cid,'revision':revisions.get(cid,0),'spans':spans,'spaced_prose':p,'normalized':n,'feedback':{'span_lengths':lens,'target':[21,29,23],'length':len(n),'crib_positions_correct':n[21:34]=='EASTNORTHEAST' and n[63:74]=='BERLINCLOCK'},'revision_note':note}
   f.write(json.dumps(item)+'\n')
   if lens!=[21,29,23]:print(cid,lens,spans)
 refresh()

def refresh():
 allrecs=[json.loads(x) for x in LOG.read_text().splitlines()]
 h={}
 for x in allrecs:h.setdefault(x['id'],[]).append(x)
 accepted=[]
 for cid,trail in h.items():
  r=trail[-1]
  if r['feedback']['span_lengths']==[21,29,23] and r['feedback']['crib_positions_correct']:
   accepted.append({'id':cid,'spaced_prose':r['spaced_prose'],'normalized':r['normalized'],'revision_history':trail,'theme':'Neutral observations, descriptions, and ordinary communications','authoring_method':'Blind constraint-aware individual whole-message composition, followed only by A-Z length/position feedback and prose review. No Cartesian phrase-bank generation. Some grammatical scaffolding recurs; no statistical independence claim. No ciphertext, keys, scores, pilot results, other author files, or external model APIs inspected.'})
 assert len({r['normalized'] for r in accepted})==len(accepted),'Duplicate within this own bank'
 OUT.write_text(json.dumps(accepted,indent=2)+'\n')
 print('ACCEPTED',len(accepted),'DRAFTED_IDS',len(h))
