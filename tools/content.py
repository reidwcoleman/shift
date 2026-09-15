"""Instagram launch content pack: Gemini world-building shots + code-made text posts + captions.

    .venv/bin/python tools/content.py

content/posts/NN_name.jpg   1080x1350 feed posts (4:5)
content/stories/*.png       1080x1920 story templates
content/CAPTIONS.md         caption + hashtags per post
"""
import os, sys, json, shutil, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from shiftlib import *
import gemini_img
from PIL import Image

MOCK = os.path.join(ROOT, "mockups"); PH = os.path.join(ROOT, "photos"); BR = os.path.join(ROOT, "brand")
OUT = os.path.join(ROOT, "content"); POSTS = os.path.join(OUT, "posts"); STORIES = os.path.join(OUT, "stories")
for d in (POSTS, STORIES): os.makedirs(d, exist_ok=True)
MODEL = "gemini-3-pro-image-preview"
LOOK = "Photorealistic, shot on 35mm with on-camera flash at night, film grain, no text overlays, no watermark."
FID = "Reproduce any printed graphic from the reference exactly; add no extra text or logos."


def gen(name, prompt, refs=(), aspect="4:5"):
    out = os.path.join(POSTS, name + ".png")
    import glob
    prev = glob.glob(os.path.join(POSTS, f"*_{name}.jpg"))
    if prev and not os.path.exists(out):
        Image.open(prev[0]).convert("RGB").save(out)
    if not os.path.exists(out):
        for model in (MODEL, "gemini-3.1-flash-image"):
            try:
                gemini_img.generate(f"{LOOK} {prompt} {FID}", refs, model=model, aspect=aspect, out=out); break
            except Exception as e:
                print("  !", name, model, str(e)[:100])
    return out


GEMINI_POSTS = [
    ("teaser_clock", "An old industrial punch-in time clock on a brick wall, hands at exactly 11:59, a paper time card in the slot, one bare bulb above it, harsh flash. Moody, cinematic, vertical.", []),
    ("teaser_arrow", "This exact arrow symbol spray-painted in white on a raw concrete wall in a parking garage at night, drips running down, harsh flash, a sodium light in the corner. The arrow is the only thing on the wall.", [os.path.join(BR, "mark_white.png")]),
    ("day1_desk", "Top-down photo of a messy desk at 2 AM: an open laptop showing this exact t-shirt graphic on screen, an energy drink can, a paper employee time card, a sketchbook with pen, a phone face down, warm lamp light. Documentary feel.", [os.path.join(MOCK, "sun_tee_front.png")]),
    ("unboxing", "Close-up of hands opening a matte black poly mailer on a wooden table, a folded black heavyweight t-shirt inside with a small white arrow sticker (this exact symbol) on the tissue paper, flash photography.", [os.path.join(BR, "mark_white.png")]),
    ("stairwell", "A young man sitting alone on the steps of a concrete stairwell under a flickering fluorescent light, hood up, looking at his phone, wearing this exact black hoodie with the praying hands print. Vertical, flash, grain.", [os.path.join(MOCK, "hands_hoodie_front.png")]),
    ("gas_station", "Two young men leaning against a car at a gas station at 1 AM under the canopy lights, one wearing this exact green hoodie seen from the front, the other this exact black tee seen from behind, laughing, candid, flash.", [os.path.join(MOCK, "web_hoodie_front.png"), os.path.join(MOCK, "wings_tee_back.png")]),
    ("laundromat_fold", "Inside a 24-hour laundromat, a stack of freshly folded black and cream heavyweight t-shirts on top of a washing machine, the top one showing this exact print, fluorescent light, vertical.", [os.path.join(MOCK, "cherub_tee_front.png")]),
    ("rooftop", "A young man on a rooftop at blue hour, city skyline behind him, back to camera, wearing this exact black tee with the moth back print, wind in the fabric. Cinematic vertical.", [os.path.join(MOCK, "moth_tee_back.png")]),
]

REUSE = [  # product photos that go straight into the feed (photos/first_shift)
    ("hazard_back", "first_shift/hazard_hoodie_model.jpg"), ("sun_front", "first_shift/league_tee_model.jpg"),
    ("web_back", "first_shift/tigers_tee_model.jpg"), ("cherub_front", "first_shift/cross_tee_model.jpg"),
    ("timecard_back", "first_shift/overtime_thermal_model.jpg"), ("skeleton_front", "first_shift/mesh_shorts_model.jpg"),
    ("group_a", "first_shift/group_a.jpg"), ("group_e", "first_shift/group_e.jpg"),
]


def text_post(name, lines, sub=None, bg=INK, fg=WHITE, accent=SIGNAL, story=False):
    w, h = (1080, 1920) if story else (1080, 1350)
    body = [f'<rect width="{w}" height="{h}" fill="{bg}"/>']
    n = len(lines); size = min(230, int(1000 / max(len(l) for l in lines) * 1.55))
    total = n * size * 0.92
    y0 = h / 2 - total / 2 + size * 0.82
    for i, l in enumerate(lines):
        col = accent if l.startswith("*") else fg
        body.append(text("Anton", l.strip("*"), size, w / 2, y0 + i * size * 0.92, col))
    if sub:
        body.append(text("Bebas Neue", sub, 44, w / 2, y0 + n * size * 0.92 + 40, CONCRETE, tracking=0.35))
    body.append(shift_mark(w / 2 - 30, 90, 60, accent))
    body.append(text("Bebas Neue", "SHIFT WORLDWIDE  •  NIGHT SHIFT DIVISION", 34, w / 2, h - 80, CONCRETE, tracking=0.3))
    p = os.path.join(STORIES if story else POSTS, name + ".svg")
    open(p, "w").write(svg_doc(w, h, "".join(body)))
    png = p.replace(".svg", ".png"); render(p, png); os.remove(p)
    return png


TEXT_POSTS = [
    ("rules", ["36 PIECES.", "48 HOURS.", "*NEVER", "*RESTOCKED."], "FIRST SHIFT — CLOCK IN"),
    ("date", ["FIRST SHIFT", "*10.09", "11:59 PM"], "THE LIST GETS IN AT 10:59"),
    ("manifesto", ["NOBODY CLAPS", "FOR THE HOURS", "BETWEEN", "*MIDNIGHT", "*AND FIVE."], "THAT'S THE SHIFT"),
    ("noreverse", ["WAKE.", "WORK.", "WIN.", "REPEAT.", "*NO REVERSE."], "MANUAL ONLY"),
]

CAPTIONS = {
    "teaser_clock": "11:59.\n\nSomething's clocking in. 10.09.\n\n#shiftworldwide #nightshiftdivision #streetwear #drop001",
    "teaser_arrow": "⇧\n\nYou'll know it when you see it.\n\n#shiftworldwide #streetwear #graphictees #nightshift",
    "day1_desk": "Day 1. No brand yet, just a laptop, a time card and a name.\n\nWe make heavyweight tees and hoodies for the people still working after everyone went home. Eleven pieces drop 10.09 at 11:59 PM. 36 of each. Never restocked.\n\nFollow along. This is the whole thing, start to finish.\n\n#startingaclothingbrand #streetwearbrand #shiftworldwide #smallbrand #graphictees",
    "unboxing": "First sample came in. Heavy. The ⇧ sticker goes in every order.\n\n#shiftworldwide #unboxing #streetwear #heavyweighttee",
    "stairwell": "2:41 AM. Pray for overtime.\n\nOVERTIME HOODIE — Drop 001 — 10.09\n\n#shiftworldwide #nightshiftdivision #hoodie #streetwearfits",
    "gas_station": "Nobody's home. Nobody's asleep either.\n\nCAUGHT UP HOODIE + GUARDIAN TEE — 10.09\n\n#shiftworldwide #streetwear #fitcheck #nightshift",
    "laundromat_fold": "Bone. 7.5 oz. Cherubs carrying the punch clock.\n\nCHERUB TEE — Drop 001\n\n#shiftworldwide #graphictee #heavyweight #streetwearbrand",
    "rooftop": "Drawn to the light.\n\nMOTH TEE — full back print — 10.09\n\n#shiftworldwide #backprint #streetwear #nightshiftdivision",
    "hazard_back": "HAZARD HOODIE. 450 GSM. Badge on the chest, hazard band across the shoulders, DO NOT CROSS down the back.\n\nFirst Shift — 10.09 — 11:59 PM. Link in bio for early access.\n\n#shiftworldwide #hoodie #streetwear #drop #nightshiftdivision",
    "sun_front": "The hero. LEAGUE RINGER TEE.\n\nCardinal red, gold rib, three-color tiger crest. Est. 2002. 36 made.\n\n#shiftworldwide #ringertee #streetwear #varsity",
    "web_back": "Every hour counts.\n\nTWIN TIGERS TEE — natural, 250 GSM, sepia and rust.\n\n#shiftworldwide #graphictee #streetwearbrand #tigers",
    "cherub_front": "Time is money.\n\nTIME IS MONEY TEE — a cross built from time cards and dollar bills, stamped LATE.\n\n#shiftworldwide #graphictee #streetwear",
    "timecard_back": "Pray for overtime.\n\nOVERTIME THERMAL — 340 GSM waffle, chrome script, drips.\n\n#shiftworldwide #thermal #streetwear #winterfits",
    "skeleton_front": "Division issue.\n\nMESH SHORTS — NSD shield, wordmark, stars. Size up for boxy.\n\n#shiftworldwide #meshshorts #streetwear",
    "group_a": "First Shift. Eleven pieces. 10.09.\n\n#shiftworldwide #streetwear #lookbook #nightshiftdivision",
    "group_e": "Last call.\n\nHAZARD HOODIE — 10.09\n\n#shiftworldwide #hoodie #streetwear",
    "rules": "The rules.\n\n36 of each piece. The store is open for 48 hours. We never restock. If you own it, you were there.\n\n#shiftworldwide #drop001 #streetwear #limited",
    "date": "Save it. 10.09. 11:59 PM.\n\nThe list gets the password at 10:59. Link in bio.\n\n#shiftworldwide #drop #streetwearbrand",
    "manifesto": "Nobody claps for the hours between midnight and five. That's the shift.\n\n#shiftworldwide #nightshiftdivision #motivation #grind",
    "noreverse": "Wake. Work. Win. Repeat. No reverse.\n\n#shiftworldwide #noreverse #streetwear #manualonly",
}

ORDER = ["day1_desk", "teaser_arrow", "manifesto", "teaser_clock", "unboxing", "rules", "sun_front", "group_a", "hazard_back",
         "web_back", "cherub_front", "noreverse", "timecard_back", "skeleton_front", "group_e", "rooftop", "stairwell", "date"]


def to_jpg(src, dst, size=(1080, 1350)):
    im = Image.open(src).convert("RGB")
    # cover-crop to 4:5
    tw, th = size; r = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l, t = (im.width - tw) // 2, (im.height - th) // 2
    im.crop((l, t, l + tw, t + th)).save(dst, quality=90)


if __name__ == "__main__":
    for name, prompt, refs in GEMINI_POSTS:
        gen(name, prompt, refs)
    for name, lines, sub in TEXT_POSTS:
        text_post(name, lines, sub)
    for name, src in REUSE:
        p = os.path.join(PH, src)
        if os.path.exists(p): Image.open(p).convert("RGB").save(os.path.join(POSTS, name + ".png"))
    # stories
    text_post("story_countdown", ["FIRST SHIFT", "*10.09", "11:59 PM", "", "THE LIST", "GETS IN", "AT 10:59"], "LINK IN BIO", story=True)
    text_post("story_comment", ["COMMENT", "*SHIFT", "FOR THE", "LINK"], "EARLY ACCESS", story=True)
    text_post("story_soldout", ["*SOLD OUT", "IN 40", "MINUTES."], "THANK YOU — NEVER RESTOCKED", story=True)
    # final numbered jpgs + captions
    md = ["# SHIFT — Launch captions\n", "Post in this order, one per day (Reels in between — see INSTAGRAM.md).\n"]
    for i, name in enumerate(ORDER, 1):
        src = os.path.join(POSTS, name + ".png")
        if not os.path.exists(src): continue
        dst = os.path.join(POSTS, f"{i:02d}_{name}.jpg"); to_jpg(src, dst); os.remove(src)
        md.append(f"## {i:02d} — {name}\n`content/posts/{i:02d}_{name}.jpg`\n\n```\n{CAPTIONS[name]}\n```\n")
    open(os.path.join(OUT, "CAPTIONS.md"), "w").write("\n".join(md))
    print("content pack:", len(ORDER), "posts")
