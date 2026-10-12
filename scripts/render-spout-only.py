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
   p.inputs['Base Color'].default_value=(.96,.96,.96,1);p.inputs['Roughness'].default_value=.035;p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.46
   transparent=m.node_tree.nodes.new('ShaderNodeBsdfTransparent')
   mix=m.node_tree.nodes.new('ShaderNodeMixShader')
   fresnel=m.node_tree.nodes.new('ShaderNodeFresnel');fresnel.inputs['IOR'].default_value=1.46
   weight=m.node_tree.nodes.new('ShaderNodeMath');weight.operation='POWER';weight.inputs[1].default_value=2
   m.node_tree.links.new(fresnel.outputs[0],weight.inputs[0]);m.node_tree.links.new(weight.outputs[0],mix.inputs[0])
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
  d=bpy.data.lights.new(name,'AREA');d.energy=power*.12;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
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

bpy.ops.wm.open_mainfile(filepath='/Users/cedric/code/water-bottle-design/output/waterbottle/waterbottle-cap-type-3-spout-only.blend')
scene=prepare()
hood=next(o for o in scene.objects if o.name.startswith('V20 • rear hinge axis'))
hood.animation_data_clear();hood.rotation_euler.x=math.radians(-112)
bpy.context.view_layer.update()
from bpy_extras.object_utils import world_to_camera_view
spout=bpy.data.objects['Drink • tall stainless open spout']
point=sum((spout.matrix_world@Vector(v) for v in spout.bound_box),Vector())/8
co=world_to_camera_view(scene,scene.camera,point)
Path('/private/tmp/bop-spout-only-label.json').write_text(json.dumps([round(co.x*1000),round((1-co.y)*1000)]))
scene.render.filepath='/private/tmp/bop-spout-only-studio.png';bpy.ops.render.render(write_still=True)
