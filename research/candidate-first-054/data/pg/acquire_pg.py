import urllib.request, pathlib, hashlib, json, re, concurrent.futures, datetime, time, threading
BASE=pathlib.Path('/workspace/shared/candidate-first-054/data/pg')
IDS=[1342,84,1661,98,1400,174,345,76,74,12,120,35,36,43,219,203,1260,768,1080,23,205,1232,1228,5001]
lock=threading.Lock(); total=0; LIMIT=100_000_000

def fetch(url,path):
 global total
 req=urllib.request.Request(url,headers={'User-Agent':'Public-domain academic corpus provenance audit; fixed 24-book metadata/plain-text acquisition'})
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(req,timeout=35) as r:
  data=r.read(8_000_001)
  if len(data)>8_000_000: raise ValueError('per-source 8MB bound')
  with lock:
   if total+len(data)>LIMIT: raise ValueError('total100MB bound')
   total+=len(data)
  path.write_bytes(data)
  rec={'url':url,'final_url':r.url,'retrieved_utc':now,'status':r.status,'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'headers':dict(r.headers)}
  path.with_suffix(path.suffix+'.receipt.json').write_text(json.dumps(rec,indent=2)+'\n')
  return data,rec

def task(i):
 try:
  html,m=fetch(f'https://www.gutenberg.org/ebooks/{i}',BASE/'metadata'/f'pg{i}.html')
  s=html.decode('utf-8','replace')
  links=re.findall(r'href="([^"]+)"[^>]*type="text/plain[^\"]*"',s)
  if not links:
   links=re.findall(r'href="([^"]+(?:\.txt(?:\.utf-8)?|\.txt\.utf-8))"',s)
  links=list(dict.fromkeys(links))
  if not links: raise ValueError('no linked official text URL')
  link=next((x for x in links if '/cache/epub/' in x),links[0])
  url=urllib.parse.urljoin(m['final_url'],link)
  if not url.startswith('https://www.gutenberg.org/'): raise ValueError('nonofficial URL')
  raw,r=fetch(url,BASE/'raw'/f'pg{i}.txt')
  title=re.search(r'<meta name="title" content="([^"]+)"',s)
  result={'pgid':i,'title_metadata':title.group(1) if title else None,'metadata':m,'raw':r,'status':'downloaded'}
 except Exception as e:
  result={'pgid':i,'status':'error','error':repr(e)}
 (BASE/'metadata'/f'pg{i}.acquisition.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'id':i,'status':result['status'],'bytes':result.get('raw',{}).get('bytes'),'error':result.get('error')}),flush=True)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: results=list(ex.map(task,IDS))
(BASE/'acquisition.json').write_text(json.dumps({'fixed_ids':IDS,'total_bytes':total,'results':results},indent=2)+'\n')
