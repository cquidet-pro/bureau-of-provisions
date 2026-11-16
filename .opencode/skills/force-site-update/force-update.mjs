#!/usr/bin/env node
// Read-only verification of a specific Firebase release and its delivered bytes.
import {readFileSync, readdirSync} from 'node:fs';
import {resolve, basename} from 'node:path';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';

const repo='cquidet-pro/bureau-of-provisions';
const args=process.argv.slice(2),assets=[];
let commit='HEAD';
for(let i=0;i<args.length;i++) {
  if(['--verify','-v'].includes(args[i]))continue;
  if(args[i]==='--commit'&&args[i+1])commit=args[++i];
  else if(args[i]==='--asset'&&args[i+1])assets.push(args[++i]);
  else throw Error(`Unknown or incomplete option: ${args[i]}. This helper is read-only; use --verify, --commit SHA and --asset /images/… only.`);
}
const root=resolve(import.meta.dirname,'../../..');
const git=(...argv)=>execFileSync('git',argv,{cwd:root,encoding:'utf8'}).trim();
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const origin=new URL(process.env.LIVE_URL||'https://bureauofprovisions.com');
if(!['https:','http:'].includes(origin.protocol)||origin.username||origin.password)throw Error('LIVE_URL must be an HTTP(S) origin without credentials');
const fetchBytes=async path=>{
  const response=await fetch(new URL(path,origin),{headers:{'Cache-Control':'no-cache'},signal:AbortSignal.timeout(60000)});
  if(!response.ok)throw Error(`HTTP ${response.status}: ${response.url}`);
  return {response,bytes:Buffer.from(await response.arrayBuffer())};
};
try {
  const expected=git('rev-parse','--verify',`${commit}^{commit}`);
  const runs=JSON.parse(execFileSync('gh',['run','list','--repo',repo,'--commit',expected,'--workflow','firebase-deploy.yml','--limit','5','--json','headSha,status,conclusion,url'],{encoding:'utf8',timeout:20000}));
  const run=runs.find(r=>r.headSha===expected);
  if(!run)throw Error(`No deployment run for ${expected.slice(0,8)}. A docs-only commit may be excluded; pass the actual site commit.`);
  if(run.status!=='completed'||run.conclusion!=='success')throw Error(`Deployment is ${run.status}/${run.conclusion||'pending'}: ${run.url}`);
  const {response,bytes}=await fetchBytes('/');
  if(!response.headers.get('cache-control')?.includes('no-cache'))throw Error('Homepage lacks Cache-Control: no-cache');
  const html=bytes.toString('utf8');
  const path=html.match(/(?:src|href)=["']([^"']*\/assets\/index-[\w-]+\.js)["']/)?.[1];
  if(!path)throw Error('No Vite entry bundle found in live HTML');
  const localBundles=readdirSync(resolve(root,'dist/assets')).filter(n=>/^index-[\w-]+\.js$/.test(n));
  if(localBundles.length!==1)throw Error('Run npm run build; expected one local Vite entry bundle');
  const local=readFileSync(resolve(root,'dist/assets',localBundles[0]));
  const live=(await fetchBytes(path)).bytes;
  if(sha(local)!==sha(live))throw Error(`Live JS bytes differ from the local build (${basename(path)} vs ${localBundles[0]})`);
  console.log(`Verified successful deploy ${expected.slice(0,8)}, root no-cache header and identical JS bytes.`);
  for(const path of assets) {
    if(!/^\/images\/[\w./-]+$/.test(path)||path.split('/').includes('..'))throw Error(`Invalid public asset path: ${path}`);
    const local=readFileSync(resolve(root,'public',path.slice(1))),hash=sha(local);
    const live=(await fetchBytes(`${path}?v=${hash.slice(0,16)}`)).bytes;
    if(sha(live)!==hash)throw Error(`Live asset differs: ${path}`);
    if(html.includes(path)&&!html.includes(`${path}?v=${hash.slice(0,16)}`))throw Error(`Homepage lacks the current content cache key: ${path}`);
    console.log(`Verified live asset bytes and applicable cache key: ${path}`);
  }
  console.log(`Live: ${origin.origin}/`);
} catch(error) {
  console.error(`Verification failed: ${error.message}`);
  process.exitCode=1;
}
