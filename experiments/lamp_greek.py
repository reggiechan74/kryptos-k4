"""Frozen LAMP-GREEK-025; ordinal codec hypotheses, not historical claims."""
from collections import Counter
import hashlib
import itertools
import math
import resource
import time
from conditional_face_lamp import ALPHABETS, WINDOWS, lamp_bits, lamp_inverse, literal_plant

GREEK='ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
LATIN='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ROLES=('L','B','G')
STARTS=(0,58,719,1438)


def check_budget(start,seconds):
    if time.monotonic()-start>seconds:raise TimeoutError('frozen stage elapsed budget; unresolved')
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Darwin bytes; Linux KiB. This project executes on Darwin.
    import sys
    if sys.platform!='darwin':rss*=1024
    if rss>512*1024**2:raise MemoryError('frozen 512 MiB RSS cap; unresolved')


def ordinal(minute,indicator,reverse=False):
    return sum(bit*(24-j if reverse else j+1) for j,bit in enumerate(lamp_bits(minute,indicator)))


def ordinal_oracle(minute,indicator,reverse=False):
    h,m=divmod(minute,60);a,b=h//5,h%5;c,d=m//5,m%5
    forward=indicator+a*(a+3)//2+b*(b+11)//2+c*(c+19)//2+d*(d+41)//2
    return 25*(indicator+a+b+c+d)-forward if reverse else forward


VALUES=tuple(tuple(tuple(ordinal_oracle(t,p,reverse) for t in range(1440)) for p in (0,1)) for reverse in (False,True))


def digits(rank,width):
    if not isinstance(rank,int) or not 0<=rank<24**width:raise ValueError('rank outside fixed width')
    out=[]
    for _ in range(width):out.append(GREEK[rank%24]);rank//=24
    return ''.join(reversed(out))


def undigits(text,limit):
    rank=0
    for c in text:rank=24*rank+GREEK.index(c)
    if rank>=limit:raise ValueError('unused rank')
    return rank


def frame(text):
    return ''.join(GREEK[LATIN.index(c)] if c in LATIN[:23] else GREEK[23]+GREEK[LATIN.index(c)-23] for c in text)


def unframe(text):
    out=[];i=0
    while i<len(text):
        v=GREEK.index(text[i]);i+=1
        if v==23:
            if i==len(text):raise ValueError('dangling escape')
            tail=GREEK.index(text[i]);i+=1
            if tail>2:raise ValueError('invalid escape tail')
            v=23+tail
        out.append(LATIN[v])
    return ''.join(out)


def model(role,reverse,t,p,name,eq):
    return dict(role=role,order='reverse' if reverse else 'row_major',start_minute=t,indicator=p,alphabet=name,equation=eq)


def parameters():
    for role,rev,t,p,name,eq in itertools.product(ROLES,(False,True),range(1440),(0,1),ALPHABETS,('plus','beaufort')):
        yield model(role,rev,t,p,name,eq)


def crypt(text,m,decrypt=False,oracle=False):
    a=ALPHABETS[m['alphabet']];role=m['role'];rev=m['order']=='reverse';t=m['start_minute'];p=m['indicator'];eq=m['equation']
    if any(c not in LATIN for c in text):raise ValueError('uppercase A-Z required')
    def key(i):return ordinal((t+i)%1440,p,rev) if oracle else VALUES[int(rev)][p][(t+i)%1440]
    def op(v,k,n):return ((v-k if decrypt else v+k) if eq=='plus' else k-v)%n
    if role=='L':return ''.join(a[op(a.index(c),key(i),26)] for i,c in enumerate(text))
    if role=='B':
        out=[]
        for i in range(0,len(text),2):
            block=text[i:i+2];n=26**len(block);rank=0
            for c in block:rank=26*rank+a.index(c)
            # Complete internal bridge, including singleton's separate width.
            assert undigits(digits(rank,3 if len(block)==2 else 2),n)==rank
            v=op(rank,key(i//2),n)
            out.append(a[v//26]+a[v%26] if len(block)==2 else a[v])
        return ''.join(out)
    if role!='G':raise ValueError('unknown role')
    if decrypt:
        if any(c not in a[:24] for c in text):raise ValueError('outside serialized Greek support')
        raw=''.join(GREEK[op(a.index(c),key(i),24)] for i,c in enumerate(text))
        return unframe(raw)
    return ''.join(a[op(GREEK.index(c),key(i),24)] for i,c in enumerate(frame(text)))


def first_constraints(cipher,role,a,eq):
    """Necessary and sufficient first-crib checks for length-preserving L/B."""
    known={start+j:c for start,word in WINDOWS[:1] for j,c in enumerate(word)}
    checks=[]
    if role=='L':
        for i,c in known.items():checks.append((i,{(a.index(cipher[i])+(-1 if eq=='plus' else 1)*a.index(c))%26},26))
    else:
        for i in sorted({2*(j//2) for j in known}):
            block=cipher[i:i+2];n=26**len(block);cv=0
            for c in block:cv=26*cv+a.index(c)
            options=[(a.index(known[j]),) if j in known else range(26) for j in range(i,i+len(block))]
            allowed=set()
            for xs in itertools.product(*options):
                rank=0
                for x in xs:rank=26*rank+x
                allowed.add((cv+(-1 if eq=='plus' else 1)*rank)%n)
            checks.append((i//2,allowed,n))
    return checks


def select(cipher,start=None,seconds=120):
    start=time.monotonic() if start is None else start
    records=[];stats={};raw=23040
    for role in ROLES:
        st=dict(raw_descriptions=raw,support_or_length_pruned=0,first_constraints_tested=0,full_decryptions=0,first_survivors=0,all_survivors=0)
        for name,a in ALPHABETS.items():
            if (role in ('L','B') and len(cipher)!=97) or (role=='G' and any(c not in a[:24] for c in cipher)):
                st['support_or_length_pruned']+=11520;continue
            for eq in ('plus','beaufort'):
                checks=first_constraints(cipher,role,a,eq) if role!='G' else None
                for rev,p in itertools.product((False,True),(0,1)):
                    vals=VALUES[int(rev)][p]
                    for t in range(1440):
                        if t%256==0:check_budget(start,seconds)
                        st['first_constraints_tested']+=1
                        if checks is not None and any(vals[(t+i)%1440]%n not in allowed for i,allowed,n in checks):continue
                        m=model(role,rev,t,p,name,eq);st['full_decryptions']+=1
                        try:plain=crypt(cipher,m,True)
                        except ValueError:continue
                        if len(plain)!=97 or plain[21:34]!=WINDOWS[0][1]:continue
                        passed=plain[63:74]==WINDOWS[1][1]
                        assert crypt(plain,m)==cipher
                        st['first_survivors']+=1;st['all_survivors']+=int(passed)
                        records.append(dict(model=m,plaintext=plain,plaintext_sha256=hashlib.sha256(plain.encode()).hexdigest(),predicted_berlin=plain[63:74],all_pass=passed,full_reencryption=True))
        assert st['support_or_length_pruned']+st['first_constraints_tested']==raw
        stats[role]=st
    return dict(models=records,accounting=stats,first_survivors=len(records),all_survivors=sum(r['all_pass'] for r in records),distinct_all_plaintexts=len({r['plaintext'] for r in records if r['all_pass']}))


def plant():
    p=list(literal_plant());p[:3]='XYZ';p[40]='X';p[50]='Y'
    return ''.join(p)


def controls():
    start=time.monotonic();state_checks=0
    for rev,p,t in itertools.product((False,True),(0,1),range(1440)):
        assert ordinal(t,p,rev)==VALUES[int(rev)][p][t]
        assert lamp_inverse(lamp_bits(t,p))==(t,p);state_checks+=1
    strings=0
    for n in range(4):
        for xs in itertools.product(LATIN,repeat=n):
            text=''.join(xs);assert unframe(frame(text))==text;strings+=1
    for n,width in ((676,3),(26,2)):
        for r in range(n):assert undigits(digits(r,width),n)==r
    errors=0
    for text in (GREEK[-1],GREEK[-1]+GREEK[3],GREEK[-1]*2):
        try:unframe(text)
        except ValueError:errors+=1
        else:raise AssertionError('invalid framing accepted')
    for text,limit in ((digits(676,3),676),(digits(26,2),26)):
        try:undigits(text,limit)
        except ValueError:errors+=1
        else:raise AssertionError('invalid numeric rank accepted')
    # Independently evaluate bits on every raw model, unrelated mixed-length text.
    raw_roundtrips=0
    for m in parameters():
        cipher=crypt('XYZABCDE',m);assert crypt(cipher,m,True)=='XYZABCDE';assert crypt('XYZABCDE',m,oracle=True)==cipher
        raw_roundtrips+=1
        if raw_roundtrips%256==0:check_budget(start,120)
    plants=[];plain=plant();timing_detected=0;mutations=0
    for fi,role in enumerate(ROLES):
        for ri,rev in enumerate((False,True)):
            for si,t in enumerate(STARTS):
                m=model(role,rev,t,(fi+si)%2,tuple(ALPHABETS)[(fi+ri+si)%2],('plus','beaufort')[(si//2+ri)%2])
                cipher=crypt(plain,m);assert crypt(cipher,m,True)==plain
                selected=select(cipher,start,120);all_models=[r for r in selected['models'] if r['all_pass']]
                assert any(r['model']==m and r['plaintext']==plain for r in all_models)
                shifted=dict(m,start_minute=(t+1)%1440)
                timing_detected+=int(crypt(plain,shifted)!=cipher)
                # A different symbol at the token corresponding to English position 22.
                index=21 if role!='G' else len(frame(plain[:21]))
                alphabet=ALPHABETS[m['alphabet']][:24] if role=='G' else ALPHABETS[m['alphabet']]
                mutated=cipher[:index]+alphabet[(alphabet.index(cipher[index])+1)%len(alphabet)]+cipher[index+1:]
                try:mp=crypt(mutated,m,True)
                except ValueError:mp=''
                assert mp!=plain;mutations+=1
                plants.append(dict(planted_model=m,ciphertext_length=len(cipher),greek_window_starts_zero_based=[len(frame(plain[:s])) for s,_ in WINDOWS] if role=='G' else None,truth_retained=True,compatible_models=all_models,distinct_plaintexts=len({r['plaintext'] for r in all_models})))
    return dict(status='passed',state_checks=state_checks,escape_strings_checked=strings,rank_checks=702,invalid_codes_rejected=errors,raw_roundtrips=raw_roundtrips,literal_plants=plants,timing_mutations_detected=timing_detected,known_symbol_mutations_detected=mutations,elapsed_seconds=time.monotonic()-start)


def representation_audit():
    from conditional_face_lamp import lamp_streams
    old={tuple(r['key']) for r in lamp_streams()};new={};pair={}
    for rev,t,p in itertools.product((False,True),range(1440),(0,1)):
        vals=VALUES[int(rev)][p];key=tuple(vals[(t+i)%1440]%26 for i in range(97))
        new[key]=new.get(key,0)+1
        keyb=tuple(vals[(t+i)%1440]%676 for i in range(49));pair[keyb]=pair.get(keyb,0)+1
    collisions={}
    for i,c in enumerate(LATIN):collisions.setdefault(i%24,[]).append(c)
    return dict(greek_order=GREEK,naive_mod24_collisions=[xs for xs in collisions.values() if len(xs)>1],letter_distinct_key_streams=len(new),letter_raw_clock_descriptions=5760,letter_streams_equal_old_binary_streams=len(set(new)&old),letter_descriptions_equal_old_binary_streams=sum(n for k,n in new.items() if k in old),pair_distinct_key_streams=len(pair),ordinal_ranges=[dict(order=('row_major','reverse')[r],minimum=min(min(v) for v in VALUES[r]),maximum=max(max(v) for v in VALUES[r])) for r in range(2)])
