#!/usr/bin/env python3
"""Reproduce a source-separated Kryptos construction audit, standard library only.

Downloads are read-only public requests, saved to an ignored local cache. Third-party
art text and source pages are NOT included in the integration archive. The program
never edits a repository ciphertext or imports/executes code from source pages.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import urllib.request

SOURCES = {
    'cp': 'https://scirealm.org/CyrillicProjector.html',
    'cp_elonka': 'https://elonka.com/kryptos/cyrillic.html',
    'corr': 'https://www.elonka.com/kryptos/mirrors/CPSolution.html',
    'kryptos_transcript': 'https://elonka.com/kryptos/transcript.html',
    'k2_correction': 'https://elonka.com/kryptos/CorrectedK2Announcement.html',
}
K4_REFERENCE_SHA256 = 'eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab'
KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
CP_PLAIN = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
CP_CIPHER = 'ТЕНЬАБВГДЖЗИЙКЛМОПРСУФХШЦЧЩЪЫЭЮЯ'
CP_KEY = 'МЕДУЗА'

def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode('utf-8')).hexdigest()

def strip_tags(s):
    return unescape(re.sub(r'<[^>]*>', '', s))

def az(s):
    return ''.join(re.findall('[A-Z]', s.upper()))

def cyr(s):
    return ''.join(re.findall('[А-Я]', s))

def poly(text, plain_alphabet, cipher_alphabet, key, key_alphabet, decrypt=False, restart=None):
    """Explicit index equation. A restart is a key-index change, not a text edit."""
    assert len(plain_alphabet)==len(cipher_alphabet)==len(set(cipher_alphabet))==len(set(plain_alphabet))
    assert key and set(key)<=set(key_alphabet)
    n=len(plain_alphabet)
    out=[]
    for i,x in enumerate(text):
        j=i if restart is None or i<restart else i-restart
        k=key_alphabet.index(key[j%len(key)])
        if decrypt:
            out.append(plain_alphabet[(cipher_alphabet.index(x)-k)%n])
        else:
            out.append(cipher_alphabet[(plain_alphabet.index(x)+k)%n])
    return ''.join(out)

class Tables(HTMLParser):
    """Capture cells with table-local state; do not execute JavaScript."""
    def __init__(self):
        super().__init__(); self.tables=[]; self.stack=[]
    def handle_starttag(self, tag, attrs):
        if tag=='table': self.stack.append({'rows':[], 'row':None, 'cell':None})
        if not self.stack: return
        state=self.stack[-1]
        if tag=='tr': state['row']=[]
        if tag in ('td','th'): state['cell']=[]
        if tag=='br' and state['cell'] is not None: state['cell'].append('\n')
    def handle_data(self, data):
        if self.stack and self.stack[-1]['cell'] is not None:
            self.stack[-1]['cell'].append(data)
    def handle_endtag(self, tag):
        if not self.stack: return
        state=self.stack[-1]
        if tag in ('td','th') and state['row'] is not None and state['cell'] is not None:
            state['row'].append(''.join(state['cell'])); state['cell']=None
        if tag=='tr' and state['row'] is not None:
            state['rows'].append(state['row']); state['row']=None
        if tag=='table': self.tables.append(self.stack.pop()['rows'])

def load_sources(cache, offline):
    cache.mkdir(parents=True, exist_ok=True)
    pages={}; receipts={}
    for name,url in SOURCES.items():
        path=cache/(name+'.html')
        if not path.exists():
            if offline: raise RuntimeError(f'Missing cached public source: {path}')
            request=urllib.request.Request(url,headers={'User-Agent':'KryptosConstructionAudit/1.0 (public-source reproducibility)','Accept':'text/html'})
            with urllib.request.urlopen(request,timeout=45) as response:
                data=response.read()
            path.write_bytes(data)
        data=path.read_bytes()
        pages[name]=data.decode('utf-8',errors='replace')
        receipts[name]={'url':url,'bytes':len(data),'sha256_bytes':sha(data)}
    return pages,receipts

def run(pages, receipts):
    checks={}
    # Ciphertext and published plaintext are independently extracted, not produced by
    # decrypting first and then declaring that generated output to be ground truth.
    parser=Tables(); parser.feed(pages['cp'])
    candidates=[t for t in parser.tables if len(t)==4 and any('Encoded' in x for row in t for x in row)]
    assert len(candidates)==1, 'Source layout changed: paired CP table is ambiguous.'
    table=candidates[0]
    # Reject unexpected letters instead of letting a regex silently discard them.
    # The ciphertext table has an asterisk annotation and both columns show MEDUSA.
    for panel in (2,3):
        for column in (0,1):
            material=table[panel][column].replace('MEDUSA','')
            if column==0: material=material.replace('*','')
            assert set(''.join(material.split()))<=set(CP_PLAIN), 'Unexpected CP table symbol.'
    cp_c=cyr(table[2][0]+table[3][0]); cp_p=cyr(table[2][1]+table[3][1])
    assert len(cp_c)==len(cp_p)==1133
    physical_rows=[]
    for panel in (2,3):
        for line in table[panel][0].splitlines():
            row=''.join(re.findall('[А-ЯA-Z]',line))
            if row: physical_rows.append(row)
    assert len(physical_rows)==32
    assert ''.join(physical_rows).count('MEDUSA')==1
    cp_other=[]
    homoglyph_map=str.maketrans('ABCEHKMOPTX','АВСЕНКМОРТХ')
    for cell in re.findall(r'<td\b[^>]*>(.*?)</td>',pages['cp_elonka'],re.I|re.S):
        s=''.join(strip_tags(cell).split())
        if s.startswith('ЛTФEЮ') or s.startswith('ЙAЧЛЬ'):
            s=s.replace('MEDUSA','').translate(homoglyph_map)
            assert set(s)<=set(CP_PLAIN), 'Unexpected character: do not silently normalize.'
            cp_other.append(s)
    assert ''.join(cp_other)==cp_c, 'Published CP ciphertext transcripts differ.'
    continuous=poly(cp_c,CP_PLAIN,CP_CIPHER,CP_KEY,CP_PLAIN,decrypt=True)
    restarted=poly(cp_c,CP_PLAIN,CP_CIPHER,CP_KEY,CP_PLAIN,decrypt=True,restart=777)
    assert restarted==cp_p
    assert poly(cp_p,CP_PLAIN,CP_CIPHER,CP_KEY,CP_PLAIN,restart=777)==cp_c
    # Per-symbol phase is uniquely identified here because all six key symbols differ.
    required=[(CP_CIPHER.index(c)-CP_PLAIN.index(p))%32 for c,p in zip(cp_c,cp_p)]
    key_values=[CP_PLAIN.index(k) for k in CP_KEY]
    relative_phases=[(key_values.index(k)-i)%6 for i,k in enumerate(required)]
    runs=[]
    for i,phase in enumerate(relative_phases):
        if not runs or runs[-1]['phase_delta_mod_6']!=phase:
            runs.append({'start_1_based':i+1,'end_1_based':i+1,'phase_delta_mod_6':phase})
        else: runs[-1]['end_1_based']=i+1
    assert runs==[{'start_1_based':1,'end_1_based':777,'phase_delta_mod_6':0},{'start_1_based':778,'end_1_based':1133,'phase_delta_mod_6':3}]
    boundary_coordinates={}; count=0
    for rownum,row in enumerate(physical_rows,1):
        for col,ch in enumerate(row,1):
            if ch in CP_PLAIN:
                count+=1
                if count in (777,778): boundary_coordinates[str(count)]={'row_1_based':rownum,'column_1_based_including_MEDUSA':col}
    ordinary_keyed=''.join(dict.fromkeys('ТЕНЬ'+CP_PLAIN))
    ordinary_dec=poly(cp_c,CP_PLAIN,ordinary_keyed,CP_KEY,CP_PLAIN,decrypt=True,restart=777)
    kstyle_dec=poly(cp_c,CP_CIPHER,CP_CIPHER,CP_KEY,CP_CIPHER,decrypt=True,restart=777)
    phase_controls={}
    for delta in range(6):
        decoded=''.join(CP_PLAIN[(CP_CIPHER.index(x)-key_values[(i+(delta if i>=777 else 0))%6])%32] for i,x in enumerate(cp_c))
        phase_controls[str(delta)]=sum(a==b for a,b in zip(decoded,cp_p))
    checks['cyrillic_projector']={
        'n_cipher_symbols_excluding_MEDUSA':len(cp_c),'n_published_plain_symbols':len(cp_p),
        'two_published_transcripts_match':True,
        'cipher_sha256_utf8':sha(cp_c),'published_plain_sha256_utf8':sha(cp_p),
        'continuous_key_matches':sum(a==b for a,b in zip(continuous,cp_p)),
        'restart_at_778_matches':sum(a==b for a,b in zip(restarted,cp_p)),
        'restart_reencryption_hamming_distance':0,'relative_phase_runs':runs,
        'phase_delta_controls_matches_out_of_1133':phase_controls,
        'normal_keyed_alphabet_control_matches':sum(a==b for a,b in zip(ordinary_dec,cp_p)),
        'kryptos_style_keyed_plain_and_key_control_matches':sum(a==b for a,b in zip(kstyle_dec,cp_p)),
        'physical_row_lengths_including_MEDUSA':list(map(len,physical_rows)),
        'panel_boundary_after_symbol':len(cyr(table[2][0])),
        'semantic_boundary_coordinates':boundary_coordinates,
        'boundary_plain_excerpt_1_based_761_through_800':cp_p[760:800],
        'literal_MEDUSA_insertion_after_cyrillic_symbol':480,
        'identifiability':'A key restart at the second-message boundary and a +3 mod 6 phase jump are identical on all retained symbols. Literal omitted text is not identified; insertion lengths 3+6m have the same downstream phase. Skipping MEDUSA or advancing six key positions is also indistinguishable.'
    }
    pre=[strip_tags(s).strip() for s in re.findall(r'<pre[^>]*>(.*?)</pre>',pages['kryptos_transcript'],re.I|re.S)]
    upper=pre[0].splitlines(); lower=pre[2].splitlines()
    k1=''.join(upper[:2]); k2raw=''.join(upper[2:]); k2=az(k2raw)
    quotes=[strip_tags(s) for s in re.findall(r'<blockquote[^>]*>(.*?)</blockquote>',pages['k2_correction'],re.I|re.S)]
    expected_k1=az(quotes[0]); expected_k2=az(quotes[-1])
    assert len(k1)==63 and len(k2)==369 and len(expected_k2)==370
    assert poly(k1,KA,KA,'PALIMPSEST',KA,decrypt=True)==expected_k1
    original_key=''.join('PALIMPSEST'[i%10] for i in range(63))
    worksheet_key=original_key[:56]+'C'+original_key[57:]
    worksheet_plain=expected_k1[:56]+'L'+expected_k1[57:]
    worksheet_prediction=''.join(KA[(KA.index(p)+KA.index(k))%26] for p,k in zip(worksheet_plain,worksheet_key))
    assert worksheet_prediction==k1
    assert poly('L',KA,KA,'C',KA)=='K'
    assert poly('Q',KA,KA,'S',KA)=='K'
    assert poly('L',KA,KA,'S',KA)=='W'
    corrected_k2=poly(expected_k2,KA,KA,'ABSCISSA',KA)
    deletion_solutions=[i for i in range(len(corrected_k2)) if corrected_k2[:i]+corrected_k2[i+1:]==k2]
    assert deletion_solutions==[361]
    assert corrected_k2[361]=='S'
    k2_as_inscribed_plain=poly(k2,KA,KA,'ABSCISSA',KA,decrypt=True)
    # The worksheet O / S / E cell and carved U / S / R cell are algebraic facts;
    # where, when, or why the physical difference arose is not inferred by this test.
    assert expected_k2[114]=='U' and k2[114]=='R'
    assert poly('O',KA,KA,'S',KA)=='E' and poly('U',KA,KA,'S',KA)=='R'
    checks['kryptos_k1_k2']={
        'k1_symbols':len(k1),'k1_published_plain_matches':True,
        'k1_single_local_key_exception_reconstructs_inscribed_63_symbols':True,
        'k1_anomaly_position_1_based':57,
        'k1_local_equivalence':{'plain_L_key_C':'K','plain_Q_key_S':'K','plain_L_key_S':'W'},
        'k2_inscribed_letters':len(k2),'k2_question_marks_ignored_for_key_advance':k2raw.count('?'),
        'k2_corrected_letters':len(expected_k2),'unique_deleted_intended_cipher_position_1_based':362,
        'deleted_cipher_symbol':'S','insert_after_observed_letters':361,
        'k2_old_tail':k2_as_inscribed_plain[-12:],'k2_corrected_tail':expected_k2[-13:],
        'k2_worksheet_difference_position_1_based_letters':115,
        'k2_local_equivalence':{'plain_O_key_S':'E','plain_U_key_S':'R'},
        'k2_correction_reencryption_then_deletion_hamming_distance':0,
    }
    k4=lower[-4].split('?')[-1]+''.join(lower[-3:])
    assert len(k4)==97 and sha(k4)==K4_REFERENCE_SHA256, 'Canonical source differs: inspect; never silently replace.'
    checks['k4_reference_only']={'length':97,'sha256_utf8':sha(k4),'physical_row_lengths':[4,31,31,31],'mutations_applied':0,'candidate_plaintexts_generated':0}
    return {'audit_version':'1.0','run_at_utc':datetime.now(timezone.utc).isoformat(),'source_receipts':receipts,'checks':checks,'scope':'Historical convention regression test, not a K4 solution or evidence that K4 is erroneous.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cache-dir',type=Path,default=Path('.audit_cache'))
    ap.add_argument('--offline',action='store_true',help='Only use already downloaded public-source pages.')
    ap.add_argument('--output',type=Path,default=Path('construction_audit_results.json'))
    args=ap.parse_args()
    pages,receipts=load_sources(args.cache_dir,args.offline)
    result=run(pages,receipts)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS: CP 1133/1133 with a message-boundary key restart; continuous key 777/1133.')
    print('PASS: K1 local worksheet equivalence; K2 historical deletion; K4 unchanged.')
    print('Wrote derived results to',args.output)
if __name__=='__main__': main()
