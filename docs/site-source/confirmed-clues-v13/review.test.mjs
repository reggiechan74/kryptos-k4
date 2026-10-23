import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {K4_CLUES,K4_CLUE_MASK,k4ClueCells,mountK4Clues} from './source/k4-clues.mjs';
const {ciphertext}=JSON.parse(readFileSync(new URL('../../../data/k4.json',import.meta.url),'utf8'));
test('all and only canonical confirmed positions',()=>{
 const known=new Map();for(const [start,w] of [[22,'EAST'],[26,'NORTHEAST'],[64,'BERLIN'],[70,'CLOCK']])for(let j=0;j<w.length;j++)known.set(start+j,w[j]);
 assert.equal(K4_CLUE_MASK.length,97);assert.equal(known.size,24);
 for(let i=1;i<=97;i++)assert.equal(K4_CLUE_MASK[i-1],known.get(i)??'·');
 assert.equal([...K4_CLUE_MASK].filter(c=>c==='·').length,73);
 for(const c of K4_CLUES)assert.equal(ciphertext.slice(c.start-1,c.start-1+c.cipher.length),c.cipher);
});
test('logical grid includes exactly 27 padding cells then all 97 positions',()=>{
 const cells=k4ClueCells(ciphertext);assert.equal(cells.length,124);assert.ok(cells.slice(0,27).every(c=>c.position===null));
 for(let i=1;i<=97;i++){const c=cells[26+i];assert.equal(c.position,i);assert.equal(c.cipher,ciphertext[i-1]);assert.equal(c.plain,K4_CLUE_MASK[i-1]);assert.equal(c.column,(26+i)%31+1);assert.equal(c.plainRow,c.cipherRow+1);}
});
test('DOM source keeps indexed buttons and accessible paired known/unknown labels',()=>{
 const doc={createElement(tag){return{tag,style:{},dataset:{},attributes:{},setAttribute(k,v){this.attributes[k]=v;}};}};
 const host={children:[],attributes:{},setAttribute(k,v){this.attributes[k]=v;},append(n){this.children.push(n);}};const clicks=[];
 mountK4Clues(host,ciphertext,i=>clicks.push(i),doc);
 const buttons=host.children.filter(n=>n.tag==='button'),plain=host.children.filter(n=>n.dataset.position);
 assert.equal(buttons.length,97);assert.equal(plain.length,97);
 for(let i=0;i<97;i++){assert.equal(buttons[i].style.gridColumn,plain[i].style.gridColumn);assert.equal(+plain[i].style.gridRow,+buttons[i].style.gridRow+1);assert.match(plain[i].attributes['aria-label'],new RegExp('K4 #'+(i+1)+' · '));}
 buttons[21].onclick();assert.deepEqual(clicks,[22]);assert.match(plain[0].className,/unknown/);assert.match(plain[21].className,/known/);
});
test('wrong span or anchor fails closed',()=>{assert.throws(()=>k4ClueCells(ciphertext.slice(1)));const bad=[...ciphertext];bad[21]='A';assert.throws(()=>k4ClueCells(bad.join('')));});
