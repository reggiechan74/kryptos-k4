"""Audit supplied local-equation function; do not repeat full parameter enumeration."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
V=ROOT/'independent/2026-10-22/calibration'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True);args=p.parse_args()
    out=Path(args.output)
    if out.exists():raise FileExistsError('do not overwrite an audit')
    start=time.monotonic()
    spec=importlib.util.spec_from_file_location('received_calibration',V/'run_calibration.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    # Execute only the reviewed function from the received audit. The module's
    # top-level re-enumeration calls are deliberately excluded, not patched away.
    tree=ast.parse((V/'audit.py').read_text())
    nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='independent_candidates']
    assert len(nodes)==1
    scope={'np':np,'m':m}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(V/'audit.py'),'exec'),scope)
    saved=json.loads((V/'synthesis_results.json').read_text())
    targets=[('K4',m.K4,saved['K4'])]+[(str(x['case']),x['ciphertext'],x) for x in saved['synthetic_positives']]
    checked=[]
    for name,cipher,stored in targets:
        found,details=scope['independent_candidates'](cipher)
        assert len(found)==stored['parameter_candidates']
        for i,row in enumerate(details):
            assert row['first_crib_seeded_fits']==stored['counts_by_alphabet'][i]['after_first_crib']
        plains=set()
        for alphabet,a,b,d,k in found:
            state=k;plain=[]
            for c in cipher:
                value=alphabet.index(c)
                plain.append(alphabet[(value-state)%26])
                state=(a*state+b+d*value)%26
            plain=''.join(plain)
            assert plain[21:34]=='EASTNORTHEAST' and plain[63:74]=='BERLINCLOCK'
            plains.add(plain)
        assert len(plains)==stored['distinct_full_plaintexts']
        ambiguous=[]
        for i in range(97):
            choices=sorted({plain[i] for plain in plains})
            if len(choices)>1:ambiguous.append({'position_1based':i+1,'possible_characters':''.join(choices)})
        assert ambiguous==stored['ambiguous_positions']
        if name!='K4':
            planted=stored['planted'];true=(planted['alphabet'],planted['a'],planted['b'],planted['d'],planted['k'])
            assert true in found and stored['planted_plaintext'] in plains
        checked.append(dict(target=name,parameter_candidates=len(found),distinct_full_plaintexts=len(plains),
                            ambiguous_positions=ambiguous,local_constraint_details=details))
    assert time.monotonic()-start<120
    result=dict(id='SUPPLIED-SYNTHESIS-LOCAL-EQUATION-AUDIT-001',status='completed',
                code_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                python=platform.python_version(),numpy=np.__version__,
                adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                source_sha256={x:hashlib.sha256((V/x).read_bytes()).hexdigest() for x in ['audit.py','run_calibration.py','synthesis_results.json']},
                method='Reviewed adjacent-known-state coefficient constraints only; replay seeds only for surviving triples; never call synthesize()',
                raw_coefficient_triples_per_alphabet=26**3,targets=checked,
                full_parameter_enumeration_repeated=False,additional_novel_K4_searches=0,
                elapsed_seconds=time.monotonic()-start)
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
