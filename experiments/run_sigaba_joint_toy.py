"""Separate-process coupled synthetic benchmarks, never actual K4 evaluation."""
import argparse,filecmp,hashlib,json,os,subprocess,sys,tempfile,time
from pathlib import Path
import sigaba_joint_toy as solver
import sigaba_joint_toy_oracle as oracle
ROOT=solver.ROOT
CASES=[(2,3,0,'short',True),(3,3,0,'short',True),(3,3,1,'long',True),(4,3,0,'long',True),(5,3,0,'long',True),(6,3,1,'long',True),(2,5,0,'long',True),(3,5,0,'long',True),(2,3,0,'empty',True),(2,3,0,'inconsistent',True),(4,5,0,'long',False),(6,5,0,'long',False),(8,5,0,'long',False)]

def member(result,f):
    plant=f['plant'];m=solver.Model(f);n=0
    for x in plant['cipher']:n=n*f['q']+x
    return bool(solver.relation_masks(result).get((tuple(plant['control']),m.class_of[tuple(plant['index'])]),0)>>n&1)

def case(which,output,seconds=600):
    q,r,v,mask,complete_truth=CASES[which];f=json.loads((ROOT/'data/sigaba-joint-toy-v1.json').read_text())['cases'][which]['fixture'];assert f==solver.fixture(q,r,v,mask);p=f['plant'];cipher=oracle.simulate(f,f['plaintext'],p['control'],p['index'],p['cipher']);assert oracle.simulate(f,cipher,p['control'],p['index'],p['cipher'],True)==f['plaintext'];obs=[(t,f['plaintext'][t],cipher[t]) for t in f['observed_positions']]
    if mask=='inconsistent':obs=[(2,f['plaintext'][2],cipher[2]),(2,f['plaintext'][2],(cipher[2]+1)%q)]
    b=solver.Budget(seconds);out=dict(case=which,fixture=f,synthetic_ciphertext=cipher,observations=obs,independent_truth_requested=complete_truth,K4_evaluations=0);result=solver.solve(f,obs,b);out['solver']=result;out['planted_full_roundtrip']=True;out['planted_key_retained']=(member(result,f) if result['completed'] or member(result,f) else None) if mask!='inconsistent' else None
    if result['completed'] and mask!='inconsistent':assert out['planted_key_retained']
    if result['completed'] and mask=='empty':assert int(result['exact_raw_key_count'])==q**(2*r)*(2*r)**2
    if result['completed'] and mask=='inconsistent':assert result['exact_raw_key_count']=='0'
    try:
        if result['completed']:
            with tempfile.TemporaryDirectory(prefix='k4-coupled-toy-') as td:
                a=Path(td)/'solver.jsonl';out['expanded']=solver.write_keys(result,f,a,b)
                if complete_truth:
                    z=Path(td)/'truth.jsonl';out['independent_truth']=oracle.truth(f,obs,z,b.check,solver.Limit);out['full_sets_byte_equal']=filecmp.cmp(a,z,shallow=False);assert out['full_sets_byte_equal'];assert out['expanded']['count']==int(out['independent_truth']['raw_key_count'])
                else:
                    checked=0
                    with a.open() as stream:
                        for line in stream:
                            b.check();row=json.loads(line);ctl=row[:r];ix=row[r:r+2];cs=row[r+2:];enc=oracle.simulate(f,f['plaintext'],ctl,ix,cs);assert all(enc[t]==c for t,_,c in obs);checked+=1
                    out['returned_raw_keys_independently_checked']=checked
    except solver.Limit as e:out['verification_completed']=False;out['verification_reason']=str(e);out['partial_independent_truth']=getattr(e,'partial_truth',None)
    else:out['verification_completed']=result['completed']
    out['benchmark_budget']=b.receipt();out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'research/SIGABA-JOINT-TOY-SPEC.md',Path(__file__),ROOT/'experiments/sigaba_joint_toy.py',ROOT/'experiments/sigaba_joint_toy_oracle.py',ROOT/'data/sigaba-joint-toy-v1.json')};Path(output).write_text(json.dumps(out,indent=2)+'\n')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int);ap.add_argument('--output');ap.add_argument('--all',action='store_true');ap.add_argument('--directory',default='results/sigaba-joint-toy');ap.add_argument('--seconds',type=float,default=600);a=ap.parse_args()
    if a.all:
        path=Path(a.directory);path.mkdir(parents=True,exist_ok=True)
        for i in range(len(CASES)):
            dest=path/f'case-{i:02d}.json';start=time.monotonic()
            try:r=subprocess.run([sys.executable,__file__,'--case',str(i),'--output',str(dest),'--seconds',str(a.seconds)],timeout=a.seconds+5)
            except subprocess.TimeoutExpired:dest.write_text(json.dumps(dict(case=i,status='watchdog_budget_unresolved',completed=False,seconds=time.monotonic()-start,K4_evaluations=0))+'\n');print(i,'watchdog_budget_unresolved',flush=True);continue
            if r.returncode:raise SystemExit(r.returncode)
            data=json.loads(dest.read_text());print(i,CASES[i],data['solver']['status'],data.get('full_sets_byte_equal'),data['solver']['exact_raw_key_count'],round(data['benchmark_budget']['seconds'],3),flush=True)
    elif a.case is not None and a.output:case(a.case,a.output,a.seconds)
    else:ap.error('choose --all or --case N --output PATH')
if __name__=='__main__':main()
