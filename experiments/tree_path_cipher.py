"""Frozen reversible tree/subtree permutation pilot. No fitting of tree geometry."""
import argparse
import hashlib
import json
from pathlib import Path
import time
from experiments.alphabet_geometry import AZ, SCHEMA, load_schema, codebook, decision_tree

ROOT = Path(__file__).resolve().parents[1]
MORSE = dict(zip(AZ, ['.-','-...','-.-.','-..','.','..-.','--.','....','..','.---','-.-','.-..','--','-.','---','.--.','--.-','.-.','...','-','..-','...-','.--','-..-','-.--','--..']))


def trees():
    schema = load_schema()
    if hashlib.sha256(SCHEMA.read_bytes()).hexdigest() != '6a5c6eae644dedf88afb68df911f0c3161a969af3815972aa5694479155aa010':
        raise ValueError('changed geometry')
    def convert(node):
        if 'letter' in node:
            return {'letter': node['letter'], 'children': {}}
        return {'children': {b: convert(n) for b, n in node['branches'].items()}}
    g = convert(decision_tree(codebook(schema), schema['feature_order']))
    m = {'children': {}}
    for c, path in MORSE.items():
        node = m
        for b in path:
            node = node['children'].setdefault(b, {'children': {}})
        node['letter'] = c
    return {'geometry': compile_tree(g, ('0','1')), 'morse': compile_tree(m, ('.','-'))}


def compile_tree(root, order):
    slots, paths, groups = [], {}, {}
    def visit(node, path):
        start = len(slots)
        if 'letter' in node:
            slots.append(node['letter']); paths[node['letter']] = path
        for b in order:
            if b in node['children']:
                visit(node['children'][b], path+b)
        groups[path] = tuple(range(start, len(slots)))
    visit(root, '')
    assert len(slots) == 26 and set(slots) == set(AZ)
    return {'slots': slots, 'paths': paths, 'groups': groups,
            'index': {c: i for i,c in enumerate(slots)}}


def update(state, tree, letter, direction):
    path = tree['paths'][letter]
    for depth in range(1, len(path)+1):
        ids = tree['groups'][path[:depth]]
        old = [state[i] for i in ids]
        for j, i in enumerate(ids):
            state[i] = old[(j-direction) % len(ids)]


def crypt(text, tree, direction, seed, decrypt=False, trace=False):
    if type(seed) is not int or not 0 <= seed < 26 or direction not in (-1,1) or any(c not in AZ for c in text):
        raise ValueError('invalid model or A-Z input')
    state = list(AZ[seed:]+AZ[:seed]); out, rows = [], []
    for i,c in enumerate(text):
        slot = state.index(c) if decrypt else tree['index'][c]
        p = tree['slots'][slot] if decrypt else c
        emitted = p if decrypt else state[slot]
        if trace:
            rows.append({'position':i+1,'plaintext':p,'ciphertext':c if decrypt else emitted,'path':tree['paths'][p],'state_before':''.join(state)})
        out.append(emitted); update(state, tree, p, direction)
    return (''.join(out), rows) if trace else ''.join(out)


def oracle(text, tree, direction, seed, decrypt=False):
    # Separate dictionary label state; derive every subtree directly by path prefix.
    labels = {c: AZ[(i+seed)%26] for i,c in enumerate(tree['slots'])}
    out = []
    for c in text:
        p = next(p for p in AZ if labels[p] == c) if decrypt else c
        out.append(p if decrypt else labels[p])
        path = tree['paths'][p]
        for depth in range(1, len(path)+1):
            letters = [x for x in tree['slots'] if tree['paths'][x].startswith(path[:depth])]
            old = dict(labels)
            for j,x in enumerate(letters):
                labels[x] = old[letters[(j-direction)%len(letters)]]
    return ''.join(out)


def framed_path_decode(paths, tree):
    reverse = {v:k for k,v in tree['paths'].items()}
    try:
        return ''.join(reverse[p] for p in paths)
    except KeyError as exc:
        raise ValueError('not a framed letter path') from exc


def models(ts):
    return [(name, d, s) for name in ts for d in (1,-1) for s in range(26)]


def select(ciphertext, ts, cribs):
    records=[]
    for name,d,s in models(ts):
        p = crypt(ciphertext,ts[name],d,s,True)
        first = p[21:34] == cribs[0]
        second = p[63:74] == cribs[1]
        records.append({'tree':name,'direction':d,'seed':s,'first_pass':first,
                        'second_pass':second,'all_pass':first and second,
                        'plaintext_sha256':hashlib.sha256(p.encode()).hexdigest(),
                        'first_prediction':p[21:34],'second_prediction':p[63:74],
                        'regenerates':crypt(p,ts[name],d,s)==ciphertext})
    return records


def controls(ts):
    started=time.monotonic(); checks=0; mutations=0; plants=[]; witnesses={}
    messages=['',AZ,AZ[::-1],'THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG','SOMESTATEISSHAREDBETWEENLETTERS']
    base=list((AZ*4)[:97]); base[21:34]='EASTNORTHEAST';base[63:74]='BERLINCLOCK';plant=''.join(base)
    for name,d,s in models(ts):
        t=ts[name]
        for p in messages:
            c=crypt(p,t,d,s)
            assert crypt(c,t,d,s,True)==p
            assert oracle(p,t,d,s)==c and oracle(c,t,d,s,True)==p
            assert framed_path_decode([t['paths'][x] for x in p],t)==p
            checks+=1
        # Every reachable sampled state is a bijection; inverse is exact for all letters.
        state=list(AZ[s:]+AZ[:s])
        for p in AZ:
            assert len(set(state))==26
            for x in AZ:
                assert t['slots'][state.index(state[t['index'][x]])]==x
                checks+=1
            update(state,t,p,d)
        if name not in witnesses:
            for p in AZ:
                state=list(AZ);update(state,t,p,d)
                if ''.join(state) not in [AZ[k:]+AZ[:k] for k in range(26)]:
                    witnesses[name]={'plaintext':p,'direction':d,'state_after':''.join(state)};break
            assert name in witnesses
        c=crypt(plant,t,d,s)
        rr=select(c,ts,['EASTNORTHEAST','BERLINCLOCK'])
        good=[r for r in rr if r['all_pass']]
        assert any((r['tree'],r['direction'],r['seed'])==(name,d,s) for r in good)
        assert all(r['regenerates'] for r in rr)
        plants.append({'tree':name,'direction':d,'seed':s,'compatible_models':good,
                       'distinct_compatible_plaintexts':len({r['plaintext_sha256'] for r in good})})
        # Timing mutant consumes P before emission. Detect rather than assuming no other model fits.
        state=list(AZ[s:]+AZ[:s]);out=[]
        for p in plant:
            update(state,t,p,d);out.append(state[t['index'][p]])
        assert ''.join(out)!=c;mutations+=1
        assert time.monotonic()-started<120
    return {'roundtrip_and_path_checks':len(models(ts))*len(messages),'bijection_letter_checks':104*26*26,
            'planted_selectors':plants,'selector_decodes':104*104,'timing_mutants_detected':mutations,
            'non_global_rotation_witnesses':witnesses,'checks':checks,
            'seconds':time.monotonic()-started}


def run(actual=False):
    ts=trees()
    out={'protocol_sha256':hashlib.sha256((ROOT/'research/TREE-PATH-CIPHER-SPEC.md').read_bytes()).hexdigest(),
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'trees':{n:{k:v for k,v in t.items() if k in ('slots','paths')} for n,t in ts.items()}}
    if not actual:
        out['controls']=controls(ts)
    else:
        start=time.monotonic();data=json.loads((ROOT/'data/k4.json').read_text())
        rr=select(data['ciphertext'],ts,[c['plaintext'] for c in data['cribs']])
        assert all(r['regenerates'] for r in rr)
        out.update({'raw_models':104,'results':rr,'first_survivors':sum(r['first_pass'] for r in rr),
                    'all_survivors':sum(r['all_pass'] for r in rr),
                    'distinct_full_decryptions':len({r['plaintext_sha256'] for r in rr}),
                    'seconds':time.monotonic()-start})
        assert out['seconds']<120
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--actual',action='store_true');parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    args.output.write_text(json.dumps(run(args.actual),indent=2)+'\n')
