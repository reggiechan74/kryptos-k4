"""Post-outcome independent direct selector; no production constraint compiler."""
import hashlib,itertools,json,time
from datetime import datetime,timezone
from pathlib import Path
from lamp_greek import ALPHABETS,WINDOWS,ROLES,STARTS,GREEK,LATIN,plant,check_budget
ROOT=Path(__file__).resolve().parents[1]


def reference_values():
    # Independent row construction with subtraction, not the triangular formula.
    tables=[]
    for reverse in (False,True):
        phases=[]
        for p in (0,1):
            row=[]
            for t in range(1440):
                h=t//60;m=t%60;bits=[p]
                for value,size,unit in ((h,4,5),(h%5,4,1),(m,11,5),(m%5,4,1)):
                    for j in range(size):bits.append(int(value>=(j+1)*unit))
                if reverse:bits=bits[::-1]
                row.append(sum((i+1)*b for i,b in enumerate(bits)))
            phases.append(row)
        tables.append(phases)
    return tables


def reference_select(cipher,tables):
    """All raw models; direct plaintext checks, not required-key sets."""
    survivors=[]
    for role,name,eq in itertools.product(ROLES,ALPHABETS,('plus','beaufort')):
        a=ALPHABETS[name]
        if role!='G' and len(cipher)!=97:continue
        if role=='G' and set(cipher)-set(a[:24]):continue
        cv=[a.index(c) for c in cipher]
        for rev,p,t in itertools.product((0,1),(0,1),range(1440)):
            table=tables[rev][p]
            def dec(v,k,n):return (v-k if eq=='plus' else k-v)%n
            if role=='L':
                first=''.join(a[dec(cv[i],table[(t+i)%1440],26)] for i in range(21,34))
                if first!=WINDOWS[0][1]:continue
                plain=''.join(a[dec(v,table[(t+i)%1440],26)] for i,v in enumerate(cv))
            elif role=='B':
                out=[]
                for i in range(0,len(cv),2):
                    pair=cv[i:i+2];n=26**len(pair);r=pair[0]*26+pair[1] if len(pair)==2 else pair[0]
                    r=dec(r,table[(t+i//2)%1440],n)
                    out.append(a[r//26]+a[r%26] if len(pair)==2 else a[r])
                plain=''.join(out)
                if plain[21:34]!=WINDOWS[0][1]:continue
            else:
                out=[];escape=False;bad=False
                for i,v in enumerate(cv):
                    v=dec(v,table[(t+i)%1440],24)
                    if escape:
                        if v>2:bad=True;break
                        out.append(LATIN[23+v]);escape=False
                    elif v==23:escape=True
                    else:out.append(LATIN[v])
                if bad or escape:continue
                plain=''.join(out)
                if len(plain)!=97 or plain[21:34]!=WINDOWS[0][1]:continue
            survivors.append(dict(role=role,order=('row_major','reverse')[rev],start_minute=t,indicator=p,alphabet=name,equation=eq,plaintext=plain,all_pass=plain[63:74]==WINDOWS[1][1]))
    return survivors


def canonical(rows):
    return sorted(json.dumps(dict(r['model'],plaintext=r['plaintext'],all_pass=r['all_pass']),sort_keys=True) for r in rows)


def run():
    from lamp_greek import select,VALUES
    start=time.monotonic();started=datetime.now(timezone.utc).isoformat();tables=reference_values()
    assert tables==[[list(xs) for xs in rev] for rev in VALUES]
    root=ROOT/'results/lamp-greek-025';folder=root/json.loads((root/'latest.json').read_text())['run_id']
    saved=json.loads((folder/'controls.json').read_text());rows=[]
    # Same 24 plants, all raw candidates and all plaintext classes, no chosen representatives.
    from lamp_greek import crypt
    for original in saved['literal_plants']:
        cipher=crypt(plant(),original['planted_model']);ref=reference_select(cipher,tables);native=select(cipher)
        assert sorted(json.dumps(x,sort_keys=True) for x in ref)==canonical(native['models'])
        assert canonical(original['compatible_models'])==canonical([x for x in native['models'] if x['all_pass']])
        rows.append(dict(model=original['planted_model'],first_survivors=len(ref),all_survivors=sum(x['all_pass'] for x in ref),complete_set_equal=True))
        check_budget(start,120)
    cipher=json.loads((ROOT/'data/k4.json').read_text())['ciphertext'];actual=reference_select(cipher,tables)
    assert actual==[] and canonical(select(cipher)['models'])==[]
    return dict(kind='post_outcome_independent_validation_not_original_run',started_at_utc=started,finished_at_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-start,complete_raw_selectors_compared=25,plant_comparisons=rows,actual_survivors=0,independent_clock_entries=5760,source_sha256={Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},limitations='Same author, separate arithmetic and direct decoder; not an external blinded audit.')
if __name__=='__main__':
    from run_io import atomic_write,json_bytes
    out=run();atomic_write(ROOT/'results/LAMP-GREEK-025-INDEPENDENT-VALIDATION.json',json_bytes(out));print(json.dumps({k:v for k,v in out.items() if k!='plant_comparisons'},indent=2))
