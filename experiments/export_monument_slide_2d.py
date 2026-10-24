"""Post-run presentation only; never changes selector, endpoints, or glyphs."""
import csv,hashlib,json
from pathlib import Path
import monument_slide_2d as m
ROOT=m.ROOT

def export():
 parent=ROOT/'results/fold-slide-2d-001-runs';pointer=json.loads((parent/'latest.json').read_text())
 if pointer['status']!='completed':raise ValueError('no completed run')
 run=parent/pointer['run_id'];actual=json.loads((run/'actual.json').read_text());manifest=json.loads((run/'manifest.json').read_text());summary=json.loads((run/'summary.json').read_text());records=actual['records'];D=actual['common_expectation_denominator'];nulls={scheme:json.loads((run/('null-'+scheme+'.json')).read_text()) for scheme in ('shuffle','rotation')};lookup={scheme:{r['id']:r['endpoints'] for r in result['per_frame']} for scheme,result in nulls.items()}
 fields=['model','dy','dx','geometric_overlap_cells','comparable_letter_pairs','label_matches','label_match_fraction','nonempty_common_aperture_pairs','common_pixel_area','full_mask_coincidences','union_pixel_area','common_over_union','matched_letters','k4_positions'];fields+=['expected_label_matches','expected_common_pixel_area','label_statistic','area_statistic']+[s+'_'+n+suffix for s in nulls for n in m.NAMES for suffix in ('_family_p','_four_report_p')]
 output=ROOT/'results/FOLD-SLIDE-2D-001-frames.csv'
 with output.open('w') as f:
  writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader()
  for r in records:
   row={k:r[k] for k in fields if k in r};row['k4_positions']=';'.join(map(str,r['k4_positions']))
   for e,name in enumerate(m.NAMES):
    N=r['expected_numerators'][e];row['expected_'+name if e==0 else 'expected_common_pixel_area']=N/D;row['label_statistic' if e==0 else 'area_statistic']=m.stat_display(r[name]*D-N,max(N,D),D) if r['geometric_overlap_cells'] else None
    for scheme in nulls:
     p=lookup[scheme][r['id']][name];row[scheme+'_'+name+'_family_p']=p['family_max_plus_one_p'] if p else None;row[scheme+'_'+name+'_four_report_p']=p['four_report_adjusted_p'] if p else None
   writer.writerow(row)
 tops={}
 for e,name in enumerate(m.NAMES):
  active=[r for r in records if r['geometric_overlap_cells']];active.sort(key=lambda r:m.exact_key(r[name]*D-r['expected_numerators'][e],max(D,r['expected_numerators'][e])),reverse=True);key=m.exact_key(active[0][name]*D-active[0]['expected_numerators'][e],max(D,active[0]['expected_numerators'][e]));tops[name]=dict(tie_count=sum(m.exact_key(r[name]*D-r['expected_numerators'][e],max(D,r['expected_numerators'][e]))==key for r in active),top_five=[{k:r[k] for k in ('id','model','dy','dx','geometric_overlap_cells','comparable_letter_pairs','label_matches','common_pixel_area','matched_letters','expected_numerators')} for r in active[:5]])
 max_labels=max(r['label_matches'] for r in records);raw_leaders=[{k:r[k] for k in ('id','geometric_overlap_cells','comparable_letter_pairs','label_matches','matched_letters')} for r in records if r['label_matches']==max_labels]
 result=dict(run=str(run.relative_to(ROOT)),manifest_start_utc=manifest['started_at_utc'],manifest_end_utc=manifest['finished_at_utc'],top_statistics=tops,maximum_raw_label_count=max_labels,raw_label_leaders=raw_leaders,source_sha256={str(p.relative_to(ROOT)):m.hashlib.sha256(p.read_bytes()).hexdigest() for p in (run/'actual.json',run/'null-shuffle.json',run/'null-rotation.json')})
 # Four full-domain count maps. Color is descriptive raw count, never a p-value.
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="980" height="790" viewBox="0 0 980 790"><rect width="980" height="790" fill="#f5f2e9"/><g font-family="sans-serif" fill="#26382f"><text x="35" y="28" font-size="20">Systematic row + column overlay: every integer displacement</text><text x="35" y="50" font-size="12">Raw counts only; overlap denominators change. Neither full-search endpoint is unusual under the declared controls.</text>']
 names=list(dict.fromkeys(r['model'] for r in records))
 for panel,(model,name) in enumerate((model,name) for model in names for name in m.NAMES):
  left=60+(panel%2)*460;top=100+(panel//2)*335;rows=[r for r in records if r['model']==model];maximum=max(r[name] for r in records);svg.append(f'<text x="{left}" y="{top-20}" font-size="13">{model}: {name}</text>')
  for r in rows:
   fraction=r[name]/maximum if maximum else 0;color=f'rgb({int(240-198*fraction)},{int(239-127*fraction)},{int(227-135*fraction)})';x=left+(r['dx']+33)*5;y=top+(r['dy']+28)*5;svg.append(f'<rect x="{x}" y="{y}" width="5" height="5" fill="{color}"><title>dx={r["dx"]}, dy={r["dy"]}, count={r[name]}, overlap={r["geometric_overlap_cells"]}</title></rect>')
  for dx in (-33,-16,0,16,33):svg.append(f'<text x="{left+(dx+33)*5-6}" y="{top+300}" font-size="11">{dx}</text>')
  for dy in (-28,-14,0,14,28):svg.append(f'<text x="{left-27}" y="{top+(dy+28)*5+4}" font-size="11">{dy}</text>')
  svg.append(f'<text x="{left}" y="{top+318}" font-size="11">Column dx →; row dy ↓. Color range 0–{maximum}; no optical calibration.</text>')
 svg.append('</g></svg>');(ROOT/'research/figures/fold-slide-2d-001.svg').write_text(''.join(svg)+'\n');(ROOT/'results/FOLD-SLIDE-2D-001-export.json').write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':print(json.dumps(export(),indent=2))
