"""054 exact crib-first running-key search. No canonical target is embedded."""
from pathlib import Path
from dataclasses import dataclass
from array import array
import hashlib,json,re,sys,base64,random
ROOT=Path(__file__).resolve().parent
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';KR=''.join(dict.fromkeys('KRYPTOS'+AZ));ALPHABETS={'AZ':AZ,'KR':KR}
CRIBS=((21,'EASTNORTHEAST'),(63,'BERLINCLOCK'))
OPERATIONS=('vigenere','beaufort','variant_beaufort')
@dataclass(frozen=True)
class Tableau:
    plain_alphabet:str
    cipher_alphabet:str
    operation:str
    @property
    def id(self):return f'{self.plain_alphabet}-{self.cipher_alphabet}-{self.operation}'
TABLEAUX=tuple(Tableau(p,c,o) for p in ALPHABETS for c in ALPHABETS for o in OPERATIONS)
BY_ID={t.id:t for t in TABLEAUX}
def sha_file(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_json(path):return json.loads(Path(path).read_text())
def write_json(path,obj):Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def rng_for(label):return random.Random(int.from_bytes(hashlib.sha256(('candidate-first-054-v1|'+label).encode()).digest(),'big'))
def valid_text(s):
    if len(s)!=97 or any(c not in AZ for c in s):raise ValueError('Exactly97A-Z letters required')
    return s

def body_bounds(raw,kind):
    if kind=='nltk_gutenberg':
        first,sep,_=raw.partition(b'\n')
        return (len(first)+len(sep),len(raw)) if first.strip().startswith(b'[') and first.strip().endswith(b']') else (0,len(raw))
    if kind=='nltk_inaugural':return 0,len(raw)
    if kind=='project_gutenberg':
        pattern=rb'^\*\*\*[ \t]*(START|END) OF (?:THE|THIS) PROJECT GUTENBERG[^\r\n]*\*\*\*[ \t]*\r?$'
        matches=list(re.finditer(pattern,raw,re.M|re.I));starts=[m for m in matches if m.group(1).upper()==b'START'];ends=[m for m in matches if m.group(1).upper()==b'END']
        if len(starts)!=1 or len(ends)!=1 or starts[0].end()>=ends[0].start():raise ValueError('Missing/ambiguous/reversed PG marker lines')
        start=starts[0].end()
        if start<len(raw) and raw[start:start+1]==b'\n':start+=1
        return start,ends[0].start()
    if kind=='synthetic':return 0,len(raw)
    raise ValueError('Unknown body extraction kind')

def normalize_with_offsets(raw,kind):
    start,end=body_bounds(raw,kind);offsets=array('I');letters=bytearray()
    if offsets.itemsize!=4:raise ValueError('Platform unsigned int is not uint32')
    for i in range(start,end):
        b=raw[i]
        if 65<=b<=90 or 97<=b<=122:letters.append(b-32 if b>=97 else b);offsets.append(i)
    if len(raw)>=2**32:raise ValueError('Raw source too large for recorded offset representation')
    stable=array('I',offsets)
    if sys.byteorder!='little':stable.byteswap()
    info={'body_start':start,'body_end':end,'body_sha256':hashlib.sha256(raw[start:end]).hexdigest(),
          'normalized_letters':len(letters),'normalized_sha256':hashlib.sha256(letters).hexdigest(),
          'offsets_uint32_le_sha256':hashlib.sha256(stable.tobytes()).hexdigest(),'removed_spans':[[0,start],[end,len(raw)]]}
    return bytes(letters),offsets,info

def encrypt(plaintext,key,t):
    valid_text(plaintext);valid_text(key);pa=ALPHABETS[t.plain_alphabet];ca=ALPHABETS[t.cipher_alphabet];out=[]
    for a,k in zip(plaintext,key):
        p,q=pa.index(a),pa.index(k)
        c=(p+q)%26 if t.operation=='vigenere' else (q-p)%26 if t.operation=='beaufort' else (p-q)%26
        out.append(ca[c])
    return ''.join(out)

def decrypt(ciphertext,key,t):
    valid_text(ciphertext);valid_text(key);pa=ALPHABETS[t.plain_alphabet];ca=ALPHABETS[t.cipher_alphabet];out=[]
    for a,k in zip(ciphertext,key):
        c,q=ca.index(a),pa.index(k)
        p=(c-q)%26 if t.operation=='vigenere' else (q-c)%26 if t.operation=='beaufort' else (c+q)%26
        out.append(pa[p])
    return ''.join(out)

def derive_fragments(ciphertext,t,cribs=CRIBS):
    valid_text(ciphertext);pa=ALPHABETS[t.plain_alphabet];ca=ALPHABETS[t.cipher_alphabet];parts=[]
    for start,word in cribs:
        chars=[]
        for pch,cch in zip(word,ciphertext[start:start+len(word)]):
            p,c=pa.index(pch),ca.index(cch)
            q=(c-p)%26 if t.operation=='vigenere' else (c+p)%26 if t.operation=='beaufort' else (p-c)%26
            chars.append(pa[q])
        parts.append(''.join(chars))
    return tuple(parts)

@dataclass
class Document:
    id:str
    raw:bytes
    normalized:bytes
    offsets:array
    metadata:dict
    @classmethod
    def from_bytes(cls,document_id,raw,kind='synthetic',metadata=None):
        norm,offsets,info=normalize_with_offsets(raw,kind)
        return cls(document_id,raw,norm,offsets,{**(metadata or {}),**info,'raw_sha256':hashlib.sha256(raw).hexdigest(),'extraction_kind':kind})

def load_corpus(root=ROOT):
    manifest=read_json(root/'corpus_manifest.json');documents=[]
    for rec in manifest['accepted_documents']:
        doc=Document.from_bytes(rec['document_id'],(root/rec['raw_path']).read_bytes(),rec['extraction_kind'],rec)
        for k in ('raw_sha256','body_sha256','normalized_sha256','normalized_letters','offsets_uint32_le_sha256','body_start','body_end'):
            if doc.metadata[k]!=rec[k]:raise ValueError('Corpus normalization/source mismatch: '+rec['document_id']+' '+k)
        documents.append(doc)
    return documents

def all_occurrences(haystack,needle):
    start=0
    while True:
        at=haystack.find(needle,start)
        if at<0:return
        yield at;start=at+1

def locate_pairs(doc,first,second,spacing=42):
    first=first.encode() if isinstance(first,str) else first;second=second.encode() if isinstance(second,str) else second
    valid=[];rejected=[];first_count=0;pair_count=0
    for at in all_occurrences(doc.normalized,first):
        first_count+=1
        if doc.normalized[at+spacing:at+spacing+len(second)]!=second:continue
        pair_count+=1;start=at-21
        if start<0 or start+97>len(doc.normalized):rejected.append({'first_fragment_start':at,'window_start':start,'insufficient_prefix':start<0,'insufficient_suffix':start+97>len(doc.normalized)})
        else:valid.append(start)
    return {'valid_starts':valid,'boundary_rejected_pairs':rejected,'first_fragment_occurrences':first_count,'spaced_pairs_before_boundary_check':pair_count}

def independent_positions(doc,first,second):
    """Reference searches the SECOND fragment and independently checks geometry."""
    a,b=first.encode(),second.encode();out=[]
    for right in all_occurrences(doc.normalized,b):
        left=right-42;window=right-63
        if left>=0 and doc.normalized[left:left+13]==a and window>=0 and window+96<len(doc.normalized):out.append(window)
    return out

def independent_reconstruction(ciphertext,key,t):
    """Separate arithmetic implementation, without encrypt/decrypt helpers."""
    alph=(AZ,KR);pi=alph[t.plain_alphabet=='KR'];ci=alph[t.cipher_alphabet=='KR'];c=[ci.index(x) for x in ciphertext];q=[pi.index(x) for x in key]
    if t.operation=='vigenere':plain=[(x-y)%26 for x,y in zip(c,q)];back=[(x+y)%26 for x,y in zip(plain,q)]
    elif t.operation=='beaufort':plain=[(y-x)%26 for x,y in zip(c,q)];back=[(y-x)%26 for x,y in zip(plain,q)]
    elif t.operation=='variant_beaufort':plain=[(x+y)%26 for x,y in zip(c,q)];back=[(x-y)%26 for x,y in zip(plain,q)]
    else:raise ValueError('Unknown operation')
    return ''.join(pi[x] for x in plain),''.join(ci[x] for x in back)

def make_hit(doc,start,ciphertext,t,fragments):
    key=doc.normalized[start:start+97].decode();plain=decrypt(ciphertext,key,t);refplain,refcipher=independent_reconstruction(ciphertext,key,t)
    checks={'full_length':len(key)==97,'full_reencryption':encrypt(plain,key,t)==ciphertext,'independent_plaintext_equal':refplain==plain,
            'independent_reencryption':refcipher==ciphertext,'cribs_exact':all(plain[s:s+len(w)]==w for s,w in CRIBS)}
    if not all(checks.values()):raise AssertionError('Hit reconstruction correctness failed')
    begin,end=doc.offsets[start],doc.offsets[start+96]+1;context_start=max(doc.metadata['body_start'],begin-120);context_end=min(doc.metadata['body_end'],end+120)
    reconstructed=bytes(b-32 if 97<=b<=122 else b for b in doc.raw[begin:end] if 65<=b<=90 or 97<=b<=122).decode()
    if reconstructed!=key:raise AssertionError('Raw-offset normalization failed')
    return {'document_id':doc.id,'tableau_id':t.id,'window_start':start,'window_end':start+97,'first_fragment_start':start+21,'second_fragment_start':start+63,
            'fragments':list(fragments),'key':key,'plaintext':plain,'raw_start':begin,'raw_end':end,
            'raw_excerpt_utf8_replacement':doc.raw[begin:end].decode('utf8',errors='replace'),'raw_excerpt_base64':base64.b64encode(doc.raw[begin:end]).decode(),
            'context_raw_start':context_start,'context_raw_end':context_end,'source_context_utf8_replacement':doc.raw[context_start:context_end].decode('utf8',errors='replace'),
            'raw_sha256':doc.metadata['raw_sha256'],'normalized_sha256':doc.metadata['normalized_sha256'],
            'historical_transcription_uncertainty':doc.metadata.get('historical_transcription_uncertainty'),
            'crossed_uncertified_compilation_boundaries':[b for b in doc.metadata.get('uncertified_compilation_boundaries',[]) if start<b['normalized_offset']<start+97],
            'historical_source_status':'modern-transcription candidate; historical cross-work adjacency unverified' if any(start<b['normalized_offset']<start+97 for b in doc.metadata.get('uncertified_compilation_boundaries',[])) else 'Exact historical passage wording still requires independent verification',
            'checks':checks}

def search_all(ciphertext,documents,verify_reference=True):
    valid_text(ciphertext);hits=[];boundary=[];coverage=[];queries=[]
    for t in TABLEAUX:
        fragments=derive_fragments(ciphertext,t);queries.append({'tableau_id':t.id,'first_fragment':fragments[0],'second_fragment':fragments[1],'start_spacing':42})
        for doc in documents:
            found=locate_pairs(doc,*fragments)
            if verify_reference and found['valid_starts']!=independent_positions(doc,*fragments):raise AssertionError('Complete hit-set reference disagreement')
            for start in found['valid_starts']:hits.append(make_hit(doc,start,ciphertext,t,fragments))
            for rejected in found['boundary_rejected_pairs']:boundary.append({'document_id':doc.id,'tableau_id':t.id,**rejected})
            coverage.append({'document_id':doc.id,'tableau_id':t.id,'normalized_letters':len(doc.normalized),'valid_97_window_count':max(0,len(doc.normalized)-96),
                             'first_fragment_occurrences':found['first_fragment_occurrences'],'spaced_pairs_before_boundary_check':found['spaced_pairs_before_boundary_check'],
                             'valid_hit_count':len(found['valid_starts']),'boundary_rejection_count':len(found['boundary_rejected_pairs'])})
    hits.sort(key=lambda x:(x['tableau_id'],x['document_id'],x['window_start']));boundary.sort(key=lambda x:(x['tableau_id'],x['document_id'],x['first_fragment_start']))
    return {'queries':queries,'hits':hits,'boundary_rejected_pairs':boundary,'coverage':coverage,'hit_count':len(hits),
            'document_count':len(documents),'tableau_count':12,'full_reference_hit_set_checked':verify_reference,
            'interpretation':'Deterministic frozen-corpus exact lookup, no statistical p-value; unrestricted key roundtrip is correctness only.'}
