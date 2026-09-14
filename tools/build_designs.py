"""Generate every SHIFT launch graphic as outlined SVG + 300 DPI transparent PNG.

    .venv/bin/python tools/build_designs.py

Outputs designs/src/<name>.svg and designs/print/<name>.png
Canvas sizes are real print areas at 300 DPI.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from shiftlib import *

SRC = os.path.join(ROOT, "designs", "src")
PRINT = os.path.join(ROOT, "designs", "print")
os.makedirs(SRC, exist_ok=True); os.makedirs(PRINT, exist_ok=True)

# --- print areas ---
CHEST = (4 * IN, 4 * IN)          # left chest
FRONT = (12 * IN, 14 * IN)        # full front
BACK = (13 * IN, 16 * IN)         # full back
HOOD_FRONT = (11 * IN, 12 * IN)   # hoodie front (above pocket)
BADGE = (5 * IN, 5 * IN)


def fit_size(font, s, target_w, tracking=0.0):
    """Font size that makes `s` exactly target_w wide."""
    f = Font.get(font)
    return target_w / f.width(s, 1000, tracking) * 1000


def rule(x1, y1, x2, y2, color, w):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="square"/>'


def stripes_defs(id_, color, gap_color=None, period=170, angle=-45):
    """Diagonal hazard stripes pattern."""
    gap = f'<rect width="{period}" height="{period}" fill="{gap_color}"/>' if gap_color else ""
    return (
        f'<pattern id="{id_}" patternUnits="userSpaceOnUse" width="{period}" height="{period}" '
        f'patternTransform="rotate({angle})">{gap}<rect width="{period/2}" height="{period}" fill="{color}"/></pattern>'
    )


def save(name, w, h, body, defs="", preview_bg=None):
    doc = svg_doc(w, h, body, defs)
    p = os.path.join(SRC, name + ".svg")
    open(p, "w").write(doc)
    render(p, os.path.join(PRINT, name + ".png"))
    print(f"  {name:28s} {w/IN:.0f}x{h/IN:.0f} in")


# ---------------------------------------------------------------- 01 CORE
def core_chest(ink):
    w, h = CHEST
    return svg_doc(w, h, wordmark(w / 2, h / 2 + 140, 300, ink))


def core_back(ink, accent):
    w, h = BACK
    body = []
    size = fit_size("Anton", "SHIFT", w - 200, -0.01)
    f = Font.get("Anton")
    cap = f.cap_height(size)
    base = h * 0.56
    body.append(shift_mark(w / 2 - 330, base - cap - 900, 660, accent))
    body.append(text("Anton", "SHIFT", size, w / 2, base, ink, tracking=-0.01))
    s2 = fit_size("Bebas Neue", "WORLDWIDE", w - 260, 0.32)
    body.append(text("Bebas Neue", "WORLDWIDE", s2, w / 2, base + s2 * 0.95, ink, tracking=0.32))
    y = base + s2 * 1.3
    body.append(rule(200, y, w - 200, y, ink, 14))
    body.append(text("Inter_wght_400_600_800_6201ab", "EST. 2026   —   CLOCK IN.", 120, w / 2, y + 190, ink, tracking=0.08))
    return svg_doc(w, h, "".join(body))


# ---------------------------------------------------------------- 02 NIGHT SHIFT
def punch_clock(cx, top, scale, ink, accent):
    """Line-art time clock with a card in the slot. ~1500x1950 at scale 1."""
    S = scale
    sw = 16 * S
    g = [f'<g transform="translate({cx},{top}) scale({S})" fill="none" stroke="{ink}" stroke-width="{16}" stroke-linejoin="round" stroke-linecap="round">']
    # body
    g.append('<rect x="-720" y="0" width="1440" height="1880" rx="90"/>')
    g.append('<rect x="-640" y="80" width="1280" height="1720" rx="60"/>')
    # screws
    for sx, sy in [(-660, 40), (660, 40), (-660, 1840), (660, 1840)]:
        g.append(f'<circle cx="{sx}" cy="{sy}" r="24"/>')
    # clock face
    fcx, fcy, r = 0, 640, 470
    g.append(f'<circle cx="{fcx}" cy="{fcy}" r="{r + 40}"/>')
    g.append(f'<circle cx="{fcx}" cy="{fcy}" r="{r}" stroke-width="10"/>')
    for i in range(60):
        a = math.radians(i * 6)
        L = 46 if i % 5 == 0 else 20
        wdt = 14 if i % 5 == 0 else 8
        x1, y1 = fcx + (r - 16) * math.sin(a), fcy - (r - 16) * math.cos(a)
        x2, y2 = fcx + (r - 16 - L) * math.sin(a), fcy - (r - 16 - L) * math.cos(a)
        g.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="{wdt}"/>')
    # numerals 12 3 6 9
    g.append("</g>")
    for n, ang in [("12", 0), ("3", 90), ("6", 180), ("9", 270)]:
        a = math.radians(ang)
        nx = cx + S * (fcx + (r - 130) * math.sin(a))
        ny = top + S * (fcy - (r - 130) * math.cos(a)) + 30 * S
        g.append(text("Anton", n, 92 * S, nx, ny, ink))
    g.append(f'<g transform="translate({cx},{top}) scale({S})" fill="none" stroke="{ink}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round">')
    # hands: 11:59 -> hour hand just before 12, minute at 59
    ha = math.radians(-6); ma = math.radians(-6 * 1)
    g.append(f'<line x1="{fcx}" y1="{fcy}" x2="{fcx + 250*math.sin(ha):.1f}" y2="{fcy - 250*math.cos(ha):.1f}" stroke-width="34"/>')
    g.append(f'<line x1="{fcx}" y1="{fcy}" x2="{fcx + 380*math.sin(ma):.1f}" y2="{fcy - 380*math.cos(ma):.1f}" stroke-width="22"/>')
    g.append(f'<line x1="{fcx}" y1="{fcy}" x2="{fcx + 410*math.sin(math.radians(150)):.1f}" y2="{fcy - 410*math.cos(math.radians(150)):.1f}" stroke="{accent}" stroke-width="12"/>')
    g.append(f'<circle cx="{fcx}" cy="{fcy}" r="30" fill="{ink}"/>')
    g.append(f'<circle cx="{fcx}" cy="{fcy}" r="12" fill="{accent}" stroke="none"/>')
    # slot + card
    g.append('<rect x="-330" y="1330" width="660" height="70" rx="20" fill="none"/>')
    g.append(f'<g transform="rotate(-4 0 1500)"><rect x="-260" y="1390" width="520" height="700" rx="18" fill="none"/>'
             f'<line x1="-200" y1="1520" x2="200" y2="1520"/><line x1="-200" y1="1620" x2="120" y2="1620"/>'
             f'<line x1="-200" y1="1720" x2="200" y2="1720"/><line x1="-200" y1="1820" x2="60" y2="1820"/></g>')
    # label plate
    g.append('<rect x="-360" y="1180" width="720" height="110" rx="14"/>')
    g.append("</g>")
    g.append(text("Bebas Neue", "PUNCH IN", 84 * S, cx, top + S * 1268, ink, tracking=0.25))
    # card text
    g.append(f'<g transform="translate({cx},{top}) scale({S}) rotate(-4 0 1500)">' + text("Anton", "SHIFT", 110, 0, 1490, ink) + "</g>")
    g.append(f'<g transform="translate({cx},{top}) scale({S}) rotate(-4 0 1500)">' + text("Anton", "LATE", 150, 0, 2000, accent, rotate=-14) + "</g>")
    return "".join(g)


def night_chest(ink):
    w, h = CHEST
    body = text("UnifrakturCook", "Night", 470, w / 2, h / 2 - 20, ink) + text("UnifrakturCook", "Shift", 470, w / 2, h / 2 + 400, ink)
    return svg_doc(w, h, body)


def night_back(ink, accent):
    w, h = BACK
    body = []
    body.append(arc_text("UnifrakturCook", "NIGHT SHIFT", 560, w / 2, 2900, 2250, ink, tracking=0.02))
    body.append(punch_clock(w / 2, 1000, 1.0, ink, accent))
    y = 3560
    body.append(text("Bebas Neue", "CLOCK IN  11:59 PM", 300, w / 2, y, ink, tracking=0.08))
    f = Font.get("Bebas Neue")
    a, b = "CLOCK OUT  ", "NEVER"
    wa, wb = f.width(a, 300, 0.08), f.width(b, 300, 0.08)
    x0 = w / 2 - (wa + wb) / 2
    body.append(text("Bebas Neue", a, 300, x0, y + 330, ink, anchor="start", tracking=0.08))
    body.append(text("Bebas Neue", b, 300, x0 + wa, y + 330, accent, anchor="start", tracking=0.08))
    body.append(arc_text("Bebas Neue", "SHIFT WORLDWIDE  •  NIGHT SHIFT DIVISION  •  EST 2026", 120, w / 2, 1900, 2600, ink, tracking=0.2, bottom=True))
    inner = f'<g mask="url(#grunge)">{"".join(body)}</g>'
    return svg_doc(w, h, inner, grunge_defs(w, h, seed=5, strength="light", bf="0.02"))


# ---------------------------------------------------------------- 03 SHIFT HAPPENS
def happens_front(ink, accent):
    w, h = HOOD_FRONT
    body = []
    size = fit_size("Archivo Black", "SHIFT", w - 500, -0.02)
    f = Font.get("Archivo Black"); cap = f.cap_height(size)
    base1 = h * 0.42
    # motion ghost
    for dx, dy, sw in ((-320, -120, 12),):
        body.append(text("Archivo Black", "SHIFT", size, w / 2 - 130 + dx, base1 + dy, "none", tracking=-0.02, extra=f'stroke="{ink}" stroke-width="{sw}"'))
    body.append(text("Archivo Black", "SHIFT", size, w / 2 - 130, base1, ink, tracking=-0.02))
    s2 = fit_size("Archivo Black", "HAPPENS", w - 500, -0.02)
    body.append(text("Archivo Black", "HAPPENS", s2, w / 2 + 130, base1 + s2 * 0.95, ink, tracking=-0.02))
    body.append(shift_mark(w - 560, base1 + s2 * 1.15, 300, accent))
    body.append(text("Bebas Neue", "SHIFT WORLDWIDE", 130, 250, base1 + s2 * 1.15 + 250, ink, anchor="start", tracking=0.3))
    return svg_doc(w, h, "".join(body))


def happens_back(ink, accent):
    w, h = BACK
    defs = stripes_defs("hz", accent, None, period=210)
    m = 3600
    mx, my = w / 2 - m / 2, 250
    pts = [(50, 4), (96, 50), (71, 50), (71, 96), (29, 96), (29, 50), (4, 50)]
    d = "M" + " L".join(f"{mx + px/100*m:.1f},{my + py/100*m:.1f}" for px, py in pts) + " Z"
    defs += f'<clipPath id="arrowclip"><path d="{d}"/></clipPath>'
    body = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#hz)" clip-path="url(#arrowclip)"/>',
            f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="70" stroke-linejoin="miter"/>']
    y = my + m + 400
    s = fit_size("Rubik Mono One", "CAUTION", w - 400)
    body.append(text("Rubik Mono One", "CAUTION", s, w / 2, y, ink))
    s2 = fit_size("Bebas Neue", "CHANGE IN PROGRESS", w - 500, 0.25)
    body.append(text("Bebas Neue", "CHANGE IN PROGRESS", s2, w / 2, y + s2 * 1.0, ink, tracking=0.25))
    return svg_doc(w, h, "".join(body), defs)


# ---------------------------------------------------------------- 04 GEAR SHIFT
def gear_front(ink, accent):
    w, h = FRONT
    body = []
    s = fit_size("Anton", "MANUAL ONLY", w - 400, 0.02)
    body.append(text("Anton", "MANUAL ONLY", s, w / 2, 780, ink, tracking=0.02))
    cx, cy = w / 2, 2050
    gx = [cx - 1000, cx, cx + 1000]
    gy = [cy - 620, cy + 620]
    sw = 44
    body.append(f'<g fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round">')
    body.append(f'<line x1="{gx[0]}" y1="{cy}" x2="{gx[2]}" y2="{cy}"/>')
    for x in gx:
        body.append(f'<line x1="{x}" y1="{gy[0]}" x2="{x}" y2="{gy[1]}"/>')
    body.append("</g>")
    slots = [("1", "WAKE", gx[0], gy[0]), ("2", "WORK", gx[0], gy[1]), ("3", "WIN", gx[1], gy[0]),
             ("4", "REPEAT", gx[1], gy[1]), ("5", "SHIFT", gx[2], gy[0]), ("R", "NEVER", gx[2], gy[1])]
    r = 210
    for n, lab, x, y in slots:
        knob = n == "5"
        body.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{accent if knob else WHITE}" stroke="{ink}" stroke-width="{sw}"/>')
        if knob:
            body.append(shift_mark(x - 130, y - 130, 260, WHITE))
        else:
            body.append(text("Anton", n, 300, x, y + 108, ink))
        ly = y - r - 70 if y < cy else y + r + 150
        body.append(text("Bebas Neue", lab, 150, x, ly, accent if knob else ink, tracking=0.12))
        if n == "R":
            body.append(rule(x - 190, ly - 50, x + 190, ly - 50, accent, 22))
    body.append(f'<circle cx="{cx}" cy="{cy}" r="60" fill="{ink}"/>')
    s3 = fit_size("Anton", "NO REVERSE.", w - 900, 0.0)
    body.append(text("Anton", "NO REVERSE.", s3, w / 2, 3780, accent))
    body.append(text("Bebas Neue", "SHIFT WORLDWIDE  —  EST 2026", 130, w / 2, 4010, ink, tracking=0.3))
    return svg_doc(w, h, "".join(body))


# ---------------------------------------------------------------- 05 TIME CARD
def stamp(txt, x, y, size, color, rot):
    f = Font.get("Anton")
    tw = f.width(txt, size, 0.05)
    pad = size * 0.28
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="{-tw/2 - pad}" y="{-size*0.72 - pad*0.7}" width="{tw + 2*pad}" height="{size*0.72 + 1.4*pad*0.7}" rx="18" fill="none" stroke="{color}" stroke-width="18"/>'
            f'<rect x="{-tw/2 - pad - 34}" y="{-size*0.72 - pad*0.7 - 34}" width="{tw + 2*pad + 68}" height="{size*0.72 + 1.4*pad*0.7 + 68}" rx="26" fill="none" stroke="{color}" stroke-width="8"/>'
            + text("Anton", txt, size, 0, 0, color, tracking=0.05) + "</g>")


def timecard_back(ink, accent):
    w, h = BACK
    cw, ch = 3000, 4300
    x0, y0 = (w - cw) / 2, (h - ch) / 2
    lw = 22
    b = [f'<g transform="rotate(-2.5 {w/2} {h/2})">']
    b.append(f'<rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" rx="40" fill="none" stroke="{ink}" stroke-width="{lw}"/>')
    b.append(f'<circle cx="{w/2}" cy="{y0 + 150}" r="60" fill="none" stroke="{ink}" stroke-width="{lw}"/>')
    b.append(text("Anton", "SHIFT WORLDWIDE", 260, w / 2, y0 + 500, ink, tracking=0.02))
    b.append(text("Bebas Neue", "EMPLOYEE TIME CARD", 150, w / 2, y0 + 660, ink, tracking=0.35))
    b.append(rule(x0, y0 + 740, x0 + cw, y0 + 740, ink, lw))
    fields = [("EMPLOYEE", "YOU"), ("DEPT", "WHATEVER IT TAKES"), ("PAY RATE", "N/A"), ("SUPERVISOR", "NONE")]
    y = y0 + 900
    for k, v in fields:
        b.append(text("Bebas Neue", k + ":", 120, x0 + 120, y, ink, anchor="start", tracking=0.15))
        b.append(text("Anton", v, 150, x0 + 900, y + 8, ink, anchor="start"))
        b.append(rule(x0 + 880, y + 40, x0 + cw - 120, y + 40, ink, 8))
        y += 210
    b.append(rule(x0, y - 60, x0 + cw, y - 60, ink, lw))
    cols = [x0 + 120, x0 + 900, x0 + 1700, x0 + 2500]
    hdr = ["DAY", "IN", "OUT", "HRS"]
    y += 100
    for cx_, t in zip(cols, hdr):
        b.append(text("Bebas Neue", t, 120, cx_, y, ink, anchor="start", tracking=0.2))
    y += 50
    b.append(rule(x0, y, x0 + cw, y, ink, 12))
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    for i, d_ in enumerate(days):
        y += 250
        b.append(text("Anton", d_, 130, cols[0], y, ink, anchor="start"))
        b.append(text("Anton", "11:59 PM", 130, cols[1], y, ink, anchor="start"))
        b.append(text("Anton", "—", 130, cols[2] + 60, y, ink, anchor="start"))
        b.append(text("Anton", "ALL", 130, cols[3], y, ink, anchor="start"))
        b.append(rule(x0, y + 60, x0 + cw, y + 60, ink, 6))
        if d_ in ("TUE", "SAT"):
            b.append(stamp("LATE", cols[2] + 260, y - 10, 140, accent, -8 if d_ == "TUE" else 6))
    y += 260
    b.append(text("Bebas Neue", "TOTAL HOURS:", 130, x0 + 120, y, ink, anchor="start", tracking=0.2))
    b.append(text("Anton", "ALL OF THEM", 170, x0 + 1000, y + 10, ink, anchor="start"))
    b.append(text("Bebas Neue", "SIGNATURE:", 130, x0 + 120, y + 260, ink, anchor="start", tracking=0.2))
    b.append(rule(x0 + 800, y + 290, x0 + cw - 120, y + 290, ink, 8))
    b.append(wordmark(x0 + 1350, y + 275, 130, ink))
    b.append(stamp("APPROVED", w / 2 + 520, y0 + 3000, 230, accent, -9))
    b.append("</g>")
    return svg_doc(w, h, f'<g mask="url(#grunge)">{"".join(b)}</g>', grunge_defs(w, h, seed=9, strength="light", bf="0.025"))


# ---------------------------------------------------------------- 06 HAZARD
def hazard_badge(ink, accent):
    w, h = BADGE
    cx, cy = w / 2, h / 2
    R = 700
    b = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{accent}" stroke-width="34"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{R - 90}" fill="none" stroke="{ink}" stroke-width="10"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{R - 300}" fill="none" stroke="{ink}" stroke-width="10"/>']
    b.append(arc_text("Bebas Neue", "SHIFT WORLDWIDE", 165, cx, cy, R - 190, ink, tracking=0.28))
    b.append(arc_text("Bebas Neue", "NIGHT SHIFT DIVISION", 165, cx, cy, R - 145, ink, tracking=0.28, bottom=True))
    for sx in (-1, 1):
        b.append(shift_mark(cx + sx * (R - 205) - 45, cy - 45, 90, accent))
    b.append(shift_mark(cx - 200, cy - 250, 400, accent))
    b.append(text("Anton", "EST. 2026", 110, cx, cy + 300, ink, tracking=0.1))
    return svg_doc(w, h, "".join(b))


def hazard_back(ink, accent):
    w, h = BACK
    defs = stripes_defs("hz2", accent, None, period=230, angle=-45)
    band_y, band_h = 500, 1500
    b = [f'<rect x="0" y="{band_y}" width="{w}" height="{band_h}" fill="url(#hz2)"/>',
         f'<rect x="0" y="{band_y}" width="{w}" height="{band_h}" fill="none" stroke="{accent}" stroke-width="40"/>']
    pw, ph = 2700, 980
    b.append(f'<rect x="{w/2 - pw/2}" y="{band_y + band_h/2 - ph/2}" width="{pw}" height="{ph}" fill="{INK}" stroke="{ink}" stroke-width="28"/>')
    s = fit_size("Anton", "SHIFT", pw - 260, -0.01)
    f = Font.get("Anton"); cap = f.cap_height(s)
    b.append(text("Anton", "SHIFT", s, w / 2, band_y + band_h / 2 + cap / 2, ink, tracking=-0.01))
    y = band_y + band_h + 520
    s2 = fit_size("Rubik Mono One", "DO NOT CROSS", w - 300)
    for i in range(3):
        b.append(text("Rubik Mono One", "DO NOT CROSS", s2, w / 2, y + i * s2 * 1.22, ink if i != 1 else accent))
    y2 = y + 3 * s2 * 1.22 + 200
    b.append(text("Bebas Neue", "CAUTION  —  CHANGE IN PROGRESS", 150, w / 2, y2, ink, tracking=0.3))
    b.append(text("Bebas Neue", "SHIFT WORLDWIDE  •  EST 2026", 110, w / 2, y2 + 200, accent, tracking=0.3))
    return svg_doc(w, h, "".join(b), defs)


# ---------------------------------------------------------------- build all
DESIGNS = {
    # name: (svg string, canvas)
    "01_core_chest_white": (lambda: core_chest(WHITE), CHEST),
    "01_core_back_white": (lambda: core_back(WHITE, SIGNAL), BACK),
    "02_nightshift_chest_white": (lambda: night_chest(WHITE), CHEST),
    "02_nightshift_back_white": (lambda: night_back(WHITE, SIGNAL), BACK),
    "03_happens_front_ink": (lambda: happens_front(INK, SIGNAL), HOOD_FRONT),
    "03_happens_back_ink": (lambda: happens_back(INK, SIGNAL), BACK),
    "04_gearshift_front_ink": (lambda: gear_front(INK, SIGNAL), FRONT),
    "05_timecard_chest_white": (lambda: core_chest(WHITE), CHEST),
    "05_timecard_back_white": (lambda: timecard_back(WHITE, SIGNAL), BACK),
    "06_hazard_badge_white": (lambda: hazard_badge(WHITE, SIGNAL), BADGE),
    "06_hazard_back_white": (lambda: hazard_back(WHITE, SIGNAL), BACK),
}

if __name__ == "__main__":
    only = sys.argv[1:]
    print("Building SHIFT print files…")
    for name, (fn, (w, h)) in DESIGNS.items():
        if only and not any(o in name for o in only):
            continue
        doc = fn()
        p = os.path.join(SRC, name + ".svg")
        open(p, "w").write(doc)
        render(p, os.path.join(PRINT, name + ".png"))
        print(f"  {name:30s} {w/IN:.0f}x{h/IN:.0f} in  ({w}x{h}px @300dpi)")
