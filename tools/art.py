"""Illustration pipeline: Gemini engraving → 1-color ink bitmap → potrace vector.

    .venv/bin/python tools/art.py            # generate everything missing in art/
    .venv/bin/python tools/art.py cherubs    # (re)generate one

art/<name>_raw.png   what Gemini returned
art/<name>_ink.png   white ink on transparent, cropped
art/<name>.svg       potrace vector (single path, fill set by the design)
"""
import os, sys, subprocess, re, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageOps, ImageFilter
import gemini_img

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "art")
os.makedirs(ART, exist_ok=True)

STYLE = ("Vintage copperplate engraving / woodcut illustration, pure white ink linework and cross-hatching on a solid pure black background, "
         "single color only (no gray fills, no gradients), bold clean lines that survive screen printing, centered composition with black margin, "
         "nothing else in frame, absolutely no text, no letters, no watermark.")

ARTS = {
    "cherubs": ("Two cherubs (baby angels with feathered wings, flowing robes) floating and holding an old industrial punch-in time clock between them, "
                "the clock face reads 11:59, a paper time card sticking out of the slot.", "4:5"),
    "sunclock": ("A large symmetrical tribal sun emblem with sharp flame-like rays radiating outward (like a tattoo sun), and in the very center a detailed "
                 "clock face with roman numerals whose hands point to 11:59. Bold, iconic, symmetrical.", "1:1"),
    "skeleton": ("A skeleton hand and forearm bones gripping a manual car gear shifter with an 8-ball knob, small flames licking around the base, "
                 "traditional tattoo flash style.", "4:5"),
    "clockweb": ("A large spider web, viewed straight on, whose concentric rings are drawn like the tick marks of a clock face, with one small spider "
                 "hanging from a thread at the bottom. Bold graphic, symmetrical.", "1:1"),
    "wings": ("A large pair of spread angel wings, perfectly symmetrical, highly detailed feathers, with a small pocket watch hanging on a chain between them "
              "at the center.", "16:9"),
    "hands": ("Praying hands (classic tattoo praying hands with a rosary) but holding a paper employee time card between the palms, "
              "small rays of light behind.", "4:5"),
    "factory": ("A circular emblem: an old brick factory with three smokestacks at night under a crescent moon and stars, smoke rising, "
                "framed inside a bold circle border, engraving style.", "1:1"),
    "moth": ("A large moth with open wings viewed from above, symmetrical, its wing markings forming two clock faces, "
             "traditional tattoo engraving.", "1:1"),
}


def generate(name):
    prompt, aspect = ARTS[name]
    raw = os.path.join(ART, f"{name}_raw.png")
    if not os.path.exists(raw):
        for model in ("gemini-3-pro-image-preview", "gemini-3.1-flash-image"):
            try:
                gemini_img.generate(prompt + " " + STYLE, model=model, aspect=aspect, out=raw)
                break
            except Exception as e:
                print(f"  {name}: {model} failed: {str(e)[:120]}")
        else:
            raise RuntimeError(name)
    vectorize(name)
    return name


def vectorize(name, threshold=120, upscale=3):
    raw = os.path.join(ART, f"{name}_raw.png")
    im = Image.open(raw).convert("L")
    # upscale before thresholding so potrace gets smooth curves
    im = im.resize((im.width * upscale, im.height * upscale), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
    ink = im.point(lambda v: 255 if v > threshold else 0)
    ink = ink.crop(ink.getbbox())
    # Gemini sometimes draws a frame around the art: detect long white runs along the edges and cut inside them
    for _ in range(3):
        w, h = ink.size
        px = ink.load()
        def row_white(y): return sum(1 for x in range(w) if px[x, y] > 0) / w
        def col_white(x): return sum(1 for y in range(h) if px[x, y] > 0) / h
        band = max(2, int(min(w, h) * 0.02))
        framed = (max(row_white(y) for y in range(band)) > 0.8 or max(row_white(h - 1 - y) for y in range(band)) > 0.8
                  or max(col_white(x) for x in range(band)) > 0.8 or max(col_white(w - 1 - x) for x in range(band)) > 0.8)
        if not framed:
            break
        m = int(min(w, h) * 0.05)
        ink = ink.crop((m, m, w - m, h - m))
        ink = ink.crop(ink.getbbox())
    # transparent ink png (white)
    rgba = Image.new("RGBA", ink.size, (255, 255, 255, 0))
    rgba.putalpha(ink)
    rgba.save(os.path.join(ART, f"{name}_ink.png"))
    # potrace wants black = ink
    pbm = os.path.join(ART, f"{name}.pbm")
    ImageOps.invert(ink).convert("1").save(pbm)
    svg = os.path.join(ART, f"{name}.svg")
    subprocess.run(["potrace", pbm, "-s", "-o", svg, "--flat", "-t", "8", "-a", "1.2", "-O", "0.3"], check=True)
    os.remove(pbm)
    return svg


def load_path(name):
    """Return (path_d, width, height, transform) from the potrace svg."""
    svg = open(os.path.join(ART, f"{name}.svg")).read()
    w = int(re.search(r'width="(\d+)', svg).group(1)); h = int(re.search(r'height="(\d+)', svg).group(1))
    m = re.search(r'<g transform="([^"]+)"[^>]*>\s*<path d="([^"]+)"', svg, re.S)
    return m.group(2), w, h, m.group(1)


def place(name, x, y, width, fill="#fff"):
    """SVG snippet placing the art with its top-left at (x,y) scaled to `width` px."""
    d, w, h, tf = load_path(name)
    s = width / w
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.5f})"><g transform="{tf}" fill="{fill}" stroke="none">'
            f'<path d="{d}"/></g></g>'), width, h * s


if __name__ == "__main__":
    names = sys.argv[1:] or list(ARTS)
    for n in names:
        if n in sys.argv[1:]:
            for suf in ("_raw.png",):
                p = os.path.join(ART, n + suf)
                if os.path.exists(p): os.remove(p)
    with cf.ThreadPoolExecutor(4) as ex:
        for n in ex.map(generate, names):
            print("  ok", n)
