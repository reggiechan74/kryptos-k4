// Independent post-run verification: ternary-coordinate equalities, not bitmask domains.
import fs from 'node:fs';
import crypto from 'node:crypto';
const data=JSON.parse(fs.readFileSync(new URL('../data/k4.json',import.meta.url)));
const spec=JSON.parse(fs.readFileSync(new URL('../research/specifications/MASK-FM-001.json',import.meta.url)));
function encode(word,mask){return [...word].map((c,i)=>spec.Morse[c]+(i<word.length-1?'x'.repeat(1+((mask>>i)&1)):'')).join('');}
function certificate(cipher,offset,raw){
 const slots=new Map();
 for(let j=0;j<raw.length;j++){
  const absolute=offset+j,c=cipher[Math.floor(absolute/3)],coordinate=absolute%3,key=c+coordinate;
  if(slots.has(key)&&slots.get(key).symbol!==raw[j])return {kind:'same_cipher_coordinate_conflict',cipher:c,coordinate,first:slots.get(key),second:{index:j,symbol:raw[j]}};
  slots.set(key,slots.get(key)??{index:j,symbol:raw[j]});
  if([0,1,2].every(k=>slots.get(c+k)?.symbol==='x'))return {kind:'forbidden_xxx',cipher:c,positions:[0,1,2].map(k=>slots.get(c+k).index)};
 }
 return null;
}
const controls=[];
for(const word of ['COMEATONCE','EASTNORTHEAST','BERLINCLOCK'])for(let phase=0;phase<3;phase++){
 const raw=encode(word,phase),prefix='.-'.repeat(4)+'.'.repeat(phase);let stream=prefix+raw;stream+='x'.repeat((3-stream.length%3)%3);
 const triples=[...new Set(Array.from({length:stream.length/3},(_,i)=>stream.slice(3*i,3*i+3)))];
 if(triples.includes('xxx'))throw Error('invalid plant');
 const cipher=Array.from({length:stream.length/3},(_,i)=>String.fromCharCode(65+triples.indexOf(stream.slice(3*i,3*i+3)))).join('');
 if(certificate(cipher,prefix.length,raw)!==null)throw Error('false contradiction');
 controls.push({word,phase,compatible:true});
}
const counts={},examples={},hash=crypto.createHash('sha256');let contexts=0,compatible=0;
for(let mask=0;mask<4096;mask++){
 const raw=encode('EASTNORTHEAST',mask);
 for(let offset=42;offset<=Math.min(126,291-raw.length);offset++){
  const cert=certificate(data.ciphertext,offset,raw);contexts++;
  if(!cert){compatible++;continue;}
  const category=cert.kind+(cert.coordinate===undefined?'':':'+cert.coordinate);counts[category]=(counts[category]??0)+1;
  if(!examples[category])examples[category]={mask,offset,certificate:cert};
  hash.update(JSON.stringify([mask,offset,cert])+'\n');
 }
}
console.log(JSON.stringify({method:'Independent coordinate-slot contradiction oracle; post-run verification, not additional K4 models',controls,contexts,compatible_contexts:compatible,complete_certificate_stream_sha256:hash.digest('hex'),rejection_counts:counts,examples},null,2));
