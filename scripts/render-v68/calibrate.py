import os,runpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
os.environ['BOP_RENDER_MODE']='setup';g=runpy.run_path(str(Path(__file__).resolve().parent/'native-studio.py'));globals().update(g)
s.frame_set(6);bpy.context.view_layer.update()
def project(p):
 q=world_to_camera_view(s,c,p);return [q.x*s.render.resolution_x,(1-q.y)*s.render.resolution_y]
record={}
for side,label,width_ratio,aspect in [(-1,'greyhound',.043,530/310),(1,'leopard',.041,615/355)]:
 # Centre the emblem on the fabric at its centre height, not its top edge.
 top=.50895*1536;width=width_ratio*1024;height=width*aspect;centre_y=top+height/2
 for p,q in zip(points,points[1:]):
  if p.x*side<=0 or p.z<.05:continue
  a,b=project(p),project(q)
  if min(a[1],b[1])<=centre_y<=max(a[1],b[1]):
   t=(centre_y-a[1])/(b[1]-a[1]);centre_x=a[0]+(b[0]-a[0])*t
   angle=abs(math.degrees(math.atan2(b[0]-a[0],b[1]-a[1])));angle=min(angle,180-angle)
   record[label]={'centre':[centre_x,centre_y],'left_percent':centre_x/1024*100,'top_percent':top/1536*100,'angle':-side*angle}
   break
route=__import__('runpy').run_path(str(Path(__file__).resolve().parent/'strap_path.py'))
record['flag_motifs']={'texture_y':route['motif_positions'](),'texture_height':route['TEXTURE_HEIGHT'],'mapping':'physical arc length'}
(BASE/'catalogue-branding-calibration.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
