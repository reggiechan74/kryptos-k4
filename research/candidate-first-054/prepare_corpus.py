"""Score/target-blind corpus normalization, historical manifest, literal controls."""
from pathlib import Path
from collections import defaultdict,Counter
import hashlib,json,re,bisect
import search as s
ROOT=Path(__file__).resolve().parent

def build_manifest():
    nltk=s.read_json(ROOT/'data/nltk/NLTK_DATE_EVIDENCE.json');pg=s.read_json(ROOT/'data/pg/corpus_manifest_draft.json')
    if pg['fixed_ids_in_prespecified_order']!=s.read_json(ROOT/'CORPUS_PLAN.json')['additional_pg_ids_frozen_before_retrieval']:raise ValueError('PG source IDs changed')
    accepted=[];excluded=[]
    def include(rec):
        raw=(ROOT/rec['raw_path']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=rec['raw_sha256']:raise ValueError('Raw source changed')
        norm,offsets,info=s.normalize_with_offsets(raw,rec['extraction_kind'])
        if len(norm)<97:raise ValueError('Accepted source too short')
        rec.update(info);rec['raw_bytes']=len(raw);rec['valid_97_window_count']=max(0,len(norm)-96)
        rec['uncertified_compilation_boundaries']=[]
        if rec['document_id']=='pg/00205':
            headings=list(re.finditer(rb'^ON THE DUTY OF CIVIL DISOBEDIENCE[ \t]*\r?$',raw[info['body_start']:info['body_end']],re.M))
            if not headings:raise ValueError('Expected declared PG205 work heading absent')
            raw_boundary=info['body_start']+headings[-1].start()
            rec['uncertified_compilation_boundaries']=[{'raw_offset':raw_boundary,'normalized_offset':bisect.bisect_left(offsets,raw_boundary),
                'description':'Last standalone ON THE DUTY OF CIVIL DISOBEDIENCE heading in body; Walden/essay combination date not established',
                'historical_adjacency_verified':False}]
            rec['historical_transcription_uncertainty']+=' PG205combines two historical works; no historical compilation/adjacency date is established. A cross-work window is a modern-transcription candidate pending adjacency verification.'
        accepted.append(rec)
    for r in nltk['records']:
        path='data/nltk/documents/'+r['corpus']+'/'+r['filename'];did='nltk/'+r['corpus']+'/'+r['filename']
        rec={'document_id':did,'collection':'nltk_'+r['corpus'],'raw_path':path,'raw_sha256':r['source_sha256'],
             'extraction_kind':'nltk_'+r['corpus'],'historical_eligibility':r['historical_eligibility'],
             'historical_available_by_year':r['historical_english_work_or_edition_available_by_year'],'date_evidence_urls':r['source_urls'],
             'source_assertions':r['source_assertions'],'historical_transcription_uncertainty':r['uncertainty'],
             'exact_transcription_edition_verified':False,'original_date_manifest':'data/nltk/NLTK_DATE_EVIDENCE.json',
             'source_url':r['source_archive_url'],'archive_entry':r['source_archive_entry'],
             'license':'Official NLTK metadata: Public Domain; retained corpus/archive notices apply.'}
        if r['historical_eligibility']=='include_work_level_only':
            if rec['historical_available_by_year']>1989:raise ValueError('Historical cutoff violated')
            include(rec)
        else:excluded.append({**rec,'exclusion_reason':r['exclusion_reason']})
    for r in pg['records']:
        rec={'document_id':f'pg/{r["pgid"]:05}','collection':'project_gutenberg','raw_path':str(Path(r['path']).relative_to(ROOT)) if r['path'] else None,
             'raw_sha256':r['sha256'],'extraction_kind':'project_gutenberg','historical_eligibility':r['eligibility'],
             'work_date':r['workdate'],'edition_date':r['editiondate'],'date_evidence_urls':[r['dateevidenceURL']],
             'source_assertions':[r['date_evidence_excerpt'],r['historical_date_note']],
             'historical_transcription_uncertainty':r['exact_transcription_historical_provenance'],
             'exact_transcription_edition_verified':False,'original_date_manifest':'data/pg/corpus_manifest_draft.json',
             'source_url':r['rawURL'],'title':r['title'],'author':r['author'],'license':r['license']}
        if r['eligibility']=='eligible_historical_work':
            dated=[int(x) for x in (r['workdate'],r['editiondate']) if x is not None]
            if not dated or any(x>1989 for x in dated):raise ValueError('PG historical cutoff/date unresolved')
            include(rec)
        else:excluded.append({**rec,'exclusion_reason':r['exclusion_reason']})
    accepted.sort(key=lambda x:x['document_id']);excluded.sort(key=lambda x:x['document_id'])
    duplicates=defaultdict(list)
    for r in accepted:duplicates[r['normalized_sha256']].append(r['document_id'])
    collection={}
    for name in sorted({r['collection'] for r in accepted}):
        rows=[r for r in accepted if r['collection']==name]
        collection[name]={'documents':len(rows),'normalized_letters':sum(r['normalized_letters'] for r in rows),'valid_97_windows':sum(r['valid_97_window_count'] for r in rows)}
    manifest={'version':'candidate-first-054-corpus-v1','historical_cutoff_inclusive':'1989-12-31','accepted_documents':accepted,'excluded_documents':excluded,
              'accepted_document_count':len(accepted),'excluded_document_count':len(excluded),'normalized_letters':sum(r['normalized_letters'] for r in accepted),
              'valid_97_windows':sum(r['valid_97_window_count'] for r in accepted),'collection_totals':collection,
              'duplicate_normalized_documents':[v for v in duplicates.values() if len(v)>1],
              'ordered_document_stream_sha256':hashlib.sha256(json.dumps([(r['document_id'],r['normalized_sha256'],r['normalized_letters']) for r in accepted],separators=(',',':')).encode()).hexdigest(),
              'source_plan_sha256':s.sha_file(ROOT/'CORPUS_PLAN.json'),'nltk_dates_sha256':s.sha_file(ROOT/'data/nltk/NLTK_DATE_EVIDENCE.json'),
              'pg_dates_sha256':s.sha_file(ROOT/'data/pg/corpus_manifest_draft.json'),
              'coverage_scope':'Work-level historical eligibility; no blanket exact-edition/wording certification. Exact transcription uncertainty disclosed per source; any hit needs historical wording verification.',
              'prior_brown_letters_not_added_to_total':4745928,'full_document_duplicates_retained':True,'target_lookup_performed':False}
    s.write_json(ROOT/'corpus_manifest.json',manifest);return manifest

def build_controls():
    docs=s.load_corpus();groups={name:sorted([d for d in docs if d.metadata['collection']==name],key=lambda d:d.id) for name in ('nltk_gutenberg','nltk_inaugural','project_gutenberg')}
    if any(not rows for rows in groups.values()):raise ValueError('Every registered source collection must be represented')
    record=s.read_json(ROOT/'control_plaintext.json');plain=s.valid_text(record['normalized'])
    if any(plain[start:start+len(word)]!=word for start,word in s.CRIBS):raise ValueError('Control plaintext cribs')
    controls=[]
    for ti,t in enumerate(s.TABLEAUX):
        for group,boundary in [('nltk_gutenberg','start'),('nltk_inaugural','interior'),('project_gutenberg','end')]:
            doc=groups[group][(7*ti)%len(groups[group])];L=len(doc.normalized);start=0 if boundary=='start' else (L-97)//2 if boundary=='interior' else L-97
            key=doc.normalized[start:start+97].decode();cipher=s.encrypt(plain,key,t)
            controls.append({'id':f'C{len(controls)+1:03}','kind':'planted_positive','tableau_id':t.id,'source_document_id':doc.id,
                             'source_window_start':start,'boundary_case':boundary,'source_collection':group,'key':key,'plaintext':plain,'ciphertext':cipher})
    for t in s.TABLEAUX:
        label='absent-key|'+t.id;rng=s.rng_for(label);key=''.join(rng.choice(s.AZ) for _ in range(97));cipher=s.encrypt(plain,key,t)
        controls.append({'id':f'C{len(controls)+1:03}','kind':'random_absent','tableau_id':t.id,'key':key,'plaintext':plain,'ciphertext':cipher,'rng_label':label})
    if any(hashlib.sha256(x['ciphertext'].encode()).hexdigest()==s.read_json(ROOT/'config.json')['canonical_target_sha256'] for x in controls):raise ValueError('Unexpected control/target collision; stop before lookup')
    assert len(controls)==48;s.write_json(ROOT/'controls.json',controls);return controls

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['manifest','controls']);args=parser.parse_args()
    value=build_manifest() if args.stage=='manifest' else build_controls()
    print(json.dumps({k:value[k] for k in ['accepted_document_count','excluded_document_count','normalized_letters','valid_97_windows','collection_totals','duplicate_normalized_documents']} if isinstance(value,dict) else {'control_count':len(value)},indent=2))
