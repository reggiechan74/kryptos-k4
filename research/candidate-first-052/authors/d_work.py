import json, re, pathlib, datetime
ROOT=pathlib.Path('/workspace/shared/candidate-first-052/authors')
LOG=ROOT/'d_drafts.jsonl'
OUT=ROOT/'d_messages.json'
def norm(s): return re.sub('[^A-Z]','',s.upper())
def submit(batch):
    current={}
    if OUT.exists(): current={x['id']:x for x in json.loads(OUT.read_text())}
    for n, v in batch.items():
        a,b,c,theme=v
        ident=f'd_{n:03d}'
        prose=a+' “EAST NORTH EAST” '+b+' BERLIN CLOCK '+c
        prose=re.sub(r'\s+([,.;:?!])', r'\1', prose)
        normalized=norm(prose)
        lengths=list(map(lambda s:len(norm(s)),[a,b,c]))
        valid=lengths==[21,29,23] and len(normalized)==97 and normalized[21:34]=='EASTNORTHEAST' and normalized[63:74]=='BERLINCLOCK'
        history=current.get(ident,{}).get('revision_history',[])
        revision={'revision':len(history)+1,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'spaced_prose':prose,'segments':[a,b,c],'feedback':{'segment_lengths':lengths,'target_lengths':[21,29,23],'normalized_length':len(normalized),'constraints_valid':valid}}
        with LOG.open('a') as f: f.write(json.dumps({'id':ident,**revision})+'\n')
        history=history+[revision]
        current[ident]={'id':ident,'spaced_prose':prose,'normalized':normalized,'revision_history':history,'theme':theme,'authoring_method':'Individually composed blind fictional English message; local feedback limited to letter counts, fixed-label positions, readability, and internal uniqueness. No key, ciphertext, scoring, solution, pilot-result, or other-author access.'}
        if not valid: print(ident, lengths, '|', a,'|',b,'|',c)
    OUT.write_text(json.dumps(list(sorted(current.values(),key=lambda x:x['id'])),indent=2)+'\n')
    ok=sum(len(x['normalized'])==97 and x['normalized'][21:34]=='EASTNORTHEAST' and x['normalized'][63:74]=='BERLINCLOCK' for x in current.values())
    print('TOTAL',len(current),'VALID',ok)
def revise(changes):
    current={x['id']:x for x in json.loads(OUT.read_text())}
    batch={}
    for n, patch in changes.items():
        x=current[f'd_{n:03d}']
        seg=x['revision_history'][-1]['segments'][:]
        for i,s in patch.items(): seg[i]=s
        batch[n]=seg+[x['theme']]
    submit(batch)
def submit_text(s):
    batch={}
    for line in s.strip().splitlines():
        n,a,b,c,theme=line.split('|')
        batch[int(n)]=[a,b,c,theme]
    submit(batch)
