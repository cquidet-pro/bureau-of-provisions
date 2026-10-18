"""Restore unclipped monogram contours and compact the logo's spacing."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
def tag(name): return '{'+NS+'}'+name
def el(xml): return ET.fromstring('<svg xmlns="'+NS+'">'+xml+'</svg>')[0]
source=Path('public/images/product/crest-vector-v8.svg').read_text()
root=ET.fromstring(source); defs=root.find(tag('defs'))
ink=defs.find(".//"+tag('path')+"[@id='ink']").attrib['d']
letters=[]
for part in re.findall(r'M[^Z]+Z',ink):
    pts=[tuple(map(float,p)) for p in re.findall(r'(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)',part)]
    if not pts: continue
    xs,ys=zip(*pts)
    if min(xs)>=450 and max(xs)<=805 and min(ys)>=440 and max(ys)<=660: letters.append(part)
assert len(letters)==7, 'Expected the original B, o and P plus their counters.'
defs.append(el('<path id="clean-monogram" d="'+''.join(letters)+'"/>'))
crest=root.find(tag('g')+"[@id='crest']")
# The old monogram was nested beneath the removed shield's mask. That mask
# crossed the shifted P bowl. Extract the letters and render them independently.
for parent in list(crest.iter()):
    for child in list(parent):
        if child.attrib.get('clip-path')=='url(#monogram-lettering)' or child.attrib.get('transform')=='translate(297 315) scale(.4)': parent.remove(child)
crest.attrib['id']='compact-logo-base'
root.remove(crest); defs.append(crest)
defs.append(el('<clipPath id="logo-upper"><rect x="0" y="0" width="1266" height="960"/></clipPath>'))
defs.append(el('<clipPath id="logo-footer"><rect x="0" y="960" width="1266" height="282"/></clipPath>'))
new=el('''<g id="crest" fill="currentColor"><use href="#compact-logo-base" clip-path="url(#logo-upper)"/><g transform="translate(0 -50)"><use href="#compact-logo-base" clip-path="url(#logo-footer)"/></g><g transform="translate(-17.24 -34) scale(1.08)"><use href="#clean-monogram"/></g><g transform="translate(268.2 306.35) scale(.432)" clip-path="url(#original-crown)"><use href="#ink"/></g></g>''')
root.insert(2,new)
Path('public/images/product/crest-vector-v9.svg').write_text(ET.tostring(root,encoding='unicode'))
