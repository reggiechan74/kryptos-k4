"""Exact byte-generated torus masks; same cache policy and semantics."""
import math,sys
from sigaba_sparse_ownership import ReservedPredicates

def periodic_low(n,period,shift):
    if not (n>0 and period>0 and n%period==0 and 0<shift<period):raise ValueError('fixed periodic mask dimensions')
    repeats=8//math.gcd(period,8);tile_bits=period*repeats
    run=(1<<shift)-1;tile=0
    for i in range(repeats):tile|=run<<(i*period)
    raw=tile.to_bytes(tile_bits//8,'little');size=(n+7)//8
    raw=(raw*((size+len(raw)-1)//len(raw)))[:size]
    return int.from_bytes(raw,'little')&((1<<n)-1)

class ByteMaskPredicates(ReservedPredicates):
    def translate(self,value,delta):
        if value<0 or value>>self.N or len(delta)!=self.m.r:raise ValueError('outside fixed torus')
        q,r=self.m.q,self.m.r
        for j,d in enumerate(delta):
            d%=q
            if not d:continue
            stride=q**(r-1-j);period=q*stride;shift=d*stride;key=(j,d)
            if key in self.masks:self.masks.move_to_end(key);low,high,size=self.masks[key]
            else:
                low=periodic_low(self.N,period,shift);high=self.full^low;size=sys.getsizeof(low)+sys.getsizeof(high)+256;self.mask_builds+=1
                if size<=self.mask_cap:
                    while self.masks and self.mask_bytes+size>self.mask_cap:
                        _,(_,_,old)=self.masks.popitem(last=False);self.mask_bytes-=old;self.mask_evictions+=1
                    self.masks[key]=(low,high,size);self.mask_bytes+=size;self.mask_peak=max(self.mask_peak,self.mask_bytes)
            value=((value&low)<<(period-shift))|((value&high)>>shift)
        return value
