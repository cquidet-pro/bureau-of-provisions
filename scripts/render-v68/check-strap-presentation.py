"""Check both fold covers and release-lever orientation in native space."""
import os,runpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
os.environ['BOP_RENDER_MODE']='setup';g=runpy.run_path(str(Path(__file__).resolve().parent/'native-studio.py'));globals().update(g)
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();checks=[]
for side in (-1,1):
 tab=s.objects['WEB-Folded-tab-'+str(side)];ev=tab.evaluated_get(dg);me=ev.to_mesh();bv=BVHTree.FromPolygons([ev.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons]);ev.to_mesh_clear()
 for name,camera in [('catalogue',(0,-.433503,.29)),('scene',(0,-.65,.22037)),('macro',(0,-.241197,.365))]:
  for dx in [-.0055,0,.0055]:
   point=Vector((side*.047+dx,-.00165,.150));direction=(Vector(camera)-point).normalized();hit=bv.ray_cast(point,direction)
   assert hit[0] is not None,(side,name,dx,'lower metal bar uncovered')
  checks.append({'side':side,'camera':name,'lower_bar_covered':True})
 lever=s.objects['WEB-snap-trigger-lever-'+str(side)];verts=[lever.matrix_world@v.co for v in lever.data.vertices]
 jaw=Vector((side*.0327,-.001,.16395));across=Vector((side*.00695,0,.0143)).normalized()
 assert min((v-jaw).dot(across) for v in verts)>0,'Release lever must be above the hook body'
# The joint line is on the actual source interface, not an added band/gasket.
joint=s.objects['WEB-cap-body-interface'];joint_z=[p.co.z for sp in joint.data.splines for p in sp.points]
assert max(abs(z-.1795) for z in joint_z)<1e-7
assert joint.data.bevel_depth<.0001
canada=next(e for e in json.loads((ROOT/'design/product-design.json').read_text())['editions'] if e['number']==27);palette(canada)
for side in (-1,1):
 bs=s.objects['WEB-Folded-tab-'+str(side)].data.materials[0].node_tree.nodes['Principled BSDF']
 assert not bs.inputs['Base Color'].is_linked,'Canada fold must not inherit the red strap texture'
 assert max(abs(a-b) for a,b in zip(bs.inputs['Base Color'].default_value[:3],rgb('#f4f3ee')))<1e-6
# Clear lid must not blend bent and straight images of the same parts.
hood=bpy.data.materials['Clear hood'];out=next(n for n in hood.node_tree.nodes if n.bl_idname=='ShaderNodeOutputMaterial');surface=out.inputs['Surface'].links[0].from_node
assert surface.bl_idname=='ShaderNodeBsdfTransparent','Lid must use a single clear photographic transmission path'
assert s.cycles.min_transparent_bounces>=s.cycles.transparent_max_bounces,'Trace the compound clear lid without roulette grain'
assert not any(n.bl_idname=='ShaderNodeMixShader' for n in hood.node_tree.nodes),'Multiple optical paths can reintroduce ghost images'
button=bpy.data.materials['Button · satin silver metal touch'].node_tree.nodes['Principled BSDF']
assert button.inputs['Metallic'].default_value==1 and button.inputs['Roughness'].default_value<=.121,'Button face must retain polished stainless finish'
record={'button_finish':'polished stainless steel; metallic 1, roughness 0.12','checks':checks,'release_lever':'above on both hooks','texture_mapping':'cumulative physical arc length; square physical texture pixels','texture_height':route['TEXTURE_HEIGHT'],'canada_folds':'both plain ivory, no red texture','cap_body_interface_z_mm':179.5,'joint_line_width_mm':joint.data.bevel_depth*2000,'lid_optics':'single unbent path, zero roughness; no reflected/offset duplicate images'}
(BASE/'strap-presentation.json').write_text(json.dumps(record,indent=2)+'\n');print('Both lower bars covered in all three views; both release levers above.')
