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
BL = os.path.join(ROOT, "photos", "blanks"); PR = os.path.join(ROOT, "designs", "print_worn")
OUT = os.path.join(ROOT, "photos", "first_shift"); os.makedirs(OUT, exist_ok=True)


def place(base, print_name, cx, top, width_in, ppi, opacity=0.96, patch=None, mask=None):
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
    g = ImageOps.grayscale(region)
    raw = np.asarray(g).astype(float) / 255
    lum = np.asarray(g.filter(ImageFilter.GaussianBlur(3))).astype(float) / 255
    med = max(np.median(lum), 0.05)
    shade = np.clip(lum / med, 0.5, 1.4)[..., None]
    a = np.asarray(art).astype(float)
    # fold displacement + weave: push the ink around by the cloth's gradient and add its texture back
    blur = np.asarray(g.filter(ImageFilter.GaussianBlur(6))).astype(float) / 255
    gy, gx = np.gradient(blur)
    yy, xx = np.mgrid[0:h, 0:w]
    ix = np.clip(xx - gx * 80, 0, w - 1).astype(int); iy = np.clip(yy - gy * 80, 0, h - 1).astype(int)
    a = a[iy, ix]
    weave = (raw - lum)[..., None] * 255 * 0.8
    rgb = np.clip(a[..., :3] * shade + weave, 0, 255)
    alpha = a[..., 3:4] / 255 * opacity
    if mask:  # occlusion: only paint where the garment is (hands, chains, hair stay on top)
        hsv = np.asarray(region.convert("HSV")).astype(float)
        H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
        if mask == "dark": m = (V < 95)
        elif mask == "light": m = (V > 150) & (S < 70)
        elif mask == "red": m = ((H < 20) | (H > 235)) & (S > 90) & (V > 60)
        else: m = np.ones_like(V, bool)
        m = Image.fromarray((m * 255).astype("uint8")).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2))
        alpha = alpha * (np.asarray(m).astype(float) / 255)[..., None]
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
    "hazard_hoodie": ("flat_b", "bl", [("30_hazard2_front", 515, 1360, 5.5, 31.7)]),
    "mesh_shorts": ("flat_c", "tl", [("26_mesh_left", 700, 510, 4, 25), ("26_mesh_right", 330, 510, 4, 25)]),
    "sweat_shorts": ("flat_c", "tr", [("27_sweat_left", 1700, 500, 5, 25)]),
    "hazard_hoodie_back": ("flat_c", "bl", [("30_hazard2_back", 505, 1400, 12, 31)]),
    "emblem_tee_back": ("flat_c", "br", [("29_emblem_back", 1515, 1230, 13, 27)]),
    "emblem_tee": ("flat_a", "bl", [("29_emblem_chest", 626, 1330, 4, 29.5)]),
    "racing_tee": ("flat_a", "br", [("31_racing_front", 1515, 1315, 12, 29)]),
    "graveyard_tee": ("flat_a", "bl", [("32_graveyard_front", 520, 1325, 12, 29.5)]),
    "owl_hoodie": ("flat_b", "bl", [("33_owl_chest", 640, 1380, 3.5, 31.7)]),
    "owl_hoodie_back": ("flat_c", "bl", [("33_owl_back", 505, 1400, 12, 31)]),
    "burnout_hoodie": ("flat_b", "bl", [("34_burnout_front", 515, 1300, 11, 31.7)]),
    "burnout_hoodie_back": ("flat_c", "bl", [("34_burnout_back", 505, 1400, 12, 31)]),
    "chrome_hoodie": ("flat_b", "bl", [("35_chrome_front", 515, 1310, 11, 31.7)]),
    "chrome_hoodie_back": ("flat_c", "bl", [("35_chrome_back", 505, 1400, 12, 31)]),
    "nosleep_hoodie": ("flat_b", "bl", [("36_nosleep_front", 640, 1380, 3.5, 31.7)]),
    "nosleep_hoodie_back": ("flat_c", "bl", [("36_nosleep_back", 505, 1400, 12, 31)]),
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
    "hazard_hoodie": ("model_e", (1350, 250, 2150, 1250), [("30_hazard2_back", 1750, 830, 13, 17.5, None)]),
    "racing_tee": ("model_a", (1271, 120, 2071, 1120), [("31_racing_front", 1671, 422, 12, 16.4, None)]),
    "graveyard_tee": ("model_b", (744, 150, 1544, 1150), [("32_graveyard_front", 1144, 476, 12, 17.9, None)]),
    "burnout_hoodie": ("model_e", (1350, 250, 2150, 1250), [("34_burnout_back", 1750, 830, 13, 17.5, None)]),
    "chrome_hoodie": ("model_e", (1350, 250, 2150, 1250), [("35_chrome_back", 1750, 830, 13, 17.5, None)]),
    "nosleep_hoodie": ("model_e", (1350, 250, 2150, 1250), [("36_nosleep_back", 1750, 830, 13, 17.5, None)]),
}


def retro(im, seed=1, warmth=1.0):
    """35mm film look: lifted blacks, warm cast, grain, soft vignette."""
    im = im.convert("RGB")
    a = np.asarray(im).astype(np.float32) / 255
    a = a * 0.86 + 0.07                       # lifted blacks / lower contrast
    a[..., 0] = np.clip(a[..., 0] * (1 + 0.05 * warmth), 0, 1)
    a[..., 2] = np.clip(a[..., 2] * (1 - 0.08 * warmth) + 0.02, 0, 1)
    a[..., 1] = np.clip(a[..., 1] + 0.01, 0, 1)
    rng = np.random.default_rng(seed)
    grain = rng.normal(0, 0.035, a.shape[:2]).astype(np.float32)[..., None]
    a = np.clip(a + grain, 0, 1)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    vig = np.clip(1 - 0.28 * np.clip(r - 0.55, 0, 1) ** 1.5, 0, 1)[..., None]
    a = a * vig
    return Image.fromarray((a * 255).astype("uint8"), "RGB")


# name: (blank, crop, [(print, seed, kind, width_in, side, drop_in, collar_override, ppi_override)], product)
POSES = {
    "league_lean": ("pose_lean", (300, 120, 1556, 1690), [("20_league_front", (916, 780), "red", 12, "center", 3.0, 582, 19.3)], "league_tee"),
    "cross_squat": ("pose_squat", (250, 150, 1650, 1900), [("22_cross_front", (964, 1000), "dark", 12, "center", 3.0, None, None)], "cross_tee"),
    "tigers_stairs": ("pose_stairs", (250, 100, 1650, 1850), [("21_tigers_front", (988, 950), "light", 12, "center", 3.0, None, None)], "tigers_tee"),
    "sundial_walk": ("pose_walk", (300, 100, 1556, 1670), [("23_sundial_front", (952, 900), "light", 12, "center", 3.0, 667, 22.7, 952)], "sundial_tee"),
    "hazard_hoodback": ("pose_hoodback", (300, 250, 1556, 1820), [("30_hazard2_back", (916, 1000), "dark", 13, "center", 3.0, 764, 17)], "hazard_hoodie"),
    "overtime_car": ("pose_car", (250, 250, 1650, 2000), [("24_thermal_front", (964, 1000), "dark", 11, "center", 3.0, None, None)], "overtime_thermal"),
    "emblem_squat": ("pose_squat", (250, 150, 1650, 1900), [("29_emblem_chest", (964, 1000), "dark", 3.5, "left", 2.5, None, None)], "emblem_tee"),
    "collage_walk": ("pose_walk", (300, 100, 1556, 1670), [("25_collage_front", (952, 900), "light", 12, "center", 3.0, 667, 22.7, 952)], "collage_thermal"),
    "racing_garage": ("pose_garage", (100, 120, 1692, 2110), [("31_racing_front", (936, 1000), "light", 12, "center", 3.0, None, None)], "racing_tee"),
    "graveyard_laundro": ("pose_laundro", (100, 120, 1692, 2110), [("32_graveyard_front", (954, 900), "dark", 12, "center", 3.0, None, None)], "graveyard_tee"),
    "owl_roof": ("pose_roof", (100, 120, 1692, 2110), [("33_owl_back", (945, 1150), "dark", 13, "center", 3.0, 886, 18)], "owl_hoodie"),
    "burnout_bodega": ("pose_bodega", (100, 120, 1692, 2110), [("34_burnout_front", (908, 900), "dark", 11, "center", 3.0, 622, 26)], "burnout_hoodie"),
    "chrome_alley": ("pose_alley", (0, 500, 1536, 2420), [("35_chrome_back", (786, 1500), "dark", 12, "center", 3.0, 1212, 21)], "chrome_hoodie"),
    "nosleep_hoodback": ("pose_hoodback", (300, 250, 1556, 1820), [("36_nosleep_back", (916, 1000), "dark", 13, "center", 3.0, 764, 17)], "nosleep_hoodie"),
    "tigers_stoop": ("pose_stoop", (100, 120, 1692, 2110), [("21_tigers_front", (796, 1194), "light", 12, "center", 3.0, None, None)], "tigers_tee"),
    "nosleep_shutter": ("pose_shutter", (100, 120, 1692, 2110), [("36_nosleep_front", (915, 796), "dark", 3.5, "left", 2.5, 600, 21)], "nosleep_hoodie"),
}

# model group shots: (blank, crop, [(print, seed, kind, width_in, side, drop_in, collar_override, ppi_override)])
MODELS2 = {
    "league_tee": ("model_a", (725, 120, 1525, 1120), [("20_league_front", (1125, 560), "red", 12, "center", 3.0, None, None)]),
    "tigers_tee": ("model_a", (1271, 120, 2071, 1120), [("21_tigers_front", (1671, 550), "light", 12, "center", 3.0, None, None)]),
    "racing_tee": ("model_a", (1271, 120, 2071, 1120), [("31_racing_front", (1671, 550), "light", 12, "center", 3.0, None, None)]),
    "cross_tee": ("model_b", (744, 150, 1544, 1150), [("22_cross_front", (1144, 600), "dark", 12, "center", 3.0, None, None)]),
    "graveyard_tee": ("model_b", (744, 150, 1544, 1150), [("32_graveyard_front", (1144, 600), "dark", 12, "center", 3.0, None, None)]),
    "emblem_tee": ("model_b", (744, 150, 1544, 1150), [("29_emblem_chest", (1144, 600), "dark", 3.5, "left", 2.5, None, None)]),
    "sundial_tee": ("model_b", (1271, 150, 2071, 1150), [("23_sundial_front", (1671, 600), "light", 12, "center", 3.0, None, None)]),
    "overtime_thermal": ("model_c", (787, 130, 1587, 1130), [("24_thermal_front", (1187, 560), "dark", 11, "center", 3.0, None, None)]),
    "collage_thermal": ("model_c", (1202, 130, 2002, 1130), [("25_collage_front", (1602, 560), "light", 12, "center", 3.0, None, None)]),
    "hazard_hoodie": ("model_e", (1350, 250, 2150, 1250), [("30_hazard2_back", (1750, 950), "dark", 13, "center", 3.0, 777, 17.5)]),
    "owl_hoodie": ("model_e", (1350, 250, 2150, 1250), [("33_owl_back", (1750, 950), "dark", 13, "center", 3.0, 777, 17.5)]),
    "burnout_hoodie": ("model_e", (1350, 250, 2150, 1250), [("34_burnout_back", (1750, 950), "dark", 13, "center", 3.0, 777, 17.5)]),
    "chrome_hoodie": ("model_e", (1350, 250, 2150, 1250), [("35_chrome_back", (1750, 950), "dark", 13, "center", 3.0, 777, 17.5)]),
    "nosleep_hoodie": ("model_e", (1350, 250, 2150, 1250), [("36_nosleep_back", (1750, 950), "dark", 13, "center", 3.0, 777, 17.5)]),
}


def fit_all(im, places):
    from fit import fit_print
    for pl in places:
        pr, seed, kind, win, side, drop, collar, ppi = pl[:8]; cx = pl[8] if len(pl) > 8 else None
        try: fit_print(im, pr, seed, kind, width_in=win, drop_in=drop, side=side, collar=collar, ppi=ppi, cx=cx)
        except Exception as e: print("   !", pr, e)


def run_poses():
    for name, (bn, box, places, prod) in POSES.items():
        im = Image.open(os.path.join(BL, bn + ".png")).convert("RGB")
        fit_all(im, places)
        out = retro(im.crop(box), seed=abs(hash(name)) % 1000)
        out.save(os.path.join(OUT, f"{name}.jpg"), quality=92)
        print("  pose", name)


def run_models():
    for prod, (bn, box, places) in MODELS2.items():
        im = Image.open(os.path.join(BL, bn + ".png")).convert("RGB")
        fit_all(im, places)
        retro(im.crop(box), seed=len(prod)).save(os.path.join(OUT, f"{prod}_model.jpg"), quality=92)
        print("  model", prod)


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
    for prod in ("mesh_shorts", "sweat_shorts"):
        bn, box, places = MODELS[prod]
        im = blank(bn)
        for pr, cx, top, win, ppi, patch in places: place(im, pr, cx, top, win, ppi, patch=patch)
        retro(im.crop(box), seed=len(prod)).save(os.path.join(OUT, f"{prod}_model.jpg"), quality=92)
    run_models()
    # the shared group shots with prints applied
    for bn, spec in (("model_a", ["league_tee", "tigers_tee"]), ("model_b", ["cross_tee", "sundial_tee"]), ("model_c", ["overtime_thermal", "collage_thermal"]), ("model_e", ["burnout_hoodie"])):
        im = blank(bn)
        for prod in spec: fit_all(im, MODELS2[prod][2])
        retro(im, seed=7).save(os.path.join(OUT, f"group_{bn[-1]}.jpg"), quality=90)
    print("done")


if __name__ == "__main__":
    if "poses" in sys.argv: run_poses()
    else: run(); run_poses()
