"""Independent nested-tree, bit arithmetic and manual UTF8 reference."""
from tree_geometry_ipa import AZ,ALPHABETS,CODES,GEO,IPA

def utf8(text):
 out=[]
 for c in text:
  n=ord(c)
  if n<128:out.append(n)
  elif n<2048:out.extend((192+(n>>6),128+(n&63)))
  elif n<65536:out.extend((224+(n>>12),128+((n>>6)&63),128+(n&63)))
  else:out.extend((240+(n>>18),128+((n>>12)&63),128+((n>>6)&63),128+(n&63)))
 return out

def right(t):
 k,l,r=t;x,a,b=l
 return (x,a,(k,b,r))
def left(t):
 k,l,r=t;x,a,b=r
 return (x,(k,l,a),b)
def splay(t,key):
 # Functional zipper: rebuild the affected grandparent subtree, then its ancestors.
 path=[];node=t
 while node[0]!=key:
  side=1 if key<node[0] else 2;path.append(side);node=node[side]
 def get(node,steps):
  for side in steps:node=node[side]
  return node
 def put(node,steps,subtree):
  if not steps:return subtree
  side=steps[0];parts=list(node);parts[side]=put(parts[side],steps[1:],subtree);return tuple(parts)
 while path:
  if len(path)==1:
   t=right(t) if path[0]==1 else left(t);path=[]
  else:
   prefix=path[:-2];g=get(t,prefix);x,y=path[-2:]
   if (x,y)==(1,1):g=right(right(g))
   elif (x,y)==(2,2):g=left(left(g))
   elif (x,y)==(1,2):g=right((g[0],left(g[1]),g[2]))
   else:g=left((g[0],g[1],right(g[2])))
   t=put(t,prefix,g);path=prefix
 return t

def preorder(t):return [] if t is None else [t[0]]+preorder(t[1])+preorder(t[2])
def step(state,value):
 bits=[(state>>j)&1 for j in range(35)];vbits=[(value>>j)&1 for j in range(35)];rot=bits[-1:]+bits[:-1];mixed=[x^y for x,y in zip(bits,vbits)];out=[];carry=0
 for x,y in zip(rot,mixed):
  z=x+y+carry;out.append(z%2);carry=z//2
 return sum(b*(2**j) for j,b in enumerate(out))

def crypt(text,m,decrypt=False):
 a=ALPHABETS[m['alphabet']];out=[]
 if m['role']=='T':
  labels=AZ if m['order']=='AZ' else GEO;s=m['seed'];labels=labels[s:]+labels[:s]
  def build(lo,hi):
   if lo>=hi:return None
   k=(lo+hi)//2;return (k,build(lo,k),build(k+1,hi))
  tree=build(0,26)
  for c in text:
   slots=preorder(tree);node=slots[a.index(c)] if decrypt else labels.index(c);out.append(labels[node] if decrypt else a[slots.index(node)]);tree=splay(tree,node)
  return ''.join(out)
 state=CODES[m['seed']] if m['role']=='G' else None;key=None if state is not None else utf8(IPA[m['key']])
 for i,c in enumerate(text):
  k=state%26 if state is not None else key[(m['phase']+i)%len(key)]%26
  n=a.index(c);n=(n-k if decrypt else n+k) if m['equation']=='plus' else k-n;v=a[n%26];out.append(v)
  if state is not None:
   p=v if decrypt else c;ct=c if decrypt else v;state=step(state,CODES[p if m['source']=='P' else ct])
 return ''.join(out)
