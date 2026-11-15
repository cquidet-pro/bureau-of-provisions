"""Vector-authored edition textile patterns; no photographic regeneration."""
from pathlib import Path
import json,subprocess,math,runpy
root=Path(__file__).resolve().parents[2];out=root/'design/v68-strap-textures';out.mkdir(exist_ok=True)
route=runpy.run_path(str(Path(__file__).resolve().parent/'strap_path.py'));H=route['TEXTURE_HEIGHT'];motif_ys=route['motif_positions']()
editions=json.loads((root/'design/product-design.json').read_text())['editions']
def stripe(x,w,c):return f'<rect x="{x}" y="0" width="{w}" height="{H}" fill="{c}"/>'
for e in editions:
 n=e['number'];base=e['accent'];bands=[];motifs=[]
 if n==11:base='#162e51';bands=[(88,80,'#eee8d8'),(100,56,'#c43240')]
 if n==12:base='#eee8d8';bands=[(88,80,'#19344c'),(106,44,'#b73542')]
 if n==13:base='#59634a';bands=[(97,62,'#b7a279')]
 if n==14:base='#31539b';bands=[(103,50,'#ba3e49')]
 if n==15:base='#b44668';bands=[(100,56,'#eee8d8')]
 if n==16:base='#695678';bands=[(13,3,'#eee8d8'),(240,3,'#eee8d8')]
 if n==17:base='#eee8d8';bands=[(96,64,'#214e43'),(114,28,'#713b44')]
 if n==18:base='#b5a1d0';bands=[(124,8,'#eee8d8')]
 if n==19:base='#ba3e49';bands=[(123,10,'#d3ad58')]
 if n==20:base='#78e4e8';bands=[(108,40,'#b5a1d0')]
 if n==21:
  base='#0d5eaf';bands=[(i*256/7,256/7,'#f4f3ee') for i in (1,3,5)]
 if n in (22,28):
  base='#002654' if n==22 else '#009246';bands=[(256/3,256/3,'#f4f3ee'),(512/3,256/3,'#ed2939' if n==22 else '#ce2b37')]
 if n==23:
  base='#012169';bands=[(256/3,256/3,'#f4f3ee'),(102.4,51.2,'#c8102e')]
  # True Union Jack cross and counterchanged saltire, rotated along webbing.
  for i,y in enumerate([.145*H,.27*H,.73*H,.855*H]):
   motifs.append(f'<g transform="translate(128,{y}) rotate(90) scale({256/30}) translate(-30,-15)"><defs><clipPath id="uf{i}"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath><clipPath id="box{i}"><rect width="60" height="30"/></clipPath></defs><g clip-path="url(#box{i})"><rect width="60" height="30" fill="#012169"/><path d="M0 0L60 30M60 0L0 30" stroke="#f4f3ee" stroke-width="6"/><path d="M0 0L60 30M60 0L0 30" stroke="#c8102e" stroke-width="4" clip-path="url(#uf{i})"/><path d="M30 0V30M0 15H60" stroke="#f4f3ee" stroke-width="10"/><path d="M30 0V30M0 15H60" stroke="#c8102e" stroke-width="6"/></g></g>')
 if n==24:
  base='#21345b';bands=[(28+i*200/9,200/9,'#b31942' if i%2==0 else '#f4f3ee') for i in range(9)]
  for y in (.1465*H,.8535*H):
   for x in (13,243):
    pts=' '.join(f'{x+(10 if i%2==0 else 4)*math.sin(i*math.pi/5)},{y-(10 if i%2==0 else 4)*math.cos(i*math.pi/5)}' for i in range(10));motifs.append(f'<polygon points="{pts}" fill="#f4f3ee"/>')
 if n==25:base='#009739';bands=[(55,146,'#fedf00'),(89,78,'#002776')]
 if n==26:
  base='#f4f3ee';bands=[(112,32,'#bc002d')]
  for y in motif_ys:motifs.append(f'<circle cx="128" cy="{y}" r="70" fill="#f4f3ee"/><circle cx="128" cy="{y}" r="55" fill="#bc002d"/>')
 if n==27:
  base='#d80621';bands=[(64,128,'#f4f3ee')]
  path=json.loads((root/'design/flag-artwork/approved-canada-leaf.json').read_text())['path']
  for i,y in enumerate(motif_ys):motifs.append(f'<path d="{path}" transform="translate(128,{y}) rotate({180 if i==0 else 0})" fill="#d80621"/>')
 if n==29:base='#aa151b';bands=[(64,128,'#f1bf00')]
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="{H}" viewBox="0 0 256 {H}">'+stripe(0,256,base)+''.join(stripe(*b) for b in bands)+''.join(motifs)+'</svg>'
 path=out/f'edition-{n:02}.svg';path.write_text(svg);subprocess.run(['rsvg-convert',str(path),'-o',str(path.with_suffix('.png'))],check=True)
