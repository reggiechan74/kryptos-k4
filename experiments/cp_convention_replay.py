"""Two fixed convention replays of a public related-art pair; no K4 input."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import platform
import subprocess
import time
from run_io import RunSnapshot, specification, json_bytes

ROOT=Path(__file__).resolve().parents[1]
SPEC='research/specifications/CP-CONVENTION-REPLAY-001.json'
N='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
C='ТЕНЬАБВГДЖЗИЙКЛМОПРСУФХШЦЧЩЪЫЭЮЯ'
KEY='МЕДУЗА'


class Source(HTMLParser):
    def __init__(self):
        super().__init__();self.text=[];self.hidden={}
    def handle_data(self,data):self.text.append(data)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='input' and attrs.get('type')=='hidden':
            self.hidden[attrs['name']]=attrs.get('value','')


def normalize(text):return ''.join(c for c in text if c in N)


def extract(raw):
    parser=Source();parser.feed(raw.decode('latin1'))
    text=''.join(parser.text)
    one=text.index('Section 1 (Sinister Methods of Secret Agents)')
    one=text.index('ВЫСОЧАЙЪИМ',one)
    end=text.index('These are the corrected words',one)
    p1=normalize(text[one:end])
    two=text.index('Section 2a (1982')
    two=text.index('ОБ',text.index('apparently typo errors.',two))
    end=text.index('These are the corrected words',two)
    p2=normalize(text[two:end])
    c1=normalize(parser.hidden['CPpart1']);c2=normalize(parser.hidden['CPpart2'])
    if (len(c1),len(p1),len(c2),len(p2)) != (777,777,356,356):
        raise ValueError('Source normalization/section lengths differ; do not repair')
    return c1+c2,p1+p2


def crypt(text,restart=False,inverse=False):
    out=[]
    for i,symbol in enumerate(text):
        position=i-777 if restart and i>=777 else i
        shift=N.index(KEY[position%6])
        out.append(N[(C.index(symbol)-shift)%32] if inverse else C[(N.index(symbol)+shift)%32])
    return ''.join(out)


def oracle_inverse(cipher,restart):
    out=[]
    for i,c in enumerate(cipher):
        phase=((i-777) if restart and i>=777 else i)%6
        table={p:C[(N.index(p)+N.index(KEY[phase]))%32] for p in N}
        out.append(next(p for p,value in table.items() if value==c))
    return ''.join(out)


def evaluate(cipher,plain):
    records=[]
    for reset in (False,True):
        encoded=crypt(plain,restart=reset)
        inverse=crypt(cipher,restart=reset,inverse=True)
        assert inverse==oracle_inverse(cipher,reset)
        mismatches=[i+1 for i,(a,b) in enumerate(zip(encoded,cipher)) if a!=b]
        assert crypt(inverse,restart=reset)==cipher
        records.append(dict(restart=reset,exact=not mismatches,
                            first_segment_matches=sum(a==b for a,b in zip(encoded[:777],cipher[:777])),
                            second_segment_matches=sum(a==b for a,b in zip(encoded[777:],cipher[777:])),
                            mismatches_one_based=mismatches,
                            inverse_matches=sum(a==b for a,b in zip(inverse,plain))))
    # Both descriptions of the phase discontinuity are algebraically equal.
    assert all((i-777)%6==(i+3)%6 for i in range(777,1133))
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html',required=True)
    parser.add_argument('--spec-commit',required=True)
    args=parser.parse_args()
    spec=specification(args.spec_commit,SPEC)
    code=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    subprocess.run(['git','merge-base','--is-ancestor',args.spec_commit,code],check=True)
    files=[SPEC,'experiments/cp_convention_replay.py','tests/test_cp_convention_replay.py','experiments/run_io.py']
    hashes={}
    for name in files:
        b=(ROOT/name).read_bytes()
        if b!=subprocess.check_output(['git','show',code+':'+name]):raise ValueError('uncommitted code/spec')
        hashes[name]=hashlib.sha256(b).hexdigest()
    assert (ROOT/SPEC).read_bytes()==subprocess.check_output(['git','show',args.spec_commit+':'+SPEC])
    raw=Path(args.html).read_bytes()
    expected=json.loads((ROOT/SPEC).read_text())
    assert len(raw)==expected['source_bytes'] and hashlib.sha256(raw).hexdigest()==expected['source_sha256']
    with RunSnapshot('results/cp-convention-runs','CP-CONVENTION-REPLAY-001',spec) as snapshot:
        start=time.monotonic()
        snapshot.manifest['jobs'].append(dict(experiment='CP-CONVENTION-REPLAY-001',status='running'))
        cipher,plain=extract(raw)
        records=evaluate(cipher,plain)
        result=dict(id='CP-CONVENTION-REPLAY-001',status='completed',spec_commit=args.spec_commit,
                    code_commit=code,python=platform.python_version(),platform=platform.platform(),
                    command='python3 experiments/cp_convention_replay.py --html <public HTML matching source hash> --spec-commit '+args.spec_commit,
                    source_url=expected['source_url'],source_sha256=expected['source_sha256'],
                    file_sha256=hashes,ciphertext_sha256=hashlib.sha256(cipher.encode()).hexdigest(),
                    plaintext_sha256=hashlib.sha256(plain.encode()).hexdigest(),
                    symbols=1133,first_segment=777,second_segment=356,
                    second_plaintext_prefix=plain[777:791],literal_MEDUSA_excluded=True,
                    observed=records,
                    conclusion='Convention matches public pair only; reset equals+3phase jump, cannot identify physical omission. No K4 reset test.',
                    elapsed_seconds=time.monotonic()-start)
        snapshot.write('CP-CONVENTION-REPLAY-001.json',json_bytes(result))
        snapshot.manifest['jobs'][-1]['status']='completed'
        def deadline():
            if time.monotonic()-start>10:raise TimeoutError('10second replay budget')
        snapshot.final_check=deadline
    print(json.dumps(dict(run_id=snapshot.run_id,observed=records,elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__=='__main__':main()
