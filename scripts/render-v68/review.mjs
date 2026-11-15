// Local-only design proof page and explicit, fingerprinted sign-off receipt.
import {readFileSync,writeFileSync,mkdirSync,copyFileSync,readdirSync,existsSync} from 'node:fs';
import {resolve,relative,join} from 'node:path';
import {createHash} from 'node:crypto';
import {parseHTML} from 'linkedom';
const root=resolve(import.meta.dirname,'../..'),out=join(root,'output/design-v68/review'),assets=join(out,'assets');
const read=p=>readFileSync(join(root,p),'utf8'),sha=b=>createHash('sha256').update(b).digest('hex');
const trackedInputs=['design/product-design.json','index.html','src/style.css','src/drinking-prototype.js',...readdirSync(join(root,'scripts/render-v68')).filter(n=>/\.(py|mjs)$/.test(n)).sort().map(n=>'scripts/render-v68/'+n)];
const inputHash=()=>{
 const design=JSON.parse(read('design/product-design.json'));
 const native=resolve(root,'../water-bottle-design',design.current_geometry.native_file);
 if(existsSync(native)&&sha(readFileSync(native))!==design.current_geometry.source_sha256)throw Error('Native source hash differs from manifest. Resolve the geometry revision before review.');
 return sha(trackedInputs.map(p=>p+'\0'+sha(readFileSync(join(root,p)))).join('\n'));
};
const snapshotHash=()=>sha(readdirSync(assets).sort().map(n=>n+'\0'+sha(readFileSync(join(assets,n)))).join('\n'));
const receipt=join(root,'design/render-approval.json'),manifest=join(out,'review.json');
if(process.argv.includes('--check-approval')) {
 if(!existsSync(receipt)) throw Error('No full-batch approval. Generate design:proof and obtain user sign-off first.');
 const a=JSON.parse(readFileSync(receipt));
 if(a.input_sha256!==inputHash()) throw Error('Design inputs changed after sign-off. Regenerate the proof and obtain fresh approval.');
 if(existsSync(manifest)&&snapshotHash()!==a.snapshot_sha256)throw Error('Proof assets changed after sign-off. Regenerate and review them.');
 console.log('Current design inputs have an explicit sign-off receipt.');
} else if(process.argv.includes('--approve')) {
 const at=process.argv.indexOf('--reviewer'),reviewer=process.argv[at+1];
 if(at<0||!reviewer||reviewer.startsWith('--')) throw Error('Use --reviewer NAME only after that person explicitly signs off.');
 const proof=JSON.parse(readFileSync(manifest));
 if(proof.input_sha256!==inputHash()||proof.snapshot_sha256!==snapshotHash()) throw Error('Proof is stale or its assets changed. Regenerate and review it.');
 writeFileSync(receipt,JSON.stringify({...proof,reviewer,approved_at:new Date().toISOString(),authorization:'Operator records an explicit user sign-off; this command does not infer approval.'},null,2)+'\n');
 console.log('Recorded explicit sign-off. Commit design/render-approval.json with the resulting batch.');
} else {
 mkdirSync(assets,{recursive:true});
 const current=process.argv.includes('--from-current');
 const names=['edition-09-native-v68.webp','platform-native-v68.webp','bottle-cutaway-native-v68.webp','lid-native-v68.webp','straw-up-native-v68.webp','spray-pressed-native-v68.webp'];
 if(current) for(const n of names)copyFileSync(join(root,'public/images/product',n),join(assets,n));
 if(current)copyFileSync(join(root,'docs/v68/snap-hook-render.png'),join(assets,'snap-hook-render.png'));
 for(const n of [...names,'snap-hook-render.png'])if(!existsSync(join(assets,n)))throw Error('Missing proof asset: '+n);
 const {document}=parseHTML(read('index.html'));
 const scene=document.querySelector('.product-scene-visual').cloneNode(true);scene.querySelector('.feature-hotspots')?.remove();
 const neutral=document.querySelector('[data-colour-number="9"] .colour-render')||document.querySelector('[data-palette="All White"] .colour-render');
 if(!neutral)throw Error('Neutral edition missing');
 const anatomy=document.querySelector('.anatomy-drawing').outerHTML;
 const lid=document.querySelector('[data-drinking-prototype]').outerHTML;
 const html=`<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BoP design proof — local review</title><link rel="stylesheet" href="/src/style.css"><link rel="stylesheet" href="/fonts/fonts.css"><style>body{padding:24px}main{max-width:1000px;margin:auto}section{margin:40px 0}h1{font-size:32px}h2{font-size:25px}.proof-neutral,.anatomy-drawing{max-width:430px;margin:auto}.proof-hook{display:block;max-width:700px;width:100%;margin:auto}.proof-note{padding:16px;border:1px solid #713b44}.proof-neutral .colour-render{display:block;position:relative}.proof-neutral img{max-width:100%}.anatomy-drawing{position:relative}.feature-popover{display:none}</style></head><body><main><h1>Design proof / One approved geometry</h1><p class="proof-note">Local review only. This page does not approve or publish anything. Review each image type and explicitly sign off before a full batch. Browser review at desktop and phone widths remains required when available. ${current?'This snapshot uses current completed masters.':'These are isolated candidate renders; the production masters were not replaced.'}</p><section><h2>01 / One neutral colourway</h2><div class="proof-neutral">${neutral.outerHTML}</div></section><section><h2>02 / Recessed snap hook</h2><img class="proof-hook" src="assets/snap-hook-render.png" alt="Snap hook seated in native recess"></section><section><h2>03 / Main scene, artwork and leaders</h2>${scene.outerHTML}</section><section><h2>04 / Cutaway</h2>${anatomy}</section><section><h2>05 / Lid, Flat / Up and spray press</h2>${lid}</section><p class="proof-note">Check: native features and proportions; hook reference and clearance; cut edge and water; both crest supporters; discreet braille only where intended; small edge dots; sharpness at intended size. Report corrections, or explicitly approve this proof.</p></main><script type="module" src="/src/drinking-prototype.js"></script></body></html>`;
 let page=html;
 for(const n of names)page=page.replaceAll('/images/product/'+n,'assets/'+n);
 writeFileSync(join(out,'index.html'),page);
 writeFileSync(manifest,JSON.stringify({created_at:new Date().toISOString(),input_sha256:inputHash(),snapshot_sha256:snapshotHash(),image_types:names,production_unchanged:!current,source:current?'current completed masters':'isolated candidate render'},null,2)+'\n');
 console.log('Review at http://localhost:4173/output/design-v68/review/ (start npm run dev -- --port 4173). No sign-off recorded.');
}
