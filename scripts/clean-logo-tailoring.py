"""Clean traced contours and tailor the shorts around a real tail opening."""
from pathlib import Path
import math
import re

source = Path('public/images/product/crest-vector-v5.svg').read_text()
old = 'M980 564Q1025 584 1075 577L1086 641L1071 674L1035 660L1016 638L982 678L937 653Q949 607 980 584Z'
new = 'M980 564Q1030 584 1082 578Q1101 580 1110 597L1122 644L1104 676L1048 668L1016 638L982 678L937 653Q949 607 980 584Z'
source = source.replace(old, new)
# White in the tailoring mask keeps the original tail visible through the hole.
source = source.replace(f'<path d="{new}" fill="black"/>', f'<path d="{new}" fill="black"/><ellipse cx="1102" cy="640" rx="14" ry="20" transform="rotate(-18 1102 640)" fill="white"/>')
source = source.replace('M976 579Q1026 600 1077 591 M943 640L978 662 M1042 649L1077 662 M1020 593L1016 638 M989 595Q976 611 976 624', 'M976 579Q1032 600 1095 596 M943 640L978 662 M1050 655L1104 662 M1020 593L1016 638 M989 595Q976 611 976 624 M1060 606Q1075 613 1083 626')
source = source.replace(f'<path d="{new}"/>', f'<path d="{new}"/><ellipse cx="1102" cy="640" rx="14" ry="20" transform="rotate(-18 1102 640)"/>')

def distance(p, a, b):
    dx,dy=b[0]-a[0], b[1]-a[1]
    if dx==0 and dy==0: return math.dist(p,a)
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)))
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def simplify(points, epsilon=.85):
    if len(points)<3: return points
    peak,index=max((distance(p,points[0],points[-1]),i) for i,p in enumerate(points[1:-1],1))
    if peak<=epsilon: return [points[0],points[-1]]
    return simplify(points[:index+1],epsilon)[:-1]+simplify(points[index:],epsilon)
def fmt(p): return ','.join(f'{v:.2f}'.rstrip('0').rstrip('.') for v in p)
def clean_contour(part):
    points=[tuple(map(float,p)) for p in re.findall(r'(-?\d+),(-?\d+)',part)]
    if len(points)<3: return part
    points=simplify(points+[points[0]])[:-1]
    if len(points)<3: return part
    joins=[]
    for i,p in enumerate(points):
        before,after=points[i-1],points[(i+1)%len(points)]
        d1,d2=math.dist(p,before),math.dist(p,after)
        trim=min(.65,d1*.22,d2*.22)
        entry=tuple(p[j]+(before[j]-p[j])*trim/d1 for j in [0,1])
        leave=tuple(p[j]+(after[j]-p[j])*trim/d2 for j in [0,1])
        joins.append((entry,p,leave))
    return 'M'+fmt(joins[-1][2])+''.join('L'+fmt(a)+'Q'+fmt(b)+' '+fmt(c) for a,b,c in joins)+'Z'
match=re.search(r'<path id="ink" d="([^"]+)"',source)
old_ink=match.group(1)
new_ink=''.join(clean_contour(part) for part in re.findall(r'M[^Z]+Z',old_ink))
source=source.replace(old_ink,new_ink,1)
Path('public/images/product/crest-vector-v6.svg').write_text(source)
print(f'Cleaned original ink: {len(old_ink):,} → {len(new_ink):,} characters; retained the original contours.')
