"""Exact finite ordinary-lexicon constraints, not an English or K4 oracle."""
import collections,hashlib,itertools,json,re,time,zipfile,sys,resource
import autokey_constraints as ak
import cover_phrase as cp
ALPHABETS={'AZ':'ABCDEFGHIJKLMNOPQRSTUVWXYZ','KRYPTOS':'KRYPTOSABCDEFGHIJLMNQUVWXZ'}
ADDITIONS=('IQLUSION','UNDERGRUUND','DESPARATLY','X','Q','WW')

def vocabularies(path):
 names=cp.validate_brown(path);s=set();j=set();plants=[]
 with zipfile.ZipFile(path) as z:
  for name in names:
   for line_no,line in enumerate(z.read(name).decode('ascii').splitlines()):
    tokens=[]
    for tagged in line.split():
     token=tagged.rsplit('/',1)[0];word=cp.eligible(token);tokens.append(word)
     if word:s.add(word)
     if re.fullmatch(r"[A-Za-z]+(?:['-][A-Za-z]+)+",token):j.add(re.sub("['-]",'',token).upper())
    if len(plants)<6:
     for start in range(len(tokens)):
      words=[];total=0
      for word in tokens[start:]:
       if word is None:break
       words.append(word);total+=len(word)
       if total==97:
        text=''.join(words)
        if text not in [p['text'] for p in plants]:plants.append(dict(file=name,line=line_no,start=start,words=words,text=text))
        break
       if total>97:break
      if len(plants)==6:break
 j|=s
 return {'S':s,'J':j,'O':j|set(ADDITIONS)},plants

def vocab_receipt(v):return dict(words=len(v),sha256=hashlib.sha256(('\n'.join(sorted(v))+'\n').encode()).hexdigest(),length_counts=dict(sorted(collections.Counter(map(len,v)).items())))

def mask_hist(total,known,vocab):
 buckets=collections.defaultdict(list)
 for w in vocab:buckets[len(w)].append(w)
 out=[]
 for i in range(total):
  h={}
  for length,words in buckets.items():
   if i+length>total:continue
   constraints=[(p-i,c) for p,c in known.items() if i<=p<i+length]
   count=len(words) if not constraints else sum(all(w[p]==c for p,c in constraints) for w in words)
   if count:h[length]=count
  out.append(h)
 return out

def distribution(hist,k=1,N=1,phase=0):
 total=len(hist);dp=[{} for _ in range(total+1)];dp[0][0]=1
 for pos in range(total):
  for j,count in dp[pos].items():
   selected=j%N==phase
   for length,mult in hist[pos].items():
    if selected and length<k:continue
    target=dp[pos+length];target[j+1]=target.get(j+1,0)+count*mult
 end=dp[-1];output=collections.Counter()
 for j,count in end.items():output[sum(t%N==phase for t in range(j))]+=count
 return dict(total=sum(end.values()),coverwords=dict(sorted(end.items())),output_lengths=dict(sorted(output.items())))

class Lexicon:
 def __init__(self,vocab):
  self.words=vocab;self.trie={}
  for word in vocab:
   node=self.trie
   for ch in word:node=node.setdefault(ch,{})
   node['']=True
 def accepts(self,text):
  reachable=bytearray(len(text)+1);reachable[0]=1
  for i in range(len(text)):
   if not reachable[i]:continue
   node=self.trie
   for j in range(i,len(text)):
    node=node.get(text[j])
    if node is None:break
    if '' in node:reachable[j+1]=1
  return bool(reachable[-1])
 def hist(self,text):
  return [{n:1 for n in range(1,len(text)-i+1) if text[i:i+n] in self.words} for i in range(len(text))]
 def witness(self,text,k=1,N=1,phase=0):
  # One deterministic feasible word path; no language ranking.
  hist=self.hist(text);states=[{} for _ in range(len(text)+1)];states[0][0]=()
  for i in range(len(text)):
   for j,words in states[i].items():
    for length in sorted(hist[i]):
     if j%N==phase and length<k:continue
     states[i+length].setdefault(j+1,words+(text[i:i+length],))
  return states[-1][min(states[-1])] if states[-1] else None

def roots(cipher,known,alphabet,equation,lag):
 sigma,tau=ak.COEFFICIENTS[equation];m=len(alphabet);cs=[alphabet.index(x) for x in cipher];a=[1]*len(cipher);b=[0]*len(cipher)
 for i in range(lag,len(cipher)):
  a[i]=-sigma*tau*a[i-lag];b[i]=(sigma*cs[i]-sigma*tau*b[i-lag])%m
 fixed={}
 for i,ch in known.items():
  value=a[i]*(alphabet.index(ch)-b[i])%m;r=i%lag
  if r in fixed and fixed[r]!=value:return None
  fixed[r]=value
 return a,b,fixed,[r for r in range(lag) if r not in fixed]

def plaintexts(cipher,known,alphabet,equation,lag):
 result=roots(cipher,known,alphabet,equation,lag)
 if result is None:return
 a,b,fixed,free=result;m=len(alphabet)
 base=bytearray(ord(alphabet[(a[i]*fixed.get(i%lag,0)+b[i])%m]) for i in range(len(cipher)))
 patches=[[[ (i,ord(alphabet[(a[i]*x+b[i])%m])) for i in range(r,len(cipher),lag)] for x in range(m)] for r in free]
 for values in itertools.product(range(m),repeat=len(free)):
  row=base[:]
  for t,x in enumerate(values):
   for i,v in patches[t][x]:row[i]=v
  yield row.decode('ascii')

def primer_for(cipher,plain,alphabet,equation,lag):
 sigma,tau=ak.COEFFICIENTS[equation];m=len(alphabet)
 return ''.join(alphabet[tau*(alphabet.index(c)-sigma*alphabet.index(p))%m] for c,p in zip(cipher[:lag],plain[:lag]))

def selectors(hist):
 return {f'k{k}:N{N}:p{phase}':distribution(hist,k,N,phase) for k in range(1,5) for N,phase in ((1,0),(2,0),(2,1))}

def search(cipher,known,lexicons,models=None,lag=27,seconds=120):
 clock=time.monotonic();models=models or [(name,equation) for name in ALPHABETS for equation in ak.COEFFICIENTS];rows=[];candidates=[];unique=set();complete=True
 for name,equation in models:
  alphabet=ALPHABETS[name];r=roots(cipher,known,alphabet,equation,lag)
  if r is None:rows.append(dict(alphabet=name,equation=equation,contradicted=True,processed=0));continue
  processed=0;counts=collections.Counter()
  for plain in plaintexts(cipher,known,alphabet,equation,lag):
   processed+=1
   if lexicons['O'].accepts(plain):
    assert all(plain[i]==v for i,v in known.items());primer=primer_for(cipher,plain,alphabet,equation,lag)
    assert ak.transform(plain,primer,alphabet,equation,'plaintext')==cipher
    compatible={}
    for label,lex in lexicons.items():
     if lex.accepts(plain):
      counts[label]+=1;h=lex.hist(plain);compatible[label]=dict(selectors=selectors(h),witness=lex.witness(plain))
    candidates.append(dict(alphabet=name,equation=equation,plaintext=plain,primer=primer,lexicons=compatible,full_reencryption=True));unique.add(plain)
   if processed%256==0 and (time.monotonic()-clock>seconds or cp.rss_bytes()>512*1024**2):complete=False;break
  rows.append(dict(alphabet=name,equation=equation,free_symbols=len(r[3]),expected=len(alphabet)**len(r[3]),processed=processed,admitted_by_lexicon=dict(counts)))
  if not complete:break
 return dict(complete=complete,elapsed_seconds=time.monotonic()-clock,peak_rss_bytes=cp.rss_bytes(),models=rows,model_key_descriptions=sum(x['processed'] for x in rows),distinct_lexical_plaintexts=len(unique),candidates=candidates)
