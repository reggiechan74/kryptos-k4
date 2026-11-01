"""Blind full31 workload adapter; inherited algebra/order, no truth or mask API.

Source preparation only. Real invocation requires the separately approved freeze.
"""
from dataclasses import dataclass, asdict
from itertools import combinations, product
import hashlib
import json
import math
import os
from pathlib import Path

VERSION='fresh-residual-workload-evidence-v2'
MIB=1024*1024

class PreflightError(ValueError): pass
class PreflightLimit(RuntimeError): pass

def require(ok, message):
    if not ok: raise PreflightError(message)

def canonical(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def input_hash(control): return hashlib.sha256(canonical(control)).hexdigest()

@dataclass(frozen=True)
class Caps:
    max_supports:int=4495
    max_generation_beta_candidates:int=35264
    max_audit_beta_candidates:int=35264
    max_generation_parity_row_tests:int=846336
    max_audit_parity_row_tests:int=846336
    max_fiber_points:int=0
    max_lift_trials:int=0
    max_solve_calls:int=4495
    max_certificate_checks:int=8990
    max_row_operations:int=1500000
    max_work_units:int=50000000
    max_witness_checks:int=0
    max_output_records:int=2000000
    max_file_bytes:int=33554432
    max_total_bytes:int=33554432
    max_line_bytes:int=65536
    point_cap:int=1000000
    max_seconds:float=60.0

def validate_caps(caps):
    require(type(caps) is Caps,'exact Caps required')
    for key in Caps.__dataclass_fields__:
        value=getattr(caps,key)
        if key=='max_seconds':
            require((type(value) is int and value>=0) or (type(value) is float and math.isfinite(value) and value>=0),'finite wall cap')
        else:
            require(type(value) is int and value>=0,'built-in nonnegative int cap: '+key)

class Meter:
    def __init__(self,caps,reference):
        validate_caps(caps)
        self.caps=caps
        self.ref=reference.Meter(reference.BudgetV3(**{k:v for k,v in asdict(caps).items() if k in reference.BudgetV3.__dataclass_fields__}))
        self.counts={k:0 for k in ('supports','generation_beta_candidates','audit_beta_candidates','generation_parity_row_tests','audit_parity_row_tests')}
    def charge(self,name,amount=1):
        require(name in self.counts and type(amount) is int and amount>=0,'preflight charge')
        if amount>getattr(self.caps,'max_'+name)-self.counts[name]: raise PreflightLimit(name+' cap')
        self.ref.work(amount)
        self.counts[name]+=amount
    def work(self,n=1): self.ref.work(n)
    def record(self,n=1): self.ref.charge('output_records',n)
    def receipt(self): return dict(self.ref.receipt(),**self.counts)

def validate_control(control,meter):
    require(type(control) is dict and set(control)=={'id','contexts','observed','sparsity','allowed_features'},'blind solver-only schema')
    identity=control['id']
    require(type(identity) is str and identity in ('G0','G1')+tuple('v%03d'%i for i in range(12)),'case id')
    require(type(control['sparsity']) is int and control['sparsity']==3,'fixed sparsity')
    allowed=control['allowed_features']
    require(type(allowed) is list and all(type(j) is int for j in allowed) and allowed==list(range(31)),'fixed full31')
    contexts=control['contexts']; observed=control['observed']
    is_gate=identity in ('G0','G1')
    require(type(contexts) is list and len(contexts)==(1 if is_gate else 91),'context count')
    for x in contexts:
        meter.work(7)
        require(type(x) is list and len(x)==6 and all(type(v) is int and 0<=v<26 for v in x),'context residues')
    require(type(observed) is list and len(observed)==(0 if identity=='G0' else 1 if identity=='G1' else 24),'observed count')
    last=-1
    for pair in observed:
        meter.work(3)
        require(type(pair) is list and len(pair)==2,'observation pair')
        i,y=pair
        require(type(i) is int and last<i<len(contexts) and type(y) is int and 0<=y<26,'observation values/order')
        last=i
    if is_gate:
        require(contexts==[[0]*6] and observed==([] if identity=='G0' else [[0,0]]),'literal gate control')
    else:
        require([pair[0] for pair in observed]==list(range(15,28))+list(range(57,68)),'public observation positions')
        for previous,current in zip(contexts,contexts[1:]):
            meter.work(5)
            require(current[1:]==previous[:5],'contiguous six-lag windows')

def features(context,meter):
    meter.work(32)
    return [1]+context+[x*x%26 for x in context]+[context[i]*context[j]%26 for i,j in combinations(range(6),2)]+[int(context[i]==context[i+1]) for i in (0,2,4)]

def group(j): return j if j<7 else j-6

def binding(control,support,digest,reference):
    return {'role':'fresh-residual-workload-v2','field':13,'n':3,'input_sha256':digest,'support':list(support),'case_id':control['id'],'reference_version':reference.VERSION}

def generated_betas(rows,observed,groups,meter):
    result=[]
    for bits in product((0,1),repeat=len(groups)):
        meter.charge('generation_beta_candidates')
        active=[g for g,b in zip(groups,bits) if b]
        compatible=True
        for i,y in observed:
            meter.charge('generation_parity_row_tests')
            meter.work(max(1,len(active)))
            parity=sum(rows[i][g if g<7 else g+6] for g in active)%2
            if parity!=y%2: compatible=False
        meter.work(len(active)+1)
        if compatible and any(g not in (0,1) for g in active):
            meter.record(1+len(active));result.append(active)
    return result

def reserve_bytes(file_bytes,total_bytes,next_bytes,caps):
    validate_caps(caps)
    require(all(type(n) is int and n>=0 for n in (file_bytes,total_bytes,next_bytes)),'byte counter types')
    if next_bytes>caps.max_line_bytes or next_bytes>caps.max_file_bytes-file_bytes or next_bytes>caps.max_total_bytes-total_bytes:
        raise PreflightLimit('certificate byte cap')
    return file_bytes+next_bytes,total_bytes+next_bytes

class EvidenceBudget:
    """One fixed case path per slot; partial bytes are never refunded."""
    def __init__(self): self.bytes=0;self.files=0

class Evidence:
    def __init__(self,path,meter,budget,checker):
        self.checker=checker
        self.path=Path(path);self.meter=meter;self.budget=budget;self.bytes=0;self.digest=hashlib.sha256();self.complete=False
        require(self.path.name=='case.cert.jsonl','evidence path')
        require(budget.files<1,'one certificate file only')
        self.handle=self.path.open('x+b');budget.files+=1
    def append(self,obj,include_hash=True):
        self.meter.work((self.meter.caps.max_line_bytes+63)//64);self.meter.record()
        data=canonical(obj);n=len(data)
        # Predebit before touching storage, with no refund even on a short write.
        self.bytes,self.budget.bytes=reserve_bytes(self.bytes,self.budget.bytes,n,self.meter.caps)
        start=self.handle.tell()
        wrote=self.handle.write(data)
        require(wrote==n,'short evidence write')
        self.handle.flush();os.fsync(self.handle.fileno())
        self.meter.work(max(1,(n+63)//64))
        self.handle.seek(start);reread=self.handle.read(n);require(reread==data,'durable evidence readback')
        if include_hash:self.digest.update(data)
        return reread
    def finish(self):
        self.handle.flush();os.fsync(self.handle.fileno())
        fd=os.open(self.path.parent,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
        self.complete=True
    def close(self):self.handle.close()
    def metadata(self):
        size=self.path.stat().st_size
        require(not self.path.is_symlink() and size==self.bytes and size<=self.meter.caps.max_file_bytes,
                'bounded unchanged certificate before hash')
        h=hashlib.sha256()
        total=0
        with self.path.open('rb') as f:
            while True:
                block=f.read(min(MIB,size-total+1))
                if not block:break
                require(len(block)<=size-total,'certificate grew during hash')
                total+=len(block)
                h.update(block)
        require(total==size and self.path.stat().st_size==size,'certificate changed size')
        return {'name':self.path.name,'bytes':size,'sha256':h.hexdigest(),'complete':self.complete}

def run(control,path,public_sha256,reference_sha256,freeze_sha256,reference,checker,evidence_budget,caps=Caps()):
    validate_caps(caps) # Prior to input, early return, file creation, or prefix path.
    meter=Meter(caps,reference);evidence=None;checked=0;lower=0
    result={'status':'PRECHECK_INCOMPLETE','checked_supports':0,'lower_bound':0,'exact_W':None,'certificate':None}
    try:
        validate_control(control,meter)
        meter.work(1024)
        digest=input_hash(control);rows=[features(x,meter) for x in control['contexts']]
        evidence=Evidence(path,meter,evidence_budget,checker)
        audit=checker.EvidenceChecker(control,public_sha256,reference_sha256,freeze_sha256,reference,meter,point_cap=caps.point_cap)
        header={'kind':'header','schema':VERSION,'case_id':control['id'],'input_sha256':digest,'public_sha256':public_sha256,'point_cap':caps.point_cap,'sparsity':3,'allowed_features':list(range(31)),'reference_sha256':reference_sha256,'freeze_sha256':freeze_sha256}
        audit.consume(evidence.append(header))
        status=None
        for index,support in enumerate(combinations(range(31),3)):
            meter.charge('supports');meter.work(1+4*len(control['observed']))
            equations=[[rows[i][j]%13 for j in support]+[y%13] for i,y in control['observed']]
            cert=reference.certify_affine(equations,3,meter=meter.ref,binding=binding(control,support,digest,reference))
            groups=sorted({group(j) for j in support})
            betas=generated_betas(rows,control['observed'],groups,meter)
            term=len(betas)*13**(3-cert['rank_a']) if cert['consistent'] else 0
            meter.work(4)
            record={'kind':'support','index':index,'support':list(support),'input_sha256':digest,'certificate':cert,'beta_groups':groups,'compatible_betas':betas,'term':term,'prefix_lower_bound':lower+term}
            stored=evidence.append(record)
            audited=audit.consume(stored)
            checked_term=audited['term']
            require(type(checked_term) is int and checked_term==term,'independent term disagreement')
            require(audited['checked_supports']==checked+1 and audited['lower_bound']==lower+checked_term,'independent prefix sum')
            checked+=1;lower+=checked_term
            if lower>caps.point_cap:
                status='GATE_REJECTED_LOWER_BOUND';break
        if status is None:
            require(checked==4495,'incomplete support inventory')
            status='WORKLOAD_ADMITTED'
        footer={'kind':'terminal','status':status,'support_count':checked,'lower_bound':lower,'exact_W':lower if status=='WORKLOAD_ADMITTED' else None,'content_sha256':evidence.digest.hexdigest()}
        audited=audit.consume(evidence.append(footer,False))
        require(audited['status']==status and audited['exact_W']==footer['exact_W'],'independent terminal')
        finished=audit.finish()
        require(finished['bytes']==evidence.bytes and finished['checked_supports']==checked,'independent completed evidence inventory')
        meter.work(0);evidence.finish()
        result.update(status=status,checked_supports=checked,lower_bound=lower,exact_W=footer['exact_W'])
    except (PreflightLimit,reference.ReferenceLimit) as exc:
        result.update(reason=str(exc),checked_supports=checked,lower_bound=lower)
    finally:
        if evidence is not None:
            evidence.close()
            try:
                meter.work(2*max(1,(evidence.path.stat().st_size+63)//64))
                result['certificate']=evidence.metadata()
                meter.work(0)
            except reference.ReferenceLimit as exc:
                result.update(status='PRECHECK_INCOMPLETE',exact_W=None,reason=str(exc),certificate_path=evidence.path.name)
        result['resources']=meter.receipt()
    return result
