# SHIFT — Launch Playbook

Brand: **SHIFT** (handle form: **SHIFT WORLDWIDE**, sub-line: *Night Shift Division*)
Lane: bold graphic streetwear · Guys 16–25 · Drop model (no restocks)
Story: *"Nobody claps for the hours between midnight and 5. That's the shift."*
Mark: the ⇧ shift-key arrow. Palette: Ink `#0B0B0B` · Bone `#EDE6D6` · Signal `#FF3B1F` · Concrete `#9A9A93`.

Everything below is the order to do it in. Each step has the number attached.

---

## 0. Lock the name (this week, ~$40)

1. **Domain** — buy `shiftworld.co` (free as of 2026-09-13). Backups that were also free: `shiftwrldwide.com`, `nightshiftworld.com`, `shiftgang.com`. `shift.com/.world/.clothing` are all taken.
2. **Handles** — try in this order: `@shift.worldwide`, `@shiftworldwide`, `@shift.wrld`, `@nightshift.division`. Grab the same one on IG + TikTok + YouTube in the same sitting.
3. **Trademark sanity check** — "SHIFT" is a dictionary word, so there will be existing marks. Search [USPTO TESS](https://tmsearch.uspto.gov) for "SHIFT" in Class 025 (clothing). You can *use* the name at launch; you'd only file (~$350) once it's selling. If a clothing brand already owns "SHIFT" outright, the fallback is filing as **SHIFT WORLDWIDE** — the logo and lockups already use it.
4. **LLC** — not needed for drop 1. Do it after the first $5k (LegalZoom/your state site, ~$100–300).

## 1. What you're actually selling (FIRST SHIFT)

Modeled on how 404 Culture builds a range (varsity tee, tigers tee, money cross, sundial, thermals, mesh + sweat shorts, beanie) — same categories, heavier garments, real illustration, real photos.

| # | Piece | Blank | Sell | Landed cost* | Margin |
|---|-------|-------|------|--------------|--------|
| 1 | League Ringer Tee (red/gold) | ringer tee, 3-color print | $48 | ~$16 | 67% |
| 2 | Twin Tigers Tee (natural) | Comfort Colors 1717 | $48 | ~$15 | 69% |
| 3 | Time Is Money Tee (black) | same | $48 | ~$15 | 69% |
| 4 | Sundial Tee (bone) | same | $48 | ~$14 | 71% |
| 5 | Emblem Tee (black, back print) | same | $48 | ~$16 | 67% |
| 6 | Overtime Thermal (black waffle) | thermal long sleeve | $58 | ~$22 | 62% |
| 7 | Never Ends Thermal (cream) | same | $58 | ~$22 | 62% |
| 8 | Division Mesh Shorts | mesh shorts | $44 | ~$17 | 61% |
| 9 | Athletic Dept Shorts (grey fleece) | fleece shorts | $52 | ~$20 | 62% |
| 10 | Wordmark Beanie | cuffed knit, embroidered | $32 | ~$11 | 66% |
| 11 | Hazard Hoodie | IND4000 / Gildan 18500 | $98 | ~$31 | 68% |

\*Landed = blank + print + mailer + tag at print-on-demand or a 36–50 piece run. Files: `designs/print/` (raster, 300 DPI) and `designs/src/` (SVG with embedded art + outlined type).

### Two ways to make them

**A. Print-on-demand first (zero cash, lower margin) — recommended for drop 1 if you have < $1,000.**
- Printful or Printify → connect to Shopify. Upload the PNGs. Use **Comfort Colors 1717** for tees and **Gildan 18500 / Independent IND4000** for hoodies (the heavyweight options they stock).
- Cost: tee ~$18–22 shipped, hoodie ~$34–40. You net ~$20/tee, ~$45/hoodie. No inventory, no packing, no risk.
- Downside: DTG prints look slightly flatter than screen print. Fine at this stage. Nobody returns a $45 tee because of ink density.

**B. Screen print a small run (needs ~$1,500 cash, real margins, real quality).**
- 36 tees (12 each of 3 designs) + 12 hoodies is the typical minimum.
- Local screen printer (search "screen printing + your city", ask for a quote with "Shaka Wear blanks, 2-color front + back, 36 pcs"). Or online: **Printful's screen-print service** / **Rushordertees** / **Underground Printing**.
- Send them the `designs/src/*.svg` files (they'll ask for "vector with outlined text" — that's exactly what these are).
- Order 20 poly mailers + custom hang tags from Sticker Mule / Vistaprint (~$60). Put the ⇧ on the tag.

Start with A. Switch to B for Drop 002 once you know which pieces sell.

## 2. Storefront

- `docs/` is a finished landing + waitlist page. Deploy it on GitHub Pages (already set up) or drop it into Shopify as the "coming soon" page.
- To collect emails: make a free form at formspree.io, paste the ID into `FORM_ENDPOINT` in `docs/index.html`. Set `DROP_AT` to your drop date.
- When you're ready to take money: **Shopify Starter ($5/mo)** + Printful. Put each product's Shopify URL in the `PRODUCTS` array `url` field and the "NOTIFY ME" buttons become "BUY" buttons.
- Use the mockups in `mockups/` as product images until you have real photos. **Real photos of real people wearing it beat everything** — see §4.

## 3. The 30-day pre-launch (this is where the money is made)

Everything the videos said matters: the feed has to look like a *world* before you sell anything. You are documenting, not advertising.

**Week 1 — Build the world (no product shots yet)**
- Post the avatar (`brand/avatar.png`), bio: `NIGHT SHIFT DIVISION · DROP 001 — 10.09 · 11:59 PM`. Link → your site.
- Day 1–7: one Reel/day. Formats that work for brands like this:
  - "Starting a clothing brand with $0 — day 1" (talk to camera, show the designs on screen)
  - Screen-record the design files (people love watching the vector)
  - Night-time B-roll: streetlights, a clock at 11:59, laptop light — with a voiceover of the story
  - "POV: you're on the night shift" trend audio
- Story every day. Polls: "which one drops first?"

**Week 2 — Show the pieces**
- Get 2 samples in hand (order 1 tee + 1 hoodie from Printful, ~$60). This is non-negotiable — you need real footage.
- Reels: unboxing the sample; wearing it at night; "the back print nobody expected"; close-ups on the print.
- Start the waitlist push: "the list gets the link 1 hour early. Sizes go in the first hour."
- DM 20 micro-creators (5–30k followers, guys 16–25, your city or your niche: gym, cars, skate, gaming). Offer a free piece for a post. 3–5 will say yes. That's your launch content.

**Week 3 — Pressure**
- Reveal one piece per day. Hazard Hoodie last (it's the hero).
- Reels: "why every piece says 11:59" · "the story behind the ⇧" · "we made 36. that's it."
- Story countdown sticker every day.
- Set up **ManyChat** (free tier): comment "SHIFT" → auto-DM the waitlist link. This is how brands get 500 emails from one Reel.

**Week 4 — Drop**
- T-48h: creators post. T-24h: "tomorrow 11:59." T-1h: email the list with the link.
- Go live on IG at 11:59 PM for the drop. Sell out one size on purpose (make fewer XL, for example) and screenshot it. "Sold out in 40 minutes" is your first ad.
- 48 hours later, close it. Post "Drop 001 closed. Thank you." Never restock.

**Posting rules**
- 1 Reel/day minimum. 3 is the real number for growth. Never a day off in the 30 days.
- Hooks in the first second: text on screen, not a logo intro.
- Every 5th post is you talking to camera. People buy from a person.
- No "link in bio" graphics. No discount codes. Scarcity is the discount.

## 4. Content you need on hand before Day 1

- 20+ clips of you / friends wearing the samples at night (phone, 4K, 30fps is fine; shoot vertical)
- 6 clean flat-lay shots on the floor of a garage/parking lot (concrete + the bone hoodie = the aesthetic)
- The lookbook (`mockups/lookbook.png`) for the site + pinned post
- 3 talk-to-camera videos: the story, the name, "why 36 pieces"

## 5. Money (first drop, print-on-demand)

- Site: $0 · Domain: $12 · Samples: $60 · Creator seeding (5 pieces): ~$110 · Hang tags/stickers: $40 · ManyChat: $0 · **Total ≈ $220**
- If 200 people are on the list and 15% buy at an average $55 → 30 orders → **$1,650 revenue, ~$800 profit**.
- Realistic first drop for an account started from 0 with daily posting: 10–40 orders. 100+ happens when a creator post lands.
- Reinvest everything into Drop 002 as a screen-printed run (§1-B) — that's where margins go to 65–70%.

## 6. After Drop 001

- Email everyone who bought: "you were there." Ask for a photo. Repost every single one.
- Drop 002 in 6 weeks. Same rules. Add 1 new piece type (crewneck or shorts) and keep the two best sellers as new colorways.
- Once you hit ~$3k/drop: register the LLC, file the trademark, open Meta ads at $20/day retargeting site visitors only.

## Files

```
brand/        logos (svg+png), avatar, palette
designs/src/  vector print files, text outlined — send these to printers
designs/print/ 300 DPI transparent PNGs — upload these to Printful/Printify
mockups/      product mockups + lookbook.png
docs/         landing page + waitlist (GitHub Pages ready)
tools/        build_designs.py / build_mockups.py — regenerate everything after edits
```

Rebuild after changing a design: `.venv/bin/python tools/build_designs.py && .venv/bin/python tools/build_mockups.py`
