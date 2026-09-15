# SHIFT — Business Setup (the "how do I actually sell this" doc)

The goal: sell real hoodies and tees, get paid, ship nothing yourself, spend as close to $0 as possible until orders exist.
Everything below is in order. Total time to be live: one evening.

---

## The stack (decided)

| Job | Tool | Cost | Why |
|---|---|---|---|
| Store + checkout + payouts + printing + shipping | **Fourthwall** (fourthwall.com) | $0/mo, ~3% + product cost | Built for creator brands. One signup gives you the store, Stripe/PayPal payouts, print-on-demand blanks (Comfort Colors 1717, Gildan/Independent hoodies), fulfillment, customer support and a "drop" mode. No inventory, no shipping, no sales-tax headaches (they collect and remit). |
| Landing page + waitlist | `docs/` (this repo, GitHub Pages) | $0 | Already live at reidwcoleman.github.io/shift. Link every "BUY" button to Fourthwall product pages. |
| Domain | shiftworld.co (Namecheap/Porkbun) | ~$12/yr | Point it at the landing page; Fourthwall gets `shop.shiftworld.co`. |
| Email list | Fourthwall's built-in "email signups" or Formspree → Mailchimp | $0 | Fourthwall lets you email your customers directly for drops. |
| Instagram / TikTok | Professional (Creator) account | $0 | Native scheduler (75 days ahead), insights, link in bio. See `INSTAGRAM.md`. |
| Design files | this repo | — | `designs/print_worn/*.png` (worn, EST. 2002) uploads directly; `designs/upload_worn/` are the <10 MB copies for Fourthwall. |

**Why not Shopify + Printful?** It works and it's what most brands use later, but it's two accounts, $5–39/mo, tax setup, and you connect the two. Fourthwall is the same result in one login for a first drop. Switch to Shopify + Printful when you're doing $5k+/month and want more control; the designs move with you.

**Why not screen printing a run?** Because you don't know what sells yet. Drop 001 on print-on-demand tells you which 3 pieces to screen print 50 of for Drop 002 (that's where margins hit 65–70%, see PLAYBOOK.md §1-B).

---

## Status (2026-09-15, later)

- **Three more hoodies, not yet on Fourthwall:** Burnout (`34_burnout_front` 11 in chest at y=2 + `34_burnout_back` 13×16), Chrome (`35_chrome_front` 11 in chest + `35_chrome_back` 13×16), No Sleep (`36_nosleep_front` 3.5 in left chest x=9.25 y=0.6 + `36_nosleep_back` 13×16). Blank: the same black hoodie as Hazard (Independent / Gildan 18500). Price **$108**. Handles the site links to: `burnout-hoodie`, `chrome-hoodie`, `no-sleep-hoodie`.
- Carousels 08 (Burnout + Chrome) and 09 (No Sleep) built with captions.
- **Blocked on logins:** the Windows Chrome that had Fourthwall + Instagram signed in is a different profile now (both logged out) and the Mac Chrome is logged into neither. Log into both in whichever Chrome has the Claude extension and everything above gets pushed in one pass.

## Status (2026-09-15)

- **New this round (not yet on Fourthwall — needs you logged in on the Windows Chrome):** Shift Racing Tee (`31_racing_front`, Comfort Colors 1717 Ivory, 12×14 in, y=1), Graveyard Shift Tee (`32_graveyard_front`, 1717 Black, 12×14 in, y=1), and the **Night Owl Hoodie** replaces the Hazard design on the hoodie product (`33_owl_chest` 3.5 in at x=9.25 y=0.6 on Front, `33_owl_back` 13×16 on Back). Files in `designs/upload_worn/`. Fourthwall slugs the site already links to: `shift-racing-tee`, `graveyard-shift-tee`, `night-owl-hoodie` — set the product URL handles to match when creating them.
- Instagram carousels 06 (Racing + Graveyard) and 07 (Night Owl) are built in `content/carousels/` with captions; 04 and 05 still queued behind the human-verification wall.

## Status (2026-09-14, evening)

- Fourthwall store: **https://shift-clothing-shop.fourthwall.com** (admin: admin.fourthwall.com/store/shift-clothing). 9 products, all carrying the **worn / EST. 2002** print files from `designs/print_worn` (or the <10 MB `designs/upload_worn` copies): League Tee, Twin Tigers Tee, Time Is Money Tee, Sundial Tee, Emblem Tee (3.5 in chest + full back), Overtime Long Sleeve, Never Ends Long Sleeve, Athletic Dept Shorts, Hazard Hoodie (new diamond badge + beacon back). The Wordmark Beanie is gone (deleted, not coming back).
- Storefront theme switched to the dark "Creator" layout; hero says **FIRST SHIFT. EST. 2002.** with `photos/first_shift/league_lean.jpg` + `cross_squat.jpg`.
- **The store is set to "Coming soon"** (Site design → status pill top-right). Visitors see a holding page, so the BUY buttons on the landing page dead-end until you flip it to **Live** (or "Coming soon + Allow early access with password" for the drop-night mechanic in Step 5). Your call — it takes one click.
- Not on Fourthwall (no matching blank): Division Mesh Shorts, the red/gold ringer (League Tee is on Comfort Colors 1717 Red), waffle thermals (long sleeves are Comfort Colors 6014). Screen printer, Drop 002.
- Instagram **@shift_clothing405**: 5 posts up — day-1 desk, League hero, and carousels 01 (League), 02 (Hazard), 03 (Time Is Money + Emblem). After post 03 Instagram showed a **"Confirm you're human"** check on the Windows Chrome — click Continue there yourself, then carousels 04 (Tigers + Sundial) and 05 (long sleeves) are ready in `content/carousels/` with captions in `CAPTIONS.md`. One per day from here.
- Still yours: rename the handle to `shift.worldwide`, display name → SHIFT (Settings → Edit profile), connect Fourthwall payouts, order samples.

## Step 1 — Fourthwall account (20 min)

1. Go to fourthwall.com → "Start for free" → sign up with the brand email (make `hello@shiftworld.co` or a fresh Gmail `shift.worldwide@gmail.com` — never your personal one).
2. Store name: **SHIFT**. URL: `shift-worldwide.fourthwall.com` (custom domain later).
3. Payouts: connect your bank (they use Stripe). Under 18? A parent's bank works — they're the "owner" on paper.
4. Theme: pick the darkest minimal theme. Upload `brand/avatar.png` as the logo/favicon, `brand/wordmark_white.png` as the header logo.

## Step 2 — Create the 15 products (90 min)

For each product: **Products → Add product → Print on demand → choose blank → Design**. Multi-color prints (`designs/print/2x_*.png`) are full-color rasters — perfect for DTG/print-on-demand; a screen printer will separate the colors themselves.

| Product | Blank on Fourthwall | File | Placement |
|---|---|---|---|
| League Ringer Tee | Ringer tee — Red/Gold (Fourthwall: "Ringer T-Shirt") | `20_league_front.png` | 12×14 in, center, 2.5 in below collar |
| Shift Racing Tee | Comfort Colors 1717 — Ivory | `31_racing_front.png` | 12×14 in center |
| Graveyard Shift Tee | Comfort Colors 1717 — Black | `32_graveyard_front.png` | 12×14 in center |
| Twin Tigers Tee | Comfort Colors 1717 — Ivory | `21_tigers_front.png` | 12×14 in center |
| Time Is Money Tee | Comfort Colors 1717 — Black | `22_cross_front.png` | 12×14 in center |
| Sundial Tee | Comfort Colors 1717 — Ivory | `23_sundial_front.png` | 12×14 in center |
| Emblem Tee | Comfort Colors 1717 — Black | `29_emblem_chest.png` (4 in left chest) + `29_emblem_back.png` (13×16 in back) | |
| Overtime Thermal | Waffle/thermal long sleeve — Black | `24_thermal_front.png` | 11×8 in, center chest |
| Never Ends Thermal | Waffle/thermal long sleeve — Natural | `25_collage_front.png` | 12×14 in center |
| Division Mesh Shorts | Mesh shorts — Black | `26_mesh_left.png` (wearer's left leg) + `26_mesh_right.png` (right leg) | 4 in each |
| Athletic Dept Shorts | Fleece sweat shorts — Heather Grey | `27_sweat_left.png` | 5 in, left leg |
| Night Owl Hoodie | Independent IND4000 / Gildan 18500 — Black | `33_owl_chest.png` (3.5 in left chest) + `33_owl_back.png` (13×16 in) | |
| Burnout Hoodie | same — Black | `34_burnout_front.png` (11 in chest) + `34_burnout_back.png` (13×16 in) | |
| Chrome Hoodie | same — Black | `35_chrome_front.png` (11 in chest) + `35_chrome_back.png` (13×16 in) | |
| No Sleep Hoodie | same — Black (washed if offered) | `36_nosleep_front.png` (3.5 in left chest) + `36_nosleep_back.png` (13×16 in) | |

Rules when placing: front full prints start ~2.5–3 in below the collar; left chest logos center ~4 in from the center line; back prints start ~3 in below the back collar. The mockups in `mockups/` show the intended placement — match them.

Prices (set these): tees **$48**, thermals **$58**, mesh shorts **$44**, sweat shorts **$52**, Night Owl / Hazard hoodie **$98**, Burnout / Chrome / No Sleep hoodies **$108**. 404 Culture sells the same categories at $36–44 with amateur photos; you're a step above on garment, art and photography, so hold the line — don't go under $40 on a tee.

Product photos: upload from `photos/first_shift/` — `<product>_flat.jpg` (white background, first image) and `<product>_model.jpg`, plus the `group_*.jpg` lifestyle shots. Product description: copy from `docs/index.html` PRODUCTS array.

## Step 3 — Order your own samples (do this the same night)

Buy one Inner Peace Tee and one Hazard Hoodie at cost from your own store (Fourthwall lets you order at production cost). ~$50 total, arrives in ~7 days. You need them for:
- checking print quality and placement before the drop
- every video you post for the next 30 days
- knowing the sizing so you can answer DMs

## Step 4 — Wire the landing page

In `docs/index.html`:
- `DROP_AT` → your drop date (a Thursday or Friday, 11:59 PM).
- `FORM_ENDPOINT` → your Formspree form ID (formspree.io → new form → copy the URL). Or replace the form with Fourthwall's email signup embed.
- each product's `url` → the Fourthwall product URL. The "NOTIFY ME" buttons turn into "BUY".
- push to GitHub (`git add -A && git commit -m "drop 001 live" && git push`) — the site updates in ~1 minute.

Custom domain: in Namecheap/Porkbun DNS, add a CNAME `www → reidwcoleman.github.io` and A records for the apex (185.199.108.153 / .109 / .110 / .111), then in GitHub → repo Settings → Pages → Custom domain → `shiftworld.co`. Fourthwall: Settings → Domain → `shop.shiftworld.co` (they give you a CNAME).

## Step 5 — Drop mechanics on Fourthwall

- Set every product to **"Available until [date]"** — 48 hours after the drop opens. Real deadline, real scarcity.
- Turn on **"Email me when back in stock"** off — you never restock; that's the whole point.
- Make the store password-protected until 11:59 PM drop night; send the password to the waitlist 1 hour early. (Settings → Password protection.)
- Add a free sticker to every order (Fourthwall "free gift" or ask them to include a pack-in). Print `brand/mark_signal.png` as 2 in die-cut stickers at Sticker Mule (~$40/100).

## Step 6 — Legal & money (short version)

- **Nothing to register for drop 1.** You can sell as an individual; Fourthwall reports income to you (1099 if > $600). Save 25% of profit for taxes.
- After the first ~$5k: form an LLC in your state (~$100–300 online), open a business bank account, move Fourthwall payouts there.
- **Trademark**: search tmsearch.uspto.gov for "SHIFT" class 025 now (10 minutes). If a clothing brand owns it outright, file as **SHIFT WORLDWIDE** (which the logos already use). File once money is coming in (~$350 DIY).
- **Copyright of the artwork**: the illustrations were AI-generated and then hand-finished into vectors; the logo, wordmark, and layouts are yours. Nobody is going to fight you over a tee, but don't use any other brand's characters/logos, ever.
- Returns: Fourthwall handles misprints/damage. Set your policy as "final sale, exchanges for misprints only" — standard for drops.

## Step 7 — Ship the first 48 hours

- Reply to every order with a DM/thank you (Fourthwall shows you the customer). Ask for a photo when it arrives.
- Screenshot "SOLD OUT" the moment a size sells out. That screenshot is your best ad.
- After 48 h, close it. Post the wrap-up. Start Drop 002 the next morning with the 3 best sellers screen-printed (PLAYBOOK §1-B).

---

## If you'd rather I do the clicking

Once you've created the Fourthwall (or Printful/Printify) account and are logged in in Chrome, say so — I can drive the browser: create the products, upload the print files at the right sizes, set prices, and paste in the photos and copy. Same for the Instagram profile once the account exists.
