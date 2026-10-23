// Independent forward-cell/pixel-string oracle. No integer-polynomial code imported.
import fs from 'node:fs';
import {performance} from 'node:perf_hooks';
let input,font;
if(process.argv.includes('--stdin')){const p=JSON.parse(fs.readFileSync(0,'utf8'));input=p.input;font=p.glyphs;}
else if(process.argv.includes('--actual')){input=JSON.parse(fs.readFileSync(new URL('../data/monument-slide-input-v2.json',import.meta.url)));font=JSON.parse(fs.readFileSync(new URL('../data/fold-aperture-surrogate-v1.json',import.meta.url))).glyph_rows;}
else throw Error('Explicit --stdin or --actual required');
const start=performance.now(),W=input.width,H=input.cipher_rows.length,Z=Array(7).fill('00000'),center=rows=>rows.map(row=>' '.repeat(Math.floor((W-row.length)/2))+row+' '.repeat(W-row.length-Math.floor((W-row.length)/2))),mirror=rows=>rows.map(r=>[...r].reverse().join('')),C=center(input.cipher_rows),out=[];
for(const[model,raw]of Object.entries(input.models)){const T=mirror(mirror(center(raw)));
for(let dy=-H;dy<=H;dy++)for(let dx=-W;dx<=W;dx++){
 if(performance.now()-start>120000||process.memoryUsage().rss>1073741824)throw Error('oracle budget unresolved');
 let geometric=0,eligible=0,area=0,nonempty=0,full=0,union=0;const positions=[],letters=[];
 for(let tr=0;tr<H;tr++)for(let tc=0;tc<W;tc++){const r=tr+dy,c=tc+dx;if(r<0||r>=H||c<0||c>=W)continue;geometric++;const a=C[r][c],b=T[tr][tc],A=font[a]??Z,B=mirror(mirror(font[b]??Z));
 if(/^[A-Z]$/.test(a)&&/^[A-Z]$/.test(b)){eligible++;if(a===b){letters.push(a);positions.push([r+1,c+1,c-Math.floor((W-input.cipher_rows[r].length)/2)+1,tr+1,tc+1,tc-Math.floor((W-raw[tr].length)/2)+1,a]);}}
 let common=0,same=true;for(let y=0;y<7;y++)for(let x=0;x<5;x++){const p=A[y][x]==='1',q=B[y][x]==='1';common+=p&&q;union+=p||q;same&&=p===q;}area+=common;nonempty+=common>0;full+=common>0&&same;}
 out.push({id:`${model}:${dy}:${dx}`,model,dy,dx,geometric_overlap_cells:geometric,comparable_letter_pairs:eligible,label_matches:letters.length,common_pixel_area:area,nonempty_common_aperture_pairs:nonempty,full_mask_coincidences:full,union_pixel_area:union,label_match_fraction:eligible?letters.length/eligible:null,common_over_union:union?area/union:null,matched_letters:letters.join(''),label_positions:positions});}}
process.stdout.write(JSON.stringify({records:out,seconds:(performance.now()-start)/1000,implementation:'Independent forward cell traversal and twice-reflected pixel strings; no packed correlation.'})+'\n');
