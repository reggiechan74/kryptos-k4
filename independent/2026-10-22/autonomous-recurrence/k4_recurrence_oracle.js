"use strict";
const config = {
  "version": "1.0",
  "frozenAt": "2026-10-22T21:46:43Z",
  "orders": [
    2,
    3,
    4,
    5,
    6
  ],
  "alphabets": {
    "AZ": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "KRYPTOS": "KRYPTOSABCDEFGHIJLMNQUVWXZ"
  },
  "affineModes": [
    false,
    true
  ],
  "coefficientEnumerationCapPerStructure": 250000,
  "millisecondsPerStructure": 30000,
  "model": "C_i=P_i+K_i mod26; K_i=b+sum_{j=1}^r a_j K_{i-j}; one-based positions; no resets/refitting; all leading-zero degeneracies retained"
};

function mod(x,p){return ((x%p)+p)%p;}
function inv(x,p){for(let y=1;y<p;y++)if(mod(x*y,p)===1)return y;throw Error("noninvertible");}
function solve(A,y,p){
 const n=A.length,m=A[0]?.length??0,M=A.map((row,i)=>[...row.map(x=>mod(x,p)),mod(y[i],p)]);
 let rank=0;const piv=[];
 for(let c=0;c<m;c++){let q=rank;while(q<n&&M[q][c]===0)q++;if(q===n)continue;
 [M[rank],M[q]]=[M[q],M[rank]];let v=inv(M[rank][c],p);M[rank]=M[rank].map(x=>mod(x*v,p));
 for(let i=0;i<n;i++)if(i!==rank){const f=M[i][c];if(f)for(let j=c;j<=m;j++)M[i][j]=mod(M[i][j]-f*M[rank][j],p);}
 piv.push(c);rank++;
 }
 const inconsistent=M.some(row=>row.slice(0,m).every(x=>x===0)&&row[m]!==0);
 const free=Array.from({length:m},(_,i)=>i).filter(i=>!piv.includes(i));
 const particular=Array(m).fill(0);piv.forEach((c,i)=>particular[c]=M[i][m]);
 const basis=free.map(c=>{const v=Array(m).fill(0);v[c]=1;piv.forEach((pc,i)=>v[pc]=mod(-M[i][c],p));return v;});
 return {prime:p,equations:n,unknowns:m,rank,augmentedRank:rank+(inconsistent?1:0),nullity:m-rank,consistent:!inconsistent,solutionCount:inconsistent?0:p**(m-rank),particular:inconsistent?null:particular,basis:inconsistent?[]:basis,rref:M,pivots:piv};
}
function enumerate(s){if(!s.consistent)return [];const out=[];for(let t=0;t<s.solutionCount;t++){let n=t,v=s.particular.slice();for(const b of s.basis){const z=n%s.prime;n=Math.floor(n/s.prime);v=v.map((x,i)=>mod(x+z*b[i],s.prime));}out.push(v);}return out;}
function crt2_13(a,b){return b+13*mod(a-b,2);}
function build(x,r,affine){const A=[],y=[];for(let i=r;i<x.length;i++){let row=Array.from({length:r},(_,j)=>x[i-j-1]);if(affine)row.push(1);A.push(row);y.push(x[i]);}return {A,y};}
function forecast(x,a,r,affine,endLength){let z=x.slice();let b=affine?a[r]:0;while(z.length<endLength){let v=b;for(let j=1;j<=r;j++)v+=a[j-1]*z[z.length-j];z.push(mod(v,26));}return z;}
function valid(a,A,y,p){return A.every((row,i)=>mod(row.reduce((s,x,j)=>s+x*a[j],0)-y[i],p)===0);}

function brute(A,y,p){const m=A[0].length,out=[];for(let n=0;n<p**m;n++){let t=n,a=[];for(let j=0;j<m;j++){a.push(t%p);t=Math.floor(t/p);}if(valid(a,A,y,p))out.push(a);}return out;}
function canonical(vs){return vs.map(v=>v.join(",")).sort().join("|");}
function seedSystem(a,r,affine,start,observed,p){
 const states=Array.from({length:r},(_,i)=>({v:Array.from({length:r},(_,j)=>i===j?1:0),c:0}));
 for(let i=r;i<start-1+observed.length;i++){const v=Array(r).fill(0);let c=affine?a[r]:0;for(let j=1;j<=r;j++){const old=states[i-j];c+=a[j-1]*old.c;for(let k=0;k<r;k++)v[k]+=a[j-1]*old.v[k];}states.push({v:v.map(x=>mod(x,p)),c:mod(c,p)});}
 return solve(observed.map((_,i)=>states[start-1+i].v),observed.map((x,i)=>mod(x-states[start-1+i].c,p)),p);
}
function makeControls(){
 let checks=0;const failures=[];let rand=123456789;
 const next=()=>{rand=(Math.imul(rand,1664525)+1013904223)>>>0;return rand;};
 for(const p of [2,3,5,13])for(let t=0;t<20;t++){
  let m=p===13?2:1+(next()%3),n=1+(next()%5),A=Array.from({length:n},()=>Array.from({length:m},()=>next()%p)),y=Array.from({length:n},()=>next()%p);
  const s=solve(A,y,p);if(canonical(enumerate(s))!==canonical(brute(A,y,p)))failures.push({kind:"field",p,A,y});checks++;
 }
 for(let t=0;t<25;t++){
  const m=1+next()%3,n=1+next()%5,A=Array.from({length:n},()=>Array.from({length:m},()=>next()%6)),y=Array.from({length:n},()=>next()%6);
  const e2=enumerate(solve(A,y,2)),e3=enumerate(solve(A,y,3)),combined=[];
  for(const a of e2)for(const b of e3)combined.push(b.map((x,i)=>x+3*mod(a[i]-x,2)));
  if(canonical(combined)!==canonical(brute(A,y,6)))failures.push({kind:"composite6",A,y});checks++;
 }
 const planted=[];
 for(const [r,affine,a,seed] of [[2,false,[1,2],[7,11]],[3,true,[5,9,13,4],[6,17,23]],[4,true,[3,5,7,0,9],[4,8,15,16]],[6,true,[2,4,6,8,10,12,14],[1,3,5,7,9,11]]]){
  const full=forecast(seed,a,r,affine,97),observed=full.slice(21,34),train=build(observed,r,affine);
  const s2=solve(train.A,train.y,2),s13=solve(train.A,train.y,13);
  const forecasted=forecast(observed,a,r,affine,76),ss2=seedSystem(a,r,affine,22,observed,2),ss13=seedSystem(a,r,affine,22,observed,13);
  const ok=valid(a,train.A,train.y,26)&&s2.consistent&&s13.consistent&&forecasted.every((v,i)=>v===full[21+i])&&ss2.consistent&&ss13.consistent;
  if(!ok)failures.push({kind:"planted",r,a,seed});
  planted.push({r,affine,coefficients:a,seed,lastCoefficient:a[r-1],trainingSolutionCount:s2.solutionCount*s13.solutionCount,seedSolutionCount:ss2.solutionCount*ss13.solutionCount,pass:ok});checks++;
 }
 // Independent exhaustive seed-state comparison over small rings with nonunit/zero final coefficients.
 for(const q of [2,3,6])for(let t=0;t<20;t++){
  const r=2,affine=true,a=Array.from({length:3},()=>next()%q),seed=Array.from({length:2},()=>next()%q),full=[...seed];
  while(full.length<10){const i=full.length;full.push(mod(a[2]+a[0]*full[i-1]+a[1]*full[i-2],q));}
  const observed=full.slice(6,10),bruteSeeds=[];
  for(let u=0;u<q;u++)for(let v=0;v<q;v++){const f=[u,v];while(f.length<10){const i=f.length;f.push(mod(a[2]+a[0]*f[i-1]+a[1]*f[i-2],q));}if(f.slice(6).every((x,i)=>x===observed[i]))bruteSeeds.push([u,v]);}
  let solved;if(q===6){const e2=enumerate(seedSystem(a,r,affine,7,observed,2)),e3=enumerate(seedSystem(a,r,affine,7,observed,3));solved=[];for(const x of e2)for(const y of e3)solved.push(y.map((v,i)=>v+3*mod(x[i]-v,2)));}else solved=enumerate(seedSystem(a,r,affine,7,observed,q));
  if(canonical(solved)!==canonical(bruteSeeds))failures.push({kind:"reachability",q,a,seed});checks++;
 }
 return {checks,failures,planted};
}

function runK4(cfg){
 const C="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR";
 const first="EASTNORTHEAST",second="BERLINCLOCK",results=[];
 for(const [name,alphabet] of Object.entries(cfg.alphabets)){
 const cv=[...C].map(c=>alphabet.indexOf(c));
 const keyFirst=[...first].map((c,i)=>mod(cv[21+i]-alphabet.indexOf(c),26)),keySecond=[...second].map((c,i)=>mod(cv[63+i]-alphabet.indexOf(c),26));
 for(const r of cfg.orders)for(const affine of cfg.affineModes){
  const start=Date.now(),{A,y}=build(keyFirst,r,affine),s2=solve(A,y,2),s13=solve(A,y,13),count=s2.solutionCount*s13.solutionCount;
  const row={alphabet:name,order:r,affine,equations:A.length,parameters:r+(affine?1:0),keyFirst,keySecond,A,y,field2:s2,field13:s13,trainingCoefficientCount:count};
  if(!count){row.status="impossible_training";row.enumerated=0;row.berlinSurvivorCoefficients=0;row.distinctFullPlaintextClasses=0;row.ms=Date.now()-start;results.push(row);continue;}
  if(count>cfg.coefficientEnumerationCapPerStructure){row.status="budget_unresolved";results.push(row);continue;}
  const candidates=[],survivors=[],forecastSets=Array.from({length:63},()=>new Set());
  coefficientLoop: for(const a2 of enumerate(s2))for(const a13 of enumerate(s13)){
   if(Date.now()-start>cfg.millisecondsPerStructure){row.status="budget_unresolved";break coefficientLoop;}
   const a=a2.map((v,i)=>crt2_13(v,a13[i])),key=forecast(keyFirst,a,r,affine,76),berlin=key.slice(42,53),forecastPlain=key.slice(13).map((v,i)=>alphabet[mod(cv[34+i]-v,26)]).join("");
   for(let i=0;i<63;i++)forecastSets[i].add(forecastPlain[i]);
   const matches=berlin.map((v,i)=>v===keySecond[i]),candidate={coefficients:a,predictedBerlinKey:berlin,predictedBerlinPlaintext:forecastPlain.slice(29,40),berlinMatches:matches.filter(Boolean).length,firstMismatchOneBased:matches.every(Boolean)?null:64+matches.findIndex(v=>!v)};
   candidates.push(candidate);
   if(matches.every(Boolean)){candidate.reachability2=seedSystem(a,r,affine,22,keyFirst,2);candidate.reachability13=seedSystem(a,r,affine,22,keyFirst,13);candidate.initialSeedCount=candidate.reachability2.solutionCount*candidate.reachability13.solutionCount;survivors.push(candidate);}
  }
  row.enumerated=candidates.length;row.candidates=candidates;row.berlinSurvivorCoefficients=survivors.length;row.survivors=survivors;row.trainingCommonPlaintext35to97=forecastSets.map(s=>s.size===1?[...s][0]:"?").join("");row.trainingForecastAmbiguousPositions=forecastSets.map((s,i)=>s.size>1?35+i:null).filter(x=>x!==null);row.status=row.status??(survivors.length?"survives_berlin":"impossible_berlin");row.distinctFullPlaintextClasses=survivors.length?null:0;row.ms=Date.now()-start;results.push(row);
 }
 }
 return {ciphertext:C,firstCrib:{start:22,text:first},secondCrib:{start:64,text:second},results};
}

function extraReachabilityControls(){
 let checks=0;const failures=[];let rnd=987654321;
 const next=()=>{rnd=(Math.imul(rnd,1103515245)+12345)>>>0;return rnd;};
 for(const q of [2,3,6])for(let t=0;t<20;t++){
  const a=Array.from({length:3},()=>next()%q),obs=Array.from({length:4},()=>next()%q),found=[];
  for(let u=0;u<q;u++)for(let v=0;v<q;v++){
   const z=[u,v];for(let i=2;i<10;i++)z.push(mod(a[2]+a[0]*z[i-1]+a[1]*z[i-2],q));
   if(z.slice(6).every((x,i)=>x===obs[i]))found.push([u,v]);
  }
  let solved;
  if(q===6){solved=[];for(const x of enumerate(seedSystem(a,2,true,7,obs,2)))for(const y of enumerate(seedSystem(a,2,true,7,obs,3)))solved.push(y.map((v,i)=>v+3*mod(x[i]-v,2)));}
  else solved=enumerate(seedSystem(a,2,true,7,obs,q));
  if(canonical(solved)!==canonical(found))failures.push({q,a,obs});checks++;
 }
 for(const p of [2,13]){
  const impossible=seedSystem([0,0,0],2,true,22,[1,0,0,0],p);
  if(impossible.consistent)failures.push({kind:"unreachable_zero_transition",p});checks++;
 }
 return {checks,failures};
}
function makeCertificates(result){
 return result.results.filter(x=>x.order===6&&x.affine).map(row=>{
 const A=row.A,y=row.y,m=A[0].length;
 const tr=Array.from({length:m},(_,j)=>A.map(r=>r[j]));tr.push(y);
 const s=solve(tr,Array(m).fill(0).concat([1]),2),lambda=s.particular;
 const cert={alphabet:row.alphabet,keyFirst:row.keyFirst,parity:row.keyFirst.map(x=>x%2),constraintPositions:Array.from({length:7},(_,i)=>28+i),lambdaMod2:lambda,selectedPositions:lambda.flatMap((x,i)=>x?[28+i]:[]),selectedRows:lambda.flatMap((x,i)=>x?[A[i].map(v=>v%2)]:[]),selectedRhs:lambda.flatMap((x,i)=>x?[y[i]%2]:[]),lhsCombination:Array.from({length:m},(_,j)=>mod(lambda.reduce((sum,x,i)=>sum+x*A[i][j],0),2)),rhsCombination:mod(lambda.reduce((sum,x,i)=>sum+x*y[i],0),2)};
 if(cert.lhsCombination.some(x=>x!==0)||cert.rhsCombination!==1)throw Error("invalid certificate");
 return cert;
 });
}
function compactReport(cfg){
 const controls=makeControls(),extra=extraReachabilityControls();
 if(controls.failures.length||extra.failures.length)throw Error("control failure");
 const result=runK4(cfg),certificates=makeCertificates(result);
 return {config:cfg,ciphertext:result.ciphertext,firstCrib:result.firstCrib,secondCrib:result.secondCrib,controls:{checks:controls.checks+extra.checks,failures:[],planted:controls.planted},
 structures:result.results.map(x=>({alphabet:x.alphabet,order:x.order,affine:x.affine,equations:x.equations,parameters:x.parameters,field2:{rank:x.field2.rank,augmentedRank:x.field2.augmentedRank,nullity:x.field2.nullity,solutionCount:x.field2.solutionCount},field13:{rank:x.field13.rank,augmentedRank:x.field13.augmentedRank,nullity:x.field13.nullity,solutionCount:x.field13.solutionCount},trainingCoefficientCount:x.trainingCoefficientCount,enumerated:x.enumerated,status:x.status,berlinSurvivorCoefficients:x.berlinSurvivorCoefficients,distinctFullPlaintextClasses:x.distinctFullPlaintextClasses})),certificates,
 conclusion:{formalStructures:result.results.length,trainingCoefficientTuples:result.results.reduce((n,x)=>n+x.trainingCoefficientCount,0),berlinEvaluations:result.results.reduce((n,x)=>n+(x.enumerated??0),0),initialStatesExamined:0,distinctFullPlaintextClasses:result.results.every(x=>x.distinctFullPlaintextClasses===0)?0:null,budgetUnresolved:result.results.filter(x=>x.status==="budget_unresolved").length,predictions:"Not applicable: no first-crib training solutions. No common-prediction or post-Berlin selection claim is made.",reachability:"Not needed for K4 rejection. Any unknown-prefix state would still have to satisfy the inconsistent local equations. Seed reachability is separately tested using linear state propagation, including singular/nonunit transitions.",scope:"Only autonomous constant-coefficient recurrences of orders 2 through 6 under C=P+K mod26 in the specified two alphabets, homogeneous or affine. No general impossibility or novelty claim."}};
}

console.log(JSON.stringify(compactReport(config), null, 2));
