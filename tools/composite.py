"""Composite the real print files onto the Gemini blank-garment photos (photos/blanks/*).

    .venv/bin/python tools/composite.py

Output: photos/first_shift/<product>_flat.jpg (white-background e-comm shot) and <product>_model.jpg
Placement table below = (blank image, print png, centre x, top y, print width in inches, pixels per inch).
Shading: the print is multiplied by the garment's local luminance so folds and flash falloff carry through.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageFilter, ImageOps
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BL = os.path.join(ROOT, "photos", "blanks"); PR = os.path.join(ROOT, "designs", "print")
OUT = os.path.join(ROOT, "photos", "first_shift"); os.makedirs(OUT, exist_ok=True)


def place(base, print_name, cx, top, width_in, ppi, opacity=0.96, patch=None):
    """Paste designs/print/<print_name>.png onto base (RGB) with garment shading."""
    art = Image.open(os.path.join(PR, print_name + ".png")).convert("RGBA")
    w = int(width_in * ppi); h = int(art.height * w / art.width)
    art = art.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.5))
    x0, y0 = int(cx - w / 2), int(top)
    region = base.crop((x0, y0, x0 + w, y0 + h)).convert("RGB")
    if patch:  # hide something on the blank (e.g. a stray logo) with the local garment colour
        px, py, pw, ph = patch
        ring = np.asarray(base.crop((px - 20, py - 20, px + pw + 20, py + ph + 20))).reshape(-1, 3)
        col = tuple(int(v) for v in np.median(ring, axis=0))
        mask = Image.new("L", (pw + 40, ph + 40), 0)
        from PIL import ImageDraw
        ImageDraw.Draw(mask).rounded_rectangle((12, 12, pw + 28, ph + 28), radius=14, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(6))
        base.paste(Image.new("RGB", mask.size, col), (px - 20, py - 20), mask)
        region = base.crop((x0, y0, x0 + w, y0 + h)).convert("RGB")
    lum = np.asarray(ImageOps.grayscale(region).filter(ImageFilter.GaussianBlur(3))).astype(float) / 255
    med = max(np.median(lum), 0.05)
    shade = np.clip(lum / med, 0.5, 1.4)[..., None]
    a = np.asarray(art).astype(float)
    rgb = np.clip(a[..., :3] * shade, 0, 255)
    alpha = a[..., 3:4] / 255 * opacity
    out = np.asarray(region).astype(float) * (1 - alpha) + rgb * alpha
    base.paste(Image.fromarray(out.astype("uint8"), "RGB"), (x0, y0))
    return base


def quadrant(img, q):
    w, h = img.size; hw, hh = w // 2, h // 2
    x, y = {"tl": (0, 0), "tr": (hw, 0), "bl": (0, hh), "br": (hw, hh)}[q]
    return img.crop((x, y, x + hw, y + hh))


FLATS = {
    # product: (blank, quadrant, [(print, cx, top, width_in, ppi)])
    "league_tee": ("flat_a", "tl", [("20_league_front", 515, 315, 12, 29)]),
    "tigers_tee": ("flat_a", "tr", [("21_tigers_front", 1515, 305, 12, 30)]),
    "cross_tee": ("flat_a", "bl", [("22_cross_front", 520, 1325, 12, 29.5)]),
    "sundial_tee": ("flat_a", "br", [("23_sundial_front", 1515, 1315, 12, 29)]),
    "overtime_thermal": ("flat_b", "tl", [("24_thermal_front", 515, 290, 11, 27)]),
    "collage_thermal": ("flat_b", "tr", [("25_collage_front", 1525, 270, 12, 26)]),
    "hazard_hoodie": ("flat_b", "bl", [("06_hazard_badge_white", 515, 1380, 5, 31.7)]),
    "beanie": ("flat_b", "br", [("28_beanie", 1540, 1690, 3.5, 96)]),
    "mesh_shorts": ("flat_c", "tl", [("26_mesh_left", 700, 510, 4, 25), ("26_mesh_right", 330, 510, 4, 25)]),
    "sweat_shorts": ("flat_c", "tr", [("27_sweat_left", 1700, 500, 5, 25)]),
    "hazard_hoodie_back": ("flat_c", "bl", [("06_hazard_back_white", 505, 1400, 12, 31)]),
    "emblem_tee_back": ("flat_c", "br", [("29_emblem_back", 1515, 1230, 13, 27)]),
    "emblem_tee": ("flat_a", "bl", [("29_emblem_chest", 626, 1330, 4, 29.5)]),
}

MODELS = {
    # product: (blank, crop box (4:5 around the person), [(print, cx, top, width_in, ppi, patch)])
    "league_tee": ("model_a", (725, 120, 1525, 1120), [("20_league_front", 1125, 435, 12, 16.4, None)]),
    "tigers_tee": ("model_a", (1271, 120, 2071, 1120), [("21_tigers_front", 1671, 422, 12, 16.4, None)]),
    "cross_tee": ("model_b", (744, 150, 1544, 1150), [("22_cross_front", 1144, 476, 12, 17.9, None)]),
    "sundial_tee": ("model_b", (1271, 150, 2071, 1150), [("23_sundial_front", 1671, 464, 12, 18.1, None)]),
    "emblem_tee": ("model_b", (744, 150, 1544, 1150), [("29_emblem_chest", 1208, 480, 4, 17.9, None)]),
    "overtime_thermal": ("model_c", (787, 130, 1587, 1130), [("24_thermal_front", 1187, 450, 11, 12.5, None)]),
    "collage_thermal": ("model_c", (1202, 130, 2002, 1130), [("25_collage_front", 1602, 436, 12, 14.7, None)]),
    "mesh_shorts": ("model_d", (740, 350, 1540, 1350), [("26_mesh_left", 1031, 935, 4, 13.6, None), ("26_mesh_right", 1240, 935, 4, 13.6, (1226, 940, 46, 40))]),
    "sweat_shorts": ("model_d", (1312, 350, 2112, 1350), [("27_sweat_left", 1712, 905, 5, 14.5, None)]),
    "beanie": ("model_e", (697, 100, 1497, 1100), [("28_beanie", 1097, 432, 3.5, 30, None)]),
    "hazard_hoodie": ("model_e", (1350, 250, 2150, 1250), [("06_hazard_back_white", 1750, 830, 13, 17.5, None)]),
}


def run():
    cache = {}
    def blank(n):
        if n not in cache: cache[n] = Image.open(os.path.join(BL, n + ".png")).convert("RGB")
        return cache[n].copy()
    for prod, (bn, q, places) in FLATS.items():
        im = blank(bn)
        for pr, cx, top, win, ppi in places: place(im, pr, cx, top, win, ppi)
        quadrant(im, q).save(os.path.join(OUT, f"{prod}_flat.jpg"), quality=92)
        print("  flat", prod)
    for prod, (bn, box, places) in MODELS.items():
        im = blank(bn)
        for pr, cx, top, win, ppi, patch in places: place(im, pr, cx, top, win, ppi, patch=patch)
        im.crop(box).save(os.path.join(OUT, f"{prod}_model.jpg"), quality=92)
        print("  model", prod)
    # the shared group shots with prints applied
    for bn, spec in (("model_a", ["league_tee", "tigers_tee"]), ("model_b", ["cross_tee", "sundial_tee"]), ("model_c", ["overtime_thermal", "collage_thermal"]),
                     ("model_d", ["mesh_shorts", "sweat_shorts"]), ("model_e", ["beanie", "hazard_hoodie"])):
        im = blank(bn)
        for prod in spec:
            for pr, cx, top, win, ppi, patch in MODELS[prod][2]: place(im, pr, cx, top, win, ppi, patch=patch)
        im.save(os.path.join(OUT, f"group_{bn[-1]}.jpg"), quality=90)
    print("done")


if __name__ == "__main__":
    run()
