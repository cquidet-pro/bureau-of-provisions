// Reproduce the last pre-V68 website under /old without touching the live root.
import {mkdtempSync,symlinkSync,cpSync,readFileSync,writeFileSync,readdirSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {execFileSync} from 'node:child_process';
const root=resolve(import.meta.dirname,'..');
const revision='dc88371d87caa1e185bb789f871d3cd1386da825';
const scratch=mkdtempSync(join(tmpdir(),'bop-old-')),checkout=join(scratch,'source');
const run=(cmd,args,cwd=root)=>execFileSync(cmd,args,{cwd,stdio:'inherit'});
try {
 run('git',['worktree','add','--detach',checkout,revision]);
 symlinkSync(join(root,'node_modules'),join(checkout,'node_modules'),'dir');
 run('npm',['run','build'],checkout);
 const target=join(root,'public/old');
 rmSync(target,{recursive:true,force:true});cpSync(join(checkout,'dist'),target,{recursive:true});
 function rewrite(dir) {
  for(const entry of readdirSync(dir,{withFileTypes:true})) {
   const file=join(dir,entry.name);
   if(entry.isDirectory())rewrite(file);
   else if(/\.(html|css|js|svg|json|xml|txt)$/.test(entry.name)) {
    let text=readFileSync(file,'utf8').replace(/https:\/\/cdn\.jsdelivr\.net\/gh\/cquidet-pro\/bureau-of-provisions@[^/]+\/public/g,'');
    for(const folder of ['images','fonts','assets','thank-you'])text=text.replaceAll('/'+folder+'/', '/old/'+folder+'/');
    text=text.replace(/((?:href|src)=")\/(favicon[^"?]*|apple-touch-icon\.png|site\.webmanifest)/g,'$1/old/$2');
    if(entry.name.endsWith('.html'))text=text.replace('<head>','<head><meta name="robots" content="noindex, follow">');
    writeFileSync(file,text);
   }
  }
 }
 rewrite(target);
 writeFileSync(join(target,'archive.json'),JSON.stringify({source_commit:revision,mount:'/old/',description:'Previous production website before the V68 update. Current website remains at /.'},null,2)+'\n');
 console.log('Archived previous website at public/old/');
} finally {
 try {run('git',['worktree','remove','--force',checkout]);} finally {rmSync(scratch,{recursive:true,force:true});}
}
