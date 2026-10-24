"""Uniform reversible source-context permutations; exact consistency, not fitted K4 keys."""
import collections,datetime,hashlib,itertools,json,math,time
from pathlib import Path
import spelling_correction as s
ROOT=Path(__file__).resolve().parents[1]
def contexts(alphabet,order):
 if not order:return ['']
 return ['^'*(order-n)+''.join(t) for n in range(order+1) for t in itertools.product(alphabet,repeat=n)]
def sites(ident,source,target,order,reverse=False):
 if len(source)!=len(target):raise ValueError('length change outside class')
 if reverse:source,target=source[::-1],target[::-1]
 history='^'*order
 for i,(a,b) in enumerate(zip(source,target)):
  yield dict(stream=ident,index_zero_based=len(source)-1-i if reverse else i,context=history[-order:] if order else '',source=a,target=b)
  history+=a

def infer(pairs,alphabet,order,reverse=False):
 tables={};seen={};inverse={};checks=0
 for ident,source,target in pairs:
  for x in sites(ident,source,target,order,reverse):
   checks+=1;c,a,b=x['context'],x['source'],x['target'];f=tables.setdefault(c,{});g=inverse.setdefault(c,{})
   if a in f and f[a]!=b:return dict(compatible=False,reason='same context/input needs different outputs',witness=[seen[(c,a)],x],processed_sites=checks)
   if b in g and g[b]!=a:return dict(compatible=False,reason='same context requires noninjective outputs',witness=[seen[(c,g[b])],x],processed_sites=checks)
   f[a]=b;g[b]=a;seen[(c,a)]=x
 prime=collections.Counter();log=0.0;unseen=0
 for c in contexts(alphabet,order):
  n=len(alphabet)-len(tables.get(c,{}));unseen+=n;log+=math.lgamma(n+1)/math.log(10)
  for v in range(2,n+1):
   p=2
   while p*p<=v:
    while v%p==0:prime[p]+=1;v//=p
    p+=1
   if v>1:prime[v]+=1
 return dict(compatible=True,tables=tables,processed_sites=checks,reachable_contexts=len(contexts(alphabet,order)),observed_contexts=len(tables),unfixed_context_input_entries=unseen,completion_prime_exponents=dict(sorted(prime.items())),log10_completion_count=log)

def apply(source,tables,order,reverse=False,inverse=False):
 value=source[::-1] if reverse else source;history='^'*order;out=[]
 for a in value:
  c=history[-order:] if order else '';f=tables[c];b=next(k for k,v in f.items() if v==a) if inverse else f[a];out.append(b);history+=b if inverse else a
 result=''.join(out);return result[::-1] if reverse else result

def predict(fit,pair,alphabet,order,reverse):
 if not fit['compatible']:return dict(training_compatible=False)
 correct=conflict=unfixed=0;fail=[]
 for x in sites(*pair,order,reverse):
  f=fit['tables'].get(x['context'],{});possible=[f[x['source']]] if x['source'] in f else [v for v in alphabet if v not in f.values()]
  if x['target'] not in possible:conflict+=1;fail.append(x)
  elif len(possible)==1:correct+=1
  else:unfixed+=1
 return dict(training_compatible=True,forced_correct_sites=correct,forced_conflicting_sites=conflict,unconstrained_sites=unfixed,first_conflicts=fail[:4])

def controls():
 abc='AB';cs=contexts(abc,1);tables=[{c:dict(zip(abc,p)) for c,p in zip(cs,ps)} for ps in itertools.product(list(itertools.permutations(abc)),repeat=len(cs))];cases=0;roundtrips=0
 for n in range(5):
  for a in map(''.join,itertools.product(abc,repeat=n)):
   for t in tables:
    b=apply(a,t,1);assert apply(b,t,1,inverse=True)==a;roundtrips+=1
   for b in map(''.join,itertools.product(abc,repeat=n)):
    fit=infer([('toy',a,b)],abc,1);truth={i for i,t in enumerate(tables) if apply(a,t,1)==b};got=set()
    if fit['compatible']:
     got={i for i,t in enumerate(tables) if all(t[c][x]==v for c,f in fit['tables'].items() for x,v in f.items())}
     count=math.prod(int(p)**e for p,e in fit['completion_prime_exponents'].items());assert count==len(got)
    assert got==truth;cases+=1
 return dict(complete_binary_table_relations=cases,all_binary_table_roundtrips=roundtrips,enumerated_reachable_tables=len(tables))
def run():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic();ctrl=controls();texts=s.full_sources(json.loads((ROOT/'data/controls.json').read_text()));rows=[]
 for role in ('normal_to_literal','literal_to_normal'):
  pairs=[(t['id'],t['normalized_comparison'],t['normalized_literal']) for t in texts[:2]]
  if role=='literal_to_normal':pairs=[(i,b,a) for i,a,b in pairs]
  for order in (0,1,2):
   for reverse in (False,True):
    fit=infer(pairs,s.AZ,order,reverse);held=[]
    for j in (0,1):
     trained=infer([pairs[j]],s.AZ,order,reverse);held.append(dict(train=pairs[j][0],test=pairs[1-j][0],training=trained,prediction=predict(trained,pairs[1-j],s.AZ,order,reverse)))
    rows.append(dict(role=role,source_memory=order,scan_direction='right_to_left' if reverse else 'left_to_right',fit=fit,cross_stream_holdouts=held))
 return dict(id='CONTEXT-SPELLING-039',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,controls=ctrl,model_descriptions=12,new_contextual_descriptions=8,rows=rows,compatible_descriptions=sum(x['fit']['compatible'] for x in rows),source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('research/CONTEXT-SPELLING-039-SPEC.md','experiments/context_spelling_039.py','data/controls.json')},K3_full_length_change_not_admitted=True,K4_trials=0,puzzle_solved=False,pushed=False)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('started_at_utc','finished_at_utc','controls','compatible_descriptions')}));print([(x['role'],x['source_memory'],x['scan_direction'],x['fit']['compatible']) for x in r['rows']])
