"""Append approved V68 strap into the current Blender scene, without saving it.
Use Blender's Scripting workspace > Open > Run Script. See the handoff guide.
Refuses a changed body or duplicate accessory; never edits source bottle meshes.
"""
import bpy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];name='BoP approved detachable strap V68'
if name in bpy.data.collections:raise RuntimeError('Strap collection already exists; inspect it instead of importing twice.')
body=bpy.context.scene.objects.get('01-Body')
if body is None:raise RuntimeError('Expected V68 01-Body. Do not append blindly to a different design.')
bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();h=hashlib.sha256()
for v in me.vertices:h.update(('%0.9f,%0.9f,%0.9f;' % tuple(ev.matrix_world@v.co)).encode())
for p in me.polygons:h.update((','.join(map(str,p.vertices))+';').encode())
ev.to_mesh_clear()
expected=json.loads((ROOT/'docs/v68/source-geometry-integrity.json').read_text())['before']['01-Body']
if h.hexdigest()!=expected:raise RuntimeError('Body differs from checked V68 geometry. Refit and rerun clearance checks before importing.')
with bpy.data.libraries.load(str(ROOT/'design/blender-assets/v68-strap-system.blend'),link=False) as (src,dst):
 if name not in src.collections:raise RuntimeError('Expected accessory collection absent from library.')
 dst.collections=[name]
collection=dst.collections[0];bpy.context.scene.collection.children.link(collection)
print('Appended approved strap at native metre coordinates. Source bottle unchanged. Inspect, then Save As a new revision manually.')
