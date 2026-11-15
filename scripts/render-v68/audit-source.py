"""Measure evaluated native source bounds, independent of rendered pictures."""
import bpy,json,math,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(os.environ.get('BOP_EVIDENCE_OUT',ROOT/'output/design-v68/native'));OUT.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene;s.frame_set(6);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();result={}
for name in ['01-Body','02-Foot','03-Fixed-cap','04-Hood','05-Button','10-Safety-loop']:
 o=s.objects[name].evaluated_get(dg);me=o.to_mesh();vs=[o.matrix_world@v.co for v in me.vertices]
 result[name]=[[min(v[i] for v in vs)*1000 for i in range(3)],[max(v[i] for v in vs)*1000 for i in range(3)]];o.to_mesh_clear()
result['actual_body_diameter_mm']=result['01-Body'][1][0]-result['01-Body'][0][0]
result['actual_closed_height_mm']=result['04-Hood'][1][2]-result['02-Foot'][0][2]
body=s.objects['01-Body'];vs=[body.matrix_world@v.co for v in body.data.vertices];sections={}
for z in [.01,.05,.12]:
 radii=[]
 for edge in body.data.edges:
  a,b=(vs[i] for i in edge.vertices)
  if (a.z-z)*(b.z-z)<0:
   p=a+(b-a)*((z-a.z)/(b.z-a.z));radii.append(round(math.hypot(p.x,p.y)*1000,2))
 sections[str(z)]=sorted(set(radii))
result['body_section_radii_mm']=sections
assert abs(result['actual_body_diameter_mm']-73)<.005
assert abs(result['actual_closed_height_mm']-249.1)<.005
(OUT/'dimension-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('Native source dimensions verified.')
