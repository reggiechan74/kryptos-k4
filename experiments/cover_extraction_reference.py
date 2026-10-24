"""Independent complete word enumeration / position-lattice extraction oracle."""
import functools,collections

def paths(vocab,remaining):
 if remaining==0:yield ();return
 for w in vocab:
  if len(w)<=remaining:
   for tail in paths(vocab,remaining-len(w)):yield (w,)+tail

def count_message(model,message,k,N,phase,total_words=None):
 # Full-position traversal, not three-run length factorization.
 spans={};pos=model.runs[0]
 for w in model.a:spans[pos]=w;pos+=len(w)
 pos+=model.runs[1]
 for w in model.b:spans[pos]=w;pos+=len(w)
 boundaries=set(spans)|{i+len(w) for i,w in spans.items()};inside={j for i,w in spans.items() for j in range(i+1,i+len(w))}
 @functools.lru_cache(None)
 def visit(pos,j,t):
  if pos==model.total:return int(t==len(message) and (total_words is None or j==total_words))
  if total_words is not None and j>=total_words:return 0
  if pos in inside:return 0
  answer=0
  for w in ([spans[pos]] if pos in spans else model.vocab):
   end=pos+len(w)
   if w not in model.vocab or end>model.total or any(pos<b<end for b in boundaries):continue
   take=j%N==phase
   if take and (len(w)<k or t>=len(message) or message[t]!=w[k-1]):continue
   answer+=visit(end,j+1,t+int(take))
  return answer
 return visit(0,0,0)

def brute_model(model,k,N,phase):
 out=collections.Counter()
 for a in paths(model.vocab,model.runs[0]):
  for b in paths(model.vocab,model.runs[1]):
   for c in paths(model.vocab,model.runs[2]):
    words=a+model.a+b+model.b+c;selected=[w for j,w in enumerate(words) if j%N==phase]
    if any(len(w)<k for w in selected):continue
    out[''.join(w[k-1] for w in selected)]+=1
 return out
