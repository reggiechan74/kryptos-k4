"""Exact adaptive bitmap / sorted u32 little-endian cipher-start sets."""
import array,copy,itertools,struct,sys
import sigaba_joint_toy as toy
class Domain:
 __slots__=('payload','kind','count','_hash','policy')
 def __setattr__(self,name,value):raise AttributeError('immutable exact set')
 def _init(self,payload,kind,count,value_hash,policy):
  for k,v in [('payload',payload),('kind',kind),('count',count),('_hash',value_hash),('policy',policy)]:object.__setattr__(self,k,v)
 @staticmethod
 def bitmap_size(highest):return sys.getsizeof(0)+(max(0,highest)//sys.int_info.bits_per_digit)*sys.int_info.sizeof_digit
 def __init__(self,bits,policy='auto'):
  if not isinstance(bits,int) or bits<0 or policy not in ('auto','bitmap','packed'):raise ValueError('exact nonnegative bitmap and declared representation required')
  count=bits.bit_count() if hasattr(int,'bit_count') else bin(bits).count('1');packed=policy=='packed' or (policy=='auto' and 4*count+sys.getsizeof(b'')<sys.getsizeof(bits))
  if packed:
   ids=self._bitmap_ids(bits);values=array.array('I',ids)
   if values.itemsize!=4:raise ValueError('u32 unavailable')
   if sys.byteorder!='little':values.byteswap()
   self._init(values.tobytes(),'u32le',count,hash(bits),policy)
  else:self._init(bits,'bitmap',count,hash(bits),policy)
 @staticmethod
 def _bitmap_ids(bits):
  raw=bits.to_bytes((bits.bit_length()+7)//8,'little')
  for offset in range(0,len(raw),8):
   word=int.from_bytes(raw[offset:offset+8],'little')
   while word:
    bit=word&-word;yield offset*8+bit.bit_length()-1;word-=bit
 @classmethod
 def from_ids(cls,ids,policy='auto'):
  values=array.array('I');last=-1;value_hash=0;P=sys.hash_info.modulus;period=P.bit_length();mersenne=P==(1<<period)-1
  for index in ids:
   if not isinstance(index,int) or not(last<index<2**32):raise ValueError('sorted unique u32 state IDs required')
   values.append(index);last=index;value_hash+=(1<<(index%period)) if mersenne else pow(2,index,P)
  count=len(values);packed=policy=='packed' or (policy=='auto' and 4*count+sys.getsizeof(b'')<cls.bitmap_size(last))
  if policy not in ('auto','bitmap','packed'):raise ValueError('unknown representation policy')
  if packed:
   if values.itemsize!=4:raise ValueError('u32 unavailable')
   if sys.byteorder!='little':values.byteswap()
   out=object.__new__(cls);out._init(values.tobytes(),'u32le',count,value_hash%P,policy);return out
  raw=bytearray((last+8)//8)
  for index in values:raw[index//8]|=1<<(index%8)
  return cls(int.from_bytes(raw,'little'),policy)
 def __hash__(self):return self._hash
 def __bool__(self):return bool(self.count)
 def __eq__(self,other):
  if not isinstance(other,Domain):return NotImplemented
  if self.count!=other.count:return False
  if self.kind==other.kind:return self.payload==other.payload
  return all(x==y for x,y in itertools.zip_longest(self.ids(),other.ids(),fillvalue=-1))
 def ids(self):
  if self.kind=='bitmap':yield from self._bitmap_ids(self.payload)
  else:
   for (index,) in struct.iter_unpack('<I',self.payload):yield index
 def to_bits(self):
  if self.kind=='bitmap':return self.payload
  if not self.count:return 0
  last=struct.unpack_from('<I',self.payload,len(self.payload)-4)[0];raw=bytearray(last//8+1)
  for index in self.ids():raw[index//8]|=1<<(index%8)
  return int.from_bytes(raw,'little')
 def meet_bitmap(self,mask):
  if self.kind=='bitmap':return Domain(self.payload&mask,self.policy)
  raw=mask.to_bytes((mask.bit_length()+7)//8,'little')
  return Domain.from_ids((i for i in self.ids() if i//8<len(raw) and raw[i//8]>>(i%8)&1),self.policy)
 def intersect(self,delta,p,c,model,predicate,budget):
  if self.kind=='bitmap':return self.meet_bitmap(predicate.get(delta,p,c)),0
  kept=[];checked=0
  for index in self.ids():
   budget.check();seed=toy.unpack(index,model.q,model.r);x=p
   for j,s in enumerate(seed):x=model.cf[j][(s+delta[j])%model.q][x]
   checked+=1
   if x==c:kept.append(index)
  return Domain.from_ids(kept,self.policy),checked
 def preimage(self,delta,model,predicate,budget):
  if not any(delta):return self
  if self.kind=='bitmap':return Domain(predicate.translate(self.payload,delta),self.policy)
  original=[]
  for index in self.ids():
   budget.check();seed=toy.unpack(index,model.q,model.r);value=0
   for s,d in zip(seed,delta):value=value*model.q+(s-d)%model.q
   original.append(value)
  return Domain.from_ids(sorted(original),self.policy)
 def encode(self):return dict(encoding='bitmaphex' if self.kind=='bitmap' else 'u32lehex',data=hex(self.payload) if self.kind=='bitmap' else self.payload.hex(),cardinality=self.count)
 @classmethod
 def decode(cls,encoded):
  if encoded['encoding']=='bitmaphex':out=cls(int(encoded['data'],16))
  elif encoded['encoding']=='u32lehex':
   raw=bytes.fromhex(encoded['data'])
   if len(raw)%4:raise ValueError('bad u32 framing')
   out=cls.from_ids((x[0] for x in struct.iter_unpack('<I',raw)))
  else:raise ValueError('unknown exact encoding')
  if out.count!=encoded['cardinality']:raise ValueError('cardinality mismatch')
  return out

def legacy(result):
 """Explicit tiny-set verifier adapter; do not expand real outputs silently."""
 out=copy.deepcopy(result)
 for row in out['relations']:
  for rel in row['relations']:
   rel['cipher_starts']=hex(Domain.decode(rel['cipher_domain']).to_bits())
 return out
