"""Permutation/domain coverage only: this module never scores K4 ciphertext."""
import gzip
import hashlib
import itertools
import json
from pathlib import Path
from bounded_models import inverse_permutation
from occupied_cell_routes import model_signature

ROOT=Path(__file__).resolve().parents[1]
PRIOR=ROOT/'results/ROUTE-001.json.gz'


def occupied_cells():
    return [(0,c) for c in range(27,31)]+[(r,c) for r in range(1,4) for c in range(31)]


def catalogue():
    result=[]
    for h,v,inv in itertools.product((False,True),repeat=3):
        indexed=[((3-r if v else r,30-c if h else c),i) for i,(r,c) in enumerate(occupied_cells())]
        pi=[i for _,i in sorted(indexed)]
        result.append({'horizontal':h,'vertical':v,'inverse':inv,
                       'permutation':inverse_permutation(pi) if inv else pi})
    return result


def coverage():
    prior=json.loads(gzip.decompress(PRIOR.read_bytes()))
    known={}
    for r in prior['route_catalogue']:
        identity=r['permutation']==list(range(97))
        for p,a,e,o in itertools.product(range(1,13),('AZ','KRYPTOS'),('plus','beaufort'),('sub_then_route','route_then_sub')):
            old_order='identity' if identity else o
            survivors=[s for s in prior['survivors'] if s['route']==r['id'] and s['period']==p and s['alphabet']==a and s['equation']==e and s['order']==old_order]
            assert not survivors,'Cannot claim prior rejection of a retained model'
            key=(a,e,p,model_signature(r['permutation'],p,o))
            known.setdefault(key,[]).append({'route_id':r['id'],'order':old_order,'result':'results/ROUTE-001.json.gz'})
    found={};raw=0
    for r,p,a,e,o in itertools.product(catalogue(),range(1,13),('AZ','KRYPTOS'),('plus','beaufort'),('sub_then_route','route_then_sub')):
        raw+=1;key=(a,e,p,model_signature(r['permutation'],p,o))
        row=found.setdefault(key,{'case_id':'FACE-%03d'%len(found),'permutation':r['permutation'],'period':p,'alphabet':a,'equation':e,'order':o,'aliases':[],'prior_coverage':known.get(key,[])})
        row['aliases'].append({k:r[k] for k in ('horizontal','vertical','inverse')}|{'order':o})
    rows=list(found.values());new=[r for r in rows if not r['prior_coverage']]
    # Only the horizontal reflection is new; both training layer orders observe every phase.
    horizontal=next(r['permutation'] for r in catalogue() if r['horizontal'] and not r['vertical'] and not r['inverse'])
    for row in new:
        assert row['permutation']==horizontal
        inv=inverse_permutation(row['permutation']);p=row['period']
        phases={(i if row['order']=='sub_then_route' else inv[i])%p for i in range(21,34)}
        assert phases==set(range(p))
    return {'kind':'prior-coverage audit; zero K4 evaluations','raw_descriptions':raw,
            'distinct_routes':len({tuple(r['permutation']) for r in catalogue()}),'canonical_models':len(rows),
            'covered_models':len(rows)-len(new),'new_models':len(new),'records':rows,
            'prior_result_sha256':hashlib.sha256(PRIOR.read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    (ROOT/'results/FACE-ROW-001-COVERAGE.json').write_text(json.dumps(coverage(),indent=2)+'\n')
