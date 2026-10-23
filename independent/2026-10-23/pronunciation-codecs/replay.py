#!/usr/bin/env python3
"""Source-fixed representation audit. No cipher key or offset search."""
import hashlib, itertools, json, pathlib, re, unicodedata

HERE = pathlib.Path(__file__).resolve().parent
spec = json.loads((HERE / 'spec.json').read_text())

def metrics(s):
    s = unicodedata.normalize('NFC', s)
    return {'text': s, 'codepoints': len(s), 'utf8_bytes': len(s.encode()),
            'glyph_inventory': sorted(set(s)), 'glyph_domain_size': len(set(s)),
            'literal_AZ': bool(re.fullmatch('[A-Z]+', s))}

def borders(s):
    return [n for n in range(1, len(s)) if s[:n] == s[-n:]]

def framed_roundtrip(tokens):
    # This preserves tokens only, not English spelling. No cipher input claim.
    payload = json.dumps(tokens, ensure_ascii=True, separators=(',', ':'))
    return json.loads(payload) == tokens

def arpa_tokens(s):
    return [re.sub('[012]$', '', t) for t in s.split()]

def ahd_normalize(s):
    return ''.join(c for c in unicodedata.normalize('NFC', s)
                   if c not in '()-\uE01F\u2032 /')

mapping = {'i':'i', 'ː':':', 'ɔ':'O', 'θ':'T', 'ɜ':'3', 'ɪ':'I', 'ɒ':'Q',
           **{x:x for x in 'bklnst'}}

def sampa_normalize(s):
    return ''.join(mapping[c] for c in s if c not in 'ˈˌ /.-')

results = {'id': spec['id'], 'spec_sha256': hashlib.sha256((HERE/'spec.json').read_bytes()).hexdigest(),
           'codecs': [], 'controls': {}}

for codec in spec['codecs']:
    cid = codec['id']
    words = {}
    for word, raw in codec['raw'].items():
        raws = raw if isinstance(raw, list) else [raw]
        entries = []
        for variant, raw_entry in enumerate(raws):
            if cid == 'CMU_ARPABET':
                tokens = arpa_tokens(raw_entry)
                normalized = ''.join(tokens)
            else:
                ts = codec['tokens'][word]
                tokens = ts[variant] if isinstance(ts[0], list) else ts
                normalized = (sampa_normalize if cid.startswith('SAMPA') else ahd_normalize)(raw_entry)
            assert ''.join(tokens) == normalized, (cid, word)
            assert framed_roundtrip(tokens)
            entries.append({'variant': variant, 'raw': metrics(raw_entry),
                            'normalized': metrics(normalized), 'tokens': tokens,
                            'token_count': len(tokens)})
        words[word] = entries
    streams = []
    for block_index, block in enumerate(spec['segmentation']):
        for variant_indices in itertools.product(*(range(len(words[w])) for w in block)):
            chosen = [words[w][i] for w,i in zip(block, variant_indices)]
            tokens = [t for x in chosen for t in x['tokens']]
            normalized = ''.join(x['normalized']['text'] for x in chosen)
            raw_join = ''.join(x['raw']['text'] for x in chosen)
            assert framed_roundtrip(tokens)
            n = [13,11][block_index]
            row = {'block':block, 'variant_indices':variant_indices,
                   'normalized':metrics(normalized), 'raw_lexical_concatenation':metrics(raw_join),
                   'tokens':tokens, 'token_count':len(tokens),
                   'one_letter_per_token_local_length_match':len(tokens)==n,
                   'one_letter_per_codepoint_local_length_match':len(normalized)==n,
                   'word_token_boundaries':[x['token_count'] for x in chosen],
                   'word_codepoint_boundaries':[x['normalized']['codepoints'] for x in chosen],
                   'framed_tokens_roundtrip':True}
            if cid == 'CMU_ARPABET':
                stressed = [t for w in block for t in codec['raw'][w].split()]
                row['stressed_compact_audit'] = metrics(''.join(stressed))
                row['stressed_space_delimited_audit'] = metrics(' '.join(stressed))
                row['stressless_space_delimited_audit'] = metrics(' '.join(tokens))
            if block_index == 0:
                east_tokens = words['EAST'][0]['tokens']
                row['source_EAST_token_prefix_suffix'] = (tokens[:len(east_tokens)] == east_tokens == tokens[-len(east_tokens):])
                assert row['source_EAST_token_prefix_suffix']
            streams.append(row)
    observed_tokens = sorted({t for es in words.values() for e in es for t in e['tokens']})
    observed_glyphs = sorted({c for es in words.values() for e in es for c in e['normalized']['text']})
    results['codecs'].append({'id':cid, 'words':words, 'streams':streams,
                             'observed_token_inventory':observed_tokens,
                             'observed_token_domain_size':len(observed_tokens),
                             'observed_glyph_inventory':observed_glyphs,
                             'observed_glyph_domain_size':len(observed_glyphs)})

# Only the disclosed first window is tested, never arbitrary shifts.
c = 'FLRVQQPRNGKSS'
results['border_certificate'] = {'ciphertext':c,'proper_border_lengths':borders(c),
   'F_positions_zero_based':[i for i,x in enumerate(c) if x=='F'],
   'conclusion':'No non-erasing context-free concatenative token code maps any frozen first stream exactly onto this fixed window.',
   'conditions':['This window is the complete encoded EAST+NORTHEAST block.',
                 'The same input token always emits the same nonempty output codeword.',
                 'No outer stateful cipher, transposition, positional salt or inserted padding.']}
assert not borders(c)

# Positive border control and negative mutation control.
east = ['IY','S','T']
stream = ['IY','S','T','N','AO','R','TH','IY','S','T']
code = {'IY':'AB','S':'C','T':'DE','N':'F','AO':'GH','R':'I','TH':'JK'}
synthetic = ''.join(code[t] for t in stream)
encoded_east = ''.join(code[t] for t in east)
assert synthetic.startswith(encoded_east) and synthetic.endswith(encoded_east)
assert len(encoded_east) in borders(synthetic)
mutated = synthetic[:-1] + 'Z'
assert len(encoded_east) not in borders(mutated)

# Unframed codeword streams are not universally uniquely decodable.
ambiguous = [(['NG'], ['N','G']), (['tS'],['t','S']), (['th'],['t','h'])]
for a,b in ambiguous:
    assert a!=b and ''.join(a)==''.join(b)

# Official English SAMPA token inventory, not a new cipher alphabet.
sampa_cons = 'p b t d k g tS dZ f v T D s z S Z h m n N r l w j'.split()
sampa_vowels = 'I e { Q V U @ i: eI aI OI u: @U aU 3: A: O: I@ e@ U@'.split()
sampa_domain = sampa_cons+sampa_vowels
assert len(sampa_domain)==44
arpa_domain = 'AA AE AH AO AW AY B CH D DH EH ER EY F G HH IH IY JH K L M N NG OW OY P R S SH T TH UH UW V W Y Z ZH'.split()
assert len(arpa_domain)==39
excerpt = (HERE/'cmu-excerpt.txt').read_text()
assert 'knight N AY1 T' in excerpt and 'night N AY1 T' in excerpt
results['controls'] = {'synthetic_variable_length_border':synthetic,
   'synthetic_prefix_suffix':encoded_east,'mutation_breaks_expected_border':True,
   'unframed_ambiguity_witnesses':[{'a':a,'b':b,'same_text':''.join(a)} for a,b in ambiguous],
   'cmu_spelling_noninvertibility':{'NIGHT':['N','AY1','T'],'KNIGHT':['N','AY1','T']},
   'arpa_base_inventory':arpa_domain,'arpa_base_inventory_size':39,
   'arpa_base_char_inventory':sorted(set(''.join(arpa_domain))),
   'sampa_english_inventory':sampa_domain,'sampa_english_inventory_size':44,
   'sampa_char_inventory':sorted(set(''.join(sampa_domain))),
   'token_roundtrips':'All frozen words and blocks passed lossless JSON token-array roundtrips. No exact-English inverse claimed.'}

(HERE/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
for codec in results['codecs']:
    for s in codec['streams']:
        m=s['normalized']
        print(codec['id'], '/'.join(s['block']),s['variant_indices'],repr(m['text']),
              'tokens',s['token_count'],'codepoints',m['codepoints'],'bytes',m['utf8_bytes'])
print('Fixed target proper borders:', results['border_certificate']['proper_border_lengths'])
print('All assertions passed; no key or offset search performed.')
