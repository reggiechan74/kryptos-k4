// Independent fixed-transition zero-displacement relaxation, not a key search.
import fs from 'node:fs';
const d=JSON.parse(fs.readFileSync(new URL('../data/k4.json',import.meta.url)));
function audit(p,c,start){
 const domains=new Map(),witnesses=[];
 for(let i=0;i+1<p.length;i++){
  const pair=p.slice(i,i+2),equal=c[i]===c[i+1],position=start+i;
  if(!domains.has(pair))domains.set(pair,{allowed:Array.from({length:26},(_,x)=>x),observations:[]});
  const state=domains.get(pair);state.allowed=state.allowed.filter(x=>equal?x===0:x!==0);state.observations.push({position,ciphertext_pair:c.slice(i,i+2),equal});
 }
 for(const [pair,state] of domains)if(state.allowed.length===0)witnesses.push({pair,observations:state.observations,allowed_displacements_mod26:[]});
 return {consistent:witnesses.length===0,contradictions:witnesses};
}
function perms(a){if(a.length===0)return [[]];return a.flatMap((x,i)=>perms(a.filter((_,j)=>j!==i)).map(t=>[x,...t]));}
let controls=0;
for(let n=2;n<=5;n++)for(const key of perms(Array.from({length:n},(_,i)=>i)))for(let q=0;q<n;q++)for(let step=0;step<n;step++){
 if((key[q]===key[(q+step)%n])!==(step===0))throw Error('injective-key zero displacement control failed');controls++;
}
if(!audit('ABAB','CCDD',1).consistent||audit('ABAB','CCDE',1).consistent)throw Error('mutation control failed');
const first=d.cribs[0],result=audit(first.plaintext,d.ciphertext.slice(first.start-1,first.end),first.start);
console.log(JSON.stringify({method:'Post-run independent arbitrary fixed transition-table relaxation: each plaintext digram has one displacement modulo26; no ring alphabet inference',injective_key_controls:controls,mutation_controls:2,first:result,Berlin_evaluations:0,key_enumeration_for_K4:0},null,2));
