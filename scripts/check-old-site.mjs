import assert from 'node:assert/strict';
import {readFileSync,existsSync,readdirSync} from 'node:fs';
import {resolve,join} from 'node:path';
const out=resolve('dist'),read=p=>readFileSync(join(out,p),'utf8');
const archive=JSON.parse(read('old/archive.json')),html=read('old/index.html');
assert.equal(archive.source_commit,'dc88371d87caa1e185bb789f871d3cd1386da825');
assert.ok(html.includes('£39')||html.includes('&#163;39'),'Archive must keep previous prices');
assert.ok(html.includes('platform-strap-reference-v18.webp'));
assert.ok(!html.includes('platform-native-v68.webp'));
assert.ok(html.includes('noindex, follow'));
assert.ok(read('index.html').includes('platform-native-v68.webp'),'Root must retain the current site');
let checked=0;
function inspect(dir) {
 for(const e of readdirSync(dir,{withFileTypes:true})) {
  const file=join(dir,e.name);
  if(e.isDirectory())inspect(file);
  else if(/\.(html|css|js|svg)$/.test(e.name)) {
   const text=readFileSync(file,'utf8');
   assert.ok(!/https:\/\/cdn\.jsdelivr\.net\/gh\//.test(text),'Archive must use self-contained local assets');
   assert.ok(!/["'(]\/images\//.test(text),'Archive must not load current root images');
   for(const match of text.matchAll(/\/old\/(?:images|fonts|assets)\/[\w./-]+\.(?:svg|webp|png|jpe?g|gif|avif|woff2?|css|js)/g)) {
    assert.ok(existsSync(join(out,match[0])),`Missing archived asset ${match[0]}`);checked++;
   }
  }
 }
}
inspect(join(out,'old'));
console.log(`Previous-site archive checks passed: isolated /old assets (${checked} references); current root preserved.`);
