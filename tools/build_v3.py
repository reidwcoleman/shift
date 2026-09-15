"""FIRST SHIFT collection — the 404-Culture-style range (varsity, tigers, cross, sundial, thermals, shorts, beanie).
Multi-color raster art (art/color/*.png) embedded at true scale + outlined vector type.

    .venv/bin/python tools/build_v3.py [filter...]
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(__file__))
from shiftlib import *
from build_designs import fit_size, rule, CHEST, FRONT, BACK, HOOD_FRONT, BADGE, SRC, PRINT, logotype
from PIL import Image

GOLD = "#E3B23C"; CREAM = "#EDE6D6"; RUST = "#B5432A"; SEPIA = "#5A3A1E"; NAVY = "#1E2740"; CARDINAL = "#A8231F"; GREY_INK = "#33332F"
COLOR = os.path.join(ROOT, "art", "color")


def raster(name, cx, top, width_px):
    """Embed art/color/<name>.png centred at cx with its top at `top`, scaled to width_px."""
    p = os.path.join(COLOR, name + ".png")
    w, h = Image.open(p).size
    s = width_px / w
    return (f'<image x="{cx - width_px/2:.1f}" y="{top:.1f}" width="{width_px:.1f}" height="{h*s:.1f}" '
            f'preserveAspectRatio="xMidYMid meet" href="{b64png(p)}"/>'), h * s


def stars(cx, y, n, r, fill, gap=None):
    """Row of n five-point stars centred at cx, centre-line y."""
    import math
    gap = gap or r * 3.2
    out = []
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * gap
        pts = []
        for k in range(10):
            rr = r if k % 2 == 0 else r * 0.42
            a = math.radians(k * 36 - 90)
            pts.append(f"{x + rr*math.cos(a):.1f},{y + rr*math.sin(a):.1f}")
        out.append(f'<polygon points="{" ".join(pts)}" fill="{fill}"/>')
    return "".join(out)


def outlined(font, s, size, x, y, fill, stroke, sw, **kw):
    """Text with a keyline: stroke pass under the fill pass."""
    return (text(font, s, size, x, y, fill=stroke, extra=f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"', **kw)
            + text(font, s, size, x, y, fill, **kw))


# 20 LEAGUE RINGER TEE — cardinal red body, gold rib. gold + cream + black
def league_front():
    w, h = FRONT
    b = []
    b.append(arc_text("Anton", "SHIFT", 720, w / 2, 3650, 3050, GOLD, tracking=0.16, extra=f'stroke="{CREAM}" stroke-width="28" stroke-linejoin="round" paint-order="stroke"'))
    snip, ah = raster("tiger_crest", w / 2, 1000, 2000); b.append(snip)
    # banner text sits inside the crest's ribbon (~90% down the art)
    b.append(text("Bebas Neue", "LEAGUE", 215, w / 2, 1000 + ah * 0.905, INK, tracking=0.25))
    b.append(text("Anton", "EST.", 170, w / 2 - 1250, 1000 + ah * 0.45, CREAM))
    b.append(text("Anton", "2002", 170, w / 2 + 1250, 1000 + ah * 0.45, CREAM))
    y = 1000 + ah + 200
    b.append(text("Bebas Neue", "NIGHT SHIFT DIVISION", 150, w / 2, y, CREAM, tracking=0.45))
    b.append(stars(w / 2, y + 140, 3, 60, GOLD))
    return svg_doc(w, h, "".join(b))


# 21 TWIN TIGERS TEE — natural tee
def tigers_front():
    w, h = FRONT
    b = []
    snip, ah = raster("twin_tigers", w / 2, 250, 3300); b.append(snip)
    y = 250 + ah + 420
    b.append(text("UnifrakturCook", "Shift", 520, w / 2, y, SEPIA))
    b.append(text("Bebas Neue", "EVERY HOUR COUNTS", 130, w / 2, y + 190, RUST, tracking=0.45))
    return svg_doc(w, h, "".join(b))


# 22 TIME IS MONEY — black tee / sleeveless
def cross_front():
    w, h = FRONT
    b = [text("UnifrakturCook", "Shift", 560, w / 2, 620, CREAM)]
    snip, ah = raster("timecard_cross", w / 2, 760, 2150); b.append(snip)
    y = 760 + ah + 300
    b.append(text("Bebas Neue", "TIME IS MONEY", 200, w / 2, y, GOLD, tracking=0.4))
    return svg_doc(w, h, "".join(b))


# 23 SUNDIAL TEE — cream 400gsm
def sundial_front():
    w, h = FRONT
    cx, cy = w / 2, 2050
    b = [arc_text("Bebas Neue", "SHIFT WORLDWIDE  •  NIGHT SHIFT DIVISION  •", 170, cx, cy, 1720, RUST, tracking=0.3),
         arc_text("Bebas Neue", "EVERY HOUR COUNTS  •  EST. 2002  •", 170, cx, cy, 1720, NAVY, tracking=0.3, bottom=True)]
    snip, ah = raster("sundial", cx, cy - 1450, 2900); b.append(snip)
    b.append(text("Anton", "11:59", 120, cx, cy + 1700 + 300, RUST, tracking=0.1))
    return svg_doc(w, h, "".join(b))


# 24 OVERTIME THERMAL — black waffle long sleeve
def thermal_front():
    w, h = (11 * IN, 8 * IN)
    b = []
    snip, ah = raster("script_drip", w / 2, 150, 3000); b.append(snip)
    b.append(text("Bebas Neue", "OVERTIME  •  NIGHT SHIFT DIVISION", 120, w / 2, 150 + ah + 220, CREAM, tracking=0.4))
    return svg_doc(w, h, "".join(b))


# 25 COLLAGE THERMAL / CREWNECK — cream
def collage_front():
    w, h = FRONT
    b = [text("UnifrakturCook", "Shift", 620, w / 2, 640, INK)]
    snip, ah = raster("collage", w / 2, 780, 2250); b.append(snip)
    b.append(text("Bebas Neue", "THE SHIFT NEVER ENDS", 150, w / 2, 780 + ah + 220, CARDINAL, tracking=0.45))
    return svg_doc(w, h, "".join(b))


# 26 MESH SHORTS — black mesh. left leg crest, right leg wordmark
def shield(cx, cy, s, fill, stroke):
    d = (f"M{cx-s/2},{cy-s*0.55} L{cx+s/2},{cy-s*0.55} L{cx+s/2},{cy+s*0.1} "
         f"Q{cx+s/2},{cy+s*0.5} {cx},{cy+s*0.62} Q{cx-s/2},{cy+s*0.5} {cx-s/2},{cy+s*0.1} Z")
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{s*0.045}" stroke-linejoin="round"/>'


def mesh_left():
    w, h = CHEST
    b = [shield(w / 2, h / 2 - 40, 900, "none", WHITE), shield(w / 2, h / 2 - 40, 760, "none", WHITE)]
    b.append(text("Anton", "NSD", 330, w / 2, h / 2 + 70, WHITE, tracking=0.02))
    b.append(stars(w / 2, h / 2 + 430, 3, 40, WHITE))
    return svg_doc(w, h, "".join(b))


def mesh_right():
    w, h = CHEST
    b = [logotype(w / 2, h / 2 + 60, 300, WHITE), stars(w / 2, h / 2 + 260, 3, 46, WHITE)]
    return svg_doc(w, h, "".join(b))


# 27 ATHLETIC DEPT SWEAT SHORTS — washed grey, tonal ink
def sweat_left():
    w, h = (5 * IN, 5 * IN)
    b = [shift_mark(w / 2 - 110, 120, 220, GREY_INK),
         text("Anton", "SHIFT", 420, w / 2, 780, GREY_INK, tracking=0.02),
         text("Bebas Neue", "ATHLETIC DEPT.", 200, w / 2, 1000, GREY_INK, tracking=0.2),
         rule(w / 2 - 520, 1060, w / 2 + 520, 1060, GREY_INK, 14),
         text("Bebas Neue", "NIGHT SHIFT DIVISION", 90, w / 2, 1190, GREY_INK, tracking=0.3)]
    return svg_doc(w, h, "".join(b))


# 28 BEANIE — embroidered wordmark
def beanie():
    w, h = (int(3.5 * IN), int(1.2 * IN))
    return svg_doc(w, h, logotype(w / 2, 265, 200, CREAM))


# 29 EMBLEM TEE — black tee back print
def emblem_back():
    w, h = BACK
    b = [text("UnifrakturCook", "Shift", 620, w / 2, 700, CREAM)]
    snip, ah = raster("spider_tiger", w / 2, 850, 3300); b.append(snip)
    y = 850 + ah + 380
    b.append(text("Bebas Neue", "THE SHIFT NEVER ENDS", 230, w / 2, y, GOLD, tracking=0.4))
    b.append(text("Bebas Neue", "NIGHT SHIFT DIVISION  •  EST. 2002", 120, w / 2, y + 220, CREAM, tracking=0.4))
    return svg_doc(w, h, "".join(b))


def emblem_chest():
    w, h = CHEST
    snip, ah = raster("spider_tiger", w / 2, 120, 900)
    return svg_doc(w, h, snip)


# 30 HAZARD HOODIE v2 — black hoodie. front: diamond badge. back: beacon emblem.
def hazard2_front():
    w, h = BADGE
    cx, cy = w / 2, h / 2 - 60
    r = 520
    d = f"M{cx},{cy-r} L{cx+r},{cy} L{cx},{cy+r} L{cx-r},{cy} Z"
    b = [f'<path d="{d}" fill="none" stroke="{SIGNAL}" stroke-width="44" stroke-linejoin="miter"/>',
         f'<path d="{d}" transform="translate({cx},{cy}) scale(0.82) translate({-cx},{-cy})" fill="none" stroke="{CREAM}" stroke-width="10"/>',
         shift_mark(cx - 150, cy - 170, 300, CREAM),
         text("Anton", "HAZARD", 150, cx, cy + 420 + 160, CREAM, tracking=0.12),
         text("Bebas Neue", "NIGHT SHIFT DIVISION  •  EST. 2002", 70, cx, cy + 420 + 260, SIGNAL, tracking=0.3)]
    return svg_doc(w, h, "".join(b))


def hazard2_back():
    w, h = BACK
    b = [arc_text("Anton", "HAZARD", 760, w / 2, 3350, 2900, SIGNAL, tracking=0.14, extra=f'stroke="{CREAM}" stroke-width="30" stroke-linejoin="round" paint-order="stroke"')]
    snip, ah = raster("beacon", w / 2, 1150, 3000); b.append(snip)
    y = 1150 + ah + 330
    b.append(text("Bebas Neue", "NIGHT SHIFT DIVISION", 230, w / 2, y, CREAM, tracking=0.4))
    b.append(text("Bebas Neue", "CAUTION  —  CHANGE IN PROGRESS", 150, w / 2, y + 220, SIGNAL, tracking=0.35))
    b.append(text("Bebas Neue", "SHIFT WORLDWIDE  •  EST. 2002", 110, w / 2, y + 400, CREAM, tracking=0.4))
    return svg_doc(w, h, "".join(b))


DESIGNS_V3 = {
    "30_hazard2_front": (hazard2_front, BADGE),
    "30_hazard2_back": (hazard2_back, BACK),
    "20_league_front": (league_front, FRONT),
    "21_tigers_front": (tigers_front, FRONT),
    "22_cross_front": (cross_front, FRONT),
    "23_sundial_front": (sundial_front, FRONT),
    "24_thermal_front": (thermal_front, (11 * IN, 8 * IN)),
    "25_collage_front": (collage_front, FRONT),
    "26_mesh_left": (mesh_left, CHEST),
    "26_mesh_right": (mesh_right, CHEST),
    "27_sweat_left": (sweat_left, (5 * IN, 5 * IN)),
    "28_beanie": (beanie, (int(3.5 * IN), int(1.2 * IN))),
    "29_emblem_back": (emblem_back, BACK),
    "29_emblem_chest": (emblem_chest, CHEST),
}

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, (fn, (w, h)) in DESIGNS_V3.items():
        if only and not any(o in name for o in only): continue
        p = os.path.join(SRC, name + ".svg"); open(p, "w").write(fn())
        render(p, os.path.join(PRINT, name + ".png"))
        print(f"  {name:22s} {w/IN:.1f}x{h/IN:.1f} in")
