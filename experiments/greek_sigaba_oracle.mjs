// Post-run second implementation; same executor, not an authentic SIGABA reference.
import fs from 'node:fs';
const read=p=>JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url),'utf8'));
const data=read('data/k4.json'),g=read('data/greek-phonetic-v1.json'),s=read('data/sigaba-inspired-v1.json');
const mod=(x,n)=>(x%n+n)%n;
const greekRows=[];let described=0,fitCount=0,secondCount=0;
for(const [name,a]of Object.entries(g.cipher_alphabets))for(const eq of g.equations)for(const p of g.periods)for(let u=0;u<=76;u++){
 const key=Array(p).fill(null);let ok=true;
 for(let j=0;j<10;j++){
  const k=mod(a.indexOf(data.ciphertext[u+j])+(eq==='plus'?-1:1)*g.greek_alphabet.indexOf(g.first_greek[j]),26),phase=(u+j)%p;
  if(key[phase]!==null&&key[phase]!==k)ok=false;key[phase]=k;
 }
 if(key.includes(null))throw Error('unfitted key');
 described+=77-u;const row={alphabet:name,equation:eq,period:p,first_start:u+1,fit:ok};
 if(ok){
  fitCount++;row.key=key;row.checks=[];
  for(let v=u+10;v<=86;v++){
   let mismatch=null;secondCount++;
   for(let j=0;j<11;j++){
    const pval=g.greek_alphabet.indexOf(g.second_greek[j]);
    const cv=a[mod((eq==='plus'?pval:-pval)+key[(v+j)%p],26)];
    if(cv!==data.ciphertext[v+j]&&mismatch===null)mismatch=v+j+1;
   }
   row.checks.push([v+1,mismatch]);
  }
 }
 greekRows.push(row);
}
// Every raw rotor key is checked independently, without production schedules/tables.
const AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const cw=s.cipher_wirings.map(w=>[...w].map(x=>AZ.indexOf(x))),sw=s.control_wirings.map(w=>[...w].map(x=>AZ.indexOf(x)));
const wire=(w,x,p)=>mod(w[mod(x+p,w.length)]-p,w.length);
const states=(q,r,length)=>{
 let counts=[0,0,0,0,0],rows=[];
 for(let i=0;i<length;i++){
  rows.push(counts.slice());const z=q+i,control=[0,Math.floor(z/676)%26,z%26,Math.floor(z/26)%26,0];
  let selected=[];
  for(let x of [5,6,7,8]){
   for(let j=0;j<5;j++)x=wire(sw[j],x,control[j]);x%=10;
   for(const w of s.index_wirings)x=wire(w,x,r);
   selected.push(Math.floor(x/2));
  }
  counts=counts.map((x,j)=>mod(x+Number(selected.includes(j)),26));
 }
 return rows;
};
const encrypt=(text,st,c)=>[...text].map((ch,i)=>{
 let x=AZ.indexOf(ch);for(let j=0;j<5;j++)x=wire(cw[j],x,mod(st[i][j]+c,26));return AZ[x];
}).join('');
const decrypt=(text,st,c)=>[...text].map((ch,i)=>{
 let x=AZ.indexOf(ch);for(let j=4;j>=0;j--){const p=mod(st[i][j]+c,26);x=mod(cw[j].indexOf(mod(x+p,26))-p,26);}return AZ[x];
}).join('');
const rotorRows=[];
for(let q=0;q<26;q++)for(let r=0;r<10;r++){
 const st=states(q,r,97);
 for(let c=0;c<26;c++){
  const expected=[...'EASTNORTHEAST'].map((ch,j)=>{
   let x=AZ.indexOf(ch);for(let k=0;k<5;k++)x=wire(cw[k],x,mod(st[21+j][k]+c,26));return AZ[x];
  });
  let mismatch=null;
  for(let j=0;j<13;j++)if(expected[j]!==data.ciphertext[21+j]){mismatch=22+j;break;}
  const row={q,c,r,first_conflict:mismatch};
  if(mismatch===null){
   const p=decrypt(data.ciphertext,st,c);row.berlin=p.slice(63,74);row.all_pass=row.berlin==='BERLINCLOCK';
   if(encrypt(p,st,c)!==data.ciphertext)throw Error('regeneration');
  }
  rotorRows.push(row);
 }
}
const controlText=AZ+AZ.split('').reverse().join(''),st=states(25,9,805),controlCipher=encrypt(controlText,st,25);
if(decrypt(controlCipher,st,25)!==controlText)throw Error('independent control inverse');
console.log(JSON.stringify({kind:'post-run separate implementation in same executor',greek:{raw_descriptions:described,first_fits:fitCount,second_checks:secondCount,records:greekRows},sigaba_inspired:{raw_keys:rotorRows.length,records:rotorRows,synthetic_control:{key:[25,25,9],plaintext:controlText,ciphertext:controlCipher}}},null,2));
