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
manifest_path = Path('design/responsive-images.json')
previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
manifest = {}
for url in sorted(photos.paths):
    master = Path('public' + url).with_suffix('.png')
    master_hash = sha256(master.read_bytes()).hexdigest()
    cached = previous.get(url)
    if cached and cached['master_sha256'] == master_hash and all(
            Path('public' + variant['src']).exists() for variant in cached['variants']):
        manifest[url] = cached
        print(master.name, '→ unchanged', flush=True)
        continue
    with Image.open(master) as image:
        variants = []
        for width in ((256, 480, 768, 1024, 1536, 2048, 3072) if master.stem == 'platform-native-v68' else (256, 480, 768, 1024)):
            if width >= image.width:
                continue
            height = round(image.height * width / image.width)
            target = output / f'{master.stem}-{width}w.webp'
            image.resize((width, height), Image.Resampling.LANCZOS).save(
                target, 'WEBP', lossless=True, method=6, exact=True)
            variants.append({'src': '/' + str(target.relative_to('public')), 'width': width})
        variants.append({'src': url, 'width': image.width})
        manifest[url] = {'master_sha256': master_hash, 'variants': variants}
    print(master.name, '→', len(variants), 'delivery sizes', flush=True)

# An animation previously delivered the original PNG on every fresh visit.
newspaper_master = Path('public/images/product/family-newspaper-turn-v1.png')
newspaper_delivery = newspaper_master.with_suffix('.webp')
if not newspaper_delivery.exists() or newspaper_delivery.stat().st_mtime < newspaper_master.stat().st_mtime:
    with Image.open(newspaper_master) as image:
        image.save(newspaper_delivery, 'WEBP', lossless=True, method=6, exact=True)
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
