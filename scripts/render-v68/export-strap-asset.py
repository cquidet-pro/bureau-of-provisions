"""Write only approved accessory objects as an appendable Blender library.
Run with the authoritative source loaded. Never saves or overwrites that source.
"""
import os,runpy
from pathlib import Path
os.environ['BOP_RENDER_MODE']='setup'
g=runpy.run_path(str(Path(__file__).resolve().parent/'native-studio.py'));globals().update(g)
collection=bpy.data.collections.new('BoP approved detachable strap V68')
collection['source_model_sha256']=__import__('hashlib').sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()
collection['units']='metres; original world coordinates; no rescaling'
collection['scope']='Visual accessory: snap hooks, separate D-rings, folded tabs and one continuous strap. No source bottle geometry.'
for o in list(s.objects):
 if o.name.startswith(('WEB-One-continuous-strap','WEB-round-opening-snap-jaw','WEB-snap-spring-gate','WEB-flat-snap-body','WEB-snap-trigger-lever','WEB-Snap-trigger-rivet','WEB-short-snap-swivel','WEB-Snap-swivel-collar','WEB-separate-D-ring','WEB-Folded-tab','WEB-tab-stitch')):
  collection.objects.link(o)
# Embed the neutral textile so the library has no external image dependency.
palette({'number':9,'body':'#f4f3ee','accent':'#f4f3ee'})
for image in bpy.data.images:
 if image.source=='FILE' and image.filepath and Path(bpy.path.abspath(image.filepath)).is_file():image.pack()
out=ROOT/'design/blender-assets/v68-strap-system.blend';out.parent.mkdir(parents=True,exist_ok=True)
bpy.data.libraries.write(str(out),{collection},fake_user=True,compress=True)
print('Exported',len(collection.objects),'accessory objects to',out)
