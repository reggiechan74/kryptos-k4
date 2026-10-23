"""Audit tracked Markdown file targets; report fragments separately from file presence.
Only explicit Markdown inline links are checked. Remote links, generated caches,
code examples and dynamic web content are not fetched or treated as verified.
"""
import json,re,subprocess
from pathlib import Path
from collections import Counter
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
def audit():
 files=subprocess.check_output(['git','ls-files'],cwd=ROOT).decode().splitlines();broken=[];checked=0;fragment_failures=[];fragments_checked=0
 for name in files:
  if not name.endswith('.md'):continue
  source=ROOT/name;text=source.read_text(errors='replace');text=re.sub(r'```.*?```','',text,flags=re.S)
  for m in re.finditer(r'!?\[[^\]\n]*\]\((<[^>]+>|[^)\n]+)\)',text):
   target=m.group(1).strip().strip('<>')
   if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):continue
   parts=target.split('#',1);fragment=unquote(parts[1]) if len(parts)>1 else None
   target=unquote(parts[0].split('?')[0]);resolved=(source.parent/target).resolve();checked+=1
   if fragment and resolved.is_file() and resolved.suffix=='.md':
    fragments_checked+=1;seen=Counter();valid=set()
    for heading in re.findall(r'^#+ (.*)',resolved.read_text(errors='replace'),re.M):
     slug=re.sub(r'[^\w -]','',heading.lower()).replace(' ','-');n=seen[slug];valid.add(slug+('-'+str(n) if n else ''));seen[slug]+=1
    if fragment not in valid:fragment_failures.append(dict(source=name,target=m.group(1)))
   if not resolved.exists():broken.append(dict(source=name,target=m.group(1),line=text[:m.start()].count('\n')+1))
 return dict(kind='Tracked Markdown local file and Markdown heading-fragment audit; no remote retrieval',checked=checked,broken=broken,markdown_fragments_checked=fragments_checked,broken_markdown_fragments=fragment_failures,scope='Fenced code blocks excluded; original independent artifacts are preserved even where their standalone-relative links are unavailable in this checkout.')
if __name__=='__main__':print(json.dumps(audit(),indent=2))
