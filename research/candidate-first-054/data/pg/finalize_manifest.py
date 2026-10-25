import pathlib,json,hashlib,re,datetime
B=pathlib.Path('/workspace/shared/candidate-first-054/data/pg');P=B/'corpus_manifest_draft.json';m=json.loads(P.read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
EV={1342:['1342_work.html'],84:['primary_catalogs_a.webtool.json'],1661:['primary_catalogs_a.webtool.json'],98:['primary_catalogs_a.webtool.json'],1400:['1400_work.pdf','1400_work.extracted.txt'],174:['primary_catalogs_a.webtool.json'],345:['primary_catalogs_c.webtool.json'],76:['primary_catalogs_b.webtool.json'],74:['primary_catalogs_b.webtool.json'],12:['primary_catalogs_b.webtool.json'],120:['primary_catalogs_c.webtool.json'],35:['primary_catalogs_c.webtool.json'],36:['primary_catalogs_c.webtool.json'],43:['searchdates8.webtool.json'],219:['219_work.html','searchdates6.webtool.json'],203:['searchdates8.webtool.json','primary_catalogs_b.webtool.json'],1260:['searchdates6.webtool.json'],768:['768_work.pdf','768_work.extracted.txt'],1080:['searchdates7.webtool.json'],23:['body_bibliographic_inspection.json'],205:['searchdates8.webtool.json','primary_catalogs_d.webtool.json'],1232:['1232_translation.html','primary_catalogs_d.webtool.json','prince_original_date.webtool.json'],1228:['body_bibliographic_inspection.json'],5001:['5001_files.html']}
def stamp(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for p in (B/'evidence').glob('*.webtool.json'):
 d=json.loads(p.read_text());d.pop('captured_utc',None);d.pop('retrieved_utc',None);d['receipt_file_created_utc']=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat();d['timestamp_note']='Capture file timestamp; upstream page crawl time is separately reported inside tool result.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
inspection={x['id']:x for x in json.loads((B/'evidence'/'body_bibliographic_inspection.json').read_text())}
for r in m['records']:
 i=r['pgid'];r['status']='eligible_source_provenance_ready_for_independent_audit' if r['eligibility']=='eligible_historical_work' else 'excluded'
 r['date_evidence_receipts']=[stamp(B/'evidence'/p) for p in EV[i]]
 r['date_evidence_interpretation']='Use only the cited primary institution/catalog or original title material; other search hits are not evidence. Web search snapshots are provider-mediated cached evidence, not original page bytes. Direct raw retrieval failures are retained in evidence_acquisition.json.'
 r['editiondate_scope']='Known historical edition or translation version where specified, not a claim that every current PG character was present in that edition.'
 r['exact_pg_printing_identified']=i in (1342,1400,1260,23,1228)
 if i in inspection:
  b=inspection[i];r['body_boundary_inspection']={k:b[k] for k in ['start_count','end_count','body_start_byte','body_end_byte','body_bytes','body_sha256']}
  raw=pathlib.Path(r['path']).read_text(encoding='utf-8-sig');rd=re.search(r'^Release date: (.+)',raw,re.M);up=re.search(r'^\s*Most recently updated: (.+)',raw,re.M)
  r['digital_release_date_not_historical']=rd.group(1).strip() if rd else None;r['digital_update_date_not_historical']=up.group(1).strip() if up else None
 r['license']['retained_license_snapshot_files']=[stamp(B/'evidence'/x) for x in ['pg_license.html','pg_permission.html','pg_terms.html']]
 r['license']['terms_summary']='PG distinguishes US-public-domain book text from its trademark and compilation/license terms. Private analysis is not publication. Preserve original licensed downloads; if redistributed with PG association, follow the complete retained license, including access to the license and applicable trademark conditions. No external redistribution authorized here.'
 if i==36:
  r['dateevidenceURL']='https://www.themorgan.org/printed-books/371751';r['date_evidence_excerpt']='London : William Heinemann, 1898.';r['historical_date_note']='Morgan first-edition catalog: book1898; original serial April–December1897. Exact PG printing unspecified.'
 if i==174:
  r['dateevidenceURL']='https://www.themorgan.org/printed-books/130859';r['date_evidence_excerpt']='first published in book form by Ward, Lock & Co., London, 1891.'
 if i==1232:
  r['workdate']='1532';r['original_language']='Italian';r['original_publication_evidence']={'url':'https://catalogue.bnf.fr/ark:/12148/cb30853370h','excerpt':"Publication : Roma : Antonio Blado d’Asola, 1532",'kind':'Primary holding catalog of original printed edition including the two supplemental works.'};r['translationdate']='1908';r['historical_date_note']='Original Italian print1532; English eligibility rests on W. K. Marriott translation1908, not1532. Introduction and supplemental pieces retained as supplied; exact PG printing is unidentified and literal passages need historical checking.'
 if i==205:r['historical_date_note']+=' Compilation date is not established; retain document boundary and do not treat a cross-work boundary as proof of historical co-occurrence.'
 if i==12:r['historical_date_note']+=' Morgan PML352454 records author inscription Christmas1871, demonstrating early availability despite1872 imprint; exclusion remains unchanged.'
 r['body_inspection_limit']='Front/end bibliographic review plus literal editorial/date sentinel scan, not a line-by-line textual collation against a historical printed copy.'
m['snapshot_utc']=now;m['source_acquisition_completed_utc']=now;m['date_audit_status']='All20 proposed eligible works have historical work or translation evidence, with edition/transcription limitations explicit; independent parent audit still required.'
m['raw_preservation']='Authoritative corpus and metadata snapshot bodies are preserved unchanged with SHA256. Two initial PG1342 connectivity smoke-test bodies were not persisted; HTTP-error response bodies were not captured, but URL/status/error records remain. All evidence relied on is preserved as raw pages/PDFs or labeled mediated receipts.'
m['normalization_status']='NOT PERFORMED by source agent. Central implementation owns ASCII normalization and reversible offset map.'
m['editorial_rule']='Exclude unresolved modern material inside START/END, no per-source trimming:12,23,1228.5001excluded for no current plaintext. No substitutions.'
m['network_outcome_notes']=['Official linked /ebooks/<id>.txt.utf-8 endpoints returned404; standard official cache URLs worked for23IDs.','5001metadata and linked files index offer no current plaintext; no old-version retrieval, HTML conversion, or alternative PG ID used.','Several official library sites denied direct raw HTML with403; public indexed primary catalog content obtained with web search and clearly labeled. National Library of New Zealand raw200 body is only an anti-bot challenge and is NOT date evidence.']
P.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
# Frozen input bytes inventory for source audit; excludes this inventory and manifests/scripts themselves.
items=[]
for d in ['raw','metadata','evidence']:
 for p in sorted((B/d).glob('*')):
  if p.is_file():items.append(stamp(p))
(B/'source_snapshot_inventory.json').write_text(json.dumps({'created_utc':now,'files':items,'total_preserved_bytes':sum(x['bytes'] for x in items)},indent=2)+'\n')
print('ready',len(m['records']),m['eligible_count'],m['excluded_ids'],hashlib.sha256(P.read_bytes()).hexdigest())
