"""Exact coordinate-torus translation of cipher-start predicates; no model change."""
import collections,sys
import sigaba_joint_toy as base
class TorusPredicates:
    def __init__(self,model,budget,cap=64<<20):
        self.m=model;self.b=budget;self.cap=cap;self.cache=collections.OrderedDict();self.cache_bytes=0;self.peak_bytes=0;self.hits=0;self.builds=0;self.evictions=0;self.translations=0;self.base_hits=0;self.calls=0;self.builder=base.Predicates(model,budget,cap=0);self.N=model.q**model.r;self.full=(1<<self.N)-1;self.masks={};maskbytes=0
        for j in range(model.r):
            stride=model.q**(model.r-1-j);period=model.q*stride
            for d in range(1,model.q):
                low=(self.full//((1<<period)-1))*((1<<(d*stride))-1);high=self.full^low;size=sys.getsizeof(low)+sys.getsizeof(high)+128
                if maskbytes+size<=cap:self.masks[j,d]=(low,high);maskbytes+=size
        self.cache_bytes=maskbytes;self.mask_bytes=maskbytes;self.peak_bytes=maskbytes
    def cached(self,key):
        if key in self.cache:self.cache.move_to_end(key);return self.cache[key][0]
        return None
    def store(self,key,value):
        size=sys.getsizeof(value)+256
        if self.mask_bytes+size>self.cap:return
        while self.cache and self.cache_bytes+size>self.cap:
            _,(_,oldsize)=self.cache.popitem(last=False);self.cache_bytes-=oldsize;self.evictions+=1
        self.cache[key]=(value,size);self.cache_bytes+=size;self.peak_bytes=max(self.peak_bytes,self.cache_bytes)
    def translate(self,value,delta):
        if value<0 or value>>self.N:raise ValueError('outside fixed-width state domain')
        q,r=self.m.q,self.m.r
        if len(delta)!=r:raise ValueError('offset dimension mismatch')
        for j,d in enumerate(delta):
            d%=q
            if not d:continue
            stride=q**(r-1-j);period=q*stride;shift=d*stride
            pair=self.masks.get((j,d))
            if pair is None:low=(self.full//((1<<period)-1))*((1<<shift)-1);high=self.full^low
            else:low,high=pair
            value=((value&low)<<(period-shift))|((value&high)>>shift)
        return value
    def get_base(self,p,c):
        key=('base',p,c);value=self.cached(key)
        if value is not None:self.base_hits+=1;return value
        value=self.builder.get((0,)*self.m.r,p,c);self.builds+=1;self.store(key,value);return value
    def get(self,delta,p,c):
        self.calls+=1;delta=tuple(x%self.m.q for x in delta);key=('delta',delta,p,c);value=self.cached(key)
        if value is not None:self.hits+=1;return value
        value=self.translate(self.get_base(p,c),delta);self.translations+=1;self.store(key,value);return value
    def metrics(self):return dict(calls=self.calls,zero_offset_builds=self.builds,base_cache_hits=self.base_hits,translated_cache_hits=self.hits,translations=self.translations,cache_evictions=self.evictions,cache_peak_accounted_bytes=self.peak_bytes,fixed_mask_bytes=self.mask_bytes,cache_cap_bytes=self.cap)
