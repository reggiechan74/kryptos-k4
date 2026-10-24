"""Exact conditional partial-ring registration; no K4 symbols or city time-zone guesses."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import random
import resource
import shutil
import subprocess
import sys
import tempfile
import time

INPUT=Path('independent/2026-10-22/historical-clock/historical_clock_evidence.json')

def band_map(slot, band):
    values=slot[band]
    ranks=slot.get(band+'_rank_override',list(range(1,len(values)+1)))
    if len(ranks)!=len(values) or len(set(ranks))!=len(ranks) or any(r<1 for r in ranks):
        raise ValueError('invalid observed ranks')
    if slot[band+'_complete'] and ranks!=list(range(1,len(values)+1)):
        raise ValueError('complete band must list all ranks')
    return dict(zip(ranks,values))

def pair_conflict(left,right):
    for band in ('upper','lower'):
        a,b=band_map(left,band),band_map(right,band)
        for rank in sorted(a.keys() & b.keys()):
            if a[rank]!=b[rank]:
                return {'kind':'different_known_labels','band':band,'rank':rank,'left':a[rank],'right':b[rank]}
        if left[band+'_complete'] and any(rank>len(a) for rank in b):
            return {'kind':'rank_beyond_complete_band','band':band,'complete_side':'left','complete_length':len(a),'other_ranks':sorted(b)}
        if right[band+'_complete'] and any(rank>len(b) for rank in a):
            return {'kind':'rank_beyond_complete_band','band':band,'complete_side':'right','complete_length':len(b),'other_ranks':sorted(a)}
        if left[band+'_complete'] and right[band+'_complete'] and len(a)!=len(b):
            return {'kind':'complete_lengths_disagree','band':band}
    return None

def enumerate_layouts(segments,size):
    if len(segments)!=3:
        raise ValueError('exactly three fixed segments required')
    if any(len(s['slots'])>size for s in segments):
        raise ValueError('segment longer than ring')
    rows=[]
    for offsets_tail in itertools.product(range(size),repeat=2):
        offsets=(0,)+offsets_tail
        occupied={};witness=None
        for segment,offset in zip(segments,offsets):
            for slot in segment['slots']:
                position=(offset+slot['s'])%size
                for old_segment,old_slot in occupied.get(position,[]):
                    conflict=pair_conflict(old_slot,slot)
                    if conflict:
                        witness=dict(conflict,global_sector=position,left_segment=old_segment,
                                     left_local_sector=old_slot['s'],right_segment=segment['id'],right_local_sector=slot['s'])
                        break
                if witness:break
                occupied.setdefault(position,[]).append((segment['id'],slot))
            if witness:break
        rows.append({'offsets':dict(zip((s['id'] for s in segments),offsets)),
                     'compatible':witness is None,'first_conflict':witness})
    return rows

def oracle_layouts(segments,size):
    """Independent simultaneous cell/rank unification, not pairwise matching."""
    accepted=set()
    for tail in itertools.product(range(size),repeat=2):
        offsets=(0,)+tail;cells={};valid=True
        for seg,offset in zip(segments,offsets):
            for slot in seg['slots']:
                for band in ('upper','lower'):
                    key=((slot['s']+offset)%size,band)
                    cells.setdefault(key,[]).append(slot)
        for (position,band),slots in cells.items():
            lengths={len(slot[band]) for slot in slots if slot[band+'_complete']}
            if len(lengths)>1:valid=False;break
            known={}
            for slot in slots:
                for rank,label in zip(slot.get(band+'_rank_override',range(1,len(slot[band])+1)),slot[band]):
                    if (lengths and rank>next(iter(lengths))) or (rank in known and known[rank]!=label):
                        valid=False;break
                    known[rank]=label
                if not valid:break
            if not valid:break
        if valid:accepted.add(offsets)
    return accepted

def phase_fit(sectors,hours,size):
    """Exact rational common phase from already specified measurements, not city inference."""
    if len(sectors)!=len(hours) or not sectors:return None
    choices={(Fraction(h)-s)%size for s,h in zip(sectors,hours)}
    return next(iter(choices)) if len(choices)==1 else None

def controls():
    rng=random.Random(2026102403);complete=0;plants=0
    for size in (4,5,6):
        for trial in range(12):
            truth=(0,rng.randrange(size),rng.randrange(size));segments=[]
            for j,offset in enumerate(truth):
                slots=[]
                for local in range(2 if j<2 else 1):
                    g=(offset+local)%size
                    slot={'s':local}
                    for band in ('upper','lower'):
                        full=[f'{band}-{g}-1',f'{band}-{g}-2']
                        is_complete=bool(rng.randrange(2))
                        slot[band]=full if is_complete else [full[rng.randrange(2)]]
                        if not is_complete:slot[band+'_rank_override']=[int(slot[band][0][-1])]
                        slot[band+'_complete']=is_complete
                    slots.append(slot)
                segments.append({'id':str(j),'slots':slots})
            actual={tuple(row['offsets'][str(i)] for i in range(3)) for row in enumerate_layouts(segments,size) if row['compatible']}
            expected=oracle_layouts(segments,size)
            assert actual==expected
            assert truth in actual
            complete+=1;plants+=1
    # Partial unknown is not empty; complete empty forbids positive ranks.
    def slot(values,complete):return {'s':0,'upper':values,'lower':[],'upper_complete':complete,'lower_complete':False}
    assert pair_conflict(slot([],False),slot(['X'],True)) is None
    assert pair_conflict(slot([],True),slot(['X'],True)) is not None
    assert pair_conflict(slot(['X'],False),slot(['Y'],False)) is not None
    rational_checks=0
    for size in (4,5,6,24):
        for phase in (Fraction(0),Fraction(1,2),Fraction(7,3)):
            sectors=[0,1,size-1];hours=[(s+phase)%size for s in sectors]
            assert phase_fit(sectors,hours,size)==phase%size
            assert phase_fit(sectors,hours[:-1]+[(hours[-1]+1)%size],size) is None
            for rotation in range(size):
                translated=[(s+rotation)%size for s in sectors]
                p=(phase-rotation)%size
                assert [(s+p)%size for s in translated]==hours
                for a,b,ha,hb in zip(sectors,sectors[1:],hours,hours[1:]):
                    assert (hb-ha)%size==(b-a)%size
                rational_checks+=1
    return {'complete_tiny_ring_solution_set_comparisons':complete,'planted_true_layouts_retained':plants,
            'rational_phase_and_gauge_cases':rational_checks,'mutations_and_unknown_vs_empty_checks_passed':True}

def analyze(data):
    segments=data['segments'];obs=data['observations'];ids=[s['id'] for s in segments]
    assert len(obs)==41 and len(segments)==3
    assert all(not o['verified_for_1989'] and o['semantic_timezone_utc'] is None for o in obs)
    assert all(not s['globally_registered'] for s in segments)
    # Ensure parser uses exact observed rank overrides, including BERLIN rank 2.
    slots={(s['id'],p['s']):p for s in segments for p in s['slots']}
    for o in obs:
        assert band_map(slots[(o['segment'],o['local_sector'])],o['physical_band'])[o['row_rank']]==o['raw_label']
    rows=enumerate_layouts(segments,24)
    compatible=[r['offsets'] for r in rows if r['compatible']]
    oracle=oracle_layouts(segments,24)
    assert {tuple(r[k] for k in ids) for r in compatible}==oracle
    # Do not impose disjointness; verify whether rank constraints imply it.
    disjoint=all(len({(r[s['id']]+p['s'])%24 for s in segments for p in s['slots']})==10 for r in compatible)
    pairs=[]
    for a,b in itertools.combinations(obs,2):
        differences=sorted({(r[b['segment']]+b['local_sector']-r[a['segment']]-a['local_sector'])%24 for r in compatible})
        pairs.append({'from_observation':a['id'],'to_observation':b['id'],'same_source_segment':a['segment']==b['segment'],
                      'sector_difference_domain':differences,'forced_under_conditional_model':len(differences)==1})
    shift_checks=0
    for r in compatible:
        for phase in range(24):
            hours=[(r[o['segment']]+o['local_sector']+phase)%24 for o in obs]
            for index,o in enumerate(obs):
                sector=(r[o['segment']]+o['local_sector'])%24
                assert (hours[index]-phase)%24==sector
                shift_checks+=1
            assert all((hours[j]-hours[i])%24==((r[b['segment']]+b['local_sector'])-(r[a['segment']]+a['local_sector']))%24 for i,(a,b,j) in enumerate(zip(obs,obs[1:],range(1,len(obs)))))
    return {'raw_gauge_fixed_offset_pairs':len(rows),'compatible_registration_count':len(compatible),
            'all_records':rows,'compatible_registrations':compatible,'independent_full_set_match':True,
            'disjointness_implied_not_assumed':disjoint,'disjoint_run_combinatorial_count_if_applicable':240 if disjoint else None,
            'pair_constraints':pairs,'within_segment_pair_count':sum(x['same_source_segment'] for x in pairs),
            'cross_segment_pair_count':sum(not x['same_source_segment'] for x in pairs),
            'forced_pair_counts':dict(Counter('within_segment' if x['same_source_segment'] else 'cross_segment' for x in pairs if x['forced_under_conditional_model'])),
            'integer_hypothetical_exposure_layout_phase_descriptions':len(compatible)*24,
            'integer_slot_roundtrips':shift_checks,'continuous_phase_not_enumerated':True,
            'semantic_UTC_offsets_assigned':0,'1989_verified_observations':0,'k4_trials':0}

def replay_old_pilot():
    original=INPUT.parent
    with tempfile.TemporaryDirectory(prefix='k4-world-clock-old-replay-') as td:
        temp=Path(td)
        for name in ('pilot.py','historical_clock_evidence.json'):shutil.copyfile(original/name,temp/name)
        subprocess.run([sys.executable,str(temp/'pilot.py')],check=True,capture_output=True,text=True)
        actual=json.loads((temp/'pilot_results.json').read_text());expected=json.loads((original/'pilot_results.json').read_text())
        assert actual==expected
    return {'all_original_result_fields_equal':True,'original_files_unchanged':True,'result':expected}

def main():
    from run_io import RunSnapshot,json_bytes,specification
    p=argparse.ArgumentParser();p.add_argument('--spec-commit',required=True);p.add_argument('--output',required=True);p.add_argument('--kind',choices=('original','replay'),default='replay');args=p.parse_args()
    spec=specification(args.spec_commit,Path('research/WORLD-CLOCK-003-SPEC.md'))
    with RunSnapshot(args.output,'WORLD-CLOCK-003',spec,execution_kind=args.kind) as snapshot:
        start=time.monotonic();control=controls();old=replay_old_pilot();result=analyze(json.loads(INPUT.read_text()))
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        if time.monotonic()-start>60:raise TimeoutError('frozen 60-second budget')
        if rss>256*1024*1024:raise MemoryError('frozen 256-MiB budget')
        result.update({'input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'controls':control,'old_pilot_replay':old,'elapsed_seconds':time.monotonic()-start,'peak_rss_bytes':rss,'scope':'Conditional unchanged common inventory; no historical continuity, geographic registration or cipher encoder established'})
        snapshot.write('registration-analysis.json',json_bytes(result))
    print(snapshot.final)

if __name__=='__main__':main()
