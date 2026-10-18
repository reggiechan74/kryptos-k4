"""Two frozen historical-mechanism pilots. No keys/alphabets fitted to K4."""
import argparse
import itertools
import json
from pathlib import Path
import random
import re
import time

from bounded_models import deadline_check
from ciphers import alphabet_check
from language_interfaces import final_crib_check
from run_bounded import ROOT,execute,inputs_hashes,validated_baseline
from run_io import specification

AUTO_SPEC='research/specifications/MASK-AUTO-001.json'
FM_SPEC='research/specifications/MASK-FM-001.json'


def read_spec(name):return json.loads((ROOT/name).read_text())


def autokey(text,alphabet,primer,feedback,decrypt=False):
    alphabet_check(alphabet)
    if not primer or any(c not in alphabet for c in primer+text):raise ValueError('explicit uppercase A-Z inputs and nonempty primer required')
    if feedback not in ['plaintext','ciphertext']:raise ValueError('unknown feedback')
    given=[alphabet.index(c) for c in text];seed=[alphabet.index(c) for c in primer];out=[];length=len(seed)
    for i,value in enumerate(given):
        if i<length:key=seed[i]
        elif (feedback=='plaintext' and decrypt) or (feedback=='ciphertext' and not decrypt):key=out[i-length]
        else:key=given[i-length]
        out.append((value-key if decrypt else value+key)%26)
    return ''.join(alphabet[i] for i in out)


def check_final(plain,data):
    cribs=[{'start':c['start'],'end':c['end'],'text':c['plaintext']} for c in data['cribs']]
    check=final_crib_check(plain,cribs)
    mask=[plain[i]==p for crib in data['cribs'] for i,p in enumerate(crib['plaintext'],crib['start']-1)]
    if not check['is_uppercase_AZ']:reason='non_AZ_final_output'
    elif len(plain)!=97:reason='final_letter_length_not_97'
    elif not all(mask):reason='crib_mismatch'
    else:reason=None
    return check,mask,reason


def autokey_scan(data,limit=10):
    started=time.monotonic();deadline_check(started,limit);spec=read_spec(AUTO_SPEC);records=[]
    for alphabet in spec['alphabets']:
        for primer in spec['primers']:
            for feedback in spec['feedback_sources']:
                deadline_check(started,limit)
                plain=autokey(data['ciphertext'],alphabet,primer,feedback,True)
                regenerated=autokey(plain,alphabet,primer,feedback)
                exact=regenerated==data['ciphertext'];check,mask,reason=check_final(plain,data)
                if reason is None and not exact:reason='failed_forward_regeneration'
                records.append({'alphabet':alphabet,'primer':primer,'primer_length':len(primer),'feedback':feedback,
                    'plaintext':plain,'final_check':check,'crib_match_mask':mask,'crib_matches':sum(mask),
                    'exact_forward_regeneration':exact,'first_rejecting_condition':reason,'accepted':reason is None})
                if len(records)>12:raise RuntimeError('fixed 12-case cap exceeded')
    assert len(records)==12;deadline_check(started,limit)
    return {'experiment':'MASK-AUTO-001','tested_models':len(records),'accepted_models':sum(r['accepted'] for r in records),
            'records':records,'scoring':'none','scope':'Only 2 fixed alphabets x3 literal primers x2 feedback sources, addition recurrence. No general masking/autokey conclusion.'}


def triple_table(alphabet):
    alphabet_check(alphabet)
    triples=[''.join(t) for t in itertools.product(('.','-','x'),repeat=3) if t!=('x','x','x')]
    return dict(zip(triples,alphabet))


class MorseParseError(ValueError):pass


def morse_encode(message,alphabet):
    if not re.fullmatch(r'[A-Z]+(?: [A-Z]+)*',message):raise ValueError('uppercase words, single ASCII spaces, no punctuation required')
    morse=read_spec(FM_SPEC)['Morse'];table=triple_table(alphabet)
    raw='xx'.join('x'.join(morse[c] for c in word) for word in message.split(' '))
    padding=(-len(raw))%3;stream=raw+'x'*padding
    if 'xxx' in stream:raise AssertionError('unexpected xxx under fixed encoder')
    cipher=''.join(table[stream[i:i+3]] for i in range(0,len(stream),3))
    return {'ciphertext':cipher,'ternary_stream':stream,'padding_x':padding,'raw_ternary_length':len(raw)}


def parse_morse_stream(stream):
    if not stream or any(c not in '.-x' for c in stream):raise MorseParseError('empty_or_nonternary_stream')
    if len(stream)%3:raise MorseParseError('incomplete_triple_stream')
    if stream.startswith('x'):raise MorseParseError('leading_separator')
    trailing=len(stream)-len(stream.rstrip('x'))
    if trailing>2:raise MorseParseError('excess_terminal_padding')
    body=stream[:-trailing] if trailing else stream
    if 'xxx' in body:raise MorseParseError('internal_separator_run_at_least_3')
    inverse={value:key for key,value in read_spec(FM_SPEC)['Morse'].items()}
    output=[]
    for token in re.split('(x+)',body):
        if token=='x':continue
        if token=='xx':output.append(' ');continue
        if token not in inverse:raise MorseParseError('invalid_Morse_letter_run:'+token)
        output.append(inverse[token])
    return {'spaced_plaintext':''.join(output),'plaintext_letters':''.join(output).replace(' ',''),'padding_x':trailing}


def morse_decode(cipher,alphabet):
    inverse={value:key for key,value in triple_table(alphabet).items()}
    if any(c not in inverse for c in cipher):raise MorseParseError('unknown_cipher_symbol')
    stream=''.join(inverse[c] for c in cipher)
    result=parse_morse_stream(stream);result['ternary_stream']=stream
    return result


def fractionated_morse_scan(data,limit=10):
    started=time.monotonic();deadline_check(started,limit);spec=read_spec(FM_SPEC);records=[]
    for alphabet in spec['alphabets']:
        deadline_check(started,limit);inverse={v:k for k,v in triple_table(alphabet).items()}
        stream=''.join(inverse[c] for c in data['ciphertext'])
        record={'alphabet':alphabet,'ternary_stream':stream,'ternary_length':len(stream),
                'spaced_plaintext':None,'plaintext_letters':None,'crib_match_mask':[None]*24,
                'exact_forward_regeneration':None,'accepted':False}
        try:decoded=parse_morse_stream(stream)
        except MorseParseError as error:record['first_rejecting_condition']=str(error)
        else:
            plain=decoded['plaintext_letters'];regenerated=morse_encode(decoded['spaced_plaintext'],alphabet)
            exact=regenerated['ciphertext']==data['ciphertext'];check,mask,reason=check_final(plain,data)
            if reason is None and not exact:reason='failed_forward_regeneration'
            record.update(decoded);record.update({'final_check':check,'crib_match_mask':mask,'crib_matches':sum(mask),
                'exact_forward_regeneration':exact,'first_rejecting_condition':reason,'accepted':reason is None})
        records.append(record)
    assert len(records)==2;deadline_check(started,limit)
    return {'experiment':'MASK-FM-001','tested_models':2,'accepted_models':sum(r['accepted'] for r in records),
            'records':records,'scoring':'none','scope':'Two fixed maps, standard A-Z Morse, exact x/xx separators and deterministic terminal padding; no keyed-alphabet, segmentation, or composite search.'}


def synthetic_data(cipher,plain):
    return {'ciphertext':cipher,'cribs':[{'start':22,'end':34,'plaintext':plain[21:34]},{'start':64,'end':74,'plaintext':plain[63:74]}]}


def autokey_controls():
    spec=read_spec(AUTO_SPEC);vectors=spec['controls']['hand_vectors']
    for feedback,expected in [('plaintext',vectors['plaintext_feedback_ciphertext']),('ciphertext',vectors['ciphertext_feedback_ciphertext'])]:
        actual=autokey(vectors['plaintext'],vectors['alphabet'],vectors['primer'],feedback)
        if actual!=expected:raise AssertionError('hand vector failed before K4 tests: '+feedback+' got '+actual)
        assert autokey(expected,vectors['alphabet'],vectors['primer'],feedback,True)==vectors['plaintext']
    rng=random.Random(20261018);roundtrips=0;plants=0;negative=0;duplicate_acceptances=[]
    for alphabet in spec['alphabets']:
        for primer in spec['primers']:
            for feedback in spec['feedback_sources']:
                samples=[alphabet,'A'*97,primer[:max(1,len(primer)-1)],primer,'' ,''.join(rng.choice(alphabet) for _ in range(97))]
                for plain in samples:
                    cipher=autokey(plain,alphabet,primer,feedback)
                    assert autokey(cipher,alphabet,primer,feedback,True)==plain;roundtrips+=1
                plain=''.join(rng.choice(alphabet) for _ in range(97))
                plain=plain[:21]+'EASTNORTHEAST'+plain[34:63]+'BERLINCLOCK'+plain[74:]
                cipher=autokey(plain,alphabet,primer,feedback);data=synthetic_data(cipher,plain)
                result=autokey_scan(data)
                true=next(r for r in result['records'] if (r['alphabet'],r['primer'],r['feedback'])==(alphabet,primer,feedback))
                assert true['accepted'] and true['plaintext']==plain and true['exact_forward_regeneration'];plants+=1
                duplicate_acceptances.append(result['accepted_models'])
                data['cribs'][0]['plaintext']='A'+data['cribs'][0]['plaintext'][1:]
                altered=autokey_scan(data)
                true=next(r for r in altered['records'] if (r['alphabet'],r['primer'],r['feedback'])==(alphabet,primer,feedback))
                assert not true['accepted'] and not true['crib_match_mask'][0];negative+=1
    return {'hand_vectors':2,'roundtrips':roundtrips,'actual_scanner_planted_recoveries':plants,
            'altered_crib_rejections':negative,'planted_case_total_acceptances_including_duplicates':duplicate_acceptances,'seed':20261018}


def fm_planted_message():
    # Deterministic SYNTHETIC control only: all crib letters, explicit word breaks,
    # and filler adjusted to make exactly 291 ternary symbols. No actual K4 fit.
    plain=list('A'*97);plain[21:34]=list('EASTNORTHEAST');plain[63:74]=list('BERLINCLOCK')
    protected=set(range(21,34))|set(range(63,74));boundaries={12,34,50,74}
    def spaced():return ''.join((' ' if i in boundaries else '')+c for i,c in enumerate(plain))
    for i in range(97):
        if len(morse_encode(spaced(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ')['ternary_stream'])<=291:break
        if i not in protected:plain[i]='E'
    message=spaced();assert len(message.replace(' ',''))==97
    assert len(morse_encode(message,'ABCDEFGHIJKLMNOPQRSTUVWXYZ')['ternary_stream'])==291
    return message


def morse_controls():
    spec=read_spec(FM_SPEC);example=spec['controls']['ACA_example'];encoded=morse_encode(example['plaintext'],example['alphabet'])
    if encoded['ciphertext']!=example['ciphertext'] or encoded['padding_x']!=example['terminal_padding_x']:
        raise AssertionError('ACA example failed before K4 tests: '+str(encoded))
    assert morse_decode(example['ciphertext'],example['alphabet'])['spaced_plaintext']==example['plaintext']
    expected=['...','..-','..x','.-.','.--','.-x','.x.','.x-','.xx','-..','-.-','-.x','--.','---','--x','-x.','-x-','-xx','x..','x.-','x.x','x-.','x--','x-x','xx.','xx-']
    assert list(triple_table(spec['alphabets'][0]))==expected
    assert len(set(spec['Morse'].values()))==26
    padding=set();roundtrips=0
    for alphabet in spec['alphabets']:
        for message in list(spec['Morse'])+['E E','A I','T E A I','I','E','S','COME AT ONCE']:
            encoded=morse_encode(message,alphabet);padding.add(encoded['padding_x'])
            assert morse_decode(encoded['ciphertext'],alphabet)['spaced_plaintext']==message;roundtrips+=1
    assert padding=={0,1,2}
    for invalid in ['x..','...xxx...','......','.xxxxx','..']:
        try:parse_morse_stream(invalid)
        except MorseParseError:pass
        else:raise AssertionError('invalid stream accepted: '+invalid)
    message=fm_planted_message();plants=0
    for alphabet in spec['alphabets']:
        cipher=morse_encode(message,alphabet)['ciphertext'];assert len(cipher)==97
        result=fractionated_morse_scan(synthetic_data(cipher,message.replace(' ','')))
        true=next(r for r in result['records'] if r['alphabet']==alphabet)
        assert true['accepted'] and true['spaced_plaintext']==message and true['exact_forward_regeneration'];plants+=1
    return {'ACA_example_pass':True,'ACA_example_ciphertext':encoded_example_cipher(), 'ACA_padding_x':2,
            'roundtrips':roundtrips,'terminal_padding_values':sorted(padding),'triple_maps_verified':26,
            'actual_scanner_planted_recoveries':plants,'synthetic_97letter_cipher_97letter_final_message':message,
            'crib_indices_checked_after_space_removal':True,
            'fixture_correction_before_K4':'.-xx.. is valid A I, not an invalid stream; moved to positive controls. This changes no cipher rule or candidate scope.'}


def encoded_example_cipher():
    e=read_spec(FM_SPEC)['controls']['ACA_example'];return morse_encode(e['plaintext'],e['alphabet'])['ciphertext']


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pilot',choices=['autokey','morse'],required=True)
    parser.add_argument('--spec-commit',required=True);parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output-dir',default='results/masking-runs');args=parser.parse_args()
    specfile=AUTO_SPEC if args.pilot=='autokey' else FM_SPEC;name='MASK-AUTO-001' if args.pilot=='autokey' else 'MASK-FM-001'
    spec=specification(args.spec_commit,specfile)
    if len(args.code_commit)!=40 or any(c not in '0123456789abcdef' for c in args.code_commit):raise ValueError('full implementation commit required')
    spec['implementation_commit']=args.code_commit;holder={}
    def preflight():holder['data']=validated_baseline(ROOT/'data/k4.json')
    def action(limit):
        started=time.monotonic();deadline_check(started,limit)
        controls=autokey_controls() if args.pilot=='autokey' else morse_controls()
        deadline_check(started,limit)
        result=autokey_scan(holder['data'],limit) if args.pilot=='autokey' else fractionated_morse_scan(holder['data'],limit)
        result['controls']=controls;deadline_check(started,limit);return result
    files=[specfile,'data/k4.json','experiments/masking_pilots.py','experiments/ciphers.py','experiments/language_interfaces.py','experiments/run_bounded.py','experiments/run_io.py','experiments/check_baseline.py',FM_SPEC]
    run_id=execute(args.output_dir,name,spec,[(name,action,10)],inputs_hashes(files),'python3 experiments/masking_pilots.py --pilot '+args.pilot+' --spec-commit '+args.spec_commit+' --code-commit '+args.code_commit,preflight)
    print('completed',name,run_id)


if __name__=='__main__':main()
