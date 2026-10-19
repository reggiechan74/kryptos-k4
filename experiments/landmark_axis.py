"""Frozen paired-ray comparison over independent official heritage-site inventory."""
from collections import Counter,defaultdict
import csv,gzip,hashlib,io,json,math,time
from pathlib import Path
from landmark_geometry import support,axis_intervals,hit
ROOT=Path(__file__).resolve().parents[1]
TARGET=67.5

def stats(values,target_count):
    ordered=sorted(values);n=len(values);median=(ordered[(n-1)//2]+ordered[n//2])/2
    return {'orientations':n,'target_count':target_count,'median':median,'maximum':max(values),'mean':sum(values)/n,'target_minus_median':target_count-median,'strict_rank_best_is1':1+sum(v>target_count for v in values),'tied_orientations':sum(v==target_count for v in values),'equal_or_higher_angular_fraction':sum(v>=target_count for v in values)/n}

def continuous(intervalsets,target_count):
    events=defaultdict(int);events[0.]+=0;events[180.]+=0
    for intervals in intervalsets:
        for a,b in intervals:
            events[a]+=1;events[b]-=1
    counts=defaultdict(float);current=0;last=0.
    for angle,change in sorted(events.items()):
        if angle>last:counts[current]+=angle-last
        current+=change;last=angle
    cumulative=0.;median=None
    for n,width in sorted(counts.items()):
        cumulative+=width
        if cumulative>=90 and median is None:median=n
    return {'angular_measure_deg':dict(sorted(counts.items())),'median_count':median,'maximum_on_positive_width_intervals':max(counts),'equal_or_higher_angular_fraction':sum(width for n,width in counts.items() if n>=target_count)/180,'interpretation':'Descriptive measure on one180degreecycle; intervalendpoints havezeroangularmeasure, no statisticalpvalue.'}

def run(spec_commit,inventory_commit,code_commit):
    started=time.monotonic();path=ROOT/'data/landmark-axis/inventory.json.gz';sites=json.loads(gzip.decompress(path.read_bytes()))['sites'];runs=[];csvrows=[];previous=None
    for step in (5.,2.5):
        scored=[]
        for site in sites:
            intervals,contains=support(site['polygons'],step);assert not contains
            scored.append({k:v for k,v in site.items() if k!='polygons'})
            scored[-1]['directional_intervals_deg']=intervals;scored[-1]['axis_intervals_deg']=axis_intervals(intervals)
            if time.monotonic()-started>180:raise TimeoutError('180secondscoringcap; no complete result')
        eligible=[s for s in scored if s['stratum']=='H1'];uncertain=[s for s in scored if s['stratum']=='U']
        angles=[i/100 for i in range(18000)];counts=[sum(hit(s['axis_intervals_deg'],a) for s in eligible) for a in angles];ucounts=[sum(hit(s['axis_intervals_deg'],a) for s in uncertain) for a in angles];target=counts[6750]
        selected=[s for s in eligible if hit(s['axis_intervals_deg'],TARGET)]
        local=[v for a,v in zip(angles,counts) if 57.5<=a<=77.5]
        item={'native_edge_densification_m':step,'eligible_H1_sites':len(eligible),'uncertain_U_sites':len(uncertain),'primary_H1_grid':stats(counts,target),'primary_H1_continuous':continuous([s['axis_intervals_deg'] for s in eligible],target),'local_pm10_grid':stats(local,target),'uncertain_U_grid_separate':stats(ucounts,ucounts[6750]),'target_H1_directional_counts':{'ENE':sum(hit(s['directional_intervals_deg'],67.5) for s in eligible),'WSW':sum(hit(s['directional_intervals_deg'],247.5) for s in eligible)},'target_H1_classes':dict(Counter(s['count_class'] for s in selected)),'all_H1_classes':dict(Counter(s['count_class'] for s in eligible)),'target_H1_ids':[s['canonical_id'] for s in selected],'target_U_ids':[s['canonical_id'] for s in uncertain if hit(s['axis_intervals_deg'],TARGET)],'coarser_grid_002':stats(counts[::2],target),'fixed_comparison_orientations':[{'orientation':a,'paired_reverse':a+180,'H1_count':counts[round(a*100)]} for a in (0,22.5,45,57.5,62.5,65.5,66.5,67,67.5,68,68.5,69.5,72.5,77.5,90,112.5,135,157.5)]}
        if previous is not None:item['convergence_from5m']={'grid_count_changes':sum(a!=b for a,b in zip(previous,counts)),'maximum_count_delta':max(abs(a-b) for a,b in zip(previous,counts)),'target_count_changed':previous[6750]!=target}
        runs.append(item);previous=counts
        if step==5:
            csvrows=[(a,a+180,c,u) for a,c,u in zip(angles,counts,ucounts)]
        finalsites=scored
    buf=io.StringIO();writer=csv.writer(buf);writer.writerow(['axis_initial_bearing_deg','paired_reverse_deg','H1_pre1990existence_modernproxy_count','U_uncertain_count']);writer.writerows(csvrows)
    out=ROOT/'results/landmark-axis';(out/'orientation-grid.csv.gz').write_bytes(gzip.compress(buf.getvalue().encode(),mtime=0))
    (out/'site-intervals.json.gz').write_bytes(gzip.compress(json.dumps(finalsites,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
    files=['research/specifications/LANDMARK-AXIS-001.json','experiments/landmark_axis.py','experiments/landmark_geometry.py','experiments/landmark_inventory.py','tests/test_landmark_axis.py','data/landmark-axis/inventory.json.gz','sources/landmark-axis/inventory-receipt.json']
    result={'experiment':'LANDMARK-AXIS-001','spec_commit':spec_commit,'inventory_commit':inventory_commit,'code_commit':code_commit,'inventory_selection':'Officialregionalheritagegeometry, nestedclusters, SHA256-IDsamplefirst200; prioraxislandmarklistnotused','historical_outline_confirmed_H0':0,'primary_is_H1_pre1990existence_current_geometry_proxy':True,'rays_m_each_direction':5000,'target_axis':[67.5,247.5],'runs':runs,'metric_buffers':{'requested_m':[5,10],'computed':False,'reason':'No independentlyvalidatedmetricbufferimplementationavailablewithoutnewdependencies; omitted per frozenfallback, not replacedwithangularbuffer. Densification andangulargrid/local-neighbor sensitivity reported.'},'interpretation':'Descriptiveconditionalrotationalcomparison only. Knownchosenaxis, heritage/sample selection, source/mapuncertainty andcorrelatedorientations prevent discoverypvalue or designer-intent inference. H0 verifiedhistoricoutlineanalysis notestimable.','elapsed_seconds':round(time.monotonic()-started,6),'input_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files},'artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}}
    assert result['elapsed_seconds']<180
    (out/'LANDMARK-AXIS-001.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'elapsed_seconds':result['elapsed_seconds'],'runs':[r['primary_H1_grid'] for r in runs],'target_ids':runs[0]['target_H1_ids']}),flush=True)
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--spec-commit',required=True);p.add_argument('--inventory-commit',required=True);p.add_argument('--code-commit',required=True);a=p.parse_args();run(a.spec_commit,a.inventory_commit,a.code_commit)
