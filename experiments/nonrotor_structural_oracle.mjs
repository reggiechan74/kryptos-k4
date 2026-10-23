// Post-run independent exact-entry audit; no function-key enumeration or K4 plaintext completion.
import fs from 'node:fs';
const root=new URL('../',import.meta.url),d=JSON.parse(fs.readFileSync(new URL('data/k4.json',root),'utf8'));
const AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ',KR='KRYPTOSABCDEFGHIJLMNQUVWXZ',mod=x=>(x%26+26)%26;
const known=new Map(d.cribs.flatMap(c=>[...c.plaintext].map((p,j)=>[c.start-1+j,p])));
function audit(ai,ao,origin,stage){
 const F=new Map(),G=new Map();
 const put=(map,input,value,positions,fn)=>{if(map.has(input)&&map.get(input).value!==value)return {function:fn,input,first_value:map.get(input).value,second_value:value,first_source:map.get(input).positions,second_source:positions};map.set(input,{value,positions});return null;};
 const rows=[];
 for(let i=origin-1;i<96;i+=2){const l=known.has(i)&&(stage==='all'||i<34)?ai.indexOf(known.get(i)):null,r=known.has(i+1)&&(stage==='all'||i+1<34)?ai.indexOf(known.get(i+1)):null;rows.push({l,r,x:ao.indexOf(d.ciphertext[i]),y:ao.indexOf(d.ciphertext[i+1]),positions:[i+1,i+2]});}
 for(const row of rows)if(row.r!==null){const bad=put(G,row.x,mod(row.y-row.r),row.positions,'G');if(bad)return {compatible:false,contradiction:bad};}
 for(const row of rows)if(row.r!==null&&row.l!==null){const bad=put(F,row.r,mod(row.x-row.l),row.positions,'F');if(bad)return {compatible:false,contradiction:bad};}
 if(rows.some(row=>row.l!==null&&row.r===null))throw Error('This narrow audit requires a contradiction before any latent partner branch; not a general solver.');
 return {compatible:true,F_entries:F.size,G_entries:G.size,key_count:(26n**BigInt(52-F.size-G.size)).toString()};
}
const rows=[];
for(const ai of [AZ,KR])for(const ao of [AZ,KR])for(const origin of [1,2]){const training=audit(ai,ao,origin,'first'),all=training.compatible?audit(ai,ao,origin,'all'):null;rows.push({input_alphabet:ai,output_alphabet:ao,pair_origin:origin,training,all_cribs:all});}
console.log(JSON.stringify({kind:'Post-run independent exact-entry certificates; actual models contradict before unsupported latent branch handling',structures:rows},null,2));
