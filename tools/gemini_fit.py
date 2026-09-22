"""Print placement via Gemini: hand the image model the blank-garment photo + the real print file and ask
for the print where a screen printer would put it (standard placements below). Exact-fidelity prompt.

    .venv/bin/python tools/gemini_fit.py OUT.png BLANK.png PRINT.png "<garment>" <placement> [aspect] [model]
"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
import gemini_img

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLACEMENTS = {
    "front":       "a full front-chest print, centred left-to-right on the body, its top edge 3 inches below the collar seam, 12 inches wide (a little over half the chest width)",
    "front_hoodie":"a front-chest print on the hoodie, centred left-to-right, its top edge 2.5 inches below the neckline / hood seam, 11 inches wide, sitting entirely above the kangaroo pocket and below the drawstrings",
    "left_chest":  "a small left-chest print (the wearer's left, so the viewer's right), 3.5 inches wide, its top edge 3 inches below the collar seam and its centre about 4 inches to the side of the centre line — where a polo logo sits",
    "back":        "a full back print, centred between the shoulder blades, its top edge 3 inches below the collar seam, 13 inches wide",
    "back_hoodie": "a full back print on the hoodie, centred between the shoulder blades, its top edge 3 inches below the hood seam (directly under the hood), 13 inches wide, ending above the waistband",
    "left_leg":    "a small print on the wearer's left leg of the shorts, 4 inches wide, centred on the thigh just above the hem",
    "both_legs":   "one small print on each leg of the shorts, 4 inches wide, centred on each thigh above the hem",
}

FIDELITY = ("Reproduce the print artwork from the second image EXACTLY: same artwork, same words, same spelling, same layout, same colours, "
            "same proportions, nothing added or removed. Do not invent extra text, tags, logos or labels anywhere on the garment or in the scene. "
            "Keep the photo otherwise identical to the first image: same person, pose, garment, garment colour, lighting, background, framing and crop. "
            "The print should look screen-printed into the fabric — soft matte ink that follows the folds, slightly worn — not a flat sticker.")


def shrink(path, max_px=1400):
    im = Image.open(path).convert("RGBA")
    if max(im.size) > max_px:
        im.thumbnail((max_px, max_px), Image.LANCZOS)
    # prints on a neutral background so the model reads the edges
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255)); bg.alpha_composite(im)
    f = tempfile.NamedTemporaryFile(suffix=".png", delete=False); bg.convert("RGB").save(f.name); return f.name


def fit(out, blank, print_png, garment, placement, aspect="1:1", model="gemini-3-pro-image-preview", extra=""):
    if os.path.exists(out): return out
    prompt = (f"The first image is a photo of a blank {garment}. The second image is the print file. "
              f"Produce the same photo with the print applied as {PLACEMENTS[placement]}. {FIDELITY} {extra}")
    b = shrink(blank, 1600); p = shrink(print_png, 1400)
    try:
        gemini_img.generate(prompt, [b, p], model=model, aspect=aspect, out=out)
    finally:
        os.unlink(b); os.unlink(p)
    return out


if __name__ == "__main__":
    out, blank, pr, garment, placement = sys.argv[1:6]
    aspect = sys.argv[6] if len(sys.argv) > 6 else "1:1"
    model = sys.argv[7] if len(sys.argv) > 7 else "gemini-3-pro-image-preview"
    fit(out, blank, pr, garment, placement, aspect, model); print("wrote", out)
