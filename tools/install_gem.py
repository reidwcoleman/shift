"""Copy Gemini placement renders (photos/gem/*.png) into the site + first_shift folders as JPGs.
    .venv/bin/python tools/install_gem.py [names...]
"""
import os, sys, glob
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEM = os.path.join(ROOT, "photos", "gem"); FS = os.path.join(ROOT, "photos", "first_shift"); SITE = os.path.join(ROOT, "docs", "assets", "photos", "fs")
names = sys.argv[1:] or [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(GEM, "*.png"))]
for n in names:
    im = Image.open(os.path.join(GEM, n + ".png")).convert("RGB")
    im.save(os.path.join(FS, n + ".jpg"), quality=92)
    s = im.copy(); s.thumbnail((1600, 1600), Image.LANCZOS); s.save(os.path.join(SITE, n + ".jpg"), quality=86, optimize=True, progressive=True)
    print("installed", n, im.size)
