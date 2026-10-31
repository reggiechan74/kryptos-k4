"""Validate public audit invariants without inferring any missing letters."""
import hashlib,json,csv
from pathlib import Path
p=Path(__file__).resolve().parent
read=lambda n:json.loads((p/n).read_text())
a,b=read('examiner-a.json'),read('examiner-b.json');audit=read('cellwise-audit.json')
coords={(r,c) for r in range(1,28) for c in range(1,31)}
for seq in [a,b,audit]:
 assert len(seq)==810 and {(x['row'],x['column']) for x in seq}==coords
for n,h in read('comparison-start.json')['files'].items():assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h
ka='KRYPTOSABCDEFGHIJLMNQUVWXZ';az='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for x,y,z in zip(a,b,audit):
 assert z['examiner_a']==x and z['examiner_b']==y
 r,c=z['row'],z['column'];assert z['expected']==(ka[(r+c-2)%26] if r<=26 else az[(c-1)%26])
assert sum(x['literal_reading']==y['literal_reading'] and x['literal_reading'] is not None for x,y in zip(a,b))==806
assert sum(x['literal_reading'] is None and y['literal_reading'] is None for x,y in zip(a,b))==1
assert sum(x['literal_reading']!=y['literal_reading'] for x,y in zip(a,b))==3
assert sum(z['comparison_status']=='matches_expected' for z in audit)==774
assert sum(z['comparison_status']=='tentative_match' for z in audit)==32
assert {(z['row'],z['column']) for z in audit if z['reconciled_literal'] is None}=={(17,21),(18,20),(27,2),(27,4)}
for n in ['examiner-a.csv','examiner-b.csv','cellwise-audit.csv']:
 with (p/n).open() as f:assert len(list(csv.DictReader(f)))==810
for f in p.iterdir():
 if f.is_file() and f.name!='SHA256SUMS':assert ('/'+'workspace'+'/') not in f.read_text() and ('/'+'tmp'+'/') not in f.read_text()
print('PASS: 810 unique coordinates each; frozen hashes; expected formulas; counts; preserved originals; unresolved cells; CSV counts; public path hygiene.')
