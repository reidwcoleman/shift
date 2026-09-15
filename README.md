# SHIFT

Bold graphic streetwear brand — *Night Shift Division*. Everything here is generated from code so a design tweak is a one-line change and a rebuild.

- `PLAYBOOK.md` — the business: name/handles, blanks + costs + margins, 30-day pre-launch, drop mechanics.
- `brand/` — logos, ⇧ mark, avatar, palette.
- `designs/src/` — vector print files (all text outlined). Send to screen printers.
- `designs/print/` — 300 DPI transparent PNGs. Upload to Printful / Printify.
- `mockups/` — garment mockups + `lookbook.png`.
- `photos/first_shift/` — product + lookbook photos (Gemini blank garments with the real prints composited on via `tools/composite.py`); `photos/blanks/` are the blanks.
- `art/color/` — multi-color artwork (Gemini on chroma green → `tools/art_color.py` keys it out).
- `docs/` — landing page + waitlist (static; GitHub Pages).

```
python3 -m venv .venv && .venv/bin/pip install pillow fonttools   # once
.venv/bin/python tools/build_designs.py     # ~7 min (grunge filters at 300dpi)
.venv/bin/python tools/build_mockups.py     # ~5 min (add `v3` for the FIRST SHIFT lineup)
.venv/bin/python tools/build_v3.py          # FIRST SHIFT print files (multi-color)
.venv/bin/python tools/composite.py         # product photos from photos/blanks
```
Fonts (Google Fonts, OFL) live in `fonts/` and are only needed at build time.
