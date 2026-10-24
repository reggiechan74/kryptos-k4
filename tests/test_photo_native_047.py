import binascii,hashlib,json,struct,sys,unittest,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'experiments'))
import photo_native_047 as p
def chunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',binascii.crc32(t+d)&0xffffffff)
class NativePhotoTests(unittest.TestCase):
 def test_independent_png_scanlines_all_filter_types(self):
  rows=[bytes([1,3,8,13,21,34,55,89,144]),bytes([2,4,9,14,22,35,56,90,145])]
  for kind in range(5):
   raw=b'';prev=bytes(9)
   for row in rows:
    encoded=[]
    for i,v in enumerate(row):
     left=row[i-3] if i>=3 else 0;up=prev[i];ul=prev[i-3] if i>=3 else 0
     if kind==0:pred=0
     elif kind==1:pred=left
     elif kind==2:pred=up
     elif kind==3:pred=(left+up)//2
     else:
      estimate=left+up-ul;choices=[left,up,ul];pred=min(enumerate(choices),key=lambda q:(abs(estimate-q[1]),q[0]))[1]
     encoded.append((v-pred)%256)
    raw+=bytes([kind])+bytes(encoded);prev=row
   png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',3,2,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')
   self.assertEqual(p.decode_rgb_png(png),(3,2,rows))
   with self.assertRaises(ValueError):p.decode_rgb_png(png[:-1])
 def test_observation_boxes_never_become_endpoint_pairs(self):
  r=json.loads((p.EVIDENCE/'annotations.json').read_text());a=p.admission(r['candidate_features']);self.assertEqual(a['certified_pairs'],0);self.assertFalse(a['primary_12_pair_gate_passed']);self.assertFalse(a['fit_performed'])
  with self.assertRaises(ValueError):p.admission([dict(certified=True,native_observation_box_ltrb=[1,2,3,4])])
  plant=[dict(certified=True,aperture_native_xy=[i,1],receiver_native_xy=[i,10],endpoint_uncertainty_native_px=1,identity_evidence='synthetic known point',source_row=i%3,source_region=i%3,role='training' if i<8 else 'holdout') for i in range(12)]
  self.assertTrue(p.admission(plant)['primary_12_pair_gate_passed'])
  for a in plant:a['source_row']=0
  self.assertFalse(p.admission(plant)['primary_12_pair_gate_passed'])
 def test_protocol_precedes_inspection_and_exact_native_crop_receipt(self):
  r=json.loads((p.EVIDENCE/'annotations.json').read_text());self.assertLess(r['protocol_saved_at_utc'],r['inspection_finished_at_utc']);self.assertEqual(hashlib.sha256((ROOT/'research/PHOTO-NATIVE-047-SPEC.md').read_bytes()).hexdigest(),r['protocol_sha256']);self.assertEqual(len(r['crops']),9)
  check=json.loads((ROOT/'results/PHOTO-NATIVE-047-CROP-CHECK.json').read_text());self.assertTrue(all(c['native_rgb_exact'] for c in check['crop_checks']));self.assertEqual(len(check['crop_checks']),9)
  for c in r['crops']:
   raw=(p.EVIDENCE/c['file']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),c['sha256']);w,h,*_=struct.unpack('>IIBBBBB',raw[16:29]);l,t,right,b=c['native_rect_ltrb'];self.assertEqual((w,h),(right-l,b-t))
