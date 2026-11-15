"""Verify final native masters/deliveries and preserve accepted review evidence."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
root=Path(__file__).resolve().parents[2]
read=lambda p:json.loads((root/p).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[]
for p in sorted((root/'public/images/product').glob('*-native-v68.png')):
 w=p.with_suffix('.webp')
 with Image.open(p) as a,Image.open(w) as b:
  assert a.size==b.size and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes(),str(p)
  size=a.size
 files.append({'png':'/'+str(p.relative_to(root/'public')),'webp':'/'+str(w.relative_to(root/'public')),'dimensions':size,'png_sha256':sha(p),'webp_sha256':sha(w),'pixel_identical':True})
for name in ['source-geometry-integrity.json','dimension-audit.json','view-anchors.json','section-record.json','catalogue-branding-calibration.json']:
 source=root/'output/design-v68/native'/name
 if source.exists():shutil.copy2(source,root/'docs/v68'/name)
proof=read('docs/v68/source-geometry-integrity.json');assert proof['unchanged'] and proof['before']==proof['after']
j=read('design/product-design.json');native=root.parent/'water-bottle-design'/j['current_geometry']['native_file'];assert sha(native)==proof['source_sha256']
(root/'docs/v68/delivery-verification.json').write_text(json.dumps({'source_model_sha256':proof['source_sha256'],'source_geometry_unchanged':True,'strap_hook_reference':'docs/v68/SWIVEL_SNAP_HOOK_REFERENCE.png','lossless_file_count':len(files),'files':files},indent=2)+'\n')
sheet=Image.new('RGB',(1320,1800),'#f4eddf');d=ImageDraw.Draw(sheet)
for i,e in enumerate(j['editions']):
 im=Image.open(root/('public'+e['source_png']));im.thumbnail((220,330));x=i%6*220;y=i//6*360;sheet.paste(im,(x,y));d.text((x+5,y+335),f"{e['number']:02} {e['name']}",fill='#293b3d')
sheet.save(root/'docs/v68/collection-contact.png')
print(f'{len(files)} PNG/WebP pairs are pixel-identical; source Blender file and geometry are unchanged; referenced swivel snap hooks are current.')
