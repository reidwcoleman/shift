"""Multi-color print artwork: Gemini 4K on chroma green → keyed RGBA PNG.

    .venv/bin/python tools/art_color.py           # all missing
    .venv/bin/python tools/art_color.py tigers    # regenerate one

art/color/<name>_raw.png   Gemini output (green background)
art/color/<name>.png       keyed, cropped, transparent — drop straight into a print file
"""
import os, sys, json, base64, urllib.request, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageFilter
import gemini_img

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "art", "color")
os.makedirs(OUT, exist_ok=True)

BG = ("Centered on a solid, flat, perfectly uniform pure chroma-key green (#00FF00) background that fills the entire frame edge to edge. "
      "No fabric texture on the background, no shadows, no frame, no border, no watermark, absolutely no text or letters anywhere unless specified.")
STYLE = "Distressed vintage screen-print t-shirt graphic, flat spot colors, slight ink cracking, 1990s college / tattoo-flash feel, high detail, print-ready."

ARTS = {
    "tiger_crest": ("A roaring tiger head inside a laurel wreath, with an empty ribbon banner beneath, in exactly three flat colors: athletic gold, cream and black. Symmetrical varsity crest.", "4:5"),
    "twin_tigers": ("Two Bengal tigers facing each other, mirror-symmetrical, prowling toward the center where an antique pocket watch sits, drawn in a vintage 1970s illustrated style in sepia brown, rust red and cream, with fine ink hatching.", "4:5"),
    "timecard_cross": ("A tall Latin cross built entirely out of overlapping vintage paper employee time cards and old dollar-bill textures, cream paper, black type marks and green-gold money-engraving details, slightly curled edges, a small red LATE stamp on one card.", "4:5"),
    "sundial": ("A classic sun face (like an old sundial or tarot sun) with wavy and straight alternating rays, a serene face, and a sundial gnomon casting a shadow across it, drawn in two colors: rust red and dark navy line art, distressed and faded.", "1:1"),
    "script_drip": ("The word 'Shift' in a glossy chrome-and-pink tattoo script lettering with sharp flourishes, red blood-drips running down from the letters, gothic and shiny, with a small crown above the S.", "16:9"),
    "collage": ("A dense vintage photo-collage print: torn newspaper clippings, an old alarm clock, a crescent moon, a city skyline at night, a punch clock, a rose, playing cards and a stopwatch, layered like a 1990s band tee collage, muted colors: cream, faded red, gold and black.", "4:5"),
    "spider_tiger": ("A tiger's face merged with an iron cross behind it, black and gold with a cream outline, like a 2000s rock band emblem.", "1:1"),
}


def generate(name):
    prompt, aspect = ARTS[name]
    raw = os.path.join(OUT, f"{name}_raw.png")
    if not os.path.exists(raw):
        body = {"contents": [{"parts": [{"text": f"{prompt} {STYLE} {BG}"}]}],
                "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect, "imageSize": "4K"}}}
        for model in ("gemini-3-pro-image-preview", "gemini-3.1-flash-image"):
            try:
                req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_img.key()}",
                                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
                d = json.load(urllib.request.urlopen(req, timeout=300))
                for p in d["candidates"][0]["content"]["parts"]:
                    if "inlineData" in p:
                        open(raw, "wb").write(base64.b64decode(p["inlineData"]["data"])); break
                if os.path.exists(raw): break
            except Exception as e:
                print(f"  ! {name} {model}: {str(e)[:120]}")
                if "imageSize" in body["generationConfig"]["imageConfig"]:
                    del body["generationConfig"]["imageConfig"]["imageSize"]
    key(name)
    return name


def key(name, soft=18):
    """Chroma-key the green background to alpha, despill edges, crop."""
    raw = os.path.join(OUT, f"{name}_raw.png")
    im = Image.open(raw).convert("RGB")
    r, g, b = im.split()
    # greenness = g - max(r,b); background is strongly green
    import numpy as np
    a = np.asarray(im).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    green = G - np.maximum(R, B)
    alpha = np.clip((80 - green) * (255 / soft) / 255 * 255 / (80 / soft), 0, 255)  # ramps from 255 (green<=~62) to 0 (green>=80)
    alpha = np.clip((80 - green) * (255 / 40), 0, 255).astype("uint8")
    # despill: pull green down toward the average of r,b where alpha is partial
    # despill everywhere: green may never exceed the other channels by more than a little
    G2 = np.minimum(G, np.maximum(R, B) + 6).clip(0, 255)
    rgba = np.dstack([R, G2, B, alpha]).astype("uint8")
    out = Image.fromarray(rgba, "RGBA")
    bbox = out.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    out = out.crop(bbox)
    out.save(os.path.join(OUT, f"{name}.png"))
    return out.size


if __name__ == "__main__":
    names = sys.argv[1:] or list(ARTS)
    for n in sys.argv[1:]:
        p = os.path.join(OUT, n + "_raw.png")
        if os.path.exists(p): os.remove(p)
    with cf.ThreadPoolExecutor(3) as ex:
        for n in ex.map(generate, names):
            print("  ok", n, key(n))
