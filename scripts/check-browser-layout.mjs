// Optional local Chromium layout smoke check against the actual lid markup.
// Requires Vite on port 4173; writes only ignored review output.
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {spawn} from 'node:child_process';
import {setTimeout as delay} from 'node:timers/promises';
import {parseHTML} from 'linkedom';
const chrome=process.env.BOP_CHROME||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
assert.ok(existsSync(chrome),'Set BOP_CHROME to the Chromium executable');
const out=resolve('output/design-v68/browser-check');mkdirSync(out,{recursive:true});
const {document}=parseHTML(readFileSync('index.html','utf8'));
const lid=document.querySelector('[data-drinking-prototype]').outerHTML;
const probe=`import '/src/drinking-prototype.js';
await new Promise(r=>setTimeout(r,100));
const q=s=>document.querySelector(s),results={};
q('[data-drinking-part="spray"]').click();
const spray=q('.part-spray').getBoundingClientRect(),gulp=q('.part-gulp').getBoundingClientRect();
results.labels_separated=gulp.top-spray.bottom>=8;
const play=q('[data-drinking-play]').getBoundingClientRect();
results.mist_control_clear=play.bottom<=spray.top;
q('[data-lid-toggle]').click();
results.closed=q('[data-lid-toggle]').textContent.trim()==='Open lid'&&getComputedStyle(q('[data-lid-closed]')).display!=='none';
q('[data-lid-toggle]').click();
results.opened=q('[data-lid-toggle]').textContent.trim()==='Close lid'&&getComputedStyle(q('[data-lid-closed]')).display==='none';
results.no_horizontal_overflow=document.documentElement.scrollWidth<=innerWidth;
q('[data-drinking-part="spray"]').click();
q('#browser-results').textContent=JSON.stringify(results);`;
writeFileSync(out+'/index.html',`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/src/style.css"><style>body{padding:12px}main{max-width:1000px;margin:auto}#browser-results{display:none}</style></head><body><main>${lid}</main><output id="browser-results"></output><script type="module">${probe}</script></body></html>`);
const profile=out+'/cdp-profile';mkdirSync(profile,{recursive:true});
const processChrome=spawn(chrome,['--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{stdio:'ignore'});
try {
 let port;
 for(let i=0;i<100;i++) {try {port=Number(readFileSync(profile+'/DevToolsActivePort','utf8').split('\n')[0]);if(port)break;}catch{}await delay(100);}
 assert.ok(port,'Chromium debugging endpoint unavailable');
 for(const [name,width,height] of [['desktop',1280,1150],['mobile',390,1800]]) {
  const target=await (await fetch('http://127.0.0.1:'+port+'/json/new?about:blank',{method:'PUT'})).json();
  const socket=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{socket.onopen=r;socket.onerror=j;});
  let sequence=0;const pending=new Map();
  socket.onmessage=e=>{const m=JSON.parse(e.data);if(!m.id)return;const p=pending.get(m.id);pending.delete(m.id);if(m.error)p.reject(Error(m.error.message));else p.resolve(m.result);};
  const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));});
  await send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:name==='mobile'});
  await send('Page.navigate',{url:'http://localhost:4173/output/design-v68/browser-check/'});
  let results;
  for(let i=0;i<100;i++) {
   await delay(100);
   const value=await send('Runtime.evaluate',{expression:'JSON.stringify({width:innerWidth,result:document.querySelector("#browser-results")?.textContent})',returnByValue:true});
   const data=JSON.parse(value.result.value);
   if(data.result){assert.equal(data.width,width,'Actual viewport must match requested width');results=JSON.parse(data.result);break;}
  }
  assert.ok(results,'Browser probe did not finish');
  for(const [check,passed] of Object.entries(results))assert.equal(passed,true,name+': '+check);
  const shot=await send('Page.captureScreenshot',{format:'png'});writeFileSync(out+'/'+name+'.png',Buffer.from(shot.data,'base64'));
  writeFileSync(out+'/'+name+'.json',JSON.stringify({viewport:[width,height],...results},null,2)+'\n');
  socket.close();await fetch('http://127.0.0.1:'+port+'/json/close/'+target.id);
  console.log(name+': exact viewport, labels separated, mist control clear, lid opens/closes, no horizontal overflow');
 }
} finally {processChrome.kill('SIGTERM');}
