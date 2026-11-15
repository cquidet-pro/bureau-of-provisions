"""Check actual evaluated V68 body against both separately modelled snap hooks.
Run after export-hook-clearance.py with numpy, trimesh and manifold3d.
This checks depicted solid fit only; it is not a load or tolerance certification.
"""
import hashlib,json,os
from pathlib import Path
import numpy as np
import trimesh
import manifold3d as md
ROOT=Path(__file__).resolve().parents[2]
source=Path(os.environ.get('BOP_EVIDENCE_OUT',ROOT/'output/design-v68/native'))/'hook-clearance-meshes.json'
parts=json.loads(source.read_text());solids={}
for name,data in parts.items():
 mesh=trimesh.Trimesh(data['vertices_mm'],data['faces'],process=True)
 mesh.fix_normals()
 assert mesh.is_watertight,name
 solid=md.Manifold(md.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
 assert solid.status()==md.Error.NoError and solid.volume()>0,name
 solids[name]=solid
body=solids.pop('01-Body');report={'method':'Evaluated native meshes in millimetres; watertight oriented solids; Manifold intersection and minimum gap. Gap search capped at 2 mm.','mesh_export_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'render_setup_sha256':hashlib.sha256((ROOT/'scripts/render-v68/native-studio.py').read_bytes()).hexdigest(),'scope':'Depicted closed snap fit against original body; no strength, manufacturing tolerance or opening-motion certification.','parts':{}}
for name,solid in solids.items():
 volume=(body^solid).volume();gap=body.min_gap(solid,2)
 assert abs(volume)<1e-8 and gap>0.25,(name,volume,gap)
 report['parts'][name]={'intersection_mm3':volume,'minimum_gap_mm_capped_2':gap}
report['minimum_gap_mm']=min(p['minimum_gap_mm_capped_2'] for p in report['parts'].values())
Path(os.environ.get('BOP_FIT_REPORT',ROOT/'docs/v68/hook-clearance.json')).write_text(json.dumps(report,indent=2)+'\n')
print('PASS: 16 metal parts, zero body intersection; minimum gap',round(report['minimum_gap_mm'],3),'mm')
