import json, re
from pathlib import Path
ROOT=Path('/workspace/shared/candidate-first-051/authors')
LOG=ROOT/'thematic_draft_log.jsonl'
def letters(s): return re.sub('[^A-Z]', '', s.upper())
def record(cid, theme, parts):
    a,b,c=parts
    prose=a+' EAST NORTH EAST '+b+' BERLIN CLOCK '+c
    norm=letters(prose)
    report={'span_lengths':[len(letters(x)) for x in parts], 'total_letters':len(norm), 'east_positions': [m.start()+1 for m in re.finditer('EASTNORTHEAST',norm)],'berlin_positions':[m.start()+1 for m in re.finditer('BERLINCLOCK',norm)]}
    good=report['span_lengths']==[21,29,23] and len(norm)==97 and norm[21:34]=='EASTNORTHEAST' and norm[63:74]=='BERLINCLOCK'
    report['valid']=good
    entry={'id':cid,'theme':theme,'spaced_prose':prose,'normalized':norm,'parts':parts,'feedback':report}
    with LOG.open('a') as f: f.write(json.dumps(entry)+'\n')
    print(cid, report, repr(prose))
    return entry
if __name__=='__main__':
    record('T01','Egypt memories',('From this temple walk due', 'and remember the first sight of the', 'as we did in our younger days.'))
