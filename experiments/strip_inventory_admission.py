"""Conservative transcription gate, not historical authentication by itself."""
import hashlib,json
from strip_source_gates import AZ,validate_strips

def cycle_from_literal(raw):
 if not isinstance(raw,str) or any(c not in AZ+' \t\r\n' for c in raw):raise ValueError('unknown characters; do not silently remove OCR uncertainty')
 letters=''.join(raw.split())
 if len(letters)==52:
  if letters[:26]!=letters[26:]:raise ValueError('two printed cycles disagree; no repair')
  letters=letters[:26]
 elif len(letters)!=26:raise ValueError('one 26-letter cycle or two identical printed cycles required')
 validate_strips([letters]);return letters

def inspect_inventory(rows,variant,source_url):
 if not variant or not source_url:raise ValueError('version and source are required')
 ids=[r['id'] for r in rows]
 if len(ids)!=len(set(ids)):raise ValueError('duplicate strip IDs')
 cycles=[cycle_from_literal(r['literal']) for r in rows]
 return dict(variant=variant,source_url=source_url,strip_ids=ids,cycles=cycles,valid_permutations=True,source_authentication='Not established by mathematical validity; requires source review and external vector.',literal_sha256=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest())
