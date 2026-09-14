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
| Design files | this repo | — | `designs/print/*.png` uploads directly. |

**Why not Shopify + Printful?** It works and it's what most brands use later, but it's two accounts, $5–39/mo, tax setup, and you connect the two. Fourthwall is the same result in one login for a first drop. Switch to Shopify + Printful when you're doing $5k+/month and want more control; the designs move with you.

**Why not screen printing a run?** Because you don't know what sells yet. Drop 001 on print-on-demand tells you which 3 pieces to screen print 50 of for Drop 002 (that's where margins hit 65–70%, see PLAYBOOK.md §1-B).

---

## Step 1 — Fourthwall account (20 min)

1. Go to fourthwall.com → "Start for free" → sign up with the brand email (make `hello@shiftworld.co` or a fresh Gmail `shift.worldwide@gmail.com` — never your personal one).
2. Store name: **SHIFT**. URL: `shift-worldwide.fourthwall.com` (custom domain later).
3. Payouts: connect your bank (they use Stripe). Under 18? A parent's bank works — they're the "owner" on paper.
4. Theme: pick the darkest minimal theme. Upload `brand/avatar.png` as the logo/favicon, `brand/wordmark_white.png` as the header logo.

## Step 2 — Create the 9 products (60 min)

For each product: **Products → Add product → Print on demand → choose blank → Design**.

| Product | Blank on Fourthwall | Front file | Back file | Extra |
|---|---|---|---|---|
| Inner Peace Tee | Comfort Colors 1717 — Black | `10_sun_front_white.png` (12×14 in, center) | `10_neck_back_white.png` (4×2 in, below collar) | sleeve: `sleeve_mark_white.png` 2 in |
| Cherub Tee | Comfort Colors 1717 — Ivory | `11_cherub_front_ink.png` | `11_neck_back_ink.png` | sleeve: `sleeve_mark_ink.png` |
| Guardian Tee | Comfort Colors 1717 — Black | `12_core_chest_white.png` (left chest, 4 in) | `12_wings_back_white.png` (13×16 in) | |
| Overtime Hoodie | Independent IND4000 or Gildan 18500 — Black | `13_hands_front_white.png` (11×12 in, above pocket) | `13_factory_back_white.png` | |
| Caught Up Hoodie | Gildan 18500 — Forest Green | `14_web_front_white.png` | `14_web_back_white.png` | hood: `14_hood_star_white.png` if the blank allows |
| Manual Only Tee | Comfort Colors 1717 — White | `15_skeleton_front_ink.png` | — | |
| Hazard Hoodie | IND4000 — Black | `06_hazard_badge_white.png` (5 in, center chest) | `06_hazard_back_white.png` | |
| Time Card Tee | Comfort Colors 1717 — Black | `05_timecard_chest_white.png` (left chest) | `05_timecard_back_white.png` | |
| Drawn To The Light Tee | Comfort Colors 1717 — Black | `16_core_chest_white.png` (left chest) | `16_moth_back_white.png` | |

Rules when placing: front full prints start ~2.5–3 in below the collar; left chest logos center ~4 in from the center line; back prints start ~3 in below the back collar. The mockups in `mockups/` show the intended placement — match them.

Prices (set these): tees **$45–48**, hoodies **$98**. The blanks cost Fourthwall ~$16 (tee) / ~$32 (hoodie) so you keep ~$28 / ~$62 per sale. Hellstar charges $120 for a tee; you're not there yet, but don't go under $40 — cheap reads as cheap.

Product photos: upload the Gemini shots from `photos/` (model front, model back, flat, detail) — 4 per product. Product description: copy from `docs/index.html` PRODUCTS array.

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
