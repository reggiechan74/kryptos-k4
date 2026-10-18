"""Tiny fixed, synthetic respelling feasibility check. No flexible mapper."""
import argparse,json,time
from bounded_models import deadline_check
from masking_pilots import check_final
from word_scramble import validate_intermediates
from run_bounded import ROOT,execute,inputs_hashes,validated_baseline
from run_io import specification

SPEC='research/specifications/PHONETIC-SUBSET-001.json'


def respell_word(word):
    if not word or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in word):raise ValueError('explicit uppercase AZ word required')
    result=word.replace('W','V')
    if result[-1]=='D':result=result[:-1]+'T'
    elif result[-1]=='G':result=result[:-1]+'K'
    return result


def controls():
    spec=json.loads((ROOT/SPEC).read_text())
    for word in ['WORD','WEDDING','DOG']:assert respell_word(word)==spec['controls'][word]
    assert respell_word('WET')==respell_word('VET')=='VET'
    assert respell_word('THIN')=='THIN' and respell_word('I')=='I'
    return {'positive_vectors':3,'WET_VET_loss_collision':True,'TH_and_I_rules_not_applied':True}


def run_subset(data,intermediates,limit=5):
    started=time.monotonic();deadline_check(started,limit);validate_intermediates(data,intermediates)
    words=json.loads((ROOT/SPEC).read_text())['known_word_units']
    converted=[respell_word(w) for w in words]
    assert converted==words
    target=[converted[0]+converted[1],converted[2]+converted[3]]
    assert target==[c['plaintext'] for c in data['cribs']]
    records=[]
    for record in intermediates:
        deadline_check(started,limit);q=record['plaintext'];_,original_mask,_=check_final(q,data)
        subset_mask=[q[i]==p for crib,text in zip(data['cribs'],target) for i,p in enumerate(text,crib['start']-1)]
        assert subset_mask==original_mask
        records.append({'alphabet':record['alphabet'],'primer':record['primer'],'feedback':record['feedback'],
                        'original_crib_mask':original_mask,'subset_crib_mask':subset_mask,
                        'original_compatible':all(original_mask),'subset_compatible':all(subset_mask),
                        'rescued':not all(original_mask) and all(subset_mask)})
    assert len(records)==12;deadline_check(started,limit)
    return {'experiment':'PHONETIC-SUBSET-001','known_words':[{'input':a,'output':b,'unchanged':a==b} for a,b in zip(words,converted)],
            'existing_models_checked':12,'rescued_models':sum(r['rescued'] for r in records),
            'all_masks_unchanged':True,'records':records,'controls':controls(),
            'scoring':'none','new_keys':0,'scope':'Only W->V, word-final D->T/G->K and the12existing fixed autokey outputs at unchanged aligned English cribs. No broader respelling/translation conclusion.',
            'alignment_caveat':'Moving Sanborn English-crib indices to a post-linguistic-reconstruction stage is an additional assumption, not an established directly enciphered-English source interpretation.',
            'German_translation':'not specified: exact rendering, English inverse/codebook, word-order and length alignment absent',
            'TH_and_short_I_rules':'not implemented: require fixed pronunciation dictionary, word boundaries and cumulative source/output alignment'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--spec-commit',required=True);parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output-dir',default='results/phonetic-subset-runs');args=parser.parse_args()
    spec=specification(args.spec_commit,SPEC)
    if len(args.code_commit)!=40 or any(c not in '0123456789abcdef' for c in args.code_commit):raise ValueError('full implementation commit required')
    spec['implementation_commit']=args.code_commit;frozen=json.loads((ROOT/SPEC).read_text());artifact=frozen['prior_fixed_autokey_artifact'];holder={}
    def preflight():
        holder['data']=validated_baseline(ROOT/'data/k4.json');holder['intermediates']=json.loads((ROOT/artifact).read_text())['records'];controls()
    files=[SPEC,artifact,'data/k4.json','experiments/phonetic_subset.py','experiments/word_scramble.py','experiments/masking_pilots.py','experiments/run_io.py','experiments/run_bounded.py','experiments/check_baseline.py']
    run_id=execute(args.output_dir,'synthetic-respelling-subset',spec,[('PHONETIC-SUBSET-001',lambda limit:run_subset(holder['data'],holder['intermediates'],limit),5)],inputs_hashes(files),'python3 experiments/phonetic_subset.py --spec-commit '+args.spec_commit+' --code-commit '+args.code_commit,preflight)
    print('completed phonetic subset run',run_id)


if __name__=='__main__':main()
