"""Same frozen synthetic fixtures/budgets, translated predicates and exact validation."""
import argparse,filecmp,hashlib,json,subprocess,sys,tempfile,time
from pathlib import Path
import sigaba_joint_toy as solver
import sigaba_joint_toy_oracle as oracle
import sigaba_compact_oracle as compact
from sigaba_torus import TorusPredicates
from run_sigaba_joint_toy import CASES,member
ROOT=solver.ROOT;FIXTURE_SHA='2ad409cafff033932a79f4aa45e3f7ac557833e540b0902bef721da4f9d03b9a'

def canonical(result,f,path,budget,prefix=None):
    domains=solver.relation_masks(result);model=solver.Model(f)
    return compact.emit_rows(f,lambda control,index:domains.get((control,model.class_of[index]),0),path,budget.check,solver.Limit,prefix)

def case(which,output,seconds=600):
    source=(ROOT/'data/sigaba-joint-toy-v1.json').read_bytes();assert hashlib.sha256(source).hexdigest()==FIXTURE_SHA;f=json.loads(source)['cases'][which]['fixture'];q,r,v,mask,truth=CASES[which];assert f==solver.fixture(q,r,v,mask)
    plant=f['plant'];cipher=oracle.simulate(f,f['plaintext'],plant['control'],plant['index'],plant['cipher']);assert oracle.simulate(f,cipher,plant['control'],plant['index'],plant['cipher'],True)==f['plaintext'];obs=[(t,f['plaintext'][t],cipher[t]) for t in f['observed_positions']]
    if mask=='inconsistent':obs=[(2,f['plaintext'][2],cipher[2]),(2,f['plaintext'][2],(cipher[2]+1)%q)]
    budget=solver.Budget(seconds);holder={}
    def factory(m,b,c):holder['backend']=TorusPredicates(m,b,c);return holder['backend']
    result=solver.solve(f,obs,budget,predicate_factory=factory);out=dict(case=which,fixture_sha256=FIXTURE_SHA,fixture=f,synthetic_ciphertext=cipher,observations=obs,solver=result,backend_metrics=holder['backend'].metrics(),K4_evaluations=0,planted_full_roundtrip=True,verification_completed=False)
    out['planted_key_retained']=(member(result,f) if result['completed'] or member(result,f) else None) if mask!='inconsistent' else None
    if result['completed'] and mask!='inconsistent':assert out['planted_key_retained']
    if result['completed'] and mask=='inconsistent':assert result['exact_raw_key_count']=='0'
    if result['completed'] and mask=='empty':assert int(result['exact_raw_key_count'])==q**(2*r)*(2*r)**2
    try:
        if result['completed']:
            baseline=json.loads((ROOT/f'results/sigaba-joint-toy/case-{which:02d}.json').read_text())['solver'];prefix=baseline['control_starts_completed']
            with tempfile.TemporaryDirectory(prefix='k4-torus-') as td:
                td=Path(td);a=td/'new-canonical';z=td/'old-canonical';newrows=canonical(result,f,a,budget,prefix);oldrows=canonical(baseline,f,z,budget,prefix);equal=filecmp.cmp(a,z,shallow=False);assert equal
                out['baseline_comparison']=dict(scope='full' if baseline['completed'] else 'completed_controller_prefix',controllers=prefix,canonical_sets_byte_equal=equal,new_rows=newrows,old_rows=oldrows)
                if truth:
                    a=td/'new-raw';z=td/'truth-raw';out['expanded']=solver.write_keys(result,f,a,budget);out['independent_truth']=oracle.truth(f,obs,z,budget.check,solver.Limit);out['full_sets_byte_equal']=filecmp.cmp(a,z,shallow=False);assert out['full_sets_byte_equal'];assert str(out['expanded']['count'])==out['independent_truth']['raw_key_count']==result['exact_raw_key_count']
                elif which==10:
                    a=td/'new-all-canonical';z=td/'truth-all-canonical';out['canonical_complete']=canonical(result,f,a,budget);out['independent_compact_truth']=compact.truth_rows(f,obs,z,budget.check,solver.Limit);out['full_sets_canonical_byte_equal']=filecmp.cmp(a,z,shallow=False);assert out['full_sets_canonical_byte_equal'];assert out['canonical_complete']['raw_key_count']==out['independent_compact_truth']['raw_key_count']==result['exact_raw_key_count']
                else:
                    if int(result['exact_raw_key_count'])>2000000:raise solver.Limit('independent_key_validation_output_cap_unresolved')
                    checked=0;model=solver.Model(f)
                    for row in result['relations']:
                        for relation in row['relations']:
                            for h in solver.bits(int(relation['index_classes'],16)):
                                for index in model.aliases[h]:
                                    for cs in solver.bits(int(relation['cipher_starts'],16)):
                                        budget.check();seed=solver.unpack(cs,q,r);enc=oracle.simulate(f,f['plaintext'],row['control'],index,seed);assert all(enc[t]==c for t,_,c in obs);checked+=1
                    out['returned_raw_keys_independently_checked']=checked;assert checked==int(result['exact_raw_key_count'])
                out['verification_completed']=True
    except solver.Limit as error:out['verification_reason']=str(error);out['partial_independent_truth']=getattr(error,'partial_truth',None)
    out['benchmark_budget']=budget.receipt();out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'research/SIGABA-TORUS-SPEC.md',ROOT/'research/SIGABA-JOINT-TOY-SPEC.md',ROOT/'experiments/sigaba_joint_toy.py',ROOT/'experiments/sigaba_joint_toy_oracle.py',ROOT/'experiments/sigaba_torus.py',ROOT/'experiments/sigaba_compact_oracle.py',ROOT/'data/sigaba-joint-toy-v1.json')};Path(output).write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int);ap.add_argument('--output');ap.add_argument('--all',action='store_true');ap.add_argument('--directory',default='results/sigaba-torus');ap.add_argument('--seconds',type=float,default=600);a=ap.parse_args()
    if a.all:
        directory=Path(a.directory);directory.mkdir(parents=True,exist_ok=True)
        for i in range(len(CASES)):
            path=directory/f'case-{i:02d}.json';start=time.monotonic()
            try:result=subprocess.run([sys.executable,__file__,'--case',str(i),'--output',str(path),'--seconds',str(a.seconds)],timeout=a.seconds+5)
            except subprocess.TimeoutExpired:path.write_text(json.dumps(dict(case=i,status='watchdog_budget_unresolved',completed=False,seconds=time.monotonic()-start,K4_evaluations=0))+'\n');print(i,'watchdog_budget_unresolved',flush=True);continue
            if result.returncode:raise SystemExit(result.returncode)
            r=json.loads(path.read_text());print(i,'inference',r['solver']['completed'],'verification',r['verification_completed'],'keys',r['solver']['exact_raw_key_count'],'seconds',round(r['benchmark_budget']['seconds'],3),flush=True)
    elif a.case is not None and a.output:case(a.case,a.output,a.seconds)
    else:ap.error('Choose --all or --case N --output PATH')
