"""Traceable scope inventory, not a theorem prover or a new cryptanalysis search.
Audits the canonical register and indexes every tracked Markdown line matching
an explicitly declared exclusion vocabulary. Original artifacts are never edited.
"""
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VOCABULARY=r'\b(?:exclud\w*|reject\w*|contradict\w*|impossib\w*|negative|no survivors|zero survivors|no fits|zero fits)\b'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def local_targets(path,text):
    targets=[]
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if target.startswith('#') or '://' in target or target.startswith('mailto:'):continue
        target=target.split('#')[0].split(':')[0]
        p=(path.parent/target).resolve()
        if p.is_file() and ROOT in p.parents:targets.append(p)
    # Code/result identifiers are also commonly written in backticks instead of links.
    for target in re.findall(r'(?:experiments|results|tests|independent|data)/[A-Za-z0-9_./-]+\.(?:py|mjs|json|md)',text):
        p=ROOT/target
        if p.is_file():targets.append(p.resolve())
    return sorted(set(targets))

def run():
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT).decode().splitlines()
    text=(ROOT/'research/HYPOTHESES.md').read_text();current=text.split('<!-- CURRENT-REGISTER:START -->')[1].split('<!-- CURRENT-REGISTER:END -->')[0]
    entries=[]
    for ident,body in re.findall(r'^### (H-[A-Z0-9-]+)\n(.*?)(?=^### H-|\Z)',current,re.M|re.S):
        f=dict(re.findall(r'^- ([A-Za-z ]+): (.+)$',body,re.M));seen=set();todo=local_targets(ROOT/'research/HYPOTHESES.md',body)
        while todo:
            p=todo.pop()
            if p in seen:continue
            seen.add(p)
            # Resolve the direct report's evidence links one level, not links back into the whole ledger.
            if p.suffix=='.md' and p.name not in ('HYPOTHESES.md','EXPERIMENTS.md') and len(seen)<100:
                for q in local_targets(p,p.read_text(errors='replace')):
                    if q not in seen and q.name not in ('HYPOTHESES.md','EXPERIMENTS.md'):todo.append(q)
        evidence=[str(p.relative_to(ROOT)) for p in sorted(seen)]
        entries.append(dict(id=ident,status=f['Status'],mechanism=f['Mechanism'],exact_tested_scope=f['Tested scope'],unexcluded_scope=f['Untested scope'],missing_inputs=f['Missing inputs'],next_discriminating_test=f['Next discriminating test'],evidence=evidence,verification='Canonical scope reviewed; linked files inventoried. Fresh regression/analytical replays are listed separately. File presence alone does not validate a claim.'))
    claims=[];docs=[]
    for name in tracked:
        p=ROOT/name
        if p.suffix!='.md':continue
        lines=p.read_text(errors='replace').splitlines();matches=[]
        for n,line in enumerate(lines,1):
            if re.search(VOCABULARY,line,re.I):matches.append(dict(line=n,text=line))
        if matches:
            docs.append(dict(path=name,sha256=sha(p),matching_lines=len(matches)))
            for row in matches:claims.append(dict(path=name,**row,review_unit='original independent artifact' if name.startswith('independent/') else 'authored document or retained source report',disposition='Interpret only with the current canonical scope and source chronology; lexical hit is not a separately verified theorem.'))
    # Fresh exact baseline replay; compare proof-bearing fields against retained result.
    import structural_checks
    fresh=structural_checks.run();old=json.loads((ROOT/'results/STRUCT-001.json').read_text())
    assert fresh==old
    from affine_digraph_boundary import verify as affine_verify
    from recurrence_certificate import run as feedback_verify
    affine=affine_verify();feedback=feedback_verify()
    assert affine==json.loads((ROOT/'results/AFFINE-DIGRAPH-PARITY-001.json').read_text())
    assert feedback==json.loads((ROOT/'results/RECURRENCE-CERTIFICATE-REVIEW-001.json').read_text())
    contexts=[]
    for name,alphabet in (('AZ','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),('KRYPTOS','KRYPTOSABCDEFGHIJLMNQUVWXZ')):
        k=[(alphabet.index(c)-alphabet.index(p))%26 for c,p in zip(json.loads((ROOT/'data/k4.json').read_text())['ciphertext'][21:34],'EASTNORTHEAST')]
        witnesses=[]
        for i in range(6,13):
            for j in range(i+1,13):
                if [x%2 for x in k[i-6:i]]==[x%2 for x in k[j-6:j]] and k[i]%2!=k[j]%2:witnesses.append(dict(target_positions=[22+i,22+j],six_lag_parity=[x%2 for x in k[i-6:i]],opposed_outputs=[k[i]%2,k[j]%2]))
        assert witnesses;contexts.append(dict(alphabet=name,witnesses=witnesses))
    proofs=dict(same_alphabet_affine_certificates=affine['analytic_exclusions'],feedback_certificates=feedback['proofs'],autonomous_order_2_to_6_context_certificates=contexts,permutation_deficit=fresh['permutation_only']['deficits'],excluded_periods=fresh['periodic_bijective']['contradicted'],structural_receipt_exact_match=True)
    return dict(version=1,method='All 57 canonical entries plus a complete deterministic lexical inventory over tracked Markdown, using the declared vocabulary. Not an exhaustive semantic parser. Historical counts are retained, not added as independent tests. Regression receipts and fresh replays have different strength.',vocabulary=VOCABULARY,canonical_entries=entries,documents=docs,claim_lines=claims,fresh_analytical_replay=proofs,limitations=['Original third-party/worker artifacts are not rewritten.','Long historical searches are not claimed independently rerun by an evidence-link scan.','Unmatched natural-language claims can exist; canonical scopes remain the status source of truth.','Numerical input changes, preprocessing and transposition can invalidate direct-alignment proofs.'],source_sha256={'research/HYPOTHESES.md':sha(ROOT/'research/HYPOTHESES.md'),'experiments/exclusion_scope_audit.py':sha(Path(__file__))})

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();Path(a.output).write_text(json.dumps(run(),indent=2,ensure_ascii=False)+'\n')
