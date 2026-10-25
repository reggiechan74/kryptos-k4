import pathlib,urllib.request,hashlib,json,datetime,concurrent.futures
B=pathlib.Path('/workspace/shared/candidate-first-054/data/pg')
IDS=[1342,84,1661,98,1400,174,345,76,74,12,120,35,36,43,219,203,1260,768,1080,23,205,1232,1228,5001]
def task(i):
 u=f'https://www.gutenberg.org/cache/epub/{i}/pg{i}.txt'; p=B/'raw'/f'pg{i}.txt'
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(u,timeout=35) as r:
   data=r.read(8_000_001)
   if len(data)>8_000_000: raise ValueError('8 MB file bound exceeded')
   p.write_bytes(data)
   d={'pgid':i,'url':u,'final_url':r.url,'retrieved_utc':now,'status':r.status,'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'headers':dict(r.headers),'alternate_reason':'Official linked ebooks/id.txt.utf-8 endpoint returned HTTP 404; standard official cache path used, no access-control bypass.'}
 except Exception as e: d={'pgid':i,'url':u,'retrieved_utc':now,'status':'error','error':repr(e)}
 p.with_suffix('.txt.receipt.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k in ['pgid','status','error','bytes']}),flush=True)
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: rs=list(ex.map(task,IDS))
(B/'canonical_acquisition.json').write_text(json.dumps(rs,indent=2)+'\n')
