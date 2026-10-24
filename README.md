# IMADI Tech Marketing Bot

Posts to IMADI Tech's **Instagram** and **Facebook Page** automatically, in American English. Nothing to copy, paste or upload: the bot designs each post, writes the caption, records the reel voiceover, and publishes it.

## What it posts

| Day | 11 AM | 3 PM | 7 PM |
|---|---|---|---|
| Monday | Carousel | Reel | Post |
| Tuesday | Post | | Carousel |
| Wednesday | Reel | | Post |
| Thursday | Carousel | | Reel |
| Friday | Post | Carousel | Reel |
| Saturday | Post | | |
| Sunday | | | |

Times are Pakistan time. That's 13 posts a week.

- **Warm-up week:** until `WARMUP_UNTIL` in `bot/config.py` (2 Nov 2026), it posts once a day, because the Instagram account was recently restored. After that the full schedule starts on its own.
- **Light and dark:** posts alternate between imadi.tech's light and dark looks, one after the other.
- **Reels:** 20 to 25 seconds, with an American English voiceover that alternates between a female voice (Ava) and a male voice (Andrew). These are Microsoft's free neural voices, so no API key is needed.
- **Real work demos:** every second reel shows a real screen recording of work IMADI Tech built: client projects (ALICO, the UK claims bot and its dashboard, the UK ERP, Company Monitor, ReNaz bot and dashboard) and IMADI's own products (AI Sales Engine, HerCommerce seller and customer sides), inside an IMADI frame, with narration and a WhatsApp call to action. The videos live in `assets/demos/` and use sample data. To add a new demo, drop the MP4 there and add an entry to `DEMOS` in `bot/content.py`.
- **WhatsApp on every post:** every image and reel shows *WhatsApp 0315 3205484*. Facebook captions include a clickable `wa.me` link. Instagram doesn't allow links in captions, so they say "tap the link in our bio".
- **Content:** 14 posts, 10 carousels, 10 talking reels and 10 demo reels in `bot/content.py`, covering lead tips, myth vs fact, how it works, and real client stories (ALICO, the UK logistics claims bot, Company Monitor, ReNaz). With the full schedule nothing repeats for about three weeks. Adding entries to those lists stretches that out.

## One-time setup

You only do this once.

### 1. Make this repository public
Instagram and Facebook download each image and video from a public link. The bot stores them on this repo's `media` branch. No passwords or tokens are ever stored in the code; they go in GitHub Secrets (step 3).

### 2. Get your Meta details
You need three values: a **Page token**, your **Facebook Page ID**, and your **Instagram account ID**.

1. In the Instagram app, switch **imadi.tech** to a **Business** account and link it to the **IMADI Tech** Facebook Page (Settings → Accounts Center, or Edit profile → Page).
2. Go to **developers.facebook.com** → **My Apps** → **Create App**. Name it "IMADI Marketing Bot", choose the **Business** type, and connect it to your business portfolio if asked.
3. Open **Tools → Graph API Explorer**. Choose your app, click **Get User Access Token**, and tick these permissions: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`, `business_management`. Click **Generate Access Token** and approve for the IMADI Tech Page and the imadi.tech Instagram account.
4. Make it long-lived: open **Tools → Access Token Debugger**, paste the token, click **Debug**, then **Extend Access Token**. Copy the new token.
5. Back in Graph API Explorer, paste the long-lived token and run `me/accounts`. Find IMADI Tech in the result:
   - `access_token` → this is your **META_PAGE_TOKEN**. Page tokens made this way don't expire.
   - `id` → this is your **FB_PAGE_ID**.
6. Run `FB_PAGE_ID?fields=instagram_business_account`, using your page id in place of FB_PAGE_ID. The `id` inside `instagram_business_account` is your **IG_USER_ID**.

The app can stay in Development mode. As its admin, you can publish to your own Page and Instagram without Meta's app review.

### 3. Add the secrets
In this repository: **Settings → Secrets and variables → Actions → New repository secret**. Add:

| Name | Value |
|---|---|
| `META_PAGE_TOKEN` | the Page access token |
| `FB_PAGE_ID` | the Facebook Page id |
| `IG_USER_ID` | the Instagram business account id |

### 4. Test it
**Actions → IMADI daily posts → Run workflow.** Tick **Build only** for a first try: it makes the post without publishing, and you can download it under the run's **Artifacts**. Then run it again without the tick to publish a real post.

After that, it runs on schedule by itself.

## If something goes wrong
- GitHub emails you when a run fails. Open the run in **Actions** to see the reason.
- If one platform fails, the other still posts.
- To pause Instagram or Facebook, set `POST_TO_INSTAGRAM` or `POST_TO_FACEBOOK` to `False` in `bot/config.py`.
- To pause everything: **Actions → IMADI daily posts → ⋯ → Disable workflow**.

## Changing things
Everything is in `bot/config.py` (schedule, times, voices, WhatsApp number) and `bot/content.py` (what the posts say). If you change a posting time, change the matching `cron` line in `.github/workflows/post.yml` too; those are in UTC (Pakistan time minus 5 hours).

Test locally without posting:

```bash
pip install -r requirements.txt && python -m playwright install chromium
python -m bot.main --dry-run --format carousel --theme light
FAKE_TTS=1 python -m bot.main --dry-run --format reel --demo 0   # client demo reel, silent voice
```

## Credits
Typeface: Inter by Rasmus Andersson and the Inter Project Authors, SIL Open Font License 1.1 (`assets/fonts/OFL.txt`).
