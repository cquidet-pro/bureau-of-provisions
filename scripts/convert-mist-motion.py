"""Convert Blender PNG frames to compact website WebP assets (Pillow required)."""
from pathlib import Path
import time
from PIL import Image
source_root = Path('/private/tmp/bop-lid-motion-spray45-beige')
output_root = Path(__file__).resolve().parents[1] / 'public/images/lids/motion-spray45-beige'
for _ in range(300):
    for source in source_root.glob('*/*.png'):
        target = output_root / source.parent.name / (source.stem + '.webp')
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with Image.open(source) as frame:
                frame.convert('RGB').save(target, 'WEBP', quality=88, method=6)
        except OSError:
            continue  # The renderer may still be writing this frame.
    if len(list(output_root.glob('*/*.webp'))) == 60:
        break
    time.sleep(2)
else:
    raise SystemExit('Incomplete render: expected 60 frames')
print('Converted all 60 motion frames')
