"""Reproduce authorised native product imagery and validate the website.
Requires Blender 5.3+, Python packages in requirements.txt, rsvg-convert and npm.
The source .blend remains read-only. No image generation or automatic deployment.
"""
import argparse,json,os,shutil,subprocess,sys,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SCRIPTS=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--part',choices=['all','catalogue','views','hero','section','proof'],default='all')
p.add_argument('--blender',default=shutil.which('blender') or '/Applications/Blender.app/Contents/MacOS/Blender')
p.add_argument('--source',type=Path,help='Authoritative .blend; defaults to manifest path in sibling source repository')
a=p.parse_args();design=json.loads((ROOT/'design/product-design.json').read_text())
source=a.source or ROOT.parent/'water-bottle-design'/design['current_geometry']['native_file']
if not source.is_file():p.error(f'Missing native source: {source}')
missing=[m for m in ['PIL','numpy','trimesh','manifold3d'] if importlib.util.find_spec(m) is None]
if missing:p.error('Missing Python packages: '+', '.join(missing)+'. Install scripts/render-v68/requirements.txt in this Python environment before rendering.')
for executable in ['node','npm','rsvg-convert']:
 if not shutil.which(executable):p.error('Missing command: '+executable)
if not Path(a.blender).is_file():p.error('Missing Blender executable: '+a.blender)
subprocess.run(['node','--input-type=module','-e',"await import('linkedom')"],cwd=ROOT,check=True)
task_env={}
if a.part=='proof':
 proof=ROOT/'output/design-v68/review';(proof/'assets').mkdir(parents=True,exist_ok=True)
 task_env={'BOP_ASSET_OUT':str(proof/'assets'),'BOP_EVIDENCE_OUT':str(proof/'evidence'),'BOP_FIT_REPORT':str(proof/'evidence/hook-clearance.json'),'BOP_HOOK_REVIEW_OUT':str(proof/'assets/snap-hook-render.png')}
if a.part in ('all','catalogue'):
 subprocess.run(['node',str(SCRIPTS/'review.mjs'),'--check-approval'],cwd=ROOT,check=True)
def run(cmd,env=None):
 print('Running',Path(cmd[-1]).name,flush=True)
 subprocess.run([str(v) for v in cmd],cwd=ROOT,env={**os.environ,**task_env,**(env or {})},check=True)
def blender(script,env=None,with_source=True):
 run([a.blender,'-b',*([source] if with_source else []),'--python-exit-code','1','--python',SCRIPTS/script],env)
def python(script):run([sys.executable,script])
# Fail before costly rendering if the source or accessory no longer fits.
python(SCRIPTS/'strap-textures.py')
blender('audit-source.py')
blender('export-hook-clearance.py');python(SCRIPTS/'check-hook-clearance.py')
blender('calibrate.py')
if a.part in ('all','catalogue','proof'):
 blender('native-studio.py',{'BOP_RENDER_MODE':'catalogue',**({'BOP_EDITION_IDS':'9'} if a.part=='proof' else {})})
if a.part in ('all','views','hero','section','proof'):
 part='all' if a.part in ('all','views','proof') else a.part
 blender('native-views.py',{'BOP_VIEWS_PART':part})
if a.part=='proof':blender('hook-review.py')
if a.part in ('all','views','hero','proof'):
 blender('compose-station.py',with_source=False)
 if a.part!='proof':python(SCRIPTS/'mist-overlay.py')
python(SCRIPTS/'export-webp.py')
if a.part=='proof':
 run(['node',SCRIPTS/'review.mjs']);sys.exit(0)
python(ROOT/'scripts/generate-responsive-images.py')
python(SCRIPTS/'verify-deliveries.py');run(['npm','run','build'])
print('Native render, delivery and website checks passed. No deployment performed.')
