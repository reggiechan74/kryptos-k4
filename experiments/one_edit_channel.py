"""5071 raw counterfactual channels; canonical input is never changed."""
from collections import Counter
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
WINDOWS=((21,'EASTNORTHEAST'),(63,'BERLINCLOCK'))
ALIGNMENTS=('ENGLISH_FIXED','OBSERVED_CELL_TRANSPORT')


def edits(observed,alphabet=AZ):
 yield dict(kind='baseline',position=None,latent_char=None,observed_char=None)
 for i,c in enumerate(observed):
  for b in alphabet:
   if b!=c:yield dict(kind='substitute',position=i,latent_char=b,observed_char=c)
 for g in range(len(observed)+1):
  for b in alphabet:yield dict(kind='insert_latent',position=g,latent_char=b,observed_char=None)
 for i,c in enumerate(observed):yield dict(kind='delete_observed',position=i,latent_char=None,observed_char=c)


def repair(observed,e):
 k=e['kind'];p=e['position']
 if k=='baseline':return observed
 if k=='substitute':return observed[:p]+e['latent_char']+observed[p+1:]
 if k=='insert_latent':return observed[:p]+e['latent_char']+observed[p:]
 if k=='delete_observed':return observed[:p]+observed[p+1:]
 raise ValueError('unknown channel')


def forward(latent,e):
 k=e['kind'];p=e['position']
 if k=='baseline':return latent
 if k=='substitute':return latent[:p]+e['observed_char']+latent[p+1:]
 if k=='insert_latent':return latent[:p]+latent[p+1:]
 if k=='delete_observed':return latent[:p]+e['observed_char']+latent[p:]
 raise ValueError('unknown channel')


def index_maps(n,e):
 k=e['kind'];p=e['position']
 if k in ('baseline','substitute'):return tuple(range(n)),tuple(range(n))
 if k=='insert_latent':return tuple(i+(i>=p) for i in range(n)),tuple(None if j==p else j-(j>p) for j in range(n+1))
 if k=='delete_observed':return tuple(None if i==p else i-(i>p) for i in range(n)),tuple(j+(j>=p) for j in range(n-1))
 raise ValueError('unknown channel')


def anchors(n,e,alignment,windows=WINDOWS):
 if alignment=='ENGLISH_FIXED':return tuple(s for s,_ in windows),None
 if alignment!='OBSERVED_CELL_TRANSPORT':raise ValueError('unknown anchor interpretation')
 mapping,_=index_maps(n,e);starts=[]
 for s,word in windows:
  positions=[mapping[i] for i in range(s,s+len(word))]
  if None in positions:return None,'deleted_known_observed_cell'
  if positions!=list(range(positions[0],positions[0]+len(word))):return None,'split_known_phrase'
  starts.append(positions[0])
 return tuple(starts),None


def mask(starts,windows=WINDOWS):return {s+j:p for s,(_,word) in zip(starts,windows) for j,p in enumerate(word)}


def catalog(observed):
 descriptions=[];maps={};strings=[];string_ids={};instances=[];instance_ids={};invalid=[]
 for edit_id,e in enumerate(edits(observed)):
  latent=repair(observed,e);assert forward(latent,e)==observed
  if latent not in string_ids:string_ids[latent]=len(strings);strings.append(latent)
  map_key=(e['kind'] if e['kind'] not in ('baseline','substitute') else 'identity',e['position'] if e['kind'] not in ('baseline','substitute') else None)
  if map_key not in maps:
   o,l=index_maps(len(observed),e);maps[map_key]=dict(map_id=len(maps),observed_to_latent=list(o),latent_to_observed=list(l))
  row=dict(edit_id=edit_id,**e,latent_id=string_ids[latent],map_id=maps[map_key]['map_id']);descriptions.append(row)
  for alignment in ALIGNMENTS:
   starts,reason=anchors(len(observed),e,alignment)
   if reason:invalid.append(dict(edit_id=edit_id,alignment=alignment,reason=reason));continue
   key=(latent,starts)
   if key not in instance_ids:
    instance_ids[key]=len(instances);instances.append(dict(instance_id=len(instances),latent_id=row['latent_id'],starts=list(starts),aliases=[]))
   instances[instance_ids[key]]['aliases'].append(dict(edit_id=edit_id,alignment=alignment))
 return dict(descriptions=descriptions,strings=strings,maps=list(maps.values()),instances=instances,alignment_inadmissible=invalid,raw_edits=len(descriptions),raw_edit_kind_counts=dict(Counter(e['kind'] for e in descriptions)),unique_latent_strings=len(strings),unique_constraint_instances=len(instances),admissible_alignment_descriptions=sum(len(i['aliases']) for i in instances),gross_alignment_descriptions=2*len(descriptions))
