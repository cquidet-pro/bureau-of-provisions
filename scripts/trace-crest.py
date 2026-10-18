"""Trace the approved single-ink brand artwork into scalable SVG paths."""
from pathlib import Path
import subprocess

source = Path('public/images/product/crest-approved-v3.png')
raw = subprocess.check_output(['magick',str(source),'-colorspace','gray','-threshold','50%','-depth','8','-compress','none','pgm:-']).decode()
tokens=[]
for line in raw.splitlines():
    if not line.startswith('#'): tokens.extend(line.split())
assert tokens.pop(0)=='P2'
w,h,maximum=map(int,tokens[:3]); pixels=[int(v)==0 for v in tokens[3:]]
def ink(x,y): return 0<=x<w and 0<=y<h and pixels[y*w+x]
edges={}
def edge(a,b): edges.setdefault(a,[]).append(b)
for y in range(h):
    for x in range(w):
        if not ink(x,y): continue
        if not ink(x,y-1): edge((x,y),(x+1,y))
        if not ink(x+1,y): edge((x+1,y),(x+1,y+1))
        if not ink(x,y+1): edge((x+1,y+1),(x,y+1))
        if not ink(x-1,y): edge((x,y+1),(x,y))
paths=[]
while edges:
    start=next(iter(edges)); point=start; points=[]
    while True:
        points.append(point); options=edges[point]; nxt=options.pop()
        if not options: del edges[point]
        point=nxt
        if point==start: break
    if len(points)<5: continue
    simple=[]
    for i,p in enumerate(points):
        a=points[i-1];b=points[(i+1)%len(points)]
        if (p[0]-a[0])*(b[1]-p[1]) != (p[1]-a[1])*(b[0]-p[0]): simple.append(p)
    if len(simple)<3: continue
    paths.append('M'+'L'.join(f'{x},{y}' for x,y in simple)+'Z')
d=''.join(paths)
# Crop the paper margin; preserve exact approved ink rather than redrawing lettering.
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="150 140 1040 1000"><title>The Bureau of Provisions — Department of Thirst</title><defs><path id="ink" d="{d}"/><clipPath id="dog-clip"><path d="M160 220H465V365L430 425L395 470L350 525L350 650L395 745H160Z"/></clipPath><clipPath id="leopard-clip"><path d="M835 160H1190V775H885L885 700L850 630L850 500L835 445Z"/></clipPath></defs><g id="crest" fill="currentColor"><use href="#ink"/></g><symbol id="greyhound" viewBox="160 220 310 530"><g fill="currentColor" clip-path="url(#dog-clip)"><use href="#ink"/></g></symbol><symbol id="leopard" viewBox="835 160 355 615"><g fill="currentColor" clip-path="url(#leopard-clip)"><use href="#ink"/></g></symbol></svg>'''
Path('public/images/product/crest-vector-v1.svg').write_text(svg)
print(f'Traced {len(paths)} contours; {len(svg):,} bytes')
