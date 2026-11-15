"""Render the authoritative V68 meshes without generative geometry changes.
Run inside a disposable background Blender process. Never saves the source file.
Website-only approved strap accessory is separate from all source objects.
"""
import bpy, math, json, hashlib, os
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(os.environ.get('BOP_ASSET_OUT',ROOT/'public/images/product'));OUT.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene;c=s.camera
BASE=Path(os.environ.get('BOP_EVIDENCE_OUT',ROOT/'output/design-v68/native'));BASE.mkdir(parents=True,exist_ok=True)
MODE=os.environ.get('BOP_RENDER_MODE','test')
# Fingerprint source geometry at the catalogue pose before appearance changes.
s.frame_set(6)
def fingerprint():
 dg=bpy.context.evaluated_depsgraph_get(); result={}
 for o in s.objects:
  if o.type!='MESH' or o.name.startswith('WEB-'):continue
  ev=o.evaluated_get(dg);mesh=ev.to_mesh();h=hashlib.sha256()
  for v in mesh.vertices:h.update(('%0.9f,%0.9f,%0.9f;' % tuple(ev.matrix_world@v.co)).encode())
  for p in mesh.polygons:h.update((','.join(map(str,p.vertices))+';').encode())
  result[o.name]=h.hexdigest();ev.to_mesh_clear()
 return result
before=fingerprint()
s.render.engine='CYCLES';s.cycles.samples=48 if MODE!='test' else 32;s.render.use_persistent_data=True;s.cycles.use_denoising=True
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
 for device in prefs.devices:device.use=device.type=='METAL'
 if any(d.type=='METAL' for d in prefs.devices):s.cycles.device='GPU'
 print('RENDER DEVICES',[(d.name,d.type,d.use) for d in prefs.devices],flush=True)
except Exception as exc:print('CPU rendering',str(exc),flush=True)
s.cycles.max_bounces=12;s.cycles.transmission_bounces=10;s.cycles.transparent_max_bounces=64;s.cycles.min_transparent_bounces=64
s.render.resolution_x=1024;s.render.resolution_y=1536;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=-2.9
for o in s.objects:
 if o.type=='LIGHT':o.hide_render=True
 if o.type=='MESH' and 'logo' in o.name.lower():o.hide_render=True
# Preserve all mesh surfaces; only shader finishes change.
for mat in bpy.data.materials:
 if not mat.use_nodes:continue
 for p in [n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED']:
  if 'stainless' in mat.name.lower() or mat.name=='Button · satin silver metal touch':p.inputs['Metallic'].default_value=1;p.inputs['Roughness'].default_value=.12;p.inputs['Base Color'].default_value=(.65,.69,.72,1)
  if mat.name=='Clear hood':p.inputs['Specular IOR Level'].default_value=0;p.inputs['Coat Weight'].default_value=0;p.inputs['Roughness'].default_value=.025;p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.46;p.inputs['Base Color'].default_value=(.97,.99,1,1)
  if mat.name=='Bureau cream':p.inputs['Roughness'].default_value=.42;p.inputs['Specular IOR Level'].default_value=.25
# Clear photographic lid: one unbent transmission path prevents doubled
# images of the drinking parts. A subtle grazing-angle tint keeps its rim
# and handle visible without reflecting studio lights or blurring the view.
hoodmat=bpy.data.materials['Clear hood'];hn=hoodmat.node_tree.nodes;hl=hoodmat.node_tree.links;hn.clear()
output=hn.new('ShaderNodeOutputMaterial');transmission=hn.new('ShaderNodeBsdfTransparent');transmission.name='WEB-Crisp clear lid transmission'
fresnel=hn.new('ShaderNodeFresnel');fresnel.inputs['IOR'].default_value=1.46
edge=hn.new('ShaderNodeMixRGB');edge.blend_type='MIX';edge.inputs[1].default_value=(.90,.92,.93,1);edge.inputs[2].default_value=(.60,.65,.70,1)
hl.new(fresnel.outputs[0],edge.inputs[0]);hl.new(edge.outputs[0],transmission.inputs['Color']);hl.new(transmission.outputs[0],output.inputs['Surface'])
s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.7,.68,.62,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.22
for name,loc,power,size in [('Key',(-.20,-.25,.37),9,.23),('Fill',(.18,-.12,.22),3,.18),('Rim',(.06,.18,.36),11,.20)]:
 d=bpy.data.lights.new('WEB-'+name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new('WEB-'+name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.13))-o.location).to_track_quat('-Z','Y').to_euler()
def material(name,color,metal=0,rough=.4):
 m=bpy.data.materials.new('WEB-'+name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
# A small dedicated strip gives the flat steel button a readable highlight.
d=bpy.data.lights.new('WEB-Button soft reflection strip','AREA');d.energy=.35;d.shape='RECTANGLE';d.size=.08;d.size_y=.16
lamp=bpy.data.objects.new('WEB-Button soft reflection strip',d);s.collection.objects.link(lamp);lamp.location=(-.035,-.30,.10);lamp.rotation_euler=(Vector((0,-.031,.194))-lamp.location).to_track_quat('-Z','Y').to_euler()
receiver=bpy.data.collections.new('WEB-Button reflection receiver');receiver.objects.link(s.objects['05-Button']);lamp.light_linking.receiver_collection=receiver
floor=material('ivory backdrop',(.66,.59,.48),rough=.8)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0002));o=bpy.context.object;o.name='WEB-Studio-floor';o.data.materials.append(floor);o.is_shadow_catcher=True
ng=bpy.data.node_groups.new('WEB-Studio composite','CompositorNodeTree');ng.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=ng;s.use_nodes=True;s.render.use_compositing=True;cn=ng.nodes;cl=ng.links;rl=cn.new('CompositorNodeRLayers');bg=cn.new('CompositorNodeRGB');bg.outputs[0].default_value=(6.76,6.32,5.51,1);over=cn.new('CompositorNodeAlphaOver');over.inputs['Factor'].default_value=1;cl.new(bg.outputs[0],over.inputs['Background']);cl.new(rl.outputs['Image'],over.inputs['Foreground']);comp=cn.new('NodeGroupOutput');cl.new(over.outputs[0],comp.inputs[0])
steel=material('strap polished steel',(.65,.69,.72),1,.12)
cloth=material('woven strap',(.75,.70,.60),rough=.68)
# An explicit UV ribbon keeps stripes on the same physical edge through the U.
route=__import__('runpy').run_path(str(Path(__file__).resolve().parent/'strap_path.py'));points=[Vector(p) for p in route['POINTS']];path_distances=route['DISTANCES'];path_length=route['LENGTH'];verts=[];uv=[];faces=[];edges=[[],[]]
for i,p in enumerate(points):
 t=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();w=Vector((0,-1,0)).cross(t).normalized()
 # Turn naturally onto the floor; keep one continuous band orientation.
 blend=max(0,min(1,(.025-p.z)/.02));floorw=Vector((0,1,0));w=(w*(1-blend)+floorw*blend).normalized()
 for side in (0,1):
  v=p+w*((side-.5)*.014);verts.append(tuple(v));uv.append((side,path_distances[i]/path_length));edges[side].append(tuple(v+Vector((0,-.00015,.00015))))
 if i:faces.append((2*i-2,2*i-1,2*i+1,2*i))
mesh=bpy.data.meshes.new('WEB-webbing');mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new('WEB-One-continuous-strap',mesh);s.collection.objects.link(ob);ob.data.materials.append(cloth)
uvlayer=mesh.uv_layers.new(name='UVMap')
for poly in mesh.polygons:
 poly.use_smooth=True
 for li in poly.loop_indices:uvlayer.data[li].uv=uv[mesh.loops[li].vertex_index]
sol=ob.modifiers.new('Woven fabric thickness','SOLIDIFY');sol.thickness=.00055;sol.offset=0
bev=ob.modifiers.new('Tidy textile edges','BEVEL');bev.width=.0002;bev.segments=2
# Fine UV warp/weft bump, shader only, never a raised jacquard geometry.
nt=cloth.node_tree;nodes=nt.nodes;links=nt.links;p=nodes['Principled BSDF'];tex=nodes.new('ShaderNodeTexCoord');sep=nodes.new('ShaderNodeSeparateXYZ');links.new(tex.outputs['UV'],sep.inputs[0]);weaves=[]
for axis,freq in [('X',125),('Y',4000)]:
 mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=freq;links.new(sep.outputs[axis],mul.inputs[0]);si=nodes.new('ShaderNodeMath');si.operation='SINE';links.new(mul.outputs[0],si.inputs[0]);weaves.append(si)
add=nodes.new('ShaderNodeMath');add.operation='ADD';links.new(weaves[0].outputs[0],add.inputs[0]);links.new(weaves[1].outputs[0],add.inputs[1]);bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.000055;links.new(add.outputs[0],bump.inputs['Height']);links.new(bump.outputs[0],p.inputs['Normal'])
def tube(name,coords,radius=.0006,mat=steel,closed=False):
 cu=bpy.data.curves.new('WEB-'+name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=radius;cu.bevel_resolution=3;cu.use_fill_caps=True;sp=cu.splines.new('POLY');sp.points.add(len(coords)-1)
 for v,co in zip(sp.points,coords):v.co=(*co,1)
 sp.use_cyclic_u=closed;ob=bpy.data.objects.new('WEB-'+name,cu);s.collection.objects.link(ob);ob.data.materials.append(mat);return ob
# Existing approved detachable-strap concept, attached inside the actual body
# recesses. No external lug is added to the collar or to the body mesh.
for side in (-1,1):
 # User's 15 November snap-hook reference: round opening jaw, broad flat
 # trigger body, visible small lever and short swivel; never a wire oval.
 jaw=Vector((side*.0327,-.001,.16395));axis=Vector((side*.0143,0,-.00695)).normalized();across=Vector((side*.00695,0,.0143)).normalized()
 def hookpoint(u,v,y=0):return jaw+axis*u+across*v+Vector((0,y,0))
 radius=.0035;gap=.65
 coords=[tuple(hookpoint(radius*math.cos(gap+(2*math.pi-2*gap)*i/64),radius*math.sin(gap+(2*math.pi-2*gap)*i/64))) for i in range(65)]
 tube('round-opening-snap-jaw-'+str(side),coords,.00045)
 tube('snap-spring-gate-'+str(side),[tuple(hookpoint(radius*math.cos(gap),-radius*math.sin(gap))),tuple(hookpoint(radius*math.cos(gap),radius*math.sin(gap)))],.00035)
 def plate(name,outline,thickness=.0013):
  vs=[tuple(hookpoint(u,v,y+(-.00065 if "trigger-lever" in name else 0))) for y in (-thickness/2,thickness/2) for u,v in outline];count=len(outline);fs=[tuple(range(count-1,-1,-1)),tuple(count+i for i in range(count))]
  for i in range(count):j=(i+1)%count;fs.append((i,j,count+j,count+i))
  me=bpy.data.meshes.new('WEB-'+name);me.from_pydata(vs,[],fs);me.update();obj=bpy.data.objects.new('WEB-'+name,me);s.collection.objects.link(obj);obj.data.materials.append(steel);be=obj.modifiers.new('Snap casting edge radius','BEVEL');be.width=.00012 if "trigger-lever" in name else .0003;be.segments=5
  return obj
 plate('flat-snap-body-'+str(side),[(.002786,-.002118),(.0038,-.0022),(.0075,-.0021),(.0106,-.00165),(.0124,-.00085),(.0124,.00085),(.0105,.0017),(.0062,.0023),(.0036,.00215),(.002786,.002118)])
 plate('snap-trigger-lever-'+str(side),[(u,-v) for u,v in [(.0035,-.00155),(.00445,-.00175),(.00515,-.0023),(.0055,-.0032),(.0055,-.00425),(.00525,-.0046),(.00465,-.0046),(.00445,-.0042),(.00445,-.0031),(.00415,-.00265),(.0035,-.0024)]],.0009)
 rivet=hookpoint(.0080,0,-.00075);bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.00055,depth=.0004,location=rivet,rotation=(math.pi/2,0,0));rv=bpy.context.object;rv.name='WEB-Snap-trigger-rivet-'+str(side);rv.data.materials.append(steel)
 stem_start=hookpoint(.0124,0);stem_end=Vector((side*.047,-.001,.157));tube('short-snap-swivel-'+str(side),[tuple(stem_start),tuple(stem_end)],.00065)
 middle=stem_start.lerp(stem_end,.56);bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.0011,depth=.0014,location=middle);sw=bpy.context.object;sw.name='WEB-Snap-swivel-collar-'+str(side);sw.rotation_euler=(stem_end-stem_start).to_track_quat('Z','Y').to_euler();sw.data.materials.append(steel)
 # Separate rounded rectangular D ring with 14 mm fabric opening.
 cx=side*.047;coords=[]
 for ox,oz,start in [(.006,.001,math.pi/2),(.006,-.002,0),(-.006,-.002,-math.pi/2),(-.006,.001,-math.pi)]:
  for k in range(11):
   a=start-(math.pi/2)*k/10;coords.append((cx+ox+.002*math.cos(a),-.001,.154+oz+.002*math.sin(a)))
 tube('separate-D-ring-'+str(side),coords,.00065,closed=True)
 # Slim folded same-fabric tabs and fine rectangular stitching, below D rings.
 bpy.ops.mesh.primitive_cube_add(size=1,location=(side*.0485,-.0013,.14325));tab=bpy.context.object;tab.name='WEB-Folded-tab-'+str(side);tab.dimensions=(.014,.0022,.0175);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);tab.data.materials.append(cloth);tab.rotation_euler.y=-side*math.atan(.003/.0175);bpy.context.view_layer.update()
 for loop in tab.data.uv_layers.active.data:loop.uv.y*=.025
 be=tab.modifiers.new('Soft fabric fold','BEVEL');be.width=.0005;be.segments=3
 thread=material('ivory sewing thread '+str(side),(.65,.61,.54),rough=.85)
 tube('tab-stitch-'+str(side),[tuple(tab.matrix_world@Vector((u,-.00125,v))) for u,v in [(-.0058,.0065),(.0058,.0065),(.0058,-.0065),(-.0058,-.0065)]],.00012,thread,closed=True)
# Subtle visual registration of the existing cap/body interface, not a gasket.
seammat=material('cap body joint shadow',(.055,.055,.052),rough=.8)
tube('cap-body-interface',[(.03023077*math.cos(i*2*math.pi/192),.03023077*math.sin(i*2*math.pi/192),.1795) for i in range(192)],.00007,seammat,closed=True)
# Camera is fixed for all editions; source model is never rescaled.
def camera(pos,target,scale):
 c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.ortho_scale=scale
def front_camera(pos,target,scale):
 assert abs(pos[0])<1e-9 and abs(target[0])<1e-9,'Non-cutaway views must face the native front without horizontal rotation'
 camera(pos,target,scale)
 record_path=BASE/'front-camera-record.json'
 records=json.loads(record_path.read_text()) if record_path.exists() else {}
 name={.127:'catalogue',.218:'lid',.1635:'main_scene'}.get(target[2],str(target[2]))
 records[name]={'position_m':pos,'target_m':target,'horizontal_view_degrees':0,'orthographic_scale_m':scale}
 record_path.write_text(json.dumps(records,indent=2)+'\n')
front_camera((0,-.433503,.29),(0,0,.127),.30)
# Appearance-only colourways. Hex values converted from display sRGB.
def rgb(h):
 vals=[int(h[i:i+2],16)/255 for i in (1,3,5)];return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals)
bodymat=bpy.data.materials['Bureau cream'];capmat=bodymat.copy();capmat.name='WEB-Collar coating'
for name in ['03-Fixed-cap','10-Safety-loop','05-Button']:
 o=s.objects[name]
 for slot in o.material_slots:
  if slot.material==bodymat:slot.material=capmat
# The long webbing colour/pattern is represented by a vector-authored strip texture.
def palette(e):
 bpy.data.materials['Cream silicone foot'].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*rgb(e['body'] if e['number']==10 else '#f4f3ee'),1)
 bodymat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*rgb(e['body']),1);capmat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*rgb(e['accent']),1)
 p.inputs['Base Color'].default_value=(*rgb(e['accent']),1)
 # Canada's folded tabs stay plain ivory, including the upper fold surface.
 for ob in s.objects:
  if ob.name.startswith('WEB-Folded-tab'):
   if e['number']==27:
    tabmat=bpy.data.materials.get('WEB-Canada plain ivory fold')
    if tabmat is None:
     tabmat=cloth.copy();tabmat.name='WEB-Canada plain ivory fold';bs=tabmat.node_tree.nodes['Principled BSDF']
     for link in list(bs.inputs['Base Color'].links):tabmat.node_tree.links.remove(link)
     bs.inputs['Base Color'].default_value=(*rgb('#f4f3ee'),1)
    ob.data.materials[0]=tabmat
   else:ob.data.materials[0]=cloth
 texpath=ROOT/'design/v68-strap-textures'/f"edition-{e['number']:02}.png"
 if texpath.exists():
  im=nodes.get('Edition textile texture') or nodes.new('ShaderNodeTexImage');im.name='Edition textile texture';im.image=bpy.data.images.load(str(texpath),check_existing=True);links.new(tex.outputs['UV'],im.inputs['Vector']);shade=nodes.get('Weave shade') or nodes.new('ShaderNodeMath');shade.name='Weave shade';shade.operation='MULTIPLY_ADD';shade.inputs[1].default_value=.06;shade.inputs[2].default_value=.88;links.new(add.outputs[0],shade.inputs[0]);mix=nodes.get('Woven albedo') or nodes.new('ShaderNodeMixRGB');mix.name='Woven albedo';mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;links.new(im.outputs['Color'],mix.inputs[1]);links.new(shade.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],p.inputs['Base Color'])
# Camera/mesh witness for all final renders.
if MODE=='test':
 s.render.resolution_x=512;s.render.resolution_y=768;s.cycles.samples=16;palette({'number':2,'body':'#31539b','accent':'#f4c84f'});s.render.filepath=str(BASE/'studio-native-test.png');bpy.ops.render.render(write_still=True)
elif MODE=='catalogue':
 editions=json.loads((ROOT/'design/product-design.json').read_text())['editions']
 for e in editions:
  if os.environ.get('BOP_EDITION_IDS') and str(e['number']) not in os.environ['BOP_EDITION_IDS'].split(','):continue
  palette(e);s.render.filepath=str(OUT/f"edition-{e['number']:02}-native-v68.png");bpy.ops.render.render(write_still=True);print('FINISHED',e['number'],flush=True)
s.frame_set(6);after=fingerprint();assert before==after,'Source geometry changed during photographic rendering'
(BASE/'source-geometry-integrity.json').write_text(json.dumps({'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'before':before,'after':after,'unchanged':before==after,'website_accessory_prefix':'WEB-','catalogue_frame':6},indent=2))
