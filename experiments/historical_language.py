"""LANG-001: exact restricted source-code audit, not translated K4 decryption."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time

from bounded_models import deadline_check
from language_interfaces import mapping_audit,unique_decodability,length_feasibility
from run_bounded import ROOT,execute,inputs_hashes,validated_baseline
from run_io import specification

MANIFEST='data/gost1981_table2_russian.json'
SPEC='research/specifications/LANG-001.json'


def suffix_trace(codewords):
    codes=set(codewords)
    residual={b[len(a):] for a in codes for b in codes if a!=b and b.startswith(a)}
    trace=[sorted(residual)];seen=set()
    while residual:
        if '' in residual:return trace,False
        state=frozenset(residual)
        if state in seen:return trace,True
        seen.add(state)
        if len(seen)>4096:raise RuntimeError('suffix state cap reached')
        residual={b[len(a):] for a in residual for b in codes if b.startswith(a)}|{a[len(b):] for a in residual for b in codes if a.startswith(b)}
        trace.append(sorted(residual))
    return trace,True


class GostCode:
    def __init__(self,mapping):
        self.mapping=dict(mapping)
        if not mapping_audit(mapping)['uniquely_decodable_symbol_sequences']:
            raise ValueError('ambiguous or lossy map')
        self.entries=list(mapping.items())

    def encode(self,text):
        if any(c not in self.mapping for c in text):raise ValueError('outside frozen uppercase Russian-letter domain')
        return ''.join(self.mapping[c] for c in text)

    def decode(self,text):
        if any(c not in ''.join(self.mapping.values()) for c in text):raise ValueError('outside output alphabet')
        paths={0:['']}
        for offset in range(len(text)):
            for prefix in paths.get(offset,[]):
                for source,code in self.entries:
                    if text.startswith(code,offset):
                        end=offset+len(code)
                        paths.setdefault(end,[]).append(prefix+source)
                        if len(paths[end])>256:raise RuntimeError('decode budget reached; incomplete')
        decoded=paths.get(len(text),[])
        if len(decoded)!=1:raise ValueError('no unique complete inverse')
        return decoded[0]


def mapping_controls(manifest):
    alphabet='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    # Independently transcribed source-column labels, not generated from the JSON mapping.
    codewords=['A','B','V','G','D','E','JO','ZH','Z','I','JJ','K','L','M','N','O','P','R','S','T','U','F','KH','C','CH','SH','SHH','"','Y',"'",'EH','JU','JA']
    if manifest['input_alphabet']!=alphabet or list(manifest['mapping'])!=list(alphabet):
        raise ValueError('source inventory/order mismatch')
    if [manifest['mapping'][c] for c in alphabet]!=codewords:raise ValueError('source mapping mismatch')
    code=GostCode(manifest['mapping'])
    for source in alphabet:
        assert code.decode(code.encode(source))==source
    assert code.encode('Ъ')=='"' and code.encode('ЬЬ')=="''"
    assert code.encode('Ъ')!=code.encode('ЬЬ')
    assert code.encode('ЁЙЖХЦЧШЩЭЮЯ')=='JOJJZHKHCCHSHSHHEHJUJA'
    assert not unique_decodability(['A','B','AB'])
    for invalid in ['б',' ',"'",'*','Ѣ']:
        try:code.encode(invalid)
        except ValueError:pass
        else:raise AssertionError('outside-domain source accepted')
    return code


def run_language(data,limit=30):
    started=time.monotonic();deadline_check(started,limit)
    manifest=json.loads((ROOT/MANIFEST).read_text());code=mapping_controls(manifest)
    alphabet=manifest['input_alphabet'];encodings=set();digest=hashlib.sha256();tested=0
    for size in range(4):
        for symbols in itertools.product(alphabet,repeat=size):
            source=''.join(symbols);encoded=code.encode(source)
            assert code.decode(encoded)==source
            assert code.encode(code.decode(encoded))==encoded
            if encoded in encodings:raise AssertionError('collision in exhaustive set')
            encodings.add(encoded);digest.update(source.encode('utf-8')+b'\0'+encoded.encode('ascii')+b'\n')
            tested+=1
            if tested>37060:raise RuntimeError('source-case cap exceeded')
            if tested%128==0:deadline_check(started,limit)
    assert tested==37060
    trace,unique=suffix_trace(manifest['mapping'].values())
    assert trace==[['H','HH'],[]] and unique
    output=set(''.join(manifest['mapping'].values()));latin=output&set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    assert ''.join(sorted(output))==manifest['output_alphabet_ascii_sorted']
    assert len(output)==25 and len(latin)==23
    cipher_support=set(data['ciphertext']);assert len(cipher_support)==26
    stripped={s:''.join(c for c in code.encode(s) if 'A'<=c<='Z') for s in ['Б','БЬ','БЪ']}
    assert set(stripped.values())=={'B'}
    extended=dict(manifest['mapping']);extended["'"]='*'
    assert len(set(''.join(extended.values())))==26
    assert GostCode(extended).decode('*')=="'"
    deadline_check(started,limit)
    return {'experiment':'LANG-001','key_searches':0,'Monte_Carlo_controls':0,
            'GOST':{'source_strings_tested':tested,'distinct_encodings':len(encodings),'collisions':tested-len(encodings),
                'all_roundtrips_pass':True,'source_case_lengths':[0,1,2,3],'enumerated_pair_sha256':digest.hexdigest(),
                'Sardinas_Patterson_suffix_sets':trace,'uniquely_decodable':unique,
                'output_characters':''.join(sorted(output)),'output_support':len(output),'output_latin_letters':''.join(sorted(latin)),
                'missing_K4_letters':''.join(sorted(cipher_support-output)),
                'literal_output_or_permutation':'incompatible: cannot emit Q W X',
                'fixed_character_substitution_then_permutation':'incompatible only for fixed single-output-character substitution of this 25-character transport alphabet, no padding/punctuation extension',
                'quote_deletion_collision':stripped,'quote_deletion_is_invertible':False,
                'source_apostrophe_extension':{'output':'*','support_upper_bound':26,'25_symbol_rejection_applies':False},
                'restricted_31_letter_no_sign_domain_support':len(set(''.join(v for k,v in manifest['mapping'].items() if k not in 'ЪЬ'))),
                '97_transport_characters_source_letter_count_bounds':[33,97],
                'parity_rejection':False,'complete_English_pipeline':'not specified: no exact translation/codebook/alignment or cipher/key family'},
            'Shavian':{'full_48_to_26_single_letter_injection_possible':48<=26,
                'uniform_pair_transport_without_framing_can_have_length_97':length_feasibility(97,[2]),
                'phonemic_inverse_obstacle':{'source_review_example':['too','two'],'same_Shavian_spelling_reported_on_page':3,'exact_conventional_spelling_inverse_without_side_information':False},
                'historical_AZ_transport_encoding':'not found in inspected primary material; no invented table used',
                'outcome':'not yet a specified testable K4 model; not Shavian disproved'},
            'scope':'Exact 1981 GOST Table 2 uppercase 33-letter domain and stated Shavian necessary gates. No exclusion of punctuation/padding extensions, whole-codeword substitutions, polyalphabetic/homophonic ciphers, fractionation, or broader language layers.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--spec-commit',required=True);parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output-dir',default='results/language-runs');args=parser.parse_args()
    spec=specification(args.spec_commit,SPEC)
    if len(args.code_commit)!=40 or any(c not in '0123456789abcdef' for c in args.code_commit):raise ValueError('full implementation commit required')
    spec['implementation_commit']=args.code_commit
    files=[SPEC,MANIFEST,'data/k4.json','experiments/historical_language.py','experiments/language_interfaces.py','experiments/run_bounded.py','experiments/run_io.py','experiments/check_baseline.py']
    holder={}
    def preflight():holder['data']=validated_baseline(ROOT/'data/k4.json')
    run_id=execute(args.output_dir,'historical-language-feasibility',spec,[('LANG-001',lambda limit:run_language(holder['data'],limit),30)],inputs_hashes(files),'python3 experiments/historical_language.py --spec-commit '+args.spec_commit+' --code-commit '+args.code_commit,preflight)
    print('completed language run',run_id)


if __name__=='__main__':main()
