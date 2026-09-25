"""Stitch the two viewport screenshots of a 1280x1280-displayed Gemini image back into 1024x1024.

    .venv/bin/python tools/stitch_shots.py NAME shotA.jpg shotB.jpg [--split 391]

shotA = page scrolled to y=0, shotB = page scrolled to y=SPLIT, image drawn at 0,0 at 1280x1280.
The extension downscales the 1920-wide viewport to 1568, so everything is scaled by 1568/1920.
"""
import sys, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "photos", "gem")

name, a, b = sys.argv[1], sys.argv[2], sys.argv[3]
split = int(sys.argv[sys.argv.index("--split") + 1]) if "--split" in sys.argv else 391
A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
s = A.width / 1920.0
w = int(round(1280 * s))
cut = int(round(split * s))
canvas = Image.new("RGB", (w, int(round(1280 * s))), "white")
canvas.paste(A.crop((0, 0, w, cut)), (0, 0))
canvas.paste(B.crop((0, 0, w, canvas.height - cut)), (0, cut))
canvas = canvas.resize((1024, 1024), Image.LANCZOS)
p = os.path.join(OUT, name + ".png")
canvas.save(p)
print(name, canvas.size, "scale=%.4f" % s)
