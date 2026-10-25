"""Deterministic score-blind window/control preparation and fixed LM training."""
from pathlib import Path
from array import array
from collections import Counter
import hashlib,json,re,time,math
import reference as p
from prepare_source_plan import normalized
ROOT=Path(__file__).resolve().parent

def load_documents():
    plan=p.load_json(ROOT/'CONTROL_SOURCE_PLAN.json');docs=[]
    for r in plan['documents']:
        raw=(ROOT/r['raw_path']).read_bytes();text,removed=normalized(raw)
        if hashlib.sha256(raw).hexdigest()!=r['raw_sha256'] or hashlib.sha256(text).hexdigest()!=r['normalized_sha256']:raise ValueError('Source changed')
        docs.append({**r,'raw':raw,'norm':text,'removed':removed})
    novels=p.load_json(ROOT/'controls/novel_key_documents.json')
    if len(novels)!=12 or [r['id'] for r in novels]!=[r['id'] for r in plan['novel_topics']]:raise ValueError('Novel count/IDs')
    for r,topic in zip(novels,plan['novel_topics']):
        raw=r['prose'].encode('utf8');text=p.normalize(raw)
        if any(ord(c)>127 and c.isalpha() for c in r['prose']):raise ValueError('Non-ASCII alphabetic novel prose')
        if r['normalized']!=text.decode() or r['alphabetic_length']!=len(text) or not 200<=len(text)<=600:raise ValueError('Novel normalization/length')
        # Author omitted optional leading articles in three metadata labels; prose is unchanged.
        canonical_topic=lambda s:re.sub(r'^(a|an) ', '', s)
        if r['style']!=topic['style'] or canonical_topic(r['topic'])!=canonical_topic(topic['topic']):raise ValueError('Novel topic mismatch')
        docs.append({'document_id':'novel/'+r['id'],'role':'novel_control','raw':raw,'norm':text,'removed':0,
                     'raw_sha256':hashlib.sha256(raw).hexdigest(),'normalized_sha256':hashlib.sha256(text).hexdigest(),
                     'style':r['style'],'topic':r['topic']})
    return docs

def window_grid(length,label):
    if length<97:return []
    margin=min(512,(length-97)//4);lo=margin;hi=length-97-margin;rng=p.rng_for(label)
    phase=rng.randrange(min(512,hi-lo+1));grid=list(range(lo+phase,hi+1,512));rng.shuffle(grid)
    return grid

def letter_offsets(doc):
    if 'offsets' not in doc:
        doc['offsets']=array('I',(i for i,b in enumerate(doc['raw']) if i>=doc['removed'] and (65<=b<=90 or 97<=b<=122)))
        assert len(doc['offsets'])==len(doc['norm'])
    return doc['offsets']

def overlap_reason(key,doc,documents):
    for other in documents:
        if other['role']==doc['role']:continue
        # Exact substring checks against full normalized other-role documents.
        for j in range(50):
            at=other['norm'].find(key[j:j+48])
            if at>=0:return {'reason':'cross_role_48_overlap','other_document':other['document_id'],'window_relative_start':j,'other_start':at}
    return None

def prepare_windows():
    docs=load_documents();seen=set();rejected=[];selected=[];grids={};cursors={}
    for d in docs:
        if d['role']=='training':continue
        label='window-grid|'+d['role']+'|'+d['document_id']
        grids[d['document_id']]=window_grid(len(d['norm']),label);cursors[d['document_id']]=0
        d['grid_label']=label
    def next_window(doc,pool,whole_tokens=False):
        did=doc['document_id'];grid=grids[did]
        while cursors[did]<len(grid):
            start=grid[cursors[did]];cursors[did]+=1;key=doc['norm'][start:start+97]
            why=None;off=letter_offsets(doc);begin=off[start];end=off[start+96]+1
            if whole_tokens:
                isletter=lambda b:65<=b<=90 or 97<=b<=122
                if (begin and isletter(doc['raw'][begin-1])) or (end<len(doc['raw']) and isletter(doc['raw'][end])):why={'reason':'not_whole_ASCII_token_boundaries'}
            if why is None and key in seen:why={'reason':'duplicate_97_window'}
            if why is None:why=overlap_reason(key,doc,docs)
            if why:
                rejected.append({'document_id':did,'start':start,'pool':pool,**why});continue
            if doc['role']=='novel_control' and any(key in d['norm'] for d in docs if d['role']!='novel_control'):raise AssertionError('Novel key source match')
            entry={'id':f'{pool}{1+sum(w["pool"]==pool for w in selected):03}','pool':pool,'document_id':did,'role':doc['role'],
                   'normalized_start':start,'normalized_end':start+97,'raw_start':begin,'raw_end':end,
                   'raw_excerpt':doc['raw'][begin:end].decode('utf8',errors='replace'),'key':key.decode(),'key_sha256':hashlib.sha256(key).hexdigest(),
                   'grid_rng_label':doc['grid_label'],'whole_ASCII_token_boundaries':whole_tokens}
            if whole_tokens:
                tokens=[p.normalize(t).decode() for t in re.findall(b'[A-Za-z]+',doc['raw'][begin:end])]
                assert ''.join(tokens)==key.decode();entry['source_tokens']=tokens
            seen.add(key);selected.append(entry);return entry
        return None
    for d in sorted((d for d in docs if d['role']=='calibration'),key=lambda d:d['document_id']):
        for _ in range(64 if d['document_id'].startswith('gutenberg/') else 4):
            if next_window(d,'CAL') is None:break
    def fill(role,pool,count,whole=False):
        sources=sorted((d for d in docs if d['role']==role),key=lambda d:d['document_id']);n=0
        while n<count:
            progressed=False
            for d in sources:
                if n==count:break
                if next_window(d,pool,whole) is not None:n+=1;progressed=True
            if not progressed:raise ValueError(f'Insufficient eligible {pool} windows: {n}/{count}; no scoring permitted')
    fill('published_prose_control','PROSE',48)
    fill('published_prose_control','STRESS',12,True)
    fill('hard_style_control','HARD',24)
    for d in sorted((d for d in docs if d['role']=='novel_control'),key=lambda d:d['document_id']):
        if next_window(d,'NOVEL') is None:raise ValueError('No eligible novel window '+d['document_id'])
    record={'source_plan_sha256':p.sha256_file(ROOT/'CONTROL_SOURCE_PLAN.json'),'novel_documents_sha256':p.sha256_file(ROOT/'controls/novel_key_documents.json'),
            'selection_order':['CAL sorted documents per-doc caps','PROSE48 round-robin','STRESS12 round-robin continuing same document grids','HARD24 round-robin','NOVEL one per sorted document'],
            'windows':selected,'rejected':rejected,'pool_counts':dict(Counter(w['pool'] for w in selected)),
            'no_language_or_cryptographic_scores_used':True,'grid_cursors':cursors,
            'cross_role_overlap_rule':'Every proposed97window: all50 contiguous48substrings checked against full normalized other-role documents; first failure recorded.'}
    p.write_json(ROOT/'windows.json',record);return record

def make_controls():
    bank=p.validate_bank(p.load_json(ROOT/'bank.json'));prior=p.load_json(ROOT/'prior051_bank.json')
    if p.sha256_file(ROOT/'bank.json')!='e929b4c5a93bab76195dd9d16556aa1def8db530a987f9bdf3dc6861c28b11e7':raise ValueError('Original052 bank changed')
    pool={k:[] for k in ('CAL','PROSE','STRESS','HARD','NOVEL')}
    for w in p.load_json(ROOT/'windows.json')['windows']:pool[w['pool']].append(w)
    groups={g:[r for r in bank if r['group']==g] for g in p.GROUPS_BANK}
    schedule=[r for row in zip(*(groups[g] for g in p.GROUPS_BANK)) for r in row]
    absent=sorted(prior,key=lambda r:hashlib.sha256(('candidate-first-053-absent|'+r['text']).encode()).digest())[:12]
    if any(r['text'] in {r['text'] for r in bank} for r in absent):raise ValueError('Absent plaintext present')
    controls=[]
    def add(kind,ti,key,record,source=None,construction=None,paired=None):
        t=p.TABLEAUX[ti];cid=f'C{len(controls)+1:03}';cipher=p.encrypt_key(record['text'],key,t)
        if p.derive_key(record['text'],cipher,t)!=key or p.decrypt_key(cipher,key,t)!=record['text']:raise AssertionError('Control crypto')
        controls.append({'id':cid,'kind':kind,'tableau_index_zero_based':ti,'tableau_id':t.id,'key':key,'plaintext_id':record['id'],
                         'plaintext_group':record.get('group','prior051'),'plaintext':record['text'],'ciphertext':cipher,
                         'source_window_id':source['id'] if source else None,'source_document':source['document_id'] if source else None,
                         'construction_rng_label':construction,'paired_control_id':paired,'calibration_rng_label':cid+'|calibration','validation_rng_label':cid+'|validation'})
    for kind,count,pk in [('published_prose',36,'PROSE'),('hard_style',24,'HARD'),('novel_prose',12,'NOVEL')]:
        for k in range(count):
            ti=k//(count//12);w=pool[pk][k];add(kind,ti,w['key'],schedule[(17*len(controls))%1024],w)
    for k in range(24):
        ti=k//2;label='uniform-key|'+str(k);rng=p.rng_for(label);key=''.join(rng.choice(p.AZ) for _ in range(97))
        add('uniform_key',ti,key,schedule[(17*len(controls))%1024],construction=label)
    for ti in range(12):
        for j in range(2):
            original=controls[3*ti+j];label='letter-permutation|'+original['id'];values=list(original['key']);p.rng_for(label).shuffle(values)
            rec=next(r for r in bank if r['id']==original['plaintext_id'])
            add('letter_permuted',ti,''.join(values),rec,pool['PROSE'][3*ti+j],label,original['id'])
    for ti in range(12):
        w=pool['PROSE'][36+ti];add('plaintext_absent',ti,w['key'],absent[ti],w)
    for ti in range(12):
        w=pool['STRESS'][ti];tokens=list(w['source_tokens']);label='word-token-permutation|'+w['id'];rng=p.rng_for(label)
        for attempt in range(100):
            rng.shuffle(tokens);key=''.join(tokens)
            if key!=w['key']:break
        else:raise ValueError('Identity token stress')
        if len(key)!=97 or Counter(key)!=Counter(w['key']):raise AssertionError('Token conservation')
        add('word_order_stress',ti,key,schedule[(17*(96+ti))%1024],w,label)
        controls[-1]['permuted_tokens']=tokens;controls[-1]['permutation_attempts']=attempt+1
    assert len(controls)==144
    p.write_json(ROOT/'controls.json',controls);return controls

def train_model():
    docs=load_documents();training=[d['norm'][:200000] for d in docs if d['role']=='training']
    model,counts=p.LanguageModel.train(training);(ROOT/'model').mkdir(exist_ok=True)
    model.save(ROOT/'model/log_tables.bin')
    for order,row in enumerate(counts,1):
        a=array('Q',row)
        import sys
        if sys.byteorder!='little':a.byteswap()
        with open(ROOT/f'model/counts{order}.bin','wb') as f:a.tofile(f)
    maxerror=0.
    for row in model.log_tables:
        for i in range(0,len(row),26):maxerror=max(maxerror,abs(sum(2**x for x in row[i:i+26])-1))
    calibration=[w for w in p.load_json(ROOT/'windows.json')['windows'] if w['pool']=='CAL']
    scored=[{'window_id':w['id'],'key_sha256':w['key_sha256'],'full_key_cross_entropy':model.full_cross_entropy(w['key'])} for w in calibration]
    values=sorted(r['full_key_cross_entropy'] for r in scored);rank=math.ceil(.99*len(values));ceiling=values[rank-1]
    receipt={'training_letters':sum(map(len,training)),'training_document_ids':[d['document_id'] for d in docs if d['role']=='training'],
             'order':4,'smoothing':[.5,5,10,20],'counts_format':'uint64 little-endian flat base26','log_format':'float64 little-endian flat base26 orders1..4',
             'files':{str(f.relative_to(ROOT)):p.sha256_file(f) for f in sorted((ROOT/'model').glob('*.bin'))},
             'maximum_probability_row_error':maxerror,'calibration_count':len(values),'ceiling_nearest_rank_one_based':rank,
             'full_key_cross_entropy_ceiling':ceiling,'calibration_scores':scored,'no_actual_bank_or_K4_scores':True}
    p.write_json(ROOT/'model/training_receipt.json',receipt);return receipt

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['windows','controls','train']);args=parser.parse_args();start=time.time()
    result={'windows':prepare_windows,'controls':make_controls,'train':train_model}[args.stage]()
    print(json.dumps({'stage':args.stage,'elapsed_seconds':time.time()-start,'counts':result.get('pool_counts') if isinstance(result,dict) else len(result)}))
