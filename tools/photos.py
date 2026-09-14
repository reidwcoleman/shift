"""Product + campaign photography with Gemini, using the mockups as print references.

    .venv/bin/python tools/photos.py            # everything missing
    .venv/bin/python tools/photos.py web_hoodie # one product
    .venv/bin/python tools/photos.py campaign   # hero shots only

photos/<key>_model_front.png / _model_back.png / _flat.png / _detail.png
photos/campaign_XX.png
"""
import os, sys, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(__file__))
import gemini_img

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK = os.path.join(ROOT, "mockups")
OUT = os.path.join(ROOT, "photos")
os.makedirs(OUT, exist_ok=True)
MODEL = "gemini-3-pro-image-preview"

FIDELITY = ("Reproduce the printed graphic from the reference image EXACTLY — identical artwork, identical words, spelling, layout and colors, "
            "nothing added, no extra text or logos anywhere. The garment color must match the reference.")

LOOK = ("Photorealistic editorial streetwear photography, shot on 35mm with on-camera flash at night, slight film grain, "
        "true-to-life skin, heavyweight boxy fit, natural pose, no watermark, no text overlays.")

TALENT = [
    "a 19 year old Black man with short twists and a silver chain",
    "a 20 year old white man with a buzzcut and a small hoop earring",
    "a 21 year old Latino man with dark curly hair and a thin mustache",
    "a 20 year old East Asian man with a middle part and a beanie pushed back",
    "a 22 year old mixed-race man with a low fade and a stud earring",
]
PLACES = [
    "an empty concrete parking garage lit by sodium-vapor lights",
    "a 24-hour laundromat with humming fluorescent light and rows of machines",
    "a gas station forecourt at 1 AM, canopy lights, wet asphalt",
    "an empty subway platform with tiled walls",
    "a rooftop at blue hour with the city skyline behind",
    "a diner counter at night with red neon in the window",
    "a loading dock behind a warehouse, roller door half open, one orange light",
    "a chain-link fence along a highway overpass at night, headlights streaking",
    "a stairwell with a flickering light and painted numbers on the wall",
]

PRODUCTS = ["sun_tee", "cherub_tee", "wings_tee", "hands_hoodie", "web_hoodie", "skeleton_tee", "hazard_hoodie", "timecard_tee", "moth_tee"]
GARMENT = {
    "sun_tee": "black heavyweight t-shirt", "cherub_tee": "bone/cream heavyweight t-shirt", "wings_tee": "black heavyweight t-shirt",
    "hands_hoodie": "black heavyweight pullover hoodie", "web_hoodie": "forest green heavyweight pullover hoodie",
    "skeleton_tee": "white heavyweight t-shirt", "hazard_hoodie": "black heavyweight pullover hoodie",
    "timecard_tee": "black heavyweight t-shirt", "moth_tee": "black heavyweight t-shirt",
}


def gen(out, prompt, refs, aspect):
    if os.path.exists(out):
        return out
    for model in (MODEL, "gemini-3.1-flash-image"):
        try:
            gemini_img.generate(prompt, refs, model=model, aspect=aspect, out=out)
            return out
        except Exception as e:
            print(f"  ! {os.path.basename(out)} {model}: {str(e)[:100]}")
    return None


def product_shots(key):
    i = PRODUCTS.index(key)
    talent = TALENT[i % len(TALENT)]
    place = PLACES[i % len(PLACES)]
    place2 = PLACES[(i + 4) % len(PLACES)]
    g = GARMENT[key]
    front = os.path.join(MOCK, f"{key}_front.png")
    back = os.path.join(MOCK, f"{key}_back.png")
    jobs = []
    jobs.append((os.path.join(OUT, f"{key}_model_front.png"),
                 f"{LOOK} {talent} wearing this exact {g} (front view shown in the reference), photographed from the front, three-quarter length, in {place}. {FIDELITY}",
                 [front], "4:5"))
    jobs.append((os.path.join(OUT, f"{key}_model_back.png"),
                 f"{LOOK} {talent} wearing this exact {g}, photographed from BEHIND so the full back print is visible and readable, three-quarter length, in {place2}. The reference shows the back of the garment. {FIDELITY}",
                 [back], "4:5"))
    jobs.append((os.path.join(OUT, f"{key}_flat.png"),
                 f"Top-down flat lay product photo of this exact {g} laid flat on a raw concrete floor, front side up, print fully visible, soft daylight, slight wrinkles, e-commerce quality, square crop. {FIDELITY}",
                 [front], "1:1"))
    jobs.append((os.path.join(OUT, f"{key}_detail.png"),
                 f"Extreme close-up macro photo of the screen-printed graphic on this exact {g}, showing ink texture on the cotton weave, shallow depth of field, moody studio light. {FIDELITY}",
                 [back if os.path.exists(back) and key not in ("sun_tee", "cherub_tee", "skeleton_tee") else front], "1:1"))
    for out, prompt, refs, aspect in jobs:
        gen(out, prompt, refs, aspect)
    return key


def campaign():
    shots = [
        ("campaign_01.png", "Three friends (a Black man, a white man and a Latino man, all around 20) standing shoulder to shoulder in an empty parking garage at night, harsh flash, wearing these exact pieces: the black hoodie with the hazard back print worn by the middle one seen from behind, the black sun-clock tee and the green splatter hoodie on the others. Cinematic, wide.",
         ["hazard_hoodie_back.png", "sun_tee_front.png", "web_hoodie_front.png"], "16:9"),
        ("campaign_02.png", "A young man sitting on the curb outside a 24-hour laundromat at 2 AM, phone light on his face, wearing this exact black hoodie with the praying-hands print. Flash photography, wide shot with the neon OPEN sign.",
         ["hands_hoodie_front.png"], "16:9"),
        ("campaign_03.png", "Close up from behind of a young man walking away down a wet street at night under sodium lights, wearing this exact black tee with the angel wings back print. Motion, grain, cinematic.",
         ["wings_tee_back.png"], "16:9"),
        ("campaign_04.png", "An old industrial punch-in time clock mounted on a brick wall, its hands at 11:59, a paper time card in the slot, harsh flash at night. Product-free mood shot, no text overlays.",
         [], "16:9"),
        ("campaign_05.png", "Flat lay from above of the whole collection on a concrete floor: three black tees, one cream tee, one white tee, two black hoodies and one green hoodie, folded and stacked, with a paper time card and a silver pocket watch on top. Soft daylight.",
         ["lookbook.png"], "4:5"),
    ]
    for name, prompt, refs, aspect in shots:
        gen(os.path.join(OUT, name), f"{LOOK} {prompt} {FIDELITY}", [os.path.join(MOCK, r) for r in refs], aspect)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["campaign"]:
        campaign()
    else:
        keys = args or PRODUCTS
        with cf.ThreadPoolExecutor(3) as ex:
            for k in ex.map(product_shots, keys):
                print("  ok", k)
        if not args:
            campaign()
