"""Derive fixed table/constants only. No message encoder, target or batch."""
import json, heapq, collections
from pathlib import Path
p=Path(__file__).parent
policy={'kind':'static table derivation only; no message inputs','frequency_order':'ETAOINSHRDLCUMWFGYPBVKJXQZ','weight':'26-zero_based_rank','node_key':['weight','minimum contained AZ letter'],'merge':'pop two smallest; first left=0, second right=1; push sum/min','sentinel':'binary leading 1','payload_symbols':97,'base26':'AZ positional, exactly97digits, leading A allowed','outer':'AZ Vigenere literal KRYPTOS phases0..6','terminal':'no extra EOF or padding; require97complete symbols, no trailing bits'}
(p/'SOURCE-POLICY.json').write_text(json.dumps(policy,indent=2)+'\n')
h=[(26-i,a,a) for i,a in enumerate(policy['frequency_order'])];heapq.heapify(h);merges=[]
while len(h)>1:
 a,b=heapq.heappop(h),heapq.heappop(h)
 n=(a[0]+b[0],min(a[1],b[1]),(a[2],b[2]))
 merges.append({'left':[a[0],a[1]],'right':[b[0],b[1]],'parent':[n[0],n[1]]});heapq.heappush(h,n)
c={}
def walk(n,b=''):
 if isinstance(n,str):c[n]=b
 else:walk(n[0],b+'0');walk(n[1],b+'1')
walk(h[0][2]);c=dict(sorted(c.items()))
(p/'CODEBOOK.json').write_text(json.dumps({'codebook':c,'merges':merges},indent=2)+'\n')
q=26**97; B=q-2**455
cert={'length_histogram':dict(sorted(collections.Counter(map(len,c.values())).items())),'min_payload_bits':97*min(map(len,c.values())),'max_payload_bits':97*max(map(len,c.values())),'capacity_integer':str(q),'capacity_bit_length':q.bit_length(),'boundary_payload_length':455,'boundary_payload_upper_exclusive':str(B),'boundary_prefix':bin(B)[2:][:50],'sum_weighted_lengths':sum((26-policy['frequency_order'].index(a))*len(b) for a,b in c.items()),'Kraft_numerator_over_256':sum(2**(8-len(b)) for b in c.values())}
(p/'STATIC-CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n');print(c);print(cert)
