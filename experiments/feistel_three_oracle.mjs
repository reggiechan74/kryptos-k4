// Independent sign-potential graph and sequential color-allocation counter.
// It reads only canonical inputs; no production result is used to compute counts.
import fs from 'node:fs';
const root=new URL('../',import.meta.url),data=JSON.parse(fs.readFileSync(new URL('data/k4.json',root),'utf8'));
const AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ',KR='KRYPTOSABCDEFGHIJLMNQUVWXZ',mod=(x,q)=>(x%q+q)%q;
function counter(rows,q){
 if(!rows.length)return {raw_key_count:(BigInt(q)**BigInt(3*q)).toString(),gauge_fixed_key_count:(BigInt(q)**BigInt(3*q-1)).toString()};
 const adj=new Map();const node=n=>{if(!adj.has(n))adj.set(n,[]);};
 for(const r of rows){if(r.R===null)throw Error('known-right scope only');let h='H:'+r.X;node(h);if(r.L!==null){let f='F:'+r.R;node(f);const d=mod(r.Y-r.L,q);adj.get(f).push([h,d]);adj.get(h).push([f,d]);}}
 const p=new Map(),sign=new Map(),ci=new Map(),comps=[];
 for(const start of [...adj.keys()].sort())if(!p.has(start)){
  const k=comps.length,c={nodes:[],pts:[]},todo=[start];p.set(start,0);sign.set(start,1);
  while(todo.length){let n=todo.shift();ci.set(n,k);c.nodes.push(n);for(const [other,d] of adj.get(n)){const a=mod(d-p.get(n),q),s=-sign.get(n);if(!p.has(other)){p.set(other,a);sign.set(other,s);todo.push(other);}else if(p.get(other)!==a||sign.get(other)!==s)return {raw_key_count:'0',gauge_fixed_key_count:'0'};}}
  comps.push(c);
 }
 for(const r of rows){const h='H:'+r.X;comps[ci.get(h)].pts.push({a:mod(r.Y-p.get(h),q),s:-sign.get(h),b:mod(r.X-r.R,q)});}
 for(const c of comps){let seen=new Map(),out=[];for(const t of c.pts){if(seen.has(t.a)&&seen.get(t.a)!==t.b)return {raw_key_count:'0',gauge_fixed_key_count:'0'};if(!seen.has(t.a)){seen.set(t.a,t.b);out.push(t);}}c.pts=out;}
 let anchor=0;for(let k=1;k<comps.length;k++)if(comps[k].pts.length>comps[anchor].pts.length)anchor=k;
 const core=comps.map((c,i)=>i).filter(i=>i!==anchor&&comps[i].pts.length>1),single=comps.filter((c,i)=>i!==anchor&&c.pts.length===1).map(c=>c.pts[0].b);
 const freeFH=2*q-adj.size,occupied=new Map();let sum=0n,assignments=0;
 function singletonWeight(gm){
  const existing=Array(q).fill(0);for(const b of gm.values())existing[b]++;const free=q-gm.size,memo=new Map();
  function rec(i,newCounts){
   const K=newCounts.reduce((a,b)=>a+b,0);if(K>free)return 0n;
   if(i===single.length){let falling=1n;for(let j=0;j<K;j++)falling*=BigInt(free-j);return falling*BigInt(q)**BigInt(free-K);}
   const id=i+':'+newCounts.join(',');if(memo.has(id))return memo.get(id);
   let b=single[i],out=BigInt(existing[b]+newCounts[b])*rec(i+1,newCounts);const more=newCounts.slice();more[b]++;out+=rec(i+1,more);memo.set(id,out);return out;
  }
  return rec(0,Array(q).fill(0));
 }
 function visit(k,offsets){
  if(k<core.length){for(let z=0;z<q;z++){offsets.set(core[k],z);visit(k+1,offsets);}return;}
  assignments++;const gm=new Map();for(const idx of [anchor,...core])for(const t of comps[idx].pts){const x=mod(t.a+t.s*offsets.get(idx),q);if(gm.has(x)&&gm.get(x)!==t.b)return;gm.set(x,t.b);}
  sum+=singletonWeight(gm)*BigInt(q)**BigInt(freeFH);
 }
 visit(0,new Map([[anchor,0]]));return {raw_key_count:(sum*BigInt(q)).toString(),gauge_fixed_key_count:sum.toString(),core_assignments:assignments,components:comps.length,free_F_H_entries:freeFH};
}
function enc(l,r,key,q){const a=mod(l+key.F[r],q),x=mod(r+key.G[a],q);return [x,mod(a+key.H[x],q)];}
function allFunctions(q){const out=[];for(let i=0;i<q**q;i++){let n=i,v=[];for(let j=0;j<q;j++){v.push(n%q);n=Math.floor(n/q);}out.push(v);}return out;}
const controls=[];
for(const q of [2,3])for(let v=0;v<3;v++){
 const key={F:Array.from({length:q},(_,x)=>mod(x*x+v,q)),G:Array.from({length:q},(_,x)=>mod(x*x*x+x+v,q)),H:Array.from({length:q},(_,x)=>mod(2*x+v,q))},rows=[];
 for(const [i,[l0,r0]] of [[0,[0,1]],[1,[1,0]],[2,[1,1]]]){const l=l0%q,r=r0%q,[x,y]=enc(l,r,key,q);rows.push({L:i===1?null:l,R:r,X:x,Y:y});}
 let brute=0n;const funcs=allFunctions(q);
 for(const F of funcs)for(const G of funcs)for(const H of funcs){let good=true;for(const r of rows){let a=mod(r.Y-H[r.X],q),pr=mod(r.X-G[a],q),pl=mod(a-F[pr],q);if(pr!==r.R||(r.L!==null&&pl!==r.L)){good=false;break;}}if(good)brute++;}
 const result=counter(rows,q);if(result.raw_key_count!==brute.toString())throw Error('independent small-system control failed');controls.push({q,case:v,raw_keys:brute.toString()});
}
const records=[];
for(const ai of [AZ,KR])for(const ao of [AZ,KR]){
 const known=new Map(data.cribs.flatMap(c=>[...c.plaintext].map((p,j)=>[c.start-1+j,ai.indexOf(p)])));
 function rows(stage){const out=[];for(let i=0;i<96;i+=2){let L=known.has(i)&&(stage==='all'||i<34)?known.get(i):null,R=known.has(i+1)&&(stage==='all'||i+1<34)?known.get(i+1):null;if(L!==null||R!==null)out.push({L,R,X:ao.indexOf(data.ciphertext[i]),Y:ao.indexOf(data.ciphertext[i+1])});}return out;}
 records.push({input_alphabet:ai,output_alphabet:ao,training:counter(rows('first'),26),all_cribs:counter(rows('all'),26)});
}
console.log(JSON.stringify({method:'Independent sign-potential propagation and sequential existing/new color-allocation recurrence with BigInt; post-run verification, not new model counts',controls,records},null,2));
