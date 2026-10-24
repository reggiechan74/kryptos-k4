import hashlib,itertools,json,time,unittest,io
from pathlib import Path
from one_edit_channel import AZ,WINDOWS,ALIGNMENTS,edits,repair,index_maps,forward,anchors,mask,catalog
from one_edit_models import MODELS,periodic_crypt,select,budget
from one_edit_reference import tagged,reflected_forward,raw_string_set,tiny_controls,audit_periodic_instances,fixed_table_crypt
ROOT=Path(__file__).resolve().parents[1]

def convention_controls():
 from strategy_followup import construction_audit
 c=construction_audit();assert c['K1']['exact63_cipher_match'] and c['K2']['exact_deletion_reproduction']
 import sys
 sys.path.insert(0,str(ROOT/'independent/2026-10-22/construction'))
 from test_audit_construction import ConventionTests
 result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(ConventionTests));assert result.wasSuccessful()
 return dict(K1_full63_cipher_match=True,K2_restored_deletion_exact=True,offline_original_convention_tests=result.testsRun,CP_restart_phase_jump_identifiability_preserved=True,new_full1133_source_fetch_or_replay=False)


def controls():
 start=time.monotonic();conventions=convention_controls();tiny=tiny_controls();n=0
 # Not K4: unrelated fixed 97-letter sample for all 5071 descriptions.
 observed=(AZ*4)[:97]
 for e in edits(observed):
  latent,o,l=tagged(observed,e);assert repair(observed,e)==latent;assert index_maps(97,e)==(o,l);assert forward(latent,e)==observed;assert reflected_forward(latent,e)==observed;n+=1
 assert n==5071
 tiny_sets=0
 for length in range(1,5):
  for xs in itertools.product('AB',repeat=length):
   text=''.join(xs);native={repair(text,e) for e in edits(text,'AB')};assert native==raw_string_set(text,'AB');tiny_sets+=1
 roundtrips=0
 for m in MODELS:
  key=[(7*j+3)%26 for j in range(m['period'])]
  for length in (96,97,98):
   plain=(AZ*4)[:length];cipher=periodic_crypt(plain,key,m);assert periodic_crypt(cipher,key,m,True)==plain;assert fixed_table_crypt(plain,key,m)==cipher;assert fixed_table_crypt(cipher,key,m,True)==plain;roundtrips+=1
 positions=(0,21,22,33,34,63,74,97);plants=[];filler='THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG'
 for j,(kind,requested) in enumerate(itertools.product(('substitute','insert_latent','delete_observed'),positions)):
  pos=min(requested,96) if kind!='insert_latent' else requested;N=98 if kind=='insert_latent' else 96 if kind=='delete_observed' else 97
  e=dict(kind=kind,position=pos,latent_char='A',observed_char='Z');alignment=ALIGNMENTS[j%2];starts,reason=anchors(97,e,alignment)
  rejected_transport=reason
  if reason:alignment='ENGLISH_FIXED';starts,_=anchors(97,e,alignment)
  plain=list((filler*4)[:N])
  for i,p in mask(starts).items():plain[i]=p
  plain=''.join(plain);mi=j*47//23;m=MODELS[mi];key=[(7*i+3)%26 for i in range(m['period'])];latent=periodic_crypt(plain,key,m)
  if kind=='substitute':e.update(latent_char=latent[pos],observed_char=AZ[(AZ.index(latent[pos])+1)%26])
  if kind=='insert_latent':e.update(latent_char=latent[pos],observed_char=None)
  if kind=='delete_observed':e.update(latent_char=None,observed_char='Z')
  observed=forward(latent,e);assert len(observed)==97 and repair(observed,e)==latent
  selected=select(observed,start=start,seconds=180);audit=audit_periodic_instances(selected);truth=[]
  for row in selected['complete_periodic_fits']:
   instance=selected['catalog']['instances'][row['instance_id']]
   if row['model_index']!=mi or row['key_at_absolute_latent_position_zero']!=key or row['plaintext']!=plain:continue
   for alias in instance['aliases']:
    actual=selected['catalog']['descriptions'][alias['edit_id']]
    if alias['alignment']==alignment and all(actual[k]==v for k,v in e.items()):truth.append(dict(instance_id=instance['instance_id'],edit_id=alias['edit_id']))
  assert truth
  plants.append(dict(kind=kind,position_zero_based=pos,requested_position=requested,alignment=alignment,transport_inadmissibility_if_any=rejected_transport,model_index=mi,key=key,truth_aliases=truth,full_periodic_compatible_records=selected['complete_periodic_fits'],distinct_periodic_plaintexts=selected['distinct_periodic_full_plaintexts'],reference_audit=audit))
  budget(start,180)
 return dict(status='passed',conventions=conventions,tiny=tiny,all_raw_channel_maps_checked=n,complete_tiny_edit_sets=tiny_sets,fixed_periodic_roundtrips=roundtrips,independent_fixed_table_checks=roundtrips,plants=plants,elapsed_seconds=time.monotonic()-start)
