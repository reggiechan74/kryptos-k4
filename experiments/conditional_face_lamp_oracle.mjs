// Post-run arithmetic cross-check, separately implemented here; not a second researcher.
import fs from 'node:fs';
const data=JSON.parse(fs.readFileSync(new URL('../data/k4.json',import.meta.url),'utf8'));
const A={AZ:'ABCDEFGHIJKLMNOPQRSTUVWXYZ',KRYPTOS:'KRYPTOSABCDEFGHIJLMNQUVWXZ'};
const mod=x=>(x%26+26)%26;
const pi=[...Array.from({length:4},(_,i)=>3-i),...Array.from({length:31},(_,i)=>34-i),...Array.from({length:31},(_,i)=>65-i),...Array.from({length:31},(_,i)=>96-i)];
if(pi.length!==97||pi.some((x,i)=>pi[x]!==i))throw Error('route inverse');
const rows=[];
for(const [name,a] of Object.entries(A))for(const eq of ['plus','beaufort'])for(let p=1;p<=12;p++)for(const order of ['sub_then_route','route_then_sub']){
 if(p===1&&order==='route_then_sub')continue;
 const key=Array(p).fill(null);let conflict=false;
 for(let off=0;off<13;off++){
  const i=21+off,j=pi[i],phase=(order==='sub_then_route'?i:j)%p;
  const k=mod(a.indexOf(data.ciphertext[j])+(eq==='plus'?-1:1)*a.indexOf('EASTNORTHEAST'[off]));
  if(key[phase]!==null&&key[phase]!==k)conflict=true;key[phase]=k;
 }
 if(key.includes(null))throw Error('undetermined key');
 const r={alphabet:name,equation:eq,period:p,order,training_consistent:!conflict};
 if(!conflict){
  let plain='';
  for(let i=0;i<97;i++){
   const j=pi[i],k=key[(order==='sub_then_route'?i:j)%p],c=a.indexOf(data.ciphertext[j]);
   plain+=a[mod(eq==='plus'?c-k:k-c)];
  }
  const c=Array(97);
  for(let i=0;i<97;i++){
   const j=pi[i],k=key[(order==='sub_then_route'?i:j)%p],v=a.indexOf(plain[i]);
   c[j]=a[mod(eq==='plus'?v+k:k-v)];
  }
  if(c.join('')!==data.ciphertext||plain.slice(21,34)!=='EASTNORTHEAST')throw Error('roundtrip');
  Object.assign(r,{key,plaintext:plain,predicted_berlin:plain.slice(63,74),all_pass:plain.slice(63,74)==='BERLINCLOCK'});
 }
 rows.push(r);
}
const certs=[];
for(const [name,a] of Object.entries(A))for(const eq of ['plus','beaufort']){
 const required=[...'EASTNORTHEAST'].map((v,j)=>mod(a.indexOf(data.ciphertext[21+j])+(eq==='plus'?-1:1)*a.indexOf(v)));
 const first=required.findIndex(v=>v%2!==required[0]%2);
 if(first<0)throw Error('parity certificate absent');
 certs.push({alphabet:name,equation:eq,positions:[22,22+first],required_keys:[required[0],required[first]]});
}
console.log(JSON.stringify({scope:'post-run independent implementation in the same executor; no model expansion',face:rows,lamp_parity:certs},null,2));
