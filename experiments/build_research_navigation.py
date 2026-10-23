"""Build navigation from the canonical ledger and recorded receipts, without running research.
Only explicit timestamp fields are interpreted; Git times, file mtimes and run-directory
names are never promoted to experiment times. Existing worker README files stay intact.
"""
import datetime,hashlib,json,re,subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'docs/tracking'
CURATION=DEST/'curated-records.json'
TIME_FIELDS={'started_at_utc':'start','run_started_at_utc':'start','finished_at_utc':'end','run_finished_at_utc':'end','run_at_utc':'run instant','recorded_at_utc':'receipt recording','created_at_utc':'artifact creation'}

def tracked():return sorted(subprocess.check_output(['git','ls-files'],cwd=ROOT).decode().splitlines())
def relative(source,target):
 import os
 return quote(os.path.relpath(ROOT/target,(ROOT/source).parent),safe='/#-_.')
def link(source,target,label=None):return '['+(label or target)+']('+relative(source,target)+')'
def clean(value):return str(value).replace('|','\\|').replace('\n',' ')
def iso(value):
 if not isinstance(value,str):return None
 try:
  d=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
  if d.tzinfo is None:return None
  return d.astimezone(datetime.timezone.utc).isoformat().replace('+00:00','Z')
 except ValueError:return None

def entry_date(title,body,date_statement):
 candidates=[('date statement',date_statement),('heading',title),('opening prose',body.split('\n',1)[0])]
 for source,text in candidates:
  if not text:continue
  m=re.search(r'\b(20\d{2}-\d{2}-\d{2})\b',text)
  if m:
   try:return dict(date=datetime.date.fromisoformat(m.group(1)).isoformat(),precision='day',source=source,not_a_run_timestamp=True)
   except ValueError:pass
  m=re.search(r'\b(\d{1,2} [A-Z][a-z]+ 20\d{2})\b',text)
  if m:
   try:return dict(date=datetime.datetime.strptime(m.group(1),'%d %B %Y').date().isoformat(),precision='day',source=source,not_a_run_timestamp=True)
   except ValueError:pass
 return None

def gather():
 import frontier_assessment as f
 curation=json.loads(CURATION.read_text())['records'];reviewed=set()
 files=tracked();canonical=f.canonical((ROOT/'research/HYPOTHESES.md').read_text());hyp=[dict(id=k,**v) for k,v in canonical.items()]
 receipts=[]
 for p in files:
  if not p.startswith('results/') or not p.endswith('.json'):continue
  try:d=json.loads((ROOT/p).read_text())
  except (ValueError,UnicodeError):continue
  if not isinstance(d,dict):continue
  times=[dict(field=k,role=TIME_FIELDS[k],utc=iso(v),original=v) for k,v in d.items() if k in TIME_FIELDS and iso(v)]
  labels=[str(d[k]) for k in ('id','label','kind','experiment','run_id') if k in d and isinstance(d[k],str)]
  receipts.append(dict(path=p,labels=labels,timestamps=times,time_status='explicit receipt fields' if times else 'exact run time unknown in top-level receipt; inspect linked original for nested metadata',status=d.get('status') if isinstance(d.get('status'),str) else None))
 text=(ROOT/'research/EXPERIMENTS.md').read_text();parts=list(re.finditer(r'^## (.+)$',text,re.M));experiments=[]
 for i,m in enumerate(parts):
  title=m.group(1);body=text[m.end():parts[i+1].start() if i+1<len(parts) else len(text)].strip();ids=list(dict.fromkeys(re.findall(r'\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{3}\b',title)))
  direct=set()
  for target in re.findall(r'\]\(([^)]+)\)',body):
   if '://' in target or target.startswith('#'):continue
   path=(ROOT/'research'/target.split('#')[0]).resolve()
   if path.is_file() and ROOT in path.parents:direct.add(str(path.relative_to(ROOT)))
  for target in re.findall(r'(?:experiments|results|research|tests|data)/[A-Za-z0-9_./-]+\.(?:py|json|md|gz|mjs)',body):
   if (ROOT/target).is_file():direct.add(target)
  related=[r for r in receipts if r['path'] in direct or any(ident in r['labels'] for ident in ids)]
  times=[dict(receipt=r['path'],**t) for r in related for t in r['timestamps']]
  date=re.search(r'(?im)^- (?:Date|Run date): ([^\n]+)',body)
  ident='LOG-'+hashlib.sha256(title.encode()).hexdigest()[:10].upper()
  if ident not in curation or curation[ident]['title']!=title:raise ValueError('Explicit category/outcome review required: '+title)
  review=curation[ident];reviewed.add(ident)
  if not review['categories'] or not review['outcome']:raise ValueError('Incomplete curated classification')
  date_statement=date.group(1) if date else None
  experiments.append(dict(record_id=ident,experiment_ids=ids,title=title,categories=review['categories'],outcome=review['outcome'],classification_basis=review['basis'],source='research/EXPERIMENTS.md',recorded_date_statement=date_statement,date_only=entry_date(title,body,date_statement),timestamps=times,links=sorted(direct),receipt_paths=[r['path'] for r in related],original_entry=body))
 if reviewed!=set(curation):raise ValueError('Stale curated record IDs need review')
 return dict(schema=2,canonical_hypothesis_source='research/HYPOTHESES.md',canonical_experiment_source='research/EXPERIMENTS.md',time_policy='Only explicit timezone-bearing receipt fields; no Git or filesystem dates inferred as run times. Date-only prose is preserved as a statement, never expanded to midnight.',hypotheses=hyp,experiments=experiments,receipts=receipts)

def build():
 DEST.mkdir(exist_ok=True,parents=True);d=gather();(DEST/'tracker.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 intro='Generated navigation; edit the canonical ledger or receipts, then run `python3 experiments/build_research_navigation.py`. The JSON retains complete scope fields and original log entries. No experiment is executed by this generator.\n\n'
 p='docs/tracking/HYPOTHESES.md';s='# Hypothesis families\n\n'+intro+'**Family status is not a universal exclusion.** A narrow negative applies only to its specified model. Evidence-blocked and non-identifiable are different from tested and false.\n\n| Stable ID | Status | Mechanism | Exact scope and remaining inputs |\n| --- | --- | --- | --- |\n'
 for h in d['hypotheses']:s+='| '+clean(h['id'])+' | '+clean(h['Status'])+' | '+clean(h['Mechanism'])+' | '+link(p,'research/HYPOTHESES.md',h['id']+' canonical record')+' (#'+h['id'].lower()+') |\n'
 # Separate the anchor correctly rather than embedding it in prose navigation.
 s=re.sub(r'\(\.\./\.\./research/HYPOTHESES.md\) \(#(h-[a-z0-9-]+)\)',r'(../../research/HYPOTHESES.md#\1)',s)
 (DEST/'HYPOTHESES.md').write_text(s)
 p='docs/tracking/EXPERIMENTS.md';s='# Experiments and reviews\n\n'+intro+'This index has one row per existing log section, not one row per independent hypothesis. IDs may share a run; repeated replications are not new discoveries. Categories and outcomes are explicitly reviewed in curated-records.json; new entries require review. Combined categories identify genuinely mixed records. The original scope controls interpretation.\n\nTimes below come only from explicit receipt fields. “Recording” and “creation” are not run start/end. UTC is canonical; no Toronto conversion is inferred. Unknown means unknown, not the commit time.\n\n| IDs / record | Entry | Type | Outcome / status | Recorded timing | Detail |\n| --- | --- | --- | --- | --- | --- |\n'
 details='# Experiment details\n\n'+intro
 for e in d['experiments']:
  name=', '.join(e['experiment_ids']) or e['record_id'];time='; '.join(dict.fromkeys(t['role']+': '+t['utc'] for t in e['timestamps'])) or 'Exact run start/end unknown'
  if e['date_only']:time+='; date-only record: '+e['date_only']['date']+' ('+e['date_only']['source']+'; not a run timestamp)'
  if e['recorded_date_statement']:time+='; original date statement: '+e['recorded_date_statement']
  s+='| '+clean(name)+' | '+clean(e['title'])+' | '+clean('; '.join(e['categories']))+' | '+clean(e['outcome'])+' | '+clean(time)+' | [Scope, result, code and receipts](EXPERIMENT-DETAILS.md#'+e['record_id'].lower()+') |\n'
  details+='## '+e['record_id']+'\n\n**'+e['title']+'**\n\n'+time+'\n\nType: '+clean('; '.join(e['categories']))+'. Outcome: '+e['outcome']+'\n\nSource: '+link('docs/tracking/EXPERIMENT-DETAILS.md','research/EXPERIMENTS.md','canonical experiment log')+'.\n\n'
  # Rebase original local Markdown links into this generated location.
  body=re.sub(r'\]\(([^)]+)\)',lambda m:']('+m.group(1)+')' if '://' in m.group(1) or m.group(1).startswith('#') else ']('+relative('docs/tracking/EXPERIMENT-DETAILS.md',str((Path('research')/m.group(1)).as_posix()))+')',e['original_entry'])
  details+=body+'\n\n'
  if e['links']:details+='Related files: '+', '.join(link('docs/tracking/EXPERIMENT-DETAILS.md',x) for x in e['links'])+'.\n\n'
 (DEST/'EXPERIMENTS.md').write_text(s);(DEST/'EXPERIMENT-DETAILS.md').write_text(details.rstrip()+'\n')
 p='docs/tracking/RECEIPTS.md';s='# Result and run receipts\n\n'+intro+'One row per tracked top-level JSON result artifact. Several artifacts can describe the same run; do not add rows as search counts. Original timestamps and their field names are retained in tracker.json. Nested metadata may contain additional detail; unknown here is not a claim that the experiment never ran.\n\n| Artifact | Recorded label / kind | Explicit timestamp roles (UTC) |\n| --- | --- | --- |\n'
 for r in d['receipts']:s+='| '+link(p,r['path'])+' | '+clean('; '.join(r['labels'])[:300])+' | '+clean('; '.join(t['role']+': '+t['utc'] for t in r['timestamps']) or 'Exact run start/end unknown; inspect original')+' |\n'
 (DEST/'RECEIPTS.md').write_text(s)
 return d
if __name__=='__main__':
 d=build();print(json.dumps(dict(hypotheses=len(d['hypotheses']),log_sections=len(d['experiments']),json_receipts=len(d['receipts']))))
