"""Read-only source inventory and deterministic role assignment; performs no scoring."""
from pathlib import Path
import hashlib,json
from collections import Counter
ROOT=Path(__file__).resolve().parent
TRAIN={'austen-emma.txt','austen-persuasion.txt','austen-sense.txt','chesterton-ball.txt','chesterton-brown.txt','chesterton-thursday.txt','edgeworth-parents.txt','melville-moby_dick.txt'}
CAL={'bryant-stories.txt','burgess-busterbrown.txt','carroll-alice.txt'}
AUTHOR={'austen':'Jane Austen','chesterton':'G K Chesterton','edgeworth':'Maria Edgeworth','melville':'Herman Melville','bryant':'Sarah Cone Bryant','burgess':'Thornton W Burgess','carroll':'Lewis Carroll','bible':'King James Bible translation tradition','blake':'William Blake','milton':'John Milton','shakespeare':'William Shakespeare','whitman':'Walt Whitman'}
TOPICS=[('ordinary','buying groceries'),('ordinary','cleaning a kitchen'),('ordinary','waiting for a bus'),('ordinary','tending indoor plants'),('procedural','routine equipment maintenance'),('procedural','recording a simple laboratory measurement'),('procedural','cataloguing library materials'),('procedural','checking a household appliance'),('correspondence','a personal thank-you letter'),('correspondence','arranging an appointment'),('correspondence','an office handover note'),('correspondence','a trip-planning email')]

def normalized(raw):
    first,sep,rest=raw.partition(b'\n');removed=0
    if first.strip().startswith(b'[') and first.strip().endswith(b']'):
        removed=len(first)+len(sep);raw=rest
    text=bytes(b-32 if 97<=b<=122 else b for b in raw if 65<=b<=90 or 97<=b<=122)
    return text,removed

def main():
    docs=[]
    for corpus in ['gutenberg','inaugural']:
        for path in sorted((ROOT/'data/documents'/corpus).glob('*.txt')):
            raw=path.read_bytes();norm,removed=normalized(raw)
            if corpus=='gutenberg':
                role='training' if path.name in TRAIN else 'calibration' if path.name in CAL else 'hard_style_control'
                attribution=AUTHOR[path.stem.split('-')[0]];kind='attributed_book_author'
            else:
                attribution=path.stem.split('-',1)[1];kind='speaker_not_verified_writer'
                role='calibration' if 'A'<=attribution[0].upper()<='M' else 'published_prose_control'
            docs.append({'document_id':str(path.relative_to(ROOT/'data/documents')),'raw_path':str(path.relative_to(ROOT)),
                         'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw),'normalized_sha256':hashlib.sha256(norm).hexdigest(),
                         'normalized_letters':len(norm),'removed_first_line_bytes':removed,'role':role,
                         'attribution_group':attribution,'attribution_kind':kind,'training_letters_used':min(200000,len(norm)) if role=='training' else 0})
    plan={'source_snapshot':json.loads((ROOT/'data/SOURCE_RECEIPTS.json').read_text())['nltk_data_commit'],
          'selection_basis':'Existing general-English NLTK collections; fixed role rules before language scores; no selection from Kryptos results.',
          'documents':docs,'novel_key_documents_required':12,
          'novel_topics':[{'id':f'K{i+1:03}','style':style,'topic':topic} for i,(style,topic) in enumerate(TOPICS)],
          'novel_author_constraints':'Each200-600ASCIIletters, complete natural prose, no ciphertext/bank/scorer access, no fixedcribs or97lettertarget, retain original wording and revisions.',
          'split_caveat':'Books use disjoint attributed authors; inaugural partitions are speaker-disjoint, not necessarily writer/ghostwriter-disjoint. Exact duplicate checks establish only their measured overlap exclusion.',
          'model_training_or_language_scoring_performed':False}
    (ROOT/'CONTROL_SOURCE_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
    print(json.dumps({'documents':len(docs),'roles':dict(Counter(x['role'] for x in docs)),'training_letters':sum(x['training_letters_used'] for x in docs)},indent=2))

if __name__=='__main__':main()
