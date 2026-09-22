# SHIFT — Instagram setup + 30-day launch

Everything you need is in `content/` (18 feed posts, 3 story templates, captions). The only thing I can't do is create the account — Instagram needs a phone number and a face for verification. That's a 5-minute job for you; everything after it is prepared.

## 1. Create the account (you, 5 min)

1. Instagram app → Sign up → use the brand email (`shift.worldwide@gmail.com` or `hello@shiftworld.co`), not your personal.
2. Handle, in this order until one is free: `shift.worldwide` → `shiftworldwide` → `shift.wrld` → `nightshift.division` → `shift.wrldwide`.
3. Name field: **SHIFT** (this is what search matches, keep it clean).
4. Switch to a **Professional → Creator** account (Settings → Account type). This unlocks insights, the native post scheduler, and the "link in bio" button.
5. Profile photo: `brand/avatar.png`.
6. Bio (150 chars):
   ```
   NIGHT SHIFT DIVISION ⇧
   Drop 001 — 10.09 — 11:59 PM
   36 of each. Never restocked.
   ```
   Link: `https://reidwcoleman.github.io/shift/` (swap to shiftworld.co once you own it).
7. Make the same account on TikTok with the same handle and avatar. Post the same Reels there.

Send me the handle when it exists — if you're logged in on Chrome I can upload and schedule the posts for you from `content/`.

## 2. What's in the content pack

| # | File | What it is |
|---|---|---|
| 01 | `day1_desk` | "Day 1" desk shot — the founder post. Pin it. |
| 02 | `teaser_arrow` | ⇧ sprayed on concrete. The mark, no explanation. |
| 03 | `manifesto` | Text post: "Nobody claps for the hours between midnight and five." |
| 04 | `teaser_clock` | The punch clock at 11:59. |
| 05 | `unboxing` | First sample in the mailer. |
| 06 | `rules` | Text post: 36 pieces / 48 hours / never restocked. |
| 07 | `hazard_back` | Hero product shot. |
| 08–17 | product + world shots | One piece per post, alternating with "world" shots (stairwell, gas station, laundromat, rooftop). |
| 18 | `date` | Save-the-date. Post it twice: T-7 and T-1. |
| stories | `story_countdown`, `story_comment`, `story_soldout` | Countdown, "comment SHIFT for the link", and the sold-out screenshot template. |

Captions with hashtags: `content/CAPTIONS.md`. Regenerate or add posts: edit `tools/content.py` and run it.

AI images: every "model" in these is generated (Gemini). That's fine for the first 10 days — but the moment your samples arrive, real footage of real people beats every AI image. Mix them: AI for the world-building shots, phone footage for the product.

## 3. The calendar (30 days to the drop)

Post **1 feed post + 1 Reel + 3 stories per day**. Feed post = from the pack. Reels = filmed on your phone (list below). Stories = behind the scenes + the countdown sticker + polls.

| Days | Feed (from pack) | Reels to film (15–30 s, text hook in the first second) |
|---|---|---|
| 1–3 | 01, 02, 03 | "Starting a clothing brand with $200 — day 1" · screen-record the design files · night B-roll + voiceover of the story |
| 4–7 | 04, 05, 06, 07 | unboxing the sample · "the back print nobody expected" · print close-up · "why every piece says 11:59" |
| 8–14 | 08–13 | try-on at night · "36 of each, here's why" · outfit with each piece · reply-to-comment videos |
| 15–21 | 14–17 | creator seeding arrives (their videos) · "the story behind the ⇧" · "how the drop works in 20 seconds" |
| 22–29 | 18 (twice), reposts | countdown daily · "which one are you getting" poll · sizing video · "the list closes tomorrow" |
| 30 | live at 11:59 PM | go live opening the store · post the sold-out story the second a size is gone |

Best posting times for 16–25 guys in the US: 7–9 PM and 11 PM–12 AM local. Schedule everything in-app: create post → Advanced settings → Schedule (up to 75 days out).

## 4. The DM machine

- Set up **ManyChat** (free tier) → connect Instagram → "Comment SHIFT" automation → auto-DM: `You're early. Here's the list: <link>`. This turns every Reel into an email capture.
- Reply to every comment for the first 30 days. Every DM too. The algorithm rewards it and so do buyers.
- DM 20 micro-creators (5–30k followers, guys 16–25: gym, cars, skate, gaming, streetwear pages). Script:
  > yo — starting a brand called SHIFT, night-shift energy, 36 of each piece. want to send you a hoodie before the drop, no strings. what size?
  3–5 will say yes. Their posts are your launch-day content.

## 5. What good looks like

- Day 30: 500–2,000 followers, 150–400 on the list. That's a normal, healthy first drop from zero.
- The feed should look like one world: black / bone / one red hit, night, flash. Delete anything that doesn't fit. No memes, no discount codes, no "link in bio" graphics with arrows.
- Every 5th post is you talking to camera. People buy from a person.

## 6. Automation later

Once the account is a Creator/Business account and linked to a Facebook Page, the Instagram Graph API can publish photos from a script (`tools/`) — worth it at Drop 002 when you have 100+ posts to schedule. Not worth it for the first 30 days; the in-app scheduler does the job.

## Status 2026-09-21

- Account: **@shift_clothing405** (Creator account). Name "Reid Coleman" (Reid keeps it; name changes are limited to 2 per 14 days and both are used up until ~10-05). Bio (Reid approved 2026-09-21): "For the hours nobody sees. ⇧ / FIRST SHIFT · 10.09 · 11:59 PM ET / 15 pieces. 36 of each. Never restocked. / reidwcoleman.github.io/shift". 12 posts, latest = carousel 10 (League + Twin Tigers, Gemini-placed prints).
- Web limitations: no post scheduling, no stories, no pinning, no bio-link editing (all mobile-app only). Reid: open the app once to (1) set the website link to the site, (2) pin post 10 + the Burnout carousel, (3) rename the handle to `shift.worldwide`/`shiftworldwide` if free.
- Old posts 02 (Hazard), 07 (Night Owl), 08 (Burnout/Chrome), 09 (No Sleep) still show the low/small back prints — repost them from the regenerated carousels once the Gemini pass is done (delete old → post new; needs Reid's OK since it deletes posts).
