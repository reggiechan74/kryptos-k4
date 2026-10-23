// Independent cell-forward/pixel-string oracle; no Python mask or score imports.
import fs from 'node:fs';
const input=JSON.parse(fs.readFileSync(new URL('../data/monument-slide-input-v2.json',import.meta.url))),font=JSON.parse(fs.readFileSync(new URL('../data/fold-aperture-surrogate-v1.json',import.meta.url))).glyph_rows,W=input.width;
const grid=rows=>rows.map(row=>' '.repeat(Math.floor((W-row.length)/2))+row+' '.repeat(W-row.length-Math.floor((W-row.length)/2))),C=grid(input.cipher_rows),blank=Array(7).fill('00000'),reflect=rows=>rows.map(row=>[...row].reverse().join('')),out=[];
for(const[name,rows]of Object.entries(input.models)){const T=grid(rows);for(let shift=-W;shift<=W;shift++){let labels=0,area=0,nonempty=0,full=0,eligible=0,union=0;
for(let r=0;r<C.length;r++)for(let j=0;j<W;j++){const commonFront=W-1-j,folded=W-1-commonFront,c=folded+shift;if(c<0||c>=W)continue;const a=C[r][c],b=T[r][j],A=font[a]??blank,B=reflect(reflect(font[b]??blank));if(/[A-Z]/.test(a)&&/[A-Z]/.test(b)){eligible++;if(a===b)labels++;}let same=true,common=0;for(let y=0;y<7;y++)for(let x=0;x<5;x++){if(A[y][x]==='1'&&B[y][x]==='1')common++;if(A[y][x]==='1'||B[y][x]==='1')union++;if(A[y][x]!==B[y][x])same=false;}area+=common;if(common)nonempty++;if(common&&same)full++;}
out.push({id:name+':'+shift,label_matches:labels,common_pixel_area:area,nonempty_common_aperture_pairs:nonempty,full_mask_coincidences:full,comparable_letter_pairs:eligible,union_pixel_area:union});}}
process.stdout.write(JSON.stringify(out,null,2)+'\n');
