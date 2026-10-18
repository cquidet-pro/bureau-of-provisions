"""Move the two supporters towards the initials without resizing them."""
from pathlib import Path
import xml.etree.ElementTree as ET
N='http://www.w3.org/2000/svg';ET.register_namespace('',N)
def tag(n):return '{'+N+'}'+n
def node(s):return ET.fromstring('<svg xmlns="'+N+'">'+s+'</svg>')[0]
root=ET.fromstring(Path('public/images/product/crest-vector-v9.svg').read_text());defs=root.find(tag('defs'))
dog='M160 220H465V365L430 425L395 470L350 525V650L395 745L365 738Q290 714 220 741L160 745Z'
leopard='M835 160H1190V775L1060 764Q990 735 900 757L885 775V700L850 630V500L835 445Z'
for name,d in [('moving-dog',dog),('moving-leopard',leopard)]:defs.append(node(f'<clipPath id="{name}"><path d="{d}"/></clipPath>'))
defs.append(node(f'<mask id="supporter-spaces" maskUnits="userSpaceOnUse" x="0" y="0" width="1266" height="1242"><rect width="1266" height="1242" fill="white"/><path d="{dog}" fill="black"/><path d="{leopard}" fill="black"/></mask>'))
crest=root.find(tag('g')+"[@id='crest']")
base=next(c for c in crest if c.attrib.get('clip-path')=='url(#logo-upper)')
base.set('mask','url(#supporter-spaces)')
crest.insert(1,node('<g transform="translate(30 0)"><use href="#compact-logo-base" clip-path="url(#moving-dog)"/></g>'))
crest.insert(2,node('<g transform="translate(-18 0)"><use href="#compact-logo-base" clip-path="url(#moving-leopard)"/></g>'))
Path('public/images/product/crest-vector-v10.svg').write_text(ET.tostring(root,encoding='unicode'))
