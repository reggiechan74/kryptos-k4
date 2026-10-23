"""Exact coupled table-constraint solver. Synthetic systems only; no K4 input."""
import collections,hashlib,itertools,json,resource,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def bits(x):
    while x:
        bit=x&-x;yield bit.bit_length()-1;x-=bit

def pop(x):return bin(x).count('1')
def unpack(x,q,r):
    out=[0]*r
    for i in range(r-1,-1,-1):x,out[i]=divmod(x,q)
    return tuple(out)
class Limit(Exception):pass
class Budget:
    def __init__(self,seconds=600,memory=1<<30):self.start=time.monotonic();self.seconds=seconds;self.memory=memory;self.calls=0;self.peak=0
    def check(self,force=False):
        self.calls+=1
        if not force and self.calls%128:return
        elapsed=time.monotonic()-self.start
        if elapsed>self.seconds:raise Limit('wall_budget_unresolved')
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);self.peak=max(self.peak,rss)
        if rss>self.memory:raise Limit('resident_memory_budget_unresolved')
    def receipt(self):
        self.peak=max(self.peak,resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024))
        return dict(seconds=time.monotonic()-self.start,peak_RSS_bytes=self.peak,wall_cap_seconds=self.seconds,RSS_cap_bytes=self.memory,guard='Measured RSS/wall checks, not an OS hard allocation limit')
class RNG:
    def __init__(self,seed):self.s=seed&0xffffffff
    def next(self,n):self.s=(1664525*self.s+1013904223)&0xffffffff;return self.s%n
    def perm(self,n):
        a=list(range(n))
        for i in range(n-1,0,-1):j=self.next(i+1);a[i],a[j]=a[j],a[i]
        return a

def fixture(q,r,variant=0,mask='long'):
    seed=(0x889012+q*1009+r*65537+variant*104729)&0xffffffff
    f=dict(q=q,r=r,index_size=2*r,variant=variant,wiring_seed=seed,collector=[x%(2*r) for x in range(q)],pulses=list(range(min(4,q))),notch=q//2)
    for bank,offset,count,n in (('cipher',0x123456, r,q),('control',0x789abc,r,q),('index',0x13579b,2,2*r)):
        rng=RNG(seed+offset);f[bank]=[rng.perm(n) for _ in range(count)]
    rng=RNG(seed+0x2468ac);f['plaintext']=[rng.next(q) for _ in range(97)];f['plant']=dict(control=[rng.next(q) for _ in range(r)],index=[rng.next(2*r) for _ in range(2)],cipher=[rng.next(q) for _ in range(r)])
    f['mask']=mask;f['observed_positions']=[] if mask=='empty' else ([2,3,6,9] if mask=='short' else list(range(21,34))+list(range(63,74)))
    return f

def tables(w):
    n=len(w);fw=[[(w[(x+p)%n]-p)%n for x in range(n)] for p in range(n)];bw=[[row.index(x) for x in range(n)] for row in fw];return fw,bw
class Model:
    def __init__(self,f):
        self.f=f;self.q=f['q'];self.r=f['r'];self.m=f['index_size'];self.cf=[tables(w)[0] for w in f['cipher']];self.cb=[tables(w)[1] for w in f['cipher']];self.ctrl=[tables(w)[1] for w in f['control']];self.ix=[tables(w)[0] for w in f['index']]
        groups={}
        for positions in itertools.product(range(self.m),repeat=2):
            h=tuple(self.ix[1][positions[1]][self.ix[0][positions[0]][x]]%self.r for x in range(self.m));groups.setdefault(h,[]).append(positions)
        self.maps=sorted(groups);self.aliases=[groups[h] for h in self.maps];self.class_of={p:i for i,rows in enumerate(self.aliases) for p in rows};self.mask_cache={}
    def digits(self,control,length):
        q,r=self.q,self.r;positions=list(control);out=[];fast=r//2;medium=fast+1;slow=fast-1
        for _ in range(length):
            hits=[]
            for x in self.f['pulses']:
                for j in range(r-1,-1,-1):x=self.ctrl[j][positions[j]][x]
                hits.append(self.f['collector'][x])
            out.append(tuple(sorted(set(hits))))
            if positions[fast]==self.f['notch']:
                if positions[medium]==self.f['notch']:positions[slow]=(positions[slow]-1)%q
                positions[medium]=(positions[medium]-1)%q
            positions[fast]=(positions[fast]-1)%q
        return out
    def mask_groups(self,digits):
        if digits not in self.mask_cache:
            groups={}
            for h,map_ in enumerate(self.maps):
                mask=0
                for d in digits:mask|=1<<map_[d]
                groups[mask]=groups.get(mask,0)|(1<<h)
            self.mask_cache[digits]=list(sorted(groups.items()))
        return self.mask_cache[digits]

class Predicates:
    def __init__(self,model,budget,cap=64<<20):
        self.m=model;self.b=budget;self.cap=cap;self.cache=collections.OrderedDict();self.cache_bytes=0;self.peak_bytes=0;self.hits=0;self.builds=0;self.evictions=0;self.entries_bytes=(model.q**model.r+7)//8+256
    def get(self,delta,p,c):
        key=(delta,p,c)
        if key in self.cache:self.hits+=1;self.cache.move_to_end(key);return self.cache[key]
        m=self.m;q,r=m.q,m.r;k=r//2;left={};tail=q**(r-k)
        for i,seed in enumerate(itertools.product(range(q),repeat=k)):
            x=p
            for j,s in enumerate(seed):x=m.cf[j][(s+delta[j])%q][x]
            left.setdefault(x,[]).append(i)
        out=bytearray((q**r+7)//8)
        for i,seed in enumerate(itertools.product(range(q),repeat=r-k)):
            self.b.check();x=c
            for j in range(r-1,k-1,-1):x=m.cb[j][(seed[j-k]+delta[j])%q][x]
            for prefix in left.get(x,()):index=prefix*tail+i;out[index//8]|=1<<(index%8)
        value=int.from_bytes(out,'little');self.builds+=1
        if self.entries_bytes<=self.cap:
            while self.cache and self.cache_bytes+self.entries_bytes>self.cap:self.cache.popitem(last=False);self.cache_bytes-=self.entries_bytes;self.evictions+=1
            self.cache[key]=value;self.cache_bytes+=self.entries_bytes;self.peak_bytes=max(self.peak_bytes,self.cache_bytes)
        return value

def merge(target,delta,cipher_domain,h_domain):
    # Correlations are retained: never merge unequal cipher domains.
    if h_domain and cipher_domain:target[delta,cipher_domain]=target.get((delta,cipher_domain),0)|h_domain

def solve(f,observations,budget=None,cache_cap=64<<20,predicate_factory=None):
    b=budget or Budget();m=Model(f);q,r=m.q,m.r;fullc=(1<<(q**r))-1;fullh=(1<<len(m.maps))-1;obs=collections.defaultdict(list)
    for t,p,c in observations:
        if not(0<=p<q and 0<=c<q and t>=0):raise ValueError('bad synthetic observation')
        obs[t].append((p,c))
    length=max(obs,default=-1)+1;pred=(predicate_factory or Predicates)(m,b,cache_cap);records=[];controllers=0;branches=0;peakbranches=0;splits=0;covered=0;reason=None;complete=True
    try:
        for control in itertools.product(range(q),repeat=r):
            b.check(force=True);nodes={((0,)*r,fullc):fullh};digits=m.digits(control,length)
            for t in range(length):
                filtered={}
                for (delta,cs),hs in nodes.items():
                    b.check();branches+=1
                    for p,c in obs[t]:cs&=pred.get(delta,p,c)
                    merge(filtered,delta,cs,hs)
                nodes=filtered
                if not nodes:break
                if t==length-1:break
                following={}
                for (delta,cs),hs in nodes.items():
                    for mask,group in m.mask_groups(digits[t]):
                        hh=hs&group
                        if hh:
                            new=tuple((v-((mask>>j)&1))%q for j,v in enumerate(delta));merge(following,new,cs,hh);splits+=1
                nodes=following;peakbranches=max(peakbranches,len(nodes))
            compact=[];seenh=0
            for (delta,cs),hs in nodes.items():
                if seenh&hs:raise AssertionError('index class represented by two final relations')
                seenh|=hs;compact.append(dict(index_classes=hex(hs),cipher_starts=hex(cs),final_offsets=list(delta)))
                covered+=pop(cs)*sum(len(m.aliases[h]) for h in bits(hs))
            if compact:records.append(dict(control=list(control),relations=compact))
            controllers+=1
    except Limit as error:complete=False;reason=str(error)
    return dict(completed=complete,reason=reason,status='complete_compatible_relation' if complete else 'budget_unresolved',exact_raw_key_count=str(covered) if complete else None,found_raw_keys_lower_bound=str(covered),control_starts_completed=controllers,control_starts_requested=q**r,complete_prefix_raw_descriptions=controllers*q**r*m.m**2,raw_key_descriptions=q**(2*r)*m.m**2,reachable_index_classes=len(m.maps),index_aliases=[[list(p) for p in rows] for rows in m.aliases],index_maps=[list(h) for h in m.maps],relations=records,inference_time_steps=length,branches_visited=branches,max_live_branches=peakbranches,index_mask_partitions=splits,predicate_builds=pred.builds,predicate_cache_hits=pred.hits,predicate_cache_evictions=pred.evictions,predicate_cache_peak_accounted_bytes=pred.peak_bytes,budget=b.receipt(),K4_evaluations=0)

def relation_masks(result):
    out={}
    for row in result['relations']:
        control=tuple(row['control'])
        for relation in row['relations']:
            for h in bits(int(relation['index_classes'],16)):
                key=control,h
                if key in out:raise AssertionError('duplicate class')
                out[key]=int(relation['cipher_starts'],16)
    return out

def write_keys(result,f,path,budget,cap=2000000,bytecap=256<<20):
    mapping=relation_masks(result);m=Model(f);count=0;size=0;dig=hashlib.sha256()
    with Path(path).open('wb') as output:
        for control in itertools.product(range(f['q']),repeat=f['r']):
            for index in itertools.product(range(m.m),repeat=2):
                domain=mapping.get((control,m.class_of[index]),0)
                for value in bits(domain):
                    budget.check();raw=json.dumps(list(control)+list(index)+list(unpack(value,f['q'],f['r'])),separators=(',',':')).encode()+b'\n';count+=1;size+=len(raw)
                    if count>cap or size>bytecap:raise Limit('output_budget_unresolved')
                    output.write(raw);dig.update(raw)
    return dict(count=count,bytes=size,sha256=dig.hexdigest())
