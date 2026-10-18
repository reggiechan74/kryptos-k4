"""Bounded, histogram-preserving calibration of published lag collisions."""
from collections import Counter
from check_baseline import validate
from bounded_models import deadline_check
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import statistics
import time

ROOT=Path(__file__).resolve().parents[1]
WIDTHS=range(1,49)
SHUFFLES=9999
CALIBRATION=4999
SEED=20261018


def collisions(text,width):
    if not 0 < width < len(text): raise ValueError('width out of range')
    counts=Counter((text[i],text[i+width]) for i in range(len(text)-width))
    return sum(n-1 for n in counts.values())


def wilson(successes,total):
    z=1.959963984540054;denom=1+z*z/total
    center=(successes/total+z*z/(2*total))/denom
    radius=z*math.sqrt(successes/total*(1-successes/total)/total+z*z/(4*total*total))/denom
    return [max(0,center-radius),min(1,center+radius)]


def run(shuffles=SHUFFLES,calibration=CALIBRATION,limit=60):
    if shuffles <= calibration or calibration < 2: raise ValueError('invalid split')
    started=time.monotonic()
    deadline_check(started, limit)
    text=validate(json.loads((ROOT/'data/k4.json').read_text()))
    original=[collisions(text,w) for w in WIDTHS]
    rng=random.Random(SEED);draws=[];letters=list(text)
    for trial in range(shuffles):
        rng.shuffle(letters)
        assert Counter(letters)==Counter(text)
        draws.append([collisions(letters,w) for w in WIDTHS])
        if trial%100==0: deadline_check(started, limit)
    means=[statistics.mean(row[i] for row in draws[:calibration]) for i in range(48)]
    deviations=[statistics.stdev(row[i] for row in draws[:calibration]) for i in range(48)]
    if any(s==0 for s in deviations): raise ValueError('zero calibration deviation')
    def maximum_z(row):return max((value-means[i])/deviations[i] for i,value in enumerate(row))
    observed_max=maximum_z(original);evaluation=draws[calibration:]
    maxima=[maximum_z(row) for row in evaluation]
    fixed=sum(row[20]>=original[20] for row in evaluation)
    adjusted=sum(value>=observed_max for value in maxima)
    max_raw=max(original)
    deadline_check(started, limit)
    return {'experiment':'STAT-001','date_utc':'2026-10-18','python':platform.python_version(),
            'seed':SEED,'generator':'Python random.Random/MT19937.shuffle',
            'statistic':'duplicate excess sum(count-1) among ordered pairs at lag w; overlapping pairs included',
            'widths':list(WIDTHS),'observed_collision_counts':original,
            'observed_maximum_raw':max_raw,'observed_maximum_raw_widths':[i+1 for i,v in enumerate(original) if v==max_raw],
            'calibration_draws':calibration,'evaluation_draws':len(evaluation),
            'calibration_means':means,'calibration_sample_sd':deviations,
            'observed_maximum_calibration_z':observed_max,
            'fixed_width_21':{'observed':original[20],'evaluation_exceedances':fixed,
                'plus_one_p':(fixed+1)/(len(evaluation)+1),'wilson_95_interval_for_underlying_null_tail':wilson(fixed,len(evaluation))},
            'maximum_over_48_widths':{'evaluation_exceedances':adjusted,
                'plus_one_p':(adjusted+1)/(len(evaluation)+1),'wilson_95_interval_for_underlying_null_tail':wilson(adjusted,len(evaluation))},
            'raw_draws':draws,'evaluation_maxima_z':maxima,
            'elapsed_seconds':round(time.monotonic()-started,3),
            'hashes':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['data/k4.json','experiments/statistical_diagnostics.py']},
            'scope':'Conditional histogram-preserving permutation null and declared 48-lag family only; not an English-language null, full-paper reproduction, or posterior probability. Published width 21 and these diagnostics were known before this run, so postselection beyond this family remains uncontrolled.'}


if __name__=='__main__':
    from run_bounded import statistics_main
    statistics_main()
