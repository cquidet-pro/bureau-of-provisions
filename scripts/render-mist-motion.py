import bpy, math, sys, json, shutil
from mathutils import Vector
from pathlib import Path

def prepare():
 s=bpy.data.scenes['Combo lid • close view'];bpy.context.window.scene=s;s.frame_set(14)
 from pathlib import Path
 texture_root=Path('/Users/cedric/code/water-bottle-design/output/archive/2026-10-11-bottle-cleanup/waterbottle')
 for mat in bpy.data.materials:
  if mat.node_tree:
   for node in mat.node_tree.nodes:
    if node.type=='TEX_IMAGE' and node.image:
     path=texture_root/Path(node.image.filepath).name
     if path.exists():node.image=bpy.data.images.load(str(path),check_existing=False)
 cam=s.camera;cam.location=(.10,-.22,.29);target=Vector((0,0,.212));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.11
 s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.film_transparent=False
 s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
 s.world=bpy.data.worlds.new('Animation warm studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.62,.53,.39,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4
 for m in bpy.data.materials:
  if not m.node_tree:continue
  p=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
  if not p:continue
  if 'copolyester' in m.name.lower():
   p.inputs['Base Color'].default_value=(.96,.96,.96,1);p.inputs['Roughness'].default_value=.035;p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.46;p.inputs['Specular IOR Level'].default_value=0
   transparent=m.node_tree.nodes.new('ShaderNodeBsdfTransparent')
   mix=m.node_tree.nodes.new('ShaderNodeMixShader')
   fresnel=m.node_tree.nodes.new('ShaderNodeFresnel');fresnel.inputs['IOR'].default_value=1.46
   weight=m.node_tree.nodes.new('ShaderNodeMath');weight.operation='POWER';weight.inputs[1].default_value=2
   soften=m.node_tree.nodes.new('ShaderNodeMath');soften.operation='MULTIPLY';soften.inputs[1].default_value=.25
   m.node_tree.links.new(weight.outputs[0],soften.inputs[0])
   m.node_tree.links.new(fresnel.outputs[0],weight.inputs[0]);m.node_tree.links.new(soften.outputs[0],mix.inputs[0])
   m.node_tree.links.new(transparent.outputs[0],mix.inputs[1]);m.node_tree.links.new(p.outputs[0],mix.inputs[2])
   output=next(n for n in m.node_tree.nodes if n.type=='OUTPUT_MATERIAL')
   m.node_tree.links.new(mix.outputs[0],output.inputs['Surface'])
  elif 'Cream • exterior' in m.name or 'Warm cream • powder' in m.name:
   p.inputs['Base Color'].default_value=(.72,.63,.47,1);p.inputs['Roughness'].default_value=.32
  elif 'stainless' in m.name.lower():
   p.inputs['Base Color'].default_value=(.55,.57,.59,1);p.inputs['Metallic'].default_value=1;p.inputs['Roughness'].default_value=.22
  elif 'Food-contact' in m.name:
   p.inputs['Base Color'].default_value=(.24,.25,.23,1);p.inputs['Roughness'].default_value=.5
 for v in s.view_layers:v.material_override=None
 for o in bpy.data.objects:
  if 'long shoulder strap' in o.name.lower():o.hide_render=True
  if o.type=='LIGHT':o.hide_render=True
 for name,loc,power,size in [('Key',(-.12,-.15,.36),7,.12),('Rim',(.1,.07,.30),10,.09),('Fill',(.1,-.2,.16),1,.15)]:
  d=bpy.data.lights.new(name,'AREA');d.energy=power*.12;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.visible_glossy=False;o.visible_transmission=False;o.location=loc;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
 # A softly mottled limestone backdrop, separate from the product geometry.
 bpy.ops.mesh.primitive_plane_add(size=2, location=(0,.10,.22), rotation=(math.pi/2,0,0))
 back=bpy.context.object;back.name='Web animation • limestone backdrop'
 # Operators may link to the active scene; keep it in this render scene.
 m=bpy.data.materials.new('Web animation • warm limestone');m.use_nodes=True
 n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.9
 tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=32;tex.inputs['Detail'].default_value=3
 r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.43,.32,.20,1);r.color_ramp.elements[1].color=(.78,.67,.49,1)
 m.node_tree.links.new(tex.outputs['Fac'],r.inputs[0]);m.node_tree.links.new(r.outputs['Color'],p.inputs['Base Color']);back.data.materials.append(m)
 return s

root=Path('/Users/cedric/code/water-bottle-design/output/waterbottle')
out=Path('/private/tmp/bop-lid-motion-spray45-beige');out.mkdir(exist_ok=True)
models=[('original','waterbottle.blend')]
metadata={}
for slug,name in models:
 bpy.ops.wm.open_mainfile(filepath=str(root/name))
 scene=prepare()
 # Camera orbit +45 degrees is equivalent to turning the bottle clockwise 45 degrees.
 from mathutils import Matrix
 # Orbit the studio with the camera so the backdrop and light balance match the other cards.
 orbit=Matrix.Rotation(math.radians(45),4,'Z')
 for studio_object in list(scene.objects):
  if studio_object.type=='LIGHT' and not studio_object.hide_render or studio_object.name=='Web animation • limestone backdrop':
   studio_object.matrix_world=orbit@studio_object.matrix_world
 scene.camera.location=Matrix.Rotation(math.radians(45),4,'Z')@scene.camera.location
 scene.camera.location.z=.26
 target=Vector((0,0,.195));scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
 scene.camera.data.ortho_scale=.12
 straw=bpy.data.objects['STRAW • fold X to -90 degrees'];straw.animation_data_clear()
 hood=next(o for o in scene.objects if o.name.startswith('V20 • rear hinge axis'));hood.animation_data_clear();hood.rotation_euler.x=math.radians(-112)
 droplets=[]
 if slug=='original':
  droplets=[o for o in bpy.data.scenes['V34 • spray animation'].objects if o.name.startswith('V34 • water mist')]
  for o in droplets:
   if o.name not in scene.objects:scene.collection.objects.link(o)
 # Clear water with specular highlights, rather than emissive white dots.
 water=bpy.data.materials.new('Web spray • clear water');water.use_nodes=True
 shader=water.node_tree.nodes.get('Principled BSDF')
 shader.inputs['Base Color'].default_value=(.88,.96,1,1)
 shader.inputs['Roughness'].default_value=.025;shader.inputs['IOR'].default_value=1.333
 shader.inputs['Transmission Weight'].default_value=.9
 for drop in droplets:
  drop.data.materials.clear();drop.data.materials.append(water)
 # Additional linked water beads make the fine spray legible at card size.
 import random
 rng=random.Random(43);water_copies=[]
 for drop in droplets:
  for _ in range(4):
   copy=drop.copy();copy.animation_data_clear();scene.collection.objects.link(copy)
   offset=Vector((rng.uniform(-.001,.001),rng.uniform(-.002,.002),rng.uniform(-.0015,.0015)))
   water_copies.append((drop,copy,offset))
 jets=[]
 for j in range(4):
  curve=bpy.data.curves.new(f'Web spray • water filament {j}','CURVE');curve.dimensions='3D';curve.bevel_depth=.00007;curve.bevel_resolution=2
  spline=curve.splines.new('POLY');spline.points.add(3)
  ob=bpy.data.objects.new(curve.name,curve);scene.collection.objects.link(ob);curve.materials.append(water)
  jets.append((ob,spline,j))
 count=60 if slug=='original' else 46
 dest=out/slug;dest.mkdir(exist_ok=True)
 metadata[slug]={'frames':count,'source':name,'strawEnd':45, 'startAngle':45, 'endAngle':180,'annotations':{}}
 for i in ([57] if '--proof' in sys.argv else range(count)):
  scene.frame_set(14 if i<=45 else 60+(i-45)*2)
  straw.rotation_euler.x=math.radians(45-3*min(i,45))
  hood.rotation_euler.x=math.radians(-112)
  for o in droplets:
   o.hide_render=i<=45
   o.scale*=1.8
  for source,copy,offset in water_copies:
   copy.location=source.location+offset;copy.rotation_euler=source.rotation_euler;copy.scale=source.scale;copy.hide_render=i<=45
  bpy.context.view_layer.update()
  nozzle=bpy.data.objects['MIST • dark spray orifice • compact lid']
  origin=sum((nozzle.matrix_world@Vector(v) for v in nozzle.bound_box),Vector())/8
  flow=max(0,min(1,(i-49)/5))
  for ob,spline,j in jets:
   ob.hide_render=flow==0
   for k,point in enumerate(spline.points):
    t=k/3;distance=.011*flow*t
    position=origin+Vector((distance,(j-1.5)*.0004*t,-.00025*t*t))
    point.co=(*position,1)
  # Project moving feature points for the leader lines.
  bpy.context.view_layer.update()
  from bpy_extras.object_utils import world_to_camera_view
  tube=bpy.data.objects['Straw • single-wall stainless mouthpiece']
  bounds=[tube.matrix_world@Vector(v) for v in tube.bound_box]
  point=sum(bounds,Vector())/8
  co=world_to_camera_view(scene,scene.camera,point)
  features={'straw':[round(co.x*1000),round((1-co.y)*1000)]}
  for feature,object_name in [('spout','Drink • tall stainless open spout'),('spray','MIST • dark spray orifice • compact lid')]:
   ob=scene.objects.get(object_name)
   if ob:
    point=sum((ob.matrix_world@Vector(v) for v in ob.bound_box),Vector())/8
    co=world_to_camera_view(scene,scene.camera,point)
    features[feature]=[round(co.x*1000),round((1-co.y)*1000)]
  metadata[slug]['annotations'][str(i)]=features
  if '--metadata-only' not in sys.argv:
   scene.render.filepath=str(dest/f'{i:02d}.png');bpy.ops.render.render(write_still=True)
  print('WEB_FRAME',slug,i,flush=True)
(out/'manifest.json').write_text(json.dumps(metadata,indent=2))
