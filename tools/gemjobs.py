"""Job list for print placement through gemini.google.com (driven from Chrome by Claude).

    .venv/bin/python tools/gemjobs.py prep      # write the blank crops to photos/refs/
    .venv/bin/python tools/gemjobs.py list      # pending jobs
    .venv/bin/python tools/gemjobs.py NAME      # print JSON {out, blank, print, prompt} for one job

Standard screen-print placements (what a printer does by default):
  front       full front, centred, top edge 3 in below the collar seam, 12 in wide
  front_hood  hoodie front, centred, top edge 2.5 in below the hood seam, 11 in wide, above the pocket
  left_chest  wearer's left chest, 3.5 in wide, top 3 in below the collar, ~4 in off centre
  back        full back, centred between the shoulder blades, top edge 3 in below the collar, 13 in wide
  back_hood   same on a hoodie, 3-4 in under the hood seam
  leg         shorts, one 4 in print on the wearer's left thigh above the hem
"""
import os, sys, json
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BL = os.path.join(ROOT, "photos", "blanks"); REF = os.path.join(ROOT, "photos", "refs"); OUT = os.path.join(ROOT, "photos", "gem")
os.makedirs(REF, exist_ok=True); os.makedirs(OUT, exist_ok=True)

PL = {
    "front":      "a full front print: centred left-to-right on the chest, its top edge about 3 inches below the collar seam, about 12 inches wide (a little over half the width of the chest)",
    "front_hood": "a front print on the hoodie: centred left-to-right, its top edge about 2.5 inches below the hood seam, about 11 inches wide, sitting entirely above the kangaroo pocket",
    "front_hood_small": "a small front print on the hoodie: centred left-to-right, about 5 inches wide, its top edge about 3 inches below the hood seam, above the kangaroo pocket",
    "left_chest": "a small left-chest print (on the wearer's left, so on the viewer's right when seen from the front): about 3.5 inches wide, its top edge about 3 inches below the collar seam, its centre about 4 inches to the side of the centre line, where a polo logo sits",
    "back":       "a full back print: centred between the shoulder blades, its top edge about 3 inches below the collar seam, about 13 inches wide",
    "back_hood":  "a full back print on the hoodie: centred between the shoulder blades, its top edge about 4 inches below the hood seam so the whole print is visible under the hood, about 13 inches wide, ending well above the waistband",
    "leg":        "one small print on the wearer's left leg of the shorts: about 4 inches wide, centred on the thigh, just above the hem",
    "legs":       "one small print on each leg of the shorts: about 4 inches wide, centred on each thigh just above the hem — the first print file on the wearer's left leg, the second on the wearer's right leg",
}

# crops of the blank photos (name -> (blank, box))
CROPS = {
    "flat_tl": ("flat_a", (0, 0, 1024, 1024)), "flat_tr": ("flat_a", (1024, 0, 2048, 1024)),
    "flat_bl": ("flat_a", (0, 1024, 1024, 2048)), "flat_br": ("flat_a", (1024, 1024, 2048, 2048)),
    "flatb_tl": ("flat_b", (0, 0, 1024, 1024)), "flatb_tr": ("flat_b", (1024, 0, 2048, 1024)), "flatb_bl": ("flat_b", (0, 1024, 1024, 2048)),
    "flatc_tl": ("flat_c", (0, 0, 1024, 1024)), "flatc_tr": ("flat_c", (1024, 0, 2048, 1024)),
    "flatc_bl": ("flat_c", (0, 1024, 1024, 2048)), "flatc_br": ("flat_c", (1024, 1024, 2048, 2048)),
    "model_a_l": ("model_a", (725, 120, 1525, 1120)), "model_a_r": ("model_a", (1271, 120, 2071, 1120)),
    "model_b_l": ("model_b", (744, 150, 1544, 1150)), "model_b_r": ("model_b", (1271, 150, 2071, 1150)),
    "model_c_l": ("model_c", (787, 130, 1587, 1130)), "model_c_r": ("model_c", (1202, 130, 2002, 1130)),
    "model_d_l": ("model_d", (740, 350, 1540, 1350)), "model_d_r": ("model_d", (1312, 350, 2112, 1350)),
    "model_e": ("model_e", (1350, 250, 2150, 1250)),
    "pose_lean": ("pose_lean", (300, 120, 1556, 1690)), "pose_squat": ("pose_squat", (250, 150, 1650, 1900)),
    "pose_stairs": ("pose_stairs", (250, 100, 1650, 1850)), "pose_walk": ("pose_walk", (300, 100, 1556, 1670)),
    "pose_hoodback": ("pose_hoodback", (300, 250, 1556, 1820)), "pose_car": ("pose_car", (250, 250, 1650, 2000)),
    "pose_garage": ("pose_garage", (100, 120, 1692, 2110)), "pose_laundro": ("pose_laundro", (100, 120, 1692, 2110)),
    "pose_roof": ("pose_roof", (100, 120, 1692, 2110)), "pose_bodega": ("pose_bodega", (100, 120, 1692, 2110)),
    "pose_alley": ("pose_alley", (0, 500, 1536, 2420)), "pose_stoop": ("pose_stoop", (100, 120, 1692, 2110)),
    "pose_shutter": ("pose_shutter", (100, 120, 1692, 2110)),
}

TEE = "heavyweight boxy t-shirt"; HOOD = "heavyweight pullover hoodie"; LS = "heavyweight long-sleeve t-shirt"
# out name: (crop, print(s), garment description, placement)
JOBS = {
    # tees
    "league_tee_flat":     ("flat_tl", "20_league_front", f"cardinal red ringer {TEE} with yellow collar and cuffs, flat-lay product photo on white", "front"),
    "league_tee_model":    ("model_a_l", "20_league_front", f"cardinal red ringer {TEE}, worn by a young man, seen from the front", "front"),
    "league_lean":         ("pose_lean", "20_league_front", f"cardinal red ringer {TEE}, worn by a young man leaning on a graffiti wall", "front"),
    "tigers_tee_flat":     ("flat_tr", "21_tigers_front", f"natural cream {TEE}, flat-lay product photo on white", "front"),
    "tigers_tee_model":    ("model_a_r", "21_tigers_front", f"natural cream {TEE}, worn by a young man, seen from the front", "front"),
    "tigers_stoop":        ("pose_stoop", "21_tigers_front", f"natural cream {TEE}, worn by a young man sitting on a stoop", "front"),
    "tigers_stairs":       ("pose_stairs", "21_tigers_front", f"natural cream {TEE}, worn by a young woman sitting on brownstone stairs", "front"),
    "cross_tee_flat":      ("flat_bl", "22_cross_front", f"black {TEE}, flat-lay product photo on white", "front"),
    "cross_tee_model":     ("model_b_l", "22_cross_front", f"black {TEE}, worn by a young man, seen from the front", "front"),
    "cross_squat":         ("pose_squat", "22_cross_front", f"black {TEE}, worn by a young man squatting in front of a brick wall", "front"),
    "sundial_tee_flat":    ("flat_br", "23_sundial_front", f"bone white {TEE}, flat-lay product photo on white", "front"),
    "sundial_tee_model":   ("model_b_r", "23_sundial_front", f"bone white {TEE}, worn by a young man, seen from the front", "front"),
    "sundial_walk":        ("pose_walk", "23_sundial_front", f"bone white {TEE}, worn by a young man walking on a city street", "front"),
    "emblem_tee_model":    ("model_b_l", "29_emblem_chest", f"black {TEE}, worn by a young man, seen from the front", "left_chest"),
    "emblem_squat":        ("pose_squat", "29_emblem_chest", f"black {TEE}, worn by a young man squatting in front of a brick wall", "left_chest"),
    "emblem_tee_back_flat":("flatc_br", "29_emblem_back", f"black {TEE} laid out showing its back, flat-lay product photo on white", "back"),
    "emblem_tee_flat":     ("flat_bl", "29_emblem_chest", f"black {TEE}, flat-lay product photo on white", "left_chest"),
    "racing_tee_flat":     ("flat_br", "31_racing_front", f"cream {TEE}, flat-lay product photo on white", "front"),
    "racing_tee_model":    ("model_a_r", "31_racing_front", f"cream {TEE}, worn by a young man, seen from the front", "front"),
    "racing_garage":       ("pose_garage", "31_racing_front", f"cream {TEE}, worn by a young man sitting on the hood of a car in a garage", "front"),
    "graveyard_tee_flat":  ("flat_bl", "32_graveyard_front", f"black {TEE}, flat-lay product photo on white", "front"),
    "graveyard_tee_model": ("model_b_l", "32_graveyard_front", f"black {TEE}, worn by a young man, seen from the front", "front"),
    "graveyard_laundro":   ("pose_laundro", "32_graveyard_front", f"black {TEE}, worn by a young man standing in front of a laundromat at night", "front"),
    # long sleeves
    "overtime_thermal_flat":  ("flatb_tl", "24_thermal_front", f"black {LS}, flat-lay product photo on white", "front"),
    "overtime_thermal_model": ("model_c_l", "24_thermal_front", f"black {LS}, worn by a young man, seen from the front", "front"),
    "overtime_car":           ("pose_car", "24_thermal_front", f"black {LS}, worn by a young man sitting on a car at a gas station", "front"),
    "collage_thermal_flat":   ("flatb_tr", "25_collage_front", f"white {LS}, flat-lay product photo on white", "front"),
    "collage_thermal_model":  ("model_c_r", "25_collage_front", f"white {LS}, worn by a young man, seen from the front", "front"),
    "collage_walk":           ("pose_walk", "25_collage_front", f"white {LS}, worn by a young man walking on a city street", "front"),
    # hoodies
    "burnout_hoodie_flat":      ("flatb_bl", "34_burnout_front", f"black {HOOD}, flat-lay product photo on white, front", "front_hood"),
    "burnout_hoodie_back_flat": ("flatc_bl", "34_burnout_back", f"black {HOOD} laid out showing its back, flat-lay product photo on white", "back_hood"),
    "burnout_hoodie_model":     ("model_e", "34_burnout_back", f"black {HOOD}, worn by a young man photographed from behind", "back_hood"),
    "burnout_bodega":           ("pose_bodega", "34_burnout_front", f"black {HOOD}, worn by a young man standing outside a bodega at night", "front_hood"),
    "chrome_hoodie_flat":       ("flatb_bl", "35_chrome_front", f"black {HOOD}, flat-lay product photo on white, front", "front_hood"),
    "chrome_hoodie_back_flat":  ("flatc_bl", "35_chrome_back", f"black {HOOD} laid out showing its back, flat-lay product photo on white", "back_hood"),
    "chrome_hoodie_model":      ("model_e", "35_chrome_back", f"black {HOOD}, worn by a young man photographed from behind", "back_hood"),
    "chrome_alley":             ("pose_alley", "35_chrome_back", f"black {HOOD}, worn by a young man walking away down an alley at night", "back_hood"),
    "nosleep_hoodie_flat":      ("flatb_bl", "36_nosleep_front", f"black {HOOD}, flat-lay product photo on white, front", "left_chest"),
    "nosleep_hoodie_back_flat": ("flatc_bl", "36_nosleep_back", f"black {HOOD} laid out showing its back, flat-lay product photo on white", "back_hood"),
    "nosleep_hoodie_model":     ("model_e", "36_nosleep_back", f"black {HOOD}, worn by a young man photographed from behind", "back_hood"),
    "nosleep_hoodback":         ("pose_hoodback", "36_nosleep_back", f"black {HOOD}, worn by a young man photographed from behind on a rainy street", "back_hood"),
    "nosleep_shutter":          ("pose_shutter", "36_nosleep_front", f"black {HOOD}, worn by a young man leaning against a shop shutter", "left_chest"),
    "owl_hoodie_flat":          ("flatb_bl", "33_owl_chest", f"black {HOOD}, flat-lay product photo on white, front", "left_chest"),
    "owl_hoodie_back_flat":     ("flatc_bl", "33_owl_back", f"black {HOOD} laid out showing its back, flat-lay product photo on white", "back_hood"),
    "owl_hoodie_model":         ("model_e", "33_owl_back", f"black {HOOD}, worn by a young man photographed from behind", "back_hood"),
    "owl_roof":                 ("pose_roof", "33_owl_back", f"black {HOOD}, worn by a young man on a rooftop, seen from behind", "back_hood"),
    "hazard_hoodie_flat":       ("flatb_bl", "30_hazard2_front", f"black {HOOD}, flat-lay product photo on white, front", "front_hood_small"),
    "hazard_hoodie_back_flat":  ("flatc_bl", "30_hazard2_back", f"black {HOOD} laid out showing its back, flat-lay product photo on white", "back_hood"),
    "hazard_hoodie_model":      ("model_e", "30_hazard2_back", f"black {HOOD}, worn by a young man photographed from behind", "back_hood"),
    "hazard_hoodback":          ("pose_hoodback", "30_hazard2_back", f"black {HOOD}, worn by a young man photographed from behind on a rainy street", "back_hood"),
    # shorts
    "sweat_shorts_flat":  ("flatc_tr", "27_sweat_left", "heather grey fleece sweat shorts, flat-lay product photo on white", "leg"),
    "sweat_shorts_model": ("model_d_r", "27_sweat_left", "heather grey fleece sweat shorts, worn by a young man", "leg"),
    "mesh_shorts_flat":   ("flatc_tl", ["26_mesh_left", "26_mesh_right"], "black mesh basketball shorts, flat-lay product photo on white", "legs"),
    "mesh_shorts_model":  ("model_d_l", ["26_mesh_left", "26_mesh_right"], "black mesh basketball shorts, worn by a young man", "legs"),
}

FIDELITY = ("Reproduce the print artwork EXACTLY as in the print file: same artwork, same words, same spelling, same layout, same colours, "
            "same proportions, nothing added or removed. Do not add any other text, logos, tags or labels anywhere on the garment or in the scene. "
            "Keep everything else identical to the first photo: same person, pose, garment, garment colour, lighting, background, framing and crop. "
            "The print should look screen-printed into the fabric: soft matte ink that follows the folds and creases, slightly worn-in, never a flat sticker. Photorealistic.")


def prompt(job):
    crop, prints, garment, pl = JOBS[job]
    n = 1 if isinstance(prints, str) else len(prints)
    files = "The second image is the screen-print file." if n == 1 else "The second and third images are the two screen-print files."
    return (f"Generate an image. The first image is a photo of a blank {garment}. {files} "
            f"Produce the exact same photo with the print applied as {PL[pl]}. {FIDELITY}")


def prep():
    for name, (bn, box) in CROPS.items():
        p = os.path.join(REF, f"blank_{name}.png")
        if not os.path.exists(p):
            Image.open(os.path.join(BL, bn + ".png")).crop(box).convert("RGB").save(p)
    print("refs ready")


if __name__ == "__main__":
    a = sys.argv[1]
    if a == "prep": prep()
    elif a == "js":
        # ready-to-paste JS for the Chrome MCP: insert prompt (verified) + send (verified)
        t = json.dumps(prompt(sys.argv[2]))
        print("const t=%s; const ed=document.querySelector('[contenteditable=\"true\"]'); let n=0; for(let k=0;k<4&&ed.innerText.trim().length<500;k++){ ed.focus(); document.execCommand('insertText', false, t); await new Promise(r=>setTimeout(r,800)); n++ } let res='attach:'+document.querySelectorAll('gem-media-attachment').length+' ins:'+n+' len:'+ed.innerText.length; if(ed.innerText.length>500){ for(let k=0;k<6;k++){ const b=[...document.querySelectorAll('button')].find(b=>/send message/i.test(b.getAttribute('aria-label')||'')); if(!b){res+=' nosend'; break;} for(const ev of ['pointerdown','mousedown','pointerup','mouseup','click']) b.dispatchEvent(new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,button:0})); await new Promise(r=>setTimeout(r,4000)); if(ed.innerText.trim().length<50){res+=' sent@'+k; break;} } } res" % t)
    elif a == "list":
        for j in JOBS:
            if not os.path.exists(os.path.join(OUT, j + ".png")): print(j)
    else:
        crop, prints, garment, pl = JOBS[a]
        prints = [prints] if isinstance(prints, str) else prints
        print(json.dumps({"out": os.path.join(OUT, a + ".png"),
                          "files": [os.path.join(REF, f"blank_{crop}.png")] + [os.path.join(REF, p + ".png") for p in prints],
                          "prompt": prompt(a)}, indent=1))
