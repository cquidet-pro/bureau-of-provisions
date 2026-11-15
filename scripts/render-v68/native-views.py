"""Native V68 macro states, source-mesh section and station product layer."""
import os,runpy,json,math,random,bmesh
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
os.environ['BOP_RENDER_MODE']='setup'
g=runpy.run_path(str(Path(__file__).resolve().parent/'native-studio.py'));globals().update(g)
palette({'number':9,'body':'#f4f3ee','accent':'#f4f3ee'})
anchors=json.loads((BASE/'view-anchors.json').read_text()) if (BASE/'view-anchors.json').exists() else {}
PART=os.environ.get('BOP_VIEWS_PART','all')
def project(p):
 v=world_to_camera_view(s,c,Vector(p));width,height=(1536,1024) if s.render.resolution_x==4608 else (s.render.resolution_x,s.render.resolution_y);return [round(v.x*width,2),round((1-v.y)*height,2)]
def witnesses(name):
 bpy.context.view_layer.update();o=s.objects['11-Spray-dummy'];verts=[o.matrix_world@v.co for v in o.data.vertices];mx=max(v.x for v in verts);end=[v for v in verts if v.x>mx-.00005];tip=sum(end,Vector())/len(end)
 anchors[name]={'spray_outlet':project(tip),'spray_head':project((.003,.015,.209)),'straw_flat':project((-.012,.012,.198)),'straw_up':project((-.012,-.025,.213)),'gulp':project((.012,-.007,.2128)),'strap_left':project(min([p for p in points if p.x<0 and p.z>.05],key=lambda p:abs(p.z-.118))),'strap_right':project(min([p for p in points if p.x>0 and p.z>.05],key=lambda p:abs(p.z-.118))),'body_logo_top':project((0,-.0365,.140)),'rear_hinge':project((0,.0364,.2093))}
def render(name):
 s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True);print('FINISHED VIEW',name,flush=True)
# Same fixed photographic camera for both actual Blender straw poses.
s.render.resolution_x=1088;s.render.resolution_y=1445
camera((.024,-.24,.34),(0,0,.193),.125)
s.frame_set(24);witnesses('lid')
if PART=='all':render('lid-native-v68')
s.frame_set(48);witnesses('straw_up')
if PART=='all':render('straw-up-native-v68')
# Existing website gesture: same native spray mesh, translated for one press.
# This is an illustrative pump pose, not a new manufacturing mechanism.
s.frame_set(24);o=s.objects['11-Spray-dummy'];old=o.location.copy();o.location.z-=.002
if PART=='all':render('spray-pressed-native-v68')
o.location=old
# Station product is rendered as an alpha layer. The photographic clean plate
# is composited separately at Standard/0 exposure to retain its exact colours.
s.render.resolution_x=4608;s.render.resolution_y=3072;s.cycles.samples=128
camera((0,-.65,.35),(0,0,.141),.54);s.frame_set(48);witnesses('station')
cl.new(rl.outputs['Image'],comp.inputs[0])
if PART!='section':render('platform-product-native-v68')
cl.new(over.outputs[0],comp.inputs[0])
(BASE/'view-anchors.json').write_text(json.dumps(anchors,indent=2))
if PART=='hero':raise SystemExit
# Anatomy uses a literal section of the source body, not a generated housing.
s.render.resolution_x=1024;s.render.resolution_y=1536;s.cycles.samples=48
camera((.17,-.36,.29),(0,0,.139),.315);s.frame_set(48)
source=s.objects['01-Body'];inner=steel
# Inner material assignment changes finish only, never the source surface.
source.data.materials.append(inner);inneridx=len(source.data.materials)-1
for poly in source.data.polygons:
 centre=poly.center;normal=poly.normal
 if centre.x*normal.x+centre.y*normal.y<0:poly.material_index=inneridx
# Make an exact half-section copy with a plane cut; preserve the source mesh.
sectionmesh=source.data.copy();sectionmesh.transform(source.matrix_world)
bm=bmesh.new();bm.from_mesh(sectionmesh)
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0000001,plane_co=(0,0,0),plane_no=(1,0,0),clear_outer=True,clear_inner=False)
bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
bm.to_mesh(sectionmesh);bm.free();sectionmesh.update()
section=bpy.data.objects.new('WEB-Native-body-half-section',sectionmesh);s.collection.objects.link(section);source.hide_render=True
# Section the existing lower foot and body O-ring with the same plane. A
# literal half-cut must not leave complete rings floating in the removed half.
for lower_name in ['02-Foot','Axial O-ring · assembly pose','H02-Body-O-ring']:
 lower=s.objects.get(lower_name)
 if not lower or not lower.visible_get():continue
 me=lower.data.copy();me.transform(lower.matrix_world);bm=bmesh.new();bm.from_mesh(me);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0000001,plane_co=(0,0,0),plane_no=(1,0,0),clear_outer=True,clear_inner=False);bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0);bm.to_mesh(me);bm.free();me.update();copy=bpy.data.objects.new('WEB-Section-'+lower_name,me);s.collection.objects.link(copy);lower.hide_render=True
# The spray pickup lies entirely in the removed (+X) half. Leaving it
# visible projects a false steel edge through the open water section.
s.objects['20-Spray-pickup'].hide_render=True
# Derive water's curved lower boundary from the actual inside body profile.
bodymesh=source.data;worldverts=[source.matrix_world@v.co for v in bodymesh.vertices];profile=[]
for zi in range(1,126):
 z=zi*.001;rr=[]
 for edge in bodymesh.edges:
  a=worldverts[edge.vertices[0]];b=worldverts[edge.vertices[1]]
  if (a.z-z)*(b.z-z)<0:
   pnt=a+(b-a)*((z-a.z)/(b.z-a.z));rr.append(math.hypot(pnt.x,pnt.y))
 if rr and max(rr)-min(rr)>.0006:profile.append((z,max(0,min(rr)-.00005)))
waterverts=[];waterfaces=[];segments=96
if profile:
 for z,r in profile:
  for i in range(segments):a=2*math.pi*i/segments;waterverts.append((r*math.cos(a),r*math.sin(a),z))
 for j in range(1,len(profile)):
  for i in range(segments):n=(i+1)%segments;waterfaces.append(((j-1)*segments+i,(j-1)*segments+n,j*segments+n,j*segments+i))
 waterfaces.append(tuple(range(segments-1,-1,-1)));waterfaces.append(tuple((len(profile)-1)*segments+i for i in range(segments)))
 me=bpy.data.meshes.new('WEB-Continuous water to native floor');me.from_pydata(waterverts,[],waterfaces);me.update();w=bpy.data.objects.new('WEB-Continuous-water',me);s.collection.objects.link(w)
 wm=material('water',(.12,.55,.72),rough=.035);bs=wm.node_tree.nodes['Principled BSDF'];bs.inputs['Transmission Weight'].default_value=.88;bs.inputs['IOR'].default_value=1.333;w.data.materials.append(wm)
 for p in me.polygons:p.use_smooth=True
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0000001,plane_co=(0,0,0),plane_no=(1,0,0),clear_outer=True,clear_inner=False);bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0);bm.to_mesh(me);bm.free();me.update()
# Lift exact native lid parts as a group for the exploded illustration.
upper=['03-Fixed-cap','04-Hood','05-Button','08-Guide-floor','10-Safety-loop','11-Spray-dummy','13-Metal-mouthpiece','15-Silicone-coupler','17-Drink-seal','18-Vent-seal','19-Water-shoulder','H01-Hood-pin','H04-Hidden-pin-L','H04-Hidden-pin-R','21-Hidden-friction-L','21-Hidden-friction-R']
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
for name in upper:
 o=s.objects.get(name)
 if not o:continue
 ev=o.evaluated_get(dg);me=bpy.data.meshes.new_from_object(ev);me.transform(ev.matrix_world);copy=bpy.data.objects.new('WEB-Exploded-'+name,me);s.collection.objects.link(copy);copy.location.z=.024;o.hide_render=True
# Only this half-cut view uses a clean-ended single flat strap strip.
full=s.objects['WEB-One-continuous-strap'];full.hide_render=True
keep=len(points)//2-18;vs2=verts2=[];fs2=[]
for i in range(keep):vs2.extend([tuple(mesh.vertices[2*i].co),tuple(mesh.vertices[2*i+1].co)])
for i in range(1,keep):fs2.append((2*i-2,2*i-1,2*i+1,2*i))
me=bpy.data.meshes.new('WEB-Cut-strap');me.from_pydata(vs2,[],fs2);me.update();strap=bpy.data.objects.new('WEB-Flat-cut-strap',me);s.collection.objects.link(strap);strap.data.materials.append(cloth);uvl=me.uv_layers.new()
for po in me.polygons:
 for li in po.loop_indices:idx=me.loops[li].vertex_index;uvl.data[li].uv=(idx%2,(idx//2)/(len(points)-1))
for obj in s.objects:
 if obj.name.startswith(('WEB-round-opening-snap-jaw-1','WEB-snap-spring-gate-1','WEB-flat-snap-body-1','WEB-snap-trigger-lever-1','WEB-Snap-trigger-rivet-1','WEB-short-snap-swivel-1','WEB-Snap-swivel-collar-1','WEB-separate-D-ring-1','WEB-Folded-tab-1','WEB-tab-stitch-1')):obj.hide_render=True
witnesses('cutaway');render('bottle-cutaway-native-v68')
(BASE/'view-anchors.json').write_text(json.dumps(anchors,indent=2))
(BASE/'section-record.json').write_text(json.dumps({'body_source':'01-Body','section':'right half removed by plane cut of a copy, only in illustrative cutaway','lid_translation_mm':24,'removed_half_interior':['20-Spray-pickup'],'steel_boundary':'native body section edge; no pickup retained in removed positive-X half','water_profile_derived_from_source_edges':True,'water_floor_z_mm':profile[0][0]*1000 if profile else None,'water_top_z_mm':125,'straw_poses':{'flat':24,'up':48},'spray_press':'same native spray mesh translated 2mm for existing illustrative gesture; no additional mechanism'},indent=2))
