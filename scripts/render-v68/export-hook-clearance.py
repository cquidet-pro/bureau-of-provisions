"""Export evaluated native body and authorised snap meshes for solid checking."""
import os,runpy,json
from pathlib import Path
os.environ['BOP_RENDER_MODE']='setup';g=runpy.run_path(str(Path(__file__).resolve().parent/'native-studio.py'));globals().update(g)
s.frame_set(6);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();data={}
for o in s.objects:
 include=o.name=='01-Body' or o.name.startswith(('WEB-round-opening-snap-jaw','WEB-snap-spring-gate','WEB-flat-snap-body','WEB-snap-trigger-lever','WEB-Snap-trigger-rivet','WEB-short-snap-swivel','WEB-Snap-swivel-collar','WEB-separate-D-ring'))
 if not include:continue
 ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();data[o.name]={'vertices_mm':[[float(x)*1000 for x in ev.matrix_world@v.co] for v in me.vertices],'faces':[list(t.vertices) for t in me.loop_triangles]};ev.to_mesh_clear()
(BASE/'hook-clearance-meshes.json').write_text(json.dumps(data))
print('Exported',len(data),'evaluated body/hook parts',flush=True)
