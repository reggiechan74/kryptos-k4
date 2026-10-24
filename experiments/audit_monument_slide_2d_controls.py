"""Supplementary standardized-selector check on the SAME synthetic plants only."""
import json
from pathlib import Path
import monument_slide_2d as m
def audit():
 start=m.utc();rows=['ABCDE','FGHIJ','KLMNO','PQRST'];models={'FORWARD':rows,'REVERSED':[r[::-1] for r in rows]};results=[]
 for model in models:
  for dy in (-1,0,1):
   for dx in (-1,0,1):
    source=[''.join(models[model][r-dy][c-dx] if 0<=r-dy<4 and 0<=c-dx<5 else 'Z' for c in range(5)) for r in range(4)];engine=m.Engine(m.toy_data(source,models));values=engine.score(engine.base.base);truth=f'{model}:{dy}:{dx}';record=dict(truth=truth)
    for e,name in enumerate(m.NAMES):
     keys=[m.exact_key(values[e][i]*engine.D-engine.expected[e][i],engine.weights[e][i]) for i in engine.active];best=max(keys);winners=[engine.frames[i]['id'] for i,key in zip(engine.active,keys) if key==best];record[name]=dict(truth_in_maximum=truth in winners,winners=winners)
    results.append(record)
 return dict(id='FOLD-SLIDE-2D-CONTROL-SUPPLEMENT-001',started_at_utc=start,finished_at_utc=m.utc(),chronology='Post-original-run supplementary validation on the same predeclared synthetic plants only; not a new actual K4 ranking or null calibration.',original_control_scope='Original retained controls used complete-domain raw label-count plant maxima. Standardized full selectors were separately validated against independent tiny null traversals before evaluation.',results=results,truth_in_label_statistic_maximum=sum(r['label_matches']['truth_in_maximum'] for r in results),truth_in_area_statistic_maximum=sum(r['common_pixel_area']['truth_in_maximum'] for r in results),actual_new_rankings_examined=False)
if __name__=='__main__':(m.ROOT/'results/FOLD-SLIDE-2D-CONTROL-SUPPLEMENT-001.json').write_text(json.dumps(audit(),indent=2)+'\n')
