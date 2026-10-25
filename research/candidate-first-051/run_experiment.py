#!/usr/bin/env python3
"""Stage-gated, deterministic local control and target runner. No network/API calls."""
import argparse
import concurrent.futures
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pilot as p

ROOT = Path(__file__).resolve().parent
AUDITED_SOURCE_NAMES = ("PROTOCOL.md", "pilot.py", "run_experiment.py", "test_pilot.py", "config.json",
                        "running_key.txt", "bank.json", "heldout.json", "controls.json")


def config():
    c = p.load_json(ROOT / "config.json")
    assert c["description_count_per_candidate"] == len(p.TABLEAUX)*len(p.STRUCTURES)*len(p.PERIODS)
    assert c["period_seed_lengths"] == [min(p.PERIODS), max(p.PERIODS)]
    assert c["candidate_count"] == 32 and c["length"] == p.LENGTH
    assert c["control_alpha"] == .05 and c["minimum_score_bits"] == 16
    return c


def build_controls():
    """Generate and freeze ciphertexts/keys before any scoring, never using K4."""
    bank = p.validate_bank(p.load_json(ROOT / "bank.json"))
    group = {g: [r for r in bank if r["group"] == g] for g in ("thematic", "neutral")}
    schedule = [r for pair in zip(group["thematic"],group["neutral"]) for r in pair]
    heldout = p.load_json(ROOT / "heldout.json")
    text = heldout["text"]
    p.validate_ciphertext(text)
    assert text not in {r["text"] for r in bank}
    for start, word in p.CRIBS:
        assert text[start:start+len(word)] == word
    running = p.letters((ROOT / "running_key.txt").read_text())
    assert len(running) >= 97 + 13*11
    controls = []

    def append(kind, ti, structure, seed, record, label, running_key=None):
        t = p.TABLEAUX[ti]
        if running_key is None:
            cipher, key = p.encrypt_structured(record["text"],seed,t,structure)
        else:
            key = tuple(p.AZ.index(c) for c in running_key)
            cipher = p.encrypt_key(record["text"],key,t)
        cid = f"C{len(controls)+1:03}"
        controls.append({"id":cid,"kind":kind,"tableau_index_zero_based":ti,"tableau_id":t.id,
                         "structure":structure,"seed_AZ":p.decode(seed,"AZ") if seed else None,
                         "full_key_AZ":p.decode(key,"AZ"),"seed_length":len(seed) if seed else None,
                         "plaintext_id":record["id"],"plaintext_group":record.get("group","heldout"),
                         "plaintext":record["text"],"ciphertext":cipher,"construction_label":label,
                         "calibration_rng_label":f"{cid}|calibration",
                         "validation_rng_label":f"{cid}|validation"})

    simple_seeds = {"periodic":"KRYPTOS","plaintext_autokey":"PALIMPSEST","ciphertext_autokey":"ABSCISSA"}
    for ti,t in enumerate(p.TABLEAUX):
        for structure in p.STRUCTURES:
            seed = tuple(p.AZ.index(c) for c in simple_seeds[structure])
            append("simple",ti,structure,seed,schedule[len(controls)%32],f"simple|{t.id}|{structure}")
    for ti,t in enumerate(p.TABLEAUX):
        for structure in ("periodic","plaintext_autokey" if ti%2==0 else "ciphertext_autokey"):
            label=f"hard-key|{t.id}|{structure}"
            rng=p.rng_for(label)
            seed=tuple(rng.randrange(26) for _ in range(29))
            append("structured_hard",ti,structure,seed,schedule[len(controls)%32],label)
    for ti,t in enumerate(p.TABLEAUX):
        append("running_key",ti,"unrestricted_running",(),schedule[len(controls)%32],
               f"running|offset={13*ti}",running[13*ti:13*ti+97])
    for ti,t in enumerate(p.TABLEAUX):
        structure=p.STRUCTURES[ti%3]
        seed=tuple(p.AZ.index(c) for c in simple_seeds[structure])
        append("bank_absent",ti,structure,seed,heldout,f"absent|{t.id}|{structure}")
    assert len(controls)==84
    return controls


def verify_audited_sources(audit, root=ROOT):
    if audit.get("passed") is not True:
        raise ValueError("Independent implementation audit has not passed")
    audited=audit.get("audited_sha256")
    if not isinstance(audited,dict):
        raise ValueError("Audit must bind all required sources through audited_sha256")
    for name in AUDITED_SOURCE_NAMES:
        if name not in audited or p.sha256_file(root/name)!=audited[name]:
            raise ValueError(f"Audited source hash missing or changed: {name}")


def freeze_sources():
    audit_path = ROOT / "implementation_audit.json"
    audit = p.load_json(audit_path)
    verify_audited_sources(audit)
    paths=[ROOT/x for x in AUDITED_SOURCE_NAMES]+[audit_path]
    paths += sorted(f for f in (ROOT/"authors").iterdir() if f.is_file())
    paths += [ROOT/"controls"/"held_out_message.json"]
    manifest={"version":config()["version"],"utc":datetime.now(timezone.utc).isoformat(),
              "status":"frozen before any real-bank/control/K4 scores",
              "files":{str(f.relative_to(ROOT)):p.sha256_file(f) for f in paths},
              "environment":p.environment_record()}
    if (ROOT/"freeze.json").exists():
        raise ValueError("Existing freeze manifest must not be overwritten")
    p.write_json(ROOT/"freeze.json",manifest)
    return manifest


def verify_freeze():
    manifest=p.load_json(ROOT/"freeze.json")
    for relative,digest in manifest["files"].items():
        if p.sha256_file(ROOT/relative)!=digest:
            raise ValueError(f"Frozen source hash mismatch: {relative}")
    return p.sha256_file(ROOT/"freeze.json")


def control_gate(results):
    c=config()
    simple=[r for r in results if r["kind"]=="simple"]
    hard=[r for r in results if r["kind"]=="structured_hard"]
    absent=[r for r in results if r["kind"]=="bank_absent"]
    counts={s:sum(r["successful_recovery"] for r in simple if r["planted_structure"]==s) for s in p.STRUCTURES}
    n_simple=sum(r["successful_recovery"] for r in simple)
    n_hard=sum(r["successful_recovery"] for r in hard)
    n_validation=sum(r["validation_flags"] for r in simple+hard)
    n_absent=sum(r["flagged"] for r in absent)
    running=[r for r in results if r["kind"]=="running_key"]
    complete=(len(results)==84 and len(simple)==36 and len(hard)==24 and len(absent)==12 and len(running)==12
              and sum(r["validation_count"] for r in simple+hard)==600)
    checks={"complete":complete,
            "simple_recovery":n_simple>=c["minimum_simple_success"],
            "simple_each_structure":all(n>=c["minimum_simple_per_structure"] for n in counts.values()),
            "hard_recovery":n_hard>=c["minimum_hard_success"],
            "matched_null_flags":n_validation<=c["maximum_inscope_validation_flags"],
            "absent_target_flags":n_absent<=c["maximum_absent_target_flags"]}
    return {"passed":all(checks.values()),"checks":checks,"simple_success":n_simple,"simple_total":len(simple),
            "simple_success_by_structure":counts,"hard_success":n_hard,"hard_total":len(hard),
            "validation_flags":n_validation,"validation_total":sum(r["validation_count"] for r in simple+hard),
            "absent_target_flags":n_absent,"absent_target_total":len(absent),
            "independence_warning":"Flags share calibration sets and a fixed bank; not independent Bernoulli trials."}


def run_controls(workers):
    freeze_hash=verify_freeze()
    c=config()
    bank=p.validate_bank(p.load_json(ROOT/"bank.json"))
    controls=p.load_json(ROOT/"controls.json")
    assert controls==build_controls(),"Frozen controls do not reproduce"
    scorer=p.Scorer(bank)
    outdir=ROOT/"results"/"controls"
    outdir.mkdir(parents=True,exist_ok=True)
    results=[]
    start=time.monotonic()
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers,initializer=p.init_worker,initargs=(bank,)) as executor:
        for control in controls:
            outfile=outdir/f"{control['id']}.json"
            if outfile.exists():
                cached=p.load_json(outfile)
                if cached["freeze_sha256"]!=freeze_hash:
                    raise ValueError("Cached result belongs to different freeze")
                results.append(cached["summary"])
                continue
            cipher=control["ciphertext"]
            scores=scorer.score(cipher,details=True)
            diagnostics=p.exact_diagnostics(bank,cipher)
            calibration=p.run_nulls(bank,cipher,c["control_calibration_nulls_per_target"],control["calibration_rng_label"],executor)
            if control["kind"] in ("simple","structured_hard"):
                nv=c["validation_nulls_per_inscope_target"]
            elif control["kind"]=="bank_absent":
                nv=c["validation_nulls_per_absent_target"]
            else:
                nv=0
            validation=p.run_nulls(bank,cipher,nv,control["validation_rng_label"],executor)
            maximum=scores["maximum_score_bits"]
            pv=p.pvalue(maximum,calibration["maximum_scores_bits"])
            top=scores["ranked_candidates"][0]
            unique_correct=scores["tied_top_candidate_ids"]==[control["plaintext_id"]]
            is_flagged=p.flag(maximum,pv)
            v_flags=[p.flag(v,p.pvalue(v,calibration["maximum_scores_bits"])) for v in validation["maximum_scores_bits"]]
            summary={"control_id":control["id"],"kind":control["kind"],"planted_candidate_id":control["plaintext_id"],
                     "planted_group":control["plaintext_group"],"planted_tableau":control["tableau_id"],
                     "planted_structure":control["structure"],"planted_seed_length":control["seed_length"],
                     "maximum_score_bits":maximum,"p_value":pv,"flagged":is_flagged,
                     "top_candidate_id":top["candidate_id"],"unique_correct_candidate":unique_correct,
                     "top_exact_full_fit":top["exact_full_fit"],
                     "recovered_tableau_id":top["tableau_id"],"recovered_structure":top["structure"],
                     "recovered_seed_AZ":top["seed_AZ"],"recovered_r":top["r"],
                     "planted_tableau_label_match":top["tableau_id"]==control["tableau_id"],
                     "planted_structure_label_match":top["structure"]==control["structure"],
                     "planted_seed_label_match":top["seed_AZ"]==control["seed_AZ"],
                     "planted_full_key_label_match":top["full_key_AZ"]==control["full_key_AZ"],
                     "label_comparison_note":"Equal score is not proof of model equivalence; exact alternative descriptions only establish same-input encryption representation.",
                     "successful_recovery":bool(unique_correct and is_flagged and top["exact_full_fit"]),
                     "margin_bits":scores["different_plaintext_margin_bits"],
                     "validation_count":nv,"validation_flags":sum(v_flags),"validation_flag_vector":v_flags}
            result={"freeze_sha256":freeze_hash,"control":control,"scores":scores,
                    "exact_diagnostics":diagnostics,"calibration":calibration,"validation":validation,"summary":summary}
            p.write_json(outfile,result)
            results.append(summary)
            p.write_json(ROOT/"results"/"control_progress.json",{"completed":len(results),"total":len(controls),
                         "elapsed_seconds":time.monotonic()-start,"latest":summary})
            print(json.dumps({"completed":len(results),"of":len(controls),**summary}),flush=True)
    gate=control_gate(results)
    gate.update({"freeze_sha256":freeze_hash,"elapsed_seconds":time.monotonic()-start,"controls":results})
    p.write_json(ROOT/"results"/"pretarget_gate.json",gate)
    return gate


def run_target(path,workers):
    freeze_hash=verify_freeze()
    gate=p.load_json(ROOT/"results"/"pretarget_gate.json")
    if gate.get("passed") is not True or gate["freeze_sha256"]!=freeze_hash:
        raise ValueError("Pretarget gate did not pass for this frozen implementation")
    outfile=ROOT/"results"/"target.json"
    if outfile.exists():
        raise ValueError("Target already scored; refusing a second target run")
    c=config()
    cipher=Path(path).read_text().strip()
    p.validate_ciphertext(cipher)
    bank=p.validate_bank(p.load_json(ROOT/"bank.json"))
    target_hash=hashlib.sha256(cipher.encode()).hexdigest()
    receipt_path=ROOT/"results"/"target_receipt.json"
    if receipt_path.exists() and p.load_json(receipt_path)["sha256"] != target_hash:
        raise ValueError("A different target was already received; target replacement prohibited")
    p.write_json(receipt_path,{"sha256":target_hash,"length":len(cipher),
                 "freeze_sha256":freeze_hash,"utc":datetime.now(timezone.utc).isoformat()})
    scorer=p.Scorer(bank)
    scores=scorer.score(cipher,details=True)
    diagnostics=p.exact_diagnostics(bank,cipher)
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers,initializer=p.init_worker,initargs=(bank,)) as executor:
        nulls=p.run_nulls(bank,cipher,c["target_nulls"],"K4|conditional-null",executor)
    value=scores["maximum_score_bits"]
    pv=p.pvalue(value,nulls["maximum_scores_bits"])
    checks={"minimum_score":value>=c["minimum_score_bits"],"global_p":pv<=c["target_alpha"],
            "different_plaintext_margin":scores["different_plaintext_margin_bits"]>=c["target_minimum_margin_bits"]}
    result={"freeze_sha256":freeze_hash,"target_sha256":target_hash,"ciphertext":cipher,
            "scores":scores,"exact_diagnostics":diagnostics,"conditional_nulls":nulls,"global_p_value":pv,
            "expansion_gate":{"passed":all(checks.values()),"checks":checks},
            "interpretation":"Conditional structural-key evidence only; no natural-language-key recognizer and no historical solution claim."}
    p.write_json(outfile,result)
    return {"target_sha256":target_hash,"maximum_score_bits":value,"global_p_value":pv,
            "margin_bits":scores["different_plaintext_margin_bits"],"expansion_gate":result["expansion_gate"]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("build-controls")
    sub.add_parser("freeze")
    sub.add_parser("verify-freeze")
    controls=sub.add_parser("controls")
    controls.add_argument("--workers",type=int,default=8)
    target=sub.add_parser("target")
    target.add_argument("path")
    target.add_argument("--workers",type=int,default=8)
    args=parser.parse_args()
    if args.command=="build-controls":
        if (ROOT/"freeze.json").exists():raise ValueError("Cannot replace frozen controls")
        value=build_controls()
        p.write_json(ROOT/"controls.json",value)
        print(json.dumps({"controls":len(value),"sha256":p.sha256_file(ROOT/"controls.json")},indent=2))
    elif args.command=="freeze":print(json.dumps(freeze_sources(),indent=2))
    elif args.command=="verify-freeze":print(verify_freeze())
    elif args.command=="controls":print(json.dumps(run_controls(args.workers),indent=2))
    elif args.command=="target":print(json.dumps(run_target(args.path,args.workers),indent=2))


if __name__=="__main__":main()
