import test from 'node:test';
import assert from 'node:assert/strict';
import {entranceDrawing,mountEntrance,ENTRANCE_SOURCES} from './source/entrance-installation.mjs';

test('both illustrative views have finite accessible geometry and explicit frame limitations',()=>{
 for(const view of ['oblique','plan']){
  const svg=entranceDrawing(view,true);
  assert.match(svg,/role="img" aria-labelledby=/);
  assert.match(svg,/not registered to true north/);
  assert.match(svg,/no metric scale/);
  assert.doesNotMatch(svg,/NaN|Infinity|<animate|247\.5|220°/);
  assert.ok((svg.match(/<polygon/g)||[]).length>8);
 }
 assert.notEqual(entranceDrawing('oblique'),entranceDrawing('plan'));
 assert.throws(()=>entranceDrawing('survey'));
});
test('labels and view controls only update the isolated illustration',()=>{
 const buttons=['oblique','plan'].map(view=>({dataset:{entranceView:view},setAttribute(k,v){this[k]=v;}}));
 const drawing={},status={},label={checked:true};
 const host={querySelector:s=>({'#entrance-drawing':drawing,'#entrance-view-status':status,'#entrance-labels':label}[s]),querySelectorAll:()=>buttons};
 const control=mountEntrance(host);
 assert.deepEqual(control.getState(),{view:'oblique',labels:true});
 buttons[1].onclick();assert.equal(control.getState().view,'plan');
 label.onchange({target:{checked:false}});assert.equal(control.getState().labels,false);
 assert.doesNotMatch(drawing.innerHTML,/ENGRAVED GRANITE/);
 control.reset();assert.deepEqual(control.getState(),{view:'oblique',labels:true});
 assert.match(host.innerHTML,/schematic, not survey scale/);
 assert.match(host.innerHTML,/separate from the courtyard copper screen/);
});
test('reference list uses source URLs without redistributing image pixels',()=>{
 assert.equal(ENTRANCE_SOURCES.length,5);
 for(const [title,url] of ENTRANCE_SOURCES){assert.ok(title.length>0);assert.equal(new URL(url).protocol,'https:');}
 assert.doesNotMatch(entranceDrawing(),/<image|data:image/);
});
