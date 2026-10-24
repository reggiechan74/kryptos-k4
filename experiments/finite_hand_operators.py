"""Exact output-index permutations/affine operators for fixed finite hand studies."""
import hashlib,itertools,json,math
A='KRYPTOSABCDEFGHIJLMNQUVWXZ';KEYS=('KRYPTOS','PALIMPSEST','ABSCISSA')
def invperm(p):
 if sorted(p)!=list(range(len(p))):raise ValueError('not a bijection')
 out=[0]*len(p)
 for i,j in enumerate(p):out[j]=i
 return bytes(out)
def columnar(word,n=97):
 order=sorted(range(len(word)),key=lambda i:(word[i],i));return bytes(i for c in order for i in range(c,n,len(word)))
def identity(n=97):return bytes(range(n)),1,bytes(n)
def compose(first,following,q=26):
 p,s,b=first;r,t,c=following
 return bytes(p[j] for j in r),s*t,bytes((t*b[j]+c[i])%q for i,j in enumerate(r))
def invert(op,q=26):
 p,s,b=op;r=invperm(p);return r,s,bytes((-s*b[j])%q for j in r)
def apply(values,op,q=26):
 p,s,b=op;return bytes((s*values[j]+b[i])%q for i,j in enumerate(p))
def signature(op):p,s,b=op;return p+bytes([s%26])+b
def primitives(n=97):
 out=[]
 for word in KEYS:
  p=columnar(word,n)
  for direction,v in [('direct',p),('inverse',invperm(p))]:out.append((dict(kind='columnar',key=word,direction=direction),(v,1,bytes(n))))
 for step in range(2,13):
  for direction,k in [('direct',step),('inverse',pow(step,-1,n))]:out.append((dict(kind='skip',step=step,direction=direction),(bytes((i*k)%n for i in range(n)),1,bytes(n))))
 out.append((dict(kind='reversal'),(bytes(reversed(range(n))),1,bytes(n))))
 for word in KEYS:
  k=[A.index(word[i%len(word)]) for i in range(n)]
  for label,s,t in [('plus',1,1),('minus',1,-1),('beaufort',-1,1)]:out.append((dict(kind='arithmetic',key=word,equation=label),(bytes(range(n)),s,bytes(t*v%26 for v in k))))
 return out
# Byte-lane zero count without borrow propagation: each XOR byte is at most31.
def packed_matches(observation,expected,size):
 x=observation^expected;low=int.from_bytes(bytes([127])*size,'big');high=int.from_bytes(bytes([128])*size,'big')
 return bin(~((x+low)|x|low)&high).count('1')
def match_constants(size):return int.from_bytes(bytes([127])*size,'big'),int.from_bytes(bytes([128])*size,'big')
def fast_matches(x,y,low,high):return bin(~(((x^y)+low)|(x^y)|low)&high).count('1')
