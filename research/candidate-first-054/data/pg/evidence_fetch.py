import pathlib, urllib.request, hashlib, json, datetime, concurrent.futures, re, html
B=pathlib.Path('/workspace/shared/candidate-first-054/data/pg')
SOURCES={
'1342_work':'https://exhibits.library.illinois.edu/s/rbml/item/1104',
'84_work':'https://www.loc.gov/item/53051218/',
'1661_work':'https://www.themorgan.org/printed-books/268783',
'98_work':'https://natlib.govt.nz/records/21706196',
'1400_work':'https://dickens.stanford.edu/dickens/archive/great/pdf/great35.pdf',
'174_work':'https://www.themorgan.org/collection/oscar-wilde/the-picture-of-dorian-gray',
'345_work':'https://rosenbach.org/wp-content/uploads/2021/05/Dracula-and-Vampire-Literature-Guide-20210420.pdf',
'76_work':'https://loc.gov/exhibits/america-reads/1750-to-1899.html',
'74_work':'https://www.loc.gov/pictures/item/2006681444/',
'12_work':'https://www.themorgan.org/printed-books/78133',
'120_work':'https://www.themorgan.org/printed-books/72350',
'35_work':'https://www.themorgan.org/printed-books/372286',
'36_work':'https://www.loc.gov/lcm/pdf/LCM_2016_0708.pdf',
'43_work':'https://www.loc.gov/item/50041978/',
'219_work':'https://catalogue.bnf.fr/ark:/12148/cb11936152f',
'203_work':'https://www.loc.gov/item/today-in-history/june-05',
'1260_work':'https://www.themorgan.org/printed-books/72468',
'768_work':'https://static-prod.lib.princeton.edu/scsites/parrish/4-Brontes.pdf',
'1080_work':'https://catalogue.nli.ie/Record/vtls000193222',
'205_civil_work':'https://utc.iath.virginia.edu/saxon/servlet/SaxonServlet?clear-stylesheet-cache=yes&source=utc%2Fxml%2Fpretexts%2Fabolitn%2Fabeshdta.xml&style=utc%2Fxsl%2Fabout.xsl',
'1232_translation':'https://ci.nii.ac.jp/ncid/BA19419516.amp?l=en',
'5001_translation':'https://www.si.edu/object/siris_sil_93270',
'5001_files':'https://www.gutenberg.org/files/5001/',
'pg_terms':'https://www.gutenberg.org/policy/terms_of_use.html',
'pg_permission':'https://www.gutenberg.org/policy/permission.html',
'pg_license':'https://www.gutenberg.org/policy/license.html'
}
(B/'evidence_sources_plan.json').write_text(json.dumps(SOURCES,indent=2)+'\n')
def task(kv):
 k,u=kv;p=B/'evidence'/(k+('.pdf' if '.pdf' in u else '.html'));now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(u,timeout=35) as r:
   data=r.read(8_000_001)
   if len(data)>8_000_000: raise ValueError('8 MB bound exceeded')
   p.write_bytes(data);d={'id':k,'url':u,'final_url':r.url,'retrieved_utc':now,'status':r.status,'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'headers':dict(r.headers)}
 except Exception as e:d={'id':k,'url':u,'retrieved_utc':now,'status':'error','error':repr(e)}
 p.with_suffix(p.suffix+'.receipt.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k in ['id','status','error','bytes']}),flush=True);return d
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rs=list(ex.map(task,SOURCES.items()))
(B/'evidence_acquisition.json').write_text(json.dumps(rs,indent=2)+'\n')
