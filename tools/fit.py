"""Garment-aware print placement (v2).

Finds the shirt in a photo, measures the torso (collar line, chest width, lean), and places the
print exactly where the printer puts it: centred on the torso, top edge N inches below the collar,
scaled from the real garment width. The print is perspective-warped to the torso, displaced by the
fabric folds, multiplied into the cloth and given the garment's own weave/grain so it reads as ink
on cotton instead of a sticker.

    from fit import fit_print
    fit_print(img, "31_racing_front", seed=(x, y), kind="light", width_in=12, drop_in=3.0)
"""
import os, math
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PR = os.path.join(ROOT, "designs", "print_worn")


def garment_mask(im, seed, kind, tol=None):
    """Binary mask of the garment containing `seed`: pixels whose chroma matches the cloth around the
    seed (so a cream tee doesn't leak into a bright sky) with a luminance window per kind."""
    ycc = np.asarray(im.convert("YCbCr")).astype(int)
    Y, Cb, Cr = ycc[..., 0], ycc[..., 1], ycc[..., 2]
    sx, sy = seed
    patch = (slice(max(0, sy - 25), sy + 25), slice(max(0, sx - 25), sx + 25))
    y0, cb0, cr0 = np.median(Y[patch]), np.median(Cb[patch]), np.median(Cr[patch])
    chroma = np.hypot(Cb - cb0, Cr - cr0)
    ct = tol or (18 if kind == "red" else 12)
    if kind == "dark":  m = (chroma < ct + 4) & (Y < min(y0 + 80, 150))
    elif kind == "light": m = (chroma < ct) & (Y > max(y0 - 90, 100))
    elif kind == "red":  m = (chroma < ct) & (Y > 40)
    else: m = (chroma < ct) & (abs(Y - y0) < 80)
    raw = Image.fromarray((m * 255).astype("uint8"))
    # close small holes (seams, wrinkles, highlights), then keep only the blob under the seed
    mask = raw.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
    fill = mask.copy(); ImageDraw.floodfill(fill, seed, 128, thresh=0)
    blob = np.asarray(fill) == 128
    if blob.sum() < 500:  # seed missed — fall back to the raw mask
        blob = np.asarray(mask) > 0
    garment_mask.raw = np.asarray(raw) > 0
    return blob


def torso_geometry(blob, seed, ppi_guess):
    """Collar line, torso centre and width at chest height, and edge lines for the warp."""
    sx, sy = seed
    col = blob[:, sx]
    # collar: walk up from seed until we leave the garment
    y = sy
    while y > 0:
        if col[y]: y -= 1; continue
        # a chain / seam / highlight can cut the mask: skip gaps shorter than ~1.5 in
        gap = 0
        while y - gap > 0 and not col[y - gap] and gap < int(ppi_guess * 1.5): gap += 1
        if y - gap > 0 and col[y - gap]: y -= gap
        else: break
    collar = y + 2
    rows = {}
    raw = garment_mask.raw
    lim = int(ppi_guess * 18)
    for yy in range(collar, min(blob.shape[0], collar + int(ppi_guess * 20)), 4):
        if not blob[yy, sx]: continue
        # walk out from the seed column to the first real gap (background/skin) on the un-closed mask
        l = sx
        while l > max(0, sx - lim) and (blob[yy, l - 1] or raw[yy, max(0, l - 14):l].any()): l -= 1
        r = sx
        while r < min(blob.shape[1] - 1, sx + lim) and (blob[yy, r + 1] or raw[yy, r:r + 14].any()): r += 1
        if r - l > ppi_guess * 6: rows[yy] = (l, r)
    return collar, rows


def find_coeffs(src, dst):
    A = []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(A, float); B = np.array([c for p in src for c in p], float)
    return np.linalg.solve(A, B)


def fit_print(base, print_name, seed, kind, width_in=12.0, drop_in=3.0, chest_in=24.0,
              opacity=0.94, curve=0.06, displace=2.5, side="center", chest_offset_in=4.0, collar=None, ppi=None, cx=None):
    """Place designs/print_worn/<print_name>.png on the garment under `seed` in `base` (RGB, modified in place).
    side: center | left (wearer's left chest badge)"""
    W, Hh = base.size
    blob = garment_mask(base, seed, kind)
    ppi0 = 20.0
    collar_auto, rows = torso_geometry(blob, seed, ppi0)
    if collar is None: collar = collar_auto
    else:
        _, rows = torso_geometry(blob, (seed[0], max(collar + 10, seed[1])), ppi0)
        rows = {k: v for k, v in rows.items()} if rows else rows
    if len(rows) < 3: raise RuntimeError(f"garment not found at {seed}")
    ys = sorted(rows)
    def band_measure(ppi_est):
        # torso under the sleeves: the narrower rows between 5 and 11 in below the collar
        sel = [rows[y] for y in ys if collar + 5 * ppi_est <= y <= collar + 11 * ppi_est]
        if len(sel) < 3: sel = [rows[y] for y in ys[len(ys) // 3: 2 * len(ys) // 3]] or [rows[y] for y in ys]
        widths = sorted((r - l, l, r) for l, r in sel)
        keep = widths[: max(2, int(len(widths) * 0.4))]
        w = float(np.median([k[0] for k in keep])); c = float(np.median([(k[1] + k[2]) / 2 for k in keep]))
        return w, c
    w, cx_m = band_measure(ppi0)
    ppi_m = w / chest_in
    w, cx_m = band_measure(ppi_m)
    ppi = ppi or w / chest_in
    cx = cx if cx is not None else cx_m
    def width_at(yy):
        k = min(ys, key=lambda r: abs(r - yy)); l, r = rows[k]; return l, r, (l + r) / 2
    art = Image.open(os.path.join(PR, print_name + ".png")).convert("RGBA")
    pw = width_in * ppi; ph = art.height * pw / art.width
    top = collar + drop_in * ppi
    if side == "left":
        cx = cx + chest_offset_in * ppi  # wearer's left = viewer's right
    # torso edge lines at the print's top and bottom -> perspective quad that follows the lean/taper
    lt, rt, ct = width_at(int(top)); lb, rb, cb = width_at(int(top + ph))
    wt, wb = rt - lt, rb - lb
    ratio = max(0.85, min(1.15, wb / max(wt, 1)))
    # keep the print on the torso axis: blend row centres toward the measured torso centre
    ct = cx * 0.7 + ct * 0.3; cb = cx * 0.7 + cb * 0.3
    if side == "left": ct, cb = ct + chest_offset_in * ppi, cb + chest_offset_in * ppi
    quad = [(ct - pw / 2, top), (ct + pw / 2, top), (cb + pw * ratio / 2, top + ph), (cb - pw * ratio / 2, top + ph)]
    # render the print into a canvas the size of the photo via perspective transform
    x0, y0 = int(min(p[0] for p in quad)) - 4, int(top) - 4
    x1, y1 = int(max(p[0] for p in quad)) + 4, int(top + ph) + 4
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(Hh, y1)
    cw, ch = x1 - x0, y1 - y0
    local = [(px - x0, py - y0) for px, py in quad]
    # cylindrical curve: squeeze the print toward its centre so the edges wrap the body
    aw = int(pw * 1.0); ah = int(ph)
    a = art.resize((aw, ah), Image.LANCZOS)
    xs = np.arange(aw) / max(aw - 1, 1) * 2 - 1
    xw = np.sin(xs * math.pi / 2) * (1 - curve) + xs * curve  # remap 
    src_x = ((xw + 1) / 2 * (aw - 1)).astype(np.float32)
    arr = np.asarray(a).astype(np.float32)
    i0 = np.clip(np.floor(src_x).astype(int), 0, aw - 1); i1 = np.clip(i0 + 1, 0, aw - 1); f = (src_x - i0)[None, :, None]
    arr = arr[:, i0] * (1 - f) + arr[:, i1] * f
    a = Image.fromarray(arr.astype("uint8"), "RGBA")
    coeffs = find_coeffs([(0, 0), (aw, 0), (aw, ah), (0, ah)], local)
    warped = a.transform((cw, ch), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    region = base.crop((x0, y0, x1, y1)).convert("RGB")
    reg = np.asarray(region).astype(np.float32)
    lum = np.asarray(ImageOps.grayscale(region)).astype(np.float32) / 255
    # fold displacement: shift the print by the luminance gradient (folds push the ink around)
    blur = np.asarray(ImageOps.grayscale(region).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    gy, gx = np.gradient(blur)
    wa = np.asarray(warped).astype(np.float32)
    yy, xx = np.mgrid[0:ch, 0:cw]
    sx = np.clip(xx - gx * displace * 40, 0, cw - 1); sy = np.clip(yy - gy * displace * 40, 0, ch - 1)
    ix, iy = sx.astype(int), sy.astype(int)
    wa = wa[iy, ix]
    # shading from the cloth (soft) + weave (high-pass) so the ink sits in the fabric
    soft = np.asarray(ImageOps.grayscale(region).filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
    inside = blob[y0:y1, x0:x1]
    med = np.median(soft[inside]) if inside.any() else max(np.median(soft), 0.05)
    shade = np.clip(soft / max(med, 0.05), 0.35, 1.35)[..., None]
    weave = (lum - soft)[..., None] * 255 * 0.8
    alpha = wa[..., 3:4] / 255 * opacity
    # only paint on the garment (hands, chains, hair stay on top)
    gm = Image.fromarray((inside * 255).astype("uint8")).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.5))
    alpha = alpha * (np.asarray(gm).astype(np.float32) / 255)[..., None]
    ink = np.clip(wa[..., :3] * shade + weave, 0, 255)
    # ink on dark cloth loses a touch of saturation; on light cloth it soaks in slightly
    out = reg * (1 - alpha) + ink * alpha
    base.paste(Image.fromarray(out.astype("uint8"), "RGB"), (x0, y0))
    return dict(collar=collar, ppi=ppi, cx=cx, top=top, pw=pw)
