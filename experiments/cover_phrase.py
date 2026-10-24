"""Finite corpus windows and fixed extraction feasibility; no K4 decryptor."""
import collections,functools,gzip,hashlib,itertools,json,os,re,resource,sys,time,zipfile
from pathlib import Path
import cover_extraction as c
BROWN_SHA='9b275f9b3b95d7bd66ccfb7cd259f445a13bbe5d1f4107aba09fd3e8364bafa6'

def eligible(word):
 if re.fullmatch('[A-Za-z]+',word) is None:return None
 w=word.upper();return w if len(w)>1 or w in ('A','I') else None

def parse_line(line):
 out=[]
 for token in line.split():
  if '/' not in token:out.append(None);continue
  out.append(eligible(token.rsplit('/',1)[0]))
 return out

def windows(tokens):
 for start in range(len(tokens)):
  if tokens[start] is None:continue
  words=[]
  for end in range(start,min(len(tokens),start+5)):
   if tokens[end] is None:break
   words.append(tokens[end])
   if len(words)>=2:yield start,len(words),tuple(words)

def validate_brown(path):
 raw=Path(path).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=BROWN_SHA:raise ValueError('Brown snapshot hash mismatch')
 with zipfile.ZipFile(path) as z:
  seen=set();total=0
  for i in z.infolist():
   if i.filename in seen or i.filename.startswith('/') or '..' in Path(i.filename).parts or '\\' in i.filename:raise ValueError('unsafe corpus archive')
   seen.add(i.filename);total+=i.file_size
   if i.file_size>2*1024**2 or total>20*1024**2:raise ValueError('corpus archive budget')
  names=sorted(n for n in seen if re.fullmatch(r'brown/c[a-r][0-9]{2}',n))
  if len(names)!=500:raise ValueError('expected complete500 text corpus')
  for n in names:z.read(n).decode('ascii')
 return names

def split_message(text,vocabulary):
 edges={i:[j for j in range(i+1,len(text)+1) if text[i:j] in vocabulary] for i in range(len(text))};dp={(0,0):1}
 for i in range(len(text)):
  for count in range(5):
   weight=dp.get((i,count),0)
   for j in edges[i]:dp[j,count+1]=dp.get((j,count+1),0)+weight
 counts={str(n):dp.get((len(text),n),0) for n in range(2,6)}
 return dict(total=sum(counts.values()),counts_by_output_words=counts,complete_split_DAG=edges,word_count_bound=[2,5])

def construct_cover(lane,message):
 m=lane.model
 for fixed,groups,length,t in lane.templates:
  if length!=len(message) or any(message[i]!=v for i,v in fixed):continue
  if not all(m.run_count(n,r,start,message[a:b],lane.k,lane.N,lane.phase) for n,r,start,a,b in groups):continue
  words=[]
  for idx,(n,r,start,a,b) in enumerate(groups):
   piece=message[a:b];used=0
   for j in range(r):
    chosen=None;selected=(start+j)%lane.N==lane.phase
    for w in m.vocab:
     if selected and (len(w)<lane.k or used>=len(piece) or w[lane.k-1]!=piece[used]):continue
     tail=piece[used+int(selected):]
     if n>=len(w) and m.run_count(n-len(w),r-j-1,start+j+1,tail,lane.k,lane.N,lane.phase):chosen=w;break
    if chosen is None:raise AssertionError('constructive DP disagreement')
    words.append(chosen);n-=len(chosen);used+=int(selected)
   assert n==0 and used==len(piece)
   if idx<2:words.extend(m.a if idx==0 else m.b)
  assert len(''.join(words))==m.total and c.extract(words,lane.k,lane.N,lane.phase)==message
  return words
 return None

def census(path,lanes,output,seconds=300,rss_cap=512*1024**2,saved_cap=64*1024**2):
 names=validate_brown(path);clock=time.monotonic();bank={};vocabulary=set();lane_by_len=collections.defaultdict(list)
 for idx,lane in enumerate(lanes):
  for n in lane.lengths:lane_by_len[n].append((idx,lane))
 counts=collections.Counter();matched_counts=collections.Counter();first={};members=[];started=utc();complete=True;last=None;reason=None
 def classify(text):
  values=[];mask=0
  for idx,lane in lane_by_len.get(len(text),[]):
   number=lane.count(text)
   if number:mask|=1<<idx;values.append((idx,number))
  return mask,values
 cache=functools.lru_cache(maxsize=4096)(classify)
 with zipfile.ZipFile(path) as z,gzip.open(output,'wt',encoding='utf-8') as f:
  for filename in names:
   raw=z.read(filename);members.append(dict(path=filename,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
   for line_no,line in enumerate(raw.decode('ascii').splitlines()):
    if not line.strip():continue
    counts['nonempty_sentence_lines']+=1;tokens=parse_line(line);vocabulary.update(x for x in tokens if x is not None);counts['tagged_tokens']+=len(tokens)
    for start,nwords,words in windows(tokens):
     counts['all_windows_2_to_5']+=1;text=''.join(words)
     if len(text) not in lane_by_len:continue
     counts['length_eligible_windows']+=1;new=text not in bank
     if new:mask,values=cache(text);bank[text]=mask
     else:mask=bank[text];values=cache(text)[1] if mask else []
     if not mask:continue
     counts['matched_window_occurrences']+=1
     if new:counts['unique_matched_letter_strings']+=1
     ref=dict(file=filename,line_zero_based=line_no,start_token_zero_based=start,output_words=nwords,joined_sha256=hashlib.sha256(text.encode()).hexdigest())
     f.write(json.dumps(dict(source=ref,model_bitmask=str(mask),cover_counts={str(i):n for i,n in values}),separators=(',',':'))+'\n')
     for i,number in values:
      matched_counts[lanes[i].id]+=1;group=(lanes[i].model.name,lanes[i].stratum)
      if group not in first:first[group]=(i,ref,text)
    last=dict(file=filename,line_zero_based=line_no)
    if counts['nonempty_sentence_lines']%100==0:
     peak=rss_bytes()
     if time.monotonic()-clock>seconds or peak>rss_cap:complete=False;reason='time' if time.monotonic()-clock>seconds else 'RSS';break
   f.flush()
   if Path(output).stat().st_size>saved_cap:complete=False;reason='saved payload budget'
   if not complete:break
 summary=dict(kind='Complete Brown windows feasibility' if complete else 'Resource-incomplete Brown windows; no negative conclusion',started_at_utc=started,finished_at_utc=utc(),elapsed_seconds=time.monotonic()-clock,peak_rss_bytes=rss_bytes(),complete=complete,incomplete_reason=reason,last_completed_unit=last,counts=dict(counts),unique_length_eligible_messages=len(bank),vocabulary_size=len(vocabulary),matched_occurrences_by_lane=dict(matched_counts),member_hashes=members,source_zip_sha256=BROWN_SHA,output_sha256=hashlib.sha256(Path(output).read_bytes()).hexdigest(),output_bytes=Path(output).stat().st_size,real_K4_cipher_trials=0,not_a_decryption=True)
 return summary,bank,vocabulary,first

def utc():
 import datetime
 return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rss_bytes():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
