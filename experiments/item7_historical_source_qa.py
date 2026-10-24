"""Replay source arithmetic with explicit partial-inventory and metadata limits."""
import contextlib,hashlib,io,json,tempfile,time
from datetime import datetime,timezone
from pathlib import Path
from strip_source_gates import ROOT,AZ,validate_strips,observations
from strip_inventory_admission import inspect_inventory
import wheatstone_transition as wheatstone
SOURCE=ROOT/'independent/2026-10-24/item7-historical-sources'

def m138_figure():
 d=json.loads((SOURCE/'visual-transcription.json').read_text());rows=d['verified_strips'];assert len(rows)==24
 admitted=inspect_inventory([dict(id=k,literal=v) for k,v in rows.items()],'M138-1935-24-visible-rows-only','NSA-A67592')
 complete=dict(rows);complete['1']=d['strip_1_visible_literal'];strips=[complete[str(n)] for n in d['figure4_key']]
 try:validate_strips(strips)
 except ValueError as error:reason=str(error)
 else:raise AssertionError('partial source must fail complete permutation gate')
 forward=[];inverse=[];trace=[]
 for i,(number,p,c) in enumerate(zip(d['figure4_key'],d['figure4_plaintext'],d['figure4_ciphertext_right_guide_edge'])):
  row=complete[str(number)]
  position=d['figure4_strip_1_plaintext_occurrence_one_based']-1 if number==1 else row.index(p)
  assert row[position]==p
  result=row[(position+d['figure4_offset'])%26];assert result==c;forward.append(result)
  assert row.count(c)==1
  decoded=row[(row.index(c)-d['figure4_offset'])%26];assert decoded==p;inverse.append(decoded)
  trace.append(dict(column=i+1,strip_number=number,plaintext=p,ciphertext=c,plaintext_position_one_based=position+1,offset=d['figure4_offset'],uses_source_occurrence_not_first_duplicate=(number==1)))
 assert ''.join(forward)==d['figure4_ciphertext_right_guide_edge'];assert ''.join(inverse)==d['figure4_plaintext']
 return dict(kind='partial_photographic_column_source_QA_not_complete_cipher_inventory',verified_permutations=24,complete_inventory_admitted=False,complete_gate_error=reason,unresolved_strip_literal=d['strip_1_visible_literal'],source_occurrence_from_figure=d['figure4_strip_1_plaintext_occurrence_one_based'],computed_ciphertext=''.join(forward),recovered_plaintext=''.join(inverse),trace=trace,source_pdf_sha256_worker_declared_not_verified_locally=d['source_sha256'])

def partial_wheatstone():
 d=json.loads((SOURCE/'friedman-reference-source-qa.json').read_text());outer=d['outer_clockwise'];inner=d['inner_clockwise_from_A_with_occlusion'];o=outer.index('G');q=inner.index('A');trace=[]
 for i,p in enumerate(d['plaintext']):
  target=outer.index(p);step=(target-o)%27;assert step>0;q=(q+step)%26;c=inner[q];assert c!='?';trace.append(dict(position=i+1,plain=p,steps=step,inner_index=q,cipher=c));o=target
 cipher=''.join(r['cipher'] for r in trace);assert cipher==d['printed_decipherment_string'];assert trace==d['forward_trace'];assert cipher!=d['printed_encipherment_string']
 o=outer.index('G');q=inner.index('A');inverse=[]
 for i,c in enumerate(cipher):
  assert inner.count(c)==1;target=inner.index(c);step=(target-q)%26 or 26;o=(o+step)%27;q=target;inverse.append(dict(position=i+1,cipher=c,steps=step,plain=outer[o]))
 assert inverse==d['inverse_trace']
 try:validate_strips([inner])
 except ValueError:partial_rejected=True
 else:raise AssertionError('source literal with ? must not authenticate full ring')
 # Explicit separate inference, never an edit to the original transcription.
 missing=set(AZ)-set(inner);assert missing=={'W'};completed=inner.replace('?','W')
 args=(outer,completed,outer.index('G'),completed.index('A'))
 assert wheatstone.crypt(d['plaintext'],*args)[0]==cipher
 assert wheatstone.crypt(cipher,*args,True)[0]==d['plaintext']
 assert wheatstone.tooth_oracle(d['plaintext'],*args)==cipher
 return dict(kind='historical_known_answer_on_visible_slots_not_new_K4_or_Plett_test',computed_ciphertext=cipher,recovered_plaintext=''.join(r['plain'] for r in inverse),forward_trace=trace,inverse_trace=inverse,preserved_conflicting_forward_string=d['printed_encipherment_string'],preserved_partial_inner=inner,source_literal_rejected_by_complete_gate=partial_rejected,occluded_slot_used=False,production_engine_matches_with_explicit_inferred_completion=True,inferred_completion='W',inferred_completion_visually_authenticated=False)

def replay_original():
 source=(SOURCE/'friedman_reference_source_qa.py').read_text();d=json.loads((SOURCE/'friedman-reference-source-qa.json').read_text())
 with tempfile.TemporaryDirectory() as temp:
  substitutions={"base=Path('/workspace/shared/item7-historical-sources')":'base=Path('+repr(temp)+')',"(base/'friedman-legacy-2006.pdf').stat().st_size":str(d['source_pdf_bytes']),"hashlib.sha256((base/'friedman-legacy-2006.pdf').read_bytes()).hexdigest()":repr(d['source_pdf_sha256'])}
  adapted=source
  for old,new in substitutions.items():assert adapted.count(old)==1;adapted=adapted.replace(old,new)
  with contextlib.redirect_stdout(io.StringIO()):exec(compile(adapted,'<temporary-source-QA-replay>','exec'),{'__name__':'__source_replay__'})
  fresh=json.loads((Path(temp)/'friedman-reference-source-qa.json').read_text());assert fresh==d
 return dict(arithmetic_receipt_equal=True,original_source_sha256=hashlib.sha256(source.encode()).hexdigest(),temporary_adapter_sha256=hashlib.sha256(adapted.replace(temp,'<temporary-output-directory>').encode()).hexdigest(),adapter_changes=['temporary output path','PDF byte count supplied from worker receipt','PDF hash supplied from worker receipt'],source_pdf_binary_rehashed_locally=False,original_source_unchanged=True)

def source_conditioned_certificate():
 cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];first=observations(cipher);known=observations(cipher,((21,'EASTNORTHEAST'),(63,'BERLINCLOCK')));fixed=[r for r in known if r['fixed']]
 assert [r['position'] for r in fixed]==[33,74]
 return dict(kind='source_conditioned_reuse_of_cyclic_permutation_fixed_point_proof',rule='SIGUHR-2 July1943 forbids zero and twenty-six intervals; valid permutation strips only.',first_crib_sufficient=any(r['fixed'] for r in first),first_witness=next(r for r in first if r['fixed']),additional_public_fixed_point=fixed[1],inventory_enumerations=0,new_held_out_evidence=False,full_M138A_inventory_authenticated=False,coverage='Direct literal aligned nonzero cyclic strip operations, including differing nonzero offsets by subgroup/column; no general layered-M138 exclusion.',unexcluded=['zero shifts outside the separately proved common-block relaxation','changed processed alignment','outer substitution or route','non-permutation alphabets','other historically modified rules'])

def run():
 started=datetime.now(timezone.utc).isoformat();clock=time.monotonic();out=dict(kind='post_source_historical_QA_and_scoped_proof_not_key_search',m138=m138_figure(),wheatstone=partial_wheatstone(),original_script_replay=replay_original(),source_conditioned=source_conditioned_certificate(),local_visual_verification='SRH366 physicalPDF101-102 only; other visual transcription attributed to worker',started_at_utc=started)
 out.update(finished_at_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),SOURCE/'visual-transcription.json',SOURCE/'friedman_reference_source_qa.py',SOURCE/'friedman-reference-source-qa.json')});return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
