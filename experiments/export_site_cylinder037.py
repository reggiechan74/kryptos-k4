"""Lossless numeric result and per-cell margin export; no Site source archive."""
import argparse,collections,csv,datetime,gzip,hashlib,json,shutil
from pathlib import Path
import site_cylinder_validation as m
ROOT=Path(__file__).resolve().parents[1]
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def archive(source,target):
 with Path(source).open('rb') as a,Path(target).open('wb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as b:shutil.copyfileobj(a,b)
 return dict(bytes=Path(target).stat().st_size,sha256=sha(target),raw_sha256=sha(source))
def run(source,destination):
 dest=Path(destination);dest.mkdir(exist_ok=True,parents=True);r=json.loads(Path(source).read_text());n=r['stages']['replay_neighborhood'];s=r['stages']['stability'];base=n['default'];records=s['records'];metadata=archive(source,dest/'SITE-CYLINDER-037-ORIGINAL.json.gz')
 with (dest/'SITE-CYLINDER-037-DEFAULT-MARGINS.csv').open('w',newline='') as f:
  writer=csv.writer(f,lineterminator="\n");writer.writerow(('sample','reticle_row0','reticle_column0','table_display_row1','table_display_column1','key_letter','margin_pitch','U100_margin_mm','U100_guard_excess_mm','R250_margin_mm','R250_guard_excess_mm'))
  for i,(cell,letter,margin) in enumerate(zip(base['result']['cell_path'],base['result']['letters'],base['result']['margins'])):
   row,col=divmod(i+27,31);writer.writerow((i+1,row,col,cell[0],cell[1],letter,margin,margin*25,(margin-.01)*25,margin*78.125,(margin-.01)*78.125))
 axial=[]
 for row in n['neighbors']:
  diff=[k for k in m.PARAMS if row['state'][k]!=m.DEFAULTS[k]]
  if len(diff)==1:
   value=row['result'];axial.append(dict(parameter=diff[0],value=row['state'][diff[0]],floor_cell_changes=sum(a!=b for a,b in zip(base['result']['cell_path'],value['cell_path'])),admission_changes=sum(a!=b for a,b in zip(base['result']['statuses'],value['statuses'])),same_key=value['key']==base['result']['key'],validCount=value['validCount'],minimum_margin=value['minimum_margin']))
 percase=[]
 for case in records:
  percase.append({k:case[k] for k in ('neighbor_id','state','scale','mm_per_unit','nominal_minimum_margin','nominal_margin_mm','assembly_cell_stable','assembly_key_stable','primary_corner_cell_stable','nuisance_cell_stable','pupil')})
 summary=dict(id='SITE-CYLINDER-037',kind='Exact inspected Site vertical-tableau numeric replay, margins and finite manual sensitivity; not K4 or Site UI QA',started_at_utc=r['started_at_utc'],finished_at_utc=r['finished_at_utc'],complete=r['complete'],source_head=r['source_head'],source_core_sha256=r['source_core_sha256'],source_sha256=r['source_sha256'],source_snapshot_sha256=r['source_snapshot_sha256'],recorded_computation_peak_rss_bytes_before_final_serialization=r['peak_rss_bytes'],original_archive=metadata,actual_K4_evaluations=0,source_files_modified=False,Site_source_archived=False,default=base,default_min_margin_fraction=base['result']['minimum_margin'],default_min_margin_sample_indices=[i+1 for i,x in enumerate(base['result']['margins']) if abs(x-base['result']['minimum_margin'])<1e-12],fixture_comparison=dict(cases=[dict(id=x['id'],validCount=x['result']['validCount']) for x in n['source_fixtures']],samples_compared=n['fixture_samples_compared']+n['neighborhood_samples_compared'],maximum_coordinate_error=n['maximum_coordinate_difference']),neighborhood=dict(states=729,complete97=n['counts']['complete97'],invalid97=729-n['counts']['complete97'],same_default_cells_and_admission=n['counts']['same_default_cellpath_and_admission'],same_default_key=n['counts']['same_default_key'],distinct_complete_keys=n['distinct_complete_keys'],selected_ids=s['selected_ids'],full_stability_selected=s['selected_states'],unselected_complete_states=n['counts']['complete97']-s['selected_states']),default_axial_sensitivity=axial,stability_cases=percase,stability_counts={scale:dict(cases=sum(x['scale']==scale for x in records),assembly_cell_passes=sum(x['scale']==scale and x['assembly_cell_stable'] for x in records),assembly_key_passes=sum(x['scale']==scale and x['assembly_key_stable'] for x in records),tiny_pupil_passes=sum(x['scale']==scale and x['pupil']['0.05']['cell_stable'] for x in records),human_scale_pupil_passes=sum(x['scale']==scale and x['pupil']['1.5']['cell_stable'] for x in records)) for scale in ('U100','R250')})
 (dest/'SITE-CYLINDER-037-SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(dict(default_margin=summary['default_min_margin_fraction'],default_samples=summary['default_min_margin_sample_indices'],neighborhood=summary['neighborhood'],stability=summary['stability_counts'],axial=axial,archive=metadata),indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--destination',required=True);a=ap.parse_args();run(a.source,a.destination)
