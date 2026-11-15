"""Export final native PNG masters once, losslessly; preserve every master."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
from PIL import Image
root=Path(__file__).resolve().parents[2]
def export(p):
 target=p.with_suffix('.webp')
 if target.exists() and target.stat().st_mtime>=p.stat().st_mtime:return
 with Image.open(p) as im:im.save(target,'WEBP',lossless=True,method=6,exact=True)
 print(p.name,flush=True)
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(export,sorted(Path(os.environ.get('BOP_ASSET_OUT',root/'public/images/product')).glob('*-native-v68.png'))))
