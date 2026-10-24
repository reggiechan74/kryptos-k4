"""Legacy .Z plus fixed whole-integer A-Z transports. No fitted alphabet or cipher."""
import datetime,hashlib,itertools,json,random,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ALPHABETS={'AZ':'ABCDEFGHIJKLMNOPQRSTUVWXYZ','KRYPTOS':'KRYPTOSABCDEFGHIJLMNQUVWXZ'}
def versions():return [(a,b,r) for a in ALPHABETS for b in (0,1) for r in (False,True)]
def encode(raw,alphabet,bijective=False,reverse=False):
 if not raw or raw[0]==0:raise ValueError('Minimal big-endian byte domain required')
 n=int.from_bytes(raw,'big');out=[]
 while n:
  n,d=divmod(n-int(bijective),26);out.append(alphabet[d])
 text=''.join(out[::-1]);return text[::-1] if reverse else text

def decode(text,alphabet,bijective=False,reverse=False):
 if reverse:text=text[::-1]
 if not text or any(x not in alphabet for x in text) or not bijective and text[0]==alphabet[0]:raise ValueError('Noncanonical base26')
 n=0
 for ch in text:n=n*26+alphabet.index(ch)+int(bijective)
 if n<=0:raise ValueError('Zero byte domain')
 return n.to_bytes((n.bit_length()+7)//8,'big')
def reference_decode(text,alphabet,bijective=False,reverse=False):
 ordered=text[::-1] if reverse else text
 if not ordered or not bijective and ordered[0]==alphabet[0]:raise ValueError('Noncanonical base26')
 n=sum((alphabet.index(ch)+int(bijective))*26**j for j,ch in enumerate(ordered[::-1]));out=[]
 while n:n,byte=divmod(n,256);out.append(byte)
 if not out:raise ValueError('Zero byte domain')
 return bytes(out[::-1])
def header(raw):return len(raw)>=3 and raw[:2]==b'\x1f\x9d' and 9<=raw[2]&31<=16 and not raw[2]&0x60

def native(raw,inverse=False):
 with tempfile.TemporaryDirectory(prefix='k4-compress043-') as d:
  p=Path(d)/('input.Z' if inverse else 'input');p.write_bytes(raw);r=subprocess.run(['/usr/bin/uncompress' if inverse else '/usr/bin/compress','-f',str(p)],capture_output=True,timeout=5);out=Path(d)/('input' if inverse else 'input.Z')
  if r.returncode or not out.is_file():raise ValueError('Native codec rejection: '+r.stderr.decode(errors='replace'))
  if out.stat().st_size>2**20:raise ValueError('Native output cap')
  return out.read_bytes()

def short_lzw(raw):
 if not header(raw):raise ValueError('Bad .Z header')
 table={i:bytes([i]) for i in range(256)};nextcode=257 if raw[2]&128 else 256;bits=int.from_bytes(raw[3:],'little');available=8*(len(raw)-3);offset=0;out=[];previous=None
 while offset+9<=available:
  code=(bits>>offset)&511;offset+=9
  if code==256 and raw[2]&128:raise ValueError('CLEAR outside independent short-control domain')
  if code in table:entry=table[code]
  elif code==nextcode and previous is not None:entry=previous+previous[:1]
  else:raise ValueError('Invalid LZW code')
  out.append(entry)
  if previous is not None:table[nextcode]=previous+entry[:1];nextcode+=1
  if nextcode>=512:raise ValueError('Width change outside independent short-control domain')
  previous=entry
 if bits>>offset:raise ValueError('Nonzero final padding')
 return b''.join(out)

def evaluate(text,known):
 records=[];candidates=[]
 for name,b,r in versions():
  row=dict(alphabet=name,bijective=bool(b),reversed_letters=r)
  try:raw=decode(text,ALPHABETS[name],b,r)
  except ValueError as exc:row.update(status='transport_rejected',reason=str(exc));records.append(row);continue
  assert raw==reference_decode(text,ALPHABETS[name],b,r) and encode(raw,ALPHABETS[name],b,r)==text
  row.update(decoded_bytes=len(raw),prefix_hex=raw[:3].hex(),header_valid=header(raw))
  if not row['header_valid']:row['status']='header_rejected';records.append(row);continue
  try:
   plain=native(raw,True);letters=plain.decode('ascii');ok=len(letters)==97 and all('A'<=x<='Z' for x in letters) and all(letters[i]==v for i,v in known.items());canonical=ok and native(plain)==raw
  except (ValueError,UnicodeError) as exc:row.update(status='codec_rejected',reason=str(exc));records.append(row);continue
  row.update(status='complete_candidate' if canonical else 'plaintext_or_canonical_replay_rejected',plaintext_length=len(plain),all_English_clues=ok,canonical_replay=canonical)
  if canonical:candidates.append(dict(version=row.copy(),plaintext=letters,compressed_hex=raw.hex(),full_transport_regeneration=True))
  records.append(row)
 return dict(records=records,candidates=candidates,transport_versions=len(records),header_survivors=sum(x.get('header_valid',False) for x in records),full_candidates=len(candidates))

def controls(known_positions):
 comparisons=0
 for n in range(1,256):
  raw=bytes([n,0,255,n^255])
  for name,b,r in versions():
   text=encode(raw,ALPHABETS[name],b,r);assert decode(text,ALPHABETS[name],b,r)==raw==reference_decode(text,ALPHABETS[name],b,r);comparisons+=1
 assert native(b'A')==bytes.fromhex('1f9d904100') and short_lzw(bytes.fromhex('1f9d904100'))==b'A'
 controls=json.loads((ROOT/'data/controls.json').read_text());base=''.join(x for x in controls['k1']['plaintext'] if x in ALPHABETS['AZ']);alphabet=ALPHABETS['AZ'];source=['A'*97,(alphabet*4)[:97],(base*2)[:97]];chars=list((alphabet*4)[:97])
 for i,ch in known_positions.items():chars[i]=ch
 source.append(''.join(chars));plants=[];wrong=0
 for plain in source:
  packed=native(plain.encode());assert short_lzw(packed).decode()==plain and native(packed,True).decode()==plain;known={i:plain[i] for i in known_positions};rows=[]
  for name,b,r in versions():
   cipher=encode(packed,ALPHABETS[name],b,r);value=evaluate(cipher,known);assert any(x['plaintext']==plain and x['compressed_hex']==packed.hex() for x in value['candidates']);bad=b'\x1e'+packed[1:];assert not header(decode(encode(bad,ALPHABETS[name],b,r),ALPHABETS[name],b,r));wrong+=1;rows.append(dict(alphabet=name,bijective=bool(b),reversed_letters=r,ciphertext=cipher,full_selector=value))
  plants.append(dict(plaintext=plain,compressed_hex=packed.hex(),independent_short_LZW_equal=True,records=rows))
 # Positional leading-zero notation must not be silently accepted.
 invalid=0
 for name in ALPHABETS:
  for r in (False,True):
   text=ALPHABETS[name][0]+ALPHABETS[name][1];text=text[::-1] if r else text
   try:decode(text,ALPHABETS[name],False,r)
   except ValueError:invalid+=1
   else:raise AssertionError('noncanonical leading zero accepted')
 return dict(integer_reference_roundtrips=comparisons,known_A_vector_hex='1f9d904100',independent_short_LZW_plants=len(plants),full_selector_plants=32,mutated_magic_rejections=wrong,noncanonical_zero_rejections=invalid,plants=plants)

def run():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic();data=json.loads((ROOT/'data/k4.json').read_text());known={x['start']-1+j:v for x in data['cribs'] for j,v in enumerate(x['plaintext'])};ctrl=controls(known);actual=evaluate(data['ciphertext'],known);rng=random.Random(430024);nulls=[]
 for i in range(31):
  chars=list(data['ciphertext']);rng.shuffle(chars);value=evaluate(''.join(chars),known);nulls.append(dict(draw=i,ciphertext=''.join(chars),search=value))
  if time.monotonic()-clock>60:raise RuntimeError('Budget unresolved')
 return dict(id='COMPRESS-TRANSPORT-043',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('research/COMPRESS-TRANSPORT-043-SPEC.md','experiments/compress_transport_043.py','data/k4.json','data/controls.json')},native_binary_sha256=hashlib.sha256(Path('/usr/bin/compress').read_bytes()).hexdigest(),controls=ctrl,actual=actual,nulls=dict(seed=430024,whole_family_statistic='Number of complete canonical97letter decompressions satisfying all24English clues',records=nulls),actual_K4_transport_descriptions=8,additional_cipher_layers_tested=0,source_selected_creator_codec=False,puzzle_solved=False,Site_changed=False,pushed=False)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(started=r['started_at_utc'],finished=r['finished_at_utc'],controls={k:v for k,v in r['controls'].items() if k!='plants'},actual=r['actual'],null_full_candidates=[x['search']['full_candidates'] for x in r['nulls']['records']])))
