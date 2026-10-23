"""Independent physical-contact simulator and full raw-state truth enumeration.
No imports from the production constraint implementation.
"""
import hashlib,itertools,json
from pathlib import Path

def wire(w,p,x,back=False):
    n=len(w)
    return ((w.index((x+p)%n) if back else w[(x+p)%n])-p)%n

def tick_control(pos,q,notch):
    f=len(pos)//2;m=f+1;s=f-1;old=pos[:]
    pos[f]=(old[f]-1)%q
    if old[f]==notch:
        pos[m]=(old[m]-1)%q
        if old[m]==notch:pos[s]=(old[s]-1)%q

def physical_mask(f,control,index):
    chosen=set()
    for signal in f['pulses']:
        for j in range(f['r']-1,-1,-1):signal=wire(f['control'][j],control[j],signal,True)
        signal=f['collector'][signal]
        for j in range(2):signal=wire(f['index'][j],index[j],signal)
        chosen.add(signal%f['r'])
    return chosen

def simulate(f,plain,control,index,cipher,decrypt=False):
    control=list(control);positions=list(cipher);out=[]
    for value in plain:
        for j in (range(f['r']-1,-1,-1) if decrypt else range(f['r'])):value=wire(f['cipher'][j],positions[j],value,decrypt)
        out.append(value);mask=physical_mask(f,control,index)
        for j in mask:positions[j]=(positions[j]-1)%f['q']
        tick_control(control,f['q'],f['notch'])
    return out

def schedule(f,control,index,length):
    control=list(control);delta=[0]*f['r'];out=[]
    for _ in range(length):
        out.append(tuple(delta));mask=physical_mask(f,control,index)
        for j in mask:delta[j]=(delta[j]-1)%f['q']
        tick_control(control,f['q'],f['notch'])
    return out

def truth(f,observations,path,guard,limit_error,cap=2000000,bytecap=256<<20):
    q,r=f['q'],f['r'];length=max((x[0] for x in observations),default=-1)+1;count=0;size=0;controllers=0;pairs=0;seeds=0;dig=hashlib.sha256()
    with Path(path).open('wb') as out:
        for control in itertools.product(range(q),repeat=r):
            for index in itertools.product(range(2*r),repeat=2):
                delta=schedule(f,control,index,length);pairs+=1
                for seed in itertools.product(range(q),repeat=r):
                    try:guard()
                    except limit_error as error:
                        error.partial_truth=dict(completed=False,control_starts_completed=controllers,controller_index_pairs_started=pairs,cipher_seeds_checked=seeds,found_raw_keys_lower_bound=str(count),bytes=size);raise
                    seeds+=1;ok=True
                    for t,p,c in observations:
                        x=p
                        for j in range(r):x=wire(f['cipher'][j],(seed[j]+delta[t][j])%q,x)
                        if x!=c:ok=False;break
                    if not ok:continue
                    raw=json.dumps(list(control)+list(index)+list(seed),separators=(',',':')).encode()+b'\n';count+=1;size+=len(raw)
                    if count>cap or size>bytecap:
                        error=limit_error('output_budget_unresolved');error.partial_truth=dict(completed=False,control_starts_completed=controllers,controller_index_pairs_started=pairs,cipher_seeds_checked=seeds,found_raw_keys_lower_bound=str(count-1),bytes=size-len(raw));raise error
                    out.write(raw);dig.update(raw)
            controllers+=1
    return dict(completed=True,raw_key_count=str(count),bytes=size,sha256=dig.hexdigest(),control_starts_completed=controllers)
