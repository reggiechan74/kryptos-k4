// Confirmed K4 clues only. One-based position1 is the first O of OBKR.
export const K4_CLUES=Object.freeze([
 Object.freeze({start:22,cipher:'FLRV',plain:'EAST'}),
 Object.freeze({start:26,cipher:'QQPRNGKSS',plain:'NORTHEAST'}),
 Object.freeze({start:64,cipher:'NYPVTT',plain:'BERLIN'}),
 Object.freeze({start:70,cipher:'MZFPK',plain:'CLOCK'})
]);
export const K4_CLUE_MASK='·'.repeat(21)+'EASTNORTHEAST'+'·'.repeat(29)+'BERLINCLOCK'+'·'.repeat(23);
export function k4ClueCells(cipher){
 if(cipher.length!==97)throw Error('Expected97K4characters');
 for(const clue of K4_CLUES)if(cipher.slice(clue.start-1,clue.start-1+clue.cipher.length)!==clue.cipher)throw Error('Confirmed clue does not match canonical K4');
 return Array.from({length:124},(_,slot)=>{const i=slot-26,line=Math.floor(slot/31);return{position:i>0?i:null,column:slot%31+1,cipherRow:line*2+1,plainRow:line*2+2,cipher:i>0?cipher[i-1]:'·',plain:i>0?K4_CLUE_MASK[i-1]:'',known:i>0&&K4_CLUE_MASK[i-1]!=='·'};});
}
export function mountK4Clues(host,cipher,onSelect,doc=document){
 host.setAttribute('aria-label','K4 ciphertext with confirmed clues directly beneath each line');
 for(const cell of k4ClueCells(cipher)){
  const encrypted=doc.createElement(cell.position?'button':'span');encrypted.textContent=cell.cipher;encrypted.style.gridColumn=String(cell.column);encrypted.style.gridRow=String(cell.cipherRow);encrypted.dataset.kind='cipher';
  if(cell.position){encrypted.dataset.i=cell.position;encrypted.title=`K4 #${cell.position} · ciphertext ${cell.cipher}`;encrypted.setAttribute('aria-label',encrypted.title);encrypted.onclick=()=>onSelect(cell.position);}else{encrypted.className='blank';encrypted.setAttribute('aria-hidden','true');}
  host.append(encrypted);
  const plain=doc.createElement('span');plain.textContent=cell.plain;plain.className=cell.position?'k4-clue '+(cell.known?'known':'unknown'):'blank';plain.dataset.kind='plain';plain.style.gridColumn=String(cell.column);plain.style.gridRow=String(cell.plainRow);
  if(cell.position){plain.dataset.position=cell.position;plain.title=`K4 #${cell.position} · ${cell.known?'confirmed '+cell.plain:'unknown'}`;plain.setAttribute('aria-label',plain.title);}else plain.setAttribute('aria-hidden','true');
  host.append(plain);
 }
}
