"""Expand the approved vector artwork into self-contained SVG image documents.

External <use> shadow trees lose nested masks/clips in some Safari/WebKit
versions. SVG <image> loads each export in its own document; exports contain
no <use>, external resources, duplicate IDs or cross-document mask references.
The editable v11 master remains untouched.
"""
from pathlib import Path
from copy import deepcopy
import json
import re
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
tag = lambda name: '{' + NS + '}' + name
folder = Path('public/images/product')
master = ET.parse(folder / 'crest-vector-v11.svg').getroot()
ids = {node.get('id'): node for node in master.iter() if node.get('id')}
palettes = {
    'navy': '#213b50', 'brand': '#22394b', 'ivory': '#fff5de',
    'cream': '#fff4db', 'charcoal': '#292f32', 'olive': '#35442e',
    'raspberry': '#922c55', 'plum': '#69465c',
}
views = {'crest': '150 140 1040 1000', 'greyhound': '160 220 310 530', 'leopard': '835 160 355 615'}

def expand(original, keep_id=False):
    node = deepcopy(original)
    if node.tag == tag('use'):
        reference = node.attrib.pop('href')
        assert reference.startswith('#')
        node.tag = tag('g')
        node.append(expand(ids[reference[1:]]))
    else:
        node[:] = [expand(child) for child in original]
    if not keep_id:
        node.attrib.pop('id', None)
    return node

def references(node):
    return set(re.findall(r'url\(#([^\)]+)\)', ET.tostring(node, encoding='unicode')))

def export(symbol, colour):
    root = ET.Element(tag('svg'), {'viewBox': views[symbol], 'color': palettes[colour], 'fill': palettes[colour]})
    title = ET.SubElement(root, tag('title'))
    title.text = 'Bureau of Provisions' if symbol == 'crest' else symbol.title()
    body = expand(ids[symbol])
    if body.tag == tag('symbol'):
        body.tag = tag('g')
        body.attrib.pop('viewBox', None)
    definitions = ET.SubElement(root, tag('defs'))
    required, included = references(body), set()
    while required - included:
        name = sorted(required - included)[0]
        definition = expand(ids[name], keep_id=True)
        definitions.append(definition)
        included.add(name)
        required |= references(definition)
    root.append(body)
    assert not any(n.tag == tag('use') for n in root.iter())
    actual_ids = [n.get('id') for n in root.iter() if n.get('id')]
    assert len(actual_ids) == len(set(actual_ids))
    path = folder / f'{symbol}-{colour}-v12.svg'
    ET.ElementTree(root).write(path, encoding='unicode')
    return '/images/product/' + path.name

renders = {symbol: {colour: export(symbol, colour) for colour in (palettes if symbol == 'crest' else ['navy', 'ivory', 'cream', 'charcoal'])} for symbol in views}
manifest_path = Path('design/product-design.json')
manifest = json.loads(manifest_path.read_text())
manifest['branding']['render_assets'] = renders
manifest['branding']['browser_compatibility'] = 'Use self-contained SVG image exports; no external SVG use chains. Original editable master retained.'

def edition_colours(name):
    crest, strap = 'navy', 'navy'
    if name in ['Cobalt / Sunshine', 'Ocean / Coral', 'Raspberry / Mint', 'Midnight Paris', 'Web Hero']: crest = 'ivory'
    if name in ['Midnight Paris', 'Safari Club', 'Web Hero', 'Pink Parade']: strap = 'ivory'
    if name == 'Safari Club': crest = 'olive'
    if name == 'Pink Parade': crest = 'raspberry'
    if name in ['All White', 'All Grey']: crest = strap = 'charcoal'
    if name in ['Orbit Club', 'Secret Identity']: crest = strap = 'cream'
    if name == 'Extra Time': crest = 'cream'
    if name == 'Royal Protocol': crest, strap = 'plum', 'cream'
    return crest, strap

html_path = Path('index.html')
html = html_path.read_text()
pattern = re.compile(r'<use href="/images/product/crest-vector-v11\.svg#(crest|greyhound|leopard)"\s*/>|<image data-brand-symbol="(crest|greyhound|leopard)"[^>]*/>')
count = [0]
def replace_uses(fragment, crest='navy', strap='navy'):
    # HTML images retain native lazy loading; don't restore eager SVG wrappers.
    def replace_img(match):
        tag = match[0]
        symbol = re.search(r'data-brand-symbol="([^"]+)"', tag)[1]
        colour = crest if symbol == 'crest' else strap
        return re.sub(r'src="[^"]+"', f'src="{renders[symbol][colour]}"', tag)
    fragment = re.sub(r'<img\b[^>]*data-brand-symbol="[^"]+"[^>]*>', replace_img, fragment)
    def replace(match):
        symbol = match[1] or match[2]
        colour = crest if symbol == 'crest' else strap
        box = 'x="150" y="140" width="1040" height="1000"' if symbol == 'crest' else ('width="310" height="530"' if symbol == 'greyhound' else 'width="355" height="615"')
        count[0] += 1
        return f'<image data-brand-symbol="{symbol}" href="{renders[symbol][colour]}" {box}/>'
    return pattern.sub(replace, fragment)

def replace_card(match):
    card = match[0]
    name = re.search(r'data-palette="([^"]+)"', card)[1]
    colours = edition_colours(name)
    return replace_uses(card, *colours)

html = replace_uses(html)
html = re.sub(r'<article class="colour-card"[\s\S]*?</article>', replace_card, html)
# Header and close-up use the original brand ink; product overlays use navy.
html = re.sub(r'<svg class="(?:header-crest|crest-enlargement)"[\s\S]*?</svg>|<img class="(?:header-crest|crest-enlargement)"[^>]*>', lambda m: replace_uses(m[0], 'brand'), html)
assert html.count('data-brand-symbol=') == 64, 'All 64 logo/animal instances must be self-contained images.'
assert 'crest-vector-v11.svg#' not in html
html_path.write_text(html)
for edition in manifest['editions']:
    crest, strap = edition_colours(edition['name'])
    edition['branding_assets'] = {'crest': renders['crest'][crest], 'greyhound': renders['greyhound'][strap], 'leopard': renders['leopard'][strap]}
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
print('Exported 16 self-contained vector images; replaced all 64 external logo uses.')
