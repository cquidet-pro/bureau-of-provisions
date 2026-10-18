"""Extend the shared shorts mask and hems around both original upper legs."""
from pathlib import Path
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
tag = lambda name: '{' + NS + '}' + name
root = ET.parse('public/images/product/crest-vector-v10.svg').getroot()
old = 'M980 564Q1028 584 1075 577Q1094 581 1100 597L1105 651L1080 675L1040 660L1016 638L982 678L937 653Q949 607 980 584Z'
new = 'M977 562Q1025 583 1075 577Q1094 584 1100 601L1113 659L1081 687L1040 669L1015 646L983 688L925 657Q940 608 977 582Z'
changed = 0
for node in root.iter(tag('path')):
    if node.get('d') == old:
        node.set('d', new)
        changed += 1
    if node.get('d') == 'M976 579Q1029 600 1092 595 M943 640L978 662 M1046 650L1084 662 M1020 593L1016 638 M989 595Q976 611 976 624 M1055 606Q1067 613 1073 626':
        node.set('d', 'M973 578Q1029 600 1092 595 M934 646L980 674 M1044 658L1084 674 M1020 593L1015 646 M989 595Q976 611 976 624 M1055 606Q1067 613 1073 626')
assert changed == 2, 'Update both the original-ink mask and shared garment outline.'
# The original sloping upper thigh extends outside the garment's left contour.
# Clear it separately: enlarging the garment's own mask alone leaves this strip.
tailoring_mask = next(node for node in root.iter(tag('mask')) if node.get('id') == 'leopard-tailoring-mask')
ET.SubElement(tailoring_mask, tag('rect'), {'x':'890', 'y':'560', 'width':'90', 'height':'100', 'fill':'black'})
Path('public/images/product/crest-vector-v11.svg').write_text(ET.tostring(root, encoding='unicode'))
