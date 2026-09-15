"""Vintage / worn pass for print files: ink cracking, fade patches, softened color.

    .venv/bin/python tools/worn.py            # all v3 + hazard prints -> designs/print_worn + designs/upload_worn
"""
import os, sys, glob
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "designs", "print"); OUT = os.path.join(ROOT, "designs", "print_worn"); UP = os.path.join(ROOT, "designs", "upload_worn")
os.makedirs(OUT, exist_ok=True); os.makedirs(UP, exist_ok=True)


def noise(shape, scale, rng):
    h, w = shape
    small = rng.random((max(2, h // scale), max(2, w // scale))).astype(np.float32)
    return np.asarray(Image.fromarray((small * 255).astype("uint8")).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255


def fractal(shape, rng, octaves=((256, 1.0), (64, 0.5), (16, 0.25), (4, 0.15))):
    acc = np.zeros(shape, np.float32); tot = 0
    for scale, amp in octaves:
        acc += noise(shape, scale, rng) * amp; tot += amp
    return acc / tot


def worn(src, dst, seed=1, strength=0.38):
    im = Image.open(src).convert("RGBA")
    a = np.asarray(im).astype(np.float32)
    rgb, alpha = a[..., :3], a[..., 3]
    rng = np.random.default_rng(seed)
    shape = alpha.shape
    # big soft fade patches (ink wearing thin)
    patches = fractal(shape, rng)
    fade = 1 - strength * np.clip((patches - 0.35) / 0.4, 0, 1)
    # fine cracks: thresholded high-frequency noise, stretched horizontally like cracked plastisol
    hf = noise(shape, 3, rng) * 0.6 + noise(shape, 7, rng) * 0.4
    hf = np.asarray(Image.fromarray((hf * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) / 255
    cracks = np.clip((hf - 0.66) / 0.08, 0, 1)  # thin flecks
    crack_mask = 1 - cracks * 0.85
    # speckle dropout
    speck = (rng.random(shape) < 0.012).astype(np.float32)
    speck = np.asarray(Image.fromarray((speck * 255).astype("uint8")).filter(ImageFilter.MaxFilter(3))).astype(np.float32) / 255
    alpha2 = alpha * fade * crack_mask * (1 - speck * 0.7) * 0.94
    # colour: pull 12% toward mid-grey and warm slightly (sun-faded)
    rgb2 = rgb * 0.88 + 128 * 0.12
    rgb2[..., 0] *= 1.02; rgb2[..., 2] *= 0.97
    out = np.dstack([np.clip(rgb2, 0, 255), np.clip(alpha2, 0, 255)]).astype("uint8")
    Image.fromarray(out, "RGBA").save(dst, optimize=True)
    return dst


if __name__ == "__main__":
    names = sys.argv[1:] or [os.path.basename(p) for p in sorted(glob.glob(os.path.join(SRC, "*.png"))) if os.path.basename(p)[:2] in ("20", "21", "22", "23", "24", "25", "26", "27", "29", "30", "31", "32", "33", "06")]
    for i, n in enumerate(names):
        worn(os.path.join(SRC, n), os.path.join(OUT, n), seed=i + 3)
        im = Image.open(os.path.join(OUT, n)); s = 200 / 300
        im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).save(os.path.join(UP, n), optimize=True)
        print("  worn", n, round(os.path.getsize(os.path.join(UP, n)) / 1e6, 1), "MB")
