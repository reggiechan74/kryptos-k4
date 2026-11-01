"""Classical deterministic-transducer / integer-interval path counting.
No target data. Counts input strings, never distinct output integers.
"""
from collections import defaultdict
from functools import lru_cache

ALPHABETS = {1:'AB',2:'ABC',3:'ABCD',4:'ABCD',5:'ABCD',6:'ABC',7:'AB',8:'AB',9:'AB',10:'ABC',11:'AB',12:'AB'}
TABLES = {1:('0','1'),2:('0','10','11'),3:('1','010','011','00100'),4:('00','01','100','101'),5:('11','011','0011','1011')}

class Model:
    deterministic = True
    def __init__(self, codec):
        self.codec=codec
        self.alphabet=ALPHABETS[codec]
        self.start = 'ABC' if codec==10 else '' if codec in (8,12) else ('',0) if codec==9 else 0
    @lru_cache(None)
    def step(self,q,a):
        c=self.codec
        if c<=5: return q,TABLES[c][self.alphabet.index(a)]
        if c==6:
            return q^(a=='B'), (('0','10','11'),('11','0','10'))[q][self.alphabet.index(a)]
        if c==7:
            if a=='A': return 0,'0'
            return (0,'10') if q==1 else (1,'1')
        if c==8:
            if not q:return a,''
            return '',{'AA':'0','AB':'10','BA':'110','BB':'111'}[q+a]
        if c==9:
            old,r=q
            if old==a:
                if r==2:return ('',0),str(int(a=='B'))+'110'
                return (a,r+1),''
            emitted='' if not old else str(int(old=='B'))+'1'*(r-1)+'0'
            return (a,1),emitted
        if c==10:
            rank=q.index(a)
            return a+q.replace(a,''),('0','10','11')[rank]
        if c==11:return q^(a=='B'),str(int(a=='B'))
        phrase=q+a
        if phrase in ('B','BB'):return phrase,''
        return '',{'A':'00','BA':'01','BBA':'10','BBB':'11'}[phrase]
    def finish(self,q):
        if self.codec==8:return {'':'','A':'0','B':'1'}[q]
        if self.codec==9:
            a,r=q
            return '' if not a else str(int(a=='B'))+'1'*(r-1)+'0'
        if self.codec==11:return str(int(q))
        if self.codec==12 and q:return None
        return ''

def interval(base,width,transport):
    if base<2 or width<1:raise ValueError('invalid radix/width')
    if transport=='minimal':return (0 if width==1 else base**(width-1)),base**width-1
    if transport=='fixed':return 0,base**width-1
    raise NotImplementedError('only unclipped positional minimal/fixed transport')

def domains(model,n,mode):
    if n < 0 or mode not in ('all','first_min','first_max'):raise ValueError('invalid domains')
    ds=[model.alphabet]*n
    if n and mode!='all':ds[0]=model.alphabet[0 if mode=='first_min' else -1]
    return ds

def lengths(model,ds,header):
    if getattr(model,'deterministic',False) is not True:raise NotImplementedError('deterministic input encoders only')
    if any(len(d)!=len(set(d)) or any(a not in model.alphabet for a in d) for d in ds):raise ValueError('invalid input domains')
    states={(model.start,len(header))}
    work=0
    for domain in ds:
        nxt=set()
        for q,t in states:
            for a in domain:
                qq,w=model.step(q,a);nxt.add((qq,t+len(w)));work+=1
        states=nxt
    out=set()
    for q,t in states:
        w=model.finish(q)
        if w is not None:out.add(t+len(w))
    return out,work

def count_interval(model,ds,header,lo,hi):
    if any(bit not in '01' for bit in header):raise ValueError('binary header required')
    ls,length_work=lengths(model,ds,header)
    total=0; witness=None;visited=0;transitions=0;bitwork=0;maxbits=0
    for L in sorted(ls):
        low=max(0,lo);high=min(hi,(1<<L)-1)
        if low>high:continue
        bounds=(format(low,f'0{L}b') if L else '',format(high,f'0{L}b') if L else '')
        def advance(t,rl,rh,w):
            nonlocal bitwork
            if t+len(w)>L:return None
            bitwork+=len(w)
            rel=[]
            for old,b in zip((rl,rh),bounds):
                chunk=b[t:t+len(w)]
                rel.append(old if old else (w>chunk)-(w<chunk))
            if rel[0]<0 or rel[1]>0:return None
            return t+len(w),rel[0],rel[1]
        initial=advance(0,0,0,header)
        if initial is None:continue
        states={(model.start,*initial):(1,'')}
        for domain in ds:
            nxt={}
            visited+=len(states)
            for (q,t,rl,rh),(ways,path) in states.items():
                for a in domain:
                    transitions+=1;qq,w=model.step(q,a);z=advance(t,rl,rh,w)
                    if z is None:continue
                    key=(qq,*z)
                    if key in nxt:nxt[key]=(nxt[key][0]+ways,nxt[key][1])
                    else:nxt[key]=(ways,path+a)
                    maxbits=max(maxbits,nxt[key][0].bit_length())
            states=nxt
        visited+=len(states)
        for (q,t,rl,rh),(ways,path) in states.items():
            w=model.finish(q)
            if w is None:continue
            z=advance(t,rl,rh,w)
            if z is not None and z[0]==L:
                total+=ways
                if witness is None:witness=path
    return {'count':total,'witness':witness,'lengths':sorted(ls),'length_work':length_work,'states':visited,'transitions':transitions,'bit_work':bitwork,'max_count_bits':max(maxbits,total.bit_length())}

def count(model,n,mode,header,base,width,transport):
    return count_interval(model,domains(model,n,mode),header,*interval(base,width,transport))
