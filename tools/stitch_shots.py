"""Stitch two viewport screenshots of a Gemini image back into the image itself.

    .venv/bin/python tools/stitch_shots.py NAME shotA.jpg shotB.jpg DISPW DISPH OUTW OUTH [SPLIT]

shotA = page scrolled to y=0, shotB = page scrolled to y=SPLIT (default 391),
with the image drawn at 0,0 at DISPW x DISPH css px in a 1920-wide viewport.
The extension downscales the viewport to 1568 wide, so everything is scaled by 1568/1920.
"""
import sys, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "photos", "gem")

name, a, b = sys.argv[1], sys.argv[2], sys.argv[3]
dispw, disph, outw, outh = (int(x) for x in sys.argv[4:8])
split = int(sys.argv[8]) if len(sys.argv) > 8 else 391
A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
s = A.width / 1920.0
w, h, cut = int(round(dispw * s)), int(round(disph * s)), int(round(split * s))
canvas = Image.new("RGB", (w, h), "white")
canvas.paste(A.crop((0, 0, w, cut)), (0, 0))
canvas.paste(B.crop((0, 0, w, h - cut)), (0, cut))
canvas = canvas.resize((outw, outh), Image.LANCZOS)
p = os.path.join(OUT, name + ".png")
canvas.save(p)
print(name, canvas.size, "scale=%.4f" % s)
