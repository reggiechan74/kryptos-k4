"""Synthetic-only timing, no actual052bank or K4 reads."""
import concurrent.futures
import json
import os
import statistics
import time
import reference as p
import native
from test_native import synthetic_bank,random_cipher


def main():
    bank=synthetic_bank(1024,seed=520052);cipher=random_cipher(520052)
    scorer=native.NativeScorer(bank)
    start=time.perf_counter();reference=p.Scorer(bank).score(cipher);python_seconds=time.perf_counter()-start
    timing=[]
    for _ in range(5):
        start=time.perf_counter();value=scorer.score(cipher);timing.append(time.perf_counter()-start)
        assert value==reference
    rng=p.rng_for('benchmark-only-null')
    nulls=[p.conditioned_null(cipher,rng) for _ in range(64)]
    start=time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:values=list(ex.map(scorer.score,nulls))
    parallel_seconds=time.perf_counter()-start
    report={'synthetic_only':True,'candidates':1024,'descriptions_per_candidate':1152,
            'python_reference_seconds':python_seconds,'c_serial_seconds':timing,'c_serial_median':statistics.median(timing),
            'exact_reference_match':True,'threads':8,'parallel_replicates':len(nulls),'parallel_wall_seconds':parallel_seconds,
            'observed_parallel_seconds_per_replicate':parallel_seconds/len(nulls),
            'projected_1999_null_seconds':parallel_seconds/len(nulls)*1999,
            'projected_9036_control_null_seconds':parallel_seconds/len(nulls)*9036,
            'projection_excludes_diagnostics_io_controls':True,'environment':p.environment_record()}
    p.write_json(native.ROOT/'synthetic_benchmark.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
