"""Flat-lay style garment mockups for every SHIFT launch piece.

    .venv/bin/python tools/build_mockups.py

Draws tee / hoodie silhouettes in SVG, drops the print PNGs on at true scale
(21in chest = 960px, so 1in = 45.7px) and renders mockups/*.png plus a lookbook.
"""
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from shiftlib import *

PRINT = os.path.join(ROOT, "designs", "print")
SRCSVG = os.path.join(ROOT, "designs", "src")
OUT = os.path.join(ROOT, "mockups")
os.makedirs(OUT, exist_ok=True)
TMP = tempfile.mkdtemp()

W, H = 2000, 2200
PPI = 960 / 21.0  # mock px per inch

GARMENT_COLORS = {
    "black": ("#161616", "#2a2a2a", "#0a0a0a"),
    "washed": ("#2f2f33", "#45454a", "#1f1f22"),
    "bone": ("#E9E2CF", "#F4EFE1", "#D3CBB5"),
    "white": ("#F1F1F1", "#FFFFFF", "#D9D9D9"),
    "forest": ("#1E3628", "#2C4A38", "#12241A"),
}

TEE_FRONT = ("M 720,330 C 740,470 1260,470 1280,330 L 1560,380 L 1800,790 L 1530,900 L 1480,760 "
             "L 1480,1700 L 520,1700 L 520,760 L 470,900 L 200,790 L 440,380 Z")
TEE_BACK = ("M 720,330 C 740,380 1260,380 1280,330 L 1560,380 L 1800,790 L 1530,900 L 1480,760 "
            "L 1480,1700 L 520,1700 L 520,760 L 470,900 L 200,790 L 440,380 Z")
HOOD_BODY = ("M 700,420 C 720,520 1280,520 1300,420 L 1600,470 L 1790,1440 L 1570,1520 L 1520,1000 "
             "L 1520,1720 L 480,1720 L 480,1000 L 430,1520 L 210,1440 L 400,470 Z")
HOOD_BACK = ("M 700,420 C 720,440 1280,440 1300,420 L 1600,470 L 1790,1440 L 1570,1520 L 1520,1000 "
             "L 1520,1720 L 480,1720 L 480,1000 L 430,1520 L 210,1440 L 400,470 Z")


def garment_defs(color_key):
    base, hi, lo = GARMENT_COLORS[color_key]
    return f"""
<linearGradient id="shade" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{lo}"/><stop offset="0.18" stop-color="{base}"/>
  <stop offset="0.5" stop-color="{hi}"/><stop offset="0.82" stop-color="{base}"/><stop offset="1" stop-color="{lo}"/>
</linearGradient>
<filter id="fabric" x="0" y="0" width="1" height="1">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0.12 0"/>
</filter>
<filter id="drop" x="-10%" y="-10%" width="120%" height="125%">
  <feGaussianBlur stdDeviation="28"/>
</filter>
<linearGradient id="fold" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="0.5" stop-color="#000" stop-opacity="0.10"/><stop offset="1" stop-color="#000" stop-opacity="0"/>
</linearGradient>
"""


def tee(color_key, back=False):
    base, hi, lo = GARMENT_COLORS[color_key]
    d = TEE_BACK if back else TEE_FRONT
    g = [f'<path d="{d}" transform="translate(0,40)" fill="#000" opacity="0.35" filter="url(#drop)"/>',
         f'<path id="body" d="{d}" fill="url(#shade)" stroke="{lo}" stroke-width="3"/>',
         f'<clipPath id="bodyclip"><path d="{d}"/></clipPath>',
         f'<rect width="{W}" height="{H}" fill="#888" filter="url(#fabric)" clip-path="url(#bodyclip)" style="mix-blend-mode:multiply"/>',
         # side fold shadows
         f'<rect x="560" y="760" width="90" height="940" fill="url(#fold)" clip-path="url(#bodyclip)"/>',
         f'<rect x="1350" y="760" width="90" height="940" fill="url(#fold)" clip-path="url(#bodyclip)"/>']
    # collar rib
    if back:
        g.append(f'<path d="M 720,330 C 740,380 1260,380 1280,330" fill="none" stroke="{lo}" stroke-width="26"/>')
        g.append(f'<path d="M 720,330 C 740,380 1260,380 1280,330" fill="none" stroke="{hi}" stroke-width="4" opacity="0.5"/>')
    else:
        g.append(f'<path d="M 720,330 C 740,470 1260,470 1280,330" fill="none" stroke="{lo}" stroke-width="30"/>')
        g.append(f'<path d="M 745,340 C 760,445 1240,445 1255,340" fill="none" stroke="{hi}" stroke-width="3" opacity="0.6"/>')
    # sleeve hems + bottom hem stitch
    g.append(f'<g fill="none" stroke="{lo}" stroke-width="3" opacity="0.8"><line x1="1548" y1="880" x2="1500" y2="750"/><line x1="452" y1="880" x2="500" y2="750"/><line x1="520" y1="1665" x2="1480" y2="1665"/></g>')
    return "".join(g)


def hoodie(color_key, back=False):
    base, hi, lo = GARMENT_COLORS[color_key]
    d = HOOD_BACK if back else HOOD_BODY
    g = [f'<path d="{d}" transform="translate(0,40)" fill="#000" opacity="0.35" filter="url(#drop)"/>']
    if back:
        # hood seen from behind: rounded shape above shoulders
        g.append(f'<path d="M 640,470 C 600,150 1400,150 1360,470 Z" fill="{base}" stroke="{lo}" stroke-width="3"/>')
        g.append(f'<path d="M 1000,180 L 1000,470" stroke="{lo}" stroke-width="4" opacity="0.6"/>')
    g.append(f'<path d="{d}" fill="url(#shade)" stroke="{lo}" stroke-width="3"/>')
    g.append(f'<clipPath id="bodyclip"><path d="{d}"/></clipPath>')
    g.append(f'<rect width="{W}" height="{H}" fill="#888" filter="url(#fabric)" clip-path="url(#bodyclip)" style="mix-blend-mode:multiply"/>')
    g.append(f'<rect x="540" y="1000" width="110" height="720" fill="url(#fold)" clip-path="url(#bodyclip)"/>')
    g.append(f'<rect x="1350" y="1000" width="110" height="720" fill="url(#fold)" clip-path="url(#bodyclip)"/>')
    if not back:
        # hood (front view: two flaps behind the neck opening)
        g.append(f'<path d="M 700,420 C 640,250 800,180 1000,190 C 1200,180 1360,250 1300,420 C 1250,500 750,500 700,420 Z" fill="{lo}" stroke="{lo}" stroke-width="3"/>')
        g.append(f'<path d="M 740,430 C 720,300 860,240 1000,245 C 1140,240 1280,300 1260,430 C 1200,470 800,470 740,430 Z" fill="{base}"/>')
        # drawstrings
        g.append(f'<g stroke="{lo}" stroke-width="10" stroke-linecap="round" fill="none"><path d="M 930,470 C 920,560 925,640 905,720"/><path d="M 1070,470 C 1080,560 1075,640 1095,720"/></g>')
        g.append(f'<g fill="{lo}"><rect x="893" y="712" width="24" height="42" rx="6"/><rect x="1083" y="712" width="24" height="42" rx="6"/></g>')
        # kangaroo pocket
        g.append(f'<path d="M 620,1330 L 1380,1330 L 1380,1650 L 620,1650 Z M 620,1330 L 700,1270 L 1300,1270 L 1380,1330" fill="none" stroke="{lo}" stroke-width="4"/>')
        g.append(f'<path d="M 620,1330 L 1380,1330 L 1380,1650 L 620,1650 Z" fill="#000" opacity="0.06"/>')
    # cuffs + hem ribs
    g.append(f'<g fill="none" stroke="{lo}" stroke-width="3" opacity="0.9">'
             f'<line x1="1738" y1="1400" x2="1560" y2="1465"/><line x1="262" y1="1400" x2="440" y2="1465"/>'
             f'<line x1="480" y1="1650" x2="1520" y2="1650"/><line x1="480" y1="1690" x2="1520" y2="1690"/></g>')
    return "".join(g)


def print_image(name, cx, top, width_in, height_in):
    """Downscale a print PNG and embed it at true scale."""
    small = os.path.join(TMP, name + ".png")
    if not os.path.exists(small):
        render(os.path.join(SRCSVG, name + ".svg"), small, width=1400)
    w = width_in * PPI
    h = height_in * PPI
    return (f'<image x="{cx - w/2:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'preserveAspectRatio="xMidYMid meet" href="{b64png(small)}" style="mix-blend-mode:normal"/>')


PRODUCTS = [
    # key, title, garment, color, price, [(view, print name, cx, top, w_in, h_in)]
    ("sun_tee", "Inner Peace Tee", "tee", "black", 48,
     [("front", "10_sun_front_white", 1000, 540, 12, 14), ("back", "10_neck_back_white", 1000, 400, 4, 2)]),
    ("cherub_tee", "Cherub Tee", "tee", "bone", 48,
     [("front", "11_cherub_front_ink", 1000, 540, 12, 14), ("back", "11_neck_back_ink", 1000, 400, 4, 2)]),
    ("wings_tee", "Guardian Tee", "tee", "black", 48,
     [("front", "12_core_chest_white", 1000 + 3.6 * PPI, 600, 4, 4), ("back", "12_wings_back_white", 1000, 480, 13, 16)]),
    ("hands_hoodie", "Overtime Hoodie", "hoodie", "black", 98,
     [("front", "13_hands_front_white", 1000, 600, 11, 12), ("back", "13_factory_back_white", 1000, 500, 13, 16)]),
    ("web_hoodie", "Caught Up Hoodie", "hoodie", "forest", 98,
     [("front", "14_web_front_white", 1000, 600, 11, 12), ("back", "14_web_back_white", 1000, 500, 13, 16)]),
    ("skeleton_tee", "Manual Only Tee", "tee", "white", 45,
     [("front", "15_skeleton_front_ink", 1000, 540, 12, 14), ("back", None, 0, 0, 0, 0)]),
    ("hazard_hoodie", "Hazard Hoodie", "hoodie", "black", 98,
     [("front", "06_hazard_badge_white", 1000, 620, 5, 5), ("back", "06_hazard_back_white", 1000, 500, 13, 16)]),
    ("timecard_tee", "Time Card Tee", "tee", "black", 45,
     [("front", "05_timecard_chest_white", 1000 + 3.6 * PPI, 600, 4, 4), ("back", "05_timecard_back_white", 1000, 480, 13, 16)]),
    ("moth_tee", "Drawn To The Light Tee", "tee", "black", 48,
     [("front", "16_core_chest_white", 1000 + 3.6 * PPI, 600, 4, 4), ("back", "16_moth_back_white", 1000, 480, 13, 16)]),
]


def build():
    made = []
    for key, title, garment, color, price, views in PRODUCTS:
        for view, pname, cx, top, wi, hi in views:
            back = view == "back"
            body = tee(color, back) if garment == "tee" else hoodie(color, back)
            if pname:
                body += print_image(pname, cx, top, wi, hi)
            doc = svg_doc(W, H, body, garment_defs(color), bg="#B8B4AC")
            svgp = os.path.join(TMP, f"{key}_{view}.svg")
            open(svgp, "w").write(doc)
            outp = os.path.join(OUT, f"{key}_{view}.png")
            render(svgp, outp, width=1400)
            made.append((key, title, view, outp, price))
            print(f"  {key}_{view}.png")
    return made


def lookbook(made):
    cols = 4
    cw, ch = 700, 770 + 90
    fronts = [m for m in made]
    rows = (len(fronts) + cols - 1) // cols
    parts = [f'<rect width="{cols*cw}" height="{rows*ch + 260}" fill="#0B0B0B"/>']
    parts.append(wordmark(cols * cw / 2, 170, 110, WHITE))
    parts.append(text("Bebas Neue", "DROP 001  —  CLOCK IN", 44, cols * cw / 2, 232, SIGNAL, tracking=0.35))
    for i, (key, title, view, path, price) in enumerate(fronts):
        x = (i % cols) * cw; y = 260 + (i // cols) * ch
        parts.append(f'<image x="{x+20}" y="{y}" width="{cw-40}" height="{770}" preserveAspectRatio="xMidYMid meet" href="{b64png(path)}"/>')
        parts.append(text("Bebas Neue", f"{title.upper()}  ·  {view.upper()}", 40, x + cw / 2, y + 810, WHITE, tracking=0.12))
        parts.append(text("Bebas Neue", f"${price}", 34, x + cw / 2, y + 850, CONCRETE, tracking=0.12))
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{cols*cw}" height="{rows*ch+260}">' + "".join(parts) + "</svg>"
    p = os.path.join(TMP, "lookbook.svg"); open(p, "w").write(doc)
    render(p, os.path.join(OUT, "lookbook.png"), width=2400)
    print("  lookbook.png")


if __name__ == "__main__":
    print("Building mockups…")
    made = build()
    lookbook(made)
