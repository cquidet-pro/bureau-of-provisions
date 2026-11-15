"""Existing cooling-mist illustration, anchored to the native spray outlet."""
import json,random,math
from pathlib import Path
root=Path(__file__).resolve().parents[2];a=json.loads((root/'output/design-v68/native/view-anchors.json').read_text())['station']['spray_outlet'];x,y=a;rng=random.Random(68);parts=[]
for i in range(8):
 t=(i+1)/8;cx=x+345*t;cy=y-190*t;parts.append(f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{18+30*t:.2f}" ry="{2+13*t:.2f}" transform="rotate(-29 {cx:.2f} {cy:.2f})" fill="white" opacity="{.025+.065*t:.3f}" filter="url(#soft-mist)"/>')
for i in range(650):
 t=rng.random();spread=rng.gauss(0,1)*(1+16*t);cx=x+345*t+spread*.483;cy=y-190*t+spread*.876;r=.28+rng.random()*.62;op=(.18+rng.random()*.5)*(1-.5*t);parts.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="white" opacity="{op:.3f}"/>')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024"><defs><filter id="soft-mist" x="-40%" y="-100%" width="180%" height="300%"><feGaussianBlur stdDeviation="4"/></filter></defs>'+''.join(parts)+'</svg>'
(root/'public/images/product/cooling-mist-native-v68.svg').write_text(svg)
