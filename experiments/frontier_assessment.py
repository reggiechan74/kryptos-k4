"""Reproducible human-review inventory/preflight; never launches cryptanalysis."""
import argparse,collections,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SPEC=ROOT/'research/specifications/FRONTIER-2026-10-23.json'
FIELDS=('Status','Mechanism','Evidence','Tested scope','Untested scope','Missing inputs','Next discriminating test','Dependencies','Results')

def canonical(text):
    text=text.split('<!-- CURRENT-REGISTER:START -->')[1].split('<!-- CURRENT-REGISTER:END -->')[0];entries={}
    for ident,body in re.findall(r'^### (H-[A-Z0-9-]+)\n(.*?)(?=^### H-|\Z)',text,re.M|re.S):
        if ident in entries:raise ValueError('duplicate stable ID')
        fields=dict(re.findall(r'^- ([A-Za-z ]+): (.+)$',body,re.M))
        if any(not fields.get(k) for k in FIELDS):raise ValueError('incomplete canonical entry '+ident)
        entries[ident]=fields
    return entries

def assess(spec=None,entries=None):
    spec=json.loads(SPEC.read_text()) if spec is None else spec;entries=canonical((ROOT/'research/HYPOTHESES.md').read_text()) if entries is None else entries
    if len(entries)!=spec.get('expected_register_entries',60):raise ValueError('New register size requires a fresh frontier review')
    gates=spec['gates'];ids=[g['id'] for g in gates]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate frontier gate')
    paths={Path(__file__),SPEC,ROOT/'research/HYPOTHESES.md',ROOT/'data/k4.json'};assignments=collections.defaultdict(list)
    for gate in gates:
        if gate['ready_for_new_K4_evaluation'] is not False:raise ValueError('This snapshot cannot authorize launch; new reviewed protocol required')
        for ident in gate['hypotheses']:
            if ident not in entries:raise ValueError('unknown registered hypothesis '+ident)
            assignments[ident].append(gate['id'])
        for p in gate['available']:
            path=(ROOT/p).resolve()
            if ROOT not in path.parents or not path.is_file():raise ValueError('Missing or nonlocal prerequisite '+p)
            paths.add(path)
        # These commands are declared replays, never executed by this preflight.
        command=gate['safe_replay_argv']
        if command is not None and (not command or command[0] not in ('python3','node')):raise ValueError('undeclared replay executable')
    rows=[]
    for ident,fields in entries.items():
        rows.append(dict(id=ident,status=fields['Status'],mechanism=fields['Mechanism'],review_gates=assignments[ident],assessment='specific_gate' if assignments[ident] else 'completed_scoped_domain_requires_new_independent_specification',missing_inputs=fields['Missing inputs'],next_discriminating_test=fields['Next discriminating test'],unexcluded_scope=fields['Untested scope'],ready_for_new_K4_evaluation=False))
    return dict(kind=spec['kind'],decision=spec['decision'],reviewed_main_commit=spec['reviewed_main_commit'],manual_judgment_not_algorithmic_exhaustiveness=True,puzzle_solved=False,registered_entries=len(rows),statuses=dict(collections.Counter(r['status'] for r in rows)),entries=rows,frontier_gates=gates,new_K4_evaluations=0,replay_commands_executed=0,ready_new_K4_experiments=0,not_claimed=spec['not_claimed'],source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args();raw=json.dumps(assess(),indent=2)+'\n'
    if args.output:Path(args.output).write_text(raw)
    else:print(raw,end='')
