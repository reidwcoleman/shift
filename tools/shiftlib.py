"""Shared helpers for generating SHIFT print files as outlined-text SVG.

Every piece of text is converted to glyph outlines with fontTools, so the
SVGs have zero font dependencies and are safe to hand to a screen printer.
Units are pixels at 300 DPI (1 in = 300 px).
"""
import math, os, glob, base64, subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "fonts")
DPI = 300
IN = DPI  # px per inch

# Palette
INK = "#0B0B0B"
BONE = "#EDE6D6"
SIGNAL = "#FF3B1F"
CONCRETE = "#9A9A93"
WHITE = "#FFFFFF"


class Font:
    _cache = {}

    def __init__(self, path):
        self.t = TTFont(path)
        self.gs = self.t.getGlyphSet()
        self.cmap = self.t.getBestCmap()
        self.upem = self.t["head"].unitsPerEm
        self.hmtx = self.t["hmtx"]
        # crude kerning table from GPOS pair positioning (first lookup found)
        self.kern = {}
        try:
            gpos = self.t["GPOS"].table
            for lk in gpos.LookupList.Lookup:
                for st in lk.SubTable:
                    if getattr(st, "LookupType", lk.LookupType) == 9:
                        st = st.ExtSubTable
                    if st.LookupType != 2:
                        continue
                    if st.Format == 1:
                        firsts = st.Coverage.glyphs
                        for g1, ps in zip(firsts, st.PairSet):
                            for pvr in ps.PairValueRecord:
                                v = pvr.Value1.XAdvance if pvr.Value1 and hasattr(pvr.Value1, "XAdvance") else 0
                                if v:
                                    self.kern[(g1, pvr.SecondGlyph)] = v
                    elif st.Format == 2:
                        cd1, cd2 = st.ClassDef1.classDefs, st.ClassDef2.classDefs
                        firsts = st.Coverage.glyphs
                        for g1 in firsts:
                            c1 = cd1.get(g1, 0)
                            rec1 = st.Class1Record[c1]
                            for g2, c2 in cd2.items():
                                v1 = rec1.Class2Record[c2].Value1
                                v = getattr(v1, "XAdvance", 0) if v1 else 0
                                if v:
                                    self.kern[(g1, g2)] = v
        except Exception:
            pass

    @classmethod
    def get(cls, name):
        if name not in cls._cache:
            hits = glob.glob(os.path.join(FONT_DIR, name.replace(" ", "_") + "*.ttf"))
            if not hits:
                raise FileNotFoundError(name)
            cls._cache[name] = cls(sorted(hits)[0])
        return cls._cache[name]

    def gname(self, ch):
        return self.cmap.get(ord(ch), ".notdef")

    def layout(self, text, size, tracking=0.0):
        """Return (glyph list, total width). tracking is in em units."""
        k = size / self.upem
        x = 0.0
        out = []
        prev = None
        for ch in text:
            g = self.gname(ch)
            if prev is not None:
                x += self.kern.get((prev, g), 0) * k
            adv = self.hmtx[g][0] * k
            if ch != " ":
                pen = SVGPathPen(self.gs)
                self.gs[g].draw(pen)
                out.append((pen.getCommands(), x, adv))
            x += adv + tracking * size
            prev = g
        total = x - tracking * size if text else 0
        return out, total

    def width(self, text, size, tracking=0.0):
        return self.layout(text, size, tracking)[1]

    def cap_height(self, size):
        try:
            return self.t["OS/2"].sCapHeight * size / self.upem
        except Exception:
            return 0.7 * size


def text(font, s, size, x, y, fill=INK, anchor="middle", tracking=0.0, rotate=0, extra=""):
    """Outlined text. (x,y) is the baseline point; anchor: start|middle|end."""
    f = Font.get(font)
    glyphs, total = f.layout(s, size, tracking)
    k = size / f.upem
    ox = {"start": 0, "middle": -total / 2, "end": -total}[anchor]
    parts = []
    for d, gx, adv in glyphs:
        parts.append(f'<path transform="translate({gx + ox:.2f},0) scale({k:.6f},{-k:.6f})" d="{d}"/>')
    rot = f" rotate({rotate})" if rotate else ""
    return (f'<g transform="translate({x:.2f},{y:.2f}){rot}" fill="{fill}" {extra}>' + "".join(parts) + "</g>")


def arc_text(font, s, size, cx, cy, r, fill=INK, tracking=0.0, bottom=False, extra=""):
    """Text laid along a circle of radius r centred at (cx,cy), centred on 12 o'clock
    (or 6 o'clock when bottom=True, letters stay upright and read left→right)."""
    f = Font.get(font)
    glyphs, total = f.layout(s, size, tracking)
    k = size / f.upem
    parts = []
    for d, gx, adv in glyphs:
        mid = gx + adv / 2 - total / 2  # arc length from centre
        a = mid / r  # radians
        if not bottom:
            px, py = cx + r * math.sin(a), cy - r * math.cos(a)
            deg = math.degrees(a)
        else:
            px, py = cx + r * math.sin(a), cy + r * math.cos(a)
            deg = -math.degrees(a)
        parts.append(
            f'<g transform="translate({px:.2f},{py:.2f}) rotate({deg:.3f})">'
            f'<path transform="translate({-adv/2:.2f},0) scale({k:.6f},{-k:.6f})" d="{d}"/></g>'
        )
    return f'<g fill="{fill}" {extra}>' + "".join(parts) + "</g>"


def shift_mark(x, y, size, fill=INK, stroke=None, sw=0):
    """The SHIFT mark: the keyboard ⇧ arrow. Box of `size` px, top-left at (x,y)."""
    pts = [(50, 4), (96, 50), (71, 50), (71, 96), (29, 96), (29, 50), (4, 50)]
    d = "M" + " L".join(f"{px/100*size:.2f},{py/100*size:.2f}" for px, py in pts) + " Z"
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="miter"' if stroke else ""
    return f'<path transform="translate({x:.2f},{y:.2f})" d="{d}" fill="{fill}"{st}/>'


def wordmark(x, y, height, fill=INK, mark=True, gap=0.18):
    """Lockup: ⇧ + SHIFT in Anton, sized by cap height, centred at x, baseline y."""
    f = Font.get("Anton")
    size = height / (f.cap_height(1.0))
    w = f.width("SHIFT", size, tracking=-0.01)
    mw = height * 0.95
    total = w + (mw + gap * height if mark else 0)
    left = x - total / 2
    out = []
    if mark:
        out.append(shift_mark(left, y - height * 0.975, mw, fill))
        left += mw + gap * height
    out.append(text("Anton", "SHIFT", size, left, y, fill, anchor="start", tracking=-0.01))
    return "".join(out)


GRUNGE_FILTER = """
<filter id="grungeF" x="0" y="0" width="1" height="1" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="{bf}" numOctaves="4" seed="{seed}" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0 0 0 0 1" result="g"/>
  <feComponentTransfer in="g" result="t">
    <feFuncR type="linear" slope="{slope}" intercept="{icpt}"/>
    <feFuncG type="linear" slope="{slope}" intercept="{icpt}"/>
    <feFuncB type="linear" slope="{slope}" intercept="{icpt}"/>
  </feComponentTransfer>
</filter>
"""


def grunge_defs(w, h, seed=7, strength="light", bf="0.03"):
    """A luminance mask that eats speckles out of whatever it's applied to.
    strength: light (~8% eaten) | medium (~20%) | heavy (~35%)."""
    slope, icpt = {"light": (14, -4.1), "medium": (14, -4.96), "heavy": (14, -5.66)}[strength]
    return (
        GRUNGE_FILTER.format(seed=seed, bf=bf, slope=slope, icpt=icpt)
        + f'<mask id="grunge" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">'
        f'<rect width="{w}" height="{h}" fill="#fff" filter="url(#grungeF)"/></mask>'
    )


def svg_doc(w, h, body, defs="", bg=None):
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f"<defs>{defs}</defs>{bgr}{body}</svg>"
    )


def render(svg_path, png_path, width=None, bg=None):
    cmd = ["rsvg-convert", svg_path, "-o", png_path]
    if width:
        cmd += ["-w", str(width)]
    if bg:
        cmd += ["-b", bg]
    subprocess.run(cmd, check=True)


def b64png(path):
    with open(path, "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode()
