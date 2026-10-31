"""Fresh synthetic oracle and metadata tests; no ciphertext arithmetic."""
import importlib.util,itertools,json,copy,hashlib,tempfile,subprocess,sys
from pathlib import Path
code=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/shared/k4-negative-index/checker.py')
spec=importlib.util.spec_from_file_location('checked',code); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def partitions(n):
 if n==1: yield [0];return
 for p in partitions(n-1):
  for x in range(max(p)+2):yield p+[x]
def vectors(p):
 return {tuple(v[k] for k in p) for v in itertools.product((0,1),repeat=max(p)+1)}
comparisons=0
for n in range(1,6):
 ps=list(partitions(n));truth={tuple(p):vectors(p) for p in ps}
 for a in ps:
  for b in ps:
   expected=truth[tuple(b)] <= truth[tuple(a)]
   assert m.contains(a,b)==expected,(a,b)
   assert m.contains([17+3*x for x in a],[99+2*x for x in b])==expected
   comparisons+=2
context={'equation':'C=P+K','q':3,'sigma':1,'tau':1,'coordinates':[0,1,2,3],'plaintext_alphabet':'ABC','ciphertext_alphabet':'ABC','key_alphabet':'ABC','data_sha256':'fresh-synthetic','normalization':'identity','alignment':'same'}
index={'context':context,'records':[{'id':'synthetic-negative','receipt_pointer':'/synthetic/0','status':'completed_exact_negative','key_domain':'unrestricted_mod_q','partition':[0,0,1,1]}]}
request={'context':copy.deepcopy(context),'partition':[0,0,0,0],'domain':{'kind':'unrestricted_mod_q'}}
assert m.check_request(index,request)['decision']=='inherited_negative'
checks=1
def reject(req):
 global checks
 try:m.check_request(index,req)
 except (ValueError,TypeError):checks+=1;return
 raise AssertionError(('accepted malformed request',req))
for key,val in [('equation','C=P-K'),('q',2),('sigma',-1),('tau',-1),('plaintext_alphabet','BAC'),('ciphertext_alphabet','BAC'),('key_alphabet','BAC'),('data_sha256','other'),('normalization','strip'),('alignment','shift'),('coordinates',[1,2,3,4]),('coordinates',[0,1,1,3]),('coordinates',[0,1,2]),('q',True),('q',3.0)]:
 r=copy.deepcopy(request);r['context'][key]=val;reject(r)
for p in [[],[0,0,0], [0,0,0,0,0],[0,False,0,0],[0,1.0,0,0],[0,-1,0,0],[0,'0',0,0],None]:
 r=copy.deepcopy(request);r['partition']=p;reject(r)
for domain in [{'kind':'primitive'},{'kind':'subset','assertion':True},{'kind':'per_class_values','allowed_values':[[0,3]]},{'kind':'per_class_values','allowed_values':[[True]]},{'kind':'per_class_values','allowed_values':[[]]},{'kind':'per_class_values','allowed_values':[[0],[1]]},{'kind':'per_class_values','allowed_values':[[0,0]]}]:
 r=copy.deepcopy(request);r['domain']=domain;reject(r)
r=copy.deepcopy(request);r['domain']={'kind':'per_class_values','allowed_values':[[0,2]]};assert m.check_request(index,r)['decision']=='inherited_negative';checks+=1
for status in ['skipped','heuristic','unknown','incomplete','compatible','ineligible']:
 idx=copy.deepcopy(index);idx['records'][0]['status']=status;assert m.check_request(idx,request)['decision']=='no_certificate';checks+=1
idx=copy.deepcopy(index);idx['records'][0]['key_domain']='restricted';assert m.check_request(idx,request)['decision']=='no_certificate';checks+=1
# Reversed containment: weak candidate does NOT inherit stronger old negative.
r=copy.deepcopy(request);r['partition']=[0,1,2,3];assert m.check_request(index,r)['decision']=='no_certificate';checks+=1
# A free-key containing model without completed negative never excludes anything.
idx=copy.deepcopy(index);idx['records'][0].update(partition=[0,1,2,3],status='ineligible');assert m.check_request(idx,request)['decision']=='no_certificate';checks+=1
# Corrupt-byte and missing artifact failures use only synthetic files.
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'evidence';p.write_bytes(b'fresh synthetic proof receipt')
 good=hashlib.sha256(p.read_bytes()).hexdigest();assert m.checked_bytes(td,'evidence',good)==p.read_bytes();checks+=1
 for file,h in [('evidence','0'*64),('missing',good)]:
  try:m.checked_bytes(td,file,h)
  except (ValueError,OSError):checks+=1
  else:raise AssertionError('invalid evidence accepted')
for raw in ['{"q":3,"q":2}', '{"outer":{"x":1,"x":2}}', '{"x":NaN}', '{"x":Infinity}']:
 try:m.load_json(raw)
 except ValueError:checks+=1
 else:raise AssertionError('ambiguous/nonfinite JSON accepted')
print(json.dumps({'classification':'fresh synthetic','partition_oracle_comparisons':comparisons,'metadata_and_evidence_checks':checks,'checker_sha256':hashlib.sha256(code.read_bytes()).hexdigest(),'result':'PASS','historical_target_replays':0,'target_arithmetic':False},indent=2))
