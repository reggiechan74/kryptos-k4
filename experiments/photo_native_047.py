"""Native crop admission/verification, not automatic optical correspondence discovery."""
import argparse,binascii,hashlib,json,struct,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'research/evidence/2026-10-24-native-loc'
def decode_rgb_png(raw):
 if raw[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('PNG signature')
 pos=8;compressed=[];header=None;ended=False
 while pos<len(raw):
  n=struct.unpack('>I',raw[pos:pos+4])[0];typ=raw[pos+4:pos+8];data=raw[pos+8:pos+8+n];crc=raw[pos+8+n:pos+12+n]
  if len(crc)!=4 or struct.unpack('>I',crc)[0]!=(binascii.crc32(typ+data)&0xffffffff):raise ValueError('chunk CRC/truncation')
  if typ==b'IHDR':header=struct.unpack('>IIBBBBB',data)
  elif typ==b'IDAT':compressed.append(data)
  elif typ==b'IEND':ended=True;break
  pos+=12+n
 if not ended or header is None:raise ValueError('incomplete PNG')
 w,h,depth,color,comp,filt,interlace=header
 if (depth,color,comp,filt,interlace)!=(8,2,0,0,0):raise ValueError('requires noninterlaced RGB8')
 packed=zlib.decompress(b''.join(compressed));stride=w*3
 if len(packed)!=h*(stride+1):raise ValueError('scanline length')
 rows=[];prev=bytes(stride)
 for y in range(h):
  offset=y*(stride+1);kind=packed[offset];row=bytearray(packed[offset+1:offset+1+stride])
  if kind not in range(5):raise ValueError('PNG filter')
  for i in range(stride):
   if not kind:break
   a=row[i-3] if i>=3 else 0;b=prev[i];c=prev[i-3] if i>=3 else 0
   if kind==1:pred=a
   elif kind==2:pred=b
   elif kind==3:pred=(a+b)//2
   else:
    p=a+b-c;pa,pb,pc=abs(p-a),abs(p-b),abs(p-c);pred=a if pa<=pb and pa<=pc else b if pb<=pc else c
   row[i]=(row[i]+pred)&255
  rows.append(bytes(row));prev=row
 return w,h,rows
def admission(annotations):
 # Observation boxes cannot silently become material-point pairs.
 certified=[]
 for a in annotations:
  if a.get('certified'):
   for k in ('aperture_native_xy','receiver_native_xy','endpoint_uncertainty_native_px','identity_evidence'):
    if not a.get(k):raise ValueError('missing certified material-point evidence: '+k)
   if a['aperture_native_xy']==a['receiver_native_xy']:raise ValueError('zero-length pair')
   certified.append(a)
 rows={a.get('source_row') for a in certified if a.get('source_row') is not None};regions={a.get('source_region') for a in certified if a.get('source_region') is not None};train=sum(a.get('role')=='training' for a in certified);held=sum(a.get('role')=='holdout' for a in certified)
 return dict(certified_pairs=len(certified),primary_12_pair_gate_passed=len(certified)>=12 and len(rows)>=3 and len(regions)>=3 and train>=8 and held>=4,exploratory_3_train_1_holdout_possible=train>=3 and held>=1,fit_performed=False,metadata_admission_is_not_independent_identity_certification=True)
def verify(original_png):
 manifest=json.loads((EVIDENCE/'annotations.json').read_text());ow,oh,original=decode_rgb_png(Path(original_png).read_bytes());assert (ow,oh)==(3384,4283)
 checks=[]
 for c in manifest['crops']:
  raw=(EVIDENCE/c['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==c['sha256'];w,h,rows=decode_rgb_png(raw);l,t,r,b=c['native_rect_ltrb'];assert (w,h)==(r-l,b-t)
  assert all(row==original[t+i][3*l:3*r] for i,row in enumerate(rows)),c['file']
  checks.append(dict(file=c['file'],native_rgb_exact=True,dimensions=[w,h]))
 return dict(kind='Independent PNG scanline/native-coordinate crop verification; no optical fit',source_conversion_png_sha256=hashlib.sha256(Path(original_png).read_bytes()).hexdigest(),crop_checks=checks,admission=admission(manifest['candidate_features']))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--original-png',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();Path(a.output).write_text(json.dumps(verify(a.original_png),indent=2)+'\n')
