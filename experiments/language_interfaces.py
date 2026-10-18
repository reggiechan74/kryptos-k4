"""Exact finite-map feasibility interfaces; no historical tables or K4 search.

A script/phonemic spelling and a Latin transport encoding are separate layers.
These functions do not infer translations, pronunciations, or missing tables.
"""
from collections import defaultdict
import time


def unique_decodability(codewords,state_budget=4096,limit=10):
    """Sardinas-Patterson decision for a finite code; empty codewords fail.

    Input codes are distinct symbol outputs. Symbol collisions are checked by
    mapping_audit separately. A non-prefix code may still be uniquely decodable.
    """
    started=time.monotonic()
    if limit<=0:raise TimeoutError('mapping audit deadline reached')
    if state_budget<1:raise ValueError('positive state budget required')
    codes=set(codewords)
    if '' in codes:return False
    residual={b[len(a):] for a in codes for b in codes if a!=b and b.startswith(a)}
    visited=set()
    while residual:
        if time.monotonic()-started>limit:raise TimeoutError('mapping audit deadline reached')
        if '' in residual:return False
        state=frozenset(residual)
        if state in visited:return True
        visited.add(state)
        if len(visited)>state_budget:raise RuntimeError('mapping audit state budget exceeded; undecided')
        residual={b[len(a):] for a in residual for b in codes if b.startswith(a)} | {a[len(b):] for a in residual for b in codes if a.startswith(b)}
    if time.monotonic()-started>limit:raise TimeoutError('mapping audit deadline reached')
    return True


def mapping_audit(mapping):
    if not mapping or any(not isinstance(k,str) or not k or not isinstance(v,str) for k,v in mapping.items()):
        raise ValueError('mapping requires nonempty string symbols and string outputs')
    outputs=defaultdict(list)
    for symbol,value in mapping.items():outputs[value].append(symbol)
    collisions={value:symbols for value,symbols in outputs.items() if len(symbols)>1}
    empty=[symbol for symbol,value in mapping.items() if not value]
    uniquely_decodable=not collisions and not empty and unique_decodability(outputs)
    lengths=sorted({len(value) for value in mapping.values()})
    return {'source_symbols':len(mapping),'distinct_outputs':len(outputs),
            'symbol_collisions':collisions,'empty_output_symbols':empty,
            'output_lengths':lengths,'all_output_characters_AZ':all('A'<=c<='Z' for value in mapping.values() for c in value),
            'uniquely_decodable_symbol_sequences':bool(uniquely_decodable),
            'fixed_length':lengths[0] if len(lengths)==1 else None,
            'scope':'Properties of this exact finite map, not all encodings of its language or script.'}


def forward_symbols(symbols,mapping):
    """Caller supplies explicit tokens; no inferred segmentation/normalization."""
    if any(symbol not in mapping for symbol in symbols):raise ValueError('unknown source symbol')
    return ''.join(mapping[symbol] for symbol in symbols)


def inverse_symbols(encoded,mapping,max_decodes=256,limit=10):
    """Bounded exact inversion; fail explicitly for lossy/ambiguous symbol codes."""
    started=time.monotonic()
    if limit<=0:raise TimeoutError('inverse deadline reached')
    if max_decodes<1:raise ValueError('positive decode budget required')
    audit=mapping_audit(mapping)
    if not audit['uniquely_decodable_symbol_sequences']:
        raise ValueError('mapping is not a lossless uniquely decodable symbol code')
    paths={0:[[]]}
    for offset in range(len(encoded)+1):
        if time.monotonic()-started>limit:raise TimeoutError('inverse deadline reached')
        for path in paths.get(offset,[]):
            for symbol,value in mapping.items():
                if encoded.startswith(value,offset):
                    end=offset+len(value)
                    paths.setdefault(end,[]).append(path+[symbol])
                    if len(paths[end])>max_decodes:raise RuntimeError('decode budget exceeded; not an exhaustive negative')
    result=paths.get(len(encoded),[])
    if time.monotonic()-started>limit:raise TimeoutError('inverse deadline reached')
    if not result:raise ValueError('encoded input has no exact inverse under this map')
    if len(result)!=1:raise ValueError('ambiguous inverse')
    return result[0]


def final_crib_check(final_plaintext,cribs,expected_length=97):
    """Check final English output only, never intermediate-language indices."""
    if not isinstance(final_plaintext,str):raise ValueError('final output must be explicit text')
    alphabet_ok=all('A'<=c<='Z' for c in final_plaintext)
    checks=[{'start':c['start'],'end':c['end'],
             'actual':final_plaintext[c['start']-1:c['end']],
             'matches':final_plaintext[c['start']-1:c['end']]==c['text']} for c in cribs]
    return {'length':len(final_plaintext),'expected_length':expected_length,
            'is_uppercase_AZ':alphabet_ok,'cribs':checks,
            'passes':len(final_plaintext)==expected_length and alphabet_ok and all(c['matches'] for c in checks)}


def length_feasibility(output_length,code_lengths,framing_length=0):
    """Finite reachability of transport lengths, without guessing plaintext."""
    if output_length<0 or framing_length<0 or not code_lengths or any(x<1 for x in code_lengths):
        raise ValueError('positive code lengths and nonnegative lengths required')
    target=output_length-framing_length
    if target<0:return False
    possible=[False]*(target+1);possible[0]=True
    for n in range(1,target+1):possible[n]=any(n>=size and possible[n-size] for size in code_lengths)
    return possible[target]
