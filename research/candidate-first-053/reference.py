"""053 fixed language-key reference mathematics; contains no K4 ciphertext."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from array import array
import hashlib, json, math, random, sys
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KR=''.join(dict.fromkeys('KRYPTOS'+AZ))
ALPHABETS={'AZ':AZ,'KR':KR}
OPERATIONS=('vigenere','beaufort','variant_beaufort')
BLOCKS=((0,21),(34,63),(74,97))
CRIBS=((21,'EASTNORTHEAST'),(63,'BERLINCLOCK'))
KNOWN=frozenset(i for s,w in CRIBS for i in range(s,s+len(w)))
UNKNOWN=tuple(i for i in range(97) if i not in KNOWN)
BASELINE=73*math.log2(26)
GROUPS_BANK=('a_themes','b_neutral','c_berlin','d_messages')
ROOT=Path(__file__).resolve().parent

def sha256_file(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load_json(path):return json.loads(Path(path).read_text())
def write_json(path,obj):Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def normalize(raw):return bytes(b-32 if 97<=b<=122 else b for b in raw if 65<=b<=90 or 97<=b<=122)
def rng_for(label):return random.Random(int.from_bytes(hashlib.sha256(('candidate-first-053-v1|'+label).encode()).digest(),'big'))
def validate_ciphertext(s):
    if len(s)!=97 or any(c not in AZ for c in s):raise ValueError('Expected exactly97 A-Z letters')
    return s

def validate_bank(records,expected_count=1024):
    if len(records)!=expected_count:raise ValueError('Wrong bank count')
    ids=set();texts=set()
    for r in records:
        validate_ciphertext(r['text'])
        if r['id'] in ids or r['text'] in texts:raise ValueError('Duplicate candidate')
        ids.add(r['id']);texts.add(r['text'])
        if any(r['text'][s:s+len(w)]!=w for s,w in CRIBS):raise ValueError('Wrong cribs')
    if expected_count==1024 and any(sum(r['group']==g for r in records)!=256 for g in GROUPS_BANK):raise ValueError('Wrong group balance')
    return sorted(records,key=lambda r:r['id'])

@dataclass(frozen=True)
class Tableau:
    plain_alphabet:str
    cipher_alphabet:str
    operation:str
    @property
    def id(self):return f'{self.plain_alphabet}-{self.cipher_alphabet}-{self.operation}'
TABLEAUX=tuple(Tableau(p,c,o) for p in ALPHABETS for c in ALPHABETS for o in OPERATIONS)
TABLEAU_BY_ID={t.id:t for t in TABLEAUX}
def encode(text,alphabet):return tuple(ALPHABETS[alphabet].index(c) for c in text)
def decode(values,alphabet):return ''.join(ALPHABETS[alphabet][v%26] for v in values)
def forward(p,k,op):
    if op=='vigenere':return (p+k)%26
    if op=='beaufort':return (k-p)%26
    if op=='variant_beaufort':return (p-k)%26
    raise ValueError(op)
def backward(c,k,op):
    if op=='vigenere':return (c-k)%26
    if op=='beaufort':return (k-c)%26
    if op=='variant_beaufort':return (c+k)%26
    raise ValueError(op)
def derive_key(plaintext,ciphertext,t):
    p=encode(plaintext,t.plain_alphabet);c=encode(ciphertext,t.cipher_alphabet)
    if t.operation=='vigenere':q=((b-a)%26 for a,b in zip(p,c))
    elif t.operation=='beaufort':q=((a+b)%26 for a,b in zip(p,c))
    else:q=((a-b)%26 for a,b in zip(p,c))
    return decode(q,t.plain_alphabet)
def encrypt_key(plaintext,key,t):
    if len(plaintext)!=len(key):raise ValueError('Key length')
    return decode((forward(a,k,t.operation) for a,k in zip(encode(plaintext,t.plain_alphabet),encode(key,t.plain_alphabet))),t.cipher_alphabet)
def decrypt_key(ciphertext,key,t):
    if len(ciphertext)!=len(key):raise ValueError('Key length')
    return decode((backward(c,k,t.operation) for c,k in zip(encode(ciphertext,t.cipher_alphabet),encode(key,t.plain_alphabet))),t.plain_alphabet)
def conditional_nulls(ciphertext,n,label):
    validate_ciphertext(ciphertext);rng=rng_for(label);out=[]
    original=[ciphertext[i] for i in UNKNOWN]
    for j in range(n):
        values=original.copy();rng.shuffle(values);c=list(ciphertext)
        for i,v in zip(UNKNOWN,values):c[i]=v
        out.append(''.join(c))
    return out

class LanguageModel:
    def __init__(self,log_tables):
        if [len(a) for a in log_tables]!=[26**i for i in range(1,5)]:raise ValueError('Wrong model table sizes')
        self.log_tables=tuple(array('d',a) for a in log_tables)
    @classmethod
    def train(cls,documents):
        counts=[array('Q',[0])*(26**i) for i in range(1,5)]
        for doc in documents:
            values=[b-65 for b in doc]
            if any(not 0<=v<26 for v in values):raise ValueError('Train on normalized A-Z only')
            for start in range(len(values)):
                index=0
                for order in range(1,min(4,len(values)-start)+1):
                    index=index*26+values[start+order-1];counts[order-1][index]+=1
        probs=[];total=sum(counts[0]);probs.append(array('d',((x+.5)/(total+13) for x in counts[0])))
        for order,alpha in ((2,5.),(3,10.),(4,20.)):
            table=array('d',[0.])*(26**order)
            for h in range(26**(order-1)):
                denominator=sum(counts[order-1][h*26:h*26+26])+alpha
                suffix=h%(26**(order-2))
                for a in range(26):table[h*26+a]=(counts[order-1][h*26+a]+alpha*probs[-1][suffix*26+a])/denominator
            probs.append(table)
        model=cls([array('d',(math.log2(x) for x in row)) for row in probs]);return model,counts
    def log_probability(self,values,start,end):
        total=0.;context=0
        for i in range(start,end):
            order=min(4,i-start+1)
            index=context*26+values[i]
            total+=self.log_tables[order-1][index]
            context=index%(26**3)
        return total
    def score_key(self,key,n=1024):
        values=encode(key,'AZ');total=0.;context=0
        # Single sequential sum matches the native accumulation order exactly.
        for start,end in BLOCKS:
            context=0
            for i in range(start,end):
                order=min(4,i-start+1);index=context*26+values[i]
                total+=self.log_tables[order-1][index];context=index%(26**3)
        return BASELINE+total-(math.log2(n)+math.log2(12))
    def full_cross_entropy(self,key):return -self.log_probability(encode(key,'AZ'),0,len(key))/len(key)
    def block_log_probabilities(self,key):
        v=encode(key,'AZ');return [self.log_probability(v,a,b) for a,b in BLOCKS]
    def save(self,path):
        with open(path,'wb') as f:
            for row in self.log_tables:
                a=array('d',row)
                if sys.byteorder!='little':a.byteswap()
                a.tofile(f)
    @classmethod
    def load(cls,path):
        raw=Path(path).read_bytes();expected=sum(26**i for i in range(1,5))*8
        if len(raw)!=expected:raise ValueError('Wrong model bytes')
        rows=[];offset=0
        for order in range(1,5):
            size=26**order*8;a=array('d');a.frombytes(raw[offset:offset+size]);offset+=size
            if sys.byteorder!='little':a.byteswap()
            rows.append(a)
        return cls(rows)

def reference_scores(bank,ciphertext,model):
    out=[]
    for r in sorted(bank,key=lambda r:r['id']):
        for t in TABLEAUX:
            key=derive_key(r['text'],ciphertext,t)
            out.append({'candidate_id':r['id'],'tableau_id':t.id,'score_bits':model.score_key(key,len(bank)),
                        'key':key,'full_key_cross_entropy':model.full_cross_entropy(key),
                        'full_reencryption':encrypt_key(r['text'],key,t)==ciphertext,'full_inverse':decrypt_key(ciphertext,key,t)==r['text']})
    return out
