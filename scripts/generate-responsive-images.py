"""Create lossless delivery sizes directly from approved PNG masters.

Run only when the photographic sources change. Originals are never overwritten.
Requires Pillow; the normal Node build uses the checked-in outputs.
"""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
from PIL import Image


class Photos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()

    def handle_starttag(self, tag, attrs):
        src = dict(attrs).get('src', '')
        if tag == 'img' and src.startswith('/images/product/') and src.endswith('.webp'):
            self.paths.add(src)


photos = Photos()
photos.feed(Path('index.html').read_text())
output = Path('public/images/product/responsive')
output.mkdir(exist_ok=True)
manifest = {}
for url in sorted(photos.paths):
    master = Path('public' + url).with_suffix('.png')
    with Image.open(master) as image:
        variants = []
        for width in (256, 480, 768, 1024):
            if width >= image.width:
                continue
            height = round(image.height * width / image.width)
            target = output / f'{master.stem}-{width}w.webp'
            image.resize((width, height), Image.Resampling.LANCZOS).save(
                target, 'WEBP', lossless=True, method=6, exact=True)
            variants.append({'src': '/' + str(target.relative_to('public')), 'width': width})
        variants.append({'src': url, 'width': image.width})
        manifest[url] = {'master_sha256': sha256(master.read_bytes()).hexdigest(), 'variants': variants}
    print(master.name, '→', len(variants), 'delivery sizes', flush=True)

# An animation previously delivered the original PNG on every fresh visit.
with Image.open('public/images/product/family-newspaper-turn-v1.png') as image:
    image.save('public/images/product/family-newspaper-turn-v1.webp',
               'WEBP', lossless=True, method=6, exact=True)
Path('design/responsive-images.json').write_text(json.dumps(manifest, indent=2) + '\n')
