// Exercise the sign-off gate in a disposable fixture, never the real receipt.
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,readFileSync,writeFileSync,copyFileSync,symlinkSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve,dirname} from 'node:path';
import {spawnSync} from 'node:child_process';
const root=resolve(import.meta.dirname,'..'),fixture=mkdtempSync(join(tmpdir(),'bop-review-test-'));
try {
 for(const file of ['design/product-design.json','index.html','src/style.css','src/drinking-prototype.js','scripts/render-v68/review.mjs']) {
  const target=join(fixture,file);mkdirSync(dirname(target),{recursive:true});copyFileSync(join(root,file),target);
 }
 symlinkSync(join(root,'node_modules'),join(fixture,'node_modules'),'dir');
 for(const name of ['edition-09-native-v68.webp','platform-native-v68.webp','bottle-cutaway-native-v68.webp','lid-native-v68.webp','straw-up-native-v68.webp','spray-pressed-native-v68.webp']) {
  const p=join(fixture,'public/images/product',name);mkdirSync(dirname(p),{recursive:true});writeFileSync(p,'test-only image placeholder');
 }
 mkdirSync(join(fixture,'docs/v68'),{recursive:true});writeFileSync(join(fixture,'docs/v68/snap-hook-render.png'),'test-only detail placeholder');
 const run=(...args)=>spawnSync(process.execPath,[join(fixture,'scripts/render-v68/review.mjs'),...args],{cwd:fixture,encoding:'utf8'});
 assert.notEqual(run('--check-approval').status,0,'Unapproved batch must be refused');
 assert.equal(run('--from-current').status,0,'Current-source review must generate');
 assert.notEqual(run('--approve').status,0,'Approval needs an identified reviewer');
 assert.equal(run('--approve','--reviewer','TEST FIXTURE ONLY').status,0);
 assert.equal(run('--check-approval').status,0,'Matching receipt should pass');
 const asset=join(fixture,'output/design-v68/review/assets/lid-native-v68.webp');writeFileSync(asset,'changed fixture');
 assert.notEqual(run('--check-approval').status,0,'Changing candidate assets invalidates receipt');
 assert.notEqual(run('--approve','--reviewer','TEST FIXTURE ONLY').status,0,'Changed snapshot must be regenerated');
 assert.equal(run('--from-current').status,0);
 assert.equal(run('--approve','--reviewer','TEST FIXTURE ONLY').status,0);
 const css=join(fixture,'src/style.css');writeFileSync(css,readFileSync(css,'utf8')+'\n/* changed fixture */');
 assert.notEqual(run('--check-approval').status,0,'Changing design inputs invalidates receipt');
 console.log('Review gate checks passed: unapproved, stale inputs and changed proof assets refused; matching fixture accepted.');
} finally {rmSync(fixture,{recursive:true,force:true});}
