import os,runpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
os.environ['BOP_RENDER_MODE']='setup';g=runpy.run_path(str(Path(__file__).resolve().parent/'native-studio.py'));globals().update(g)
s.frame_set(6);bpy.context.view_layer.update()
def project(p):
 q=world_to_camera_view(s,c,p);return [q.x*s.render.resolution_x,(1-q.y)*s.render.resolution_y]
record={}
for side,label in [(-1,'greyhound'),(1,'leopard')]:
 path=[p for p in points if p.x*side>0 and p.z>.05];p=min(path,key=lambda p:abs(p.z-.118));i=points.index(p);a=project(points[max(0,i-1)]);b=project(points[min(len(points)-1,i+1)]);xy=project(p);width=.043*1024 if side<0 else .041*1024;height=width*(530/310 if side<0 else 615/355);angle=-math.degrees(math.atan2(b[0]-a[0],b[1]-a[1]));angle=angle if -90<angle<90 else angle+180 if angle<0 else angle-180
 record[label]={'centre':xy,'left_percent':xy[0]/1024*100,'top_percent':(xy[1]-height/2)/1536*100,'angle':angle}
left=[(i,p) for i,p in enumerate(points) if p.x<0 and p.z>.025];i,pnt=min(left,key=lambda pair:abs(project(pair[1])[1]-945));record['flag_motifs']={'path_v_left':i/(len(points)-1),'svg_y_left':(1-i/(len(points)-1))*4096,'svg_y_right':i/(len(points)-1)*4096,'left_pixel':project(pnt)}
(BASE/'catalogue-branding-calibration.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
