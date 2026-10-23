"use strict";
// Synthetic-only proof harness for full-state meet-in-the-middle inference.
// No K4 text, historical wiring, or real search is evaluated here.
function mod(x,n){return (x%n+n)%n;}
function perms(n){return Array.from({length:5},(_,j)=>Array.from({length:n},(_,x)=>mod((j%2?-1:1)*x+j+1,n)));}
function turn(w,p,x){return mod(w[mod(x+p,w.length)]-p,w.length);}
function back(w,p,x){return mod(w.indexOf(mod(x+p,w.length))-p,w.length);}
function product(n,k){let out=[[]];for(let i=0;i<k;i++)out=out.flatMap(v=>Array.from({length:n},(_,x)=>v.concat(x)));return out;}
function enc(p,w,delta,seed){return p.map((x,i)=>{for(let j=0;j<5;j++)x=turn(w[j],mod(seed[j]+delta[i][j],w[0].length),x);return x;});}
function mitm(p,c,w,delta){
 const n=w[0].length,left=new Map(),out=[];
 for(const s of product(n,2)){
  const sig=p.slice(0,3).map((x,i)=>{for(let j=0;j<2;j++)x=turn(w[j],mod(s[j]+delta[i][j],n),x);return x;}).join(",");
  if(!left.has(sig))left.set(sig,[]);left.get(sig).push(s);
 }
 for(const t of product(n,3)){
  const sig=c.slice(0,3).map((x,i)=>{for(let j=4;j>=2;j--)x=back(w[j],mod(t[j-2]+delta[i][j],n),x);return x;}).join(",");
  for(const s of left.get(sig)||[]){const seed=s.concat(t);if(enc(p,w,delta,seed).every((x,i)=>x===c[i]))out.push(seed);}
 }
 return out.map(x=>x.join(",")).sort();
}
function direct(p,c,w,d){return product(w[0].length,5).filter(s=>enc(p,w,d,s).every((x,i)=>x===c[i])).map(x=>x.join(",")).sort();}
function controls(){
 const results=[];
 for(const n of [2,3,4,6])for(let v=0;v<4;v++){
  const w=perms(n),p=Array.from({length:7},(_,i)=>mod(i*i+v,n)),delta=Array.from({length:7},(_,i)=>Array.from({length:5},(_,j)=>mod((j+1)*i+i*i+v*j,n))),seed=Array.from({length:5},(_,j)=>mod(j+v,n));
  const c=enc(p,w,delta,seed),a=mitm(p,c,w,delta),b=direct(p,c,w,delta);
  if(JSON.stringify(a)!==JSON.stringify(b)||!a.includes(seed.join(",")))throw Error("complete compatible-set mismatch");
  const z=Array.from({length:7},()=>[0,0,0,0,0]),p0=[0,1,0,1,0,1,0].map(x=>x%n),bad=enc(p0,w,z,seed);bad[2]=mod(bad[0]+1,n);
  if(mitm(p0,bad,w,z).length!==0||direct(p0,bad,w,z).length!==0)throw Error("mutation should be incompatible");
  results.push({modulus:n,case:v,raw_states:n**5,compatible:a.length,truth_included:true,complete_sets_equal:true,mutation_rejected:true});
 }
 return {cases:results,complete_set_comparisons:results.length,mutation_comparisons:results.length,K4_evaluations:0,location:"Orchestration JavaScript runtime while Mac executor unavailable; not a Mac production replay"};
}
controls();
