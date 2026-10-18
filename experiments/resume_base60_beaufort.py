"""Checkpoint continuation of the unchanged exact BASE60-BEAUFORT-001 model."""
import argparse
import collections
import datetime
import hashlib
import heapq
import json
import os
from pathlib import Path
import platform
import tempfile
import time
from base60_beaufort import ROOT, baseline, graph_model, solve, stream

OLD_HASH='9bc9019856d56fce0adb988de2d47859478a68100aeab2b8f97b75641078ab36'
OUTPUT=ROOT/'results/BASE60-BEAUFORT-CONTINUATION-001.json'

def rank_value(rank,mask):
    digits=[0]*len(mask)
    for i in range(len(mask)-1,-1,-1):digits[i]=rank%30;rank//=30
    primer=tuple(2*d+b for d,b in zip(digits,mask));code=0
    for d in primer:code=60*code+d
    return code,primer

def class_start_rank(mask,start_code):
    lo,hi=0,30**len(mask)
    while lo<hi:
        mid=(lo+hi)//2
        if rank_value(mid,mask)[0]<start_code:lo=mid+1
        else:hi=mid
    return lo

def remaining_iterator(proof,start_code):
    def one(mask):
        for rank in range(class_start_rank(mask,start_code),30**len(mask)):
            yield rank_value(rank,mask)
    return heapq.merge(*(one(m['primer_parity']) for m in proof['parity_masks'] if m['compatible']))

class Peek:
    def __init__(self,it):self.it=iter(it);self.pending=None;self.exhausted=False
    def peek(self):
        if self.pending is None and not self.exhausted:
            try:self.pending=next(self.it)
            except StopIteration:self.exhausted=True
        return self.pending
    def pop(self):
        value=self.peek();self.pending=None
        if value is None:raise StopIteration
        return value

def atomic_save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix=path.name+'.',suffix='.tmp',dir=str(path.parent))
    try:
        with os.fdopen(fd,'w') as f:json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)

def run(spec_commit,code_commit):
    source=ROOT/'results/BASE60-BEAUFORT-001.json';raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=OLD_HASH:raise ValueError('original checkpoint hash mismatch')
    old=json.loads(raw);vertices,positions,pairs=baseline();model=graph_model(vertices,pairs)
    assert len(model)==1 and len(model[0]['nodes'])==21
    for name,h in old['file_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('old input/code changed: '+name)
    files=['experiments/resume_base60_beaufort.py','tests/test_base60_resume.py','research/specifications/BASE60-BEAUFORT-CONTINUATION-001.json']
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    if OUTPUT.exists():
        result=json.loads(OUTPUT.read_text())
        assert result['original_checkpoint_sha256']==OLD_HASH
        assert result['spec_commit']==spec_commit and result['code_commit']==code_commit and result['file_sha256']==hashes
        if result['status']=='complete':raise ValueError('already complete; no repetition allowed')
    else:
        configs=json.loads(json.dumps(old['configurations']))
        result={'experiment':'BASE60-BEAUFORT-CONTINUATION-001','status':'in_progress','spec_commit':spec_commit,'code_commit':code_commit,'original_checkpoint_sha256':OLD_HASH,'python':platform.python_version(),'file_sha256':hashes,'nominal_labeled_tuples':old['nominal_labeled_tuples'],'unique_tuples':old['unique_tuples'],'initial_evaluated_after_parity':100000,'new_evaluated':0,'configurations':configs,'chunks':[],'complete_alphabet_witnesses':list(old['complete_alphabet_witnesses']),'unresolved':list(old['unresolved']),'elapsed_seconds':0.0,'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'limits':{'aggregate_seconds':120,'chunk_seconds':5,'max_new_candidates':3140000,'chunk_candidates':50000,'processes':1},'model':'Original two mod60 recurrences, L2-4, direct shared unknown alphabet trueBeaufort; no scope change.'}
    previous_elapsed=result['elapsed_seconds'];begun=time.monotonic()
    iterators={j:Peek(remaining_iterator(p,c['next_original_code'])) for j,(p,c) in enumerate(zip(old['parity_proofs'],result['configurations'])) if not c['complete']}
    atomic_save(OUTPUT,result)
    while any(not c['complete'] for c in result['configurations']):
        progress=False
        for j,it in iterators.items():
            c=result['configurations'][j]
            if c['complete']:continue
            if previous_elapsed+time.monotonic()-begun>=120 or result['new_evaluated']>=3140000:break
            start=time.monotonic();n=0;first=None;hist=collections.Counter();global_start=c['evaluated']
            while n<50000 and time.monotonic()-start<5 and previous_elapsed+time.monotonic()-begun<120 and result['new_evaluated']<3140000:
                item=it.peek()
                if item is None:c['complete']=True;break
                code,primer=it.pop()
                assert c['last_original_code'] is None or code>c['last_original_code']
                if first is None:first=code
                d=stream(primer,c['rule']);labels=[d[i]%26 for i in positions]
                if d[32]%2 or d[73]%2 or (d[27]-d[65])%26:
                    answer={'status':'local_sum_or_injectivity_contradiction','reason':'self_loop_parity_or_duplicate_edge'}
                else:answer=solve(vertices,pairs,labels,model=model)
                status=answer['status'];hist[status]+=1;n+=1;c['evaluated']+=1;result['new_evaluated']+=1;c['last_original_code']=code;progress=True
                if status=='complete_global_alphabet_feasible':result['complete_alphabet_witnesses'].append({'lag':c['lag'],'rule':c['rule'],'code':code,'primer':list(primer),**answer})
                if status=='unresolved_resource_cap':result['unresolved'].append({'lag':c['lag'],'rule':c['rule'],'code':code})
            item=it.peek();c['next_original_code']=None if item is None else item[0];c['complete']=item is None
            for key,v in hist.items():c['classifications'][key]=c['classifications'].get(key,0)+v
            if n:result['chunks'].append({'lag':c['lag'],'rule':c['rule'],'new_evaluated':n,'first_original_code':first,'last_original_code':c['last_original_code'],'next_original_code':c['next_original_code'],'eligible_rank_start_zero_based':global_start,'eligible_rank_end_exclusive':c['evaluated'],'classifications':dict(hist),'elapsed_seconds':round(time.monotonic()-start,6)})
            result['elapsed_seconds']=round(previous_elapsed+time.monotonic()-begun,6)
            result['remaining_unevaluated']=sum(c['remaining_after_parity']-c['evaluated'] for c in result['configurations'])
            atomic_save(OUTPUT,result)
        if not progress or previous_elapsed+time.monotonic()-begun>=120 or result['new_evaluated']>=3140000:break
    result['elapsed_seconds']=round(previous_elapsed+time.monotonic()-begun,6)
    result['remaining_unevaluated']=sum(c['remaining_after_parity']-c['evaluated'] for c in result['configurations'])
    result['status']='complete' if all(c['complete'] for c in result['configurations']) and not result['unresolved'] else 'verified_partial'
    result['stop_reason']='all_iterators_exhausted' if not result['remaining_unevaluated'] else 'declared_budget_cap'
    result['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    atomic_save(OUTPUT,result)
    print(json.dumps({'status':result['status'],'new_evaluated':result['new_evaluated'],'remaining':result['remaining_unevaluated'],'elapsed_seconds':result['elapsed_seconds'],'chunks':len(result['chunks']),'feasible':len(result['complete_alphabet_witnesses']),'unresolved':len(result['unresolved'])}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--spec-commit',required=True);p.add_argument('--code-commit',required=True);a=p.parse_args();run(a.spec_commit,a.code_commit)
