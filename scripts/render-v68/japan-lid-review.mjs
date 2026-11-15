// One-edition local review, using the retained proof lid and steel button.
import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {parseHTML} from 'linkedom';
const out='output/design-v68/japan-lid-trial';
const image=out+'/assets/edition-26-native-v68.webp';
if(!existsSync(image))throw Error('Render/export the Japan sample first');
const hash=createHash('sha256').update(readFileSync(image)).digest('hex').slice(0,16);
const {document}=parseHTML(readFileSync('index.html','utf8'));
const render=document.querySelector('[data-colour-number="26"] .colour-render').outerHTML.replace('/images/product/edition-26-native-v68.webp','assets/edition-26-native-v68.webp?review='+hash);
writeFileSync(out+'/index.html',`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Japan / Local review</title><link rel="stylesheet" href="/src/style.css"><style>body{padding:24px}main{max-width:520px;margin:auto}h1{font-size:30px}.colour-render{display:block;position:relative}.colour-render>img:first-child{width:100%;height:auto;display:block}</style></head><body><main><h1>Japan / Local review</h1><p>Previous proof lid retained. Stainless-steel button and centred strap animals.</p>${render}</main></body></html>`);
console.log('http://localhost:4173/'+out+'/');
