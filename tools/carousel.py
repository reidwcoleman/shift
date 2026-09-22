"""Make an Instagram carousel (1080x1350 slides) from site photos.
    .venv/bin/python tools/carousel.py 10_league_tigers league_lean tigers_stoop league_tee_flat tigers_tee_flat
"""
import os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FS = os.path.join(ROOT, "photos", "first_shift")
name, files = sys.argv[1], sys.argv[2:]
out = os.path.join(ROOT, "content", "carousels", name); os.makedirs(out, exist_ok=True)
W, H = 1080, 1350
for i, f in enumerate(files, 1):
    im = Image.open(os.path.join(FS, f + ".jpg")).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    # flats: centre crop on a white/neutral background; people: bias the crop upward a touch
    x = (im.width - W) // 2; y = int((im.height - H) * (0.5 if f.endswith("_flat") else 0.35))
    im.crop((x, y, x + W, y + H)).save(os.path.join(out, f"{i:02d}_{f}.jpg"), quality=92)
    print("slide", i, f)
