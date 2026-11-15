"""Native V68 macro states, source-mesh section and station product layer."""
import os,runpy,json,math,random,bmesh
from pathlib import Path
from contextlib import contextmanager
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
@contextmanager
def lid_pose(degrees=90):
 originals=[s.objects[n] for n in ['04-Hood','17-Drink-seal','18-Vent-seal']];copies={};visibility={o.name:o.hide_render for o in originals}
 try:
  for original in originals:
   copy=original.copy();copy.data=original.data.copy();copy.animation_data_clear();copy.name='WEB-Photographic-pose-'+original.name;copy.rotation_euler.x=-math.radians(degrees);s.collection.objects.link(copy);original.hide_render=True;copies[original.name]=copy
  bpy.context.view_layer.update();yield copies
 finally:
  for original in originals:original.hide_render=visibility[original.name]
  for copy in copies.values():bpy.data.objects.remove(copy,do_unlink=True)
def render(name):
 if os.environ.get('BOP_QUICK_PROOF')=='1':
  assert OUT.resolve()!=(ROOT/'public/images/product').resolve(),'Quick proof cannot overwrite production masters'
  s.render.resolution_percentage=40;s.cycles.samples=16
 s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True);print('FINISHED VIEW',name,flush=True)
def render_open(name):
 with lid_pose():render(name)
# Same fixed photographic camera for both actual Blender straw poses.
s.render.resolution_x=1088;s.render.resolution_y=1445
front_camera((0,-.241197,.365),(0,0,.218),.205)
s.frame_set(24);witnesses('lid')
if PART in ('all','macro'):
 s.frame_set(6);render('lid-closed-native-v68');s.frame_set(24);render_open('lid-native-v68')
s.frame_set(48);witnesses('straw_up')
if PART in ('all','macro'):render_open('straw-up-native-v68')
# Existing website gesture: same native spray mesh, translated for one press.
# This is an illustrative pump pose, not a new manufacturing mechanism.
s.frame_set(24);o=s.objects['11-Spray-dummy'];old=o.location.copy();o.location.z-=.002
if PART in ('all','macro'):render_open('spray-pressed-native-v68')
o.location=old
# Station product is rendered as an alpha layer. The photographic clean plate
# is composited separately at Standard/0 exposure to retain its exact colours.
s.render.resolution_x=4608;s.render.resolution_y=3072;s.cycles.samples=128
front_camera((0,-.65,.22037),(0,0,.1635),.58);s.frame_set(48)
with lid_pose() as main_pose:
 # Darker main-scene glazing; the native centred handle stays unmodified.
 main_glass=hoodmat.copy();main_glass.name='WEB-Main scene dark smoke';mix=next(n for n in main_glass.node_tree.nodes if n.bl_idname=='ShaderNodeMixRGB');mix.inputs[1].default_value=(.78,.80,.82,1);mix.inputs[2].default_value=(.40,.44,.48,1);main_pose['04-Hood'].data.materials[0]=main_glass
 witnesses('station');cl.new(rl.outputs['Image'],comp.inputs[0])
 if PART in ('all','hero'):render('platform-product-native-v68')
cl.new(over.outputs[0],comp.inputs[0])
(BASE/'view-anchors.json').write_text(json.dumps(anchors,indent=2))
s.frame_set(48)
if PART in ('hero','macro'):raise SystemExit
# Anatomy uses a literal section of the source body, not a generated housing.
s.render.resolution_x=1024;s.render.resolution_y=1536;s.cycles.samples=48
camera((.17,-.36,.308),(0,0,.157),.365);s.frame_set(48)
CUT_NORMAL=Vector((math.cos(math.radians(7)),-math.sin(math.radians(7)),0));CUT_TANGENT=Vector((math.sin(math.radians(7)),math.cos(math.radians(7)),0))
source=s.objects['01-Body'];inner=steel
# Inner material assignment changes finish only, never the source surface.
source.data.materials.append(inner);inneridx=len(source.data.materials)-1
for poly in source.data.polygons:
 centre=poly.center;normal=poly.normal
 if centre.x*normal.x+centre.y*normal.y<0:poly.material_index=inneridx
# Make an exact half-section copy with a plane cut; preserve the source mesh.
sectionmesh=source.data.copy();sectionmesh.transform(source.matrix_world)
bm=bmesh.new();bm.from_mesh(sectionmesh)
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0000001,plane_co=(0,0,0),plane_no=CUT_NORMAL,clear_outer=True,clear_inner=False)
cutfaces=bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)['faces']
for face in cutfaces:face.material_index=inneridx
bm.to_mesh(sectionmesh);bm.free();sectionmesh.update()
section=bpy.data.objects.new('WEB-Native-body-half-section',sectionmesh);s.collection.objects.link(section);source.hide_render=True
# Section the existing lower foot and body O-ring with the same plane. A
# literal half-cut must not leave complete rings floating in the removed half.
for lower_name in ['02-Foot','Axial O-ring · assembly pose','H02-Body-O-ring']:
 lower=s.objects.get(lower_name)
 if not lower or not lower.visible_get():continue
 me=lower.data.copy();me.transform(lower.matrix_world);bm=bmesh.new();bm.from_mesh(me);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0000001,plane_co=(0,0,0),plane_no=CUT_NORMAL,clear_outer=True,clear_inner=False);bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0);bm.to_mesh(me);bm.free();me.update();copy=bpy.data.objects.new('WEB-Section-'+lower_name,me);s.collection.objects.link(copy);lower.hide_render=True
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
 wm=material('water',(.56,.83,.94),rough=.035);bs=wm.node_tree.nodes['Principled BSDF'];bs.inputs['Transmission Weight'].default_value=1.0;bs.inputs['IOR'].default_value=1.333;w.data.materials.append(wm)
 # Mix a clear cut-face treatment for diagram legibility, retaining water
 # reflections without hiding the native steel pickup behind refraction.
 transparent=wm.node_tree.nodes.new('ShaderNodeBsdfTransparent');transparent.inputs[0].default_value=(.8,.94,1,1);watermix=wm.node_tree.nodes.new('ShaderNodeMixShader');watermix.inputs[0].default_value=.65;wm.node_tree.links.new(bs.outputs[0],watermix.inputs[1]);wm.node_tree.links.new(transparent.outputs[0],watermix.inputs[2]);wm.node_tree.links.new(watermix.outputs[0],wm.node_tree.nodes['Material Output'].inputs['Surface'])
 for p in me.polygons:p.use_smooth=True
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0000001,plane_co=(0,0,0),plane_no=CUT_NORMAL,clear_outer=True,clear_inner=False);bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0);bm.to_mesh(me);bm.free();me.update()
# Lift exact native lid parts as a group for the exploded illustration.
upper=['WEB-cap-body-interface','03-Fixed-cap','04-Hood','05-Button','08-Guide-floor','10-Safety-loop','11-Spray-dummy','12-Metal-pickup','13-Metal-mouthpiece','15-Silicone-coupler','17-Drink-seal','18-Vent-seal','19-Water-shoulder','H01-Hood-pin','H04-Hidden-pin-L','H04-Hidden-pin-R','21-Hidden-friction-L','21-Hidden-friction-R']
with lid_pose() as posed:
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 for name in upper:
  o=posed.get(name) or s.objects.get(name)
  if not o:continue
  ev=o.evaluated_get(dg);me=bpy.data.meshes.new_from_object(ev);me.transform(ev.matrix_world)
  if name in ['19-Water-shoulder','15-Silicone-coupler']:
   # The latest illustration keeps only the metallic connector below the cap.
   bm=bmesh.new();bm.from_mesh(me);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,.1795),plane_no=(0,0,1),clear_inner=True,clear_outer=False);bm.to_mesh(me);bm.free();me.update()
  if name=='12-Metal-pickup':
   # Continue the same native tube section into the deck; hide the exposed
   # white socket in this illustration instead of leaving a white collar.
   bm=bmesh.new();bm.from_mesh(me);top=max(v.co.z for v in bm.verts)
   for vertex in bm.verts:
    if abs(vertex.co.z-top)<1e-6:vertex.co.z=.1796
   bm.to_mesh(me);bm.free();me.update()
   me.materials.clear();me.materials.append(steel)
   for polygon in me.polygons:polygon.use_smooth=True
  copy=bpy.data.objects.new('WEB-Exploded-'+name,me);s.collection.objects.link(copy);copy.location.z=.034
for name in upper:
 if s.objects.get(name):s.objects[name].hide_render=True
# Cut-face material key: bright steel skins and a dark insulation gap. The
# band follows the native inner/outer profiles; it is not a new exterior wall.
void=material('section vacuum gap',(.012,.016,.02),rough=1)
gapverts=[];gapfaces=[];gap_profile=[]
for zi in range(12,175):
 z=zi*.001;rr=[]
 for edge in source.data.edges:
  a,b=(source.matrix_world@source.data.vertices[i].co for i in edge.vertices)
  if (a.z-z)*(b.z-z)<0:
   q=a+(b-a)*((z-a.z)/(b.z-a.z));rr.append(math.hypot(q.x,q.y))
 if rr and max(rr)-min(rr)>.0011:gap_profile.append((z,max(min(rr)+.0004,max(rr)-.0017),max(rr)-.0004))
for side in (-1,1):
 start=len(gapverts)
 for z,ri,ro in gap_profile:
  for r in (ri,ro):gapverts.append(tuple(CUT_TANGENT*(side*r)+CUT_NORMAL*.000035+Vector((0,0,z))))
 for j in range(1,len(gap_profile)):a=start+2*j;gapfaces.append((a-2,a-1,a+1,a))
# The base section uses the same dark material between its steel skins.
for y,z in [(-.030,.004),(.030,.004),(.030,.0052),(-.030,.0052)]:gapverts.append(tuple(CUT_TANGENT*y+CUT_NORMAL*.000035+Vector((0,0,z))))
gapfaces.append(tuple(range(len(gapverts)-4,len(gapverts))))
me=bpy.data.meshes.new('WEB-Insulation-gap-cut-face');me.from_pydata(gapverts,[],gapfaces);me.materials.append(void);obj=bpy.data.objects.new('WEB-Insulation-gap-cut-face',me);s.collection.objects.link(obj)
# Latest explicit user request: restore a matching visible steel screw
# connection in this illustrative anatomy view. These WEB-only threads are
# not represented as native V68 machining or a manufacturing specification.
def annulus(name,outer,inner,z0,z1):
 vs=[];fs=[];N=128
 for z,r in [(z0,outer),(z1,outer),(z0,inner),(z1,inner)]:
  for i in range(N):a=i*2*math.pi/N;vs.append((r*math.cos(a),r*math.sin(a),z))
 for i in range(N):j=(i+1)%N;fs.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 me=bpy.data.meshes.new('WEB-'+name);me.from_pydata(vs,[],fs);me.materials.append(steel);o=bpy.data.objects.new('WEB-'+name,me);s.collection.objects.link(o)
 for f in me.polygons:f.use_smooth=True
annulus('Illustrative-steel-thread-sleeve',.0225,.0212,.2045,.2135)
for name,z0,half in [('Illustrative-male-thread',.2053,False),('Illustrative-female-thread',.1708,True)]:
 coords=[];groups=[]
 for i in range(1009):
  angle=i/1008*7*math.pi;q=Vector((.0228*math.cos(angle),.0228*math.sin(angle),z0+i/1008*.0063))
  if not half or q.dot(CUT_NORMAL)<=0:coords.append(tuple(q))
  elif coords:groups.append(coords);coords=[]
 if coords:groups.append(coords)
 for j,group in enumerate(groups):
  if len(group)>1:tube(name+'-'+str(j),group,.0004)

# Only this half-cut view uses a clean-ended single flat strap strip.
full=s.objects['WEB-One-continuous-strap'];full.hide_render=True
keep=len(points)//2-18;vs2=verts2=[];fs2=[]
for i in range(keep):vs2.extend([tuple(mesh.vertices[2*i].co),tuple(mesh.vertices[2*i+1].co)])
for i in range(1,keep):fs2.append((2*i-2,2*i-1,2*i+1,2*i))
me=bpy.data.meshes.new('WEB-Cut-strap');me.from_pydata(vs2,[],fs2);me.update();strap=bpy.data.objects.new('WEB-Flat-cut-strap',me);s.collection.objects.link(strap);strap.data.materials.append(cloth);uvl=me.uv_layers.new()
for po in me.polygons:
 for li in po.loop_indices:idx=me.loops[li].vertex_index;uvl.data[li].uv=(idx%2,path_distances[idx//2]/path_length)
for obj in s.objects:
 if obj.name.startswith(('WEB-round-opening-snap-jaw-1','WEB-snap-spring-gate-1','WEB-flat-snap-body-1','WEB-snap-trigger-lever-1','WEB-Snap-trigger-rivet-1','WEB-short-snap-swivel-1','WEB-Snap-swivel-collar-1','WEB-separate-D-ring-1','WEB-Folded-tab-1','WEB-tab-stitch-1')):obj.hide_render=True
# The pickup belongs to the lifted deck assembly, with its original overlap
# into the silicone coupler; it must not remain as a body-fixed duplicate.
bpy.context.view_layer.update()
def bounds_world(obj):
 vv=[obj.matrix_world@v.co for v in obj.data.vertices]
 return [[min(p[i] for p in vv) for i in range(3)],[max(p[i] for p in vv) for i in range(3)]]
pickup=s.objects['WEB-Exploded-12-Metal-pickup'];coupler=s.objects['WEB-Exploded-15-Silicone-coupler'];pb=bounds_world(pickup);cb=bounds_world(coupler)
assert abs(pickup.location.z-.034)<1e-7 and abs(coupler.location.z-.034)<1e-7
assert all(min(pb[1][i],cb[1][i])>max(pb[0][i],cb[0][i]) for i in range(3)),'Metallic pickup must reach its hidden deck socket'
assert s.objects['12-Metal-pickup'].hide_render and s.objects.get('WEB-Section-native-metal-pickup') is None
cap_bottom=bounds_world(s.objects['WEB-Exploded-03-Fixed-cap'])[0][2]
assert bounds_world(s.objects['WEB-Exploded-19-Water-shoulder'])[0][2]>=cap_bottom-1e-6,'No extra white thread projection below the cap'
assert abs(bounds_world(s.objects['WEB-Illustrative-steel-thread-sleeve'])[1][2]-cap_bottom)<1e-6
# The exploded button is a new object: light linking does not follow its
# source. Include it explicitly and place the reflection strip opposite the
# oblique camera so the polished face reads as steel in this view too.
button=s.objects['WEB-Exploded-05-Button']
receiver.objects.link(button)
lamp.location=(-.17,-.30,.15)
button_target=Vector((0,-.031,.228))
lamp.rotation_euler=(button_target-lamp.location).to_track_quat('-Z','Y').to_euler()
witnesses('cutaway');render('bottle-cutaway-native-v68')
(BASE/'view-anchors.json').write_text(json.dumps(anchors,indent=2))
(BASE/'section-record.json').write_text(json.dumps({'body_source':'01-Body','section':'right half removed by plane cut of a copy, only in illustrative cutaway','lid_translation_mm':34,'open_lid_pose_degrees':90,'pickup_attachment':'12-Metal-pickup lifted with upper deck by the same 34 mm; metallic continuation reaches hidden socket; no body-fixed duplicate','connector':'metallic thread only; plastic neck projection trimmed in illustration','removed_half_interior':['20-Spray-pickup'],'steel_boundary':'native body section edge; no pickup retained in removed positive-X half','water_profile_derived_from_source_edges':True,'water_floor_z_mm':profile[0][0]*1000 if profile else None,'water_top_z_mm':125,'straw_poses':{'flat':24,'up':48},'spray_press':'same native spray mesh translated 2mm for existing illustrative gesture; no additional mechanism'},indent=2))
