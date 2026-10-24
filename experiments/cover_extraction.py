"""Post-decryption word-cover feasibility. Never decrypts actual K4."""
import collections,functools,itertools,math,random,re
NATO='ALFA BRAVO CHARLIE DELTA ECHO FOXTROT GOLF HOTEL INDIA JULIETT KILO LIMA MIKE NOVEMBER OSCAR PAPA QUEBEC ROMEO SIERRA TANGO UNIFORM VICTOR WHISKEY XRAY YANKEE ZULU'.split()

def models():
 out=[]
 for split in ('ENE','EN'):
  words=['EAST','NORTH','EAST'] if split=='ENE' else ['EAST','NORTHEAST']
  replace={'B':'BERLIN','C':'CLOCK','E':'EAST','N':words[1]}
  for kind in ('A30','R26'):
   vocab=sorted(set(NATO+list(replace.values()))) if kind=='A30' else sorted(replace.get(w[0],w) for w in NATO)
   out.append(Model(kind+'-'+split,vocab,words))
 return out

class Model:
 def __init__(self,name,vocab,block_a,block_b=('BERLIN','CLOCK'),runs=(21,29,23)):
  self.name=name;self.vocab=tuple(sorted(vocab));self.a=tuple(block_a);self.b=tuple(block_b);self.runs=tuple(runs);self.fixed=len(self.a)+len(self.b);self.total=sum(runs)+sum(map(len,self.a+self.b));self.lengths=tuple(sorted(collections.Counter(map(len,self.vocab)).items()));self.labels={}
  for k in range(1,5):
   for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':self.labels[k,c]=tuple(sorted(collections.Counter(len(w) for w in self.vocab if len(w)>=k and w[k-1]==c).items()))
  self._run=functools.lru_cache(maxsize=32768)(self._run_uncached)
 @functools.lru_cache(maxsize=None)
 def ways(self,n,r):
  if r==0:return int(n==0)
  if n<0:return 0
  return sum(weight*self.ways(n-length,r-1) for length,weight in self.lengths)
 def run_options(self,n):return [r for r in range(n//min(map(len,self.vocab))+1) if self.ways(n,r)]
 def distributions(self):
  out=collections.Counter();triples=[]
  for a,b,c in itertools.product(*(self.run_options(n) for n in self.runs)):
   count=math.prod(self.ways(n,r) for n,r in zip(self.runs,(a,b,c)));total=a+b+c+self.fixed;out[total]+=count;triples.append(dict(a=a,b=b,c=c,coverwords=total,count=count))
  return dict(counts={str(k):out[k] for k in sorted(out)},total=sum(out.values()),triples=triples)
 def _run_uncached(self,n,r,startmod,piece,k,N,phase):
  dp=[0]*(n+1);dp[0]=1;t=0
  for j in range(r):
   if (j+startmod)%N==phase:
    if t>=len(piece):return 0
    choices=self.labels.get((k,piece[t]),());t+=1
   else:choices=self.lengths
   nxt=[0]*(n+1)
   for length,weight in choices:
    for pos in range(n-length+1):
     if dp[pos]:nxt[pos+length]+=dp[pos]*weight
   dp=nxt
  return dp[n] if t==len(piece) else 0
 def run_count(self,n,r,start,piece,k,N,phase):return self._run(n,r,start%N,piece,k,N,phase)
 def sample(self,rng,total_words=None):
  rows=[x for x in self.distributions()['triples'] if total_words is None or x['coverwords']==total_words]
  if not rows:return None
  t=weighted_choice(rows,[x['count'] for x in rows],rng)
  def fill(n,r):
   out=[]
   while r:
    options=[w for w in self.vocab if self.ways(n-len(w),r-1)];weights=[self.ways(n-len(w),r-1) for w in options];w=weighted_choice(options,weights,rng);out.append(w);n-=len(w);r-=1
   assert n==0;return out
  return fill(self.runs[0],t['a'])+list(self.a)+fill(self.runs[1],t['b'])+list(self.b)+fill(self.runs[2],t['c'])
 def lanes(self):
  return [Lane(self,k,N,phase,stratum) for stratum in ('all','15') if stratum=='all' or self.distributions()['counts'].get('15',0) for N,phase in [(1,0),(2,0),(2,1)] for k in range(1,5)]

class Lane:
 def __init__(self,model,k,N,phase,stratum):
  self.model=model;self.k=k;self.N=N;self.phase=phase;self.stratum=stratum;self.id=f'{model.name}:k{k}:N{N}:p{phase}:{stratum}';self.templates=[]
  for t in model.distributions()['triples']:
   if stratum=='15' and t['coverwords']!=15:continue
   pattern=[];groups=[];j=0
   for index,(n,r) in enumerate(zip(model.runs,[t['a'],t['b'],t['c']])):
    start=len(pattern);begin=j
    for _ in range(r):
     if j%N==phase:pattern.append('.')
     j+=1
    groups.append((n,r,begin,start,len(pattern)))
    if index<2:
     for w in (model.a if index==0 else model.b):
      if j%N==phase:
       if len(w)<k:raise ValueError('selected fixed word too short')
       pattern.append(w[k-1])
      j+=1
   self.templates.append((tuple((i,c) for i,c in enumerate(pattern) if c!='.'),groups,len(pattern),t))
  self.lengths=sorted({x[2] for x in self.templates});patterns=[''.join(dict(t[0]).get(i,'.') for i in range(t[2])) for t in self.templates];self.regex=re.compile('(?:'+'|'.join(sorted(set(patterns)))+')')
 def count(self,message):
  if len(message) not in self.lengths or self.regex.fullmatch(message) is None:return 0
  answer=0
  for fixed,groups,length,t in self.templates:
   if length!=len(message) or any(message[i]!=c for i,c in fixed):continue
   count=1
   for n,r,start,a,b in groups:
    count*=self.model.run_count(n,r,start,message[a:b],self.k,self.N,self.phase)
    if not count:break
   answer+=count
  return answer

def weighted_choice(items,weights,rng):
 total=sum(weights)
 if total<=0:raise ValueError('empty weighted domain')
 x=rng.randrange(total)
 for item,w in zip(items,weights):
  if x<w:return item
  x-=w
 raise AssertionError('unreachable')

def extract(words,k=1,N=1,phase=0):
 out=[]
 for j,w in enumerate(words):
  if j%N==phase:
   if len(w)<k:raise ValueError('selected word too short')
   out.append(w[k-1])
 return ''.join(out)

def fixed_spans(model):
 spans=[];pos=model.runs[0]
 for w in model.a:spans.append((pos,w));pos+=len(w)
 pos+=model.runs[1]
 for w in model.b:spans.append((pos,w));pos+=len(w)
 return spans

def word_lattice(vocab,length,known,forced=()):
 forced=dict(forced);ends={i+len(w) for i,w in forced.items()};bounds=set(forced)|ends
 edges={}
 for pos in range(length):
  options=[forced[pos]] if pos in forced else vocab
  es=[]
  for w in options:
   if w not in vocab or pos+len(w)>length or any(pos<b<pos+len(w) for b in bounds):continue
   if any(i<pos<i+len(word) for i,word in forced.items()):continue
   if all(known.get(pos+j,c)==c for j,c in enumerate(w)):es.append((pos+len(w),w))
  edges[pos]=es
 return edges

def lattice_counts(edges,length):
 dp={(0,0):1}
 for pos in range(length):
  for (p,j),count in list(dp.items()):
   if p!=pos:continue
   for end,w in edges[pos]:dp[end,j+1]=dp.get((end,j+1),0)+count
 return {str(j):n for (pos,j),n in sorted(dp.items()) if pos==length}

def source_known(k4):return {c['start']-1+i:x for c in k4['cribs'] for i,x in enumerate(c['plaintext'])}
def prefix_free(words):return not any(a!=b and b.startswith(a) for a in words for b in words)
def decode_cover(text,vocab):
 @functools.lru_cache(None)
 def walk(i):
  if i==len(text):return [()]
  return [(w,)+tail for w in vocab if text.startswith(w,i) for tail in walk(i+len(w))]
 return walk(0)
