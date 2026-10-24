"""Independent tiny path enumeration, string-edit BFS and congruence oracle."""
import functools,itertools,math

def brute_alignments(a,b):
 @functools.lru_cache(None)
 def paths(i,j):
  if i==len(a) and j==len(b):return [(0,'')]
  out=[]
  if i<len(a) and j<len(b):
   op='M' if a[i]==b[j] else 'S';out += [(v+(op=='S'),op+s) for v,s in paths(i+1,j+1)]
  if i<len(a):out += [(v+1,'D'+s) for v,s in paths(i+1,j)]
  if j<len(b):out += [(v+1,'I'+s) for v,s in paths(i,j+1)]
  return out
 allpaths=paths(0,0);best=min(x[0] for x in allpaths);return best,{s for v,s in allpaths if v==best}

def bfs_distance(source,target,max_edits):
 alphabet=set(source+target);level={source};seen=set(level)
 for depth in range(max_edits+1):
  if target in level:return depth
  if depth==max_edits:break
  nxt=set()
  for s in level:
   for i in range(len(s)):
    nxt.add(s[:i]+s[i+1:])
    for c in alphabet:nxt.add(s[:i]+c+s[i+1:])
   for i in range(len(s)+1):
    for c in alphabet:nxt.add(s[:i]+c+s[i:])
  level=nxt-seen;seen|=level
 return None

def congruence_candidates(pairs,alphabet,units_only):
 n=len(alphabet);(u,v),(x,y)=[(alphabet.index(a),alphabet.index(b)) for a,b in pairs];out=[]
 for scale in range(n):
  if (scale*(x-u)-(y-v))%n:continue
  shift=(v-scale*u)%n
  if not units_only or math.gcd(scale,n)==1:out.append((scale,shift))
 return out

def brute_function_count(source,target,alphabet,injective):
 n=0
 for output in itertools.product(alphabet,repeat=len(alphabet)):
  if injective and len(set(output))!=len(output):continue
  table=dict(zip(alphabet,output))
  if ''.join(table[c] for c in source)==target:n+=1
 return n
