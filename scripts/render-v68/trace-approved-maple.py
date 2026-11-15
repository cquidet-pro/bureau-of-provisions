"""Trace the approved old Canada motif, rather than inventing a new leaf.
Only the isolated red component on the left strap is used. Output is vector.
"""
from pathlib import Path
from PIL import Image
import math,json,hashlib
ROOT=Path(__file__).resolve().parents[2];src=ROOT/'public/images/product/edition-27-canada-v1.png';im=Image.open(src).convert('RGB')
red=lambda xy:(lambda c:c[0]>90 and c[0]>1.5*c[1] and c[0]>1.5*c[2])(im.getpixel(xy))
seed=(208,945);todo=[seed];pixels={seed}
while todo:
 x,y=todo.pop()
 for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 164<q[0]<247 and 898<q[1]<990 and q not in pixels and red(q):pixels.add(q);todo.append(q)
assert len(pixels)>1000,'Approved motif not found'
edges={}
for x,y in pixels:
 for neighbour,a,b in [((x,y-1),(x,y),(x+1,y)),((x+1,y),(x+1,y),(x+1,y+1)),((x,y+1),(x+1,y+1),(x,y+1)),((x-1,y),(x,y+1),(x,y))]:
  if neighbour not in pixels:edges[a]=b
loops=[]
while edges:
 start=next(iter(edges));p=start;loop=[]
 while p in edges:loop.append(p);p=edges.pop(p)
 if len(loop)>20:loops.append(loop)
loop=max(loops,key=len)
def simplify(points,eps):
 if len(points)<3:return points
 a,b=points[0],points[-1];dx=b[0]-a[0];dy=b[1]-a[1];den=math.hypot(dx,dy)
 ds=[abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/den if den else math.dist(a,p) for p in points];k=max(range(len(ds)),key=ds.__getitem__)
 if ds[k]<=eps:return [a,b]
 return simplify(points[:k+1],eps)[:-1]+simplify(points[k:],eps)
# Undo the old left strap's lean before reapplying the motif to new webbing.
a=math.radians(10);pts=[((x-208)*math.cos(a)+(y-945)*math.sin(a),-(x-208)*math.sin(a)+(y-945)*math.cos(a)) for x,y in simplify(loop+[loop[0]],.8)]
minx,maxx=min(x for x,y in pts),max(x for x,y in pts);miny,maxy=min(y for x,y in pts),max(y for x,y in pts);scale=110/(maxx-minx)
pts=[((x-(minx+maxx)/2)*scale,(y-(miny+maxy)/2)*scale) for x,y in pts]
path='M'+' L'.join(f'{x:.2f},{y:.2f}' for x,y in pts)+' Z'
out=ROOT/'design/flag-artwork';out.mkdir(exist_ok=True)
(out/'approved-canada-leaf.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-64 -72 128 144"><path d="{path}" fill="#d80621"/></svg>\n')
(out/'approved-canada-leaf.json').write_text(json.dumps({'source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop_seed':[208,945],'method':'Boundary trace of the approved red maple leaf component; deskew old strap lean by 10 degrees; simplify subpixel weave edge only. No generated replacement symbol.','path':path},indent=2)+'\n')
